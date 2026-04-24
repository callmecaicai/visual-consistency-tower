# §1 · SAM —— 分割任务本身被重新定义

作者：Kirillov, Mintun, Ravi, Mao, ... Girshick（Meta FAIR，2023）。

## 1.1 问题的重新提法 —— 不是更好的分割，而是新的分割

SAM 之前，分割任务的定义是：

> 给一张图，输出一组 pixel → class 的映射。
> 

这个定义里"做什么分割"**由训练集决定**——你在 COCO 训，它就分 80 类；在 ADE20K 训，就分 150 类。换一个领域就要重训。

SAM 把问题**重新定义**了：

> 给一张图 **+ 一个提示（prompt）**，输出和提示对应的 mask。
> 

这一改动的分量：**分割从"任务"变成了"可调用的原语"**。任务的规格不在模型内部，在运行时输入里——这和 OS 领域从"专用程序"到"shell + 命令"的转化同构。

## 1.2 SAM 的三件套

SAM 论文里叫这套组合 **"Promptable Segmentation Task + Model + Data"**——三个东西耦合才 work：

**(1) 任务（task）**

- 输入：image + prompt（SAM 原始主体能力主要是 point / box / mask；text prompt 不是 SAM 1 的核心提示能力，而是后续与 language grounding / open-vocabulary 模型结合后的外接方向）
- 输出：一张或几张 mask
- "Ambiguity-aware"：一次提示可能对应多个合理答案（比如点在衬衫上可以意指衬衫、人、或衣袋）——SAM 会输出 3 个候选 mask

**(2) 模型（SAM architecture）**

```
Image encoder (ViT-H, 636M)  ──── 大且慢（贵：1 次/图，但可缓存）
        ↓ image embedding
Prompt encoder (~几 MB)       ──── 小且快
        ↓ prompt embedding
Mask decoder (~几 M)          ──── 小且快（便宜：每个 prompt 1 次）
        ↓
    N masks + N IoU predictions
```

**这个非对称分工是 SAM 架构的核心设计**：

- Image encoder 贵 → 每张图跑一次，缓存后重复用
- Prompt encoder + Mask decoder 几乎免费（~50ms）→ 可以实时响应用户交互

这让 SAM 在**交互式**场景（用户反复点击）下是"一次贵操作 + 多次极廉操作"——工程上漂亮。

**(3) 数据（SA-1B）**

- 11M 图，1.1B masks
- **这是前所未有的规模**——前 SOTA 的 Open Images 只有 2.8M masks
- 标注方式：data engine 循环——SAM 训练 → 标注员用 SAM 辅助标 → 新数据训更好的 SAM → 再标更多
- 数据工程本身是 SAM 贡献的一半

**没有 SA-1B，SAM 训不出来；没有 SAM，SA-1B 标不出来**——典型的 bootstrap。

## 1.3 为什么"可提示分割"是本体论上的跃迁

SAM 的可提示性（promptability）看起来只是加了个 prompt 参数，但它对应一个更深的哲学转变：

**前 SAM**：模型的能力域 = 训练数据的类别域

**后 SAM**：模型的能力域 = "对任何对象都能响应提示"的泛化能力

这和 GPT 对 NLP 做的事**完全同构**：

- 前 GPT：每个 NLP 任务一个专用模型（翻译、摘要、分类）
- 后 GPT：一个模型 + prompt 涵盖全部任务

SAM 的贡献不是做了"最好的分割模型"——它做的是**视觉领域的第一个 foundation model for spatial understanding**。这种"基础模型"的定义里，**promptability 是本质特征**。

## 1.4 SAM 的 mask decoder —— 轻量版 MaskFormer

SAM 的 mask decoder 结构和 MaskFormer 惊人地相似但更简化：

- 若干个 **output tokens**（可学习 token，每个对应一个候选 mask）
- 拼上 prompt tokens
- 对 image embedding 做两层 cross-attention（bidirectional）
- 最后用 output token 和 upsampled image embedding 做**点积**生成 mask

**这就是 MaskFormer 的 query-based 结构**——只是 query 数量很少（3 个候选）且由 prompt 条件化。你之前吃透的"mask embedding · pixel embedding 点积"机制在 SAM 里原封不动沿用。

所以 SAM 不是新机制——**它是"MaskFormer 的 query 被 prompt 条件化 + 大规模数据训练"**。架构创新度不高，**范式创新度极高**。

## 1.5 SAM 最被高估和最被低估的两点

**最被高估**：SAM 的"zero-shot"能力

- SAM 在训练分布外（医学、遥感、显微）**常常工作得不好**
- 社区涌现大量 Medical SAM / Remote Sensing SAM / Personalize SAM 等领域适配
- SAM 的 zero-shot 是"自然图像里的 zero-shot"，不是真正的 universal

**最被低估**：SAM 的 image encoder

- SAM 的 ViT-H encoder 在 1.1B mask 上训练，**其 pixel embedding 本身就是极强的视觉表征**
- 很多后续工作直接拿 SAM encoder 做 backbone（比如 Personalize SAM、HQ-SAM）
- **SAM 的"副产品"是一个一流的视觉编码器**——这件事产品叙事里完全没强调

## 1.6 SAM 的残差（被 SAM 2 和 SAM 3 继承的问题）

