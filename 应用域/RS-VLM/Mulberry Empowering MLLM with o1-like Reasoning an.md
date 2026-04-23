# Mulberry: Empowering MLLM with o1-like Reasoning and Reflection via Collective MCTS（2024）

与五阶段关系: III · 语言共形
优先级: P1 · 重点
关键贡献: 提出 Collective MCTS：多个 VLM 在推理树上联合搜索 + 互验证；达到长了「似 o1」的反思轨迹；同时开源 Mulberry-260K CoT 数据集成为 Vision-R1 等工作的 cold-start。
基座 / 起点: LLaVA-1.5 / Qwen-VL
局限 / 残差 / 它催生了什么: MCTS 运行成本高；验证器来自同类 VLM 存在自相关风险——对「异构验证器」的研究是下一步。
年份: 2024
思考载体: 文本 token
我的视角 / 为什么重要: R5 与 R9 的桥。
机构 / 团队: THU / Shanghai AI Lab
测试时扩展机制: 多模态验证器, 树搜索 / MCTS, 自我修正 / self-refine, 长 CoT
研究路线: R9 · 测试时搜索 · 验证器
范式标签: Dataset, Framework, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: Distillation, SFT
链接: https://arxiv.org/abs/2412.18319
阅读状态: 待读