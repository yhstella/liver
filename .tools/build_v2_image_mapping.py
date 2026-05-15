#!/usr/bin/env python3
"""Build image mapping using ONLY v2 (page-generated-v2/) images.

Scans v2/detail and v2/pilot, maps each filename to a page URL via slug heuristics.
"""
import json, pathlib, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
V2_DETAIL = ROOT / 'assets/img/page-generated-v2/detail'
V2_PILOT = ROOT / 'assets/img/page-generated-v2/pilot'

# Filename slug fragment → page URL
SLUG_TO_URL = {
    # v2/detail names (cat-slug pattern)
    'viral-hcv-2025-kasl-가이드라인': '/C형간염-2025-KASL-가이드라인/',
    'diagnostics-알파태아단백': '/알파태아단백/',
    'diagnostics-alp-ggt-담도-간세포': '/ALP-GGT-담도-간세포/',
    'hcc-hcc-bclc병기': '/간암-BCLC병기/',
    'viral-hbv-functional-cure': '/B형간염-functional-cure/',
    'viral-hbv-검사결과': '/B형간염-검사결과/',
    'viral-hbv-항바이러스제-비교': '/B형간염-항바이러스제-비교/',
    'viral-hcv-완치-daa': '/C형간염-완치-DAA/',
    'diagnostics-fibroscan-수치': '/간섬유화스캔-수치/',
    'masld-fibroscan-수치': '/간섬유화스캔-수치/',  # duplicate covering same URL
    'benign-benign-진단': '/간양성종양-진단/',
    'cirrhosis-cirrhosis-encephalopathy': '/간경변-간성혼수/',
    'hcc-hcc-tace-종류-결정': '/간암-TACE-종류-결정/',
    'hcc-hcc-면역치료-1차': '/간암-면역치료-1차/',
    'cirrhosis-cirrhosis-ascites': '/간경변-복수/',
    'cirrhosis-cirrhosis-varices': '/간경변-식도정맥류/',
    'diagnostics-dili-간손상-dili': '/약물성-간손상-DILI/',
    'autoimmune-pbc-원발성담즙성담관염': '/PBC-원발성담즙성담관염/',
    'autoimmune-aih-진단': '/자가면역간염-진단/',
    'hcc-hcc-치료-선택': '/간암-치료-선택/',
    'masld-masld-정밀검사': '/지방간-정밀검사/',
    'masld-masld-음식': '/지방간-음식/',
    'viral-hbv-재활성화': '/B형간염-재활성화/',
    # pilot fragments
    '절제술-vs-색전술-vs-방사선': '/간암-치료-선택/',
    'b형간염-검사-결과지-해석hbsag-hbeag-anti-hbs-각각-무엇을-뜻하나요': '/B형간염-검사결과/',
    '지방간-진단-후-섬유화-정밀검사가-필요한-사람은-누구인가': '/지방간-정밀검사/',
    '식도정맥류': '/간경변-식도정맥류/',
    'fibroscan-간섬유화-스캔-수치-읽는-법': '/간섬유화스캔-수치/',
    '자가면역간염-aih-진단': '/자가면역간염-진단/',
    '간-양성종양-진단': '/간양성종양-진단/',
}


def parse_detail_filename(name: str):
    """d###-cat-slug-{top|lower}.webp → (slug, kind)"""
    m = re.match(r'd\d+-([^-]+)-(.+)-(top|lower)\.webp', name)
    if not m:
        return None, None
    cat, slug, kind = m.groups()
    return f'{cat}-{slug}', kind


def parse_pilot_filename(name: str):
    """pilot-##-cat-slug-{top|lower}.webp → (slug, kind)"""
    m = re.match(r'pilot-\d+-[^-]+-(.+)-(top|lower)\.webp', name)
    if not m:
        return None, None
    slug, kind = m.groups()
    return slug, kind


mapping: dict[str, dict] = {}

for f in sorted(V2_DETAIL.iterdir()):
    slug, kind = parse_detail_filename(f.name)
    if slug is None:
        print(f'SKIP unparseable: {f.name}')
        continue
    if slug not in SLUG_TO_URL:
        print(f'SKIP no URL for slug: {slug}')
        continue
    url = SLUG_TO_URL[slug]
    mapping.setdefault(url, {})[kind] = f'/assets/img/page-generated-v2/detail/{f.name}'

for f in sorted(V2_PILOT.iterdir()):
    slug, kind = parse_pilot_filename(f.name)
    if slug is None:
        print(f'SKIP unparseable: {f.name}')
        continue
    if slug not in SLUG_TO_URL:
        print(f'SKIP no URL for pilot slug: {slug}')
        continue
    url = SLUG_TO_URL[slug]
    # Pilot images override detail (higher quality)
    mapping.setdefault(url, {})[kind] = f'/assets/img/page-generated-v2/pilot/{f.name}'

# Filter to entries that have BOTH top and lower (or at least top)
final = {}
for url, kinds in mapping.items():
    if 'top' not in kinds:
        print(f'NO TOP for {url} — skipping')
        continue
    final[url] = {
        'top': kinds['top'],
        'lower': kinds.get('lower'),  # may be None
    }

with open(ROOT / '.tools/page_image_mapping_v2.json', 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print(f'\nFinal v2 mapping: {len(final)} URLs')
for url, info in sorted(final.items()):
    lower_status = 'OK' if info['lower'] else 'MISSING'
    print(f'  {url}: top OK, lower {lower_status}')
