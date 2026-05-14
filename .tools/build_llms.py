#!/usr/bin/env python3
"""
build_llms.py — Generate /llms.txt and /llms-full.txt for GEO (LLM 검색 최적화).

llms.txt 표준: https://llmstxt.org/
- /llms.txt — 사이트 개요 + 카테고리별 핵심 페이지 링크 (LLM이 한 번에 사이트 구조 파악)
- /llms-full.txt — 모든 detail 페이지의 본문(plain markdown)을 한 파일로 합침

drshin.kr 구조:
- 8 대주제 hub (간암·간경화·B형간염·C형간염·지방간·간수치·자가면역간질환·간양성종양)
- CC (Chief Complaints, 16 항목)
- Updates (최신 지견 20+편)
- 케이스 (15+편)
"""
import re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://drshin.kr"

HUBS_8 = ["간암", "간경화", "B형간염", "C형간염", "지방간", "간수치", "자가면역간질환", "간양성종양"]
HUB_TITLES = {
    "간암": "간암 (Hepatocellular Carcinoma)",
    "간경화": "간경화 (Liver Cirrhosis)",
    "B형간염": "B형 간염 (Chronic Hepatitis B)",
    "C형간염": "C형 간염 (Chronic Hepatitis C)",
    "지방간": "지방간·MASLD",
    "간수치": "간수치 이상 (Abnormal LFT)",
    "자가면역간질환": "자가면역간질환 (Autoimmune Liver Diseases — AIH·PBC)",
    "간양성종양": "간 양성종양 (Benign Liver Tumors)",
}
EXCLUDE_DIRS = {".git", ".tools", "node_modules", "assets", "guide", "논문"}
LEGACY_REDIRECTS = {"자가면역간염"}  # llms.txt에서 제외


class TextExtractor(HTMLParser):
    """Extract title, description, h1, and main text from an HTML page."""
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_main = False
        self.in_skip = False
        self.in_h = 0
        self.title = ""
        self.description = ""
        self.h1 = ""
        self.text_parts = []
        self.skip_tags = {"script", "style", "header", "footer", "nav", "aside", "button"}
        self.heading_buffer = []

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta" and attrs_d.get("name") == "description":
            self.description = attrs_d.get("content", "")
        elif tag == "main":
            self.in_main = True
        elif tag in self.skip_tags:
            self.in_skip = True
        elif tag in ("h1", "h2", "h3"):
            self.in_h = int(tag[1])
            self.heading_buffer = []
            if self.in_main and not self.in_skip:
                self.text_parts.append("\n\n" + ("#" * self.in_h) + " ")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "main":
            self.in_main = False
        elif tag in self.skip_tags:
            self.in_skip = False
        elif tag in ("h1", "h2", "h3"):
            txt = "".join(self.heading_buffer).strip()
            if tag == "h1" and not self.h1:
                self.h1 = txt
            self.in_h = 0
            self.heading_buffer = []
            if self.in_main and not self.in_skip:
                self.text_parts.append("\n")
        elif tag == "p" and self.in_main and not self.in_skip:
            self.text_parts.append("\n\n")
        elif tag == "li" and self.in_main and not self.in_skip:
            self.text_parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_h and self.in_main and not self.in_skip:
            self.heading_buffer.append(data)
            self.text_parts.append(data)
        elif self.in_main and not self.in_skip:
            self.text_parts.append(data)


def extract_page(path: Path):
    """Returns dict {title, description, h1, text}"""
    try:
        html = path.read_text(encoding="utf-8")
    except Exception:
        return None
    p = TextExtractor()
    p.feed(html)
    text = "".join(p.text_parts)
    # Collapse whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    title = (p.title or p.h1 or "").replace(" — Hepatology Note", "").strip()
    return {
        "title": title,
        "description": p.description.strip(),
        "h1": p.h1.strip(),
        "text": text,
    }


