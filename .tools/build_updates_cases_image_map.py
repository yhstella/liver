#!/usr/bin/env python3
"""Build image mapping for /updates/ and /케이스/ pages by reusing detail page images."""
import json, pathlib, re, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
with open(ROOT / '.tools/page_image_mapping_v2.json', encoding='utf-8') as f:
    base = json.load(f)


# Slug fragments (exact match) for direct detail pages
slug_to_detail = {
    # most cases will match via keyword rules; this dict is for full-exact case names if needed
}

# Keyword regex rules: ordered (first match wins)
keyword_rules = [
    # HCC related
    (r'BCLC.?A.?다발|BCLC.?A.?소작', '/간암-소작술-RFA-MWA/'),
    (r'BCLC.?A.?절제|단일3cm', '/간암-치료-선택/'),
    (r'BCLC.?B.?다발|TACE', '/간암-TACE-종류-결정/'),
    # adjuvant 시험은 면역치료 검색어보다 먼저 매칭되어야 함 (atezo-bev 키워드가 겹치기 때문)
    (r'IMbrave050|adjuvant.?atezo|Shin.?CIK', '/간암-재발-추적/'),
    (r'면역치료.?1차|atezo.?bev|AtezoBev|문맥침범', '/간암-면역치료-1차/'),
    (r'STRIDE|durvalumab|tremelimumab|HIMALAYA', '/간암-면역치료-1차/'),
    (r'CheckMate.?9DW|nivo.?ipi', '/간암-면역치료-1차/'),
    (r'IMbrave150', '/간암-면역치료-1차/'),
    (r'EMERALD|LEAP.?012', '/간암-TACE-종류-결정/'),
    (r'HCC.?폐전이|HCC.?림프절|혈관침범', '/간암-혈관침범-치료/'),
    (r'다운스테이징|ChildB|ChildC|이식대기|단일4cm.?이식', '/간암-간이식/'),
    (r'절제후.*재발|소작후.*재발|간기능회복.?재절제|재절제|단일결절', '/간암-재발-추적/'),
    (r'SBRT|양성자', '/간암-SBRT-양성자/'),
    (r'TACE.?SBRT|큰종양.?결합', '/간암-혈관침범-치료/'),
    (r'AFP.?상승|영상음성', '/알파태아단백/'),
    (r'PIVKAII|PIVKA.?II.?와파린|와파린.?위양성', '/PIVKA-II-간암마커/'),
    (r'우연발견.?결절|1cm결절|건강검진.?결절', '/간암-진단-첫외래/'),
    (r'LR3|LR4|모호결절|결절.?추적', '/간암-진단-첫외래/'),
    (r'B형간염.?검진.?새결절|간경변.?새결절', '/B형간염-간암검진/'),
    # AIH
    (r'AIH.?급성|자가면역.?급성', '/자가면역간염-급성간부전/'),
    (r'AIH.?임신|AIH.?약물전환', '/자가면역간염-임신/'),
    (r'AIH.?소아|AIH.?청소년', '/자가면역간염-소아청소년/'),
    (r'스테로이드.?당뇨|AIH.?스테로이드', '/자가면역간염-스테로이드-부작용/'),
    (r'AIH.?PBC|PBC.?overlap', '/자가면역간염-PBC-overlap/'),
    (r'AIH.?약중단|약중단.?재발', '/자가면역간염-약중단/'),
    (r'AIH.?첫진단|자가면역간염.?첫진단', '/자가면역간염-진단/'),
    (r'AIH', '/자가면역간염-진단/'),
    # HBV
    (r'B형간염.?소아|B형간염.?청소년.?치료시작', '/B형간염-소아청소년-치료/'),
    (r'B형간염.?HDV|HDV.?동반', '/B형간염-D형간염-HDV/'),
    (r'B형간염.?Occult|Occult.?항암', '/B형간염-Occult-잠복감염/'),
    (r'B형간염.?수술전|수술전.?예방|항암치료전.?재활성화|재활성화.?예방', '/B형간염-재활성화/'),
    (r'B형간염.?신기능|신기능저하.?TAF', '/B형간염-신기능-약물선택/'),
    (r'HBeAg.?seroclearance|HBeAg.?약중단', '/B형간염-HBeAg-양성-음성/'),
    (r'ETV.?TAF|ETV-TAF-전환|Shin.?ETV|Shin.?TAF', '/B형간염-항바이러스제-비교/'),
    (r'임신중.?HBsAg|HBsAg.?발견', '/B형간염-결혼-임신/'),
    (r'직장검진.?HBsAg', '/B형간염-검사결과/'),
    (r'Bepirovirsen', '/B형간염-functional-cure/'),
    (r'Pan-TDF.?pregnancy|TDF.?pregnancy', '/B형간염-결혼-임신/'),
    (r'Shin.?HBeAg', '/B형간염-HBeAg-양성-음성/'),
    # HCV
    (r'C형간염.?DAA실패|DAA실패.?재치료', '/C형간염-DAA-실패-재치료/'),
    (r'C형간염.?HIV|HIV동반.?동시', '/C형간염-HIV-동반/'),
    (r'C형간염.?혈액투석|투석.?치료', '/C형간염-신부전-치료/'),
    (r'C형간염.?임신', '/C형간염-임신수유/'),
    (r'C형간염.?재감염', '/C형간염-재감염-위험군/'),
    (r'anti-HCV.?양성', '/C형간염-진단/'),
    (r'C형간염.?간경변', '/C형간염-완치후-추적/'),
    # Cirrhosis
    (r'반복SBP|SBP.?예방|복수.?SBP', '/간경변-감염-SBP-예방/'),
    (r'식도정맥류.?출혈|첫.?식도정맥류|preemptive-TIPS|TIPS', '/간경변-식도정맥류/'),
    (r'간성혼수', '/간경변-간성혼수/'),
    (r'Recompensation|바이러스억제후|recompensation', '/간경변-대상성-비대상성/'),
    (r'저나트륨|tolvaptan|복수', '/간경변-복수/'),
    (r'혈소판저하|romiplostim', '/간경변-혈소판감소/'),
    (r'Sarcopenia|근감소|영양', '/간경변-영양-근감소증/'),
    (r'Baveno', '/간경변-식도정맥류/'),
    # MASLD/MASH
    (r'MASH.?F3|MASH.?당뇨|MASH.?종합', '/지방간염-MASH/'),
    (r'MASLD.?F2|MASLD.?GLP1', '/지방간-SGLT2-GLP1/'),
    (r'MASLD.?HCC|MASLD.?비만당뇨', '/지방간-간암/'),
    (r'MASLD.?비만수술', '/지방간-비만수술/'),
    (r'MASLD.?수면|CPAP', '/지방간-수면무호흡-OSA/'),
    (r'MASLD.?심혈관', '/지방간-심혈관-CVD/'),
    (r'MASLD.?청소년|MASLD.?가족력', '/지방간-소아청소년-MASLD/'),
    (r'MetALD|당뇨.?음주', '/지방간-MetALD/'),
    (r'lean-MASLD|lean.?MASLD', '/지방간-lean-MASLD/'),
    (r'resmetirom', '/지방간-신약-resmetirom/'),
    (r'MAESTRO', '/지방간-신약-resmetirom/'),
    (r'ESSENCE|survodutide|Newsome.?semaglutide|semaglutide.?NASH', '/지방간염-MASH/'),
    (r'orforglipron|GLP1RA.?small', '/지방간-SGLT2-GLP1/'),
    (r'MASLD-nomenclature|nomenclature', '/대사이상지방간-MASLD/'),
    (r'검진ALT.?MASLD|ALT상승.?MASLD', '/대사이상지방간-MASLD/'),
    (r'Chung-SGLT2', '/지방간-SGLT2-GLP1/'),
    (r'Ahn-Aspirin', '/지방간-간암/'),
    # Alcohol
    (r'Klausen|Semaglutide.?AUD|GLP1RA.?ALD|GLP1RA.?알코올|알코올.?간질환|PEth', '/알코올성-간질환/'),
    # DILI / LFT
    (r'약물성|독성간염|항결핵|보충제.?ALT|야생버섯', '/약물성-간손상-DILI/'),
    (r'AST우세|근육질환', '/간수치-AST-우세-원인/'),
    (r'ALT일과성.?운동|격렬한운동', '/간수치-운동후-상승/'),
    (r'임신중.?ALT', '/간수치-임신중-변화/'),
    (r'소아청소년.?ALT|청소년.?ALT|소아청소년.?검진', '/간수치-소아청소년-기준/'),
    (r'만성경증ALT|원인불명', '/간수치-높음/'),
    (r'검진ALT.?원인|검진ALT상승.?원인', '/간수치-검진주기-결정/'),
    # Benign
    (r'경구피임약.?HCA|HCA의심', '/간양성종양-경구피임약/'),
    (r'NRH', '/간양성종양-NRH/'),
    (r'bile-duct-hamartoma|담관과오종', '/간양성종양-담관과오종/'),
    (r'focal-fat|국소.?지방|focal.?sparing', '/간양성종양-국소지방-변화/'),
    (r'큰낭종|bleomycin|경화요법', '/간양성종양-낭종-관리/'),
    (r'혈관종.?확대|임신중.?혈관종', '/간양성종양-임신중/'),
    # Shin et al 논문 — 주제별 분리
    # Shin-CIK는 면역치료(adjuvant)이므로 위쪽 IMbrave050 그룹에서 이미 처리
    (r'Shin.?COVID.?HBV', '/B형간염-검사결과/'),
    (r'Shin.?HCC-Guidelines', '/간암-BCLC병기/'),
    (r'Shin.?Antiviral.?CV', '/B형간염-항바이러스제-비교/'),
    (r'Shin.?AI.?CT', '/알파태아단백/'),
    (r'AI.?CT.?HCC.?validation', '/알파태아단백/'),
]


