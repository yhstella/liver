"""Build 20 case pages for series 2-5 (간경화, B형간염, 지방간, 간수치).

Page IDs:
  간경화 cases: 2-11 to 2-15
  B형간염 cases: 3-11 to 3-15
  지방간 cases:  4-11 to 4-15
  간수치 cases:  5-10 to 5-14 (includes 독성간염, DILI, 자가면역간염)
"""
import os, sys, html as htmllib
sys.path.insert(0, os.path.dirname(__file__))
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def esc(s): return htmllib.escape(s or "")

NAV = '''<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></nav></div></header>'''
FOOTER = '''<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>'''

ANON_NOTE = (
    '<p class="disclaimer" style="margin-top:48px">본 케이스는 외래에서 자주 만나는 임상 케이스를 '
    '익명화하여 재구성한 교육 자료입니다. 환자 식별 정보는 모두 변경되었으며, 임상 결정은 표준 가이드라인의 한 예시일 뿐 '
    '개별 환자에 그대로 적용되지 않습니다.</p>'
)


def fig_timeline(title, marks):
    """Generate horizontal timeline SVG. marks = [(x_pct, label, sublabel, color)]"""
    items = []
    for x, label, sub, color in marks:
        cx = 60 + (x * 6.4)  # x in 0-100
        fill = color or "#1f6f5c"
        r = 11 if "current" in (color or "") else 9
        items.append(
            f'<circle cx="{cx}" cy="100" r="{r}" fill="{fill}" stroke="#fff" stroke-width="2"/>'
            f'<text x="{cx}" y="80" text-anchor="middle" font-size="12" font-weight="700" fill="{fill}">{label}</text>'
            f'<text x="{cx}" y="128" text-anchor="middle" font-size="11" fill="#5a5a5a">{sub}</text>'
        )
    return (
        f'<svg class="fig" viewBox="0 0 720 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">'
        f'<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">{esc(title)}</text>'
        '<line x1="40" y1="100" x2="690" y2="100" stroke="#5a5a5a" stroke-width="2"/>'
        + "".join(items) +
        '</svg>'
    )


def fig_compare(title, left_label, left_items, right_label, right_items):
    """Two-column comparison."""
    li = "".join(f'<text x="40" y="{84+i*22}" font-size="13" fill="#1a1a1a">• {esc(t)}</text>' for i,t in enumerate(left_items))
    ri = "".join(f'<text x="400" y="{84+i*22}" font-size="13" fill="#1a1a1a">• {esc(t)}</text>' for i,t in enumerate(right_items))
    h = max(160, 80 + 22 * max(len(left_items), len(right_items)) + 30)
    return (
        f'<svg class="fig" viewBox="0 0 720 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">'
        f'<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">{esc(title)}</text>'
        f'<rect x="20" y="48" width="340" height="{h-58}" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>'
        f'<rect x="380" y="48" width="320" height="{h-58}" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="1.5"/>'
        f'<text x="190" y="68" text-anchor="middle" font-size="13" font-weight="700" fill="#1a1a1a">{esc(left_label)}</text>'
        f'<text x="540" y="68" text-anchor="middle" font-size="13" font-weight="700" fill="#1f6f5c">{esc(right_label)}</text>'
        + li + ri +
        '</svg>'
    )


