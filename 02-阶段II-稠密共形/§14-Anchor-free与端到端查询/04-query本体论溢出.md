# 先把论断本身抽象化

原始 DETR 里，query 是：

- **内生的**（模型自己学出来的）
- **无语义的**（N 个向量，含义不可解释）
- **任务绑定的**（专门用于 COCO 检测的 80 类 + 框）

这三个属性**每一个都会在后续五代里被打破**。最终留下的只有一件事：

> **query = k 个与稠密特征做 cross-attention 的向量，输出绑定到这 k 个 query 上。**
> 

**这个最小骨架才是 object query 的真正身份**。"对象槽位"只是它在 DETR 里最早的一个具体用法。把它当"对象槽位"理解，是**把特例当成一般定义**。

为避免 query 变成万能词，后续使用必须标注类型，并遵守判定边界：一个对象要被称为 query，至少要规定输出槽位或调用目标，主动从某个表征场索取信息，并且它的改变会改变模型输出的对象、区域、属性或任务。否则它只是 input token、condition token、latent token 或 routing variable。

## Query 是绑定制度，不是意义制度

query 的本体不是语义，而是绑定。

它回答“由哪个槽位接管这片证据”，但不自动回答“这片证据是什么意思”。一个 DETR query 可以绑定到一个框，一个 MaskFormer query 可以绑定到一张 mask，一个 SAM prompt 可以绑定到一片空间支撑；但这些绑定的意义仍要靠类别表、mask head、文本 embedding、prompt 或任务定义赋予。

因此 query 机制的胜利，必然把阶段 II 推到接口闭合；接口闭合的胜利，又暴露出语义主权仍在外部。

下面五代每一代打破了什么属性：

| 代 | 打破了什么 | query 变成了什么 |
| --- | --- | --- |
| Mask2Former | 打破"任务绑定 = 检测" | mask 槽位 |
| SAM | 打破"内生" | 用户提供的 prompt |
| Grounding DINO | 打破"单模态" | 文本 embedding |
| SEEM / SegGPT | 打破"固定模态" | 任意模态 prompt |
| LLM soft prompt | 打破"视觉任务" | 任务指令 |

---

# §1 · Mask2Former —— query 从"对象"到"mask"的广义化

## 1.1 问题背景

DETR 出来之后一个立刻出现的问题：**分割任务能不能也用 query 范式？**

分割的传统做法（FCN / DeepLab / PSPNet）是"**每个像素分 C 类**"——softmax 在通道维度上做。这是**pixel classification** 范式。

Cheng 等人（FAIR）在 MaskFormer（2021）里做了一个看似简单但极其本质的切换：

> **不要预测每个像素的类别。预测一组 mask，每个 mask 配一个类别。**
> 

这叫 **mask classification** 范式。一次切换把三个分割任务统一了：

- **语义分割**：mask 数 = 类别数，每个 mask 对应一个类
- **实例分割**：mask 数 = N，每个 mask 对应一个对象实例
- **全景分割**：mask 数 = N，有的 mask 是 stuff 类，有的是 thing 实例

## 1.2 架构怎么做

```
Image → backbone → feature map (pixel embedding, HxWxC)
                   +
N 个 query ─→ Transformer decoder ─→ N 个输出:
                                      ├─ class logits (N × (K+1))
                                      └─ mask embedding (N × C)
                                          ↓
                              每个 mask embedding × pixel embedding
                                      → N 张 mask (HxW)
```

**这里 query 的含义从"对象槽位"变成了"mask 槽位"**——每个 query 最终输出的是"一张 mask + 一个类"而不是"一个框 + 一个类"。

机制其实只改了一点：**预测 head 从回归 box 改为和 pixel embedding 做点积得到 mask**。其他（Hungarian matching、cross-attention、query 结构）**全部照搬 DETR**。

## 1.3 Mask2Former 的进一步改进

Mask2Former（2022）在 MaskFormer 上加了 **masked attention**：

