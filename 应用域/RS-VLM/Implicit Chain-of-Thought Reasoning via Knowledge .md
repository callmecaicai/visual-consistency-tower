# Implicit Chain-of-Thought Reasoning via Knowledge Distillation（Deng 2023）

与五阶段关系: 谱系外 / 一般理论
优先级: P1 · 重点
关键贡献: 用 teacher 的显式 CoT 隐层状态蒸馕 student 的一步向前；「先显式，再内化」的范式；为 R4 提供了「从显式到潜式」的路径方案。
基座 / 起点: GPT-2 small / Llama
局限 / 残差 / 它催生了什么: 依赖 teacher 、需要蒸馕管道；在 VLM 上直接复制的按部就班方案尚待验证。
年份: 2023
思考载体: 潜向量
我的视角 / 为什么重要: 和 Coconut / Recurrent-Depth 三份合读，R4 的三种不同理论革商说完了。
机构 / 团队: Harvard
测试时扩展机制: 潜空间迭代
研究路线: R4 · Latent Visual Reasoning
范式标签: Analysis / 理论, Model
视觉在推理中的角色: ⑤ 在潜空间直接参与
训练范式: Distillation, SFT
链接: https://arxiv.org/abs/2311.01460
阅读状态: 待读