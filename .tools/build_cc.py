"""Build /CC/ (Chief Complaints) hub + 14 patient-facing complaint pages.

Patient-facing intake guides: 외래에서 자주 듣는 주호소 14개.
각 페이지는 환자 시점에서 '왜 그런가, 어떻게 진료받게 되는가, 무엇을 준비할까'를
설명하고, 관련 세부주제 / 사례 페이지로 링크합니다.
"""
import os, sys, html as htmllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
def esc(s): return htmllib.escape(s or "")

NAV = '''<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></nav></div></header>'''
FOOTER = '''<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>'''


CC_LIST = [
    {
        "slug": "검진-혹-발견",
        "title": "건강검진 초음파에서 혹이 보였어요",
        "summary": "위험 인자(B형간염·간경변·음주)와 결절의 영상 패턴 두 가지 축으로 평가합니다.",
        "what_we_check": [
            "<strong>위험 인자 평가</strong> — B형/C형 간염 검사, 음주력, 가족력",
            "<strong>혈액검사</strong> — 간 효소(ALT/AST), 간 합성능(알부민·PT), 종양표지자(AFP·PIVKA-II)",
            "<strong>정밀 영상</strong> — 동적 CT 또는 EOB-MRI (혹의 패턴 분석)",
            "위험 인자가 있으면 간세포암 우선 의심, 없으면 양성종양(혈관종·낭종·FNH·선종) 평가",
        ],
        "what_to_bring": [
            "건강검진 결과지 원본",
            "초음파 사진(가능하면 영상 CD)",
            "복용 약물·영양제 목록",
            "과거 B형/C형 간염 검사 결과(있다면)",
        ],
        "related": [
            ("/간암-진단-첫외래/", "간암 진단 첫 외래"),
            ("/간양성종양-진단/", "간 양성종양 진단"),
            ("/케이스/건강검진-우연발견-1cm결절/", "사례: 검진에서 우연 발견된 1cm 결절"),
            ("/알파태아단백/", "AFP — 종양표지자"),
        ],
    },
    {
        "slug": "지방간-진단",
        "title": "지방간이 있다고 들었어요",
        "summary": "지방간은 한 덩어리가 아닙니다. 단순 지방간과 지방간염(MASH)의 분기를 비침습 검사로 평가합니다.",
        "what_we_check": [
            "<strong>위험 인자 평가</strong> — 비만·당뇨·고지혈증·고혈압·음주",
            "<strong>혈액검사</strong> — ALT, AST, 공복혈당·HbA1c, 지질, FIB-4 자동 계산",
            "<strong>Fibroscan(간섬유화 스캔)</strong> — 진행 섬유화 여부 평가",
            "다른 원인 배제 — 바이러스(HBV/HCV), 자가면역, 약물·보충제",
        ],
        "what_to_bring": [
            "건강검진 결과지",
            "복용 약물·영양제·한약 목록 (사진 권장)",
            "과거 간 효소 추적 기록(있다면)",
            "체중·식이·운동 패턴 (대략적으로)",
        ],
        "related": [
            ("/대사이상지방간-MASLD/", "MASLD"),
            ("/지방간염-MASH/", "지방간염(MASH)"),
            ("/지방간-정밀검사/", "지방간 정밀검사"),
            ("/지방간-치료/", "지방간 치료"),
            ("/케이스/검진ALT상승-MASLD진단/", "사례: ALT 상승으로 시작한 MASLD 평가"),
        ],
    },
    {
        "slug": "간-통증",
        "title": "간 쪽이 아파요",
        "summary": "우상복부 통증의 원인은 간 외에도 담낭·담관·장·근골격 등 다양합니다. 위치·양상·동반 증상으로 감별합니다.",
        "what_we_check": [
            "<strong>통증 양상</strong> — 위치, 시작 시점, 식사·자세와의 관계, 강도",
            "<strong>동반 증상</strong> — 발열, 황달, 소화불량, 체중 변화",
            "<strong>혈액검사</strong> — 간 효소(ALT/AST), 빌리루빈, ALP/GGT(담도), CRP·CBC(염증)",
            "<strong>복부 초음파</strong> — 담낭·담관·간 평가가 1차 영상",
            "필요 시 동적 CT/MRI로 정밀 평가",
        ],
        "what_to_bring": [
            "통증 일기 (시작·악화·호전 시점)",
            "최근 식사·약물 변화 기록",
            "건강검진 결과지",
        ],
        "related": [
            ("/간경변-복수/", "복수와 우상복부 불편감"),
            ("/간양성종양-낭종-관리/", "큰 낭종에 의한 압박"),
            ("/약물성-간손상-DILI/", "약물성 간손상"),
        ],
    },
    {
        "slug": "간수치-상승",
        "title": "간수치가 올랐어요",
        "summary": "ALT/AST 상승의 흔한 원인은 지방간·약물·바이러스·알코올·자가면역입니다. 첫 외래에 한 번에 다중 원인을 감별합니다.",
        "what_we_check": [
            "<strong>혈액검사 패널</strong> — 바이러스(HBsAg, anti-HCV), 자가면역(ANA, ASMA, IgG), 대사(혈당·지질), 갑상선, 철·구리, 알코올 바이오마커",
            "<strong>약물·영양제·한약 자세 문진</strong>",
            "<strong>복부 초음파 + Fibroscan</strong>",
            "흔한 원인 순서: 지방간 → 알코올 → 약물 → 바이러스 → 자가면역",
        ],
        "what_to_bring": [
            "최근 간 수치 결과지(가능하면 추세)",
            "복용 모든 약·영양제·한약 사진",
            "음주 패턴 (주당 횟수·양)",
            "최근 체중·운동·식이 변화",
        ],
        "related": [
            ("/간수치-높음/", "간수치 높음"),
            ("/간수치-종류-차이/", "간수치 종류·차이"),
            ("/약물성-간손상-DILI/", "약물성 간손상"),
            ("/케이스/검진ALT상승-원인감별/", "사례: ALT 95/AST 80 원인 감별"),
            ("/케이스/보충제-ALT상승/", "사례: 보충제 후 ALT 상승"),
        ],
    },
    {
        "slug": "황달",
        "title": "황달이 생겼어요",
        "summary": "황달은 <strong>간세포 손상 · 담관 폐쇄 · 적혈구 파괴</strong> 세 가지 큰 원인이 있습니다. 빌리루빈 직접·간접 비율과 영상으로 빠르게 감별합니다.",
        "what_we_check": [
            "<strong>빌리루빈 직접·간접 분획</strong> — 직접 우세는 담관·간세포 문제, 간접 우세는 적혈구·유전",
            "<strong>혈액검사</strong> — ALT/AST, ALP/GGT, 알부민·PT(간 합성능), CBC(빈혈·용혈)",
            "<strong>복부 초음파</strong> — 담관 확장 여부 즉시 확인",
            "필요 시 MRCP, ERCP 또는 동적 영상",
        ],
        "what_to_bring": [
            "증상 시작 시점, 진행 속도",
            "동반 증상 — 발열, 통증, 소변·대변 색 변화, 가려움",
            "복용 약물·영양제·한약",
            "최근 음주·여행·노출력",
        ],
        "related": [
            ("/빌리루빈-직접-간접/", "빌리루빈 직접·간접"),
            ("/ALP-GGT-담도-간세포/", "ALP/GGT — 담도 표지"),
            ("/약물성-간손상-DILI/", "약물성 간손상"),
            ("/케이스/독성간염-야생버섯/", "사례: 야생 버섯 급성 간부전"),
        ],
    },
    {
        "slug": "B형간염-진단",
        "title": "B형간염이 발견되었어요",
        "summary": "HBsAg 양성 첫 발견 시 활동성 평가, 가족 검사, 간암 검진 시작 시점을 정합니다. 모든 환자가 즉시 치료가 필요한 것은 아닙니다.",
        "what_we_check": [
            "<strong>HBV 활동성 평가</strong> — HBeAg, HBV DNA, ALT 추세",
            "<strong>간 손상 정도</strong> — 혈소판, 알부민, Fibroscan, 초음파",
            "<strong>치료 적응증</strong> — 활동성 간염 + DNA ≥ 2,000 또는 진행 섬유화·간경변",
            "<strong>가족 검사 권유</strong> — 부모·형제·배우자에게 HBsAg/anti-HBs 검사",
            "<strong>간암 검진 시작</strong> — 40세 이상 남성/50세 이상 여성, 또는 진행 섬유화 시 6개월마다",
        ],
        "what_to_bring": [
            "HBV 검사 결과지 (HBsAg, HBeAg, HBV DNA, anti-HBs)",
            "과거 간 효소 추적 기록",
            "가족력 — 부모·형제 중 B형간염·간암 환자 여부",
        ],
        "related": [
            ("/B형간염-검사결과/", "B형간염 검사 결과지 해석"),
            ("/B형간염-평생약/", "B형간염 약을 평생 먹어야 하나"),
            ("/가족-B형간염-검사/", "가족 B형간염 검사"),
            ("/B형간염-간암검진/", "B형간염 환자 간암 검진"),
            ("/케이스/직장검진-HBsAg양성/", "사례: 직장 검진 HBsAg 첫 발견"),
        ],
    },
    {
        "slug": "C형간염-진단",
        "title": "C형간염이 발견되었어요",
        "summary": "anti-HCV 양성은 \"노출\" 표지일 뿐이며 활동성 감염은 HCV RNA(PCR)로 확인합니다. RNA 양성이면 8-12주 직접 작용 항바이러스제(DAA)로 95% 이상 완치 가능합니다.",
        "what_we_check": [
            "<strong>HCV RNA(PCR)</strong> — 활동성 감염 여부 확인 (자연 회복 시 음성)",
            "<strong>Genotype, Fibroscan</strong> — 약물 선택과 추적 강도 결정",
            "<strong>간경변 동반 평가</strong> — Fibroscan ≥ 12.5 kPa 또는 임상 소견 시 평생 간암 검진",
            "<strong>HBV 동반 평가</strong> — DAA 중 HBV 재활성화 위험으로 사전 확인",
        ],
        "what_to_bring": [
            "anti-HCV 결과지",
            "과거 수혈·시술·문신·정맥주사력",
            "동반 질환 (당뇨·HIV·신장 질환 등)",
        ],
        "related": [
            ("/C형간염-진단/", "C형간염 진단"),
            ("/C형간염-완치-DAA/", "DAA 8주 완치"),
            ("/C형간염-완치후-추적/", "SVR 후 평생 추적"),
            ("/케이스/anti-HCV양성-첫발견/", "사례: anti-HCV 첫 발견부터 SVR까지"),
        ],
    },
    {
        "slug": "자가면역간염-의심",
        "title": "자가면역간염이 의심된다고 들었어요",
        "summary": "자가면역간염(AIH)은 면역계가 간을 공격하는 만성 진행성 질환입니다. ALT 상승 + IgG 상승 + 자가항체(ANA, ASMA) + 조직 4가지 축으로 진단합니다.",
        "what_we_check": [
            "<strong>자가항체</strong> — ANA, ASMA, anti-LKM 역가",
            "<strong>면역글로불린</strong> — IgG 정량 (상승 시 진단 점수 가산)",
            "<strong>다른 원인 배제</strong> — HBV/HCV/HEV, 윌슨병, 약물성, 지방간",
            "<strong>간생검</strong> — interface hepatitis, plasma cell 침윤 등 조직 진단",
            "<strong>Simplified AIH score</strong>로 점수화 (6점 probable, 7점 이상 definite)",
        ],
        "what_to_bring": [
            "이미 받은 자가면역 패널 결과지",
            "다른 자가면역질환력 (갑상선·셀리악·류마티스 등)",
            "약물·영양제 목록",
            "가족력 — 자가면역질환",
        ],
        "related": [
            ("/자가면역간염-진단/", "자가면역간염 진단"),
            ("/자가면역간염-치료/", "자가면역간염 표준 치료"),
            ("/자가면역간염-약중단/", "자가면역간염 약 중단 결정"),
            ("/케이스/자가면역간염-첫진단/", "사례: 32세 여성 AIH 첫 진단"),
        ],
    },
    {
        "slug": "간섬유화-진단",
        "title": "간섬유화가 생겼대요",
        "summary": "섬유화는 간경변으로 가는 단계입니다. F0-F1은 안전, F2-F3은 진행 섬유화, F4는 간경변. 비침습 검사로 단계화하고 원인 치료가 핵심입니다.",
        "what_we_check": [
            "<strong>Fibroscan</strong>(간섬유화 스캔) — kPa 수치로 단계 평가",
            "<strong>FIB-4</strong> — 나이·AST·ALT·혈소판으로 자동 계산",
            "<strong>원인 평가</strong> — 바이러스, 지방간, 알코올, 자가면역, 담관",
            "<strong>간경변 동반 시</strong> — 6개월 간암 검진 + 정맥류 내시경",
            "필요 시 MRE 또는 간생검",
        ],
        "what_to_bring": [
            "Fibroscan 결과지 (kPa, CAP, IQR 등)",
            "이미 받은 혈액검사 결과",
            "음주·체중·약물 정보",
        ],
        "related": [
            ("/간섬유화스캔-수치/", "Fibroscan 수치 읽는 법"),
            ("/지방간-정밀검사/", "지방간 정밀검사"),
            ("/간경변-정상수치-함정/", "간기능검사 정상인데 간경변?"),
            ("/간생검-언제-필요한가/", "간생검 — 언제 필요한가"),
        ],
    },
    {
        "slug": "복부-팽만-복수",
        "title": "배가 점점 부풀어요 / 복수가 생겼어요",
        "summary": "복부 팽만은 복수, 큰 낭종, 종양, 단순 가스 등 원인이 다양합니다. 간 질환 환자에서 새로 생긴 복수는 비대상성 신호로 즉시 평가합니다.",
        "what_we_check": [
            "<strong>복부 초음파</strong> — 복수 여부·양 즉시 확인",
            "<strong>복수가 있으면 진단적 천자</strong> — 다형핵백혈구(자발성 세균성 복막염 평가), 알부민·총단백",
            "<strong>혈액검사</strong> — 간 합성능, Child-Pugh·MELD 점수",
            "이뇨제 시작·식염 제한, 자발성 세균성 복막염 동반 시 즉시 항생제",
        ],
        "what_to_bring": [
            "체중 추세 (최근 몇 주간 변화)",
            "동반 증상 — 발열, 통증, 호흡곤란",
            "기존 간 질환 추적 기록",
            "복용 약물 (이뇨제·NSAID 등)",
        ],
        "related": [
            ("/간경변-복수/", "복수 단계별 관리"),
            ("/간경변-Child-Pugh-MELD/", "Child-Pugh와 MELD"),
            ("/간경변-대상성-비대상성/", "대상성 vs 비대상성"),
            ("/케이스/복수-SBP-진단치료/", "사례: 복수 + 자발성 세균성 복막염"),
        ],
    },
    {
        "slug": "AFP-상승",
        "title": "AFP 수치가 올랐어요",
        "summary": "알파태아단백(AFP) 상승은 간세포암 표지일 수 있지만 활동성 간염·간 재생·임신·일부 종양에서도 오를 수 있습니다. <strong>추세</strong>가 절대값보다 더 의미 있습니다.",
        "what_we_check": [
            "<strong>AFP 추세 평가</strong> — 이전 값 대비 변화",
            "<strong>위험 인자 평가</strong> — B형간염·간경변 동반 여부",
            "<strong>정밀 영상</strong> — 동적 CT 또는 EOB-MRI (작은 결절을 놓치지 않기 위해)",
            "<strong>PIVKA-II</strong> 보완 측정",
        ],
        "what_to_bring": [
            "AFP 추세 — 이전 값들과 측정 일자",
            "현재까지 받은 영상 결과 (CD 가능하면)",
            "B형간염·간경변 추적 기록",
        ],
        "related": [
            ("/알파태아단백/", "AFP — 정상범위와 의심 기준"),
            ("/PIVKA-II-간암마커/", "PIVKA-II"),
            ("/B형간염-간암검진/", "간암 검진 흐름"),
            ("/케이스/AFP상승-영상음성/", "사례: AFP만 오르고 영상은 정상"),
            ("/케이스/PIVKAII-와파린-위양성/", "사례: PIVKA-II 와파린 위양성"),
        ],
    },
    {
        "slug": "약물-간손상",
        "title": "약 먹고 간수치가 올랐어요",
        "summary": "약물성 간손상(DILI)은 처방 약·영양제·한약·헬스 보충제 모두 원인이 될 수 있습니다. 의심 약물 중단이 가장 중요한 첫 단계입니다.",
        "what_we_check": [
            "<strong>약물·영양제·한약 자세 문진</strong> — 시작 시점·복용 기간",
            "<strong>다른 원인 배제</strong> — 바이러스, 자가면역, 지방간",
            "<strong>RUCAM/CIOMS 평가</strong> — 시간 관계 + 약물 중단 후 호전 + 다른 원인 배제",
            "<strong>의심 약물 중단</strong> 후 ALT 추적 (1·2·4·8주)",
            "ALT > 5×ULN 또는 증상 시 즉시 중단, 필요 시 입원",
        ],
        "what_to_bring": [
            "<strong>모든 복용 약·영양제·한약 사진</strong> (라벨 포함)",
            "복용 시작 시점·기간",
            "ALT 추적 결과 (가능하면 추세)",
            "동반 증상 — 발열·발진·황달·가려움",
        ],
        "related": [
            ("/약물성-간손상-DILI/", "약물성 간손상"),
            ("/케이스/약물성간손상-항결핵제/", "사례: 항결핵제 후 DILI"),
            ("/케이스/보충제-ALT상승/", "사례: 보충제 후 ALT 상승"),
            ("/케이스/독성간염-야생버섯/", "사례: 야생 버섯 급성 간부전"),
        ],
    },
    {
        "slug": "가족-B형간염",
        "title": "가족 중에 B형간염이 있어요",
        "summary": "B형간염 환자의 가족(특히 배우자·자녀)은 검사와 백신 평가가 필요합니다. 한국은 1995년 이후 출생자 대부분 백신 면역이 있지만 확인이 권장됩니다.",
        "what_we_check": [
            "<strong>3가지 검사</strong> — HBsAg, anti-HBs, anti-HBc",
            "결과 조합 해석 — 감염 / 자연 회복 / 백신 면역 / 미접촉",
            "anti-HBs 음성 + HBsAg 음성 → <strong>백신 시리즈 권장</strong>",
            "HBsAg 양성 → 평가·치료 적응 검토",
            "백신 후 anti-HBs 확인 (고위험군)",
        ],
        "what_to_bring": [
            "가족 환자의 HBV 상태 (HBsAg/HBeAg)",
            "본인의 과거 백신 접종력 (어렸을 때 포함)",
            "과거 anti-HBs 검사 결과 (있다면)",
        ],
        "related": [
            ("/가족-B형간염-검사/", "가족 B형간염 검사"),
            ("/B형간염-백신/", "B형간염 백신"),
            ("/B형간염-결혼-임신/", "B형간염과 결혼·임신"),
        ],
    },
    {
        "slug": "음주-간걱정",
        "title": "술 때문에 간이 걱정돼요",
        "summary": "알코올성 간 질환은 단순 지방간부터 알코올성 간염, 간경변까지 단계가 있습니다. 음주량과 기간이 위험 인자이며, 금주가 가장 강력한 치료입니다.",
        "what_we_check": [
            "<strong>음주 패턴 평가</strong> — 주당 양·횟수·기간, AUDIT 설문",
            "<strong>혈액검사</strong> — AST/ALT 비율(>2 시 알코올 시사), GGT, MCV",
            "<strong>알코올 바이오마커</strong> — PEth(필요 시) — 객관적 음주량 평가",
            "<strong>Fibroscan + 초음파</strong> — 지방간·섬유화·간경변 평가",
            "동반 질환 평가 — MASLD, 영양 결핍, 정신 건강",
        ],
        "what_to_bring": [
            "솔직한 음주 패턴 — 외래에서는 비밀 보장",
            "동반 약물·영양제",
            "최근 체중·식이",
            "기존 간 검사 결과",
        ],
        "related": [
            ("/대사이상지방간-MASLD/", "MASLD/MetALD"),
            ("/술-안마셔도-지방간/", "술 안 마셔도 지방간"),
            ("/updates/PEth-알코올-바이오마커/", "PEth — 알코올 바이오마커"),
            ("/updates/GLP1RA-알코올성-간질환-ALD/", "GLP-1RA와 알코올성 간 질환"),
        ],
    },
    {
        "slug": "피로-식욕부진",
        "title": "지속적인 피로·식욕 부진이 있어요",
        "summary": "비특이적 증상이지만 진행된 간 질환에서 자주 보입니다. 다른 원인(빈혈·갑상선·우울·종양)과 함께 간 평가를 동시 진행합니다.",
        "what_we_check": [
            "<strong>전반적 평가</strong> — CBC, 신장·갑상선·전해질, 종양 표지 (필요 시)",
            "<strong>간 평가</strong> — 간 효소, 알부민·PT(합성능), 빌리루빈, Fibroscan",
            "<strong>영양 상태</strong> — 체중·BMI·근감소증 평가",
            "<strong>정신 건강</strong> — 우울·수면·스트레스 평가",
            "필요 시 종합 검진 흐름으로 의뢰",
        ],
        "what_to_bring": [
            "증상 시작 시점·진행 양상",
            "체중 추세",
            "최근 약물·영양제 변경",
            "동반 증상 — 황달, 발열, 통증, 출혈 경향",
        ],
        "related": [
            ("/간경변-영양-근감소증/", "간경변 영양·근감소증"),
            ("/간경변-대상성-비대상성/", "비대상성 신호"),
            ("/알부민-PT-간합성능/", "알부민·PT — 간 합성능"),
        ],
    },
]


