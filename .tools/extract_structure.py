"""Extract structure (title, sections, FAQ, tldr) from each article into JSON."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 3 series mapping (based on home page)
SERIES = {
    "시리즈 1 · 간 검진 결과 해석": [
        "간수치-높음", "간수치-종류-차이", "지방간-정밀검사",
        "알파태아단백", "간섬유화스캔-수치",
    ],
    "시리즈 2 · 지방간": [
        "대사이상지방간-MASLD", "술-안마셔도-지방간", "지방간-치료",
        "지방간-음식", "지방간-간암", "지방간-회복-6개월",
    ],
    "시리즈 3 · B형·C형 간염": [
        "B형간염-평생약", "B형간염-검사결과", "B형간염-결혼-임신",
        "가족-B형간염-검사", "C형간염-완치-DAA", "B형간염-간암검진",
    ],
}

def extract(slug: str) -> dict:
    p = ROOT / slug / "index.html"
    if not p.exists():
        return {"slug": slug, "missing": True}
    html = p.read_text(encoding="utf-8")

    # Title (h1)
    h1 = re.search(r"<h1>(.*?)</h1>", html, re.S)
    h1_text = h1.group(1).strip() if h1 else ""

    # meta description
    desc = re.search(r'<meta name="description" content="(.*?)"', html)
    desc_text = desc.group(1).strip() if desc else ""

    # tldr
    tldr_block = re.search(r'<div class="tldr">.*?<strong>.*?</strong>(.*?)</div>', html, re.S)
    tldr_text = ""
    if tldr_block:
        tldr_text = re.sub(r"<[^>]+>", "", tldr_block.group(1)).strip()
        tldr_text = re.sub(r"\s+", " ", tldr_text)

    # h2 sections (skip FAQ heading)
    h2_matches = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)
    sections = []
    for h in h2_matches:
        clean = re.sub(r"<[^>]+>", "", h).strip()
        if clean and "자주 묻는 질문" not in clean:
            sections.append(clean)

    # FAQ details summaries
    faq = re.findall(r"<details><summary>(.*?)</summary>", html, re.S)
    faq = [re.sub(r"<[^>]+>", "", q).strip() for q in faq]

    # published / modified
    pub = re.search(r'article:published_time" content="(.*?)"', html)
    mod = re.search(r'article:modified_time" content="(.*?)"', html)

    return {
        "slug": slug,
        "url": f"/{slug}/",
        "h1": h1_text,
        "description": desc_text,
        "tldr": tldr_text,
        "sections": sections,
        "faq": faq,
        "published": pub.group(1) if pub else None,
        "modified": mod.group(1) if mod else None,
    }

result = {}
for series_name, slugs in SERIES.items():
    result[series_name] = [extract(s) for s in slugs]

out = ROOT / ".tools" / "structure.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Wrote {out}")
print(f"Articles: {sum(len(v) for v in result.values())}")
