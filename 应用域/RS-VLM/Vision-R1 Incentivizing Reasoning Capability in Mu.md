# Vision-R1: Incentivizing Reasoning Capability in Multimodal LLMs（2025）

与五阶段关系: III · 语言共形
优先级: P1 · 重点
关键贡献: 首次在数学 / 几何类多模态历险上用 R1 范式研究。以人工标注的 Mulberry-260K CoT 数据作为 cold-start，再用 GRPO 推进；在 MathVista / MathVision 上大幅超过规模更大的模型。
基座 / 起点: Qwen2.5-VL + DeepSeek-R1 cold-start
局限 / 残差 / 它催生了什么: 依赖大量高质量人工 CoT；后续工作正在探索如何用 self-play / 规则奖励 减少对人工 CoT 的依赖。
年份: 2025
思考载体: 文本 token
我的视角 / 为什么重要: R1 在「视觉数学 / 几何」任务上的代表性应用点。
机构 / 团队: MMLab@Jerusalem
测试时扩展机制: 自我修正 / self-refine, 长 CoT
研究路线: R5 · RL 驱动的视觉推理
范式标签: Framework, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: GRPO / R1-RL, SFT
链接: https://arxiv.org/abs/2503.06749
阅读状态: 待读