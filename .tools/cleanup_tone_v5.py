#!/usr/bin/env python3
"""세부주제 톤·표기 wave 5.

A. 생검 → 조직검사 (조사·문맥별 매칭, URL/슬러그는 보호)
B. 가돌리늄 MRI → MRI (헷갈림 방지)
C. second opinion / Second opinion → 다른 의견
D. '환자가 권리' / '환자의 권리' → '환자분의 권리'
E. 특정 병원명 list 제거 (서울대·삼성·아산·세브란스 등)
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {'.git','.tools','node_modules','private-figures','assets','guide'}

# === A. 생검 → 조직검사 ===
# URL은 href="/간생검..." 같은 경로 — 보존 위해 href= 컨텍스트는 skip 안전
# 가장 안전한 방법: 명사·조사 패턴으로 구체화
SAENGGEOM = [
    # 정확한 phrase
    ('조직 생검', '조직검사'),
    ('생검 없이', '조직검사 없이'),
    ('생검 없는', '조직검사 없는'),
    ('생검 후', '조직검사 후'),
    ('생검 직후', '조직검사 직후'),
    ('생검 전', '조직검사 전'),
    ('생검 추가', '조직검사 추가'),
    ('생검 검토', '조직검사 검토'),
    ('생검 결과', '조직검사 결과'),
    ('생검을 추가', '조직검사를 추가'),
    ('생검을 시행', '조직검사를 시행'),
    ('생검을 검토', '조직검사를 검토'),
    ('생검을 통해', '조직검사를 통해'),
    ('생검은 ', '조직검사는 '),
    ('생검이 ', '조직검사가 '),
    ('생검과 ', '조직검사와 '),
    ('생검에서 ', '조직검사에서 '),
    ('생검에 ', '조직검사에 '),
    ('생검·', '조직검사·'),
    (' 생검 ', ' 조직검사 '),
    (' 생검,', ' 조직검사,'),
    (' 생검.', ' 조직검사.'),
    (' 생검)', ' 조직검사)'),
    ('(생검)', '(조직검사)'),
    ('또는 생검', '또는 조직검사'),
    ('필요시 생검', '필요시 조직검사'),
    # 영문 'liver biopsy' 같은 건 그대로 둠 (전문 용어)
]

# === B. 가돌리늄 MRI → MRI ===
GADO = [
    ('가돌리늄 MRI', 'MRI'),
]

# === C. second opinion → 다른 의견 ===
SECOND = [
    ('second opinion', '다른 의견'),
    ('Second opinion', '다른 의견'),
    ('second-opinion', '다른 의견'),
    ('Second-opinion', '다른 의견'),
]

# === D. 환자가/의 권리 → 환자분의 권리 ===
PATIENT_RIGHT = [
    ('환자가 권리', '환자분의 권리'),
    ('환자의 권리', '환자분의 권리'),
]

# === E. 특정 병원명 list 제거 ===
HOSPITAL_LISTS = [
    # 1-1 FAQ 패턴
    ('대형 간센터(서울대병원·삼성서울·아산병원·세브란스 등)는 다학제 평가 경험이 풍부합니다.', ''),
    ('대형 간센터(서울대병원·삼성서울·아산병원·세브란스 등)는 다학제 평가 경험이 풍부합니다', ''),
    ('대형 간센터(서울대병원·삼성서울·아산병원·세브란스 등)', '간 전문 진료가 가능한 의료기관'),
    # 다른 형식들 (functional-cure 등)
    ('서울대병원·삼성서울·아산병원·세브란스', '주요 간 전문 의료기관'),
    ('서울대학교병원·삼성서울·아산병원·세브란스', '주요 간 전문 의료기관'),
    ('서울대·삼성·아산·세브란스', '주요 간 전문 의료기관'),
    ('서울대병원, 삼성서울, 아산병원, 세브란스', '주요 간 전문 의료기관'),
]


def detail_pages():
    for p in ROOT.rglob('*.html'):
        if any(part in EXCLUDE_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        yield p


def main():
    counts = {'생검→조직검사': 0, '가돌리늄 MRI→MRI': 0, 'second opinion→다른 의견': 0,
              '환자_권리': 0, '병원list 제거': 0}
    pages_changed = 0

    for f in detail_pages():
        text = f.read_text(encoding='utf-8')
        orig = text
        # A
        for old, new in SAENGGEOM:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, new)
                counts['생검→조직검사'] += n
        # B
        for old, new in GADO:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, new)
                counts['가돌리늄 MRI→MRI'] += n
        # C
        for old, new in SECOND:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, new)
                counts['second opinion→다른 의견'] += n
        # D
        for old, new in PATIENT_RIGHT:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, new)
                counts['환자_권리'] += n
        # E
        for old, new in HOSPITAL_LISTS:
            n = text.count(old)
            if n > 0:
                text = text.replace(old, new)
                counts['병원list 제거'] += n

        if text != orig:
            f.write_text(text, encoding='utf-8')
            pages_changed += 1

    print(f'Pages changed: {pages_changed}')
    for k, v in counts.items():
        print(f'  {k}: {v}건')


if __name__ == '__main__':
    main()
