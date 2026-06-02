#!/usr/bin/env python3
"""
ai_tells_audit.py — Detect patterns that suggest a page was written or augmented by
an AI tool rather than by the author (신현재). drshin.kr is a patient-facing site
where the author's voice is the trust signal; anything that breaks the illusion
of a doctor's own clinic notes is a defect.

Heuristics are intentionally simple and conservative. Reports counts; does NOT
modify pages.

Output: JSON report at .tools/ai_tells_report.json — per-page tells with counts,
plus a global frequency table.

Usage:
  python .tools/ai_tells_audit.py            # full site
  python .tools/ai_tells_audit.py --top 20   # show top 20 most-affected pages
  python .tools/ai_tells_audit.py --path X   # audit one folder
"""
from __future__ import annotations
import argparse, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / '.tools' / 'ai_tells_report.json'

SKIP = {'.git', '.tools', 'assets', 'guide', 'private-figures', 'node_modules'}

# Each rule: (id, description, regex pattern, severity 1-3)
RULES = [
    ('tldr-box',      'TLDR/핵심 요약 박스 (정형 패턴)',
     re.compile(r'<div\s+class="tldr">|class="tldr"|>한 문단 요약<|>한 줄 요약<|>핵심 요약<'), 2),
    ('entry-box',     '본인 시점 진입 박스 (처음 X 받으신 분께 등)',
     re.compile(r'처음\s+[^<>]{0,30}받으신\s+분께|본인\s+시점\s+가이드|오늘\s+할\s+일\s+[0-9N]+가지|오늘\s+바꿀\s+[0-9N]+가지'), 3),
    ('checklist-box', '체크리스트 박스 (오늘 해야 할 N가지 등)',
     re.compile(r'해야\s+할\s+[0-9N]+가지|체크리스트\s+박스|환자가\s+오늘'), 2),
    ('bottom-line',   'BOTTOM LINE / KEY FINDINGS 정형 헤더',
     re.compile(r'BOTTOM\s+LINE|KEY\s+FINDINGS|CLINICAL\s+TAKEAWAY|INTERPRETATION'), 2),
    ('snuh-pitch',    'SNUH 임상시험 안내 정형 단락',
     re.compile(r'본원\(서울대학교병원\)에서도[^<>]{10,80}임상시험\s+몇\s+건'), 3),
    ('label-pill',    'note-section .label 약식 라벨 (BACKGROUND·KEY 등)',
     re.compile(r'<span\s+class="label">\s*(BACKGROUND|KEY\s+FINDINGS|CLINICAL|BOTTOM|INTERPRETATION)'), 2),
    ('parenthetical-gloss', '약어 첫 등장 시 인라인 한글 풀이 일률 (HBeAg(B형간염 e항원) 등)',
     re.compile(r'\b(HBeAg|HBsAg|HBV|HCV|HCC|MASLD|MASH|TDF|ETV|TAF|FIB-4|CAP|LSM|BCLC|TACE|RFA|SBRT|MELD|UDCA|GLP-1|SGLT2|OSA|CPAP|PNPLA3|ASCVD|cccDNA)\s*\([가-힣][^)]{2,30}\)'), 1),
    ('hwanjabun-overuse', '"환자분" 과다 (한 문단 3회↑)',
     None, 2),  # special handling: per-paragraph count
    ('arrow-bullet',  '▶●◆ 등 marker 잔재',
     re.compile(r'[▶●◆✓✗★☆➤➜]'), 2),
    ('strong-overuse', '<strong> 한 문단 5회↑',
     None, 1),  # special handling
    ('jargon-burst',  '의학 약어 풀이 없이 연속 (BCLC·ALBI·ECOG·LI-RADS·STOP-BANG 등)',
     re.compile(r'(?:BCLC|ALBI|ECOG|LI-RADS|STOP-BANG|RUCAM|POISE|GLOBE|UK-PBC)\s*[,，·、]\s*(?:BCLC|ALBI|ECOG|LI-RADS|STOP-BANG|RUCAM|POISE|GLOBE|UK-PBC)'), 1),
    ('emphasis-words', '"결정적·사실상·절대·매우" 강조어 빈출',
     re.compile(r'결정적입니다|사실상|매우\s+(?:드뭅|흔합|중요)|절대\s+(?:금지|아님|불가)'), 1),
    ('every-paragraph-conj', '"다만/그러나/또한/따라서" 매 단락 시작',
     None, 1),  # special handling
    ('three-pronged-conclusion', '같은 결론이 TLDR + KEY FINDINGS + BOTTOM LINE 3중 반복',
     None, 2),  # special handling: page-level
]

KOREAN_RE = re.compile(r'[가-힣]')


