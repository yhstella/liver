"""Series 02 친근한 톤 TLDR + 새 시각 SVG 추가."""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from build_articles import svg_flow_arrows, svg_progression_bar, svg_compare_two
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REWRITES = {
    "간경변-Child-Pugh-MELD": {
        "tldr": "외래에서 \\\"Child-Pugh가 어떻게 되나요\\\" 또는 \\\"MELD 점수가 뭐예요\\\"라는 질문 자주 받아요. 두 점수 모두 간경변 환자분 상태를 평가하는 도구인데 보는 축이 달라요. <em>Child-Pugh</em>는 간경변이 얼마나 진행됐고 합병증(복수·정맥류·황달·간성혼수)이 얼마나 있는지를 종합해서 봐요. <em>MELD</em>는 다음 3개월 안의 사망 위험과 간이식 우선순위를 정하기 위한 점수입니다. 두 점수를 함께 보면서 환자분 상황을 종합 평가하는 게 표준이에요. Child-Pugh A·B·C는 5년 생존율이 약 90%·70%·30% 정도 되고, MELD가 15 이상이 되면 간이식 평가를 본격적으로 시작합니다.",
        "extra_svg": svg_progression_bar(
            [("Child-Pugh A", "5-6점"), ("Child-Pugh B", "7-9점"), ("Child-Pugh C", "10-15점")],
            caption="등급은 5개 항목 점수 합산으로 결정",
            title="Child-Pugh 등급"
        ),
    },
    "간경변-식도정맥류": {
        "tldr": "식도정맥류는 간경변에서 문맥압이 올라가면서 식도 점막 아래 정맥이 부풀어 오른 상태예요. \\\"왜 식도에 정맥류가 생기죠?\\\"라는 질문 많이 받는데요, 간이 굳어지면 그 안의 혈류 저항이 커지면서 혈액이 우회로(식도·위 정맥)로 빠져나가요. 이 우회로의 정맥이 압력을 받아 부풀고 얇아지면 사소한 자극에도 터질 수 있습니다. 한 번 출혈하면 6주 사망률이 15-20%로 가장 위험한 합병증 중 하나예요. 그래서 <em>중·대형 정맥류는 출혈 전에 비선택적 베타차단제 또는 내시경 결찰술로 1차 예방</em>합니다. 출혈 이후엔 두 가지를 병행하는 2차 예방이 필수입니다.",
        "extra_svg": svg_flow_arrows(
            [("간경변", "원인 질환", "normal"),
             ("문맥압 ↑", "혈류 저항", "warn"),
             ("우회로", "식도 정맥", "warn"),
             ("정맥류", "F1→F2→F3", "danger"),
             ("출혈", "응급", "danger")],
            title="식도정맥류 형성 흐름",
            caption="문맥압 항진이 출혈로 이어지는 경로 — 단계별 차단이 핵심"
        ),
    },
    "간경변-복수": {
        "tldr": "복수는 비대상성 간경변의 가장 흔한 첫 신호예요. \\\"갑자기 배가 부풀어요\\\"라는 말씀으로 외래에 오시는 경우가 많죠. Grade 1·2·3로 분류하고 식이 나트륨 제한 + 이뇨제(스피로놀락톤·푸로세미드)로 치료를 시작합니다. 천자(paracentesis)는 진단과 치료에 모두 사용되고, 5L 이상 빼면 알부민도 함께 보충해요. 난치성 복수가 되면 반복 천자·TIPS·간이식까지 단계적으로 갑니다. <em>SBP(자발성 세균성 복막염)</em>은 한 번이라도 겪으면 평생 항생제 예방이 필요해요. 복수 환자분께서 가장 신경 쓰셔야 할 건 <em>나트륨 5g/일 이하 제한</em>입니다.",
        "extra_svg": svg_progression_bar(
            [("Grade 1", "초음파만"), ("Grade 2", "배 부풂·체중↑"), ("Grade 3", "팽팽·호흡곤란")],
            title="복수 등급",
            caption="Grade 2부터 외래 적극 관리, Grade 3은 천자 검토"
        ),
    },
    "간경변-간성혼수": {
        "tldr": "간성혼수는 간경변에서 암모니아 같은 신경독성 물질이 뇌에 영향을 줘 일어나는 인지·의식 변화예요. 흥미롭게도 본인보다 <em>가족이 먼저 알아채는</em> 경우가 많아요 — 수면-각성 패턴이 뒤바뀌거나, 손이 떨리고, 계산이 안 되거나, 평소와 다른 행동을 보이는 식으로요. 1차 약물은 락툴로스이고, 재발하면 리팍시민을 추가합니다. 한 번 발생하면 평생 예방이 표준이고, 유발 요인(감염·출혈·변비·약물)을 점검하는 게 핵심이에요. 과거의 \\\"단백 제한\\\" 권고는 폐기됐고 오히려 적정 단백 섭취가 권장됩니다.",
        "extra_svg": svg_flow_arrows(
            [("Grade 0/1", "수면 변화", "accent"),
             ("Grade 2", "손떨림·혼동", "warn"),
             ("Grade 3", "의식 흐림", "danger"),
             ("Grade 4", "혼수", "danger")],
            title="West Haven 간성혼수 등급",
            caption="외래에서 1-2단계가 가장 흔하고 가족 관찰이 결정적"
        ),
    },
    "간경변-간신증후군": {
        "tldr": "간신증후군(HRS)은 진행된 간경변에서 신장 자체엔 병이 없는데 신기능이 빠르게 떨어지는 합병증이에요. 콩팥은 멀쩡한데 강한 혈관 확장으로 신혈류가 줄어들면서 기능이 망가져요. 한 달 내 사망률이 50%를 넘는 응급 상황입니다. 표준 흐름은 <em>알부민 부하 → 진단 확인 → 즉시 혈관수축제(테르리프레신 우선)</em>예요. 결국 <em>간이식</em>이 가장 강력한 근본 치료고, MELD 점수가 자동으로 올라가 우선 배정 대상이 됩니다. 2015년 이후 \\\"HRS-AKI / HRS-NAKI\\\" 새 분류를 사용해요.",
        "extra_svg": svg_flow_arrows(
            [("Cr ↑", "AKI 신호", "warn"),
             ("이뇨제 중단", "+ 알부민", "accent"),
             ("호전 X", "원인 배제", "warn"),
             ("HRS-AKI", "테르리프레신", "danger"),
             ("간이식", "우선 배정", "accent")],
            title="HRS-AKI 진단·치료 흐름",
            caption="조기 진단 → 즉시 약물 → 이식 평가"
        ),
    },
    "간경변-영양-근감소증": {
        "tldr": "간경변 환자에서 \\\"단백질 제한\\\"은 옛 권고로 이미 폐기됐어요. 오히려 <em>체중당 단백 1.2-1.5g, 열량 30-35 kcal/일</em>이 표준이고, 근감소증(sarcopenia)이 있으면 더 적극적으로 보충합니다. 흥미로운 권고가 하나 있는데 — <em>야식(취침 전 200-250 kcal 간식)</em>이에요. 간경변 환자는 6-8시간 단식만으로도 근육 분해가 시작되거든요. 야식으로 야간 단식 시간을 줄이면 근육량이 보존됩니다. 식물성·유제품 단백이 동물성보다 유리하고, BCAA(가지사슬 아미노산) 보충도 도움이 될 수 있어요.",
        "extra_svg": svg_compare_two(
            "권장 — 적극 섭취",
            ["열량 30-35 kcal/kg/일",
             "단백 1.2-1.5 g/kg/일",
             "식물성·유제품 단백",
             "취침 전 야식 200-250 kcal",
             "주 3-5회 운동 (유산소 + 근력)"],
            "회피 — 옛 권고",
            ["단백 제한 (이미 폐기)",
             "장시간 단식 (6시간+)",
             "동물성 단백만",
             "취침 전 공복 유지",
             "운동 회피"],
            caption="근감소증 예방이 간이식 후 결과를 좌우"
        ),
    },
    "간경변-간이식-평가": {
        "tldr": "간이식은 비대상성 간경변의 근본 치료예요. 일반적으로 <em>MELD 15 이상</em>이 평가 시작 임계값이고, 한국은 KONOS 등록 후 MELD 기반 우선순위를 받습니다. 뇌사자 이식 외에도 한국은 <em>살아있는 기증자(LDLT)</em> 이식이 활발해요 — 전체 간이식의 약 70%로 세계 최고 수준이라 평균 대기 기간이 짧은 편입니다. 평가는 다학제로 진행돼서 의학·외과·심리·사회 모든 측면을 함께 봐요. 보통 1-2주 안에 완료되고, 결정에 따라 등록·기증자 평가가 시작됩니다. 이식 후 5년 생존율은 70-80%로 비대상성 간경변의 자연 경과보다 의미 있게 좋아요.",
        "extra_svg": svg_flow_arrows(
            [("MELD 15+", "or 비대상성", "warn"),
             ("다학제 평가", "1-2주", "accent"),
             ("KONOS or LDLT", "등록·평가", "accent"),
             ("이식", "수술", "accent"),
             ("평생 추적", "면역억제제", "normal")],
            title="간이식 평가에서 시행까지",
            caption="한국은 LDLT 비율 70%로 평균 대기 기간 짧음"
        ),
    },
    "간경변-약물-주의": {
        "tldr": "간경변 환자분은 약물 대사·배설이 떨어지고 신기능도 약해요. 그래서 일반인에게 안전한 약이 위험할 수 있어요. 절대 피해야 할 대표 약물 — <em>NSAIDs(이부프로펜·디클로페낙)</em>는 신독성과 출혈로 가장 위험하고, <em>벤조다이아제핀·마약성 진통제</em>는 간성혼수를 유발합니다. 한국에서는 약물성 간 손상의 30-40%가 한약·건강기능식품과 관련 있어요. \\\"이건 자연이라 안전하다\\\"는 인식이 가장 위험합니다. 외래에서 복용 중인 모든 제품을 사진으로 정리해 보여주시는 게 평가의 첫 단계예요. 진통제가 필요하면 아세트아미노펜(2g/일 이하)이 가장 안전합니다.",
        "extra_svg": svg_compare_two(
            "위험 — 회피",
            ["NSAIDs (이부프로펜·디클로페낙)",
             "벤조다이아제핀 (수면제·진정제)",
             "마약성 진통제 (코데인·트라마돌)",
             "1세대 항히스타민",
             "한약·민간요법 (검증되지 않은)",
             "녹차 농축 보충제"],
            "안전 — 사용 가능",
            ["아세트아미노펜 (2g/일 이하)",
             "옥사제팜·로라제팜 단기",
             "2세대 항히스타민",
             "스타틴 (대상성, 신중)",
             "표준 처방약 (진료의 결정)",
             "건강한 식이·운동"],
            caption="새 약·영양제는 진료의에게 먼저 알리세요"
        ),
    },
    "간경변-정상수치-함정": {
        "tldr": "간기능검사(AST·ALT·빌리루빈·알부민)가 \\\"정상\\\"으로 나와도 진행된 간경변일 수 있다는 건 환자분들이 잘 모르시는 부분이에요. 진행된 간경변에서는 살아있는 간세포가 줄어들어 \\\"새어 나올 효소 자체\\\"가 적어지면서 수치가 정상으로 측정돼요. 그래서 간세포 손상이 진행 중인데 효소 수치는 오히려 낮은 \\\"burnt-out\\\" 패턴이 나타납니다. 이게 알코올성과 진행된 MASH 간경변에서 특히 흔해요. 그래서 <em>혈소판 감소·INR 상승·영상에서의 간 모양 변화·섬유화 검사</em>를 함께 봐야 합니다. \\\"수치 정상으로 안심하다 진행 간경변 발견\\\"이 가장 흔한 임상 함정이에요.",
        "extra_svg": svg_flow_arrows(
            [("간 손상", "효소 새어나옴", "warn"),
             ("간세포 ↓", "효소 ↑", "warn"),
             ("진행 간경변", "효소 ↓", "danger"),
             ("\\\"수치 정상\\\"", "오해", "danger"),
             ("영상 평가", "진단", "accent")],
            title="\\\"수치 정상 간경변\\\"의 함정",
            caption="진행될수록 새어나올 효소가 줄어 정상으로 보일 수 있음"
        ),
    },
    "간경변-대상성-비대상성": {  # hand-written - HTML edit
        "tldr": "간경변은 한 덩어리 진단이 아니에요. 두 단계로 나누는데, 합병증이 한 번도 없으면 <em>대상성</em>(compensated), 4가지 합병증(복수·정맥류 출혈·간성혼수·황달) 중 하나라도 등장하면 <em>비대상성</em>(decompensated)입니다. 두 단계의 5년 생존율 차이는 약 80% 대 20-50%로 매우 커요. 그런데 좋은 소식이 있어요 — 원인 치료(B형간염 항바이러스제, 알코올 금주, MASH 체중감량)가 잘 되면 비대상성에서 다시 대상성으로 돌아오는 경우(recompensation)도 있습니다. 외래에서 \\\"한번 비대상성이면 끝인가요?\\\"라는 질문 많이 받는데, 끝이 아니에요.",
        "extra_svg": svg_flow_arrows(
            [("대상성", "5년 80-90%", "accent"),
             ("첫 합병증", "4가지", "warn"),
             ("비대상성", "5년 20-50%", "danger"),
             ("원인 치료", "1년+ 합병증 X", "accent"),
             ("재대상화", "Baveno VII", "accent")],
            title="간경변 단계 — 양방향 흐름",
            caption="원인 치료로 비대상성 → 대상성 후퇴(recompensation)도 가능"
        ),
    },
}

