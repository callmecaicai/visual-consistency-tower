# RS_CD 总纲：从代数差分到开放词汇变化检测

适用范围：本总纲只根据当前 `RS_CD` 文件夹内部材料，以及后续已补入的 `2025-01` 到 `2026-04` 前沿文献梳理而成。  
目标：固定成一个**5 阶段版本**，不再在阶段数上来回摆动。

编号纪律：`RS_CD` 内部若出现 `5A / 5B / 5C` 或历史遗留的 `⑤ / ⑥ / ⑦` 材料，只表示应用域内部子形态，不构成对主理论五阶段结构的修改。主理论仍以公理层的 I-V 五种闭合制度为准。

RS_CD 不是遥感应用综述，而是视觉理论大厦的第一个领域实例化场，用来检验“时间差异如何进入表征并形成状态闭合”。

因此，本目录的理论身份是：

```text
时间差异视觉 / temporal differential vision / state-transition closure
```

遥感变化检测只是它的第一个复杂真实场景；真正要检验的是：双时相、多时相与长期状态差异如何从输出结果上升为内部状态对象。

## 总判断

对这个目录来说，最稳的切法不是 6 段也不是 7 段，而是下面这 **5 个阶段**：

1. **光谱差分与 CNN 范式阶段**
2. **Transformer 架构阶段**
3. **基础模型迁移阶段**
4. **开放词汇与免训练阶段**
5. **变化理解与统一系统阶段**

这样切的原因很简单：

- 前两个阶段已经相对收敛，主问题、代表方法、残差都比较清楚；
- 后三个阶段才是当前前沿，内部仍在快速分化。

如果压成一句最短的话：

**RS-CD 的演进，不是单纯换 backbone，而是“变化”这个对象被不断抬升到更高的表征层：先是像素与光谱差值，然后是监督特征差异，再是全局关系差异，再是 foundation prior 下的开放变化，最后是可被描述、提问、统一调度的变化理解。**

## 同一套协议

稳定差异：
双时相之间那些在噪声、配准误差、尺度变化、季节变化和纹理扰动之后，仍值得被保留为“变化”的关系。

闭合半径：
从二值 change map，逐步扩大到语义 change、开放词汇 change、query-conditioned change，以及 change understanding。

当前总残差：
**变化语义大多仍是借来的，不是 RS-CD 自己持有的稳定状态空间。**

## 五阶段总表

| 阶段 | 核心问题 | 代表论文 / 方法 | 这一阶段保留了什么稳定差异 | 出口残差 |
| --- | --- | --- | --- | --- |
| ① 光谱差分与 CNN 范式 | 两时相之间哪些局部差异算变化 | `CVA`、`IR-MAD`、`FC-EF / FC-Siam`、`STANet`、`SNUNet-CD` | 从光谱差值到局部监督表征中的时相差异 | 关系建模弱、语义弱、仍主要是“哪里不同” |
| ② Transformer 架构 | 如何让变化在全局关系中成立 | `BIT`、`ChangeFormer`，以及后续 `M-CD`、`DDPM-CD`、`DiffRegCD`、`RemoteVAR` 这类强增强 | 全局 token / patch 关系中的跨时相关系差异 | 仍多是封闭集、change-map 导向、强依赖监督 |
| ③ 基础模型迁移 | 如何借助更大的通用先验做 CD | `SAM-CD / TTP / RSPrompter`、`ChangeCLIP / RemoteCLIP`、`BAN`、`MTP`、`SkySense V2` | foundation model 先验约束下的变化对象与变化语义 | 能力大多是借来的，统一时序表征仍不存在 |
| ④ 开放词汇与免训练 | 如果不给 CD 专训，还能不能找变化 | `AnyChange`、`Semantic-CD`、`AdaptOVCD`、`OpenDPR`、`CoRegOVCD`、`Seg2Change` | 可被开放类别描述、可被 zero-shot / training-free 召回的变化 | 概念跨时相可比性差，query 能力强但状态持有弱 |
| ⑤ 变化理解与统一系统 | 变化能否成为可描述、可提问、可统一建模的对象 | `Change Captioning` 系列、`RSCC`、`UniChange`、`TeoChat / Change-Agent`、`Delta-LLaVA` | 不仅可定位，还可命名、描述、问答、统一 BCD/SCD | 仍主要是任务统一，不是长期、多时相世界状态统一 |

## 第一阶段：光谱差分与 CNN 范式阶段

这一阶段我建议视作一个整体，不再拆成“传统方法”和“CNN 方法”两个正式阶段。

