# MkDocs 文档站初版

这套目录是给当前知识库做 **HTML 可视化 / GitHub Pages 部署** 用的构建层。

它不会改写原始知识库内容，而是：

1. 从根目录选取指定的 Markdown 内容
2. 复制到 `docs_site/docs/` 作为构建镜像
3. 自动生成 `mkdocs.yml` 导航
4. 用 `MkDocs Material` 输出成适合手机阅读的静态网站

## 当前接入范围

- `INDEX.md`
- `00-公理层`
- `01-阶段I-判别共形`
- `02-阶段II-稠密共形`
- `03-阶段III-语言共形`
- `04-阶段IV-生成共形`
- `05-阶段V-表征共形`
- `横切`
- `RS_CD`

## 目录说明

- `scripts/build_mkdocs_site.py`：同步源 Markdown 并生成导航配置
- `requirements.txt`：本地构建依赖
- `assets/stylesheets/extra.css`：少量移动端和排版样式覆盖
- `docs/`：生成的文档镜像目录
- `site/`：MkDocs 构建后的 HTML 输出

## 本地使用

建议先用虚拟环境，避免和当前 Python / Conda 环境里的科研包发生依赖冲突：

```powershell
python -m venv .venv-docs
.\.venv-docs\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\docs_site\requirements.txt
```

如果你确定直接装到当前环境，也可以这样：

```powershell
python -m pip install -r .\docs_site\requirements.txt
```

生成文档镜像与导航：

```powershell
python .\docs_site\scripts\build_mkdocs_site.py
```

本地预览：

```powershell
python -m mkdocs serve -f .\docs_site\mkdocs.yml
```

构建静态站点：

```powershell
python -m mkdocs build -f .\docs_site\mkdocs.yml
```

## GitHub Pages

仓库根目录已经放置：

- `.github/workflows/deploy-docs.yml`

只要这个目录进入 Git 仓库并推到 GitHub，Pages 工作流就会：

1. 安装依赖
2. 运行 `build_mkdocs_site.py`
3. 构建静态站点
4. 发布到 GitHub Pages

GitHub 端还需要确认两件事：

1. 仓库默认分支是 `main`；如果不是，需要改 workflow 触发分支。
2. 仓库 `Settings -> Pages` 使用 `GitHub Actions` 作为部署方式。

## 注意

- 目前会自动修正一部分 `D:/AboveAll_A_World/...` 形式的绝对 Markdown 链接，把它们转成站点内相对链接。
- 如果后续新文档继续写入本地绝对路径，重新运行构建脚本即可。
- 这版重点是“先可读、可导航、可手机访问”，不是做复杂交互站点。
