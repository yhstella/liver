#!/usr/bin/env python3
"""
place_db_figures.py — Match selected DB figures to detail pages and inject.

전략:
1) manifest.csv 로드 — 702개 선별 이미지
2) 각 detail 페이지에 매칭 (slug 키워드 + topic 매핑)
3) 페이지당 최대 1개 figure 추가 (value_score 가장 높은 매칭)
4) 매칭된 이미지 파일을 private-figures/db/ → assets/img/db/{topic}/ 로 복사
5) HTML에 <figure class="db-fig"> 블록 삽입 (마커로 idempotent)

마커: <!-- db-figure:auto:start --> ... <!-- db-figure:auto:end -->
"""
from __future__ import annotations
import csv
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'private-figures' / 'db' / 'manifest.csv'
ASSETS_DIR = ROOT / 'assets' / 'img' / 'db'

MARK_START = '<!-- db-figure:auto:start -->'
MARK_END = '<!-- db-figure:auto:end -->'

# Slug-prefix → topic priority list (first match wins)
SLUG_TOPIC = [
    # HCC / 간암
    ('간암', ['hcc']),
    # cirrhosis
    ('간경변', ['cirrhosis_portal_htn']),
    ('간경화', ['cirrhosis_portal_htn']),
    # viral hepatitis
    ('B형간염', ['viral_hepatitis']),
    ('C형간염', ['viral_hepatitis']),
    ('A형간염', ['viral_hepatitis']),
    ('가족-B형간염', ['viral_hepatitis']),
    # MASLD/MASH
    ('지방간', ['masld_mash']),
    ('지방간염', ['masld_mash']),
    ('대사이상지방간', ['masld_mash']),
    ('술-안마셔도', ['masld_mash']),
    ('알코올성', ['masld_mash']),
    # AIH/PBC/PSC
    ('자가면역간염', ['autoimmune_cholestatic']),
    # benign
    ('간양성종양', ['imaging', 'hcc']),
    # LFT / labs / diagnostics
    ('PIVKA-II', ['hcc']),
    ('알파태아단백', ['hcc']),
    ('ALP-GGT', ['autoimmune_cholestatic', 'imaging']),
    ('빌리루빈', ['autoimmune_cholestatic']),
    ('알부민-PT', ['cirrhosis_portal_htn']),
    ('약물성-간손상', ['imaging']),
    ('간섬유화스캔', ['imaging', 'masld_mash']),
    ('간생검', ['imaging']),
    ('간수치', ['imaging']),
]

# Slug-specific keyword hints to refine within topic
SLUG_KW = {
    '간경변-식도정맥류': ['varices', '정맥류', 'EVL', '결찰'],
    '간경변-복수': ['ascites', '복수'],
    '간경변-간성혼수': ['encephalopathy', '간성혼수'],
    '간경변-Child-Pugh-MELD': ['child-pugh', 'MELD', 'score'],
    '간경변-간이식-평가': ['transplant', '간이식'],
    '간경변-간신증후군': ['HRS', '간신증후군'],
    '간경변-영양-근감소증': ['sarcopenia', '근감소'],
    '간경변-대상성-비대상성': ['decompensat', 'recompensat'],
    '간경변-약물-주의': ['drug', '약물'],
    '간경변-정상수치-함정': ['normal', 'compensated'],
    '간암-BCLC병기': ['BCLC', 'staging'],
    '간암-치료-선택': ['treatment', '치료'],
    '간암-진단-첫외래': ['diagnosis', '진단', 'LI-RADS'],
    '간암-방사선색전술': ['TARE', 'radioembolization', 'Y90'],
    '간암-면역치료-1차': ['atezolizumab', 'immunotherapy', 'IMbrave'],
    '간암-간이식': ['liver transplant', '이식'],
    '간암-재발-추적': ['recurrence', '재발'],
    '간암-식이-일상': ['diet', '식이'],
    '간암-소작술-RFA-MWA': ['RFA', 'MWA', 'ablation', '소작'],
    '간암-TACE-종류-결정': ['TACE', 'chemoembolization'],
    '간암-SBRT-양성자': ['SBRT', 'proton', 'radiation'],
    '간암-혈관침범-치료': ['vascular invasion', 'portal', '혈관침범'],
    '간암-가족력-검진': ['family history', '가족력'],
    'B형간염-검사결과': ['HBsAg', 'HBeAg', 'serology'],
    'B형간염-항바이러스제-비교': ['entecavir', 'tenofovir', 'TAF'],
    'B형간염-결혼-임신': ['pregnancy', '임신'],
    'B형간염-간암검진': ['surveillance', '검진'],
    'B형간염-재활성화': ['reactivation', '재활성화'],
    'B형간염-functional-cure': ['functional cure', 'HBsAg loss'],
    'B형간염-HBeAg-양성-음성': ['HBeAg', 'natural history'],
    'B형간염-백신': ['vaccine', '백신'],
    'B형간염-평생약': ['long-term', '평생'],
    'C형간염-진단': ['anti-HCV', 'RNA', 'PCR'],
    'C형간염-완치-DAA': ['DAA', 'SVR', 'glecaprevir', 'sofosbuvir'],
    'C형간염-완치후-추적': ['SVR', 'surveillance', 'post'],
    '대사이상지방간-MASLD': ['MASLD', 'steatosis', 'NAFLD'],
    '지방간-치료': ['weight loss', '체중'],
    '지방간-음식': ['diet', 'mediterranean'],
    '지방간-신약-resmetirom': ['resmetirom', 'THR'],
    '지방간-SGLT2-GLP1': ['SGLT2', 'GLP1', 'semaglutide'],
    '지방간-정밀검사': ['FIB-4', 'fibrosis', 'fibroscan'],
    '지방간-lean-MASLD': ['lean', 'BMI'],
    '지방간-회복-6개월': ['recovery', '회복'],
    '지방간-간암': ['HCC', 'MASLD-HCC'],
    '지방간염-MASH': ['MASH', 'NASH', 'ballooning'],
    '술-안마셔도-지방간': ['MASLD', 'metabolic'],
    '알코올성-간질환': ['alcoholic', 'ALD'],
    '자가면역간염-진단': ['simplified score', 'AIH score', 'interface'],
    '자가면역간염-치료': ['prednisolone', 'azathioprine'],
    '자가면역간염-약중단': ['discontinuation', 'relapse'],
    '간양성종양-혈관종': ['hemangioma', '혈관종'],
    '간양성종양-FNH-Adenoma': ['FNH', 'adenoma', 'HCA'],
    '간양성종양-낭종-관리': ['cyst', '낭종'],
    '간양성종양-진단': ['benign', 'imaging'],
}


