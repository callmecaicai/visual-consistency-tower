# STANet（+ LEVIR-CD 数据集）

CD 任务类型: 二值 CD（Binary）, 建筑 CD
与 VLM 视觉思考主线关联: LEVIR-CD 是下游所有 RS-CD 论文（含 ChangeCLIP、SAM-CD、Change-Agent、你的 VLM+SAM 方案）的公用跑分集——所以本条也是 VLM 库众多条目的「数据集母体」。
代表基座 / 骨干: ResNet-18 + BAM/PAM（Basic/Pyramid Attention Module）
优先级: P0 · 必读
关键创新: (1) 提出 LEVIR-CD，至今最重要的高分 RS 建筑 CD 评测集（637 对 1024×1024 图像、7 万建筑变化）；(2) BAM/PAM 空间-时间注意力模块，显式建模跨时相像素对关系。
局限 / 残差 / 催生了什么: 注意力计算量大；仅局部感受野扩展，未实现真正全局建模。催生了 BIT 用 Transformer 做全局注意力。
年份: 2020
我的视角 / 落地价值: LEVIR-CD 是「CD 领域的 ImageNet」——没读过这篇不算入门。所有 training-free 方案的零样本评估都从 LEVIR-CD 开始。
方法家族: Siamese CNN, Spatial-Temporal Attention
机构 / 团队: Hao Chen, Zhenwei Shi · Beihang University（LEVIR Lab）
模态支持: 光学 RGB
演进阶段: ③ 空间-时间注意力（2019-2021）
监督方式: 像素级全监督
训练 / 评测数据集: LEVIR-CD
链接: https://www.mdpi.com/2072-4292/12/10/1662
阅读状态: 待读