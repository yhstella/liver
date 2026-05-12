#!/usr/bin/env python3
"""표 직전 중복 bullet list 제거 (보수적 휴리스틱).

판단 기준 (AND 조건):
  1. <ul>...</ul>의 <li> 중 50% 이상에 ' / ' 또는 ' · ' 비교 separator 존재
  2. </ul> 뒤 600자 이내에 <table 시작
  3. <ul>이 <table>과 동일 페이지에서 같은 H2 섹션 내 (양쪽 사이에 <h2>가 없어야 함)
  4. <ul> 안에 link(<a>)나 image 없음 (관련 글, 인용 등 보호)

이 모든 조건을 만족하면 ul 제거.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','간양성종양',
    '케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search',
    '.tools','.git','.github','private-figures','node_modules',
}

UL_RE = re.compile(r'<ul>(.*?)</ul>', re.DOTALL)
LI_RE = re.compile(r'<li>(.*?)</li>', re.DOTALL)


def is_duplicate_candidate(ul_content: str) -> bool:
    if '<a ' in ul_content or '<img ' in ul_content:
        return False
    items = LI_RE.findall(ul_content)
    if len(items) < 3:
        return False
    sep_count = 0
    for it in items:
        # Strip tags
        plain = re.sub(r'<[^>]+>', '', it)
        # Detect comparison-style separators (with surrounding spaces, ko 슬래시 등)
        if (' / ' in plain) or (re.search(r'\b\d.*?\s*[/–-]\s*\d', plain) and len(plain) < 120):
            sep_count += 1
    return sep_count >= len(items) * 0.5


def followed_by_table_in_same_section(text: str, ul_end: int, max_dist: int = 600) -> bool:
    after = text[ul_end:ul_end + max_dist]
    tbl_pos = after.find('<table')
    if tbl_pos == -1:
        return False
    # Check no <h2 between ul_end and table
    h2_pos = after.find('<h2')
    if h2_pos != -1 and h2_pos < tbl_pos:
        return False
    return True


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in EXCLUDE and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx


def main():
    pages = 0
    total = 0
    for f in detail_pages():
        text = f.read_text(encoding='utf-8')
        # We need to iterate over UL matches in reverse to keep offsets valid
        matches = list(UL_RE.finditer(text))
        to_remove = []
        for m in matches:
            ul_inner = m.group(1)
            if not is_duplicate_candidate(ul_inner):
                continue
            if not followed_by_table_in_same_section(text, m.end()):
                continue
            to_remove.append((m.start(), m.end()))
        if not to_remove:
            continue
        # Remove in reverse to preserve offsets
        new = text
        for start, end in reversed(to_remove):
            new = new[:start] + new[end:]
        # Cleanup extra blanks
        new = re.sub(r'\n{3,}', '\n\n', new)
        f.write_text(new, encoding='utf-8')
        pages += 1
        total += len(to_remove)
        print(f'  {f.parent.name}: removed {len(to_remove)} duplicate ul(s)')
    print(f'\nPages changed: {pages}, duplicate UL removed: {total}')


if __name__ == '__main__':
    main()
