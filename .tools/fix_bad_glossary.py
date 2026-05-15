#!/usr/bin/env python3
"""Fix wrong inline glossary expansions across all HTML pages.

Each entry: (search_pattern, replacement). String literal search/replace.
"""
import pathlib, subprocess, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Clear-cut errors: gloss is not the actual abbreviation expansion
REPLACEMENTS = [
    # PIVKA-II — partial/wrong glosses
    ('PIVKA-II(간세포암 표지자)', 'PIVKA-II'),
    ('PIVKA-II(또 다른 종양표지자)', 'PIVKA-II'),
    ('PIVKA-II(간경변·간암 위험군)', 'PIVKA-II'),

    # ALP / GGT — wrong genericized gloss
    ('ALP(담도 지표 효소)', 'ALP'),
    ('GGT(담도 지표 효소)', 'GGT'),
    ('ALP(담도)', 'ALP'),
    ('GGT(담도 막힘)', 'GGT'),
    ('GGT(담도 패턴)', 'GGT'),

    # AST / ALT — wrong description gloss
    ('AST(간세포 손상)', 'AST'),
    ('ALT(간세포 손상)', 'ALT'),
    ('ALT(간 손상 활동성)', 'ALT'),

    # EGD — wrong (EGD is the procedure, not a disease)
    ('EGD(간경변)', 'EGD'),

    # LDLT — partial, just "생체 기증" is not the expansion
    ('LDLT(생체 기증)', 'LDLT'),

    # SVR — partial gloss
    ('SVR(완치)', 'SVR'),

    # BCLC 병기 — redundant parenthetical
    ('BCLC 병기(간세포암 병기 분류)', 'BCLC 병기'),

    # RNA — context not abbreviation
    ('RNA(고위험군)', 'RNA'),
    ('RNA(재감염 의심 시)', 'RNA'),

    # DAA — drug examples, not expansion
    ('DAA(글레카프레비르 등)', 'DAA'),
    ('DAA(소포스부비르 함유)', 'DAA'),

    # MASH — description, not expansion
    ('MASH(염증·간세포 손상 동반)', 'MASH'),

    # BCAA — context, not expansion
    ('BCAA(간경변·근감소증)', 'BCAA'),

    # AFP — fragment of sentence, not expansion
    ('AFP(태반·태아 평가에서 설명되지 않는)', 'AFP'),

    # HCA spacing fix
    ('HCA(간세포선종)', 'HCA(간세포 선종)'),

    # MASLD — sentence fragment as gloss
    ('MASLD(체중 감량으로 호전)', 'MASLD'),

    # PT — wrong context glosses (PT = prothrombin time)
    ('PT(간 합성능)', 'PT'),
    ('PT(합성능)', 'PT'),

    # CBC — wrong, CBC is complete blood count
    ('CBC(빈혈·용혈)', 'CBC'),

    # HE — wrong, HE is hepatic encephalopathy
    ('HE(아주 경한 단계)', 'HE'),

    # LP — wrong, anti-SLA/LP had availability comment captured
    ('LP(가능 기관에서)', 'LP'),

    # HBV — wrong, HBV is the virus
    ('HBV(드물지만 가능)', 'HBV'),

    # CK spacing — 크레아틴키나아제 → 크레아틴 키나아제
    ('크레아틴키나아제(CK)', '크레아틴 키나아제(CK)'),
    ('CK(크레아틴키나아제)', 'CK(크레아틴 키나아제)'),

    # CAP — partial gloss "CAP(지방량)" — keep as is (지방량 describes what CAP shows)
    # Actually CAP is controlled attenuation parameter. (지방량) is context.
    # The instances are likely "CAP(지방량 측정 파라미터)" or similar. Leave for now.

    # CT — "필요 시" is "as needed" annotation, fine in some contexts but
    # not as a glossary. Specific known wrong: "CT(필요 시)" appearing
    # inline as abbreviation explanation. The instances I found were
    # "PET-CT(필요 시)" which clinically means CT as needed; leave those.
    # Skip for now.

    # MRI — "(가돌리늄 회피)" describes administration, not expansion.
    # Context "MRI(가돌리늄 회피)" in pregnant patients is legitimate
    # clinical shorthand. Leave but note.
]


def fix_file(path):
    text = path.read_text(encoding='utf-8')
    original = text
    changes = []
    for old, new in REPLACEMENTS:
        if old in text:
            count = text.count(old)
            text = text.replace(old, new)
            changes.append((old, new, count))
    if text != original:
        path.write_text(text, encoding='utf-8')
    return changes


# Find all HTML files with any of these patterns
result = subprocess.run(['git', 'grep', '-l', '-z', '-F', '|'.join(p[0] for p in REPLACEMENTS), '--', '*.html'],
                       capture_output=True)
# git grep -F with | won't union. Use simpler approach: iterate
search_terms = list(set(p[0] for p in REPLACEMENTS))
all_files = set()
for term in search_terms:
    r = subprocess.run(['git', 'grep', '-l', '-z', '-F', term, '--', '*.html'], capture_output=True)
    for f in r.stdout.split(b'\x00'):
        if f and f.endswith(b'.html'):
            all_files.add(f.decode('utf-8'))

print(f'Files to process: {len(all_files)}')

total_changes = 0
total_files = 0
for f in sorted(all_files):
    p = ROOT / f
    changes = fix_file(p)
    if changes:
        total_files += 1
        for old, new, count in changes:
            total_changes += count

print(f'Files modified: {total_files}')
print(f'Total replacements: {total_changes}')