1. **没有时间维度**：视频完全不支持
2. **没有真正的语义**：SAM 1 的核心提示接口是 point / box / mask；text prompt 不应被当成原始主体能力，语义主要靠点/框/mask 来"指定"，后续才经 grounding / open-vocabulary 路线外接语言
3. **没有跨 prompt 的实例一致性**：多次点击、多次提示之间没有追踪绑定
4. **计算成本**：ViT-H 很贵，移动端/实时应用难

前两条催生了 SAM 2 和 SAM 3。第三条催生了整个"SAM 跟踪"研究。第四条催生了 MobileSAM / FastSAM / EfficientSAM 等小化工作。

---

# §2 · SAM 2 —— 时间维度进入可提示原语

作者：Ravi, Gabeur, Hu, Hu, Ryali, Ma, ..., Feichtenhofer（Meta，2024 年 7 月）。ICLR 2025 收录。

## 2.1 核心问题

SAM 只能处理图像。视频分割、视频对象追踪（VOS / VOT）历史上是**独立的研究领域**——有自己的架构（memory network、XMem、DeAOT）、自己的数据集（DAVIS、YouTube-VOS）、自己的评估。

SAM 2 的问题是：

> **能不能一个模型同时吃图像和视频？而且图像性能不退化？**
> 

答案：**能**——但需要加一个 memory 模块，和重新定义任务边界。

## 2.2 架构核心 —— Streaming Memory

**关键观察**：视频 = 图像 + 时间。所以 SAM 2 的 backbone 不变（还是 ViT），只在外面加一层 memory：

```
Frame_t  ──→  Image Encoder  ──→  Image Embedding_t
                                        ↓
Memory Bank ──→ Memory Attention ──→ Conditioned Embedding_t
(past frames' features + masks)         ↓
Prompt  ──────────────────────────→  Mask Decoder ──→ Mask_t
                                        ↓
                                    Memory Encoder
                                        ↓
                                    新记忆写入 Memory Bank
```

**工作方式**：

- 视频逐帧处理（streaming）
- 每帧的 image embedding 先被 memory attention **条件化**（attend 到过去几帧的 features + masks）
- 条件化后的 embedding 进入 mask decoder
- 当前帧的输出 + embedding 写入 memory bank 供未来帧使用

**这个设计的巧妙之处**：

- 当 memory bank 为空 → 退化成 SAM（图像模式）
- 当 memory bank 有内容 → 视频模式
- **同一个模型、同一套权重**，图像/视频自动切换

## 2.3 Memory 机制的本质

SAM 2 的 memory attention 本质是**让当前帧的 pixel embedding"知道"过去帧里对象在哪、长什么样**。

为什么这个能工作？回到你之前吃透的"pixel embedding + mask embedding 点积生成 mask"机制：

- 在 SAM 1 里，mask embedding 来自 prompt（一次性）
- 在 SAM 2 里，mask embedding 来自 prompt + memory（时间积累）

**memory attention 做的是：把第一帧的 prompt（"这个对象"）传播到后续所有帧，让每一帧的 query 都"记得"它在追谁**。

这是一个纯 attention 机制——没有显式的 tracker、没有 Kalman filter、没有 ReID 特征——**时间追踪被完全吸收进了 transformer**。

## 2.4 任务边界的重新定义

SAM 2 的任务规格：

- 输入：视频 + 某一帧的 prompt（point/box/mask）
- 输出：整段视频里对应对象的 mask 轨迹

**注意**：

- prompt 只需要在**一帧**上给出
- 可以在任意一帧（不一定是第一帧）
- 可以**中途修正**：如果某帧追错了，用户可以点一下重新 condition 后续帧

**这实际上是交互式视频分割**——一种新的人机交互范式。

## 2.5 SA-V —— 数据引擎再一次发力

SAM 2 配套的 SA-V 数据集：

- 50.9K 视频，642.6K masklet（masklet = 一个对象在视频里的 mask 轨迹）
- **同样用 data engine bootstrap**：人工 + SAM 2 辅助标注
- 规模远超之前任何视频分割数据集（YouTube-VOS ~4K）

这**再一次验证了 SAM 的 bootstrap 数据工程可以迁移**——换一个任务，重新 bootstrap，又吃下一个新领域。

## 2.6 SAM 2 在图像上反而更好了

一个反直觉的结果：**SAM 2 在图像分割上也比 SAM 1 更好**。

为什么？几个原因：

- 训练数据更多（SA-1B + SA-V 图像帧）
- 架构更统一（hierarchy ViT + 更好的 decoder）
- memory 机制在单帧时退化为 identity，但 loss 设计改进了分割质量

**所以 SAM 2 对 SAM 1 是一个严格包含**——图像模式等价于 SAM 1+，视频模式是新能力。

## 2.7 SAM 2 的残差

1. **仍然没有"概念"**：text prompt 依然弱，语义靠点/框/mask 指定
2. **被追踪对象是"anonymous"的**：模型不知道追的是"狗"还是"车"——只知道"prompt 里指定的那个东西"
3. **一次只能追一个对象**（逻辑上）——多对象要跑多次，效率低
4. **memory 是"短期"的**：长视频里对象消失再出现，可能追丢

第 1、2 条催生 SAM 3。第 3 条催生 SAM 3.1。第 4 条仍是 open。

---
