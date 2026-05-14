#!/usr/bin/env python3
"""표 헤더 cleanup (재실행 안전).

1. <tr><th></th><th... 형태의 빈 헤더 셀 → <tr><th scope="col">구분</th><th scope="col"...
   - screen reader 친화 + 시각적 의미 부여
2. KASL(대한간학회) → 대한간학회(KASL) (한글-영문 어순 통일)
3. 유사하게 다른 이중 약어 패턴도 동일하게 한글-영문 순서로 정렬
   - 본 스크립트는 KASL/대한간학회만 대상으로 함 (다른 패턴은 grep 후 별도 처리)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {'.git', '.tools', 'node_modules', 'private-figures', 'assets', 'guide'}


def fix_empty_th(text: str) -> tuple[str, int]:
    """빈 첫 <th></th>를 <th scope="col">구분</th>로 변경."""
    pattern = re.compile(r'<tr>\s*<th></th>(\s*<th[^>]*>)', re.IGNORECASE)
    new_text, count = pattern.subn(r'<tr><th scope="col">구분</th>\1', text)
    return new_text, count


def fix_kasl(text: str) -> tuple[str, int]:
    """KASL(대한간학회) → 대한간학회(KASL)."""
    count = text.count('KASL(대한간학회)')
    new_text = text.replace('KASL(대한간학회)', '대한간학회(KASL)')
    return new_text, count


def process(p: Path) -> tuple[int, int]:
    txt = p.read_text(encoding='utf-8')
    new_txt = txt
    new_txt, n1 = fix_empty_th(new_txt)
    new_txt, n2 = fix_kasl(new_txt)
    if new_txt != txt:
        p.write_text(new_txt, encoding='utf-8')
    return n1, n2


def main():
    total_th = 0
    total_kasl = 0
    files_changed = 0
    for p in ROOT.rglob('*.html'):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        if any(part.startswith('.') for part in p.relative_to(ROOT).parts):
            continue
        n_th, n_kasl = process(p)
        if n_th or n_kasl:
            files_changed += 1
            total_th += n_th
            total_kasl += n_kasl
            rel = p.relative_to(ROOT).as_posix()
            print(f'  [ok] {rel}: th={n_th}, kasl={n_kasl}')

    print(f'{files_changed} files changed: empty <th>={total_th}, KASL reorder={total_kasl}')


if __name__ == '__main__':
    main()
