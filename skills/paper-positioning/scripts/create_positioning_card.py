from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """# 新对象定位卡

对象: {title}
对象类型: {kind}

主阶段: {stage}
主章节: {chapter}
次级关联: {secondary}
读取建议: {tier}

输入输出:
- 输入:
- 输出:

共形维度:
- 

归属理由:
1.
2.
3.

边界排除:
- 不优先归入:
  理由:
- 不优先归入:
  理由:

建议写入位置:
- 主线:
- 应用域:
- 暂不写入:

最小必读文件:
- 
- 
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a positioning card stub for a new paper or project.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--kind", default="论文")
    parser.add_argument("--stage", default="")
    parser.add_argument("--chapter", default="")
    parser.add_argument("--secondary", default="")
    parser.add_argument("--tier", default="T1")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        TEMPLATE.format(
            title=args.title,
            kind=args.kind,
            stage=args.stage,
            chapter=args.chapter,
            secondary=args.secondary,
            tier=args.tier,
        ),
        encoding="utf-8",
    )
    print(path)


if __name__ == "__main__":
    main()
