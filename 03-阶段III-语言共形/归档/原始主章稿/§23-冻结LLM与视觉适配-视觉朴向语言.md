# §23

标题: 冻结 LLM + 视觉适配
类型: 主章
要点: 放弃从头训 VL 骨干，把 LLM 冻住、用小适配器把视觉接进去；共形重心第一次外移——视觉从「与语言对偶」转为「为语言服务」

# 阶段 III · 冻结 LLM + 视觉适配：视觉朴向语言（Frozen / Flamingo / BLIP-2 / LLaVA / MiniGPT-4）

作者 / 机构: Tsimpoukelli 等 (DeepMind) / Alayrac 等 (DeepMind) / Li 等 (Salesforce) / Liu 等 (Wisconsin–Madison + Microsoft) / Zhu 等 (KAUST)
共形维度: 载体, 度量, 材料
关键贡献: 放弃从头训 VL 骨干的路子，改为**冻住已有的大语言模型**、**只训一个小适配器**把视觉信息翻译为 LLM 可读的软 token。适配器形状从前缀式（Frozen）→ 层内注入 gated cross-attention（Flamingo）→ Q-Former（BLIP-2）→ 线性投影（LLaVA 简化版）。共形重心第一次外移：视觉从「与语言对偶」转为「为语言服务」。
年份: 2021–2023
序号: 23
残差 / 它催生了什么: 视觉信息仍然被压过一个窄接口（Q-Former 32 token / Perceiver 64 query），像素级精度被刨掉 → 催生 §25 原生多模态（图文 token 平权馈入同一 Transformer）；指令遵循能力在这里仅有雏形 → 催生 §24 视觉指令微调；LLM 的「词典」仍纯文本，视觉自身不能被 LLM 生成 → 汇入 §27 账单。
类型: 架构 / 适配训练
阶段: III · 语言共形

🎯
**主题**：§22 的结构极限暴露了一件事——**从头训 VL 骨干永远追不上 LLM 的缩放红利**。§23 回答的是：既然 LLM 已经存在、已经很强、还很贵，能不能不重训它，只训一个「让 LLM 听懂视觉」的接口？五篇一起从观念到架构到极简回答这一问。关键的条线是**适配器的形状**（前缀 → 层内注入 → Q-Former → 线性投影）和**冻结的淡化**（从纯冻 → 层内打间隔插 → 微调阶段解冻）。

## 1 · Frozen —— *Multimodal Few-Shot Learning with Frozen Language Models* (Tsimpoukelli 等, DeepMind, NeurIPS 2021)

**共形贡献**：第一次把「冻住大语言模型」当做设计原则。做法：训练一个视觉 encoder 把图像映射为一串与 word embedding **同维**的软 token（比如 2 个），把它们插在文本 token 前面作为**视觉前缀**。关键洞见：LLM 的输入口（embedding 层）是一个**可以被任意软 token 注入的接口**——你给它什么向量，它就当「有这个词」来继续生成。Frozen 的 LM 只有 7B，能力有限，但**已经展示出从 multi-image 交错上下文里做 few-shot 迁移的雏形**——这是 Flamingo 的观念起点。

