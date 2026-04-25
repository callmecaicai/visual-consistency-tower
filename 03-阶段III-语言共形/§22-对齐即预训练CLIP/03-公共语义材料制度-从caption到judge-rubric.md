# 公共语义材料制度：从 caption 到 judge rubric

作者 / 机构: —
共形维度: 材料, 度量
关键贡献: 把阶段 III 的语言材料从“文本监督”提升为“公共语义制度”。caption、alt-text、query balancing、instruction、preference、judge rubric 都不是中性输入，而是决定视觉系统能命名什么、忽略什么、如何被评价的材料法律。本页是 §22 的材料制度补页，也为 §27 的账单清算提供根因层。
类型: 理论/分析
阶段: III · 语言共形的深化

## 章首协议

| 问项 | 本页回答 |
|---|---|
| 纯存在态 | `Image-Text Corpus -> Public Semantic Coordinate`：图文材料被制度化为公共语义坐标。 |
| 稳定差异 | caption、alt-text、query、instruction、rubric 中反复出现并能与图像对齐的差异。 |
| 闭合制度 | `C_22B=(Z_image-text, Π_retrieval/prompt/judge, Γ_caption/query/noise, M_contrastive/judge/preference, D_data-curation/alignment)`。 |
| 成功标准 | web-scale 对齐空间可复用，可支持 zero-shot、检索、开放词汇和 VLM 前端。 |
| 遮蔽对象 | caption 没写出的方向、计数、细粒度空间、状态、遮挡、局部关系。 |
| 内在残差 | caption 稳定了公共语义，也把视觉压进“可描述的视觉子空间”。 |

## 一、材料制度不是数据清单

阶段 III 的材料不是“很多图文对”这么简单。

它是一套公共语义材料制度：

| 材料层 | 典型形式 | 它规定什么 | 它遮蔽什么 |
|---|---|---|---|
| caption / alt-text | web image-text pair | 哪些视觉差异值得被自然语言描述 | 未描述的方向、计数、遮挡、状态 |
| query balancing | CLIP / MetaCLIP 式采样策略 | 哪些词、概念和长尾类别进入训练分布 | 非 query 覆盖的视觉结构 |
| instruction data | VQA / dialogue / synthetic instruction | 哪些视觉任务可被语言调用 | 不适合问答格式的状态变量 |
| preference data | human preference / DPO / RLHF | 什么回答被认为好、礼貌、可信 | 不讨好偏好但视觉上真实的证据 |
| judge rubric | benchmark / LLM-as-judge | 什么输出算通过 | 能讨好题面但不看图的捷径 |

因此，阶段 III 不是“视觉遇到文本”，而是视觉被纳入一套社会语义生产、筛选和评价制度。

## 二、caption-stabilized visual subspace

CLIP 之所以强，是因为 caption 把大量公共语义坐标稳定下来：物体名、场景名、动作、常见属性、社会类别、风格和文本中常被提及的关系。

但这个空间不是完整视觉空间，而是：

```text
C_caption = visual differences repeatedly stabilized by captions
```

可以称为：

> caption-stabilized visual subspace

它的正面意义是公共可调用性：模型终于能把图像放进人类可命名的语义空间。

它的负面代价是视觉压缩：caption 不写的视觉差异，即使在图像中稳定存在，也很难成为对齐目标。

## 三、query balancing 的制度意义

MetaCLIP 的关键启发不只是“数据更多”或“模型更大”，而是重建了 CLIP 式 query balancing 的材料治理逻辑：

```text
哪些词被拿来采样？
每个词允许多少图文对？
长尾如何不被热门词吞没？
噪声如何被保留、过滤或重新加权？
```

这说明公共语义不是自然流入模型的，它需要采样制度。query balancing 是阶段 III 的材料层法律：它决定哪些概念获得训练带宽，哪些概念继续留在公共语义契约之外。

## 四、从 caption 到 judge

阶段 III 后半程，语言材料不只负责训练视觉，也负责裁判视觉：

```text
caption -> prompt -> instruction -> rationale -> preference -> judge rubric
```

这条链让 VLM 获得对话、解释和评估能力，也让语言制度进一步接管“什么算看懂”的定义。

因此，阶段 III 的度量残差不是单纯 benchmark 噪声，而是评价主权外包：

> 视觉系统越依赖语言评价，越可能学会满足语言裁判，而不是保留视觉证据。

## 五、进入 §27 的账单

| 账单 | 材料根因 |
|---|---|
| CLIP-blindness | caption 对方向、计数、空间关系、状态覆盖不足 |
| no-image baseline | benchmark 题面携带过多语言线索 |
| 感知故障伪装成推理故障 | instruction / rationale 倾向把错误包装成推理链 |
| CoT 视觉衰减 | 推理材料主要在语言空间展开，视觉 token 逐步边缘化 |

这就是 §22 到 §27 的根链：caption 让视觉进入公共语义，也让视觉欠下未命名差异的债。

## 六、一句话

> 阶段 III 的材料不是文本，而是公共语义制度；它给视觉公共名字，也规定视觉的失明边界。
