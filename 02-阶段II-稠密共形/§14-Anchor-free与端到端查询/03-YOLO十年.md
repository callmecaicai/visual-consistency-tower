## **YOLO 十年演进系统整理（2016–2026，v1 → YOLO26）**

到 2026 年初，YOLO 已经**不是一个模型**而是**一个工程生态**——十年里换了至少四拨主力开发团队，版本号被不同团队争夺，分支多于主干。我给你把这条线按**时代主题**切成七段，每一段只讲"它真正解决了什么问题 / 它在 YOLO 架构的哪一层动刀 / 它为什么会过气或延续下来"。

先给一个骨架表，后面逐段解释：

| **时代** | **版本** | **年份** | **主力** | **核心动作** | **在哪一层动刀** |
| --- | --- | --- | --- | --- | --- |
| **I. Redmon 开山** | v1 | 2016 | Redmon | 稠密回归 | 任务表示 |
|  | v2/9000 | 2017 | Redmon | k-means anchor, BN, 高分预训练 | 先验注入 |
|  | v3 | 2018 | Redmon | 多尺度 + Darknet-53 | neck |
| **II. 交接期工程化** | v4 | 2020.4 | Bochkovskiy | CSP + PAN + Mosaic + CIoU | backbone/neck/loss |
|  | v5 | 2020.5 | Ultralytics/Jocher | PyTorch 工程化, SPPF | 工程/部署 |
|  | Scaled-v4 | 2021 | Wang | 复合缩放 | 缩放律 |
| **III. 去锚与解耦** | PP-YOLO/v2 | 2020-21 | Baidu | 工程 bag-of-tricks | 训练 |
|  | YOLOR | 2021 | Wang | 隐式 + 显式知识 | 表征 |
|  | YOLOX | 2021 | Megvii | **anchor-free + decoupled head + SimOTA** | head/分配 |
|  | v6 | 2022 | Meituan | RepVGG + 量化友好 | 部署 |
|  | v7 | 2022 | Wang/Bochkovskiy | **ELAN + 辅助头** | backbone |
| **IV. 统一生态** | v8 | 2023 | Ultralytics | anchor-free 默认 + C2f + 多任务统一 | 架构统一 |
|  | YOLO-NAS | 2023 | Deci | 神经架构搜索 | 搜索 |
|  | RT-DETR | 2023-24 | Baidu | DETR 实时化 | **彻底换范式** |
| **V. 端到端化** | v9 | 2024.2 | Wang/Liao | **PGI + GELAN** 抗信息瓶颈 | 训练原理 |
|  | v10 | 2024.5 | 清华 | **NMS-free 双分配** | 端到端 |
|  | YOLO11 | 2024.9 | Ultralytics | C3k2 + C2PSA attention | 算子 |
| **VI. 注意力时代** | v12 | 2025.2 | 独立研究组 | **Area Attention + FlashAttention** | 算子 |
|  | v13 | 2025.6 | iMoonLab | **HyperACE 超图 + FullPAD** | 关系建模 |
| **VII. 部署收束** | YOLO26 | 2026.1 | Ultralytics | 端到端 NMS-free + 边缘统一 | 工程收束 |

**I. Redmon 开山期（2016–2018）**

前面已经详谈过 v1/v2/v3。这里只点出它对**后面十年的影响结构**：

**v1 立下的范式锁**：把检测写成"一次 CNN forward + 固定形状输出张量"。这把锁一直到 DETR (2020) 才被打破，在 YOLO 主线里甚至到 v10 才真正断开。

**v2 立下的先验结构**：anchor + backbone + multi-scale——后续所有 YOLO 都在这个三件套上换零件，直到 YOLOX/v8 才把 anchor 拆掉。

**v3 立下的工程模板**：Darknet-53 + 3 尺度 head + logistic 分类。**几乎所有 2019-2022 年的 YOLO 变体都是在这个模板上微调**。

