"""Build 15 case pages for 간암 series + /케이스/ landing page.

Page IDs: 1-12 through 1-26 (continuing from 간암 series topics 1-1..1-11).
Tone: formal -입니다 / -했습니다.
No 가상 케이스 badge, no CASE numbering, no 진단/치료 split.
Anonymization disclaimer only at bottom.
"""
import sys, os, re, html as htmllib
sys.path.insert(0, os.path.dirname(__file__))
from pathlib import Path
from case_figures import CASE_FIGURES

ROOT = Path(__file__).resolve().parent.parent
def esc(s): return htmllib.escape(s or "")

NAV = '''<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></nav></div></header>'''
FOOTER = '''<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>'''

ANONYMIZATION_NOTE = (
    '<p class="disclaimer" style="margin-top:48px">본 케이스는 외래에서 자주 만나는 임상 케이스를 '
    '익명화하여 재구성한 교육 자료입니다. 환자 식별 정보는 모두 변경되었으며, 임상 결정은 표준 가이드라인의 한 예시일 뿐 '
    '개별 환자에 그대로 적용되지 않습니다.</p>'
)

# === Tone normalization (~어요/~예요 → ~었습니다/~입니다) ===
SUBS = [
    ("들고 오셨어요", "들고 오셨습니다"),
    ("받으셨어요", "받으셨습니다"),
    ("받으셨었어요", "받으셨습니다"),
    ("퇴원하셨어요", "퇴원하셨습니다"),
    ("놀라셨어요", "놀라셨습니다"),
    ("올랐어요", "올랐습니다"),
    ("떨어졌어요", "떨어졌습니다"),
    ("나왔어요", "나왔습니다"),
    ("발견됐어요", "발견되었습니다"),
    ("발견됐고", "발견되었고"),
    ("발견됐", "발견되었"),
    ("좋아졌어요", "좋아졌습니다"),
    ("끝났어요", "끝났습니다"),
    ("오셨어요", "오셨습니다"),
    ("질문이었어요", "질문이었습니다"),
    ("이번이었어요", "이번이었습니다"),
    ("보였어요", "보였습니다"),
    ("들렀어요", "들렀습니다"),
    ("올라요", "오릅니다"),
    ("올라가요", "올라갑니다"),
    ("내려가요", "내려갑니다"),
    ("바뀌어요", "바뀝니다"),
    ("바뀝니다", "바뀝니다"),
    ("바꿉니다", "바꿉니다"),
    ("필요해요", "필요합니다"),
    ("가능해요", "가능합니다"),
    ("결정해요", "결정합니다"),
    ("시작해요", "시작합니다"),
    ("좋아요", "좋습니다"),
    ("나빠요", "나쁩니다"),
    ("괜찮아요", "괜찮습니다"),
    ("아니에요?", "아닙니까?"),
    ("아니에요.", "아닙니다."),
    ("아니에요", "아닙니다"),
    ("이에요?", "입니까?"),
    ("이에요.", "입니다."),
    ("이에요", "입니다"),
    ("거예요?", "것입니까?"),
    ("거예요.", "것입니다."),
    ("거예요", "것입니다"),
    ("회색지대예요", "회색지대입니다"),
    ("좋은 시작점이에요", "좋은 시작점입니다"),
    ("적예요", "적습니다"),
    ("크예요", "큽니다"),
    ("있어요?", "있습니까?"),
    ("있어요.", "있습니다."),
    ("있어요", "있습니다"),
    ("없어요?", "없습니까?"),
    ("없어요.", "없습니다."),
    ("없어요", "없습니다"),
    ("있으세요", "있으십니다"),
    ("없으세요", "없으십니다"),
    ("그러세요", "그러십니다"),
    ("궁금해 하세요", "궁금해 하십니다"),
    ("불안해하세요", "불안해 하십니다"),
    ("불안해 하세요", "불안해 하십니다"),
    ("궁금해하세요", "궁금해 하십니다"),
    ("받으세요", "받으십니다"),
    ("드세요", "드십니다"),
    ("계세요", "계십니다"),
    ("주세요", "주십시오"),
    ("말씀하세요", "말씀하십니다"),
    ("질문하세요", "질문하십니다"),
    ("받으셨", "받으셨"),
    ("진단됐어요", "진단되었습니다"),
    ("진단됐", "진단되었"),
    ("적용됐어요", "적용되었습니다"),
    ("시행됐어요", "시행되었습니다"),
    ("시행됐", "시행되었"),
    ("바뀌었어요", "바뀌었습니다"),
    ("바뀌었", "바뀌었"),
    ("듣고 있음", "잘 듣고 있는 상태"),
    ("느껴요", "느낍니다"),
    ("받아요", "받습니다"),
    ("줘요", "줍니다"),
    ("드려요", "드립니다"),
    ("말해요", "말합니다"),
    ("말씀드려요", "말씀드립니다"),
    ("같아요", "같습니다"),
    ("아세요?", "아십니까?"),
    ("모르세요", "모르십니다"),
    ("선호해요", "선호합니다"),
    ("기억 없음", "기억은 없으십니다"),
]


def formalize(s: str) -> str:
    out = s
    for a, b in SUBS:
        out = out.replace(a, b)
    return out


# === CASES ===
CASES = []

