# Long Context Transfer from Language to Vision（LongVA, 2024）

与五阶段关系: III · 语言共形
优先级: P2 · 参考
关键贡献: 证明开发长上下文视频 VLM 只需要在 LLM 侧预训练长上下文，按部就班迁移到视觉即可；为视频 R1 等提供了长历险基座基础。
基座 / 起点: Qwen2 long-context LLM
局限 / 残差 / 它催生了什么: 仍以文本为推理主轴；视频中的事件因果关系本身仍仍是长相寄生比季。
年份: 2024
思考载体: 文本 token
我的视角 / 为什么重要: R8 基座基础，背景性读物。
机构 / 团队: NTU
测试时扩展机制: 多次感知 / re-look
范式标签: Analysis / 理论, Model
视觉在推理中的角色: ① 仅输入被语言化
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2406.16852
阅读状态: 待读