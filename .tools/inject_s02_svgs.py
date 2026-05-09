"""Inject new visual SVGs into Series 02 article HTMLs (post-build)."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from build_articles import svg_flow_arrows, svg_progression_bar, svg_compare_two
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# slug -> SVG to inject after <div class="tldr">...</div>
SVGS = {
    "간경변-Child-Pugh-MELD": svg_progression_bar(
        [("Child-Pugh A", "5-6점"), ("Child-Pugh B", "7-9점"), ("Child-Pugh C", "10-15점")],
        title="Child-Pugh 등급",
        caption="등급은 5개 항목 점수 합산으로 결정"
    ),
    "간경변-식도정맥류": svg_flow_arrows(
        [("간경변", "원인", "normal"),
         ("문맥압 ↑", "혈류 저항", "warn"),
         ("우회로", "식도 정맥", "warn"),
         ("정맥류", "F1→F2→F3", "danger"),
         ("출혈", "응급", "danger")],
        title="식도정맥류 형성 흐름",
        caption="문맥압 항진이 출혈로 이어지는 경로 — 단계별 차단이 핵심"
    ),
    "간경변-복수": svg_progression_bar(
        [("Grade 1", "초음파만"), ("Grade 2", "배 부풂·체중↑"), ("Grade 3", "팽팽·호흡곤란")],
        title="복수 등급",
        caption="Grade 2부터 외래 적극 관리, Grade 3은 천자 검토"
    ),
    "간경변-간성혼수": svg_flow_arrows(
        [("Grade 0/1", "수면 변화", "accent"),
         ("Grade 2", "손떨림·혼동", "warn"),
         ("Grade 3", "의식 흐림", "danger"),
         ("Grade 4", "혼수", "danger")],
        title="West Haven 간성혼수 등급",
        caption="외래에서 1-2단계가 가장 흔하고 가족 관찰이 결정적"
    ),
    "간경변-간신증후군": svg_flow_arrows(
        [("Cr ↑", "AKI 신호", "warn"),
         ("이뇨제 중단", "+ 알부민", "accent"),
         ("호전 X", "원인 배제", "warn"),
         ("HRS-AKI", "테르리프레신", "danger"),
         ("간이식", "우선 배정", "accent")],
        title="HRS-AKI 진단·치료 흐름",
        caption="조기 진단 → 즉시 약물 → 이식 평가"
    ),
    "간경변-영양-근감소증": svg_compare_two(
        "권장 — 적극 섭취",
        ["열량 30-35 kcal/kg/일",
         "단백 1.2-1.5 g/kg/일",
         "식물성·유제품 단백",
         "취침 전 야식 200-250 kcal",
         "주 3-5회 운동"],
        "회피 — 옛 권고",
        ["단백 제한 (이미 폐기)",
         "장시간 단식 (6시간+)",
         "동물성 단백만",
         "취침 전 공복",
         "운동 회피"],
        caption="근감소증 예방이 간이식 후 결과를 좌우"
    ),
    "간경변-간이식-평가": svg_flow_arrows(
        [("MELD 15+", "or 비대상성", "warn"),
         ("다학제 평가", "1-2주", "accent"),
         ("KONOS or LDLT", "등록·평가", "accent"),
         ("이식", "수술", "accent"),
         ("평생 추적", "면역억제제", "normal")],
        title="간이식 평가에서 시행까지",
        caption="한국은 LDLT 비율 70%로 평균 대기 기간 짧음"
    ),
    "간경변-약물-주의": svg_compare_two(
        "위험 — 회피",
        ["NSAIDs (이부프로펜·디클로페낙)",
         "벤조다이아제핀",
         "마약성 진통제",
         "1세대 항히스타민",
         "한약·민간요법",
         "녹차 농축 보충제"],
        "안전 — 사용 가능",
        ["아세트아미노펜 (2g/일 이하)",
         "옥사제팜·로라제팜 단기",
         "2세대 항히스타민",
         "스타틴 (대상성, 신중)",
         "표준 처방약",
         "건강한 식이·운동"],
        caption="새 약·영양제는 진료의에게 먼저 알리세요"
    ),
    "간경변-정상수치-함정": svg_flow_arrows(
        [("간 손상", "효소 새어나옴", "warn"),
         ("간세포 ↓", "효소 ↑", "warn"),
         ("진행 간경변", "효소 ↓", "danger"),
         ("\"수치 정상\"", "오해", "danger"),
         ("영상 평가", "진단", "accent")],
        title="\"수치 정상 간경변\"의 함정",
        caption="진행될수록 새어나올 효소가 줄어 정상으로 보일 수 있음"
    ),
    "간경변-대상성-비대상성": svg_flow_arrows(
        [("대상성", "5년 80-90%", "accent"),
         ("첫 합병증", "4가지", "warn"),
         ("비대상성", "5년 20-50%", "danger"),
         ("원인 치료", "1년+ 합병증 X", "accent"),
         ("재대상화", "Baveno VII", "accent")],
        title="간경변 단계 — 양방향 흐름",
        caption="원인 치료로 비대상성 → 대상성 후퇴(recompensation)도 가능"
    ),
}

# Anchor: insert after </div> of <div class="tldr">...</div>
n = 0
for slug, svg in SVGS.items():
    p = ROOT / slug / "index.html"
    if not p.exists():
        print(f"  SKIP missing: {slug}")
        continue
    text = p.read_text(encoding="utf-8")
    # Skip if already injected (look for unique caption text)
    cap_marker = svg[svg.find('fig-caption">')+13:svg.find('</p>', svg.find('fig-caption">'))] if 'fig-caption' in svg else ''
    if cap_marker and cap_marker in text:
        print(f"  already has: {slug}")
        continue
    # Find tldr block end and inject after it
    m = re.search(r'(<div class="tldr">.*?</div>)', text, re.S)
    if not m:
        print(f"  no tldr anchor: {slug}")
        continue
    new_text = text[:m.end()] + '\n\n' + svg + text[m.end():]
    p.write_text(new_text, encoding="utf-8")
    print(f"  injected: {slug}")
    n += 1

print(f"\nTotal: {n} articles got new visual SVG.")
