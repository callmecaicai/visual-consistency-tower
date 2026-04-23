# Chameleon: Mixed-Modal Early-Fusion Foundation Models（Meta 2024）

与五阶段关系: IV · 生成共形
优先级: P1 · 重点
关键贡献: 第一个开源的真正统一 token 的 early-fusion 多模态基模 — 图像和文本共享自回归空间，为后续所有 R3 路线（MVoT / TwGI / Janus 等）提供基座。
基座 / 起点: Pretrain from scratch（统一图文 token）
局限 / 残差 / 它催生了什么: 图像 tokenizer 带来信息损失；与扩散模型对比图像质量仍有 gap——催生 Janus / Janus-Pro / Emu3 在理解和生成上的解耦设计。
年份: 2024
思考载体: 文本 token, 生成图像
我的视角 / 为什么重要: R3 路线的「可行性证明」基座文献；作为了解 R3 的技术栈必读。
机构 / 团队: Meta FAIR
测试时扩展机制: 图像生成反思
研究路线: R3 · Thinking with Generated Images
范式标签: Infrastructure, Model
视觉在推理中的角色: ④ 主动被生成作为思考
训练范式: Pretrain from scratch
链接: https://arxiv.org/abs/2405.09818
阅读状态: 待读