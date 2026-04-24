> 编者说明：本页是“统一 Mask 架构”组的深推导汇编稿，内部保留了若干从 SegFormer / OneFormer / SegGPT / EoMT 逐步累积而来的专题段落。阅读时可先看 §6 主体与其残差判断，再按后续专题追踪 decoder 变薄、单权重统一与 encoder-centric regime 的细部推演。

# §6 · EoMT —— Decoder 变薄到 encoder-centric regime

本节按重要性展开，并先校正几条背景事实：

- **作者**：Kerssies, Cassara, Fontanel, de Geus, Cordts, Gall（TU Eindhoven + RWTH + Mercedes-Benz + Uni Bonn）
- **发表**：**CVPR 2025 Highlight**，不是 ECCV 2024
- **arxiv 2503.19108**（2025 年 3 月）
- 完整名字：**Encoder-only Mask Transformer**

## 6.1 核心问题 —— 任务特异组件真的必要吗

Mask2Former 架构（你已经吃透了）：

```
ViT → Adapter (加多尺度)  → Pixel Decoder → Transformer Decoder with queries → masks
     ↑                    ↑                  ↑
     为ViT补多尺度        融合多尺度         query cross-attention
```

**这里的每个组件都是"任务特异的"**：

- ViT-Adapter：ViT 没有多尺度，加 conv adapter 补多尺度（为分割量身打造）
- Pixel Decoder：多尺度融合（专门给分割/检测用的）
- Transformer Decoder：query cross-attention（MaskFormer 范式）

EoMT 作者的关键问题：

> **这些"任务特异的归纳偏置"，真的必要吗？还是说，如果 ViT 本身足够大 + 预训练足够强，它自己就能学会这些？**
> 

这个问题不是他们凭空提的——它对应 LLM 领域已经被回答的问题：

- 早期 NLP：要 CNN 做 n-gram、要 LSTM 做长依赖、要专用架构做机器翻译
- GPT-3 之后：一个纯 transformer 在足够规模和预训练下，可以把大量任务压到通用接口里
- 特异架构被 scale 显著削弱，但没有在所有任务中彻底消失

EoMT 赌的是：视觉会部分重复 NLP 的故事。在强预训练 ViT 与适当 query 注入条件下，adapter / pixel decoder / transformer decoder 可以在一部分分割任务上大幅变薄，甚至退化为可选读出机制。

## 6.2 EoMT 的架构 —— 极简到令人震惊

```
Image patches: P_1, P_2, ..., P_M
Queries:       Q_1, Q_2, ..., Q_N

拼成一个序列: [P_1, ..., P_M, Q_1, ..., Q_N]
              ↓
          ViT (DINOv2 预训练的)
              ↓ 所有层都是标准 self-attention
          [P'_1, ..., P'_M, Q'_1, ..., Q'_N]
              ↓
    用 Q' 和 P' 做点积生成 mask (就像 MaskFormer)
```

**没有 adapter。没有 pixel decoder。没有 transformer decoder。就是一个 ViT + N 个 query token 一起塞进去**。

**精确描述**：

- ViT 的每层标准 transformer block（self-attn + FFN）
- patch tokens 和 query tokens **完全平权**——都是 token，一起做 self-attention
- query tokens 通过 self-attention **自发地**去 attend patch tokens（反之也成立）
- 最后一层输出后：取出 query tokens 和 patch tokens，做点积生成 mask

**这等价于说**：**Cross-attention 是 self-attention 的一个特例**——只要把 query 和 key/value 塞进同一个序列，self-attention 自动就在做 cross-attention。**DETR 原本专门设计的 transformer decoder 是多余的**。

## 6.3 Mask Annealing —— 去掉 masked attention

Mask2Former 用 masked attention 让每层 query 只看自己上一层的 mask 区域。EoMT 在训练早期也用——但论文发现这在推理时是**速度瓶颈**。

EoMT 的解决方案 **mask annealing**：

- 训练时用 masked attention（帮助收敛）
- 但**训练过程中逐渐降低 mask 的强度**——让模型慢慢适应没有 mask 的情况
- 训练结束时模型已经不依赖 mask
- **推理时不用 masked attention**——纯 self-attention，速度翻倍

这个 trick 让 EoMT 在推理时比 Mask2Former 快——因为最贵的 masked attention 被去掉了。

## 6.4 性能上限 —— 你最关心的

数据来自论文 Table 1 和 CVPR 2025 officially published version：

### COCO 全景分割（PQ）

| 模型 | Backbone | PQ | FPS | 参数量 |
| --- | --- | --- | --- | --- |
| ViT-Adapter + M2F | ViT-B | 54.4 | 32 | ~150M |
| ViT-Adapter + M2F | ViT-L | 55.9 | 18 | ~320M |
| ViT-Adapter + M2F | ViT-g | 58.2 | 5 | ~1.1B |
| **EoMT** | ViT-S | 50.7 | ~300+ | 22M |
| **EoMT** | ViT-B | 53.0 | ~200+ | 86M |
| **EoMT** | ViT-L | **56.0** | **128** | 300M |
| **EoMT** | ViT-g | **56.9 ~ 58.3** | ~30-50 | 1B+ |

**关键数据点**：

- **EoMT-L（ViT-L）**：56.0 PQ @ 128 FPS
- vs **ViT-Adapter + M2F (ViT-L)**：55.9 PQ @ 18 FPS
- **同等 backbone，EoMT 精度略高 + 速度快 7 倍**

### ADE20K 语义分割（mIoU）

| 模型 | mIoU |
| --- | --- |
| Mask2Former (Swin-L) | 56.1 |
| ViT-Adapter + M2F (ViT-L) | 58.0 |
| **EoMT-G (ViT-g/14 DINOv2)** | **58.1** |

EoMT-G 在 ADE20K 达到 **58.1 mIoU**——持平或略超 state-of-the-art，**但用的是完全 decoder-free 架构**。

### COCO 实例分割

论文报告 EoMT-L: 46 AP 左右，和 Mask2Former-L 接近但更快。

### 后续版本：EoMT + DINOv3 (2025 年后)

Hugging Face 已经放出了 **EoMT-DINOv3 变体**。DINOv3 相比 DINOv2：

- 更大的预训练数据（1.7B 图像）
- RoPE 位置编码
- 可选 gated MLP
- **在所有三个任务上都进一步提升**（ADE20K 可能到 60+ mIoU 的量级，但具体数字看官方 model zoo）

### 速度性能曲线

论文里最核心的图（Figure 1）是**速度-精度 Pareto 曲线**：

- ViT-Adapter + Mask2Former 曲线在左上（慢但精度高）
- **EoMT 曲线整体在它右上方**（更快 + 同精度，或同速度 + 更高精度）
- 所有 ViT 规模（S/B/L/g）都是如此

**这就是 EoMT 的真正卖点**：不是"精度 SOTA"，而是**同精度下速度 4× 提升，或同速度下精度大幅提升**。

## 6.5 性能上限的判断

**精度上限**在哪？直接看趋势：

**EoMT 的精度线性依赖于 ViT 的预训练质量**。论文一个关键 ablation 表明：

- ViT-L with ImageNet pretrain: 落后 Mask2Former
- ViT-L with MAE pretrain: 接近
- **ViT-L with DINOv2 pretrain: 超过** Mask2Former

**核心洞察**：**EoMT 的天花板就是"通用视觉预训练"的天花板**——DINOv2 / DINOv3 / 后续更强的预训练模型越强，EoMT 越强。

这意味着 EoMT 把分割从**"分割任务的专门研究"**变成了**"通用视觉预训练的下游应用"**——分割精度的提升不再来自 segmentation-specific 创新，而是**完全跟随预训练 scaling law**。

**当前（2025）的上限估计**：

- COCO 全景：EoMT-G (DINOv3) 可能摸到 **58-60 PQ**
- ADE20K 语义：**58-61 mIoU**
- COCO 实例：**46-50 AP**

**但这个"上限"的性质和以前不同**：

- Mask2Former 时代的 SOTA 竞争是"各路人马在 backbone / decoder / loss 上微调"
- EoMT 时代的 SOTA 竞争**归约到"谁有更好的预训练 ViT"**——分割精度的上限约等于 ViT 的表征质量

## 6.6 真正的天花板在哪里

这是更深层的问题。几条线索：

**(1) 预训练 scaling**

- DINOv2 ViT-g: 1.1B 参数
- DINOv3: 6.7B 参数（最大版本）
- 未来还能继续 scale，EoMT 直接吃这个红利

**(2) 任务头的 poverty**

- EoMT 的 query 做点积生成 mask——仍然是 MaskFormer 的头
- 这个头本身不是瓶颈——瓶颈在 pixel embedding 的质量
- 未来若有更聪明的 query 头，可能还有小幅提升（但边际）

**(3) 数据的 poverty**

- EoMT 在 COCO / ADE20K 上训
- 这些数据集的 GT 天花板本身就有限（标注误差 ~2-3 mIoU）
- **真正的突破需要更大的标注数据或合成数据**
- SAM-2 的 1B mask 数据就是这条路

**(4) 理论上的真正天花板**

- "给一张图，它的语义分割 GT 是唯一确定的吗？"——不是。边界总有歧义
- 人标注者之间的一致性 ~90-95%——这是**人类 Bayes 上限**
- EoMT-G 的 58 mIoU 大概是人类上限的 85-90%——**剩下的 10-15% 可能已经是标注噪声**

所以 EoMT 的天花板不是"还能继续涨 5-10 个点"的问题——它已经接近**任务本身的信息上限**。

## 6.7 EoMT 的本体论意义

EoMT 做的事情**在阶段 II 里具有极限节点意义**。让我说明：

**阶段 II 的整条线可以这样概括**：

```
FCN         → encoder-decoder 都需要，decoder 重
MaskFormer  → encoder 可以轻 (ViT)，decoder 中等
Mask2Former → decoder 更重 (多尺度 + masked attn)
SegFormer   → 把 decoder 砍到 MLP
EoMT        → 连轻 decoder 也不要，encoder 自己承担全部
```

**这不是一个线性下降的曲线——它是"任务结构被通用表征吃掉"的 phase transition**：

- 早期：**任务特异组件 + 通用 backbone**
- 中期：**任务特异 decoder + 通用 encoder**
- encoder-centric regime：**通用 encoder 承担更多读出责任，任务 token / query 作为输入的一部分**

EoMT 的论文副标题是《Your ViT is Secretly an Image Segmentation Model》——这句话本身是一个宣言：强视觉预训练模型已经包含大量分割所需的空间表征；我们过去加在 decoder 上的若干工作，可能已被 encoder 吸收。

这和 NLP 的命运完全平行：

- NLP: "LSTM 要翻译头，BERT 要 seq2seq 头"——GPT 系列证明大规模预训练可以显著减少任务特异结构
- Vision: "ViT 要 adapter 要 pixel decoder 要 transformer decoder"——EoMT 证明 ViT + DINO 级预训练可以在部分分割任务上大幅削弱专用 decoder

