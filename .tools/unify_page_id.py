#!/usr/bin/env python3
"""세부 페이지 breadcrumb에 누락된 page-id (N-M) 일괄 보강.

방침:
  1. breadcrumb의 hub link (e.g. <a href="/간암/">) URL을 보고 section 결정
  2. section 내 기존 page-id 최대값 + 1부터 sequential 할당 (slug 알파벳순)
  3. breadcrumb label은 기존 <span> 내용 그대로 보존
     (UX 차원에서 일부는 길지만, 자동 변경은 위험 — 수동 cleanup용)
  4. 이미 page-id 있는 페이지는 건드리지 않음
  5. hub link 없는 비표준 crumb (A형간염 등)은 skip — 수동 처리
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUB_BY_HREF = {
    '/간암/': 1, '/간경화/': 2, '/B형간염/': 3, '/지방간/': 4,
    '/간수치/': 5, '/C형간염/': 6, '/자가면역간염/': 7, '/간양성종양/': 8,
}

EXCLUDE_DIRS = {
    '간암', '간경화', 'B형간염', '지방간', '간수치', 'C형간염', '자가면역간염', '간양성종양',
    '케이스', 'CC', 'updates', 'keywords', 'assets', 'guide', '소개', '연구', '논문', 'search',
    '.tools', '.git', '.github', 'private-figures', 'node_modules',
}

# Crumb의 hub link href 추출
HUB_HREF_RE = re.compile(
    r'<nav class="crumb">[^<]*<a href="/"[^>]*>[^<]*</a>[^<]*›[^<]*<a href="([^"]+)"',
    re.DOTALL,
)
PAGE_ID_RE = re.compile(r'<span class="page-id">(\d+)-(\d+)</span>')

# 두 번째 <span>...</span> (breadcrumb 마지막 라벨) 위치 + closing </nav>
# 패턴: › <span>LABEL</span></nav>  또는  › <span>LABEL</span> <span class="page-id">...</span></nav>
LAST_SPAN_RE = re.compile(
    r'(<nav class="crumb">.*?›\s*<span>[^<]+</span>)\s*</nav>',
    re.DOTALL,
)


def detail_pages():
    for p in ROOT.iterdir():
        if not p.is_dir() or p.name in EXCLUDE_DIRS or p.name.startswith('.'):
            continue
        idx = p / 'index.html'
        if idx.exists():
            yield idx


def main():
    used_by_section: dict[int, set[int]] = {}
    no_id_files: list[tuple[int, Path]] = []  # (section, file)
    skipped: list[str] = []

    for f in detail_pages():
        txt = f.read_text(encoding='utf-8')
        m = PAGE_ID_RE.search(txt)
        if m:
            used_by_section.setdefault(int(m.group(1)), set()).add(int(m.group(2)))
            continue
        hm = HUB_HREF_RE.search(txt)
        if not hm:
            skipped.append(f.parent.name)
            continue
        href = hm.group(1)
        if href not in HUB_BY_HREF:
            skipped.append(f.parent.name)
            continue
        no_id_files.append((HUB_BY_HREF[href], f))

    # Sort within each section by slug for deterministic assignment
    by_section: dict[int, list[Path]] = {}
    for sec, f in no_id_files:
        by_section.setdefault(sec, []).append(f)
    for sec in by_section:
        by_section[sec].sort(key=lambda p: p.parent.name)

    total = 0
    for sec in sorted(by_section):
        used = used_by_section.get(sec, set())
        next_id = max(used, default=0) + 1
        for f in by_section[sec]:
            while next_id in used:
                next_id += 1
            slug = f.parent.name
            txt = f.read_text(encoding='utf-8')
            new_txt, n = LAST_SPAN_RE.subn(
                rf'\1 <span class="page-id">{sec}-{next_id}</span></nav>',
                txt,
                count=1,
            )
            if n == 0:
                print(f'  SKIP (no last-span match): {slug}')
                continue
            f.write_text(new_txt, encoding='utf-8')
            print(f'  {sec}-{next_id:<3}  {slug}')
            used.add(next_id)
            next_id += 1
            total += 1

    print(f'\nUpdated: {total} files')
    if skipped:
        print(f'\nSkipped (manual handling needed):')
        for s in skipped:
            print(f'  {s}')


if __name__ == '__main__':
    main()
