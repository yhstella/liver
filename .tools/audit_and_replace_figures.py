#!/usr/bin/env python3
"""
audit_and_replace_figures.py — Re-audit every detail page's figure
against the unified candidate pool (db/ + personal-web-figures/) and
swap to a more specific match when one exists.

전략:
  1) Unified pool 빌드 — 731 (db) + 210 (pwf) = 941 후보, 메타 통합
  2) 각 detail page에 대해:
     - slug + h1에서 키워드 추출
     - 현재 figure id 식별 → 점수 측정
     - 풀 전체에서 최고 점수 후보 탐색
     - alternative score - current score >= SWAP_THRESHOLD 이면 교체
  3) 교체된 figure는 assets/img/{prefix}/ 로 복사 (pwf는 db/{pwf_topic}/)
  4) HTML 갱신 — caption은 figure-specific (pwf의 caption 필드 우선)
  5) report 출력
"""
from __future__ import annotations
import csv
import re
import shutil
from pathlib import Path
from urllib.parse import quote
import html as h

ROOT = Path(__file__).resolve().parent.parent
DB_MANIFEST = ROOT / 'private-figures' / 'manifest.csv'
PWF_MANIFEST = ROOT / 'private-figures' / 'personal-web-figures' / 'manifest.csv'
ASSETS_DB = ROOT / 'assets' / 'img' / 'db'
SWAP_THRESHOLD = 15

# Korean slug-specific captions (mirror of improve_db_captions.py CAPTIONS)
# Falls back to PWF/db caption if not found
KO_CAPTIONS_PATH = None  # loaded lazily

def _load_ko_captions():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'improve_captions',
        ROOT / '.tools' / 'improve_db_captions.py',
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, 'CAPTIONS', {})

KO_CAPTIONS = _load_ko_captions()

MARK_START = '<!-- db-figure:auto:start -->'
MARK_END = '<!-- db-figure:auto:end -->'

# ─── slug → topic mapping (db topics + pwf topics) ────────────────────
SLUG_TOPICS = [
    # HCC pages (간암-*)
    ('간암-BCLC', ['hcc', 'hcc_systemic_trial']),
    ('간암-치료-선택', ['hcc_systemic_trial', 'hcc']),
    ('간암-진단-첫외래', ['hcc_imaging_pathology', 'hcc']),
    ('간암-면역치료', ['hcc_systemic_trial', 'hcc']),
    ('간암-혈관침범', ['hcc_systemic_trial', 'hcc']),
    ('간암-방사선색전술', ['hcc_imaging_pathology', 'hcc']),
    ('간암-소작술', ['hcc_imaging_pathology', 'hcc']),
    ('간암-TACE', ['hcc_systemic_trial', 'hcc']),
    ('간암-SBRT', ['hcc_systemic_trial', 'hcc']),
    ('간암-간이식', ['acute_liver_failure_transplant', 'hcc']),
    ('간암-재발', ['hcc']),
    ('간암-가족력', ['hcc']),
    ('간암-식이', ['hcc']),
    ('간암', ['hcc']),
    # Cirrhosis (간경변-*)
    ('간경변', ['cirrhosis_portal_htn']),
    ('간경화', ['cirrhosis_portal_htn']),
    # B형간염
    ('B형간염', ['hbv_lifecycle_serology', 'viral_hepatitis']),
    ('가족-B형간염', ['hbv_lifecycle_serology', 'viral_hepatitis']),
    # C형간염
    ('C형간염', ['hcv_daa_lifecycle', 'viral_hepatitis']),
    # A형간염
    ('A형간염', ['viral_hepatitis']),
    # 지방간 / MASLD
    ('지방간', ['masld_mash']),
    ('지방간염', ['masld_mash']),
    ('대사이상지방간', ['masld_mash']),
    ('술-안마셔도', ['masld_mash']),
    ('알코올성', ['masld_mash']),
    # AIH
    ('자가면역간염', ['autoimmune_cholestatic']),
    # 간양성종양
    ('간양성종양', ['benign_liver_lesions', 'imaging']),
    # 간수치 / labs
    ('PIVKA-II', ['liver_tests_diagnostics', 'hcc']),
    ('알파태아단백', ['liver_tests_diagnostics', 'hcc']),
    ('ALP-GGT', ['liver_tests_diagnostics', 'autoimmune_cholestatic']),
    ('빌리루빈', ['liver_tests_diagnostics', 'autoimmune_cholestatic']),
    ('알부민-PT', ['liver_tests_diagnostics', 'cirrhosis_portal_htn']),
    ('약물성-간손상', ['liver_tests_diagnostics']),
    ('간섬유화스캔', ['liver_tests_diagnostics', 'masld_mash']),
    ('간생검', ['liver_tests_diagnostics']),
    ('간수치', ['liver_tests_diagnostics']),
]