**架构简化的背后是表征质量的提升**——这是 scaling 时代的通用规律。

## 6.8 对阶段 III / IV / V 的意义

EoMT 不只是"更快的 Mask2Former"——它是**通用视觉基础模型时代的第一个完整落地案例**。它证明：

> **许多"从稠密视觉表征读出区域/实例类结构化输出"的任务，可以被强力表达为"通用 ViT + 任务 query token + 点积读出"。**
> 

这条判断直接推广到：

- **3D 分割**：ViT + 3D query token + 点积 → EoMT 的 3D 版（已经有人在做）
- **视频分割**：VidEoMT（论文 2024 12 月，已经验证）
- **开放词汇分割**：EoMT + CLIP text embedding 作为 class head
- **Depth estimation**：DPT 已经这样做了，只是还没叫 EoMT

换句话说，**EoMT 不仅是阶段 II 的极限节点，也向阶段 III / IV / V 回流**。后续许多区域/实例类稠密任务会靠近这种 encoder-centric 形态，但连续场、时序、3D、关系与开放语义任务仍可能需要 decoder、adapter、memory 或 tool head 回流。

这就是它的**真正地位**——不是 "the final segmentation model"，而是 "**the first post-segmentation model**" 的强候选：一个尽量不把"分割"当特殊任务的分割模型。

## 6.9 EoMT 的残差

- **训练仍然依赖大规模预训练的 ViT**——没有 DINOv2/v3 级预训练，EoMT 精度下降明显
- **推理时仍需要 query 机制**——如果未来想做"无 query"架构，EoMT 还不是终点
- **对开放词汇的支持不原生**——需要把 class head 换成 CLIP 风格的 text similarity（但这是 trivial 的工程工作）
- **视频、3D 扩展仍在研发中**——VidEoMT 还在 arxiv preprint，没完全成熟

## 6.10 一条后续延伸

EoMT 作者的跟进工作 **VidEoMT** (《Your ViT is Secretly Also a Video Segmentation Model》，2025-2026) 把同样的哲学推到视频分割：

- 同样的 ViT
- 加一些轻量的 cross-frame attention 扩展
- 对比专用视频分割模型（DVIS++、CAVIS）**持平或超过**
- **再次证明"decoder-free + 通用预训练"是普适的**

所以 EoMT 不是一篇 paper——它是**一个正在铺开的研究 program**。它的上限不是单篇论文能定的，而是由**通用视觉预训练的上限**决定的。

---

## 编排建议

页面 [阶段 II · 统一 Mask 架构：区域/实例类稠密任务的一种强统一范式](00-定位卡.md) 目前 §5 Painter/SegGPT 和 §6 EoMT 仍然偏短，因此本页更适合承担它们的深度正文角色。保留定位卡负责速览、保留本页负责深推，是这一组最稳的两级分工方式：

- **A. 替换 §5 和 §6**：把上面两段（SegGPT + EoMT 完整展开）替换原有短描述
- **B. 整合整页**：把之前聊天里积累的 MaskFormer/Mask2Former、SegFormer/OneFormer、SegGPT/EoMT **六篇一起大翻新**，页面从短条目转成完整深度展开版（这是最彻底的做法，和你之前整合 [阶段 II · Anchor-free 与端到端查询：从先验到查询（CornerNet / CenterNet / FCOS / DETR / Deformable DETR / DINO-DETR / Co-DETR）](..\§14-Anchor-free与端到端查询\00-定位卡.md) 的做法一致）
- **C. 保留为独立深推页**：让定位卡维持轻量，本页专门承载技术细部与跨阶段判断。

从长期编排看，A 适合局部补页，B 适合整组重构，C 适合保持“总览页 + 深推页”的分工。

## 5 · Painter / SegGPT (Wang 等, CVPR / ICCV 2023)

**共形贡献**：把分割改造成「给定示例图像-掩码对，对新图像做 in-context 推断」——分割获得提示化雏形（以图-掩码对做提示，不必文字）。In-context 稠密预测的开端，直接启发了 SAM 的交互范式。

