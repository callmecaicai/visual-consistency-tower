from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# 知识库增量更新记录

更新对象: {title}
更新类型: {change_type}

定位前提:
- 主阶段: {stage}
- 主章节: {chapter}
- 读取层级: {tier}

本次变更:
1.
2.
3.

选择该位置的原因:
1.
2.

未改动部分:
- 
- 

需要同步的导航:
- INDEX:
- 阶段导航:
- 无:

后续待补:
- 
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a knowledge-base update note stub.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--change-type", default="扩展稿")
    parser.add_argument("--stage", default="")
    parser.add_argument("--chapter", default="")
    parser.add_argument("--tier", default="T2")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        TEMPLATE.format(
            title=args.title,
            change_type=args.change_type,
            stage=args.stage,
            chapter=args.chapter,
            tier=args.tier,
        ),
        encoding="utf-8",
    )
    print(path)


if __name__ == "__main__":
    main()
