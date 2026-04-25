# DINOv3 与 dense feature scaling：从全局特征到状态载体

类型: 前沿补遗 / dense feature
阶段: V · 表征共形
对应章节: §43 / §44
核心命题: DINOv3 的意义不是“又一个 DINO”，而是把 dense feature quality 与长训稳定性推到阶段 V 的中心。

## 一、为什么 DINOv3 是阶段 V 节点

DINOv2 把视觉表征推向 all-purpose visual features。Registers 暴露出 dense token 场会出现 artifacts，说明 dense feature 并不天然干净。

DINOv3 的意义在于：dense feature 退化不再是附带问题，而成为 scaling 过程必须正面处理的问题。

## 二、状态对象审计

| 审计项 | 判断 |
|---|---|
| 状态对象 | high-quality dense feature field |
| H 等级 | H2-H3 |
| 主要接口 | segmentation、depth、correspondence、dense transfer |
| 扩张半径 | dense feature radius、长训稳定性、跨任务迁移 |
| 主要残差 | dense feature 高质量不等于对象、几何、遮挡、物理状态被持有 |

## 三、三层读法

| 层级 | 命题 |
|---|---|
| 技术事实 | DINOv3 继续扩大视觉自监督数据与模型规模，并把 dense feature 稳定性作为关键目标。 |
| 机制解释 | 视觉表征 scaling 不再只是 global embedding scaling，而是 dense token field scaling。 |
| 哲学映射 | 阶段 V 的状态持有必须经过 dense feature 的稳定化；全局向量再强，也不能直接持有世界状态。 |

## 四、DINOv3 的边界

不要把 DINOv3 直接写成 H4 完成形态。它证明 dense field 变强，但不证明：

```text
object permanence
occlusion continuation
physical causality
metric state uncertainty
```

这些仍需 §46 和 §47 的状态对象审计。

## 五、参考

- [Siméoni et al., *DINOv3* (arXiv 2025)](https://arxiv.org/abs/2508.10104)
- [Darcet et al., *Vision Transformers Need Registers* (arXiv 2023)](https://arxiv.org/abs/2309.16588)
