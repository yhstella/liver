#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""푸터 '안내' 컬럼 끝에 /문의/ 링크를 idempotent하게 삽입.

라이브 *.html 과 빌드 스크립트(.tools/build_*.py)의 푸터 문자열을 모두 처리한다.
'<strong>안내</strong>' 는 푸터에만 등장하므로 헤더 nav 의 동일 링크와 충돌하지 않는다.
이미 /문의/ 가 안내 컬럼에 있으면 건너뛴다(재실행 안전).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# <strong>안내</strong> 뒤로 이어지는 <a>...</a> 묶음을 잡고, 닫는 </div> 직전에 삽입
PAT = re.compile(r'(<strong>안내</strong>(?:\s*<a\b[^>]*>.*?</a>)+)(\s*</div>)', re.DOTALL)
LINK = '<a href="/문의/">문의</a>'


def patch(text: str) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        col = m.group(1)
        if '/문의/' in col:          # 이미 있음 → 그대로
            return m.group(0)
        n += 1
        return col + LINK + m.group(2)

    return PAT.sub(repl, text), n


def iter_targets():
    skip = {'.git', 'private-figures', 'node_modules', '__pycache__'}
    for p in ROOT.rglob('*.html'):
        if any(part in skip for part in p.parts):
            continue
        yield p
    for p in (ROOT / '.tools').glob('build_*.py'):
        yield p


def main():
    changed = 0
    total_links = 0
    for p in iter_targets():
        try:
            text = p.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        if '<strong>안내</strong>' not in text:
            continue
        new, n = patch(text)
        if n:
            p.write_text(new, encoding='utf-8')
            changed += 1
            total_links += n
            print(f'  + {p.relative_to(ROOT)}  ({n})')
    print(f'\n총 {changed}개 파일에 문의 링크 {total_links}개 삽입.')


if __name__ == '__main__':
    main()
