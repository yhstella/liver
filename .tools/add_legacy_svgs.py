"""Add SVG figures to legacy articles (those migrated/hand-written without svg.fig)."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from build_articles import svg_table, svg_checklist, svg_compare_two
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Per-slug SVG (one figure per legacy article, placed after first h2 section)
SVGS = {
    "간수치-높음": svg_table(
        "AST·ALT 상승 정도와 권장 행동",
        ["상승 배수", "절대값 (IU/L)", "권장"],
        [["1-2배 (경증)", "40-80", "4-6주 후 재검"],
         ["2-5배 (중등)", "80-200", "가능한 한 빨리 외래"],
         ["5배 초과 (중증)", ">200", "즉시 진료"],
         ["+ 황달·복통", "어느 단계든", "응급실"]],
        caption="외래에서 자주 쓰는 우선순위 기준"),

    "간수치-종류-차이": svg_compare_two(
        "ALT > AST 패턴",
        ["MASLD·지방간",
         "약물성 간 손상",
         "급성 바이러스성 간염 회복기",
         "정상 비율 (De Ritis < 1)"],
        "AST > ALT 패턴",
        ["알코올성 (De Ritis > 2)",
         "진행 간경변·섬유화",
         "근육 손상 (CK 동반)",
         "허혈성 간염"],
        caption="두 효소의 비율(De Ritis ratio)이 진단 방향을 좁힘"),

    "지방간-정밀검사": svg_table(
        "단계별 비침습 평가 흐름",
        ["단계", "검사", "임계값", "다음"],
        [["1차", "FIB-4 (혈액 자동 계산)", "<1.30 안전 / >2.67 위험", "위험이면 2차"],
         ["2차", "Fibroscan (간섬유화 스캔)", "MASLD <8 안전 / >12 진행", "모호하면 3차"],
         ["3차", "MRE 또는 간생검", "정확도 높지만 비싸거나 침습", "최종 판정"]],
        caption="단계 누적으로 간생검 회피 가능"),

    "알파태아단백": svg_table(
        "AFP 수치 구간별 해석",
        ["AFP (ng/mL)", "구간", "임상 행동"],
        [["≤ 10", "정상", "일반 검진 유지"],
         ["10-200", "회색지대", "영상 + 추적, 다른 원인 점검"],
         ["200-400", "의심", "동적 영상 적극, 1-3개월 추적"],
         ["> 400 + 영상 결절 ≥1cm", "강한 간암 의심", "다학제 진료"]],
        caption="AFP 단독으로 진단하지 않음 - 영상과 패턴이 결정"),

    "간섬유화스캔-수치": svg_table(
        "Fibroscan kPa 해석 (원인 질환별)",
        ["원인", "안전", "진행 의심", "간경변 의심"],
        [["MASLD", "< 8 kPa", "8-12", "> 12-15"],
         ["만성 B형간염", "< 7", "7-11", "> 11"],
         ["만성 C형간염", "< 7", "7-12.5", "> 12.5"],
         ["알코올성", "< 9.5", "9.5-17", "> 17-20"]],
        caption="원인별 임계값이 다름 - 단일 cutoff 사용 금지"),

    "대사이상지방간-MASLD": svg_compare_two(
        "MASLD (대사이상)",
        ["BMI 또는 허리둘레 ↑",
         "공복혈당·HbA1c·인슐린 저항성",
         "혈압·고지혈증",
         "대사 위험 1개 이상 + 영상 지방간"],
        "MetALD (대사+알코올)",
        ["MASLD 기준 충족",
         "+ 음주 (남 140-350g/주, 여 70-210g/주)",
         "두 원인 동시 작용",
         "심혈관·간 위험 가산"],
        caption="2023년 새 명명 - \"비-X\" 부정형 정의에서 \"대사 양성형\" 정의로"),

    "술-안마셔도-지방간": svg_checklist(
        "비음주성 지방간 5가지 시나리오",
        ["1. 비만·복부 비만 + 인슐린 저항성 (가장 흔함)",
         "2. 정상 체중이지만 인슐린 저항성 (lean MASLD)",
         "3. 2형 당뇨 + 이상지질혈증",
         "4. 과당 음료·정제 탄수화물 과다",
         "5. 약물·갑상선 기능 저하·수면 무호흡 등"],
        caption="여러 시나리오가 겹치는 경우가 흔함"),

    "지방간-치료": svg_table(
        "체중 감량 % 와 간 호전 효과",
        ["감량 %", "단순 지방간", "MASH 해결", "섬유화 호전"],
        [["3-5%", "지방량 감소", "일부", "거의 없음"],
         ["5-7%", "다수 호전", "일부", "낮은 비율"],
         ["7-10%", "대부분 호전", "약 50%", "약 25-30%"],
         ["≥ 10%", "정상화 다수", "약 90%", "약 45-50%"]],
        caption="Vilar-Gomez Gastroenterology 2015 기반"),

    "지방간-음식": svg_compare_two(
        "줄여야 할 5가지",
        ["과당 음료 (콜라·주스)",
         "정제 탄수화물 (흰빵·면)",
         "트랜스지방 (튀김·과자)",
         "가공육 (소시지·베이컨)",
         "과음 (남 1잔/일·여 0.5잔/일 이상)"],
        "늘려야 할 5가지",
        ["지중해식 식단 (전체 패턴)",
         "식이섬유 (채소·콩류·통곡물)",
         "등푸른 생선 (오메가-3)",
         "견과류 (호두·아몬드 한 줌/일)",
         "커피 (블랙 2-4잔/일)"],
        caption="특정 슈퍼푸드보다 전체 식단의 패턴"),

    "지방간-간암": svg_table(
        "MASLD 진행 단계와 연간 간암 발생률",
        ["단계", "10년 진행", "연간 HCC 위험"],
        [["단순 지방간", "MASH로 약 20%", "< 0.1%"],
         ["MASH (염증)", "섬유화로 진행", "0.1-0.3%"],
         ["F2-F3 진행 섬유화", "간경변으로 진행", "0.3-0.5%"],
         ["F4 간경변", "—", "1-2%"]],
        caption="섬유화 단계가 가장 결정적인 분기점"),

    "지방간-회복-6개월": svg_table(
        "회복 시간표 (체중 7% 감량 + 운동)",
        ["기간", "변화", "전형 패턴"],
        [["1-2개월", "ALT 시작 호전", "20-30% 감소"],
         ["3-4개월", "지방량(CAP) 감소", "10-15% 감소"],
         ["5-6개월", "변화가 굳어짐", "ALT 30-50% / CAP 10-20% 감소"],
         ["6개월+", "유지·섬유화 호전 가능", "지속 운동·식이 필요"]],
        caption="\"6개월 평가\"가 임상 표준"),

    "B형간염-평생약": svg_table(
        "1선 항바이러스제 3종",
        ["", "TDF", "TAF", "ETV"],
        [["효과", "강력", "강력 (= TDF)", "강력"],
         ["신·골 부담", "있음 (소수)", "최소", "신부전 시 용량 조정"],
         ["임신 안전성", "가장 풍부", "데이터 누적 중", "제한적"],
         ["복용", "1정/일, 식사 무관", "1정/일, 식사 무관", "공복 (식전·후 2h)"],
         ["약가 (한국)", "저렴", "비쌈", "중간"]],
        caption="환자별 신기능·골밀도·임신 계획·약가로 결정"),

    "B형간염-검사결과": svg_table(
        "HBV 표지자 조합 해석",
        ["HBsAg", "anti-HBs", "anti-HBc", "해석"],
        [["+", "-", "+", "현재 감염 (만성 또는 급성)"],
         ["-", "+", "+", "과거 감염 회복 후 면역"],
         ["-", "+", "-", "백신 면역 (자연 감염 X)"],
         ["-", "-", "-", "감수성자 - 백신 권장"],
         ["-", "-", "+", "잠복 감염 가능 - 면역억제 시 주의"]],
        caption="3개 표지자 조합으로 환자 위치 결정"),

    "B형간염-결혼-임신": svg_checklist(
        "임신 단계별 관리 체크리스트",
        ["임신 전 - HBV DNA, ALT, 섬유화 평가",
         "임신 28-32주 - DNA > 200,000이면 TDF 시작 (수직감염 차단)",
         "출산 12시간 이내 - HBIG + 백신 1차 (영아)",
         "1·6개월 - 영아 백신 2·3차",
         "9-12개월 - 영아 anti-HBs 확인",
         "수유 - TDF/TAF·ETV 모두 안전"],
        caption="HBIG+백신 + 산모 항바이러스제 = 영아 감염 거의 0%"),

    "가족-B형간염-검사": svg_checklist(
        "받아야 할 검사 3가지 (배우자·자녀)",
        ["1. HBsAg - 현재 감염 여부",
         "2. anti-HBs - 면역 (백신 또는 회복) 여부",
         "3. anti-HBc - 과거 감염력",
         "→ 셋 다 음성 → 백신 0/1/6개월 시리즈",
         "→ HBsAg 양성 → 본인도 정기 추적·치료 평가",
         "→ 노출 직후 → 24시간 이내 HBIG (PEP)"],
        caption="검사·백신·노출 후 예방 3가지가 가족 보호의 핵심"),

    "B형간염-간암검진": svg_table(
        "6개월 간암 검진 구성과 보완 관계",
        ["검사", "역할", "한계"],
        [["복부 초음파", "1차 영상 검진", "비만·간경변에서 민감도 ↓"],
         ["AFP", "혈액 종양표지자", "30-40% 간암에서 정상"],
         ["PIVKA-II", "AFP와 보완", "와파린 복용 시 위양성"],
         ["+ 동적 CT/MRI", "초음파 한계 시", "방사선·조영제 부담"]],
        caption="3개 조합이 단일보다 검출률 높음 (한국 KLCA-NCC 표준)"),

    "C형간염-완치-DAA": svg_table(
        "DAA 치료 - 약제와 기간",
        ["약제", "성분", "기간 (일반)", "기간 (간경변)"],
        [["마비렛", "글레카프레비르 + 피브렌타스비르", "8주", "12주"],
         ["엡클루사", "소포스부비르 + 벨파타스비르", "12주", "12주"],
         ["보세비", "소포스부비르+벨파+복실라프레비르", "12주 (재치료)", "12주"]],
        caption="치료 12주 후 SVR12 검사로 완치 확인 - 95%+ 도달"),
}

n = 0
for slug, svg_html in SVGS.items():
    p = ROOT / slug / "index.html"
    if not p.exists():
        print(f"  SKIP missing: {slug}")
        continue
    text = p.read_text(encoding="utf-8")
    if 'svg class="fig"' in text or 'class="fig"' in text:
        print(f"  already has SVG: {slug}")
        continue

    # Insert after first </h2> tag (between first h2 section and the next)
    # Find first <h2>...</h2> closing
    m = re.search(r'</h2>', text)
    if not m:
        print(f"  no h2 found: {slug}")
        continue

    # Insert AFTER the first paragraph(s) following the h2 - find next </p> or next <h2>
    # Simpler: find first </h2>, then find next <h2> or end of body section, insert before
    # Most natural: insert after first </ul>, </ol>, or </p> following first h2
    h2_end = m.end()
    # Find next major boundary: <h2 again
    next_h2 = text.find('<h2>', h2_end)
    if next_h2 == -1: next_h2 = len(text)
    # Within first section, find a good insertion point - before next h2
    # Look for last </p> or </ul> before next h2
    sub = text[h2_end:next_h2]
    candidates = [m2.end() for m2 in re.finditer(r'</p>|</ul>|</ol>|</table>', sub)]
    if not candidates:
        insert_at = h2_end
    else:
        insert_at = h2_end + candidates[-1]

    new_text = text[:insert_at] + '\n\n' + svg_html + '\n' + text[insert_at:]
    p.write_text(new_text, encoding="utf-8")
    print(f"  added SVG: {slug}")
    n += 1

print(f"\nTotal: {n} legacy articles got an SVG figure.")
