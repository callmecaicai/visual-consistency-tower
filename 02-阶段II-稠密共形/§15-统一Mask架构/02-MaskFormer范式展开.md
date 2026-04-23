> 编者说明：本页保存的是“MaskFormer / Mask2Former 深推导 + 跨阶段外溢判断”的合并稿。阅读时可先看导前，再进入 §1–§5 的机制展开；这样既能看清本页的技术内核，也能看清它为什么会成为阶段 II 向后几层的接口转折。

# 导前 · object query 的跨阶段意义

回到你的谱系语言：

**阶段 II** 的核心是"**稠密穿透**"——从整图分类穿透到每像素。这个阶段结束时留下的**唯一本体论原语**就是 object query。

**阶段 III（语言共形）** 的一条关键接口线**确实建在 object query 上**：

- 3D 重建的 NeRF / Gaussian splatting 也用 query 做视角条件
- 视频理解的 tracking query、action query
- 跨模态对齐的 text-image cross-attention 就是 query 机制

**阶段 IV（生成共形）**：

- Diffusion 的 class-conditional / text-conditional 生成 = query 注入机制
- Classifier-free guidance = 在 query 空间做插值
- ControlNet / T2I-Adapter = prompt token 额外注入

**阶段 V（表征共形）**：

- CLIP 的对齐 = text 作为 query / image 作为 key-value
- SAM 的 "Segment Anything" = 任意 prompt 作为 query
- LLaVA / GPT-4V 的 visual token = ViT 输出 projected 成 LLM 的 "query-side" 输入

**在阶段 II 出现的 object query，实质上是后面所有阶段的"接口母版"**。别的东西（FPN、RoIAlign、anchor）都是具体任务的组件，只有 object query 是**跨任务、跨模态、跨阶段**的架构原语。

这就是为什么我说 DETR 在检测里的命运（被 YOLO 吞掉）**不重要**——DETR 这四代真正留下的是**把 object query 从一个检测 trick 提炼成 transformer 时代通用接口**这件事。之后的每一个基础模型，都在用这个接口。

---

从编排上看，这段导前判断更适合作为**阶段 II → 阶段 III 的桥梁说明**，即便保留在本页，也应被理解为后续几页的总接口说明，而不是待定的编辑分支。它的作用，是先把 object query 的外溢意义钉住，再回到 MaskFormer / Mask2Former 的具体机制。

下面按和 DETR 展开同样的密度，把 MaskFormer / Mask2Former 打穿。核心要回答三个问题：**为什么"逐像素分类"是错的? mask classification 凭什么更根本? Mask2Former 的三个改进各自在修什么?**

---

# 先定义问题：分割这个任务的"错位"在哪

## 0.1 三种分割任务的表面区别

| 任务 | 输出 | 传统做法 |
| --- | --- | --- |
| **语义分割** | 每个像素属于哪类（"天空/道路/狗"） | FCN: per-pixel softmax over C 类 |
| **实例分割** | 每个对象的 mask + 类别 | Mask R-CNN: detect + RoI mask |
| **全景分割** | 每个像素 (class_id, instance_id) | Panoptic FPN: 两个 branch 合并 |

**表面看**：三个任务要的东西不一样——一个要密集标签，一个要对象 mask，一个要两者合并。

**底层看**：它们要的是**同一个东西**——**把图片分成若干块 + 每块贴一个标签**。区别只是：

- 语义分割：块和"类别"一对一（同类的不同区域合并成一块）
- 实例分割：块和"对象"一对一（同类不同对象是不同块）
- 全景分割：两者混合

**传统架构分歧的根因不是任务本身不同，而是输出格式硬编码了三种不同的解法**。

## 0.2 逐像素分类为什么是"错位的"

FCN / DeepLab / PSPNet 的范式：

```
每个像素输出 C 个 logits → softmax → argmax 分类
```

这里**每个像素都要在 C 个类别之间做一次独立选择**。问题：

**问题一:  "同属一个对象"的信息被架构抛弃**

