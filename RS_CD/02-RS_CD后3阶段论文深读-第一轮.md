# RS_CD 后 3 阶段论文深读：第一轮

范围：
- 对应 `5 阶段` 总纲里的 **第 3-5 阶段**
- 目标不是穷尽所有论文，而是先抓住**定义阶段边界**的关键论文
- 读取依据：当前 `RS_CD` 目录内部材料 + 论文一手页面（arXiv / CVF Open Access / OpenReview）

阅读原则：
- 不按“性能最好”选，而按“最能定义阶段”的论文选
- 每篇都回答 5 个问题：
  - 这篇真正想解决什么残差？
  - 它的方法核心到底是什么？
  - 它为什么属于这个阶段？
  - 它真正推进了什么，而不是表面说了什么？
  - 它还留下了什么残差？

## 这一轮的核心结论

后 3 个阶段不能混着看。

- **第 3 阶段** 的关键词是：`借用 foundation model 的能力`
- **第 4 阶段** 的关键词是：`开放词汇 + 免训练 + query-conditioned`
- **第 5 阶段** 的关键词是：`变化不再只是输出，而是变成可统一建模的理解对象`

真正的跃迁不是从一个模型换到另一个模型，而是：

- 从“做更强的 CD 网络”
- 走到“让 foundation model 参与变化判定”
- 再走到“让变化接受语言条件与开放类别”
- 最后走到“让变化成为统一的理解任务”

---

## 第 3 阶段：基础模型迁移

这一阶段最该读的，不是所有基座适配论文，而是 5 篇边界最清楚的。

### 1. TTP

