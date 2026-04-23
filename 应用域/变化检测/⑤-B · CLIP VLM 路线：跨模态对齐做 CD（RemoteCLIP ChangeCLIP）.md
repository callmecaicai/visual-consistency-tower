# ⑤-B · CLIP/VLM 路线：跨模态对齐做 CD（RemoteCLIP / ChangeCLIP）

CD 任务类型: 二值 CD（Binary）, 语义 CD（Semantic）
与 VLM 视觉思考主线关联: RS-VLM 主线 R5（文本锚点）+ R12（开放词汇桥梁）。CLIP 是整个 ⑥⑦ 的底层语言-视觉对齐器。
代表基座 / 骨干: CLIP ViT-B/L + RS 继续预训练 / prompt 引导
优先级: P1 · 重点
关键创新: CLIP 原生是自然图像 + 图像级对齐；RS CD 需要领域适配 + 像素级 + 对变化敏感。两条子路分别攻不同缺口：RemoteCLIP 继续预训练（用 Box-to-Text / Mask-to-Box 把检测/分割数据转图文对，修正 domain bias）；ChangeCLIP 用文本 prompt 直接引导双时相特征聚焦「变化类别」。
局限 / 残差 / 催生了什么: CLIP 特征低分辨率 + 全局偏差大（[CLS] token 主导）；在 RS 上「物体边界」和「小目标」弱。催生 SegEarth-OV 的 SimFeatUp（无监督高分辨率恢复）+ Global Bias Alleviation。
年份: 2024
我的视角 / 落地价值: CLIP 是「语义锚点」而非「定位器」，必须与 SAM（定位器）组合。我的 training-free 方案正是 CLIP 语义 + SAM 定位 + VLM 描述的三件套。
方法家族: CLIP-based, Hybrid CNN-Transformer
机构 / 团队: RemoteCLIP 团队 / ChangeCLIP 团队
模态支持: 光学 RGB, 多光谱, 文本 prompt
演进阶段: ⑤ 视觉基础模型驱动（2023-2024）
监督方式: 像素级全监督
训练 / 评测数据集: CDD, LEVIR-CD, SYSU-CD, WHU-CD
阅读状态: 待读

## 核心问题

CLIP 是图像-文本对齐器，天然懂「What」；但它不是定位器（弱「Where」），也不直接懂「变化」。⑤-B 回答：**如何把一个自然图像对齐的全局 VLM 改造成 RS 的像素级、时序敏感、变化感知的 backbone？**

## CLIP 用于 RS CD 的四重原生困难

| 困难 | 表现 | 根因 |
| --- | --- | --- |
| 领域偏移 | CLIP 在 RS 零样本分类急剧掉点 | 预训练 WebImageText 自然视角；RS 俯视 + 多光谱稀少 |
| 分辨率弱 | 最后一层 14×14 或 16×16 特征；小目标与边界崩溃 | ViT patch 16；全局 [CLS] 主导 |
| 全局偏差 | patch tokens 被 [CLS] 吸引，局部判别力弱（SegEarth-OV 称 Global Bias） | 对比 loss 只约束图像级对齐 |
| 对「变化」中性 | 不知道「新增建筑」这个事件是否发生 | 训练样本是静态图文对；无双时相监督 |

## 三条攻法

| 路径 | 攻击面 | 代表 | 代价 |
| --- | --- | --- | --- |
| A · 领域继续预训练 | 领域偏移 + 全局偏差 | **RemoteCLIP** · GeoRSCLIP · SkyCLIP · RS-CLIP | 需大规模 RS 图文对；仅底层 backbone 不做 CD |
| B · 多模态融合 + prompt 注入 | 领域偏移 + 对变化中性 | **ChangeCLIP** · ClearSCD · CDVQA | 需 CD 监督；prompt 设计启发式 |
| C · 特征修补 + OVS 架桥 | 分辨率 + 全局偏差 | SegEarth-OV 的 SimFeatUp + GBA（已归 ⑦-B） | 无训练但引入外部超分网络 |

## 典型论文卡

### RemoteCLIP · Liu 2024 TGRS（arXiv:2306.11029）

- **一句话**：首个针对 RS 的 CLIP 继续预训练，把自然图像对齐器改造为 RS 视觉-语言基础模型。
- **数据工程（三个配方）**：
    - **B2T（Box-to-Text）**：从检测数据集的 box 标注自动生成图文对。
    - **M2B + B2T（Mask → Box → Text）**：从语义分割掩膜先生成 box，再转文本描述。
    - **RET-3**：把 17 个异构 RS 数据集整合成约 12 倍扩充的图文对数据集。
