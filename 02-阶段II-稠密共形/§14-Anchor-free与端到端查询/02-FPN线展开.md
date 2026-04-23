# 回到主线：FPN → RetinaNet → Mask R-CNN → Panoptic FPN 的四级共形推进

这四篇是 2017-2019 年检测/分割"合流"的四个关键节点。我把它们按**解决的问题 → 机制 → 第一性原理 → 下游影响**的格式打穿。

最后再把"手工先验"这个残差往深里推一层——你会发现那四条先验其实是同一个更底层失配的四种表现。

---

## 3 · FPN —— 多尺度从"trick"变成"基础设施"

### 3.1 它解决的问题：多尺度

检测（和分割）都逃不开一个事实：**物体尺度差别能到 100×**。COCO 里小物体 <32²，大物体 >96²。一个单尺度特征图几乎必然在某一端表现差：

- 如果用**浅层 feature**（大分辨率）：空间细节够，能定位小物体——但语义弱（只有低级纹理，不知道是啥）
- 如果用**深层 feature**（小分辨率）：语义强（知道是狗还是车）——但分辨率差，小物体直接丢失

### 3.2 FPN 之前的三种方案，都不优雅

| 方案 | 做法 | 问题 |
| --- | --- | --- |
| **Image pyramid**（传统） | 把原图缩放成多种尺度，每个尺度跑一遍 backbone | 计算爆炸，内存吃不消 |
| **In-network pyramid (SSD)** | 用 backbone 自带的 C3/C4/C5 多尺度 feature map 各出预测 | 浅层 feature 语义弱，小物体依然检测不好 |
| **Hourglass / U-Net-like** | encoder-decoder 对称结构做逐级精修 | 为特定任务（pose）设计，没有成为通用 neck |

SSD 的方案看起来最接近，但它有一个致命缺陷——**C3 层就是拿来做"小物体检测"的，但 C3 那么浅，它根本不知道这些物体是啥**。所以 SSD 在小物体上精度低。

### 3.3 FPN 的关键洞察

> **Backbone 本身已经是一个金字塔**（feature maps at stride 4/8/16/32）。问题不在"要不要做多尺度"——多尺度**天然存在**在 backbone 里——而在于**怎么让每一级都同时拥有语义 + 分辨率**。
> 

FPN 的做法，三步：

```
Backbone: C2 (stride 4) → C3 (8) → C4 (16) → C5 (32)
                                              ↓
                              1×1 conv (reduce channel) → P5
                                              ↓
                                 2× upsample + lateral
P4 = upsample(P5) + 1×1(C4)
P3 = upsample(P4) + 1×1(C3)
P2 = upsample(P3) + 1×1(C2)
```

三个算子，每个都有精确的功能：

1. **1×1 lateral conv**：把 backbone 各级 channel 统一（比如都对齐到 256），同时过滤掉和当前尺度语义不兼容的 feature。
2. **2× upsample（nearest neighbor）**：不是学习的——纯空间复制。**选 nearest 而不是 bilinear 是关键**——因为 bilinear 会引入"平均值"这种中间态语义，nearest 保留"这个 token 属于哪个对象"的明确归属。
3. **逐元素加**：不 concat——这点和 U-Net 不同。加法保留两个来源的信息，但总通道数不变，计算成本受控。

### 3.4 第一性原理：为什么这三步的组合是必然的

把 FPN 看成一个**信息合成问题**。你手里有：

- 高级语义（C5：低分辨率、强语义）
- 中级空间（C3：中分辨率、弱语义）
- 低级细节（C2：高分辨率、最弱语义）

你想要：**每个分辨率都同时具备对应尺度所需的语义**。

这等价于一个**跨层信息路由**任务。FPN 给出的最优廉价解：

- **语义只从深层往浅层流**（top-down）——因为浅层没有别处可以取语义
- **空间只从浅层横向注入当前层**（lateral）——因为深层没有空间分辨率
- **融合用加法**——最省参数的对齐方式

你会发现，这其实又是**聚合-广播原语的一次特例**：

- C5 是"全局 aggregate"（整张图压成一个粗语义）
- top-down upsample + lateral add 是"结构化 broadcast"——把 C5 的语义，根据每一层的空间结构，分发下去

这是**广播原语在纯 CNN 架构下的第一次出场**——比 PPM（2017）、non-local（2018）、DETR（2020）都早。FPN 不自觉地做到了"低维中介（C5 顶端）+ 逐层广播"，只是 FPN 的中介不是 k 个 token，而是整个 C5 feature map。