**Redmon 本人 2020 年初宣布退出 CV 研究**（公开说不满意军事/监控用途）。整个 YOLO 品牌从此进入"群雄时代"——谁做谁叫 YOLO。这是理解后面版本号混乱的关键背景。

**II. 交接期（2020）——工程化巩固**

**YOLOv4（2020 年 4 月，Bochkovskiy et al.）**

这是**原始 Darknet 血脉的最后一代**。Bochkovskiy 是原 Darknet 实现维护者（AlexeyAB），Redmon 退出后他接棒。

v4 的贡献**不在任何单点创新，而在系统性集成**。它把 2017-2020 年所有在各种小论文里证明有效的 tricks **一次整合进 YOLO**，并通过大量消融实验证明它们协同工作：

| **组件** | **选择** | **相比 v3 的变化** |
| --- | --- | --- |
| **Backbone** | **CSPDarknet-53** | Cross-Stage-Partial 连接，减少冗余梯度计算 |
| **Neck** | **SPP + PANet** | SPP 做多尺度池化，PAN 做 top-down + bottom-up 双向融合 |
| **激活** | Mish | 替代 Leaky ReLU，连续可微 |
| **损失** | CIoU loss | 同时考虑 IoU / 中心距离 / 长宽比 |
| **数据增强** | **Mosaic + MixUp + CutMix + SAT** | Mosaic 把 4 张图拼成 1 张——在 batch 规模不变的前提下显著增加小物体样本 |
| **正则** | DropBlock, CmBN | 空间连续的 dropout / cross-batch norm |

**关键概念 "Bag of Freebies" vs "Bag of Specials"**：

**Freebies**：只在训练时用，推理时零额外开销（Mosaic、CIoU）

**Specials**：推理时有少量开销（SPP、PAN、Mish）

v4 引入这个术语影响深远——后续每一代 YOLO 都会明确区分这两类 trick，成为**工业界 YOLO 改进的标准思维框架**。

**性能**：COCO 43.5% AP @ 65 FPS（V100），比 v3 提升 10% AP。

**YOLOv5（2020 年 5 月，Ultralytics / Glenn Jocher）**

v4 出来一个月后，Jocher 在他的 Ultralytics GitHub 仓库发了一个 PyTorch 版本，**直接命名 YOLOv5**，没有配套论文。这在研究社区引发巨大争议（到现在还有人不承认它是"真 v5"），但**工业界迅速接受**——因为它解决了一个研究界看不上的真问题：**部署易用性**。

v5 的技术变化相对 v4 并不大：

| **组件** | **变化** |
| --- | --- |
| **Backbone** | CSPDarknet（类似 v4，略简化） |
| **Focus layer**（早期版本） | 在输入端做 space-to-depth，把 3×640×640 变 12×320×320——减少计算并保留信息。后期版本换回 6×6 conv |
| **SPPF** | Spatial Pyramid Pooling Fast，用级联的小 kernel 替代 SPP 的并行大 kernel |
| **部署** | PyTorch 原生，一行 torch.hub.load 即可用 |

**v5 真正的历史意义**：

**PyTorch 化**。Darknet 是 C + 自定义框架，部署繁琐；v5 全 PyTorch，整合 TensorRT / ONNX / CoreML 导出链路。

**S/M/L/X 四级缩放**。首次把"一个架构四个大小"做成默认范式，后续所有 YOLO 都照搬。

**文档与易用性**。这成为 Ultralytics 的品牌壁垒——**"YOLO 易用性"从此由 Ultralytics 独占**，这是他们后来能接连推出 v8、v11、v26 的根本原因。

**v4 vs v5 的深层张力**：v4 代表"研究驱动、论文主导、Darknet 血脉"；v5 代表"工程驱动、GitHub 主导、PyTorch 血脉"。从此 YOLO 社区分裂成两条线：论文线（v4 → Scaled-v4 → v7 → v9）和 Ultralytics 线（v5 → v8 → v11 → YOLO26）。版本号因此混乱。