def find_match(slug):
    for s, url in slug_to_detail.items():
        if s == slug:
            return url
    for pat, url in keyword_rules:
        if re.search(pat, slug, re.IGNORECASE):
            return url
    return None


# Process updates
updates_map = {}
unmatched_updates = []
for d in sorted(os.listdir(ROOT / 'updates')):
    full = ROOT / 'updates' / d
    if not full.is_dir():
        continue
    if not (full / 'index.html').exists():
        continue
    match = find_match(d)
    if match:
        updates_map[f'/updates/{d}/'] = match
    else:
        unmatched_updates.append(d)

# Process cases
cases_map = {}
unmatched_cases = []
for d in sorted(os.listdir(ROOT / '케이스')):
    full = ROOT / '케이스' / d
    if not full.is_dir():
        continue
    if not (full / 'index.html').exists():
        continue
    match = find_match(d)
    if match:
        cases_map[f'/케이스/{d}/'] = match
    else:
        unmatched_cases.append(d)

print(f'Updates: {len(updates_map)} matched, {len(unmatched_updates)} unmatched')
for u in unmatched_updates:
    print(f'  UNMATCHED: {u}')

print(f'\nCases: {len(cases_map)} matched, {len(unmatched_cases)} unmatched')
for u in unmatched_cases:
    print(f'  UNMATCHED: {u}')

# Combine into final map — but ONLY include if target detail page has v2 images
combined = {}
dropped = []
for url, target_url in {**updates_map, **cases_map}.items():
    if target_url in base:
        combined[url] = {
            'top': base[target_url]['top'],
            'lower': base[target_url].get('lower'),  # may be None
            'source': target_url,
        }
    else:
        dropped.append((url, target_url))

if dropped:
    print(f'\nDropped (target detail has no v2 image): {len(dropped)}')
    for u, t in dropped[:5]:
        print(f'  {u} → {t}')
    if len(dropped) > 5:
        print(f'  ... and {len(dropped)-5} more')

with open(ROOT / '.tools/updates_cases_image_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print(f'\nSaved {len(combined)} URL mappings to .tools/updates_cases_image_mapping.json')
