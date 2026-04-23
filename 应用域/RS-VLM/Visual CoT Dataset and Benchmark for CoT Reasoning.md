# Visual CoT: Dataset and Benchmark for CoT Reasoning（Shao 2024）

与五阶段关系: 跨 III-IV
优先级: P1 · 重点
关键贡献: 首个大规模带 bbox 的多模态 CoT 数据集（43万 VQA pairs）；训练模型在回答前先生成关键区域的 bounding box，再重新聚焦该区域产答——推理链正式带上空间锚点。
基座 / 起点: LLaVA-1.5 / Vicuna
局限 / 残差 / 它催生了什么: bbox 的粒度受 annotation 限制，本质仍是「一次锚点 + 文本 CoT」——产出了 R2 的雏形但仍未进入 o3 级的迭代操作。
年份: 2024
思考载体: bbox/mask 标注, 文本 token, 裁剪/缩放图像
我的视角 / 为什么重要: R1→R2 的过渡作品。这个数据集后面被大量 R2 工作复用，值得当成「视觉 CoT 数据工程」的标杆来读。
机构 / 团队: CUHK / Shanghai AI Lab
测试时扩展机制: 多次感知 / re-look, 长 CoT
研究路线: R1 · 文本式 CoT 移植
范式标签: Benchmark, Dataset, Model
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2403.16999
阅读状态: 待读