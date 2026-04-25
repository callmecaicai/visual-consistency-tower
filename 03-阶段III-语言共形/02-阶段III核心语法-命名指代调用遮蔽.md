# 阶段 III 核心语法：命名、指代、调用、遮蔽

本页是阶段 III 的中层语法页。它不替代 `00-总纲` 与 `§21-§27`，而是给它们提供共同协议：阶段 III 不是模型清单，而是视觉差异进入公共语义契约的过程。

---

## 章首协议（五问版）

| 问项 | 本页回答 |
|---|---|
| 纯存在态 | `Visual Difference -> Public Linguistic Contract`：视觉差异进入公共语言契约。 |
| 稳定差异 | 可被名称、caption、embedding、phrase、instruction、rationale 与评价语言调用的视觉差异。 |
| 闭合制度 | `C_III=(Z_image-text, Π_caption/VQA/grounding/instruction, Γ_modality/language/prompt, M_contrastive/IT/judge, D_alignment/IT/projector)`。 |
| 成功标准 | 可命名、可指代、可调用、可在公共语义接口中回答。 |
| 遮蔽对象 | 未命名视觉、细粒度空间、对象状态、视觉语义主权。 |
| 内在残差 | 语言越强，越可能替视觉说话；公共语义成立不等于视觉自身持有世界。 |
| 下一步重写 | 系统必须证明语义不只是会说，而能外显生产观测，推出阶段 IV。 |

---

## 一、纯存在态

阶段 I 的最小公式是：

```text
Image -> Label
```

阶段 II 的最小公式是：

```text
Image-as-domain -> Field / Object / Interface
```

阶段 III 的最小公式是：

```text
Visual Difference -> Public Linguistic Contract
```

更展开地写：

```text
delta_v -> name_l -> refer(x, name_l) -> act_or_answer(x, instruction_l)
```

也就是：

1. 视觉差异被语言命名。
2. 语言名称被指到图像中的对象、区域、属性或关系。
3. 语言指令开始调用视觉系统完成任务。
4. 语言同时遮蔽那些没有被命名、没有被描述、没有被评价的视觉差异。

阶段 III 的全部技术史，都是为了让这张契约更深地嵌入模型内部。阶段 III 的全部残差，也都来自这张契约不是视觉自身的主权。

---

## 二、语言不是单一对象

阶段 III 中的“语言”不是一种东西。它至少承担七种角色：

| 角色 | 典型形式 | 对应章节 | 功能 | 风险 |
|---|---|---|---|---|
| 名称语言 | label / object tag | §21 | 给视觉对象命名 | 闭集、标签偏见 |
| 描述语言 | caption / alt-text | §22 | 提供自然语言监督 | caption bias |
| 对齐语言 | text embedding | §22 | 形成跨模态相似度空间 | 压扁未描述属性 |
| 指代语言 | phrase / referring expression | §23 / §26 | 指到框、mask、region | 指代歧义 |
| 指令语言 | prompt / instruction | §25 / §26 | 调用任务与行为 | 接口强于感知 |
| 推理语言 | CoT / rationale | §25 / §27 | 组织多步回答 | 思考越长越不看图 |
| 评价语言 | preference / judge / rubric | §25 / §27 | 规范输出质量 | 度量仍外部给定 |

因此，“语言内化”不是一次性事件，而是这些语言角色逐层进入视觉系统的不同位置。

---

## 三、语言内化深度谱

| 级别 | 名称 | 语言进入哪里 | 代表 | 核心残差 |
|---|---|---|---|---|
| L0 | 标签语言 | 训练标签 / 类别名 | ImageNet、检测类别表 | 名称闭集 |
| L1 | 后端外挂 | region feature + BERT 融合 | ViLBERT、LXMERT、UNITER、VinVL | 二手视觉 |
| L2 | 损失内化 | 文本成为预训练目标 | CLIP、ALIGN、LiT、SigLIP | 全图压缩 |
| L3 | 稠密锚定 | 文本进入检测 / 分割 / region 输出链 | GLIP、Grounding DINO、CAT-Seg | 指代不等于状态 |
| L4 | 统一骨干 | 多任务图文理解共用骨干 | CoCa、BLIP、OFA、Florence-2 | 接口统一不等于世界统一 |
| L5 | LLM 后端 | 视觉 token 被送入语言推理系统 | Flamingo、BLIP-2、LLaVA、Qwen-VL | 语义主权在语言 |
| L6 | 像素调用 | 语言指令产生 mask / grounding 输出 | LISA、GLaMM、PixelLM | 单向输出，不等于生成与持有 |

CLIP 是 L2：语言进入预训练目标和共享相似度空间。它不是完整的语言骨干。VLM 是 L5：视觉进入已经完成语言预训练的语义后端。LISA / GLaMM / PixelLM 是 L6：语言不只回答，还开始触发像素级输出。

---

## 四、四种机制

| 机制线 | 对应章节 | 本体功能 | 自我否定 |
|---|---|---|---|
| 命名 | §21-§22 | 视觉差异进入标签、caption、文本嵌入和公共概念空间 | 名字来自语言分布，不来自视觉自身 |
| 指代 | §23 / §26 | 语言概念落到框、mask、region、属性和关系 | 指对了不等于持有空间状态 |
| 调用 | §24-§26 | prompt / instruction 让视觉成为可调用服务 | 接口扩张不等于状态闭合 |
| 遮蔽 | §27 | 语言先验暴露视觉盲区 | 能说对，不等于看对 |

这四条机制不是四个并列专题，而是阶段 III 的内在展开链：命名让视觉进入公共语义，指代让语义落回空间，调用让系统成为服务，遮蔽让阶段 III 意识到借来的语义不是自己的世界。

