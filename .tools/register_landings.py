#!/usr/bin/env python3
"""Register new cases/CCs/updates in their landing pages + update series-meta counts."""
from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent

# ─── New cases by series (hub) ────────────────────────────────────────
NEW_CASES = {
    1: [  # 간암
        ('소작후-2년재발-단일결절', '소작 2년 후 같은 부위 재발'),
        ('AtezoBev-실패-2차치료', 'AtezoBev 실패 후 2차 치료'),
        ('LR4-결절-추적', 'LR-4 결절 추적'),
        ('HCC-림프절전이', 'HCC 림프절 전이'),
        ('간기능회복-재절제', '간 기능 회복 후 재절제'),
        ('HCC-폐전이-단독', 'HCC 단독 폐 결절(oligometastasis)'),
    ],
    2: [  # 간경화
        ('혈소판저하-romiplostim', '혈소판 25,000 — TPO 작용제로 치과 발치'),
        ('반복SBP-예방요법', '반복 SBP — 평생 예방 항생제 + 이식 평가'),
        ('저나트륨혈증-tolvaptan', 'Na 124 — Tolvaptan으로 정상화'),
        ('Sarcopenia-운동개선', 'Sarcopenia 운동·영양 개선 12개월'),
        ('Recompensation-바이러스억제후', '비대상성 → 재대상화'),
    ],
    3: [  # B형간염
        ('B형간염-Occult-항암치료', 'R-CHOP 전 occult HBV 예방'),
        ('B형간염-신기능저하-TAF전환', 'TDF 10년 후 TAF 전환'),
        ('B형간염-HDV-동반', '빠른 진행에서 HDV 발견'),
        ('B형간염-소아청소년-치료시작', '16세 면역활동기 진입'),
        ('B형간염-수술전-예방', '신장이식 전 평생 예방'),
    ],
    4: [  # 지방간
        ('MASLD-청소년-가족력', '15세 학생 — 가족력 + 비만'),
        ('MASLD-수면무호흡-CPAP개선', 'OSA + MASLD — CPAP으로 ALT 호전'),
        ('MetALD-당뇨-음주', '당뇨 + 매일 소주 — MetALD'),
        ('MASLD-비만수술-회복', 'BMI 42 위소매절제 — MASH 호전'),
        ('MASLD-심혈관-종합관리', 'MASLD + 협심증 — Statin 시작'),
    ],
    5: [  # 간수치
        ('ALT일과성상승-격렬한운동', '마라톤 직후 AST 380'),
        ('임신중-ALT상승-감별', '임신 32주 ICP 진단'),
        ('소아청소년-검진ALT상승', '14세 ALT 35 — 소아 기준'),
        ('AST우세-근육질환배제', 'AST 250 — 다발성 근염'),
        ('만성경증ALT상승-원인불명', '3년 ALT 60대 — PNPLA3 변이'),
    ],
    6: [  # C형간염
        ('C형간염-DAA실패-재치료', '마비렛 실패 → 보세비 재치료'),
        ('C형간염-혈액투석-치료', '투석 환자 마비렛 8주'),
        ('C형간염-HIV동반-동시치료', 'HIV·HCV 동반 동시 치료'),
        ('C형간염-임신중-발견', '임신 8주 산전 검사에서 발견'),
        ('C형간염-재감염', 'DAA 완치 2년 후 재감염'),
    ],
    7: [  # 자가면역간염
        ('AIH-PBC-overlap-진단', 'ALT·ALP 동시 상승 + AMA·ANA — Overlap'),
        ('AIH-임신중-약물전환', 'MMF → AZA 임신 계획'),
        ('AIH-스테로이드-당뇨발생', 'Pred 6개월 — 스테로이드 유발 당뇨'),
        ('AIH-소아청소년-진단', '13세 소녀 ALT 600 — ASC overlap'),
        ('AIH-급성간부전', '급성 간부전으로 첫 진단'),
    ],
    8: [  # 간양성종양
        ('NRH-진단', 'SLE + AZA 10년 — NRH 발견'),
        ('임신중-혈관종확대', '임신 중 8→11cm 혈관종'),
        ('bile-duct-hamartoma-우연발견', '건강검진 다발성 결절 — 담관 과오종'),
        ('경구피임약-HCA의심', '피임약 8년 + 6cm HCA — 절제'),
        ('focal-fat-sparing-PET', 'PET 양성 — Focal sparing'),
    ],
}