- Cross-attention 时，每个 query 只看"它上一层预测的 mask 内部的像素"
- 这是 Deformable DETR 稀疏化思想的变体——**用 mask 本身作为 attention 的稀疏先验**
- 训练快 3 倍，精度全面超过 MaskFormer

## 1.4 本质判断

Mask2Former 证明了：**object query 的"object"可以是任何可数离散的输出单元**——可以是框、可以是 mask、可以是关键点组。query 的**骨架不变**，换的只是**输出解码方式**。

这是 query 原语第一次广义化——**从"物体"解放到"离散输出槽位"**。

---

# §2 · SAM —— 最关键的一次质变：query 从"内生"到"外生"

这是五代里**最本质的一次升级**。其他四代都是换"query 是什么东西"，SAM 换的是"**query 从哪里来**"。

## 2.1 SAM 之前：query 是模型自己学的

DETR / Mask2Former / 所有 DETR 系：

- N 个 query = N 个**可学习参数向量**
- 训练时梯度更新这些向量
- 推理时 query 是**模型内部状态**——用户只能吃预测结果，不能干预过程

这意味着：**分割什么、分割多少个对象，完全由模型决定，用户没有控制权**。

## 2.2 SAM 的关键切换

> **Query 不从模型里学出来，从用户那里拿。**
> 

用户在图上点一个点、画一个框、画一个粗 mask —— 这些**被 encode 成 query token** 喂给 decoder：

```
用户操作                 Prompt Encoder              Prompt tokens
──────────             ─────────────              ───────────────
点 (x, y, fg/bg)  ──→  positional encoding  ──→   1 个 token
框 (x1,y1,x2,y2)  ──→  左上 + 右下各一个 PE  ──→   2 个 token
粗 mask (HxW)     ──→  downsample + conv    ──→   和 image embedding 加
文本 (后续版本)    ──→  CLIP text encoder    ──→   若干 token

image embedding (由 ViT encoder 预计算, 每张图只算一次)
       +
prompt tokens (用户每次交互动态变化)
       ↓
Lightweight mask decoder (2 层 transformer, 轻量)
       ↓
N 个 mask (通常 N=3, 代表不同粒度)
```

## 2.3 为什么这是质变

三个量级上的翻转：

**(a) 语义 query ≠ 位置 query**

- DETR 里 query 是抽象嵌入 + 训练学出位置偏好
- SAM 里 query 是**直接的位置编码**——点的坐标直接 embed
- 这把"**query 是什么**"从"可学习的语义向量"扩到了"**可被编码成向量、并能改变输出目标的用户意图**"

**(b) 推理时 query 可以变**

- DETR 系推理时 query 数量和值都固定
- SAM 推理时每次 prompt 不同 → query 就不同 → 输出不同
- **模型变成了"prompt → output"的函数**——这和 LLM 的范式完全同构

**(c) image encoder 和 prompt encoder 解耦**

- Image encoder（ViT-H）很大，每张图跑一次
- Prompt encoder + mask decoder 极轻量，每次交互跑一次
- 用户每秒点一次，实时出 mask——**交互式分割**
- 这个架构分离直接决定了 SAM 能商用

## 2.4 SAM 揭示的本体论

SAM 让人看清了一件事：**object query 本质上就是"任务的外部输入"这个位置的占位符**。

在 DETR 里这个占位符被内生化（模型自己填）是**因为任务是封闭的**（COCO 80 类 + 固定位置）。一旦任务变成"用户想分什么就分什么"——开放、动态、交互——这个占位符就强烈倾向于外生化。

**这不是"SAM 发明了新东西"，是"SAM 把 object query 最深的结构暴露了出来"**——它本来就是一个任务指令接口，DETR 只是把它塞在模型内部而已。

## 2.5 "输出-query 绑定"的核心属性

SAM 让另一个属性浮出水面：**每个 prompt 对应一个输出**——一对一。

这和 DETR 的 Hungarian matching 是**同构的**：

