from __future__ import annotations

import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VIEWER_DIR = ROOT / "工具" / "轻量MD查看器原型" / "viewer"
OUTPUT_FILE = VIEWER_DIR / "data" / "knowledge-base.js"

EXCLUDE_TOP_LEVEL = {"ZIP合并", ".claude", "工具", "docs_site"}
EXCLUDE_PARTS = {"导出残留"}

TOP_LEVEL_ORDER = [
    "ROOT",
    "00-公理层",
    "01-阶段I-判别共形",
    "02-阶段II-稠密共形",
    "03-阶段III-语言共形",
    "04-阶段IV-生成共形",
    "05-阶段V-表征共形",
    "横切",
    "应用域",
    "skills",
]

SELECTED_META_KEYS = [
    "标题",
    "类型",
    "阶段",
    "共形维度",
    "关键贡献",
    "残差 / 它催生了什么",
    "要点",
    "定位标签",
]

LOCATOR_SCHEMA = [
    {
        "id": "stage-I",
        "level": "stage",
        "stage": "I",
        "title": "阶段 I · 判别共形",
        "summary": "整图到标签，核心问题是分类、判别、优化、卷积归纳偏置。",
        "keywords": [
            "classification",
            "classifier",
            "label",
            "分类",
            "标签",
            "判别",
            "cnn",
            "alexnet",
            "resnet",
            "relu",
            "batchnorm",
            "optimizer",
            "数据增强",
            "loss",
        ],
    },
    {
        "id": "§01",
        "level": "chapter",
        "stage": "I",
        "title": "§01 奠基与数据地基",
        "summary": "数据集、标注、训练地基、基准构成问题。",
        "keywords": ["imagenet", "dataset", "benchmark", "数据集", "标注", "训练地基"],
    },
    {
        "id": "§02",
        "level": "chapter",
        "stage": "I",
        "title": "§02 AlexNet冲击与深度竞赛",
        "summary": "深度 CNN 成为主轴，竞赛式提升出现。",
        "keywords": ["alexnet", "深度网络", "convnet", "1x1", "卷积竞赛"],
    },
    {
        "id": "§03",
        "level": "chapter",
        "stage": "I",
        "title": "§03 激活·初始化·正则",
        "summary": "训练动力学从可训性角度展开。",
        "keywords": ["初始化", "activation", "dropout", "regularization", "正则", "xavier"],
    },
    {
        "id": "§04",
        "level": "chapter",
        "stage": "I",
        "title": "§04 Inception族与归一化",
        "summary": "网络宽度组织、归一化与结构并行化。",
        "keywords": ["inception", "batchnorm", "normalization", "归一化"],
    },
    {
        "id": "§05",
        "level": "chapter",
        "stage": "I",
        "title": "§05 优化器与残差革命",
        "summary": "优化器与残差网络把深层训练推到新阶段。",
        "keywords": ["optimizer", "adam", "sgd", "residual", "resnet", "残差网络"],
    },
    {
        "id": "stage-II",
        "level": "stage",
        "stage": "II",
        "title": "阶段 II · 稠密共形",
        "summary": "整图到稠密场，检测、分割、query、提示化都在此层。",
        "keywords": [
            "segmentation",
            "detection",
            "mask",
            "dense",
            "稠密",
            "检测",
            "分割",
            "iou",
            "detr",
            "sam",
            "open vocabulary",
        ],
    },
    {
        "id": "§11",
        "level": "chapter",
        "stage": "II",
        "title": "§11 全卷积转向",
        "summary": "从整图分类转向逐像素预测。",
        "keywords": ["fcn", "全卷积", "pixel-wise", "dense prediction"],
    },
    {
        "id": "§12",
        "level": "chapter",
        "stage": "II",
        "title": "§12 空洞卷积与多尺度",
        "summary": "感受野、空洞、多尺度汇聚。",
        "keywords": ["dilation", "aspp", "空洞卷积", "多尺度", "deeplab"],
    },
    {
        "id": "§13",
        "level": "chapter",
        "stage": "II",
        "title": "§13 检测共形的流水线化",
        "summary": "proposal、anchor、两阶段检测流水线。",
        "keywords": ["faster r-cnn", "proposal", "anchor", "检测流水线"],
    },
    {
        "id": "§14",
        "level": "chapter",
        "stage": "II",
        "title": "§14 Anchor-free与端到端查询",
        "summary": "从 anchor-free 到 DETR/query 本体论。",
        "keywords": ["anchor-free", "detr", "query", "yolo", "hungarian"],
    },
    {
        "id": "§15",
        "level": "chapter",
        "stage": "II",
        "title": "§15 统一Mask架构",
        "summary": "统一 query/mask 范式与稠密分割框架。",
        "keywords": ["maskformer", "mask2former", "mask", "pixel decoder", "seggpt"],
    },
    {
        "id": "§16",
        "level": "chapter",
        "stage": "II",
        "title": "§16 提示化与开放词汇",
        "summary": "SAM、开放词汇、VLM 看不清问题。",
        "keywords": ["sam", "prompt", "开放词汇", "grounding dino", "cat-seg", "depth anything"],
    },
    {
        "id": "stage-III",
        "level": "stage",
        "stage": "III",
        "title": "阶段 III · 语言共形",
        "summary": "语言从外挂到骨架，多模态理解与 VLM 成为主轴。",
        "keywords": [
            "clip",
            "vlm",
            "multimodal",
            "caption",
            "language",
            "instruction tuning",
            "多模态",
            "语言",
            "视觉语言",
            "qwen-vl",
            "llava",
        ],
    },
    {
        "id": "§21",
        "level": "chapter",
        "stage": "III",
        "title": "§21 外挂的工程极限",
        "summary": "融合式 VLM 前史，语言仍然是外挂。",
        "keywords": ["vilbert", "lxmert", "uniter", "vinvl", "外挂"],
    },
    {
        "id": "§22",
        "level": "chapter",
        "stage": "III",
        "title": "§22 对齐即预训练CLIP",
        "summary": "对比对齐成为预训练主轴。",
        "keywords": ["clip", "siglip", "align", "contrastive", "对比学习", "图文对齐"],
    },
    {
        "id": "§23",
        "level": "chapter",
        "stage": "III",
        "title": "§23 语言锚定稠密任务",
        "summary": "语言进入检测/分割/稠密任务的锚定层。",
        "keywords": ["glip", "owl-vit", "ape", "grounding", "开放词汇检测", "语言锚定"],
    },
    {
        "id": "§24",
        "level": "chapter",
        "stage": "III",
        "title": "§24 统一多模态骨干",
        "summary": "从两个塔走向一个流，多任务共骨干。",
        "keywords": ["coca", "blip", "florence", "pali", "ofa", "统一多模态"],
    },
    {
        "id": "§25",
        "level": "chapter",
        "stage": "III",
        "title": "§25 VLM的诞生",
        "summary": "冻结 LLM、视觉适配、指令微调与原生多模态并轨。",
        "keywords": ["flamingo", "blip-2", "llava", "instructblip", "qwen-vl", "internvl", "视觉指令微调"],
    },
    {
        "id": "§26",
        "level": "chapter",
        "stage": "III",
        "title": "§26 语言条件可提示视觉",
        "summary": "语言指令到像素动作的闭环。",
        "keywords": ["grounded-sam", "lisa", "seem", "ferret", "pixel grounding", "可提示视觉"],
    },
    {
        "id": "§27",
        "level": "chapter",
        "stage": "III",
        "title": "§27 借语言的代价",
        "summary": "MMVP、CLIP-blindness、遥感 VLM 等账单汇总。",
        "keywords": ["mmvp", "clip-blindness", "rs-vlm", "遥感视觉语言", "look light think heavy"],
    },
    {
        "id": "stage-IV",
        "level": "stage",
        "stage": "IV",
        "title": "阶段 IV · 生成共形",
        "summary": "从判别翻入图像生成，外显生产主体性首次点燃，diffusion 是当前主轴。",
        "keywords": [
            "generation",
            "diffusion",
            "gan",
            "image generation",
            "扩散",
            "生成",
            "文本生成图像",
            "dall-e",
            "sdxl",
            "flux",
            "dit",
        ],
    },
    {
        "id": "§31",
        "level": "chapter",
        "stage": "IV",
        "title": "§31 觉醒前夜：密度与能量模型",
        "summary": "RBM/EBM/PixelRNN 等图像生成前夜。",
        "keywords": ["rbm", "ebm", "pixelcnn", "pixelrnn", "密度模型", "能量模型"],
    },
    {
        "id": "§32",
        "level": "chapter",
        "stage": "IV",
        "title": "§32 GAN与自我对抗",
        "summary": "对抗式图像生成与主体点火。",
        "keywords": ["gan", "stylegan", "wgan", "dcgan", "对抗生成"],
    },
    {
        "id": "§33",
        "level": "chapter",
        "stage": "IV",
        "title": "§33 潜空间与生成主体的内在语",
        "summary": "VAE/VQ-VAE/Glow/MaskGIT 等潜空间与离散词汇工程。",
        "keywords": ["vae", "vq-vae", "glow", "maskgit", "潜空间", "codebook"],
    },
    {
        "id": "§34",
        "level": "chapter",
        "stage": "IV",
        "title": "§34 扩散革命与内部时间",
        "summary": "DDPM 到 Stable Diffusion，迭代成为内部时间。",
        "keywords": ["ddpm", "stable diffusion", "ldm", "ddim", "score", "扩散革命"],
    },
    {
        "id": "§35",
        "level": "chapter",
        "stage": "IV",
        "title": "§35 文本条件与图像生成接口",
        "summary": "DALL·E/Imagen/SDXL 以及 prompt/guidance/adapters。",
        "keywords": ["dall-e", "imagen", "parti", "sdxl", "text-to-image", "prompt", "controlnet", "adapter"],
    },
    {
        "id": "§36",
        "level": "chapter",
        "stage": "IV",
        "title": "§36 图像生成工艺系统化与最前沿",
        "summary": "DiT/MMDiT/SD3/Flux/Rectified Flow/Consistency 等 diffusion 最前沿。",
        "keywords": ["dit", "mmdit", "sd3", "flux", "rectified flow", "consistency", "distillation", "图像生成工艺"],
    },
    {
        "id": "§37",
        "level": "chapter",
        "stage": "IV",
        "title": "§37 生成器反身成表征器",
        "summary": "MAE/BEiT 与 diffusion features 把桥送向阶段 V。",
        "keywords": ["mae", "beit", "dift", "repa", "生成器特征", "表征桥梁"],
    },
    {
        "id": "stage-V",
        "level": "stage",
        "stage": "V",
        "title": "阶段 V · 表征共形",
        "summary": "真正的世界表征与状态预测，自监督与 JEPA 是主要入口。",
        "keywords": [
            "representation",
            "self-supervised",
            "ssl",
            "jepa",
            "dino",
            "predictive",
            "表征",
            "自监督",
            "状态预测",
            "world model",
            "世界表征",
        ],
    },
]