def strip_head_and_scripts(html: str) -> str:
    """Body-ish text by removing head/script/style/json-ld."""
    html = re.sub(r'<head[\s\S]*?</head>', '', html, flags=re.I)
    html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.I)
    html = re.sub(r'<style[\s\S]*?</style>', '', html, flags=re.I)
    return html


def count_hwanjabun_overuse(body: str) -> int:
    """Number of <p> blocks where '환자분' appears 3+ times."""
    paragraphs = re.findall(r'<p[^>]*>([\s\S]*?)</p>', body)
    hits = 0
    for p in paragraphs:
        if p.count('환자분') >= 3:
            hits += 1
    return hits


def count_strong_overuse(body: str) -> int:
    """Number of <p> blocks with 5+ <strong> tags."""
    paragraphs = re.findall(r'<p[^>]*>([\s\S]*?)</p>', body)
    hits = 0
    for p in paragraphs:
        if p.count('<strong>') >= 5:
            hits += 1
    return hits


def count_conj_starts(body: str) -> int:
    """Paragraphs starting with 다만/그러나/또한/따라서."""
    paragraphs = re.findall(r'<p[^>]*>\s*([\s\S]*?)</p>', body)
    hits = 0
    for p in paragraphs:
        plain = re.sub(r'<[^>]+>', '', p).strip()
        if re.match(r'^(다만|그러나|또한|따라서)[\s,·]', plain):
            hits += 1
    return hits


def count_three_pronged(body: str) -> int:
    """1 if the page has TLDR + KEY FINDINGS + BOTTOM LINE in the same body."""
    has_tldr = 'class="tldr"' in body or '핵심 요약' in body or '한 문단 요약' in body
    has_key = 'KEY FINDINGS' in body
    has_bottom = 'BOTTOM LINE' in body or 'bottom-line' in body
    return 1 if (has_tldr and has_key and has_bottom) else 0


def audit_page(path: Path) -> dict:
    try:
        html = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None
    body = strip_head_and_scripts(html)

    tells = {}
    for rule_id, desc, pattern, severity in RULES:
        if pattern is not None:
            count = len(pattern.findall(body))
        elif rule_id == 'hwanjabun-overuse':
            count = count_hwanjabun_overuse(body)
        elif rule_id == 'strong-overuse':
            count = count_strong_overuse(body)
        elif rule_id == 'every-paragraph-conj':
            count = count_conj_starts(body)
        elif rule_id == 'three-pronged-conclusion':
            count = count_three_pronged(body)
        else:
            count = 0
        if count > 0:
            tells[rule_id] = {'count': count, 'severity': severity, 'desc': desc}

    if not tells:
        return None

    score = sum(t['count'] * t['severity'] for t in tells.values())
    return {'tells': tells, 'score': score}


def collect_pages(start: Path):
    for p in start.rglob('index.html'):
        rel = p.relative_to(ROOT)
        if any(part in SKIP or part.startswith('.') for part in rel.parts):
            continue
        yield p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--top', type=int, default=15)
    parser.add_argument('--path', default='.')
    args = parser.parse_args()

    start = (ROOT / args.path).resolve()
    if not start.exists():
        print(f'Path not found: {start}')
        return

    per_page = {}
    rule_freq = defaultdict(int)
    rule_pages = defaultdict(int)
    for path in collect_pages(start):
        result = audit_page(path)
        if result is None:
            continue
        rel = str(path.relative_to(ROOT)).replace('\\', '/')
        per_page[rel] = result
        for rule_id, t in result['tells'].items():
            rule_freq[rule_id] += t['count']
            rule_pages[rule_id] += 1

    ranked = sorted(per_page.items(), key=lambda x: -x[1]['score'])

    report = {
        'totalPagesWithTells': len(per_page),
        'ruleFrequency': dict(sorted(rule_freq.items(), key=lambda x: -x[1])),
        'rulePageCounts': dict(sorted(rule_pages.items(), key=lambda x: -x[1])),
        'topPages': [{'page': p, 'score': r['score'], 'tells': list(r['tells'].keys())} for p, r in ranked[:50]],
        'perPage': per_page,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'Pages with AI tells: {len(per_page)}')
    print('\nRule frequency (rule_id: page_count):')
    for rid, n in list(rule_pages.items())[:12]:
        print(f'  {rid}: {n} pages')
    print(f'\nTop {args.top} affected pages (by weighted score):')
    for page, r in ranked[:args.top]:
        print(f'  [{r["score"]:>4}] {page} — {", ".join(r["tells"].keys())}')
    print(f'\nFull report: .tools/ai_tells_report.json')


if __name__ == '__main__':
    main()
