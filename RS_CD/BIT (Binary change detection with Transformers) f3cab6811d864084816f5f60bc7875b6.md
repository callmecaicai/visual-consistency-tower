# BIT (Binary change detection with Transformers)

CD 任务类型: 二值 CD（Binary）, 建筑 CD
与 VLM 视觉思考主线关联: CD 领域第一次展示「全局语境 > 局部特征」——为后续 CLIP/VLM 引入埋下伏笔。BIT 的 token 思想与 Perceiver / DETR 同源。
代表基座 / 骨干: ResNet-18 + 轻量 Transformer Encoder-Decoder（少量 semantic token）
优先级: P0 · 必读
关键创新: 把 CNN 特征「token 化」（每张图只保留 ~4 个 semantic token），仅在 token 空间跑 Transformer，再反投影回像素。把全局语境引入 CD 而几乎不增计算。
局限 / 残差 / 催生了什么: token 压缩丢失细节；仍是「双时相对齐」范式。催生了纯 Transformer CD（ChangeFormer）和 SAM-CD 的「先分 mask 再比」。
年份: 2021
我的视角 / 落地价值: 读懂 BIT 就读懂了「低 token 数 + Transformer」在 dense prediction 中的潜力——对你理解 VLM 怎样用少量视觉 token 做 CD 推理也直接相关。
方法家族: Hybrid CNN-Transformer
机构 / 团队: Hao Chen 等 · Beihang（LEVIR Lab）
模态支持: 光学 RGB
演进阶段: ④ Transformer 主导（2021-2023）
监督方式: 像素级全监督
训练 / 评测数据集: DSIFN, LEVIR-CD, WHU-CD
链接: https://arxiv.org/abs/2103.00208
阅读状态: 待读