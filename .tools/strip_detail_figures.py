#!/usr/bin/env python3
"""세부주제(detail) 페이지의 figure 블록 일괄 제거. 표(<table>)는 보존.

제거 대상:
  - <!-- db-figure:auto:start --> ... <!-- db-figure:auto:end -->
  - <!-- fig --> ... <!-- /fig -->
  - 그 외 standalone <figure>...</figure> (혹시 모를 잔재)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {
    '간암', '간경화', 'B형간염', '지방간', '간수치', 'C형간염', '자가면역간염', '간양성종양',
    '케이스', 'CC', 'updates', 'keywords', 'assets', 'guide', '소개', '연구', '논문', 'search',
    '.tools', '.git', '.github', 'private-figures', 'node_modules',
}

PATTERNS = [
    re.compile(r'<!-- db-figure:auto:start -->.*?<!-- db-figure:auto:end -->\s*', re.DOTALL),
    re.compile(r'<!-- fig -->.*?<!-- /fig -->\s*', re.DOTALL),
    re.compile(r'<figure\b[^>]*>.*?</figure>\s*', re.DOTALL),
]

EXTRA_BLANK = re.compile(r'\n{3,}')


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in EXCLUDE and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx


def main():
    total_removed = 0
    pages_changed = 0
    for f in detail_pages():
        text = f.read_text(encoding='utf-8')
        new = text
        removed_here = 0
        for pat in PATTERNS:
            new2, n = pat.subn('', new)
            removed_here += n
            new = new2
        new = EXTRA_BLANK.sub('\n\n', new)
        if new != text:
            f.write_text(new, encoding='utf-8')
            pages_changed += 1
            total_removed += removed_here
            print(f'  {f.parent.name}: removed {removed_here}')
    print(f'\nPages changed: {pages_changed}')
    print(f'Figure blocks removed: {total_removed}')


if __name__ == '__main__':
    main()