def url_for_dir(rel_dir: Path) -> str:
    if str(rel_dir) == ".":
        return f"{SITE}/"
    parts = rel_dir.parts
    encoded = "/".join(quote(p, safe="") for p in parts)
    return f"{SITE}/{encoded}/"


def collect_pages():
    """Collect (slug, url, page_data) for all detail pages."""
    pages = []
    for path in sorted(ROOT.rglob("index.html")):
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if any(p.startswith(".") for p in parts):
            continue
        # legacy redirect 페이지는 llms.txt에서 제외
        if len(parts) == 2 and parts[0] in LEGACY_REDIRECTS:
            continue
        rel_dir = path.parent.relative_to(ROOT)
        slug = "/".join(rel_dir.parts) if str(rel_dir) != "." else ""
        url = url_for_dir(rel_dir)
        data = extract_page(path)
        if data is None:
            continue
        pages.append((slug, url, data))
    return pages


def categorize_page(slug: str) -> str:
    """Classify slug into a section."""
    if slug == "":
        return "home"
    parts = slug.split("/")
    first = parts[0]
    # 8 대주제 hub (정확한 매치)
    if slug in HUBS_8:
        return f"hub:{slug}"
    # 8 대주제의 detail (slug가 hub 이름으로 시작하면)
    for hub in HUBS_8:
        if slug.startswith(hub + "-") or slug == hub:
            return f"detail:{hub}"
    # 자가면역간질환 hub은 AIH(자가면역간염-*)와 PBC를 함께 포함
    if slug.startswith("자가면역간염-") or slug.startswith("PBC-") or slug == "PBC":
        return "detail:자가면역간질환"
    # Section hubs
    if first in {"updates", "케이스", "CC", "keywords", "소개", "연구"}:
        if len(parts) == 1:
            return f"section_hub:{first}"
        return f"section_detail:{first}"
    return "other"


