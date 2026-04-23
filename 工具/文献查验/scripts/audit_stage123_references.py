from __future__ import annotations

import csv
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
STAGE_DIRS = [
    ROOT / "01-阶段I-判别共形",
    ROOT / "02-阶段II-稠密共形",
    ROOT / "03-阶段III-语言共形",
]
OUT_DIR = ROOT / "横切" / "文献查验"
CACHE_DIR = ROOT / "工具" / "文献查验" / "cache"
OPENALEX_CACHE = CACHE_DIR / "openalex_title_cache.json"
ARXIV_CACHE = CACHE_DIR / "arxiv_cache.json"
DBLP_CACHE = CACHE_DIR / "dblp_title_cache.json"
DBLP_RUNTIME_CACHE: dict = {}
ARXIV_RUNTIME_CACHE: dict = {}

TITLE_PATTERNS = [
    re.compile(r"\*([^*]{6,240})\*\s*\(([^)\n]{0,240})\)"),
    re.compile(r"《([^》]{2,240})》\s*\(([^)\n]{0,240})\)"),
]
ARXIV_PATTERN = re.compile(r"(?i)(?:arxiv\s*)?([0-9]{4}\.[0-9]{4,5})(?:v\d+)?")
YEAR_PATTERN = re.compile(r"\b(19|20)\d{2}\b")
VENUE_PATTERN = re.compile(
    r"\b(CVPR|ICCV|ECCV|NeurIPS|NIPS|ICML|ICLR|AAAI|TPAMI|IJCV|TGRS|ISPRS|MICCAI|"
    r"ICML|ICML 2025|TMLR|PMLR|ICASSP|IGARSS|OpenReview|Nature|ScienceDirect|"
    r"MDPI Remote Sensing|Remote Sensing)\b",
    re.IGNORECASE,
)
SKIP_TITLES = {
    "不可分割的残余",
    "世界时代",
}
VENUE_ALIASES = {
    "TMLR": "TRANS. MACH. LEARN. RES.",
    "TPAMI": "IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE",
    "TGRS": "IEEE TRANSACTIONS ON GEOSCIENCE AND REMOTE SENSING",
    "IJCV": "INTERNATIONAL JOURNAL OF COMPUTER VISION",
}
MANUAL_VERIFIED = {
    "Adam: A Method for Stochastic Optimization": {
        "title": "Adam: A Method for Stochastic Optimization",
        "authors": "Diederik P. Kingma; Jimmy Ba",
        "year": "2015",
        "venue": "ICLR",
        "publisher": "ICLR",
        "official_url": "https://arxiv.org/abs/1412.6980",
    },
    "Fully Convolutional Networks for Semantic Segmentation": {
        "title": "Fully Convolutional Networks for Semantic Segmentation",
        "authors": "Jonathan Long; Evan Shelhamer; Trevor Darrell",
        "year": "2015",
        "venue": "CVPR",
        "publisher": "IEEE / CVF",
        "official_url": "https://openaccess.thecvf.com/content_cvpr_2015/html/Long_Fully_Convolutional_Networks_2015_CVPR_paper.html",
    },
    "Deep High-Resolution Representation Learning for Visual Recognition": {
        "title": "Deep High-Resolution Representation Learning for Visual Recognition",
        "authors": "Jingdong Wang; Ke Sun; Tianheng Cheng; Borui Jiang; Chaorui Deng; Yang Zhao; Dong Liu; Yadong Mu; Mingkui Tan; Xinggang Wang; Wenyu Liu; Bin Xiao",
        "year": "2020",
        "venue": "TPAMI",
        "publisher": "IEEE",
        "official_url": "https://arxiv.org/abs/1908.07919",
    },
    "Semantic Image Segmentation with Deep CNNs, Atrous Convolution, and Fully Connected CRFs": {
        "title": "Semantic Image Segmentation with Deep CNNs, Atrous Convolution, and Fully Connected CRFs",
        "authors": "Liang-Chieh Chen; George Papandreou; Iasonas Kokkinos; Kevin Murphy; Alan L. Yuille",
        "year": "2017",
        "venue": "TPAMI",
        "publisher": "IEEE",
        "official_url": "https://doi.org/10.1109/TPAMI.2016.2572683",
    },
    "Delving Deep into Rectifiers": {
        "title": "Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification",
        "authors": "Kaiming He; Xiangyu Zhang; Shaoqing Ren; Jian Sun",
        "year": "2015",
        "venue": "ICCV",
        "publisher": "IEEE / CVF",
        "official_url": "https://openaccess.thecvf.com/content_iccv_2015/html/He_Delving_Deep_into_ICCV_2015_paper.html",
    },
    "Inception-v4, Inception-ResNet...": {
        "title": "Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning",
        "authors": "Christian Szegedy; Sergey Ioffe; Vincent Vanhoucke; Alex Alemi",
        "year": "2017",
        "venue": "AAAI",
        "publisher": "AAAI Press",
        "official_url": "https://ojs.aaai.org/index.php/AAAI/article/view/11231",
    },
    "Fuyu-8B: A Multimodal Architecture for AI Agents": {
        "title": "Fuyu-8B: A Multimodal Architecture for AI Agents",
        "authors": "Rohan Bavishi; Erich Elsen; Curtis Hawthorne; Maxwell Nye; Augustus Odena; Arushi Somani; Sagnak Tasirlar",
        "year": "2023",
        "venue": "Adept Blog / Technical Report",
        "publisher": "Adept AI Labs",
        "official_url": "https://www.adept.ai/blog/fuyu-8b",
    },
    "Change-Agent: Toward Interactive Comprehensive Remote Sensing Change Interpretation and Analysis": {
        "title": "Change-Agent: Toward Interactive Comprehensive Remote Sensing Change Interpretation and Analysis",
        "authors": "Chenyang Liu; Keyan Chen; Haotian Zhang; Zipeng Qi; Zhengxia Zou; Zhenwei Shi",
        "year": "2024",
        "venue": "IEEE Transactions on Geoscience and Remote Sensing",
        "publisher": "Institute of Electrical and Electronics Engineers (IEEE)",
        "official_url": "https://doi.org/10.1109/TGRS.2024.3425815",
    },
    "MV-CC: Mask Enhanced Video Model for Remote Sensing Change Caption": {
        "title": "MV-CC: Mask Enhanced Video Model for Remote Sensing Change Caption",
        "authors": "Ruixun Liu; Kaiyu Li; Jiayi Song; Dongwei Sun; Xiangyong Cao",
        "year": "2024",
        "venue": "CoRR / arXiv",
        "publisher": "Cornell University",
        "official_url": "https://arxiv.org/abs/2410.23946",
    },
    "Change-LISA: Language-Guided Reasoning for Remote Sensing Change Detection": {
        "title": "Change-LISA: Language-Guided Reasoning for Remote Sensing Change Detection",
        "authors": "Xiangyu Jia; Zhibo Chen; Shengyi Zhang; Xiaojing Xue",
        "year": "2026",
        "venue": "IEEE Transactions on Geoscience and Remote Sensing",
        "publisher": "Institute of Electrical and Electronics Engineers (IEEE)",
        "official_url": "https://doi.org/10.1109/TGRS.2026.3684817",
    },
    "EarthMind: Leveraging Cross-Sensor Data for Advanced Earth Observation Interpretation with a Unified Multimodal LLM": {
        "title": "EarthMind: Leveraging Cross-Sensor Data for Advanced Earth Observation Interpretation with a Unified Multimodal LLM",
        "authors": "Yan Shu; Bin Ren; Zhitong Xiong; Danda Pani Paudel; Luc Van Gool; Begum Demir; Nicu Sebe; Paolo Rota",
        "year": "2025",
        "venue": "OpenReview (ICLR 2026 submission)",
        "publisher": "OpenReview.net",
        "official_url": "https://openreview.net/forum?id=ooYtHcj6LI",
    },
    "DisasterM3: A Remote Sensing Vision-Language Dataset for Disaster Damage Assessment and Response": {
        "title": "DisasterM3: A Remote Sensing Vision-Language Dataset for Disaster Damage Assessment and Response",
        "authors": "Junjue Wang; Weihao Xuan; Heli Qi; Zhihao Liu; Kunyi Liu; Yuhan Wu; Hongruixuan Chen; Jian Song; Junshi Xia; Zhuo Zheng; Naoto Yokoya",
        "year": "2025",
        "venue": "NeurIPS 2025 Datasets and Benchmarks Track",
        "publisher": "NeurIPS Foundation / OpenReview",
        "official_url": "https://openreview.net/forum?id=sQO1ZEQGqX",
    },
    "EarthDial: Turning Multi-sensory Earth Observations to Interactive Dialogues": {
        "title": "EarthDial: Turning Multi-sensory Earth Observations to Interactive Dialogues",
        "authors": "Sagar Soni; Akshay Dudhane; Hiyam Debary; Mustansar Fiaz; Muhammad Akhtar Munir; Muhammad Sohail Danish; Paolo Fraccaro; Campbell D Watson; Levente J Klein; Fahad Shahbaz Khan; Salman Khan",
        "year": "2025",
        "venue": "CVPR",
        "publisher": "IEEE / CVF",
        "official_url": "https://openaccess.thecvf.com/content/CVPR2025/html/Soni_EarthDial_Turning_Multi-sensory_Earth_Observations_to_Interactive_Dialogues_CVPR_2025_paper.html",
    },
}


