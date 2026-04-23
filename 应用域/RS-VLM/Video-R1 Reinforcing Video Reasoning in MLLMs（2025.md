# Video-R1: Reinforcing Video Reasoning in MLLMs（2025）

与五阶段关系: 跨 III-IV
优先级: P1 · 重点
关键贡献: 从文本到视频的 R1 移植；提出 T-GRPO（时间感知 GRPO）鼓励模型在推理链中引用多帧证据；证明 RL 在视频历险上也能激发长链时间推理。
基座 / 起点: Qwen2.5-VL + GRPO 于视频 CoT
局限 / 残差 / 它催生了什么: 视频 token 开销大，帧采样策略仍是升工启发式；空间-时间联合推理（R7×R8）是下一个残差。
年份: 2025
思考载体: 文本 token
我的视角 / 为什么重要: R8 当下最洁净的可复复点。
机构 / 团队: CUHK / Shanghai AI Lab
测试时扩展机制: 自我修正 / self-refine, 长 CoT
范式标签: Framework, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: GRPO / R1-RL, SFT
链接: https://arxiv.org/abs/2503.21776
阅读状态: 待读