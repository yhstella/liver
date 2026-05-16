#!/usr/bin/env python3
"""Fix specific awkward sentence endings and translation-style phrases.

Focused list — only clear-cut cases that improve readability without
overcorrecting intentional brevity (e.g., hub tile descriptions).
"""
import pathlib, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Specific full-paragraph awkward endings → fixed
FIXES = [
    # Case narratives — full sentences cut off in noun form
    ('TAF로의 전환 결정.', 'TAF로의 전환을 결정했습니다.'),
    ('SBRT 전환 검토.', 'SBRT 전환을 검토합니다.'),
    ('이식 전 평가에서 평생 예방 필요로 결정.', '이식 전 평가에서 평생 예방이 필요하다고 결정했습니다.'),
    ('수직감염 없음 확인.', '수직감염이 없음을 확인했습니다.'),
    ('위소매절제술(sleeve gastrectomy) 결정.', '위소매절제술(sleeve gastrectomy)을 결정했습니다.'),
    ('환자별 결정.', '환자별로 결정합니다.'),
    ('다음 단계는 섬유화 단계 평가.', '다음 단계는 섬유화 단계를 평가합니다.'),
    ('Fibroscan으로 확인.', 'Fibroscan으로 확인합니다.'),
    ('근육 기원 우선 — 횡문근융해, 다발근염, 스타틴 부작용.', '근육 기원을 먼저 의심합니다 — 횡문근융해, 다발근염, 스타틴 부작용 등입니다.'),
    ('AST 단독 ↑이면 거의 무조건 근육 평가.', 'AST만 단독으로 오르면 거의 대부분 근육 원인을 먼저 평가합니다.'),
    ('직접 비교 데이터는 없어 부작용·환자 선호로 결정.', '직접 비교 데이터가 없어 부작용·환자 선호로 결정합니다.'),
    ('의료기관 약사 평가.', '의료기관 약사와 함께 평가합니다.'),
    ('Darunavir/cobicistat은 글레카프레비르와 상호작용 가능 — 의료기관 약사 평가.',
     'Darunavir/cobicistat은 글레카프레비르와 상호작용이 있을 수 있어 의료기관 약사와 함께 평가합니다.'),
    ('LDLT 검토.', 'LDLT를 검토합니다.'),
    ('이때 면역치료(EMERALD-1 결과 적용) 또는 SBRT 전환 검토.',
     '이때 면역치료(EMERALD-1 결과 적용) 또는 SBRT 전환을 검토합니다.'),

    # Translation-style 강압 표현 → 부드러운 표현
    ('반드시 알려야 합니다.', '담당 의사에게 꼭 알려 주세요.'),
    ('반드시 확인해야 합니다.', '꼭 확인합니다.'),
    ('반드시 진료를 통해 의료진과 상의하시기 바랍니다.',
     '진료를 통해 의료진과 상의하시기 바랍니다.'),

    # 번역체 명백한 사례
    ('SVR에도 불구하고', 'SVR 도달 후에도'),
    ('흡연력에도 불구하고', '흡연력이 있었으나'),
    ('할 수 있다는 점이 ', '한다는 점이 '),

    # 명사형 마침표 미세 보강 — case 페이지에서 자주 등장하는 표현
    ('가능하면 조직 호전 확인 후', '가능하면 조직 호전을 확인한 뒤 결정합니다'),

    # AIH-약중단 case
    ('환자와 충분히 합의 후 결정', '환자와 충분히 합의한 뒤 결정합니다'),
    ('본인의 일상·임신 계획·생활을 종합해 함께 결정', '본인의 일상·임신 계획·생활을 종합해 함께 결정합니다'),
    ('재발은 무증상으로 발견되는 경우가 흔하다 — 정기 외래가 결정적',
     '재발은 무증상으로 발견되는 경우가 흔합니다 — 정기 외래가 결정적입니다'),
    ('저용량(Pred 5 + 아자티오프린(AZA) 75) 유지의 누적 부작용은 적은 편',
     '저용량(Pred 5 + 아자티오프린(AZA) 75) 유지의 누적 부작용은 적은 편입니다'),
    ('1년 시점 ALT 18, IgG 13, 골밀도 정상 유지, 일상 활동에 지장 없음.',
     '1년 시점에 ALT 18, IgG 13, 골밀도가 정상으로 유지되었고 일상 활동에 지장이 없었습니다.'),

    # B형간염-간암검진 — long sentence fragment
    ('이런 경우 동적 CT 또는 MRI(특히 MRI)로 보완.',
     '이런 경우 동적 CT 또는 MRI로 보완합니다.'),
]


def fix_file(path):
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in FIXES:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


result = subprocess.run(['git', 'ls-files', '--', '*.html'], capture_output=True, text=True, encoding='utf-8')
files = [f for f in result.stdout.split('\n') if f]

count = 0
for f in files:
    p = ROOT / f
    if not p.exists():
        continue
    if fix_file(p):
        count += 1

print(f'Files modified: {count}')
