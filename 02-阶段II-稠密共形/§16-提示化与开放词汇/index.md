# §16 · 接口主权的临界点：prompt 打开空间，语言夺走语义

§16 是阶段 II 的出口章，不是普通的开放词汇模型列表。

阶段 II 前半程把图像变成场、对象和 mask；§16 则让这些空间结构在推理时被外部提示调用。这里发生的不是“视觉自己拥有开放语义”，而是：

> 视觉把空间支撑服务化；语义主权则暂时交给语言、示例、数据引擎和外部概念制度。

## 1. 为什么 §16 是阶段 II 的出口

MaskFormer / Mask2Former 统一了区域 / 实例类任务，但它们仍默认一个闭集类别表。训练集中没有的类别，就没有对应通道。

SAM、Grounding DINO、YOLO-World、Florence-2、CAT-Seg、Depth Anything 等方法共同拆开了这个封闭口：

- 点、框、mask 让用户直接调用空间支撑。
- 文本和名词短语让外部概念进入检测与分割。
- 示例图像让“像这个”成为可操作提示。
- 大规模数据引擎让稠密监督可以持续扩张。

§16 的成功标准不是某个 AP 数值，而是：空间输出不再完全由训练集类别表规定，而可以在推理时由 prompt / text / exemplar 指定。

## 2. Prompt 与 Query 的差别

query 是绑定制度：它规定由哪个槽位接管某片证据。

prompt 是调用制度：它把外部意图、位置、文本或示例转化为 query / token / condition，使模型在推理时改变输出目标。

因此，prompt 并不自动提供意义。它只是把“要分什么 / 找什么 / 回答什么”的权力交给外部接口。意义仍然来自提示背后的语言、示例、标注和训练分布。

## 3. SAM 打开的是什么

SAM 打开的不是 universal semantic understanding，而是 promptable segmentation：

> 给定空间提示，返回相容空间支撑。

SAM 的核心接口是 point / box / mask。它让分割成为空间服务，但不回答概念从哪里来、语义如何自持、关系如何组织。

## 4. Grounding 与 Open-Vocabulary 打开的是什么

Grounding DINO、YOLO-World、APE、CAT-Seg、FC-CLIP 等路线让文本概念进入稠密输出。它们把阶段 II 的空间场接到阶段 III 的公共语义契约上。

但这条连接本身就是出口残差：

> 空间接口开放了；语义主权外包了。

## 5. 本章阅读入口

- [00-定位卡](00-定位卡.md)：§16 的总定位。
- [01-SAM展开](01-SAM展开.md)：promptable segmentation 的核心机制。
- [02-SAM2与SAM3](02-SAM2与SAM3.md)：从图像提示到视频记忆与概念提示。
- [03-视觉scaling分析](03-视觉scaling分析.md)：理论假说页，解释视觉 scaling 的结构压力。
- [04-VLM看不清问题](04-VLM看不清问题.md)：阶段 II 出口残差，说明语言可能遮蔽视觉。
- [05A-DINO-SSL线](05A-DINO-SSL线-语言无关视觉表征scaling.md)：语言无关视觉表征 scaling。
- [05B-DINO-DETR线](05B-DINO-DETR线-检测query与开放词汇.md)：检测 query 与开放词汇。
- [05C-Universal-Dense-Foundation线](05C-Universal-Dense-Foundation线-Florence2-DepthAnything-RADIO-SAMencoder.md)：通用稠密基础模型。

## 6. 出口残差

§16 的最终残差不是“开放词汇 AP 还不够高”，而是：

1. SAM 能返回空间支撑，却不拥有概念。
2. Grounding 能把文本指向区域，却不保证视觉真的看清。
3. Florence-2 / DINO-X / SAM 3 能统一更多接口，却仍依赖外部语义制度。
4. VLM 接上语言后，语言能力可能替视觉完成回答。

因此阶段 III 不是“给阶段 II 加一个文本模块”，而是阶段 II 自己说出：空间已经被打开，但公共意义仍在系统之外。