- FCN 里两个相邻像素"是否属于同一对象"这个事实**从来没有被模型利用**
- 模型只学"每个位置是啥类"，不学"哪些位置是一起的"
- 实例信息在语义分割架构里**根本没地方放**

**问题二: 类别数爆炸时不 scale**

- C=150 (ADE20K) 还行
- C=1000、C=∞（开放词汇）时，最后一层的 softmax 变得极其笨重
- **分类的复杂度和类别数线性相关**——这是硬天花板

**问题三: "逐像素独立"是个假的前提**

- 相邻像素几乎必然同类（空间一致性），但 softmax 看不见这个
- 要靠 CRF / dense prediction head 事后补
- **模型的归纳偏置和任务的结构不一致**

所以逐像素分类的问题不是"精度不够"，是**范式和任务的真实结构错位**。

---

# §1 · MaskFormer —— 一次看似简单、实际极深的范式切换

## 1.1 关键洞察

Cheng 等人的原始动机来自一个观察：

> **DETR 已经证明"k 个 query + 每个 query 出一个对象"在检测上比 per-pixel dense prediction 更好。分割为什么不能这样做？**
> 

具体形式化：

**传统（per-pixel classification）**：

$$

P(y_i = c | x) text{ for each pixel } i, text{ class } c in {1, ..., C}

$$

输出是 $H times W times C$ 的概率张量。

**MaskFormer（mask classification）**：

$$

text{预测 } N text{ 个 (binary mask, class label) 对}: {(m_1, c_1), (m_2, c_2), ..., (m_N, c_N)}

$$

每个 mask $m_k in [0,1]^{H times W}$，类别 $c_k in {1, ..., C, text{no-object}}$。

**最终像素级预测**通过聚合这 N 个 mask 得到：

$$

P(y_i = c | x) = sum_{k=1}^{N} m_k(i) cdot mathbb{1}[c_k = c]

$$

（实践中用 soft version，把 0/1 mask 换成 softmax over N 个 query 的 mask，再和 class 概率相乘）

## 1.2 为什么这个切换是本质的

表面上这只是"换了一种输出格式"。实际上它**改变了模型在学什么**：

| 学什么 | per-pixel classification | mask classification |
| --- | --- | --- |
| 每个像素的类 | ✓（直接学） | ✓（从 mask 聚合得到） |
| 哪些像素是一起的 | ✗（不学） | ✓（同一个 mask 里的像素就是一起的） |
| 类别总数 C | 在网络结构里硬编码 | **和网络结构解耦** |
| 对象/实例概念 | ✗（没地方放） | ✓（一个 query 就是一个实例） |

**第三条尤其关键**——类别数从网络里解耦出去了。mask 本身（$m_k in [0,1]^{HW}$）和类别数无关，类别只在 "每个 mask 贴标签" 这一步出现。这就是为什么**开放词汇分割（SAM、CAT-Seg）能直接从 MaskFormer 框架扩展过来**——只需要把 "per-mask classification" 换成 "per-mask CLIP text similarity" 即可，mask 生成部分完全不用改。

## 1.3 架构的具体实现

```
Image
  ↓
Backbone (ResNet / Swin)
  ↓
Pixel decoder (类似 FPN)  ──→  Pixel embedding  E_pix ∈ R^{HW×C}
  ↓                                       ↑
Transformer decoder                       │
  + N 个可学习 query          ─→ N 个 mask embedding E_mask ∈ R^{N×C}
                               ─→ N 个 class logits    C ∈ R^{N×(K+1)}
                                          │
                                          ▼
                             Mask_k = sigmoid(E_mask[k] · E_pix^T)  ∈ [0,1]^{HW}
```

三个关键模块：

**(a) Pixel decoder**

- 功能：把 backbone 的 C5 feature 逐步上采样到高分辨率
- 输出：**像素级的 embedding 场** $E_{pix} in mathbb{R}^{H times W times C}$
- 每个像素变成一个 C 维向量——**不是类别概率，是表征向量**
- 这一步就是 FCN 的 encoder-decoder 思想，但**输出语义改了**

