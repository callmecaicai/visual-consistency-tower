# Latent Visual Reasoning（LVR, 2025）

与五阶段关系: 跨 III-V
优先级: P0 · 必读
关键贡献: 将 Coconut 思路搬入 VLM：推理直接在视觉嵌入流形上迭代，不生成文本 token，不调外部工具——R4 路线的标志性第一步（与用户现有收藏 Latent Visual Reasoning: Reasoning in Visual Embedding Space without Generating Text (https://www.notion.so/Latent-Visual-Reasoning-Reasoning-in-Visual-Embedding-Space-without-Generating-Text-2d6748d64800836ca4bb01b09ae92dfd?pvs=21) / Latent Visual Reasoning (LVR) (https://www.notion.so/Latent-Visual-Reasoning-LVR-2f3748d6480083648939014250a87f55?pvs=21) 对应）。
基座 / 起点: LLaVA 类 VLM + visual embedding loop
局限 / 残差 / 它催生了什么: 潜空间思考的步骤可解释性最差；需要与 R10 的忠实性工具配套使用。催生 Monet 以及对潜空间通道的探针工作。
年份: 2025
思考载体: 潜向量
我的视角 / 为什么重要: 你主线上「视觉内省」的平行最近作品之一，值得种树坐最低单元读一次。
机构 / 团队: 开源社区
测试时扩展机制: 潜空间迭代, 长 CoT
研究路线: R4 · Latent Visual Reasoning
范式标签: Framework, Model
视觉在推理中的角色: ⑤ 在潜空间直接参与
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2506.01117
阅读状态: 待读