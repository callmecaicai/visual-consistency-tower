# FC-EF / FC-Siam-conc / FC-Siam-diff (Daudt 2018)

CD 任务类型: 二值 CD（Binary）, 建筑 CD
与 VLM 视觉思考主线关联: 与 VLM 库 R7/R8 的「让 CNN/FM 学会看 RS」是同一逻辑起点——只是本库聚焦「双时相差异建模」，VLM 库聚焦「单时相表征」。
代表基座 / 骨干: 基于 U-Net 的三种变体（EF / Siam-conc / Siam-diff）
优先级: P0 · 必读
关键创新: 首次将端到端深度学习系统性地引入 CD。三种融合策略：Early Fusion（FC-EF）在输入端拼接双时相；Siam-conc 在编码器后拼接特征；Siam-diff 在编码器后取特征差——奠定了 CD 网络的「三大融合范式」。
局限 / 残差 / 催生了什么: 感受野受限（纯 CNN）；对伪变化（季节、光照）敏感；模型容量小。催生了 SNUNet（稠密跳连）、STANet（注意力）、BIT（Transformer）——都是在回答「如何比 Siam-diff 更好地融合双时相特征」。
年份: 2018
我的视角 / 落地价值: CD 深度学习史的「起点论文」。Siam-diff 至今仍是大多数新方法的 baseline——你的方案也必须与之对标。
方法家族: FCN / U-Net, Siamese CNN
机构 / 团队: Rodrigo Caye Daudt 等 · ONERA / Télécom ParisTech
模态支持: 光学 RGB
演进阶段: ② 早期 DL · Siamese/FCN（2015-2019）
监督方式: 像素级全监督
训练 / 评测数据集: OSCD
链接: https://arxiv.org/abs/1810.08462
阅读状态: 待读