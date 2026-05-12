#!/usr/bin/env python3
"""UX: add intro paragraph to each hub + exclude self from '다른 주제' grid."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUB_INTROS = {
    '간암': '간세포암(HCC) 환자와 가족이 알아야 할 진단·병기·치료 흐름을 정리합니다. BCLC 병기에서 시작해 절제·소작·면역치료·이식까지, 한국 KLCA-NCC 가이드라인을 임상 현장의 결정과 함께 다룹니다.',
    '간경화': '간경변의 두 단계(대상성·비대상성), 합병증(복수·정맥류·간성혼수·간신증후군) 평가, Child-Pugh·MELD로 본 예후, 간이식 시점까지. 외래에서 자주 만나는 결정들을 단계별로 정리합니다.',
    'B형간염': '만성 B형간염의 진단·약물 결정·평생 추적·합병증 검진을 환자 시점에서 정리합니다. 검사 결과지 해석, 항바이러스제 비교, 임신·결혼·가족 검사, 간암 검진 등 외래에서 자주 받는 질문 중심.',
    'C형간염': 'DAA 시대 C형간염의 진단부터 8~12주 완치(SVR), 그 이후 평생 추적까지. 한국 검진에서 anti-HCV 양성으로 발견된 환자가 거치는 단계를 정리합니다.',
    '지방간': 'NAFLD에서 MASLD로 명명이 바뀐 지방간의 진단·정밀검사·생활습관·약물(resmetirom·GLP-1·SGLT2)을 다룹니다. lean MASLD, MetALD 같은 새 분류와 한국 진료 현장의 결정 흐름.',
    '간수치: 이상': '검진에서 발견된 간 효소 이상을 어떻게 평가하는지. AST·ALT·GGT의 차이, 빌리루빈·알부민·PT 같은 합성능 지표, AFP·PIVKA-II 종양표지자, Fibroscan·생검 단계까지.',
    '자가면역간염': '자가면역간염(AIH)의 4축 진단(ALT·IgG·자가항체·조직), 표준 면역억제 치료, 약 중단 결정, PBC overlap·임신·소아 등 특수 상황까지.',
    '간양성종양': '검진에서 우연히 발견되는 간 결절의 가장 흔한 4가지(혈관종·낭종·FNH·HCA) 감별과 추적·시술 결정. 영상으로 대부분 진단되지만 함정도 있습니다.',
}

# 정확한 hub key (간수치 typo 수정)
HUB_INTROS['간수치'] = HUB_INTROS.pop('간수치: 이상')

HUBS = list(HUB_INTROS.keys())


def add_intro(slug: str, intro: str) -> bool:
    p = ROOT / slug / 'index.html'
    text = p.read_text(encoding='utf-8')
    # Skip if already has intro
    if 'series-intro' in text:
        return False
    # Insert after series-meta
    pattern = re.compile(r'(<div class="series-meta">.*?</div>)\s*\n', re.DOTALL)
    block = f'\n<p class="series-intro">{intro}</p>\n\n'
    new_text = pattern.sub(lambda m: m.group(1) + block, text, count=1)
    if new_text == text:
        return False
    p.write_text(new_text, encoding='utf-8')
    return True


def remove_self_from_grid(slug: str) -> bool:
    """Remove the current hub from its own 'series-grid' (다른 주제) section."""
    p = ROOT / slug / 'index.html'
    text = p.read_text(encoding='utf-8')
    # Pattern: <a href="/{slug}/" class="series-tile">...</a>  inside series-grid
    pattern = re.compile(
        rf'\s*<a href="/{re.escape(slug)}/"\s+class="series-tile">.*?</a>',
        re.DOTALL,
    )
    new_text = pattern.sub('', text)
    if new_text == text:
        return False
    p.write_text(new_text, encoding='utf-8')
    return True


def main():
    n_intro = n_grid = 0
    for slug in HUBS:
        if add_intro(slug, HUB_INTROS[slug]):
            n_intro += 1
            print(f'  intro added: {slug}')
        if remove_self_from_grid(slug):
            n_grid += 1
            print(f'  self removed from grid: {slug}')
    print(f'\n{n_intro} hubs got intro, {n_grid} hubs cleaned grid')


if __name__ == '__main__':
    main()