**(b) Transformer decoder + N queries**

- 和 DETR 几乎完全一样：N 个 query 经过 cross-attention 聚合图像信息
- 输出：每个 query 的 **mask embedding**（C 维向量）+ **class logit**（K+1 维）
- **query 的含义从"对象槽位"升级为"mask 槽位"**

**(c) Mask 预测：点积生成**

- 每个 query 的 mask embedding $e_k in mathbb{R}^C$
- 和 pixel embedding $E_{pix}$ 做点积：$m_k(i) = sigma(e_k cdot E_{pix}[i])$
- 得到每个 query 自己的 $H times W$ binary mask

**这个点积机制极其优雅**——它把"如何生成 mask"转化为"如何让 query embedding 和目标区域的 pixel embedding 对齐"——**一个纯表征学习问题**。

## 1.4 训练：Hungarian matching 直接搬过来

和 DETR 一模一样：

- 预测集合：${(m_k, c_k)}_{k=1}^N$
- GT 集合：${(m_k^{gt}, c_k^{gt})}_{k=1}^M$（其中 $M leq N$，不足的部分填 no-object）
- cost matrix：$C_{ij} = -log p_j(c_i^{gt}) + lambda_{mask} L_{mask}(m_i^{gt}, m_j)$
- Hungarian 算法找最优一对一匹配
- 每个 GT 的监督只作用于被匹配到的那个 query

**关键点：语义分割原来没有 "Hungarian matching" 这个概念**——per-pixel classification 里每个像素的 loss 是独立的。MaskFormer 第一次把 set-based matching 带进了语义分割。

## 1.5 一个特别容易被忽略的细节

对语义分割，一个类有多个区域（比如图里有两棵树），**MaskFormer 倾向于让一个 query 覆盖所有这些区域**（只要它们都是"tree"）。这和实例分割（一个 query 一棵树）正好相反。

**同一个架构如何适应两种行为？**

- 关键在 GT 构造方式：语义分割的 GT 里，"所有 tree 像素" 被合并成一个 mask；实例分割里每棵 tree 是独立的 mask
- Hungarian matching 根据 GT 结构自动适应——query 学到"是按类聚还是按实例分"

这就是**同一公式接管两种任务**的具体机制：**模型结构不变，只有监督信号的结构变**。全景分割更是直接继承——stuff 类按类聚，thing 类按实例分，一张图里两种混合。

## 1.6 MaskFormer 的性能与残差

性能：

- 语义分割 ADE20K：55.6% mIoU（超过 Swin-L UperNet）
- 全景分割 COCO：52.7% PQ（超过专用 panoptic 模型）
- **一个架构超越三种专用架构**——这是"经验上"证成合流

残差（Mask2Former 要修的）：

- **小物体分割差**：DETR 的老病又来了——cross-attention 在高分辨率 feature 上看什么都"模糊一片"
- **训练慢**：也是 DETR 的病
- **多尺度没用好**：只用 backbone 最后一层 feature

---

# §2 · Mask2Former —— 把三个 DETR 式工程病一起修掉

Mask2Former 是 MaskFormer 出来半年后**同一作者的续作**。它做了三件事，每一件都能单独成文，但合起来才让 universal segmentation 成立。

## 2.1 改进一：Masked Attention —— 最关键的一步

### 问题定位

DETR / MaskFormer 的 cross-attention 在整张 feature map 上做：

- 每个 query 对 $HW$ 个位置做点积 → softmax
- 初始化时权重接近均匀 → 梯度稀释

Mask2Former 的观察：

> **既然每个 query 最终要预测一个 mask，为什么不直接让 query 在 cross-attention 阶段就只看自己预测的 mask 内部？**
> 

### 具体做法

```
Layer l 的 cross-attention:
  query_k attends to pixel i, with attention weight:

    A(k, i) = softmax_i( q_k · K_i + M_l(k, i) )

  where M_l(k, i) = 0  if mask_{l-1}[k, i] > 0.5   (prev layer 预测这个位置属于 query k)
                   -∞  otherwise                   (硬性屏蔽)
```

