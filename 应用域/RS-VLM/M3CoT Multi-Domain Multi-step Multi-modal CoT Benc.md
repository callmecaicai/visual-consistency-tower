# M3CoT: Multi-Domain Multi-step Multi-modal CoT Benchmark（Chen 2024, ACL）

与五阶段关系: 跨 III-IV
优先级: P1 · 重点
关键贡献: 首个明确针对「多步 + 视觉必须参与每一步」的 benchmark；暴露出开源 VLM 与 GPT-4V 与人类的争锋相接差距；而且观察到「加 CoT 反而性能下降」的结构性现象。
基座 / 起点: GPT-4V / Gemini / LLaVA 评测
局限 / 残差 / 它催生了什么: 评测仍是 text-answer，无法捕捉潜空间 / 生成图像的步骤质量；只能从结果反推 R1 路线的天花板。
年份: 2024
思考载体: 文本 token
我的视角 / 为什么重要: 诊断 R1 路线天花板的极好银子。「加了 CoT 反而变差」直接相满了 R2–R4 的必要性，值得在比较论文里引用。
机构 / 团队: HIT (Harbin Institute of Technology)
研究路线: R1 · 文本式 CoT 移植
范式标签: Benchmark, Dataset
视觉在推理中的角色: ⑧ 忠实性 / 诊断对象
训练范式: Prompting / zero-shot
链接: https://arxiv.org/abs/2405.16473
阅读状态: 待读