@dataclass
class Citation:
    title: str
    tail: str
    file: Path
    line: int
    kind: str


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_title(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[\W_]+", "", text, flags=re.UNICODE)
    return text


def title_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_title(a), normalize_title(b)).ratio()


def parse_claimed_year(tail: str) -> str:
    years = parse_claimed_years(tail)
    return years[0] if years else ""


def parse_claimed_years(tail: str) -> list[str]:
    return [m.group(0) for m in YEAR_PATTERN.finditer(tail)]


def parse_claimed_venue(tail: str) -> str:
    matches = [m.group(0) for m in VENUE_PATTERN.finditer(tail)]
    dedup: list[str] = []
    for item in matches:
        item_up = item.upper()
        if item_up not in dedup:
            dedup.append(item_up)
    return " / ".join(dedup)


def venue_matches(claimed_venue: str, verified_venue: str) -> bool:
    if not claimed_venue or not verified_venue:
        return True
    verified_up = verified_venue.upper()
    tokens = [token.strip().upper() for token in claimed_venue.split(" / ") if token.strip()]
    expanded = set(tokens)
    for token in tokens:
        expanded.add(VENUE_ALIASES.get(token, token))
    return any(token in verified_up for token in expanded)


def extract_citations() -> list[Citation]:
    entries: list[Citation] = []
    seen: set[tuple[str, str, str, int]] = set()
    for stage_dir in STAGE_DIRS:
        for path in stage_dir.rglob("*.md"):
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for lineno, line in enumerate(lines, 1):
                for pattern in TITLE_PATTERNS:
                    for match in pattern.finditer(line):
                        title = " ".join(match.group(1).split())
                        tail = " ".join(match.group(2).split())
                        if title in SKIP_TITLES:
                            continue
                        key = (title, tail, str(path), lineno)
                        if key in seen:
                            continue
                        seen.add(key)
                        entries.append(Citation(title=title, tail=tail, file=path, line=lineno, kind="structured"))
    return entries


