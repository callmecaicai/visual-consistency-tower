# Set-of-Mark Prompting Unleashes Visual Grounding in GPT-4V（Yang 2023）

与五阶段关系: III · 语言共形
优先级: P1 · 重点
关键贡献: 先用 SAM 分割为每个区域打数字 mark，再让 VLM 直接按「#3」指代物体——让 VLM 首次拥有了可靠的「指认」能力。是 R2 与 R3 之间最廉价有效的桥。
基座 / 起点: GPT-4V + SAM/SEEM 分割
局限 / 残差 / 它催生了什么: mark 由外部 SAM 提供，模型自己不会生成 mark；这一残差被 GLaMM / LISA / Ferret 主动包含 mask/bbox 产出的模型补齐。
年份: 2023
思考载体: bbox/mask 标注, 文本 token
我的视角 / 为什么重要: R2 内部「最低成本设计」的代表；任何 prompt-time 的视觉思考都需要和 SoM 比例尺。
机构 / 团队: Microsoft Research
测试时扩展机制: 外部工具调用
范式标签: Framework, Prompting
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: Prompting / zero-shot
链接: https://arxiv.org/abs/2310.11441
阅读状态: 待读