原因是：

- 它们解决的是同一个核心问题；
- 只是“差分发生的空间”不同；
- 前者在低层观测空间做差，后者在监督学习得到的局部特征空间做差。

### 代表性论文

- [Change Vector Analysis (CVA)](<Change Vector Analysis (CVA) e5e4cce09b4b4b2183b850a2db79b818.md>)
- [IR-MAD](<IR-MAD (Iteratively Reweighted MAD) 1783d2b98b4d4514bc54eb5be22910f7.md>)
- [FC-EF / FC-Siam-conc / FC-Siam-diff](<FC-EF FC-Siam-conc FC-Siam-diff (Daudt 2018) 3578e9698cb04545870fafead020246c.md>)
- [STANet（+ LEVIR-CD 数据集）](<STANet（+ LEVIR-CD 数据集） e2023d19bd2643108ed01e15418e0769.md>)
- [SNUNet-CD](<SNUNet-CD ec1f5864f4b0406eb77843d3bc5cd949.md>)

### 这一阶段到底完成了什么

第一，它把“变化”第一次稳定成一个计算对象。

在 `CVA / IR-MAD` 里，这个对象还是：

- 像素级的光谱差；
- 向量差；
- 统计显著性差异。

到了 `FC-EF / FC-Siam` 这一类，变化被重写成：

- 双时相局部表征的差异；
- 像素级监督学习可以直接输出的 dense binary map。

再到 `STANet / SNUNet-CD`，这条线已经非常清楚：

- 现代二值建筑 CD 的标准数据、标准评测、标准网络套路都成形了；
- Siamese、差分融合、编码器-解码器、局部注意力等部件基本齐全。

所以这一阶段保留下来的稳定差异是：

**局部区域中那些能够稳定映射到二值变化标签的跨时相差异。**

### 为什么说这一阶段“基本收敛”

因为它的任务定义已经非常稳定了：

- 输入：双时相图像；
- 输出：二值变化图；
- 监督：像素级标签；
- 成败标准：mask 精度。

你今天再看这类方法，改进当然还会继续有，但大方向基本不变。

### 这一阶段的总残差

它最深的问题不是“卷积不够深”，而是：

- 变化大多被局部化；
- 全局长程依赖弱；
- 语义仍然弱；
- 系统只能回答“哪里变了”，很难回答“变成了什么”。

所以第二阶段的推进，不是简单换成 Transformer，而是：

**把变化从局部差异提升成全局关系。**

## 第二阶段：Transformer 架构阶段

这一阶段我也建议看成一个整体，而且它同样相对收敛。

因为无论是标准 Transformer，还是后面的 Mamba、diffusion feature、autoregressive 版本，它们大多还在同一问题框架里：

- 仍然以 `change map prediction` 为中心；
- 仍然主要解决“如何把关系建模得更强、更全局、更稳”；
- 还没有真正改写任务边界。

### 代表性论文

- [BIT](<BIT (Binary change detection with Transformers) f3cab6811d864084816f5f60bc7875b6.md>)
- [ChangeFormer](<ChangeFormer 59c116b8f70a497dbdd886bd549e60cc.md>)

这一阶段的后续强增强，可以一并归在这里理解：

- `M-CD`：A Mamba-Based Siamese Network for Remote Sensing Change Detection
- `DDPM-CD`：Denoising Diffusion Probabilistic Models as Feature Extractors for RS-CD
- `DiffRegCD`：Integrated Registration and Change Detection with Diffusion Features
- `RemoteVAR`：Autoregressive Visual Modeling for Remote Sensing Change Detection

### 这一阶段到底完成了什么

`BIT` 的决定性意义，是把变化第一次放进了 **token 级全局关系** 里。  
`ChangeFormer` 则把纯 Transformer CD 做成了一条正式方法线。

所以这一阶段保留下来的稳定差异，不再只是局部纹理差分，而是：

**全局上下文中仍然成立的跨时相关系差异。**

到这个阶段，CD 的表达能力明显上升：

- 不是只看一个 patch 像不像变了；
- 而是看这个区域在整幅图、在两时相整体结构中，关系是否被破坏。

### 为什么说这一阶段也“基本收敛”

因为它的主问题和主残差也已经很稳定了：

- 主问题：如何把 long-range dependency、global context、配准扰动、结构一致性处理得更好；
- 主输出：仍然是二值或少量语义 mask；
- 主评价：仍然是 dense prediction 精度。

`M-CD`、`DDPM-CD`、`DiffRegCD`、`RemoteVAR` 看起来新，但本质上还是在这条轴上增强：

