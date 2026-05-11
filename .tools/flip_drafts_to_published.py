#!/usr/bin/env python3
"""Flip noindex,nofollow → index,follow on all DRAFT pages except /guide/."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {'guide'}  # legitimately noindex

OLD_META = re.compile(
    r'<meta\s+name="robots"\s+content="noindex,nofollow">(<!--\s*DRAFT:[^>]*-->)?',
    re.IGNORECASE,
)
NEW_META = '<meta name="robots" content="index,follow,max-image-preview:large">'

n = 0
for p in ROOT.rglob('index.html'):
    parts = p.relative_to(ROOT).parts
    if any(x in EXCLUDE for x in parts):
        continue
    if any(x.startswith('.') for x in parts):
        continue
    text = p.read_text(encoding='utf-8')
    if 'noindex,nofollow' not in text:
        continue
    new = OLD_META.sub(NEW_META, text)
    # Also handle case where comment is on separate line
    new = re.sub(r'<!--\s*DRAFT:\s*전문 번역가 검수 대기\s*-->\s*\n?', '', new)
    if new != text:
        p.write_text(new, encoding='utf-8')
        n += 1
        print(f'  flipped: {p.relative_to(ROOT)}')
print(f'\n{n} pages flipped to index,follow')