- **意义**：解决 RS 图文对稀缺问题的「数据配方」；是后续 RSGPT / GeoChat / LHRS-Bot / SkySense 的数据组装参考。

### ChangeCLIP · Dong 2024 ISPRS JPRS（arXiv:2401.15942）

- **一句话**：用 CLIP 的跨模态对齐做 RS CD，二值 + 语义同步提升。
- **三件套**：
    - ① 视觉-语言驱动的 binary CD 框架：CLIP 的无监督分类能力生成「当前图覆盖哪些类别」的文本 prompt，作为 CD 任务的多模态输入。
    - ② 双时相插值 + 分数图（score map）：把 CLIP 分类置信度直接用作变化识别的额外通道。
    - ③ 注意力融合 + 加权融合：文本特征与差异视觉特征跨模态对齐。
- **消融（张继贤综述转述）**：双时相插值、分数图、注意力、加权融合——逐个模块都带来稳定增益。
- **定位**：[⑥-A · Change Captioning 奠基：双分支 Transformer → 自然语言描述（Chg2Cap / RSICCformer+LEVIR-CC）](%E2%91%A5-A%20%C2%B7%20Change%20Captioning%20%E5%A5%A0%E5%9F%BA%EF%BC%9A%E5%8F%8C%E5%88%86%E6%94%AF%20Transformer%20%E2%86%92%20%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E6%8F%8F%206a40583827ef4f438e6b2a03763f6868.md) 系列的前哨——⑥ 是让 VLM 直接输出自然语言 caption；⑤-B 是用 CLIP 文本塔先做语义注入。

### GeoRSCLIP / SkyCLIP / RS-CLIP（领域预训练生态）

- 思路一致：收集 RS 领域图文对，继续训练 CLIP。
- **数据规模是分水岭**：RemoteCLIP RET-3 百万级；GeoRSCLIP 结合 RS5M；SkyCLIP 千万级。
- 这些 backbone 可直接替换 ChangeCLIP / SegEarth-OV 的 CLIP 基座，获得 RS 先验。

### ClearSCD · 2024

- **定位**：时空特征工程派，高分辨率 RS 影像表现突出。
- **贡献**：不再单押 CLIP 语义，而是把 CLIP 特征与时空一致性约束联合。

### CDVQA · Change Detection Visual Question Answering

- **定位**：最早把 CD 表述为视觉问答任务。
- **结构**：多时相特征编码 + 多时相融合 + 多模态融合 + 答案预测。
- **意义**：[⑥-B · Change Captioning 三条进化路径：语义化 / 高效化 / 解耦化（KCFI / RSCaMa / PromptCC）](%E2%91%A5-B%20%C2%B7%20Change%20Captioning%20%E4%B8%89%E6%9D%A1%E8%BF%9B%E5%8C%96%E8%B7%AF%E5%BE%84%EF%BC%9A%E8%AF%AD%E4%B9%89%E5%8C%96%20%E9%AB%98%E6%95%88%E5%8C%96%20%E8%A7%A3%E8%80%A6%E5%8C%96%EF%BC%88KCFI%20RS%20954e7c5bcf3a4f14b7c8d925dd25e125.md) 的真正原点。

## 为什么 CLIP 路线必然与 SAM 组合

- CLIP 的输出是**语义概念空间**（类别、属性）——比 SAM 的**实例 / mask 空间**高一层。
- 但 CLIP 的空间分辨率和局部判别力远弱于 SAM。
- 结论：
    - CLIP 回答 **What**（是什么类别变化）
    - SAM 回答 **Where**（像素级边界）
    - 两者必须组合。
- 这是我的 training-free 方案、以及 [⑦-B · Training-Free Open-Vocabulary CD：开放词汇分割 → 时相差分（SegEarth-OV / Seg2Change / AdaptOVCD）](%E2%91%A6-B%20%C2%B7%20Training-Free%20Open-Vocabulary%20CD%EF%BC%9A%E5%BC%80%E6%94%BE%E8%AF%8D%E6%B1%87%E5%88%86%E5%89%B2%20%E2%86%92%20%E6%97%B6%E7%9B%B8%205fb75eaa0503480095aa4c2c72635306.md)、UniVCD（SAM2 + CLIP 无监督 OV CD）、AdaptVFMs-RSCD 等工作共同的底层架构假设。