def render_cc_page(spec: dict) -> None:
    slug = spec["slug"]
    title = spec["title"]
    summary = spec["summary"]
    checks = spec["what_we_check"]
    bring = spec["what_to_bring"]
    related = spec["related"]
    canonical = f"https://drshin.kr/CC/{slug}/"

    checks_html = "".join(f"<li>{c}</li>" for c in checks)
    bring_html = "".join(f"<li>{b}</li>" for b in bring)
    related_html = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in related)

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Hepatology Note</title>
<meta name="description" content="{esc(title)} — 외래에서 어떻게 진료받게 되는지 단계별 안내.">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
</head>
<body>
{NAV}
<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="/CC/">주호소</a> › <span>{esc(title)}</span></nav>
<article>
<h1 style="font-size:24px;line-height:1.4">"{esc(title)}"</h1>
<div class="tldr"><strong>한 줄 안내</strong>{summary}</div>

<h2>외래에서 무엇을 확인하는가</h2>
<ul style="font-size:16px;line-height:1.85">{checks_html}</ul>

<h2>가져오시면 좋은 것</h2>
<ul style="font-size:16px;line-height:1.85">{bring_html}</ul>

<aside class="related" style="margin-top:36px"><h2>관련 가이드 · 사례</h2><ul>{related_html}</ul></aside>