# slug → keyword hints for caption matching
SLUG_KW = {
    '간경변-식도정맥류': ['varices', '정맥류', 'EVL', 'banding', 'band ligation'],
    '간경변-복수': ['ascites', '복수', 'paracentesis'],
    '간경변-간성혼수': ['encephalopathy', '간성혼수', 'ammonia'],
    '간경변-Child-Pugh-MELD': ['child-pugh', 'MELD', 'score', '점수'],
    '간경변-간이식-평가': ['transplant', '간이식', 'allocation'],
    '간경변-간신증후군': ['HRS', '간신증후군', 'hepatorenal'],
    '간경변-영양-근감소증': ['sarcopenia', '근감소', 'nutrition'],
    '간경변-대상성-비대상성': ['decompensat', 'recompensat'],
    '간경변-약물-주의': ['drug', '약물', 'NSAIDs'],
    '간경변-정상수치-함정': ['normal', 'compensated', 'cirrhosis'],
    '간경변-혈소판감소': ['platelet', '혈소판', 'thrombocytopenia', 'spleen'],
    '간경변-감염-SBP-예방': ['SBP', 'spontaneous bacterial peritonitis', '복막염'],
    '간경변-피로감-증상관리': ['fatigue', '피로'],
    '간경변-수면-가려움증': ['pruritus', '가려움', 'sleep', '수면'],
    '간경변-여행-항공-주의': ['travel', '여행'],
    '간암-BCLC병기': ['BCLC', 'staging', 'algorithm'],
    '간암-치료-선택': ['treatment algorithm', '치료'],
    '간암-진단-첫외래': ['diagnosis', '진단', 'LI-RADS', 'imaging'],
    '간암-방사선색전술': ['TARE', 'radioembolization', 'Y90', 'yttrium'],
    '간암-면역치료-1차': ['atezolizumab', 'immunotherapy', 'IMbrave', 'PD-L1'],
    '간암-간이식': ['liver transplant', '이식', 'Milan'],
    '간암-재발-추적': ['recurrence', '재발', 'surveillance'],
    '간암-식이-일상': ['diet', '식이', 'nutrition'],
    '간암-소작술-RFA-MWA': ['RFA', 'MWA', 'ablation', '소작', 'radiofrequency', 'microwave'],
    '간암-TACE-종류-결정': ['TACE', 'chemoembolization', 'DEB-TACE'],
    '간암-SBRT-양성자': ['SBRT', 'proton', 'radiation', 'stereotactic'],
    '간암-혈관침범-치료': ['vascular invasion', 'portal vein', '혈관침범'],
    '간암-가족력-검진': ['family history', '가족력', 'screening'],
    'B형간염-검사결과': ['HBsAg', 'HBeAg', 'serology', 'natural history'],
    'B형간염-항바이러스제-비교': ['entecavir', 'tenofovir', 'TAF'],
    'B형간염-결혼-임신': ['pregnancy', '임신', 'vertical'],
    'B형간염-간암검진': ['surveillance', '검진', 'HBV HCC'],
    'B형간염-재활성화': ['reactivation', '재활성화', 'cccDNA'],
    'B형간염-functional-cure': ['functional cure', 'HBsAg loss', 'cccDNA'],
    'B형간염-HBeAg-양성-음성': ['HBeAg', 'natural history', 'phase'],
    'B형간염-백신': ['vaccine', '백신', 'HBV vaccination'],
    'B형간염-평생약': ['long-term', '평생', 'lifetime'],
    'B형간염-Occult-잠복감염': ['occult', '잠복', 'cccDNA'],
    'B형간염-소아청소년-치료': ['pediatric', '소아', 'childhood'],
    'B형간염-D형간염-HDV': ['HDV', 'D형', 'delta'],
    'B형간염-신기능-약물선택': ['renal', '신기능', 'CKD'],
    'B형간염-수술전-예방': ['surgery', '수술전', 'rituximab'],
    'C형간염-진단': ['anti-HCV', 'RNA', 'PCR', 'HCV diagnosis'],
    'C형간염-완치-DAA': ['DAA', 'SVR', 'glecaprevir', 'sofosbuvir', 'maviret'],
    'C형간염-완치후-추적': ['SVR', 'surveillance', 'post-DAA'],
    'C형간염-재감염-위험군': ['reinfection', '재감염'],
    'C형간염-신부전-치료': ['renal', 'CKD', 'dialysis', '투석'],
    'C형간염-임신수유': ['pregnancy', '임신', 'vertical'],
    'C형간염-HIV-동반': ['HIV', 'coinfection'],
    'C형간염-DAA-실패-재치료': ['retreatment', 'voxilaprevir', 'failure'],
    '대사이상지방간-MASLD': ['MASLD', 'NAFLD', 'steatosis'],
    '지방간-치료': ['weight loss', '체중', 'lifestyle'],
    '지방간-음식': ['diet', 'mediterranean', '식단'],
    '지방간-신약-resmetirom': ['resmetirom', 'THR', 'thyroid hormone'],
    '지방간-SGLT2-GLP1': ['SGLT2', 'GLP-1', 'semaglutide', 'tirzepatide'],
    '지방간-정밀검사': ['FIB-4', 'fibrosis', 'fibroscan', 'MRE'],
    '지방간-lean-MASLD': ['lean', 'BMI', 'PNPLA3'],
    '지방간-회복-6개월': ['recovery', '회복', 'reversal'],
    '지방간-간암': ['HCC', 'MASLD-HCC'],
    '지방간염-MASH': ['MASH', 'NASH', 'ballooning', 'inflammation'],
    '지방간-소아청소년-MASLD': ['pediatric', '소아', 'children'],
    '지방간-수면무호흡-OSA': ['OSA', 'sleep apnea'],
    '지방간-MetALD': ['MetALD', 'alcohol'],
    '지방간-심혈관-CVD': ['cardiovascular', '심혈관'],
    '지방간-비만수술': ['bariatric', 'sleeve', 'gastric bypass'],
    '술-안마셔도-지방간': ['MASLD', 'metabolic'],
    '알코올성-간질환': ['alcoholic', 'ALD', 'alcohol liver'],
    '자가면역간염-진단': ['simplified score', 'AIH score', 'interface hepatitis'],
    '자가면역간염-치료': ['prednisolone', 'azathioprine', 'AIH treatment'],
    '자가면역간염-약중단': ['discontinuation', 'relapse', 'withdrawal'],
    '자가면역간염-PBC-overlap': ['overlap', 'AIH-PBC', 'Paris criteria'],
    '자가면역간염-임신': ['pregnancy', '임신'],
    '자가면역간염-스테로이드-부작용': ['steroid', '스테로이드', 'side effect'],
    '자가면역간염-소아청소년': ['pediatric', '소아', 'childhood AIH'],
    '자가면역간염-급성간부전': ['acute liver failure', '급성', 'fulminant'],
    '간양성종양-혈관종': ['hemangioma', '혈관종'],
    '간양성종양-FNH-Adenoma': ['FNH', 'adenoma', 'HCA', 'focal nodular'],
    '간양성종양-낭종-관리': ['cyst', '낭종', 'simple cyst'],
    '간양성종양-진단': ['benign', 'imaging', '양성'],
    '간양성종양-담관과오종': ['hamartoma', 'Von Meyenburg'],
    '간양성종양-국소지방-변화': ['focal fat', 'sparing', 'deposition'],
    '간양성종양-NRH': ['NRH', 'nodular regenerative'],
    '간양성종양-임신중': ['pregnancy', '임신'],
    '간양성종양-경구피임약': ['oral contraceptive', '피임약', 'estrogen'],
}