def should_skip(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if any(part in EXCLUDE_PARTS for part in relative.parts):
        return True
    if relative.parts and relative.parts[0] in EXCLUDE_TOP_LEVEL:
        return True
    return False


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="ignore")


def first_heading(lines: list[str], fallback: str) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return fallback


def parse_meta(lines: list[str]) -> dict[str, str]:
    meta: dict[str, str] = {}
    pattern = re.compile(r"^([^:#]{1,40}):\s*(.+)$")
    for line in lines[:40]:
        stripped = line.strip()
        match = pattern.match(stripped)
        if not match:
            continue
        key = match.group(1).strip()
        value = match.group(2).strip()
        if key in SELECTED_META_KEYS:
            meta[key] = value
    return meta


def build_excerpt(lines: list[str]) -> str:
    excerpt_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if re.match(r"^[^:#]{1,40}:\s*.+$", stripped):
            continue
        excerpt_lines.append(stripped)
        if len(" ".join(excerpt_lines)) >= 420:
            break
    return "\n".join(excerpt_lines[:10])[:700]


def detect_stage(top_level: str, meta: dict[str, str]) -> str:
    if top_level.startswith("01-阶段I"):
        return "I"
    if top_level.startswith("02-阶段II"):
        return "II"
    if top_level.startswith("03-阶段III"):
        return "III"
    if top_level.startswith("04-阶段IV"):
        return "IV"
    if top_level.startswith("05-阶段V"):
        return "V"
    stage_meta = meta.get("阶段", "")
    for token in ("I", "II", "III", "IV", "V"):
        if f"{token} ·" in stage_meta or stage_meta.startswith(token):
            return token
    return ""


