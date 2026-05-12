#!/usr/bin/env python3
"""세부주제 톤 wave 3.

규칙:
  1. 간세포암 → 간암 (body text 사용; 정의문 '간세포암(HCC)' 등은 보존)
  2. 잔여 '한국 X' 패턴 제거 (한글 자료에 굳이 한국 안 붙임)
  3. 30초 요약·짧은 박스 반말 → 존댓말 (개별 케이스로 등록)
  4. 근거 없는 단정 표현 톤다운
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','간양성종양',
    '케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search',
    '.tools','.git','.github','private-figures','node_modules',
}

# --- 1) 간세포암 → 간암 (body text only) ---
# Korean particles after 간세포암 = body text reference
PARTICLES = ['의', '을', '를', '이', '가', '에', '에서', '에는', '에도', '으로', '은', '는', '과', '와']
# 간세포암 + space + common nouns → 간암 + space + same
BODY_NOUNS = ['환자', '진단', '발생', '발견', '위험', '치료', '검진', '추적', '예후', '재발',
              '검출', '조기', '진행', '병기', '병태', '경로']
# 간세포암 + 한 + ...
TRAILING_HAN = ['한 ', '하면', '하고']

# --- 2) 잔여 한국 패턴 ---
KOR_DROPS = [
    ('한국 검진 시작', '검진 시작'),
    ('한국 간암', '국내 간암'),
    ('한국 의료기관', '국내 의료기관'),
    ('한국 가이드라인', '국내 가이드라인'),
    ('한국 환자에', '국내 환자에'),
    ('한국 간학회', '대한간학회'),
    ('한국 KASL', 'KASL'),
    ('한국 KLCA', 'KLCA'),
    ('한국 NCC', 'NCC'),
    ('한국 LDLT', '국내 LDLT'),
    ('한국 KONOS', 'KONOS'),
    ('한국 B형간염', '국내 B형간염'),
    ('한국 보건의료', '국내 보건의료'),
    ('한국에서 자주', '외래에서 자주'),
    ('한국에서 임상', '국내 임상'),
]

# --- 3) 30초 요약 반말 → 존대 (이미 5개 직접 수정 — 추가 발견 시 등록) ---
# (현재 5개 외 케이스 없음 — wave 4에서 확장)

# --- 4) AI/근거 없는 단정 ---
AI_PHRASES = [
    # 자주 보이는 AI 문구
    ('명확히 설명하는 것이 표준입니다.', '"왜 이 치료로 정했는지" 외래에서 설명드리는 것이 원칙입니다.'),
    ('명확히 설명하는 것이 원칙입니다.', '"왜 이 치료로 정했는지" 외래에서 설명드리는 것이 원칙입니다.'),
    ('근거가 됩니다.', '근거로 활용합니다.'),
    ('큰 문제 없음.', '대체로 큰 영향은 없습니다.'),
    ('큰 문제 없음', '대체로 큰 영향은 없습니다'),
    ('실제 임상에서는', '외래 진료에서는'),
    ('실제 진료에서는', '외래 진료에서는'),
]


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in EXCLUDE and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx


def soft_replace_hcc(text: str) -> tuple[str, int]:
    """간세포암 → 간암 (body text). 정의문 '간세포암(HCC)', '간세포암 (HCC)' 등은 보존."""
    count = 0

    # 1. Particles: 간세포암의/을/이/가/에/에서/...
    for p in PARTICLES:
        old = f'간세포암{p}'
        new = f'간암{p}'
        n = text.count(old)
        if n > 0:
            text = text.replace(old, new)
            count += n
    # 2. Common nouns with space: 간세포암 환자, 간세포암 진단 ...
    for n_word in BODY_NOUNS:
        old = f'간세포암 {n_word}'
        new = f'간암 {n_word}'
        n = text.count(old)
        if n > 0:
            text = text.replace(old, new)
            count += n
    # 3. 간세포암 + (한 가지|하면|...) 등 동사 시작
    for trail in TRAILING_HAN:
        old = f'간세포암{trail}'
        new = f'간암{trail}'
        n = text.count(old)
        if n > 0:
            text = text.replace(old, new)
            count += n
    return text, count


def main():
    pages = 0
    by_rule = {'간세포암→간암 (body)': 0}
    for f in detail_pages():
        text = f.read_text(encoding='utf-8')
        orig = text

        text, hcc_n = soft_replace_hcc(text)
        if hcc_n > 0:
            by_rule['간세포암→간암 (body)'] += hcc_n

        for old, repl in KOR_DROPS:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, repl)
                by_rule[f'한국: {old}'] = by_rule.get(f'한국: {old}', 0) + n
        for old, repl in AI_PHRASES:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, repl)
                by_rule[f'AI: {old[:30]}'] = by_rule.get(f'AI: {old[:30]}', 0) + n

        if text != orig:
            f.write_text(text, encoding='utf-8')
            pages += 1

    print(f'Pages changed: {pages}\n')
    for rule, count in sorted(by_rule.items(), key=lambda x: -x[1]):
        if count == 0:
            continue
        print(f'  {count:4d} × {rule}')


if __name__ == '__main__':
    main()
