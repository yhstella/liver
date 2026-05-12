#!/usr/bin/env python3
"""Detail 페이지의 <!-- tags --> tag-row 블록을 본문 하단(related-auto/disclaimer 직전)으로 이동.

소개 페이지의 tag-row(진료분야 카드)는 마커 없으니 안 건드림.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TAGS_BLOCK_RE = re.compile(
    r'\n?<!-- tags -->\s*\n?<p class="tag-row">.*?</p>\s*\n?<!-- /tags -->\s*\n?',
    re.DOTALL,
)

SKIP_DIRS = {'.git', '.tools', 'node_modules', 'private-figures', 'assets'}


def insertion_point(text: str) -> int:
    # priority: before related-auto, else before disclaimer, else before </article>
    for marker in ['<aside class="related-auto"',
                   '<p class="disclaimer"',
                   '</article>']:
        i = text.find(marker)
        if i != -1:
            return i
    return -1


def main():
    changed = 0
    for p in ROOT.rglob('*.html'):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        text = p.read_text(encoding='utf-8')
        m = TAGS_BLOCK_RE.search(text)
        if not m:
            continue
        # Already at bottom? Check if related-auto is BEFORE the tag-row
        rel_pos = text.find('<aside class="related-auto"')
        if rel_pos != -1 and rel_pos < m.start():
            continue  # already moved
        block = m.group(0).strip()  # without surrounding whitespace
        removed = text[:m.start()] + text[m.end():]
        insert_at = insertion_point(removed)
        if insert_at == -1:
            continue
        # Wrap with new class to style as bottom tag-strip
        block = block.replace('<p class="tag-row">', '<p class="tag-row tag-row-bottom">')
        new = removed[:insert_at] + block + '\n' + removed[insert_at:]
        p.write_text(new, encoding='utf-8')
        changed += 1
    print(f'Pages updated: {changed}')


if __name__ == '__main__':
    main()
