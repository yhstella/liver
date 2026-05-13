#!/usr/bin/env python3
"""세부주제 톤·표기 wave 4.

A. HBV DNA 단위 IU/mL 일괄 보강 (사용자: '단위를 꼭 써라')
B. 방사선색전술(경동맥방사선색전술(TARE)) 이중 괄호 제거 (1-11 패턴)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {'.git','.tools','node_modules','private-figures','assets','guide'}

# === A. DNA 단위 보강 ===
DNA_PATTERNS = [
    # `(DNA ≥ 2,000)` → `(DNA ≥ 2,000 IU/mL)`
    (re.compile(r'\(DNA\s*([≥<>])\s*([\d,]+)\)(?!\s*IU/m[lL])'),
     lambda m: f'(DNA {m.group(1)} {m.group(2)} IU/mL)'),
    # `DNA ≥ 2,000` → `DNA ≥ 2,000 IU/mL` (괄호 없음)
    (re.compile(r'\bDNA\s*([≥<>])\s*([\d,]+)(?!\s*IU/m[lL])(?!\s*[가-힣A-Za-z])'),
     lambda m: f'DNA {m.group(1)} {m.group(2)} IU/mL'),
    # `DNA ≥2,000` (no space)
    (re.compile(r'\bDNA\s*([≥<>])([\d,]+)(?!\s*IU/m[lL])'),
     lambda m: f'DNA {m.group(1)} {m.group(2)} IU/mL'),
    # `HBV DNA가 2,000 이상` → `HBV DNA가 2,000 IU/mL 이상`
    (re.compile(r'\bDNA(가|는|이|을)\s*([\d,]+)\s*(이상|초과|미만|이하)(?!\s*IU/m[lL])'),
     lambda m: f'DNA{m.group(1)} {m.group(2)} IU/mL {m.group(3)}'),
    # `DNA 2,000 초과` → `DNA 2,000 IU/mL 초과`
    (re.compile(r'\bDNA\s+([\d,]+)\s*(이상|초과|미만|이하)(?!\s*IU/m[lL])'),
     lambda m: f'DNA {m.group(1)} IU/mL {m.group(2)}'),
    # `HBV DNA 12,000` (SVG text or table cell, no operator) — guard for 4-digit+ only
    (re.compile(r'>HBV\s+DNA\s+([1-9]\d{3,})<(?!\s*IU/m[lL])'),
     lambda m: f'>HBV DNA {m.group(1)} IU/mL<'),
]

# === B. TARE 이중 괄호 ===
LITERAL = [
    ('방사선색전술(경동맥방사선색전술(TARE))', '경동맥방사선색전술(TARE)'),
    ('방사선색전술 (경동맥방사선색전술(TARE))', '경동맥방사선색전술(TARE)'),
    # 가능한 다른 잔재
    ('방사선색전술(경동맥방사선색전술 (TARE))', '경동맥방사선색전술 (TARE)'),
]


def in_jsonld(text: str, pos: int) -> bool:
    """text[pos]가 <script type='application/ld+json'>...</script> 안인지."""
    starts = [m.end() for m in re.finditer(r'<script type="application/ld\+json"[^>]*>', text) if m.end() <= pos]
    if not starts:
        return False
    last_start = max(starts)
    end = text.find('</script>', last_start)
    return end == -1 or pos < end


def main():
    pages_dna = 0
    pages_tare = 0
    dna_count = 0
    tare_count = 0
    for p in ROOT.rglob('*.html'):
        if any(part in EXCLUDE_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # A) DNA 단위 보강 — JSON-LD 포함 (Google rich snippet 일관성)
        # 주의: " IU/mL" 추가는 JSON 문법 깨지 않음 (특수문자·인용부호 없음)
        for pat, repl in DNA_PATTERNS:
            new_text = []
            last = 0
            for m in pat.finditer(text):
                new_text.append(text[last:m.start()])
                new_text.append(repl(m))
                last = m.end()
                dna_count += 1
            new_text.append(text[last:])
            text = ''.join(new_text) if last > 0 else text

        if text != orig:
            pages_dna += 1

        # B) TARE
        before_tare = text
        for old, new in LITERAL:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, new)
                tare_count += n
        if text != before_tare:
            pages_tare += 1

        if text != orig:
            p.write_text(text, encoding='utf-8')

    print(f'A) DNA 단위 보강: {dna_count}건 / {pages_dna} 페이지')
    print(f'B) TARE 이중괄호 제거: {tare_count}건 / {pages_tare} 페이지')


if __name__ == '__main__':
    main()
