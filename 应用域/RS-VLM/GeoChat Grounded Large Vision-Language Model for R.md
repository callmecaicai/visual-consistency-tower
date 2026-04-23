# GeoChat: Grounded Large Vision-Language Model for Remote Sensing（Kuckreja 2024, CVPR）

与五阶段关系: III · 语言共形
优先级: P0 · 必读
关键贡献: 第一个 grounded multimodal model for RS；支持区域级描述、RS-VQA、visual grounding、多轮对话；发布 GeoChat-Instruct 数据集（318K 指令对）
基座 / 起点: LLaVA-1.5 + CLIP ViT-L
局限 / 残差 / 它催生了什么: 视觉思考很浅——只有 R1 式的文本 CoT，没有 zoom / tile / 多次感知；视觉塔仍是通用 CLIP 非 RS FM，丢失光谱与尺度先验；催生了 LHRS-Bot / VHM / H2RSVLM / GeoReason 等一系列后继工作
年份: 2024
思考载体: bbox/mask 标注, 文本 token
我的视角 / 为什么重要: RS-VLM 的事实起点与 baseline；同时暴露了两个关键问题——(a) 通用 CLIP 视觉塔的 RS 不适配，(b) R1 路线在 RS 超大图上的先天局限（无法 zoom 细节）。这两个问题分别指向 R7 和 R2
机构 / 团队: MBZUAI
研究路线: R8 · 遥感专用 VLM（RS-VLM）
范式标签: Dataset, Model, RS-VLM
视觉在推理中的角色: ① 仅输入被语言化
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2311.15826
阅读状态: 待读

GeoChat = 把 LLaVA-1.5 直接搬到 RS。核心工程贡献：

- **指令数据合成**：从 NWPU-RESISC45, FAIR1M, SAMRS 等构造 318K 多任务指令
- **Grounding 支持**：<coord> token 让模型输出区域框
- **spatial-aware 训练**：支持 region-level question answering

病理诊断：

- 输入 512×512 就已经吃力，真实 RS tile 10K+ 像素完全无解
- 通用 CLIP 对 SAR / 多光谱零先验
- 复杂推理完全仰仗 LLM 的 R1 式文本 CoT，缺视觉回环