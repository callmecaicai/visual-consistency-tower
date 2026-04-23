# Eyes Wide Shut? Exploring the Visual Shortcomings of MLLMs（MMVP, Tong 2024）

与五阶段关系: 谱系外 / 一般理论
优先级: P0 · 必读
关键贡献: 首次系统性地诊断「CLIP-blindness」：找出人能一眼分辨但 CLIP 表征几乎相同的视觉 pair，并证明基于 CLIP 的 VLM 在这些 pair 上系统性跳伤；表明 VLM 的「感知瓶颈」主要来自视觉 encoder 而不是 LLM。
基座 / 起点: CLIP + GPT-4V / LLaVA 评测
局限 / 残差 / 它催生了什么: 只诊断不给方案；催生了 DINOv2+CLIP hybrid encoder、SigLIP、高分辨率 VLM、R2 的「多次感知」一系列答案。
年份: 2024
思考载体: 文本 token
我的视角 / 为什么重要: P0。在你的五阶段话语里——MMVP 是【阶段 III 残差的直接实证】：CLIP 共形的视觉将纹理/方向/数量等特征利估没编进去。
机构 / 团队: NYU / Meta FAIR (Xie et al.)
研究路线: R10 · 忠实性 · 机制 · 诊断
范式标签: Analysis / 理论, Benchmark
视觉在推理中的角色: ⑧ 忠实性 / 诊断对象
训练范式: Prompting / zero-shot
链接: https://arxiv.org/abs/2401.06209
阅读状态: 待读