ba = ROOT / ".tools" / "build_articles.py"
ba_text = ba.read_text(encoding="utf-8")

for slug, data in REWRITES.items():
    if slug == "간경변-대상성-비대상성":
        continue
    new_tldr = data["tldr"]
    # Match TLDR field — capture (prefix)(content)(suffix=closing quote)
    pattern = r'("slug":\s*"' + re.escape(slug) + r'",.*?"tldr":\s*")([^"]+(?:\\"[^"]*)*)(")'
    m = re.search(pattern, ba_text, re.S)
    if m:
        ba_text = ba_text[:m.start(2)] + new_tldr + ba_text[m.end(2):]
        print(f"  TLDR: {slug}")
    else:
        print(f"  TLDR not found: {slug}")

    # Append extra SVG to svgs list
    extra_svg = data["extra_svg"]
    pattern2 = r'("slug":\s*"' + re.escape(slug) + r'",.*?"svgs":\s*\[)(.*?)(\n\s*\],\s*\n\s*"related")'
    m2 = re.search(pattern2, ba_text, re.S)
    if m2:
        existing = m2.group(2).rstrip()
        # SVG escaped as Python triple-string literal
        # Need to escape any """ inside the SVG (unlikely but safe)
        svg_lit = extra_svg.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')
        new_block = existing + '\n        """' + svg_lit + '""",'
        ba_text = ba_text[:m2.start(2)] + new_block + ba_text[m2.end(2):]
        print(f"  SVG appended: {slug}")
    else:
        print(f"  svgs list not found: {slug}")

ba.write_text(ba_text, encoding="utf-8")

# Hand-written: 간경변-대상성-비대상성/index.html
hand = ROOT / "간경변-대상성-비대상성" / "index.html"
if hand.exists():
    text = hand.read_text(encoding="utf-8")
    data = REWRITES["간경변-대상성-비대상성"]
    new_tldr_html = '<div class="tldr"><strong>핵심 요약</strong>' + data["tldr"].replace('\\\\\"', '"').replace('\\"', '"') + '</div>'
    text = re.sub(r'<div class="tldr"><strong>핵심 요약</strong>.*?</div>', lambda m: new_tldr_html, text, count=1, flags=re.S)
    if 'class="fig"' in text:
        m = re.search(r'(<svg class="fig"[^>]*>.*?</svg>(?:\s*<p class="fig-caption">[^<]*</p>)?)', text, re.S)
        if m and data["extra_svg"] not in text:
            text = text[:m.end()] + '\n\n' + data["extra_svg"] + text[m.end():]
            print(f"  hand-written: {hand.name}")
    hand.write_text(text, encoding="utf-8")

print("Done.")