def load_manifest(path: Path, source_kind: str) -> list[dict]:
    rows = []
    with path.open(encoding='utf-8-sig') as f:
        for r in csv.DictReader(f):
            r['_source'] = source_kind  # 'db' or 'pwf'
            rows.append(r)
    return rows


def slug_to_topic(slug: str) -> list[str]:
    for prefix, topics in SLUG_TOPICS:
        if slug.startswith(prefix) or slug == prefix:
            return topics
    return []


def score_match(row: dict, slug: str, target_topics: list[str]) -> int:
    """Score 0~250+; higher = better."""
    if not target_topics:
        return 0
    img_topics = (row.get('topic') or row.get('topics', '')).split(';')
    if not any(t in img_topics for t in target_topics):
        return 0
    score = 0
    # base: source quality (pwf > db b/c per-figure caption)
    if row['_source'] == 'pwf':
        score += 50
    else:
        score += int(row.get('value_score', 0) or 0)
    # primary topic bonus
    if img_topics and img_topics[0] in target_topics:
        score += 15
    # slug-keyword hits in caption/meaning/subtopic
    text = ' '.join([
        (row.get('caption') or ''),
        (row.get('meaning_ko') or ''),
        (row.get('subtopic') or ''),
        (row.get('keywords') or ''),
        (row.get('context_excerpt') or ''),
        (row.get('figure_title') or ''),
    ]).lower()
    kws = SLUG_KW.get(slug, [])
    matched = 0
    for kw in kws:
        if kw.lower() in text:
            score += 25
            matched += 1
    # bonus for figure-specific caption (pwf)
    if row['_source'] == 'pwf' and matched > 0:
        score += 20
    return score


