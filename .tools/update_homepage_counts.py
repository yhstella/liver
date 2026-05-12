#!/usr/bin/env python3
"""
update_homepage_counts.py — Recount every hub/section and refresh the
display numbers on:
  - / (homepage 8 hub cards + 최신 지견 count)
  - /간암/ /간경화/ etc (series-meta 8 hubs)

Idempotent. Safe to run after every content change.
Wired into .tools/rebuild_seo.py.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUBS = [
    ('간암',         '간암'),
    ('간경화',       '간경화'),
    ('B형간염',      'B형 간염'),
    ('지방간',       '지방간'),
    ('간수치',       '간수치 이상'),
    ('C형간염',      'C형 간염'),
    ('자가면역간염', '자가면역간염'),
    ('간양성종양',   '간 양성종양'),
]
HUB_SERIES_NUM = {
    '간암': 1, '간경화': 2, 'B형간염': 3, '지방간': 4,
    '간수치': 5, 'C형간염': 6, '자가면역간염': 7, '간양성종양': 8,
}


def count_li_published(html: str, ul_class: str) -> int:
    m = re.search(rf'<ul[^>]*class="{ul_class}"[^>]*>(.*?)</ul>', html, re.DOTALL)
    if not m:
        return 0
    return len(re.findall(r'<li class="published">', m.group(1)))


def count_cases_in_series(landing_html: str, series_n: int) -> int:
    m = re.search(
        rf'<section[^>]+data-series="{series_n}"[^>]*>(.*?)</section>',
        landing_html, re.DOTALL,
    )
    if not m:
        return 0
    return len(re.findall(r'class="case-row"', m.group(1)))


def main():
    # Load landings once
    cases_landing = (ROOT / '케이스' / 'index.html').read_text(encoding='utf-8')
    updates_landing = (ROOT / 'updates' / 'index.html').read_text(encoding='utf-8')
    cc_landing = (ROOT / 'CC' / 'index.html').read_text(encoding='utf-8')

    n_updates = count_li_published(updates_landing, 'topic-list')
    n_cc = len(re.findall(r'class="cc-row"', cc_landing))

    print(f'updates total: {n_updates}편')
    print(f'CC total: {n_cc}편')
    print()

    # Per-hub counts
    counts = {}
    for slug, _ in HUBS:
        hub_html = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
        n_detail = count_li_published(hub_html, 'topic-list')
        n_cases = count_cases_in_series(cases_landing, HUB_SERIES_NUM[slug])
        counts[slug] = (n_detail, n_cases)
        print(f'  {slug}: 세부주제 {n_detail}편 · 사례 {n_cases}편')

    # ── Update 케이스 landing intro "총 N편" ──────────────────────────
    n_cases_total = sum(c[1] for c in counts.values())
    cases_landing_path = ROOT / '케이스' / 'index.html'
    cases_text = cases_landing_path.read_text(encoding='utf-8')
    new_cases_text = re.sub(
        r'(<p class="intro"[^>]*>[^<]*?총\s*)\d+(편[^<]*</p>)',
        rf'\g<1>{n_cases_total}\g<2>',
        cases_text,
        count=1,
    )
    if new_cases_text != cases_text:
        cases_landing_path.write_text(new_cases_text, encoding='utf-8')
        print(f'케이스 landing intro: 총 {n_cases_total}편')

    # ── Update each hub's series-meta ─────────────────────────────────
    for slug, _ in HUBS:
        n_detail, n_cases = counts[slug]
        hub_path = ROOT / slug / 'index.html'
        text = hub_path.read_text(encoding='utf-8')
        target = f'<div class="series-meta"><span>세부주제 {n_detail}편 · 사례 {n_cases}편</span></div>'
        # Match any existing series-meta (single or two-span variant) and replace
        new_text = re.sub(
            r'<div class="series-meta">\s*(?:<span>[^<]*</span>\s*)+</div>',
            target,
            text,
            count=1,
        )
        if new_text != text:
            hub_path.write_text(new_text, encoding='utf-8')

    # ── Update homepage hub cards + updates count ─────────────────────
    home = ROOT / 'index.html'
    text = home.read_text(encoding='utf-8')
    for slug, label in HUBS:
        n_detail, n_cases = counts[slug]
        new_count = f'세부주제 {n_detail}편 · 사례 {n_cases}편'
        # Find each tile by href and replace the count span content
        pattern = re.compile(
            rf'(<a href="/{slug}/" class="series-tile">\s*<h3>[^<]+</h3>\s*<span class="count">)([^<]+)(</span>)',
        )
        text = pattern.sub(lambda m: m.group(1) + new_count + m.group(3), text, count=1)

    # Update "N updates" / "N편" in updates-tile
    text = re.sub(
        r'(<section class="updates-section">.*?<span class="count">)([^<]+)(</span>)',
        lambda m: f'{m.group(1)}{n_updates}편{m.group(3)}',
        text,
        count=1,
        flags=re.DOTALL,
    )

    home.write_text(text, encoding='utf-8')
    print(f'\nupdated homepage hub cards (8) + updates count → {n_updates}편')


if __name__ == '__main__':
    main()
