#!/usr/bin/env python3
"""사이트 모든 페이지 헤더에 site-search 박스 + search.js 스크립트 삽입."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Marker for search box (inside site-nav)
SEARCH_HTML = '''<form id="site-search" role="search" autocomplete="off" onsubmit="return false">
        <span class="search-icon" aria-hidden="true"><svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="6"/><line x1="13.5" y1="13.5" x2="17.5" y2="17.5"/></svg></span>
        <input class="search-input" type="search" placeholder="검색" aria-label="사이트 검색">
        <div class="search-panel">
          <div class="search-hits"></div>
          <ul class="search-results" role="listbox"></ul>
          <div class="search-status">↑↓ 이동 · Enter 열기 · Esc 닫기</div>
        </div>
      </form>'''

# Insertion point: before <nav class="site-nav">
NAV_RE = re.compile(r'(\s*)(<nav class="site-nav">)')

SCRIPT_TAG = '<script src="/assets/js/search.js" defer></script>'

SKIP_DIRS = {'.git', '.tools', 'node_modules', 'private-figures', 'assets'}


def main():
    pages = 0
    for p in ROOT.rglob('*.html'):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        text = p.read_text(encoding='utf-8')
        if 'id="site-search"' in text and SCRIPT_TAG in text:
            continue
        changed = False
        # Insert search form before site-nav
        if 'id="site-search"' not in text:
            new = NAV_RE.sub(r'\1' + SEARCH_HTML + r'\1\2', text, count=1)
            if new != text:
                text = new
                changed = True
        # Add script tag to head (before </head>)
        if SCRIPT_TAG not in text:
            text = text.replace('</head>', SCRIPT_TAG + '\n</head>', 1)
            changed = True
        if changed:
            p.write_text(text, encoding='utf-8')
            pages += 1
    print(f'Pages updated: {pages}')


if __name__ == '__main__':
    main()
