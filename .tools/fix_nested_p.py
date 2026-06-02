#!/usr/bin/env python3
"""
fix_nested_p.py — Collapse invalid `<p><p>...</p></p>` nesting in FAQ blocks.

These came from a build step that wrapped already-`<p>`-wrapped FAQ answers in
another `<p>`. Browsers auto-correct, but the DOM is invalid and JSON-LD
regeneration can lose content. Fix is idempotent: only collapses doubled tags.

Per page the count of `<p><p>` equals the count of `</p></p>`, so a plain
literal replace is safe.

Usage:
  python .tools/fix_nested_p.py            # fix all index.html
  python .tools/fix_nested_p.py --dry-run  # report only
"""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {'.git', '.tools', 'assets', 'guide', 'private-figures', 'node_modules'}


def collect_pages():
    for p in ROOT.rglob('index.html'):
        rel = p.relative_to(ROOT)
        if any(part in SKIP or part.startswith('.') for part in rel.parts):
            continue
        yield p


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    total_pages = 0
    total_fixes = 0
    for path in collect_pages():
        text = path.read_text(encoding='utf-8')
        open_n = text.count('<p><p>')
        close_n = text.count('</p></p>')
        if open_n == 0 and close_n == 0:
            continue
        if open_n != close_n:
            print(f'  SKIP (unbalanced {open_n} open / {close_n} close): {path.relative_to(ROOT)}')
            continue
        rel = str(path.relative_to(ROOT)).replace('\\', '/')
        if args.dry_run:
            print(f'  would fix {open_n}x: {rel}')
            total_pages += 1
            total_fixes += open_n
            continue
        new = text.replace('<p><p>', '<p>').replace('</p></p>', '</p>')
        path.write_text(new, encoding='utf-8', newline='')
        print(f'  fixed {open_n}x: {rel}')
        total_pages += 1
        total_fixes += open_n

    verb = 'would fix' if args.dry_run else 'fixed'
    print(f'\n{verb} {total_fixes} nested-p occurrences across {total_pages} pages')


if __name__ == '__main__':
    main()