机制：

- 第 1 层 decoder 时还没有"上一层预测"——用 initial mask（均匀分布 / backbone 粗预测）
- 每一层 decoder 的 cross-attention **只在上一层预测的 mask 区域内**做
- 这是一个**逐层精修**的过程：每层缩小 query 看的范围，把注意力集中到真正相关的像素上

### 第一性原理

这是 Deformable DETR "稀疏化 attention" 思想的**变体**——但用的不是"采样点 + 可学习偏移"（那是几何先验），而是"**模型自己预测的 mask**"（内容先验）。

两者的对比：

- **Deformable DETR**: 稀疏化依据是 **位置**（query 自己指定看哪 K 个参考点）
- **Mask2Former**: 稀疏化依据是 **语义**（query 上层预测覆盖的区域）

后者比前者更强——**因为语义层面的稀疏化和任务目标直接对齐**。检测里"对象在哪"是外生的；分割里"mask 在哪"就是输出本身——**用输出做 attention 的先验，信号最强**。

### 效果

- Cross-attention 计算从 $O(N cdot HW)$ 实际只看 $O(N cdot |mask|)$——平均稀疏 10x 以上
- **训练收敛 3 倍**加速（和 Deformable DETR 的加速倍数接近）
- **小物体精度大幅提升**——因为小 mask 区域内的 attention 不再被 background 稀释

## 2.2 改进二：多尺度 Decoder —— 轮流注入不同尺度

### 问题定位

MaskFormer 的 decoder 只在 backbone 最后一层 feature 上做 cross-attention。但分割天然需要多尺度：

- 大物体（整片天空）需要低分辨率（高语义）
- 小物体（远处的人）需要高分辨率（精细空间）

加 FPN 再全分辨率做 attention？计算爆炸。

### 具体做法

Mask2Former 的 decoder **共 9 层**，分 3 组，每组 3 层：

```
第 1-3 层:  cross-attention 到 1/32 scale (coarse, 全局语义)
第 4-6 层:  cross-attention 到 1/16 scale (中等)
第 7-9 层:  cross-attention 到 1/8  scale (精细)
```

**轮流**而不是**并联**——这是省计算的关键：

- 并联多尺度 = 每层要处理 3 个 scale 的 feature，计算 3 倍
- 轮流多尺度 = 每层只处理 1 个 scale，计算 1 倍，但三层合起来覆盖三个 scale

query 在 decoder 中**逐步精修**：

- 前三层在 coarse feature 上做粗定位
- 后三层在 fine feature 上做精细 mask 修正
- 这是 **coarse-to-fine** 思想在 transformer 里的自然实现

### 和 DAB-DETR 的对比

DAB-DETR 用"query 每层输出 box 增量"做逐层精修；Mask2Former 用"query 每层看不同 scale 的 feature"做逐层精修。**两种精修机制都是 DETR 范式在不同输出形式下的自然推论**——有"逐层迭代"这个结构，就一定会有"每层做什么不同"的设计空间。

## 2.3 改进三：高效训练 —— Point Sampling Loss

### 问题定位

训练时 mask loss 要计算 query mask 和 GT mask 的逐像素差异。GT mask 大小 $H times W = 640 times 640$ 时，一张图 100 个 query 就有 $100 times 640 times 640 = 4 times 10^7$ 个像素要算 loss——**显存和计算都顶不住**。

### 做法

借鉴 PointRend 的思路：

- **不在全 mask 上算 loss**，只在 "采样 K 个 point" 上算
- 采样策略：**重要性采样**——优先采"预测不确定"的点（mask 值接近 0.5 的点）
- K = 112 × 112 = 12544 个点就够（比 640×640 小 30 倍）

效果：**训练显存降 3 倍、速度提升 3 倍，精度几乎无损**——这是工程性的加速，让 Mask2Former 能在单张 GPU 上训。

## 2.4 Mask2Former 的性能——架构统一在经验上被证成