def detect_chapter(relative_parts: tuple[str, ...]) -> str:
    for part in relative_parts:
        match = re.match(r"^(§\d+)", part)
        if match:
            return match.group(1)
    return ""


def detect_role(path: Path, top_level: str) -> str:
    name = path.name
    relative = path.relative_to(ROOT)
    if name == "INDEX.md":
        return "index"
    if name == "README.md" and top_level == "skills":
        return "skill-meta"
    if name == "SKILL.md" and top_level == "skills":
        return "skill"
    if "归档" in relative.parts:
        return "archive"
    if top_level == "应用域":
        return "application"
    if top_level == "横切":
        return "cross-cut"
    if name.startswith("00-总纲") or name.startswith("00-阶段导读"):
        return "stage-entry"
    if name.startswith("01-总纲扩展"):
        return "stage-extension"
    if name.startswith("00-定位卡"):
        return "locator"
    if re.match(r"^01-.*\.md$", name):
        return "mechanism"
    if re.match(r"^0[2-8]-.*\.md$", name):
        return "expansion"
    if name.startswith("90-"):
        return "meta"
    if name.startswith("结语"):
        return "conclusion"
    if "补章" in relative.parts or name.startswith("补章"):
        return "appendix"
    return "document"


def detect_retrieval_tier(role: str, top_level: str) -> int:
    if role in {"index", "stage-entry", "meta", "skill-meta"}:
        return 0
    if role == "skill":
        return 1
    if top_level == "横切" or role == "locator":
        return 1
    if role in {"mechanism", "stage-extension", "conclusion"}:
        return 2
    if role in {"expansion", "appendix", "document"}:
        return 3
    if role in {"application", "archive"}:
        return 4
    return 3


