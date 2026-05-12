#!/usr/bin/env python3
"""Add cache-busting ?v=N query to all favicon link tags site-wide.

모바일 브라우저(특히 iOS Safari)는 favicon을 매우 공격적으로 캐시합니다.
변경 적용에는 URL 변경이 가장 확실.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "3"

# (old, new) pairs. URL이 변경된 적이 없으니 첫 일괄 적용.
# 이미 ?v=X가 있으면 그것을 ?v={VERSION}으로 교체.
import re

PATTERNS = [
    (r'(href="/favicon\.ico)(\?v=\d+)?(")', rf'\1?v={VERSION}\3'),
    (r'(href="/favicon-16\.png)(\?v=\d+)?(")', rf'\1?v={VERSION}\3'),
    (r'(href="/favicon-32\.png)(\?v=\d+)?(")', rf'\1?v={VERSION}\3'),
    (r'(href="/favicon-192\.png)(\?v=\d+)?(")', rf'\1?v={VERSION}\3'),
    (r'(href="/favicon-512\.png)(\?v=\d+)?(")', rf'\1?v={VERSION}\3'),
    (r'(href="/apple-touch-icon\.png)(\?v=\d+)?(")', rf'\1?v={VERSION}\3'),
    (r'(href="/site\.webmanifest)(\?v=\d+)?(")', rf'\1?v={VERSION}\3'),
]
COMPILED = [(re.compile(p), r) for p, r in PATTERNS]

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
    new = text
    for pat, repl in COMPILED:
        new = pat.sub(repl, new)
    if new != text:
        p.write_text(new, encoding="utf-8")
        hit += 1

print(f"Total files updated: {hit}")

# Also update the site.webmanifest itself to point to versioned icons
manifest = ROOT / "site.webmanifest"
if manifest.exists():
    txt = manifest.read_text(encoding="utf-8")
    new = re.sub(r'(/favicon-192\.png)(\?v=\d+)?', rf'\1?v={VERSION}', txt)
    new = re.sub(r'(/favicon-512\.png)(\?v=\d+)?', rf'\1?v={VERSION}', new)
    if new != txt:
        manifest.write_text(new, encoding="utf-8")
        print(f"  manifest updated")