CASES.append({
    "slug": "건강검진-우연발견-1cm결절",
    "title": "건강검진에서 우연히 발견된 1cm 결절",
    "intro": (
        "<p>52세 남성 회사원 환자입니다. BMI 25로 비만 범위는 아니며, 음주와 약물 복용은 없습니다. "
        "직장 건강검진에서 시행한 복부 초음파에서 우엽에 약 1.0 cm 크기의 저에코 결절이 우연히 발견되어 "
        "정밀검사 권유 소견으로 외래에 내원하셨습니다. 과거 B형간염 검사를 받은 기억은 없으십니다.</p>"
    ),
    "sections": [
        ("첫 만남",
         "<p>증상은 전혀 없으십니다. 가족력도 특별한 것이 없으십니다. 몸이 무겁거나 배가 부른 느낌도 없고, 식욕도 정상입니다. "
         "이런 경우 외래에서 가장 먼저 확인하는 것은 두 가지입니다. <strong>위험 인자가 있는가</strong>(B형/C형 간염, 간경변, 음주, 가족력)와 "
         "<strong>이 결절이 무엇으로 보이는가</strong>입니다.</p>"),
        ("검사 — 위험 인자부터",
         "<p>혈액검사를 새로 시행하였습니다.</p>"
         "<table class=\"lab-table\"><tr><td>HBsAg</td><td class=\"abn\">양성</td></tr>"
         "<tr><td>anti-HBs</td><td>음성</td></tr><tr><td>anti-HBc</td><td>양성</td></tr>"
         "<tr><td>HBV DNA</td><td class=\"abn\">12,000 IU/mL</td></tr>"
         "<tr><td>HBeAg</td><td>음성, anti-HBe 양성</td></tr>"
         "<tr><td>AST / ALT</td><td>38 / 42 IU/L</td></tr>"
         "<tr><td>알부민 / PT INR</td><td>4.2 / 1.0</td></tr>"
         "<tr><td>혈소판</td><td>168 ×10³/μL</td></tr>"
         "<tr><td>AFP / PIVKA-II</td><td>15 ng/mL / 28 mAU/mL</td></tr></table>"
         "<p>모르고 있던 만성 B형간염이 새로 발견되었습니다. 이는 결절을 평가하는 시각을 완전히 바꿉니다. "
         "50세 이상 남성 + 만성 B형간염 + 간 결절이라는 조합은 간세포암 가능성을 1순위로 두고 평가하게 됩니다.</p>"),
        ("영상 — 동적 CT",
         "<p>역동적 4-phase CT를 시행하였습니다. 우엽 S5 segment에 1.1 cm 결절이 동맥기에 강한 조영 증강을 보이고, "
         "정맥기·지연기에서는 washout이 명확히 관찰되었습니다. 전형적인 간세포암의 영상 진단 기준(KLCA-NCC)을 만족합니다.</p>"),
        ("진단·결정",
         "<p>BCLC 0기(very early) 간세포암으로 진단하였습니다. 조직검사 없이 영상 기준만으로 진단되는 드문 종양 중 하나가 간세포암입니다. "
         "1cm 단일 종양 + Child-Pugh A + ECOG 0 — 임상적으로 가장 좋은 시작점입니다.</p>"
         "<p>다학제적 논의에서 외과 절제와 고주파열치료술 두 옵션을 검토하였습니다. 종양 위치(피막에서 약간 깊음)와 간 기능 보존을 고려해 "
         "<strong>고주파열치료술</strong>을 권유하였습니다. 동시에 <strong>TDF 항바이러스제</strong>를 시작하였습니다.</p>"),
        ("경과",
         "<p><strong>1개월</strong> 시점에 시술 부위 통증은 며칠 내 소실되었고 영상에서 종양 부위 완전 괴사가 확인되었습니다. "
         "<strong>3개월</strong> AFP 8, PIVKA-II 22로 정상화되었고, CT에서 잔존 종양은 없었습니다. "
         "<strong>6개월</strong> 새 결절은 발견되지 않았으며 HBV DNA도 불검출 상태입니다. "
         "향후 6개월마다 영상과 종양표지자 추적을 시행하며, TDF는 평생 복용 계획입니다.</p>"),
    ],
    "teaching": [
        "건강검진에서 \"간 결절\" 발견 시 가장 먼저 위험 인자(B/C형 간염·간경변·음주·가족력) 확인",
        "본인이 모르고 있던 만성 B형간염이 결절 평가 시 새로 발견되는 경우가 외래에서 흔함",
        "1cm 결절이라도 위험 인자 + 영상 기준 충족 시 BCLC 0기 간세포암 진단·즉시 치료",
        "조기 발견(0/A기) 5년 생존율 70-80% — 검진의 의미를 보여주는 사례",
        "치료와 함께 항바이러스제 시작은 재발 위험 감소·간 기능 유지에 결정적",
    ],
    "related": [
        ("/B형간염-간암검진/", "B형간염 환자 6개월 간암 검진"),
        ("/간암-진단-첫외래/", "간암 진단 첫 외래에서 결정되는 것"),
        ("/B형간염-검사결과/", "B형간염 검사 결과지 해석"),
        ("/B형간염-평생약/", "B형간염 약을 평생 먹어야 하나"),
    ],
})

CASES.append({
    "slug": "B형간염-검진-새결절",
    "title": "B형간염 정기 검진에서 새로 발견된 2cm 결절",
    "intro": (
        "<p>55세 여성 환자입니다. 만성 B형간염으로 10년간 정기 추적을 받아오시며 TDF를 꾸준히 복용하셨습니다. "
        "6개월마다 빠짐없이 받으신 정기 간암 검진에서 이번 초음파로 우엽에 2.1 cm 크기의 결절이 새로 발견되어 내원하셨습니다. "
        "AFP는 6 ng/mL, PIVKA-II는 28 mAU/mL로 두 마커 모두 정상 범위입니다.</p>"
    ),
    "sections": [
        ("첫 만남",
         "<p>10년 동안 한 번도 빠지지 않고 6개월마다 검진을 받으셨고, 작년 검진까지는 모두 정상이었습니다. "
         "이번 초음파에서 우엽 S6에 2.1 cm 결절이 새로 보였습니다. \"마커가 정상인데 간암일까요?\"라는 것이 환자분의 첫 질문이었습니다. "
         "충분히 가질 수 있는 의문입니다. 그러나 종양표지자가 정상이어도 약 30-40%의 간암이 발견되기 때문에, 결절 평가에서는 영상이 결정적입니다.</p>"),
        ("영상 — 동적 MRI",
         "<p>Gd-EOB-MRI를 시행하였습니다. 동맥기에 강한 조영 증강, 정맥기에 washout, 간담도기에 hypointensity가 관찰되어 "
         "전형적인 간세포암 패턴을 보였습니다. 다른 부위 새 결절은 없었으며 혈관 침범과 원격 전이도 확인되지 않았습니다.</p>"),
        ("진단·결정",
         "<p>BCLC A기 단일 2.1 cm 간세포암으로 진단하였습니다. Child-Pugh A, ECOG 0이며 HBV DNA는 불검출 상태로 TDF가 잘 듣고 있습니다. "
         "다학제적 논의에서 절제·소작·이식을 모두 검토하였고, 종양이 피막 가까이에 있어 절제와 소작이 모두 가능하였습니다. "
         "환자분의 선호와 회복 시간을 고려하여 <strong>복강경 부분 절제</strong>를 결정하였습니다.</p>"),
        ("경과",
         "<p>수술은 합병증 없이 종료되었고 5일째 퇴원하셨습니다. 병리 결과 단일 간세포암, 미세혈관 침범 없음, 절제연 음성으로 확인되었습니다. "
         "<strong>3개월</strong> 회복 양호하며 영상 정상이었고, <strong>1년</strong>과 <strong>2년</strong> 시점에서도 새 결절은 발견되지 않았습니다. "
         "AFP·PIVKA-II 모두 정상으로 유지되고 있으며, 향후 6-12개월 추적과 TDF 평생 유지 계획입니다.</p>"),
    ],
    "teaching": [
        "정기 검진(6개월 간격)이 조기 발견의 핵심 — 작년 정상이었어도 이번에 발견 가능",
        "AFP·PIVKA-II가 정상이어도 간암 발견 가능 (약 10-15%는 두 마커 모두 정상)",
        "영상이 진단의 결정적 도구 — 동적 CT 또는 EOB-MRI가 표준",
        "TDF로 HBV DNA가 잘 억제되어 있어도 간세포암 위험은 0이 아님 — 검진 평생 유지",
        "초기에 발견된 단일 종양은 복강경 절제로 빠른 회복 가능",
    ],
    "related": [
        ("/B형간염-간암검진/", "B형간염 환자 6개월 간암 검진"),
        ("/알파태아단백/", "AFP — 정상범위와 간암 의심 기준"),
        ("/PIVKA-II-간암마커/", "PIVKA-II — 간암 종양표지자"),
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선"),
    ],
})

