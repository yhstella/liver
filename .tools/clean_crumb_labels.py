#!/usr/bin/env python3
"""세부 페이지 breadcrumb의 마지막 라벨을 짧고 일관되게 정리.

규칙:
  1. ' — ', ' – ', '—', '–' separator가 있으면 → 첫 부분만 keep
  2. label이 14자 초과면 → slug에서 hub prefix 제거 + '-' → '·' 변환으로 derive
  3. 변경 후에도 1자 이하거나 비어있으면 원본 keep
  4. 기존 page-id span은 보존
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUB_PREFIXES = {
    '/간암/': ['간암-'],
    '/간경화/': ['간경변-', '간경화-'],
    '/B형간염/': ['B형간염-', '가족-B형간염-'],
    '/지방간/': ['지방간-', '지방간염-', '대사이상지방간-'],
    '/간수치/': ['간수치-', '간생검-', '간섬유화스캔-', 'PIVKA-II-', 'ALP-GGT-', '알부민-PT-',
                '약물성-간손상-', '빌리루빈-', '알파태아단백', '알코올성-간질환'],
    '/C형간염/': ['C형간염-'],
    '/자가면역간염/': ['자가면역간염-'],
    '/간양성종양/': ['간양성종양-'],
}

EXCLUDE_DIRS = {
    '간암', '간경화', 'B형간염', '지방간', '간수치', 'C형간염', '자가면역간염', '간양성종양',
    '케이스', 'CC', 'updates', 'keywords', 'assets', 'guide', '소개', '연구', '논문', 'search',
    '.tools', '.git', '.github', 'private-figures', 'node_modules',
}

SEPARATORS = [' — ', ' – ', ' -- ', '—', '–']
MAX_LABEL_LEN = 14


def derive_from_slug(slug: str, hub_href: str) -> str:
    s = slug
    for prefix in HUB_PREFIXES.get(hub_href, []):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    if not s:
        s = slug
    # leading dash 제거
    s = s.lstrip('-')
    # 짧은 토큰들: '-' → '·', 그 외 → space
    tokens = s.split('-')
    if len(tokens) >= 2 and all(len(t) <= 6 for t in tokens):
        s = '·'.join(tokens)
    else:
        s = ' '.join(tokens)
    return s


CRUMB_RE = re.compile(
    r'(<nav class="crumb">.*?<a href="(/[^/]+/)"[^>]*>[^<]*</a>[^<]*›\s*<span>)'
    r'([^<]+)'
    r'(</span>)',
    re.DOTALL,
)


def detail_pages():
    for p in ROOT.iterdir():
        if not p.is_dir() or p.name in EXCLUDE_DIRS or p.name.startswith('.'):
            continue
        idx = p / 'index.html'
        if idx.exists():
            yield idx


def clean_label(old_label: str, slug: str, hub_href: str) -> str:
    # 1) separator-based split
    cur = old_label.strip()
    for sep in SEPARATORS:
        if sep in cur:
            cur = cur.split(sep)[0].strip()
            break
    # 2) Still too long? derive from slug
    if len(cur) > MAX_LABEL_LEN:
        derived = derive_from_slug(slug, hub_href).strip()
        if 1 < len(derived) < len(cur):
            cur = derived
    return cur or old_label


def main():
    changed = 0
    samples = []
    for f in detail_pages():
        txt = f.read_text(encoding='utf-8')
        m = CRUMB_RE.search(txt)
        if not m:
            continue
        prefix, hub_href, old_label, suffix = m.groups()
        new_label = clean_label(old_label, f.parent.name, hub_href)
        if new_label == old_label:
            continue
        new_txt = txt.replace(
            prefix + old_label + suffix,
            prefix + new_label + suffix,
            1,
        )
        f.write_text(new_txt, encoding='utf-8')
        changed += 1
        if len(samples) < 25:
            samples.append((f.parent.name, old_label, new_label))

    print(f'Labels cleaned: {changed}\n')
    print('Sample changes:')
    for slug, old, new in samples:
        print(f'  [{slug}]')
        print(f'     OLD: {old}')
        print(f'     NEW: {new}')


if __name__ == '__main__':
    main()
