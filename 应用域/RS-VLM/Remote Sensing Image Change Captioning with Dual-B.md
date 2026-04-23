# Remote Sensing Image Change Captioning with Dual-Branch Transformers / RSICCformer（Liu 2022-2024, TGRS）

与五阶段关系: 谱系外 / 一般理论
优先级: P1 · 重点
关键贡献: 首个 RS 变化描述（change captioning）模型；双分支 Transformer 分别编码 T1/T2 然后交叉注意；发布 LEVIR-CC 数据集（10077 对图像 + 50385 条描述），奠定「变化描述」作为独立任务
基座 / 起点: Transformer + ResNet
局限 / 残差 / 它催生了什么: 仅 caption 无推理链；尺度单一；但直接催生了 Change-Agent / PromptCC / Chg2Cap / SITSCC 等一整代 change captioning × VLM 工作
年份: 2023
思考载体: 双时相图像对, 文本 token
我的视角 / 为什么重要: RS CD 从「二值/多类掩码」向「结构化语言描述」转型的分水岭——这正是打开 R12 × R1/R8 通道的钥匙。没有 LEVIR-CC，就没有后续 Change-Agent 这类 agent 化 CD
机构 / 团队: 北京航空航天大学 / LEVIR 组
研究路线: R12 · 变化检测 · 双时相 / 多时相 RS 视觉思考
范式标签: Change Detection, Dataset, Model
视觉在推理中的角色: ① 仅输入被语言化
训练范式: Pretrain from scratch, SFT
链接: https://arxiv.org/abs/2212.01843
阅读状态: 待读

LEVIR-CC 的意义 > 模型本身：

- 10077 对 1024×1024 的双时相图（Google Earth，20 个城市）
- 50385 条人工 caption，每对 5 条
- 首次把「变化」从像素任务抬升到语言任务

RSICCformer 架构：

- Dual-branch ViT：T1/T2 独立编码
- Cross-attention 模块：对齐并差分
- Transformer decoder：生成 caption