CASES.append({
    "slug": "AFP상승-영상음성",
    "title": "AFP만 올라가는데 영상은 정상",
    "intro": (
        "<p>62세 남성 환자로, 만성 B형간염과 간경변 의심 소견으로 엔테카비르를 복용 중이십니다. "
        "정기 검진에서 AFP가 6→48→350 ng/mL로 지난 1년간 점진적으로 상승하였으나, "
        "그동안 시행한 초음파와 CT에서는 결절이 발견되지 않아 추가 평가를 위해 외래에 내원하셨습니다.</p>"
    ),
    "sections": [
        ("첫 만남",
         "<p>지난 1년간 AFP가 6→48→350 ng/mL로 점진적으로 상승하였습니다. 매번 영상을 추가하였으나 결절은 보이지 않았습니다. "
         "환자분은 \"이 정도면 간암이 시작된 것 아닙니까?\"라며 불안해 하십니다.</p>"
         "<p>AFP 상승의 원인은 다양합니다. 간세포암 외에도 활동성 간염, 간 재생, 임신, 일부 다른 종양에서도 상승할 수 있습니다. "
         "그러나 350 정도 수준이라면 간암 의심을 적극 평가해야 하는 수치입니다.</p>"),
        ("재평가 — 영상 강화",
         "<p>EOB-MRI를 시행하였습니다. 그동안 초음파와 CT에서 보이지 않던 우엽 S8에 0.8 cm 결절이 동맥기 조영 증강과 "
         "간담도기 hypointensity로 확인되었습니다. 작은 크기여서 일반 영상에서는 놓쳤던 병변입니다.</p>"
         "<p>혈액검사: ALT 35, HBV DNA 불검출(약물 잘 반응), 알부민 3.6, INR 1.1, 혈소판 105 ×10³(혈소판 감소 — 간경변 신호).</p>"),
        ("진단·결정",
         "<p>EOB-MRI에서의 패턴, AFP 추세 상승, 위험 인자(B형간염·간경변)를 종합하여 <strong>BCLC 0기 간세포암으로 진단</strong>하였습니다. "
         "0.8 cm로 작지만 진단 기준을 충족합니다. 다학제적 논의에서 <strong>고주파열치료술</strong>을 결정하였습니다. "
         "위치가 피막에서 충분히 떨어져 있어 안전한 시술이 가능합니다.</p>"),
        ("경과",
         "<p><strong>1개월</strong> 시술 후 영상에서 완전 괴사가 확인되었고 AFP는 60으로 빠르게 떨어졌습니다. "
         "<strong>3개월</strong> AFP 12로 정상화, <strong>6개월</strong> AFP 8 유지, 새 결절 없음. "
         "이후 6개월 추적과 엔테카비르 유지를 지속하며 추후 TAF 전환을 검토할 계획입니다.</p>"),
    ],
    "teaching": [
        "AFP가 점진적 상승하는데 영상이 정상이면 한 번 더 정밀 영상(EOB-MRI) 시행 — 작은 결절을 놓칠 수 있음",
        "AFP 추세(이전 값 대비 변화)가 절대값보다 더 의미 있는 경우가 많음",
        "혈소판 감소(< 150) 동반 시 간경변 진행 신호 — 간세포암 위험 가산",
        "간경변 환자에서 AFP 상승 평가 임계값은 일반인보다 낮게 적용",
        "EOB-MRI는 초음파·CT보다 작은 결절(< 1cm) 검출률 우수",
    ],
    "related": [
        ("/알파태아단백/", "AFP — 정상범위와 간암 의심 기준"),
        ("/PIVKA-II-간암마커/", "PIVKA-II — 간암 종양표지자"),
        ("/B형간염-간암검진/", "B형간염 환자 6개월 간암 검진"),
        ("/간경변-정상수치-함정/", "간기능검사 정상인데 간경변? — 진행된 간경변의 함정"),
    ],
})

CASES.append({
    "slug": "LR3-모호결절-추적",
    "title": "LI-RADS 3 모호한 결절 — 추적인가, 정밀인가",
    "intro": (
        "<p>58세 여성 환자입니다. 만성 B형간염으로 TAF를 복용하며 정기 추적 중이시며, "
        "Fibroscan에서 11 kPa로 진행 섬유화가 확인된 상태입니다. 정기 검진 EOB-MRI에서 1.5 cm 결절이 발견되었으나 "
        "동맥기 조영 증강이 약하고 washout이 명확하지 않아 LI-RADS 3(중등도 의심)으로 분류되어 내원하셨습니다.</p>"
    ),
    "sections": [
        ("첫 만남",
         "<p>EOB-MRI 결과지를 들고 오셨습니다. 결과지에 적힌 \"LI-RADS 3\"이라는 단어의 의미를 궁금해 하십니다. "
         "LI-RADS는 간세포암 영상 분류 체계로 LR-1(확실히 양성)부터 LR-5(확실한 간세포암)까지 5단계로 나눕니다. "
         "<strong>LR-3는 중등도 의심</strong>으로 양성과 악성 어느 쪽도 단정할 수 없는 회색지대입니다.</p>"
         "<p>이 단계에서 선택은 두 가지입니다 — 추적 관찰 또는 추가 영상·생검.</p>"),
        ("판단 — 위험과 추가 평가",
         "<p>이 환자는 만성 B형간염, 진행 섬유화(Fibroscan 11 kPa), 50대 후반 여성으로 간세포암 위험이 의미 있게 높습니다. "
         "단순 추적보다 적극적 평가를 결정하였습니다. 조영 초음파(CEUS)를 추가하였고, 동맥기 조영 증강 후 비교적 빠른 washout 양상이 관찰되어 "
         "LR-4(가능성 있는 간세포암)으로 reclassify되었습니다.</p>"),
        ("진단·결정",
         "<p>LR-4는 단독으로 진단 확정이 어려워 다학제적 논의에서 결정하였습니다. 옵션은 1) 짧은 간격 추적(2-3개월), 2) 생검, "
         "3) 시술적 진단·치료(고주파열치료술 시 조직 동시 채취)였습니다. 환자분 선호로 <strong>2-3개월 후 EOB-MRI 추적</strong>을 결정하였습니다.</p>"
         "<p>3개월 후 EOB-MRI에서 결절이 1.7 cm로 약간 커지고 동적 패턴이 더 명확해져 LR-5(확실한 간세포암)로 reclassify되었으며 진단이 확정되었습니다.</p>"),
        ("치료와 경과",
         "<p>1.7 cm 단일 종양, Child-Pugh A 상태에서 고주파열치료술을 시행하였습니다. "
         "시술 후 1·3·6개월 영상에서 완전 반응이 유지되었고 AFP·PIVKA-II도 정상으로 유지되었습니다. TAF는 지속하고 있습니다.</p>"),
    ],
    "teaching": [
        "LI-RADS 3은 회색지대 — 위험 인자에 따라 추적 vs 정밀 평가 결정",
        "조영 초음파(CEUS)가 모호한 결절의 reclassification에 유용",
        "B형간염 + 진행 섬유화 + 50대 이상은 적극 평가 임계값 낮춤",
        "2-3개월 짧은 간격 추적은 모호한 결절의 진행 평가에 표준 옵션",
        "결절 크기 증가 + 동적 패턴 명확화는 진단 신뢰도를 빠르게 올림",
    ],
    "related": [
        ("/B형간염-간암검진/", "B형간염 환자 6개월 간암 검진"),
        ("/간섬유화스캔-수치/", "Fibroscan 수치 읽는 법"),
        ("/간암-진단-첫외래/", "간암 진단 첫 외래"),
    ],
})