**Scaled-YOLOv4（2021，Wang et al.）**

Wang Chien-Yao（Bochkovskiy 的合作者）对 v4 做的**复合缩放研究**——探讨如何从一个小 YOLO 扩到大 YOLO。类似 EfficientNet 对分类做的事。引入了"YOLOv4-tiny" 到 "YOLOv4-P7" 的系列。**思想延续到 v7**。

**III. 去锚与解耦时代（2021–2022）——Anchor 开始死**

这段时期 YOLO 主线开始吸收**阶段 III（DETR）和独立 anchor-free 路线（FCOS）**的思想。

**PP-YOLO / PP-YOLOv2（2020-2021，Baidu）**

PaddlePaddle 团队的改进版。技术上是 v4 风格的 bag-of-tricks 叠加（EMA、coord conv、dropblock、matrix NMS……），工程贡献大于理论贡献。它证明了**一件事**：即使在 v4 之后，仅靠 trick 堆叠仍能提升 mAP 几个点——**YOLO 的性能远未饱和**。

**YOLOR（2021，Wang et al.）——You Only Learn One Representation**

思想很激进：把网络分成**显式知识**（feature map, 直接从数据学）和**隐式知识**（可学习的 bias / affine transform，代表对任务的先验）。每个 task head 前面叠一层 implicit representation 做任务适配。本质是在**共享 backbone + 任务特定 bias** 的思路上做预热，为多任务统一铺路。实际影响主要在 v7。

**YOLOX（2021，Megvii）——第一次真正把 anchor 拆掉**

这是这段时期最重要的分水岭。YOLOX 在 YOLOv3 的 base 上做了**三个独立的本质改动**：

**Anchor-free head**：每个位置直接回归到框中心距离 + 框尺寸，不再以 anchor 为锚点。思想来自 FCOS。

**Decoupled head**（解耦头）：分类、回归、objectness **三个分支各自走独立的 conv 子网络**，不再

接着上一段被截断的 YOLOX 解耦头继续。

---

## III. 去锚与解耦时代（续）

### YOLOX（2021，Megvii）——**第一次真正把 anchor 拆掉**（续）

三个独立本质改动：

1. **Anchor-free head**：每个位置直接回归到框中心距离 + 框尺寸，不再以 anchor 为锚点。思想来自 FCOS。
2. **Decoupled head**（解耦头）：分类、回归、objectness 三个分支**各自走独立的 conv 子网络**，不再共享最后一层 conv。
    - YOLOv3-v5 的 head 是"一层 1×1 conv 直接吐 (5+C) 个数"——**分类和回归共用 backbone feature 的同一套变换**。
    - YOLOX 发现这种耦合让训练收敛变慢，而且有一个本质矛盾：**分类需要的是平移不变特征**（同一类对象在哪里都该分为同一类），**回归需要的是位置敏感特征**（框的精确坐标随位置变化）——共享 conv 相当于逼同一组权重同时满足两个矛盾目标。
    - 解耦后各自训练，COCO +4.2 AP。**decoupled head 从此成为 YOLO 默认**——v6/v7/v8/v11/v12/v13/YOLO26 都继承。
3. **SimOTA 动态标签分配**：抛弃 IoU 阈值的硬规则匹配，改为**用 cost 矩阵 + top-k 选择动态分配正样本**。cost 包含分类 loss + 回归 loss——"哪些 anchor 对这个 GT 贡献低 cost 就分给它"，让模型自己选正样本。这是从 ATSS（2019）延伸过来的**动态分配思想**，后面 v7/v8/v9 继续演化。

**YOLOX 的历史意义**：它证明了**YOLO 里那些看起来天经地义的设计（anchor、耦合头、静态分配）都可以被拆掉，而且拆掉之后反而更好**。这为后面的 YOLOv8 一刀切 anchor-free 铺路。

