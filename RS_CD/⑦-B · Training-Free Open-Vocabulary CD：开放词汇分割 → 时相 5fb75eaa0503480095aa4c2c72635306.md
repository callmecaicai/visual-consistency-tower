# ⑦-B · Training-Free Open-Vocabulary CD：开放词汇分割 → 时相差分（SegEarth-OV / Seg2Change / AdaptOVCD）

CD 任务类型: Referring CD, 二值 CD（Binary）, 语义 CD（Semantic）
与 VLM 视觉思考主线关联: RS-VLM 主线 R12（开放词汇桥梁）+ L1/L2（CLIP/SAM 接口）+ R13（免训练）。SegEarth-OV 的 AlignEarth 还打通了 SAR 模态，扩展了模态底座。
代表基座 / 骨干: 开放词汇分割模型（CAT-Seg / SegEarth-OV）+ SAM 精修 + 自适应融合
优先级: P0 · 必读
关键创新: 用开放词汇语义分割（OVS）模型对两时相分别推理 → 差分/融合 → 变化 mask。完全免训练 + 开放类别 + 支持语言 referring。三个关键工作：SegEarth-OV（奠基组件：SimFeatUp 无监督高分辨率恢复 + Global Bias Alleviation 去 [CLS] 偏差 + AlignEarth 光学→SAR 蒸馏，17 光学+8 SAR SOTA）；Seg2Change（直接把 CAT-Seg/SegEarth-OV 适配成 CD，时相间 mask 一致性分析 + SAM 精修）；AdaptOVCD（自适应融合流程：CLIP 语义图差分 + 阈值 + SAM 精修，形成完整 pipeline）。
局限 / 残差 / 催生了什么: 对「外观变、语义同」（季节/光照）和「语义变、外观同」（crop type）仍有盲区；VLM 环节缺失，不直接输出自然语言描述——催生下一代「OVS + VLM」融合方案。
年份: 2025
我的视角 / 落地价值: 这条路直接可作为方案的后端——SegEarth-OV 做双时相分割 → 差分 → SAM 精修 → 接 VLM 做 caption。管线已齐，贡献空间在「管线末端的语言描述」和「管线级评测」（在 LEVIR-CC 逼近 TeoChat）。
方法家族: CLIP-based, Open-Vocabulary CD, SAM-based, Training-Free CD
机构 / 团队: Earth-Insights lab / Seg2Change 团队 / AdaptOVCD 团队
模态支持: SAR, 光学 RGB, 多光谱, 文本 prompt
演进阶段: ⑦ 零监督 · 开放词汇 · Referring CD（2025+）
监督方式: 零监督 / Training-free
训练 / 评测数据集: GVLM-CD, LEVIR-CD, SECOND, WHU-CD
阅读状态: 待读

## 核心主题

**开放词汇分割 → 时相差分**。完全免训练 + 开放类别 + 支持语言 referring。与 ⑦-A（定位器驱动）互补，这条是**语义驱动**。

## 管线框架

```jsx
Image_A ─→ OVS (e.g. SegEarth-OV) ─→ semantic_map_A
Image_B ─→ OVS                    ─→ semantic_map_B
                ↓ 差分 / 一致性分析
                    change_coarse
                ↓ SAM 精修
                    change_fine
                ↓ （可选）VLM caption
                    change_description
```

## 三个关键工作

| 代表 | 定位 | 核心贡献 |
| --- | --- | --- |
| **SegEarth-OV** (2025) | 奠基组件 | SimFeatUp（无监督高分辨率恢复）+ Global Bias Alleviation（去 [CLS] 偏差）+ AlignEarth（光学→SAR 蒸馏）。17 光学 + 8 SAR SOTA |
| **Seg2Change** (2025) | 适配层 | 直接把 CAT-Seg / SegEarth-OV 的分割输出适配成 CD，时相间 mask 一致持性分析 + SAM 精修 |
| **AdaptOVCD** (2025) | 融合层 | 自适应融合流程：CLIP 语义概率图差分 + 阈值 + SAM 精修 → 完整 training-free pipeline |

## 本质观察

- OVS 的三大天然短板：低分辨率 · 全局偏差 · 跨模态鸿沟（SAR/光学）。
- 三篇各攻一块：SegEarth-OV 攻**特征质量** · Seg2Change 攻**整合流程** · AdaptOVCD 攻**融合策略**。
- 三篇合起来已经形成完整的 training-free OVCD 技术栈。

## 局限

- 「外观变、语义同」（季节、光照、阴影）容易误报。
- 「语义变、外观同」（crop type 切换）精度依赖 OVS 类别粒度。
- **VLM 环节缺失**——不直接输出自然语言描述。这是空白。

## 对我方案的意义

- **直接可用作方案后端**：SegEarth-OV 做分割 → 差分 → SAM 精修 → 接 VLM 做 caption。
- 我的贡献空间集中在两点：
    1. **管线末端的语言描述**（补上 VLM 环节）。
    2. **管线级评测**（在 LEVIR-CC / xBD 逼近监督版 TeoChat）。
- 组合⑦-A：SAM Everything 负责实例变化、OVS 负责语义变化、VLM 负责语言描述 → 三件套。

## 论文

- SegEarth-OV：[arxiv.org/abs/2508.18067](http://arxiv.org/abs/2508.18067)
- Seg2Change：2025 (待填)
- AdaptOVCD：2025 (待填)