CASES.append({
    "slug": "PIVKAII-와파린-위양성",
    "title": "PIVKA-II 1500인데 와파린 복용 중",
    "intro": (
        "<p>70세 남성 환자입니다. 심방세동으로 와파린을 5년째 복용하고 계시며, 만성 B형간염도 동반되어 엔테카비르로 잘 조절되고 있습니다. "
        "정기 검진에서 PIVKA-II가 1500 mAU/mL로 매우 높게 측정되어 외래에 내원하셨습니다. AFP는 12 ng/mL로 정상이며 환자분께서는 매우 불안해 하십니다.</p>"
    ),
    "sections": [
        ("첫 만남",
         "<p>먼저 알아야 할 점이 있습니다. <strong>와파린·DOAC·항생제·비타민 K 결핍은 PIVKA-II를 위양성으로 매우 높게 만들 수 있습니다</strong>. "
         "이 환자에서 1500이라는 수치는 위양성 가능성이 매우 높습니다. 그러나 종양 가능성을 확실히 배제하지 않은 채 안심시킬 수는 없으므로 영상으로 명확히 확인합니다.</p>"),
        ("배제 — 영상부터",
         "<p>EOB-MRI를 시행하였습니다. 간 전체 영역에서 결절은 발견되지 않았고 종양 의심 소견도 전혀 없었습니다. "
         "추가로 흉부 CT와 뼈 영상에서 다른 종양도 확인되지 않았습니다.</p>"
         "<p>혈액검사: AFP 12(정상), ALT 28, HBV DNA 불검출, INR 2.4(와파린 적정).</p>"),
        ("결정",
         "<p>PIVKA-II 위양성으로 결론지었습니다. \"종양표지자 1500\"이 환자분께는 무서운 숫자였지만 임상 맥락이 모두 설명됩니다. "
         "와파린이 비타민 K 의존적 카르복실화를 차단하면 비정상 prothrombin(PIVKA-II) 측정이 상승하기 때문입니다.</p>"
         "<p>와파린을 DOAC(아픽사반 등)로 전환하면 PIVKA-II 측정에 미치는 영향이 크게 줄어들지만, "
         "환자분의 심방세동 관리 안정성이 우선이라 와파린 유지를 결정하였습니다. 향후 PIVKA-II 추적은 와파린 영향을 함께 고려하여 해석합니다.</p>"),
        ("경과",
         "<p>3개월·6개월·12개월 EOB-MRI 모두 정상으로 확인되었습니다. 환자분은 안심하고 일상으로 복귀하셨습니다. "
         "이후 6개월 영상과 AFP를 위주로 추적하며, PIVKA-II는 와파린 유지 동안 해석 보조 용도로만 사용하고 있습니다.</p>"),
    ],
    "teaching": [
        "PIVKA-II 단독 상승 시 위양성 원인 평가 필수 — 와파린·DOAC·항생제·비타민 K 결핍",
        "위양성 의심이라도 영상으로 종양 확실히 배제하는 것이 표준",
        "와파린 환자에서 PIVKA-II는 종양 추적 마커로 신뢰도 떨어져 AFP·영상에 더 의존",
        "DOAC가 비타민 K 의존 경로 영향 적어 PIVKA-II 측정에 더 우호적이지만 약 변경은 임상 우선순위로 결정",
        "환자가 충격받은 수치도 임상 맥락이 다 설명하면 안심 가능 — 충분한 설명이 진료의 일부",
    ],
    "related": [
        ("/PIVKA-II-간암마커/", "PIVKA-II — 간암 종양표지자"),
        ("/알파태아단백/", "AFP — 정상범위와 간암 의심 기준"),
        ("/B형간염-간암검진/", "B형간염 환자 6개월 간암 검진"),
    ],
})

CASES.append({
    "slug": "MASLD-HCC-비만당뇨",
    "title": "MASLD 추적 중 발견된 간세포암",
    "intro": (
        "<p>65세 남성 환자입니다. BMI 31의 비만 체형이며 2형 당뇨와 고지혈증을 동반하고 있습니다. "
        "B형·C형 간염은 모두 음성이고 음주는 거의 없으십니다. 5년 전 건강검진에서 지방간과 ALT 상승으로 평가를 시작하여 "
        "MASLD F2 섬유화로 진단된 후 1년마다 추적해 오셨고, 이번 EOB-MRI에서 좌엽 S3에 2.5 cm 새 결절이 발견되어 내원하셨습니다.</p>"
    ),
    "sections": [
        ("첫 만남",
         "<p>5년 전 평가 시작 이후 그동안 체중을 5 kg 감량하셨고 ALT 수치도 좋아졌습니다. 그런데 이번 EOB-MRI에서 새 결절이 발견되었습니다. "
         "\"술도 안 마시고 B형간염도 없는데 간암이라뇨\"라며 환자분이 놀라셨습니다. "
         "그러나 MASLD 기반 간세포암(MASLD-HCC)은 빠르게 늘어나고 있는 영역이며, 이 환자처럼 비만·당뇨·진행 섬유화 조합에서는 충분히 발생 가능합니다.</p>"),
        ("영상·검사",
         "<p>EOB-MRI에서 좌엽 S3에 2.5 cm 결절이 동맥기 조영 증강, 정맥기 washout, 간담도기 hypointensity 패턴(LR-5)으로 확인되었습니다. "
         "다른 결절이나 혈관 침범은 없었습니다.</p>"
         "<p>혈액검사: AFP 45, PIVKA-II 89, ALT 38, AST 42, 알부민 4.0, INR 1.05, 혈소판 142, HbA1c 7.2%, BMI 31.</p>"),
        ("진단·결정",
         "<p>BCLC A기 단일 2.5 cm 간세포암으로 진단하였습니다. Child-Pugh A이며 다학제적 논의에서 절제와 소작이 모두 가능하다고 평가되었습니다. "
         "위치(좌엽 표면 가까움)와 환자 선호를 고려하여 <strong>복강경 좌엽 외측구역 절제</strong>를 결정하였습니다.</p>"
         "<p>동시에 동반 질환 평가를 진행하였습니다 — 당뇨 강화 관리(metformin에 SGLT2/GLP-1 추가), "
         "체중 7-10% 감량 목표 설정, 식이·운동 영양사 협진을 시작하였습니다.</p>"),
        ("경과",
         "<p>수술은 합병증 없이 회복되었습니다. 병리에서 단일 간세포암, 미세혈관 침범 없음, 절제연 음성이 확인되었으며 "
         "배경 간조직에는 MASH F3 섬유화가 동반되어 있었습니다. <strong>1년</strong> 시점에 새 결절은 없었고 체중 6 kg 감량, "
         "HbA1c 6.5%, ALT 28로 호전되었습니다. 6개월마다 영상과 마커 추적, MASLD 관리를 지속하고 있습니다.</p>"),
    ],
    "teaching": [
        "MASLD-HCC는 비-바이러스성 간암의 빠르게 늘어나는 영역 — 50세 이상·당뇨·진행 섬유화 시 검진 적극 검토",
        "MASLD F2-F3 환자에서 6-12개월 영상 + 종양표지자 검진 권장",
        "MASLD-HCC는 일부에서 비-간경변 상태에서도 발생 가능 — 위험 인자 누적 시 적극 평가",
        "치료 후 동반 질환(당뇨·비만) 강화 관리가 재발 위험 감소에 결정적",
        "GLP-1·SGLT2가 당뇨 + MASLD 환자에서 1차 옵션",
    ],
    "related": [
        ("/지방간-간암/", "지방간이 간암으로 가는 길"),
        ("/지방간염-MASH/", "지방간염(MASH)"),
        ("/지방간-SGLT2-GLP1/", "SGLT2·GLP-1 작용제와 지방간"),
        ("/간암-진단-첫외래/", "간암 진단 첫 외래"),
    ],
})

