# ChangeFormer

CD 任务类型: 二值 CD（Binary）, 建筑 CD
与 VLM 视觉思考主线关联: 让「预训练 Transformer → 迁移到 CD」的路径正式打开；直接承接 VLM 库 R7「RS FMs」的思路。
代表基座 / 骨干: SegFormer 的 MiT encoder + MLP decoder
优先级: P0 · 必读
关键创新: 彻底放弃 CNN backbone，改用分层 Transformer (MiT)；通过 Siamese 架构差分后统一解码，实现 FC-Siam-diff 的 Transformer 升级版。
局限 / 残差 / 催生了什么: 训练数据饥渴；缺少语义先验；仍需标注变化标签。催生了 SAM-CD——「如果能蹭 SAM 的分割先验，是不是可以免大部分标注？」
年份: 2022
我的视角 / 落地价值: ChangeFormer 是「纯 Transformer CD」的代表——比较它与你的 VLM+SAM 方案，可以直观展示从有监督→零监督的跃迁。
方法家族: Pure Transformer
机构 / 团队: Wele Gedara Chaminda Bandara, Vishal Patel · Johns Hopkins
模态支持: 光学 RGB
演进阶段: ④ Transformer 主导（2021-2023）
监督方式: 像素级全监督
训练 / 评测数据集: DSIFN, LEVIR-CD
链接: https://arxiv.org/abs/2201.01293
阅读状态: 待读