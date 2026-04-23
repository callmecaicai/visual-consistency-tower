# V*: Guided Visual Search as a Core Mechanism in Multimodal LLMs（Wu & Xie 2023）

与五阶段关系: III · 语言共形
优先级: P0 · 必读
关键贡献: 明确提出「视觉搜索作为 VLM 核心机制」：CLIP 的全图编码在高分辨率、小目标、细粒度上崩坏，因此需要显式搜索；还提出 V*Bench 提示这一问题。R2 路线的动机文献。
基座 / 起点: CLIP + LLaVA + 视觉搜索器
局限 / 残差 / 它催生了什么: 搜索策略由规则 + 辅助检测器提供，模型本身没学会「何时整体眼何时放大」——这一残差被 ZoomEye / DeepEyes / o3 用端到端训练接走。
年份: 2023
思考载体: 文本 token, 裁剪/缩放图像
我的视角 / 为什么重要: R2 流派的「理论奠基书」——它直接用 CLIP-blindness 的数据证据给出了「为什么必须视觉思考」。
机构 / 团队: UCSD / NYU (Wu, Saining Xie)
测试时扩展机制: 外部工具调用, 多次感知 / re-look
范式标签: Framework, Model
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2312.14135
阅读状态: 待读