<p class="disclaimer" style="margin-top:36px">본 페이지는 외래 진료의 일반적 흐름을 안내합니다. 실제 진료는 환자 개별 상황에 따라 달라질 수 있습니다.</p>
</article>
</main>
{FOOTER}
</body>
</html>
'''
    out = ROOT / "CC" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: /CC/{slug}/")


def render_cc_hub() -> None:
    rows = "".join(
        f'<a href="/CC/{c["slug"]}/" class="cc-row">'
        f'<div class="cc-cite">"{esc(c["title"])}"</div>'
        f'<p class="cc-sum">{esc(c["summary"])}</p>'
        f'</a>'
        for c in CC_LIST
    )
    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>주호소 안내 — Hepatology Note</title>
<meta name="description" content="외래에서 자주 듣는 {len(CC_LIST)}가지 주호소와 단계별 진료 흐름.">
<link rel="canonical" href="https://drshin.kr/CC/">
<meta property="og:type" content="website">
<meta property="og:title" content="주호소 안내">
<meta property="og:url" content="https://drshin.kr/CC/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<style>
.cc-list{{display:flex;flex-direction:column;gap:0;border-top:1px solid var(--line);margin:24px 0}}
.cc-row{{display:block;padding:18px 4px;border-bottom:1px solid var(--line);text-decoration:none;color:var(--fg);transition:background .12s}}
.cc-row:hover{{background:#f9f8f3}}
.cc-cite{{font-family:'Times New Roman',Georgia,serif;font-size:18px;font-weight:600;color:var(--fg);margin-bottom:4px;letter-spacing:-0.005em}}
.cc-row:hover .cc-cite{{color:var(--accent)}}
.cc-sum{{margin:4px 0 0;font-size:14px;color:var(--muted);line-height:1.55}}
</style>
</head>
<body>
{NAV}
<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>주호소 안내</span></nav>
<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:32px;letter-spacing:-0.02em;font-weight:600;margin:8px 0 8px">주호소 안내 (Chief Complaints)</h1>
<p class="intro">외래에서 자주 듣는 {len(CC_LIST)}가지 주호소를 정리하였습니다. 각 페이지에서 외래 진료가 어떻게 진행되는지, 무엇을 가져오시면 좋은지 안내합니다.</p>

<div class="cc-list">{rows}</div>
</main>
{FOOTER}
</body>
</html>
'''
    out = ROOT / "CC" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: /CC/ (hub)")


print(f"Building {len(CC_LIST)} chief-complaint pages...")
for c in CC_LIST:
    render_cc_page(c)
render_cc_hub()
print("Done.")
