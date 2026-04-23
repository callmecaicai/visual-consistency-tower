# SNUNet-CD

CD 任务类型: 二值 CD（Binary）
与 VLM 视觉思考主线关联: 作为「CNN 时代终章」存在——之后 CD 整条路线向 Transformer / FM / VLM 迁移。
代表基座 / 骨干: NestedUNet (UNet++) + ECAM（Ensemble Channel Attention Module）
优先级: P2 · 参考
关键创新: 用 UNet++ 的稠密跳连解决深浅特征混融；引入 ECAM 做多尺度通道注意力加权——让纯 CNN 的 CD 网络走到性能天花板。
局限 / 残差 / 催生了什么: 纯 CNN 范式天花板；感受野不够全局。SNUNet 之后社区普遍承认：想再提升必须引入 Transformer。
年份: 2021
方法家族: FCN / U-Net, Siamese CNN
机构 / 团队: Sheng Fang 等 · NUIST
模态支持: 光学 RGB
演进阶段: ③ 空间-时间注意力（2019-2021）
监督方式: 像素级全监督
训练 / 评测数据集: CDD, LEVIR-CD
链接: https://ieeexplore.ieee.org/document/9355573
阅读状态: 待读