---

## 五、公共语义的材料层

阶段 III 的语言不是纯粹文本 token，而是社会语义制度。它包括 caption、alt-text、人类标签、对象 tag、指令、偏好、benchmark 问题、LLM prior 和评价 rubrics。

这意味着语言共形的本体代价不是简单的“文本噪声”，而是：

> 视觉模型把人类公共语义制度当作自己的语义骨架。

这套制度带来公共可调用性，也带来省略、偏见、礼貌、文化背景、任务偏好和评价外包。视觉进入公共语义，不等于视觉拥有公共语义的主权。

---

## 六、语义主权：谁决定什么算意义

语义主权不是模型能不能输出语义词，而是谁规定语义空间的坐标、粒度、边界、评价和纠错方式。阶段 III 的核心悖论在于：视觉获得了公共语义接口，却没有获得公共语义主权。

| 权能 | 阶段 III 是否拥有 | 说明 |
|---|---|---|
| 命名权 | 部分拥有 | 能输出名称，但名称来自语言制度、类别表、caption 和 LLM prior。 |
| 指代权 | 部分拥有 | 能指到区域、框、mask 或 token，但指代词和消歧规则来自语言。 |
| 调用权 | 较强 | prompt / instruction 可以调用任务，VLM 能在对话中复用视觉入口。 |
| 评价权 | 很弱 | 多由 benchmark、LLM judge、人类偏好和 rubric 控制。 |
| 生成权 | 未完成 | 阶段 III 不能稳定反向生产新观测，推出阶段 IV。 |
| 状态持有权 | 未完成 | 公共语义不等于对象、几何、遮挡、对应等视觉状态自持，推出阶段 V。 |

因此，阶段 III 的胜利不是“视觉获得自己的语义”，而是“视觉获得进入公共语言游戏的资格”。它的代价是：语义空间的主权仍然在语言制度手里。

---

## 七、语言的三层制度

| 层级 | 内容 | 技术表现 | 残差 |
|---|---|---|---|
| 语言形式层 | token、caption、prompt、phrase | CLIP text encoder、VLM prompt、referring expression | 语言歧义与提示敏感 |
| 语义制度层 | 类别、概念、命名习惯、文化偏见 | web-scale alt-text、标签空间、LLM prior | 未命名视觉被压扁 |
| 评价制度层 | benchmark、rubric、preference、judge | VQA、人类评测、LLM-as-judge、DPO/RLHF | 能讨好评测不等于看见 |

这三层说明：阶段 III 不是把“文本”接入视觉，而是把视觉接入一套社会语义制度。caption、instruction、judge 和 preference 都会塑造视觉系统最终保留什么、忽略什么、回答什么。

---

## 八、阶段 III 闭合制度矩阵

| 环节 | Z：表征域 | Π：接口 | Γ：变换族 | M：度量 | D：动力机制 | 遮蔽对象 |
|---|---|---|---|---|---|---|
| §21 外挂 | frozen region feature | VQA / caption / ITM | box / phrase / region | MLM / ITM / WRA | detector + BERT fusion | 原始像素与开放对象 |
| §22 对齐 | image-text embedding | retrieval / zero-shot / prompt classifier | caption / class prompt / web noise | InfoNCE / sigmoid contrastive | web-scale alignment | 空间、计数、方向、状态 |
| §23 稠密锚定 | dense CLIP / query feature | box / mask / region grounding | phrase / open vocab / spatial prompt | AP / mIoU / grounding | text-as-query / adapter | 指代后的状态关系 |
| §24 统一骨干 | multimodal shared representation | caption / VQA / grounding / task prompt | task prompt / output format | ITC / ITM / LM / seq2seq | multi-task VLP | 世界统一与度量主权 |
| §25 LLM 后端 | visual tokens in LLM space | dialogue / instruction / CoT | prompt / multi-image / resolution | VQA / judge / preference | projector / Q-Former / SFT | 视觉证据存活 |
| §26 像素调用 | language-conditioned mask token | bbox / mask / grounded output | region prompt / instruction | mask IoU / grounding score | pipeline / SEG token / decoder | 新观测生成与状态验证 |
| §27 账单清算 | failure cases / audit traces | benchmark stress / no-image control | counterfactual / adversarial pair | MMVP / MMStar / attention audit | error taxonomy / falsifier | 语言契约本身 |

这张表把阶段 III 从“模型谱系”压回闭合制度：每一章都在改变表征、接口、变换、度量或动力机制，但每一次成功都把某些视觉证据继续留在契约之外。

---

## 九、自我否定

阶段 III 的自我否定分三层：

| 层级 | 成功 | 自我否定 | 典型账单 |
|---|---|---|---|
| 命名的自我否定 | 视觉差异被语言命名 | 语言没有命名的视觉差异被压扁 | CLIP-blindness、方向、计数、状态 |
| 指代的自我否定 | 语言能指到框、mask、region | 指到某处不等于持有对象关系、几何状态和时间延续 | grounding 歧义、referring 失败 |
| 调用的自我否定 | prompt / instruction 让视觉系统灵活可用 | 接口成功不等于视觉主体性，回答成功不等于视觉自持 | no-image baseline、CoT 视觉衰减 |

阶段 III 的失败不是语言不够强。阶段 III 的失败恰恰来自语言太强：它能替视觉完成许多公共语义工作，因此遮蔽了视觉自身仍未闭合的部分。

---

## 十、一句话

> 视觉不是终于“拥有语言”，而是进入了语言的公共契约；这张契约让视觉获得命名、指代、调用和对话能力，但契约的主权仍在语言手里。