def extract_arxiv_refs() -> dict[str, list[dict[str, str | int]]]:
    refs: dict[str, list[dict[str, str | int]]] = {}
    for stage_dir in STAGE_DIRS:
        for path in stage_dir.rglob("*.md"):
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for lineno, line in enumerate(lines, 1):
                for match in ARXIV_PATTERN.finditer(line):
                    aid = match.group(1)
                    month = int(aid[2:4])
                    if not 1 <= month <= 12:
                        continue
                    refs.setdefault(aid, []).append(
                        {"file": str(path), "line": lineno, "text": line.strip()}
                    )
    return refs


def fetch_json(url: str, retries: int = 2) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "stage123-reference-audit/1.0"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8", errors="ignore"))
        except urllib.error.HTTPError:
            if attempt >= retries:
                raise
            time.sleep(0.5 * (attempt + 1))
    return {}


def fetch_openalex_match(title: str, cache: dict) -> dict:
    if title in cache:
        return cache[title]

    query = urllib.parse.quote(f'"{title}"')
    url = f"https://api.openalex.org/works?search={query}&per-page=5"
    data = fetch_json(url)
    candidates = data.get("results", [])

    best: dict | None = None
    best_score = -1.0
    for item in candidates:
        cand_title = item.get("display_name") or item.get("title") or ""
        score = title_similarity(title, cand_title)
        if score > best_score:
            best = item
            best_score = score

    payload = {
        "matched": bool(best and best_score >= 0.82),
        "score": round(best_score, 4),
        "result": best or {},
    }
    cache[title] = payload
    time.sleep(0.1)
    return payload