- `M-CD`：用更长序列建模能力替代或增强 Transformer；
- `DDPM-CD`：用更强生成式预训练表征作为 feature extractor；
- `DiffRegCD`：把 registration residual 正式纳入统一模型；
- `RemoteVAR`：把 autoregressive generation 拉进 change map 预测。

这些都重要，但它们更多是在把第二阶段做强，而不是彻底换阶段。

### 这一阶段的总残差

这一阶段最深的问题是：

- 仍以封闭集为主；
- 仍重监督；
- 仍主要围绕 change map；
- 高层语义仍缺失；
- 用户不能按需指定“我到底想看哪一种变化”。

所以第三阶段才会真正切到另一条线：

**不再只做更强的 CD 网络，而开始借用 foundation model 的先验。**

## 第三阶段：基础模型迁移阶段

这一阶段是前沿的第一层。

### 代表性论文 / 方法

- [⑤-A · SAM 路线：冻结分割基座 → 适配 CD](<⑤-A · SAM 路线：冻结分割基座 → 适配 CD（RSPrompter TTP SAM-CD） 0d70be6fdc424966bbff49b7aebd3b2c.md>)
- [⑤-B · CLIP VLM 路线：跨模态对齐做 CD](<⑤-B · CLIP VLM 路线：跨模态对齐做 CD（RemoteCLIP ChangeCLIP） 33cbb84c193341109136b17e3a18ec5b.md>)
- [⑤-C · 统一 FM 适配器 & RS 多任务预训练](<⑤-C · 统一 FM 适配器 & RS 多任务预训练（BAN MTP） 98e248b8649643aab1d7d3b3d85530c7.md>)
- [SkySense V2: A Unified Foundation Model for Multi-modal Remote Sensing](https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_SkySense_V2_A_Unified_Foundation_Model_for_Multi-modal_Remote_Sensing_ICCV_2025_paper.html)

### 这一阶段的本质

CD 不再只靠自己训练一个任务专用模型，而开始系统性借用：

- `SAM` 的定位先验；
- `CLIP / VLM` 的语义先验；
- `DINOv2 / DINOv3` 的表征先验；
- `RS foundation model` 的领域先验。

所以这一步保留下来的稳定差异，已经不是单纯的 CD 内部特征差异，而是：

**foundation model 先验约束下，哪些双时相关系值得被解释为变化。**

### 这一阶段的总残差

最关键的一条是：

**能力大多是借来的。**

具体说：

- 定位能力常借自 SAM；
- 语义能力常借自 CLIP / VLM；
- 表征鲁棒性常借自 DINO / SSL；
- 但这些能力还没有在 RS-CD 里形成一个自持的统一时序表征。

因此，第四阶段自然会出现：

**既然语义主要靠借，那就进一步追问：能不能开放词汇，甚至不给 CD 专门训练。**

## 第四阶段：开放词汇与免训练阶段

这一阶段是最近最清楚的一轮前沿。

### 代表性论文

