"""Build 15 virtual case pages for 간암 series + /케이스/ landing page."""
import sys, os, html as htmllib
sys.path.insert(0, os.path.dirname(__file__))
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def esc(s): return htmllib.escape(s or "")

NAV = '''<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a></nav></div></header>'''
FOOTER = '''<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>'''

CASES = []

# === 진단 케이스 ===
CASES.append({
    "slug": "건강검진-우연발견-1cm결절",
    "category": "진단",
    "title": "건강검진에서 우연히 발견된 1cm 결절",
    "subtitle": "50대 남성, 무증상, B형간염 검사력 모름",
    "patient": "52세 남성 · 회사원 · BMI 25",
    "summary": "직장 건강검진 복부 초음파에서 우연히 발견된 약 1.0 cm 저에코 결절. 음주 없음, 약물 없음. 과거 B형간염 검사 받은 기억 없음.",
    "sections": [
        ("첫 만남",
         "<p>증상은 전혀 없으십니다. 가족력도 특별한 것 없으세요. 몸이 가볍고 배도 안 부으시고, 식욕도 좋으시다고 하시고요. 그런데 회사 건강검진 결과지에 \"간 우엽에 약 1cm 저에코 결절, 추가 정밀검사 권유\"라고 적혀 있었어요.</p><p>이런 경우 외래에서 가장 먼저 확인하는 건 두 가지예요. <strong>위험 인자가 있는가</strong>(B형/C형 간염, 간경변, 음주, 가족력)와 <strong>이 결절이 무엇으로 보이는가</strong>입니다.</p>"),
        ("검사 — 위험 인자부터",
         "<p>혈액검사를 새로 시행했습니다.</p>"
         "<table class=\"lab-table\"><tr><td>HBsAg</td><td class=\"abn\">양성</td></tr><tr><td>anti-HBs</td><td>음성</td></tr><tr><td>anti-HBc</td><td>양성</td></tr><tr><td>HBV DNA</td><td class=\"abn\">12,000 IU/mL</td></tr><tr><td>HBeAg</td><td>음성, anti-HBe 양성</td></tr><tr><td>AST / ALT</td><td>38 / 42 IU/L</td></tr><tr><td>알부민 / PT INR</td><td>4.2 / 1.0</td></tr><tr><td>혈소판</td><td>168 ×10³/μL</td></tr><tr><td>AFP / PIVKA-II</td><td>15 ng/mL / 28 mAU/mL</td></tr></table>"
         "<p>몰랐던 만성 B형간염이 발견되었어요. 이게 결절을 보는 시각을 완전히 바꿉니다. 50세 이상 남성 + 만성 B형간염 + 간 결절 = 간세포암 가능성을 1순위로 두고 평가하게 됩니다.</p>"),
        ("영상 — 동적 CT",
         "<p>역동적 4-phase CT를 시행했습니다. 우엽 S5 segment에 1.1 cm 결절이 동맥기에 강한 조영 증강, 정맥기·지연기에 washout을 보였어요. 전형적인 간세포암의 영상 진단 기준(KLCA-NCC)을 만족합니다.</p>"),
        ("진단·결정",
         "<p>BCLC 0기(very early) 간세포암으로 진단합니다. 조직검사 없이 영상 기준만으로 진단되는 드문 종양 중 하나가 간세포암이에요. 1cm 단일 종양 + Child-Pugh A + ECOG 0 — 가장 좋은 시작점입니다.</p><p>다학제 회의에서 두 옵션을 검토했습니다 — 외과 절제 vs 고주파열치료술. 종양 위치(피막에서 약간 깊음)·간 기능 보존을 고려해 <strong>고주파열치료술</strong>을 권유했어요. 동시에 <strong>TDF 항바이러스제</strong>를 시작합니다.</p>"),
        ("경과",
         "<p><strong>1개월</strong> — 시술 부위 통증 며칠 후 사라짐. 영상에서 종양 부위 완전 괴사 확인. <strong>3개월</strong> — AFP 8, PIVKA-II 22로 정상화. CT에서 잔존 종양 없음. <strong>6개월</strong> — 새 결절 없음, HBV DNA 불검출. 향후 6개월마다 영상 + 종양표지자 추적 + TDF 평생 복용 계획입니다.</p>"),
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
    "category": "진단",
    "title": "B형간염 정기 검진에서 새로 발견된 2cm 결절",
    "subtitle": "55세 여성, 만성 B형간염 10년 추적 중",
    "patient": "55세 여성 · 만성 B형간염 보균 10년",
    "summary": "TDF 복용 중인 만성 B형간염 환자. 6개월마다 정기 간암 검진 중 이번 초음파에서 우엽에 2.1 cm 새 결절 발견. AFP·PIVKA-II는 모두 정상.",
    "sections": [
        ("첫 만남",
         "<p>10년 동안 한 번도 안 빠지고 6개월마다 검진을 받으셨어요. 작년 검진까지는 모두 정상이었습니다. 이번 초음파에서 우엽 S6에 2.1 cm 결절이 새로 보였어요. AFP는 6 ng/mL, PIVKA-II는 28 mAU/mL로 모두 정상 범위입니다.</p><p>\"마커가 정상인데 간암일까요?\"가 환자분의 첫 질문이었어요. 충분히 그러실 만합니다. 그런데 마커가 정상이어도 약 30-40%의 간암이 발견되기 때문에 영상이 결정적입니다.</p>"),
        ("영상 — 동적 MRI",
         "<p>Gd-EOB-MRI를 시행했습니다. 동맥기에 강한 조영 증강, 정맥기에 washout, 간담도기에 hypointensity — 전형적인 간세포암 패턴입니다. 다른 부위 새 결절 없음, 혈관 침범 없음, 원격 전이 없음.</p>"),
        ("진단·결정",
         "<p>BCLC A기 단일 2.1 cm 간세포암. Child-Pugh A, ECOG 0, HBV DNA 불검출(TDF 잘 듣고 있음). 다학제에서 절제·소작·이식을 모두 검토했어요. 종양 위치가 피막 가까이라 절제·소작 모두 가능. 환자분 선호와 회복 시간을 고려해 <strong>복강경 부분 절제</strong>를 결정했습니다.</p>"),
        ("경과",
         "<p>수술은 합병증 없이 끝났고 5일째 퇴원하셨어요. 병리에서 단일 간세포암, 미세혈관 침범 없음, 절제연 음성. <strong>3개월</strong> — 회복 양호, 영상 정상. <strong>1년</strong> — 새 결절 없음. <strong>2년</strong> — 새 결절 없음, AFP·PIVKA-II 모두 정상. 평생 6-12개월 추적 + TDF 유지 계획입니다.</p>"),
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
    "category": "진단",
    "title": "AFP만 올라가는데 영상은 정상",
    "subtitle": "60대 남성, B형간염 환자, AFP 350",
    "patient": "62세 남성 · 만성 B형간염 · 간경변 의심",
    "summary": "엔테카비르 복용 중. 정기 검진에서 AFP가 6→48→350 ng/mL로 점진적 상승. 그러나 초음파·CT에서는 결절 안 보임. 어떻게 평가하나.",
    "sections": [
        ("첫 만남",
         "<p>지난 1년간 AFP가 6→48→350 ng/mL로 점진적으로 올랐어요. 매번 영상을 추가했지만 결절은 안 보입니다. 환자분은 \"이 정도면 간암이 시작된 거 아니에요?\"라며 불안해하세요.</p><p>AFP 상승의 원인은 다양합니다. 간세포암 외에도 활동성 간염, 간 재생, 임신, 일부 다른 종양에서도 오를 수 있어요. 350 정도면 간암 의심을 적극 평가해야 하는 수준입니다.</p>"),
        ("재평가 — 영상 강화",
         "<p>EOB-MRI를 시행했습니다. 그동안 초음파·CT에서 안 보였던 우엽 S8에 0.8 cm 결절이 동맥기 조영 증강, 간담도기에 hypointensity로 보였어요. 작은 크기라 일반 영상에서는 놓쳤던 거예요.</p><p>혈액검사: ALT 35, HBV DNA 불검출(약 잘 듣고 있음), 알부민 3.6, INR 1.1, 혈소판 105 ×10³(혈소판 감소 — 간경변 신호).</p>"),
        ("진단·결정",
         "<p>EOB-MRI에서의 패턴 + AFP 추세 상승 + 위험 인자(B형간염·간경변)를 종합해 <strong>BCLC 0기 간세포암으로 진단</strong>했습니다. 0.8cm는 작지만 진단 기준을 충족합니다.</p><p>다학제에서 <strong>고주파열치료술</strong>을 결정했어요. 위치가 피막에서 충분히 떨어져 안전합니다.</p>"),
        ("경과",
         "<p><strong>1개월</strong> — 시술 후 영상에서 완전 괴사. AFP 60으로 빠르게 떨어짐. <strong>3개월</strong> — AFP 12로 정상화. <strong>6개월</strong> — AFP 8 유지, 새 결절 없음. 6개월 추적 + 엔테카비르 유지 + 추후 TAF 전환 검토.</p>"),
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
    "category": "진단",
    "title": "LI-RADS 3 모호한 결절 — 추적인가, 정밀인가",
    "subtitle": "58세 여성, B형간염, LR-3 결절 발견",
    "patient": "58세 여성 · 만성 B형간염 · TAF 복용 중",
    "summary": "정기 검진 EOB-MRI에서 1.5 cm 결절 발견. 동맥기 조영 증강은 약하고 washout 명확하지 않음 — LI-RADS 3(중등도 의심) 분류.",
    "sections": [
        ("첫 만남",
         "<p>EOB-MRI 결과지를 들고 오셨어요. \"LI-RADS 3\"이라는 단어가 적혀 있어 무슨 뜻인지 궁금해 하세요. LI-RADS는 간세포암 영상 분류 체계로 LR-1(확실히 양성)부터 LR-5(확실한 간세포암)까지 5단계로 나눕니다. <strong>LR-3는 중등도 의심</strong>으로 양성·악성 어느 쪽도 단정 못 하는 회색지대예요.</p><p>이 단계에서 선택은 두 가지: 추적 관찰 vs 추가 영상·생검.</p>"),
        ("판단 — 위험과 추가 평가",
         "<p>이 환자는 만성 B형간염 + 진행 섬유화(Fibroscan 11 kPa) + 50대 후반 여성 — 간세포암 위험이 의미 있게 높습니다. 단순 추적보다 적극적 평가를 결정했어요.</p><p>조영 초음파(CEUS)를 추가했습니다. 동맥기 조영 증강 후 비교적 빠른 washout 양상이 보였어요. 일부 LR-4(가능성 있는 간세포암)으로 reclassify됩니다.</p>"),
        ("진단·결정",
         "<p>LR-4는 단독으로 진단 확정은 어려워 다학제에서 결정했어요. 옵션: 1) 짧은 간격 추적(2-3개월), 2) 생검, 3) 시술적 진단·치료(고주파열치료술 시 조직 동시 채취). 환자분 선호로 <strong>2-3개월 후 EOB-MRI 추적</strong>을 결정했습니다.</p><p>3개월 후 EOB-MRI: 결절이 1.7 cm로 약간 커지고, 동적 패턴이 더 명확해져 LR-5(확실한 간세포암)로 reclassify. 진단 확정.</p>"),
        ("치료와 경과",
         "<p>1.7 cm 단일 종양 — Child-Pugh A. 고주파열치료술 시행. 시술 후 1·3·6개월 영상에서 완전 반응 유지. AFP·PIVKA-II 정상 유지. TAF 지속.</p>"),
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
    "category": "진단",
    "title": "PIVKA-II 1500인데 와파린 복용 중",
    "subtitle": "70세 남성, 심방세동·B형간염, PIVKA-II 위양성?",
    "patient": "70세 남성 · 심방세동 · 만성 B형간염 · 와파린 복용",
    "summary": "정기 검진에서 PIVKA-II 1500 mAU/mL로 매우 높음. 와파린 복용 중이라 위양성 가능. AFP는 12로 정상.",
    "sections": [
        ("첫 만남",
         "<p>심방세동으로 와파린을 5년째 복용하고 계세요. 만성 B형간염도 동반 — 엔테카비르로 잘 조절되고 있습니다. 정기 검진에서 PIVKA-II가 1500 mAU/mL로 충격적으로 높게 나왔어요. 환자분이 매우 불안해 하십니다.</p><p>먼저 알아야 할 것: <strong>와파린·DOAC·항생제·비타민 K 결핍은 PIVKA-II를 위양성으로 매우 높게 만들 수 있습니다</strong>. 이 환자에서 1500은 위양성 가능성이 매우 높아요.</p>"),
        ("배제 — 영상부터",
         "<p>EOB-MRI를 시행. 간 전체 영역에서 결절 없음. 종양 의심 소견 전혀 없음. 추가로 흉부 CT·뼈 영상에서 다른 종양도 없음.</p><p>혈액검사: AFP 12 (정상), ALT 28, HBV DNA 불검출, INR 2.4 (와파린 적정).</p>"),
        ("결정",
         "<p>PIVKA-II 위양성으로 결론. \"종양표지자 1500\"이 환자분께는 무서운 숫자였지만 임상 맥락이 다 설명합니다. 와파린 → 비타민 K 의존적 카르복실화 차단 → 비정상 prothrombin(PIVKA-II) 측정 상승.</p><p>만약 와파린을 DOAC(아픽사반 등)로 전환하면 PIVKA-II 측정 영향이 크게 줄지만 환자 심방세동 관리 안정성이 우선이라 와파린 유지를 결정. 향후 PIVKA-II 추적은 해석에 와파린 영향을 함께 고려.</p>"),
        ("경과",
         "<p>3개월·6개월·12개월 EOB-MRI 모두 정상. 환자분은 안심하고 일상으로 복귀. 6개월 영상 + AFP만 추적, PIVKA-II는 와파린 유지 동안 해석 보조 용도로만 사용.</p>"),
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
    "category": "진단",
    "title": "MASLD 추적 중 발견된 간세포암",
    "subtitle": "65세 비만·당뇨, B/C형 음성, 5년 추적 중 새 결절",
    "patient": "65세 남성 · BMI 31 · 2형 당뇨 · 고지혈증 · MASLD 5년",
    "summary": "MASLD F2 섬유화로 1년마다 추적 중. 이번 EOB-MRI에서 좌엽 S3에 2.5 cm 결절 새로 발견. B/C형 간염 모두 음성, 음주 없음.",
    "sections": [
        ("첫 만남",
         "<p>5년 전 건강검진에서 지방간 + ALT 상승으로 평가 시작, F2 섬유화 진단으로 1년마다 추적 중이세요. 그동안 체중을 5kg 감량하셨고 ALT는 좋아졌어요. 그런데 이번 EOB-MRI에서 새 결절이 발견됐습니다.</p><p>\"술도 안 마시고 B형간염도 없는데 간암이라뇨\"라고 환자분이 놀라셨어요. 그러나 MASLD 기반 간세포암(MASLD-HCC)은 빠르게 늘어나는 영역입니다.</p>"),
        ("영상·검사",
         "<p>EOB-MRI: 좌엽 S3에 2.5 cm 결절, 동맥기 조영 증강 + 정맥기 washout + 간담도기 hypointensity — LR-5. 다른 결절 없음, 혈관 침범 없음.</p><p>혈액검사: AFP 45, PIVKA-II 89, ALT 38, AST 42, 알부민 4.0, INR 1.05, 혈소판 142, HbA1c 7.2%, BMI 31.</p>"),
        ("진단·결정",
         "<p>BCLC A기 단일 2.5 cm 간세포암. Child-Pugh A. 다학제에서 절제·소작 모두 가능 평가. 위치(좌엽 표면 가까움)와 환자 선호로 <strong>복강경 좌엽 외측구역 절제</strong>를 결정.</p><p>동시에 동반 질환 평가 — 당뇨 강화 관리(metformin → SGLT2/GLP-1 추가), 체중 7-10% 감량 목표, 식이·운동 영양사 협진.</p>"),
        ("경과",
         "<p>수술 합병증 없이 회복. 병리: 단일 간세포암, 미세혈관 침범 없음, 절제연 음성, 배경 간조직에 MASH F3 섬유화 확인. <strong>1년</strong> — 새 결절 없음, 체중 6kg 감량, HbA1c 6.5%, ALT 28. 6개월마다 영상 + 마커 추적, MASLD 관리 지속.</p>"),
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

# === 치료 케이스 ===
CASES.append({
    "slug": "BCLC-A-단일3cm-절제vs소작",
    "category": "치료",
    "title": "단일 3cm 종양 — 절제와 고주파열치료술 사이",
    "subtitle": "60세 남성, BCLC A, 두 옵션이 비슷할 때",
    "patient": "60세 남성 · 만성 B형간염 · TDF 복용 · Child-Pugh A",
    "summary": "정기 검진에서 우엽 S8에 단일 3.0 cm 결절. 영상 진단 기준 충족. BCLC A, ECOG 0. 절제와 고주파열치료술 모두 가능.",
    "sections": [
        ("결정 인자 분석",
         "<p>3cm 이하 단일 결절에서 두 치료의 5년 생존이 비슷합니다. 결정은 종양 위치·간 기능·환자 선호로 갈립니다.</p><ul><li>위치: S8(우엽 후방, 횡격막 가까움) — 소작 시 횡격막 손상 위험·시야 확보 까다로움</li><li>간 기능: Child-Pugh A, HVPG 측정에서 5 mmHg(낮음) — 절제 안전</li><li>환자: 60세 BMI 24, 동반 질환 적음, 회복 의지 강함</li></ul>"),
        ("다학제 결정",
         "<p>위치 특성과 환자 상태로 <strong>복강경 우엽 부분 절제</strong>를 권유. 절제 후 정상 간 부피 충분(약 65% 잔여), 출혈 위험 낮음.</p>"),
        ("경과",
         "<p>수술 4시간, 출혈 200 mL. 5일 입원 후 퇴원. 병리: 단일 3.1cm 간세포암, 미세혈관 침범 없음, 절제연 1cm 음성. <strong>1·3·6개월</strong> 영상에서 정상, 종양표지자 정상. <strong>1년</strong> 무재발. 6개월마다 평생 추적.</p>"),
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
    "category": "치료",
    "title": "BCLC A 다발성 — 3개 결절·각 2cm 이하",
    "subtitle": "55세 여성, 다발성 RFA",
    "patient": "55세 여성 · 만성 C형간염 → DAA 완치 · 간경변 동반",
    "summary": "C형간염 DAA 완치 3년 후 정기 검진에서 우엽·좌엽에 결절 3개 (1.8/1.5/1.2 cm) 새로 발견. 모두 LR-5.",
    "sections": [
        ("결정 흐름",
         "<p>3개 결절 모두 BCLC A의 \"3개·각 ≤3cm\" 기준 안. 절제는 다중 위치라 간 부피 부담 큼. 이식은 적응증이지만 한국 KONOS·LDLT 평가에 시간 필요. 다학제에서 <strong>같은 회기에 3개 결절 모두 고주파열치료술</strong>을 결정.</p>"),
        ("시술과 경과",
         "<p>중재영상의학과에서 3개 위치를 단일 회기에 모두 소작. 시술 시간 1.5시간, 합병증 없음. <strong>1개월</strong> — 영상에서 3개 모두 완전 괴사. <strong>3개월</strong> — AFP 정상화, 새 결절 없음. <strong>6개월·1년</strong> — 무재발.</p>"),
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
    "category": "치료",
    "title": "Child-Pugh B + 단일 4cm — 절제 어렵고 이식 평가",
    "subtitle": "58세 남성, 비대상성 간경변 + HCC, LDLT 평가",
    "patient": "58세 남성 · 알코올성 간경변 · 1년 금주 중 · Child-Pugh B7",
    "summary": "정기 검진에서 우엽 단일 4.0 cm 간세포암 발견. Child-Pugh B7(복수 경증, 알부민 3.0). MELD 14. 절제는 간 기능 부담 큼.",
    "sections": [
        ("평가",
         "<p>Milan criteria(단일 ≤5cm) 안. Child-Pugh B로 절제 위험 큼. 알코올 1년 금주 유지 중 — 이식 평가 가능. 다학제에서 <strong>간이식 평가 시작</strong> 결정. 동시에 대기 기간 동안 종양 진행 막기 위한 bridging therapy로 <strong>TACE</strong>를 시행.</p>"),
        ("이식 평가와 경과",
         "<p>다학제 평가 1.5주 — 의학·외과·정신건강의학(알코올 평가)·심혈관 모두 적합. 가족 중 50대 형이 LDLT 기증자로 적합 평가. <strong>2개월</strong> 후 LDLT 시행. 합병증 없이 회복.</p><p>병리: Milan 기준 안의 단일 간세포암, 미세혈관 침범 없음. <strong>3개월</strong> — 면역억제 안정. <strong>1년</strong> — 무재발, 절대 금주 유지. mTOR 억제제(시롤리무스)로 전환 검토.</p>"),
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
    "category": "치료",
    "title": "BCLC B 다발성 — TACE 1차",
    "subtitle": "67세 남성, 4개 결절 양엽, Child-Pugh A",
    "patient": "67세 남성 · 만성 B형간염 · TAF 복용 · Child-Pugh A6",
    "summary": "양엽에 4개 결절 (3.5/2.8/2.2/1.5 cm). 혈관 침범 없음, 원격 전이 없음. BCLC B. ECOG 0.",
    "sections": [
        ("결정",
         "<p>BCLC B 표준은 TACE. 다발성·양엽이라 절제는 간 부피 부담 큼, 다중 RFA도 어려움. 다학제에서 <strong>conventional TACE</strong> 1차 결정.</p>"),
        ("시술과 경과",
         "<p>좌·우엽 분리 시행. 첫 회기에 우엽 3개 결절, 4주 후 좌엽 1개. 각 시술 후 발열·복통(post-embolization syndrome) 2-3일. <strong>4-6주 후 영상</strong> — 4개 모두 종양 위축, 1개는 잔존 viable 부분 확인. <strong>3개월</strong>에 잔존 부위 추가 TACE. <strong>6개월</strong> — 모두 완전 괴사. <strong>1년</strong> — 새 결절 없음, 간 기능 안정.</p>"),
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
    "category": "치료",
    "title": "8cm 큰 종양 — TACE + SBRT 결합",
    "subtitle": "62세 남성, BCLC B 큰 단일 종양",
    "patient": "62세 남성 · 만성 B형간염 · Child-Pugh A · BMI 26",
    "summary": "우엽에 단일 8.2 cm 종양, 혈관 침범 없음. 절제는 잔여 간 부피 부족 위험. 다학제에서 결합 치료 결정.",
    "sections": [
        ("결정",
         "<p>8cm 단일 큰 종양은 절제·이식·TACE 단독 모두 한계. 다학제에서 <strong>TACE → 4-6주 후 SBRT</strong> 결합을 결정. 큰 종양에서 두 치료 결합이 단독보다 우월한 데이터(STRBED, TACE-HIGH 등) 활용.</p>"),
        ("시술과 경과",
         "<p>TACE 시행 — 종양 약 30% 위축. <strong>5주 후</strong> SBRT 시행 (3분할 고선량). <strong>3개월 후</strong> 영상 — 종양 약 70% 위축, 일부 viable. <strong>6개월</strong> — 안정 또는 추가 위축. AFP는 850→120→45로 빠른 감소. 다학제에서 <strong>다운스테이징 성공으로 이식 평가</strong> 시작.</p>"),
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
    "category": "치료",
    "title": "문맥 침범 BCLC C — atezo+bev 1차",
    "subtitle": "55세 남성, 문맥 분지 침범, 면역치료 시작",
    "patient": "55세 남성 · 만성 B형간염 · Child-Pugh A · ECOG 1",
    "summary": "5cm 단일 종양 + 우문맥 분지 침범. 폐·뼈 전이 없음. BCLC C. 정맥류 작은 정도, 출혈 이력 없음.",
    "sections": [
        ("결정",
         "<p>BCLC C 1차 표준은 면역치료. 정맥류 평가에서 작은 정맥류 + 출혈 이력 없음 — 베바시주맙 사용 가능. 다학제에서 <strong>atezolizumab + bevacizumab</strong> 1차 결정.</p>"),
        ("치료와 경과",
         "<p>3주마다 외래 정주. 첫 6주 — 경증 피로 외 부작용 없음. <strong>9주</strong> 영상 — 종양 30% 위축, 문맥 침범 부분 안정. AFP 1200→340. <strong>6개월</strong> — 종양 50% 위축, 문맥 침범 일부 복원, 새 병변 없음. 갑상선 기능 저하 발생 — 갑상선 호르몬 보충으로 조절. <strong>1년</strong> — 안정 반응 유지, AFP 65.</p>"),
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
    "category": "치료",
    "title": "정맥류 출혈 이력 + BCLC C — STRIDE 선택",
    "subtitle": "63세 남성, 베바시주맙 회피, durva+treme",
    "patient": "63세 남성 · 만성 B형간염 + 간경변 · 과거 정맥류 출혈 1회 (2년 전)",
    "summary": "다발성 종양 + 우문맥 침범. BCLC C. 2년 전 식도정맥류 출혈 후 결찰술 + 카베디롤 유지 중. Child-Pugh B7.",
    "sections": [
        ("결정",
         "<p>BCLC C 1차 옵션 atezo+bev은 베바시주맙 출혈 위험으로 회피. 다학제에서 <strong>STRIDE(durvalumab + tremelimumab 1회 priming)</strong> 결정. HIMALAYA 시험 근거.</p>"),
        ("치료와 경과",
         "<p>트레멜리무맙 1회 + 듀발루맙 4주마다 유지. 첫 12주 — 면역 부작용 없음, 종양 약간 위축. <strong>6개월</strong> — 종양 안정, 문맥 침범 일부 복원. <strong>1년</strong> — 안정 반응, ALT 약간 상승했으나 약물 보류·스테로이드 짧게로 조절. <strong>2년</strong> — 무진행 생존, 환자 일상 활동 유지.</p>"),
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
    "category": "치료",
    "title": "큰 종양 다운스테이징 → 이식 후보 전환",
    "subtitle": "57세 남성, 7cm 종양 → TACE+SBRT → 이식",
    "patient": "57세 남성 · 만성 B형간염 + 초기 간경변 · Child-Pugh A6",
    "summary": "단일 7.0 cm 종양, 혈관 침범 없음. Milan(≤5cm) 밖이라 처음엔 이식 후보 아님. 다운스테이징 시도.",
    "sections": [
        ("다운스테이징 시도",
         "<p>다학제에서 <strong>TACE → SBRT → 6개월 안정 평가 후 이식 등록</strong> 흐름 결정. AFP 시작 1500.</p><p>TACE 시행 → 종양 5.5 cm로 축소. 6주 후 SBRT → 3개월 후 4.5 cm로 축소(Milan 기준 안). AFP 1500→320→90으로 감소. 6개월 추적에서 안정 반응 확인 후 <strong>KONOS 등록</strong> + LDLT 평가 시작.</p>"),
        ("이식과 경과",
         "<p>딸이 LDLT 기증자 적합. <strong>4개월 후</strong> LDLT 시행. 병리: 다운스테이징 후 4.2 cm 단일 간세포암, 미세혈관 침범 없음. <strong>1년</strong> — 무재발, 면역억제 안정. mTOR 억제제(시롤리무스)로 전환. <strong>2년</strong> — 무재발 유지.</p>"),
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
    "category": "치료",
    "title": "절제 2년 후 새 결절 — 재발 결정 흐름",
    "subtitle": "65세 여성, 첫 절제 후 2년 시점 새 결절 1개",
    "patient": "65세 여성 · 만성 C형간염 DAA 완치 · 2년 전 우엽 절제 후 무재발 추적 중",
    "summary": "절제 후 2년 6개월 시점 정기 EOB-MRI에서 좌엽 S2에 1.5 cm 새 결절 발견. 같은 위치 아닌 다른 위치 — 새로운 결절(de novo).",
    "sections": [
        ("재발 평가",
         "<p>이전 절제 부위가 아닌 다른 위치 — \"새 결절\"로 분류. 간경변 환자에서 흔한 \"second primary\" 패턴. AFP 28(약간 상승), PIVKA-II 45.</p>"),
        ("결정과 경과",
         "<p>다학제에서 위치(좌엽 표면)·크기(1.5cm)·간 기능(Child-Pugh A) 평가 — <strong>고주파열치료술</strong> 결정. 시술 합병증 없이 완전 괴사. <strong>3개월</strong> — AFP 정상화. <strong>1년</strong> — 무재발. 동시에 환자분께 \"앞으로 또 새 결절 가능\"을 충분히 설명, 6개월 검진 평생 유지 동기 강화.</p>"),
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

# === Render functions ===
def render_case(spec):
    sections_html = ""
    for h2, body in spec["sections"]:
        sections_html += f'<div class="case-section"><h2>{esc(h2)}</h2>\n{body}\n</div>\n\n'

    teaching_html = "".join(f'<li>{esc(t)}</li>' for t in spec["teaching"])
    related_html = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for u, t in spec["related"])

    canonical = f"https://drshin.kr/케이스/{spec['slug']}/"

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec["title"])} — 가상 케이스 · Hepatology Note</title>
<meta name="description" content="{esc(spec["subtitle"])}. 교육 목적 가상 환자 케이스.">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(spec["title"])} — 가상 케이스">
<meta property="og:description" content="{esc(spec["subtitle"])}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"MedicalCase","@id":"{canonical}#webpage","url":"{canonical}","name":"{esc(spec["title"])}","description":"{esc(spec["subtitle"])} (가상 교육 케이스)","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}}}},
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
<nav class="crumb"><a href="/">홈</a> › <a href="/케이스/">케이스</a> › <span>{esc(spec["title"])}</span></nav>

<span class="case-badge">{esc(spec["category"])} 케이스 · 가상</span>
<h1>{esc(spec["title"])}</h1>
<p class="meta" style="font-size:14px;color:var(--muted);margin:4px 0 16px">{esc(spec["subtitle"])}</p>

<div class="patient-card">
<h3>환자 (가상)</h3>
<p class="demo">{esc(spec["patient"])}</p>
<p class="summary">{esc(spec["summary"])}</p>
</div>

{sections_html}

<div class="teaching-box">
<h2>Teaching points</h2>
<ul>{teaching_html}</ul>
</div>

<div class="case-disclaimer">
<strong>가상 케이스</strong> — 본 환자는 교육 목적으로 만든 가상 시나리오로, 실제 환자 정보가 아닙니다. 임상 지침은 표준 가이드라인을 단순화한 예시이며 개별 환자에 그대로 적용되지 않습니다.
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

<p class="disclaimer">본 콘텐츠는 일반적 의료 정보 제공을 목적으로 하며, 개별 진료를 대체하지 않습니다.</p>
</main>

{FOOTER}
</body>
</html>
'''
    out = ROOT / "케이스" / spec["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: 케이스/{spec['slug']}")


def render_landing(cases):
    diag = [c for c in cases if c["category"] == "진단"]
    tx = [c for c in cases if c["category"] == "치료"]

    def grid_html(items, start_n):
        rows = []
        for i, c in enumerate(items, start_n):
            rows.append(f'<a href="/케이스/{c["slug"]}/"><span class="case-num">CASE {i:02d}</span><h3>{esc(c["title"])}</h3><p>{esc(c["subtitle"])}</p></a>')
        return '\n'.join(rows)

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>간암 케이스 모음 — Hepatology Note</title>
<meta name="description" content="간암(HCC) 진단·치료 가상 케이스 {len(cases)}편. 외래에서 자주 만나는 임상 시나리오 교육 목적 정리.">
<link rel="canonical" href="https://drshin.kr/케이스/">
<meta property="og:type" content="website">
<meta property="og:title" content="간암 케이스 모음 — 가상 시나리오 {len(cases)}편">
<meta property="og:description" content="진단 {len(diag)} + 치료 {len(tx)} 가상 케이스. 외래 임상 결정 흐름 교육.">
<meta property="og:url" content="https://drshin.kr/케이스/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"CollectionPage","@id":"https://drshin.kr/케이스/#webpage","url":"https://drshin.kr/케이스/","name":"간암 케이스 모음","description":"가상 환자 케이스 {len(cases)}편","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}}}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},{{"@type":"ListItem","position":2,"name":"케이스","item":"https://drshin.kr/케이스/"}}]}}
]}}
</script>
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>케이스</span></nav>

<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:32px;letter-spacing:-0.02em;font-weight:600;margin:8px 0 8px">간암 케이스 모음</h1>
<p class="intro">외래에서 자주 만나는 간세포암(HCC) 임상 시나리오를 가상 환자로 풀어낸 교육 케이스입니다. 진단 {len(diag)}편 + 치료 {len(tx)}편. 표준 가이드라인의 임상 결정 흐름을 시나리오로 따라가는 방식이며, 실제 환자 정보가 아닙니다.</p>

<p class="case-section-label">진단 케이스</p>
<div class="case-grid">
{grid_html(diag, 1)}
</div>

<p class="case-section-label">치료 케이스</p>
<div class="case-grid">
{grid_html(tx, len(diag) + 1)}
</div>

<p class="disclaimer" style="margin-top:48px">모든 케이스는 교육 목적의 가상 환자 시나리오이며, 실제 환자 정보가 아닙니다. 임상 결정은 표준 가이드라인의 예시이며 개별 환자에 그대로 적용되지 않습니다.</p>
</main>

{FOOTER}
</body>
</html>
'''
    (ROOT / "케이스" / "index.html").write_text(html, encoding="utf-8")
    print(f"  wrote: 케이스/index.html (landing)")


print(f"Building {len(CASES)} case pages...")
for c in CASES:
    render_case(c)
render_landing(CASES)
print("Done.")
