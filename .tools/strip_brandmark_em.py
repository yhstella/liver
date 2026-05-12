#!/usr/bin/env python3
"""Strip the <em> wrap from header brand-mark across site (B option)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = '<a href="/" class="brand-mark">Hepatology<em> Note</em></a>'
NEW = '<a href="/" class="brand-mark">Hepatology<em> Note</em></a>'

SKIP_DIRS = {".git", ".tools", "node_modules", "private-figures"}

def walk_files():
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        # skip ignored dirs
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        if p.suffix.lower() in (".html", ".py"):
            yield p
    # explicitly include .tools/*.py and guide_template.html
    for p in (ROOT / ".tools").glob("*.py"):
        yield p
    for p in (ROOT / ".tools").glob("*.html"):
        yield p

seen = set()
hit = 0
for p in walk_files():
    rp = p.resolve()
    if rp in seen:
        continue
    seen.add(rp)
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        continue
    if OLD in text:
        text = text.replace(OLD, NEW)
        p.write_text(text, encoding="utf-8")
        hit += 1
        print(f"  {p.relative_to(ROOT)}")

print(f"\nTotal files updated: {hit}")