### 3.5 下游影响：成为稠密任务的默认 neck

FPN 之后的每一个稠密架构——RetinaNet、Mask R-CNN、Panoptic FPN、FCOS、DETR 的 multi-scale feature map、SegFormer 的 hierarchical features——**全部继承或变体了 FPN 的 top-down + lateral 结构**。

后来的变体：

- **PANet (2018)**：在 FPN 上再加一条 bottom-up 路径，变成双向金字塔。YOLOv4/v5 的 neck 就是 PANet。
- **BiFPN (EfficientDet, 2019)**：把 FPN 的融合换成可学习权重 + 多次双向迭代。
- **NAS-FPN**：直接 NAS 搜一个最优连接结构，发现人工设计的 FPN 确实接近最优。

**这组变体说明了一件事**：FPN 的拓扑结构（top-down + lateral）是本质对的，后续只是在通路数量、融合权重上做微调。

---

## 4 · RetinaNet / Focal Loss —— 损失函数第一次适应样本难度

### 4.1 它解决的问题：一阶段的极端类不平衡

前面讲过这个，但这里要精确化：

一张 COCO 图 ~5 个 GT 对象。RetinaNet 在多尺度 FPN 上每个位置 9 个 anchor → **总 anchor 数 ~100,000**。

正负比 = 5 : 100,000 = **1 : 20,000**。

如果用普通 cross-entropy，每个 anchor 贡献 loss $-log p_t$。哪怕所有负样本都已经被正确判为背景（$p_t = 0.99$，$-log p_t approx 0.01$），100,000 × 0.01 = 1000 的累计负样本 loss 也会**压过 5 × 1 = 5 的正样本 loss**——网络被"容易分辨的背景"带着跑，学不到前景。

### 4.2 之前的缓解方案及其局限

**OHEM (Online Hard Example Mining)**：训练时每个 batch 挑 loss 最大的前 k 个样本反传。

- 好处：把梯度导向难样本
- 坏处：需要显式排序操作，实现复杂；而且它**硬筛掉了所有"中等难度"的样本**（只保留最难的），信息浪费

**Hard negative mining (SSD)**：保持正负比 1:3 固定采样。

- 好处：简单
- 坏处：**负样本总数仍然被硬限死**，有很多有用信号被丢掉

### 4.3 Focal Loss 的关键洞察

> 不要靠**采样**（丢数据）或**筛选**（丢梯度）来平衡——**改损失函数本身**，让每个样本按难度自动加权。
> 

**Focal Loss 的定义**：

$$
\text{FL}(p_t) = -(1 - p_t)^\gamma \log p_t
$$

其中：

- $p_t = p$（if 真标签为 1）或 $1-p$（if 真标签为 0）——也就是"模型给出的对正确答案的置信度"
- $\gamma$ 是一个调节超参，标准取 2

**加权因子** $(1-p_t)^\gamma$ **的行为**：

| 样本状态 | $p_t$ | $(1-p_t)^2$ | 效果 |
| --- | --- | --- | --- |
| 极易负样本（背景已判对） | 0.99 | 0.0001 | 几乎不贡献 loss |
| 中等负样本 | 0.7 | 0.09 | 适度贡献 |
| 难负样本（被误判为前景） | 0.3 | 0.49 | **大幅贡献** |
| 完全错分 | 0.01 | 0.98 | **最大贡献** |

**机制上看**：这是一个**"已经学会的别再学"**的自动门控。

### 4.4 第一性原理：为什么这个损失函数是必然的

从信息论角度，每个样本提供给模型的"**新信息量**" ≈ $-log p_t$（模型的惊讶度）。当 $p_t to 1$，$-log p_t to 0$——这个样本**已经不含新信息**了，再继续学它就是浪费。

但标准 cross-entropy 没有"饱和后断流"的机制——它用的是线性 log，不会自动截断。

Focal Loss 加的 $(1-p_t)^\gamma$ 就是**一个信息门**：

$$
\text{effective gradient} \propto (1-p_t)^\gamma \cdot \frac{1}{p_t}
$$

γ 控制门的陡峭度。γ=0 退化为普通 CE；γ=2 是经验最优；γ→∞ 类似 OHEM 的硬筛。

