# Thinking in Space: How MLLMs See, Remember, and Recall Spaces（VSI-Bench, Yang/Fei-Fei 2024）

与五阶段关系: V · 表征共形
优先级: P0 · 必读
关键贡献: 提出 VSI-Bench（从视频推断空间布局）；给出一个罕见结论：端到端 CoT 在空间推理上会降低性能（与文本推理相反），模型更依赖「心赌地图」而非语言推理。
基座 / 起点: GPT-4o / Gemini / Qwen2-VL 评测
局限 / 残差 / 它催生了什么: 仅是 benchmark，未提供训练方案；开启了「空间思考需要不同于文本思考的机制」这一新课题。
年份: 2024
思考载体: 文本 token
我的视角 / 为什么重要: P0。你「视觉主体」方向的正字标识作品之一——它直接在说：空间推理不能依赖语言。
机构 / 团队: NYU + Stanford (Fei-Fei Li lab)
范式标签: Analysis / 理论, Benchmark, Dataset
视觉在推理中的角色: ⑧ 忠实性 / 诊断对象
训练范式: Prompting / zero-shot
链接: https://arxiv.org/abs/2412.14171
阅读状态: 待读