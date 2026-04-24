from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple

import yaml


ROOT = Path(__file__).resolve().parents[2]
SITE_ROOT = ROOT / "docs_site"
DOCS_ROOT = SITE_ROOT / "docs"
CONFIG_PATH = SITE_ROOT / "mkdocs.yml"

TOP_LEVEL_ITEMS: List[Tuple[str, Path]] = [
    ("首页", ROOT / "INDEX.md"),
    ("00-公理层", ROOT / "00-公理层"),
    ("01-阶段I-判别共形", ROOT / "01-阶段I-判别共形"),
    ("02-阶段II-稠密共形", ROOT / "02-阶段II-稠密共形"),
    ("03-阶段III-语言共形", ROOT / "03-阶段III-语言共形"),
    ("04-阶段IV-生成共形", ROOT / "04-阶段IV-生成共形"),
    ("05-阶段V-表征共形", ROOT / "05-阶段V-表征共形"),
    ("横切", ROOT / "横切"),
    ("RS_CD", ROOT / "RS_CD"),
]

TOP_LEVEL_DIR_NAMES = {
    source.name
    for _, source in TOP_LEVEL_ITEMS
    if source.is_dir()
}

EXCLUDE_SITE_PARTS = {
    "导出残留",
    "归档",
    "90-归档导航.md",
    "展开债务审计.md",
}
COLLAPSED_NAV_DIRS: set[str] = set()

WINDOWS_ROOT_PATTERN = re.escape(ROOT.as_posix())
ABSOLUTE_MD_LINK = re.compile(
    rf"\((<?){WINDOWS_ROOT_PATTERN}/([^)>:]+?\.md)(?::\d+)?(>?)\)"
)
MARKDOWN_ANGLE_LINK = re.compile(r"(?<!\!)\[([^\]]+)\]\(<([^>]+)>\)")
MARKDOWN_LINK = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^()\s]+)\)")
LINE_SUFFIX_PATTERN = re.compile(r"(?P<path>.+?\.md):\d+$", re.IGNORECASE)
HOMEPAGE_TRIM_MARKER = "## 应用域（实验楼）"


def natural_sort_key(name: str):
    parts = re.split(r"(\d+)", name)
    key = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part.casefold())
    return key


def display_name(path: Path) -> str:
    if path.name == "index.md":
        return "首页"
    return path.stem if path.is_file() else path.name


def reset_generated_dirs() -> None:
    if DOCS_ROOT.exists():
        shutil.rmtree(DOCS_ROOT)
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)

    site_dir = SITE_ROOT / "site"
    if site_dir.exists():
        shutil.rmtree(site_dir)


def copy_selected_sources() -> None:
    def ignore_excluded(_directory: str, names: list[str]) -> set[str]:
        if Path(_directory).name in COLLAPSED_NAV_DIRS:
            return {name for name in names if name.lower() != "readme.md"}
        return {name for name in names if name in EXCLUDE_SITE_PARTS}

    for label, source in TOP_LEVEL_ITEMS:
        if source.is_file():
            target_name = "index.md" if source.name.upper() == "INDEX.MD" else source.name
            shutil.copy2(source, DOCS_ROOT / target_name)
        elif source.is_dir():
            shutil.copytree(source, DOCS_ROOT / source.name, ignore=ignore_excluded)


def relative_target_for(source_md: Path, target_rel: str) -> str:
    target_path = DOCS_ROOT / target_rel
    if target_rel == "INDEX.md":
        target_path = DOCS_ROOT / "index.md"
    rel = os.path.relpath(target_path, source_md.parent).replace("\\", "/")
    return rel


def markdown_path_target(path: str) -> str:
    if any(char in path for char in [" ", "(", ")"]):
        return f"<{path}>"
    return path


