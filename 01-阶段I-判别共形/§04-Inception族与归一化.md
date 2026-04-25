# 阶段 I · §4 · Inception 族与归一化（GoogLeNet / BatchNorm / Inception v3 / Inception-v4）

作者 / 机构: Szegedy 等 / Ioffe-Szegedy / Google Brain
共形维度: 动力, 度量, 材料
关键贡献: 用稀疏+多尺度分支把宽度做厚；BN 原论文以 internal covariate shift 解释其作用，但从大厦角度更重要的是批统计接管层间尺度调节，共同把非残差路线的可训深度和工程性能推到高点。
年份: 2017
序号: 4
残差 / 它催生了什么: 多分支架构手工味过重；BN 稳住层间尺度但未从拓扑上解决深层退化 → 残差连接从根上改写。
类型: 架构, 训练技术
阶段: I · 判别共形的奠基

<aside>
🧭

**章首协议（七栏版）**：

| 项 | 本章回答 |
|---|---|
| 零度设定 | 单柱深度难以继续，宽度、多尺度和 batch 统计必须进入闭合。 |
| 反面 / 无 | 只靠堆深会遇到尺度、分支效率和层间分布稳定性问题。 |
| 成为 | Inception 与 BN 让多尺度分工和批统计调节成为判别工艺。 |
| 闭合制度 | `C_04=(Z_branch/batch, Π_label, Γ_scale/batch, M_ImageNet/CE, D_Inception/BN)` |
| 成功标准 | 非残差路线的分类性能和工程深度达到高点。 |
| 遮蔽对象 | 手工分支和 batch 依赖仍不能从拓扑上解决深层状态更新。 |
| 内在残差 | 50+ / 100+ 量级的主导稳定机制转向残差路径。 |

</aside>

---

## 本页命题等级表

| 命题 | 等级 |
| --- | --- |
| Inception 引入多尺度并行、1×1 瓶颈与稀疏分支近似 | F |
| BN 最初以 internal covariate shift 被解释，但也可读作批统计接管层间尺度调节 | F/M |
| Inception-ResNet 表明多尺度分支继续存在，但深层训练主导稳定机制转向残差路径 | F/M |
| Inception 四条基因在 FPN、U-Net、MobileNet、Swin、SAM 等后续路线中回流 | G |
| “主干范式更替，技术基因长期保留”是架构史的谱系归纳 | G/P |

<aside>
📍

**本页坐标** · 阶段 I「判别共形的奠基」· 第 4 / 5 页

**总纲对位** · 共形维度：**材料 × 度量 × 动力** · 非残差路线的工艺极限 + Inception 基因向整个视觉生态的扩散

**衔接** · 上游：[阶段 I · §3 · 激活 · 初始化 · 正则：训练工艺的共形修正（Xavier / ReLU / PReLU+He / Dropout）](§03-激活·初始化·正则.md) · 下游：[阶段 I · §5 · 优化器与残差革命（Momentum / Adam / ResNet / Pre-activation / DenseNet）](§05-优化器与残差革命\00-定位卡.md)

</aside>

<aside>
🎯

**本页核心命题**：当深度单条柱子堆不上去时，宽度、稀疏分支与归一化一起登场。四篇文献给出「非残差路线」的工艺极限。但更深的命题是——**Inception 路线被残差范式吸收，而非简单失败**；它的四条技术基因（G1/G2/G3/G4）没有消亡，而是被拆解进整个视觉生态。这是阶段 I 进入残差革命前留下的重要遗产。

</aside>

