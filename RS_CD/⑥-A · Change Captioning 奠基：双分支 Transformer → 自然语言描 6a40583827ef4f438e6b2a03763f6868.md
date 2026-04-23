# ⑥-A · Change Captioning 奠基：双分支 Transformer → 自然语言描述（Chg2Cap / RSICCformer+LEVIR-CC）

CD 任务类型: 变化描述（Captioning）, 建筑 CD
与 VLM 视觉思考主线关联: RS-VLM 主线 R8（视觉 → 语言生成）的起点。是我方案「语言出口」的直接对标。
代表基座 / 骨干: 双分支 Transformer encoder + caption decoder
优先级: P0 · 必读
关键创新: 首次把 CD 从「掩码预测」扩展到「语言生成」——输出的不再是 mask，而是对「什么变了」的自然语言描述。Chg2Cap 奠基双分支 Transformer + 交叉注意力差分 + caption decoder 架构；RSICCformer 提出 LEVIR-CC 数据集（10077 对 + 5 句描述），构成 RS Change Captioning 的「ImageNet 时刻」。
局限 / 残差 / 催生了什么: 封闭词汇、固定句式、语义粒度粗、不可交互。催生了三条进化路径（⑥-B：语义化/高效化/解耦化）以及 ⑥-C 的会话 & Agent 化。
年份: 2023
我的视角 / 落地价值: LEVIR-CC 是我 training-free 方案的核心 benchmark。把 VLM 当 caption decoder 接到 SAM+CLIP 管线后面即可零监督复现此主线——不用训练 decoder，换成 prompt 工程。
方法家族: Change Captioning, Hybrid CNN-Transformer
机构 / 团队: Chg2Cap / RSICCformer 团队
模态支持: 光学 RGB, 文本 prompt
演进阶段: ⑥ VLM/LLM 驱动 · Change Captioning / Agent（2024-2025）
监督方式: 像素级全监督
训练 / 评测数据集: LEVIR-CC, LEVIR-CD
阅读状态: 待读

## 核心主题

把 CD 的输出形态从 mask 升级到自然语言。回答一个运营侧的真实需求：**一张 binary mask 无法填进巡检报告 / 灾情通告，需要一句话描述**。

## 架构共性

两篇的架构几乎一致：

```
时相 A  ┐                         ┐
        ├─ 双分支 Transformer 编码  ├─ 交叉注意力差分 ─→ caption decoder ─→ 自然语言
时相 B  ┘                         ┘
```

技术难点不在架构，在**如何把差异特征转成可生成的 token**。

## 两篇分工

| 代表 | 关键贡献 |
| --- | --- |
| **Chg2Cap** (2023) | 架构奠基：双分支 + 交叉注意力 + caption decoder 三件套 |
| **RSICCformer** (2023) | 数据奠基：**LEVIR-CC** 数据集（10077 对图像 + 5 句描述），整个赛道的基准 |

## 共享局限

- 封闭词汇表（训练集见过的才能说）。
- 固定句式（套路化，缺少 spatial reasoning）。
- 单轮输出（不支持追问、不支持 referring）。
- 语义粒度停留在「什么变了」，不到「变成了什么」（催生 ⑥-B 语义化）。

## 催生了什么

- **⑥-B**：三条进化路径分别攻语义粒度（KCFI）、计算复杂度（RSCaMa）、任务耦合（PromptCC）。
- **⑥-C**：把单轮 caption → 多轮对话 + Agent 化（TeoChat/ChangeChat/Change-Agent）。

## 对我方案的意义

- LEVIR-CC 是**必须刷的 benchmark**——它是「CD → 语言」的 ImageNet。
- 架构借鉴：training-free 版即 SAM+CLIP 差分 → VLM caption（把 Transformer decoder 换成 VLM zero-shot caption）。

## 论文

- Chg2Cap：[arxiv.org/abs/2304.01091](http://arxiv.org/abs/2304.01091)
- RSICCformer / LEVIR-CC：[arxiv.org/abs/2212.02549](http://arxiv.org/abs/2212.02549)