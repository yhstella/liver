#!/usr/bin/env python3
"""place_figures_v2.py — Label-aware figure placement for detail pages.

업데이트된 visual-label-audit/{db,personal-web}.visual-labels.csv 활용:
  - primary_topic, visual_type, label_ko, label_confidence, needs_review, mismatch_flag
  - 슬러그 키워드 → 선호 visual_type 매핑으로 의미 맞는 그림 자동 선정
  - label_ko가 신뢰도 높으면 그대로 caption

Marker: <!-- db-figure:auto:start --> ... <!-- db-figure:auto:end -->
"""
from __future__ import annotations
import csv
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DB_CSV = ROOT / 'private-figures' / 'visual-label-audit' / 'db.visual-labels.csv'
PWF_CSV = ROOT / 'private-figures' / 'visual-label-audit' / 'personal-web.visual-labels.csv'
ASSETS_DB = ROOT / 'assets' / 'img' / 'db'
ASSETS_PWF = ROOT / 'assets' / 'img' / 'pwf'

MARK_START = '<!-- db-figure:auto:start -->'
MARK_END = '<!-- db-figure:auto:end -->'
BLOCK_RE = re.compile(rf'{re.escape(MARK_START)}.*?{re.escape(MARK_END)}', re.DOTALL)

# Slug prefix → DB primary_topic candidates (first preferred)
SLUG_TOPIC = [
    ('간암', ['hcc']),
    ('알파태아단백', ['hcc']),
    ('PIVKA-II', ['hcc']),
    ('간경변', ['cirrhosis_portal_htn']),
    ('간경화', ['cirrhosis_portal_htn']),
    ('B형간염', ['hbv']),
    ('가족-B형간염', ['hbv']),
    ('A형간염', ['hbv']),
    ('C형간염', ['hcv']),
    ('자가면역간염', ['autoimmune_cholestatic']),
    ('ALP-GGT', ['autoimmune_cholestatic', 'liver_tests_diagnostics']),
    ('빌리루빈', ['liver_tests_diagnostics', 'autoimmune_cholestatic']),
    ('알부민-PT', ['cirrhosis_portal_htn', 'liver_tests_diagnostics']),
    ('지방간', ['masld_mash']),
    ('대사이상지방간', ['masld_mash']),
    ('지방간염', ['masld_mash']),
    ('술-안마셔도', ['masld_mash']),
    ('알코올성', ['masld_mash', 'cirrhosis_portal_htn']),
    ('간양성종양', ['benign_liver_lesions']),
    ('간섬유화스캔', ['liver_tests_diagnostics', 'anatomy_intervention']),
    ('간생검', ['liver_tests_diagnostics', 'anatomy_intervention']),
    ('약물성-간손상', ['liver_tests_diagnostics']),
    ('간수치', ['liver_tests_diagnostics']),
]

