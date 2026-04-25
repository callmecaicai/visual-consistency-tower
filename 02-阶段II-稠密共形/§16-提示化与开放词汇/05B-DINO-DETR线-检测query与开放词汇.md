# 05B · DINO-DETR 线：检测 query 与开放词汇

本页从原“05-两条DINO线”中拆出，专门处理 DINO-DETR / Grounding DINO / DINO-X 这一条检测与开放词汇线。

## 本线定位

| 项 | 内容 |
|---|---|
| 所属闭合 | 阶段 II 的对象闭合与接口闭合。 |
| 主要对象 | box / object query / text-conditioned detection。 |
| 语义来源 | 类别表、文本 embedding、grounding 数据和开放词汇训练。 |
| 阶段 II 功能 | 让检测从封闭类别表走向文本条件与开放词汇。 |
| 残差 | query 负责绑定证据，文本负责赋义；语义仍不完全属于视觉自身。 |

## 从 DINO-DETR 到 Grounding DINO

DINO-DETR 的核心是让 DETR 式 query 更快、更稳地收敛：显式位置、去噪训练、匹配制度和多监督共同降低原始 DETR 的训练成本。

Grounding DINO 则把文本引入这套检测制度：文本不再只是输出标签，而成为检测 query / condition 的语义来源。

这条线的关键不是“检测精度更高”，而是：

> 对象槽位开始接受公共语言的调用。

## DINO-X 的位置

DINO-X / T-Rex2 等后续系统继续把检测 query、示例提示、开放词汇和数据引擎接在一起，使“找所有这种东西”成为一种服务化接口。

但这种开放依然要区分两层：

- 绑定层：query / box / matching 规定哪片证据归哪个输出。
- 意义层：文本、示例、类别体系规定这个输出“是什么”。

## 出口残差

本线最适合承担阶段 II 到阶段 III 的桥：

> 检测 query 已经能被语言调用，但语言的进入同时暴露出语义主权仍在视觉系统之外。
