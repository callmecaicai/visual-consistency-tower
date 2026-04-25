# 持续 3D/4D 状态：CUT3R 与 D4RT

类型: 前沿补遗 / 4D 状态外推
阶段: V · 表征共形
对应章节: §46 / 外推接口
核心命题: CUT3R 与 D4RT 说明阶段 V 正在向 persistent scene state 与 4D reconstruction 扩张，但这属于阶段 V 的时空外推，不替代单图状态核心。

## 一、为什么这条线重要

阶段 V 的核心是图像证据约束下的部分世界状态。但一旦图像序列进入，状态持有自然走向：

```text
persistent state
streaming update
3D / 4D reconstruction
tracking
query-based scene state
```

这说明阶段 V 正在逼近更广义的 world model 接口。

## 二、代表节点

| 节点 | 主要贡献 | 状态对象 |
|---|---|---|
| CUT3R | recurrent framework，连续更新内部 state representation，从图像流在线生成 metric-scale pointmaps | persistent 3D state |
| D4RT | 统一 4D scene reconstruction and tracking，用 query 追问任意时间和相机视角下的 3D 位置 | dynamic 4D state |
| V-JEPA 2.1 | dense video self-supervised representation，接入短期物体交互、导航、抓取等接口 | dense predictive video state |

## 三、状态对象审计

| 审计项 | 判断 |
|---|---|
| 状态对象 | persistent / dynamic scene state |
| H 等级 | H4 外推 |
| 主要接口 | streaming 3D perception、4D tracking、navigation、action-facing tasks |
| 变换族 | time、viewpoint、occlusion、camera motion |
| 主要残差 | 已越过单图阶段 V 核心；物理、因果和行动后果仍需独立审计 |

## 四、边界协议

这条线不能把阶段 V 改写成“视频 world model 百科”。更稳的定位是：

> CUT3R / D4RT 是阶段 V 状态持有向时空世界模型扩张的证据，而不是阶段 V 当前核心定义的替代。

阶段 V 当前仍以图像中的状态对象为根基。视频、4D、机器人、planning 是外推接口。

## 五、参考

- [CUT3R (arXiv 2025)](https://arxiv.org/abs/2501.12387)
- [Google DeepMind, *D4RT* (official post, 2026)](https://deepmind.google/blog/d4rt-teaching-ai-to-see-the-world-in-four-dimensions/)
- [V-JEPA 2.1 (arXiv 2026)](https://arxiv.org/abs/2603.14482)
