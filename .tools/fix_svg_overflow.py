#!/usr/bin/env python3
"""Targeted fixes for overflowing SVG text elements."""
import pathlib, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent

FIXES = [
    (
        'updates/Shin-ETV-TAF-RCT-GnL-2026/index.html',
        '<text x="180" y="80" font-size="13" font-weight="700" fill="#1f6f5c">바이러스 억제 (HBV DNA &lt;LLOQ)</text>',
        '<text x="180" y="80" font-size="11" font-weight="700" fill="#1f6f5c">바이러스 억제 (HBV DNA &lt;LLOQ)</text>',
    ),
    (
        'updates/Chung-SGLT2-Liver-MR-Hepatology-2024/index.html',
        '<text x="590" y="106" font-size="11" fill="#15803d">MASLD↓ · 간경변·간세포암(HCC)↓</text>',
        '<text x="590" y="106" font-size="10" fill="#15803d">MASLD↓ · 간경변·HCC↓</text>',
    ),
    (
        'updates/Chung-SGLT2-Liver-MR-Hepatology-2024/index.html',
        '<text x="110" y="106" font-size="11" fill="#5a5a5a">유전적 instrument</text>',
        '<text x="110" y="106" font-size="10" fill="#5a5a5a">유전 instrument</text>',
    ),
    (
        'updates/GLP1RA-small-molecule-orforglipron/index.html',
        '<text x="490" y="86" font-size="13" font-weight="700" fill="#15803d">Orforglipron — 경구 small-molecule</text>',
        '<text x="490" y="86" font-size="11" font-weight="700" fill="#15803d">Orforglipron — 경구 small-molecule</text>',
    ),
    (
        'updates/GLP1RA-small-molecule-orforglipron/index.html',
        '<text x="130" y="138" font-size="13" fill="#a16207">peptide · 보관 까다로움</text>',
        '<text x="130" y="138" font-size="11" fill="#a16207">peptide · 보관 까다로움</text>',
    ),
    (
        'updates/GLP1RA-small-molecule-orforglipron/index.html',
        '<text x="490" y="138" font-size="13" fill="#15803d">단백질 분해 영향 적음 · 음식·물 자유</text>',
        '<text x="490" y="138" font-size="11" fill="#15803d">분해 영향 적음 · 음식·물 자유</text>',
    ),
    (
        'updates/GLP1RA-small-molecule-orforglipron/index.html',
        '<text x="130" y="86" font-size="13" font-weight="700" fill="#a16207">주사형 (semaglutide)</text>',
        '<text x="130" y="86" font-size="11" font-weight="700" fill="#a16207">주사형 (semaglutide)</text>',
    ),
    (
        'updates/Shin-TDF-ETV-TAF-switch-HCC-HepRes-2024/index.html',
        '<text x="120" y="86" font-size="13" font-weight="700" fill="#a16207">ETV 또는 TAF 유지</text>',
        '<text x="120" y="86" font-size="12" font-weight="700" fill="#a16207">ETV·TAF 유지</text>',
    ),
    (
        'updates/MAESTRO-NASH-resmetirom-NEJM-2024/index.html',
        '<text x="580" y="86" font-size="12" font-weight="600" fill="#15803d">resmetirom 100mg</text>',
        '<text x="580" y="86" font-size="11" font-weight="600" fill="#15803d">resmetirom 100mg</text>',
    ),
]

# Excluded: aHR <1 cases (likely fit due to short content despite heuristic flag)
# Excluded: 잔존부위/4-6주/→ 6개월/양성가능성/HCC 가능성 — likely fit (heuristic FP)

count = 0
fail = 0
for f, old, new in FIXES:
    p = ROOT / f
    text = p.read_text(encoding='utf-8')
    if old not in text:
        print(f'NOT FOUND in {f}: {old[:60]}...')
        fail += 1
        continue
    text = text.replace(old, new)
    p.write_text(text, encoding='utf-8')
    count += 1

print(f'\nFixed: {count}, NotFound: {fail}')
