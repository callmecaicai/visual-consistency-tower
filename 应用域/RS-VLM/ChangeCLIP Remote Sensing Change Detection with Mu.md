# ChangeCLIP: Remote Sensing Change Detection with Multimodal Vision-Language Representation Learning（Dong 2024, ISPRS JPRS）

与五阶段关系: III · 语言共形
优先级: P0 · 必读
关键贡献: 首次系统地把 CLIP 多模态预训练表征引入 RS 变化检测；用语言先验消歧「表观变化 vs 真实语义变化」；在 LEVIR-CD / SYSU-CD / S2Looking 多数据集 SoTA
基座 / 起点: CLIP
局限 / 残差 / 它催生了什么: 不是 VLM，只是 VL 表征 + CD head；没有推理链；开放词汇能力仍受限于 CLIP 预训练域
年份: 2024
思考载体: 双时相图像对, 变化掩码
我的视角 / 为什么重要: 把 L3 (CLIP) 作为 CD 桥接层的代表作；与你的 VLM+SAM 方案互为镜像——VLM+SAM 是「用 VLM 做语义 + SAM 做几何」，ChangeCLIP 是「用 CLIP 做对齐 + CD head 做几何」。这张对照图决定了 R12 的两条主干道
机构 / 团队: 武汉大学
研究路线: R12 · 变化检测 · 双时相 / 多时相 RS 视觉思考
范式标签: Change Detection, Model
视觉在推理中的角色: ② 被动看但只读一次
训练范式: SFT
链接: https://www.sciencedirect.com/science/article/pii/S0924271624000042
阅读状态: 待读

核心直觉：RS 变化检测的核心难点是**区别「无关变化」（光照、季节、配准误差）与「真实语义变化」**。语言先验（CLIP text encoder）可以为每个像素/区域提供「该类物体通常不变」的先验分布。

架构：

- 双时相图像分别编码（共享 CLIP ViT）
- 用 text prompt（类别名）调制视觉特征
- 差分 + CD head 输出变化掩码