- DETR：N 个内生 query ↔ N 个输出（可能被匹配到 GT，可能是 no-object）
- SAM：k 个 prompt ↔ k 组输出

"**输出被 query 索引**"这个结构是 object query 原语的**不可压缩部分**——不管 query 从哪里来、代表什么，**输出永远和 query 一对一绑定**。这就是为什么 DETR 系可以"无 NMS"——因为不存在"多对一"的结构性模糊。

---

# §3 · Grounding DINO —— query 跨模态

## 3.1 问题

DETR / SAM 的 query 仍然是"视觉域内"的东西——位置 embedding、抽象向量、或者用户点击。**能不能直接让文本作为 query？**

"请检测图里的所有'红色的杯子'" —— "红色的杯子"这段文本，能不能直接变成 query，让 decoder 去图里找？

这就是**开放词汇检测 (open-vocabulary detection)**：训练时见过的类别之外，也能检测。核心需求是**让 query 携带类别语义**。

## 3.2 Grounding DINO 的做法

基于 DINO-DETR 骨架，做两个关键注入：

**(a) 文本经 BERT 类 encoder → 文本 token 序列**

- 每个单词一个 token
- "a red cup on the table" → N_text 个 token

**(b) 文本 token 和 image token 做 cross-attention**

- Encoder 里：text token ↔ image token 双向 cross-attention（**这叫 cross-modal feature fusion**）
- 结果：**image feature 已经带上了文本语义**，文本 feature 也带上了图像信息
- Decoder 里：query 同时 attend text 和 fused image

**(c) Query 的初始化也从文本驱动**

- 用 text 去 encoder 的 fused image feature 里找"最相关的位置"
- 这些位置的 embedding 作为 query 的初始化
- 相当于**文本在选择 decoder 的起点**

## 3.3 这是 query 的哪一步升级

在 DETR 里 query 是"槽位"——不知道要找什么，靠匹配和梯度自己学。

在 Grounding DINO 里 query 是"**带着文本语义去找**"——query 本身已经 encode 了"我要找什么类别"。

Query 的**信息承载密度**发生了跃迁：

- DETR query: $vec{q}$ = 可学习向量（任务固有）
- Grounding DINO query: $vec{q}$ = 函数(文本) = **可变语义载体**

这意味着**同一个模型，不同文本 prompt，就是不同的"专用检测器"**——一套权重覆盖无限类别。这就是开放词汇的本质。

## 3.4 和 CLIP 的合流

Grounding DINO 的**文本-图像对齐**本质上就是 CLIP 思想的一次落地：用大规模图文对预训练一个**共享 embedding 空间**，让文本和图像 feature 可以在同一个空间做点积。

但 CLIP 只做"整图 vs 整句"的对齐。Grounding DINO 做的是"**文本 token ↔ image token 级别的稠密对齐**"——这是 DETR 范式 + CLIP 思想的合流。

---

# §4 · SEEM / SegGPT —— query 任意模态

Grounding DINO 还是"文本 query + 图像 feature"的固定组合。**SEEM / SegGPT 往前推了一步：多种模态都可以在满足调用边界时成为 query**。

## 4.1 SEEM (Segment Everything Everywhere, 2023)

一个统一的分割模型，支持：

- 点 prompt（像 SAM）
- 框 prompt（像 SAM）
- 文本 prompt（像 Grounding DINO）
- **参考图像 prompt**（"这张图里的物体，在目标图里找出来"）
- **mask prompt**（"和这个 mask 相似的区域"）
- 多模态组合

做法：**为每种 prompt 设计一个 encoder，全部 encode 成 token，统一输入 decoder**：

```
point  ─┐
box    ─┤
text   ─┼─→ 对应 encoder ─→ prompt tokens ─→ decoder ─→ mask
image  ─┤
mask   ─┘
```

## 4.2 SegGPT (2023)

思想更激进——**把分割变成 in-context learning**：