def page_caption(row: dict, slug: str | None = None) -> str:
    """Pick best caption: Korean slug-specific > pwf English caption > db meaning_ko."""
    # 1) Korean slug-specific (if defined in improve_db_captions.py)
    if slug and slug in KO_CAPTIONS:
        return KO_CAPTIONS[slug]
    # 2) PWF figure-specific English caption
    if row['_source'] == 'pwf':
        cap = (row.get('caption') or '').strip()
        if cap:
            cap = re.split(r'(?<=[.。])\s+', cap)[0]
            if len(cap) > 220:
                cap = cap[:200].rsplit(' ', 1)[0] + '…'
            return cap
        return (row.get('figure_title') or row.get('subtopic') or row.get('meaning_ko') or '')
    # 3) DB meaning_ko (generic)
    return row.get('meaning_ko', '')[:200]


def asset_url(row: dict) -> str | None:
    """Copy source to assets/img/db/ and return public URL."""
    src = ROOT / row['local_path']
    if not src.exists():
        return None
    if row['_source'] == 'pwf':
        # Use pwf topic directly under assets/img/db/
        topic = row['topic']
        dst_dir = ASSETS_DB / topic
    else:
        topic = src.parent.name
        dst_dir = ASSETS_DB / topic
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    return f"/assets/img/db/{quote(topic, safe='')}/{quote(src.name, safe='')}"


def attribution(row: dict) -> str:
    """Return short attribution suffix (for CC BY / source)."""
    if row['_source'] != 'pwf':
        return ''
    src_kind = row.get('source_kind', '')
    src_url = row.get('source_url', '')
    if 'wikimedia' in src_kind.lower():
        return ' <span style="font-size:10.5px;color:var(--muted)">· Wikimedia Commons (CC BY 4.0)</span>'
    if 'pmc' in src_kind.lower() or row.get('pmcid'):
        return ' <span style="font-size:10.5px;color:var(--muted)">· PMC OA</span>'
    return ''


def find_current_figure_id(html: str) -> str | None:
    m = re.search(r'/assets/img/db/[^/]+/(img_\d+|pwf_\d+)', html)
    return m.group(1) if m else None


