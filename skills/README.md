# Skills

这个目录是这座知识库的 agent-first 运行时。

核心判断：

- 这座仓库的主要消费者不是一次性通读全库的人，而是上下文有限、需要快速落位的 agent。
- 因此最重要的配套物不是复杂软件，而是稳定的 skill 协议。
- `工具/轻量MD查看器原型` 是辅助浏览器；`skills/` 才是后续真正的执行入口。

当前技能：

- [paper-positioning](paper-positioning/SKILL.md)
  负责把新论文、新模型、新 benchmark、新项目需求快速落到 `阶段 / 章节 / 读取层级 / 更新目标`。
- [kb-incremental-update](kb-incremental-update/SKILL.md)
  负责在落位之后，对知识库进行最小但一致的增量更新。

建议工作流：

1. 先调用 `paper-positioning`
2. 再调用 `kb-incremental-update`
3. 必要时才打开查看器或下钻应用域 / 归档

最小原则：

- 先定位，后阅读
- 先主线，后证据
- 先增量更新，后结构扩张
- 非必要不新建章节，非必要不改主编号