CASES.append({
    "slug": "BCLC-A-단일3cm-절제vs소작",
    "title": "단일 3cm 종양 — 절제와 고주파열치료술 사이",
    "intro": (
        "<p>60세 남성 환자입니다. 만성 B형간염으로 TDF를 복용 중이며 간경변은 없고 Child-Pugh A를 유지하고 있습니다. "
        "정기 6개월 검진에서 우엽 S8 위치에 단일 3.0 cm 결절이 새로 확인되었습니다. "
        "역동적 CT에서 동맥기 조영 증강과 정맥기 washout 패턴이 명확하여 영상 진단 기준을 충족하였고, BCLC A, ECOG 0으로 평가되었습니다. "
        "종양 크기와 단일 병변, 충분한 잔간 기능을 고려할 때 절제와 고주파열치료술 두 옵션이 모두 가능한 상황입니다.</p>"
    ),
    "sections": [
        ("결정 인자 분석",
         "<p>3cm 이하 단일 결절에서 절제와 소작 두 치료의 5년 생존은 비슷합니다. "
         "결정은 종양 위치, 간 기능, 환자 선호로 갈립니다.</p>"
         "<ul>"
         "<li>위치: S8(우엽 후방, 횡격막 가까움) — 소작 시 횡격막 손상 위험과 시야 확보의 어려움이 있습니다.</li>"
         "<li>간 기능: Child-Pugh A, HVPG 측정에서 5 mmHg(낮음) — 절제가 안전한 조건입니다.</li>"
         "<li>환자 요인: 60세 BMI 24, 동반 질환이 적고 회복 의지가 강합니다.</li>"
         "</ul>"),
        ("다학제 결정",
         "<p>위치 특성과 환자 상태를 종합하여 <strong>복강경 우엽 부분 절제</strong>를 권유하였습니다. "
         "절제 후 정상 간 부피가 약 65% 잔여로 충분하며 출혈 위험도 낮은 조건입니다.</p>"),
        ("경과",
         "<p>수술은 4시간 소요, 출혈 200 mL로 종료되었고 5일 입원 후 퇴원하셨습니다. "
         "병리에서 단일 3.1 cm 간세포암, 미세혈관 침범 없음, 절제연 1 cm 음성으로 확인되었습니다. "
         "<strong>1·3·6개월</strong> 영상에서 정상이며 종양표지자도 정상입니다. <strong>1년</strong> 시점 무재발 상태이며 향후 6개월마다 평생 추적합니다.</p>"),
    ],
    "teaching": [
        "3cm 이하 단일 종양에서 절제와 소작은 효과 비슷 — 위치·간 기능·환자 상태가 결정",
        "S7/S8 같은 우엽 후방·횡격막 가까운 위치는 소작 기술적 어려움",
        "HVPG < 10 mmHg, Child-Pugh A는 절제 안전 가능 환자",
        "복강경 절제는 회복 빠름·미용적 장점",
        "병리에서 미세혈관 침범 유무가 재발 위험 예측의 핵심",
    ],
    "related": [
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선"),
        ("/간암-BCLC병기/", "BCLC 병기와 치료 옵션"),
        ("/간암-재발-추적/", "간암 재발 추적"),
    ],
})

CASES.append({
    "slug": "BCLC-A-다발3개-소작",
    "title": "BCLC A 다발성 — 3개 결절·각 2cm 이하",
    "intro": (
        "<p>55세 여성 환자입니다. 과거 만성 C형간염으로 진단되었고 DAA 치료로 SVR을 달성하여 완치된 지 3년이 경과한 상태입니다. "
        "기저에 간경변이 동반되어 있어 정기 검진을 지속하고 계시며, 이번 검진에서 우엽과 좌엽에 결절 3개(1.8/1.5/1.2 cm)가 새로 발견되었습니다. "
        "세 결절 모두 EOB-MRI에서 LR-5 패턴을 보였으며 BCLC A에 해당합니다.</p>"
    ),
    "sections": [
        ("결정 흐름",
         "<p>3개 결절 모두 BCLC A의 \"3개·각 ≤3cm\" 기준 안에 들어갑니다. "
         "절제는 다중 위치라 간 부피 부담이 크고, 이식은 적응증이지만 한국 KONOS·LDLT 평가에 시간이 필요합니다. "
         "다학제적 논의에서 <strong>같은 회기에 3개 결절을 모두 고주파열치료술</strong>로 시행하기로 결정하였습니다.</p>"),
        ("시술과 경과",
         "<p>중재영상의학과에서 3개 위치를 단일 회기에 모두 소작하였습니다. 시술 시간 1.5시간, 합병증 없이 종료되었습니다. "
         "<strong>1개월</strong> 영상에서 3개 모두 완전 괴사가 확인되었고, <strong>3개월</strong> AFP가 정상화되었으며 새 결절도 없었습니다. "
         "<strong>6개월·1년</strong> 시점에서도 무재발 상태입니다.</p>"),
    ],
    "teaching": [
        "BCLC A 다발성(3개·각 ≤3cm)에서 같은 회기 다중 RFA가 선택 옵션",
        "C형간염 DAA 완치 후에도 간경변·HCC 위험은 남아 검진 평생 유지",
        "절제 vs 소작 결정에 종양 개수·간 부피 잔여가 큰 영향",
        "이식은 다발성에서도 적응증이지만 대기 기간·LDLT 평가 시간 고려",
        "다중 RFA는 단일 시술로 끝나 환자 부담·회복 시간 짧음",
    ],
    "related": [
        ("/C형간염-완치-DAA/", "C형간염 DAA 완치"),
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선"),
        ("/간암-간이식/", "간암에서의 간이식"),
    ],
})

