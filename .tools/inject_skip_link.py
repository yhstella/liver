#!/usr/bin/env python3
"""모든 페이지 <body> 직후에 skip-to-content 링크 + <main>에 id='content' 추가.

a11y 표준: 키보드 사용자가 nav를 건너뛰고 본문으로 바로 이동.
이미 있으면 skip.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'.git','.tools','node_modules','private-figures','assets'}

SKIP_LINK = '<a class="skip-link" href="#content">본문 바로가기</a>'
BODY_RE = re.compile(r'(<body[^>]*>)')
MAIN_RE = re.compile(r'<main(\s[^>]*)?>')


def main():
    skip = 0
    main_id = 0
    for p in ROOT.rglob('*.html'):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # 1. <body> 직후 skip-link 추가
        if 'class="skip-link"' not in text:
            text = BODY_RE.sub(r'\1\n' + SKIP_LINK, text, count=1)
            skip += 1
        # 2. <main>에 id="content" 추가 (없으면)
        m = MAIN_RE.search(text)
        if m and 'id=' not in m.group(0):
            old_main = m.group(0)
            attrs = m.group(1) or ''
            new_main = f'<main id="content"{attrs}>'
            text = text.replace(old_main, new_main, 1)
            main_id += 1
        if text != orig:
            p.write_text(text, encoding='utf-8')
    print(f'skip-link added: {skip}')
    print(f'main id added: {main_id}')


if __name__ == '__main__':
    main()
