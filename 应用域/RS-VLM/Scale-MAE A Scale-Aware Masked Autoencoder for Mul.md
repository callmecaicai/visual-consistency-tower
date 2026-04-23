# Scale-MAE: A Scale-Aware Masked Autoencoder for Multiscale Geospatial Representation Learning（Reed 2023, ICCV）

与五阶段关系: 谱系外 / 一般理论
优先级: P0 · 必读
关键贡献: 把「地面覆盖面积」（而非图像分辨率）写进 ViT positional encoding；用 bandpass 解码器同时重建低/高频图像，强制网络在多尺度上学习；8 个 RS 数据集平均 kNN 提升 2.4-5.6%
基座 / 起点: ViT + MAE
局限 / 残差 / 它催生了什么: 仍是单模态 encoder；对多光谱支持不如 SatMAE 精细；催生了「尺度感知」成为 RS FM 标配
年份: 2023
思考载体: 潜向量
我的视角 / 为什么重要: RS 第一性问题「尺度」（从 0.3m 到 30m 跨百倍）的理论奠基——这也正是 RS-VLM 在 R2 路线上做瓦片/金字塔推理的物理依据。SatMAE 解决光谱，Scale-MAE 解决尺度，二者合起来才是 RS FM 的完整起点
机构 / 团队: UC Berkeley
研究路线: R7 · 遥感视觉基础模型（RS FMs）
范式标签: Model, RS Foundation Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: Pretrain from scratch
链接: https://arxiv.org/abs/2212.14532
阅读状态: 待读

核心：视觉编码器必须「知道」当前 patch 代表的地表物理尺度。实现：位置编码 × 地面覆盖面积 × ViT patch，解码分为高/低频分支分别重建。

与 R2 的耦合：下游 RS-VLM 做 zoom-in / 滑窗推理时，视觉塔如果本身就是尺度感知的，能直接把「哪一层金字塔」语义编码进 token，大幅降低 VLM 在空间关系上的幻觉。