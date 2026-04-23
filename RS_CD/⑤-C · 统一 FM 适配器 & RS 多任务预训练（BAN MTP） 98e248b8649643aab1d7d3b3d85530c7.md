# ⑤-C · 统一 FM 适配器 & RS 多任务预训练（BAN / MTP）

CD 任务类型: 二值 CD（Binary）, 建筑 CD, 语义 CD（Semantic）
与 VLM 视觉思考主线关联: RS-VLM 主线 R7（FM 作视觉塔）+ R9（多任务统一）。BAN 是 FM 组合学的工程模板；MTP 是 RS-VLM 预训练数据构造的参考。
代表基座 / 骨干: SAM + CLIP + DINOv2 并联 / 多任务预训练统一 backbone
优先级: P1 · 重点
关键创新: 单一 FM 都有盲区（SAM 无语义 / CLIP 无定位 / DINOv2 无对齐）；RS 下游任务多样。两个正交答案：横向并联多 FM 走 adapter 路线（BAN：轻量 bi-temporal adapter，<10% 参数，统一适配 SAM/CLIP/DINOv2）；纵向在预训练阶段就注入多任务让 FM 「见过」CD（MTP：分类/检测/分割/CD 统一多任务预训练）。
局限 / 残差 / 催生了什么: Adapter 路线仍需 CD 标注；MTP 需大规模 RS 多任务标注。两者都把「FM + CD」做到了监督路线的天花板，催生 ⑦ 的 training-free 释放。
年份: 2024
我的视角 / 落地价值: BAN 验证「FM 冻结 + 轻适配」是工程最优；MTP 验证「CD 应从预训练阶段就前置」。我的零监督方案本质是把 adapter 也砍掉——如果做到，则证明多 FM 并联 + training-free 可以同时成立。
方法家族: CLIP-based, DINOv2-based, SAM-based, Self-Supervised CD
机构 / 团队: BAN 团队 / 武大 MTP 团队
模态支持: 光学 RGB
演进阶段: ⑤ 视觉基础模型驱动（2023-2024）
监督方式: 像素级全监督
训练 / 评测数据集: CLCD, LEVIR-CD, S2Looking, SYSU-CD, WHU-CD
阅读状态: 待读

## 核心问题

单一 FM 都有盲区；RS CD 又要求像素级 + 语义 + 时间。⑤-C 回答两种正交策略：

- **横向** · PEFT 框架让多个 FM 可插拔组合
- **纵向** · 把 CD 当一等公民放进预训练

## 单一 FM 能力矩阵（为什么必须组合）

| FM | Where 定位 | What 语义 | 跨模态 | 时间 / 多时相 | RS 领域性 |
| --- | --- | --- | --- | --- | --- |
| SAM / SAM2 | ★★★ | ✗ | ✗ | △（SAM2 memory） | 弱 |
| CLIP | △ | ★★★ | ★★★ | ✗ | 弱 |
| DINOv2 / DINOv3 | ★★ | ★★（自监督表征） | ✗ | ✗ | 弱 |
| RemoteCLIP / GeoRSCLIP | △ | ★★★ | ★★★ | ✗ | ★★ |
| SatMAE / Scale-MAE / RVSA | ★★ | ★ | ✗ | △（SatMAE 有时序通道） | ★★★ |
| SkySense · msGFM | ★★ | ★★ | ★★ | ★★（多时相预训练） | ★★★ |

## 两种正交策略

| 维度 | 本质 | 代表 | 释放了什么 |
| --- | --- | --- | --- |
| **横向 · 多 FM 并联 + PEFT** | 不押单一 FM，提供 FM 无关的适配框架 | **BAN** · PeftCD · MSF-SAM · UPetu | CD 适配器与基座解耦，基座升级直接吃红利 |
| **纵向 · 预训练前置** | 让 FM 在预训练阶段就见过 CD / 时序 / RS 多任务 | **MTP** · SkySense · SatMAE · Scale-MAE · RingMo · CMID · SpectralGPT · DINO-MM · SeCo · GeoKR | 从「afterthought 下游微调」变成「一等预训练任务」 |

## 横向策略 · PEFT + FM 组合学

### BAN · Bi-Temporal Adapter Network（arXiv:2312.01163）

