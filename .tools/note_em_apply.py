#!/usr/bin/env python3
"""Re-apply <em> around 'Note' in brand-mark site-wide.

User feedback: 'Note'가 브랜드 그린 액센트인 편이 시각적으로 더 낫다.
B option에서 너무 멀리 갔던 부분 되돌리기 (단, H1 강조는 그대로 유지).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = '<a href="/" class="brand-mark">Hepatology<em> Note</em></a>'
NEW = '<a href="/" class="brand-mark">Hepatology<em> Note</em></a>'

SKIP_DIRS = {".git", "node_modules", "private-figures"}

hit = 0
seen = set()
for p in list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.py")):
    rp = p.resolve()
    if rp in seen:
        continue
    seen.add(rp)
    if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if OLD in text:
        text = text.replace(OLD, NEW)
        p.write_text(text, encoding="utf-8")
        hit += 1

print(f"Total files updated: {hit}")
