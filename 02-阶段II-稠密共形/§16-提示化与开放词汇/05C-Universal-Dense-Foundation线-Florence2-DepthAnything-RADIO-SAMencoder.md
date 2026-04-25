# 05C · Universal Dense Foundation 线：Florence-2 / Depth Anything / RADIO / SAM Encoder

本页从原“05-两条DINO线”中拆出，专门处理通用稠密基础模型线。

## 本线定位

| 项 | 内容 |
|---|---|
| 所属闭合 | 阶段 II 的接口闭合与横切基础设施。 |
| 主要对象 | task prompt、dense feature、continuous field、multi-teacher representation。 |
| 语义来源 | 文本 token、伪标签、视觉 SSL、数据引擎和多教师蒸馏。 |
| 阶段 II 功能 | 把检测、分割、描述、深度、定位等任务推向统一接口或统一骨干。 |
| 残差 | 接口统一不等于世界统一；连续场与状态持有仍需更强审计。 |

## Florence-2：任务序列化

Florence-2 把多种视觉任务序列化成 prompt 与结构 token 输出。它的贡献是接口统一：同一模型可以在文本式任务提示下输出 caption、box、region、dense 标注等结果。

但这种统一首先是接口统一，不是世界状态统一。

## Depth Anything：连续场边界节点

Depth Anything 说明阶段 II 不只包含离散语义 / 实例任务。深度这类连续几何场也能通过强视觉表征、伪标签和大规模数据获得零样本能力。

它更像阶段 II 与阶段 V 之间的边界节点：连续场变强，但深度图本身仍是投影表面的估计，不是完整 3D 世界持有。

## RADIO / SAM Encoder：基础设施聚合

RADIO、SAM encoder、DINOv2/v3、CLIP 等模型共同说明，阶段 II 末端的骨干不再只是任务专用网络，而是可插拔基础设施。

多教师蒸馏和聚合路线的价值在于保留不同闭合制度的互补能力：CLIP 的公共语义、DINO 的 dense feature、SAM 的空间支撑、MAE / JEPA 的表征压力。

## 出口残差

本线不是单纯通向阶段 III，也不是直接完成阶段 V。

它说明阶段 II 末端出现了横切基础设施：

- 公共语义路线进入阶段 III；
- 视觉自持路线进入阶段 V；
- 工艺聚合路线成为跨阶段骨干。
