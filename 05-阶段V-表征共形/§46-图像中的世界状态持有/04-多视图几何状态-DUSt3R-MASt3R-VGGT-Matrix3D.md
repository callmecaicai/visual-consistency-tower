# 多视图几何状态：DUSt3R、MASt3R、VGGT 与 Matrix3D

类型: 前沿补遗 / 多视图状态
阶段: V · 表征共形
对应章节: §46
核心命题: 多视图几何模型把阶段 V 的状态对象推进到 camera、pose、pointmap、dense correspondence 与 view consistency。

## 一、从 depth map 到 pointmap / pose / track

单图几何只能约束部分状态。多视图几何进一步要求系统持有：

```text
camera
pose
pointmap
dense correspondence
view consistency
track
```

这使阶段 V 的“图像世界状态”从单一投影表面扩展到多个视图之间的一致状态。

## 二、代表节点

| 节点 | 主要贡献 | 状态对象 |
|---|---|---|
| DUSt3R | 从任意图像对/集合回归 dense pointmap，降低相机先验依赖 | pointmap / 3D correspondence |
| MASt3R | 在 DUSt3R 基础上强化 dense local features 与 matching | matching / 3D reconstruction |
| VGGT | feed-forward 推断 camera parameters、point maps、depth maps、3D point tracks | camera / pose / track |
| Matrix3D | 统一 pose estimation、depth prediction、novel view synthesis | multi-modal photogrammetry state |

## 三、状态对象审计

| 审计项 | 判断 |
|---|---|
| 状态对象 | 多视图几何、camera、pose、pointmap、track |
| H 等级 | H4 候选 |
| 主要接口 | reconstruction、matching、view synthesis、tracking |
| 变换族 | viewpoint、camera baseline、partial overlap、multi-image consistency |
| 主要残差 | 几何一致不等于物理、因果、行动和不确定性闭合 |

## 四、理论位置

多视图几何是阶段 V 的强证据，因为它要求系统在不同观测之间保持同一结构。它比单图 depth 更接近“世界片段”的内部持有。

但它仍然不是完整 world model。它主要持有几何状态，而不是：

```text
physical law
causal intervention
object intention
action consequence
```

## 五、参考

- [DUSt3R (arXiv 2023)](https://arxiv.org/abs/2312.14132)
- [MASt3R (arXiv 2024)](https://arxiv.org/abs/2406.09756)
- [VGGT (arXiv 2025)](https://arxiv.org/abs/2503.11651)
- [Apple, *Matrix3D* (official research page, 2025)](https://machinelearning.apple.com/research/large-photogrammetry-model)