🔗 [https://arxiv.org/abs/2304.03284](https://arxiv.org/abs/2304.03284)

## 6 · EoMT —— *Your ViT is Secretly an Image Segmentation Model* (Kerssies, Fontanel, Cordts, Gall, CVPR 2025)

**共形贡献**：连 Mask2Former 那套专用 transformer decoder 都可以省掉——直接把 segment query 混进 ViT 的 token 序列里，和图像 patch token 一起做自注意力，encoder 同时承担 backbone 和 decoder。ViT 预训练越强，EoMT 越受益——它把「分割架构」彻底还原成「通用视觉表征 + 查询读出」。

🔗 [https://arxiv.org/abs/2503.19108](https://arxiv.org/abs/2503.19108)

---

## 本组合力的残差

到 2024，区域/实例类稠密任务的**架构维度**高度收束：一个 backbone + 一组查询 + 一种匹配/读出机制，接管了大量分割、检测和全景任务。但架构收束之后，一个更深的问题暴露出来：

- **类别边界仍在训练集之内**。Mask2Former 在 COCO 上训，只能输出 COCO 的 80 类。第 81 类（「独角兽」）没有通道，mask 出不来。
- **语义来源单一**。所有分类头都是一个线性层 + softmax——语义存在于训练集的离散索引里，不存在于语言或提示里。
- **提示化的雏形（SegGPT）只做到视觉提示**，文字作为提示进不来。

→ 这两条残差合起来，指向阶段 II 的出口：**引入语言 / 点 / 框作为一级提示原语，把类别闭集拆开**。SAM、Grounding DINO、APE、CAT-Seg、Depth Anything 这一代要出场——同时这也是 Pre-LLM 时代稠密视觉的自然终点，以及视觉-语言共形（阶段 III / V）的入口。

**每一处架构选择本质上都在回答：'这件事由谁来负责最经济？'**

- **Mask embedding vs Pixel embedding**：分工是"选择由 query 做，承载由 feature 场做"
- **Projector vs Cross-attn**：分工是"粗对齐交给 projector，细对齐让 LLM self-attn 包办"
- **Bottleneck vs FFN**：分工是"主干维度 vs 工作维度 —— 按任务选压缩或扩张"
- **FPN 加法**：分工是"语义 channel 共享 + 尺度作为 orthogonal 维度"

四个问题的共同主线：**深度学习里"信息的分工"是设计的核心艺术**。

# 小结

---

这个分工逻辑在后面的 SAM / Grounding DINO 里被进一步放大——SAM 的贡献是"把 mask embedding 的来源从内生参数换成用户 prompt"，但"prompt 只负责选择方向、pixel embedding 承载形状"这个分工**一字不差地继承下来**。

三个维度各司其职，在点积那一步汇合——这就是 MaskFormer 范式的"**稀疏选择 + 稠密承载**"的分工哲学。

- **语义/对象身份** 由 mask embedding 的方向选择决定
- **位置** 由 pixel embedding 场的 positional encoding 决定
- **形状** 由 pixel embedding 场的空间结构决定

形状、位置、语义这三件事被**分工**：

**更准确的说法**：mask embedding 是一个**选择算子**——它在嵌入空间里投票"我想要长这样的像素"，然后 pixel embedding 场**自动告诉它这种像素在图像平面上在哪**。

正确答案：**都不是**。mask embedding 编码的是"**pixel embedding 空间里的一个方向偏好**"——既不是形状（形状在 pixel embedding 场里），也不是位置（位置在 pixel embedding 的 positional encoding 里）。

> mask embedding 本质上是编码了要去观察的物体的形状吗，还是指向某个位置呢？
> 

你最初的问题：

## 4.10 和你之前直觉的对接

这就是为什么 Mask2Former 在 COCO 上训、在 ADE20K 上测**形状精度还能接受**——类别可能错，但"哪些像素连在一起"的判断依赖 pixel embedding 的普适表征能力，这个是可迁移的。

**所以形状泛化能力来自 pixel embedding 场的表征泛化，不来自 mask embedding**。

- **mask 形状自动适应新狗的实际轮廓**——因为 pixel embedding 场本身对新输入做了编码
- mask embedding 就能正确激活这些像素
- 只要 backbone + pixel decoder 把这只狗的像素映射到**接近训练时学到的那个狗方向**

**推理时见到新的狗**（没见过的品种、姿势、光照）：

训练集里见过"狗"的样本，pixel embedding 场学会把"狗像素"映射到空间某个方向。

## 4.9 深一层：这个机制为什么意味着"泛化"

- **输出分辨率和 pixel embedding 场一样——随意分辨率**
- 形状从 pixel embedding 场"天然涌现"
- $D$ 个参数（mask embedding 自身）

MaskFormer 的点积机制：

- 输出分辨率固定——换图像大小就失败
- **mask 的空间结构完全要从 query 参数里学**，没有利用 pixel embedding 场的空间先验
- $D \to HW$ 的参数量是 $D cdot HW = 256 cdot 224^2 approx 12.8M$——每个 query 要 12M 参数

问题：

另一种架构：让 mask embedding 直接输出一个 $H \times W$ 的 mask（相当于一个 MLP: $D to HW$）。

## 4.8 对比：如果让 mask embedding 自己编码形状

**这是一种极其经济的设计**——**把"高维输出"的信息存储从 query 端 offload 到了 pixel embedding 场**。query 只管"选哪一类"（低维决策），pixel embedding 场承担"这一类长什么样子"（高维表征）。

**答案：从 pixel embedding 场里来**。pixel embedding 场是 $HW \times D$ 的张量——它编码了"每个位置应该在哪个嵌入方向"。mask embedding 只需要指定"我要哪个方向"，形状这个 $HW$ 维的东西就**由 pixel embedding 场的空间结构自动展开**。

但 MaskFormer 的 mask embedding 只有 $D=256$ 维！**它用** $D$ **维向量生成了** $HW$ **维输出**——多出来的 $(HW - D)$ 维信息从哪来？

换个视角看："**形状生成**"是一个本来需要 $HW$ 个空间坐标的输出——如果要让 mask embedding 直接编码形状，它需要是 $HW$ 维才行。

## 4.7 为什么这个设计巧妙

**mask 的形状 = 被磁极吸起的粉末在桌面上的图案**

**pixel embedding 场 = 金属粉末的空间分布**

**mask embedding = 磁铁的磁极**

- 这些粉末颗粒在桌面上的原始分布（对应：这些像素在图像平面上的原始位置）
- 哪些粉末颗粒能被这个磁极吸引（对应：哪些 pixel 的 embedding 和 mask embedding 对齐）

磁铁没有任何关于"形状"的信息。形状完全取决于：

想象你在一堆金属粉末（pixel embeddings）上放一块磁铁（mask embedding）——磁铁本身没有形状，只有磁极方向。但它一接近粉末，所有"能被这个磁极吸引的粉末颗粒"都会向上浮起——**这些浮起的颗粒在桌面上的分布图，就是"磁铁的 mask 形状"**。

## 4.6 用个类比

> **mask embedding 从来没见过"形状"。它只知道"嵌入空间里的某个方向"。形状是图像像素到嵌入空间的映射的"反向投影"**——**mask embedding 的语义责任只到"是不是一类"，形状是 pixel embedding 的映射场**自动赋予的。
> 

**关键洞察**：

1. "对齐的像素在图像平面上占据哪些 $(x,y)$" —— **这个集合就是 mask 的形状**
2. 对每个图像像素，判断它的 pixel embedding 是否和这个方向对齐
3. mask embedding $e_k$ 在**嵌入空间**里画一条方向（纯代数）

**形状的生成过程**：

**两个空间被"pixel embedding 场"这个映射连接**：每个图像像素 $(x,y)$ 被映射成嵌入空间的一个点。

- mask embedding 指向这个簇——这是嵌入意义上的"选中这一类"
- 狗的所有像素聚成一个簇——这是嵌入意义上的"一类"

**嵌入空间（pixel embedding 的** $D$ **维空间）**：

- 这是我们希望 mask 输出的东西
- 狗占据 (x, y) 坐标下的某个区域——这是视觉上的"形状"

**图像平面（真实像素空间）**：

让我把这个问题切得非常细。形状这件事**存在于两个完全不同的地方**：

## 4.5 关键点：形状从哪里来

**这个 mask 在图像平面上的几何形状——就是狗的轮廓**。

**结果**：扫描整张图的 HW 个像素，得到一个 $H \times W$ 的 mask：每个像素是否属于狗。

- 树像素 embedding 和 $e_{dog}$ 在不同方向 → 点积小（甚至负）→ sigmoid ≈ 0 → **不属于 dog mask**
- 天空像素 embedding 和 $e_{dog}$ 近乎正交 → 点积 ≈ 0 → sigmoid ≈ 0.5（这个临界值会被后续 class head 的 "no-object" 过滤）
- 狗像素的 embedding **和** $e_{dog}$ **同向** → 点积大 → sigmoid ≈ 1 → **属于 dog mask**

对 dog query ($e_{dog}$)：

$$
m_k(i) = \sigma(e_k \cdot E_{pix}[i])
$$

对每个像素 $i$，计算它和每个 mask embedding 的点积：

## 4.4 Mask 怎么生成

三个 mask embedding 是**嵌入空间里的三个方向向量**。**它们本身没有形状，只是方向**。

```
           第二维 ↑
                  │
                  │     ↗ e_dog     ← 指向狗簇的方向
                  │
                  │
← e_sky ⬋          │
                  │
                  │              e_tree →    ← 指向树簇
                  │
                  │
                  └──────────────→  第一维
```

假设训练完后，模型有三个 mask query，对应三个输出 mask。它们经过 transformer decoder，得到三个 mask embedding 向量：

## 4.3 Mask embedding 做什么

- **自然而然**，狗的所有像素被推向嵌入空间的同一个方向——形成簇
- 训练梯度反向传播会把"应该属于狗的像素"在那个方向上推高
- 这要求这些像素的 embedding 在**某个方向上是正的**
- "被同一个向量激活" = "和同一个方向有正点积"
- 每个对象（狗）的所有像素最终要被**同一个 mask embedding** 激活

**为什么会聚？** 不是因为模型被直接教"把同类像素聚一起"——而是因为**下游的 mask prediction 在逼着它聚**：

```
            第二维 ↑
                   │
                   │     ★★★★        ← 狗像素的簇
                   │    ★★★★★
                   │     ★★★
                   │
 ●●●               │
●●●●●              │
 ●●●               │
← 天空像素的簇      │
 ●●                │           ■■■      ← 树像素的簇
                   │          ■■■■■
                   │           ■■■
                   │
                   └──────────────→   第一维
```

训练好的模型，这张图的 $HW$ 个像素在嵌入空间里不是随机分布的——**它们会聚成若干簇**：

## 4.2 训练会把 pixel embedding 排成什么样

为了可视化，把 $D$ 简化成 2 维。每个像素在**2 维嵌入空间**里是一个点。

每个像素是一个 $D$ 维向量（比如 $D=256$）。

$$
E_{pix} \in \mathbb{R}^{H \times W \times D}
$$

想象一张图，里面有一只狗、一棵树、一片天空。图像经过 backbone + pixel decoder 后，得到 pixel embedding 场：

## 4.1 先铺设定

这段你没完全吃透，我估计卡点在"判别方向如何变成形状"这一步。我用具体数值例子把它打穿。

# §4 · "形状是浮现的"—— 把机制讲透

---

这是一个"让下游的强模型承担更多工作"的设计哲学——同样的思路还出现在 Diffusion 的 CLIP conditioning（CLIP embedding 直接塞进 UNet）、SAM 的 prompt encoder（简单 MLP）、甚至 ControlNet（zero conv 注入）等地方。

> **Projector 是 cross-attention 的"极简版"——它放弃了每层重做对齐的能力，换来零改动 LLM 的工程便利。当 LLM 自身足够强大时，self-attention 可以覆盖大部分对齐需求，projector 足矣**。
> 

**一个凝练的判断**：

- 在 VLM 里，场2（图像 token）和场1（文本 token）的对齐是**极其高阶的语义任务**——分两步做，把重活交给已有的 LLM，是更经济的选择
- 在 MaskFormer 里，场2（pixel embedding）相对简单——cross-attention 一次就够

**哪种更好？取决于"场2"的复杂度**：

而 MaskFormer / DETR 把这两步**合并成一个 cross-attention**——每一层都同时做坐标对齐 + 细粒度对齐。

1. **LLM 的 self-attention 做细粒度对齐**：在共享坐标系里反复 mixing
2. **Projector 做坐标系对齐**：让两个场处于同一张"语言坐标系"

**所以 projector + LLM 的组合，是另一种"异构场共形桥"——它把"跨模态对齐"这件事分成两步：**

| 维度 | MaskFormer | VLM (LLaVA) |
| --- | --- | --- |
| 场1 | 100 个 query | Text token stream |
| 场2 | Pixel embedding 场 | Image token 集合 |
| 桥的机制 | Cross-attention (学习的对齐) | Projector (MLP) + LLM 的 self-attn |
| 桥的重量 | 重（每层都 cross-attn） | 轻（一次 projection）+ 复用 self-attn |
| 桥的设计哲学 | **显式对齐** —— 每层在两个场之间建立新的对齐 | **隐式对齐** —— 让两个场共用一个坐标系，依赖 self-attn 在混合序列里自然对齐 |

精确的对照：

回到你的原始问题："cross-attention 是异构场之间的共形桥，那 projector 承担了什么角色？"

## 3.5 和 MaskFormer 的架构对比

**历史结论**：**Projector 赢了**。2023-2024 主流 VLM（LLaVA 系、Qwen-VL 系、InternVL、MiniCPM-V）几乎都是 projector 派。Flamingo 路线基本被淘汰。

| 方案 | 代表模型 | 特点 |
| --- | --- | --- |
| **Projector** (MLP) | LLaVA, MiniGPT-4 | 最简单，LLM 零改动，训练便宜 |
| **Q-Former** | BLIP-2 | 可学习 query 做语义压缩，再塞给 LLM |
| **Cross-attention layer** | Flamingo, IDEFICS | 在 LLM 内部插 cross-attention 层 |

**三条路对比**：

- 然后把这 32 个 query 作为 prefix 塞给 LLM（又变回 projector 思路）
- 通过 cross-attention 从图像里聚合信息
- 32 个可学习 query（和 DETR 一样的思路）

**BLIP-2** 用的是 "Q-Former"——介于 projector 和 cross-attention 之间：

- 让 LLM 在这些层里专门从图像 key-value 里检索
- 在冻结的 LLM 每隔几层插入一个 "gated cross-attention" layer

你不是完全没见过 cross-attention 的 VLM——**Flamingo (DeepMind, 2022)** 就用了 cross-attention：

## 3.4 Flamingo 和 BLIP-2 的异类选择

**LLM 自身就是一个超级灵活的"动态 query 生成器"**——它在 self-attention 里通过每一步的 token 不断重新组织"我现在要看图像的哪部分"。你不需要外部的 cross-attention layer 提供这种能力，LLM 自己会做。

Cross-attention 的设计假设是"query 是简单的信息需求，需要从 key 场里检索"。但在 VLM 里，"query"是 LLM 的整个推理链——这是一个极其复杂的动态 query，不是 100 个固定 slots。

### 理由 4：LLM 已经在做高级 reasoning

LLaVA 的 projector 只有几百万参数，几 GPU 小时就能训到可用——这在 cross-attention 方案下不可能。

Projector 只要学**两个空间的坐标旋转**，参数少得多，训练效率高。

Cross-attention layer 需要从零学**跨模态对齐**，这要大量 paired data。

### 理由 3：训练数据的奢侈

这比专门加 cross-attention layer **更优雅**——复用了 LLM 已有的结构。

**Projector 只负责"让图像 token 进入 LLM 的语言空间"，之后的跨模态对齐全部由 LLM 的 self-attention 免费提供**。

所以 LLM 的 self-attention 层**自己就承担了 cross-attention 的功能**——只要 projector 把图像 embedding 摆到 LLM 能看懂的位置上，self-attention 会在每一层反复把文字和图像对齐。

- **text ↔ image**（这就是 cross-attention 的本质）
- image ↔ image（visual self-attention，相当于 ViT 的一部分）
- text ↔ text（原本的 text attention）

在 LLM 里塞进图像 token 后，**self-attention 同时在做三件事**：

### 理由 2：LLM 的 self-attention 已经是 cross-modal attention 了

**Projector 是"零架构改动"的方案——LLM 以为自己收到的就是一串普通 token，不知道里面有图像**。这个"兼容性"极其珍贵——省去了在每个 LLM 架构（Llama / Mistral / Qwen）上重新实现 cross-attention layer 的工程成本。

- LLM 架构**完全不改动**
- 然后 image token 和 text token 一起**只做 self-attention**（原本就有的，计算量不变）
- **一次 projection**（几 million 参数）

用 projector + 塞进 sequence 的做法：

- 每层 $32 \times 2048 \times 256 = 16.7M$ 次点积
- $N_v$ 是 256（CLIP-14, 16x16 patches）
- $N_t$ 可以到 2048
- Llama-7B 有 32 层

Cross-attention 在每层 LLM 都要做一次——$L$ 层 LLM × $N_t$ text tokens × $N_v$ image tokens 的 attention 计算。

### 理由 1：计算复杂度

这是关键问题。我给你四个理由，按重要性排序：

## 3.3 为什么不用 cross-attention？

> **把两个分离的表征空间的坐标系对齐，让跨模态的 token 能混在一起被 LLM 处理**。
> 

所以 projector 的任务是：

- Projector 学一个**线性/MLP 变换**，把图像 embedding 旋转 + 缩放到 text token 空间里能被 LLM "直接读懂"的位置
- 两个空间的**基（basis）不同**——768 维的第一个方向和 4096 维的第一个方向是两回事
- LLM 的输入 token 空间 $mathbb{R}^{D_t}$（比如 Llama 的 4096 维）
- Vision encoder 的输出空间 $mathbb{R}^{D_v}$（比如 CLIP ViT 的 768 维）

具体地：

**Projector 不是在做"cross-attention 对齐"的工作——它在做一件更弱的事：空间对齐（subspace alignment）**。

## 3.2 Projector 到底做了什么

Projector 是一个 MLP（通常 2 层），把 image embedding 从 $D_v$ 维**简单线性投影**到 text token 空间 $D_t$ 维。

```
Image → Vision Encoder → E_img ∈ R^{N_v × D_v}
                              ↓
                        Projector (MLP)        ← 这一步
                              ↓
                        Ẽ_img ∈ R^{N_v × D_t}
                              ↓
                     [被塞到 text token 序列里]
                              ↓
Text + Ẽ_img → LLM → 输出
```

**主流 VLM（LLaVA / MiniGPT / BLIP）**：

Query 直接通过 cross-attention 在 $E_{img}$ 里检索信息。**两个场通过 attention 对齐**。

```
Image → Vision Encoder → E_img ∈ R^{HW×D_v}
                                      ↓
                              (Cross-attention)
                                      ↓
Query → Transformer Decoder → Mask
```

**MaskFormer / DETR 式**（纯 cross-attention 对齐）：

## 3.1 两种架构对比

这是一个很锋利的问题。你抓到了 VLM 架构里一个看似"退步"的选择，实际上是**一个经过深思熟虑的工程权衡**。

# §3 · VLM 里的 projector —— 为什么不用 cross-attention？

---

这和你的共形理论可以挂上：**残差分支的维度选择，是由"那一层具体测量什么共形关系"决定的**——空间共形（卷积）在低维做，语义共形（非线性分类）在高维做。

**两者都在"主干 stream 之外另开一个合适的工作空间"**——只是工作空间的维度取决于要做的事。如果"做事"是空间卷积（昂贵），就压；如果"做事"是非线性判别（便宜），就扩。

- FFN 分支: 扩到 $4D$ 做非线性——扩容量
- Bottleneck 分支: 压到 $D/4$ 做 conv——省算力
- 主干 stream: $D$ 维

> **残差分支里那个"做事的 sub-module"，需要在一个和主干 stream 不同的维度上工作。**
> 

Bottleneck 和 FFN 看似对立，但**合起来讲的是同一件事**：

## 2.6 一个统一视角

**Mixture of Experts (MoE)** 模型就是在这里动刀的——把 $D \to 4D$ 的 FFN 换成**多个专家**，每个 token 只激活 2 个专家——**容量扩张但计算不扩张**。MoE 的本质就是"把 FFN 这一步做得更激进：扩到 $32D$ 但只激活 $2D$"。

这是个"激活稀疏性"的工程反推。用 $8D$ 更好？**边际收益递减，计算成本加倍**——$4D$ 是甜点。

- 加上"多余容量让非线性分类更稳"的 safety margin，变成 $4D$
- 要在激活后还有 $D$ 维有效信息，激活前至少要 $2D$
- GELU / ReLU 激活大约**砍掉一半的神经元**（负的部分被置零）

这个 4× 是经验值，从 BERT 到 GPT-4 几乎不变。直觉是：

**为什么 $4D$？**

## 2.5 还有更深的一层

- Transformer 时代，token 数 N 不大（如 100 query, 196 patches），每个 token 的计算预算充足——可以扩
- 卷积时代，空间维度（HW）很大（如 224×224），channel 维度再大计算就爆——必须省

**这两种假设都对，只是适用场景不同**：

| 维度 | Bottleneck | FFN |
| --- | --- | --- |
| 形状 | $D \to D/4 \to D$ | $D \to 4D \to D$ |
| 中间维度的角色 | "真正信息的子空间" | "临时非线性展开空间" |
| 假设 | 高维冗余，用低维做重活 | 低维受限，临时升维做非线性 |
| 重活做在哪 | 中间的 3×3 conv | 中间的激活函数 |
| 目的 | 节省计算 | 扩大非线性表征能力 |

## 2.4 本质差异 —— 两者对立的"哪里有信息"假设

这是一个**容量扩张**的设计——假设当前维度不够，需要外扩到更高维暂时处理。

> **在** $D$ **维里不够表达丰富的非线性，需要**临时扩展到 $4D$**去做非线性判别，再**投影回 $D$**作为残差注入**。
> 

**FFN 的核心假设**：

- 压回 $D$——把 $4D$ 维里学到的非线性混合**浓缩**回 $D$ 维的残差 stream
- GELU 激活在 $4D$ 维空间里做非线性判别——在高维里，不同概念更容易线性可分
- 升维到 $4D$——让每个 token 的表征在更高维空间里"**展开**"，高维里才有足够的空间给非线性（GELU / ReLU）"切"

具体机制：

**FFN 的任务**：**在每个 token 上做一次非线性的表征扩容**。

Self-attention 是一个**线性**操作——它只是 token 之间的加权线性混合。一个 Transformer block 如果只有 self-attention，整个模型会塌成线性（虽然 softmax 非线性一点，但表达力有限）。

Transformer FFN 的**设计动机完全相反**：

## 2.3 FFN 的目的：非线性表征扩容

这是一个**容量节约**的设计——假设高维有冗余。

> **在** $D$ **维里能表达的有用信息，其实活在一个** $D/4$ **维的子空间里。把它压到** $D/4$ **维做重活（3×3 conv），再升回** $D$ **维广播**。
> 

**Bottleneck 的核心假设**：

总共 ~70k 乘法/位置 vs 原本的 589k——**约 8× 加速**，精度几乎不损失。

- $1\times1$ conv: $16k \cdot HW$
- $3\times3$ conv: $9 \cdot (D/4)^2 \cdot HW = 9 \cdot 4096 \cdot HW = 37k \cdot HW$
- $1\times1$ conv: $D \cdot (D/4) \cdot HW = 64 \cdot 256 \cdot HW = 16k \cdot HW$

bottleneck 把它改成三步：

如果 $D=256$，$9 D^2 = 589k$，每个位置 589k 次乘法。

$3\times3$ conv 在 $D$ 维 feature 上的计算量是 $propto D^2 cdot 9 cdot HW$。

ResNet bottleneck 的**设计动机是计算成本**：

## 2.2 Bottleneck 的目的：计算效率

**两者维度走向完全相反**。这不是随意的——两者优化的目标根本不同。

所以是 $D to 4D to D$（"倒沙漏形"）。

```
输入: [N, 256]
 ↓ Linear: 256→1024    ← 先升维
 ↓ GELU activation
 ↓ Linear: 1024→256    ← 再压回
输出: [N, 256]
```

**Transformer FFN**：

所以是 $D to D/4 to D/4 to D$（"沙漏形"）。

```
输入: [H, W, 256]
 ↓ 1×1 conv: 256→64    ← 先压缩
 ↓ 3×3 conv: 64→64     ← 在小维度做重活
 ↓ 1×1 conv: 64→256    ← 再升回
输出: [H, W, 256]
```

**CNN Bottleneck（ResNet 的经典残差块）**：

## 2.1 两种结构的形式对比

**你感觉到的差异是真实的，而且很本质。两者服务于完全相反的目的**。

# §2 · FFN 的"先升维再压缩" vs CNN Bottleneck 的"先压缩再升维"

---

ResNet 用加法，DenseNet 用 concat——这两条线的分歧你在阶段 I 里已经追过一遍。FPN 选加法，本质是继承 ResNet 的哲学。

- **Concat** 对应"**保留信息哲学**"——历史信息不被覆盖，下游自己挑
- **加法** 对应"**残差哲学**"——每层只是对当前表征的增量修正

**一个更深的对比**：

实际上 concat 版本也被试过，叫 **PANet (2018)**——在 FPN 之上又加了一条 bottom-up 路径，用了 concat + conv 融合。效果提升有限，而且显著增加计算。工业界最终还是以 FPN 加法为主流，concat 只在少数精度导向的 heavy 模型里出现。

## 1.4 历史证据

**所以加法不是"简单所以快"，是"对齐了语义假设所以共用下游成为可能"**。

FPN 的一大胜利就是**P2-P5 共用一个 detection head（RetinaNet / FCOS 都这样）**——这在 concat 版本下做不到，因为每层 channel 语义分裂。

| 维度 | 加法 | Concat + conv |
| --- | --- | --- |
| 参数量 | 只多 lateral 的 1×1 conv | 多 2× lateral 的 1×1 conv + 融合 conv |
| 语义假设 | 多尺度共享语义空间 | 多尺度独立语义空间 |
| Channel 的意义 | "某个概念"（尺度无关） | "某个概念在某个尺度的版本" |
| 下游一致性 | P2-P5 可以用同一个检测头 | 需要尺度感知的检测头 |

**表格对比**：

FPN 的设计哲学是"**让多尺度变成一个 orthogonal 的维度，而不是 channel 维度里的一个子分区**"。

## 1.3 为什么加法赢了

- **阻碍后续特征解释**：如果第 k 层的 channel c 和第 k+1 层的 channel c 语义分离，你就没法在 P 金字塔上做**一致的特征采样**
- **破坏"多尺度语义一致性"的先验**：concat 把"尺度"变成了"channel 分叉"——下游 conv 可能学出"前 256 维管细节、后 256 维管粗概念"的分裂表征
- **参数量多**：1×1 conv of 512→256 有 131k 参数，每个 P 层都要一个

这更灵活，但也有代价：

> **两个来源的 feature 可能语义不同，不假设它们对齐。把选择权交给下游的 1×1 conv，让它学怎么组合**。
> 

Concat 拼起来相当于说：

## 1.2 Concat + conv 的隐含假设

- 所以"大物体的 P5 response"和"小物体的 P3 response"可以被塞进同一个 channel，只是空间位置不同
- 图像在不同尺度上看到的东西是**同一类语义的不同分辨率版本**

这是一个非常强的归纳偏置。它假设：

> **"多尺度的同一语义在同一维度上"——不同尺度只提供不同的空间精细度，语义本身共享**。
> 

**加法的本质判断**：

这一步 1×1 conv 的作用不是"降维"，而是"**把不同层的 feature 对齐到同一个表征坐标系**"。一旦对齐了，"P5 的第 37 个 channel"和"C4 的第 37 个 channel"语义一致——相加才有意义。

**FPN 的加法成立，是因为它提前做了一步关键操作**——`Lateral(C_k)` 用 1×1 conv 把 $C_k$ 的 channel 数从原本的 [256, 512, 1024, 2048] 全部投影到 256 维的**共享表征空间**。

- 否则加完得到一个"半生不熟的 channel"，下游 conv 无法解释
- 相加之后，每个 channel 的语义必须和加之前相同

$P_k = A + B$ 这个操作**只有在 A 和 B 处于同一表征空间时才合理**。

## 1.1 加法的隐含假设

**两者区别不在于"输出维度一样"，而在于"隐含假设不一样"**。

两个 256-channel 拼成 512-channel，再用一个 $512\to256$ 的 1×1 conv 降维回 256。

$$
P_k = \text{Conv}*{1\times1}\big(\text{Concat}(\text{Lateral}(C_k), \text{Upsample}(P*{k+1}))\big)
$$

**Concat + 1×1 conv 版本（你的候选）**：

两个 256-channel tensor 直接逐元素相加，输出仍是 256-channel。

$$
P_k = \text{Lateral}(C_k) + \text{Upsample}(P_{k+1})
$$

**加法版本（FPN 实际用的）**：

这是个"表面是工程选择，底层是表征假设"的问题。两种做法的数学对比：

# §1 · 为什么 FPN 是加法，不是 concat + 1×1 conv

---

四个都是根子上的问题。一个一个展开。

还有一个关联问题值得挖：**Painter / SegGPT** 这条"in-context 分割"的线，它和 LLM 的 in-context learning 有**严格同构**，是阶段 II 里和提示化并列的关键机制。和 EoMT 合在一起看，它们共同承担了“统一 Mask 架构”组的收官工作：前者提示化，后者去 decoder 化。

## 后续连接

---

**OneFormer 的贡献不在 decoder 层面，在训练协议层面**——它证明架构就绪后，"一份权重"是下一个要攻克的统一化目标。它把"模型能做什么"从"架构支持什么"推进到"权重能同时承载什么"。

- **EoMT = 两者合流**：encoder 吞掉 decoder + query 混进 encoder → decoder 完全消失
- **MaskFormer/Mask2Former 路径**：query 机制 → decoder 是轻量 transformer
- **SegFormer 路径**：encoder 多尺度化 → decoder 可以是 MLP

**两条独立的"薄化"路径最终合流**：

```
                      Decoder        Query                Task         Class
                      复杂度         机制                 条件化       闭/开
FCN (2015)             重            无                   无           闭
Mask R-CNN (2017)      重            RoI-based            无           闭
MaskFormer (2021)      中            通用 N queries       无           闭
SegFormer (2021)       极薄 (MLP)    无 (per-pixel)       无           闭
Mask2Former (2022)     薄 (query)    通用 N queries       无           闭
OneFormer (2023)       薄 (query)    通用 N queries       task token   闭
EoMT (2024)            几乎没有      query 混进 encoder   (可选)       闭
        ↓
阶段 II 出口:
SAM / Grounding DINO / CAT-Seg → query 外生化 + class 开放化
```

到这里，你手里的 6 条文献各自在哪一层做贡献：

# §5 · 四篇合力的架构演进

---

这个残差指向阶段 II 的出口——**开放词汇分割（Grounding DINO / CAT-Seg / ODISE）需要把 class head 从离散 softmax 换成 CLIP text similarity**。和 query-text contrastive loss 已经埋下的伏笔合流——OneFormer 的对比 loss 已经让 query 对齐到文本空间了，下一步只要把这个对齐推到 class head 层面，就是开放词汇。

**OneFormer 做了 task 条件化，但没做 class 条件化**——前者让 query 行为适应任务，后者需要让 class head 适应词汇。

- 没见过"独角兽"，输出不了独角兽 mask
- 它在 COCO 上训，推理时只能输出 COCO 的 80 个 thing + 53 个 stuff 类

OneFormer 做到了**任务统一**，但**类别仍然闭集**：

## 4.9 OneFormer 的残差

这也暗示了**视觉和语言在"任务条件化"机制上没有本质区别**——都是"把任务差异压缩到一个 prompt token 里，让模型条件化地表达不同行为"。这个通用性后来在 SEEM / SegGPT 这些 prompt-anything 分割模型里进一步放大——视觉可以任意 prompt，和语言一样。

**一个模型 + 多任务 prompt + 联合训练 = 一份权重多种行为**。这是 2022-2023 整个 AI 领域的共同趋势。OneFormer 是这个趋势在**稠密视觉任务**上的兑现——比 NLP 的 FLAN (2022) 稍晚，但节奏完全对齐。

- OneFormer: "the task is semantic" / "the task is instance" / "the task is panoptic"
- LLM: "Summarize: ..." / "Translate to French: ..." / "Answer the question: ..."

OneFormer 的机制（task token + 条件化训练）和 LLM 的 instruction tuning **结构上完全一样**：

## 4.8 和 LLM instruction tuning 的深层同构

- 是真正的 **"一个 shared computation 可以处理三种监督信号"**
- 不是每个任务各训一份权重凑 SOTA
- 不是碰巧同架构 work

这三步走完，"三任务是一个任务"这个命题被**完整证明**：

- OneFormer 说 **"甚至可以用同一份权重**"
- Mask2Former 说 **"实际训出来精度也一样"**
- MaskFormer 说 **"范式是一样的"**

每一步都比前一步深一层：

**OneFormer**: 权重层面统一（一份参数 cover 三任务）

**Mask2Former**: 经验层面证成（同架构跑出三任务 SOTA）

**MaskFormer**: 架构层面统一（per-pixel → per-mask）

OneFormer 完成了 Mask2Former 留下的最后一个缺口。

## 4.7 OneFormer 的哲学升级

**一份权重匹配三份权重的性能**——彻底证成"任务本质同一"。

| 数据集 | 任务 | OneFormer | Mask2Former (per-task) |
| --- | --- | --- | --- |
| COCO | panoptic | 57.9 PQ | 57.8 PQ |
| COCO | instance | 50.6 AP | 50.5 AP |
| COCO | semantic | 67.4 mIoU | 67.4 mIoU |

在 COCO 全景、ADE20K 语义、Cityscapes 实例这三个不同数据集上，**同一组训练参数**（只是数据集换）都拿到 SOTA：

## 4.6 OneFormer 的性能

**它本质上是 Mask2Former 的一个"训练协议升级"，而非架构重构**。这证明 Mask2Former 的架构已经 ready for universal——只需要训练协议和条件化机制补齐。

```
Mask2Former 原结构: backbone + pixel decoder + transformer decoder + N queries

OneFormer 改动:
  + Task token (在 transformer decoder 每层参与 cross-attention)
  + Query-text contrastive branch (训练 only)
  + 三任务 GT 派生 (训练数据构造)
```

OneFormer **不重新设计架构**，它直接在 Mask2Former 上加：

## 4.5 架构层面 —— 在 Mask2Former 上做 surgery

这是一个关键的桥接——**OneFormer 的 query 同时是 mask slot 和 semantic anchor**。这个双重角色让 OneFormer 天然和 CLIP 合流，为后面开放词汇铺路。

**效果**：让 query 学到的表征具有**语言可对齐性**——每个 query 不仅仅是 mask slot，还是某种"对齐到文本概念"的 slot。

```
一张图的 GT mask 和类别 → 生成一段任务描述
  例: "a photo with a dog, a car, a tree" + task 信息
  这段文本过 CLIP text encoder → text_embedding

模型输出: N 个 mask embedding + class predictions
  取出预测为有效对象的 query embeddings → pool → image_task_embedding

对比 loss: 拉近 (text_embedding, image_task_embedding)
```

具体：

OneFormer 还加了一个副 loss：**让 query embedding 和任务描述的文本 embedding 对齐**。

## 4.4 Query-Text Contrastive Loss

- 派生是**无信息损失的**——全景 GT 包含全部必要信息
- 全景 GT 是最细粒度的，可以**下采样派生**出其他两种
- 不需要三个 loss
- 不需要三份独立数据集

这个设计的优雅之处：

**一个数据集 + 三种 GT 派生 + task token 条件化**——训练过程中模型在三种 GT 结构间交替学习，**同一份权重被迫同时掌握三种行为**。

```
只需要一份全景标注的数据集
每个训练 batch:
  随机选一个 task ∈ {semantic, instance, panoptic}
  从全景 GT 派生出对应 task 的 GT:
    - semantic: 合并同类 mask
    - instance: 只保留 thing 类的独立 mask
    - panoptic: 原本的全景 GT
  喂给模型：(image, task_token, derived_GT)
```

**训练数据的构造极其重要**。OneFormer 的做法：

## 4.3 训练策略 —— 从全景 GT 派生另外两种

**task token 让一份权重条件化成三种行为模式**。本质上这是"**prompting**"——和 LLM 里"instruction tuning"的思想一样：模型能力本身是通用的，任务差异通过 prompt 注入。

- 输入 "the task is panoptic" → 混合行为
- 输入 "the task is instance" → 100 query 按实例分开
- 输入 "the task is semantic" → 100 query 按类聚集

所以同一份模型，**输入不同 task token，输出不同行为**：

```
训练时:
  当前 task ∈ {"semantic", "instance", "panoptic"}
  文本 prompt: "the task is {task}"
  文本通过 CLIP text encoder → task_embedding ∈ R^D
  这个 task_embedding 被广播加到所有 N 个 query 上（或 concat 作为额外 query）
```

具体做法：

核心创新：**在 query 集合里引入一个"task token"**，明确告诉模型当前要做哪个任务。

## 4.2 OneFormer 的关键机制 —— Task Token

**两种行为相互冲突**——直接 mix 训练，模型会在中间"精神分裂"，两个任务精度都下降。

- 喂实例 GT → query 学"按实例分开"
- 喂语义 GT → query 学"按类聚集"

训练时 Hungarian matching 的 GT 结构决定 query 学到的行为：

- 全景 GT：混合（things 按实例，stuff 按类）
- 实例 GT：同类不同实例分开（狗 A、狗 B 是两个 mask）
- 语义 GT：所有同类像素合并成一个 mask（狗 A + 狗 B = 一个"狗"mask）

问题：**三个任务的 GT 结构冲突**：

直觉做法：把 COCO 的语义/实例/全景三份 GT 合起来，交替训练。

## 4.1 为什么不能直接在三个数据集上联合训练

OneFormer 直接挑战后者：**一次训练、一份权重、三个任务同时 SOTA**。

**"一种架构" ≠ "一份权重"**。架构能 cover 三个任务是一回事，但一份权重能同时 cover 三个任务**是另一回事**——前者是便于复用代码，后者是更深的模型统一。

**Mask2Former 训一个全景模型时，这个模型只擅长全景；要语义，得在语义数据集上再训一份；要实例，得再训一份**。

Mask2Former 已经是"universal architecture"——同一套代码，可以跑语义/实例/全景。但有个事实被忽略：

# §4 · OneFormer —— 清算"每任务一份权重"

---

**两者合流是 EoMT (2024)**——EoMT 证明 Mask2Former 的专用 decoder 也可以去掉，segment query 直接混进 ViT 的 token 序列。**SegFormer 的"encoder 吃掉 decoder"哲学在 EoMT 时彻底胜利**——encoder 把 backbone 和 decoder 都吃掉了，只剩 query 作为外置 token。

- Mask2Former：query + cross-attention → universal 分割
- SegFormer：encoder 升级 + decoder 极简 → 语义分割的极致

这个残差被 Mask2Former 填——Mask2Former 把 query 机制加回来，同时保留 decoder 轻量化。**SegFormer 和 Mask2Former 是两条不同的收敛路径**：

SegFormer 只做语义分割——它没有 object query 机制，所以**做不了实例分割/全景分割**。它沿的是 FCN 的衣钵，只是 encoder 升级了。

## 3.6 SegFormer 的残差

SegFormer 用**36% 参数量拿 97% 精度**——decoder 砍掉那么多，代价很小。

- SegFormer-B5: 84M params, 51.8 mIoU
- Swin-L UperNet: 234M params, 53.5 mIoU (AD20K)

**关键对比**：

同等参数下比 Swin + UperNet 高 1-2 个 mIoU 点，且**推理速度快 1.5-3 倍**（decoder 超薄，延迟极低）。

- SegFormer-B5 (84M params): 51.8
- SegFormer-B0 (3.8M params): 37.4

ADE20K mIoU：

## 3.5 SegFormer 的性能

这条规律在 LLM 里体现为"LoRA / 线性 probing / adapter"；在 VLM 里体现为"projector = 简单 MLP"（我们刚讲过）；在分割里体现为"MLP decoder"——**它们都是同一种哲学的不同实现**。

> **表征学习时代，模型的"任务特异性"应该尽量往后压——backbone 学通用表征，task head 越薄越好**。
> 

这个哲学转移是**深层的**。它对应的更大规律：

> 只要 backbone 本身是多尺度的 + 有全局 attention，**decoder 就是一个 shallow "读出头"**。分割的"复杂度"应该摊到 backbone 里，而不是堆在 decoder 上。
> 

SegFormer 之后：

> Backbone 提供特征，**decoder 负责做分割的所有重活**（多尺度融合、空间聚合、上采样、分类）。Decoder 是分割的核心。
> 

在 SegFormer 之前，分割模型的主流心智：

**它是第一个明确说"decoder 可以很薄"的分割工作**。

## 3.4 SegFormer 的哲学判断

**Decoder 的任务被彻底降级**：只需要做"**把四个尺度的 feature 混合 + 每个像素做一次分类**"这两件事。Linear 就够。

- 位置编码——Mix-FFN 的 depthwise conv 已经处理了
- 空间上下文聚合——encoder 的 self-attention 已经做了全局 mixing
- 多尺度归纳偏置——encoder 的 4 stage 已经有了

因为重活已经被 encoder 做完了：

**为什么这么简单的 decoder 够用？**

**没有 conv 3×3，没有 FPN lateral add，没有 ASPP，没有 deformable attention——什么复杂结构都没有**。

**总计：4 个 per-stage Linear + 1 个融合 Linear + 1 个分类 Linear = 6 个 Linear 层，全部都是 1×1 等效操作**。

```
四个 stage 输出:
  F1: [1/4,  C1]
  F2: [1/8,  C2]
  F3: [1/16, C3]
  F4: [1/32, C4]
      ↓ 每个过一个 Linear 投影到统一 channel 数 C
  F1': [1/4, C]
  F2': [1/8, C]
  F3': [1/16, C]
  F4': [1/32, C]
      ↓ 全部双线性上采样到 1/4
  F1': [1/4, C]
  F2': [1/4, C] (from 1/8 upsampled)
  F3': [1/4, C]
  F4': [1/4, C]
      ↓ concat → [1/4, 4C]
      ↓ Linear: 4C → C
      ↓ Linear: C → num_classes
  输出: [1/4, num_classes]
      ↓ 双线性上采样到原分辨率
```

这是 SegFormer 最激进的部分。Decoder 只有 **4 个 MLP + 一个 concat + 一个 classification MLP**：

## 3.3 SegFormer 的 decoder —— 只有 MLP

**这个选择超前且深远**。后来的 RoPE（relative positional encoding，LLM 里用的那个）、Swin v2 的 log-CPB、乃至 ViT 后续改进都是朝"相对位置取代绝对位置"的方向走。SegFormer 是视觉 Transformer 里第一批明确抛弃绝对 PE 的工作。

- 分割天然是"**空间相对关系**"的任务——相对位置比绝对位置更本质
- 相对位置（conv 提供的）在任何分辨率下都保持一致——**邻居就是邻居**
- 绝对 PE 在换分辨率时失效（训练 224，推理 1024 就错位）

**相对位置 vs 绝对位置**：

**关键洞察**：卷积本身就编码了**相对位置信息**——相邻 token 通过 3×3 conv 会彼此影响，模型从而知道"哪些 token 是邻居"。而 PE 是显式编码"每个 token 的绝对位置"。

在 FFN 里插入一个 **3×3 depthwise conv**。为什么这样能替代 PE？

```
Mix-FFN: token → Linear → 3×3 depthwise conv → GELU → Linear → 加到残差
```

ViT 需要显式的 position embedding，SegFormer **完全去掉**了 PE。代替方案：

### 改动 4：用 Conv 替代 Positional Encoding

这是 attention 里"非对称稀疏化"的一个典型思路——**Q 维度保精度，K/V 维度保信息密度**。

- 类比：你要问"哪个餐厅最近"，精度要求在于"问这个问题的地点"（Q），而不在于"全市的餐厅索引"（K/V）——后者可以被压缩成 coarse lookup
- K/V 代表"有什么信息可查"——粗粒度的信息对"我要看什么"已经足够
- Q 代表"每个位置要查询什么"——查询的细粒度决定了输出精度，必须保留

**为什么 K/V 可以下采样而 Q 不行？**

**这个做法和 PVT (Pyramid Vision Transformer) 几乎一样**——PVT 是第一个提出 sequence reduction 的，SegFormer 借用了它。

复杂度从 $O(N^2 D)$ 降到 $O(N^2 D / R^2)$。早期 stage 用 $R=8$，晚期 stage 用 $R=1$——越深分辨率越低，就不需要 reduction 了。

```
Q stays: shape [N, D]
K, V → reshape to [H, W, D] → conv with stride R → [N/R², D]

Attention: softmax(Q K^T / √D) V
           shape: [N, D] × [D, N/R²] → [N, N/R²] × [N/R², D] → [N, D]
```

SegFormer 的做法：**K 和 V 先做空间下采样**。具体：

标准 self-attention：$Q, K, V in mathbb{R}^{N times D}$，attention 复杂度 $O(N^2 D)$。

### 改动 3：Efficient Self-Attention (Sequence Reduction)

两者本质都是"在高分辨率上稀疏化 attention"，但**Swin 的稀疏是几何的（按空间窗口），SegFormer 的稀疏是表征的（压缩 key/value 数量）**。你可以把它和 Deformable DETR / Mask2Former 的 masked attention 放一起看：深度学习遇到"attention 太贵"时永远在想办法稀疏化，但稀疏化的依据是几何还是表征，是个持续的设计分歧。

- SegFormer 用 **sequence reduction**（见改动 3）——不分 window，而是对 key/value 做下采样
- Swin 也是 4 stage hierarchical，但用的是 **window attention** 限制计算（每个 window 内全连接）

和 Swin 的对比：

**每个 stage 自带多尺度——4 层 feature 直接对应 CNN 的 C2/C3/C4/C5**。这就是"多尺度归纳偏置被 Transformer 分层结构自然吸收"的意思——**Transformer 不再是单尺度，它变成了和 ResNet 一样的多尺度 backbone**。

```
Stage 1: patch size 7, stride 4  → 1/4  分辨率, 32 或 64 channel
Stage 2: patch size 3, stride 2  → 1/8  分辨率, 64 或 128 channel
Stage 3: patch size 3, stride 2  → 1/16 分辨率, 160 或 320 channel
Stage 4: patch size 3, stride 2  → 1/32 分辨率, 256 或 512 channel
```

MiT 分 4 个 stage，每个 stage 做一次 patch merging + 一组 transformer block：

### 改动 2：4 层 hierarchical encoder

这个改动本质上是**把 CNN 里"conv 的滑动窗口重叠"思想搬回 patch 划分**。ViT 当初故意放弃重叠是为了"**完全抛弃卷积的局部先验**"——而 SegFormer 重新拾回它，因为分割需要这个先验。

代价：**token 数略增多，但每个 token 的感受野也增大**——整体是净赚。

**为什么重叠？** 不重叠的划分在 patch 边界上有**硬切割**——横跨 patch 边界的对象结构被砍断，分割的精度就差。重叠让 patch 之间有信息流——**相邻 patch 共享部分像素，天然保留空间连续性**。

```
ViT:       16×16 patch, stride 16  → 相邻 patch 完全不重叠
SegFormer: 7×7  patch, stride 4    → 相邻 patch 有 3-pixel 重叠
```

**ViT 用不重叠 patch 划分**（stride = patch size）。SegFormer 改成**重叠**：

### 改动 1：Overlapping Patch Merging

MiT 的设计是 ViT 和 Swin 之间的一种折中。四个关键改动：

## 3.2 SegFormer 的 encoder —— MiT (Mix Transformer)

SegFormer 的回答：**把 encoder 变成多尺度（Swin 已经这样做了，SegFormer 做得更彻底），然后把 decoder 砍到只剩 MLP**。

- **decoder 参数量常常比 backbone 还大**——对"decoder 是多余的"这个怀疑没有被直面
- UPerNet 的 PSP pooling + FPN 融合
- DeepLab 的 ASPP + 多层 upsample conv

**(4) Decoder 传统上很重**

- 推理时换到 1024×1024，PE 就对不上——要 interpolate PE，效果打折
- 学的时候分辨率是 224×224

**(3) ViT 的 positional encoding 固定**

- Patch 8 时 token 数 $approx 4096$，复杂度 $1.6times10^7$——训练很慢
- Patch 16 时 token 数 $approx 1024$，self-attention 复杂度 $O(N^2)=10^6$ 还可以
- 分割要 512×512 甚至 1024×1024 输入

**(2) 全局 self-attention 在高分辨率下爆炸**

- 单尺度的 ViT 给分割留了个烂摊子：decoder 需要自己造多尺度
- 分割天生要多尺度——大物体要粗，小物体要细
- ViT 一开始就 patch 化（16×16 patch → 14×14 token），之后**所有层的 token 数都不变**

**(1) ViT 是单尺度的**

ViT (2020) 出来后很快有人把它搬去分割，但效果很尴尬。问题：

## 3.1 动机 —— ViT 用到分割上水土不服

SegFormer 出在 MaskFormer 同年（2021 NeurIPS），作者 Xie Enze 等（NVIDIA + HKUST + Nanjing Univ）。它和 MaskFormer 不是竞争关系——**它走的是另一条让 decoder 变薄的路线**，两者的思路合流到 EoMT 时就汇成一条江。

# §3 · SegFormer —— Decoder 坍缩的第一个标志

---

继续按同样密度打穿。这两篇都属于"架构成熟之后的清算型工作"——一个清算稠密 decoder，一个清算"每任务一份权重"的残余。

还有一个关联问题值得挖：**Painter / SegGPT** 这条"in-context 分割"的线，它和 LLM 的 in-context learning 有**严格同构**，是阶段 II 里和提示化并列的关键机制。和 EoMT 合在一起看，它们共同承担了“统一 Mask 架构”组的收官工作：前者提示化，后者去 decoder 化。

## 后续连接

---

**OneFormer 的贡献不在 decoder 层面，在训练协议层面**——它证明架构就绪后，"一份权重"是下一个要攻克的统一化目标。它把"模型能做什么"从"架构支持什么"推进到"权重能同时承载什么"。

- **EoMT = 两者合流**：encoder 吞掉 decoder + query 混进 encoder → decoder 完全消失
- **MaskFormer/Mask2Former 路径**：query 机制 → decoder 是轻量 transformer
- **SegFormer 路径**：encoder 多尺度化 → decoder 可以是 MLP

**两条独立的"薄化"路径最终合流**：

```
                      Decoder        Query                Task         Class
                      复杂度         机制                 条件化       闭/开
FCN (2015)             重            无                   无           闭
Mask R-CNN (2017)      重            RoI-based            无           闭
MaskFormer (2021)      中            通用 N queries       无           闭
SegFormer (2021)       极薄 (MLP)    无 (per-pixel)       无           闭
Mask2Former (2022)     薄 (query)    通用 N queries       无           闭
OneFormer (2023)       薄 (query)    通用 N queries       task token   闭
EoMT (2024)            几乎没有      query 混进 encoder   (可选)       闭
        ↓
阶段 II 出口:
SAM / Grounding DINO / CAT-Seg → query 外生化 + class 开放化
```

到这里，你手里的 6 条文献各自在哪一层做贡献：

# §5 · 四篇合力的架构演进

---

这个残差指向阶段 II 的出口——**开放词汇分割（Grounding DINO / CAT-Seg / ODISE）需要把 class head 从离散 softmax 换成 CLIP text similarity**。和 query-text contrastive loss 已经埋下的伏笔合流——OneFormer 的对比 loss 已经让 query 对齐到文本空间了，下一步只要把这个对齐推到 class head 层面，就是开放词汇。

**OneFormer 做了 task 条件化，但没做 class 条件化**——前者让 query 行为适应任务，后者需要让 class head 适应词汇。

- 没见过"独角兽"，输出不了独角兽 mask
- 它在 COCO 上训，推理时只能输出 COCO 的 80 个 thing + 53 个 stuff 类

OneFormer 做到了**任务统一**，但**类别仍然闭集**：

## 4.9 OneFormer 的残差

这也暗示了**视觉和语言在"任务条件化"机制上没有本质区别**——都是"把任务差异压缩到一个 prompt token 里，让模型条件化地表达不同行为"。这个通用性后来在 SEEM / SegGPT 这些 prompt-anything 分割模型里进一步放大——视觉可以任意 prompt，和语言一样。

**一个模型 + 多任务 prompt + 联合训练 = 一份权重多种行为**。这是 2022-2023 整个 AI 领域的共同趋势。OneFormer 是这个趋势在**稠密视觉任务**上的兑现——比 NLP 的 FLAN (2022) 稍晚，但节奏完全对齐。

- OneFormer: "the task is semantic" / "the task is instance" / "the task is panoptic"
- LLM: "Summarize: ..." / "Translate to French: ..." / "Answer the question: ..."

OneFormer 的机制（task token + 条件化训练）和 LLM 的 instruction tuning **结构上完全一样**：

## 4.8 和 LLM instruction tuning 的深层同构

- 是真正的 **"一个 shared computation 可以处理三种监督信号"**
- 不是每个任务各训一份权重凑 SOTA
- 不是碰巧同架构 work

这三步走完，"三任务是一个任务"这个命题被**完整证明**：

- OneFormer 说 **"甚至可以用同一份权重**"
- Mask2Former 说 **"实际训出来精度也一样"**
- MaskFormer 说 **"范式是一样的"**

每一步都比前一步深一层：

**OneFormer**: 权重层面统一（一份参数 cover 三任务）

**Mask2Former**: 经验层面证成（同架构跑出三任务 SOTA）

**MaskFormer**: 架构层面统一（per-pixel → per-mask）

OneFormer 完成了 Mask2Former 留下的最后一个缺口。

## 4.7 OneFormer 的哲学升级

**一份权重匹配三份权重的性能**——彻底证成"任务本质同一"。

| 数据集 | 任务 | OneFormer | Mask2Former (per-task) |
| --- | --- | --- | --- |
| COCO | panoptic | 57.9 PQ | 57.8 PQ |
| COCO | instance | 50.6 AP | 50.5 AP |
| COCO | semantic | 67.4 mIoU | 67.4 mIoU |

在 COCO 全景、ADE20K 语义、Cityscapes 实例这三个不同数据集上，**同一组训练参数**（只是数据集换）都拿到 SOTA：

## 4.6 OneFormer 的性能

**它本质上是 Mask2Former 的一个"训练协议升级"，而非架构重构**。这证明 Mask2Former 的架构已经 ready for universal——只需要训练协议和条件化机制补齐。

```
Mask2Former 原结构: backbone + pixel decoder + transformer decoder + N queries

OneFormer 改动:
  + Task token (在 transformer decoder 每层参与 cross-attention)
  + Query-text contrastive branch (训练 only)
  + 三任务 GT 派生 (训练数据构造)
```

OneFormer **不重新设计架构**，它直接在 Mask2Former 上加：

## 4.5 架构层面 —— 在 Mask2Former 上做 surgery

这是一个关键的桥接——**OneFormer 的 query 同时是 mask slot 和 semantic anchor**。这个双重角色让 OneFormer 天然和 CLIP 合流，为后面开放词汇铺路。

**效果**：让 query 学到的表征具有**语言可对齐性**——每个 query 不仅仅是 mask slot，还是某种"对齐到文本概念"的 slot。

```
一张图的 GT mask 和类别 → 生成一段任务描述
  例: "a photo with a dog, a car, a tree" + task 信息
  这段文本过 CLIP text encoder → text_embedding

模型输出: N 个 mask embedding + class predictions
  取出预测为有效对象的 query embeddings → pool → image_task_embedding

对比 loss: 拉近 (text_embedding, image_task_embedding)
```

具体：

OneFormer 还加了一个副 loss：**让 query embedding 和任务描述的文本 embedding 对齐**。

## 4.4 Query-Text Contrastive Loss

- 派生是**无信息损失的**——全景 GT 包含全部必要信息
- 全景 GT 是最细粒度的，可以**下采样派生**出其他两种
- 不需要三个 loss
- 不需要三份独立数据集

这个设计的优雅之处：

**一个数据集 + 三种 GT 派生 + task token 条件化**——训练过程中模型在三种 GT 结构间交替学习，**同一份权重被迫同时掌握三种行为**。

```
只需要一份全景标注的数据集
每个训练 batch:
  随机选一个 task ∈ {semantic, instance, panoptic}
  从全景 GT 派生出对应 task 的 GT:
    - semantic: 合并同类 mask
    - instance: 只保留 thing 类的独立 mask
    - panoptic: 原本的全景 GT
  喂给模型：(image, task_token, derived_GT)
```

**训练数据的构造极其重要**。OneFormer 的做法：

## 4.3 训练策略 —— 从全景 GT 派生另外两种

**task token 让一份权重条件化成三种行为模式**。本质上这是"**prompting**"——和 LLM 里"instruction tuning"的思想一样：模型能力本身是通用的，任务差异通过 prompt 注入。

- 输入 "the task is panoptic" → 混合行为
- 输入 "the task is instance" → 100 query 按实例分开
- 输入 "the task is semantic" → 100 query 按类聚集

所以同一份模型，**输入不同 task token，输出不同行为**：

```
训练时:
  当前 task ∈ {"semantic", "instance", "panoptic"}
  文本 prompt: "the task is {task}"
  文本通过 CLIP text encoder → task_embedding ∈ R^D
  这个 task_embedding 被广播加到所有 N 个 query 上（或 concat 作为额外 query）
```

具体做法：

核心创新：**在 query 集合里引入一个"task token"**，明确告诉模型当前要做哪个任务。

## 4.2 OneFormer 的关键机制 —— Task Token

**两种行为相互冲突**——直接 mix 训练，模型会在中间"精神分裂"，两个任务精度都下降。

- 喂实例 GT → query 学"按实例分开"
- 喂语义 GT → query 学"按类聚集"

训练时 Hungarian matching 的 GT 结构决定 query 学到的行为：

- 全景 GT：混合（things 按实例，stuff 按类）
- 实例 GT：同类不同实例分开（狗 A、狗 B 是两个 mask）
- 语义 GT：所有同类像素合并成一个 mask（狗 A + 狗 B = 一个"狗"mask）

问题：**三个任务的 GT 结构冲突**：

直觉做法：把 COCO 的语义/实例/全景三份 GT 合起来，交替训练。

## 4.1 为什么不能直接在三个数据集上联合训练

OneFormer 直接挑战后者：**一次训练、一份权重、三个任务同时 SOTA**。

**"一种架构" ≠ "一份权重"**。架构能 cover 三个任务是一回事，但一份权重能同时 cover 三个任务**是另一回事**——前者是便于复用代码，后者是更深的模型统一。

**Mask2Former 训一个全景模型时，这个模型只擅长全景；要语义，得在语义数据集上再训一份；要实例，得再训一份**。

Mask2Former 已经是"universal architecture"——同一套代码，可以跑语义/实例/全景。但有个事实被忽略：

# §4 · OneFormer —— 清算"每任务一份权重"

---

**两者合流是 EoMT (2024)**——EoMT 证明 Mask2Former 的专用 decoder 也可以去掉，segment query 直接混进 ViT 的 token 序列。**SegFormer 的"encoder 吃掉 decoder"哲学在 EoMT 时彻底胜利**——encoder 把 backbone 和 decoder 都吃掉了，只剩 query 作为外置 token。

- Mask2Former：query + cross-attention → universal 分割
- SegFormer：encoder 升级 + decoder 极简 → 语义分割的极致

这个残差被 Mask2Former 填——Mask2Former 把 query 机制加回来，同时保留 decoder 轻量化。**SegFormer 和 Mask2Former 是两条不同的收敛路径**：

SegFormer 只做语义分割——它没有 object query 机制，所以**做不了实例分割/全景分割**。它沿的是 FCN 的衣钵，只是 encoder 升级了。

## 3.6 SegFormer 的残差

SegFormer 用**36% 参数量拿 97% 精度**——decoder 砍掉那么多，代价很小。

- SegFormer-B5: 84M params, 51.8 mIoU
- Swin-L UperNet: 234M params, 53.5 mIoU (AD20K)

**关键对比**：

同等参数下比 Swin + UperNet 高 1-2 个 mIoU 点，且**推理速度快 1.5-3 倍**（decoder 超薄，延迟极低）。

- SegFormer-B5 (84M params): 51.8
- SegFormer-B0 (3.8M params): 37.4

ADE20K mIoU：

## 3.5 SegFormer 的性能

这条规律在 LLM 里体现为"LoRA / 线性 probing / adapter"；在 VLM 里体现为"projector = 简单 MLP"（我们刚讲过）；在分割里体现为"MLP decoder"——**它们都是同一种哲学的不同实现**。

> **表征学习时代，模型的"任务特异性"应该尽量往后压——backbone 学通用表征，task head 越薄越好**。
> 

这个哲学转移是**深层的**。它对应的更大规律：

> 只要 backbone 本身是多尺度的 + 有全局 attention，**decoder 就是一个 shallow "读出头"**。分割的"复杂度"应该摊到 backbone 里，而不是堆在 decoder 上。
> 

SegFormer 之后：

> Backbone 提供特征，**decoder 负责做分割的所有重活**（多尺度融合、空间聚合、上采样、分类）。Decoder 是分割的核心。
> 

在 SegFormer 之前，分割模型的主流心智：

**它是第一个明确说"decoder 可以很薄"的分割工作**。

## 3.4 SegFormer 的哲学判断

**Decoder 的任务被彻底降级**：只需要做"**把四个尺度的 feature 混合 + 每个像素做一次分类**"这两件事。Linear 就够。

- 位置编码——Mix-FFN 的 depthwise conv 已经处理了
- 空间上下文聚合——encoder 的 self-attention 已经做了全局 mixing
- 多尺度归纳偏置——encoder 的 4 stage 已经有了

因为重活已经被 encoder 做完了：

**为什么这么简单的 decoder 够用？**

**没有 conv 3×3，没有 FPN lateral add，没有 ASPP，没有 deformable attention——什么复杂结构都没有**。

**总计：4 个 per-stage Linear + 1 个融合 Linear + 1 个分类 Linear = 6 个 Linear 层，全部都是 1×1 等效操作**。

```
四个 stage 输出:
  F1: [1/4,  C1]
  F2: [1/8,  C2]
  F3: [1/16, C3]
  F4: [1/32, C4]
      ↓ 每个过一个 Linear 投影到统一 channel 数 C
  F1': [1/4, C]
  F2': [1/8, C]
  F3': [1/16, C]
  F4': [1/32, C]
      ↓ 全部双线性上采样到 1/4
  F1': [1/4, C]
  F2': [1/4, C] (from 1/8 upsampled)
  F3': [1/4, C]
  F4': [1/4, C]
      ↓ concat → [1/4, 4C]
      ↓ Linear: 4C → C
      ↓ Linear: C → num_classes
  输出: [1/4, num_classes]
      ↓ 双线性上采样到原分辨率
```

这是 SegFormer 最激进的部分。Decoder 只有 **4 个 MLP + 一个 concat + 一个 classification MLP**：

## 3.3 SegFormer 的 decoder —— 只有 MLP

**这个选择超前且深远**。后来的 RoPE（relative positional encoding，LLM 里用的那个）、Swin v2 的 log-CPB、乃至 ViT 后续改进都是朝"相对位置取代绝对位置"的方向走。SegFormer 是视觉 Transformer 里第一批明确抛弃绝对 PE 的工作。

- 分割天然是"**空间相对关系**"的任务——相对位置比绝对位置更本质
- 相对位置（conv 提供的）在任何分辨率下都保持一致——**邻居就是邻居**
- 绝对 PE 在换分辨率时失效（训练 224，推理 1024 就错位）

**相对位置 vs 绝对位置**：

**关键洞察**：卷积本身就编码了**相对位置信息**——相邻 token 通过 3×3 conv 会彼此影响，模型从而知道"哪些 token 是邻居"。而 PE 是显式编码"每个 token 的绝对位置"。

在 FFN 里插入一个 **3×3 depthwise conv**。为什么这样能替代 PE？

```
Mix-FFN: token → Linear → 3×3 depthwise conv → GELU → Linear → 加到残差
```

ViT 需要显式的 position embedding，SegFormer **完全去掉**了 PE。代替方案：

### 改动 4：用 Conv 替代 Positional Encoding

这是 attention 里"非对称稀疏化"的一个典型思路——**Q 维度保精度，K/V 维度保信息密度**。

- 类比：你要问"哪个餐厅最近"，精度要求在于"问这个问题的地点"（Q），而不在于"全市的餐厅索引"（K/V）——后者可以被压缩成 coarse lookup
- K/V 代表"有什么信息可查"——粗粒度的信息对"我要看什么"已经足够
- Q 代表"每个位置要查询什么"——查询的细粒度决定了输出精度，必须保留

**为什么 K/V 可以下采样而 Q 不行？**

**这个做法和 PVT (Pyramid Vision Transformer) 几乎一样**——PVT 是第一个提出 sequence reduction 的，SegFormer 借用了它。

复杂度从 $O(N^2 D)$ 降到 $O(N^2 D / R^2)$。早期 stage 用 $R=8$，晚期 stage 用 $R=1$——越深分辨率越低，就不需要 reduction 了。

```
Q stays: shape [N, D]
K, V → reshape to [H, W, D] → conv with stride R → [N/R², D]

Attention: softmax(Q K^T / √D) V
           shape: [N, D] × [D, N/R²] → [N, N/R²] × [N/R², D] → [N, D]
```

SegFormer 的做法：**K 和 V 先做空间下采样**。具体：

标准 self-attention：$Q, K, V in mathbb{R}^{N times D}$，attention 复杂度 $O(N^2 D)$。

### 改动 3：Efficient Self-Attention (Sequence Reduction)

两者本质都是"在高分辨率上稀疏化 attention"，但**Swin 的稀疏是几何的（按空间窗口），SegFormer 的稀疏是表征的（压缩 key/value 数量）**。你可以把它和 Deformable DETR / Mask2Former 的 masked attention 放一起看：深度学习遇到"attention 太贵"时永远在想办法稀疏化，但稀疏化的依据是几何还是表征，是个持续的设计分歧。

- SegFormer 用 **sequence reduction**（见改动 3）——不分 window，而是对 key/value 做下采样
- Swin 也是 4 stage hierarchical，但用的是 **window attention** 限制计算（每个 window 内全连接）

和 Swin 的对比：

**每个 stage 自带多尺度——4 层 feature 直接对应 CNN 的 C2/C3/C4/C5**。这就是"多尺度归纳偏置被 Transformer 分层结构自然吸收"的意思——**Transformer 不再是单尺度，它变成了和 ResNet 一样的多尺度 backbone**。

```
Stage 1: patch size 7, stride 4  → 1/4  分辨率, 32 或 64 channel
Stage 2: patch size 3, stride 2  → 1/8  分辨率, 64 或 128 channel
Stage 3: patch size 3, stride 2  → 1/16 分辨率, 160 或 320 channel
Stage 4: patch size 3, stride 2  → 1/32 分辨率, 256 或 512 channel
```

MiT 分 4 个 stage，每个 stage 做一次 patch merging + 一组 transformer block：

### 改动 2：4 层 hierarchical encoder

这个改动本质上是**把 CNN 里"conv 的滑动窗口重叠"思想搬回 patch 划分**。ViT 当初故意放弃重叠是为了"**完全抛弃卷积的局部先验**"——而 SegFormer 重新拾回它，因为分割需要这个先验。

代价：**token 数略增多，但每个 token 的感受野也增大**——整体是净赚。

**为什么重叠？** 不重叠的划分在 patch 边界上有**硬切割**——横跨 patch 边界的对象结构被砍断，分割的精度就差。重叠让 patch 之间有信息流——**相邻 patch 共享部分像素，天然保留空间连续性**。

```
ViT:       16×16 patch, stride 16  → 相邻 patch 完全不重叠
SegFormer: 7×7  patch, stride 4    → 相邻 patch 有 3-pixel 重叠
```

**ViT 用不重叠 patch 划分**（stride = patch size）。SegFormer 改成**重叠**：

### 改动 1：Overlapping Patch Merging

MiT 的设计是 ViT 和 Swin 之间的一种折中。四个关键改动：

## 3.2 SegFormer 的 encoder —— MiT (Mix Transformer)

SegFormer 的回答：**把 encoder 变成多尺度（Swin 已经这样做了，SegFormer 做得更彻底），然后把 decoder 砍到只剩 MLP**。

- **decoder 参数量常常比 backbone 还大**——对"decoder 是多余的"这个怀疑没有被直面
- UPerNet 的 PSP pooling + FPN 融合
- DeepLab 的 ASPP + 多层 upsample conv

**(4) Decoder 传统上很重**

- 推理时换到 1024×1024，PE 就对不上——要 interpolate PE，效果打折
- 学的时候分辨率是 224×224

**(3) ViT 的 positional encoding 固定**

- Patch 8 时 token 数 $approx 4096$，复杂度 $1.6times10^7$——训练很慢
- Patch 16 时 token 数 $approx 1024$，self-attention 复杂度 $O(N^2)=10^6$ 还可以
- 分割要 512×512 甚至 1024×1024 输入

**(2) 全局 self-attention 在高分辨率下爆炸**

- 单尺度的 ViT 给分割留了个烂摊子：decoder 需要自己造多尺度
- 分割天生要多尺度——大物体要粗，小物体要细
- ViT 一开始就 patch 化（16×16 patch → 14×14 token），之后**所有层的 token 数都不变**

**(1) ViT 是单尺度的**

ViT (2020) 出来后很快有人把它搬去分割，但效果很尴尬。问题：

## 3.1 动机 —— ViT 用到分割上水土不服

SegFormer 出在 MaskFormer 同年（2021 NeurIPS），作者 Xie Enze 等（NVIDIA + HKUST + Nanjing Univ）。它和 MaskFormer 不是竞争关系——**它走的是另一条让 decoder 变薄的路线**，两者的思路合流到 EoMT 时就汇成一条江。

# §3 · SegFormer —— Decoder 坍缩的第一个标志

---
