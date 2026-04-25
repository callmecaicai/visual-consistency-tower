# 05A · DINO-SSL 线：语言无关视觉表征 scaling

本页从原“05-两条DINO线”中拆出，专门处理 DINO / DINOv2 / DINOv3 这一条语言无关视觉表征线。

## 本线定位

| 项 | 内容 |
|---|---|
| 所属闭合 | 阶段 II 的稠密基础特征回流，同时通向阶段 V 的表征共形。 |
| 主要对象 | patch / dense feature / objectness signal。 |
| 语义来源 | 主要来自视觉自监督与数据分布，不直接来自文本 prompt。 |
| 阶段 II 功能 | 为分割、检测、深度、对应等稠密任务提供可迁移骨干。 |
| 残差 | 强 feature 不等于世界状态；objectness signal 不等于对象持有。 |

## 为什么它不应和 Grounding DINO 混写

DINO SSL 线处理的是“视觉表征如何在无语言监督下形成可迁移结构”。它的核心问题是 feature quality、dense transfer、objectness emergence 和 scaling 稳定性。

Grounding DINO 处理的是“文本如何作为 query / condition 进入检测”。二者名字相同，但闭合对象不同。

## 在阶段 II 中的角色

DINO 类表征让阶段 II 的 dense feature field 变得更强，尤其改善：

- 无监督 objectness 信号；
- dense transfer；
- depth / segmentation / correspondence 的预训练底座；
- SAM / detection / open-vocab pipeline 的视觉侧材料。

但它不是阶段 II 的语义主权答案。即便 dense feature 很强，开放概念、语言调用和公共语义仍要进入阶段 III；对象状态、几何、遮挡和对应的持有则要在阶段 V 中审计。

## 出口残差

本线最适合登记为桥接节点：

> DINO SSL 是阶段 II 的强视觉材料层，也是阶段 V 的证据线；但它不是阶段 III 的公共语义契约，也不是阶段 V 的完成形态。