**这实际上是把"课程学习（curriculum learning）"从一个训练调度层面**（先学简单的再学难的）**内化到损失函数的每个前向里**——每一步都是一次迷你 curriculum：简单样本自动让位，复杂样本自动抬头。

### 4.5 更深一层：损失函数作为"共形度量"的一次进化

你的谱系语言里 loss 是"度量"维度。一般 CE loss 是静态度量——每个样本的权重固定为 1。Focal Loss 是**自适应度量**——权重随模型状态动态改变。

这条线后来一直被扩展：

- **GIoU / DIoU / CIoU loss**（2019）：对几何度量做类似改造——标准 L1/L2 loss 忽略 IoU 本身的几何含义，这些 loss 直接把 IoU 作为优化目标
- **Varifocal Loss / Quality Focal Loss**（2020）：把置信度和 IoU quality 耦合进一个统一 loss
- **Distribution Focal Loss**（2020, YOLOv8 继承）：把框坐标的回归从"点估计"升级成"分布估计"

所有这些都是"**度量本身内含动态结构**"这条思路的延续——度量不再是外部的静态尺子，而是**随训练状态演化的动态场**。

**这是阶段 II 在"度量维度"上最大的一次升级**。

---

## 5 · Mask R-CNN —— RoIAlign + 多任务头，全景时代的前奏

### 5.1 它解决的问题：Instance segmentation

在 2017 年前，实例分割主要靠两种思路：

- **Proposal-based (Deepmask, Sharpmask)**：先出 mask 候选，再分类——慢且精度差
- **Semantic + instance grouping**：FCN 先语义分割，然后某种聚类算法合并相同对象的连通分量——依赖后处理

Mask R-CNN 的思路**极其简单**：

> Faster R-CNN 已经在 RoI head 里做了"分类 + 框回归"两个任务。**再加一个 mask 分支**——反正 RoI feature 都已经提好了，多一个 head 不花什么。
> 

### 5.2 看似简单的两个关键变化

### 变化一：RoIAlign 替代 RoIPool

这是 Mask R-CNN 的**最核心技术贡献**，远比"加了个 mask head"重要。

**RoIPool 的问题**：RoIPool 做两次量化：

1. RoI 坐标从 input 图映射到 feature map 时，除以 stride 后**用 floor 量化**到整数
2. 每个 bin 的边界也用 floor 量化

这两次量化对**分类**影响很小（类别是对对象整体的判断，亚像素偏移无关）——但对**mask 预测**是致命的。mask 需要像素级精度，任何量化都直接导致边界错位。

**RoIAlign 的做法**：

- 不量化。RoI 在 feature map 上的坐标保持浮点
- 每个 bin 内取 4 个采样点（常见选择），每个采样点的 feature 用 **bilinear interpolation** 从邻近 4 个 feature pixel 计算
- 4 个采样点再 average（或 max）pool 成 bin 的输出

**效果**：mask AP 提升 +10.5（对小物体更是 +15）。**只换一个算子**，精度变化巨大。

### 变化二：Class-specific mask + binary loss

标准语义分割（FCN）的 mask head 是：每个像素预测 C+1 个类别概率，用 softmax——**类与类之间互相竞争**。

Mask R-CNN 不这么做。它的 mask head 每个 RoI **独立为每个类预测一个 mask**，总共 C 个二值 mask，用 **per-class sigmoid + BCE**。推理时先从 classification head 确定这个 RoI 是哪一类，**只取那一类对应的 mask**。

为什么这样设计？

- RoI 的分类已经在 classification head 决定了——mask head 不需要重做这个判断
- 这把"**这是啥**"（classification）和"**它的形状是啥**"（segmentation）在任务层面解耦
- 每类的 mask 不需要和其他类"竞争"同一个像素——一个像素是狗的像素，不是"狗比猫概率高 0.1"，而是"狗的 mask = 1"

### 5.3 第一性原理：解耦的哲学

Mask R-CNN 背后的判断是：

> **检测任务已经给了我们一个好先验——每个 RoI 就是一个独立对象**。在这个先验下，像素级形状预测可以简化为一个**局部二分类问题**（这个像素是不是这个对象的一部分）。
> 

这比 FCN 面对"不知道对象在哪"时需要解 C+1 类竞争**要简单得多**。

这是"**任务分解**"的一次优美应用：先解决大问题（在哪、是啥），再解决小问题（形状）。和 coarse-to-fine 同源。

### 5.4 下游影响

