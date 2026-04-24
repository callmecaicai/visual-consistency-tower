# §28-补

标题: 多时相 RS-VLM 专题补遗：十五篇被主章漏掉的关键工作（CDChat / UniRS / UniChange / BTCChat / CCExpert / Change-Agent / Change-LISA / Delta-LLaVA / Prithvi-EO-2.0 / TiMo / TimeSenCLIP / EarthMind / DisasterM3 / EarthDial / Forest-Chat）
类型: 补章
要点: §28 主章锁定了三条主线的五篇代表作（TEOChat / ChangeChat / DeltaVLM / TAMMs / ViLaCD-R1），但每条主线下仍有关键变体与延伸工作未被收录，且存在三类与 VLM 平行演化的工作也必须纳入视野。本补章按五类补齐：A 让 VLM 理解变化的漏掉的五篇——CDChat / CCExpert / BTCChat / Change-Agent / MV-CC；B 统一多任务多时相输入的三篇——UniRS / UniChange / Change-LISA；C 2026 最新前沿的两篇——Delta-LLaVA / 双粒度 VLM；D 非 VLM 但影响 VLM 的三篇时间序列 foundation model——Prithvi-EO-2.0 / TiMo / TimeSenCLIP；E 跨传感器 + 灾害 + 林业专题的四篇——EarthMind / DisasterM3 / EarthDial / Forest-Chat。补遗后对主章 5 条残差进行三项修正：TAMMs 不再是唯一 TAM 路线（UniRS 视频路径提供另一基线）、ViLaCD-R1 不再是唯一端到端 VLM→mask（UniChange Token-Driven Decoder 给出 token 路径）、Prithvi-EO-2.0 + TiMo 指明 SITS 长时序 foundation 与 VLM 融合才是第二条残差的现实路径。

# 阶段 III · 多时相 RS-VLM 专题补遗：十五篇被主章漏掉的关键工作

作者 / 机构: Noman 等 (MBZUAI, IGARSS 2025) / Wang 等 (CCExpert, arxiv 2411.11360) / Li 等 (BTCChat, arxiv 2509.05895) / Liu 等 (Change-Agent, IEEE TGRS 2024) / Liu 等 (MV-CC, arxiv 2410.23946) / Li 等 (UniRS, arxiv 2412.20742) / Zhang 等 (UniChange, arxiv 2511.02607) / Jia 等 (Change-LISA, IEEE TGRS 2026) / Xue 等 (双粒度 VLM, arxiv 2509.23105) / Li 等 (Delta-LLaVA, arxiv 2604.14044) / Szwarcman 等 (IBM-NASA, arxiv 2412.02732) / Qin 等 (TiMo, arxiv 2505.08723) / Jain 等 (TimeSenCLIP, arxiv 2508.11919) / Shu 等 (EarthMind, OpenReview 2025 / ICLR 2026 submission) / Wang+Xuan 等 (DisasterM3, NeurIPS 2025 Datasets and Benchmarks Track) / Soni 等 (EarthDial, CVPR 2025) / Brock 等 (Forest-Chat, arxiv 2601.04497)
共形维度: 结构 + 时序 + 多任务 + 跨传感器
关键贡献: 补齐 §28 主章未收录的五类工作：(A) 让 VLM 理解变化的另外五篇——CDChat 与 ChangeChat 几乎同期、CCExpert 把差异感知做成通用 MLLM 接口、BTCChat 在 bi-temporal 场景与多任务之间架桥、Change-Agent 用 MCI 把 CD + CC 统一为 agent 工作流、MV-CC 首次把低分变化 mask 作为 CC 的显式引导；(B) 统一多任务多时相输入的三篇——UniRS 把单图 / 双时相 / 视频三类输入统一进一个 VLM、UniChange 用 Token-Driven Decoder 让 MLLM 端到端输出 BCD 与 SCD mask、Change-LISA 把 LISA 的推理分割范式迁到 CD；(C) 2026 最新前沿两篇——Delta-LLaVA 把差异提取从视觉侧做到 LLM 侧、双粒度 VLM 把交互式变化理解做成大规模 benchmark；(D) 与 VLM 平行演化的时间序列 foundation model 三篇——Prithvi-EO-2.0 / TiMo / TimeSenCLIP，它们不是 VLM 但决定了 VLM 能不能真正走进 multi-temporal；(E) 跨传感器 + 灾害 + 林业专题四篇——EarthMind / DisasterM3 / EarthDial / Forest-Chat。补遗后对主章五条残差做三项修正。
年份: 2024/09 – 2026/04
序号: 28-补
残差 / 它催生了什么: 对主章残差三项修正：残差 3 benchmark 空白应降级（CCExpert-5M / DisasterM3 / RSCC 三个数据集已部分填补）；残差 4「端到端 VLM → mask」应细化（UniChange 给出 token 路径，ViLaCD-R1 给出两阶段路径，两条路线并存）；残差 2「>2 时相」应修正（UniRS 视频路径 + Prithvi-EO-2.0 / TiMo 时序 foundation 已提供 SITS 基座，缺的是 VLM 与其融合）。两条新残差：(新1) SITS foundation model 与 VLM 的融合范式缺失；(新2) Token-Driven Decoder vs Two-Stage MGD 两条 VLM→mask 路线的优劣尚无公允比较。
类型: 专题补遗 / 文献完善
阶段: III · 语言共形

