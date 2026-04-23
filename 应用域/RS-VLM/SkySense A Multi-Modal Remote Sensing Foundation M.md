# SkySense: A Multi-Modal Remote Sensing Foundation Model Towards Universal Interpretation（Guo 2024, CVPR）

与五阶段关系: 谱系外 / 一般理论
优先级: P0 · 必读
关键贡献: 21.5 亿参数的统一 RS 基础模型；同时处理 HSR 光学 + 多光谱 Sentinel-2 + SAR 三种模态；在 16 个下游任务上全面 SoTA；后继 SkySense V2（ICCV 2025）与 SkySense++（Nature MI 2025）进一步扩展
基座 / 起点: ViT + 多模态对比 + MIM
局限 / 残差 / 它催生了什么: 模型参数量巨大，部署困难；多模态对齐仍依赖配准；与 VLM 的对接还在早期阶段
年份: 2024
思考载体: 多光谱通道, 潜向量
我的视角 / 为什么重要: 现阶段 RS 领域最强的视觉基础模型之一；「RS 领域的 DINOv2」。RS-VLM 如果要对标 GPT-4V 级能力，视觉塔大概率在 SkySense 系、SatMAE 系、Prithvi 系里三选一
机构 / 团队: Ant Group / 武汉大学
研究路线: R7 · 遥感视觉基础模型（RS FMs）
范式标签: Model, RS Foundation Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: Pretrain from scratch
链接: https://arxiv.org/abs/2312.10115
阅读状态: 待读

SkySense 的三件事：

1. **多模态统一**：光学 HSR + Sentinel-2 多光谱 + SAR，三塔共享 backbone
2. **几何-时空语义解耦**：设计了 multi-granularity 的对比目标
3. **规模化**：21 亿参数 + 2150 万样本

V2 (ICCV 2025)：unified foundation model for multi-modal RS

SkySense++ (Nature MI 2025)：语义增强版