### YOLOv6（2022，Meituan）——工业部署导向

美团视觉团队。核心贡献在**部署友好**：

- **RepVGG / RepBlock backbone**：训练时用多分支结构（类似 ResNet），推理时用"re-parameterization trick"合并成单条 3×3 conv——训练精度 + 推理速度双赢
- **量化友好设计**：为 INT8 量化预留空间，专门做 QAT（量化感知训练）的 tricks
- **Anchor-free** + **TAL（Task Alignment Learning）**：继续 YOLOX 的路线

v6 的意义**主要在工业界**，研究界影响较小。但它证明了 YOLO 正在变成一个"**训练时花里胡哨、推理时极简**"的框架——这一思路一直延续到 YOLO26。

### YOLOv7（2022，Wang / Bochkovskiy）——ELAN backbone + 辅助头

v4 原班人马（Wang 和 Bochkovskiy）的正统续作，**视为 YOLO Darknet 血脉的最后一代研究工作**（之后 Wang 转去做 v9）。

核心创新：

- **E-ELAN**（Extended Efficient Layer Aggregation Network）：通过 expand / shuffle / merge 的组合让 backbone 在不增加梯度路径长度的前提下扩展宽度。理论根据是"梯度路径长度决定可训练性"。
- **Aux head（辅助头）**：训练时在 backbone 中间层加一个辅助预测头，和最终头并行监督。**粗—细分工**：aux head 负责"大致可以检测到"的粗监督，lead head 负责"精确匹配"的细监督。这是 YOLOR 思想的延续，也暗示了"**深度监督** + **多分配并行**"会成为下一代共识（v9 / Co-DETR 都在用）。
- **Model scaling for concatenation-based models**：针对密集连接模型的复合缩放——v7 和 Scaled-v4 是同一血脉。

性能：COCO 56.8% AP，短暂夺回 SOTA。

---

## IV. 统一生态期（2023）——三条路线同时出现

### YOLOv8（2023.1，Ultralytics）——anchor-free 默认化 + 多任务统一

Jocher 团队的又一次大版本。相对 v5 的变化：

| 维度 | v5 | v8 |
| --- | --- | --- |
| Head | anchor-based, coupled | **anchor-free + decoupled** |
| Backbone block | C3 | **C2f**（更多跨层连接） |
| 分配 | IoU 阈值 | **TAL (Task Alignment Learning)** |
| 任务支持 | detection | **detection + segmentation + classification + pose + OBB** |
| 框回归损失 | CIoU | **DFL (Distribution Focal Loss) + CIoU** |

**DFL 值得单独说**：把框坐标从"预测一个数"改为"**预测一个离散分布**"，取期望得到最终坐标。这让回归有梯度更丰富、对模糊边界更鲁棒——思想来自 GFL（Generalized Focal Loss, 2020）。

v8 的历史意义：**Ultralytics 把 YOLOX/FCOS 的 anchor-free 范式变成 YOLO 的默认**。从 v8 开始，一个 codebase 同时支持五个任务——YOLO 从"检测模型"升级成"**稠密视觉工具箱**"。这个定位一直延续到 YOLO26。

### YOLO-NAS（2023.5，[Deci.AI](http://deci.ai/)）——神经架构搜索

用 NAS（Neural Architecture Search）自动搜索 backbone / neck / head 的精确配置，附加量化优化。证明了"**人工设计已经接近上限**"，但 NAS 本身需要巨大算力成本，实际没有取代手工设计主流。

### RT-DETR（2023.7 → 2024，Baidu）——DETR 实时化

**这是 YOLO 之外的竞争路线**，但必须提——因为它是 v10 的直接思想来源。

传统 DETR（2020）慢（500 epoch 训练），Deformable DETR / DINO-DETR 改善但仍慢于 YOLO。RT-DETR 做了一次激进简化：