def build_block(url: str, caption: str, attribution_html: str) -> str:
    safe = h.escape(caption)
    return (
        f'{MARK_START}\n'
        f'<figure class="db-fig" style="margin:24px auto;max-width:720px;text-align:center">\n'
        f'  <img src="{url}" alt="{safe}" loading="lazy" decoding="async" '
        f'style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px">\n'
        f'  <figcaption style="font-size:12.5px;color:var(--muted);margin-top:8px;line-height:1.5;text-align:center">{safe}{attribution_html}</figcaption>\n'
        f'</figure>\n'
        f'{MARK_END}'
    )


def replace_block(html: str, block: str) -> str:
    return re.sub(
        re.escape(MARK_START) + r'.*?' + re.escape(MARK_END),
        block.replace('\\', '\\\\'),
        html,
        count=1,
        flags=re.DOTALL,
    )


def gather_pages():
    HUBS = {'간암','간경화','B형간염','C형간염','지방간','간수치','자가면역간염','간양성종양'}
    SECT = {'CC','updates','케이스','keywords','소개','연구','guide','논문','assets','.tools','.git','private-figures'}
    targets = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith('.') or d.name in HUBS or d.name in SECT:
            continue
        idx = d / 'index.html'
        if idx.exists():
            text = idx.read_text(encoding='utf-8')
            if MARK_START in text:
                targets.append(d.name)
    return targets


def main():
    db_rows = load_manifest(DB_MANIFEST, 'db')
    pwf_rows = load_manifest(PWF_MANIFEST, 'pwf')
    pool = db_rows + pwf_rows
    # Index by id
    pool_by_id = {}
    for r in pool:
        fid = r.get('image_id') or r.get('figure_id')
        if fid:
            pool_by_id[fid] = r

    print(f'pool: {len(db_rows)} db + {len(pwf_rows)} pwf = {len(pool)} total')

    targets = gather_pages()
    print(f'pages with db-figure: {len(targets)}\n')

    swapped = 0
    kept = 0
    no_match = 0
    used = set()
    used_in_other_pages = set()  # avoid same image on multiple pages

    # First pass: build current usage
    for slug in targets:
        html = (ROOT / slug / 'index.html').read_text(encoding='utf-8')
        fid = find_current_figure_id(html)
        if fid:
            used_in_other_pages.add(fid)

    log_lines = []
    for slug in targets:
        page_path = ROOT / slug / 'index.html'
        html = page_path.read_text(encoding='utf-8')
        topics = slug_to_topic(slug)
        if not topics:
            no_match += 1
            log_lines.append(f'  ?  {slug}: no topic mapping')
            continue
        cur_fid = find_current_figure_id(html)
        cur_score = 0
        if cur_fid and cur_fid in pool_by_id:
            cur_score = score_match(pool_by_id[cur_fid], slug, topics)

        # Find best alternative (not currently used elsewhere)
        best = None
        best_score = 0
        for r in pool:
            fid = r.get('image_id') or r.get('figure_id')
            if not fid:
                continue
            if fid == cur_fid:
                continue
            if fid in used:
                continue
            # avoid replacing with image already used on another page
            if fid in used_in_other_pages and fid != cur_fid:
                continue
            s = score_match(r, slug, topics)
            if s > best_score:
                best = r
                best_score = s

        if best and (best_score - cur_score) >= SWAP_THRESHOLD:
            url = asset_url(best)
            if not url:
                kept += 1
                continue
            cap = page_caption(best, slug)
            attr = attribution(best)
            block = build_block(url, cap, attr)
            new_html = replace_block(html, block)
            if new_html != html:
                page_path.write_text(new_html, encoding='utf-8')
                swapped += 1
                fid_new = best.get('figure_id') or best.get('image_id')
                used.add(fid_new)
                if cur_fid:
                    used_in_other_pages.discard(cur_fid)
                used_in_other_pages.add(fid_new)
                log_lines.append(f'  ↑  {slug}: {cur_fid} ({cur_score}) → {fid_new} ({best_score}) [{best["_source"]}]')
                continue
        kept += 1
        if cur_fid:
            used.add(cur_fid)

    print(f'swapped: {swapped}, kept: {kept}, no-match: {no_match}')
    print()
    for line in log_lines[:60]:
        print(line)
    if len(log_lines) > 60:
        print(f'  … +{len(log_lines)-60} more')


if __name__ == '__main__':
    main()
