# ⑥-C · 从单轮 caption → 会话 & Agent 化 RS CD（TeoChat / ChangeChat / Change-Agent）

CD 任务类型: Referring CD, 变化描述（Captioning）, 变化问答（Change QA）, 多时相 CD（Multi-temporal）, 损毁评估（Damage Assessment）
与 VLM 视觉思考主线关联: RS-VLM R8 + R12 的集大成者（TeoChat）+ L3（Agent 调度层，Change-Agent）。是时序 RS-VLM 赛道未来几年的基准。
代表基座 / 骨干: LLaVA-1.5 + 时序视觉 tokens / LLM 中枢调度 CD 工具链
优先级: P0 · 必读
关键创新: CD 从「固定输入-固定输出」升级为「交互式 + 多任务 + 可调工具」。三个代表：TeoChat——第一个多时相 RS-VLM（N 时相，不限双时相），TeoChatlas 指令集覆盖 6 类时序任务；ChangeChat——多轮对话式 CD，支持链式追问 + referring；Change-Agent——LLM 作中枢，按需调度 CD 模型 / captioner / VQA 工具。
局限 / 残差 / 催生了什么: 需指令微调数据 + LLM 推理成本高 + 细粒度像素精度弱。催生 ⑦ 的 training-free 开放词汇 CD——把工具链中每个组件换成免训练版本。
年份: 2024
我的视角 / 落地价值: TeoChat 是方案的北极星 benchmark——若 training-free 管线能在 xBD / LEVIR-CC 逼近 TeoChat 即有发表级贡献。Change-Agent 的调度层可直接复用，把其 CD 工具换成 SegEarth-OV + SAM + VLM。
方法家族: CLIP-based, Change Captioning, LLM-Agent
机构 / 团队: Stanford（TeoChat，吴恩达组） / ChangeChat / Change-Agent 团队
模态支持: 光学 RGB, 文本 prompt
演进阶段: ⑥ VLM/LLM 驱动 · Change Captioning / Agent（2024-2025）
监督方式: 像素级全监督
训练 / 评测数据集: LEVIR-CC, S2Looking, xBD
阅读状态: 待读

## 核心主题

CD 从「固定输入 → 固定输出」跨举升级为「交互式 + 多任务 + 可调工具」。现实 RS 运营需要的不是固定接口，而是「**问什么答什么、要什么给什么**」。

## 三个代表（按能力扩张排序）

| 层级 | 代表 | 关键突破 | 机构 |
| --- | --- | --- | --- |
| 时序 RS-VLM | **TeoChat** (2024) | 第一个多时相 RS-VLM（N 时相，不限双）；TeoChatlas 覆盖 6 类时序任务（caption / QA / damage / referring / 时序分类 / 时序 grounding） | Stanford（吴恩达组） |
| 多轮对话 | **ChangeChat** (2024) | 链式追问：「这两个时相发生了什么？」→「在哪里？」→「哪些建筑消失了？」 + referring | × |
| LLM-Agent | **Change-Agent** (2024) | LLM 作中枢，按需调度 CD / captioner / VQA 工具；支持开放任务 | × |

## 本质观察

- 前两代架构是「任务固定、模型单一」；这一代的平移是「把 CD 拆成可调工具链」。
- **Agent 化不是模型升级，而是范式切换**：从「端到端模型」→「组合式系统」。

## 共享局限

- 需指令微调数据（TeoChatlas / ChangeChat 指令集成本高）。
- LLM 推理成本高 + 延迟大。
- 细粒度像素精度弱（VLM 本身不擅长 pixel-level mask）。

## 催生了什么

- **⑦ 路线**：把工具链中每个组件换成免训练版本（CLIP/SAM/OVS + VLM zero-shot），形成 training-free 开放词汇 CD。

## 对我方案的意义

- **TeoChat = 北极星 benchmark**。若 training-free 管线能在 xBD / LEVIR-CC 逼近 TeoChat → 有发表级贡献。
- **Change-Agent 的调度层**可直接复用：把其 CD 工具换成 SegEarth-OV + SAM + VLM 即可。
- 要重点读 TeoChat 的**任务定义与评测 protocol**，确保对标条件一致。

## 论文

- TeoChat：[arxiv.org/abs/2410.06234](http://arxiv.org/abs/2410.06234)
- ChangeChat：[arxiv.org/abs/2409.08582](http://arxiv.org/abs/2409.08582)
- Change-Agent：[arxiv.org/abs/2403.19646](http://arxiv.org/abs/2403.19646)