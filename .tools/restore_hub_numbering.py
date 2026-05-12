#!/usr/bin/env python3
"""Restore sequential <span class="num">NN</span> numbering to 8 hub topic-lists.

`<a href="/...">` 와 `<div class="body">` 사이에 num span 삽입. 이미 num span이 있는
항목(updates/index.html의 '2026·4' 형식 등)은 자연스럽게 skip됨 (regex가 whitespace만 허용).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUBS = ["간암", "간경화", "B형간염", "C형간염", "지방간", "간수치", "자가면역간염", "간양성종양"]

PATTERN = re.compile(r'(<a href="[^"]+">)(\s*)(<div class="body">)')

total = 0
for hub in HUBS:
    p = ROOT / hub / "index.html"
    if not p.exists():
        print(f"  skip (missing): {hub}")
        continue
    text = p.read_text(encoding="utf-8")

    # Only operate within <ul class="topic-list">...</ul>
    m = re.search(r'<ul class="topic-list">(.*?)</ul>', text, re.DOTALL)
    if not m:
        print(f"  skip (no topic-list): {hub}")
        continue
    block = m.group(1)

    counter = [0]
    def repl(match):
        counter[0] += 1
        a_open, ws, div_open = match.group(1), match.group(2), match.group(3)
        return f'{a_open}<span class="num">{counter[0]:02d}</span>{ws}{div_open}'

    new_block = PATTERN.sub(repl, block)
    if counter[0] == 0:
        print(f"  no changes: {hub}")
        continue

    text = text[:m.start(1)] + new_block + text[m.end(1):]
    p.write_text(text, encoding="utf-8")
    total += counter[0]
    print(f"  {hub}: numbered {counter[0]} items (01..{counter[0]:02d})")

print(f"\nTotal items numbered: {total}")