- **一句话**：首个**基础模型无关**的 CD 适配框架——冻结 SAM / CLIP / DINOv2 任一，只训轻量 Bi-TAB 适配器（<10% 参数）。
- **架构**：
    - Frozen Foundation Encoder（可换 SAM ViT / CLIP ViT / DINOv2 ViT）
    - Bi-Temporal Adapter（Bi-TAB）：双分支注入时相交互
    - 轻量 CD 解码头
- **意义**：证明「FM 无关的 CD 适配器」可行——换基座成本接近零，这是工程落地的关键。

### PeftCD · 2025（SAM2 + DINOv3）

- **一句话**：BAN 思路在新基座上的实例——SAM2（分割）+ DINOv3（自监督表征）双基座冻结 + PEFT。
- **成绩**：7 个 RS CD 公开数据集 SOTA。
- **意义**：验证 BAN 范式的可持续性——基座升级，pipeline 不动。

### Conv-LoRA · arXiv:2401.17868（ICLR 2024）

- LoRA 瓶颈里嵌 MoE 卷积专家，同时恢复 SAM 的局部先验 + 高层语义能力。
- 关键洞察：SAM 的二值分割预训练本身压制 ViT 的语义能力；Conv-LoRA 用多尺度卷积 MoE 路由解压。

### MSF-SAM / UPetu / AiRs / SCD-SAM（PEFT 混合与特化）

- **MSF-SAM**：Adapter + LoRA 混合，多模态 RS 多任务统一。
- **UPetu**：统一多个 PEFT 方法到一个框架。
- **AiRs**：SCA（Spatial Context Adapter）+ SRA（Semantic Response Adapter），专攻 RS 空间-语义复杂度。
- **SCD-SAM**：语义适配器 + 重叠 patch embedding，专攻语义 CD。

### PEFT 六范式一览（清华 CVMJ 2025）

Adapter Tuning · Prompt Tuning · Reparameterized（LoRA 系）· Hybrid Tuning · Partial Tuning · Improved Tuning。[⑤-A · SAM 路线：冻结分割基座 → 适配 CD（RSPrompter / TTP / SAM-CD）](%E2%91%A4-A%20%C2%B7%20SAM%20%E8%B7%AF%E7%BA%BF%EF%BC%9A%E5%86%BB%E7%BB%93%E5%88%86%E5%89%B2%E5%9F%BA%E5%BA%A7%20%E2%86%92%20%E9%80%82%E9%85%8D%20CD%EF%BC%88RSPrompter%20TTP%20SAM-CD%EF%BC%89%200d70be6fdc424966bbff49b7aebd3b2c.md) + ⑤-C 所有 SAM / CLIP 适配工作都落在前四类。

## 纵向策略 · RS FM 预训练谱系

### MTP · Multi-Task Pretraining（Wang 2024, arXiv:2403.13430）

- **一句话**：首次把「语义分割 + 实例分割 + 旋转物体检测」三任务联合作为 RS FM 预训练目标，CD 作为下游验证。
- **架构**：共享编码器（RVSA / InternImage）+ 任务特定解码器，SAMRS 数据集。
- **验证**：14 个下游数据集、300M+ 参数；与同规模模型比优、与更大模型比具竞争力。
- **意义**：从 MAE 类自监督 pretraining 转向**监督多任务 pretraining**，弥合「预训练任务 vs 下游任务」差异。
- **对我方案**：若要走 self-supervised CD，数据构造方式比模型更重要；MTP 的 SAMRS + 多任务监督是当前最强的「数据蒸馏」思路。

### SatMAE · NeurIPS 2022

- MAE 范式在 RS 的首个落地，显式建模**时序通道 + 多光谱通道**。
- 后续 Scale-MAE / Cross-Scale MAE / GFM 的母体。

### Scale-MAE · ICCV 2023

- MAE + 尺度感知——encoder 显式注入 GSD（Ground Sample Distance），解决 RS 多分辨率下游适配。

### RingMo · RVSA · InternImage-RS

- **RingMo**：中科院大规模 RS 预训练。
- **RVSA**：Rotated Varied-Size Attention for ViT，专门解决 RS 俯视的旋转不变性。
- **InternImage-RS**：CNN-based RS FM（MTP 的对比基座）。

### SkySense · CVPR 2024（V2 ICCV 2025）

- 多模态 RS 通用 FM（光学 + SAR + 多光谱 + 时序），目标是「universal interpretation」。
- 规模：msGFM 报告 mAP 92.9%；SkySense 像素级 mF1 93.99%（综述数据）。
- **意义**：⑤-C 纵向路线的天花板工作——把 RS 所有模态与任务塞进一个 FM。

