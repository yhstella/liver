#!/usr/bin/env python3
"""Replace prose slashes with 중점(·), fix translation-style phrases.

Idempotent. Excludes:
- URL paths (케이스/, updates/)
- Drug combination names (글레카프레비르/피브렌타스비르 etc.)
- Unit fractions (정/일, 회/일, 잔/일, 병/주 etc.)
- Binary positive/negative (양/음성, 양성/음성)
"""
import re, pathlib, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Specific prose slash pairs → middle dot
SLASH_FIXES = [
    ('비만/심대사', '비만·심대사'),
    ('빌리루빈/알부민', '빌리루빈·알부민'),
    ('양성/악성', '양성·악성'),
    ('낭선종/낭선암', '낭선종·낭선암'),
    ('혈청/간 HBV DNA', '혈청·간 HBV DNA'),
    ('수혈/장기이식', '수혈·장기이식'),
    ('약/시술', '약·시술'),
    ('고/중위험', '고·중위험'),
    ('단백뇨/혈뇨', '단백뇨·혈뇨'),
    ('엔테카비어/테노포비어', '엔테카비어·테노포비어'),
    ('직접/간접', '직접·간접'),
    ('혈소판/알부민', '혈소판·알부민'),
    ('위고비/오젬픽', '위고비·오젬픽'),
    ('테르리프레신/옥트레오타이드', '테르리프레신·옥트레오타이드'),
    ('유지/증량', '유지·증량'),
    ('비알코올성/대사이상', '비알코올성·대사이상'),
    ('시롤리무스/에베롤리무스', '시롤리무스·에베롤리무스'),
    ('단일/다발', '단일·다발'),
    ('줄이기/끊기', '줄이기·끊기'),
    ('단백/크레아티닌', '단백·크레아티닌'),
    ('다파/엠파', '다파·엠파'),
    ('당뇨/고지혈증', '당뇨·고지혈증'),
    ('감량/중단', '감량·중단'),
    ('당뇨/고혈압', '당뇨·고혈압'),
    ('심근경색/뇌졸중', '심근경색·뇌졸중'),
    ('비만/당뇨', '비만·당뇨'),
    ('한약/보충제', '한약·보충제'),
    ('보상성/비대상성', '보상성·비대상성'),
    ('비리어드/베믈리디', '비리어드·베믈리디'),
]

# Translation-style Korean → natural Korean
TRANSLATION_FIXES = [
    # "필요로 한다/합니다" → "필요합니다"
    ('필요로 합니다', '필요합니다'),
    ('필요로 한다', '필요하다'),
    # "에 의하여" → "에 따라"
    ('에 의하여 ', '에 따라 '),
    # "에 의해서" → "에 따라"
    ('에 의해서 ', '에 따라 '),
    # "을 통해서" → "을 통해"
    ('을 통해서 ', '을 통해 '),
    ('를 통해서 ', '를 통해 '),
    # Double passive 되어집니다 → 됩니다
    ('되어집니다', '됩니다'),
    ('되어진다', '된다'),
    ('되어진', '된'),
    # "있어집니다" → "있습니다"
    ('있어집니다', '있습니다'),
    # "을 가지고 있습니다" → "이 있습니다"
    ('을 가지고 있습니다', '이 있습니다'),
    ('를 가지고 있습니다', '가 있습니다'),
    ('을 가지고 있다', '이 있다'),
    ('를 가지고 있다', '가 있다'),
    # "는 것이 가능합니다" → "할 수 있습니다"
    # Risk: too contextual. Skip.
    # "을 위하여" → "을 위해"
    ('을 위하여 ', '을 위해 '),
    ('를 위하여 ', '를 위해 '),
]


def fix_file(path):
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in SLASH_FIXES + TRANSLATION_FIXES:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


result = subprocess.run(['git', 'ls-files', '--', '*.html'], capture_output=True, text=True, encoding='utf-8')
files = [f for f in result.stdout.split('\n') if f and not f.startswith('updates/feed.xml')]

count = 0
for f in files:
    p = ROOT / f
    if not p.exists():
        continue
    if fix_file(p):
        count += 1

print(f'Files modified: {count}')