def rewrite_absolute_links(md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")

    def replace(match: re.Match) -> str:
        target_rel = match.group(2)
        rel = relative_target_for(md_path, target_rel)
        return f"({rel})"

    updated = ABSOLUTE_MD_LINK.sub(replace, text)
    if updated != text:
        md_path.write_text(updated, encoding="utf-8")


def choose_landing_page(directory: Path) -> Path | None:
    index_path = directory / "index.md"
    if index_path.exists():
        return index_path

    readme_path = directory / "README.md"
    if readme_path.exists():
        return readme_path

    preferred_exact = [
        "00-定位卡.md",
        "00-总纲.md",
        "00-总览.md",
        "00-阶段导读.md",
        "00-公理层导航.md",
        "90-阶段导航.md",
    ]
    for name in preferred_exact:
        candidate = directory / name
        if candidate.exists():
            return candidate

    preferred_prefixes = [
        "00-总纲",
        "00-",
        "90-",
    ]
    markdown_children = [
        child
        for child in directory.iterdir()
        if child.is_file()
        and child.suffix.lower() == ".md"
        and child.name.lower() not in {"index.md", "readme.md"}
    ]
    markdown_children.sort(key=lambda p: natural_sort_key(p.name))

    for prefix in preferred_prefixes:
        for child in markdown_children:
            if child.name.startswith(prefix):
                return child

    if markdown_children:
        return markdown_children[0]

    for child in sorted(directory.iterdir(), key=lambda p: natural_sort_key(p.name)):
        if child.is_dir():
            nested = choose_landing_page(child)
            if nested is not None:
                return nested
    return None


def build_index_content(directory: Path) -> str | None:
    children = [
        child
        for child in directory.iterdir()
        if not child.name.startswith(".")
        and child.name not in EXCLUDE_SITE_PARTS
    ]
    children.sort(key=lambda p: natural_sort_key(p.name))
    if not children:
        return None

    sections: List[str] = [f"# {directory.name}", "", "> 自动生成的章节入口页。", ""]

    landing = choose_landing_page(directory)
    if landing is not None and landing.name.lower() != "index.md":
        landing_rel = os.path.relpath(landing, directory).replace("\\", "/")
        sections.extend(
            [
                "## 推荐入口",
                "",
                f"- [{landing.stem}]({markdown_path_target(landing_rel)})",
                "",
            ]
        )

    markdown_children = [
        child for child in children
        if child.is_file() and child.suffix.lower() == ".md" and child.name.lower() != "readme.md"
    ]
    if markdown_children:
        sections.append("## 文件")
        sections.append("")
        for child in markdown_children:
            sections.append(f"- [{child.stem}]({markdown_path_target(child.name)})")
        sections.append("")

    subdirs = [child for child in children if child.is_dir()]
    if subdirs:
        sections.append("## 子目录")
        sections.append("")
        for child in subdirs:
            sections.append(f"- [{child.name}]({markdown_path_target(f'{child.name}/')})")
        sections.append("")

    asset_children = [
        child for child in children
        if child.is_file()
        and child.suffix.lower() != ".md"
    ]
    if asset_children:
        sections.append("## 附属文件")
        sections.append("")
        for child in asset_children:
            sections.append(f"- [{child.name}]({markdown_path_target(child.name)})")
        sections.append("")

    return "\n".join(sections).rstrip() + "\n"


def generate_directory_indexes() -> None:
    directories = sorted(
        [path for path in DOCS_ROOT.rglob("*") if path.is_dir()],
        key=lambda p: (len(p.relative_to(DOCS_ROOT).parts), natural_sort_key(p.name)),
    )
    for directory in directories:
        index_path = directory / "index.md"
        if index_path.exists():
            continue

        readme_path = directory / "README.md"
        if readme_path.exists():
            shutil.copy2(readme_path, index_path)
            readme_path.unlink()
            continue

        content = build_index_content(directory)
        if content is not None:
            index_path.write_text(content, encoding="utf-8")


def resolve_internal_target(md_path: Path, target: str) -> str | None:
    stripped = target.strip()
    if not stripped:
        return None

    if stripped.startswith("<") and stripped.endswith(">"):
        stripped = stripped[1:-1]

    if stripped.startswith(("http://", "https://", "mailto:", "#")):
        return None

    anchor = ""
    if "#" in stripped:
        stripped, fragment = stripped.split("#", 1)
        anchor = f"#{fragment}"

    stripped = stripped.replace("\\", "/")

    line_match = LINE_SUFFIX_PATTERN.match(stripped)
    if line_match:
        stripped = line_match.group("path")

    if stripped.startswith(ROOT.as_posix() + "/"):
        stripped = stripped[len(ROOT.as_posix()) + 1 :]

    if stripped == "INDEX.md":
        candidate = DOCS_ROOT / "index.md"
    else:
        candidate = (md_path.parent / stripped).resolve()

    try:
        candidate.relative_to(DOCS_ROOT.resolve())
    except ValueError:
        return None

    if candidate.name.lower() == "readme.md":
        index_candidate = candidate.with_name("index.md")
        if index_candidate.exists():
            candidate = index_candidate

    if candidate.is_dir():
        landing = choose_landing_page(candidate)
        if landing is None:
            return None
        candidate = landing

    if not candidate.exists():
        return None

    rel = os.path.relpath(candidate, md_path.parent).replace("\\", "/")
    return f"{rel}{anchor}"


def rewrite_internal_links(md_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")

    def is_external_target(raw_target: str) -> bool:
        stripped = raw_target.strip()
        if stripped.startswith("<") and stripped.endswith(">"):
            stripped = stripped[1:-1]
        return stripped.startswith(("http://", "https://", "mailto:", "#"))

    def replace(match: re.Match) -> str:
        label = match.group(1)
        raw_target = match.group(2)
        rewritten = resolve_internal_target(md_path, raw_target)
        if rewritten is None:
            if not is_external_target(raw_target):
                return label
            return match.group(0)
        return f"[{label}]({markdown_path_target(rewritten)})"

    updated = MARKDOWN_ANGLE_LINK.sub(replace, text)
    updated = MARKDOWN_LINK.sub(replace, updated)
    if updated != text:
        md_path.write_text(updated, encoding="utf-8")


def sanitize_homepage() -> None:
    index_path = DOCS_ROOT / "index.md"
    if not index_path.exists():
        return

    text = index_path.read_text(encoding="utf-8")
    if HOMEPAGE_TRIM_MARKER not in text:
        return

    kept = text.split(HOMEPAGE_TRIM_MARKER, 1)[0].rstrip()
    note = (
        "\n\n---\n\n"
        "## 本站范围\n\n"
        "- 当前首版已纳入：`INDEX`、`00-公理层`、`01-05 阶段`、`横切`、`RS_CD`\n"
        "- 当前首版暂未纳入：`应用域`、`skills`、`工具`\n"
        "- 本地原始仓库仍保留这些目录；本次 GitHub Pages 初版只发布主线阅读层\n"
    )
    index_path.write_text(kept + note, encoding="utf-8")


def rewrite_markdown_links() -> None:
    for md_path in DOCS_ROOT.rglob("*.md"):
        rewrite_absolute_links(md_path)
    for md_path in DOCS_ROOT.rglob("*.md"):
        rewrite_internal_links(md_path)


def build_directory_nav(rel_dir: Path) -> List[object]:
    absolute_dir = DOCS_ROOT / rel_dir
    items: List[object] = []

    index_path = absolute_dir / "index.md"
    if absolute_dir.name in COLLAPSED_NAV_DIRS:
        return [index_path.relative_to(DOCS_ROOT).as_posix()] if index_path.exists() else []

    children = [
        child
        for child in absolute_dir.iterdir()
        if not child.name.startswith(".")
        and child.name not in EXCLUDE_SITE_PARTS
        and (child.is_dir() or child.suffix.lower() == ".md")
    ]
    children.sort(key=lambda p: natural_sort_key(p.name))

    if index_path.exists():
        items.append(index_path.relative_to(DOCS_ROOT).as_posix())

    for child in children:
        child_rel = child.relative_to(DOCS_ROOT)
        if child.is_dir():
            nested = build_directory_nav(child_rel)
            if nested:
                items.append({display_name(child): nested})
        elif child.name.lower() not in {"index.md", "readme.md"}:
            items.append({display_name(child): child_rel.as_posix()})
    return items


def build_nav() -> List[object]:
    nav: List[object] = [{"首页": "index.md"}]
    for label, source in TOP_LEVEL_ITEMS[1:]:
        if source.is_dir():
            nav.append({label: build_directory_nav(Path(source.name))})
    return nav


def generate_config() -> None:
    config = {
        "site_name": "视觉理论大厦",
        "site_description": "一致性建模知识库",
        "docs_dir": "docs",
        "site_dir": "site",
        "use_directory_urls": True,
        "theme": {
            "name": "material",
            "language": "zh",
            "font": False,
            "features": [
                "navigation.indexes",
                "navigation.tabs",
                "navigation.sections",
                "navigation.top",
                "navigation.tracking",
                "search.highlight",
                "search.suggest",
                "toc.follow",
                "content.code.copy",
            ],
            "palette": [
                {
                    "media": "(prefers-color-scheme: light)",
                    "scheme": "default",
                    "primary": "custom",
                    "accent": "custom",
                    "toggle": {
                        "icon": "material/weather-night",
                        "name": "切换到深色模式",
                    },
                },
                {
                    "media": "(prefers-color-scheme: dark)",
                    "scheme": "slate",
                    "primary": "custom",
                    "accent": "custom",
                    "toggle": {
                        "icon": "material/weather-sunny",
                        "name": "切换到浅色模式",
                    },
                },
            ],
        },
        "plugins": ["search"],
        "markdown_extensions": [
            "admonition",
            "attr_list",
            "md_in_html",
            "tables",
            "toc",
            "pymdownx.details",
            "pymdownx.superfences",
            "pymdownx.highlight",
            "pymdownx.inlinehilite",
            "pymdownx.tabbed",
        ],
        "extra_css": ["assets/stylesheets/extra.css"],
        "nav": build_nav(),
    }

    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            config,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=100,
        )


def main() -> None:
    reset_generated_dirs()
    copy_selected_sources()
    generate_directory_indexes()
    rewrite_markdown_links()
    sanitize_homepage()
    generate_config()
    print(f"Generated docs mirror at: {DOCS_ROOT}")
    print(f"Generated config at: {CONFIG_PATH}")


if __name__ == "__main__":
    main()
