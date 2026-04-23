# LHRS-Bot: Empowering Remote Sensing with VGI-Enhanced Large Multimodal Language Model（Muhtar 2024, ECCV）

与五阶段关系: III · 语言共形
优先级: P1 · 重点
关键贡献: 利用 VGI（志愿地理信息，如 OpenStreetMap）做弱监督，构造大规模 RS image-text 对 LHRS-Align（1.15M）与 LHRS-Instruct（多任务指令）；设计 vision perceiver 处理高分辨率 RS 图
基座 / 起点: LLaVA + ViT-L
局限 / 残差 / 它催生了什么: 仍主要是 R1 范式，未引入显式的视觉回环机制；但 perceiver 架构为高分辨率处理开了口
年份: 2024
思考载体: 文本 token, 裁剪/缩放图像
我的视角 / 为什么重要: RS instruction 数据的「规模化关口」——从 GeoChat 的 318K 跳到百万级；VGI 监督的思路极聪明，把地球本身的人类标注（OSM）转为 pretrain 信号。perceiver 架构预示了向 R2（瓦片/滑窗）靠拢
机构 / 团队: 南京大学
研究路线: R8 · 遥感专用 VLM（RS-VLM）
范式标签: Dataset, Model, RS-VLM
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: Instruction tuning
链接: https://arxiv.org/abs/2402.02544
阅读状态: 待读

LHRS-Bot 的两个关键创新：

1. **VGI-Enhanced 数据**：把 OpenStreetMap 作为弱 caption 来源，与 Google Earth 图像配对
2. **Vision Perceiver**：在 ViT 和 LLM 之间插入 perceiver resampler，压缩高分辨率 token

与你的工作的连接：perceiver 的本质是一种「有限 token 预算下的选择性感知」——这正是 R2 路径的物理前置。