- 论文：[Time Travelling Pixels: Bitemporal Features Integration with Foundation Model for Remote Sensing Image Change Detection](https://arxiv.org/abs/2312.16202)
- 时间：`2023-12-23`

#### 它真正解决的残差

前一阶段的问题是：即便 Transformer 已经把全局关系做出来了，CD 仍然主要在自己的监督数据里学。  
这意味着：

- 数据少时泛化差；
- 模型知识边界基本被 CD 数据集锁死；
- 很难直接吃到 foundation model 已有的通用先验。

TTP 直面的就是这条残差：

**能不能把 SAM 这类 foundation model 的“通用视觉知识”转译成双时相变化知识。**

#### 方法核心

按论文摘要和当前目录整理，TTP 的关键不是简单换 backbone，而是三件事同时做：

- 用 `SAM` 作为知识源；
- 用 `LoRA / 轻量注入` 处理自然图像到遥感的域偏移；
- 用时间相关的激活 / 融合机制，把双时相信息真正写进 feature interaction，而不是只把两张图拼起来。

#### 为什么它属于第 3 阶段

因为它的本质不是开放词汇，也不是语言接口。  
它仍然是监督 CD，但它第一次清楚地说：

**我不再只从 CD 数据学，我要从 foundation model 借知识。**

#### 它真正推进了什么

它把“foundation model for CD”从口号变成了可操作范式：

- 主干冻结或弱微调；
- 双时相模块另行设计；
- 用基础模型做上游知识源，而不是 end-to-end 重训。

#### 它留下的残差

- 仍依赖监督；
- 语义能力仍不强；
- foundation model 的知识是借来的，不是时序任务自己长出来的。

### 2. SAM-CD

- 论文：[Adapting Segment Anything Model for Change Detection in HR Remote Sensing Images](https://arxiv.org/abs/2309.01429)
- 时间：`2023-09-04`

#### 它真正解决的残差

SAM 强在单图对象分割，但天然不懂：

- 双时相；
- 变化；
- RS 的窄域目标。

SAM-CD 的残差判断非常明确：

**如果 SAM 直接拿来做 CD 不行，那能不能保留它的视觉 recognition 能力，只在外围做最小适配。**

#### 方法核心

按论文摘要与本目录整理，它做了两件关键事：

- 用 `FastSAM / SAM` 的视觉编码器做 frozen feature extractor；
- 用卷积 adaptor 聚合 change-specific 信息；
- 额外引入 task-agnostic semantic learning branch，尝试从双时相中抽 semantic latent。

#### 为什么它属于第 3 阶段

因为它还是标准 supervised CD，但它已经不再把 CD 当成“从零训练一个模型”的问题，而是把它改写成：

**如何适配现成视觉 foundation model。**

#### 它真正推进了什么

它证明了一个工程事实：

**冻结强基座 + 轻适配器** 对 RS-CD 是成立的。

这件事很重要，因为后面的 `BAN`、`training-free SAM 路线`，都默认了这个前提。

#### 它留下的残差

- 语义仍弱；
- 变化仍主要被当作二值任务；
- 依赖监督，没有把“变化”变成开放对象。

### 3. ChangeCLIP

- 论文：[Single-temporal Supervised Remote Change Detection for Domain Generalization](https://arxiv.org/abs/2404.11326)
- 时间：`2024-04-17`

#### 它真正解决的残差

第 3 阶段里不只是 SAM 路线，CLIP 路线的关键残差也很清楚：

- CLIP 懂语义；
- 但它不懂变化；
- 更不懂像素级遥感变化。

ChangeCLIP 直接瞄准的是：

**如何把视觉-语言预训练的语义优势变成 change detection 的泛化能力。**

#### 方法核心

摘要里最重要的三个关键词是：

- `multimodal contrastive learning`
- `dynamic context optimization for prompt learning`
- `single-temporal controllable AI-generated training strategy (SAIN)`

也就是说，它不只是“把 CLIP 拿来做分类”，而是：

- 用 prompt 让类别语义进入 CD；
- 用单时相合成训练策略缓解 pair-labeled data 稀缺；
- 目标直指 `domain generalization`。

#### 为什么它属于第 3 阶段

因为它的核心仍是 foundation-model adaptation，而不是开放词汇变化本身。  
它还没有把任务改写成 arbitrary concept change detection，而是在做：

**如何让 CD 模型借助 CLIP 获得更稳的跨域语义先验。**

#### 它真正推进了什么

它第一次比较系统地把：

- 语义 prompt
- 单时相数据利用
- 跨域 change generalization

放进了同一个框架里。

#### 它留下的残差

- 还是 supervised setting；
- 还是以既定任务为中心；
- 开放词汇只是被预示，还没有完全展开。

### 4. BAN

- 论文：[A New Learning Paradigm for Foundation Model-based Remote Sensing Change Detection](https://arxiv.org/abs/2312.01163)
- 时间：`2023-12-02`

#### 它真正解决的残差

前面的 SAM-CD、TTP、ChangeCLIP 其实都还有一个共同问题：

**每个 foundation model 都要单独设计一套适配方式。**

BAN 的目标不是只把某一个大模型用好，而是：

**把 foundation model 适配 CD 这件事，抽象成一个更通用的范式。**

#### 方法核心

它提出了 `Bi-Temporal Adapter Network (BAN)`：

- foundation model 冻结；
- 通过 `Bi-TAB` 抽 task/domain-specific 双时相特征；
- 用 bridging module 做特征选择、对齐、注入。

#### 为什么它属于第 3 阶段

因为它把第 3 阶段真正说清楚了：

**第 3 阶段不是“用某个大模型”，而是“如何系统性地把 foundation model 的知识引入 CD”。**

#### 它真正推进了什么

BAN 的推进不在某个数字，而在范式：

- foundation model 不再是孤立案例；
- adapter 成为抽象层；
- CD 开始和“基础模型生态”接轨。

#### 它留下的残差

- 还是 supervised；
- 还是把变化定义在任务头里；
- 还没有迈到开放词汇与 query-conditioned。

### 5. MTP

- 论文：[MTP: Advancing Remote Sensing Foundation Model via Multi-Task Pretraining](https://arxiv.org/abs/2403.13430)
- 时间：`2024-03-20`

#### 它真正解决的残差

前面的 foundation model 多半不是为 CD 预训练的。  
所以第 3 阶段的深层问题其实是：

**如果大基座从一开始就没见过 RS 的任务结构，那后面再适配总会有 task discrepancy。**

MTP 正是在解决这点。

#### 方法核心

它的核心不是单一结构，而是：

- shared encoder；
- task-specific decoder；
- 在 `SAMRS` 上做 supervised multi-task pretraining；
- 然后迁移到包括 `change detection` 在内的多个下游任务。

#### 为什么它属于第 3 阶段

因为它不是开放词汇，也不是语言接口。  
它做的是更根的事情：

**把 CD 的需要往 pretraining 阶段前移。**

#### 它真正推进了什么

它把问题从：

- “怎么适配别人训练好的基础模型”

往前推成：

- “能不能直接训练更适合 RS 任务结构的 foundation model”

这使得 `foundation model for CD` 不再只是借用，而开始有领域原生化倾向。

#### 它留下的残差

- 监督成本大；
- 仍未处理开放类别与语言接口；
- 对“变化”本体依然是任务层使用，不是状态层持有。

---

## 第 4 阶段：开放词汇与免训练

这个阶段的关键不是某一个 backbone，而是**任务定义被改写了**。

### 6. AnyChange

- 论文：[Segment Any Change](https://arxiv.org/abs/2402.01188)
- 时间：`2024-02-02`

#### 它真正解决的残差

第 3 阶段的残差是：

- 还是监督；
- 还是 closed-set；
- 还是 task-specific model。

AnyChange 直接问：

**不给 CD 专门训练，只用 SAM，本身能不能做 zero-shot change detection。**

#### 方法核心

摘要里的核心机制非常清楚：

- `training-free adaptation`
- `bitemporal latent matching`
- 利用 SAM latent space 中的 intra-image / inter-image semantic similarities
- 再加 point query 机制做 object-centric change detection

#### 为什么它属于第 4 阶段

因为它第一次让“training-free CD”变成一个明确方向。  
这已经不是“如何更好适配 foundation model”，而是：

**如何不训练，直接让 foundation model 产出变化。**

#### 它真正推进了什么

它把第 4 阶段的一个极端端点立住了：

- 定位器驱动；
- 先做对象分割；
- 再做对应关系；
- 不把变化当 supervision 学出来，而是从对应失败中显现。

#### 它留下的残差

- 更强在实例级变化；
- 对细粒度语义变化弱；
- 语言接口还很弱。

### 7. Semantic-CD

- 论文：[Semantic-CD: Remote Sensing Image Semantic Change Detection towards Open-vocabulary Setting](https://arxiv.org/abs/2501.06808)
- 时间：`2025-01-12`

#### 它真正解决的残差

AnyChange 解决的是 “training-free object-level change”。  
但另一条更深的残差是：

**变化类别能不能不被固定标签表锁死。**

Semantic-CD 就是在回答这条。

#### 方法核心

摘要明确给出 4 个部件：

- bi-temporal CLIP visual encoder
- open semantic prompter
- binary CD decoder
- semantic CD decoder

它的真正做法不是直接 end-to-end 统一，而是：

**用解耦多任务把“哪里变了”和“变成什么”同时处理。**

#### 为什么它属于第 4 阶段

因为它明确把 `semantic change detection` 推到了 `open-vocabulary`。

第 4 阶段的本质就在这里：

**变化开始接受开放类别定义，而不再是固定 label space。**

#### 它真正推进了什么

它把 “开放词汇 change” 这件事从想法变成了正式任务定义。

#### 它留下的残差

- 还不是 training-free；
- 开放类别在两时相之间仍不稳定；
- 概念响应的可比性还没有真正解决。

### 8. OpenDPR

- 论文：[OpenDPR: Open-Vocabulary Change Detection via Vision-Centric Diffusion-Guided Prototype Retrieval for Remote Sensing Imagery](https://arxiv.org/abs/2603.27645)
- 时间：`2026-03-29`
- 状态：论文页标注 `Accepted by CVPR 2026`

#### 它真正解决的残差

Semantic-CD 之后，一个更深的残差暴露出来：

**变化区域找到了，类别到底靠什么认。**

OpenDPR 的价值就在于，它把这个问题讲得很明确：

- `change proposal` 不是主瓶颈；
- `category identification` 才是。

#### 方法核心

摘要里核心结构是两段式：

- visual foundation models 做 class-agnostic change proposals
- VLM / prototype retrieval 做 category identification

它又进一步指出：

- 图文匹配型 VLM 对细粒度 land-cover 类别不够强；
- 所以引入 diffusion-guided prototype retrieval；
- 同时再加 `S2C` 去补 change localization。

#### 为什么它属于第 4 阶段

因为它还是开放词汇与免训练的问题域。  
但它更进一步，把第 4 阶段的核心瓶颈重述为：

**开放类别变化的识别不能只靠文本相似度。**

#### 它真正推进了什么

它把 OVCD 从“语义提示 + 差分”推进到“proposal + identification 的分解框架”。

#### 它留下的残差

- 仍是组合 pipeline；
- prototype 覆盖长尾类别仍不稳；
- 还不是统一时序语义模型。

### 9. CoRegOVCD

- 论文：[CoRegOVCD: Consistency-Regularized Open-Vocabulary Change Detection](https://arxiv.org/abs/2604.02160)
- 时间：`2026-04-02`

#### 它真正解决的残差

OpenDPR 之后，第 4 阶段最深的残差被进一步集中成一句话：

**两时相的 dense concept response 根本不直接可比。**

CoRegOVCD 就是在正面解决这件事。

#### 方法核心

摘要里最关键的四个词是：

- calibrated posterior discrepancy
- Competitive Posterior Calibration
- Semantic Posterior Delta
- geometry-aware / regional consistency

这说明它的核心不是再做更强 backbone，而是：

**把跨时相语义响应先校准，再做差。**

#### 为什么它属于第 4 阶段

因为这正是开放词汇 CD 的核心残差，而不是旧式监督 CD 的问题。

#### 它真正推进了什么

它第一次把“跨时相概念可比性”单独提出来，作为 OVCD 的一等问题。

#### 它留下的残差

- 还是后验校准思路；
- 还不是长期状态建模；
- 变化本体仍未内生化。

---

## 第 5 阶段：变化理解与统一系统

这一阶段的特点是：变化不再只是 detection output，而开始被当作统一理解对象。

### 10. Change-Agent

- 论文：[Change-Agent: Towards Interactive Comprehensive Remote Sensing Change Interpretation and Analysis](https://arxiv.org/abs/2403.19646)
- 时间：`2024-03-28`

#### 它真正解决的残差

前面的方法无论多强，大多还是：

- 单一任务；
- 固定接口；
- 结果静态。

Change-Agent 直接瞄准的问题是：

**真实场景里，变化分析不是一个单一输出，而是一个交互式、多任务、可延展的过程。**

#### 方法核心

摘要里结构非常清楚：

- `MCI model` 作为 eyes
- `LLM` 作为 brain
- pixel-level CD + semantic-level change captioning 双分支
- 再加 Change-Agent 完成交互式分析

#### 为什么它属于第 5 阶段

因为它已经明显超出“change detection model”的范畴，进入：

**变化解释系统**

这个层级。

#### 它真正推进了什么

它把“变化检测”和“变化描述”第一次明确塞进一个 agentic interaction 框架。

#### 它留下的残差

- 依然较重；
- 对 pixel-level grounding 仍受限；
- 统一的是工具链，不是统一时序表征。

### 11. TEOChat

- 论文：[TEOChat: A Large Vision-Language Assistant for Temporal Earth Observation Data](https://arxiv.org/abs/2410.06234)
- 时间：`2024-10-08`

#### 它真正解决的残差

VLM 适配到遥感后，很多系统仍然只能看单图。  
而 temporal EO 的核心问题是：

**系统能不能围绕时间序列对话。**

#### 方法核心

摘要清楚说明：

- 构建 instruction-following temporal EO dataset
- 任务包含 building change、damage assessment、semantic change detection 等
- 模型是 temporal sequence aware vision-language assistant

#### 为什么它属于第 5 阶段

因为它已经不是简单 caption / QA，而是：

**temporal EO assistant**

换句话说，变化只是它支持的多个时间任务之一。

#### 它真正推进了什么

它把“变化”从一个专门任务，推进成 temporal EO assistant 的基础能力之一。

#### 它留下的残差

- 更偏 assistant，未必对精细 mask 最优；
- 多时相理解能力仍受训练任务范围限制；
- 还不是统一 BCD/SCD 框架。

### 12. RSCC

- 论文：[RSCC: A Large-Scale Remote Sensing Change Caption Dataset for Disaster Events](https://arxiv.org/abs/2509.01907)
- OpenReview 页面：[RSCC @ OpenReview](https://openreview.net/forum?id=yn2fJYBKEB)
- 时间：`2025-09-02`

#### 它真正解决的残差

变化理解系统不可能只靠模型，没有数据基座就不成立。  
RSCC 解决的是：

**变化描述这条线长期数据太小、场景太窄、不足以支撑真正的大模型训练。**

#### 方法核心

它本身不是模型创新，而是：

- `62k+` 灾害 pre/post 图像对；
- rich human-like change captions；
- 直接瞄准 disaster-aware bi-temporal understanding。

#### 为什么它属于第 5 阶段

因为它给的是“变化理解系统”的数据基础，而不是普通 CD benchmark。

#### 它真正推进了什么

它把 change captioning 从小规模实验任务拉到更像真正训练资源的规模。

#### 它留下的残差

- 仍主要是灾害场景；
- 更像数据扩张，还不是统一方法论。

### 13. UniChange

- 论文：[UniChange: Unifying Change Detection with Multimodal Large Language Model](https://arxiv.org/abs/2511.02607)
- 时间：`2025-11-04`

#### 它真正解决的残差

一个很深但常被忽略的问题是：

**BCD 和 SCD 长期是两套模型、两套头、两套数据体系。**

UniChange 直接试图统一它们。

#### 方法核心

摘要里最关键的是：

- 用 MLLM 统一 `BCD` 和 `SCD`
- 引入 `[T1]`、`[T2]`、`[CHANGE]`
- 用 text prompts 代替固定分类头
- 允许从 label 定义冲突的多源数据里一起学

#### 为什么它属于第 5 阶段

因为这已经不是“开放词汇 CD”本身，而是：

**变化任务体系的统一。**

#### 它真正推进了什么

它把“变化”从单个任务进一步推进成：

- 一个 query-guided 统一接口；
- 一个可以跨 BCD / SCD 数据集共同学习的问题。

#### 它留下的残差

- 统一的是任务接口，不是时序世界状态；
- 仍主要围绕双时相任务展开。

### 14. Delta-LLaVA

- 论文：[Decoding the Delta: Unifying Remote Sensing Change Detection and Understanding with Multimodal Large Language Models](https://arxiv.org/abs/2604.14044)
- 时间：`2026-04-15`

#### 它真正解决的残差

第 5 阶段最关键的一条残差，被这篇写得非常清楚：

**通用 MLLM 在多时相变化理解上存在 temporal blindness。**

#### 方法核心

摘要里有三件关键模块：

- `Change-Enhanced Attention`
- `Change-SEG` with Change Prior Embedding
- `Local Causal Attention`

同时配套 `Delta-QA`，把 segmentation 与 VQA 放在一个 change understanding benchmark 里。

#### 为什么它属于第 5 阶段

因为它已经不满足于：

- mask；
- caption；
- 单一问答。

它想做的是：

**统一的多时相变化理解。**

#### 它真正推进了什么

它是目前最接近“变化理解系统统一框架”的工作之一。  
不是因为它一定最终最好，而是因为它第一次把：

- 时相差分机制
- 空间定位
- 语言问答
- 统一 benchmark

明确放进同一框架。

#### 它留下的残差

- 还是双/三时相主导；
- 还没有走向长期状态与反事实变化；
- 更像统一多任务，而不是统一世界状态。

---

## 第一轮深读后的总收束

### 第 3 阶段真正完成了什么

不是“用了大模型”，而是：

**CD 开始系统性借用 foundation model 的先验。**

它的代表不是某个单论文，而是 `SAM-CD / ChangeCLIP / BAN / MTP` 这一组共同说明的事实：

- foundation model 先验是可迁移的；
- adapter 是核心中介；
- 但能力多数仍是借来的。

### 第 4 阶段真正完成了什么

不是“更自由地分类变化”，而是：

**变化开始接受语言条件、开放类别定义和免训练推断。**

`AnyChange / Semantic-CD / OpenDPR / CoRegOVCD` 这组论文共同说明：

- 变化不再由固定标签头定义；
- 变化开始由 query、开放类别、跨时相概念比较来定义。

### 第 5 阶段真正完成了什么

不是“又多了几个 VLM 任务”，而是：

**变化开始被组织成统一理解任务。**

`Change-Agent / TEOChat / UniChange / Delta-LLaVA` 这组论文共同说明：

- 变化检测、变化描述、变化问答、BCD/SCD 统一，不再是完全分裂的子任务；
- 但这还只是“统一任务接口”，不是“统一时序状态空间”。

## 现在最关键的总残差

第一轮深读之后，我认为最值得保留的总残差是：

**RS-CD 已经能借用 foundation model，把变化做成开放词汇、可指代、可问答、可统一任务接口的对象；但它还没有把变化变成系统内部自持的稳定时序状态。**

换句话说：

- 第 3 阶段解决了“知识不够”；
- 第 4 阶段解决了“类别不够开放”；
- 第 5 阶段解决了“任务不够统一”；

但还没有解决：

- **变化到底是不是一个被系统真正持有的状态对象。**

## 下一轮阅读顺序

如果继续第二轮深读，我建议按这个顺序推进：

1. `OpenDPR` + `CoRegOVCD` + `Seg2Change`
   目标：把第 4 阶段彻底压实，特别是“跨时相概念可比性”。

2. `UniChange` + `Delta-LLaVA`
   目标：区分“统一任务接口”和“统一变化理解”的边界。

3. `RSCC` + `TEOChat` + `Change-Agent`
   目标：补齐第 5 阶段的数据与系统层。