- [⑦-A · Training-Free CD 路线 A：SAM Segment-Everything + Mask 对应匹配](<⑦-A · Training-Free CD 路线 A：SAM Segment-Everything d28bfe9dd5264f118f9000d3b1a9ddb8.md>)
- [Semantic-CD](https://arxiv.org/abs/2501.06808)
- [AdaptOVCD](https://arxiv.org/abs/2602.06529)
- [OpenDPR](https://arxiv.org/abs/2603.27645)
- [CoRegOVCD](https://arxiv.org/abs/2604.02160)
- [Seg2Change](https://arxiv.org/abs/2604.11231)
- [Referring Change Detection in Remote Sensing Imagery](https://openaccess.thecvf.com/content/WACV2026/html/Korkmaz_Referring_Change_Detection_in_Remote_Sensing_Imagery_WACV_2026_paper.html)

### 这一阶段的本质

这个阶段的任务定义已经明显变化了：

- 不是只输出一个总的 change map；
- 而是开始回答任意类别、任意 query、任意指定变化类型；
- 并且越来越多地追求 `zero-shot`、`training-free`、`query-conditioned`。

这一阶段保留下来的稳定差异是：

**那些即便不专门为 CD 训练，仍能被 foundation model 稳定召回的变化对象与变化语义。**

### 这一阶段的总残差

它已经比“普通监督 CD”高一层，但仍有明显裂缝：

- 概念在两时相之间可比性不稳；
- subtle change 仍难；
- 纯定位驱动缺语义；
- 纯语义驱动缺精细边界；
- 大多数方法还是 pipeline 拼接，而不是统一变化空间。

所以第五阶段继续前推时，问题会变成：

**变化能否不只是被检测出来，而是被理解、被描述、被统一组织。**

## 第五阶段：变化理解与统一系统阶段

这一阶段是当前最前沿的一层。

### 代表性论文 / 数据 / 系统

- [⑥-A · Change Captioning 奠基](<⑥-A · Change Captioning 奠基：双分支 Transformer → 自然语言描 6a40583827ef4f438e6b2a03763f6868.md>)
- [⑥-B · Change Captioning 三条进化路径](<⑥-B · Change Captioning 三条进化路径：语义化 高效化 解耦化（KCFI RS 954e7c5bcf3a4f14b7c8d925dd25e125.md>)
- [⑥-C · 从单轮 caption → 会话 & Agent 化 RS CD](<⑥-C · 从单轮 caption → 会话 & Agent 化 RS CD（TeoChat Cha b965de08b3ff414bbf50aa8054a62616.md>)
- [RSCC](https://openreview.net/forum?id=yn2fJYBKEB)
- [UniChange](https://arxiv.org/abs/2511.02607)
- [Decoding the Delta / Delta-LLaVA](https://arxiv.org/abs/2604.14044)

### 这一阶段的本质

这一步已经不再满足于：

- 找哪里变了；
- 给一个类别；
- 或给一个 query 的 mask。

它想做的是：

- 变化描述；
- 变化问答；
- 变化指代；
- 统一 `BCD / SCD`；
- 最终走向统一的 multi-temporal change understanding。

所以这一阶段保留下来的稳定差异是：

**那些不仅能被定位，还能被命名、被描述、被提问、被统一建模的变化对象。**

### 这一阶段的总残差

到这里，最深的问题已经不是某个 benchmark 的 IoU 还差多少，而是：

- 统一的是任务接口，还是内部状态？
- 系统是否真的持有了变化，而不只是把多个任务缝到一起？
- 多时相、长期状态、反事实变化、世界状态一致性还没有真正进入主线。

## 现在最稳的读法

如果你现在要一句非常稳的阶段判断，我建议以后统一用下面这条：

1. **光谱差分与 CNN 范式阶段**
2. **Transformer 架构阶段**
3. **基础模型迁移阶段**
4. **开放词汇与免训练阶段**
5. **变化理解与统一系统阶段**

再压成一条主链，就是：

**变化先被做差，后被表征，再被全局化，再被 foundation model 借力开放，最后开始被统一理解。**

## 当前最值得保留的总残差

如果只允许留下一个总残差，我会保留这一条：

**RS-CD 现在已经能把变化开放词汇化、可指代化、可描述化，但它仍然主要在借用外部 foundation model / VLM 的语义空间，而没有形成自己稳定的变化状态空间。**

这也是为什么，后面如果继续深入，真正该问的不是：

- 怎么再把 CD 做准一点；

而是：

- **如何让“变化”从一个任务输出，变成系统内部可持有、可比较、可推理的时序对象。**

## 前沿补遗入口

后面三阶段对应的最新前沿补遗在这里：

- [01-RS_CD前沿补遗-2025到2026-04-从开放词汇CD到变化理解系统](D:/AboveAll_A_World/视觉理论大厦的一致性建模/RS_CD/01-RS_CD前沿补遗-2025到2026-04-从开放词汇CD到变化理解系统.md)
- [02-RS_CD后3阶段论文深读-第一轮](D:/AboveAll_A_World/视觉理论大厦的一致性建模/RS_CD/02-RS_CD后3阶段论文深读-第一轮.md)
- [03-RS_CD代码开源梳理-截至2026-04-23](D:/AboveAll_A_World/视觉理论大厦的一致性建模/RS_CD/03-RS_CD代码开源梳理-截至2026-04-23.md)
- [04-RS_CD开源仓库路线图-按残差串联](D:/AboveAll_A_World/视觉理论大厦的一致性建模/RS_CD/04-RS_CD开源仓库路线图-按残差串联.md)

那一篇主要补的是：

- `Semantic-CD / AdaptOVCD / OpenDPR / CoRegOVCD / Seg2Change`
- `RSCC / UniChange / Delta-LLaVA`
- 弱监督、免训练、query-conditioned、change understanding 的最新残差

而 `02` 这篇则开始逐篇压实：

- 每篇论文真正解决的残差是什么；
- 为什么它属于对应阶段；
- 它到底推进了什么；
- 以及它还留下了什么问题。