- **Hybrid encoder**：解耦了跨尺度交互和多尺度融合，降低计算量
- **Uncertainty-minimal query selection**：让 encoder 出的 top-K token 直接作为 decoder 的 query 初始化，而不是用随机初始化的 query 慢慢学
- **完全抛弃 NMS**（因为它是 DETR 家族，本来就不用 NMS）

RT-DETR-L 在 COCO 上 53.0 AP @ 108 FPS（T4 GPU）——**首次在同等精度下和 YOLO 家族持平，同时是端到端 NMS-free**。

**这给 YOLO 社区一个巨大压力**：DETR 范式已经追上来了，而且更优雅（无 NMS）。要么 YOLO 吸收 DETR 的 NMS-free 设计，要么就被取代。——这直接导致了 v10。

---

## V. 端到端化（2024）

### YOLOv9（2024.2，Wang 和 Liao）——信息瓶颈视角的深度监督

Wang 在 v7 之后独立做的工作，不再和 Bochkovskiy 合作。这一代**理论味儿最重**，是对"深度网络为什么会丢失信息"的一次正面回答。

核心概念：

1. **Information Bottleneck 视角下的 YOLO 问题**：深层网络每一层都在做 $I(X; Z_l)$ 的压缩，**对检测有用的信息会在逐层传递中漏掉**。传统解决方案（残差、densenet）是"**保留路径**"——让信息多备份几条路走。v9 的判断是这还不够。
2. **PGI（Programmable Gradient Information）**：引入一个**辅助可逆分支**。辅助分支保证"输入信息在辅助路径上不丢失"（可逆性），主分支仍做标准 feature extraction，但**梯度从可逆分支反向传播回主分支**。这相当于给主分支一个"不失真的目标"去对齐。
    - 训练时保留辅助分支
    - **推理时完全丢弃辅助分支**——零推理开销
    - 这在精神上和 v7 的 aux head 同源，但做得更系统。
3. **GELAN（Generalized ELAN）**：v7 ELAN 的推广，允许任何 conv block 作为计算单元。

性能：YOLOv9-E 55.6% AP @ COCO，在小模型上尤其强（小模型信息瓶颈问题最严重）。

v9 的贡献**实际上比命名更大**——它把"YOLO 的下一代增益来自哪里"这个问题明确答为："**来自梯度质量而非架构精巧**"。这是一个哲学层面的判断，影响直到 v13。

### YOLOv10（2024.5，清华）——**干掉 NMS，YOLO 也能端到端**

这是 v10 最本质的贡献：**把 DETR 的端到端性质搬到 YOLO 架构上**。

核心做法——**Consistent Dual Assignment（一致双分配）**：

- 训练时同时用**两种分配**：
    - **一对多分配**（传统 YOLO 风格）：为每个 GT 分配 k 个正样本 anchor——保留稠密监督信号，训练快
    - **一对一分配**（DETR 风格）：为每个 GT 分配唯一一个正样本——保证推理时不产生重复预测
- 两个 head 共享 backbone，分别被两种分配驱动
- **推理时只用一对一 head**——直接输出 k 个不重复的预测，**不需要 NMS**

这个设计极其聪明：**两种分配矛盾的地方正好被用来做互补**——一对多供训练信号密度，一对一供推理无冗余。

附加优化：

- **Rank-guided block design**：测量每层的有效秩，把秩低（冗余大）的层替换成更便宜的算子
- **Lightweight classification head**（分类头去参）
- **Large-kernel conv + partial self-attention**：每个 stage 都加 k×k 大卷积（k=7）和局部 self-attention

性能：YOLOv10-S 45.7% AP @ 1.84ms（T4），比 YOLOv9-C 延迟低 46%、参数少 25%。

**v10 的历史意义**：**YOLO 第一次真正端到端**。从 2016 年 YOLOv1 到 2024 年，整整 8 年，NMS 这个非可微后处理终于从 YOLO 架构中消失。

