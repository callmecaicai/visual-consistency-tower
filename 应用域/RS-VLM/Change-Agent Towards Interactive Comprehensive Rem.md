# Change-Agent: Towards Interactive Comprehensive Remote Sensing Change Interpretation and Analysis（Liu 2024, TGRS）

与五阶段关系: III · 语言共形
优先级: P0 · 必读
关键贡献: 首次将 LLM 作为 controller 编排 RS 变化解译工具链（CD 模型 + change captioning + QA）；支持多轮交互式分析；发布 LEVIR-MCI 多任务 CD 数据集
基座 / 起点: LLM controller + 专业 CD / captioning 模型
局限 / 残差 / 它催生了什么: 仍依赖成品 CD 模型产出 mask，LLM 不直接「看」像素；Agent 规划是离散的，缺连续视觉回环
年份: 2024
思考载体: 双时相图像对, 变化掩码, 外部工具, 文本 token
我的视角 / 为什么重要: R12 × R6 的典型交叉点；证明「Agent 化 CD」可行；与你的 VLM+SAM 免训练 CD 方案同宗同源——都走 Program-as-Thought 路线。区别：Change-Agent 仍依赖有监督 CD 模型，你的方案用 SAM + VLM 零监督开放词汇，后者是更前沿的进化
机构 / 团队: 北京航空航天大学
测试时扩展机制: 外部工具调用, 多次感知 / re-look
研究路线: R12 · 变化检测 · 双时相 / 多时相 RS 视觉思考
范式标签: Agent, Change Detection, Framework, RS-VLM
视觉在推理中的角色: ⑥ 通过工具 / 代码调度
训练范式: Agent framework（无训练）
链接: https://arxiv.org/abs/2403.19646
阅读状态: 待读

Change-Agent 三组件：

- **CI Model**：Change Interpretation，做 mask + captioning
- **LLM Planner**：任务规划 + 多轮对话
- **Tool APIs**：检测变化、计数、分类、对象级问答

与你方案 [VLM+SAM 免训练开放词汇变化检测：视觉上下文学习引导方案](https://www.notion.so/VLM-SAM-4e5748d64800821f84be013b8e9b517d?pvs=21) 的对照：

| 维度 | Change-Agent | 你的方案 |
| --- | --- | --- |
| CD 工具 | 有监督 CI model | SAM（零监督分割） |
| 语义 | 预定义类别 | VLM 开放词汇 |
| 训练成本 | 需 CI 训练 | 完全免训练 |
| 主体性 | LLM 调工具 | VLM 直接做上下文学习 |