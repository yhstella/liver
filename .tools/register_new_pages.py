#!/usr/bin/env python3
"""Register new detail/case/CC/update pages in their landing pages."""
from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent

# ─── New detail pages by hub ──────────────────────────────────────────
HUB_ENTRIES = {
    '간암': [
        ('간암-소작술-RFA-MWA', '간암 소작술 — RFA와 MWA', '3cm 이하 단일 간암의 비절제 옵션, 두 방식의 차이'),
        ('간암-TACE-종류-결정', 'TACE — cTACE와 DEB-TACE', '중간기 간암의 표준, 두 색전 방식 비교'),
        ('간암-SBRT-양성자', 'SBRT와 양성자 치료', '비침습 정밀 방사선 — 절제·소작이 어려운 위치의 대안'),
        ('간암-혈관침범-치료', '혈관 침범 동반 간암의 치료', '문맥·간정맥 침범 시 면역치료·SBRT·국소 치료'),
        ('간암-가족력-검진', '가족력 있는 사람의 간암 검진', '본인 위험 평가와 검진 시점·주기'),
    ],
    '간경화': [
        ('간경변-혈소판감소', '혈소판 감소와 시술 결정', '비장 비대·TPO 작용제 사용 시점'),
        ('간경변-감염-SBP-예방', 'SBP 예방 항생제', '복수 환자의 평생 norfloxacin 예방'),
        ('간경변-피로감-증상관리', '만성 피로감 — 원인 평가', '빈혈·잠재성 간성혼수·근감소증 등 다중 원인'),
        ('간경변-수면-가려움증', '수면 장애와 가려움증', '두 가지 흔한 비특이 증상의 단계적 약물'),
        ('간경변-여행-항공-주의', '여행과 항공기 탑승', '비대상성 환자의 안전한 여행 준비'),
    ],
    'B형간염': [
        ('B형간염-Occult-잠복감염', 'Occult HBV — 잠복 감염', 'HBsAg 음성·anti-HBc 양성, 항암 전 평가'),
        ('B형간염-소아청소년-치료', '소아·청소년 B형간염', '면역관용기에서 활동기로의 전환, 치료 시점'),
        ('B형간염-D형간염-HDV', 'D형간염(HDV) 동반', '가장 빠른 간경변 진행 원인 + bulevirtide'),
        ('B형간염-신기능-약물선택', '신기능 저하 환자의 약물', 'CKD·투석에서 TAF·entecavir 선호'),
        ('B형간염-수술전-예방', '수술·면역억제 전 예방', 'Rituximab·항암 전 항바이러스제 단기 예방'),
    ],
    'C형간염': [
        ('C형간염-재감염-위험군', 'DAA 완치 후 재감염', '위험 행동 지속 환자의 1년 RNA 추적'),
        ('C형간염-신부전-치료', '신부전·투석 환자 치료', '글레카프레비르/피브렌타스비르 1차'),
        ('C형간염-임신수유', '임신·수유와 C형간염', '임신 전 완치 권장, 수직감염 약 5~6%'),
        ('C형간염-HIV-동반', 'HIV·HCV 동반 감염', 'DAA + ART 약물 상호작용 평가'),
        ('C형간염-DAA-실패-재치료', 'DAA 1차 실패 후 재치료', '보세비(SOF/VEL/VOX) 12주 표준'),
    ],
    '지방간': [
        ('지방간-소아청소년-MASLD', '소아·청소년 MASLD', '한국에서 늘고 있는 진단, 가족 단위 개입'),
        ('지방간-수면무호흡-OSA', '수면 무호흡(OSA)과 지방간', 'CPAP·체중 감량의 양방향 효과'),
        ('지방간-MetALD', 'MetALD — 대사 + 알코올 동반', '두 원인 동시 관리'),
        ('지방간-심혈관-CVD', '지방간과 심혈관 질환', 'MASLD 환자의 가장 흔한 사망 원인은 심혈관'),
        ('지방간-비만수술', '비만 수술과 MASH 호전', '고도 비만 + MASH의 가장 강력한 옵션'),
    ],
    '간수치': [
        ('간수치-운동후-상승', '격렬한 운동 후 AST·ALT 상승', '근육 기원 — 1주 휴식 후 재검'),
        ('간수치-임신중-변화', '임신 중 간수치', 'ALP 자연 상승, ALT·총담즙산 변화는 의심'),
        ('간수치-검진주기-결정', '검진 주기 — 위험 인자별', '일반인 1~2년, B/C형·간경변 6개월'),
        ('간수치-소아청소년-기준', '소아·청소년 정상 범위', '성인보다 낮은 상한 — MASLD 조기 발견'),
        ('간수치-AST-우세-원인', 'AST > ALT 패턴의 원인', '알코올·근육·진행 섬유화·Wilson'),
    ],
    '자가면역간염': [
        ('자가면역간염-PBC-overlap', 'AIH·PBC overlap 증후군', 'Paris criteria + UDCA + 면역억제 병합'),
        ('자가면역간염-임신', 'AIH와 임신', 'AZA 유지, MMF 금기, 산후 30~50% 재발'),
        ('자가면역간염-스테로이드-부작용', '스테로이드 부작용 관리', 'Budesonide 전환과 모니터 일정'),
        ('자가면역간염-소아청소년', '소아·청소년 AIH', 'ASC overlap이 흔함, MRCP 필수'),
        ('자가면역간염-급성간부전', '급성 발현 AIH', '빠른 면역억제 + 이식 평가 동시 진행'),
    ],
    '간양성종양': [
        ('간양성종양-담관과오종', '담관 과오종(Von Meyenburg)', '다발 작은 양성 결절, MRCP로 진단'),
        ('간양성종양-국소지방-변화', 'Focal fat sparing/deposition', '종양으로 오해되는 영상 변종'),
        ('간양성종양-NRH', '결절성 재생 과형성(NRH)', '자가면역·약물·혈관 질환 — 비간경변성 문맥압 항진'),
        ('간양성종양-임신중', '임신 중 양성종양', '혈관종·HCA의 변화와 출혈 위험'),
        ('간양성종양-경구피임약', '경구피임약과 HCA', '5년 이상 사용 시 위험 의미 있게 상승'),
    ],
}

