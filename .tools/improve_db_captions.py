#!/usr/bin/env python3
"""
improve_db_captions.py — Replace generic topic-level captions with
slug-specific captions reflecting the actual page topic.

Strategy: for every page with <!-- db-figure:auto:start --> block,
take the page's H1 (or slug) and use that as the caption seed
(instead of meaning_ko which is topic-generic).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK_START = '<!-- db-figure:auto:start -->'
MARK_END = '<!-- db-figure:auto:end -->'

# slug → caption (page-specific, short clinical description)
CAPTIONS = {
    '간경변-Child-Pugh-MELD': 'Child-Pugh와 MELD 점수의 구성 항목과 임상적 의미',
    '간경변-간성혼수': '간성혼수의 발생 메커니즘 — 암모니아·뇌 부종·치료 경로',
    '간경변-간신증후군': '간신증후군 — 간경변에서의 신기능 저하와 치료 흐름',
    '간경변-간이식-평가': '간이식 평가의 의학적·외과적 고려 사항',
    '간경변-감염-SBP-예방': '자발성 세균성 복막염(SBP) 예방과 치료 흐름',
    '간경변-대상성-비대상성': '대상성에서 비대상성 간경변으로의 진행과 합병증',
    '간경변-복수': '간경변 복수의 단계별 치료 — 식이·이뇨제·천자',
    '간경변-수면-가려움증': '간경변 환자의 수면·가려움증 — 흔한 비특이 증상의 원인과 대처',
    '간경변-식도정맥류': '식도정맥류 — 내시경 평가와 예방·치료',
    '간경변-약물-주의': '간경변에서 피해야 할 약물·영양제',
    '간경변-여행-항공-주의': '간경변 환자의 여행·항공기 탑승 시 안전 점검',
    '간경변-영양-근감소증': '근감소증과 영양 — 단백·열량 권고와 야식의 의미',
    '간경변-정상수치-함정': '간수치 정상이어도 간경변일 수 있는 상황',
    '간경변-피로감-증상관리': '간경변 환자의 만성 피로 — 원인 평가',
    '간경변-혈소판감소': '간경변에서의 혈소판 감소 — 비장 비대와 TPO 변화',
    '간생검-언제-필요한가': '간생검의 적응증과 시술 흐름',
    '간섬유화스캔-수치': 'Fibroscan(간섬유화 스캔) 수치 해석',
    '간수치-AST-우세-원인': 'AST 우세 상승 패턴 — 알코올·근육·진행 섬유화',
    '간수치-검진주기-결정': '간 검진 주기 결정 — 위험 인자별 권고',
    '간수치-높음': '검진 간수치 상승 — 첫 단계 평가',
    '간수치-소아청소년-기준': '소아·청소년 ALT 정상 범위 — 성인보다 낮음',
    '간수치-운동후-상승': '격렬한 운동 후 일시적 간수치 상승 — 근육 기원',
    '간수치-임신중-변화': '임신 중 간수치 정상 변화와 의심 패턴',
    '간수치-종류-차이': 'AST·ALT·GGT 세 효소의 출처와 패턴 차이',
    '간암-BCLC병기': '간세포암 BCLC 5단계와 표준 치료',
    '간암-SBRT-양성자': 'SBRT와 양성자 치료 — 비침습 정밀 방사선',
    '간암-TACE-종류-결정': 'cTACE와 DEB-TACE — 두 방식의 차이',
    '간암-가족력-검진': '가족력 있는 사람의 간암 검진 시점·주기',
    '간암-간이식': '간이식 평가와 Milan criteria',
    '간암-면역치료-1차': '1차 면역치료 — Atezolizumab + Bevacizumab',
    '간암-방사선색전술': 'TARE 방사선 색전술 — Y90 마이크로구',
    '간암-소작술-RFA-MWA': 'RFA와 MWA 소작술 — 작은 간암의 비절제 옵션',
    '간암-식이-일상': '간암 환자의 식이·일상 활동 권고',
    '간암-재발-추적': '간암 치료 후 재발 추적 일정',
    '간암-진단-첫외래': 'LI-RADS 영상 진단과 첫 외래 흐름',
    '간암-치료-선택': 'BCLC 단계별 표준 치료 알고리듬',
    '간암-혈관침범-치료': '혈관 침범(문맥·간정맥) 동반 간암의 치료 옵션',
    '간양성종양-FNH-Adenoma': 'FNH와 HCA — 영상으로 가르는 두 양성종양',
    '간양성종양-NRH': '결절성 재생 과형성(NRH) — 비간경변성 문맥압 항진의 원인',
    '간양성종양-경구피임약': '경구피임약과 HCA — 위험과 평가',
    '간양성종양-국소지방-변화': 'Focal fat sparing/deposition — 영상 변종',
    '간양성종양-낭종-관리': '간 낭종 — 단순 낭종의 추적과 시술 적응증',
    '간양성종양-담관과오종': '담관 과오종(Von Meyenburg complex) — 다발 작은 양성 결절',
    '간양성종양-임신중': '임신 중 양성종양의 변화 — 혈관종·HCA',
    '간양성종양-진단': '간 양성종양 진단 — 영상 패턴으로 가르는 4가지',
    '간양성종양-혈관종': '간 혈관종 — 동맥기 가장자리 결절 조영 패턴',
    'A형간염': 'A형 간염의 전파 경로와 진단·예방',
    'ALP-GGT-담도-간세포': 'ALP와 GGT — 담도 vs 간세포 손상의 패턴',
    'B형간염-D형간염-HDV': 'D형간염(HDV) — B형간염 동반 시 가장 빠른 간경변 진행',
    'B형간염-HBeAg-양성-음성': 'HBeAg 양성·음성의 임상적 의미',
    'B형간염-Occult-잠복감염': 'Occult HBV — HBsAg 음성이지만 cccDNA 잠복',
    'B형간염-functional-cure': 'B형간염 기능적 완치(HBsAg 소실)의 현재 위치',
    'B형간염-간암검진': 'B형간염 환자의 6개월 간암 검진',
    'B형간염-검사결과': 'B형간염 표지자 5개 — HBsAg, anti-HBs, HBeAg, anti-HBe, anti-HBc',
    'B형간염-결혼-임신': 'B형간염 환자의 결혼·임신·수유 안내',
    'B형간염-백신': 'B형간염 백신 — 접종 일정과 항체 확인',
    'B형간염-소아청소년-치료': '소아·청소년 만성 B형간염의 자연사와 치료',
    'B형간염-수술전-예방': '수술·면역억제 전 B형간염 평가와 예방',
    'B형간염-신기능-약물선택': '신기능 저하 환자의 항바이러스제 선택',
    'B형간염-재활성화': 'B형간염 재활성화 — 발생 위험과 예방',
    'B형간염-평생약': '평생 항바이러스제 복용의 의미와 결정',
    'B형간염-항바이러스제-비교': 'Entecavir·TDF·TAF 세 약물의 비교',
    'C형간염-DAA-실패-재치료': 'DAA 1차 실패 후 재치료 — 보세비(SOF/VEL/VOX)',
    'C형간염-HIV-동반': 'HIV·HCV 동반 — DAA와 ART 약물 상호작용',
    'C형간염-신부전-치료': '신부전·투석 환자의 C형간염 DAA 치료',
    'C형간염-완치-DAA': 'DAA로 C형간염 완치 — 8~12주 SVR12 도달',
    'C형간염-완치후-추적': 'SVR 후 평생 간암 검진 — 섬유화 단계별 결정',
    'C형간염-임신수유': '임신·수유와 C형간염 치료 시점',
    'C형간염-재감염-위험군': 'DAA 완치 후 재감염 — 위험군과 추적',
    'C형간염-진단': 'anti-HCV → HCV RNA(PCR)로 활동성 감염 확인',
    '대사이상지방간-MASLD': 'MASLD(대사이상지방간) — 진단과 자연사',
    '술-안마셔도-지방간': '술을 마시지 않는 사람의 지방간 — 대사 원인',
    '알부민-PT-간합성능': '알부민·PT(INR) — 간 합성능의 두 지표',
    '알코올성-간질환': '알코올성 간질환의 4단계 스펙트럼',
    '알파태아단백': 'AFP(알파태아단백) — 간암 종양표지자 해석',
    '약물성-간손상-DILI': '약물성 간 손상(DILI) — 약·영양제·한약',
    '자가면역간염-PBC-overlap': 'AIH-PBC overlap 증후군 — Paris criteria',
    '자가면역간염-급성간부전': '급성 발현 AIH — 즉시 면역억제 + 이식 평가',
    '자가면역간염-소아청소년': '소아·청소년 AIH — ASC overlap 흔함',
    '자가면역간염-스테로이드-부작용': '장기 스테로이드 사용의 부작용과 관리',
    '자가면역간염-약중단': 'AIH 약 중단 — 2년 안정 + 조직 호전 후 신중',
    '자가면역간염-임신': 'AIH 환자의 임신 — Azathioprine 유지, MMF 금기',
    '자가면역간염-진단': 'Simplified AIH Score (Hennes 2008) — 4축 진단',
    '자가면역간염-치료': 'AIH 표준 치료 — Prednisolone + Azathioprine',
    '지방간-MetALD': 'MetALD — 대사 위험 + 적당량 음주 동반',
    '지방간-SGLT2-GLP1': 'SGLT2·GLP-1 작용제와 지방간 호전',
    '지방간-lean-MASLD': 'Lean MASLD — 정상 BMI에서의 지방간',
    '지방간-간암': '지방간(MASLD)에서의 간세포암 위험',
    '지방간-비만수술': '비만 수술(bariatric)과 MASH 호전',
    '지방간-소아청소년-MASLD': '소아·청소년 MASLD — 한국에서 늘고 있는 진단',
    '지방간-수면무호흡-OSA': '수면 무호흡(OSA)과 지방간 — 양방향 악화',
    '지방간-신약-resmetirom': 'Resmetirom — 첫 MASH 치료제',
    '지방간-심혈관-CVD': 'MASLD 환자의 가장 흔한 사망 원인 — 심혈관 질환',
    '지방간-음식': '지방간에 좋은 음식·피해야 할 음식',
    '지방간-정밀검사': 'FIB-4 → Fibroscan → 생검의 단계별 평가',
    '지방간-치료': '체중 감량 5·7·10%의 효과 — 정량적 차이',
    '지방간-회복-6개월': '지방간 회복 — 6개월의 변화 패턴',
    '지방간염-MASH': '지방간염(MASH) — 풍선화·염증·섬유화 단계',
    'PIVKA-II-간암마커': 'PIVKA-II — AFP와의 보완 관계, 와파린 영향',
    '빌리루빈-직접-간접': '빌리루빈 직접·간접 분획 — 용혈·간세포성·담도성 패턴',
    '가족-B형간염-검사': '가족 중 B형간염 환자가 있을 때 받아야 할 검사 3가지',
}


def update_one(slug: str, path: Path) -> bool:
    cap = CAPTIONS.get(slug)
    if not cap:
        return False
    text = path.read_text(encoding='utf-8')
    if MARK_START not in text or MARK_END not in text:
        return False
    # Find figure block and replace alt + figcaption text
    import html as h
    safe_cap = h.escape(cap)
    block_re = re.compile(
        re.escape(MARK_START) + r'(.*?)' + re.escape(MARK_END),
        flags=re.DOTALL,
    )
    m = block_re.search(text)
    if not m:
        return False
    block = m.group(1)
    # Replace alt attribute
    block_new = re.sub(r'alt="[^"]*"', f'alt="{safe_cap}"', block, count=1)
    # Replace figcaption content (use function to avoid backref ambiguity)
    def _repl(m):
        return m.group(1) + safe_cap + m.group(2)
    block_new = re.sub(
        r'(<figcaption[^>]*>)[^<]*(</figcaption>)',
        _repl,
        block_new,
        count=1,
    )
    if block_new == block:
        return False
    new_text = text[:m.start()] + MARK_START + block_new + MARK_END + text[m.end():]
    path.write_text(new_text, encoding='utf-8')
    return True


def main():
    n = 0
    for slug, _ in CAPTIONS.items():
        p = ROOT / slug / 'index.html'
        if not p.exists():
            continue
        if update_one(slug, p):
            n += 1
            print(f'  caption updated: {slug}')
    print(f'\n{n} pages updated')


if __name__ == '__main__':
    main()