- 📑 本页目录
    - **第一部分 · 文献骨架（四张定位卡）**
        - §1.1 GoogLeNet / Inception v1 — 宽度与多尺度并联
        - §1.2 BatchNorm — 归一化革命的母题
        - §1.3 Inception v2/v3 — 架构工程学的教科书
        - §1.4 Inception-v4 / Inception-ResNet — 被残差路线吸收
    - **第二部分 · 本页合力的残差**
        - §2 面向 §05 残差革命的入口形状
    - **第三部分 · Inception 遗产图谱：被吸收的技术基因**
        - §3 Inception 的四条基因与它们的分化谱
        - §4 G1 的演化——从「单层多尺度」到「多层级多分辨率」
        - §5 G2 的演化——FPN 家族（跨层级特征金字塔）
        - §6 G2 的另一条分支——U-Net 家族（编解码器多尺度）
        - §7 G3/G4 的演化——1×1 瓶颈与深度可分离卷积（移动端架构线）
        - §8 Transformer 时代的 Inception 影子
        - §9 一张遗产全景图
        - §10 最终观察：四种基因在现代视觉里的现状

---

# 第一部分 · 文献骨架（四张共形定位卡）

<aside>
🌐

**主题**：当深度单条柱子堆不上去时，宽度、稀疏分支与归一化一起登场。四篇文献给出「非残差路线」的工艺极限。

</aside>

## §1.1 · GoogLeNet / Inception v1 — *Going Deeper with Convolutions* (Szegedy et al., 2015)

**共形贡献**：Inception 模块 = 同层多尺度并联的稀疏卷积。用 1×1 瓶颈把参数量压到 AlexNet 的 1/12。首次证明**宽度（分支多样性）**和深度一样重要。

