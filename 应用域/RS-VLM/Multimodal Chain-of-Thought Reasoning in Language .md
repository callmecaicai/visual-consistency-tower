# Multimodal Chain-of-Thought Reasoning in Language Models（MM-CoT, Zhang 2023）

与五阶段关系: III · 语言共形
优先级: P1 · 重点
关键贡献: 首次将 CoT 显式拆为两段：Rationale Generation（结合图像生成推理链）+ Answer Inference（仅根据 rationale 产答），解决「单阶段 CoT 在小LM 上幻觉加剧」的问题；基础链路线的奠基作品。
基座 / 起点: UnifiedQA / T5-base + DETR 图像特征
局限 / 残差 / 它催生了什么: 视觉信息经过首次编码后就消失，CoT 本身完全在文本内进行——「看一眼然后全程思考都不回头看图」这一残差被 R2 / R3 / R4 后续路线分别接走。
年份: 2023
思考载体: 文本 token
我的视角 / 为什么重要: R1 的洁净起点，值得用来诊断后面所有路线的「视觉参与程度」——MM-CoT 就是【视觉参与=0】的标准零点。
机构 / 团队: Amazon Science
测试时扩展机制: 长 CoT
研究路线: R1 · 文本式 CoT 移植
范式标签: Framework, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: SFT
链接: https://arxiv.org/abs/2302.00923
阅读状态: 待读