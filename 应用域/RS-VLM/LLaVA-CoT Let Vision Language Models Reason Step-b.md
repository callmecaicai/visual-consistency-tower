# LLaVA-CoT: Let Vision Language Models Reason Step-by-Step（Xu 2024）

与五阶段关系: III · 语言共形
优先级: P0 · 必读
关键贡献: 把推理显式拆为四阶段 tag：<SUMMARY> / <CAPTION> / <REASONING> / <CONCLUSION>；高质量数据（LLaVA-CoT-100K）+ 阶段级 Beam Search。是「用结构化 CoT 模拟 o1」的最清晰样板。
基座 / 起点: LLaVA / Llama-3.1-8B
局限 / 残差 / 它催生了什么: 仍在文本 CoT 内部模拟视觉推理，<CAPTION> 之后视觉 token 不再参与——Look Light Think Heavy 在这里非常明显。后来的 RL 路线（R5）重新用 GRPO 有机地推进了这一服段结构。
年份: 2024
思考载体: 文本 token
我的视角 / 为什么重要: P0。你在做「视觉思考」时，当下开源社区的第一个直观 baseline 就是 LLaVA-CoT——它排除了“我能不能用纯文本 CoT 走到多远”的问题。
机构 / 团队: NTU / Peking University
测试时扩展机制: Best-of-N, 长 CoT
研究路线: R1 · 文本式 CoT 移植
范式标签: Dataset, Framework, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2411.10440
阅读状态: 待读