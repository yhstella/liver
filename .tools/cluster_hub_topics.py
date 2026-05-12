#!/usr/bin/env python3
"""8 hub 페이지의 topic-list 항목을 의미별 클러스터로 재정렬.

각 hub: {cluster_name: [slug, ...]}
페이지의 <li> 항목을 cluster 순서대로 재배치 + <h3 class="cluster-header"> 삽입.
페이지 ID(NN)는 그대로 유지 (시각 흐름만 clustering).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CLUSTERS = {
    '간암': [
        ('진단·평가', ['간암-진단-첫외래','간암-BCLC병기','알파태아단백','PIVKA-II-간암마커','B형간염-간암검진','간암-가족력-검진','지방간-간암']),
        ('치료',     ['간암-치료-선택','간암-면역치료-1차','간암-간이식','간암-소작술-RFA-MWA','간암-TACE-종류-결정','간암-방사선색전술','간암-SBRT-양성자','간암-혈관침범-치료']),
        ('추적·일상', ['간암-재발-추적','간암-식이-일상']),
    ],
    '간경화': [
        ('진단·중증도', ['간경변-대상성-비대상성','간경변-Child-Pugh-MELD','간경변-정상수치-함정','간경변-혈소판감소','알코올성-간질환']),
        ('합병증',      ['간경변-식도정맥류','간경변-복수','간경변-간성혼수','간경변-간신증후군','간경변-감염-SBP-예방']),
        ('일상·관리',   ['간경변-영양-근감소증','간경변-약물-주의','간경변-피로감-증상관리','간경변-수면-가려움증','간경변-여행-항공-주의']),
        ('이식',        ['간경변-간이식-평가']),
    ],
    'B형간염': [
        ('진단·평가',     ['B형간염-검사결과','B형간염-HBeAg-양성-음성','B형간염-Occult-잠복감염']),
        ('치료',          ['B형간염-평생약','B형간염-항바이러스제-비교','B형간염-재활성화','B형간염-functional-cure','B형간염-신기능-약물선택','B형간염-수술전-예방']),
        ('예방',          ['B형간염-백신','A형간염']),
        ('특수상황',      ['가족-B형간염-검사','B형간염-D형간염-HDV','B형간염-결혼-임신','B형간염-소아청소년-치료']),
    ],
    '지방간': [
        ('진단·용어',   ['지방간-정밀검사','대사이상지방간-MASLD','지방간-MetALD','지방간염-MASH']),
        ('치료',        ['지방간-치료','지방간-신약-resmetirom','지방간-SGLT2-GLP1','지방간-비만수술','지방간-회복-6개월','지방간-음식']),
        ('진행·합병',   ['지방간-간암']),
        ('특수상황',    ['술-안마셔도-지방간','지방간-lean-MASLD','지방간-소아청소년-MASLD','지방간-수면무호흡-OSA','지방간-심혈관-CVD']),
    ],
    '간수치': [
        ('검사 이해',   ['간수치-종류-차이','간수치-높음','간수치-AST-우세-원인','간수치-임신중-변화','간수치-운동후-상승','간수치-검진주기-결정','간수치-소아청소년-기준']),
        ('표지자',      ['ALP-GGT-담도-간세포','빌리루빈-직접-간접','알부민-PT-간합성능']),
        ('영상·생검',   ['간섬유화스캔-수치','간생검-언제-필요한가']),
        ('원인',        ['약물성-간손상-DILI']),
    ],
    'C형간염': [
        ('진단',        ['C형간염-진단']),
        ('치료',        ['C형간염-완치-DAA','C형간염-DAA-실패-재치료','C형간염-신부전-치료','C형간염-HIV-동반']),
        ('추적·재감염', ['C형간염-완치후-추적','C형간염-재감염-위험군']),
        ('특수상황',    ['C형간염-임신수유']),
    ],
    '자가면역간염': [
        ('진단',     ['자가면역간염-진단','자가면역간염-PBC-overlap']),
        ('치료',     ['자가면역간염-치료','자가면역간염-약중단','자가면역간염-스테로이드-부작용']),
        ('특수상황', ['자가면역간염-임신','자가면역간염-소아청소년','자가면역간염-급성간부전']),
    ],
    '간양성종양': [
        ('진단',     ['간양성종양-진단','간양성종양-국소지방-변화','간양성종양-담관과오종']),
        ('종양 종류', ['간양성종양-혈관종','간양성종양-FNH-Adenoma','간양성종양-NRH','간양성종양-낭종-관리']),
        ('특수상황', ['간양성종양-임신중','간양성종양-경구피임약']),
    ],
}

LI_RE = re.compile(
    r'<li class="published">\s*<a href="/([^/]+)/">.*?</li>',
    re.DOTALL,
)
TOPIC_LIST_RE = re.compile(r'<ul class="topic-list">(.*?)</ul>', re.DOTALL)


def main():
    for hub, clusters in CLUSTERS.items():
        idx = ROOT / hub / 'index.html'
        if not idx.exists():
            print(f'  MISSING hub: {hub}')
            continue
        text = idx.read_text(encoding='utf-8')
        m = TOPIC_LIST_RE.search(text)
        if not m:
            print(f'  no topic-list: {hub}')
            continue
        block = m.group(1)
        # Extract all li → map slug → html
        li_map = {}
        for li_match in LI_RE.finditer(block):
            slug = li_match.group(1)
            li_map[slug] = li_match.group(0)
        if not li_map:
            print(f'  no li items: {hub}')
            continue

        # Build clustered output
        out_parts = []
        used_slugs = set()
        for cluster_name, slugs in clusters:
            cluster_lis = []
            for s in slugs:
                if s in li_map:
                    cluster_lis.append(li_map[s])
                    used_slugs.add(s)
            if not cluster_lis:
                continue
            out_parts.append(f'<h3 class="cluster-header">{cluster_name}</h3>')
            out_parts.extend(cluster_lis)

        # Any leftovers (slugs in page but not in cluster spec) — append under "기타"
        leftovers = [li_map[s] for s in li_map if s not in used_slugs]
        if leftovers:
            out_parts.append('<h3 class="cluster-header">기타</h3>')
            out_parts.extend(leftovers)

        new_block = '\n  '.join(out_parts)
        new_text = text[:m.start(1)] + '\n  ' + new_block + '\n' + text[m.end(1):]
        idx.write_text(new_text, encoding='utf-8')
        leftover_n = len(leftovers)
        print(f'  {hub}: {len(used_slugs)} clustered, {leftover_n} leftover')


if __name__ == '__main__':
    main()
