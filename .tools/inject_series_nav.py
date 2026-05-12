#!/usr/bin/env python3
"""Detail 페이지 하단에 같은 hub 내 prev/next 시리즈 내비게이션 삽입.

각 페이지의 page-id (N-M)를 읽어 section N에서 정렬 → prev/next 찾음.
삽입 위치: <aside class="related-auto"> 직전.
마커: <!-- series-nav:auto:start --> ... <!-- series-nav:auto:end -->
"""
import re
import html
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','간양성종양',
    '케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search',
    '.tools','.git','.github','private-figures','node_modules',
}

PAGE_ID_RE = re.compile(r'<span class="page-id">(\d+)-(\d+)</span>')
H1_RE = re.compile(r'<h1[^>]*>([^<]+)</h1>')
CRUMB_LABEL_RE = re.compile(r'<nav class="crumb">.*?›\s*<span>([^<]+)</span>', re.DOTALL)
HUB_LINK_RE = re.compile(r'<nav class="crumb">.*?<a href="(/[^/]+/)"[^>]*>([^<]+)</a>', re.DOTALL)

MARK_START = '<!-- series-nav:auto:start -->'
MARK_END = '<!-- series-nav:auto:end -->'
BLOCK_RE = re.compile(rf'{re.escape(MARK_START)}.*?{re.escape(MARK_END)}\s*', re.DOTALL)


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in EXCLUDE and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx


def gather():
    """Return: {section: [(item_id, slug, short_label, h1)]} sorted by item_id."""
    by_sec: dict[int, list[tuple[int, str, str, str]]] = {}
    hub_label_by_sec: dict[int, tuple[str, str]] = {}
    for f in detail_pages():
        txt = f.read_text(encoding='utf-8')
        pidm = PAGE_ID_RE.search(txt)
        if not pidm:
            continue
        sec, item = int(pidm.group(1)), int(pidm.group(2))
        labm = CRUMB_LABEL_RE.search(txt)
        label = labm.group(1) if labm else f.parent.name
        h1m = H1_RE.search(txt)
        h1 = h1m.group(1).strip() if h1m else f.parent.name
        hubm = HUB_LINK_RE.search(txt)
        if hubm and sec not in hub_label_by_sec:
            hub_label_by_sec[sec] = (hubm.group(1), hubm.group(2))
        by_sec.setdefault(sec, []).append((item, f.parent.name, label, h1))
    for sec in by_sec:
        by_sec[sec].sort(key=lambda x: x[0])
    return by_sec, hub_label_by_sec


def make_nav(prev_t: tuple | None, next_t: tuple | None, hub: tuple[str, str] | None) -> str:
    """prev_t/next_t = (item, slug, label, h1)"""
    prev_html = ''
    if prev_t:
        item, slug, label, h1 = prev_t
        href = '/' + quote(slug) + '/'
        prev_html = (
            f'<a class="series-nav-link prev" href="{href}">'
            f'<span class="dir">← 이전</span>'
            f'<span class="title">{html.escape(label)}</span>'
            f'</a>'
        )
    else:
        prev_html = '<span class="series-nav-link empty"></span>'
    if next_t:
        item, slug, label, h1 = next_t
        href = '/' + quote(slug) + '/'
        next_html = (
            f'<a class="series-nav-link next" href="{href}">'
            f'<span class="dir">다음 →</span>'
            f'<span class="title">{html.escape(label)}</span>'
            f'</a>'
        )
    else:
        next_html = '<span class="series-nav-link empty"></span>'
    hub_html = ''
    if hub:
        hub_href, hub_name = hub
        hub_html = (
            f'<a class="series-nav-hub" href="{hub_href}">'
            f'<span class="dir">목록</span>'
            f'<span class="title">{html.escape(hub_name)} 전체 보기</span>'
            f'</a>'
        )
    return (
        f'{MARK_START}\n'
        '<nav class="series-nav" aria-label="시리즈 이동">\n'
        f'  {prev_html}\n  {hub_html}\n  {next_html}\n'
        '</nav>\n'
        f'{MARK_END}'
    )


def main():
    by_sec, hub_label_by_sec = gather()
    changed = 0
    for f in detail_pages():
        txt = f.read_text(encoding='utf-8')
        pidm = PAGE_ID_RE.search(txt)
        if not pidm:
            continue
        sec, item = int(pidm.group(1)), int(pidm.group(2))
        seq = by_sec.get(sec, [])
        # find index of this item
        idx = next((i for i, t in enumerate(seq) if t[0] == item and t[1] == f.parent.name), None)
        if idx is None:
            continue
        prev_t = seq[idx - 1] if idx > 0 else None
        next_t = seq[idx + 1] if idx + 1 < len(seq) else None
        if prev_t is None and next_t is None:
            continue
        hub = hub_label_by_sec.get(sec)
        nav = make_nav(prev_t, next_t, hub)

        # insert before related-auto, else before disclaimer, else before </article>
        if MARK_START in txt:
            new = BLOCK_RE.sub(nav + '\n', txt)
        else:
            insert_before = None
            for marker in ['<aside class="related-auto"',
                           '<p class="disclaimer"',
                           '</article>']:
                i = txt.find(marker)
                if i != -1:
                    insert_before = i
                    break
            if insert_before is None:
                continue
            new = txt[:insert_before] + nav + '\n' + txt[insert_before:]
        if new != txt:
            f.write_text(new, encoding='utf-8')
            changed += 1
    print(f'Pages updated: {changed}')


if __name__ == '__main__':
    main()
