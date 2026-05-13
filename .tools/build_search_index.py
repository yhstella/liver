#!/usr/bin/env python3
"""사이트 전체 search-index.json 생성.

각 entry: {u, t, tl, c, pid, d, k}
  u  = URL (e.g., /간암-진단-첫외래/)
  t  = full title (H1)
  tl = short label (breadcrumb 마지막 span)
  c  = category (hub|detail|case|cc|update|page)
  pid= page-id "N-M" (있으면)
  d  = TLDR snippet 또는 lede 첫 ~120자
  k  = keywords (쉼표로 join)

홈/소개/연구/keywords 페이지는 c='page'로 포함 (검색 가능).
"""
import json
import re
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parent.parent

HUB_SLUGS = {'간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간질환','간양성종양'}
SKIP_DIRS = {'.git','.tools','node_modules','private-figures','assets','guide','search'}
LEGACY_REDIRECTS = {'자가면역간염'}  # search index에서 제외

H1_RE = re.compile(r'<h1[^>]*>(.+?)</h1>', re.DOTALL)
CRUMB_LABEL_RE = re.compile(r'<nav class="crumb">.*?›\s*<span>([^<]+)</span>', re.DOTALL)
PID_RE = re.compile(r'<span class="page-id">([^<]+)</span>')
TLDR_RE = re.compile(r'<div class="tldr">(?:<strong>[^<]+</strong>)?(.+?)</div>', re.DOTALL)
LEDE_RE = re.compile(r'<p class="lede">(.+?)</p>', re.DOTALL)
META_DESC_RE = re.compile(r'<meta name="description" content="([^"]+)"')
TAG_CHIP_RE = re.compile(r'class="tag-chip"[^>]*>([^<]+)</a>')


def strip_tags(s: str) -> str:
    return unescape(re.sub(r'<[^>]+>', '', s)).strip()


def trim(s: str, n: int) -> str:
    s = re.sub(r'\s+', ' ', s)
    if len(s) <= n:
        return s
    return s[:n].rstrip() + '…'


def url_for(p: Path) -> str:
    rel = p.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('/index.html')] + '/'
    return '/' + rel


def categorize(p: Path) -> str:
    rel = p.relative_to(ROOT).as_posix()
    parts = rel.split('/')
    if rel == 'index.html':
        return 'home'
    if parts[0] in HUB_SLUGS and parts[1] == 'index.html':
        return 'hub'
    if parts[0] == '케이스':
        return 'case'
    if parts[0] == 'CC':
        return 'cc'
    if parts[0] == 'updates':
        return 'update'
    if parts[0] in ('소개', '연구', 'keywords'):
        return 'page'
    return 'detail'


def main():
    out = []
    for p in ROOT.rglob('index.html'):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        if any(part.startswith('.') for part in p.relative_to(ROOT).parts):
            continue
        # legacy redirect 페이지는 search index에서 제외
        rel_parts = p.relative_to(ROOT).parts
        if len(rel_parts) == 2 and rel_parts[0] in LEGACY_REDIRECTS:
            continue
        txt = p.read_text(encoding='utf-8')
        cat = categorize(p)
        h1m = H1_RE.search(txt)
        title = strip_tags(h1m.group(1)) if h1m else ''
        labm = CRUMB_LABEL_RE.search(txt)
        short = strip_tags(labm.group(1)) if labm else title
        pidm = PID_RE.search(txt)
        pid = pidm.group(1) if pidm else ''
        # description: TLDR > lede > meta desc
        desc = ''
        if (m := TLDR_RE.search(txt)):
            desc = trim(strip_tags(m.group(1)), 160)
        elif (m := LEDE_RE.search(txt)):
            desc = trim(strip_tags(m.group(1)), 160)
        elif (m := META_DESC_RE.search(txt)):
            desc = trim(m.group(1), 160)
        # keywords from tag-chips
        kw = list(set(TAG_CHIP_RE.findall(txt)))
        entry = {
            'u': url_for(p),
            't': title or short,
            'tl': short,
            'c': cat,
        }
        if pid:
            entry['pid'] = pid
        if desc:
            entry['d'] = desc
        if kw:
            entry['k'] = ','.join(kw[:8])
        if entry['t']:
            out.append(entry)

    # Sort: hub > detail > case > cc > update > page, by category then title then URL
    # URL을 tertiary key로 추가 — 같은 (cat, title) 항목의 안정적 정렬 (rglob 순서 의존 제거)
    cat_order = {'hub': 0, 'detail': 1, 'case': 2, 'cc': 3, 'update': 4, 'page': 5, 'home': 6}
    out.sort(key=lambda e: (cat_order.get(e['c'], 9), e['t'], e['u']))

    dst = ROOT / 'search-index.json'
    dst.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Wrote {dst} ({len(out)} entries, {dst.stat().st_size//1024} KB)')


if __name__ == '__main__':
    main()
