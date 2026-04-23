# SatMAE: Pre-Training Transformers for Temporal and Multi-Spectral Satellite Imagery（Cong 2022, NeurIPS）

与五阶段关系: 谱系外 / 一般理论
优先级: P0 · 必读
关键贡献: 首个针对多光谱 + 时序卫星影像的 MAE 预训练框架；按光谱波段分组做独立 positional encoding；时间维度用独立 temporal embedding + 跨时相独立 masking
基座 / 起点: ViT + MAE
局限 / 残差 / 它催生了什么: 只是 encoder，不直接参与 VLM 推理；多尺度能力弱（被 Scale-MAE 接力）；催生了一整代 RS pretrain 方法
年份: 2022
思考载体: 多光谱通道, 潜向量
我的视角 / 为什么重要: RS-VLM「视觉主体性」的真正起点——所有 RS-VLM 的视觉塔要么用通用 CLIP（浪费 RS 先验），要么用 SatMAE 类 RS FM。这是 R7 的第 0 号基石
机构 / 团队: Stanford（Ermon Lab）
研究路线: R7 · 遥感视觉基础模型（RS FMs）
范式标签: Model, RS Foundation Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: Pretrain from scratch
链接: https://arxiv.org/abs/2207.08051
阅读状态: 待读

RS 基础模型 R7 的奠基之作。要点：

- **光谱位置编码**：把多光谱看作分组 tokens，不同波段有独立的光谱位置编码
- **时间位置编码**：时相独立 masking 让模型学到跨时间关联
- 在 fMoW-Sentinel 上预训练；下游分类、分割提升显著

与 RS-VLM 的关系：作为视觉塔，能把 RS 先验（多光谱 / 时序）注入 VLM 的视觉侧。