# Visual Programming: Compositional Visual Reasoning Without Training（VisProg, Gupta 2023）

与五阶段关系: 跨 III-IV
优先级: P1 · 重点
关键贡献: 用 in-context 示例让 LLM 纯零样本地生成视觉程序（命令语言）；最早明确只用 prompt 就完成「视觉编程」的工作，与 ViperGPT 同时出现是 R6 两个奇粒子。
基座 / 起点: GPT-3 + CLIP / BLIP / Stable Diffusion
局限 / 残差 / 它催生了什么: 与 ViperGPT 类似的框结约束；脚本库是手工写的——后续的 VisuoThink / UI-TARS 等换成更宽的 DSL / 视觉动作。
年份: 2023
思考载体: 外部工具, 生成代码
我的视角 / 为什么重要: 和 ViperGPT 一同当作 R6 范式的奠基二体阅读。
机构 / 团队: Allen Institute for AI
测试时扩展机制: 外部工具调用
研究路线: R6 · Visual Agent · Program-as-Thought
范式标签: Agent, Framework, Prompting
视觉在推理中的角色: ⑥ 通过工具 / 代码调度
训练范式: ICL / few-shot, Prompting / zero-shot
链接: https://arxiv.org/abs/2211.11559
阅读状态: 待读