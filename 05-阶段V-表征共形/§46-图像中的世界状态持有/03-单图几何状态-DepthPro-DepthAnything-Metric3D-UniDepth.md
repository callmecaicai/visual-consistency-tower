# 单图几何状态：Depth Pro、Depth Anything、Metric3D 与 UniDepth

类型: 前沿补遗 / 几何状态
阶段: V · 表征共形
对应章节: §46
核心命题: 单图几何模型把阶段 V 的状态对象从“好表征”压实到 depth、normal、metric scale、camera ambiguity 与 boundary geometry。

## 一、为什么单图几何属于阶段 V

单图 depth 不是普通下游任务。它要求模型从有限投影表面中持有一种受证据约束的几何状态：

```text
image -> depth / normal / metric scale / camera-aware geometry
```

这正是阶段 V 的问题：图像不是世界，但图像约束了一族可能世界状态。

## 二、代表节点

| 节点 | 主要贡献 | 状态对象 |
|---|---|---|
| Depth Pro | zero-shot metric monocular depth，强调高分辨率、绝对尺度、边界质量 | metric depth / boundary geometry |
| Depth Anything V2 | 大规模 synthetic + pseudo-labeled real data，提升 zero-shot depth | dense depth field |
| Metric3D / Metric3D v2 | zero-shot metric depth 与 surface normal 的统一几何路线 | metric geometry / normal |
| UniDepth | 直接预测 metric 3D points 与 camera-aware depth | metric 3D point state |

## 三、状态对象审计

| 审计项 | 判断 |
|---|---|
| 状态对象 | 单图几何深度、法向、尺度、边界 |
| H 等级 | H3-H4 局部 |
| 主要接口 | depth、normal、3D reconstruction、view-aware tasks |
| 变换族 | crop、scale、domain shift、camera ambiguity |
| 主要残差 | 单图状态欠定；几何状态不等于物理、因果、对象意图 |

## 四、单图几何的边界

单图几何强，不代表完整世界状态。它仍然面临：

1. 遮挡背后的多解。
2. 相机参数与尺度的歧义。
3. 物体材质、支撑、因果与意图的缺席。
4. 单帧无法确定的时间状态。

因此，单图几何是 H4 的局部入口，不是 H4 的完成形态。

## 五、参考

- [Apple, *Depth Pro* (official research page, 2024)](https://machinelearning.apple.com/research/depth-pro)
- [Depth Anything V2 (arXiv 2024)](https://arxiv.org/abs/2406.09414)
- [Metric3D v2 (arXiv 2024)](https://arxiv.org/abs/2404.15506)
- [UniDepth (arXiv 2024)](https://arxiv.org/abs/2403.18913)