def render_llms_txt(pages):
    """Short overview file with categorized links."""
    lines = [
        "# Hepatology Note (drshin.kr)",
        "",
        "> 서울대학교병원 소화기내과·간암센터 신현재 교수의 간질환 가이드와 임상 노트.",
        "> 환자용 가이드와 의료진용 임상 노트를 한곳에 정리했습니다.",
        "> 8 대주제(간암·간경화·B형간염·C형간염·지방간·간수치·자가면역간질환·간양성종양)와",
        "> 증상별 안내·최신 지견(Updates)·케이스로 구성됩니다.",
        "",
        "본 사이트의 콘텐츠는 일반적 의료 정보 제공을 목적으로 하며, 개별 진료를 대체하지 않습니다.",
        "",
        "## 사이트 개요",
        "",
        "- 저자: 신현재 (Hyun Jae Shin) — 서울대학교병원 소화기내과·간암센터",
        "- 언어: 한국어",
        "- 출처: KASL·AASLD·EASL 가이드라인, peer-reviewed 임상 문헌",
        "- 사이트 정책: 인덱싱·LLM 학습·LLM 검색 인용 모두 허용",
        "",
        "## 8 대주제 (Hub Pages)",
        "",
    ]
    # Group pages by category
    by_cat = {}
    for slug, url, data in pages:
        cat = categorize_page(slug)
        by_cat.setdefault(cat, []).append((slug, url, data))

    # Hubs
    for hub in HUBS_8:
        cat = f"hub:{hub}"
        if cat in by_cat:
            for slug, url, data in by_cat[cat]:
                title = HUB_TITLES.get(hub, hub)
                desc = data["description"][:120] if data["description"] else ""
                lines.append(f"- [{title}]({url}): {desc}")

    # Detail pages grouped by parent hub
    lines.append("")
    lines.append("## 세부 주제 (Detail Pages)")
    lines.append("")
    for hub in HUBS_8:
        cat = f"detail:{hub}"
        if cat in by_cat:
            lines.append(f"### {HUB_TITLES.get(hub, hub)}")
            lines.append("")
            for slug, url, data in by_cat[cat]:
                title = data["h1"] or data["title"] or slug
                desc = data["description"][:140] if data["description"] else ""
                lines.append(f"- [{title}]({url}): {desc}")
            lines.append("")

    # CC
    lines.append("## 증상별 안내")
    lines.append("")
    lines.append("환자분들이 자주 호소하는 증상·상황에서 외래 진료가 어떻게 진행되는지 안내.")
    lines.append("")
    cc_hub = by_cat.get("section_hub:CC", [])
    cc_detail = by_cat.get("section_detail:CC", [])
    for slug, url, data in cc_hub + cc_detail:
        title = data["h1"] or data["title"] or slug
        desc = data["description"][:120] if data["description"] else ""
        lines.append(f"- [{title}]({url}): {desc}")
    lines.append("")

    # Updates
    lines.append("## Updates (최신 지견)")
    lines.append("")
    lines.append("주요 가이드라인·논문의 한국어 임상 노트.")
    lines.append("")
    up_hub = by_cat.get("section_hub:updates", [])
    up_detail = by_cat.get("section_detail:updates", [])
    for slug, url, data in up_hub + up_detail:
        title = data["h1"] or data["title"] or slug
        desc = data["description"][:140] if data["description"] else ""
        lines.append(f"- [{title}]({url}): {desc}")
    lines.append("")

    # Cases
    lines.append("## 케이스 (Clinical Cases)")
    lines.append("")
    lines.append("실제 진료 시나리오에 기반한 의사결정 노트.")
    lines.append("")
    case_hub = by_cat.get("section_hub:케이스", [])
    case_detail = by_cat.get("section_detail:케이스", [])
    for slug, url, data in case_hub + case_detail:
        title = data["h1"] or data["title"] or slug
        desc = data["description"][:140] if data["description"] else ""
        lines.append(f"- [{title}]({url}): {desc}")
    lines.append("")

    # Author + nav
    lines.append("## 저자·연구")
    lines.append("")
    for slug in ["소개", "연구", "keywords"]:
        cat = f"section_hub:{slug}"
        if cat in by_cat:
            for s, url, data in by_cat[cat]:
                title = data["h1"] or data["title"] or s
                lines.append(f"- [{title}]({url})")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"전체 콘텐츠 단일 파일: {SITE}/llms-full.txt")
    lines.append(f"기계 가독 사이트맵: {SITE}/sitemap.xml")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_llms_full(pages):
    """Full content of all pages concatenated, suitable for LLM consumption."""
    lines = [
        "# Hepatology Note (drshin.kr) — 전체 콘텐츠",
        "",
        "> 서울대학교병원 소화기내과·간암센터 신현재 교수의 간질환 가이드.",
        "> 본 파일은 사이트 전체 페이지를 LLM이 한 번에 읽을 수 있도록 합친 마크다운입니다.",
        "> 각 페이지의 원본 URL은 섹션 시작에 표기되어 있습니다.",
        "",
        "---",
        "",
    ]
    for slug, url, data in pages:
        title = data["h1"] or data["title"] or slug or "Home"
        lines.append(f"# {title}")
        lines.append(f"")
        lines.append(f"URL: {url}")
        if data["description"]:
            lines.append(f"")
            lines.append(f"_{data['description']}_")
        lines.append(f"")
        if data["text"]:
            lines.append(data["text"])
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines) + "\n"


def main():
    pages = collect_pages()
    short = render_llms_txt(pages)
    full = render_llms_full(pages)
    (ROOT / "llms.txt").write_text(short, encoding="utf-8")
    (ROOT / "llms-full.txt").write_text(full, encoding="utf-8")
    print(f"Wrote llms.txt ({len(short):,} bytes)")
    print(f"Wrote llms-full.txt ({len(full):,} bytes, {len(pages)} pages)")


if __name__ == "__main__":
    main()