# Slug keyword → preferred visual_type list (additive)
SLUG_VTYPE = [
    (re.compile(r'진단|검진|검사|screen|diagno'), ['algorithm_flowchart', 'radiology_ct_mri', 'ultrasound_elastography']),
    (re.compile(r'치료|약|수술|이식|면역치료|RFA|TACE|SBRT|색전|소작'),
     ['treatment_schema', 'algorithm_flowchart', 'survival_curve']),
    (re.compile(r'병기|stag|BCLC'), ['algorithm_flowchart', 'treatment_schema']),
    (re.compile(r'영상|imaging|CT|MRI|초음파'), ['radiology_ct_mri', 'ultrasound_elastography']),
    (re.compile(r'식이|운동|일상|체중|음식|식단'), ['diet_lifestyle']),
    (re.compile(r'정맥류|varices|식도|EVL'), ['endoscopy']),
    (re.compile(r'병태|기전|mech'), ['mechanism_diagram', 'virology_diagram']),
    (re.compile(r'생검|biopsy|조직'), ['histology_pathology']),
    (re.compile(r'백신|vacc|serolog|혈청'), ['serology_lab', 'virology_diagram']),
    (re.compile(r'복수|ascites'), ['radiology_ct_mri', 'mechanism_diagram', 'clinical_photo']),
    (re.compile(r'재발|추적|surveil'), ['survival_curve', 'algorithm_flowchart']),
    (re.compile(r'바이러스|virus|HBV|HCV|HDV|HIV'), ['virology_diagram', 'serology_lab']),
    (re.compile(r'섬유화|fibrosis|elasto|fibroscan'), ['ultrasound_elastography']),
    (re.compile(r'수치|alt|ast|level|marker'), ['statistical_plot', 'text_table_slide']),
    (re.compile(r'명칭|용어|terminolog|MetALD|nomencl'), ['algorithm_flowchart', 'text_table_slide']),
    (re.compile(r'대상성|비대상성|recompensat|decompensat'), ['survival_curve', 'algorithm_flowchart']),
    (re.compile(r'간성혼수|encephal'), ['mechanism_diagram', 'algorithm_flowchart']),
    (re.compile(r'간이식|transplant'), ['algorithm_flowchart', 'survival_curve']),
    (re.compile(r'근감소|sarcopen|영양'), ['diet_lifestyle', 'text_table_slide']),
]

EXCLUDE_DIRS = {
    '간암', '간경화', 'B형간염', '지방간', '간수치', 'C형간염', '자가면역간염', '간양성종양',
    '케이스', 'CC', 'updates', 'keywords', 'assets', 'guide', '소개', '연구', '논문', 'search',
    '.tools', '.git', '.github', 'private-figures', 'node_modules',
}


def load_images():
    """Return list of dicts with normalized fields."""
    imgs = []
    for csv_path, kind in [(DB_CSV, 'db'), (PWF_CSV, 'pwf')]:
        with open(csv_path, encoding='utf-8-sig', newline='') as f:
            r = csv.DictReader(f)
            for row in r:
                # Skip mismatch high-severity
                if row.get('needs_review', '').strip() == 'yes':
                    continue
                imgs.append({
                    'kind': kind,
                    'id': row['id'],
                    'local_path': row['local_path'],
                    'primary_topic': row['primary_topic'],
                    'revised_topics': [t.strip() for t in row['revised_topics'].split(';') if t.strip()],
                    'visual_type': row['visual_type'],
                    'keywords': [k.strip().lower() for k in row['revised_keywords'].split(';') if k.strip()],
                    'label_ko': row.get('label_ko', '').strip(),
                    'confidence': int(row.get('label_confidence', '0') or 0),
                    'needs_review': row.get('needs_review', '').strip(),
                    'mismatch': row.get('mismatch_flag', '').strip(),
                })
    return imgs


def slug_to_topics(slug: str) -> list[str]:
    for prefix, topics in SLUG_TOPIC:
        if slug.startswith(prefix):
            return topics
    return []


def slug_to_vtypes(slug: str) -> list[str]:
    s = slug.lower()
    out = []
    for pat, vts in SLUG_VTYPE:
        if pat.search(s):
            for v in vts:
                if v not in out:
                    out.append(v)
    return out


def score(img: dict, topics: list[str], vtypes: list[str], slug_kw: list[str]) -> int:
    sc = 0
    if img['primary_topic'] == topics[0] if topics else False:
        sc += 100
    elif topics and img['primary_topic'] in topics:
        sc += 80
    # Revised topics match
    for t in topics:
        if t in img['revised_topics']:
            sc += 40
            break
    # Visual type match
    if vtypes:
        if img['visual_type'] in vtypes:
            sc += 50
            # rank bonus: earlier in preference list = higher
            idx = vtypes.index(img['visual_type'])
            sc += max(0, 20 - idx * 5)
    # Keyword match
    for kw in slug_kw:
        if kw.lower() in img['keywords']:
            sc += 15
    # Confidence
    sc += (img['confidence'] - 50) // 2
    # needs_review penalty
    if img['needs_review'] == 'maybe':
        sc -= 15
    if img['mismatch']:
        sc -= 10
    return sc


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in EXCLUDE_DIRS and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx


