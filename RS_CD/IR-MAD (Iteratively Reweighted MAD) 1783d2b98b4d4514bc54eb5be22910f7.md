# IR-MAD (Iteratively Reweighted MAD)

CD 任务类型: 二值 CD（Binary）
与 VLM 视觉思考主线关联: 展示了「无监督 + 统计变换」的天花板——也正是这个天花板让深度学习 CD 获得了入场券。
代表基座 / 骨干: 典型相关分析（CCA）+ 迭代重加权
优先级: P2 · 参考
关键创新: 迭代重加权扩展 MAD (Multivariate Alteration Detection)，让「不变像素」获得更高权重，自动提纯「变化」子空间。纯无监督。
局限 / 残差 / 催生了什么: 依赖高斯假设；对复杂地物（城市异质区）失效；只能输出连续变化强度图。催生了后续基于深度特征的 Deep Slow Feature Analysis (DSFA) 与无监督深度 CD。
年份: 2007
方法家族: Transform (PCA/MAD/CVA)
机构 / 团队: Allan A. Nielsen · DTU
模态支持: 多光谱
演进阶段: ① 经典 · 代数/变换/PCC（pre-2015）
监督方式: 无监督（经典）
链接: https://www2.imm.dtu.dk/pubdb/edoc/imm5362.pdf
阅读状态: 待读