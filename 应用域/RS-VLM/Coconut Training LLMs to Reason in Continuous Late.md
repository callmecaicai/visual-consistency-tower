# Coconut: Training LLMs to Reason in Continuous Latent Space（Hao 2024）

与五阶段关系: 谱系外 / 一般理论
优先级: P0 · 必读
关键贡献: 用「最后一层隐状态作为下一步输入」替换文本 token，构造在潜空间而非词表空间的 CoT；证明在潜空间推理可以同时探索多条推理分支（breadth-first）。R4 基础文献。
基座 / 起点: GPT-2 / Llama 类 LM（潜向量回套）
局限 / 残差 / 它催生了什么: 文本侧 LLM，未直接涉及视觉——但正是它催生了 LVR / Monet 把潜空间思考搜入视觉嵌入的理论路径。
年份: 2024
思考载体: 潜向量
我的视角 / 为什么重要: P0。你要评估「视觉潜空间思考」的理论合理性，必须先打实 Coconut 的代理可视化方法。
机构 / 团队: Meta FAIR / UCSD
测试时扩展机制: 潜空间迭代
研究路线: R4 · Latent Visual Reasoning
范式标签: Analysis / 理论, Model
视觉在推理中的角色: ⑤ 在潜空间直接参与
训练范式: SFT
链接: https://arxiv.org/abs/2412.06769
阅读状态: 待读