# ─── New cases ─────────────────────────────────────────────────────────
NEW_CASES = [
    # 간암 hub cases
    ('소작후-2년재발-단일결절', '소작 2년 후 같은 부위 재발', '간암'),
    ('AtezoBev-실패-2차치료', 'AtezoBev 실패 후 2차 치료', '간암'),
    ('LR4-결절-추적', 'LR-4 결절 추적', '간암'),
    ('HCC-림프절전이', 'HCC 림프절 전이', '간암'),
    ('간기능회복-재절제', '간 기능 회복 후 재절제', '간암'),
    ('HCC-폐전이-단독', 'HCC 단독 폐 결절(oligometastasis)', '간암'),
    # 간경화
    ('혈소판저하-romiplostim', '혈소판 25,000 — TPO 작용제로 치과 발치', '간경화'),
    ('반복SBP-예방요법', '반복 SBP — 평생 예방 항생제 + 이식 평가', '간경화'),
    ('저나트륨혈증-tolvaptan', 'Na 124 — Tolvaptan으로 정상화', '간경화'),
    ('Sarcopenia-운동개selen', 'Sarcopenia 운동·영양 개선 12개월', '간경화'),
    ('Sarcopenia-운동개선', 'Sarcopenia 운동·영양 개선 12개월', '간경화'),
    ('Recompensation-바이러스억제후', '비대상성 → 재대상화', '간경화'),
    # B형간염
    ('B형간염-Occult-항암치료', 'R-CHOP 전 occult HBV 예방', 'B형간염'),
    ('B형간염-신기능저하-TAF전환', 'TDF 10년 후 TAF 전환', 'B형간염'),
    ('B형간염-HDV-동반', '빠른 진행에서 HDV 발견', 'B형간염'),
    ('B형간염-소아청소년-치료시작', '16세 면역활동기 진입', 'B형간염'),
    ('B형간염-수술전-예방', '신장이식 전 평생 예방', 'B형간염'),
    # C형간염
    ('C형간염-DAA실패-재치료', '마비렛 실패 → 보세비 재치료', 'C형간염'),
    ('C형간염-혈액투석-치료', '투석 환자 마비렛 8주', 'C형간염'),
    ('C형간염-HIV동반-동시치료', 'HIV·HCV 동반 동시 치료', 'C형간염'),
    ('C형간염-임신중-발견', '임신 8주 산전 검사에서 발견', 'C형간염'),
    ('C형간염-재감염', 'DAA 완치 2년 후 재감염', 'C형간염'),
    # MASLD
    ('MASLD-청소년-가족력', '15세 학생 — 가족력 + 비만', '지방간'),
    ('MASLD-수면무호흡-CPAP개선', 'OSA + MASLD — CPAP으로 ALT 호전', '지방간'),
    ('MetALD-당뇨-음주', '당뇨 + 매일 소주 — MetALD', '지방간'),
    ('MASLD-비만수술-회복', 'BMI 42 위소매절제 — MASH 호전', '지방간'),
    ('MASLD-심혈관-종합관리', 'MASLD + 협심증 — Statin 시작', '지방간'),
    # 간수치
    ('ALT일과성상승-격렬한운동', '마라톤 직후 AST 380', '간수치'),
    ('임신중-ALT상승-감별', '임신 32주 ICP 진단', '간수치'),
    ('소아청소년-검진ALT상승', '14세 ALT 35 — 소아 기준', '간수치'),
    ('AST우세-근육질환배제', 'AST 250 — 다발성 근염', '간수치'),
    ('만성경증ALT상승-원인불명', '3년 ALT 60대 — PNPLA3 변이', '간수치'),
    # AIH
    ('AIH-PBC-overlap-진단', 'ALT·ALP 동시 상승 + AMA·ANA — Overlap', '자가면역간염'),
    ('AIH-임신중-약물전환', 'MMF → AZA 임신 계획', '자가면역간염'),
    ('AIH-스테로이드-당뇨발생', 'Pred 6개월 — 스테로이드 유발 당뇨', '자가면역간염'),
    ('AIH-소아청소년-진단', '13세 소녀 ALT 600 — ASC overlap', '자가면역간염'),
    ('AIH-급성간부전', '급성 간부전으로 첫 진단', '자가면역간염'),
    # 간양성종양
    ('NRH-진단', 'SLE + AZA 10년 — NRH 발견', '간양성종양'),
    ('임신중-혈관종확대', '임신 중 8→11cm 혈관종', '간양성종양'),
    ('bile-duct-hamartoma-우연발견', '건강검진 다발성 결절 — 담관 과오종', '간양성종양'),
    ('경구피임약-HCA의심', '피임약 8년 + 6cm HCA — 절제', '간양성종양'),
    ('focal-fat-sparing-PET', 'PET 양성 — Focal sparing', '간양성종양'),
]

