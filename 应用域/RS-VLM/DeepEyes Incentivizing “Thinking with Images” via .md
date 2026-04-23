# DeepEyes: Incentivizing “Thinking with Images” via Reinforcement Learning（2025）

与五阶段关系: 跨 III-IV
优先级: P0 · 必读
关键贡献: 用 RL 直接奖励「何时 zoom/crop 能答对」的行为，而不是用外部规则；模型自发地学会「先整体看 → 锁定区域 → 放大再答」。o3 行为最直接的开源复刻。
基座 / 起点: Qwen2.5-VL + GRPO
局限 / 残差 / 它催生了什么: 工具格子仍由人定义（28 种工具抽象）；面向「工具从哪里来」这一它催生 R6 / R4 的两条出口。
年份: 2025
思考载体: 文本 token, 裁剪/缩放图像
我的视角 / 为什么重要: P0。R2×R5 交叉的最干净单点，可以直接拿来做个人研究的 baseline。
机构 / 团队: 开源社区（Xiaomi 等）
测试时扩展机制: 多次感知 / re-look, 长 CoT
范式标签: Framework, Model
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: GRPO / R1-RL, SFT
链接: https://arxiv.org/abs/2505.14362
阅读状态: 待读