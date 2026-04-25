# JEPA 系谱：从 I-JEPA 到 V-JEPA 2.1

类型: 前沿补遗 / 预测式表征
阶段: V · 表征共形
对应章节: §45
核心命题: JEPA 系列的意义不是换一种 reconstruction loss，而是把学习对象从观测恢复切到 latent / state prediction；V-JEPA 2.1 则把这条线推进到 dense predictive representation。

## 一、系谱总表

| 节点 | 学习对象 | 主要推进 | 阶段 V 定位 |
|---|---|---|---|
| I-JEPA | 图像 context -> target representation | 从像素重建切到 joint-embedding prediction | H3 起点 |
| V-JEPA | 视频中的 feature prediction | 把预测式表征推向时序视觉 | H3 外推 |
| V-JEPA 2 | understanding、prediction、planning 接口 | 把预测式表征接到物理世界任务 | H3-H4 候选 |
| V-JEPA 2.1 | dense, high-quality image/video representations | 用 dense predictive loss 强化 spatial-temporal grounding | H3 -> H4 候选 |

## 二、I-JEPA 的本体切换

I-JEPA 的关键不是“masked image modeling 的另一种版本”，而是：

```text
predict representation, not pixels
```

这意味着阶段 V 的学习对象从可见观测切到抽象目标状态。

## 三、V-JEPA 与 V-JEPA 2 的外推

V-JEPA 把状态预测推入视频；V-JEPA 2 把理解、预测、规划接口放到同一条预测式表征线上。

这很重要，但要保持边界：

> 视频和规划接口是阶段 V 的外推，不替代阶段 V 当前关于图像证据约束状态的核心定义。

## 四、V-JEPA 2.1 的关键变化

V-JEPA 2.1 的理论位置在于：

```text
global prediction -> dense predictive representation
```

也就是说，JEPA 不再只被读成全局语义表征，而开始面对 dense feature、depth、navigation、robot grasping 等需要空间状态的接口。

## 五、状态对象审计

| 审计项 | 判断 |
|---|---|
| 状态对象 | predictive dense state |
| H 等级 | H3-H4 候选 |
| 主要接口 | missing target prediction、dense features、video understanding、action-facing tasks |
| 扩张半径 | prediction radius、temporal radius、dense radius |
| 主要残差 | predicted latent 是否真是 world state，仍需 §46/§47 裁判 |

## 六、不能过度宣称

JEPA 系列不能被写成“world model 已完成”。更稳的判断是：

> JEPA 是阶段 V 的核心方向，但不是自动完成形态。

它把目标从 pixel 改成 representation；representation 是否真是 state，需要状态对象登记表、证据等级和反 probe 协议共同裁判。

## 七、参考

- [LeCun, *A Path Towards Autonomous Machine Intelligence* (OpenReview 2022)](https://openreview.net/pdf?id=BZ5a1r-kVsf)
- [Assran et al., *I-JEPA* (CVPR 2023)](https://arxiv.org/abs/2301.08243)
- [Bardes et al., *V-JEPA* (arXiv 2024)](https://arxiv.org/abs/2404.08471)
- [V-JEPA 2 official post (Meta, 2025)](https://about.fb.com/news/2025/06/our-new-model-helps-ai-think-before-it-acts/)
- [Bordes et al., *V-JEPA 2.1* (arXiv 2026)](https://arxiv.org/abs/2603.14482)
