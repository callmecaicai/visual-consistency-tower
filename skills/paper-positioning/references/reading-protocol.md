# Reading Protocol

## Purpose

Prevent full-repository scanning. Enforce a layered read policy that matches the repository's context limits.

## Tiers

### T0 · Global Entry

Read only these files first:

- `INDEX.md`
- stage-level `00-总纲` or `00-阶段导读`
- `90-*` navigation/protocol files

Use when the task only asks for a stage-level judgement.

### T1 · Positioning

Read:

- `横切/知识库编号与索引协议.md`
- target chapter `00-定位卡.md`

Use when the task asks for chapter-level location.

### T2 · Main Mechanism

Read:

- `01-机制展开.md`
- `01-总纲扩展-*`
- stage `结语*`

Use when the chapter is known but the mechanism needs confirmation.

### T3 · Expansion Evidence

Read:

- `02+` 扩展稿
- 专题稿
- 补章

Use when T1/T2 cannot distinguish nearby mechanisms.

### T4 · Archive / Domain Evidence

Read:

- `应用域`
- `归档`

Use only after a main chapter anchor exists.

## Stop Conditions

Stop descending when all four items are stable:

1. primary stage
2. primary chapter
3. minimal read tier
4. write target

If all four are stable at `T1`, do not continue to `T2-T4`.