def slug_to_topic(slug: str) -> list[str]:
    for prefix, topics in SLUG_TOPIC:
        if slug.startswith(prefix) or slug == prefix:
            return topics
    return []


def load_manifest():
    rows = []
    with MANIFEST.open(encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def score_match(row: dict, slug: str, target_topics: list[str]) -> int:
    """Score how well this image matches the page."""
    if not target_topics:
        return -1
    img_topics = row.get('topics', '').split(';')
    if not any(t in img_topics for t in target_topics):
        return -1
    score = int(row.get('value_score', 0) or 0)
    # boost by slug-specific keyword hits
    kws = SLUG_KW.get(slug, [])
    text = (row.get('keywords', '') + ' ' + row.get('meaning_ko', '') + ' ' + row.get('context_excerpt', '')).lower()
    for kw in kws:
        if kw.lower() in text:
            score += 30
    # primary topic match bonus
    if img_topics and img_topics[0] == target_topics[0]:
        score += 10
    return score


def pick_best_for_page(slug: str, manifest: list[dict], used: set) -> dict | None:
    topics = slug_to_topic(slug)
    if not topics:
        return None
    best = None
    best_score = 0
    for row in manifest:
        if row['image_id'] in used:
            continue
        s = score_match(row, slug, topics)
        if s > best_score:
            best = row
            best_score = s
    return best if best_score >= 50 else None  # threshold


def copy_to_assets(row: dict) -> str | None:
    """Copy DB image to assets/img/db/{topic}/ and return public URL."""
    src_rel = row['local_path']
    src = ROOT / src_rel
    if not src.exists():
        return None
    topic = src.parent.name
    dst_dir = ASSETS_DIR / topic
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    return f"/assets/img/db/{quote(topic, safe='')}/{quote(src.name, safe='')}"


def make_figure_block(url: str, caption: str) -> str:
    import html as h
    safe_cap = h.escape(caption)
    return (
        f'{MARK_START}\n'
        f'<figure class="db-fig" style="margin:24px auto;max-width:720px;text-align:center">\n'
        f'  <img src="{url}" alt="{safe_cap}" loading="lazy" decoding="async" '
        f'style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px">\n'
        f'  <figcaption style="font-size:12.5px;color:var(--muted);margin-top:8px;line-height:1.5;text-align:center">{safe_cap}</figcaption>\n'
        f'</figure>\n'
        f'{MARK_END}'
    )


def insert_block(html: str, block: str) -> str:
    """Insert/replace block. Place after first </h2> or after .tldr."""
    if MARK_START in html and MARK_END in html:
        return re.sub(
            re.escape(MARK_START) + r'.*?' + re.escape(MARK_END),
            block.replace('\\', '\\\\'),
            html,
            count=1,
            flags=re.DOTALL,
        )
    # insert after first </h2> of an article body section, or after TLDR
    m = re.search(r'</div>\s*<h2>', html)  # tldr ends with </div>, then h2 follows
    if m:
        idx = m.start() + len('</div>')
        return html[:idx] + '\n\n' + block + '\n\n' + html[idx:]
    # fallback: after H1
    m = re.search(r'</h1>\s*', html)
    if m:
        idx = m.end()
        return html[:idx] + '\n' + block + '\n' + html[idx:]
    return html


def gather_targets():
    """Find all detail page slugs (depth-1 dirs that have index.html and aren't hubs/sections)."""
    HUBS = {'간암','간경화','B형간염','C형간염','지방간','간수치','자가면역간염','간양성종양'}
    SECTIONS = {'CC','updates','케이스','keywords','소개','연구','guide','논문','assets','.tools','.git'}
    targets = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith('.') or d.name in HUBS or d.name in SECTIONS:
            continue
        if (d / 'index.html').exists():
            targets.append(d.name)
    return targets


def main():
    manifest = load_manifest()
    print(f'manifest: {len(manifest)} images')
    targets = gather_targets()
    print(f'detail pages: {len(targets)}')

    used = set()
    n_placed = 0
    for slug in targets:
        row = pick_best_for_page(slug, manifest, used)
        if not row:
            continue
        url = copy_to_assets(row)
        if not url:
            continue
        # Caption from meaning_ko (truncated) + source
        cap = row.get('meaning_ko', '')[:120].rstrip()
        if not cap:
            cap = row.get('keywords', '')[:120]
        block = make_figure_block(url, cap)
        page_path = ROOT / slug / 'index.html'
        html = page_path.read_text(encoding='utf-8')
        new_html = insert_block(html, block)
        if new_html != html:
            page_path.write_text(new_html, encoding='utf-8')
            used.add(row['image_id'])
            n_placed += 1
            print(f'  {slug}  ←  {row["image_id"]} (score≈{score_match(row, slug, slug_to_topic(slug))})')
    print(f'\nplaced figures on {n_placed} pages')


if __name__ == '__main__':
    main()