> 领域实例化说明：本补遗服务于阶段 III 的遥感回灌，不改变主线结构。它用于观察语言共形在空间定位、时间变化、变化 mask 输出和 RS foundation model 融合中的残差放大。

🎯
**主题**：§28 主章按「多图塞进 VLM → 理解图间差异 → 输出像素变化 mask」三条主线锁了 TEOChat / ChangeChat / DeltaVLM / TAMMs / ViLaCD-R1 五篇。但这三条主线每一条下都还有关键变体、有若干平行演化的工作（时序 foundation model、跨传感器 VLM、灾害专题 VLM、林业专题 VLM）对本专题至关重要。本补章按五类（A/B/C/D/E）把它们补齐，并在最后对主章的五条残差做修正。

---

# A · 「让 VLM 理解变化」这条线上被漏掉的五篇

## A.1 · CDChat —— *arxiv 2409.16261 / IGARSS 2025* (Noman 等, MBZUAI)

**共形贡献**：与 ChangeChat 几乎同期（二者都在 2024/09 投出，ChangeChat 投 ICASSP，CDChat 投 IGARSS）。CDChat 的关键贡献是**首次为 SYSU-CD 这个大规模 CD 数据集补充自然语言变化描述**——这弥补了 LEVIR-CC 只覆盖 LEVIR-CD 一个场景的缺陷。其架构以 GeoChat 为起点，在 GeoChat 之上做双时相指令微调，用自定义标注工具人工标注 SYSU-CD 的变化文本。

**与 ChangeChat 的区别**：ChangeChat 的数据生成依赖 GPT-assisted 流水线（半自动）；CDChat 用**人工标注工具**对 SYSU-CD 进行全人工标注，因此标注质量更高但规模更小（量级在万级 vs ChangeChat-87k）。**这条数据生成范式之争在 2025 年延续为「GPT 半自动 vs 人工金标」的 benchmark 构造方法论争议**。

**漏掉原因与纳入必要性**：主章选 ChangeChat 作为 bi-temporal VLM 的代表是因为它开辟了 RSICA 任务范式，但 CDChat 作为同期另一路线——**以人工标注和 SYSU-CD 为核心**——也应当被明确列出，否则读者会误以为 bi-temporal VLM 只有 ChangeChat 一条路径。

