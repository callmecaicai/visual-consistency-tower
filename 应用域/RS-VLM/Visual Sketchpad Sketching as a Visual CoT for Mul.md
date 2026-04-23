# Visual Sketchpad: Sketching as a Visual CoT for Multimodal LMs（Hu 2024, NeurIPS）

与五阶段关系: 跨 III-IV
优先级: P1 · 重点
关键贡献: 让 VLM 在解几何/图论/游戏问题时先生成 Python 代码画辅助草图，再根据草图正产答——「画了再想」。R2↔R3 的交叉具象化。
基座 / 起点: GPT-4o + matplotlib / networkx 等绘图库
局限 / 残差 / 它催生了什么: 从头到尾依赖 GPT-4o 的编程能力 + 外部 Python 运行环境；本身不训练模型——直接催生 MVoT / TwGI 一类「把画图能力内化」的 R3 路线。
年份: 2024
思考载体: 文本 token, 生成代码, 生成图像
我的视角 / 为什么重要: 把「画草图帮思考」这件事从模糊提到实证的作品；是 R2/R3 边界的关键档案。
机构 / 团队: University of Washington / Allen Institute
测试时扩展机制: 图像生成反思, 外部工具调用, 长 CoT
范式标签: Framework, Prompting
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: Agent framework（无训练）, Prompting / zero-shot
链接: https://arxiv.org/abs/2406.09403
阅读状态: 待读