def sort_key(relative: Path) -> str:
    return relative.as_posix().lower()


def build_search_blob(title: str, meta: dict[str, str], excerpt: str, relative: Path) -> str:
    parts = [title, excerpt, relative.as_posix(), " ".join(f"{k} {v}" for k, v in meta.items())]
    return " ".join(parts).lower()


def build_docs() -> list[dict]:
    docs: list[dict] = []
    for path in sorted(ROOT.rglob("*.md")):
        if should_skip(path):
            continue
        relative = path.relative_to(ROOT)
        top_level = relative.parts[0] if len(relative.parts) > 1 else "ROOT"
        text = read_text(path)
        lines = text.splitlines()
        meta = parse_meta(lines)
        title = first_heading(lines, path.stem)
        excerpt = build_excerpt(lines)
        stage = detect_stage(top_level, meta)
        chapter = detect_chapter(relative.parts)
        role = detect_role(path, top_level)
        retrieval_tier = detect_retrieval_tier(role, top_level)
        docs.append(
            {
                "id": relative.as_posix(),
                "title": title,
                "path": relative.as_posix(),
                "openPath": Path(os.path.relpath(path, VIEWER_DIR)).as_posix(),
                "topLevel": top_level,
                "stage": stage,
                "chapter": chapter,
                "role": role,
                "retrievalTier": retrieval_tier,
                "archived": "归档" in relative.parts,
                "meta": meta,
                "excerpt": excerpt,
                "searchBlob": build_search_blob(title, meta, excerpt, relative),
                "sortKey": sort_key(relative),
            }
        )
    return docs


def build_stats(docs: list[dict]) -> dict[str, int]:
    chapters = {doc["chapter"] for doc in docs if doc["chapter"]}
    stages = {doc["stage"] for doc in docs if doc["stage"]}
    archived = sum(1 for doc in docs if doc["archived"])
    by_role = Counter(doc["role"] for doc in docs)
    by_top_level = Counter(doc["topLevel"] for doc in docs)
    by_tier = Counter(doc["retrievalTier"] for doc in docs)
    return {
        "documents": len(docs),
        "stages": len(stages),
        "chapters": len(chapters),
        "archived": archived,
        "byRole": dict(by_role),
        "byTier": dict(by_tier),
        "byTopLevel": {name: by_top_level.get(name, 0) for name in TOP_LEVEL_ORDER if by_top_level.get(name, 0)},
    }


def build_payload() -> dict:
    docs = build_docs()
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "rootName": ROOT.name,
        "topLevelOrder": TOP_LEVEL_ORDER,
        "stats": build_stats(docs),
        "locatorSchema": LOCATOR_SCHEMA,
        "docs": docs,
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    js = "window.KNOWLEDGE_BASE = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    OUTPUT_FILE.write_text(js, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")
    print(f"Indexed {payload['stats']['documents']} markdown files.")


if __name__ == "__main__":
    main()
