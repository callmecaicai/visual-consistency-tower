# Visual-RFT: Visual Reinforcement Fine-Tuning（2025）

与五阶段关系: III · 语言共形
优先级: P0 · 必读
关键贡献: 提出视觉特有的验证奖励（IoU、所有类别的单一判断、计数等），在小数据（几十到几百样本）下就可以通过 GRPO 显著提升基座的少样本视觉理解能力。
基座 / 起点: Qwen2-VL / Qwen2.5-VL
局限 / 残差 / 它催生了什么: 奖励的表达力受限于人工设计；对「步骤内部的视觉忠实性」不做奖励——与 R10 上的忠实性诊断需要交叉阅读。
年份: 2025
思考载体: bbox/mask 标注, 文本 token
我的视角 / 为什么重要: R1 范式在 VLM 上的最早、最洁净的一个部署。应该先读。
机构 / 团队: Shanghai AI Lab (Liu et al.)
测试时扩展机制: 长 CoT
研究路线: R5 · RL 驱动的视觉推理
范式标签: Framework, Model
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: GRPO / R1-RL
链接: https://arxiv.org/abs/2503.01785
阅读状态: 待读