# ViperGPT: Visual Inference via Python Execution for Reasoning（Surís 2023）

与五阶段关系: 跨 III-IV
优先级: P1 · 重点
关键贡献: LLM 生成 Python 程序调用一组 pre-trained 视觉模型（检测、分割、深度估计等）；「视觉理解 = 程序组合」的深切口号。奠基 R6 范式。
基座 / 起点: GPT-3.5 + GLIP / X-VLM / MiDaS 工具箱
局限 / 残差 / 它催生了什么: 程序输出被固定 API 约束，模型自己不“看”；不适合 open-ended 视觉语义——这一残差被 CogAgent / UI-TARS / 端到端 VLA 接走。
年份: 2023
思考载体: 外部工具, 生成代码
我的视角 / 为什么重要: R6 的危机作品。从技术层面看，它也是「将视觉切割为工具」这种「前-主体化」视觉理解的极致样本。
机构 / 团队: Columbia University
测试时扩展机制: 外部工具调用
研究路线: R6 · Visual Agent · Program-as-Thought
范式标签: Agent, Framework
视觉在推理中的角色: ⑥ 通过工具 / 代码调度
训练范式: Agent framework（无训练）, Prompting / zero-shot
链接: https://arxiv.org/abs/2303.08128
阅读状态: 待读