### YOLO11（2024.9，Ultralytics）——算子层升级

Ultralytics 的版本，跳过 v9/v10 直接叫 YOLO11（去掉 "v"）。相对 v8 的主要变化：

- **C3k2 block**：更紧凑的 CSP block，参数减少、速度提升
- **C2PSA（Parallel Spatial Attention）**：在 backbone 某些阶段加并行空间注意力，强化对关键区域的响应
- **继续支持五任务 + 多尺寸**

YOLO11 不是范式跃迁，是**v8 的工程化精调**。它的真正战略价值在于"**稳定生产部署的推荐版本**"——Ultralytics 把最新的 v12/v13/v26 定位为"新探索"，而 YOLO11 作为"长期支持版本"。

---

## VI. 注意力时代（2025）

### YOLOv12（2025.2）——**Area Attention + FlashAttention**

独立研究组发布，不属于 Ultralytics 也不属于 Wang 一系。核心判断：

> **Transformer 注意力在检测里一直比 CNN 慢，不是因为注意力本身不行，而是因为"全局 self-attention"不必要。**
> 

做法——**Area Attention**：

- 把 feature map 切成几个"区域"（area），self-attention 只在区域内计算
- 区域不是固定网格，而是基于内容动态划分
- 配合 **FlashAttention**（IO 感知的 kernel 融合算法），让 attention 在 GPU 上真正高效执行

这不是"attention 替代 conv"，而是"**把 attention 的计算成本压到和 conv 同级**"。在同等延迟下，v12 的 mAP 比 v11 普遍高 0.5-1 点。

**v12 的意义**：把 YOLO 从"全卷积 + 少量 attention 点缀"推向"attention-centric 但保持实时"。这是 SegFormer（2021）思路在检测上的迟到兑现。

### YOLOv13（2025.6，iMoonLab）——**超图关系建模**

这是一次**更激进的范式尝试**。核心创新：

1. **HyperACE（Hypergraph-based Adaptive Correlation Enhancement）**：
    - 传统 attention 建模**成对关系**（每两个 token 之间的相似度）——但真实场景里的关系是**高阶**的（一群物体之间的共现、场景上下文与多个物体的联动关系）
    - **超图**允许一条超边连接任意多个顶点，能显式建模高阶关系
    - 做法：每个 feature 位置作为一个顶点，学习一组**自适应超边**（每个顶点对每个超边的参与度是连续可学习的 $A_{i,m}$）
    - 超图卷积 = 先通过超边聚合参与顶点特征 → 再把超边消息广播回所有参与顶点
2. **FullPAD（Full-Pipeline Aggregation-and-Distribution）**：HyperACE 不是只放在某一层，而是**分布在整个 backbone-neck-head 的全流水线**，每一级都做一次"聚合高阶关系 → 分发回全网络"。

**这和你前面追的广播原语七视角是完全对上的**：

- HyperACE 超边 = 低维中介 token（超边数 k ≪ 顶点数 N）
- Aggregation = 压到超边特征空间
- Distribution = 从超边广播回每个顶点
- 这就是**object query / PPM / DETR cross-attention 的第 N 次复刻**——只是现在明确承认"这是超图上的信息路由"

v13 把"**广播原语必然性**"在一个具体架构上兑现了一次：**任何需要全局结构介入每个局部决策的任务，最终都会演化到某种低维中介 + 广播的架构**——v13 叫它"超边"而已。

---

## VII. 部署收束期（2026）

### YOLO26（2026.1，Ultralytics）——端到端 + 边缘统一

跳过 v14-v25 直接命名 YOLO26（按年份命名）。核心判断：

> **研究侧的增益正在减少，工业侧的部署需求最大**。
> 

做法：