🔗 [https://arxiv.org/abs/2106.13884](https://arxiv.org/abs/2106.13884)

## 2 · Flamingo —— *Flamingo: a Visual Language Model for Few-Shot Learning* (Alayrac 等, DeepMind, NeurIPS 2022)

**共形贡献**：把 Frozen 的雏形推到工程规模。三件关键东西：**Perceiver Resampler** 用少量 learnable query 把任意数量的视觉 token 压成固定的 64 个（解决「图像 token 多出文本 token 一两个数量级」的计算爆炸）；**Gated Cross-Attention** 插在冻结 LM 每隔几层，tanh 门控从 0 初始化、训练时慢慢打开（保证 LM 在训练初期行为不被破坏）；**交错图文文档预训练（M3W 2.4B）**，直接从网页原生格式学习。结果：VLM 第一次拥有真正的 **in-context few-shot learning**（给几个 image-text 示例后对新图做对应任务）。机制意义：**注入点从输入口下沉到层内**。

🔗 [https://arxiv.org/abs/2204.14198](https://arxiv.org/abs/2204.14198)

## 3 · BLIP-2 —— *BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models* (Li 等, Salesforce, ICML 2023)

**共形贡献**：提出 **Q-Former**（Querying Transformer），并用**两阶段训练**把模板定型。Q-Former 内部有一组 learnable query tokens（典型 32），它们一路通过 cross-attention 从冻结的视觉 encoder 抽特征、另一路通过 self-attention 与文本 token 交互。**阶段 1**：只训 Q-Former，用 ITC + ITM + LM 三损失（仿 BLIP）把视觉-语言表示先独立学好；**阶段 2**：把 Q-Former 输出经线性投影输给冻结的 LLM，只训 Q-Former + 投影层。两阶段的精妙在于拆掉了纠缠的两个目标：**先学读图，再学翻译**。这套架构成为 §23 之后最广泛被继承的模板。

🔗 [https://arxiv.org/abs/2301.12597](https://arxiv.org/abs/2301.12597)

## 4 · LLaVA —— *Visual Instruction Tuning* (Liu 等, Wisconsin–Madison + Microsoft, NeurIPS 2023)

**共形贡献**：把适配器简化到极限： CLIP ViT → **一个线性投影层** → LLaMA。没有 Perceiver、没有 Q-Former、没有 cross-attention——就是一次矩阵乘法。第二贡献（也是它更大的贡献）：**用 GPT-4（纯文本）从 COCO 的 caption+bbox 标注合成视觉指令数据**（对话 / 详细描述 / 复杂推理 三类）。训练：阶段 1 pretrain 投影层（冻结 ViT 和 LLaMA），阶段 2 **解冻 LLaMA** 一起调投影层 + LLaMA。LLaVA 证明：**极简线性投影 + 好的指令数据**就能让 LLM 成为 VLM——复杂性从架构转移到数据。但也在此处开始滑向 §24：它的微调阶段已经「解冻」了 LLM。

🔗 [https://arxiv.org/abs/2304.08485](https://arxiv.org/abs/2304.08485)

## 5 · MiniGPT-4 —— *MiniGPT-4: Enhancing Vision-Language Understanding with Advanced Large Language Models* (Zhu 等, KAUST, 2023)

**共形贡献**：架构上也极简，但证明了**模块跨工作的可复用性**：EVA-CLIP ViT → **BLIP-2 的 Q-Former（直接复用）** → 一个线性投影 → Vicuna。只训最后的线性投影；**4 张 A100 训 10 小时**就能跑出功能性能。意义： Q-Former 成为可移植的「视觉接口标准件」，LLM backbone 也成为可替换的「语言骨干」——§23 的架构模板真正被**工程标准化**。

🔗 [https://arxiv.org/abs/2304.10592](https://arxiv.org/abs/2304.10592)

---

# 关于 §23 五篇的机制追问

## 一、「冻结 LLM」是一次哲学翻转，而不是技术优化

### §22 与 §23 的继承关系

- §22 的立场：我们自己训一个 VL 骨干（或两个塔、或一个流、或多路 experts），视觉和语言**并肩**。
- §23 的立场：放弃从头训 VL 骨干。LLM 太大、太贵、太好用——把它冻住，只训一个「让它听懂视觉」的接口。

这两个立场的差别不是工程上的（「资源不够」），是**共形结构上的**：

- §22：视觉模态和语言模态 **对等**进入骨干，两者在骨干内部协同演化。
- §23：语言骨干 **先存在**，视觉 **后适配**。视觉不再是与语言对等的一条主轴，而是「被翻译成语言听得懂的形式」的输入。

这是**共形重心的第一次外移**。阶段 III 的主题一直是「语言共形」，但在 §21 和 §22 里，「共形」还是双向的，只是在损失侧或架构侧让它们逆花。到 §23，**「共形」正式变成单向的：视觉 → 语言**。语言不再去适配视觉，视觉来适配语言。

### 这次翻转的代价与收益

- 收益：得到 LLM 所有能力的“赠品”——推理、常识、指令遵循、in-context learning。可训练参数从 100B+ 降到 1B 以下，辫本从 B 级降到 M 级。
- 代价：视觉的所有信息都必须在**LLM 预训练的 token 空间**里被表达。这个空间不是为视觉设计的，所以总有亜视觉信息放不进去（像素级精度 / 非常规空间关系）——这条就是 §23 的根残差，会汇入 §25 和 §27 账单。

后面的章节要按这个单向判断重读：§25 的原生多模态是对这种单向性的回播（让视觉和语言重新平权）；§26 的「视觉作为语言原语」是这个单向性的极端化（就当视觉是语言）；V 阶段的反身度量会质疑这个单向选择本身。

---

## 二、适配器的形状：注入点从输入口到层内再到极简线性

### 四种典型写法的对照

| 模型 | 适配器形状 | 注入点 | 视觉 token 数 | 可训参数量 |
| --- | --- | --- | --- | --- |
| Frozen | 视觉 encoder 直接输出软 token | 文本 token 前缀（输入口） | 极少（2 个） | 视觉 encoder 全部 |
| Flamingo | Perceiver Resampler + gated cross-attention | LM 每隔几层插入（层内） | 固定 64 | Perceiver + cross-attention（占 LM 总参 ∼10%） |
| BLIP-2 | Q-Former（learnable query + 两路 attention） | 文本 token 前缀（输入口） | 固定 32 | Q-Former（∼188M） |
| LLaVA | 单层线性投影 | 文本 token 前缀（输入口） | ViT patch 数（∼256） | 线性层（∼MB 级） + 微调时解冻 LLaMA |
| MiniGPT-4 | 复用 BLIP-2 的 Q-Former + 线性投影 | 文本 token 前缀（输入口） | 固定 32 | 只训最后的线性投影 |

### 三种注入点 vs 两种压缩者

这五篇的设计空间可以分成两个独立轴：

**注入点**（视觉软 token 在哪里进入 LLM）：

- 输入口前缀：Frozen / BLIP-2 / LLaVA / MiniGPT-4
- 层内插入：Flamingo
- （后续 §25 的原生多模态将彻底模糊「注入」概念——因为没有「主」和「客」之分）

**压缩者**（怎么把不定长视觉特征变成固定长的 token）：

- Learnable query + cross-attention：Flamingo（Perceiver）/ BLIP-2（Q-Former）——原理相同：让一小组 learnable query 去问视觉特征
- 直连：Frozen / LLaVA ——不压缩，有多少 patch 用多少

### 为什么 BLIP-2 为代表的 Q-Former 路线胜出而不是 Flamingo 的层内注入

- Flamingo 的层内注入要改 LLM 的结构（插入新层），这意味着每换一个 LLM backbone 都得重新设计插入布局；它与 LLM 强耦合。
- BLIP-2 的前缀式只需要 LLM 的输入口——这个接口所有 LLM 都一样，换 backbone 不用改架构。
- MiniGPT-4 直接把 BLIP-2 的 Q-Former 挂到 Vicuna 上就能跑，是这种解耦合性的直接证据。

所以 Q-Former + 前缀注入成为「工业标准件」——不是因为它精度最高，而是因为它**模块最干净**。

---

## 三、BLIP-2 的两阶段训练：为什么必须把「读图」和「翻译」分开学

### 一阶段训的随准其实都失败过

如果有一个小模块直接接在冻结的视觉 encoder 和冻结的 LLM 之间，只用最终目标（比如 captioning / VQA）直接训，状况是：小模块要同时学两件事——

1. 从视觉 encoder 里**读出**有用的视觉特征（哪些表征有语义价值？哪些是噪声？）；
2. 把读出的视觉特征**翻译**成 LLM 听得懂的软 token（这个软 token 空间应该指向 LLM 的哪片？）。

这两个目标互相干扰：如果你读到了有用的视觉信息但翻译途径不对，LLM 给的梯度就会把你拹回去令你重新读图（换一种读法确保能塑出好翻译）——于是两者都训不好。

### BLIP-2 的解法：按层次解耦

BLIP-2 的精妙在于把两个目标**在时间上隔开**：

- 阶段 1（只视觉-语言，不接 LLM）：用 ITC + ITM + LM 三损失（仿 BLIP §22 范式）训 Q-Former。目标：让 learnable query **学会从图像里提取语义**。此时没有 LLM 纠缠，专心读图。
- 阶段 2（接 LLM，闭着 阶段 1 已学到的读图能力）：把 Q-Former 输出经线性投影喂给 LLM，用图文生成目标训练。目标：让 Q-Former 的输出**落入 LLM 的词典空间**。阶段 1 已经凝固的读图能力至此只需做微调。

这套逐层解耦后面被大量因袭：InstructBLIP、mPLUG-Owl、Otter等在 §24 也基本走「先读图、再指令微调」的两阶段分解。

### 与「对齐在前融合在后」（ALBEF）的平行

§22 的「对齐在前融合在后」是在 **损失侧** 做解耦（先有 ITC 的对齐，后有 ITM/MLM 的细粒度融合）；§23 的 BLIP-2 两阶段是在 **训练流程侧** 做解耦（先训视觉-语言表示，后接 LLM）。两者都在处理同一个结构问题——**不要让多个异质目标同时争夺模块容量**——但分层次在不同维度。

---

## 四、Flamingo 的 Gated Cross-Attention：为什么「零门控初始化」是关键设计

### 问题：怎么在一个已经训好的 LLM 里面新插层而不破坏它

Flamingo 要做的事是在冻结的 Chinchilla 每隔几层插入 cross-attention。即使新插的 cross-attention 参数一开始是随机的、没有语义，它的**输出也会被添加进 LM 的残差流**。如果无护地加，LM 的每层输入分布立刻被干扰，它几十层下来稯积的语言能力被打碎。

### 解法：tanh gate 从 0 开始

每个新插的 cross-attention 模块的输出乘以 tanh(α)，其中 α 是一个可学 scalar，初始化为 0。

- 训练之初：tanh(0) = 0，新层的输出完全不进残差流。LM 行为 = 原 LM 行为，无干扰。
- 训练中：梯度告诉 α 「打开这一层会让 loss 变小」时，α 逐步离开 0，新层开始发挥作用。
- **每一层打开的节奏都由梯度自己决定**，不是被外面强迫。

### 为什么这件事值得单独救出来讲

从共形视角看：LLM 是一个**高度受训的动力系统**——它的每一层都被调到精确的结构平衡。强行加新输入等于扰动这个平衡。零门控初始化的本质是：**让新信息的注入强度成为可微的、可梯度优化的变量**，而不是一个硬碰硬的静态参数。注入进不进、什么时候进、进多少，都由训练自己回答。这是阶段 III 的一条微小但深刻的工程哲学，后面 LoRA / adapter / QLoRA 都能看到这种「扩展不破原动态」的思路。

---

## 五、「冻结」到底冻了什么：§23 和 §24 的边界是滑动的

### 各家的冻结程度不一样

| 方法 | 视觉 encoder | LLM | 新增模块 |
| --- | --- | --- | --- |
| Frozen | 训 | 冻 | 视觉 encoder 就是适配器 |
| Flamingo | 冻 | 冻（但层内插入了可训 cross-attention） | Perceiver + gated cross-attention |
| BLIP-2 | 冻 | 冻 | Q-Former + 线性投影 |
| LLaVA 阶段 1 | 冻 | 冻 | 线性投影 |
| LLaVA 阶段 2（微调） | 冻 | **解冻** | 线性投影 + LLaMA |
| MiniGPT-4 | 冻 | 冻 | 只训最后的线性投影 |

### 关键观察：LLaVA 的微调阶段其实解冻了 LLaMA

这一点是 §23 和 §24 边界的关键：

- 严格的 §23（Frozen / Flamingo / BLIP-2 / MiniGPT-4）：**LLM 从头到尾一直冻**。有能力来自“给 LLM 提供好的软 token”。
- LLaVA 微调：**为了取得更强的指令遵循，仅仅给 LLM 好软 token 不够，还得让 LLM 自己学怎么用这些软 token**——这就需要解冻 LLM。

这里的条线实际上是连续滑动的：构造 §23 = 「冻 LLM + 训适配器」；释放的而 §24 = 「解冻 LLM + 用指令数据全模微调」。LLaVA 的两阶段正好横跨了这个边界。

### 为什么 §23 不抛开「冻」的默认假设

即便 §24 的方法解冻 LLM，§23 的**结构设计矩阵**仍然被继承：

- 还是先用大量图文对做**预训练阶段**（冻 LLM）让适配器与 LLM 对齐。
- 再用指令数据做 **微调阶段**（解冻 LLM）让 LLM 学会使用。

也就是说，§23 不是被 §24 打碎的，而是**成为 §24 的必需前置**。任何传眼 §24 方法的第一步都是「做好预训练阶段」，而「预训练阶段」就是 §23 的门府。

---

## 小结：§23 的谱系内逻辑

- **Frozen**：将「冻住 LLM」当做设计原则。定义「前缀式适配」最简版本。
- **Flamingo**：注入点下沉到层内，零门控初始化 + Perceiver 压缩 + 交错图文预训练，第一次实现真正的 in-context few-shot。
- **BLIP-2**：Q-Former 两阶段训练，把「读图」与「翻译」按时序解耦，架构模板正式定型。
- **LLaVA**：架构简化到一个线性投影；复杂性转移到**用 GPT-4 合成指令数据**。开始滑向 §24。
- **MiniGPT-4**：直接复用 BLIP-2 的 Q-Former + 换 LLM backbone，证明适配器与 backbone 成为可互换的工业标准件。

五篇合起来完成一件事：**把“LLM 挂视觉”这个想法从雏形（Frozen）推到工程规模（Flamingo）推到模板定型（BLIP-2）推到极简平民化（LLaVA / MiniGPT-4）**。整个路子的底层就是一件事：在 LLM 这条主线上挂一个视觉接口，让 LLM 能看图说话。

---

## 本组合力的残差

「视觉朴向语言」做成了，但暴露三条新残差：

1. **视觉信息被窄接口刨掉像素级精度**——Q-Former 的 32 token、Perceiver 的 64 query、乃至 LLaVA 不压缩的 ∼256 patch，都是把一张图的所有细节卸到一个固定的、较窄的软 token 轴上。对需要像素级精度的任务（OCR、小物体检测、表格精确读取、教科书数学符号），**接口宽度就是精度天花板**。这条残差定义 §25 入口：放弃「挂接口」的观念，让图文 token **平权**馈入同一 Transformer（Chameleon / Kosmos / Fuyu / GPT-4o 一系）。
2. **指令遵循能力在这里仅有雏形**——Frozen / Flamingo / BLIP-2 能看图说话，但「听从任意指令」还没有被系统训。LLaVA / MiniGPT-4 开了头，但真正系统化的视觉指令数据合成、多轮对话、grounded instruction、指令混合比例、评估基准，都需要一整章来处理。这条残差定义 §24 入口：视觉指令微调（InstructBLIP / mPLUG-Owl / Otter / LLaVA-1.5 向 §24 深化）。
3. **LLM 的「词典」仍然是纯文本的**——视觉被适配进来作为输入，但视觉自身**不能被 LLM 生成**。LLM 的 output head 永远在纯文本词表上 softmax。这条残差在 §23 里解不了——因为就是定义性的：只要你「冻住纯文本 LLM + 只接视觉输入」，就不能出图像。这条残差最终**汇入 §27 账单**，在阶段 IV / V 的分流里被处理：IV 会说「把视觉 token 加入 LLM 的输出空间，让它能生成像素」（Chameleon / GPT-4o）；V 会问「为什么一定要把视觉被翻译为语言 token 才算比对、有没有其他的对比方式」。

第 1 条定义 §25 入口；第 2 条定义 §24 入口；第 3 条汇入 §27 账单。**§23 把「视觉挂接 LLM」这件事做实了，但同时把「视觉必须变成 LLM 听得懂的东西」这个假设入箱到阶段 III 的底层——这个假设在 §25、§26、V 会被逐步松动或反省。**