def dblp_hits(title: str) -> list[dict]:
    query = urllib.parse.quote(title)
    url = f"https://dblp.org/search/publ/api?q={query}&h=10&format=json"
    try:
        data = fetch_json(url)
    except urllib.error.HTTPError:
        return []
    hits = data.get("result", {}).get("hits", {}).get("hit", [])
    if isinstance(hits, dict):
        return [hits]
    return hits


def infer_publisher_from_venue(venue: str) -> str:
    venue_up = venue.upper()
    if "CVPR" in venue_up or "ICCV" in venue_up:
        return "IEEE / CVF"
    if "ECCV" in venue_up or "LNCS" in venue_up or "MICCAI" in venue_up:
        return "Springer"
    if venue_up in {"ICML", "COLT"} or "PMLR" in venue_up:
        return "PMLR"
    if "ICLR" in venue_up or "TMLR" in venue_up or "OPENREVIEW" in venue_up:
        return "OpenReview"
    if "NEURIPS" in venue_up or venue_up == "NIPS":
        return "NeurIPS Foundation"
    if "TPAMI" in venue_up or "TGRS" in venue_up or "ICASSP" in venue_up or "IGARSS" in venue_up:
        return "IEEE"
    if "IJCV" in venue_up:
        return "Springer"
    if "REMOTE SENSING" in venue_up:
        return "MDPI"
    if "COMMUN. ACM" in venue_up:
        return "ACM"
    return ""


def fetch_dblp_match(title: str, claimed_year: str, claimed_venue: str, cache: dict) -> dict:
    cache_key = f"{title}|||{claimed_year}|||{claimed_venue}"
    if cache_key in cache:
        return cache[cache_key]

    candidates = dblp_hits(title)
    best_hit: dict | None = None
    best_score = -1.0
    claimed_venue_tokens = [token.strip().upper() for token in claimed_venue.split(" / ") if token.strip()]

    for hit in candidates:
        info = hit.get("info", {})
        cand_title = info.get("title", "").rstrip(".")
        score = title_similarity(title, cand_title)
        if claimed_year and info.get("year") == claimed_year:
            score += 0.15
        venue = str(info.get("venue", "")).upper()
        if claimed_venue_tokens and any(token in venue for token in claimed_venue_tokens):
            score += 0.15
        if score > best_score:
            best_score = score
            best_hit = info

    payload = {
        "matched": bool(best_hit and best_score >= 0.78),
        "score": round(best_score, 4),
        "result": best_hit or {},
    }
    cache[cache_key] = payload
    time.sleep(0.1)
    return payload


