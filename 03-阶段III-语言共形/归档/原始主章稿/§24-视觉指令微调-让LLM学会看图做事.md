# §24

标题: 视觉指令微调
类型: 主章
要点: 把 §23 的架构模板配上指令数据；重心从架构转移到「LLM 给 VLM 发教材」；指令遵循能力实际上是 LLM 自身能力的视觉激活，而非从零发展的视觉推理

# 阶段 III · 视觉指令微调：让 LLM 学会「看图做事」（InstructBLIP / LLaVA-1.5 / mPLUG-Owl2 / Qwen-VL / ShareGPT4V）

作者 / 机构: Dai 等 (Salesforce) / Liu 等 (Wisconsin–Madison + Microsoft) / Ye 等 (Alibaba) / Bai 等 (Alibaba) / Chen 等 (Shanghai AI Lab + CUHK)
共形维度: 度量, 材料
关键贡献: 在 §23 完成「视觉挂接 LLM」的架构模板之后，把重心从「架构」转移到「数据 + 训练配方」——用 GPT-4 / GPT-4V 等强大的 LM 自动合成指令数据，让 VLM 学会听从任意自然语言指令看图做事。这是 NLP 侧 InstructGPT / FLAN / Alpaca 在多模态端的平移。同时催生 MM-Vet / MMBench / POPE / SEED-Bench 等新评估基准，把「指令跟随」当作第一位的能力。
年份: 2023–2024
序号: 24
残差 / 它催生了什么: VLM 的指令遵循实际上是「LLM 自己的指令能力 + 视觉输入激活」，不是独立发展出的「视觉推理」 → 催生 §25 对原生视觉推理的尝试；数据合成的环是「GPT-4V → VLM → VLM 评估」的单循环，评估本身已经「共形」于另一个 VLM → 汇入 V 反身度量；幻觉问题凸显 → 汇入 §27 账单。
类型: 训练范式 / 数据
阶段: III · 语言共形

🎯
**主题**：§23 做好了「视觉挂接 LLM」的接口，但这个接口仅有「看图说话」的能力。§24 要回答的是：怎么让这个接口能**听从任意指令**（不只是 captioning 或 VQA 这种固定任务）？五篇一起从范式到数据到评估回答这一问。关键识别：**指令能力是“转移”来的不是“从零教会”的**——这点在机制追问的第五节展开。

## 1 · InstructBLIP —— *InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning* (Dai 等, Salesforce, NeurIPS 2023)

**共形贡献**：第一个系统化的视觉指令微调工作。架构在 BLIP-2 上加一个 **instruction-aware Q-Former**：Q-Former 的 learnable query 不再与指令文本无关，而是在 cross-attention 里让 query 也参与指令 token 的计算——这样抽取的视觉特征是**按指令裁剪**的。数据侧把 **26 个 VL 数据集**（VQA、Captioning、Reasoning、OCR、Grounding等）统一转为指令格式，用模板 prompt 包装原任务。可以看成 NLP 中 **FLAN / T0** 在多模态端的对应物——把现有任务的 prompt 模板化就得到指令数据。训练上沿用 BLIP-2 的两阶段：先表示预训练，再指令微调（只训 Q-Former）。

