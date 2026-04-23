# OpenAI o3 / o4-mini — Thinking with Images（OpenAI 2025-04）

与五阶段关系: 跨 III-IV
优先级: P0 · 必读
关键贡献: 第一个在思维链内部 native 地调用 crop/zoom/rotate 等图像工具的产品级模型；把「感知」本身推上 test-time compute 的新轴。合成图像与文本推理的边界，在多模态 benchmark 上新 SOTA。
基座 / 起点: o-series reasoning 模型 + native image tool-use
局限 / 残差 / 它催生了什么: 闭源，机制不明；工具操作仍是仿仿外部的「旋转 / 裁剪」，而非模型内部的表征级操作——R4 路线对此直接抽质疑。催生 R2 的开源复刻浪潮（DeepEyes / Visual Sketchpad / Monet）。
年份: 2025
思考载体: 外部工具, 文本 token, 裁剪/缩放图像
我的视角 / 为什么重要: R2 的旗舰，所有开源 R2 / R5 工作都以它为隐性比较线。方法论层面的主线对标点。
机构 / 团队: OpenAI
测试时扩展机制: 外部工具调用, 多次感知 / re-look, 自我修正 / self-refine, 长 CoT
范式标签: Framework, Model
视觉在推理中的角色: ③ 主动被操作（zoom/crop/mark）
训练范式: GRPO / R1-RL, SFT
链接: https://openai.com/index/thinking-with-images/
阅读状态: 待读