# ─── New CCs (with group label) ───────────────────────────────────────
NEW_CCS = [
    ('잇몸-출혈-멍', '"잇몸에서 피가 나고 멍이 잘 들어요"',
     '응고 장애·간경변·혈소판 감소의 단서. PT/INR + 혈소판 + 알부민 검사로 평가합니다.'),
    ('다리부종', '"다리가 자꾸 붓고 양말 자국이 깊게 남아요"',
     '간경변·심부전·신증후군·정맥부전·갑상선 여러 원인. 양쪽 vs 한쪽으로 분기합니다.'),
    ('만성-가려움증', '"전신이 가려운데 발진은 없어요"',
     '담즙정체(PBC·PSC)·만성 신부전·갑상선·임신성 ICP 등 전신 원인을 시사합니다.'),
    ('거미혈관-수장홍반', '"가슴이나 얼굴에 거미줄 같은 혈관이 생겼어요"',
     '간경변의 흔한 피부 소견. 임신·갑상선·정상 변종 가능성도 함께 평가합니다.'),
    ('검은변-피섞임', '"검은 변이 나오거나 토할 때 피가 섞여요"',
     '위장관 출혈 응급 신호. 정맥류·궤양 등을 즉시 평가해야 합니다.'),
]

# ─── New Updates ──────────────────────────────────────────────────────
NEW_UPDATES = [
    ('EMERALD-1-TACE-durva-bev-Lancet-2024', 'EMERALD-1 — TACE + durva + bev', 'Lancet 2024'),
    ('CheckMate-9DW-nivo-ipi-Lancet-2024', 'CheckMate 9DW — Nivolumab + Ipilimumab 1차', 'Lancet 2024'),
    ('LEAP-012-TACE-pembro-lenva-Lancet-2024', 'LEAP-012 — TACE + Pembro + Lenva', 'Lancet 2024'),
    ('ESSENCE-survodutide-MASH-Lancet-2024', 'Survodutide — GLP-1/Glucagon 이중 작용제', 'Lancet 2024'),
    ('MASLD-nomenclature-AASLD-EASL-2023', 'MASLD 새 명명', 'Hepatology 2023'),
    ('Bepirovirsen-HBV-Lancet-2024', 'Bepirovirsen — B형간염 functional cure ASO', 'Lancet 2024'),
    ('MAESTRO-NASH-resmetirom-3년-2024', 'Resmetirom 3년 추적', 'Hepatology 2024'),
    ('Baveno-VII-recompensation-2024', 'Baveno VII — 재대상화 정의', 'J Hepatol 2022/2024'),
    ('AI-CT-HCC-validation-Hepatology-2024', 'AI CT HCC 진단 다기관 검증', 'Hepatology 2024'),
    ('IMbrave050-adjuvant-atezo-bev-Lancet-2023', 'IMbrave050 — 절제 후 보조 면역치료', 'Lancet 2023'),
]


def case_row_html(slug: str, page_id: str, title: str) -> str:
    return (
        f'\n<a href="/케이스/{quote(slug, safe="")}/" class="case-row">'
        f'<span class="page-id">{page_id}</span>'
        f'<div class="body"><h3>{title}</h3></div></a>'
    )


def update_cases_landing():
    p = ROOT / '케이스' / 'index.html'
    text = p.read_text(encoding='utf-8')
    n_added = 0
    for series, cases in NEW_CASES.items():
        # find this section's case-list
        pattern = re.compile(
            r'(<section[^>]+data-series="' + str(series) + r'"[^>]*>.*?<div class="case-list"[^>]*>.*?)(</div></section>)',
            re.DOTALL,
        )
        m = pattern.search(text)
        if not m:
            print(f'  series {series} not found')
            continue
        section_html = m.group(1)
        # find max page-id within this section to continue numbering
        ids = re.findall(rf'<span class="page-id">{series}-(\d+)</span>', section_html)
        max_id = max([int(x) for x in ids], default=0)
        new_blocks = []
        for slug, title in cases:
            if f'/케이스/{slug}/' in section_html:
                continue
            max_id += 1
            new_blocks.append(case_row_html(slug, f'{series}-{max_id}', title))
            n_added += 1
        # Replace
        new_section = section_html + ''.join(new_blocks)
        text = text[:m.start()] + new_section + m.group(2) + text[m.end():]
        # Update count "N편" — count all case-row hrefs in this updated section
        count_re = re.compile(
            r'(<section[^>]+data-series="' + str(series) + r'"[^>]*>.*?<span style="font-size:12px;color:var\(--muted\);font-weight:400;margin-left:10px">)(\d+)편(</span>)',
            re.DOTALL,
        )
        m2 = count_re.search(text)
        if m2:
            section_for_count = re.search(
                r'<section[^>]+data-series="' + str(series) + r'"[^>]*>(.*?)</section>',
                text, re.DOTALL,
            )
            n_cases_now = len(re.findall(r'class="case-row"', section_for_count.group(1)))
            text = text[:m2.start(2)] + str(n_cases_now) + text[m2.end(2):]
    p.write_text(text, encoding='utf-8')
    print(f'  cases landing: +{n_added} entries')


