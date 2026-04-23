# 接下来

下一个核心问题是 Hungarian matching 的一对一绑定机制（这个是 DETR 系的另一条腿，和 query、cross-attention 同样重要但你还没系统追过）。或者继续深挖点积在别的场景里的变体（比如为什么 QK^T 要除以 $sqrt{d}$、为什么有 multi-head）。

你想先进哪一条？还是先把现在的展开整合进某个页面再继续？

## 3 · SegFormer —— *Simple and Efficient Design for Semantic Segmentation with Transformers* (Xie 等, NeurIPS 2021)

**共形贡献**：纯 ViT backbone + 纯 MLP decoder——证明「多尺度归纳偏置」可以被 Transformer 的分层结构自然吸收。稠密任务的 decoder 开始变薄。

🔗 [https://arxiv.org/abs/2105.15203](https://arxiv.org/abs/2105.15203)

## 4 · OneFormer —— *One Transformer to Rule Universal Image Segmentation* (Jain, Li, Chiu, Hassani, Orlov, Shi, CVPR 2023)

**共形贡献**：一次训练、一份权重，同时胜任语义 / 实例 / 全景——训练时引入 task token 告诉模型当前任务类型。「一个模型 vs 三组模型」的彻底清算。

🔗 [https://arxiv.org/abs/2211.06220](https://arxiv.org/abs/2211.06220)

先纠个小事：EoMT 实际上是 **CVPR 2025 Highlight**（arXiv 2503.19108 是 2025 年 3 月），不是 ECCV 2024。你之前条目里写错了年份/会议——后面你若整合进页面可以顺手改掉。

下面按同样密度打穿。

---

# §5 · Painter / SegGPT —— In-context learning 首次登陆稠密预测

作者：Wang Xinlong 等（BAAI 智源）。Painter 是 CVPR 2023，SegGPT 是 ICCV 2023——**同一组作者半年内连续两篇**，思路一脉相承，SegGPT 是 Painter 的分割特化版。

## 5.1 问题背景 —— 为什么分割"差一口气"

到 2022 年底，分割这件事已经走到一个尴尬的点：

- Mask2Former：同架构跑三任务——但每个数据集还要重新训练
- OneFormer：一份权重跑三任务——但类别闭集
- SAM 还没出来

**核心缺口**：

> 训练一次的模型，能不能不需要 fine-tuning，就直接适应新的分割任务？（新类别、新 domain、新输出格式）
> 

这个需求在 NLP 已经被解决：**GPT-3 / ChatGPT 的 in-context learning**——给几个例子在 prompt 里，模型直接模仿。

**视觉能不能做到同样的事？**

Painter / SegGPT 的回答：**可以，而且机制惊人地简单**。

## 5.2 Painter 的设定 —— 把所有稠密任务改成"图像修复"

Painter 的核心把戏：**把所有稠密视觉任务都重新表达成"图像到图像的翻译"**：

```
输入: [Example_image | Example_output | Query_image | (空白)]
      这是一个 2×2 拼图
输出: [Example_image | Example_output | Query_image | Predicted_output]
      只需要填补最后一格
```

具体做法：

- 拿一张示例图像 + 它的 output（分割 mask、depth map、keypoint heatmap 等）
- 拿一张 query 图像 + 一块**空白**区域
- 四张图拼成 2×2 网格
- 用一个 **MAE-style masked autoencoder** 模型去"恢复"空白那格
- 空白那格的恢复结果 = query 图像的预测输出

**所有任务用同一种表达**：

- 语义分割？output 就是一张彩色 mask 图
- 深度估计？output 就是一张灰度 depth map
- 关键点检测？output 就是一张 heatmap
- 全景分割？output 就是一张实例着色图

Painter 把不同的任务统一成"**视觉输出都是图像**"——这是一个**超级抽象的统一**。

## 5.3 这个做法的本体论意义

Painter 做了一件比它看起来更深的事：**它把"任务"从架构里彻底抽走了**。

看它的架构：

- 就是一个 ViT（具体用 ViT-L）
- MAE 式训练目标（重建被 mask 的 patch）
- 没有 task head，没有 query，没有 class head——**什么特殊结构都没有**

**"要做什么任务"这件事，完全由 in-context 的示例决定**。模型推理时不知道"这是分割还是深度"，它只知道"我要补全这一格，要让它和左上的 example_image→example_output 的映射关系保持一致"。

**这是 LLM 的 instruction following 思想的视觉版**：

- LLM: "Translate 'hello' to French: 'bonjour'. Translate 'goodbye' to French: ___" → "au revoir"
- Painter: [狗的图, 狗的 mask, 猫的图, ___] → 猫的 mask

模型并不知道任务是什么，它只做**模式延续（pattern completion）**。

## 5.4 SegGPT —— 分割特化 + 多 context

SegGPT 在 Painter 基础上做了两个改动：

**(1) 专注分割**

- 不做深度/光流/关键点，只做分割
- 但做**所有类型的分割**：语义、实例、全景、部件、医学、甚至视频帧
- 训练数据全部改写成"mask 图"形式

**(2) 支持多 context**

- Painter 只用 1 个 example
- SegGPT 支持 k 个 example 拼在一起——few-shot prompting
- 更多 example → 更稳定的任务推断

SegGPT 还加了一个 **"in-context tuning"** 技术：推理时可以针对特定 example 做一次梯度更新（只更新 1 个 learnable prompt token），适应率再提升。**这在机制上和 Visual Prompt Tuning 同构**。

## 5.5 为什么这条路是"提示化的雏形"

到 SegGPT，**分割第一次不需要通过类别标签 / 文字 / 点击框来"指定任务"**——直接通过**一张示例图 + 它的 mask** 来指定："我要分割 **和这个 example 一样性质** 的东西"。

这是一种 **更弱但更通用的接口**：

- 弱：你要给示例——比直接文字提示"段出树"更笨拙
- 通：示例可以表达文字无法描述的任务（"帮我段出这种奇怪的纹理结构"）

**本质上 SegGPT 把"任务的规格"外部化到一对样本对上**——这比 Grounding DINO 的文本 prompt 更加"**无语言**"的提示。

## 5.6 SegGPT 在后续工作里的影响

- **SAM 的交互范式**：SAM 的 prompt-based 分割继承了 SegGPT 的"外部指定任务"思想
- **Matcher / PerSAM**：直接把 SegGPT 的 in-context 分割和 SAM 的 prompt 分割合流
- **Painter 开出一条 "unified dense prediction" 的线**：后续 Unified-IO、4M 都在走这条路
- **Visual in-context learning 整个研究方向**：Painter 是该方向最早的有影响力的工作之一

但 SegGPT 本身**没有成为业界主流**——因为精度上不打 Mask2Former 或 SAM。它的价值在于**开了一条路**，但这条路的终点还没被达到（视觉 in-context learning 到 2025 仍然是 open problem）。

## 5.7 SegGPT 的残差

- **精度天花板较低**：ADE20K ~58 mIoU（和 Mask2Former 差不多），但单任务 SOTA 达不到
- **2×2 网格的空间预算有限**：分辨率减半，对精细分割不利
- **样本选取敏感**：in-context 依赖 example 质量——选不好的 example 模型就废
- **不是 query-based**：它不走 MaskFormer 的路，所以不能自然扩展到开放词汇

这些残差让 SegGPT 没能成为统一分割的终点——**它的接棒者是 SAM**（prompt 更精确）和 **CAT-Seg / ODISE**（开放词汇更彻底）。

---