🔗 [https://arxiv.org/abs/2305.06500](https://arxiv.org/abs/2305.06500)

## 2 · LLaVA-1.5 —— *Improved Baselines with Visual Instruction Tuning* (Liu 等, Wisconsin–Madison + Microsoft, CVPR 2024)

**共形贡献**：把 LLaVA 的概念验证代码库打磨成可复现的「数据配方经典化」。三件关键改动：**两层 MLP 投影**（从 LLaVA 的单层线性换成 MLP）给了适配器更强的映射能力；**混入学术 VQA 数据**（VQAv2 / GQA / OKVQA / OCRVQA 等）结合 GPT-4 合成指令，**证明传统 VQA 数据在指令微调框架里仍然有主力价值**；**图像分辨率从 224 升到 336**对 OCR 和细节任务提升显著。关键判断：**指令数据不需要全是 GPT-4 合成的新数据，旧的 VQA 常模板化后仍然是高效教材**。数据总量仅约 665K，却在多个 benchmark 上超过更复杂的模型。

🔗 [https://arxiv.org/abs/2310.03744](https://arxiv.org/abs/2310.03744)

## 3 · mPLUG-Owl2 —— *mPLUG-Owl2: Revolutionizing Multi-modal Large Language Model with Modality Collaboration* (Ye 等, Alibaba, arXiv 2023)

**共形贡献**：提出 **Modality-Adaptive Module**（MAM）——在 LLM 的每个 Transformer 层里为视觉 token 和文本 token 分别配一套 **独立的 Key/Value 投影**而共享 Query 投影 + FFN。这样的效果：视觉 token 和文本 token 在 attention 里能“对话”（共享 Q就能在同一空间比较），但各自有各自的 KV 表示（不会被对方的统计压平）。**模态协作不再靠“把视觉翻译为文本软 token”一条路**，而是将视觉保持为一类独立 token 类型参与混合 attention。三阶段训练：多模态预训练 → 多任务联合 → 指令微调。

🔗 [https://arxiv.org/abs/2311.04257](https://arxiv.org/abs/2311.04257)

## 4 · Qwen-VL —— *Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond* (Bai 等, Alibaba, 2023)

**共形贡献**：将 §24 的能力清单明确扩展到四项：多语言（英/中）、细粒度 **grounding 与 referring**（模型能输出坐标 〈45, 123, 78, 201》指向图中某块区域，也能理解输入的坐标）、文字识别（OCR）、多图对话。关键设计：把 bounding box **编码为文本 token**——特殊的《》标记 + 四个整数，直接融入 LLM 的文本词表。三阶段训练：pretrain（冻 LLM）→ multi-task 预训练（解冻）→ supervised fine-tuning（解冻 + 指令数据）。意义：**Grounding 能力不再从架构层设计跟踪头，而是直接在文本 token 空间里用数字表达**——LLM 的词表被再度被用作万用接口。

🔗 [https://arxiv.org/abs/2308.12966](https://arxiv.org/abs/2308.12966)

## 5 · ShareGPT4V —— *ShareGPT4V: Improving Large Multi-Modal Models with Better Captions* (Chen 等, Shanghai AI Lab + CUHK, 2023)

**共形贡献**：不改架构、不改训练配方，只做一件事：用 **GPT-4V** 为 100K 图像重新生成详细、准确、结构化的 caption，并用这批 100K 高质量 caption 替换或补充到现有指令微调数据中。结果：LLaVA-1.5 / Qwen-VL 等多个基线在 MM-Vet / MMBench / SEED-Bench 上均有显著提升。关键判断：**质量辈于数量**——100K 高质量 caption 超过 1M 低质量 caption。不仅于此：ShareGPT4V 正式把「用更强的多模态模型来教更弱的多模态模型」当作一种可复用的方法学。但同时它也把一个根本问题扔出来：**VLM 学的到底是图像的真实关系，还是 GPT-4V 的「看图风格」？**

🔗 [https://arxiv.org/abs/2311.12793](https://arxiv.org/abs/2311.12793)

---

# 关于 §24 五篇的机制追问

## 一、什么叫「视觉指令微调」：输入空间从「固定任务」到「任意自然语言指令」

### 从 §23 的能力到 §24 的能力

- §23 的能力：给图像 + 给一个固定任务词（captioning / VQA / retrieval），模型产生对应输出。
- §24 的能力：给图像 + 给**任意自然语言指令**，模型能生成对应回答。指令可以是：
    - 「描述这张图中的人物关系」
    - 「分析这张图表的趋势、用 markdown 列出关键数值」
    - 「这两张图有什么差异」
    - 「按表格内容生成 SQL」
    - 「用英文回答这张中文发票的总金额」

关键区别：**输入空间从「一个固定任务」变为「任意自然语言指令」**。任务本身被词表化了：任务 ≈ 指令句子。

### 为什么这件事是「NLP 侧 InstructGPT 的平移」

这条路在 NLP 侧已经走过一遍：

- GPT-3 只会「接续上文」（like §23 的 VLM）——能力强但需要用户巧妙 prompt。
- InstructGPT / ChatGPT 重新按「人用自然语言下指令」对齐 → 能力层没变、但接口层变了，用户不再需要会 prompt engineering。

§24 正是把这个接口转换平移到多模态端：

- §23 的 VLM 只会「看图接语」（对应 GPT-3）。
- §24 的 VLM 能「看图听指令」（对应 InstructGPT）。

不过一个重要区别：NLP 侧的 InstructGPT 用了大量人工标注的指令-回答对 + RLHF；而视觉指令微调几乎不依赖人工标注，**直接用另一个模型生成指令数据**。这是下一节的主要话题。

---

## 二、数据合成：「LLM 给 VLM 发教材」这件事的双重性

### 指令数据主要来自什么

| 方法 | 主要数据来源 | 规模 |
| --- | --- | --- |
| LLaVA / LLaVA-1.5 | GPT-4（纯文本）从 COCO caption + bbox 合成指令 + 学术 VQA | 158K + 665K |
| InstructBLIP | 26 个 VL 数据集 统一模板化 + 一部分 GPT-4 生成 | 数千万量级 |
| Otter / MIMIC-IT | 多图/视频指令，部分由 GPT-4 生成 | 2.8M |
| Qwen-VL-Chat | 自产 + GPT-4 生成 + 人工校验 | 千万级 |
| ShareGPT4V | GPT-4V（多模态）为 100K 图像重新生成详细 caption | 100K 高质 + 1.2M 微调 |

### 「LLM 给 VLM 发教材」的双重性

指令数据合成的核心分差：

- 早期（LLaVA / InstructBLIP）：用**纯文本 LLM**（GPT-4）读图像的标注（caption + bbox）生成指令。LLM 实际上看不见图，只是「口述描述的指令作者」。
- 后期（ShareGPT4V）：用**多模态 LLM**（GPT-4V）直接看图生成指令/caption。LLM 真的看见了图。

两种模式都有一个共同的场景结构：**强的模型给弱的模型发教材**。这里有两重意味：

- 输入侧：**教材的内容**（指令 + 回答）完全由教师模型的风格决定。VLM 学到的并不是「图像本身的真实关系」，而是「教师模型对图像讲解的风格」。
- 评估侧：VLM 的输出被另一个 LLM（通常也是 GPT-4）打分，打分为「更接近教师风格」的回答分高。

### 从共形视角：双重中介带来的生对应性保证的问题

记 §21 的起点：alt-text 是人对图的描述，已经是一层语义中介。§24 的指令数据是 GPT-4V 对图的描述，是**另一层中介**。VLM 学到的映射是：

$\\text\\{图像\\} \\to \\text\\{GPT-4V 对图像的描述\\}$

而不是：

$\\text\\{图像\\} \\to \\text\\{图像的真实关系\\}$

这两者都不相同。§共形的第一要义是保相关性§——但在 §24 这里，「被保的相关性」已经被 GPT-4V 的风格筛过一遍。VLM 对图像的理解不是直接与图像保共形，而是**与《图像的 GPT-4V 解读》保共形**。

这是§共形中介§的结构性现象。在 V 反身度量中会重新审视：当评估 VLM 的模型也是 VLM / 与 VLM 同源的模型时，这个闭合回路什么时候能被打开？

---

## 三、指令数据的类型学：五大类

| 类别 | 示例指令 | 代表数据源 | 目标能力 |
| --- | --- | --- | --- |
| Conversation | 关于图像的多轮问答 | LLaVA conversation set | 对话能力 |
| Detailed description | 「详细描述这张图」 | LLaVA description / ShareGPT4V | 长文本生成、细节覆盖 |
| Complex reasoning | 「为什么这个场景看起来危险」 | LLaVA reasoning set | 多步推理、因果分析 |
| Grounded instruction | 「在图中指出起居室的沙发」 | Qwen-VL / Shikra / Kosmos-2 | 坐标输出、空间定位 |
| Multi-image / video | 「比较这两张图的差异」 | MIMIC-IT / Video-ChatGPT | 跨图比对、时间序列 |

### 为什么必须是五大类而不是一大类

每一类开训的是一组不同的能力维度：

- **Conversation** 训的是上下文一致性和对话轮次管理。不训这个，VLM 每一轮都洗掉上下文。
- **Detailed description** 训的是长文本生成与细节覆盖。不训这个，输出就喷不出三行。
- **Complex reasoning** 训的是多步推理与因果结构。不训这个，VLM 只会简单描述，不会「因为…所以…」。
- **Grounded instruction** 训的是位置输出格式。不训这个，即使 LLM 能“认出」某物体，也不会说「在坐标 〈45, 123, 78, 201》 处」。
- **Multi-image / video** 训的是跨输入对比与时序。不训这个，多图输入时模型容易只用第一张或最后一张。

这五类的混合比例之争一直是 §24 的曲线之一：LLaVA 初版没有 grounded / multi-image；Qwen-VL 第一次把 grounded 整合到主流；LLaVA-1.5 把传统 VQA 重新带回；MIMIC-IT 深入 multi-image。「指令数据配方」是一个以每年运行次序归纳的工程参数空间。

---

## 四、训练配方：两阶段 vs 三阶段，以及「解冻到什么程度」

### 三种配方的对比

|  | 阶段 1 | 阶段 2 | 阶段 3 |
| --- | --- | --- | --- |
| LLaVA / LLaVA-1.5 | pretrain 投影层（冻 ViT + 冻 LLM） | instruction tuning（冻 ViT + **解冻 LLM**） | — |
| InstructBLIP | 沿用 BLIP-2 两阶段预训练 | instruction tuning（只训 Q-Former） | — |
| mPLUG-Owl2 / Qwen-VL | 多模态预训练（冻 LLM） | 多任务联合训练（解冻，但用标准 VL 数据） | 指令微调（解冻，用指令数据） |

### 解冻 LLM 的三种题律

- 全模解冻：LLaVA / InstructBLIP。训练成本高，需要较多指令数据来防止灾难性遗忘。
- LoRA 微调：Qwen-VL-Chat。参数高效，保持原 LLM 能力，但指令遵循深度有限。
- 部分层解冻 / 新增模块：mPLUG-Owl2 的 MAM。只解冻和新增 Modality-Adaptive Module 相关的参数。

### 为什么「解冻到什么程度」是 §24 的核心技术变量

训 LLM 是是否解冻，权衡的是两件事：

- 能力获得：**解冻越多， LLM 有了越多自由度适应新的输入分布（视觉软 token + 多模态指令 prompt）**，表现在 benchmark 上更好。
- 能力损失：**解冻越多， LLM 越可能在小量指令数据上过拟合、丢掉原本的推理能力和世界知识**（灾难性遗忘）。

这两条曲线的交叉点决定最佳解冻程度。也是为什么 §24 出现了各种变种解冻策略——LoRA、分层学习率、击射式解冻、MAM 这种解冻方式——权衡都在这条曲线上找最佳点。

---

## 五、指令能力到底从哪里来：一个常被忽略的核心观察

### 反直觉的数据量对比

- LLaVA-1.5 的指令数据：约 665K。
- BLIP-2 / LLaVA 的预训练图文对：数百 M 到 B 级。
- InstructGPT 的 NLP 指令数据 + RLHF：数十K 到 数百K。

问题：为什么仅凭几十K-百K的指令数据（相比于预训练数据是万分之一的级别）就能让 VLM “学会”听指令？

### 答案：指令能力并非 VLM 自己学到的，而是从 LLM 那里「转移」来的

LLM 在 InstructGPT 阶段已经学会了“听指令”。它知道：

- 「请描述…」开头的输入应该产生描述性输出。
- 「为什么…」开头的输入应该产生原因分析。
- 「列出…」开头的输入应该产生列表输出。

这些都是在 NLP 侧预训练 + 指令对齐阶段学到的。视觉指令微调实际上做的事：

- **让 LLM 意识到**：「当输入是‘视觉软 token + 自然语言指令’时，指令应该被理解为针对这些视觉 token 的、按原先的指令方式来回答」。
- **同时让 Q-Former / 投影层 发出的视觉软 token 适配 LLM 的指令模板**。

**指令微调不是“教会”而是“激活”**。它激活的是 LLM 已有的指令能力，并让它与新的输入模态（视觉软 token）兼容。

### 这个观察的观察性含义

1. **base LLM 越强，VLM 指令能力越强**。Vicuna → LLaMA-2 → Qwen-2 进化中，即使视觉部分不改，VLM 能力也随之上升。
2. **指令数据的多样性比数量重要**。既然是激活而不是教会，需要的是「让 LLM 认出各种指令模式在视觉输入下的对应表现」，而不是「从头学」。
3. **VLM 的“视觉推理”其实还是语言推理**。所有的推理链都走在 LLM 内部的语言 token 空间里，视觉只是提供了初始条件。一旦图像被翻译成软 token 进了 LLM，后面的一切都是 LLM 在自言自语。

第 3 条会直接成为 §25 的主要动机之一：原生多模态能否让视觉在推理中被真正”运算“，而不是被只当作很少的初始条件？V 反身度量也会问：这个“激活”观念本身在多大程度上是我们的“开汽车的人看很像自己在开难而不是车在开”的错觉？

---

## 小结：§24 的谱系内逻辑

- **InstructBLIP**：第一个系统化的视觉指令微调。提出 instruction-aware Q-Former，把 26 个标准 VL 数据集统一模板化。
- **LLaVA-1.5**：数据配方经典化。证明混入传统 VQA + GPT-4 合成 + MLP 投影 + 高分辨率这 665K 数据就够了。
- **mPLUG-Owl2**：提出 Modality-Adaptive Module，让视觉 token 与文本 token 在 attention 里“对话”但保持各自 KV。
- **Qwen-VL**：扩展多语言 / grounding / OCR；把 bounding box 编码为文本 token 直接融入 LLM 词表。
- **ShareGPT4V**：用 GPT-4V 重生 100K 高质 caption，证明**质量辈于数量**，仍旧构架下多个基线均有显著提升。

五篇合起来完成一件事：**把 §23 的架构接口配上「任意指令都可调用」的能力，且这种能力不依赖重新预训练 LLM——只需要少量高质量指令数据**。重心从「架构设计」转移到「数据配方 + 解冻判断」。

---

## 本组合力的残差

「视觉听指令」做成了，但暴露三条新残差：

1. **指令推理能力来自 LLM，不是独立的「视觉推理」**——VLM 的指令能力是被激活的而非被教会的。推理链走在 LLM 内部的文本 token 空间，视觉只是初始条件。对需要「原生视觉推理」的任务（空间推理、几何问题、纯图形 puzzle、反直觉视觉错觉），表现有系统性的弱于同类问题的文字陈述版本。这条残差**挺战 §25**：原生多模态架构能否让视觉不再只是「转为语言 token 的初始条件」，而是在推理中真正参与运算？
2. **数据合成的单循环幻觉**——GPT-4V 生成 caption 和指令 → VLM 训练 → VLM 输出被 GPT-4 评分 → 得分高的 VLM 被视为更好。这个回路整体居于同一个模型家族的「看图风格」内部。VLM 学到的不是图像本身的真实关系，而是「图像的 GPT-4V 解读」。当评估 VLM 的也是与 GPT-4V 同源的模型时，闭合全部走完。这条残差**汇入 V 反身度量**：评估 VLM 的标准什么时候可以跳出这个闭合？或能否跳出？
3. **幻觉问题凸显、而且指令微调不但没解决、反而加剧了它**——POPE / HallusionBench 显示 VLM 在「图中是否存在某物体」这种问题上的幻觉率相当高。机制：LLM 的先验分布（厘房里通常有烤箱）压过了视觉证据（这张图里没有烤箱）。指令微调让 LLM 「更自信」地回答，反而使幻觉更明显。这条残差也**汇入 §27 账单**——幻觉不是单纯的数据问题，是「语言先验 vs 视觉证据」的结构性冲突。

第 1 条挺战 §25；第 2 条汇入 V 反身度量；第 3 条汇入 §27 账单。**§24 把「视觉听指令」这件事工程化了，但同时把「视觉推理就是 LLM 文本推理 + 视觉初始条件」这个方程式写定了**——这个方程式是§25 要挑战的目标，也是 V 反身度量要审视的前提。
