#!/usr/bin/env python3
"""
inject_author_box.py — Add a small author-box at the bottom of every detail page,
just above </main>. Boosts E-E-A-T (Expertise · Experience · Authoritativeness · Trust).

Marker: <!-- author:auto:start --> ... <!-- author:auto:end -->
Idempotent: replaces if marker exists, otherwise inserts before </main>.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUBS_8 = {"간암", "간경화", "B형간염", "C형간염", "지방간", "간수치", "자가면역간염", "간양성종양"}
SECTION_HUBS = {"updates", "케이스", "CC", "keywords", "소개", "연구"}
EXCLUDE_DIRS = {".git", ".tools", "node_modules", "assets", "guide", "논문"}

MARKER_START = "<!-- author:auto:start -->"
MARKER_END = "<!-- author:auto:end -->"

AUTHOR_BLOCK = f"""{MARKER_START}
<aside class="author-mini">
  <img src="/assets/img/author/drshin.jpg" alt="" loading="lazy">
  <div class="author-mini-text">
    <strong>신현재</strong>
    <span class="role">서울대학교병원 소화기내과 · 간암센터</span>
    <span class="links"><a href="/소개/">소개</a> · <a href="/연구/">연구</a> · <a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진</a> · <a href="https://scholar.google.com/citations?user=-0ZNZw0AAAAJ" target="_blank" rel="noopener">Scholar</a></span>
  </div>
</aside>
{MARKER_END}"""


def is_detail_page(rel_dir: Path) -> bool:
    if str(rel_dir) == ".":
        return False
    parts = rel_dir.parts
    first = parts[0]
    if len(parts) == 1 and first in HUBS_8:
        return False
    if len(parts) == 1 and first in SECTION_HUBS:
        return False
    return True


def inject(html: str) -> str:
    if MARKER_START in html and MARKER_END in html:
        return re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            AUTHOR_BLOCK,
            html, count=1, flags=re.S,
        )
    if "</main>" in html:
        return html.replace("</main>", f"{AUTHOR_BLOCK}\n</main>", 1)
    return html


def main():
    n = 0
    for path in ROOT.rglob("index.html"):
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if any(p.startswith(".") for p in parts):
            continue
        rel_dir = path.parent.relative_to(ROOT)
        if not is_detail_page(rel_dir):
            continue
        html = path.read_text(encoding="utf-8")
        new_html = inject(html)
        if new_html != html:
            path.write_text(new_html, encoding="utf-8")
            n += 1
    print(f"Injected/updated author-box on {n} detail pages.")


if __name__ == "__main__":
    main()
