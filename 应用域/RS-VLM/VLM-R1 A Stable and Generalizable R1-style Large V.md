# VLM-R1: A Stable and Generalizable R1-style Large Vision-Language Model（2025）

与五阶段关系: III · 语言共形
优先级: P1 · 重点
关键贡献: 开源 R1-style VLM 的工程化复复；系统梳理训练数据、奖励函数和稳定性。行业 baseline 框架之一。
基座 / 起点: Qwen2.5-VL
局限 / 残差 / 它催生了什么: 仍停留在文本 CoT 时；不涉及图像操作或潜空间——残差被 Vision-R1 / DeepEyes 接走。
年份: 2025
思考载体: 文本 token
我的视角 / 为什么重要: 如果要开 R1-style 开源基设，这是当下第一个工程第一申请读件的文献。
机构 / 团队: Om AI Lab
测试时扩展机制: 自我修正 / self-refine, 长 CoT
研究路线: R5 · RL 驱动的视觉推理
范式标签: Framework, Infrastructure, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: GRPO / R1-RL, SFT
链接: https://arxiv.org/abs/2504.07615
阅读状态: 待读