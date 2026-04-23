---
name: paper-positioning
description: Determine where a new paper, model, benchmark, or project requirement belongs in this layered markdown knowledge base. Use when a task asks which stage or chapter something belongs to, what minimal documents to read first, or how a new item should be positioned before updating the repository.
---

# Paper Positioning

## Overview

Determine the primary location of a new paper, model, benchmark, or project requirement inside this knowledge base without scanning the whole repository. Produce a stable positioning result that downstream update work can consume directly.

## Apply This Skill When

Apply when encountering any of these situations:

- A new paper arrives and needs a `阶段 / 章节` judgement.
- A new project requirement arrives and needs a theoretical location before implementation or writing.
- A request asks which files to read first instead of reading the whole repository.
- A request asks whether something belongs to主线、应用域、归档，还是应暂时不写入仓库。

Do not apply this skill after the location is already known and the task is purely editorial. In that case, hand off to `kb-incremental-update`.

## Minimal Read Order

Read in the following order and stop as soon as the location is stable:

1. Read [references/reading-protocol.md](references/reading-protocol.md)
2. Read [references/stage-map.md](references/stage-map.md)
3. Read [../../../INDEX.md](../../../INDEX.md) only to confirm concrete paths
4. Read a target chapter `00-定位卡.md` only after a chapter candidate exists
5. Read `01-机制展开` or `02+` only if chapter-level ambiguity remains

Do not default to reading all Markdown files in a stage.

## Workflow

### 1. Normalize the input

Extract the minimum problem statement:

- Input / output
- Main task type
- Primary technical novelty
- Claimed capability
- Failure mode or residual if present

### 2. Decide the primary stage

Use [references/stage-map.md](references/stage-map.md) and force a primary stage choice:

- Stage I: classification, label prediction, optimization, CNN training dynamics
- Stage II: dense prediction, detection, segmentation, query, promptable dense vision
- Stage III: language enters the visual backbone, VLM understanding, grounding, instruction following
- Stage IV: generation, diffusion, GAN, video/world generation, image synthesis as understanding
- Stage V: representation prediction, JEPA, DINO-style self-supervision, non-generative understanding

When the item spans two stages, record one primary stage and one secondary stage. Do not split the item across multiple primary stages.

### 3. Decide the primary chapter

After the stage is stable, map to a chapter candidate:

- Prefer the chapter that explains the main mechanism, not the most famous model name.
- Prefer the chapter that absorbs the main residual, not the newest date.
- Route application-only material to `应用域` only after a main chapter anchor exists.

### 4. Decide the retrieval depth

Assign a minimal read set:

- `T0`: global entry and navigation are enough
- `T1`: chapter `00-定位卡` is needed
- `T2`: `01-机制展开` is needed
- `T3`: `02+` evidence is needed
- `T4`: `应用域` or `归档` is needed

Prefer the shallowest tier that resolves the task.

### 5. Decide the write target

Produce one of these outcomes:

- `主线已有位置，无需新增文件`
- `写入现有章节的 02+ 扩展稿`
- `写入 应用域，并反链到主章节`
- `需要新建章节骨架`
- `暂不入库，只记录定位结论`

Treat `需要新建章节骨架` as a high bar.

## Output Contract

Produce the result in this exact shape whenever possible:

```md
# 新对象定位卡

对象: ...
对象类型: 论文 / 项目需求 / benchmark / 模型

主阶段: ...
主章节: ...
次级关联: ...
读取建议: T0 / T1 / T2 / T3 / T4

归属理由:
1. ...
2. ...
3. ...

边界排除:
- 不优先归入 ...，因为 ...
- 不优先归入 ...，因为 ...

建议写入位置:
- ...

最小必读文件:
- ...
- ...
```

Prefer using the bundled template [assets/paper-positioning-card-template.md](assets/paper-positioning-card-template.md). When a repeatable stub is useful, run [scripts/create_positioning_card.py](scripts/create_positioning_card.py).

## Chapter Boundary Rules

Apply these boundary rules strictly:

- `III` vs `IV`: understanding-side VLM stays in III; image/video generation moves to IV
- `IV` vs `V`: pixel-space reconstruction/generation stays in IV; representation prediction without generation moves to V
- `主线` vs `应用域`: domain evidence goes to `应用域`; mechanism-defining theory stays in stage chapters
- `应用域` vs `归档`: current-use evidence goes to `应用域`; old exports or non-canonical drafts stay in `归档`

## Resources

- [references/reading-protocol.md](references/reading-protocol.md): T0-T4 read order and stop conditions
- [references/stage-map.md](references/stage-map.md): stage and chapter heuristics
- [assets/paper-positioning-card-template.md](assets/paper-positioning-card-template.md): reusable output template
- [scripts/create_positioning_card.py](scripts/create_positioning_card.py): deterministic card stub generator
