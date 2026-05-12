#!/usr/bin/env python3
"""세부주제 페이지 톤·표기 정리.

규칙:
  1. 이중 괄호 번역 정리:
     - 'X(X-한글, X-한글(영어))' 패턴 → 'X (한글, 영어)'
     - 동일 단어 반복 '경동맥화학색전술(경동맥화학색전술(TACE))' → '경동맥화학색전술(TACE)'
  2. 외래어 표기 통일:
     - 'Gd-EOB-MRI' → '가돌리늄 MRI'
  3. SNUH 비보유 옵션 제거:
     - 다학제 list에서 'SBRT·양성자' → 'SBRT'
     - 'SBRT, 양성자' → 'SBRT'
  4. '한국에서는' 톤 다운 (특정 패턴만):
     - '한국에서는 일부 절제·SBRT 검토' → '절제 또는 SBRT 고려 가능'
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','간양성종양',
    '케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search',
    '.tools','.git','.github','private-figures','node_modules',
}

# 직접 치환 (사이트 전체 적용 안전한 것만)
SIMPLE_REPLACES = [
    # 표기 통일
    ('Gd-EOB-MRI', '가돌리늄 MRI'),
    ('EOB-MRI', '가돌리늄 MRI'),

    # 이중 괄호 반복 (동일 단어 반복)
    ('간암(간세포암, 간세포암(HCC))', '간암 (간세포암, HCC)'),
    ('간세포암(간세포암(HCC))', '간세포암 (HCC)'),
    ('조영 초음파(조영초음파(CEUS))', '조영초음파(CEUS)'),
    ('조영초음파(조영초음파(CEUS))', '조영초음파(CEUS)'),
    ('경동맥화학색전술(경동맥화학색전술(TACE))', '경동맥화학색전술(TACE)'),
    ('고주파열치료술(고주파열치료술(RFA))', '고주파열치료술(RFA)'),
    ('마이크로웨이브(마이크로웨이브(MWA))', '마이크로웨이브(MWA)'),
    ('정위적 체부 방사선치료(정위적 체부 방사선치료(SBRT))', '정위적 체부 방사선치료(SBRT)'),
    ('대사이상지방간질환(대사이상지방간질환(MASLD))', '대사이상지방간질환(MASLD)'),
    ('대사이상지방간염(대사이상지방간염(MASH))', '대사이상지방간염(MASH)'),
    ('알라닌 아미노전이효소(알라닌 아미노전이효소(ALT))', '알라닌 아미노전이효소(ALT)'),
    ('아스파테이트 아미노전이효소(아스파테이트 아미노전이효소(AST))', '아스파테이트 아미노전이효소(AST)'),

    # 자가면역
    ('자가면역간염(자가면역간염(AIH))', '자가면역간염(AIH)'),
    ('원발 담즙성 담관염(원발 담즙성 담관염(PBC))', '원발 담즙성 담관염(PBC)'),
    ('원발 경화성 담관염(원발 경화성 담관염(PSC))', '원발 경화성 담관염(PSC)'),

    # 한국 KLCA-NCC 표현 단순화
    ('한국 KLCA(대한간암학회)-NCC', '대한간암학회(KLCA)-국립암센터(NCC)'),
    ('KLCA(대한간암학회)-NCC', '대한간암학회(KLCA)-국립암센터(NCC)'),

    # 다학제 리스트에서 양성자 빼기 (정확 패턴만)
    ('정위적 체부 방사선치료(SBRT)·양성자', '정위적 체부 방사선치료(SBRT)'),
    ('정위적 체부 방사선치료(SBRT) · 양성자', '정위적 체부 방사선치료(SBRT)'),
    ('SBRT·양성자', 'SBRT'),
    ('SBRT, 양성자', 'SBRT'),
    ('SBRT 및 양성자', 'SBRT'),

    # 'BCLC B → ..., 한국에서는 일부 절제·SBRT 검토' → '절제나 SBRT 고려 가능'
    ('한국에서는 일부 절제·SBRT 검토', '절제나 SBRT 고려 가능'),
    ('한국에서는 일부 절제 · SBRT 검토', '절제나 SBRT 고려 가능'),
    ('한국에서는 절제·SBRT 검토', '절제나 SBRT 고려 가능'),

    # 'PT(프로트롬빈 시간)(PT(프로트롬빈 시간))' 같은 가능한 사례
    ('PT(프로트롬빈 시간)(프로트롬빈 시간)', 'PT(프로트롬빈 시간)'),
]


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in EXCLUDE and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx


def main():
    changed = 0
    by_rule = {}
    for f in detail_pages():
        text = f.read_text(encoding='utf-8')
        new = text
        for old, repl in SIMPLE_REPLACES:
            if old in new:
                n = new.count(old)
                new = new.replace(old, repl)
                by_rule[old] = by_rule.get(old, 0) + n
        if new != text:
            f.write_text(new, encoding='utf-8')
            changed += 1
    print(f'Pages changed: {changed}\n')
    for rule, count in sorted(by_rule.items(), key=lambda x: -x[1]):
        if count:
            print(f'  {count:3d} × "{rule[:50]}{"…" if len(rule)>50 else ""}"')


if __name__ == '__main__':
    main()
