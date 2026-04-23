---
name: kb-incremental-update
description: Update this layered markdown knowledge base after a paper or requirement has already been positioned. Use when the task is to add, merge, rename, scaffold, or revise markdown files while preserving numbering, directory roles, and cross-stage consistency.
---

# Kb Incremental Update

## Overview

Apply consistent, minimal updates to the repository after a location decision already exists. Preserve numbering, stage boundaries, and the `主线 / 应用域 / 归档 / 工具 / skills` role split.

## Apply This Skill When

Apply when the task is any of the following:

- add a new paper note into the right place
- merge fresh content into an existing chapter
- create a new `02+` expansion draft
- scaffold a new chapter directory in stage IV or V
- rename files to match numbering rules
- update navigation after structural changes

Do not apply this skill before a location decision exists. Call `paper-positioning` first.

## Minimal Read Order

Read in the following order:

1. Read [references/update-policy.md](references/update-policy.md)
2. Read [references/change-matrix.md](references/change-matrix.md)
3. Read the exact target directory only
4. Read `INDEX.md` or `90-*` navigation only if visible entry points change

Do not open unrelated stages.

## Workflow

### 1. Confirm the write target

Require these four items before editing:

- primary stage
- primary chapter
- write type
- visibility level

If any item is missing, stop and run `paper-positioning`.

### 2. Choose the smallest valid write type

Prefer this order:

1. update existing `02+` expansion file
2. create a new `02+` expansion or `03-专题` file inside an existing chapter
3. update an existing `00-定位卡` or `01-机制展开`
4. write to `应用域`
5. create a new chapter directory

Treat `create a new chapter directory` as exceptional.

### 3. Preserve numbering and roles

Enforce these rules:

- stage root: `00-*`, `01-*`, `§xx-*`, `结语*`, `90-*`
- chapter root: `00-定位卡`, `01-机制展开`, `02+`, `03+`, `90+`
- archive material stays in `归档`
- domain evidence stays in `应用域`
- agent workflow files stay in `skills`
- viewer/script utilities stay in `工具`

Do not scatter fresh Markdown files into a stage root when a chapter directory already exists.

### 4. Update visible entry points

Update only what changed:

- `INDEX.md` if the structure visible from root changed
- stage `90-*` navigation if chapter structure changed
- stage total-state docs if the chapter maturity meaningfully changed

Avoid cosmetic churn.

### 5. Emit a concise update note

Record:

- what changed
- why this target was chosen
- what was intentionally not changed

Prefer using [assets/kb-update-note-template.md](assets/kb-update-note-template.md). When a repeatable stub is helpful, run [scripts/create_update_note.py](scripts/create_update_note.py).

## Decision Rules

Apply these rules strictly:

- New evidence for an existing mechanism: write to `02+`
- Domain-specific case study: write to `应用域`, then backlink conceptually to main chapter
- Canonical theory shift inside an existing chapter: update `00/01`
- New residual chain with no valid host chapter: create a new chapter only after checking the stage bandwidth
- Export leftovers or old drafts: move to `归档`, do not mix into active directories

## Refusal Rules

Refuse the larger structural move when a smaller move already solves the problem.

Examples:

- Do not create a new stage for a single paper
- Do not create a new chapter when an existing `02+` file can host the material
- Do not rewrite old stages for stylistic uniformity unless the task explicitly asks for refactor-level cleanup

## Resources

- [references/update-policy.md](references/update-policy.md): numbering and role rules
- [references/change-matrix.md](references/change-matrix.md): mapping from update type to file target
- [assets/kb-update-note-template.md](assets/kb-update-note-template.md): reusable update summary
- [scripts/create_update_note.py](scripts/create_update_note.py): deterministic update-note stub generator