### 自监督 RS 预训练旁支

- **SeCo**（ICCV 2021）：Seasonal Contrast——季节变化作对比学习正样本。
- **GeoKR**（TGRS 2021）：Geographical Knowledge-Driven——地理先验作监督信号。
- **DINO-MM**：SAR-光学联合自监督。
- **CMID**：Multi-Instance Discrimination RS SSL。
- **SpectralGPT**：光谱维度的 GPT 化尝试。

## 催生 ⑦ 的必然性

⑤-C 把「监督 + FM + CD」三要素组合做到工程天花板：

- BAN 证明 **PEFT + 多 FM** 是工程最优；
- MTP 证明 **多任务预训练 + 监督** 是性能最优。

下一步只剩释放「监督」这一条约束——这就是 ⑦ 的出发点：[⑦-A · Training-Free CD 路线 A：SAM Segment-Everything + Mask 对应匹配（AnyChange）](%E2%91%A6-A%20%C2%B7%20Training-Free%20CD%20%E8%B7%AF%E7%BA%BF%20A%EF%BC%9ASAM%20Segment-Everything%20d28bfe9dd5264f118f9000d3b1a9ddb8.md)、[⑦-B · Training-Free Open-Vocabulary CD：开放词汇分割 → 时相差分（SegEarth-OV / Seg2Change / AdaptOVCD）](%E2%91%A6-B%20%C2%B7%20Training-Free%20Open-Vocabulary%20CD%EF%BC%9A%E5%BC%80%E6%94%BE%E8%AF%8D%E6%B1%87%E5%88%86%E5%89%B2%20%E2%86%92%20%E6%97%B6%E7%9B%B8%205fb75eaa0503480095aa4c2c72635306.md)、UniVCD（SAM2 + CLIP 无监督 OV CD）。

## 对我方案的意义

- **BAN 的 FM 无关性** = 我方案的 **Pipeline 无关性**：把管线写死为「定位器 + 语义器 + 描述器」协议，后端插任一 FM。
- **MTP 的多任务信号**：提醒未来做 self-supervised CD 时，优先考虑「SAMRS 风格的合成数据 + 多任务监督」，而非纯 MAE。
- **SkySense 的多模态统一**：长期方向——SkySense-V2 级 FM 开源后，我的 pipeline 直接升级为「多模态 training-free」。
- **能力矩阵的用法**：
    - 定位层 → SAM / SAM2（通用）+ SkySense（RS 领域加成）
    - 语义层 → CLIP / RemoteCLIP / GeoRSCLIP
    - 描述层 → TeoChat / LHRS-Bot / GeoChat（VLM 侧）
    - 表征层（可选）→ DINOv2 / DINOv3 / Scale-MAE（作差分敏感特征）

## 论文链接

- BAN：[arxiv.org/abs/2312.01163](http://arxiv.org/abs/2312.01163)
- MTP：[arxiv.org/abs/2403.13430](http://arxiv.org/abs/2403.13430)
- Conv-LoRA：[arxiv.org/abs/2401.17868](http://arxiv.org/abs/2401.17868)
- SatMAE：[arxiv.org/abs/2207.08051](http://arxiv.org/abs/2207.08051)
- Scale-MAE：[arxiv.org/abs/2212.14532](http://arxiv.org/abs/2212.14532)
- SkySense：[arxiv.org/abs/2312.10115](http://arxiv.org/abs/2312.10115)
- SpectralGPT：[arxiv.org/abs/2311.07113](http://arxiv.org/abs/2311.07113)
- PeftCD · SAM2 + DINOv3：[zhuanlan.zhihu.com/p/1949847926517002833](http://zhuanlan.zhihu.com/p/1949847926517002833)
- Awesome-Remote-Sensing-Foundation-Models：[github.com/Jack-bo1220/Awesome-Remote-Sensing-Foundation-Models](http://github.com/Jack-bo1220/Awesome-Remote-Sensing-Foundation-Models)
- 综述 · Vision Foundation Models in RS：[arxiv.org/abs/2408.03464](http://arxiv.org/abs/2408.03464)
- 综述 · 清华 CVMJ 2025 RS 微调：[hub.baai.ac.cn/view/50020](http://hub.baai.ac.cn/view/50020)