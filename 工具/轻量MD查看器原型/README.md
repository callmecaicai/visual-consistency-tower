# 轻量 MD 查看器原型

这是一个零依赖、静态文件可打开的知识库查看器雏形，目标不是替代写作，而是把这座大厦变成“可被快速定位和消费”的分层索引系统。

## 目标

- 用目录、编号、元数据头把整座知识库变成机器可读结构。
- 让人或 agent 在面对一篇新论文 / 一个新项目需求时，先快速判断它落在哪一层、哪一章、响应哪条残差。
- 保持足够轻量：纯 HTML / CSS / JS + 一个 Python 索引脚本。

## 当前能力

1. 浏览 `00-公理层`、阶段 I-V、`横切`、`应用域` 的结构化索引。
2. 按阶段、章节、文档角色快速过滤。
3. 按 `T0-T4` 分层读取顺序组织文档，不鼓励全库扫读。
4. 读取 Markdown 文件前部元数据与内容摘要。
5. 对新输入做本地关键词定位，给出章节候选与相关文档候选。
6. 直接跳转到原始 Markdown 文件。
7. 支持 URL 参数深链：`?q=...` 用于文档筛选，`?locate=...&chapter=§25` 用于直接打开定位上下文。

## 文件结构

- `viewer/index.html`：静态页面入口
- `viewer/styles.css`：样式
- `viewer/app.js`：交互逻辑与定位器
- `viewer/data/knowledge-base.js`：由脚本生成的索引数据
- `scripts/build_knowledge_manifest.py`：扫描知识库并生成索引

## 使用方式

1. 运行：

```powershell
python .\工具\轻量MD查看器原型\scripts\build_knowledge_manifest.py
```

2. 打开：

```powershell
start .\工具\轻量MD查看器原型\viewer\index.html
```

如果后续需要更稳定的本地预览，也可以在仓库根目录临时起一个静态服务：

```powershell
python -m http.server 8080
```

然后访问 `http://localhost:8080/工具/轻量MD查看器原型/viewer/`。

## 下一步建议

- 把 `定位标签:` 逐步补到新的正式文档头部。
- 给阶段 IV、V 从一开始就按目录化章节协议写作。
- 后续若要接 agent，可把“新论文定位结果”直接输出成一张标准 `定位卡`。
- 若要进一步自动化，可让 agent 先只读 `T0/T1`，确认定位后再授权它下钻 `T2/T3`。