## 共享局限

1. CLIP 特征像素级精度不够 → 必须接 SAM / SAM2 做 mask refinement。
2. RS 继续预训练仍依赖大规模图文对 → 数据瓶颈仍在（RemoteCLIP 的 B2T / M2B 是目前最实用的「数据配方」）。
3. CLIP 的类别受限于 caption 分布 → 对 RS 长尾（稀有地物、细粒度作物）覆盖不足。
4. 「变化」不是 CLIP 的一等公民 → 要么靠融合模块（ChangeCLIP），要么靠事后 prompt（SegEarth-OV）。

## 催生了什么

- **特征修补** → [⑦-B · Training-Free Open-Vocabulary CD：开放词汇分割 → 时相差分（SegEarth-OV / Seg2Change / AdaptOVCD）](%E2%91%A6-B%20%C2%B7%20Training-Free%20Open-Vocabulary%20CD%EF%BC%9A%E5%BC%80%E6%94%BE%E8%AF%8D%E6%B1%87%E5%88%86%E5%89%B2%20%E2%86%92%20%E6%97%B6%E7%9B%B8%205fb75eaa0503480095aa4c2c72635306.md) 的 SimFeatUp（无监督特征超分）+ Global Bias Alleviation + AlignEarth SAR 蒸馏，打通 CLIP → OVS → 零监督 CD 链路。
- **端到端 VLM 化** → [⑥-C · 从单轮 caption → 会话 & Agent 化 RS CD（TeoChat / ChangeChat / Change-Agent）](%E2%91%A5-C%20%C2%B7%20%E4%BB%8E%E5%8D%95%E8%BD%AE%20caption%20%E2%86%92%20%E4%BC%9A%E8%AF%9D%20&%20Agent%20%E5%8C%96%20RS%20CD%EF%BC%88TeoChat%20Cha%20b965de08b3ff414bbf50aa8054a62616.md)：把 CLIP 文本塔直接换成 LLM。
- **多 FM 融合** → [⑤-C · 统一 FM 适配器 & RS 多任务预训练（BAN / MTP）](%E2%91%A4-C%20%C2%B7%20%E7%BB%9F%E4%B8%80%20FM%20%E9%80%82%E9%85%8D%E5%99%A8%20&%20RS%20%E5%A4%9A%E4%BB%BB%E5%8A%A1%E9%A2%84%E8%AE%AD%E7%BB%83%EF%BC%88BAN%20MTP%EF%BC%89%2098e248b8649643aab1d7d3b3d85530c7.md) 把 CLIP / SAM / DINOv2 统一纳入 adapter 框架。

## 对我方案的意义

- CLIP 是 training-free 管线的**语义入口**，不可替代。
- 直接用原版 CLIP 会踩两个坑（分辨率 + 全局偏差）→ 必须接入 SegEarth-OV 的 **SimFeatUp + GBA**，否则像素级 CD 精度天花板很低。
- RS 继续预训练的 CLIP 变体（GeoRSCLIP / SkyCLIP）可直接替换 backbone，不改其余管线。
- ChangeCLIP 的「双时相插值 + 分数图」可作为零监督 baseline 的对照组（我把监督替换为 VLM zero-shot caption）。

## 论文链接

- RemoteCLIP：[arxiv.org/abs/2306.11029](http://arxiv.org/abs/2306.11029)
- ChangeCLIP：[arxiv.org/abs/2401.15942](http://arxiv.org/abs/2401.15942)
- GeoRSCLIP / RS5M：[arxiv.org/abs/2306.11300](http://arxiv.org/abs/2306.11300)
- SkyCLIP：[arxiv.org/abs/2312.12856](http://arxiv.org/abs/2312.12856)
- CDVQA：[arxiv.org/abs/2112.11644](http://arxiv.org/abs/2112.11644)
- ClearSCD / DynamicEarth（AAAI 2026 Oral OVCD benchmark）：[github.com/likyoo/DynamicEarth](http://github.com/likyoo/DynamicEarth)
- 面向零样本分类的 RS-VLM 综述：[ygxb.ac.cn/rc-pub/front/front-article/download/149792795](http://ygxb.ac.cn/rc-pub/front/front-article/download/149792795)