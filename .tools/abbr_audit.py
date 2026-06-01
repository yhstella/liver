#!/usr/bin/env python3
"""
abbr_audit.py — Per-page audit: which abbreviations from abbreviations.json appear
WITHOUT an inline Korean gloss on first mention?

Reports only — does NOT modify pages. Used to track progress on hybrid abbreviation policy.

Heuristic:
- Read all index.html pages (excluding .git, .tools, assets, guide, private-figures).
- For each abbreviation in abbreviations.json, check whether the page contains it.
- Determine "first mention has a gloss" by looking for either:
    1. `<abbr title=` wrapping the term, OR
    2. The term followed within ~30 chars by `(한글...)` containing Korean characters
       OR by the literal Korean gloss listed in abbreviations.json.
- A page is "covered" for that abbreviation if either is true.

Output: JSON report at .tools/abbr_audit_report.json with per-page lists of
uncovered abbreviations, and a global frequency table of uncovered occurrences.
"""
from __future__ import annotations
import json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ABBR_FILE = ROOT / '.tools' / 'abbreviations.json'
OUT = ROOT / '.tools' / 'abbr_audit_report.json'

SKIP = {'.git', '.tools', 'assets', 'guide', 'private-figures', 'node_modules'}

KOREAN_RE = re.compile(r'[가-힣]')


def load_abbrs():
    data = json.loads(ABBR_FILE.read_text(encoding='utf-8'))
    return {k: v for k, v in data.items() if not k.startswith('_')}


def collect_pages():
    for path in ROOT.rglob('index.html'):
        rel = path.relative_to(ROOT)
        if any(p in SKIP or p.startswith('.') for p in rel.parts):
            continue
        yield path


def strip_head_and_scripts(html: str) -> str:
    """Return body-ish text by stripping head, scripts, styles, and JSON-LD."""
    html = re.sub(r'<head[\s\S]*?</head>', '', html, flags=re.I)
    html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.I)
    html = re.sub(r'<style[\s\S]*?</style>', '', html, flags=re.I)
    return html


def first_mention_covered(body: str, term: str, gloss: str) -> bool:
    """Return True if first occurrence of `term` is followed by an inline gloss or wrapped in <abbr>."""
    # Look for first occurrence
    idx = body.find(term)
    if idx < 0:
        return True  # not on this page, trivially covered
    # Check if wrapped in <abbr title="..."> by looking back ~40 chars
    back = body[max(0, idx - 60):idx]
    if 'abbr title' in back:
        return True
    # Check ~40 chars after for gloss
    fwd = body[idx + len(term): idx + len(term) + 50]
    if fwd.lstrip().startswith('('):
        inside = fwd[fwd.find('(') + 1: fwd.find(')')] if ')' in fwd else ''
        if KOREAN_RE.search(inside):
            return True
    # Also check whether literal gloss text appears within 40 chars
    if gloss[:8] in fwd:
        return True
    return False


def main():
    abbrs = load_abbrs()
    by_page = {}
    freq = defaultdict(int)
    for path in collect_pages():
        try:
            html = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        body = strip_head_and_scripts(html)
        rel = str(path.relative_to(ROOT)).replace('\\', '/')
        uncovered = []
        for term, gloss in abbrs.items():
            if term not in body:
                continue
            if not first_mention_covered(body, term, gloss):
                uncovered.append(term)
                freq[term] += 1
        if uncovered:
            by_page[rel] = uncovered

    report = {
        'totalAbbreviations': len(abbrs),
        'pagesWithUncovered': len(by_page),
        'frequency': dict(sorted(freq.items(), key=lambda x: -x[1])),
        'byPage': by_page,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Pages with uncovered abbreviations: {len(by_page)}')
    print('Top uncovered abbreviations (frequency):')
    for term, count in list(report['frequency'].items())[:15]:
        print(f'  {term}: {count} pages')
    print(f'\nFull report: .tools/abbr_audit_report.json')


if __name__ == '__main__':
    main()
