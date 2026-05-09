"""Replace 논문 → 연구 across all HTML files and build scripts.
Targets:
- nav links: <a href="/논문/">논문</a> → <a href="/연구/">연구</a>
- footer column links: same
- internal references in articles
- builder NAV/FOOTER strings (build_articles.py, build_series_hubs.py, build_updates.py)
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

# Patterns to replace
REPLACEMENTS = [
    ('href="/논문/"', 'href="/연구/"'),
    ('href="/논문/" class="active"', 'href="/연구/" class="active"'),
    ('>논문</a>', '>연구</a>'),
    ('"https://drshin.kr/논문/"', '"https://drshin.kr/연구/"'),
    ('"name":"논문"', '"name":"연구"'),
]

n_changed = 0
n_files = 0

# All HTML files
for p in ROOT.rglob("*.html"):
    if "/.git/" in str(p).replace("\\","/") or "/.tools/" in str(p).replace("\\","/"):
        continue
    if p.name == "guide_template.html":
        continue
    text = p.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        n_changed += 1
        rel = p.relative_to(ROOT)
        print(f"  updated: {rel}")
    n_files += 1

# Build scripts
for fname in ["build_articles.py", "build_series_hubs.py", "build_updates.py", "build_research.py"]:
    p = ROOT / ".tools" / fname
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        print(f"  updated: .tools/{fname}")

# Update guide_template.html (NOT built file)
gt = ROOT / ".tools" / "guide_template.html"
if gt.exists():
    text = gt.read_text(encoding="utf-8")
    orig = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != orig:
        gt.write_text(text, encoding="utf-8")
        print(f"  updated: .tools/guide_template.html")

print(f"\nTotal HTML files scanned: {n_files}, changed: {n_changed}")