- **键点检测**：把 mask head 换成 "每个像素 × K 个关节"的 heatmap，自动变 pose 估计
- **DensePose**：Mask head 输出 UV 坐标，做体表 surface mapping
- **3D mesh**：Pixel2Mesh 等把 head 变 3D 几何预测

**这条路证明了一个通用范式**：`(backbone → RoI-specific feature extractor → task-specific head)` 是极其灵活的模板。**只要 RoI 概念存在，几乎所有对象级稠密任务都能套进来**。

这个模板一直用到 DETR 推翻"RoI"这个概念本身为止（2020）。

---

## 6 · Panoptic FPN —— 提出任务本身

### 6.1 Stuff vs Thing 的区分

这是这篇论文真正的贡献——不是模型，是**重定义任务**。

- **Thing**：可数名词对象（person, car, dog）。有实例概念，同类多个对象要区分。实例分割的范畴。
- **Stuff**：不可数的背景区域（sky, road, grass）。没有实例概念——"天空 #1" 和 "天空 #2" 无意义。语义分割的范畴。

传统上这两者是**两个独立任务**，两套评估指标，两套 benchmark。**实际用户关心的是同一张完整的场景理解图**——你想知道"画面上所有 pixel 都属于什么，而且 thing 类要区分实例"。

**Panoptic segmentation 的定义**：

> 每个像素分配一个 (class_id, instance_id) 对。对 stuff 类，instance_id 为 null；对 thing 类，instance_id 区分实例。
> 

配套的 **Panoptic Quality (PQ)** 度量：

$$
PQ = \underbrace{\frac{\sum_{(p,g) \in TP} \text{IoU}(p,g)}{|TP|}}*{\text{segmentation quality}} \times \underbrace{\frac{|TP|}{|TP| + \frac{1}{2}|FP| + \frac{1}{2}|FN|}}*{\text{recognition quality}}
$$

第一项看 matched 分割质量，第二项看检测 F1——**一个度量同时评估语义和实例**。

### 6.2 Panoptic FPN 的简单方案

论文提的模型极简：

```
同一 backbone + FPN
           ↓
        两个 head 并联:
        ├─ Instance branch: Mask R-CNN head → 输出 (框, 类, 实例 mask)
        └─ Semantic branch: 把 P2-P5 上采样到 1/4 后融合 → 全分辨率 stuff/thing 语义图
           ↓
        后处理合并 (启发式规则)
```

**关键选择**：

- 两个 branch 共享 backbone + FPN
- 合并规则是**手工的**：优先相信 instance branch 的 mask（对 thing 类），stuff 类从 semantic branch 拿
- 冲突时（一个像素同时被 instance mask 和 stuff 语义标记）用置信度决定

### 6.3 第一性原理：它做了什么，没做什么

**做到了**：

- 把**任务**统一——同一张场景图、一种度量
- 证明 backbone / neck / 多数特征可以**共享**，不需要两套完整网络

**没做到**：

- **head 仍然分立**（instance 一套、semantic 一套）
- **合并仍然手工**（置信度规则，不可微）
- **训练仍然是两个 loss 加权**，权重手调

所以 Panoptic FPN 是**一次"语义级合并"而非"架构级合并"**。它定义了问题，但没优雅地解决它。

### 6.4 下游影响：迫使下一代架构真正合并

Panoptic FPN 留下的悬念——"instance 和 semantic 能不能真的在一个 head 里做"——催生了 Panoptic 时代的几条主流路线：

- **Panoptic-DeepLab (2020)**：anchor-free + bottom-up，在一个网络里直接出 center heatmap + offset + semantic seg
- **MaskFormer (2021)**：**把所有分割任务统一成"mask classification"**——semantic、instance、panoptic 都是"预测一组 mask + 每个 mask 分一个类"的变体
- **Mask2Former (2022)**：MaskFormer + masked attention，彻底统一

**从 Panoptic FPN 的"两头并联" 到 Mask2Former 的"一头全包"，花了 3 年**。这三年的主线就是你这张谱系下一组的故事。

---

## 本组合力的残差：更深一层看手工先验

你现在的残差分析是四条手工先验：anchor / NMS / RoI Pooling / IoU 匹配。

每一条都对，但它们**不是平行的四个问题**——它们是**同一个底层失配在四个位置的露头**。

### 这个底层失配是什么？

> **神经网络在连续实数空间里运行，但"对象"这个本体是离散的**。
> 

