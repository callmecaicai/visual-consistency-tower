# RSGPT: A Remote Sensing Vision Language Model and Benchmark（Hu 2023）

与五阶段关系: III · 语言共形
优先级: P1 · 重点
关键贡献: 早期 RS VQA / captioning VLM；构造并发布 RSICap（2585 张高质量人工标注 caption）与 RSIEval 评测集；证明了 instruction tuning 可迁移到 RS
基座 / 起点: InstructBLIP + Vicuna
局限 / 残差 / 它催生了什么: 规模小；单轮对话；无区域级能力；无 grounding；催生了 RSICap 评测标准与 RS-VLM 浪潮
年份: 2023
思考载体: 文本 token
我的视角 / 为什么重要: RS-VLM 的「零代」——证明迁移路径可行，但也暴露了数据稀缺问题。RSICap 至今仍是 RS-VLM caption 评测的常用集
机构 / 团队: 武汉大学
研究路线: R8 · 遥感专用 VLM（RS-VLM）
范式标签: Benchmark, Dataset, Model, RS-VLM
视觉在推理中的角色: ① 仅输入被语言化
训练范式: Instruction tuning
链接: https://arxiv.org/abs/2307.15266
阅读状态: 待读

RSGPT 的历史地位 > 技术贡献：

- 2023 年做 RS-VLM 的首发作品之一
- RSICap 数据集至今仍是评测标准
- InstructBLIP 架构对 RS 任务的可行性验证