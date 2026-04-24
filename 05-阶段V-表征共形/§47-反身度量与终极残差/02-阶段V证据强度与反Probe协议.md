# 阶段 V · §47 补页：证据强度与反 Probe 协议

类型: 评估协议/横切
阶段: V · 表征共形
共形维度: 度量, 反身, 证据
关键贡献: 给阶段 V 建立证据强度分级，避免把 probe、attention map、dense transfer、state prediction 混成同等强度的世界状态证明。
残差 / 它催生了什么: 证据分级仍是理论和共同体反身，尚未等于模型自身能修订度量。
定位标签: evidence ladder, anti-probe, metric stack, reflexive metric

## 一、为什么需要证据强度分级

阶段 V 的对象是内部状态，不是外显标签、mask、caption 或图像样本。因此，任何单一指标都只能提供局部证据。

如果不分级，下面这些会被误看成同一件事：

- linear probe 高；
- attention map 看起来有对象；
- dense transfer 强；
- correspondence 稳；
- 遮挡状态能预测；
- 模型知道哪个指标不适合当前状态对象。

这些证据强度完全不同。阶段 V 必须先把它们分开。

## 二、证据强度 E0-E6

| 等级 | 名称 | 含义 | 典型例子 |
|---|---|---|---|
| `E0` | 分数证据 | 表征在分类、linear probe、VTAB 等分数上有用 | linear probe、classification、global retrieval |
| `E1` | 迁移证据 | 表征迁移到多个下游任务仍有效 | transfer learning、few-shot、cross-dataset adaptation |
| `E2` | 显现证据 | attention map、object discovery 或聚类显示结构浮现 | DINO attention、LOST、TokenCut |
| `E3` | 密集接口证据 | 表征支持 depth、segmentation、correspondence 等 dense task | DINOv2 dense transfer、DenseCL、PixPro、DetCon |
| `E4` | 结构一致性证据 | 在遮挡、跨图、视角、局部编辑中保持对象或几何结构 | correspondence under view change、occlusion consistency |
| `E5` | 预测/反事实证据 | 能预测缺失状态、表达多假设不确定性，或通过反事实一致性测试 | JEPA-style missing latent prediction、amodal/counterfactual tests |
| `E6` | 反身证据 | 系统能判断某个度量是否适合当前状态对象，并能选择、修订或生成度量 | 当前阶段尚未闭合 |

## 三、方法定位示例

| 方法/证据 | 推荐定位 | 不能过度声称 |
|---|---|---|
| DINO attention emergence | `E2` | 不能直接说已持有物理对象 |
| DINOv2 dense transfer | `E3` | 不能直接说已完成世界状态 |
| DenseCL / PixPro / DetCon | `E3` | 不能直接说已预测隐藏状态 |
| LOST / TokenCut / STEGO | `E2-E3` | 不能把后处理提取误写成模型显式持有 |
| JEPA / I-JEPA | 目标是 `E5` | 是否达到取决于 target 表征是否真含状态变量 |
| `§47` 反身度量 | 目标是 `E6` | 研究者反思不等于模型自身反身 |

## 四、反 Probe 协议

任何声称“持有世界状态”的方法，不能只用一个 probe 证明。必须给出以下五项：

1. **状态对象**：它持有的是对象身份、部件拓扑、几何深度、遮挡关系、跨图对应、布局关系，还是状态不确定性？
2. **调用接口**：这个状态通过 depth、correspondence、segmentation、matching、editing、prediction 中的哪些接口被调用？
3. **变换族**：它在哪些变换下稳定，在哪些变换下等变？
4. **误判指标**：哪些指标会高估或低估它？
5. **破裂反例**：在哪些反例中它会失败？

probe 不是错，probe 崇拜才是错。probe 只能作为 `E0-E1` 级证据，不能替代状态对象本身。

## 五、多度量栈

阶段 V 的评估至少需要下面几层共同出现：

| 度量层 | 问题 | 对应章节 |
|---|---|---|
| 不变性度量 | 同一图像实例或对象在增强下是否稳定？ | `§42` |
| 等变性度量 | 视角、姿态、遮挡、局部编辑下结构是否按规则改变？ | `§42-§46` |
| 迁移性度量 | 表征是否能跨任务、跨域复用？ | `§43` |
| 结构显化度量 | 对象、部件、边界、对应是否可被读出？ | `§44` |
| 状态预测度量 | 缺失或目标状态是否能在 latent 层被预测？ | `§45` |
| 世界一致性度量 | 深度、遮挡、对应、布局在多接口中是否互相支持？ | `§46` |
| 反身度量 | 系统是否知道当前度量命中什么、遮蔽什么？ | `§47` |

## 六、三种反身主体

| 类型 | 主体 | 含义 | 阶段 V 当前状态 |
|---|---|---|---|
| `Rfl-T` | 理论反身 | 研究者或理论框架审计度量合法性 | 已经出现 |
| `Rfl-C` | 共同体反身 | benchmark、leaderboard、评测协议被共同体修订 | 部分出现 |
| `Rfl-M` | 模型反身 | 模型能发现、选择、修订或生成度量 | 尚未闭合 |

这张表的作用，是防止把“我们在反思模型指标”误写成“模型自己已经反身”。

## 七、本页结论

阶段 V 的强度不应由单一分数决定，而应由证据层级决定：

```text
E0/E1: feature useful
E2/E3: structure visible and callable
E4/E5: state stable, predictive, counterfactual
E6: metric reflexive
```

如果一个方法只到 `E0-E1`，它可以是好表征，但不能直接被称为世界状态持有。若它能到 `E4-E5`，才开始接近阶段 V 的核心命题。`E6` 则仍是终极残差。
