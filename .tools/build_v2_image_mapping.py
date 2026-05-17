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
    'viral-hbv-hcc검진': '/B형간염-간암검진/',
    'cirrhosis-cirrhosis-child-pugh-meld': '/간경변-Child-Pugh-MELD/',
    'viral-hcv-완치-daa': '/C형간염-완치-DAA/',
    'viral-hcv-완치후-추적': '/C형간염-완치후-추적/',
    'diagnostics-fibroscan-수치': '/간섬유화스캔-수치/',
    'masld-fibroscan-수치': '/간섬유화스캔-수치/',  # duplicate covering same URL
    'masld-masld-sglt2-glp1': '/지방간-SGLT2-GLP1/',
    'benign-benign-진단': '/간양성종양-진단/',
    'cirrhosis-cirrhosis-encephalopathy': '/간경변-간성혼수/',
    'cirrhosis-cirrhosis-간신증후군': '/간경변-간신증후군/',
    'hcc-hcc-소작술-rfa-mwa': '/간암-소작술-RFA-MWA/',
    'hcc-hcc-진단-첫외래': '/간암-진단-첫외래/',
    'hcc-hcc-transplant': '/간암-간이식/',
    'hcc-hcc-sbrt-양성자': '/간암-SBRT-양성자/',
    'hcc-hcc-tace-종류-결정': '/간암-TACE-종류-결정/',
    'hcc-hcc-면역치료-1차': '/간암-면역치료-1차/',
    'hcc-hcc-혈관침범-치료': '/간암-혈관침범-치료/',
    'cirrhosis-cirrhosis-ascites': '/간경변-복수/',
    'cirrhosis-cirrhosis-varices': '/간경변-식도정맥류/',
    'diagnostics-dili-간손상-dili': '/약물성-간손상-DILI/',
    'autoimmune-pbc-원발성담즙성담관염': '/PBC-원발성담즙성담관염/',
    'autoimmune-aih-진단': '/자가면역간염-진단/',
    'hcc-hcc-치료-선택': '/간암-치료-선택/',
    'masld-masld-신약-resmetirom': '/지방간-신약-resmetirom/',
    'masld-masld-정밀검사': '/지방간-정밀검사/',
    'masld-masld-음식': '/지방간-음식/',
    'viral-hbv-신기능-약물선택': '/B형간염-신기능-약물선택/',
    'viral-hbv-재활성화': '/B형간염-재활성화/',
    'diagnostics-pivka-ii-hcc마커': '/PIVKA-II-간암마커/',
    'hcc-hcc-재발-추적': '/간암-재발-추적/',
    'hcc-hcc-방사선색전술': '/간암-방사선색전술/',
    'masld-masld-hcc': '/지방간-간암/',
    'hcc-hcc-가족력-검진': '/간암-가족력-검진/',
    'cirrhosis-cirrhosis-영양-근감소증': '/간경변-영양-근감소증/',
    'cirrhosis-cirrhosis-약물-주의': '/간경변-약물-주의/',
    'cirrhosis-cirrhosis-혈소판감소': '/간경변-혈소판감소/',
    'cirrhosis-cirrhosis-감염-sbp-예방': '/간경변-감염-SBP-예방/',
    'cirrhosis-cirrhosis-transplant-평가': '/간경변-간이식-평가/',
    'cirrhosis-cirrhosis-대상성-비대상성': '/간경변-대상성-비대상성/',
    'cirrhosis-cirrhosis-수면-가려움증': '/간경변-수면-가려움증/',
    'cirrhosis-cirrhosis-여행-항공-주의': '/간경변-여행-항공-주의/',
    'cirrhosis-cirrhosis-피로감-증상관리': '/간경변-피로감-증상관리/',
    'hcc-hcc-식이-일상': '/간암-식이-일상/',
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
