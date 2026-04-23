# MVoT: Multimodal Visualization-of-Thought（Li 2025）

与五阶段关系: IV · 生成共形
优先级: P0 · 必读
关键贡献: 首次让模型在推理链中交替输出「文本思考 + 生成中间图像」；在迷宫 / FrozenLake / MiniBehavior 等空间任务上大幅超过纯文本 CoT。Chain-of-Image 的旗舰式作品。
基座 / 起点: Chameleon-7B（统一图文 token）
局限 / 残差 / 它催生了什么: 图像生成代价高，且限于 Chameleon 体量较小的基座；生成的图质量仍是瑞士奠基方式，精度受标志 codec 限制——直接催生 Emu3 / Janus / Visual Planning 等更纯粹视觉的路线。
年份: 2025
思考载体: 文本 token, 生成图像
我的视角 / 为什么重要: P0。这是「生成主体性来承担思考」在组合空间上的首个实证突破点。
机构 / 团队: Microsoft Research / Tsinghua
测试时扩展机制: 图像生成反思, 长 CoT
研究路线: R3 · Thinking with Generated Images
范式标签: Framework, Model
视觉在推理中的角色: ④ 主动被生成作为思考
训练范式: Instruction tuning, SFT
链接: https://arxiv.org/abs/2501.07542
阅读状态: 待读