def copy_image(img: dict) -> tuple[str, Path]:
    """Copy private image to assets/img/{db|pwf}/{topic}/ and return (url_path, dest)."""
    src = ROOT / img['local_path']
    topic = img['primary_topic']
    if img['kind'] == 'db':
        dest_dir = ASSETS_DB / topic
        url_prefix = f'/assets/img/db/{topic}/'
    else:
        dest_dir = ASSETS_PWF / topic
        url_prefix = f'/assets/img/pwf/{topic}/'
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    if not dest.exists():
        shutil.copy2(src, dest)
    url = url_prefix + quote(src.name)
    return url, dest


def make_block(img: dict, url: str, slug: str) -> str:
    caption = img['label_ko'] if img['confidence'] >= 55 and img['label_ko'] else slug.replace('-', ' ')
    alt = caption
    return (
        f'{MARK_START}\n'
        f'<figure class="db-fig" style="margin:24px auto;max-width:720px;text-align:center">\n'
        f'  <img src="{url}" alt="{alt}" loading="lazy" decoding="async" '
        f'style="max-width:100%;height:auto;border:1px solid var(--line);border-radius:6px">\n'
        f'  <figcaption style="font-size:12.5px;color:var(--muted);margin-top:8px;line-height:1.5;text-align:center">{caption}</figcaption>\n'
        f'</figure>\n'
        f'{MARK_END}'
    )


def derive_slug_keywords(slug: str) -> list[str]:
    # Drop hub prefix, split by '-', take meaningful tokens
    tokens = []
    for prefix in ['간암-', '간경변-', '간경화-', 'B형간염-', 'C형간염-', '자가면역간염-',
                   '지방간-', '간수치-', '간양성종양-', '대사이상지방간-', '약물성-간손상-',
                   '가족-B형간염-', 'ALP-GGT-', 'PIVKA-II-', '알부민-PT-']:
        if slug.startswith(prefix):
            slug_rest = slug[len(prefix):]
            break
    else:
        slug_rest = slug
    for tok in re.split(r'[-_]', slug_rest):
        if tok and len(tok) >= 2:
            tokens.append(tok)
    return tokens


def main():
    imgs = load_images()
    print(f'Loaded {len(imgs)} images')
    used_ids = {}  # img_id → count (avoid heavy reuse)
    changed = 0
    skipped = 0
    for idx in detail_pages():
        slug = idx.parent.name
        topics = slug_to_topics(slug)
        if not topics:
            skipped += 1
            continue
        vtypes = slug_to_vtypes(slug)
        slug_kw = derive_slug_keywords(slug)
        # Score
        candidates = []
        for img in imgs:
            if img['primary_topic'] not in topics and not any(t in img['revised_topics'] for t in topics):
                continue
            sc = score(img, topics, vtypes, slug_kw)
            # Reuse penalty
            sc -= used_ids.get(img['id'], 0) * 25
            candidates.append((sc, img))
        if not candidates:
            skipped += 1
            print(f'  no candidates: {slug}')
            continue
        candidates.sort(key=lambda x: (-x[0], x[1]['id']))
        best = candidates[0][1]
        used_ids[best['id']] = used_ids.get(best['id'], 0) + 1

        url, _ = copy_image(best)
        block = make_block(best, url, slug)

        txt = idx.read_text(encoding='utf-8')
        if MARK_START in txt:
            new = BLOCK_RE.sub(block, txt, count=1)
        else:
            # Inject before first <h2>
            m = re.search(r'<h2', txt)
            if not m:
                skipped += 1
                continue
            new = txt[:m.start()] + block + '\n\n' + txt[m.start():]
        if new != txt:
            idx.write_text(new, encoding='utf-8')
            changed += 1
            print(f'  {slug}: {best["id"]} ({best["primary_topic"]}/{best["visual_type"]}, score={candidates[0][0]})')
    print(f'\nChanged: {changed}, Skipped: {skipped}')


if __name__ == '__main__':
    main()
