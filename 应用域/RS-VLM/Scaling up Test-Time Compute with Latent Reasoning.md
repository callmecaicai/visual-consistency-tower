# Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach（Geiping 2025）

与五阶段关系: 谱系外 / 一般理论
优先级: P0 · 必读
关键贡献: 用递归层在潜空间迭代代替长 CoT；test-time compute 直接等于「运行多少次递归层」——不需要 token 作为思考介质。和 Coconut 一起支撑了「潜空间思考」的理论框架。
基座 / 起点: 递归层 Transformer（35B）
局限 / 残差 / 它催生了什么: 需要重塑架构，无法无缝套用在现有 LLaVA 系基座上；对多模态的近期适配概忽——Monet / LVR 是对此的 VLM 具象化。
年份: 2025
思考载体: 潜向量
我的视角 / 为什么重要: 与 Coconut 配读，理解「为什么潜空间迭代相当于 CoT」的条件与边界。
机构 / 团队: ELLIS Tuebingen / Max Planck
测试时扩展机制: 潜空间迭代
研究路线: R4 · Latent Visual Reasoning
范式标签: Analysis / 理论, Model
视觉在推理中的角色: ⑤ 在潜空间直接参与
训练范式: Pretrain from scratch
链接: https://arxiv.org/abs/2502.05171
阅读状态: 待读