# ─── New CCs ───────────────────────────────────────────────────────────
NEW_CCS = [
    ('잇몸-출혈-멍', '잇몸 출혈·잘 멍드는 증상'),
    ('다리부종', '양쪽 다리 부종'),
    ('만성-가려움증', '만성 가려움증'),
    ('거미혈관-수장홍반', '거미혈관·수장 홍반'),
    ('검은변-피섞임', '검은변·토혈'),
]

# ─── New Updates ──────────────────────────────────────────────────────
NEW_UPDATES = [
    ('EMERALD-1-TACE-durva-bev-Lancet-2024', 'EMERALD-1 — TACE + durva + bev (Lancet 2024)', 'BCLC B 표준 변화의 첫 양성 무작위 시험'),
    ('CheckMate-9DW-nivo-ipi-Lancet-2024', 'CheckMate 9DW — Nivo + Ipi 1차 (Lancet 2024)', '진행기 HCC 1차 면역치료 옵션 확대'),
    ('LEAP-012-TACE-pembro-lenva-Lancet-2024', 'LEAP-012 — TACE + Pembro + Lenva (Lancet 2024)', 'BCLC B 표준 변화의 두 번째 근거'),
    ('ESSENCE-survodutide-MASH-Lancet-2024', 'Survodutide — GLP-1/Glucagon 이중 작용제', 'MASH 2상에서 NASH·섬유화 호전'),
    ('MASLD-nomenclature-AASLD-EASL-2023', 'MASLD 새 명명 (AASLD/EASL 2023)', 'NAFLD/NASH → MASLD/MASH/MetALD'),
    ('Bepirovirsen-HBV-Lancet-2024', 'Bepirovirsen — HBV ASO (Lancet 2024)', 'B형간염 functional cure 첫 후보'),
    ('MAESTRO-NASH-resmetirom-3년-2024', 'Resmetirom 3년 추적', '첫 MASH 치료제의 장기 효과'),
    ('Baveno-VII-recompensation-2024', 'Baveno VII — 재대상화 정의', '비대상성 간경변의 재대상화 임상 기준'),
    ('AI-CT-HCC-validation-Hepatology-2024', 'AI CT HCC 진단 — 다기관 검증', '영상 전문의 수준 진단 정확도'),
    ('IMbrave050-adjuvant-atezo-bev-Lancet-2023', 'IMbrave050 — 절제 후 보조 면역치료', '간암 보조 면역치료 첫 양성 시험'),
]


def hub_entry_html(slug: str, title: str, desc: str) -> str:
    return (
        '  <li class="published">\n'
        f'    <a href="/{slug}/">\n'
        '      <div class="body">\n'
        f'        <h3>{title}</h3>\n'
        f'        <p>{desc}</p>\n'
        '      </div>\n'
        '      <span class="status published">읽기 →</span>\n'
        '    </a>\n'
        '  </li>'
    )


def add_entries_to_hub(hub_name: str, entries: list[tuple[str, str, str]]) -> int:
    p = ROOT / hub_name / 'index.html'
    text = p.read_text(encoding='utf-8')
    # Build new entries HTML
    blocks = []
    for slug, title, desc in entries:
        # skip if already present
        if f'href="/{slug}/"' in text:
            continue
        blocks.append(hub_entry_html(slug, title, desc))
    if not blocks:
        return 0
    new_block = '\n'.join(blocks) + '\n'
    # Insert before closing </ul> of first topic-list
    new_text = re.sub(
        r'(<ul class="topic-list">.*?)(</ul>)',
        lambda m: m.group(1) + new_block + m.group(2),
        text,
        count=1,
        flags=re.DOTALL,
    )
    if new_text == text:
        return 0
    p.write_text(new_text, encoding='utf-8')
    return len(blocks)


def main():
    total = 0
    for hub, entries in HUB_ENTRIES.items():
        n = add_entries_to_hub(hub, entries)
        print(f'  {hub}: +{n} entries')
        total += n
    print(f'\nadded {total} new detail entries to hub topic-lists')


if __name__ == '__main__':
    main()
