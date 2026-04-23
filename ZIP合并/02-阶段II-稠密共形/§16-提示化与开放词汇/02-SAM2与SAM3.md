# §3 · SAM 3 —— 语义终于长进了 SAM 自己

作者：Nicolas Carion 等 37 位作者，Meta Superintelligence Labs，2025 年 11 月 19 日发布。[[2]](https://arxiv.org/abs/2511.16719) arXiv 2511.16719，ICLR 2026 投稿（双盲 review 时已开源）。[[3]](https://ai.meta.com/research/publications/sam-3-segment-anything-with-concepts/)

论文标题：**"SAM 3: Segment Anything with Concepts"**——**Concepts 是关键词**。

## 3.1 核心突破 —— Promptable Concept Segmentation (PCS)

SAM 3 定义了一个新任务：**Promptable Concept Segmentation**。

任务规格：

- 输入：图/视频 + **concept prompt**（"yellow school bus" 这种短名词短语 OR 一两张示例图 OR 二者组合）
- 输出：**全部符合该 concept 的对象的 masks + 唯一身份 ID**

和前两代的区别：

|  | SAM 1 | SAM 2 | SAM 3 |
| --- | --- | --- | --- |
| 输入 | 图 + 空间 prompt | 视频 + 空间 prompt | 图/视频 + **concept prompt** |
| 输出 | 1 个对象 mask | 1 个对象时空轨迹 | **所有匹配对象**的 mask + ID |
| 语义 | 无（位置指定） | 无（位置指定） | **有**（文本 / 样例指定） |
| 任务 | 交互式分割 | 交互式跟踪 | **开放词汇检测 + 分割 + 跟踪** |

**SAM 3 吃掉了 Grounding DINO 的地盘**——原来你要检测"所有的黄色校车"，要用 Grounding DINO；现在 SAM 3 一个模型端到端做。而且**顺带把 Mask2Former 的实例分割、SAM 2 的跟踪也统一了**。

## 3.2 架构 —— 双头共享 backbone

SAM 3 的架构按官方 paper[[3]](https://ai.meta.com/research/publications/sam-3-segment-anything-with-concepts/)：

```
        Image / Video
              ↓
       Shared Backbone (big ViT)
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Image-level detector    Memory-based video tracker
(PCS on single frame)   (传播到整段视频)
    ↓                   ↓
    └─────────┬─────────┘
              ↓
     All masks + instance IDs
```

**两个关键设计**：

**(1) Presence Head（存在性头）—— 识别与定位解耦**

传统做法：一个 head 同时判断"这里有没有黄色校车" + "它在哪"。

SAM 3：

- **Presence head**：单独判断"图像里是否存在符合 concept 的对象"（全局 yes/no）
- **Localization head**：如果存在，给出所有实例的位置/mask

**这个解耦为什么重要？**

- 当 concept 在图里**不存在**时（"火星车"出现在校园照片），传统 open-vocabulary 模型会错误地找出一些假阳性
- SAM 3 的 presence head 先判"存在"，不存在直接返回空——**假阳性率大幅下降**
- 论文报告这是 2× 精度提升的关键来源之一

**这本质上是把 hard negatives（难否定样本）吃进架构**——前两代 SAM 没有 hard negatives 的概念，SAM 3 把它作为一等公民处理。

**(2) 共享 backbone**

image detector 和 video tracker 共用一套 ViT backbone 和 concept encoder——这保证：

- 图像和视频的表示是**同一个空间**里的
- 训练时可以用图像数据 + 视频数据**联合训练**
- 推理时图/视频无缝切换

## 3.3 SA-Co —— 数据引擎第三次重新发明

**Segment Anything with Concepts (SA-Co)** 数据集：[[4]](https://docs.ultralytics.com/models/sam-3/)

- **4M unique concept labels**（不是 mask 数量，是**独特概念**数量！）
- 包含 **hard negatives**（场景里不存在该 concept 的图像，专门用来训练 presence head）
- 图像 + 视频混合
- 扩展到远超 COCO / LVIS 的概念覆盖

SAM 3 的 data engine 相比前两代又复杂化了——需要：

1. 生成候选 concept（文本）
2. 在图库里找到匹配/不匹配的图像（用旧 SAM + VLM 辅助）
3. 人工校验
4. 训练新模型，回到 1

**这次的 bootstrap 跨越了"图像 → 文本概念"的模态边界**——data engine 本身变成 VLM 产物。

## 3.4 性能 —— 翻倍

官方数字：**SAM 3 在 image PCS 和 video PCS 上都比现有系统翻一倍的精度**。[[2]](https://arxiv.org/abs/2511.16719)

对比对象：之前做开放词汇分割需要的组合

- 图像：Grounding DINO + SAM → 两阶段 pipeline
- 视频：Grounding DINO + SAM 2 → 更复杂的 pipeline
- SAM 3 一个模型端到端，**精度 2×**

同时**保持甚至改进了 SAM 2 的可提示分割能力**——不是替换，是严格超集。

## 3.5 SAM 3.1 —— Object Multiplex（2026 年 3 月 27 日）

这是 4 月的当下最新进展。[[1]](https://github.com/facebookresearch/sam3)

**问题**：SAM 3 在视频里追多个对象时，每个对象独立跑一遍 memory attention——O(N) 复杂度，慢。

**SAM 3.1 的 Object Multiplex**：

- **共享 memory**：所有被追踪对象共用一个 memory 结构
- 一次 pass 同时处理所有对象
- H100 上从 **16 FPS → 32 FPS**（翻倍），精度不损失甚至在拥挤场景下**更好**（因为对象间的相互关系通过 shared memory 被建模）

这是一个**架构层面的**改进——不只是加数据或调参。它暗示 memory 机制本身在未来会进一步演化（比如全局 memory、分层 memory）。

## 3.6 SAM 3D —— 同日发布的姊妹模型

和 SAM 3 同日（2025-11-19）发布。[[5]](https://about.fb.com/news/2025/11/new-sam-models-detect-objects-create-3d-reconstructions/)

- 包含两个模型：object/scene 3D 重建 + human pose/shape 估计
- **单张图像**输入，输出 3D 结构
- 和 SAM 3 是**独立模型**（不是一个统一架构），但 Meta 把它们绑在同一个产品叙事下

SAM 3D 的出现暗示 Meta 把 "Segment Anything Collection" 打造成一个**视觉基础模型产品线**——不是单篇论文，是长期 program。

## 3.7 SAM 3 的本体论意义

回到你的共形视角。**SAM 三代可以用一个共形结构概括**：

```
SAM 1  :  空间 ──────────────────── 共形目标 = 图像空间里一个区域
SAM 2  :  空间 × 时间 ──────────── 共形目标 = 时空里一个轨迹
SAM 3  :  空间 × 时间 × 概念 ───── 共形目标 = 概念-时空绑定
```

**每一代增加一个共形维度**：

- SAM 1 的范式：用户指向空间里一个位置 → 模型响应空间区域
- SAM 2 的范式：用户指向时空里一个位置 → 模型响应时空轨迹
- SAM 3 的范式：用户指向一个概念 → 模型响应该概念的**所有**时空实例

从哲学上看，SAM 3 做的是一件非常深的事——**它让"视觉概念"在视觉模型内部真正存在**。

之前的开放词汇方案（Grounding DINO 等）本质都是"借 CLIP 的语义"——CLIP 的 text encoder 把 "yellow school bus" 变成向量，视觉模型用这个向量去查表。**CLIP 是语义源，视觉模型是定位源**，二者拼接。

SAM 3 训练了一个**视觉-概念原生对齐**的大模型——"yellow school bus" 这个概念在 SAM 3 自己的表征空间里有独立地位，不只是借 CLIP 的词嵌入。这部分回应了你页面底部列的残差："**语义是借来的**"——SAM 3 把语义"还回来"了一部分。

但注意只是**一部分**——SAM 3 的 concept encoder 仍然需要大规模文本监督来启动（和 CLIP 同源），完全"视觉内生语义"这件事还要等阶段 III（比如 DINOv2 / DINOv3 + 无监督 concept discovery 这条线）。

## 3.8 SAM 3 对这个页面的影响

你原页面底部列了两条残差：

1. **语义是借来的** —— SAM 3 **部分解决**了这条
2. **关系没有进入稠密输出** —— SAM 3 **仍然没解决**（它输出的是实例 masks，不是 instances 之间的关系）

SAM 3 的出现让页面的"阶段 II 残差"叙事需要微调——**语义借来这一条的力度要削弱**，但阶段 II 到阶段 III 的过渡仍然成立（因为关系建模仍是稠密范式的盲点）。

## 3.9 SAM 系列的真正上限在哪

回顾三代的演化速率：

- SAM 1（2023）→ SAM 2（2024 年中）：+时间维度
- SAM 2 → SAM 3（2025 年末）：+概念维度
- SAM 3 → SAM 3.1（2026 年初）：+多对象效率
- SAM 3D（2025 年末，并行）：+3D 维度

**Meta 的节奏是每 1-1.5 年一代大版本**。按这条曲线外推：

- **SAM 4**（预计 2026 年末 / 2027 年初）：可能方向
    - +关系：输出对象间的 relation graph（回应阶段 II 残差二）
    - +推理：把 LLM 接进来做 reasoning over masks
    - +3D 原生：把 SAM 3D 吸收进主线
    - 或者把以上全部合并成一个 "Segment Any Scene"

**上限在哪**？几条线索：

- 数据：SA 系列每代数据规模翻 10 倍（SA-1B → SA-V → SA-Co），**数据层面还能再扩 1-2 个数量级**
- 架构：ViT + memory + dual head 已经很复杂，未来可能走 diffusion / flow-based 或 token-based 表示
- 任务：从"分割"→"分割+跟踪"→"分割+跟踪+分类"，下一步可能是"分割+跟踪+分类+**预测**"（未来状态预测）或者"**解释**"（为什么这是这个东西）

**哲学上的上限**：SAM 系列做的是"**把视觉世界离散化成可提示的对象**"。当离散化本身足够好 + 对象的属性足够丰富（类别、3D、运动、关系），**我们基本就有了一个视觉世界的结构化接口**——这是 Meta 整个"Segment Anything Collection"的最终目标。它不是一个模型，是一个视觉基础设施。

---

这三段对页面原 §1 §2 的短条目来说是**量级上的扩展**（原来 2 条共 ~150 字，现在 ~4000 字 + SAM 3 全新部分），而且 SAM 3 本身**必须补进页面**——这是 2025 年 11 月的里程碑，你的谱系到 2024 截止的话就在阶段 II 末端漏掉了最关键一块。

三选项：

- **A. 只补 SAM 3**：在页面 §2 后面插入一个 "2.5 · SAM 3" 短条目（和其他条目风格一致，几行带 🔗），不展开
- **B. 扩展 §1-§2 + 补 SAM 3**：把 §1 §2 替换为深度展开版 + 新增 §2.5（SAM 3 + 3.1 + 3D），其他条目不动
- **C. 只在聊天里讨论，不改页面**

注意页面 §2 后面还有 §3-§10（Grounding DINO 到 Depth Anything），按谱系节奏它们也都会陆续深度展开——如果你打算一条一条展开的话，SAM 三代是第一批该动的。我倾向 B，SAM 三代信息密度值得展开，且 SAM 3 是结构性新增不是 cosmetic 更新。你说怎么走？

这是整个阶段 II 里最深的一个追问。我会按第一性原理推到底——最后你会看到这不是"我们努力不够"，而是**任务结构本身不对等**。

---