一个模型、一套训练代码、一个超参配置，在三个任务上同时拿 SOTA：

| 任务 | Mask2Former | 之前 SOTA (专用) | 差距 |
| --- | --- | --- | --- |
| 语义分割 ADE20K | 57.7 mIoU | 55.1 (Swin-L UperNet) | +2.6 |
| 实例分割 COCO | 50.5 AP | 49.3 (Swin-L HTC) | +1.2 |
| 全景分割 COCO | 57.8 PQ | 52.3 (Panoptic-DeepLab) | +5.5 |

**三个任务一起超**——这在 Mask2Former 之前是没人做到的。

## 2.5 论文里那一句话的真正分量

"经验上被证成"这句话听起来平淡，实际上是**一个本体论判断被数据支持**：

> **语义 / 实例 / 全景分割不是三个任务，是一个任务的三种监督格式。**
> 

在 Mask2Former 之前这只是一个假设；在 Mask2Former 之后这是事实——**同一个架构、同一套超参、同一种损失函数，在三个任务上全面 SOTA**——没有其他解释方式，只能说三个任务的本质是同一个。

这和 Ising 模型里"二阶相变在不同系统中都遵循同一套临界指数"是同一种性质的结论——**表面不同的现象共享同一个底层结构**。

---

# §3 · 这次合流的更深判断：分割从"任务"变成了"表征的读出"

## 3.1 架构层面的判断

Mask2Former 之后看 MaskFormer-style 架构，它的组件分工是：

```
图像  ─→  [Backbone + Pixel Decoder]  ─→  像素级表征 E_pix
                                              ↑
                                         (不关心任务)

任务  ─→  [N 个 query + Transformer]  ─→  mask embedding + class
                                              ↑
                                         (不关心图像)

                                            点积
                                              ↓
                                          最终输出
```

**左路**只做"让每个像素有一个好表征"——这是 SegFormer / DPT / ViT 都能做的事

**右路**只做"从稠密表征里读出 k 个结构化输出"——这是 object query 机制的本职工作

分割这个任务的**全部特殊性**被压到了 GT 结构（同类合并 or 按实例分）里——架构里**没有任何分割特有的归纳偏置**。

## 3.2 这意味着什么

**分割不再是一个独立任务，分割是"稠密表征 + k-query 读出"的一种特例**。

同一架构可以做的其他事：

- 把 N 个 mask 换成 N 个 3D occupancy → **3D 分割**
- 把 mask 换成 attention map on video → **视频对象分割 (VOS)**
- 把 mask 换成 depth map → **Depth Estimation (PixelFormer)**
- 把 mask 的类别换成 CLIP text embedding → **开放词汇分割**

**所以 Mask2Former 不是"分割架构的巅峰"——它是"把分割还原成 query 读出"的第一步**。后面的 SAM / SEEM / SegGPT / CAT-Seg 全部是在这个还原基础上继续加维度（prompt、模态、in-context）。

## 3.3 和你前面追的那条线合流

你前面已经追出来的命题：

> **凡是需要"从稠密特征里提取结构化输出"的任务，最终都会演化出 k 个外生 token 作为接口**。
> 

Mask2Former 是**这个命题在分割任务上的第一次完整兑现**。DETR 是在检测上的首次兑现，Mask2Former 是在分割上的兑现。两者的共同骨架（backbone + pixel/feature + N queries + cross-attention + Hungarian matching）完全一致——不同任务的差异全部在"如何从 query 解码输出"这一步。

**Mask2Former 实际完成的更深事件**：**它把 object query 这个原语从"检测专用"扩成了"稠密预测通用"**。没有这一步，后面 SAM / Grounding DINO 都没地方落脚——因为这些工作的输出都是 mask，而 mask 的 query-based 生成范式就是 MaskFormer 立起来的。

---

# §4 · 残差：架构统一之后的本体论缺口

Mask2Former 把"三个分割任务"的架构统一了，但留下了两个**跨架构无法解决**的问题：

## 4.1 类别闭集问题