CASES.append({
    "slug": "ChildB-단일4cm-이식",
    "title": "Child-Pugh B + 단일 4cm — 절제 어렵고 이식 평가",
    "intro": (
        "<p>58세 남성 환자입니다. 알코올성 간경변으로 1년간 금주를 유지하고 있으며, 정기 검진에서 우엽에 단일 4.0 cm 간세포암이 발견되어 내원하셨습니다. "
        "Child-Pugh B7(복수 경증, 알부민 3.0)이며 MELD는 14점입니다. 종양은 Milan criteria 안에 들어가지만 간 기능 부담으로 절제는 위험이 큰 상황입니다.</p>"
    ),
    "sections": [
        ("평가",
         "<p>단일 종양으로 Milan criteria(단일 ≤5 cm) 안에 들어갑니다. Child-Pugh B로 절제 위험이 크며, "
         "알코올 1년 금주를 유지 중이라 이식 평가가 가능한 조건입니다. 다학제적 논의에서 <strong>간이식 평가 시작</strong>을 결정하였습니다. "
         "동시에 대기 기간 동안 종양 진행을 막기 위한 bridging therapy로 <strong>TACE</strong>를 시행하였습니다.</p>"),
        ("이식 평가와 경과",
         "<p>다학제 평가는 1.5주가 소요되었고 의학·외과·정신건강의학(알코올 평가)·심혈관 모두 적합 판정을 받았습니다. "
         "가족 중 50대 형이 LDLT 기증자로 적합 평가되었고, <strong>2개월</strong> 후 LDLT를 시행하였습니다. 합병증 없이 회복되었습니다.</p>"
         "<p>병리 결과 Milan 기준 안의 단일 간세포암, 미세혈관 침범 없음으로 확인되었습니다. "
         "<strong>3개월</strong> 면역억제 안정, <strong>1년</strong> 무재발이며 절대 금주를 유지하고 있습니다. mTOR 억제제(시롤리무스)로의 전환을 검토 중입니다.</p>"),
    ],
    "teaching": [
        "Child-Pugh B + 단일 종양에서 절제보다 이식 평가가 우선 검토",
        "한국은 LDLT 비율 70%로 평균 대기 기간 짧음 — 가족 기증자 평가 빠르게 진행",
        "알코올성 간경변에서 이식 적응에 6개월 이상 금주 + 정신건강 평가 필수",
        "Bridging therapy(TACE 등)로 대기 기간 종양 진행 억제",
        "HCC 이식 후 mTOR 억제제(시롤리무스) 사용은 재발 감소 효과 일부 보고",
    ],
    "related": [
        ("/간경변-간이식-평가/", "간이식 평가 — 누가, 언제 시작하나"),
        ("/간암-간이식/", "간암에서의 간이식"),
        ("/간경변-Child-Pugh-MELD/", "Child-Pugh와 MELD"),
    ],
})

CASES.append({
    "slug": "BCLC-B-다발성-TACE",
    "title": "BCLC B 다발성 — TACE 1차",
    "intro": (
        "<p>67세 남성 환자입니다. 만성 B형간염으로 TAF를 복용 중이며 Child-Pugh A6를 유지하고 있습니다. "
        "정기 검진에서 양엽에 4개 결절(3.5/2.8/2.2/1.5 cm)이 새로 발견되었으며 혈관 침범과 원격 전이는 없었습니다. "
        "BCLC B에 해당하며 ECOG 0으로 전신 상태는 양호합니다.</p>"
    ),
    "sections": [
        ("결정",
         "<p>BCLC B의 표준 1차 치료는 TACE입니다. 다발성·양엽 분포로 절제는 간 부피 부담이 크고 다중 RFA도 어려운 조건입니다. "
         "다학제적 논의에서 <strong>conventional TACE</strong>를 1차로 결정하였습니다.</p>"),
        ("시술과 경과",
         "<p>좌엽과 우엽을 분리하여 시행하였습니다. 첫 회기에 우엽 3개 결절을, 4주 후 좌엽 1개 결절을 시술하였습니다. "
         "각 시술 후 발열·복통(post-embolization syndrome)이 2-3일 지속되었습니다. "
         "<strong>4-6주 후 영상</strong>에서 4개 모두 종양 위축이 확인되었고 1개에서 잔존 viable 부분이 남아 있었습니다. "
         "<strong>3개월</strong>에 잔존 부위에 추가 TACE를 시행하였고, <strong>6개월</strong>에는 모두 완전 괴사가 확인되었습니다. "
         "<strong>1년</strong> 시점 새 결절이 없으며 간 기능도 안정적입니다.</p>"),
    ],
    "teaching": [
        "BCLC B 다발성에서 conventional TACE 또는 DEB-TACE가 1차 표준",
        "Post-embolization syndrome(발열·복통·구역)은 시술 후 2-3일 흔하고 대부분 자가 회복",
        "TACE는 한 번에 완전 괴사가 안 될 수 있어 4-6주 후 영상 평가·반복 시행",
        "양엽 침범 시 좌·우엽 분리 시행으로 간 부담 분산",
        "TACE 부적합 또는 실패 시 면역치료(atezo+bev) 또는 SBRT·TARE로 전환 검토",
    ],
    "related": [
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선"),
        ("/간암-방사선색전술/", "방사선색전술(TARE)"),
        ("/간암-BCLC병기/", "BCLC 병기와 치료 옵션"),
    ],
})

CASES.append({
    "slug": "큰종양-TACE-SBRT-결합",
    "title": "8cm 큰 종양 — TACE + SBRT 결합",
    "intro": (
        "<p>62세 남성 환자입니다. 만성 B형간염을 앓고 계시며 Child-Pugh A, BMI 26 상태입니다. "
        "우엽에 단일 8.2 cm 큰 종양이 발견되었으나 혈관 침범은 없었습니다. "
        "절제를 시행하기에는 잔여 간 부피 부족 위험이 있어 다학제적 논의에서 결합 치료 전략을 결정하셨습니다.</p>"
    ),
    "sections": [
        ("결정",
         "<p>8 cm 단일 큰 종양은 절제·이식·TACE 단독 모두 한계가 있습니다. "
         "다학제적 논의에서 <strong>TACE → 4-6주 후 SBRT</strong> 결합을 결정하였습니다. "
         "큰 종양에서 두 치료 결합이 단독보다 우월하다는 데이터(STRBED, TACE-HIGH 등)를 활용한 전략입니다.</p>"),
        ("시술과 경과",
         "<p>먼저 TACE를 시행하여 종양이 약 30% 위축되었습니다. <strong>5주 후</strong> SBRT(3분할 고선량)를 시행하였고, "
         "<strong>3개월 후</strong> 영상에서 종양이 약 70% 위축되었으며 일부 viable 영역이 남아 있었습니다. "
         "<strong>6개월</strong> 안정 또는 추가 위축이 관찰되었고 AFP는 850→120→45로 빠르게 감소하였습니다. "
         "다학제적 논의에서 <strong>다운스테이징 성공으로 이식 평가</strong>를 시작하였습니다.</p>"),
    ],
    "teaching": [
        "큰 단일 종양(>5-7cm)에서 단일 치료 한계 — TACE+SBRT, TACE+TARE 등 결합 검토",
        "결합 치료가 단독보다 국소 제어·생존 우수 데이터 누적",
        "TACE 후 SBRT 시기는 4-6주가 표준 (회복·평가 시간)",
        "큰 종양 다운스테이징 성공 시 이식 후보 전환 가능 — Mazzaferro Lancet Oncol 2020",
        "AFP 추세 감소가 치료 반응의 좋은 지표",
    ],
    "related": [
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선"),
        ("/간암-방사선색전술/", "방사선색전술(TARE)"),
        ("/간암-간이식/", "간암에서의 간이식"),
    ],
})