def fig_decision(title, top_box, branches):
    """Top box with downward branches. branches = [(label, subtext, highlight)]"""
    n = len(branches)
    bw = min(220, (700 - (n+1)*10) // n)
    items = []
    sx = 360
    for i, (lbl, sub, hl) in enumerate(branches):
        x = 20 + i * (bw + 14)
        cx = x + bw // 2
        bg = "#fed7aa" if hl else "#fff"
        bd = "#c2410c" if hl else "#bcbcb0"
        bw_attr = "3" if hl else "1.5"
        items.append(
            f'<line x1="{sx}" y1="100" x2="{cx}" y2="130" stroke="#5a5a5a" stroke-width="1.5"/>'
            f'<rect x="{x}" y="130" width="{bw}" height="80" rx="8" fill="{bg}" stroke="{bd}" stroke-width="{bw_attr}"/>'
            f'<text x="{cx}" y="158" text-anchor="middle" font-size="13" font-weight="600" fill="{"#c2410c" if hl else "#1a1a1a"}">{esc(lbl)}</text>'
            f'<text x="{cx}" y="180" text-anchor="middle" font-size="11" fill="{"#c2410c" if hl else "#5a5a5a"}">{esc(sub)}</text>'
        )
    return (
        f'<svg class="fig" viewBox="0 0 720 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(title)}">'
        f'<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">{esc(title)}</text>'
        f'<rect x="240" y="46" width="240" height="50" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="2"/>'
        f'<text x="360" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="#1f6f5c">{esc(top_box)}</text>'
        + "".join(items) +
        '</svg>'
    )


CASES = []

# ====================================================
# === 간경화 (Series 2) cases : 2-11 ~ 2-15
# ====================================================

CASES.append({
    "slug": "첫-식도정맥류-출혈", "page_id": "2-11", "series": "간경화",
    "title": "첫 식도정맥류 출혈 — 응급 결찰술과 2차 예방",
    "intro": "<p>58세 남성 환자입니다. 만성 B형간염 + 간경변(Child-Pugh B7)으로 외래 추적 중이셨고, 어제 저녁 흑색변과 토혈로 응급실에 내원하셨습니다. 활력징후는 혈압 95/60, 맥박 110으로 출혈 진행 상태입니다.</p>",
    "sections": [
        ("응급 처치",
         "<p>혈역학적 안정화를 먼저 시작하였습니다 — 두 개의 굵은 정맥로, 결정질 + 혈액 수혈 (Hb 7 g/dL 목표), terlipressin 정주 시작, 광범위 항생제(ceftriaxone) 예방적 투여. 위 식도 내시경을 6시간 이내 시행하여 식도정맥류 grade III에서 활동성 출혈 확인 후 <strong>내시경 결찰술(EVL)</strong>로 지혈에 성공하였습니다.</p>"),
        ("2차 예방과 경과",
         "<p>지혈 후 5일간 terlipressin 유지, 7일간 항생제 지속하였습니다. 퇴원 시 <strong>비선택적 베타차단제(카베디롤 6.25 mg bid)</strong>를 시작하고 2-4주 간격 EVL을 정맥류 소실까지 반복하기로 하였습니다. 6주 후 추적 내시경에서 정맥류 grade I로 호전, 카베디롤 유지 중 1년간 재출혈 없이 안정 상태입니다.</p>"),
    ],
    "teaching": [
        "급성 정맥류 출혈에서 terlipressin + 광범위 항생제 + 6시간 이내 내시경이 표준",
        "지혈 후 2차 예방은 EVL 반복 + 비선택적 베타차단제 병용",
        "Pre-emptive TIPS는 Child-Pugh C 또는 B + 활동성 출혈 등 고위험 환자에서 24시간 이내 검토",
        "출혈 후 항생제는 7일간 (감염 예방 효과 명확)",
    ],
    "related": [
        ("/간경변-식도정맥류/", "식도정맥류"),
        ("/updates/Baveno-VII-portal-hypertension-J-Hepatol-2022/", "Baveno VII"),
        ("/updates/preemptive-TIPS-식도정맥류-출혈/", "Preemptive TIPS 노트"),
    ],
    "figure": fig_timeline("첫 정맥류 출혈 — 응급에서 2차 예방까지", [
        (5, "0h", "응급실 도착", "#c9542b"),
        (20, "6h", "내시경 EVL", "#fbbf24"),
        (35, "5d", "약물 종료", "#fbbf24"),
        (55, "6주", "EVL 추가", "#1f6f5c"),
        (78, "3개월", "정맥류 소실", "#1f6f5c"),
        (95, "1년", "재출혈 없음", "#1f6f5c-current"),
    ]),
})

CASES.append({
    "slug": "복수-SBP-진단치료", "page_id": "2-12", "series": "간경화",
    "title": "복수 + SBP — 즉시 항생제와 albumin 보충",
    "intro": "<p>62세 여성 환자입니다. 알코올성 간경변(Child-Pugh C10)으로 비대상성 진행 후 복수가 있어 이뇨제(spironolactone + furosemide)를 복용 중이셨습니다. 3일 전부터 복부 통증·발열·의식 둔화로 응급실에 내원하셨습니다.</p>",
    "sections": [
        ("진단 — 복수천자",
         "<p>도착 즉시 진단적 복수천자를 시행하였습니다. 복수 분석에서 <strong>다형핵백혈구(PMN) 350/mm³</strong>(>250 진단 기준)로 자발성 세균성 복막염(SBP) 진단을 확정하였습니다. 혈액 배양에서는 E. coli가 확인되었습니다.</p>"),
        ("치료와 경과",
         "<p>즉시 cefotaxime 2g q8h 정주를 시작하였습니다. 동시에 <strong>albumin 1.5 g/kg(1일째) + 1 g/kg(3일째)</strong>를 보충하여 간신증후군 발생 위험을 낮추었습니다. 5일째 추적 복수천자에서 PMN 80/mm³로 호전 — 7일간 항생제 완료 후 안정 상태로 퇴원하였습니다. 퇴원 시 <strong>norfloxacin 400 mg/day</strong> 2차 예방을 시작하였습니다.</p>"),
    ],
    "teaching": [
        "발열·복통·의식 변화의 비대상성 간경변 환자 → 즉시 복수천자, 결과 기다리지 않고 항생제 시작",
        "복수 PMN ≥ 250/mm³가 SBP 진단 기준 (배양 음성이라도)",
        "Albumin 1.5/1 g/kg 보충은 간신증후군 예방에 의미 있는 효과 (Sort NEJM 1999)",
        "SBP 첫 episode 후 평생 norfloxacin 2차 예방",
    ],
    "related": [
        ("/간경변-복수/", "복수"),
        ("/간경변-간신증후군/", "간신증후군"),
    ],
    "figure": fig_compare("SBP 진단·치료의 핵심", "진단",
        ["복수천자 PMN ≥ 250/mm³", "발열·복통·의식 변화", "혈액배양 양성/음성 무관"],
        "치료",
        ["3세대 cephalosporin 즉시", "Albumin 1.5/1 g/kg", "5일째 복수 재평가", "퇴원 시 norfloxacin 2차예방"]),
})

CASES.append({
    "slug": "간성혼수-첫발생", "page_id": "2-13", "series": "간경화",
    "title": "간성혼수 첫 발생 — 유발 인자 평가와 lactulose",
    "intro": "<p>65세 남성 환자입니다. C형간염 → DAA 완치 후 잔존 간경변으로 추적 중이셨습니다. 가족이 \"오늘 아침부터 말이 어눌하고 시간을 못 맞추신다\"며 모시고 오셨습니다. West Haven grade 2 간성혼수가 의심되는 상태입니다.</p>",
    "sections": [
        ("유발 인자 평가",
         "<p>간성혼수는 거의 항상 유발 인자가 있어 그것부터 찾았습니다. 변비(3일간 배변 없음), 일주일 전 새로 시작한 PPI, 경증 요로감염 소견을 확인하였습니다. 혈액검사에서 NH3 130 μmol/L, K+ 3.0 mmol/L(저칼륨), 신기능 정상이었습니다.</p>"),
        ("치료와 예방",
         "<p>즉시 <strong>lactulose 30 mL q4h</strong>로 1일 3-4회 묽은 변 유도, 저칼륨 교정, 요로감염 항생제 시작하였습니다. 12시간 후 의식이 호전되어 grade 0로 회복되었습니다. 퇴원 시 <strong>lactulose 30 mL bid + rifaximin 550 mg bid</strong>를 시작하고 PPI를 중단하기로 하였습니다. 3개월간 재발 없이 안정 상태입니다.</p>"),
    ],
    "teaching": [
        "간성혼수는 유발 인자(변비·감염·전해질·출혈·신부전·약물·식이)를 항상 평가",
        "Lactulose 표준 — 1일 2-3회 묽은 변 목표",
        "재발 예방에 rifaximin 추가 시 재입원율 감소 (Bass NEJM 2010)",
        "PPI 장기 사용은 간성혼수 위험 인자 — 적응증 재평가 필요",
    ],
    "related": [
        ("/간경변-간성혼수/", "간성혼수"),
        ("/간경변-약물-주의/", "간경변 약물 주의"),
    ],
    "figure": fig_decision("간성혼수 — 유발 인자 평가", "간성혼수 발생", [
        ("변비", "lactulose 적정", True),
        ("감염", "항생제 + 평가", False),
        ("저칼륨", "K+ 보충", False),
        ("PPI/약물", "재평가·중단", False),
    ]),
})

CASES.append({
    "slug": "ChildC-이식대기", "page_id": "2-14", "series": "간경화",
    "title": "Child-Pugh C 진행 — 이식 평가와 대기 관리",
    "intro": "<p>54세 남성 환자입니다. 알코올성 간경변으로 1년 8개월 금주 유지 중이며, 최근 3개월간 복수 악화·간성혼수 2회·황달 진행으로 Child-Pugh C11, MELD 22점으로 비대상성이 진행되었습니다. 이식 평가 의뢰로 외래에 내원하셨습니다.</p>",
    "sections": [
        ("이식 평가",
         "<p>다학제 평가는 2주에 걸쳐 진행되었습니다. 의학적 적합(심혈관·폐·신장 모두 통과), 정신건강의학과 알코올 평가에서 6개월 이상 금주 유지·재발 위험 낮음으로 적합 판정, 사회 지지망 평가도 양호하였습니다. <strong>KONOS 이식 대기 등록</strong>과 동시에 가족 LDLT 가능성을 함께 검토하였습니다.</p>"),
        ("대기 중 관리와 경과",
         "<p>이식 대기 중에는 합병증 진행 억제가 핵심입니다 — 이뇨제 + 식염 제한 복수 관리, lactulose + rifaximin 간성혼수 재발 예방, 6주 간격 영상으로 새 결절 모니터링. 41세 동생이 LDLT 기증자로 적합하여 <strong>3개월 후 LDLT</strong> 시행하였습니다. 이식 후 1년 무재발, 면역억제 안정 상태입니다.</p>"),
    ],
    "teaching": [
        "Child-Pugh C 또는 MELD ≥ 15는 이식 평가 의뢰 임계값",
        "한국은 LDLT 비율 70%로 가족 기증 평가가 빠르게 진행됨",
        "알코올성 간경변 이식에 6개월 이상 금주 + 정신건강 평가 표준",
        "대기 중 합병증 진행 억제(복수·간성혼수·정맥류·HCC 검진)가 결과에 결정적",
    ],
    "related": [
        ("/간경변-간이식-평가/", "간이식 평가"),
        ("/간경변-Child-Pugh-MELD/", "Child-Pugh와 MELD"),
        ("/간암-간이식/", "간세포암 이식"),
    ],
    "figure": fig_timeline("Child-Pugh C → 이식 대기 → LDLT", [
        (5, "0d", "외래 의뢰", "#c9542b"),
        (15, "2주", "다학제 적합", "#fbbf24"),
        (28, "1개월", "KONOS 등록", "#fbbf24"),
        (50, "2개월", "LDLT 기증자 적합", "#1f6f5c"),
        (75, "3개월", "LDLT 시행", "#1f6f5c"),
        (95, "1년", "무재발", "#1f6f5c-current"),
    ]),
})

CASES.append({
    "slug": "간경변-새결절-평가", "page_id": "2-15", "series": "간경화",
    "title": "간경변 환자에서 새로 발견된 결절 — 정밀 평가",
    "intro": "<p>61세 여성 환자입니다. 만성 B형간염 + 간경변(Child-Pugh A6)으로 6개월마다 정기 검진을 받으시던 중, 이번 초음파에서 우엽에 1.6 cm 결절이 새로 발견되었습니다. AFP 22 ng/mL, PIVKA-II 38 mAU/mL.</p>",
    "sections": [
        ("정밀 영상",
         "<p>간경변 환자에서 새 결절은 간세포암을 우선 의심합니다. EOB-MRI를 시행하여 우엽 S5에 1.6 cm 결절에서 동맥기 조영 증강 + 정맥기 washout + 간담도기 hypointensity 패턴이 확인되었으며 LR-5(확실한 HCC)로 판정되었습니다.</p>"),
        ("결정과 경과",
         "<p>BCLC A기 단일 1.6 cm HCC, Child-Pugh A로 다학제 회의에서 <strong>고주파열치료술</strong>을 결정하였습니다. 시술은 합병증 없이 완전 괴사가 확인되었고, 1·3·6개월 영상에서 잔존 종양 없음, AFP·PIVKA-II 모두 정상화되었습니다. 향후 6개월마다 평생 추적 + 항바이러스제(TAF) 유지 계획입니다.</p>"),
    ],
    "teaching": [
        "간경변 환자의 새 결절은 HCC를 우선 의심 — 정밀 영상(동적 CT 또는 EOB-MRI) 즉시 시행",
        "1cm 이상 + 영상 진단 기준 충족 시 생검 없이 HCC 진단 가능",
        "BCLC 0/A기 + Child-Pugh A에서는 절제·소작·이식 모두 검토",
        "치료 후에도 간경변 자체는 남아 평생 6개월 검진 필요",
    ],
    "related": [
        ("/간암-진단-첫외래/", "간암 진단 첫 외래"),
        ("/B형간염-간암검진/", "B형간염 환자 간암 검진"),
        ("/간암-치료-선택/", "간암 치료 선택"),
    ],
    "figure": fig_decision("간경변 + 새 결절 — 평가 흐름", "새 결절 발견 (1.6 cm)", [
        ("동적 CT/MRI", "조영 증강 + washout", False),
        ("LR-5", "HCC 진단 확정", True),
        ("BCLC A", "RFA 또는 절제", False),
    ]),
})

# ====================================================
# === B형간염 (Series 3) cases : 3-11 ~ 3-15
# ====================================================

CASES.append({
    "slug": "직장검진-HBsAg양성", "page_id": "3-11", "series": "B형간염",
    "title": "직장 건강검진에서 HBsAg 양성 첫 발견",
    "intro": "<p>34세 남성 환자입니다. 직장 입사 건강검진에서 HBsAg 양성이 처음 확인되어 외래에 내원하셨습니다. 본인은 증상이 전혀 없으시고 가족력도 정확히 모르시는 상태입니다.</p>",
    "sections": [
        ("초기 평가",
         "<p>혈액 panel을 새로 검사하였습니다 — HBsAg 양성, HBeAg 음성/anti-HBe 양성, HBV DNA 8,000 IU/mL, ALT 28, AST 25, 알부민 4.4, 혈소판 215. 비교적 활동성이 낮은 만성 B형간염 patron 상태입니다. 복부 초음파에서 간 표면 매끈, 비장 정상으로 간경변 소견은 없었습니다.</p>"),
        ("계획",
         "<p>현재 ALT 정상 + DNA 낮음으로 즉시 항바이러스제 적응은 아닙니다. <strong>3-6개월마다 ALT/DNA 추적</strong>으로 활동성 발현 시 치료 시작 계획입니다. 동시에 <strong>가족 검사</strong>를 권고 — 부모·형제·배우자에게 HBsAg/anti-HBs/anti-HBc 검사를 받게 하였고, anti-HBs 음성인 가족은 백신 시리즈를 시작하였습니다. <strong>40세 이후 또는 진행 섬유화 시</strong>부터 6개월 간암 검진 시작 계획입니다.</p>"),
    ],
    "teaching": [
        "HBsAg 첫 양성 시 평가: HBeAg/anti-HBe, HBV DNA, ALT, 혈소판, 초음파, FIB-4",
        "치료 적응증: 활동성 간염(ALT 상승) + DNA ≥ 2,000 IU/mL, 또는 진행 섬유화·간경변",
        "가족 검사·예방 백신은 즉시 시행 (수직·수평 전파 차단)",
        "40세 이상 남성 / 50세 이상 여성 + B형간염 → 6개월 간암 검진",
    ],
    "related": [
        ("/B형간염-검사결과/", "B형간염 검사 결과지"),
        ("/가족-B형간염-검사/", "가족 검사"),
        ("/B형간염-간암검진/", "B형간염 간암 검진"),
    ],
    "figure": fig_decision("HBsAg 첫 양성 — 평가 분기", "HBsAg(+) 첫 확인", [
        ("정밀 평가", "ALT·DNA·섬유화", False),
        ("가족 검사", "anti-HBs(-) 백신", False),
        ("치료 적응증", "재평가 또는 시작", False),
        ("간암 검진", "40세부터 6개월", False),
    ]),
})

CASES.append({
    "slug": "임신중-HBsAg발견", "page_id": "3-12", "series": "B형간염",
    "title": "임신 중 HBsAg 양성 발견 — 수직 전파 예방",
    "intro": "<p>29세 임신 24주 산모 환자입니다. 산전 검사에서 HBsAg 양성이 처음 발견되어 외래 협진 의뢰가 들어왔습니다. HBeAg 양성, HBV DNA 4×10⁷ IU/mL로 매우 높은 바이러스 부하가 확인되었습니다.</p>",
    "sections": [
        ("임신 중 항바이러스 시작",
         "<p>HBV DNA가 매우 높아 출생 시 면역글로불린 + 백신만으로는 수직 전파 예방이 불충분할 수 있습니다(약 10% breakthrough). <strong>임신 28주에 TDF 300 mg/day</strong>를 시작하여 출산 시점까지 DNA를 가능한 한 낮추기로 하였습니다. TDF는 임신 카테고리 B로 안전성이 잘 입증된 약물입니다.</p>"),
        ("출산과 신생아 관리",
         "<p>출산 시점 HBV DNA 6×10⁵ IU/mL로 감소하였습니다. 신생아는 출생 12시간 이내 <strong>HBIG(B형간염 면역글로불린) + B형간염 백신 1차</strong>를 동시 접종하였고, 1·6개월에 백신 2·3차 시행하였습니다. 9개월에 HBsAg 음성 + anti-HBs 양성으로 수직 전파 차단 성공 확인. 산모의 TDF는 출산 후 4-12주까지 유지 후 ALT 모니터링 하면서 중단 검토하였습니다.</p>"),
    ],
    "teaching": [
        "임신 중 HBV DNA ≥ 2×10⁵ IU/mL는 28-32주에 TDF 시작 권고 (수직 전파 추가 차단)",
        "TDF는 임신 안전성 잘 입증 (Pan NEJM 2016) — TAF·ETV는 임신 데이터 부족",
        "신생아 출생 12시간 이내 HBIG + 백신 동시 접종 표준",
        "출산 후 산모 TDF는 ALT 추적하며 중단 검토 (재발 위험 30-50%)",
    ],
    "related": [
        ("/B형간염-결혼-임신/", "B형간염 결혼·임신"),
        ("/B형간염-평생약/", "B형간염 평생약"),
        ("/updates/Pan-TDF-pregnancy-HBV-NEJM-2016/", "Pan TDF pregnancy 노트"),
    ],
    "figure": fig_timeline("임신 중 HBV — 수직 전파 예방", [
        (10, "24주", "DNA 4×10⁷", "#c9542b"),
        (28, "28주", "TDF 시작", "#fbbf24"),
        (50, "출산", "DNA 6×10⁵", "#fbbf24"),
        (60, "12h", "HBIG+백신", "#1f6f5c"),
        (75, "6개월", "백신 3차", "#1f6f5c"),
        (92, "9개월", "anti-HBs(+)", "#1f6f5c-current"),
    ]),
})

CASES.append({
    "slug": "항암치료전-재활성화예방", "page_id": "3-13", "series": "B형간염",
    "title": "항암치료 시작 전 HBV 재활성화 예방",
    "intro": "<p>56세 남성 환자입니다. 미만성 거대 B세포 림프종으로 R-CHOP(rituximab 포함) 항암치료 시작 예정으로 종양내과에서 사전 평가 의뢰가 들어왔습니다. HBsAg 음성, anti-HBc 양성, anti-HBs 양성(약 25 mIU/mL)로 과거 자연 감염력이 있는 상태입니다.</p>",
    "sections": [
        ("재활성화 위험 평가",
         "<p>Rituximab은 B세포 고갈로 잠복 HBV 재활성화 고위험 약물입니다. anti-HBc 단독 양성 또는 anti-HBs와 함께 양성이라도 일부 환자에서 재활성화가 발생합니다(약 17% — Hsu Hepatology 2014). HBsAg 양성이라면 매우 고위험이지만, 본 환자는 HBsAg 음성·anti-HBc 양성으로 중등도 위험에 해당합니다.</p>"),
        ("예방적 항바이러스 시작",
         "<p>R-CHOP 시작 1주 전부터 <strong>엔테카비르 0.5 mg/day</strong> 예방적 투여를 시작하였습니다. 항암치료 중 매월 ALT/HBV DNA 모니터링, 항암치료 종료 후 12개월까지 항바이러스제 유지하기로 하였습니다. 6개월 항암치료 완료 후에도 ALT 정상·HBV DNA 불검출 유지 — 18개월 시점에 ETV 중단 후 3개월 추가 추적에서 재활성화 없이 안정 상태입니다.</p>"),
    ],
    "teaching": [
        "항암 시작 전 HBsAg + anti-HBc + anti-HBs 평가 표준 (특히 rituximab·면역억제제)",
        "HBsAg 양성 → 모든 환자 사전 항바이러스 (TDF/TAF/ETV)",
        "HBsAg 음성·anti-HBc 양성 → rituximab·고위험 면역억제 시 ETV 예방 권고",
        "치료 종료 후 12개월까지 항바이러스 유지 (조기 중단 시 재활성화 위험)",
    ],
    "related": [
        ("/B형간염-재활성화/", "B형간염 재활성화"),
        ("/B형간염-검사결과/", "B형간염 검사 결과지"),
    ],
    "figure": fig_compare("재활성화 위험과 예방", "환자 상태",
        ["HBsAg(-) anti-HBc(+)", "anti-HBs 25 (낮음)", "Rituximab 예정"],
        "예방 전략",
        ["엔테카비르 0.5 mg/day", "항암 1주 전 시작", "치료 종료 후 12개월 유지", "월 1회 ALT/DNA 모니터링"]),
})

CASES.append({
    "slug": "ETV-TAF-전환", "page_id": "3-14", "series": "B형간염",
    "title": "장기 ETV → TAF 전환 — 신·골 부담 평가",
    "intro": "<p>64세 남성 환자입니다. 만성 B형간염으로 엔테카비르 0.5 mg/day를 8년간 복용 중이시며 HBV DNA 불검출, ALT 정상으로 잘 조절되고 있습니다. 다만 최근 검사에서 eGFR 65 mL/min(2년 전 78), 골밀도 검사에서 요추 T-score -1.8(골감소증)이 확인되어 신·골 안전성이 더 좋은 약으로의 전환을 검토하게 되었습니다.</p>",
    "sections": [
        ("전환 결정",
         "<p>ETV는 신·골 친화적 약물이지만, 본 환자처럼 고령 + 신기능 저하 진행 + 골감소증 위험 인자가 있을 때는 TAF로의 전환을 검토합니다. TAF는 동일 효과 + 신·골 안전성 일부 우세를 가집니다. <strong>TAF 25 mg/day로 전환</strong>하기로 결정하였습니다.</p>"),
        ("경과",
         "<p>전환 후 <strong>3·6·12개월</strong> ALT/HBV DNA 모두 안정 유지(불검출). 3개월 시점 eGFR 67로 안정, 12개월 시점 eGFR 70으로 약간 호전. 골밀도는 12개월 후 T-score -1.7로 추가 악화 없이 유지 — 비타민 D + 칼슘 보충, 운동 처방 추가하였습니다.</p>"),
    ],
    "teaching": [
        "장기 ETV 사용 환자 + 신·골 위험 인자 동반 시 TAF 전환 검토",
        "전환 후에도 바이러스 억제 효과는 동등 (Shin GnL 2026 등)",
        "신기능 저하 단순한 경우 TDF는 회피, TAF가 1차",
        "골밀도 위험 인자(고령·여성·저체중·스테로이드) 시 골 평가 동시 진행",
    ],
    "related": [
        ("/B형간염-항바이러스제-비교/", "B형간염 항바이러스제 비교"),
        ("/B형간염-평생약/", "B형간염 평생약"),
        ("/updates/Shin-ETV-TAF-RCT-GnL-2026/", "Shin ETV vs TAF RCT 노트"),
    ],
    "figure": fig_compare("ETV vs TAF 전환 결정", "ETV 8년 사용 후",
        ["바이러스 억제: 우수", "ALT 정상 지속", "eGFR 78→65 (저하)", "골 T-score -1.8 (골감소증)"],
        "TAF 전환 후 1년",
        ["바이러스 억제: 동등", "eGFR 70 (약간 호전)", "골밀도 -1.7 (안정)", "비타민D·칼슘 보충"]),
})

CASES.append({
    "slug": "HBeAg-seroclearance-약중단", "page_id": "3-15", "series": "B형간염",
    "title": "HBeAg seroclearance 후 약 중단 검토",
    "intro": "<p>52세 여성 환자입니다. 만성 B형간염으로 12년간 TAF 복용 중이시며 안정 유지하던 중, 6개월 전 HBeAg 음성/anti-HBe 양성 전환(seroclearance), 최근 추적에서 HBV DNA 불검출 1년 이상 지속이 확인되어 약 중단을 검토하게 되었습니다.</p>",
    "sections": [
        ("중단 가능성 평가",
         "<p>HBeAg seroclearance + DNA 불검출 1년 이상 + 간경변 없음(Fibroscan 6.5 kPa)이라는 조건은 일부 가이드라인에서 약 중단 검토 가능 범주에 들어갑니다. 그러나 <strong>중단 후 30-50% 환자에서 ALT flare 또는 HBV DNA 재활성화</strong>가 발생할 수 있으며, 일부는 심한 간염 발생 위험이 있어 신중한 결정이 필요합니다. 환자분과 충분한 상의 후 \"약 중단 시도 + 1·3·6개월 밀착 추적\" 방향으로 결정하였습니다.</p>"),
        ("경과",
         "<p>약 중단 후 <strong>1개월</strong> ALT 32, HBV DNA 검출 안 됨. <strong>3개월</strong> ALT 45(약간 상승), HBV DNA 1,200 IU/mL — 경계 상태. <strong>6개월</strong> ALT 95, HBV DNA 8,500 IU/mL로 명확한 재활성화 발생. 환자 증상은 없었지만 활동성 간염 진단으로 <strong>TAF 재시작</strong>하였습니다. 재시작 3개월 후 ALT/DNA 모두 정상화되었습니다. \"평생 약\"의 의미를 재확인한 사례입니다.</p>"),
    ],
    "teaching": [
        "HBeAg seroclearance 후 약 중단은 일부 가이드라인 옵션이지만 30-50% 재활성화 위험",
        "중단 시도 시 1·3·6·12개월 밀착 추적 (ALT, HBV DNA)",
        "ALT > 5×ULN 또는 임상 증상 시 즉시 약 재시작",
        "HBsAg seroclearance(기능적 완치)가 진정한 중단 가능 시점",
    ],
    "related": [
        ("/B형간염-functional-cure/", "B형간염 functional cure"),
        ("/B형간염-평생약/", "B형간염 평생약"),
        ("/updates/Shin-HBeAg-seroclearance-HCC-JHepR-2024/", "HBeAg seroclearance HCC 위험"),
    ],
    "figure": fig_timeline("약 중단 시도 → 재활성화 → 재시작", [
        (5, "0", "TAF 중단", "#fbbf24"),
        (20, "1개월", "ALT 32", "#1f6f5c"),
        (40, "3개월", "DNA 1,200", "#fbbf24"),
        (62, "6개월", "ALT 95 / DNA 8,500", "#c9542b"),
        (75, "재시작", "TAF 재투여", "#1f6f5c"),
        (92, "+3개월", "정상화", "#1f6f5c-current"),
    ]),
})

# ====================================================
# === 지방간 (Series 4) cases : 4-11 ~ 4-15
# ====================================================

CASES.append({
    "slug": "검진ALT상승-MASLD진단", "page_id": "4-11", "series": "지방간",
    "title": "건강검진 ALT 65 — FIB-4부터 시작하는 평가",
    "intro": "<p>47세 남성 환자입니다. 직장 건강검진에서 ALT 65 IU/L(정상 상한 40), 초음파에서 \"중등도 지방간\" 소견으로 외래에 내원하셨습니다. BMI 27.5(과체중), 공복혈당 110, 중성지방 220, HbA1c 5.9% — 대사증후군 위험 인자 동반.</p>",
    "sections": [
        ("위험 단계화",
         "<p>지방간 환자에서 가장 중요한 질문은 \"섬유화가 있는가\"입니다. 모든 지방간 환자에게 간생검을 하지는 않고 비침습 검사로 위험을 단계화합니다. <strong>FIB-4(나이·AST·ALT·혈소판) = 1.45</strong>로 중간 위험 영역(1.30-2.67) — <strong>Fibroscan 추가 시행</strong>하여 LSM 7.2 kPa(F1-F2 의심), CAP 285 dB/m(중등도 지방축적)이 확인되었습니다. F2 진행성 섬유화 가능성으로 적극적 평가·관리 대상입니다.</p>"),
        ("관리 시작과 경과",
         "<p>B형/C형간염 음성, 자가면역·과음력 없음, 약물성 원인 없음 → MASLD로 확정 진단하였습니다. 핵심은 <strong>체중 7-10% 감량</strong> — 식이·운동 영양사 협진 + 매월 외래 추적 시작. 6개월 후 체중 6 kg 감량(80→74 kg), ALT 38로 정상화, Fibroscan 5.8 kPa로 호전. 12개월 시점 체중 9 kg 감량 유지, 모든 지표 안정 — 식이 패턴 변화가 지속되도록 동기 강화 진료 지속하였습니다.</p>"),
    ],
    "teaching": [
        "지방간 발견 시 비침습 평가 흐름: FIB-4 → Fibroscan → 모호 시 MRE/생검",
        "FIB-4 < 1.30이면 진행 섬유화 위험 낮음 (negative predictive value 우수)",
        "체중 7-10% 감량은 MASLD/MASH 호전·섬유화 회복의 가장 강한 예측 인자",
        "외래 추적 빈도 증가 + 영양사 협진이 체중 감량 성공률 향상",
    ],
    "related": [
        ("/대사이상지방간-MASLD/", "MASLD"),
        ("/지방간-정밀검사/", "지방간 정밀검사"),
        ("/지방간-치료/", "지방간 치료"),
        ("/간섬유화스캔-수치/", "Fibroscan 수치"),
    ],
    "figure": fig_decision("지방간 발견 — 비침습 평가 흐름", "ALT 65 + 초음파 지방간", [
        ("FIB-4 < 1.30", "추적 only", False),
        ("FIB-4 1.30-2.67", "Fibroscan", True),
        ("FIB-4 > 2.67", "MRE/생검", False),
    ]),
})

CASES.append({
    "slug": "MASLD-F2-GLP1시작", "page_id": "4-12", "series": "지방간",
    "title": "MASLD F2 + 비만 — GLP-1 작용제 시작",
    "intro": "<p>52세 여성 환자입니다. MASLD F2 섬유화 + 비만(BMI 32) + 2형 당뇨로 6개월간 식이·운동 관리만 시도하였으나 체중 감량 2 kg에 그쳤습니다. HbA1c 7.4%, ALT 58, Fibroscan 9 kPa로 진행성 섬유화 의심 상태가 지속되어 약물 동반을 결정하였습니다.</p>",
    "sections": [
        ("GLP-1 시작",
         "<p>당뇨 + MASLD 환자에서 <strong>GLP-1 작용제(semaglutide 1 mg/주 또는 liraglutide)</strong>는 1차 옵션이 됩니다. 체중 감량 효과 + 혈당 조절 + MASH 호전 가능성이라는 다중 효과를 가지며, Newsome NEJM 2021 RCT에서 NASH 해소 효과가 입증되었습니다. <strong>semaglutide 0.25 mg/주 시작 → 4주 간격으로 0.5, 1.0 mg까지 증량</strong>하기로 하였습니다.</p>"),
        ("경과",
         "<p><strong>3개월</strong> — 체중 4 kg 감량(80→76), HbA1c 6.8%, ALT 42. <strong>6개월</strong> — 체중 7 kg 감량 유지, HbA1c 6.5%, ALT 32, Fibroscan 7.8 kPa. <strong>12개월</strong> — 체중 9 kg 감량(80→71), Fibroscan 6.8 kPa(F1으로 호전 가능성), 환자 만족도 높음. 부작용은 초기 구역(2주 내 자연 소실) 외 없었습니다.</p>"),
    ],
    "teaching": [
        "GLP-1 작용제는 당뇨 + MASLD 환자에서 1차 옵션 — 체중·혈당·NASH 동시 효과",
        "Semaglutide(NASH RCT 데이터) > liraglutide > tirzepatide 순으로 데이터 누적",
        "0.25 → 0.5 → 1.0 mg 주별 증량으로 구역 등 부작용 최소화",
        "체중 감량과 함께 Fibroscan 호전 추세 모니터링 — 6-12개월 평가",
    ],
    "related": [
        ("/지방간-치료/", "지방간 치료"),
        ("/지방간-SGLT2-GLP1/", "SGLT2·GLP-1"),
        ("/updates/Newsome-semaglutide-NASH-NEJM-2021/", "Newsome semaglutide NASH"),
    ],
    "figure": fig_timeline("GLP-1 시작 후 1년 경과", [
        (5, "시작", "BMI 32, ALT 58", "#c9542b"),
        (25, "3개월", "체중 -4kg", "#fbbf24"),
        (50, "6개월", "체중 -7kg, ALT 32", "#1f6f5c"),
        (75, "9개월", "체중 -8kg", "#1f6f5c"),
        (95, "1년", "Fibroscan 6.8", "#1f6f5c-current"),
    ]),
})

CASES.append({
    "slug": "MASH-F3-당뇨-종합관리", "page_id": "4-13", "series": "지방간",
    "title": "MASH F3 + 당뇨 — 다약제 종합 관리",
    "intro": "<p>58세 남성 환자입니다. MASH F3 섬유화(생검 확진) + 2형 당뇨(HbA1c 8.5%) + 비만(BMI 34) + 고지혈증 동반 환자입니다. ALT 95, AST 78, Fibroscan 14 kPa로 진행성 섬유화이며 단독 약물보다 종합 관리가 필요한 상태입니다.</p>",
    "sections": [
        ("종합 관리 전략",
         "<p>F3 진행 섬유화는 간경변·HCC 위험이 의미 있게 높아 적극 관리합니다. 다음을 병행 시작 — <strong>SGLT2 억제제(empagliflozin 25 mg) + GLP-1 작용제(semaglutide 1 mg/주)</strong>(당뇨 + 체중 + 잠재적 간 보호), 영양사 협진으로 1,500 kcal 식단, 주 150분 중강도 운동, 알코올 완전 제한.</p>"),
        ("6개월 평가와 추적",
         "<p>6개월 시점 체중 8 kg 감량(95→87), HbA1c 6.7%, ALT 48, Fibroscan 11 kPa로 호전. 1년 시점 체중 12 kg 감량(95→83), Fibroscan 9 kPa로 진행 섬유화에서 중등도로 호전. <strong>HCC 검진</strong>(6개월 영상 + AFP)을 평생 유지 계획. 추후 resmetirom 적응증 평가도 검토 중입니다.</p>"),
    ],
    "teaching": [
        "MASH F3는 HCC·간경변 위험 의미 있게 높음 — 6개월 영상 검진 시작",
        "당뇨 + MASH는 SGLT2 + GLP-1 병용이 종합 효과 (체중·혈당·간)",
        "Fibroscan 호전 추적이 치료 반응 평가의 핵심 (생검 반복 회피)",
        "F2-F3 환자에서 resmetirom(MAESTRO-NASH)이 새 옵션 — 적응증 평가",
    ],
    "related": [
        ("/지방간염-MASH/", "MASH"),
        ("/지방간-SGLT2-GLP1/", "SGLT2·GLP-1"),
        ("/updates/MAESTRO-NASH-resmetirom-NEJM-2024/", "MAESTRO-NASH"),
        ("/지방간-간암/", "지방간이 간암으로"),
    ],
    "figure": fig_compare("MASH F3 — 종합 관리 6개월 결과", "치료 시작 시점",
        ["BMI 34, 체중 95 kg", "HbA1c 8.5%", "ALT 95, AST 78", "Fibroscan 14 kPa (F3)"],
        "12개월 후",
        ["BMI 30, 체중 -12 kg", "HbA1c 6.5%", "ALT 38", "Fibroscan 9 kPa (호전)"]),
})

CASES.append({
    "slug": "lean-MASLD-비만없음", "page_id": "4-14", "series": "지방간",
    "title": "BMI 22의 lean MASLD — 대사 평가에서 발견된 인슐린 저항",
    "intro": "<p>43세 여성 환자입니다. BMI 22로 정상 체중이지만 건강검진에서 ALT 58, 초음파 \"경증 지방간\" 소견으로 의뢰되었습니다. 음주력 없음, B형/C형간염 음성으로 lean MASLD로 분류됩니다.</p>",
    "sections": [
        ("정밀 평가",
         "<p>마른 사람의 지방간은 흔히 간과되지만 비만 MASLD와 비슷한 진행 위험을 가집니다. 정밀 평가 결과 — 공복 인슐린 22 (HOMA-IR 4.5, 인슐린 저항성), 중성지방 195, HDL 38(낮음), 허리둘레 78 cm로 \"체중은 정상이지만 metabolically obese\" 패턴이 확인되었습니다. FIB-4 0.95(낮음), Fibroscan 5.8 kPa(F0-F1)로 섬유화는 경미.</p>"),
        ("관리와 경과",
         "<p>체중 감량보다는 <strong>대사 개선</strong>이 핵심입니다 — 근육량 증가를 위한 저항 운동 + 정제 탄수화물·당분 제한 식이, 알코올 완전 제한. 12개월 시점 체중은 1 kg 감량으로 거의 변화 없지만 <strong>HOMA-IR 2.8, 중성지방 130, ALT 32</strong>로 모두 호전. 향후 매년 ALT/Fibroscan 추적 계획입니다.</p>"),
    ],
    "teaching": [
        "Lean MASLD(BMI < 25)도 MASLD의 25-30% 차지 — 진행 위험은 비만 MASLD와 유사",
        "허리둘레·인슐린 저항성·중성지방 등 metabolic syndrome 평가가 BMI보다 중요",
        "체중 감량 어려운 경우 근육량 증가 + 식이 질 개선이 효과적",
        "GLP-1·SGLT2는 lean 환자에서 데이터 제한적 — 약물보다 생활 습관 우선",
    ],
    "related": [
        ("/지방간-lean-MASLD/", "lean MASLD"),
        ("/대사이상지방간-MASLD/", "MASLD"),
        ("/술-안마셔도-지방간/", "술 안 마셔도 지방간"),
    ],
    "figure": fig_compare("Lean MASLD — BMI 정상이라도 대사 위험 평가", "겉보기",
        ["BMI 22 (정상)", "체중 정상"],
        "metabolically obese",
        ["허리둘레 78 cm", "HOMA-IR 4.5", "중성지방 195", "HDL 38 (낮음)"]),
})

CASES.append({
    "slug": "resmetirom-신약시작", "page_id": "4-15", "series": "지방간",
    "title": "MASH F2 + 비만 — resmetirom 신약 시작",
    "intro": "<p>54세 여성 환자입니다. MASH F2(생검 확진) + 비만(BMI 31) + 고지혈증 환자로 1년간 GLP-1 + 식이·운동을 유지하였으나 체중 감량은 4 kg에 그쳤고 ALT 65 지속되었습니다. 2024년 FDA 가속승인된 <strong>resmetirom</strong>(Rezdiffra) 적응증 검토 후 약을 추가하기로 하였습니다.</p>",
    "sections": [
        ("Resmetirom 시작",
         "<p>Resmetirom은 간 선택적 thyroid hormone receptor β agonist로 MASH 환자에서 NASH 해소·섬유화 호전을 보여 MAESTRO-NASH RCT 결과로 가속승인되었습니다. 적응증은 <strong>F2-F3 섬유화 동반 MASH</strong>이며 본 환자가 해당됩니다. <strong>resmetirom 80 mg/day</strong> 시작 — 갑상선 검사·LDL 기저값 확인 후 투여하였습니다.</p>"),
        ("경과",
         "<p><strong>3개월</strong> — ALT 48, LDL 95(기저 130에서 감소), 갑상선 정상. <strong>6개월</strong> — ALT 38, Fibroscan 7.5 kPa(기저 9.5), 부작용 경증 설사 외 없음. <strong>12개월</strong> — ALT 32, Fibroscan 6.8 kPa로 의미 있는 호전. 매년 평가 + 갑상선·LDL 모니터링 지속 계획입니다.</p>"),
    ],
    "teaching": [
        "Resmetirom 적응증: MASH F2-F3 섬유화 + 생검 또는 비침습 진단",
        "갑상선 호르몬 receptor β 작용 — TSH·LDL·AST/ALT 모니터링",
        "비용 부담 큰 신약 — 환자 동기·접근성 함께 평가",
        "GLP-1 등 기존 치료에 추가하는 보조 옵션",
    ],
    "related": [
        ("/지방간-신약-resmetirom/", "Resmetirom"),
        ("/지방간염-MASH/", "MASH"),
        ("/updates/MAESTRO-NASH-resmetirom-NEJM-2024/", "MAESTRO-NASH 노트"),
    ],
    "figure": fig_timeline("Resmetirom 시작 후 1년", [
        (5, "0", "ALT 65, F2", "#c9542b"),
        (28, "3개월", "ALT 48, LDL ↓", "#fbbf24"),
        (55, "6개월", "ALT 38", "#1f6f5c"),
        (78, "9개월", "Fibroscan 7", "#1f6f5c"),
        (95, "1년", "F2 → F1 호전", "#1f6f5c-current"),
    ]),
})

# ====================================================
# === 간수치 이상 (Series 5) cases : 5-10 ~ 5-14
# === 사용자 요청 포함: 독성간염, 약물유발 간손상, 자가면역간염
# ====================================================

CASES.append({
    "slug": "검진ALT상승-원인감별", "page_id": "5-10", "series": "간수치",
    "title": "검진 ALT 95 / AST 80 — 흔한 원인 감별",
    "intro": "<p>49세 남성 환자입니다. 직장 건강검진에서 ALT 95 / AST 80(정상 ≤ 40)으로 처음 이상 소견 발견되어 외래에 내원하셨습니다. 무증상이며, 음주는 주 1-2회 소량, 약물 복용 없음이 자기 보고입니다.</p>",
    "sections": [
        ("원인 감별 검사",
         "<p>ALT/AST 상승의 흔한 원인을 한 번에 감별하는 패널을 시행하였습니다 — HBsAg/anti-HCV(바이러스), 자가면역(ANA, ASMA, anti-LKM, IgG), 대사(공복혈당·HbA1c·지질), 갑상선(TSH·T4), 철·구리(ferritin·ceruloplasmin), 알코올 바이오마커. 동시에 <strong>복부 초음파 + Fibroscan</strong>을 시행하였습니다.</p>"),
        ("진단과 관리",
         "<p>결과: HBsAg/anti-HCV 음성, 자가면역 패널 음성, ferritin/ceruloplasmin 정상. 공복혈당 105, 중성지방 240, HDL 36, BMI 28, 초음파 \"중등도 지방간\", Fibroscan 6.5 kPa, CAP 295 — <strong>MASLD</strong>로 진단하였습니다. 약물 영향 의심 가능성은 추가 자세 문진 결과 없음. 체중 7-10% 감량 목표 + 영양사 협진 시작, 6개월 후 추적 검사 계획입니다.</p>"),
    ],
    "teaching": [
        "ALT/AST 상승 첫 평가에서 한 번에 다중 원인 감별 패널 시행 (반복 검사 회피)",
        "흔한 원인 순서: MASLD/지방간 → 알코올 → 약물 → 바이러스 → 자가면역 → 대사 (Wilson·hemochromatosis 등)",
        "복부 초음파 + Fibroscan을 첫 외래에 함께 시행하면 진단까지 시간 단축",
        "약물·보충제는 환자가 \"약 안 먹는다\" 말해도 자세히 다시 묻기 (감기약·진통제·영양제 포함)",
    ],
    "related": [
        ("/간수치-높음/", "간수치 높음"),
        ("/간수치-종류-차이/", "간수치 종류·차이"),
        ("/간섬유화스캔-수치/", "Fibroscan 수치"),
    ],
    "figure": fig_decision("ALT/AST 상승 — 첫 외래 감별 패널", "ALT 95 / AST 80", [
        ("바이러스", "HBsAg, anti-HCV", False),
        ("자가면역", "ANA, ASMA, IgG", False),
        ("대사·지방간", "초음파, Fibroscan", True),
        ("약물·알코올", "재문진", False),
    ]),
})

CASES.append({
    "slug": "자가면역간염-첫진단", "page_id": "5-11", "series": "간수치",
    "title": "젊은 여성의 자가면역간염 — 첫 진단과 치료",
    "intro": "<p>32세 여성 환자입니다. 6개월 전부터 피로·식욕 부진이 있어 검사한 결과 ALT 380, AST 290, IgG 28 g/L(상승), ANA 1:640, ASMA 양성으로 외래에 의뢰되었습니다. 음주력 없음, 약물·보충제 복용 없음. 다른 자가면역질환력 없음.</p>",
    "sections": [
        ("진단 — Simplified AIH score",
         "<p>자가면역간염(AIH)을 의심하여 추가 평가를 시행하였습니다. 바이러스(HBV/HCV/HEV) 모두 음성, 윌슨병·hemochromatosis 배제. <strong>간생검</strong>에서 interface hepatitis + plasma cell infiltration + rosetting 확인 — 전형적 AIH 조직 소견. Simplified AIH score 7점(definite)으로 AIH type 1 진단을 확정하였습니다.</p>"),
        ("치료와 경과",
         "<p>표준 치료로 <strong>prednisolone 30 mg/day + azathioprine 50 mg/day</strong>를 시작하였습니다. 4주 후 ALT 95로 빠른 반응, 8주 후 ALT 35로 정상화 — prednisolone을 점진적으로 감량(매주 5 mg씩) 시작. <strong>6개월</strong> 시점 prednisolone 7.5 mg + azathioprine 75 mg 유지로 ALT 25, IgG 정상화 확인. 향후 1년 안정 시 prednisolone 추가 감량 또는 중단 검토 계획입니다.</p>"),
    ],
    "teaching": [
        "AIH 의심 단서: 젊은 여성 + ALT 상승 + IgG 상승 + ANA/ASMA 양성",
        "Simplified AIH score (Hennes Hepatology 2008): 항체 + IgG + 조직 + 바이러스 배제로 진단",
        "표준 치료: prednisolone 단독 또는 + azathioprine 병용 (스테로이드 부작용 감소)",
        "치료 반응 평가: ALT/IgG가 정상화되면 점진 감량 — 너무 빠른 중단은 재발 위험",
    ],
    "related": [
        ("/약물성-간손상-DILI/", "약물성 간손상"),
        ("/간수치-높음/", "간수치 높음"),
        ("/간생검-언제-필요한가/", "간생검 언제 필요한가"),
    ],
    "figure": fig_timeline("AIH 첫 진단 → 6개월 안정 유도", [
        (5, "0", "ALT 380, IgG 28", "#c9542b"),
        (15, "1주", "스테로이드 시작", "#fbbf24"),
        (30, "4주", "ALT 95", "#fbbf24"),
        (50, "8주", "ALT 35 정상화", "#1f6f5c"),
        (78, "6개월", "유지요법 안정", "#1f6f5c-current"),
    ]),
})

CASES.append({
    "slug": "약물성간손상-항결핵제", "page_id": "5-12", "series": "간수치",
    "title": "항결핵제 시작 후 ALT 300 — DILI 평가",
    "intro": "<p>57세 남성 환자입니다. 잠복 결핵 양성 진단 후 isoniazid + rifampin + pyrazinamide + ethambutol 4제 표준 치료를 시작하였습니다. 6주 후 정기 검사에서 ALT 320, AST 280, 빌리루빈 1.8(정상), ALP 정상 — 무증상이지만 의미 있는 ALT 상승으로 의뢰되었습니다.</p>",
    "sections": [
        ("DILI 평가와 약물 중단",
         "<p>항결핵제 4제는 약물성 간손상의 대표적 원인이며 isoniazid·pyrazinamide가 가장 흔한 원인입니다. CIOMS/RUCAM 평가에서 시간 관계·다른 원인 배제로 <strong>약물성 간손상(probable)</strong>으로 판단하였습니다. ALT > 5×ULN(또는 ALT > 3×ULN + 증상) 기준 충족 → <strong>모든 항결핵제 즉시 중단</strong>하였습니다. 동시에 바이러스(HBV/HCV/HAV) 패널 시행 → 모두 음성 확인.</p>"),
        ("약 재시작과 경과",
         "<p>약물 중단 후 ALT 추적: 1주 후 ALT 180, 2주 후 ALT 75, 3주 후 ALT 38로 정상화 — 약물 원인 확인. 결핵 치료를 계속해야 하므로 <strong>단계적 재시작</strong> 시행 — rifampin → ethambutol → isoniazid 순으로 1주 간격 추가, ALT 모니터링. Pyrazinamide는 회피, isoniazid는 저용량부터 단계 증량. 재시작 8주 후 ALT 안정 + 결핵 치료 지속 가능 확인하였습니다.</p>"),
    ],
    "teaching": [
        "약물성 간손상(DILI) 평가: 시간 관계, 약물 중단 후 호전, 다른 원인 배제 (RUCAM score)",
        "항결핵제 중 isoniazid·pyrazinamide가 가장 흔한 DILI 원인",
        "ALT > 5×ULN 또는 임상 증상 시 즉시 약물 중단",
        "필수 약물(결핵·HIV 등)은 단계적 재시작으로 원인 약 식별 가능",
    ],
    "related": [
        ("/약물성-간손상-DILI/", "약물성 간손상"),
        ("/간수치-높음/", "간수치 높음"),
    ],
    "figure": fig_timeline("항결핵제 DILI — 중단 후 호전 → 단계 재시작", [
        (5, "0", "약 시작", "#1f6f5c"),
        (20, "6주", "ALT 320", "#c9542b"),
        (28, "중단", "모든 약 중지", "#fbbf24"),
        (42, "+2주", "ALT 75", "#1f6f5c"),
        (55, "+3주", "정상화", "#1f6f5c"),
        (75, "재시작", "단계적 재투여", "#1f6f5c"),
        (95, "+8주", "안정 유지", "#1f6f5c-current"),
    ]),
})

CASES.append({
    "slug": "독성간염-야생버섯", "page_id": "5-13", "series": "간수치",
    "title": "야생 버섯 식이 후 급성 간부전 — α-amanitin 독성",
    "intro": "<p>61세 남성 환자입니다. 등산에서 채취한 야생 버섯을 식이한 12시간 후부터 심한 구토·복통·설사로 응급실 도착, 24시간 후 ALT 4500, AST 5800, INR 2.8, 빌리루빈 4.5로 급성 간부전 양상이 진행되어 즉시 입원하였습니다. 가족이 가져온 버섯 사진에서 Amanita phalloides(독우산광대버섯)으로 동정되었습니다.</p>",
    "sections": [
        ("응급 처치",
         "<p>α-amanitin은 RNA polymerase II를 억제하여 간세포·신장 세포 사멸을 일으키는 강력한 독소입니다. 표준 치료를 즉시 시작 — <strong>고용량 silibinin(Legalon SIL) 정주</strong>(α-amanitin 흡수 차단), <strong>N-acetylcysteine(NAC) 정주</strong>(글루타치온 보충), <strong>활성탄</strong>(장간순환 차단), 적극적 수액·전해질 교정. 동시에 KONOS 응급 이식 등록(MELD 32, status 1)을 진행하였습니다.</p>"),
        ("경과",
         "<p>치료 48시간 후에도 ALT/AST 상승 지속(ALT 5800, INR 3.5), King's College criteria 충족 — <strong>응급 LT</strong>가 유일한 생존 옵션 상태가 되었습니다. 다행히 <strong>3일째</strong> deceased donor liver transplant(DDLT) 시행하여 합병증 없이 회복되었습니다. <strong>6개월</strong> 시점 면역억제 안정, 신기능·간기능 모두 정상. 환자 가족 교육 — \"야생 버섯은 절대 먹지 않는다\" 강력 권고.</p>"),
    ],
    "teaching": [
        "Amanita phalloides 독성: 잠복기 6-24시간 후 위장관 증상 → 간부전 (\"deceptive\" 패턴)",
        "α-amanitin 표준 치료: silibinin + NAC + 활성탄 + 적극적 supportive care",
        "King's College criteria 충족 시 응급 이식 등록 — 한국 KONOS status 1",
        "야생 버섯·민간요법 약초·일부 한약은 독성간염 흔한 원인 — 환자 교육 필수",
    ],
    "related": [
        ("/약물성-간손상-DILI/", "약물성 간손상"),
        ("/간수치-높음/", "간수치 높음"),
        ("/간경변-간이식-평가/", "간이식 평가"),
    ],
    "figure": fig_timeline("야생 버섯 독성 → 급성 간부전 → 이식", [
        (5, "0h", "버섯 식이", "#1f6f5c"),
        (15, "12h", "구토·복통", "#fbbf24"),
        (28, "24h", "ALT 4500", "#c9542b"),
        (45, "48h", "INR 3.5, 이식 등록", "#c9542b"),
        (65, "3일", "DDLT 시행", "#fbbf24"),
        (88, "6개월", "안정 회복", "#1f6f5c-current"),
    ]),
})

CASES.append({
    "slug": "보충제-ALT상승", "page_id": "5-14", "series": "간수치",
    "title": "보디빌딩 보충제 후 ALT 150 — 영양제 평가",
    "intro": "<p>28세 남성 환자입니다. 헬스장에서 권유받은 단백질·근성장 보충제와 \"천연 테스토스테론 부스터\"를 3개월 복용 후 정기 건강검진에서 ALT 152, AST 95 발견되어 의뢰되었습니다. 무증상, 음주력 거의 없음, 처방 약물 없음.</p>",
    "sections": [
        ("원인 평가",
         "<p>젊은 환자에서 ALT 상승의 흔한 \"숨은\" 원인이 보충제·약초·근성장 supplement입니다. 환자분께 모든 복용 supplement를 사진 찍어 가져오시도록 한 결과 — pre-workout 보충제, 단백질 파우더 외 \"natural anabolic\"이라는 라벨의 한 제품에 anabolic steroid 유사 성분이 포함된 것으로 확인되었습니다. 자세한 평가 — 바이러스 패널 음성, 자가면역 음성, 초음파 정상.</p>"),
        ("관리와 경과",
         "<p>모든 보충제 중단 권고하였습니다. <strong>4주 후</strong> ALT 65, <strong>8주 후</strong> ALT 32로 정상화 — supplement 원인 확인. 환자분께 \"천연·natural\"이라는 라벨이 안전을 보장하지 않으며 무허가 anabolic 성분이 포함될 수 있음을 충분히 설명. 향후 supplement 시작 전 라벨·성분 확인 + 의료진 상담 권고하였습니다.</p>"),
    ],
    "teaching": [
        "젊은 환자 ALT 상승의 흔한 원인: supplement(보충제·근성장·다이어트제·한약·영양제)",
        "환자에게 \"약 안 먹는다\" 답변에도 supplement·한약·차·다이어트제 추가 질문 필수",
        "Anabolic steroid 함유 무허가 supplement는 콜레스타시스·간염·종양 위험",
        "원인 의심 supplement 중단 후 ALT 추세 추적이 진단 확인의 가장 강력한 도구",
    ],
    "related": [
        ("/약물성-간손상-DILI/", "약물성 간손상"),
        ("/간수치-높음/", "간수치 높음"),
    ],
    "figure": fig_timeline("Supplement 중단 → ALT 호전", [
        (5, "0", "보충제 3개월", "#c9542b"),
        (20, "검진", "ALT 152", "#c9542b"),
        (35, "중단", "모든 supplement", "#fbbf24"),
        (58, "+4주", "ALT 65", "#fbbf24"),
        (85, "+8주", "ALT 32 정상화", "#1f6f5c-current"),
    ]),
})


# === Render ===
def render_case(spec):
    sections_html = ""
    for idx, (h2, body) in enumerate(spec["sections"]):
        sections_html += f'<div class="case-section"><h2>{esc(h2)}</h2>\n{body}\n</div>\n\n'
        if idx == 0 and spec.get("figure"):
            sections_html += spec["figure"] + "\n\n"

    teaching_html = "".join(f'<li>{esc(t)}</li>' for t in spec["teaching"])
    related_html = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for u, t in spec["related"])

    canonical = f"https://drshin.kr/케이스/{spec['slug']}/"
    series = spec["series"]
    series_url = {
        "간경화": "/간경화/", "B형간염": "/B형간염/",
        "지방간": "/지방간/", "간수치": "/간수치/",
    }[series]

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec["title"])} — Hepatology Note</title>
<meta name="description" content="{esc(spec["title"])} — {esc(series)} 임상 케이스 노트.">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(spec["title"])}">
<meta property="og:description" content="{esc(series)} 임상 케이스 노트">
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
{{"@type":"MedicalCase","@id":"{canonical}#webpage","url":"{canonical}","name":"{esc(spec["title"])}","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}}}},
{{"@type":"BreadcrumbList","itemListElement":[
{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},
{{"@type":"ListItem","position":2,"name":"{esc(series)}","item":"https://drshin.kr{series_url}"}},
{{"@type":"ListItem","position":3,"name":"케이스","item":"https://drshin.kr/케이스/"}},
{{"@type":"ListItem","position":4,"name":"{esc(spec["title"])}","item":"{canonical}"}}
]}}
]}}
</script>
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="{series_url}">{esc(series)}</a> › <a href="/케이스/">케이스</a> › <span>{esc(spec["title"])}</span> <span class="page-id">{spec["page_id"]}</span></nav>
<h1>{esc(spec["title"])}</h1>

<div class="case-intro">
{spec["intro"]}
</div>

{sections_html}

<div class="teaching-box">
<h2>Teaching points</h2>
<ul>{teaching_html}</ul>
</div>

<aside class="related"><h2>관련 가이드</h2><ul>{related_html}</ul></aside>

{ANON_NOTE}
</main>

{FOOTER}
</body>
</html>
'''
    out = ROOT / "케이스" / spec["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: 케이스/{spec['slug']} [{spec['page_id']}]")


print(f"Building {len(CASES)} new case pages...")
for c in CASES:
    render_case(c)
print(f"Done.")
