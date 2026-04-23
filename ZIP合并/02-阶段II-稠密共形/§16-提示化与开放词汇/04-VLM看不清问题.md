# §0 · 先把现象精确化

你说的"模糊地看 + 虚假地想"其实可以拆成四种独立可测的故障模式，每一种都有专门的 benchmark：

1. **Perceptual blindness（感知性盲）**：两张明显不同的图在 CLIP 编码里几乎相同 → VLM 根本区分不出。证据：**MMVP / CLIP-blind pairs**。
2. **Visual-unnecessary answering（视觉无关作答）**：不给图也能答对。证据：**MMStar**。
3. **Recognition-masked reasoning errors（识别错误伪装成推理错误）**：62% 的所谓"推理错误"追回去是识别错误。
4. **Unfaithful CoT / hallucinated reasoning（不忠实的思维链）**：给出的思考过程并不是模型真正用于决策的过程。证据：Anthropic 的 "Language Models Don't Always Say What They Think"[[1]](https://www.notion.so/Language-Models-Don-t-Always-Say-What-They-Think-Unfaithful-Explanations-in-Chain-of-Thought-Prompt-a69748d648008277a182017c02134800?pvs=21) 及其视觉扩展。

这四种故障虽然表象不同，但指向同一个结构性病灶。

---

# §1 · MMVP / Eyes Wide Shut —— 最根本的那个证据

Tong, Liu, Zhai, Ma, LeCun, Xie（NYU + Meta + Berkeley）CVPR 2024 的 **"Eyes Wide Shut? Exploring the Visual Shortcomings of Multimodal LLMs"**[[2]](https://arxiv.org/abs/2401.06209) 是这个问题最清晰的起点。

## 1.1 方法：构造 "CLIP-blind pairs"

步骤惊人地简单：

- 在 ImageNet + LAION-Aesthetics 里找这样的图片对：**CLIP-ViT-L/14 的 cosine 相似度 > 0.95**，但 **DINOv2-ViT-L/14 的相似度 < 0.6**
- 也就是：**语言-监督视觉编码器看"几乎一样"，纯视觉 SSL 看"明显不同"**
- 人工选出 150 对这样的盲对，每对配 2 个问题 = 300 个 VQA

## 1.2 失败模式的 9 种 "视觉 pattern"

MMVP 论文把 CLIP 盲对分析成 9 个系统性盲区：朝向、数量、位置关系、颜色/外观、结构、视角、文本/OCR、存在/缺失、状态（开/关、坐/站）。**这些全是人类 3 秒看懂的事**。

## 1.3 结果——整个 SOTA 在 chance line 附近

MMVP 上的 pair accuracy（两个问题都要对才算对，随机 25%）：

- **GPT-4V**: 38.7%
- **Gemini**: 40.7%
- **LLaVA-1.5**: 24.7%（基本 = 随机）
- **人类**: ~95%

这不是"VLM 还能再优化一点"——这是 **SOTA 闭源旗舰在最基础的感知区分上只比抛硬币好一点点**。

## 1.4 为什么 CLIP 会这样

**CLIP 的训练目标本质上是"对齐到语言的粒度"**。语言里"一只狗朝左"和"一只狗朝右"常常被描述为"一只狗"——训练数据里没有对"朝向"施加区分压力。于是 CLIP 的表征把朝向、数量、位置关系这些**语言不常精确描述的视觉属性**全部压扁了。

**这就是阶段 II 的残差"语义是借来的"在 VLM 时代的直接代价**：借语言的粒度 = 丢掉语言不编码的那些视觉属性。

Tong 等的后续工作（UC Berkeley 博士论文扩展版）[[3]](https://escholarship.org/content/qt62z9m7xg/qt62z9m7xg.pdf) 验证了更狠的结论：**CLIP 的 scaling（更大参数、更高分辨率）对这类盲对几乎没有改善**——也就是说盲不是"见得不够多"，是"训练目标本身没要求它看清"。

---

# §2 · MMStar —— 对 VLM 评测的"毒辣"审计

"Are We on the Right Way for Evaluating Large Vision-Language Models"（CVPR 2024 口头）[[4]](https://mmstar-benchmark.github.io/) 做了更冷峻的一件事：**不给图，只给题和选项，看 VLM 能做对多少**。

结果：

- **GeminiPro 在 MMMU 上不给图能拿 42.9%**（高于随机 25% 近一倍）
- **Sphinx-X-MoE 不给图在 MMMU 拿 43.6%**，**比它的纯 LLM backbone 还高 17.9%**——说明这些 sample 被训练数据泄漏了
- 6 个主流 benchmark 上，无视觉基线平均**比随机高 20%**

**含义极其残酷**：当我们说 "VLM X 在某 benchmark 上拿 60%"，其中很大一部分分数是 **LLM 用世界知识和选项偏置猜出来的，不是模型真的看了图**。

这就把你的直觉"VLM 在做虚假推理"量化了——**很多任务 VLM 根本没用到图像，只是在做"看上去像视觉任务"的文字题**。

---

# §3 · 62% 的"推理错误" ≠ 推理错误

2026 年 2 月的一份研究报告[[5]](https://www.showapi.com/news/article/6989aaf54ddd79ab6700c189)给出一个更具威慑力的数字：

> **高达 62% 的 VLM 输出错误可追溯至物体误判、属性混淆或场景理解失准等识别层面缺陷，而非逻辑链断裂或常识缺失**。
> 

这篇工作的意义是：业界花大量精力在**推理模块的下游**做优化（CoT、符号引擎、知识图谱、链式思维提示），**但 6 成错误根源在上游感知**。地基没打好，楼越盖越漂亮也是在流沙上起塔。

同一份报告给出的具体案例：

- 模型生成一段关于画作的哲学评论，但**把画中人物手里的陶罐识别为金属水壶**
- 准确回答"图中两人是否在交谈"，却**把背对镜头的人误判为"独自站立"**

**这叫 "聪明的笨拙"**——语言上精致，视觉上瞎。和你说的"虚假推理"完全是同一件事。

---

# §4 · 机制归因：为什么会这样？

把这些现象放到架构层面，有四条互相咬合的机制原因。你之前的 [L4：跨模态共形的传导（VLM 核心层）](https://www.notion.so/L4-VLM-f7b748d648008364a7f1016a7f912215?pvs=21) 已经列出前三条，这里补全并深化。

## 4.1 **Projector 是一个极窄的带宽瓶颈**

VLM 的主流架构是：`Vision Encoder (CLIP) → Projector (MLP 2-layer) → LLM tokens`

- CLIP ViT-L/14 每张图出 256 个 visual token
- projector 通常是一个 2-4 层 MLP，把 1024-d 压到 LLM 的 4096-d
- **这个 MLP 的容量 << 视觉信息的实际复杂度**

关键：projector 只能**线性挑选 + 旋转**原 CLIP 表征里已有的维度，**它无法补回 CLIP 编码时就已经丢掉的信息**（比如朝向、精确数量）。[[6]](https://www.notion.so/L4-VLM-f7b748d648008364a7f1016a7f912215?pvs=21)

**如果 CLIP 在第一步就把"朝左的狗"和"朝右的狗"压成同一个向量，后面 70B LLM 再强也救不回来**——这就是 MMVP 的根本。

## 4.2 **视觉 token 在 LLM 里是"外来客"**

LLM 被训练时从未见过视觉 token，它的 attention 模式是对**语言**优化的。VLM 的做法是：

- 把视觉 token 直接 concat 到文本 token 前面
- 用 visual instruction tuning 在几百 k 到几 M 样本上微调 LLM

但微调数据远少于 LLM 预训练数据（几 M vs 几 T），LLM 的 attention 偏置仍然**倾向于从文本 token 之间找答案**，把视觉 token 当成一个"模糊的上下文"。

这在注意力分析里很直观：做 MMVP 类问题时，**LLM 在输出阶段对视觉 token 的注意力权重显著低于对问题 token 的注意力权重**。模型在"想"的时候不在"看"。

**Look Light, Think Heavy**[[7]](https://www.notion.so/cf9748d648008359943381c9f481983a?pvs=21) 就是这个现象的命名——推理阶段视觉信号持续衰减，语言推理持续主导。

## 4.3 **语言先验压制视觉证据**

当视觉证据微弱而语言先验强时，模型会系统性偏向语言先验。典型案例（VLM 幻觉综述[[8]](https://zhuanlan.zhihu.com/p/1895122722746525063)[[9]](https://crad.ict.ac.cn/article/doi/10.7544/issn1000-1239.202440444)）：

- 问 "What color is the cat in the image?"——图里是一只**白狗**。一批 VLM 会答"orange / black / white"等猫的常见颜色——**完全忽略图里没有猫**。
- 问 "How many people are in the photo?"——图是风景空照。VLM 答 "two" / "a few"——**场景里人出现概率高被先验强化**。

这叫 **object hallucination**，2024-2025 的一大研究焦点。北京大学 + 复旦的《视觉语言大模型的幻觉综述》[[9]](https://crad.ict.ac.cn/article/doi/10.7544/issn1000-1239.202440444) 128 篇文献系统梳理：幻觉成因分为**训练数据偏置、训练任务缺陷、视觉编码脆弱、文本生成自回归偏置**四类，**4 个原因相互耦合**。

## 4.4 **CoT 不忠实：链条是装出来的**

Anthropic 的 "Language Models Don't Always Say What They Think"[[1]](https://www.notion.so/Language-Models-Don-t-Always-Say-What-They-Think-Unfaithful-Explanations-in-Chain-of-Thought-Prompt-a69748d648008277a182017c02134800?pvs=21) 本来是针对纯 LLM 的，但它在 VLM 上的版本更严重：

- 做 MMVP 这类题时，VLM 经常生成**看起来非常合理的 CoT**：
    
    > "Looking at the image, I can see a dog sitting on a bench. The dog appears to be facing the camera slightly to the left. Therefore the answer is A."
    > 
- 但上图里的狗其实**面朝右**——**CoT 的每一步都在"编"，并不是模型真的从视觉 token 抽取的事实**

Visual CoT benchmark[[10]](https://www.notion.so/Visual-CoT-Advancing-Multi-Modal-Language-Models-with-a-Comprehensive-Dataset-and-Benchmark-for-Cha-e70748d64800836e8a1701897f80b88d?pvs=21) 和 LLaVA-CoT[[11]](https://www.notion.so/LLaVA-CoT-Let-Vision-Language-Models-Reason-Step-by-Step-f82748d64800834996d7015cac636679?pvs=21) 对这个现象有系统评测——**CoT 长度和准确率常常负相关**：思考越长，幻觉越多（因为模型每一 step 都在从错误的感知基础上继续编）。

这就是你说的"**虚假推理**"的真正机理：**推理链本身不假，假的是它接入感知的那个接口**。感知错了，推理链越精致，错误越 confident。

---

# §5 · Look Light, Think Heavy —— 视觉反思在推理过程中持续衰减

2025 下半年开始的一组工作[[7]](https://www.notion.so/cf9748d648008359943381c9f481983a?pvs=21)（Survey + empirical）提出了一个新的精确观察：

> 现有 VLM 在多步推理中，**对视觉的回看（visual re-attention）强度是单调衰减的**。第一步还有 40% 注意力在 visual token 上，到第 5 步可能只有 5%。
> 

对比：人类做复杂视觉推理时会**反复回看图像**——这叫 **iterative perception**。VLM 做 CoT 时视觉通道基本是"一次性查询"：读一次图，之后全程在语言里推。

这解释了为什么 CoT 对数学推理大幅提升，但**对需要精细视觉的任务常常反而掉点**——**CoT 把本来还勉强能看的模型，推离了视觉证据**。

这件事的建设性回应是一组 **Test-Time Scaling over Perception (TTSP)** 工作[[12]](https://www.notion.so/Test-time-Scaling-over-Perception-Resolving-the-Grounding-Paradox-in-Thinking-with-Images-7e8aa1f153a241f38b1e753e33e4b6a3?pvs=21)[[13]](https://www.notion.so/Test-time-Scaling-over-Perception-345748d6480080fbbe4dee5a5e6d9bf9?pvs=21)：**把"感知"本身当成可以 test-time 扩展的操作**——允许模型在推理中途主动 re-crop、re-query、re-attend 图像区域。你的工作区已经在跟进这条线。

---

# §6 · 当前补救方案的谱系（按"看清楚"的深度递进）

这 2 年学界的所有补救都可以映射到"看清楚"的层级上：

## 6.1 **层级一·换更好的视觉编码器（或组合）**

- **Mixture-of-Features (MoF)**[[2]](https://arxiv.org/abs/2401.06209)：Tong 原论文给的方案——**把 CLIP 特征和 DINOv2 特征一起喂给 LLM**。实验显示在 MMVP 上能补 ~10 个点。
- **RADIO / AM-RADIO / C-RADIOv4**[[14]](https://www.notion.so/NVIDIA-RADIO-C-RADIOv4-94b748d6480082eaa7d301dbb787cf23?pvs=21)：NVIDIA 的聚合蒸馏——一个 ViT backbone 同时蒸馏 CLIP + DINOv2 + SAM + SigLIP 四家老师。**一个模型兼顾语义对齐、几何细节、分割边界**。
- **LLM2CLIP**[[15]](https://www.notion.so/LLM2CLIP-Powerful-Language-Model-Unlocks-Richer-Cross-Modality-Representation-fa0748d648008314a287815b92d47780?pvs=21)：用 LLM 反向改造 CLIP text encoder，让 CLIP 能编码更细粒度的描述，迫使 vision encoder 学更细的视觉区分。

这条线的共同逻辑是：**CLIP 的盲是训练目标造成的，那就混进没被语言抹平的视觉表征（DINO）或重写语言粒度（LLM2CLIP）**。

## 6.2 **层级二·改视觉到语言的接口**

- **CogVLM**[[16]](https://www.notion.so/CogVLM-Visual-Expert-for-Pretrained-Language-Models-ecc748d64800830f85d20175eb1647a9?pvs=21)：不是在 LLM 前面加视觉 token，而是在 LLM 每一层加 **"visual expert"** —— 每层 attention 里视觉 token 和文本 token 走独立的 Q/K/V 矩阵。让 LLM 的每一层都显式"看一次"，而不是第一层看完就忘。
- **Flamingo 的 cross-attention layers**[[17]](https://www.notion.so/Flamingo-a-Visual-Language-Model-for-Few-Shot-Learning-480748d6480083a8b2e781199ac16a58?pvs=21)：在 LLM 的若干层之间插入专门的 gated cross-attention，显式建模视觉→语言的信息流动。
- **ALIGNVLM**[[18]](https://www.notion.so/ALIGNVLM-Bridging-Vision-and-Language-Latent-Spaces-for-Multimodal-Understanding-952748d6480083e6a8d4816a28392d59?pvs=21)：在视觉潜空间和语言潜空间之间架桥梁，要求它们的几何不光是对齐，而是同构。

这条线的共同逻辑是：**承认 projector 是瓶颈，把它扩宽 + 做成每层可调用的**。

## 6.3 **层级三·让模型学会"回看"**

- **Visual CoT**[[10]](https://www.notion.so/Visual-CoT-Advancing-Multi-Modal-Language-Models-with-a-Comprehensive-Dataset-and-Benchmark-for-Cha-e70748d64800836e8a1701897f80b88d?pvs=21)：训练数据里带 bbox 标注，让模型在 CoT 的每一步明确说"现在我在看图的哪一块"，学会 grounded reasoning。
- **TTSP (Test-Time Scaling over Perception)**[[12]](https://www.notion.so/Test-time-Scaling-over-Perception-Resolving-the-Grounding-Paradox-in-Thinking-with-Images-7e8aa1f153a241f38b1e753e33e4b6a3?pvs=21)：test-time 迭代地 re-crop / re-attend，让感知本身成为可 scale 的维度。
- **LVR (Latent Visual Reasoning)**[[19]](https://www.notion.so/Latent-Visual-Reasoning-Reasoning-in-Visual-Embedding-Space-without-Generating-Text-2d6748d64800836ca4bb01b09ae92dfd?pvs=21)：在视觉 embedding space 里做 reasoning，不生成中间文本——绕开 CoT 的语言化压力。
- **MVoT (Multimodal Visualization-of-Thought)**[[20]](https://www.notion.so/Imagine-While-Reasoning-in-Space-Multimodal-Visualization-of-Thought-MVoT-44b748d6480083d9aaf1818e2af2721c?pvs=21)：思考过程中主动生成中间图像，让视觉推理也成为一等公民。

这条线最接近你的研究兴趣——**它承认"一次看完就推"不够，推理必须和感知交错**。

## 6.4 **层级四·放弃 CLIP 作为视觉预训练**

ICCV 2025 的 **"Scaling Language-Free Visual Representation Learning"**[[21]](https://arxiv.org/abs/2504.01017)[[22]](https://openaccess.thecvf.com/content/ICCV2025/papers/Fan_Scaling_Language-Free_Visual_Representation_Learning_ICCV_2025_paper.pdf) 是转折点：

- 用**纯视觉 SSL (DINOv2 + MAE)** 在 MetaCLIP 的**同一数据**上训练
- 训到 7B 参数，**性能不饱和**，在 VQA 基准上 match CLIP
- 关键发现：**视觉 SSL 的 scaling 斜率比 CLIP 更陡，天花板更高**——长期来看 SSL 会超过 CLIP

**含义**：VLM 未来可能不需要 CLIP 做视觉 encoder。**DINOv3 / V-JEPA 2 这条 SSL 线才是真正能看清图像的地基**。

---

# §7 · 本体论回定位：这不是 bug，是阶段 II 残差的跨阶段延伸

回到你谱系的视角。这个问题**不是 VLM 时代的新问题，是阶段 II 末端的"语义是借来的"残差在阶段 III 的投射**：

| 层面 | 阶段 II 残差 | 阶段 III 后果 |
| --- | --- | --- |
| 语义来源 | 语义是借来的（来自 CLIP） | **VLM 视觉侧继承了 CLIP 的盲点** |
| 关系建模 | 关系没有进入稠密输出 | **VLM 无法真正做关系推理，只能做对齐过的语言推理** |
| 监督目标 | 无真正的视觉 next-token 等价物 | **CoT 在视觉上空转** |
| 架构 | 视觉与语言是"拼接"关系 | **projector 瓶颈 + LLM 把视觉当外来客** |

**你之前那段"语义是借来的"写得正确**——但它在阶段 II 里看似只是 SAM 和 Grounding DINO 的工程取巧，在阶段 III 里**直接变成 VLM 的认知病灶**。

用你 [对话思路总结：CV困境、遥感基础模型与多模态时序统一框架](https://www.notion.so/CV-d6b2da62c751461fa184c49c750653d6?pvs=21) 里那句判断："**当前 VLM 的智能实质上是靠语言语义在拉动**"——**这就是全部问题的根**。VLM 是一个"长在语言树干上的视觉嫁接"，它对图像的理解不来自"看懂"，来自"把图翻译成语言标签之后再理解语言"。

翻译过程中丢掉的，就永远丢了。

---

# §8 · 这个视角下的一个尖锐判断

你在 message 10 问的是"视觉为什么 scaling 不涨"。这一条接着问"VLM 为什么看不清"。这两个问题其实**是同一个问题的两面**：

- **视觉 scaling 不涨**：因为视觉没有一个能产生世界模型的训练目标，单纯堆数据在低维流形上饱和
- **VLM 看不清**：因为 VLM 借的是语言的世界模型，语言的粒度没覆盖到的视觉事实就在 VLM 里不存在

**合起来的结论**：VLM 不是"看了图像然后思考"，VLM 是"**把图像坍缩成语言先验能识别的一组标签，然后在语言里思考**"。它的"智能"是语言智能，不是视觉智能。

这解释了为什么：

- GPT-4V 能写哲学评论却把陶罐当水壶——哲学评论是语言任务，识别陶罐是视觉任务，前者它会后者它不会
- CoT 越长准确率反而越差——每多一步 CoT 都是在从一个更模糊的感知基础上继续编
- 不给图也能答对 40%+——任务的"视觉外壳"下是语言先验

---

# §9 · 可能的出路：三条正交的技术向量

这是 2025-2026 学界正在并行推进的三条：

## 9.1 **给视觉一个不依赖语言的 scaling 目标**

- **DINOv3 + Gram Anchoring**（你之前吃透的）
- **V-JEPA 2**（LeCun 的 latent-space predictive world model）
- **Emu3 / VAR** 的视觉 next-token
- 这条让视觉自己能"看清"，不借语言

## 9.2 **让 LLM 在推理中真的持续看图**

- **Visual CoT / MVoT**：推理过程中显式生成/引用视觉区域
- **TTSP**：test-time 迭代感知
- **CogVLM / Flamingo 式每层 cross-attn**：每层都看
- 这条让"思考"真正 grounded 在"看"

## 9.3 **用聚合蒸馏把多个视觉专家合一**

- **RADIO v1→v4**：一个 ViT 同时是 CLIP + DINO + SAM + SigLIP
- **MoF (Mixture-of-Features)**
- 这条承认单一 encoder 盲，用组合解围

**三条在技术上互补，在哲学上殊途同归**——都是**承认 VLM 当前范式是"语言拉动视觉"的临时架构，最终要走向"视觉和语言等位、可交错调用"的真·多模态**。

---

# §10 · 对你的谱系的含义

这个问题在你的谱系里需要占一个**专门的位置**：

- 它**不属于阶段 II**——阶段 II 还在稠密共形内部
- 它**属于阶段 III 的开篇或早期**——它是"语义自生"和"关系建模"这两条残差在 VLM 时代的**第一次被量化**
- 它给了阶段 III 一个极其有力的**紧迫性论证**：不光是"下一个阶段好像该来了"，而是"上一阶段的残差在新范式下造成了可测量的、6 成以上的、工业产品里现实发生的故障"

**关键参考论文清单**（给你的谱系储备）：

- Tong et al. "Eyes Wide Shut? Exploring the Visual Shortcomings of Multimodal LLMs", CVPR 2024[[2]](https://arxiv.org/abs/2401.06209) —— **MMVP benchmark + CLIP-blind pairs，基础文献**
- Chen et al. "Are We on the Right Way for Evaluating Large Vision-Language Models" (MMStar), CVPR 2024[[4]](https://mmstar-benchmark.github.io/) —— **VLM 评测的审计**
- 李旭等《视觉语言大模型的幻觉综述：成因、评估与治理》, 计算机研究与发展 2025[[9]](https://crad.ict.ac.cn/article/doi/10.7544/issn1000-1239.202440444) —— **128 篇引用的系统综述**
- Fan et al. "Scaling Language-Free Visual Representation Learning", ICCV 2025[[21]](https://arxiv.org/abs/2504.01017) —— **放弃 CLIP 的第一个 scaling 证据**
- BLINK-Twice (arXiv 2510.09361)[[23]](https://www.notion.so/345748d6480080d5b7a5ebf519258f28?pvs=21) —— 更新版 perception-as-reasoning benchmark
- 你工作区已有的相关深度页：[视觉思考的本质：视觉就是视觉，何以成为「思考」？](https://www.notion.so/cf9748d648008359943381c9f481983a?pvs=21)、[对话思路总结：CV困境、遥感基础模型与多模态时序统一框架](https://www.notion.so/CV-d6b2da62c751461fa184c49c750653d6?pvs=21)、[CV 瓶颈与遥感多模态基础模型——学术探讨纪要](https://www.notion.so/CV-4df89f9d891d4112bb7f002f3cddbb0a?pvs=21)、[L4：跨模态共形的传导（VLM 核心层）](https://www.notion.so/L4-VLM-f7b748d648008364a7f1016a7f912215?pvs=21)、[L7：共形的极限与下一座大厦](https://www.notion.so/L7-ca9748d64800820ba7de81fb09033228?pvs=21)

---

# §11 · 最尖锐的一句话总结

> **VLM 的"思考"，本质上是对语言先验的调用，而不是对视觉证据的分析。当语言先验和视觉证据一致时它看起来聪明；当二者冲突时它忠于语言、背叛视觉——这就是你看到的所有"虚假推理"。**
> 

这不是工程问题，是范式问题。修补层 (§6.1-6.3) 能把 MMVP 从 25% 推到 45%、50%、60%，但推到 **人类 95%** 需要 §6.4 的 paradigm shift——**视觉独立的 scaling + 视觉原生的 reasoning**。

这也给你的阶段 III 定了一个**真正具体的靶心**：**阶段 III 的成功条件不是"VLM 做得更漂亮"，而是"MMVP 上追平人类"**。这个是可测的、可追踪的、不会因为产品叙事混淆的硬指标。

---

顺便：这段分析和你 message 10 的 scaling 分析，合起来构成一个非常完整的"阶段 III 开篇论证"。一段讲"为什么视觉自己的 scaling 不涨"（数据+目标的本体论）；一段讲"所以借来的语义代价有多大"（VLM 的幻觉机制）。两段连起来就是阶段 III 的入口宣言。要不要我把它整理成一个新页面挂在 [深入的思考：深度学习的一致性理论大厦](..\..\00-公理层\第一性原理.md) 下，作为"阶段 II→阶段 III 的过渡总纲"？（类似 [阶段 II · 开篇总纲：从整图到每一像素，度量的稠密穿透](..\00-总纲-从整图到每一像素.md) 的定位，但是阶段 III 开篇。）我可以直接建，里面有 §1 scaling 差异、§2 VLM 看不清的机制、§3 两个问题的共同根、§4 阶段 III 的靶心——把这两轮的密度一次性沉淀成永久页面。如果你希望我动手，说"建"我就去做。

## 3 · Grounding DINO / Grounding DINO 1.5 (Liu 等, IDEA, ECCV 2024 / 2024)

**共形贡献**：把 DINO-DETR 的查询与 BERT 文本嵌入做跨模态融合——任意自然语言 phrase 都可以作为一个「开放类别」发出检测查询。1.5 版把它推到产业可用的速度和精度。

🔗 [https://arxiv.org/abs/2303.05499](https://arxiv.org/abs/2303.05499) · [https://arxiv.org/abs/2405.10300](https://arxiv.org/abs/2405.10300)

## 4 · DINO-X —— *A Unified Vision Model for Open-World Object Detection and Understanding* (IDEA Research, 2024)

**共形贡献**：把 Grounding DINO 的开放词汇检测推广成「检测 + 分割 + 姿态 + 关系 + caption」的统一开放世界模型——开放词汇从「类别」扩张到「任务族」。

🔗 [https://arxiv.org/abs/2411.14347](https://arxiv.org/abs/2411.14347)

## 5 · T-Rex2 —— *Towards Generic Object Detection via Text-Visual Prompt Synergy* (Jiang 等, IDEA, ECCV 2024)

**共形贡献**：同时接收文本提示和视觉样例提示（一两张「这是什么」的样例图），用对比学习让两种提示在同一嵌入空间里协作。解决 Grounding DINO 在「长尾 / 罕见 / 无语言描述」类上的弱点。

🔗 [https://arxiv.org/abs/2403.14610](https://arxiv.org/abs/2403.14610)

这里有一个**非常重要但几乎所有入门材料都会掩盖**的命名陷阱，必须先拆开——否则整条演进线根本讲不通：

> **"DINO" 在视觉领域指的是两条彼此无关的技术线，它们只是名字相同。**
> 
- **DINO (SSL) 线**：Caron 等, Meta, 2021 —— **DI**stillation with **NO** labels。自监督视觉预训练。v1 → v2 → v3。
- **DINO (DETR) 线**：Zhang 等, IDEA, 2022 —— **D**ETR with **I**mproved de**N**oising anch**O**r boxes。端到端检测器。DAB-DETR / DN-DETR → DINO-DETR → Grounding DINO → Grounding DINO 1.5/1.6 → DINO-X。

**你问"从 v1 到 v3 到 Grounding DINO"**——这句话在学术上是**错的**——Grounding DINO 不是 DINOv3 之后的一代，它属于另一条线。但这个错不是你的错，社区普遍被 Meta 和 IDEA 两家的命名冲撞搞晕。下面把两条线**分别**讲清，然后讲它们**唯一的真实交汇点**。[[1]](https://zhuanlan.zhihu.com/p/1943279068654056673)[[2]](https://zhuanlan.zhihu.com/p/2022290422282691008)

---