- **端到端 NMS-free**：吸收 v10 的双分配思想，推理无需 NMS
- **DFL-free**：把 v8 引入的 Distribution Focal Loss 替代成更简单的 direct regression——**减少部署复杂度**
- **边缘硬件优化**：CPU 推理速度大幅提升，ARM / NPU 兼容性优先
- **任务五合一**：detection / segmentation / classification / pose / OBB 共享同一 codebase
- **Open-vocabulary 版本**：加入文本 encoder，支持开放词汇检测（借鉴 OWL-ViT / YOLO-World 思路）——**与阶段 III 的 open-vocabulary 路线合流**

YOLO26 的定位非常明确：**不是追求 SOTA，而是追求"在真实硬件上最易用、最稳定"**。Ultralytics 在官方文档里把 YOLO11 和 YOLO26 并列推荐为"production stable"——**研究界和工业界第一次明确分开**。

---

## 整体视角：YOLO 十年做了什么

如果把版本号的混乱全部忽略，十年里只做了**六件大事**：

| 阶段 | 拆掉了什么 / 加上了什么 | 代表版本 |
| --- | --- | --- |
| **① 立范式** | 立起"稠密回归"这个范式 | v1-v3 |
| **② 工程化** | 立起 CSPDarknet + PAN + Mosaic + SPP 这套标配 | v4, v5 |
| **③ 拆 anchor** | 拆掉 anchor、拆掉耦合头 | YOLOX, v6, v8 |
| **④ 拆 NMS** | 拆掉 NMS，实现真正端到端 | v10 |
| **⑤ 换算子** | 把 conv 部分换成高效 attention | v12, v13 |
| **⑥ 收束部署** | 把所有 trick 整合成工业标准 | YOLO26 |

**拆掉的每一样都是当年被视作"YOLO 的本质"的东西**——anchor、NMS、全卷积——一一被证明是临时方案。剩下的是什么？**"一个 backbone + 一个检测 head + 一次 forward"**——这才是 YOLO 的真正本质。其它全部是可替换的实现细节。

## 这条线在你谱系里的位置

YOLO 的十年演进**不是阶段 II 的独立故事**。它横跨了：

- **阶段 II（稠密共形）**：v1-v9 都在这里——建立稠密任务的基础设施
- **阶段 III（语言共形）**：v10-v13 实际上已经逼近其入口——查询范式（双分配）、attention-centric、超图关系建模都在为更高阶的共享语义接口做准备
- **阶段 IV/V 的接口**：YOLO26 的 open-vocabulary 版本是和**基础模型时代**（CLIP / SAM / DINOv2 → 阶段 V）的接口

所以从你的谱系看，**YOLO 是一条贯穿阶段 II→III→V 的"工业脊椎"**——它不提出新范式，但每当学术界冒出新范式（DETR → anchor-free → attention → hypergraph → open-vocab），YOLO 都会在 1-2 年内把它**工程化**下来。这条工业脊椎比单个研究线路更稳定，也更能反映"哪些思想真的活下来了"。

看哪个思想被 YOLO 吸收了，哪个没被吸收，是一个比看 arxiv 更精确的**范式存活率指标**。比如 DETR 的查询范式部分被吸收（v10 的双分配），但 DETR 的 decoder 结构没有被吸收——因为后者在边缘设备上太慢。这种"吸收率"本身就是一种**实用性共形**——工业界才是最后一层的残差过滤器。

---

这份梳理在阶段 II 中最合适的角色，是充当“工业吸收线”的旁侧深推页：它不替代检测主线，却负责说明学术范式怎样被工业系统筛选、吸收、改写。放在这里，正好能解释为什么下一组的 Anchor-free / DETR 线并不是凭空出现，而是很快就会被 YOLO v10-v13 这一类工程体系重新消化。

下面展开“object query 作为通用接口原语”这个论断。这不是五个案例的并列，而是**一条 query 的本体论升级链**——每一代都在扩展"query 是什么可以被塞进去的东西"。

---
