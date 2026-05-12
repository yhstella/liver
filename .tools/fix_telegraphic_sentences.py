#!/usr/bin/env python3
"""세부주제 페이지의 명사형 telegraphic 종결 비문 → 풀 문장(~합니다/~권유드립니다)으로 교체.

스캔 + targeted 치환 (각 비문에 맥락 맞춰 자연 문장 부여).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = [
    # (file_slug, old, new)
    ('B형간염-Occult-잠복감염',
     '<li>일부 환자는 anti-HBs도 양성(과거 자연 회복 패턴), 그래도 occult 상태 가능.</li>',
     '<li>일부 환자분은 anti-HBs도 함께 양성(과거 자연 회복 패턴)으로 나오는데, 이때도 occult 상태일 가능성은 남아 있습니다.</li>'),

    ('B형간염-결혼-임신',
     '<li>여전히 무반응이면 2배 용량 백신 또는 새로운 보조제 백신(HepB-CpG, Heplisav-B) 검토.</li>',
     '<li>그래도 무반응이라면 2배 용량 백신이나 새로운 보조제 백신(HepB-CpG, Heplisav-B)을 검토합니다.</li>'),
    ('B형간염-결혼-임신',
     '<li>임신 중 약을 시작했다면 산후 4~12주에 중단 가능 여부 평가.</li>',
     '<li>임신 중에 약을 시작하셨다면 출산 후 4~12주 시점에 중단 가능 여부를 평가합니다.</li>'),

    ('간경변-복수',
     '<li>다제내성균 노출 환자에서는 노르플록사신 효과 감소 — 배양 패턴에 따라 변경 검토.</li>',
     '<li>다제내성균에 노출된 환자분에서는 노르플록사신의 효과가 떨어지므로, 배양 결과에 따라 항생제 변경을 검토합니다.</li>'),

    ('간경변-영양-근감소증',
     '<li>가공식품 영양표시 1회 분량 기준 확인.</li>',
     '<li>가공식품을 드실 때는 영양표시의 1회 분량 기준을 확인하시는 것이 좋습니다.</li>'),

    ('간수치-AST-우세-원인',
     '<li>영상 — 간경변 평가.</li>',
     '<li>복부 초음파나 CT 등 영상 검사로 간경변 여부를 평가합니다.</li>'),
    ('간수치-AST-우세-원인',
     '<li>알코올 이력 — 가장 흔한 원인. 솔직한 음주력 확인.</li>',
     '<li>가장 흔한 원인은 알코올이므로, 음주력을 정확히 확인하는 것이 진단의 첫 단계입니다.</li>'),

    ('간양성종양-낭종-관리',
     '<li>거대 PCLD가 삶의 질을 심각하게 저하시키면 간이식 검토.</li>',
     '<li>거대 PCLD가 삶의 질을 심각하게 떨어뜨리는 경우에는 간이식까지도 검토할 수 있습니다.</li>'),

    ('대사이상지방간-MASLD',
     '<li>아시아 비만 기준(BMI ≥ 23, 허리둘레 남 ≥ 90, 여 ≥ 80)이 서양 기준(BMI ≥ 25)보다 낮아 국내 환자에서 mild overweight 단계부터 평가 필요.</li>',
     '<li>아시아 비만 기준(BMI ≥ 23, 허리둘레 남자 ≥ 90 cm, 여자 ≥ 80 cm)이 서양 기준(BMI ≥ 25)보다 낮기 때문에, 국내 환자분은 mild overweight 단계에서부터 평가하는 것이 필요합니다.</li>'),

    ('자가면역간염-임신',
     '<li>6개월 이상 안정 유지 후 임신 계획 권장.</li>',
     '<li>6개월 이상 안정된 상태가 유지된 뒤에 임신 계획을 잡으시기를 권유드립니다.</li>'),

    ('지방간-소아청소년-MASLD',
     '<li>비타민 E — 비당뇨·고섬유화 청소년 일부에서 검토.</li>',
     '<li>비타민 E는 당뇨가 없으면서 섬유화가 진행된 청소년 일부에서 사용을 검토할 수 있습니다.</li>'),
]


def main():
    fixed = 0
    for slug, old, new in REPLACEMENTS:
        f = ROOT / slug / 'index.html'
        if not f.exists():
            print(f'  MISSING: {slug}')
            continue
        text = f.read_text(encoding='utf-8')
        if old in text:
            f.write_text(text.replace(old, new, 1), encoding='utf-8')
            fixed += 1
            print(f'  fixed: {slug}')
        else:
            print(f'  NOT FOUND in {slug}')
    print(f'\nFixed: {fixed}/{len(REPLACEMENTS)}')


if __name__ == '__main__':
    main()