def update_cc_landing():
    p = ROOT / 'CC' / 'index.html'
    text = p.read_text(encoding='utf-8')
    # Add new group at end of cc-list (before its closing </div>)
    pattern = re.compile(r'(<div class="cc-list">.*?)(</div>\s*</main>)', re.DOTALL)
    m = pattern.search(text)
    if not m:
        print('  cc-list close not found')
        return
    block = '\n<span class="cc-group-label">신체 소견·출혈·증상</span>\n'
    n = 0
    for slug, cite, summary in NEW_CCS:
        if f'/CC/{slug}/' in text:
            continue
        block += (
            f'<a href="/CC/{quote(slug, safe="")}/" class="cc-row">'
            f'<div class="cc-cite">{cite}</div>'
            f'<p class="cc-sum">{summary}</p></a>\n'
        )
        n += 1
    new_text = text[:m.start()] + m.group(1) + block + m.group(2) + text[m.end():]
    p.write_text(new_text, encoding='utf-8')
    print(f'  CC landing: +{n} entries')


def update_updates_landing():
    p = ROOT / 'updates' / 'index.html'
    text = p.read_text(encoding='utf-8')
    # The updates landing structure varies; look for body main content
    # Try simple approach: find <ul class="topic-list"> or similar, or just check existing pattern
    # If empty-state exists, replace with cards listing
    # Otherwise append before </main>
    block_items = []
    for slug, title, journal in NEW_UPDATES:
        if f'/updates/{slug}/' in text:
            continue
        block_items.append(
            f'  <li><a href="/updates/{quote(slug, safe="")}/" style="display:block;padding:14px 18px;border:1px solid var(--line);border-radius:8px;text-decoration:none;color:var(--fg);margin-bottom:10px">'
            f'<strong style="color:var(--accent);font-size:11px;letter-spacing:0.06em;text-transform:uppercase;display:block;margin-bottom:2px">{journal}</strong>'
            f'<span style="font-size:15px;font-weight:600">{title}</span>'
            f'</a></li>'
        )
    if not block_items:
        print('  updates: nothing new')
        return
    block = '<ul class="updates-list" style="list-style:none;padding:0;margin:24px 0">\n' + '\n'.join(block_items) + '\n</ul>'
    # Try to remove empty-state if present and insert
    if 'class="empty-state"' in text:
        text = re.sub(
            r'<div class="empty-state">.*?</div>',
            block,
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        text = text.replace('</main>', block + '\n</main>', 1)
    p.write_text(text, encoding='utf-8')
    print(f'  updates landing: +{len(block_items)} entries')


def update_hub_series_meta():
    """Update series-meta on each hub to reflect current detail/case counts."""
    HUBS = ['간암', '간경화', 'B형간염', 'C형간염', '지방간', '간수치', '자가면역간염', '간양성종양']
    SERIES_OF = {'간암':1,'간경화':2,'B형간염':3,'지방간':4,'간수치':5,'C형간염':6,'자가면역간염':7,'간양성종양':8}
    case_landing = (ROOT / '케이스' / 'index.html').read_text(encoding='utf-8')
    for hub in HUBS:
        p = ROOT / hub / 'index.html'
        text = p.read_text(encoding='utf-8')
        # count detail entries in this hub's topic-list
        m = re.search(r'<ul class="topic-list">(.*?)</ul>', text, re.DOTALL)
        if not m:
            continue
        n_detail = len(re.findall(r'<li class="published">', m.group(1)))
        # count cases in landing for this series
        series = SERIES_OF.get(hub)
        n_cases = 0
        if series:
            sec_m = re.search(
                rf'<section[^>]+data-series="{series}"[^>]*>(.*?)</section>',
                case_landing, re.DOTALL,
            )
            if sec_m:
                n_cases = len(re.findall(r'class="case-row"', sec_m.group(1)))
        # Update series-meta line
        new_text = re.sub(
            r'<div class="series-meta">\s*<span>세부주제\s*\d+편\s*[·\s]*\d+편?\s*</span>(?:<span>[^<]*</span>)?\s*</div>',
            f'<div class="series-meta"><span>세부주제 {n_detail}편 · 사례 {n_cases}편</span></div>',
            text,
            count=1,
        )
        # Also handle single-span format
        new_text = re.sub(
            r'<div class="series-meta"><span>세부주제\s*\d+편\s*·\s*사례\s*\d+편</span></div>',
            f'<div class="series-meta"><span>세부주제 {n_detail}편 · 사례 {n_cases}편</span></div>',
            new_text,
            count=1,
        )
        # Two-span format
        new_text = re.sub(
            r'<div class="series-meta">\s*<span>세부주제\s*\d+편</span>\s*<span>·\s*케이스\s*\d+편</span>\s*</div>',
            f'<div class="series-meta"><span>세부주제 {n_detail}편 · 사례 {n_cases}편</span></div>',
            new_text,
            count=1,
            flags=re.DOTALL,
        )
        if new_text != text:
            p.write_text(new_text, encoding='utf-8')
            print(f'  {hub}: series-meta → {n_detail}편 · {n_cases}편')


def main():
    print('=== updating landing pages ===')
    update_cases_landing()
    update_cc_landing()
    update_updates_landing()
    print('\n=== updating hub series-meta ===')
    update_hub_series_meta()


if __name__ == '__main__':
    main()