这两个空间之间的**接口**，每撞一次就需要一条手工先验来临时修补：

| 接口位置 | 失配表现 | 手工先验 |
| --- | --- | --- |
| **GT 离散 vs. anchor 连续** | GT 框的形状空间是连续的，但 anchor 必须是有限 k 个 | Anchor 设计（尺度/比例/步长人工挑） |
| **预测连续 vs. 对象离散** | 网络输出一个稠密置信度场，但"一个对象"应该只对应一个输出 | NMS 后处理 |
| **RoI 连续 vs. grid 离散** | RoI 坐标浮点，feature map grid 整数 | RoI Pooling 的量化（或 RoIAlign 的 bilinear 缓解） |
| **GT 单一 vs. anchor 多样** | 一个 GT 要被分配给某些 anchor 而不是另一些 | IoU 阈值规则 |

每一条都在说同一件事：**"对象是离散的一级概念"这个本体论，在"神经网络是连续可微函数"的框架里找不到原生表达**。所以每一次接口碰撞都要打一个补丁。

### 这四个补丁的共同特征

- **不可微**：anchor 选择是离散超参，NMS 是启发式排序，RoI 量化是 floor，IoU 匹配是 hard threshold
- **不随数据分布自适应**：在 COCO 上调好的 anchor，换个数据集可能就废
- **在训练-推理间不一致**：训练时 NMS 不参与，推理时依赖 NMS；训练用 IoU 阈值匹配，推理用 score 阈值过滤

这三个特征每一个都是**"端到端共形"的反面**。

### DETR 怎么一次性解决？

把"对象是离散一级概念"这个本体论**直接塞进架构里**——用 k 个 object query 作为"k 个离散对象槽位"的显式表达。

这一步走完后：

| 原失配 | DETR 的解决方式 |
| --- | --- |
| anchor 设计 | query embedding 可学习——**数据决定 k 个"anchor"的位置和形状** |
| NMS | Hungarian matching 在训练时强制 one-to-one——**推理自然无重复** |
| RoI pooling | Cross-attention 从 feature map 里"自由取"——**没有量化** |
| IoU 匹配 | Hungarian matching 可微（通过 Sinkhorn 松弛）——**匹配过程可学习** |

**四条先验一次性全干掉，而且不是分别修补——是因为换了一个本体论表达方式**。Object query = 离散对象槽位的连续嵌入——第一次，对象这个离散概念在连续网络里有了一个原生表达。

### 所以这组的残差真正指向的：本体论补齐

不是"检测架构还能调优吗"的残差，而是"**我们的架构语言能不能表达'离散对象'这个基本概念**"的残差。

FPN / RetinaNet / Mask R-CNN / Panoptic FPN 已经把"连续框架内能做的"做到了顶：

- FPN 解决了多尺度
- Focal Loss 解决了类不平衡
- RoIAlign 解决了像素级精度
- Panoptic FPN 定义了最终任务

**剩下的残差不是技术问题，是本体论问题**——你需要一个能在连续可微框架里表达"k 个离散槽位"的原语。

这个原语就是**object query**——而你已经知道了，它在更高层的抽象里就是**低维中介 token 作为广播源**的这个原语。从 PPM 到 object query 到 DETR 到 Mask2Former 到 SAM 到 LLM soft prompt——**都是同一个公理在不同任务上的落地**。

所以这组的残差**不是"DETR 要来了"这么简单的叙事**，而是：**稠密共形的进一步前进，必须先解决连续-离散的本体论接口问题**。而解决它的那个原语，注定会成为之后整个深度学习所有需要"全局结构介入局部决策"的任务的共同基座。

这张谱系图里阶段 II 最后这块残差，**其实是阶段 III / IV / V 的全部前提**——没有 object query 这个本体论原语，transformer 时代的稠密架构就没办法统一起来。

---

这一组的最佳安放位置，是作为 [阶段 II · 检测共形的流水线化：从区域提议到特征金字塔（R-CNN 家族 / YOLO / SSD / FPN / RetinaNet / Mask R-CNN / Panoptic FPN）](..\§13-检测共形的流水线化.md) 的深度补页，专门承接其中 3-6 条目。这样处理之后，§13 负责主线速览，本页负责把 FPN / Focal / Mask R-CNN / Panoptic FPN 的机制与残差完整展开，再自然交给下一组的 anchor-free / DETR 线。