def fetch_arxiv_metadata(arxiv_ids: list[str], cache: dict) -> dict:
    pending = [aid for aid in arxiv_ids if aid not in cache]
    if pending:
        entry_ns = "{http://www.w3.org/2005/Atom}"
        for start in range(0, len(pending), 20):
            batch = pending[start : start + 20]
            url = (
                "https://export.arxiv.org/api/query?id_list="
                + ",".join(batch)
                + f"&max_results={len(batch)}"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "stage123-reference-audit/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                xml = resp.read()
            root = ET.fromstring(xml)
            found: set[str] = set()
            for entry in root.findall(f"{entry_ns}entry"):
                id_url = entry.findtext(f"{entry_ns}id", default="") or ""
                match = re.search(r"/abs/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?$", id_url)
                if not match:
                    continue
                aid = match.group(1)
                found.add(aid)
                title = " ".join((entry.findtext(f"{entry_ns}title", default="") or "").split())
                published = entry.findtext(f"{entry_ns}published", default="")
                authors = [
                    " ".join((author.findtext(f'{entry_ns}name', default='') or "").split())
                    for author in entry.findall(f"{entry_ns}author")
                ]
                cache[aid] = {
                    "found": True,
                    "title": title,
                    "published": published,
                    "authors": authors,
                    "official_url": f"https://arxiv.org/abs/{aid}",
                    "venue": "arXiv",
                    "publisher": "Cornell University",
                }
            for aid in batch:
                if aid not in found:
                    cache[aid] = {"found": False}
            time.sleep(0.2)
    return cache


def authors_to_short_list(authorships: list[dict], limit: int = 6) -> str:
    names: list[str] = []
    for item in authorships[:limit]:
        author = item.get("author", {})
        name = author.get("display_name", "")
        if name:
            names.append(name)
    return "; ".join(names)


def summarize_openalex(result: dict) -> dict:
    location = result.get("primary_location") or {}
    source_meta = location.get("source") or {}
    source = source_meta.get("display_name", "")
    host_org = source_meta.get("host_organization_name", "")
    official_url = (
        location.get("landing_page_url")
        or location.get("pdf_url")
        or result.get("doi")
        or result.get("id", "")
    )
    year = str(result.get("publication_year", ""))
    return {
        "title": result.get("display_name") or result.get("title") or "",
        "authors": authors_to_short_list(result.get("authorships", [])),
        "year": year,
        "venue": source,
        "publisher": host_org,
        "official_url": official_url,
        "type": result.get("type", ""),
    }


def citation_row(citation: Citation, openalex_cache: dict) -> dict:
    title = citation.title
    tail = citation.tail
    claimed_year = parse_claimed_year(tail)
    claimed_years = parse_claimed_years(tail)
    claimed_venue = parse_claimed_venue(tail)
    claimed_org = tail

    row = {
        "status": "待人工复核",
        "kind": citation.kind,
        "title_or_id": title,
        "claimed_year": claimed_year,
        "claimed_venue": claimed_venue,
        "claimed_org_or_tail": claimed_org,
        "verified_year": "",
        "verified_authors": "",
        "verified_venue": "",
        "verified_publisher": "",
        "official_url": "",
        "file": str(citation.file),
        "line": citation.line,
        "note": "",
    }

    title_lower = title.lower()
    if title_lower.startswith("arxiv "):
        match = ARXIV_PATTERN.search(title)
        if match:
            aid = match.group(1)
            meta = ARXIV_RUNTIME_CACHE.get(aid, {})
            row["title_or_id"] = aid
            row["note"] = "题名缺失，仅给出 arXiv 号。"
            if meta.get("found"):
                row["status"] = "仅 arXiv / 仓储核验"
                row["verified_year"] = (meta.get("published", "") or "")[:4]
                row["verified_authors"] = "; ".join(meta.get("authors", [])[:6])
                row["verified_venue"] = meta.get("venue", "")
                row["verified_publisher"] = meta.get("publisher", "")
                row["official_url"] = meta.get("official_url", "")
        else:
            row["note"] = "题名缺失，仅给出 arXiv 号。"
        return row

    manual = MANUAL_VERIFIED.get(title)
    if manual:
        row["verified_year"] = manual["year"]
        row["verified_authors"] = manual["authors"]
        row["verified_venue"] = manual["venue"]
        row["verified_publisher"] = manual["publisher"]
        row["official_url"] = manual["official_url"]
        problems: list[str] = []
        if claimed_years and manual["year"] not in claimed_years:
            problems.append(f"年份声称 {' / '.join(claimed_years)}，核验为 {manual['year']}")
        if not venue_matches(claimed_venue, manual["venue"]):
            problems.append(f"venue 声称 {claimed_venue}，核验为 {manual['venue']}")
        if problems:
            row["status"] = "字段不一致"
            row["note"] = "；".join(problems)
        else:
            row["status"] = "已核验"
        return row

    dblp_match = fetch_dblp_match(title, claimed_year, claimed_venue, DBLP_RUNTIME_CACHE)
    if dblp_match.get("matched"):
        info = dblp_match["result"]
        venue = str(info.get("venue", ""))
        authors = info.get("authors", {}).get("author", [])
        if isinstance(authors, dict):
            authors = [authors]
        author_names = []
        for author in authors[:6]:
            if isinstance(author, dict):
                author_names.append(author.get("text", ""))
            elif isinstance(author, str):
                author_names.append(author)
        verified = {
            "title": str(info.get("title", "")).rstrip("."),
            "authors": "; ".join([name for name in author_names if name]),
            "year": str(info.get("year", "")),
            "venue": venue,
            "publisher": infer_publisher_from_venue(venue),
            "official_url": info.get("ee", "") or info.get("url", ""),
        }
        row["verified_year"] = verified["year"]
        row["verified_authors"] = verified["authors"]
        row["verified_venue"] = verified["venue"]
        row["verified_publisher"] = verified["publisher"]
        row["official_url"] = verified["official_url"]

        problems: list[str] = []
        if claimed_years and verified["year"] and verified["year"] not in claimed_years:
            problems.append(f"年份声称 {' / '.join(claimed_years)}，核验为 {verified['year']}")
        if not venue_matches(claimed_venue, verified["venue"]):
            problems.append(f"venue 声称 {claimed_venue}，核验为 {verified['venue']}")

        if problems:
            row["status"] = "字段不一致"
            row["note"] = "；".join(problems)
        else:
            row["status"] = "已核验"
        return row

    match = fetch_openalex_match(title, openalex_cache)
    if not match.get("matched"):
        row["note"] = f"题名匹配不足；DBLP/OpenAlex 最高相似度 {match.get('score', 0)}。"
        return row

    verified = summarize_openalex(match["result"])
    row["verified_year"] = verified["year"]
    row["verified_authors"] = verified["authors"]
    row["verified_venue"] = verified["venue"]
    row["verified_publisher"] = verified["publisher"]
    row["official_url"] = verified["official_url"]
    row["status"] = "仅 arXiv / 仓储核验" if "arxiv" in verified["venue"].lower() else "已核验"
    if claimed_years and verified["year"] and verified["year"] not in claimed_years:
        row["status"] = "字段不一致"
        row["note"] = f"年份声称 {' / '.join(claimed_years)}，核验为 {verified['year']}"
    return row


def arxiv_rows(arxiv_refs: dict[str, list[dict]], arxiv_cache: dict) -> list[dict]:
    rows: list[dict] = []
    for aid, refs in sorted(arxiv_refs.items()):
        meta = arxiv_cache.get(aid, {})
        sample = refs[0]
        row = {
            "arxiv_id": aid,
            "status": "存在" if meta.get("found") else "未找到",
            "verified_title": meta.get("title", ""),
            "verified_year": (meta.get("published", "") or "")[:4],
            "verified_authors": "; ".join(meta.get("authors", [])[:6]),
            "venue": meta.get("venue", ""),
            "publisher": meta.get("publisher", ""),
            "official_url": meta.get("official_url", ""),
            "occurrences": len(refs),
            "sample_file": sample["file"],
            "sample_line": sample["line"],
        }
        rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_summary(citation_rows: list[dict], arxiv_rows_data: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    verified = sum(1 for row in citation_rows if row["status"] == "已核验")
    repo_only = sum(1 for row in citation_rows if row["status"] == "仅 arXiv / 仓储核验")
    mismatches = [row for row in citation_rows if row["status"] == "字段不一致"]
    unresolved = [row for row in citation_rows if row["status"] == "待人工复核"]
    arxiv_missing = [row for row in arxiv_rows_data if row["status"] != "存在"]

    lines = [
        "# 前三阶段文献查验摘要",
        "",
        "对 `01-阶段I-判别共形`、`02-阶段II-稠密共形`、`03-阶段III-语言共形` 里的显式论文题名与 arXiv 号做了批量核验。",
        "",
        "## 统计",
        "",
        f"- 结构化题名引用：`{len(citation_rows)}` 条",
        f"- 其中自动核验通过：`{verified}` 条",
        f"- 仅 arXiv / 仓储核验：`{repo_only}` 条",
        f"- 字段不一致：`{len(mismatches)}` 条",
        f"- 待人工复核：`{len(unresolved)}` 条",
        f"- 显式 arXiv 号：`{len(arxiv_rows_data)}` 条",
        f"- arXiv 官方 API 未找到：`{len(arxiv_missing)}` 条",
        "",
        "## 重点异常",
        "",
    ]

    if mismatches:
        for row in mismatches[:30]:
            lines.append(
                f"- `{row['title_or_id']}` — {row['note']} "
                f"([定位]({row['file']}:{row['line']}))"
            )
    else:
        lines.append("- 当前自动核验没有发现明确的年份 / venue 不一致。")

    lines.extend([
        "",
        "## 待人工复核",
        "",
    ])
    if unresolved:
        for row in unresolved[:30]:
            lines.append(
                f"- `{row['title_or_id']}` — {row['note']} "
                f"([定位]({row['file']}:{row['line']}))"
            )
    else:
        lines.append("- 当前没有待人工复核条目。")

    lines.extend([
        "",
        "## 输出文件",
        "",
        "- `横切/文献查验/前三阶段文献查验总表.csv`",
        "- `横切/文献查验/前三阶段arXiv核验.md`",
        "",
    ])

    (OUT_DIR / "前三阶段文献查验摘要.md").write_text("\n".join(lines), encoding="utf-8")


def write_arxiv_markdown(rows: list[dict]) -> None:
    lines = [
        "# 前三阶段 arXiv 核验",
        "",
        "| arXiv | 状态 | 年份 | 标题 | 官方页 | 出现次数 |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        title = row["verified_title"].replace("|", " ")
        url = row["official_url"]
        link = f"[官方页]({url})" if url else ""
        lines.append(
            f"| `{row['arxiv_id']}` | {row['status']} | {row['verified_year']} | "
            f"{title} | {link} | {row['occurrences']} |"
        )
    (OUT_DIR / "前三阶段arXiv核验.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    citations = extract_citations()
    arxiv_refs = extract_arxiv_refs()

    openalex_cache = load_json(OPENALEX_CACHE)
    dblp_cache = load_json(DBLP_CACHE)
    arxiv_cache = fetch_arxiv_metadata(sorted(arxiv_refs), load_json(ARXIV_CACHE))

    global DBLP_RUNTIME_CACHE
    global ARXIV_RUNTIME_CACHE
    DBLP_RUNTIME_CACHE = dblp_cache
    ARXIV_RUNTIME_CACHE = arxiv_cache

    citation_rows = [citation_row(citation, openalex_cache) for citation in citations]
    arxiv_rows_data = arxiv_rows(arxiv_refs, arxiv_cache)

    save_json(OPENALEX_CACHE, openalex_cache)
    save_json(DBLP_CACHE, dblp_cache)
    save_json(ARXIV_CACHE, arxiv_cache)

    write_csv(
        OUT_DIR / "前三阶段文献查验总表.csv",
        citation_rows,
        [
            "status",
            "kind",
            "title_or_id",
            "claimed_year",
            "claimed_venue",
            "claimed_org_or_tail",
            "verified_year",
            "verified_authors",
            "verified_venue",
            "verified_publisher",
            "official_url",
            "file",
            "line",
            "note",
        ],
    )
    write_arxiv_markdown(arxiv_rows_data)
    write_markdown_summary(citation_rows, arxiv_rows_data)

    print(f"structured citations: {len(citation_rows)}")
    print(f"arxiv refs: {len(arxiv_rows_data)}")
    print(f"summary: {OUT_DIR / '前三阶段文献查验摘要.md'}")


if __name__ == "__main__":
    main()
