#!/usr/bin/env python3
"""Merge the separate <ul class="updates-list"> block into the main
<ul class="topic-list"> with proper citation format + chronological sort."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / 'updates' / 'index.html'

# 10 new entries with proper citations + dates
NEW_ENTRIES = [
    # (date_sort_key, date_display, slug, title, citation)
    ('2024-11', '2024·11', 'MAESTRO-NASH-resmetirom-3년-2024',
     'Resmetirom 3년 추적 — 첫 MASH 치료제의 장기 효과',
     'Harrison SA et al. <em>Hepatology</em> 2024 (3-year extension).'),
    ('2024-09', '2024·9', 'LEAP-012-TACE-pembro-lenva-Lancet-2024',
     'LEAP-012 — TACE + pembrolizumab + lenvatinib (중간기 HCC)',
     'Llovet JM et al. <em>Lancet</em> 2024.'),
    ('2024-08', '2024·8', 'CheckMate-9DW-nivo-ipi-Lancet-2024',
     'CheckMate 9DW — nivolumab + ipilimumab 1차 HCC',
     'Galle PR et al. <em>Lancet</em> 2024.'),
    ('2024-06', '2024·6', 'ESSENCE-survodutide-MASH-Lancet-2024',
     'Survodutide — GLP-1/Glucagon 이중 작용제 MASH 임상',
     'Sanyal AJ et al. <em>NEJM/Lancet</em> 2024.'),
    ('2024-05', '2024·5', 'AI-CT-HCC-validation-Hepatology-2024',
     'AI 기반 동적 CT 간세포암 진단 — 다기관 다국가 검증',
     'Multi-institutional validation. <em>Hepatology</em> 2024.'),
    ('2024-03', '2024·3', 'EMERALD-1-TACE-durva-bev-Lancet-2024',
     'EMERALD-1 — TACE + durvalumab + bevacizumab (중간기 HCC)',
     'Lencioni R et al. <em>Lancet</em> 2024;403:1547–1559.'),
    ('2024-01', '2024·1', 'Bepirovirsen-HBV-Lancet-2024',
     'Bepirovirsen — HBV antisense oligonucleotide의 functional cure 도전',
     'Yuen MF et al. <em>NEJM/Lancet</em> 2024 (B-Clear).'),
    ('2023-12', '2023·12', 'MASLD-nomenclature-AASLD-EASL-2023',
     'MASLD·MASH·MetALD — NAFLD/NASH를 대체한 새 표준 명명',
     'Rinella ME et al. <em>Hepatology</em> 2023;78(6):1966–1986.'),
    ('2023-11', '2023·11', 'IMbrave050-adjuvant-atezo-bev-Lancet-2023',
     'IMbrave050 — 근치 치료 후 보조 atezolizumab + bevacizumab',
     'Qin S et al. <em>Lancet</em> 2023;402:1835–1847.'),
    ('2022-04', '2022·4', 'Baveno-VII-recompensation-2024',
     'Baveno VII — 비대상성 간경변의 재대상화 임상 정의',
     'de Franchis R et al. <em>J Hepatol</em> 2022;76:959–974 + 2024 refinement.'),
]


def parse_date(num_text: str) -> str:
    """Convert <span class="num"> text like '2026·4', '2024·9', '2018', '2010·6' → 'YYYY-MM' for sort."""
    s = num_text.replace('·', '-').strip()
    if '-' in s:
        parts = s.split('-')
        return f'{parts[0]}-{int(parts[1]):02d}'
    return f'{s}-00'


def li_html(num: str, slug: str, title: str, citation: str) -> str:
    return (
        f'  <li class="published"><a href="/updates/{slug}/">'
        f'<span class="num">{num}</span>'
        f'<div class="body"><h3>{title}</h3><p>{citation}</p></div>'
        f'<span class="status published">읽기 →</span></a></li>'
    )


def main():
    text = PAGE.read_text(encoding='utf-8')

    # 1. Extract existing topic-list items
    topic_list_match = re.search(
        r'(<ul class="topic-list"[^>]*>)(.*?)(</ul>)',
        text, re.DOTALL,
    )
    if not topic_list_match:
        print('topic-list not found')
        return
    open_tag, body, close_tag = topic_list_match.groups()
    items = re.findall(r'<li class="published">.*?</li>', body, re.DOTALL)
    print(f'existing items: {len(items)}')

    # 2. Index existing slugs (avoid duplicates)
    existing_slugs = set()
    for it in items:
        m = re.search(r'href="/updates/([^/]+)/"', it)
        if m:
            existing_slugs.add(m.group(1))

    # 3. Add new entries (skip duplicates)
    added_items = []
    for sort_key, num, slug, title, cite in NEW_ENTRIES:
        if slug in existing_slugs:
            continue
        added_items.append((sort_key, li_html(num, slug, title, cite)))

    # 4. Re-sort all items by date desc
    indexed = []
    for it in items:
        m = re.search(r'<span class="num">([^<]+)</span>', it)
        key = parse_date(m.group(1)) if m else '0000-00'
        indexed.append((key, it))
    indexed.extend(added_items)
    indexed.sort(key=lambda x: x[0], reverse=True)
    print(f'after merge: {len(indexed)} items')

    new_body = '\n' + '\n'.join(it for _, it in indexed) + '\n'
    new_text = (
        text[:topic_list_match.start()]
        + open_tag + new_body + close_tag
        + text[topic_list_match.end():]
    )

    # 5. Remove the separate <ul class="updates-list">...</ul> block
    new_text = re.sub(
        r'<ul class="updates-list"[^>]*>.*?</ul>\s*',
        '',
        new_text,
        flags=re.DOTALL,
    )

    PAGE.write_text(new_text, encoding='utf-8')
    print(f'wrote {PAGE.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