- 给一张"例图 + 例 mask"作为 context
- 模型看一张新图，模仿 context 给出 mask
- 不需要显式 prompt encoder——context 本身承担 prompt 角色

```
Context image + mask  ─┐
                        ├─→ 拼在一起送进 ViT ─→ 输出新图的 mask
New image            ─┘
```

这是**query 机制和 LLM few-shot 的合流**——"prompt" 不再是显式的 token，而是**context 本身**。

## 4.3 本质升级

从 SEEM 到 SegGPT，query 机制的**接口层在收缩**：

- SAM：每种 prompt 要一个专用 encoder
- SEEM：所有 prompt encode 到统一 token 空间
- SegGPT：连 encoder 都不需要，context 自己就是 prompt

这和 NLP 里"**从 task-specific fine-tuning 到 in-context learning**"的转变是**同一条路径的视觉版**。

---

# §5 · LLM soft prompt / visual prompt tuning —— query 下放到大模型通用接口

最后一代：query 从视觉任务**下放到所有深度学习任务**。

## 5.1 Soft prompt / Prefix tuning (2021)

LLM 时代的 parameter-efficient fine-tuning 方法：

- 冻结整个 LLM 主干
- 在输入序列前加 k 个**可学习的 token**（soft prompt）
- 只训练这 k 个 token，让 LLM 适应新任务

```
[soft token 1] [soft token 2] ... [soft token k] [input text tokens] ─→ LLM
     ↑                                                                   ↓
   可学习                                                              output
```

**这 k 个 soft token 就是 object query 的 LLM 版**：

- 可学习向量 ✓
- 承载任务语义 ✓
- 和主体特征做 attention ✓（LLM 的 self-attention 里，soft token 会被其他 token attend）
- 一对一绑定输出？——在 prefix tuning 里 soft token 影响所有后续输出，这是广义版

## 5.2 Visual Prompt Tuning (VPT, 2022)

几乎一模一样的思路搬到 ViT：

- 冻结 ViT
- 在 patch token 序列前加 k 个可学习 prompt token
- 只训练 prompt token，让 ViT 适应新下游任务

## 5.3 本质判断

到 soft prompt / VPT，**"外生 query token"已经不是视觉检测任务专用**——它是**整个 transformer 时代的通用接口原语**。

不管任务是什么（检测、分割、分类、生成、理解、跨模态），只要架构是 transformer：

- 想定制输出 → 加 k 个 query/prompt token
- 想交互 → 让用户喂 prompt
- 想跨模态 → 把别的模态 encode 成 token

**DETR 的 object query 在 2020 年看起来像是一个检测任务的 clever hack，到 2024 年成了整个深度学习的通用装配接口**。

---

# §6 · 机制推导：为什么"k 个外生 token"会反复出现

现在可以回答：为什么许多这类任务会反复演化到 k 个 query token 这个架构。

## 6.1 形式化问题

许多"**从稠密特征提取结构化输出**"的任务都有三个约束：

1. **输入是稠密的**（图像 feature map、LLM 的 hidden state 序列，都是 "N 个位置"的表达，N 很大）
2. **输出是结构化的**（k 个对象、k 个 mask、k 段生成、k 项答案——**可数、离散**）
3. **任务可能动态变化**（不同 prompt、不同类别、不同指令）

问题本质：**如何在一个可微、并行、硬件友好的架构里，把 N 个位置的稠密信息，路由到 k 个结构化输出上？**

## 6.2 可能的架构方案

| 方案 | 机制 | 问题 |
| --- | --- | --- |
| 固定 slot attention | 定义 k 个 slot，每个 slot 通过迭代聚类聚合位置 | 迭代慢、难以控制 slot 语义 |
| **k 个 query + cross-attention** | k 个外生向量主动 attend 稠密特征 | —— |

## 6.3 为什么 query + cross-attention 成为主导形态

**可微** ✓ —— cross-attention 全程可微

**并行** ✓ —— k 个 query 可以同时 attend

**一对一绑定** ✓ —— 输出和 query 天然一一对应

