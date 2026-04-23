# Test-time Scaling over Perception: Grounding Paradox · 潜在探索作品（2025）

与五阶段关系: 跨 III-IV
优先级: P1 · 重点
关键贡献: 系统证明「将 test-time compute 投入感知步骤」比投入推理步骤更划算；提出“grounding paradox”——大多数 VLM 的短板不在推理而在感知。
基座 / 起点: LLaVA 类 VLM + 感知述搜索
局限 / 残差 / 它催生了什么: 仍为分析型工作，缺少配套上预可以落地的训练策略；催生了与 RL 的联合方案。
年份: 2025
思考载体: 文本 token, 裁剪/缩放图像
我的视角 / 为什么重要: 你已经收藏 Test-time Scaling over Perception: Resolving the Grounding Paradox in Thinking with Images (https://www.notion.so/Test-time-Scaling-over-Perception-Resolving-the-Grounding-Paradox-in-Thinking-with-Images-7e8aa1f153a241f38b1e753e33e4b6a3?pvs=21)；它是 R9 路线最明确的「为什么要做感知搜索」陈述。
机构 / 团队: 开源社区
测试时扩展机制: Best-of-N, 多模态验证器, 多次感知 / re-look
研究路线: R9 · 测试时搜索 · 验证器
范式标签: Analysis / 理论, Framework
视觉在推理中的角色: ⑧ 忠实性 / 诊断对象
训练范式: Agent framework（无训练）
链接: https://arxiv.org/abs/2505.22881
阅读状态: 待读