CASES.append({
    "slug": "문맥침범-AtezoBev",
    "title": "문맥 침범 BCLC C — atezo+bev 1차",
    "intro": (
        "<p>55세 남성 환자입니다. 만성 B형간염을 동반하고 있으며 Child-Pugh A, ECOG 1 상태입니다. "
        "5 cm 단일 종양과 함께 우문맥 분지 침범이 확인되었으나 폐와 뼈 전이는 없었습니다. BCLC C에 해당합니다. "
        "내시경 검사에서는 작은 정맥류만 확인되었고 출혈 이력은 없으십니다.</p>"
    ),
    "sections": [
        ("결정",
         "<p>BCLC C의 1차 표준은 면역치료입니다. 정맥류 평가에서 작은 정맥류와 출혈 이력이 없어 베바시주맙 사용이 가능한 조건입니다. "
         "다학제적 논의에서 <strong>atezolizumab + bevacizumab</strong> 1차 치료를 결정하였습니다.</p>"),
        ("치료와 경과",
         "<p>3주마다 외래에서 정주하였습니다. 첫 6주 동안 경증 피로 외 부작용은 없었습니다. "
         "<strong>9주</strong> 영상에서 종양이 30% 위축되었고 문맥 침범 부분도 안정 상태였습니다. AFP는 1200→340으로 감소하였습니다. "
         "<strong>6개월</strong> 시점에 종양 50% 위축, 문맥 침범 일부 복원, 새 병변 없음. 갑상선 기능 저하가 발생하여 갑상선 호르몬 보충으로 조절하였습니다. "
         "<strong>1년</strong> 안정 반응이 유지되고 있으며 AFP는 65입니다.</p>"),
    ],
    "teaching": [
        "BCLC C 1차는 IMbrave150 이후 atezo+bev이 표준",
        "베바시주맙 사용 전 정맥류 내시경 평가 필수 — 출혈 위험 환자엔 STRIDE 대안",
        "면역 매개 부작용 모니터링 — 갑상선·간·폐·대장·내분비",
        "9-12주 영상으로 첫 반응 평가, 안정·반응 시 지속",
        "AFP 추세 감소가 치료 반응 지표로 유용",
    ],
    "related": [
        ("/간암-면역치료-1차/", "면역치료 1차 — atezo+bev"),
        ("/간경변-식도정맥류/", "식도정맥류"),
        ("/updates/IMbrave150-atezolizumab-bevacizumab-NEJM-2020/", "IMbrave150 노트"),
    ],
})

CASES.append({
    "slug": "정맥류출혈이력-STRIDE",
    "title": "정맥류 출혈 이력 + BCLC C — STRIDE 선택",
    "intro": (
        "<p>63세 남성 환자입니다. 만성 B형간염과 간경변을 동반하고 있으며 2년 전 식도정맥류 출혈로 결찰술을 받으셨고 이후 카베디롤을 유지하고 있습니다. "
        "현재 다발성 종양과 우문맥 침범이 확인되어 BCLC C에 해당하며, Child-Pugh B7 상태입니다. "
        "정맥류 출혈 이력으로 베바시주맙 사용은 회피해야 하는 조건입니다.</p>"
    ),
    "sections": [
        ("결정",
         "<p>BCLC C의 1차 옵션인 atezo+bev은 베바시주맙의 출혈 위험으로 회피해야 합니다. "
         "다학제적 논의에서 <strong>STRIDE(durvalumab + tremelimumab 1회 priming)</strong>를 결정하였습니다. HIMALAYA 시험이 근거입니다.</p>"),
        ("치료와 경과",
         "<p>트레멜리무맙 1회와 듀발루맙 4주마다 유지로 치료를 시작하였습니다. "
         "첫 12주 동안 면역 부작용은 없었고 종양도 약간 위축되었습니다. <strong>6개월</strong> 종양 안정과 문맥 침범 일부 복원이 확인되었습니다. "
         "<strong>1년</strong> 안정 반응 유지 상태이며, ALT가 약간 상승하였으나 약물 보류와 짧은 스테로이드 투여로 조절되었습니다. "
         "<strong>2년</strong> 시점 무진행 생존이며 환자분은 일상 활동을 유지하고 계십니다.</p>"),
    ],
    "teaching": [
        "베바시주맙 회피 필요 환자(정맥류 출혈 이력)에서 STRIDE가 1차 대안",
        "HIMALAYA에서 STRIDE 4년 생존 25% — long survivor 가능성",
        "트레멜리무맙은 1회만 사용해 면역 부작용 누적 부담 적음",
        "면역 매개 간염 발생 시 약물 보류 + 스테로이드로 대부분 조절",
        "Child-Pugh B에서 면역치료 안전성은 제한적 — 신중한 모니터링",
    ],
    "related": [
        ("/간암-면역치료-1차/", "면역치료 1차"),
        ("/간경변-식도정맥류/", "식도정맥류"),
        ("/updates/HIMALAYA-durvalumab-tremelimumab-NEJM-Evid-2022/", "HIMALAYA 노트"),
    ],
})

CASES.append({
    "slug": "다운스테이징-이식전환",
    "title": "큰 종양 다운스테이징 → 이식 후보 전환",
    "intro": (
        "<p>57세 남성 환자입니다. 만성 B형간염과 초기 간경변을 동반하고 있으며 Child-Pugh A6 상태입니다. "
        "단일 7.0 cm 종양이 발견되었고 혈관 침범은 없었습니다. Milan(≤5 cm) 기준 밖이라 처음에는 이식 후보가 아닌 상태로 다운스테이징을 시도하기로 결정하셨습니다.</p>"
    ),
    "sections": [
        ("다운스테이징 시도",
         "<p>다학제적 논의에서 <strong>TACE → SBRT → 6개월 안정 평가 후 이식 등록</strong> 흐름을 결정하였습니다. AFP 시작값은 1500이었습니다.</p>"
         "<p>TACE 시행 후 종양이 5.5 cm로 축소되었고, 6주 후 SBRT를 추가하여 3개월 후 4.5 cm로 더 축소되어 Milan 기준 안에 들어갔습니다. "
         "AFP는 1500→320→90으로 감소하였습니다. 6개월 추적에서 안정 반응이 확인된 후 <strong>KONOS 등록</strong>과 LDLT 평가를 시작하였습니다.</p>"),
        ("이식과 경과",
         "<p>딸이 LDLT 기증자로 적합 평가되어 <strong>4개월 후</strong> LDLT를 시행하였습니다. "
         "병리에서 다운스테이징 후 4.2 cm 단일 간세포암, 미세혈관 침범 없음으로 확인되었습니다. "
         "<strong>1년</strong> 무재발이며 면역억제 안정 상태에서 mTOR 억제제(시롤리무스)로 전환하였습니다. <strong>2년</strong> 무재발이 유지되고 있습니다.</p>"),
    ],
    "teaching": [
        "Milan 밖 큰 종양도 다운스테이징 성공 시 이식 후보 전환 가능 (Mazzaferro Lancet Oncol 2020)",
        "TACE+SBRT 결합이 큰 종양 다운스테이징에 유용",
        "다운스테이징 후 3-6개월 안정 평가 + 등록이 표준 흐름",
        "AFP 추세 감소는 종양 생물학적 반응의 강력한 지표",
        "다운스테이징 성공 환자의 이식 후 5년 생존은 직접 Milan 환자와 유사",
    ],
    "related": [
        ("/간암-간이식/", "간암에서의 간이식"),
        ("/간암-방사선색전술/", "방사선색전술(TARE)"),
        ("/간경변-간이식-평가/", "간이식 평가"),
    ],
})

