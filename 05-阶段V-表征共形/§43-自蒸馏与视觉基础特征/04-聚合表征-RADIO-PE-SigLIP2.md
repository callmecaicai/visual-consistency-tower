# 聚合表征：RADIO、Perception Encoder 与 SigLIP2

类型: 前沿补遗 / 多教师闭合
阶段: V · 表征共形
对应章节: §43
核心命题: 当单一训练目标无法覆盖所有状态对象时，阶段 V 出现多教师、多接口、多层 embedding 的聚合表征路线。

## 一、聚合表征为什么重要

阶段 V 的前沿不再只有“一个最强 encoder”。不同闭合制度已经各自形成强项：

```text
DINO: language-free dense visual feature
SigLIP / CLIP: language-aligned semantic feature
SAM: mask / support / promptable spatial feature
depth / geometry models: geometric state feature
```

聚合表征的目标不是证明某个目标函数最优，而是把多个闭合制度的能力压进同一视觉前端。

## 二、代表节点

| 节点 | 主要能力 | 理论位置 |
|---|---|---|
| RADIO / AM-RADIO / C-RADIO | 多教师蒸馏，把异构视觉能力合成一个学生模型 | 聚合表征闭合 |
| Perception Encoder | 发现强视觉 embedding 不一定在输出层，并通过 alignment 释放中间层能力 | 层级表征审计 |
| SigLIP2 | 图文编码器向 localization、dense prediction、masked prediction 回补 | III -> V 的语义回流 |

## 三、状态对象审计

| 审计项 | 判断 |
|---|---|
| 状态对象 | 多接口视觉基础特征 |
| H 等级 | H2-H3 |
| 主要接口 | VLM、dense prediction、retrieval、localization、tracking |
| 扩张半径 | multi-interface radius |
| 主要残差 | 多教师能力混合不等于统一世界状态持有 |

## 四、理论边界

聚合表征很容易被误写成“统一世界模型”。更准确的说法是：

> 它统一的是多个教师的可调用能力，不是自动统一这些能力背后的状态对象。

因此，聚合表征应被登记为 H2-H3 的强基础设施，是否进入 H4 仍要通过几何、遮挡、对应、预测和反事实任务审计。

## 五、参考

- [C-RADIOv4 technical report](https://arxiv.org/html/2601.17237v1)
- [Perception Encoder (arXiv 2025)](https://arxiv.org/abs/2504.13181)
- [SigLIP2 (arXiv 2025)](https://arxiv.org/abs/2502.14786)