Mask2Former 的最后一层 class head 是一个固定的 $C to K+1$ 线性层。

- 训练时见过 K 类就只能输出 K 类
- 换数据集需要重训练这一层
- **"独角兽"永远出不来**——因为 class head 没有这一个 index

这个问题**不能靠改架构**解决——要解决它必须改"**类别是什么**"的定义：

- **从离散 index → 连续 embedding**（CLIP text embedding）
- 让分类变成"mask embedding 和 text embedding 的相似度"
- 这就是 CAT-Seg / ODISE / OpenSeg 的思路

## 4.2 Prompt 缺失问题

Mask2Former 的 query 是**内生**的——模型自己学的 100 个向量。用户不能说"我只想分割这只狗"——N 个 query 全部会激活，无法只输出一个。

解决要靠**把 query 外生化**——SAM 的路线。

## 4.3 这两条残差都指向同一出口

两者合起来决定了阶段 II 的最终出口（你数据库里的"提示化与开放词汇"那页）：

- **类别闭集** → CLIP-based 开放词汇
- **内生 query** → prompt-based 交互

**Mask2Former 把 per-pixel → per-query 这一层打通后，剩下的只有 class 和 prompt 这两个环节的"开放化"了**——这就是为什么阶段 II 的最后一页讲的是 SAM / Grounding DINO / Depth Anything 这批工作。它们全部在解 Mask2Former 留下的这两个残差。

---

# §5 · 一张总图：从 FCN 到 Mask2Former 的分割范式演进

```
FCN (2015)
    per-pixel classification
    C+1 类 softmax
         │
         │ 残差：没有实例概念，类别爆炸时不 scale
         ▼
DeepLab v3+ / PSPNet (2017-18)
    per-pixel classification + multi-scale pooling
    ASPP / PPM 在像素级补上下文
         │
         │ 残差：仍是 per-pixel，实例分割另走一路
         ▼
Mask R-CNN (2017)
    detect + per-RoI mask
    RoI 决定"对象在哪"，mask 做"形状"
         │
         │ 残差：只能实例分割，语义/全景另做
         ▼
Panoptic FPN (2019)
    两个 branch 拼接
    语义 branch + 实例 branch → 启发式合并
         │
         │ 残差：合并不可微，架构仍分立
         ▼
DETR (2020)
    k queries + Hungarian matching
    立起 query 范式（但只做检测）
         │
         │ 残差：分割怎么办？
         ▼
MaskFormer (2021)   ←── 范式切换：per-pixel → per-mask classification
    k queries + point-product mask
    语义/实例/全景在架构上合流
         │
         │ 残差：DETR 式的慢 + 小物体差
         ▼
Mask2Former (2022)  ←── 工程完备：三任务同时 SOTA
    masked attention + multi-scale decoder
    合流在经验上被证成
         │
         │ 残差：类别闭集 + query 内生
         ▼
SAM / Grounding DINO / CAT-Seg (2023+)
    query 外生化 + class embedding 化
    阶段 II 的出口
```

每一步只改了一件事，但每一步都是**下一步的前提**。MaskFormer 的位置**刚好在 DETR 范式和普世分割之间**——它是 query 机制从检测走向所有稠密任务的转折点。

---

## 编排定位

这份展开应被视为 [阶段 II · 统一 Mask 架构：任何稠密任务一种范式（MaskFormer / Mask2Former / SegFormer / OneFormer / SegGPT / EoMT）](00-定位卡.md) 中 §1–§2 的正文支撑。定位卡保留总览与坐标，本页负责给出完整机制、性能判断与残差传递；二者合用，才能把“mask classification 为什么是范式切换”这件事真正讲透。

本页到此完成两项工作：一是把分割从“逐像素分类”改写为“query 驱动的 mask 读出”；二是把这一改写和后续提示化、开放词汇、跨模态接口的生长链条提前接通。后续若继续下钻，最自然的承接页就是 SegFormer / OneFormer / SegGPT / EoMT 那条“decoder 逐步退场”的路线。