**语义可控** ✓ —— query 从外部喂（SAM/Grounding DINO/prompt）

**模态无关** ✓ —— 只要能 encode 成向量就能当 query

**k 动态** ✓ —— k 每次推理都可以不一样

在当前 Transformer 工具箱和 GPU-friendly 的可微并行约束下，k 个 query + cross-attention 是处理“稠密输入 → 结构化输出”的主导局部最优形式之一。这就是为什么它到处出现。

这不是"伟大发明被不断借鉴"的叙事，而是约束联立后反复逼出的工程稳定点。但它不是数学上的唯一解：slot attention、routing networks、implicit fields、diffusion refinement、energy-based inference、graph message passing 都可以在某些条件下替代或补充它。

## 6.4 关于"外生"的结构压力

"内生 query"（DETR 原版）看起来也行——为什么会强烈走向外生化？

因为**内生 query 只能覆盖训练时见过的任务**。只要任务要开放、要交互、要跨模态，**任务规格必须在推理时才能确定**——所以规格必须从外部喂，而 query 是最自然的任务接口位置之一。

所以 SAM 的"外生化"不是凭空创新，而是 DETR 范式开放化后最稳定的展开方向之一。

---

# §7 · 这个原语的边界——什么任务不适用

为了不把这个论断泛化过头，也要指出它**不适用**的地方：

**(a) 输出不是可数离散的任务**

- 比如深度估计（每个像素一个连续深度值）、光流、超分——输出是稠密场
- 这些任务更适合 U-Net / DPT 这类 dense-to-dense 架构
- 虽然也可以硬套 query（比如 Depth Anything 的 MLP head），但 query 不是核心机制

**(b) k 已知且很小的任务**

- 分类（k=1 输出）——虽然可以用 [CLS] token（这其实就是一个 query token），但机制已经退化到可以直接用 global pooling
- k=1 时 query 机制的优势不明显

**(c) 稠密特征本身不稠密的场景**

- 表格数据、点云稀疏表示——输入不是"N 个位置"的稠密场，query-feature cross-attention 的收益下降

所以论断的**精确版**是：

> **在"输入是稠密表征 + 输出是 k 个结构化单元 + 任务规格可能动态变化"的任务上，"k 个外生 query token + cross-attention" 是当前最强、最常见的接口形态之一。**
> 

这个定义下包含检测、分割、全景、开放词汇、交互分割、in-context 分割、LLM few-shot、visual prompt tuning、多模态大模型的 visual tokenizer 输出等现代 transformer 系的大量交互界面。但它不能抹掉阶段 II 的其他遗产：field、pyramid、object/slot、mask/support、matching/assignment 仍然是同等重要的结构原语。

---

# §8 · 对阶段 III / IV / V 的意义

回到你的谱系语言：

**阶段 II** 的核心是"**稠密穿透**"——从整图分类穿透到每像素。这个阶段结束时留下的不是唯一一个原语，而是一组遗产：field、pyramid、object/slot、mask/support、matching/assignment，以及最具跨阶段外溢能力的 query/prompt。

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

**在阶段 II 出现的 object query，实质上是后面许多阶段的"接口母版"**。FPN、RoIAlign、anchor、mask、assignment 不是无关组件，而是阶段 II 的不同遗产；其中 object query 是最会向后外溢、最容易被跨任务和跨模态复用的接口原语。

这就是为什么我说 DETR 在检测里的命运（被 YOLO 吞掉）**不重要**——DETR 这四代真正留下的是**把 object query 从一个检测 trick 提炼成 transformer 时代通用接口**这件事。之后的每一个基础模型，都在用这个接口。

---

从全书结构看，这一段最适合承担**阶段 II → 阶段 III 的桥梁**功能，而不只是作为 DETR 组的附录。原因在于 object query 在这里已经不再是检测技巧，而是跨任务、跨模态、跨阶段的接口原语；若把它仅仅塞回定位卡页尾，它的本体论分量会被低估。