🔗 [https://arxiv.org/abs/1409.4842](https://arxiv.org/abs/1409.4842)

## §1.2 · Batch Normalization — *Accelerating Deep Network Training by Reducing Internal Covariate Shift* (Ioffe & Szegedy, 2015)

**共形贡献**：BN 最初以 internal covariate shift 被解释；从本大厦角度，它更重要的是把批统计引入层间尺度调节，使深层训练的度量稳定性被外部 batch 结构接管。学习率提升 30×，初始化敏感性大幅下降——**这是深度网络第一次变得"便宜"**。BN 也是后续所有归一化家族（LN、GN、IN）的母题。

🔗 [https://arxiv.org/abs/1502.03167](https://arxiv.org/abs/1502.03167)

## §1.3 · Inception v2/v3 — *Rethinking the Inception Architecture for Computer Vision* (Szegedy et al., 2016)

**共形贡献**：把 5×5 分解为两个 3×3，把 n×n 分解为 1×n + n×1；引入 label smoothing 正则。架构工程学的教科书式范例。

🔗 [https://arxiv.org/abs/1512.00567](https://arxiv.org/abs/1512.00567)

## §1.4 · Inception-v4 / Inception-ResNet — *Inception-v4, Inception-ResNet...* (Szegedy et al., 2017)

**共形贡献**：多尺度分支可以继续存在，但深层训练的主导稳定机制转向残差路径。Inception-ResNet 是 Inception 路线被残差范式**吸收**的公开节点，而非简单失败。

🔗 [https://arxiv.org/abs/1602.07261](https://arxiv.org/abs/1602.07261)

<aside>
🔄

**四张卡的内在分工**：

- **GoogLeNet / Inception v1** ——推出**宽度 × 稀疏分支**的组合，证明单条柱子不是唯一答案
- **BatchNorm** ——用**层间归一化**和批统计尺度调节，让深度训练稳定性上一个数量级
- **Inception v2/v3** ——用**卷积分解与正则化**把架构工程学推到教科书水平
- **Inception-v4 / Inception-ResNet** ——多尺度分支继续存在，但深层训练的主导稳定机制转向残差路径——「非残差路线被残差范式吸收」

四者合起来证明两件事：（1）**非残差路线能打到十分深入的工艺**——宽度、归一化、分解、正则缺一不可；（2）**但最终被残差范式吸收**——阶段 I 的终点主线既定。

</aside>

---

# 第二部分 · 本页合力的残差

## §2 · 面向 §05 残差革命的入口形状

Inception 的宽度+BN 把可训练深度拓到 50 层量级。下一页的残差连接不是「又一次架构调参」，而是几何上改写了梯度路径——可训练深度的上限被显著抬高。

<aside>
➡️

**残差传递**：本页不是阶段 I 的终点，而是非残差路线的工艺极限。宽度、分支、卷积分解与 BN 共同扩大了判别闭合半径，但它们仍没有从拓扑上改写深层梯度路径。下一页 [阶段 I · §5 · 优化器与残差革命（Momentum / Adam / ResNet / Pre-activation / DenseNet）](§05-优化器与残差革命\00-定位卡.md) 将把状态保留与差异更新分离出来，完成阶段 I 的架构侧封顶。

在进入阶段 II 之前，还需要先通过 [阶段 I · §6 · 标签制度的异化](§06-标签制度的异化.md) 审计分类成功本身遮蔽了什么。

</aside>

---

# 第三部分 · Inception 基因的跨阶段回流图谱

<aside>
🧬

**第三部分的定位**：以下不是阶段 I 的内部展开，而是阶段 I 形成的多尺度、分支、瓶颈与稀疏近似基因在后续阶段的回流与变形。表面上 ResNet 成为更强的主干范式，Inception-v4 / Inception-ResNet 则把残差短路吸收到 Inception 内部。但 Inception 不是简单失败，它是被**拆解吸收**到整个视觉生态里。本部分把四条基因（G1/G2/G3/G4）的分化谱完整铺开，直到 ConvNeXt、Swin、SAM 这一代全部指认。

</aside>

好。Inception 这套"多尺度 + 稀疏分支 + 瓶颈"的 DNA 在视觉领域的扩散极其广泛——可以说，如果你打开 2016 年之后任何一个视觉模型的源码，里面都能找到至少一个 Inception 的直接后代。下面系统梳理一下这张"遗产图谱"。

---

## §3 · Inception 的四条基因与它们的分化谱

先把原始 Inception 模块的技术 DNA 分解清楚，这样后面的演化才有脉络可循：

| 基因 | 含义 | 主要后裔 |
| --- | --- | --- |
| **G1: 多尺度并行** | 同层并联多个感受野 | SPP、PPM、ASPP、Res2Net、HRNet |
| **G2: 跨层级融合** | concat 聚合不同层信息 | FPN、PANet、BiFPN、U-Net |
| **G3: 1×1 瓶颈** | 用 1×1 压缩通道 | ResNet bottleneck、MobileNet、SE-Net |
| **G4: 稀疏分支近似稠密** | 分支化替代稀疏矩阵 | Xception、ShuffleNet、ResNeXt |

下面一条条展开。

<aside>
💎

**§3 要义**：Inception 模块不是一个单一架构，而是**四条技术基因的耦合**：G1 多尺度并行、G2 跨层级融合、G3 1×1 瓶颈、G4 稀疏分支近似稠密。这四条基因**各自独立演化**，各自长出一条后裔谱系，这是 Inception 遗产在当代视觉里无处不在的根本原因。

</aside>

---

## §4 · G1 的演化——从"单层多尺度"到"多层级多分辨率"

这是 Inception 最核心的基因，也是演化最丰富的一条。

### §4.1 第一波：SPP / PPM / ASPP（2014-2017）

**SPP (Spatial Pyramid Pooling, He et al., 2014)**

- 何恺明在 ResNet 之前的工作
- 在 feature map 上做多个尺度的池化（1×1、2×2、4×4），然后 concat
- 第一次把"金字塔"这个词正式引入深度学习
- 最初用途：让 CNN 接受任意尺寸输入（不再需要 resize）
- **与 Inception 的关系**：Inception 是"并联多尺度卷积"，SPP 是"并联多尺度池化"——同一个哲学的两种实例化

**PPM (Pyramid Pooling Module, PSPNet, 2017)**

- 中大/商汤的经典工作
- 在 backbone 输出上做 1×1、2×2、3×3、6×6 的自适应池化
- 每个尺度后接 1×1 conv 降维，最后 concat + 上采样
- **用途**：语义分割（PSPNet 拿下 ImageNet scene parsing 2016 冠军）
- **本质**：把 Inception 的多尺度从"细节纹理"搬到"全局上下文"——用于需要理解"整幅图"的任务

**ASPP (Atrous Spatial Pyramid Pooling, DeepLab v2/v3, 2016-2017)**

- Google 团队（Chen Liang-Chieh 等）的核心创新
- 用**空洞卷积**（dilated/atrous conv）做并行分支——dilation rate = 6, 12, 18, 24
- 不需要下采样就能获得大感受野
- **与 Inception 的关系**：Inception 用不同尺寸的 conv 扩大感受野（3×3、5×5），ASPP 用不同空洞率的 conv（3×3 但 dilation=6/12/18）——**同样的哲学，更高效的实现**
- DeepLab v3+ 里还加了 image pooling 分支（借鉴 PPM），进一步合流

**这三个工作的共同逻辑**：**密集预测任务（分割、深度估计）比分类更需要多尺度**。分类只要"是不是猫"，分割要"每个像素的语义"——像素级任务的难点就是**同一张图里物体尺度差异巨大**。Inception 的多尺度基因天然适合这个场景。

### §4.2 第二波：把多尺度放进残差块里（2019）

**Res2Net (Gao et al., 2019)**

这是一个非常聪明的工作——它问：**为什么多尺度必须在层和层之间？能不能在一个 block 内部就获得多尺度？**

Res2Net 把 ResNet 的 bottleneck 中间的 3×3 conv 做了个改造——把通道切成 $s$ 组，让后面的组接收前面的组处理过的结果：

```
x → split into s groups →
  group 1: pass through
  group 2: 3×3 conv
  group 3: 3×3 conv(group 2 output + group 3 input)
  group 4: 3×3 conv(group 3 output + group 4 input)
  ... → concat
```

这样一个 3×3 conv 等效地产生了多个不同感受野的输出——**Inception 的多尺度思想被折叠进了残差块内部**。几乎零额外参数，但精度普遍提升 1-2%。

**SKNet (Selective Kernel Network, 2019)**

- 并联 3×3 和 5×5 分支（真正的 Inception 结构）
- 用注意力机制**动态选择**哪个尺度更重要
- 这是"Inception + attention"的融合

### §4.3 第三波：多分辨率并行主干（HRNet, 2019）

**HRNet (High-Resolution Network, Sun et al., 2019)**

这是 Inception 多尺度基因的**极限形式**——整个主干网络始终保持多个分辨率的分支并行，而不是像传统 CNN 那样不断下采样。

```
Stage 1: [1/4 分辨率]
Stage 2: [1/4] [1/8]
Stage 3: [1/4] [1/8] [1/16]
Stage 4: [1/4] [1/8] [1/16] [1/32]
```

各分辨率之间**持续交换信息**（upsample + downsample + element-wise sum）。

**这是 Inception 哲学的终极实现**——多尺度不再是"单层内的并联"，而是"整个网络的并联"。在姿态估计、语义分割、关键点检测上是多年 SOTA。

<aside>
💎

**§4 要义**：G1 多尺度并行的演化是**从尺度作为「感受野」到尺度作为「分辨率」的越层升级**：SPP/PPM/ASPP 把尺度扩到全局上下文→ Res2Net/SKNet 把尺度折进残差块→ HRNet 把尺度扩到整个主干。密集预测任务天然需要多尺度——这条基因在2025 年仍在扩张。

</aside>

---

## §5 · G2 的演化——FPN 家族（跨层级特征金字塔）

这是你主动提到的那一条，也是**在工业界应用最广**的一条。FPN 本质上把 Inception 的"分支 concat"从**单层内**搬到了**层级间**。

### §5.1 FPN 本身（2017）

**Feature Pyramid Network (Lin et al., 2017)** - He Kaiming + RBG 组

**问题起点**：检测任务里，小物体（远处的车、人脸）需要高分辨率特征，大物体需要高语义特征。传统做法（SSD）是从不同深度抽特征，但**浅层特征语义弱**。

**FPN 的解**：**自上而下**做特征融合——

```
深层（高语义/低分辨率） ────┐
                              ↓ upsample
中层 + 1×1 ─────────────→ element-wise sum
                              ↓ upsample
浅层 + 1×1 ─────────────→ element-wise sum
```

每一层得到的融合特征 = **高语义 + 高分辨率**。

**为什么这是 Inception 的后代**：

- Inception 在**同一层**并联多尺度 conv，然后 concat
- FPN 在**多层之间**做多尺度聚合，然后 element-wise sum

同一个"多尺度融合"哲学，只是尺度维度从"感受野大小"换成了"网络深度"。

**FPN 影响巨大**：

- Mask R-CNN、RetinaNet、Cascade R-CNN、PANet 全部基于它
- 成为两阶段检测器的**默认组件**
- 语义分割、实例分割、全景分割都用它

### §5.2 PANet（2018）——双向 FPN

**Path Aggregation Network (Liu et al., 2018)**

FPN 是自上而下单向的。PANet 补了**自下而上**的第二条路径：

```
FPN (top-down) → PAN (bottom-up) → 输出
```

低层精细细节 → 也能反向流到高层。**双向融合比单向更完整**。

PANet 是 YOLO v4/v5/v7 的核心 neck 结构。

### §5.3 BiFPN（2019）——带权可学习的双向融合

**EfficientDet 里的 BiFPN (Tan et al., 2019)**

BiFPN 的三个改进：

- **移除只有一个输入的节点**（简化拓扑）
- **给每条跨层融合路径加可学习权重**：$O = sum_i w_i cdot I_i / (epsilon + sum w_j)$
- **重复堆叠 BiFPN 块**（像 Transformer 一样堆）

这是 FPN 的"可微架构搜索"版本——让网络自己决定哪条跨层路径更重要。

### §5.4 NAS-FPN（2019）——搜索出来的 FPN

Google 用神经架构搜索搜出来的 FPN 拓扑，比手工设计的 FPN 强一截——**证明 FPN 的"最优拓扑"还没被人类穷尽**。

### §5.5 FPN 家族总结

| 架构 | 特点 | 典型应用 |
| --- | --- | --- |
| FPN | 自上而下单向 | Mask R-CNN, RetinaNet |
| PANet | 双向 | YOLO v4+ |
| BiFPN | 双向 + 可学习权重 + 堆叠 | EfficientDet |
| NAS-FPN | 搜索出来的拓扑 | Google 内部 |
| Recursive FPN | 把 FPN 本身递归堆叠 | DetectoRS |

**一句话总结**：**FPN = 把 Inception 的多分支思想跨层级展开的工业标准件**。现代任何检测/分割模型都有一个 FPN-like 的 neck。

<aside>
💎

**§5 要义**：FPN 把 Inception 「多分支 concat」的基因从**单层内**搬到**层级间**，成为现代检测/分割模型的**工业标准 neck**。Mask R-CNN → RetinaNet → YOLOv4/5/7 → EfficientDet → Mask2Former ——每个身上都带着 Inception G2 基因的直接后裔。

</aside>

---

## §6 · G2 的另一条分支——U-Net 家族（编解码器多尺度）

FPN 主要服务检测；**U-Net 走的是"对称编解码器 + 跳接"的路线，在密集预测**（分割、深度、重建、生成）领域统治多年。

### §6.1 U-Net（2015）

**Ronneberger et al., 医学影像分割**

```
Encoder: 下采样 4 次，提取语义
Decoder: 上采样 4 次，逐步恢复分辨率
Skip connections: 把 encoder 每一层的特征 concat 到 decoder 对应层
```

**和 Inception 的关系**：U-Net 的 skip connection 做的是**跨层级多尺度融合**——decoder 既有深层语义（来自底部），也有浅层细节（来自 skip）。这是 Inception "多尺度 concat" 思想在**时间反向维度上**的展开（encoder 走一遍下采样，decoder 再走一遍上采样+融合）。

### §6.2 U-Net 的后代

- **SegNet (2015)**: 用池化索引做上采样，不用 skip concat
- **U-Net++ (2018)**: skip 连接变成嵌套稠密结构（DenseNet 思想）
- **U-Net 3+ (2020)**: 每个 decoder 层都接收所有 encoder 层
- **DeepLab v3+ (2018)**: Encoder 用 ASPP（pyramid pooling）+ Decoder（简化 U-Net）——**这直接把 G1 和 G2 两条基因合流**
- **nnU-Net (2020)**: 医学影像通用框架
- **Stable Diffusion 的 U-Net**: 扩散模型的去噪主干——**U-Net 在生成领域被 Transformer 取代之前的终极形态**

**U-Net 的真正哲学**：**任何"输入和输出尺寸相同"的密集预测任务都适合 U-Net 结构**。分割、深度估计、去噪、超分、光流、图像翻译、扩散模型——全都用它。

<aside>
💎

**§6 要义**：U-Net 把 G2 的「多尺度 concat」思想展开为**对称编解码器 + skip connection**的拓扑。任何输入输出同尺寸的密集预测任务都用它——分割、扩散模型、超分、深度估计。DeepLab v3+ 把 G1（ASPP）与 G2（编解码器）**在同一个架构里合流**。

</aside>

---

## §7 · G3/G4 的演化——1×1 瓶颈与深度可分离卷积（移动端架构线）

这条线走向了**效率极致**——把 Inception 的"稀疏分支近似"思想推到硬件友好的极限。

### §7.1 Xception（2017）——"极限 Inception"

**Xception = eXtreme Inception (Chollet, 2017)**

Francois Chollet（Keras 作者）明确说：**我要把 Inception 的假设推到极限**。

Inception 的假设是：**空间相关性和通道相关性可以部分解耦**（多分支本质上在做这个）。

Xception 说：**那就让它们完全解耦**——

- Depthwise conv: 每个通道独立做 3×3（只管空间相关性）
- Pointwise conv (1×1): 跨通道做 1×1（只管通道相关性）
- 堆叠二者 = 完整的卷积

这就是 **depthwise separable convolution**。参数量从 $k^2 C_{\text{in}} C_{\text{out}}$ 降到 $k^2 C_{\text{in}} + C_{\text{in}} C_{\text{out}}$——**几乎一个数量级的压缩**。

### §7.2 MobileNet 家族（2017-2019）

Google 的移动端专用架构：

- **MobileNet v1 (2017)**: 就是 Xception 的移动端工程版，加上 width multiplier
- **MobileNet v2 (2018)**: **Inverted residual + linear bottleneck**——先 1×1 expand，再 depthwise，再 1×1 project，外加残差。这里 1×1 瓶颈（Inception 基因）和 residual 连接（ResNet 基因）合流
- **MobileNet v3 (2019)**: 加入 SE 模块（通道注意力）+ h-swish 激活 + NAS 搜索

### §7.3 ShuffleNet / GhostNet

**ShuffleNet (2018)**: 分组卷积 + channel shuffle 打破组间壁垒——另一种"稀疏近似"

**GhostNet (2020)**: 用 1×1 + cheap linear ops 生成"幽灵特征"——进一步压缩

### §7.4 EfficientNet（2019）

**Tan & Le, 2019**

Google 的复合缩放研究——在 MobileNetV2 风格的 MBConv（Inverted Residual）基础上，系统地缩放深度/宽度/分辨率。

EfficientNet 的 MBConv 块里能看见:

- **Inception 的 1×1 瓶颈**
- **Xception 的 depthwise separable**
- **ResNet 的残差**
- **SENet 的通道注意力**

**四种基因在一个 block 里合流**。这就是为什么说 Inception 没死——它作为一个架构死了，但它的基因在 EfficientNet 里活得比任何单一路线都长。

### §7.5 ConvNeXt（2022）——CNN 的终极形态

**Liu et al., 2022**

ConvNeXt 是 CNN 对 Transformer 的回应——在不用 attention 的前提下，把 ResNet 改造得尽可能像 Swin Transformer。关键修改：

- 7×7 depthwise conv（Inception/Xception 的 depthwise 基因）
- inverted bottleneck（MobileNet v2 的 1×1 expand-project 基因）
- LayerNorm（Transformer 的 LN 基因）
- GELU（Transformer 的激活基因）
- 更大 kernel、更少 activation

**ConvNeXt 证明**：把 Inception-Xception-MobileNet 路径上积累的所有优化用好，纯 CNN 可以追平 Swin Transformer。

<aside>
💎

**§7 要义**：G3/G4 的演化造就了整个**移动端/效率优化架构线**：Xception 把 Inception 的稀疏假设推到极限 → MobileNet v1-v3 把它工程化 → EfficientNet 把四条基因全部合流 → ConvNeXt 证明纯 CNN 可以追平 Swin。**Inception 的技术遗产在每个手机摄像头背后都在运行**。

</aside>

---

## §8 · Transformer 时代的 Inception 影子

很多人以为 Transformer 取代了 CNN 就把 Inception 的遗产彻底埋了——其实不是。**多尺度和金字塔思想在 Transformer 里被重新发明了**。

### §8.1 PVT / Swin——层级 Transformer

**PVT (Pyramid Vision Transformer, 2021)**

- 模仿 CNN 的层级下采样结构，每个 stage 分辨率减半、通道翻倍
- 让 Transformer 有了像 ResNet/FPN 那样的层级特征

**Swin Transformer (2021)**

- 窗口化 attention + shifted window + 层级结构
- 从 stage 1 到 stage 4 分辨率递减——**就是 CNN 金字塔的 Transformer 版本**
- Swin 的层级特征可以直接接 FPN 做检测/分割

**这些层级 Transformer 的贡献**：**让 FPN 这些 Inception 遗产在 Transformer 时代继续活着**——Mask2Former、DETR 等现代检测/分割模型大量用 Swin + FPN 的组合。

### §8.2 MViT / UniFormer——多尺度注意力

**MViT (Multiscale Vision Transformer, Fan et al., 2021)**

- 在 attention 内部做多尺度池化（Q/K/V 各自不同尺度）
- 视频理解任务的 SOTA

**UniFormer (2022)**

- 浅层用卷积（局部多尺度）
- 深层用 attention（全局交互）
- **CNN 和 Transformer 的共形合流**

### §8.3 SAM / DINOv2 的 backbone 选择

- SAM (Segment Anything, 2023) 用 ViT 主干 + **FPN-style neck**
- DINOv2 用 ViT + **多尺度 patch 预训练**
- Stable Diffusion 3 用 DiT（Diffusion Transformer），但还是用了**多分辨率预测**

**在大模型时代，Inception 的多尺度基因依然活着——只是被装进了 Transformer 的外壳里**。

<aside>
💎

**§8 要义**：Transformer 贯除 CNN 的叙事是片面的——**Inception 的多尺度基因在 PVT / Swin / MViT / UniFormer 里被重新发明**。层级 Transformer + FPN neck 成为 Mask2Former / DETR 的默认代码构型——SAM 的 backbone 也是 ViT + FPN。

</aside>

---

## §9 · 一张遗产全景图

把这整条演化写成一张图：

```
Inception 模块 (2014)
 │
 ├── G1: 多尺度并行
 │    ├── SPP (2014) ─┐
 │    ├── PPM (2017) ─┼─→ DeepLab v3+ (ASPP + U-Net)
 │    ├── ASPP (2016-2017) ─┘        │
 │    ├── Res2Net (2019)             │
 │    ├── SKNet (2019)               │
 │    └── HRNet (2019) ── 多分辨率并行主干
 │
 ├── G2: 跨层级融合
 │    ├── FPN (2017) ──┐
 │    │    ├── PANet (2018)
 │    │    ├── BiFPN (2019, EfficientDet)
 │    │    ├── NAS-FPN (2019)
 │    │    └── Recursive FPN (2020, DetectoRS)
 │    │
 │    └── U-Net (2015) ──┐
 │         ├── SegNet
 │         ├── U-Net++
 │         ├── DeepLab v3+ ← 和 ASPP 合流
 │         └── Stable Diffusion U-Net
 │
 ├── G3: 1×1 瓶颈
 │    ├── ResNet bottleneck (2015)
 │    ├── MobileNet v2 inverted bottleneck (2018)
 │    ├── SE 模块 (1×1 的通道注意力, 2018)
 │    └── EfficientNet MBConv (2019)
 │
 └── G4: 稀疏分支近似稠密 → depthwise separable
      ├── Xception (2017)
      ├── MobileNet v1/v2/v3 (2017-2019)
      ├── ShuffleNet (2018)
      ├── EfficientNet (2019) ← G3+G4 合流
      └── ConvNeXt (2022) ← CNN 终极形态

+ Transformer 时代的复活：
  ├── PVT / Swin (2021) ── 层级 Transformer = Transformer 版金字塔
  ├── MViT (2021) ── attention 内部多尺度
  ├── UniFormer (2022) ── CNN + Transformer 合流
  └── SAM backbone (2023) ── ViT + FPN neck
```

---

## §10 · 最终观察：四种基因在现代视觉里的现状

如果你打开 2025-2026 年任何一个主流视觉模型（检测、分割、生成、理解），检查它的组件，你会发现：

| Inception 基因 | 当代存在形式 |
| --- | --- |
| 多尺度并行 | FPN / BiFPN neck（几乎所有检测/分割模型） |
| 跨层级融合 | U-Net 主干（扩散模型、分割模型） |
| 1×1 瓶颈 | 所有现代 CNN 和 Transformer 都在用 |
| Depthwise separable | 所有移动端和效率优化架构的基础 |

**这就是为什么 Inception 的"死"是一种特殊的死**——它不是被删除了，而是被**拆解吸收**到了整个视觉生态里。原作者 Szegedy 的名字大家可能不记得，但他留下的技术零件在每个打开摄像头的手机、每个分割掩码、每个检测框后面**都在运行**。

**这是深度学习架构演化里一种非常值得记录的模式**——一条路线的主干地位下降，不等于其技术基因消失。残差路线成为主干范式，但它的许多组织方式仍吸收了 Inception 留下的多尺度、瓶颈与分支思想。

---

这张遗产图谱适合作为本页的后记来理解：Inception 没有作为主干范式活到最后，却把自己的四条基因拆散后输送给了后续几乎全部主流架构。把这一点说清，才能避免把 Inception 误写成一条简单的"失败支线"。

<aside>
🌀

**第三部分总收束**：Inception 不是被删除，而是被**拆解吸收**。G1「FPN/BiFPN/HRNet」→ G2「U-Net/DeepLab/Diffusion」→ G3「ResNet/MobileNet/SE」→ G4「Xception/ConvNeXt」→ Transformer 时代「Swin/MViT/SAM」——**到 2026 年，Inception 的四条基因没有一条消亡**。这是架构演化里“主干范式更替，技术基因长期保留”的经典范例。

</aside>

<aside>
🏁

**本页总收束**：本页作为阶段 I 的第四环，完成两件事：（1）说明「非残差路线」的主干地位被残差范式吸收，而非简单失败；（2）**揭示 Inception 四条基因的远期继承**——G1/G2/G3/G4 跨越整个视觉生态，从移动端到生成模型到大模型都在被使用。阶段 I 的判别共形工程还需要在 §05 中通过残差革命完成封顶。

</aside>

<aside>
➡️

**进入 §05 与 §06**：本页之后，先读 [阶段 I · §5 · 优化器与残差革命（Momentum / Adam / ResNet / Pre-activation / DenseNet）](§05-优化器与残差革命\00-定位卡.md)，理解判别共形如何在深层训练中封顶；再读 [阶段 I · §6 · 标签制度的异化](§06-标签制度的异化.md)，理解为什么标签闭合的胜利会反过来逼出阶段 II。

</aside>