🔗 [https://arxiv.org/abs/2409.16261](https://arxiv.org/abs/2409.16261)

## A.2 · CCExpert —— *arxiv 2411.11360* (Liu 等, 2024/11)

**共形贡献**：把 DeltaVLM 的「差异感知 + 指令引导」思想做成**通用 MLLM 接口**——即不再是一个专门为 change captioning 设计的模型，而是在任意 MLLM（LLaVA / Qwen-VL / InternVL 类）上可插拔的差异感知模块。同时贡献 **CC-Foundation-5M**，一个 500 万量级的 RSICC 基础数据集（远超 LEVIR-CC 的 5 万 + 和 ChangeChat-105k 的 10 万 +）。

**三件关键事**：

**（1）Difference-Aware Integration（DAI）模块**：插在视觉编码器与 LLM 之间，先做跨时相特征对齐（cross-temporal alignment）再做差异提炼（difference refinement）。与 DeltaVLM 的 CSRM 思路一致，但做成了模块化、即插即用。

**（2）CC-Foundation-5M 数据集**：从 Google Earth、GaoFen、Sentinel-2 等多源混合采集 5M 对双时相对，用 GPT-4V + 专家 review 构造变化描述。**这是目前最大规模的 RSICC 数据集**——把主章残差 3 的「语言-变化 benchmark 缺失」从「全空白」改写为「大规模但未配 mask」。

**（3）多阶段预训练**：第一阶段 5M 对上做 DAI 模块预训练；第二阶段在 LEVIR-CC / DUBAI-CCD / SECOND 等标注数据上做下游微调。这种「大规模弱监督 + 小规模强监督」的两阶段范式回应了 §24 视觉指令微调的 scale 观察。

**为什么必须纳入**：CCExpert 在 2024/11 已把 RSICC 数据规模推到 5M，这直接修正主章残差 3「benchmark 缺失」的说法——缺的不是数据规模，而是**同时覆盖图 + 语言 + mask + 对话**四者的数据集。

🔗 [https://arxiv.org/abs/2411.11360](https://arxiv.org/abs/2411.11360)

## A.3 · BTCChat —— *arxiv 2509.05895* (2025/09)

**共形贡献**：在 ChangeChat / DeltaVLM 的基础上进一步把 bi-temporal MLLM 做成**既能做 change captioning 又能做单图 VQA 的双任务模型**，而非只做变化任务。这对应于你研究方向的一个现实需求——**模型不能只会看变化，也必须能单独解读每一时相**（灾前评估、灾后评估、变化评估三位一体）。

**两件关键事**：

**（1）通用 MLLM 预处理阶段**：在 change captioning 之前，先用一个大模型（GPT-4o / InternVL3）对每一时相单独做视觉解读，把语言化的上下文作为 task instruction 注入 BTCChat——这是**「让大模型预解读、小模型做专项」的蒸馏式范式**，工程上非常实用。

**（2）混合多任务微调**：BTCChat 在 LEVIR-CC + RSVQA + SEMVG 等单图 + 双时相混合数据上微调，结果在两类任务上都 SOTA——验证了「多任务混合反哺」现象。

**与主章的关联**：主章第 5 条残差「VLM + 时序 + 矢量多边形」是远景目标；BTCChat 展示了近景目标——**一个既能解读单时相又能解读变化的 MLLM，即使不输出 mask 也极有业务价值**。你的研究第一阶段可以直接借用 BTCChat 范式。

🔗 [https://arxiv.org/abs/2509.05895](https://arxiv.org/abs/2509.05895)

## A.4 · Change-Agent —— *Change-Agent: Toward Interactive Comprehensive Remote Sensing Change Interpretation and Analysis* (Liu 等, IEEE TGRS 2024)

**共形贡献**：**RSICI（Remote Sensing Image Change Interpretation）agent 范式的奠基作**。Change-Agent 不是一个 VLM，而是一个 **LLM-orchestrated 多模型工作流**——LLM 作为调度器，在运行时调用 MCI（Multi-level Change Interpretation）视觉模型、CD 网络、captioning 模型等工具来响应用户查询。这是 §28 第二条主线（「理解图间差异」）的**另一条技术路径——工具调用式而非端到端式**。

**MCI 模型的贡献**：统一 CD + CC 为多任务学习，输出层同时产像素 mask 和描述 caption。MCI 作为 Change-Agent 的核心工具被反复调用。

**与 DeltaVLM 的路线区别**：DeltaVLM 是端到端单一 MLLM；Change-Agent 是 LLM + 工具组合。两条路线各有优劣——端到端更容易扩展任务范围但工程复杂度高，agent 式更容易维护和调试但性能上限受限于工具。

**BUAA LEVIR lab 这条系谱**：Change-Agent → MCI → LEVIR-CC / LEVIR-MCI → RS-STVLM survey（主章已引用 2412.02573）→ 最近的双粒度 VLM（A.7）。这是整个 RS-STVLM 领域最连贯的研究线，主章却没有提 Change-Agent 作为其起点——这是重大遗漏。

🔗 [https://ieeexplore.ieee.org/document/10591792](https://ieeexplore.ieee.org/document/10591792) · arxiv 2403.19646

## A.5 · MV-CC —— *MV-CC: Mask Enhanced Video Model for Remote Sensing Change Caption* (Liu 等, arXiv 2024)

**共形贡献**：**首次把低分辨率 change detection mask 作为 change captioning 模型的显式引导信号**。此前的 RSICC 模型都是纯视觉输入 + 语言输出，MV-CC 证明**把 CD 网络先跑一遍的结果作为「注意力先验」喂给 CC 模型，能显著提升小结构 + 低光条件下的描述精度**。

**三件关键事**：

**（1）两阶段架构**：Stage 1 用 BIT / ChangeFormer 等专用 CD 网络产出低分辨率变化 mask；Stage 2 把该 mask 作为空间注意力权重与视觉特征相乘，再送入 CC 解码器。

**（2）验证了 CD 与 CC 的互补性**：在 LEVIR-CC 上比基线提升 3–5 个 BLEU-4 点。

**（3）MV-CC 思路在 RS-STVLM survey 中被专门作为一章（II-B 2 Multi-task learning of Change Detection and Change Captioning）讨论**——这是主章完全没提到的重要设计哲学。

**为什么必须纳入**：ViLaCD-R1 的 MIR + MGD 两阶段设计在某种意义上是 MV-CC 思路的反向版本——MV-CC 是 CD→CC，ViLaCD-R1 是 VLM→CD。理解 MV-CC 有助于理解 ViLaCD-R1 的设计动机。

🔗 [https://arxiv.org/abs/2410.23946](https://arxiv.org/abs/2410.23946)

---

# B · 「统一多任务 / 多时相输入」这条线

## B.1 · UniRS —— *arxiv 2412.20742* (2024/12)

**共形贡献**：**第一个把「单图 + 双时相 + 视频」三种视觉输入统一在同一 VLM 框架里的工作**。这正是主章提出的残差 2「>2 时相研究空白」的早期回应——UniRS 把视频路径当作 >2 时相序列的通用载体，直接复用了 Video-LLaVA / VideoChat 的视频处理技术。

**三件关键事**：

**（1）输入类型感知路由**：推理时先检测输入是单图 / 双时相 / 视频，再路由到对应的视觉 tokenizer。

**（2）任务-输入配对**：场景分类走单图、变化描述走双时相、视频分类走视频。

**（3）打破 bi-temporal 的二元困局**：TEOChat 能吃多帧但训练集偏 bi-temporal；UniRS 直接把视频作为 native 支持项，是目前最靠近 SITS VLM 的设计。

**为什么必须纳入**：UniRS 与 TAMMs 是 >2 时相 VLM 的两条并行路径——TAMMs 是 TAM 适配器路径，UniRS 是视频路径。主章只提了 TAMMs 是严重偏颇。

🔗 [https://arxiv.org/abs/2412.20742](https://arxiv.org/abs/2412.20742)

## B.2 · UniChange —— *arxiv 2511.02607* (2025/11)

**共形贡献**：**第一个用 MLLM 同时做 BCD（二值变化检测）与 SCD（语义变化检测）的统一框架**，而且是端到端 mask 输出。这直接和 ViLaCD-R1 平行——ViLaCD-R1 走两阶段 MIR + MGD，UniChange 走 **Token-Driven Decoder** 单阶段路径。

**Token-Driven Decoder 机制**：在 MLLM 中注入三个特殊 token——[T1]、[T2]、[CHANGE]——分别对应第一时相 token、第二时相 token、变化 mask 生成 token。训练时 MLLM 同时学「描述 + 变化 mask」。推理时 [CHANGE] token 的 hidden state 通过 mask decoder 解码为像素级 mask，类似 LISA 的 [SEG] token 机制。

**与 ViLaCD-R1 对比（两条端到端路线之争）**：

- **ViLaCD-R1**：两阶段 = MIR（SFT + RL 出块级粗 mask） + MGD（上采样为像素 mask）。优点：RL 带来额外 2–3 个点；缺点：两阶段耦合弱。
- **UniChange**：单阶段 = Token-Driven Decoder（直接从 [CHANGE] token 解码为 mask）。优点：端到端纯粹；缺点：尚未引入 RL。

**这是主章残差 4 的直接修正**——端到端 VLM→mask 不再只有 ViLaCD-R1 一条路径。

🔗 [https://arxiv.org/abs/2511.02607](https://arxiv.org/abs/2511.02607)

## B.3 · Change-LISA —— *Change-LISA: Language-Guided Reasoning for Remote Sensing Change Detection* (Jia 等, IEEE TGRS 2026)

**共形贡献**：**把 LISA（Reasoning Segmentation via LLM）的范式迁到 RS 双时相 CD**——让 MLLM 通过推理链驱动变化分割。LISA 是 §27 GeoPixel / GeoGround 背后的启发源头，Change-LISA 是 LISA 在时序上的直接延拓。

**关键机制**：与 UniChange 的 [CHANGE] token 类似，但 Change-LISA 更强调**在推理链（chain-of-thought）中多轮提示**—— 用户问「这里建筑有变化吗？」，模型先推理「第一时相有 3 栋建筑，第二时相有 5 栋，因此新增 2 栋」，然后输出对应的 mask。

**与 DeltaVLM 的对比**：DeltaVLM 做多轮对话但不输出 mask；Change-LISA 做推理 + mask 但对话轮数少。两者是互补维度。

**为什么必须纳入**：这是 §27 GeoPixel / GeoGround → §28 ViLaCD-R1 / UniChange 路径上的关键中间节点。

🔗 [https://doi.org/10.1109/TGRS.2026.3684817](https://doi.org/10.1109/TGRS.2026.3684817)

---

# C · 2026 最新前沿两篇

## C.1 · Delta-LLaVA —— *arxiv 2604.14044* (2026/04)

**共形贡献**：把 DeltaVLM 的思路从「视觉侧算差异」推进到「LLM 侧算差异」——让 LLM 在自回归过程中**显式提取并放大时间差异信号**。这是 2026 年 4 月最新工作，在主章发稿后刚出现。

**核心创新**：

**（1）Temporal Difference Attention（TDA）**：在 LLM 的某些 attention head 专门处理跨时相 token 的差异，而非混合处理。

**（2）差异放大正则化**：训练时加损失项鼓励模型在 TDA head 的 attention map 上集中到真实变化区域。

**（3）通用 MLLM backbone**：基于 LLaVA-1.5 / LLaVA-NeXT，可直接迁移到其他 RS 任务。

**意义**：Delta-LLaVA 是 DeltaVLM 路线（视觉侧差异）与 UniChange 路线（LLM token 侧差异）的**融合路径**——用 LLM 侧注意力直接处理差异，不再依赖视觉侧的 CSRM。这预示 2026 下半年会出现一批「纯 LLM 端处理时序」的工作。

🔗 [https://arxiv.org/abs/2604.14044](https://arxiv.org/abs/2604.14044)

## C.2 · 双粒度 Enhanced VLM（Comprehensive Interactive Change Understanding） —— *arxiv 2509.23105* (Liu 等, BUAA LEVIR lab, 2025/09)

**共形贡献**：继 Change-Agent → DeltaVLM → 本工作，BUAA LEVIR lab 继续推进 RSICI，把任务体系扩展到 **change counting + spatial localization + comprehensive captioning 的三件一体**，并构造一个大规模交互式数据集。

**双粒度设计**：在 VLM 中同时处理 patch-level（粗粒度）和 pixel-level（细粒度）变化表示——这是对 DeltaVLM 单粒度 Q-former 的扩展。patch-level 供 counting / classification，pixel-level 供 localization / segmentation。

**benchmark 贡献**：数据量规模未披露但涵盖 6 大类 20 子任务，**是目前最齐全的 RSICA benchmark**。

🔗 [https://arxiv.org/abs/2509.23105](https://arxiv.org/abs/2509.23105)

---

# D · 非 VLM 但决定 VLM 未来的三篇时序 foundation model

这三篇都不是 VLM，但它们是 SITS 基座，**任何 multi-temporal VLM 要真正走向 >10 时相、>5 年跨度的长时序任务，都需要这类 foundation model 作为视觉编码器**。主章完全没提这条平行线是重大缺失。

## D.1 · Prithvi-EO-2.0 —— *arxiv 2412.02732* (IBM + NASA + Jülich, 2024/12)

**共形贡献**：NASA + IBM 联合训练的地球观测 foundation model 第二代。基于 NASA 的 HLS（Harmonized Landsat + Sentinel-2）数据集，420 万全球时间序列样本预训练，参数规模 300M–600M。

**核心设计**：

**（1）Temporal + location embeddings**：每个输入 token 带时间戳和经纬度编码——这是 multi-temporal foundation model 的标配。

**（2）在 GEO-Bench 上比 Prithvi-EO-1.0 提升 8%**，并超过六个其他 geospatial foundation model。

**（3）开源 + 多个尺寸**（100M / 300M / 600M）覆盖不同算力层。

**为 VLM 带来的意义**：Prithvi-EO-2.0 是目前最好的 multi-temporal 视觉编码器之一，但尚未有人把它作为 VLM 的视觉 backbone。**「Prithvi-EO-2.0 + LLaMA」或「Prithvi-EO-2.0 + Qwen2.5-VL backbone 替换」会是一个直接可做的 multi-temporal RS-VLM 工程**——这是你研究方向的一个低成本切入点。

🔗 [https://arxiv.org/abs/2412.02732](https://arxiv.org/abs/2412.02732) · HuggingFace：ibm-nasa-geospatial/Prithvi-EO-2.0-300M

## D.2 · TiMo —— *arxiv 2505.08723* (2025/05)

**共形贡献**：**Spatiotemporal Foundation Model for SITS**。核心创新是 **spatiotemporal gyroscope attention**——在多尺度时空关系上做层次化注意力。Prithvi 用的是普通 ViT，TiMo 用层次化 ViT + gyroscope 机制。

**为什么重要**：TiMo 是目前唯一显式声称「多尺度时空注意力」的 RS foundation model——它正好回应主章残差 1 的「时间方向原生 attention 缺失」。**把 TiMo 的 gyroscope attention 作为 VLM 视觉 backbone 的替换** 是一条未被探索的研究路径。

🔗 [https://arxiv.org/abs/2505.08723](https://arxiv.org/abs/2505.08723)

## D.3 · TimeSenCLIP —— *arxiv 2508.11919 / ISPRS J 2026* (Berg 等)

**共形贡献**：**第一个 time-series VLM for RS**——用 cross-view temporal contrastive 把 Sentinel-2 多光谱时间序列与地面图像对齐，不需要文本标注。**是 CLIP 在 SITS 上的延拓**。

**关键突破**：单像素时间序列 + 对比学习 + 与 Flickr 地面图像地理标签对齐，得到一个「pixel-temporal 语义嵌入空间」——这让 SITS 数据能「被语言描述」而不依赖人工打标。

**为主章残差 3 的意义**：TimeSenCLIP 给出了一个**无需人工标注构造 SITS VLM 训练数据**的范式——这是解决「语言-时间 benchmark 缺失」的最具扩展性路径。

🔗 [https://arxiv.org/abs/2508.11919](https://arxiv.org/abs/2508.11919)

---

# E · 跨传感器 + 灾害 + 林业专题四篇

## E.1 · EarthMind —— *EarthMind: Leveraging Cross-Sensor Data for Advanced Earth Observation Interpretation with a Unified Multimodal LLM* (Shu 等, OpenReview 2025 / ICLR 2026 submission)

**共形贡献**：**Cross-Sensor EO MLLM**——专门处理光学 + SAR + 红外的多源时序融合，回应主章残差 5「多传感器多时相空白」。EarthMind 用不同传感器各自的视觉编码器，输出到统一 token 空间再送入 LLM。

**意义**：这是目前最接近「多传感器 + 多时相」组合目标的 VLM——虽然时序部分仍有限，但**多传感器架构模板已给出**。

🔗 [https://openreview.net/forum?id=ooYtHcj6LI](https://openreview.net/forum?id=ooYtHcj6LI)

## E.2 · DisasterM3 —— *DisasterM3: A Remote Sensing Vision-Language Dataset for Disaster Damage Assessment and Response* (Wang 等, NeurIPS 2025 Datasets and Benchmarks Track)

**共形贡献**：**大规模多传感器灾害评估 VLM benchmark**。9 个灾害相关视觉感知 + 推理任务，从灾害体识别到结构损伤评估到长文报告生成。**评测了 14 个通用 + RS VLM，发现 SOTA 模型在灾害任务上普遍失败**——主要原因是缺少灾害特定语料、跨传感器 gap、损伤目标计数不敏感。

**为什么必须纳入**：这是主章提到的「benchmark 缺失」命题的**直接反驳**——灾害子领域已有 DisasterM3 这样大规模基准。你的研究若涉及灾害应用必须以 DisasterM3 为评测集。

🔗 [https://openreview.net/forum?id=sQO1ZEQGqX](https://openreview.net/forum?id=sQO1ZEQGqX)

## E.3 · EarthDial —— *EarthDial: Turning Multi-sensory Earth Observations to Interactive Dialogues* (Soni 等, CVPR 2025)

**共形贡献**：**MBZUAI 出品的 RS 通用 conversational assistant**，明确支持 **high-resolution + multi-spectral + multi-temporal**（三件事同时做，在 §27 的 GeoChat / LHRS-Bot-Nova 时代都是各自单独做的）。

**关键创新**：多分辨率任意尺寸输入 + 多光谱通道摄入 + 时序对话。MBZUAI 在官网明确对比指出「developers have also built VLMs specifically for geospatial data, but today's models don't work well with high-resolution images of varying sizes, and they don't support multi-spectral or multi-temporal analysis」—— EarthDial 自己填了这个空白。

**为什么必须纳入**：EarthDial 与 TEOChat 是两条最接近「通用 RS 多时相助手」的路线——TEOChat 偏时序深度，EarthDial 偏多模态广度。

🔗 [https://openaccess.thecvf.com/content/CVPR2025/html/Soni_EarthDial_Turning_Multi-sensory_Earth_Observations_to_Interactive_Dialogues_CVPR_2025_paper.html](https://openaccess.thecvf.com/content/CVPR2025/html/Soni_EarthDial_Turning_Multi-sensory_Earth_Observations_to_Interactive_Dialogues_CVPR_2025_paper.html)

## E.4 · Forest-Chat —— *arxiv 2601.04497 / ScienceDirect 2026* (Zhang 等)

**共形贡献**：**第一个 domain-specialized 的时序 RS-VLM agent**——专门为 forest change analysis 设计。两条路线：FC-Supervised 用 MCI 模型产出监督 pixel-level CD；FC-Zero-shot 用 AnyChange（§27 残差涉及的 SAM 泛化）+ GPT-4o 组合做零样本 CD + CC。

**意义**：Forest-Chat 展示了 **domain-specialized agent** 的可行性——你研究方向的图斑产出若专注于某一地物类型（建筑、森林、农田、水体），Forest-Chat 是直接可借鉴的 agent 工程模板。

🔗 [https://arxiv.org/abs/2601.04497](https://arxiv.org/abs/2601.04497)

---

# 补遗后对主章五条残差的三项修正

## 修正 1 · 残差 3（语言-时间-图斑三位一体 benchmark 缺失）应**降级为「语言 + 时间 + 图斑 + 对话」四位一体 benchmark 缺失**

**修正理由**：

- **CCExpert 的 CC-Foundation-5M**（500 万对双时相 + 语言）已把「语言 + 时间」规模推到 5M。
- **DisasterM3**（NeurIPS 2025）已把「灾害子领域 + 多任务」benchmark 做出。
- **RSCC**（NeurIPS 2025 D&B）已有 62k 对灾害前后 + captions。
- **双粒度 Enhanced VLM**（C.2）已有 6 大类 20 子任务的交互式数据集。

**真正缺失的是「双时相图 + 自由语言 + 像素 mask + 多轮对话」四者并存的单一数据集**。这个表述更精确。

## 修正 2 · 残差 4（矢量多边形 + 时间联合生成为零）应**分拆为两条**

**修正理由**：

- **端到端 VLM → 像素 mask** 不再是空白——ViLaCD-R1（两阶段 MIR + MGD） + UniChange（单阶段 Token-Driven Decoder）两条路线并存。你研究应关注这两条路线的**公允对比**（尚无人做），而非认为这片领域全空。
- **端到端 VLM → 矢量多边形**（+ 时间）仍然是空白——GeoGround 的 Text-Mask 单时相可做，双时相矢量变化输出完全无人涉足。**这才是真正的护城河方向**。

## 修正 3 · 残差 2（>2 时相 SITS 研究空白）应**修正为「SITS foundation model 与 VLM 的融合范式缺失」**

**修正理由**：

- **UniRS（视频路径）+ TAMMs（TAM 适配器路径）** 已提供 >2 时相 VLM 的两条并行路线。
- **Prithvi-EO-2.0 + TiMo + TimeSenCLIP** 三大 SITS foundation model 已提供视觉基座。
- 真正缺的是**把 SITS foundation model（Prithvi-EO-2.0 / TiMo）作为 VLM 视觉 backbone 来训练一个 multi-temporal RS-VLM**——目前没人做这件事。这是你研究的**第二条护城河方向**。

---

# 补遗后的两条新残差

**新残差 1 · SITS foundation model 与 VLM 的融合范式缺失** → 汇入 V 反身度量

Prithvi-EO-2.0 / TiMo 等时序 foundation model 的视觉表征是否能「无缝接入」LLM 的语言空间，尚无系统研究。Prithvi 的 temporal + location embeddings 与 Qwen2.5-VL 的 MRoPE 的相互转换关系也未被探索。解这条残差需要在 §V 反身度量章里新设「时序表征对齐度量」。

**新残差 2 · Token-Driven Decoder vs Two-Stage MGD 两条 VLM→mask 路线的公允比较尚无人做** → 汇入 IV 生成对齐

ViLaCD-R1 的 MIR + MGD 与 UniChange 的 [T1]/[T2]/[CHANGE] token 在同一 benchmark 上的公允对比、RL 增益在 Token-Driven Decoder 路线上的表现、两条路线在矢量多边形输出上的可扩展性——这三件事都无人回答。这是你研究第三个切入点。

---

# 更新后的谱系图

```jsx
        产出形式（空间）
          ↑
          │
矢量多边形│   ?          ?            ?              ?
          │ PolyBuilding ?            ?              ?
像素 mask │ GeoPixel    UniChange     ViLaCD-R1       ?
          │ GeoGround   Change-LISA   TAMMs(forecast) ?
bbox      │ GeoChat     TEOChat       ChangeChat      ?
          │ LHRS-Bot    DeltaVLM      CDChat
          │ EarthDial   BTCChat       CCExpert
文本      │ RSICC       LEVIR-CC      TEOChat         UniRS(video)
          │ Delta-LLaVA Change-Agent  MV-CC           TimeSenCLIP
SITS 基座 │ Prithvi-EO-2.0 · TiMo · TimeSenCLIP（非 VLM 但视觉 backbone 候选）
          └──────────────────────────────→ 时间维度
             单时相       双时相       3–5 时相        多时相 SITS
```

坐标系右上角「多时相 SITS × 矢量多边形」仍然空白。坐标系下半部的 SITS 基座（Prithvi-EO-2.0 / TiMo / TimeSenCLIP）是可立即用于填补该空白的视觉 backbone。

---

# 你研究方向的三个实验方向修订版

**实验 1 修订** · 构造「四合一」双时相 RS-VLM benchmark：**以 CCExpert 的 CC-Foundation-5M 作为起点**（已有 5M 对图 + 文），**从中采样子集补充像素 mask + 多轮对话**——即「5M 大规模弱标注 + 20k 精标子集」的两层架构，而非从零构造 100k。工作量大幅降低。

**实验 2 修订** · 不再局限于「TAM + MIR + MGD」组合，而是做 **「UniChange Token-Driven Decoder vs ViLaCD-R1 Two-Stage MGD」的公允对比**——在同一数据集（LEVIR-CD + SECOND + 你的新 benchmark）上训练两条路线，报告精度、效率、RL 增益。这直接对应新残差 2，审稿人友好度高。

**实验 3 修订** · 不再从 GeoGround 起步，而是从 **「Prithvi-EO-2.0 视觉 backbone + Qwen2.5-VL LLM + UniChange token-driven decoder + 矢量多边形顶点序列输出」** 起步——这等于同时回应新残差 1（SITS foundation 与 VLM 融合）+ 主章残差 4（矢量多边形 + 时间）两大空白。工程量大但护城河最深。
