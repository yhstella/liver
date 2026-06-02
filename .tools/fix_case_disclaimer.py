#!/usr/bin/env python3
"""
fix_case_disclaimer.py — Replace "anonymized real patient" disclaimers on case
pages with an honest "constructed teaching example" disclaimer.

The 케이스/ pages are typical-scenario illustrations of guideline application
(built by build_cases*.py), not records of real anonymized patients. The old
disclaimers ("환자 정보는 익명화 처리되었습니다" / "식별을 위해 모두 변경되었으며")
implied a real patient existed, which is inaccurate and manufactures false trust.

Idempotent: only replaces the two known old strings.

Usage:
  python .tools/fix_case_disclaimer.py
  python .tools/fix_case_disclaimer.py --dry-run
"""
from __future__ import annotations
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / '케이스'

OLD = [
    "환자 정보는 익명화 처리되었습니다. 임상 결정은 표준 가이드라인 적용의 한 예시이며, 개별 환자에게 그대로 적용되지는 않습니다.",
    "환자 정보는 식별을 위해 모두 변경되었으며, 임상 결정은 표준 가이드라인의 한 예시일 뿐 개별 환자에게 그대로 적용되지 않습니다.",
]
NEW = "이 사례는 표준 진료 흐름을 보여주기 위해 구성한 교육용 예시이며, 특정 환자의 기록이 아닙니다. 실제 진료는 개인의 상태에 따라 달라집니다."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if not CASES.exists():
        print('케이스/ not found')
        return

    pages = 0
    total = 0
    for idx in sorted(CASES.glob('*/index.html')):
        text = idx.read_text(encoding='utf-8')
        n = sum(text.count(o) for o in OLD)
        if n == 0:
            continue
        if args.dry_run:
            print(f'  would fix {n}x: {idx.parent.name}')
            pages += 1
            total += n
            continue
        new = text
        for o in OLD:
            new = new.replace(o, NEW)
        idx.write_text(new, encoding='utf-8', newline='')
        print(f'  fixed {n}x: {idx.parent.name}')
        pages += 1
        total += n

    verb = 'would fix' if args.dry_run else 'fixed'
    print(f'\n{verb} {total} disclaimer strings across {pages} case pages')


if __name__ == '__main__':
    main()