CASES.append({
    "slug": "절제후-2년재발",
    "title": "절제 2년 후 새 결절 — 재발 결정 흐름",
    "intro": (
        "<p>65세 여성 환자입니다. 만성 C형간염을 DAA로 완치한 병력이 있으시고 2년 전 간세포암으로 우엽 절제를 받으신 후 무재발 상태로 추적 중이셨습니다. "
        "이번 정기 EOB-MRI(절제 후 2년 6개월 시점)에서 좌엽 S2에 1.5 cm 새 결절이 발견되었습니다. "
        "이전 절제 부위가 아닌 다른 위치로 새로운 결절(de novo)에 해당합니다.</p>"
    ),
    "sections": [
        ("재발 평가",
         "<p>이전 절제 부위가 아닌 다른 위치에 발생한 결절로 \"새 결절\"로 분류됩니다. "
         "간경변 환자에서 흔히 관찰되는 \"second primary\" 패턴입니다. AFP는 28(약간 상승), PIVKA-II는 45였습니다.</p>"),
        ("결정과 경과",
         "<p>다학제적 논의에서 위치(좌엽 표면), 크기(1.5 cm), 간 기능(Child-Pugh A)을 평가하여 "
         "<strong>고주파열치료술</strong>을 결정하였습니다. 시술은 합병증 없이 완전 괴사가 확인되었습니다. "
         "<strong>3개월</strong> AFP 정상화, <strong>1년</strong> 무재발 상태입니다. "
         "동시에 환자분께 \"앞으로 또 새 결절 가능성이 있다\"는 점을 충분히 설명드려 6개월 검진 평생 유지에 대한 동기를 강화하였습니다.</p>"),
    ],
    "teaching": [
        "절제 2년 이후 발견되는 \"재발\"은 대부분 새 결절(de novo) — 사실상 새 간세포암",
        "간경변 환자에서 새 결절은 평생 발생 가능 — 검진 평생 유지",
        "재발 시 위치·크기·간 기능 따라 절제·소작·SBRT·TACE 모두 옵션",
        "1cm대 단일 새 결절은 RFA 효과·회복 우수",
        "환자 동기 부여를 위한 \"왜 평생 검진인가\" 설명이 검진 미수율 감소에 결정적",
    ],
    "related": [
        ("/간암-재발-추적/", "간암 재발 추적"),
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선"),
        ("/C형간염-완치-DAA/", "C형간염 DAA 완치"),
    ],
})


# === Render ===
def render_case(spec, page_id):
    intro_html = formalize(spec["intro"])
    fig_spec = CASE_FIGURES.get(spec["slug"])
    fig_after = fig_spec["after"] if fig_spec else -1
    fig_html = fig_spec["svg"] if fig_spec else ""

    sections_html = ""
    for idx, (h2, body) in enumerate(spec["sections"]):
        sections_html += f'<div class="case-section"><h2>{esc(h2)}</h2>\n{formalize(body)}\n</div>\n\n'
        if idx == fig_after and fig_html:
            sections_html += fig_html + "\n\n"

    teaching_html = "".join(f'<li>{esc(t)}</li>' for t in spec["teaching"])
    related_html = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for u, t in spec["related"])

    canonical = f"https://drshin.kr/케이스/{spec['slug']}/"

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec["title"])} — Hepatology Note</title>
<meta name="description" content="{esc(spec["title"])} — 간암 임상 케이스 노트.">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(spec["title"])}">
<meta property="og:description" content="간암 임상 케이스 노트">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=3">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=3">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=3">
<link rel="manifest" href="/site.webmanifest?v=3">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"MedicalCase","@id":"{canonical}#webpage","url":"{canonical}","name":"{esc(spec["title"])}","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}}}},
{{"@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},
{{"@type":"ListItem","position":2,"name":"케이스","item":"https://drshin.kr/케이스/"}},
{{"@type":"ListItem","position":3,"name":"{esc(spec["title"])}","item":"{canonical}"}}
]}}
]}}
</script>
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="/간암/">간암</a> › <a href="/케이스/">케이스</a> › <span>{esc(spec["title"])}</span> <span class="page-id">{page_id}</span></nav>
<h1>{esc(spec["title"])}</h1>

<div class="case-intro">
{intro_html}
</div>

{sections_html}

<div class="teaching-box">
<h2>Teaching points</h2>
<ul>{teaching_html}</ul>
</div>

<aside class="related"><h2>관련 가이드</h2><ul>{related_html}</ul></aside>

<aside class="author-box">
<img class="author-photo" src="/assets/img/author/drshin.jpg" alt="" loading="lazy">
<div class="author-info">
<p><strong>서울대학교병원 소화기내과 · 간암센터</strong></p>
<p class="muted">간암·간경변·만성 간질환 진료. 대한간학회 정회원.</p>
<p><a href="/소개/" class="more">소개 보기 →</a></p>
</div>
</aside>

{ANONYMIZATION_NOTE}
</main>

{FOOTER}
</body>
</html>
'''
    out = ROOT / "케이스" / spec["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: 케이스/{spec['slug']} [{page_id}]")


def render_landing(cases, start_page_id=12):
    rows = []
    for i, c in enumerate(cases):
        pid = f"1-{start_page_id + i}"
        intro_text = re.sub(r'<[^>]+>', '', c["intro"]).strip()
        # Use first sentence of intro as the landing card preview
        first_sentence = intro_text.split(". ")[0]
        if not first_sentence.endswith("."):
            first_sentence += "."
        rows.append(
            f'<a href="/케이스/{c["slug"]}/" class="case-row">'
            f'<span class="page-id">{pid}</span>'
            f'<div class="body"><h3>{esc(c["title"])}</h3>'
            f'<p>{esc(first_sentence)}</p></div></a>'
        )
    rows_html = "\n".join(rows)

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>간암 케이스 모음 — Hepatology Note</title>
<meta name="description" content="간암 임상 케이스 노트 {len(cases)}편.">
<link rel="canonical" href="https://drshin.kr/케이스/">
<meta property="og:type" content="website">
<meta property="og:title" content="간암 케이스 모음 — {len(cases)}편">
<meta property="og:description" content="외래 임상 결정 흐름 케이스 노트.">
<meta property="og:url" content="https://drshin.kr/케이스/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=3">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=3">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=3">
<link rel="manifest" href="/site.webmanifest?v=3">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"CollectionPage","@id":"https://drshin.kr/케이스/#webpage","url":"https://drshin.kr/케이스/","name":"간암 케이스 모음","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}}}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},{{"@type":"ListItem","position":2,"name":"케이스","item":"https://drshin.kr/케이스/"}}]}}
]}}
</script>
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="/간암/">간암</a> › <span>케이스</span></nav>

<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:32px;letter-spacing:-0.02em;font-weight:600;margin:8px 0 8px">간암 케이스 모음</h1>
<p class="intro">외래에서 자주 만나는 간세포암(HCC) 임상 시나리오를 풀어 정리한 케이스 노트입니다. 표준 가이드라인의 임상 결정 흐름을 시나리오로 따라가는 방식입니다.</p>

<div class="case-list">
{rows_html}
</div>

<p class="disclaimer" style="margin-top:48px">이 사례는 표준 진료 흐름을 보여주기 위해 구성한 교육용 예시이며, 특정 환자의 기록이 아닙니다. 실제 진료는 개인의 상태에 따라 달라집니다.</p>
</main>

{FOOTER}
</body>
</html>
'''
    (ROOT / "케이스" / "index.html").write_text(html, encoding="utf-8")
    print(f"  wrote: 케이스/index.html (landing)")


print(f"Building {len(CASES)} case pages...")
for i, c in enumerate(CASES):
    render_case(c, f"1-{12 + i}")
render_landing(CASES, start_page_id=12)
print(f"Done. Page IDs: 1-12 to 1-{12 + len(CASES) - 1}.")
