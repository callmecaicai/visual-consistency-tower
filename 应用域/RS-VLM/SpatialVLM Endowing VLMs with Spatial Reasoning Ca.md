# SpatialVLM: Endowing VLMs with Spatial Reasoning Capabilities（Chen 2024, Google）

与五阶段关系: V · 表征共形
优先级: P0 · 必读
关键贡献: 首次用单目深度 + 开放词汇检测大批量合成「定性 + 定量」空间 VQA 数据（中位数 20、极值 30亿）以解决 VLM 在距离 / 大小 / 方位上的系统性崩坏；让 VLM 第一次获得直接制答米级距离的能力。
基座 / 起点: PaLM-E + 单目深度估计
局限 / 残差 / 它催生了什么: 合成数据受深度估计器系统性误差的约束；未涉及多视图推理——催生 SpatialRGPT / VSI-Bench / Thinking in Space 等后续。
年份: 2024
思考载体: 文本 token
我的视角 / 为什么重要: R7 路线的奠基作；且从你的「视觉主体性」角度看——三维度量是最难被语言合成的一个维度。
机构 / 团队: Google DeepMind
测试时扩展机制: 长 CoT
范式标签: Dataset, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2401.12168
阅读状态: 待读