#!/usr/bin/env python3
"""남은 <svg class="fig"> ... </svg>+캡션 일괄 제거 (non-grid 다이어그램)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','간양성종양',
    '케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search',
    '.tools','.git','.github','private-figures','node_modules',
}

PATTERN = re.compile(
    r'<svg class="fig"[^>]*>.*?</svg>(\s*<p class="fig-caption">[^<]*</p>)?\s*',
    re.DOTALL,
)
EXTRA = re.compile(r'\n{3,}')

total = 0
pages = 0
for p in ROOT.iterdir():
    if not p.is_dir() or p.name in EXCLUDE or p.name.startswith('.'):
        continue
    idx = p / 'index.html'
    if not idx.exists():
        continue
    text = idx.read_text(encoding='utf-8')
    new, n = PATTERN.subn('', text)
    if n == 0:
        continue
    new = EXTRA.sub('\n\n', new)
    idx.write_text(new, encoding='utf-8')
    pages += 1
    total += n
    print(f'  {p.name}: removed {n}')

print(f'\nPages changed: {pages}, SVG figs removed: {total}')
