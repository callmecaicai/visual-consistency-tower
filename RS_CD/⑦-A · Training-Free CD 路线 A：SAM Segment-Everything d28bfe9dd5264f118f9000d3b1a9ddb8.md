# ⑦-A · Training-Free CD 路线 A：SAM Segment-Everything + Mask 对应匹配（AnyChange）

CD 任务类型: Referring CD, 二值 CD（Binary）, 损毁评估（Damage Assessment）
与 VLM 视觉思考主线关联: RS-VLM 主线 L2（SAM 接口）+ R13（免训练范式）。确立了「不常训练、只做匹配」的免训练 CD 范式。
代表基座 / 骨干: SAM Segment-Everything + embedding 相似度匹配
优先级: P0 · 必读
关键创新: 完全免训练——用 SAM 对两时相分别 segment everything，通过 mask embedding 相似度匹配两组 mask：无对应的 mask 即为变化。可叠加文本 prompt 实现 referring CD（「只关注建筑变化」）。
局限 / 残差 / 催生了什么: 依赖 SAM 实例级分割质量；对「语义变化但外观相似」（如 crop type change）不敏感；只能输出实例级变化，不输出像素级类别。催生路线 B（用 OVS 获取像素语义后差分）。
年份: 2024
我的视角 / 落地价值: 这条路是定位器驱动——以 SAM 为主、语言为辅。与路线 B（语义驱动）互补。我的方案可取两者之长：SAM 定位 + OVS 语义 + VLM 描述。尤适合实例清晰的建筑 CD、损毁评估场景。
方法家族: Open-Vocabulary CD, SAM-based, Training-Free CD
机构 / 团队: AnyChange / Segment Any Change 团队
模态支持: 光学 RGB, 文本 prompt
演进阶段: ⑦ 零监督 · 开放词汇 · Referring CD（2025+）
监督方式: 零监督 / Training-free
训练 / 评测数据集: LEVIR-CD, S2Looking, xBD
阅读状态: 待读

## 核心主题

完全免训练的 CD。根本思路：**不建模差异、只建模对应**——两时相各自独立分割 → 匹配 → 无匹配 = 变化。

## 管线

```jsx
Image_A ─→ SAM segment everything ─→ {mask_A_i, emb_A_i}
Image_B ─→ SAM segment everything ─→ {mask_B_j, emb_B_j}

对每个 mask_A_i：
  if max_j sim(emb_A_i, emb_B_j) < τ:
    mask_A_i ∈ change
  else:
    mask_A_i ∈ unchanged

可选：文本 prompt 过滤 → referring CD
```

## 代表

- **AnyChange / Segment Any Change** (2024)——这条路线目前唯一的成熟代表。

## 为什么取消「建模差异」可行

- 变化的本质是**相异**，不是**减法**。相异可用实例对应关系刻画。
- SAM + 特征相似度意味着不需要双时相配对监督。
- 文本 prompt 过滤是后置步骤，不影响前端 SAM 分割。

## 局限

- 依赖 SAM 实例级分割质量；大片均质区域（洪水、没边界的砍伐）分割失灵。
- 「语义变但外观相似」（如 crop type 切换）不敏感——SAM 会认为同一个 mask。
- 只输出实例级变化，不输出「变成了什么」的语义。

## 催生了什么

- **路线 B（⑦-B）**：用开放词汇分割 → 像素级语义后差分，补上「语义变化」与「像素级类别」。

## 对我方案的意义

- 这条是**定位器驱动**（SAM 为主）；路线 B 是**语义驱动**（CLIP 为主）。
- 我的最优策略是两者互补：
    - SAM Everything 负责**实例变化**（建筑出现/消失、建筑损毁）。
    - OVS 负责**语义变化**（crop type、land cover 类别切换）。
    - VLM 负责**语言描述**。
- 优先攻 AnyChange 不擅长的「语义变化」场景，作为方案的差异点。

## 论文

- AnyChange：[arxiv.org/abs/2402.01188](http://arxiv.org/abs/2402.01188)