#!/usr/bin/env python3
"""Phase 2 (5 CC) + Phase 3 (10 Updates)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gen_draft_pages import write_pages

# === Phase 2: CC ===
CC_HUB, CC_LBL, CC_SEC = "/CC/", "증상별 안내", "증상별 안내"

CC = [
{"slug":"잇몸-출혈-멍", "is_cc":True, "hub_path":CC_HUB, "hub_label":CC_LBL, "section":CC_SEC,
"title":"잇몸 출혈·잘 멍드는 증상", "h1":"\"잇몸에서 피가 나고 멍이 잘 들어요\"",
"desc":"잇몸 출혈·작은 외상에도 잘 멍드는 증상이 외래에서 호소되면 무엇을 보는가. 응고 장애·간경변·혈소판 감소의 단서.",
"keywords":"잇몸출혈, 멍, 응고장애, 혈소판",
"tags":[("잇몸출혈",),("멍",),("응고장애",)],
"tldr":"잇몸에서 자주 피가 나거나, 작은 충격에도 멍이 빠르게 퍼지는 증상은 간 질환과 연결될 수 있습니다. 간이 응고 인자를 만들고 비장 비대로 혈소판이 적어지기 때문입니다. 다른 원인(혈액 질환·약물·비타민 K 부족)도 함께 평가합니다. 외래에서 첫 단계는 PT/INR + 혈소판 + 알부민 검사입니다.",
"sections":[
{"heading":"외래에서 듣는 흔한 호소","html":"<ul><li>\"양치할 때 자주 피가 나요\"</li><li>\"별일 없이도 다리에 멍이 들어요\"</li><li>\"코피가 자주 나요\"</li><li>\"수술 후 출혈이 평소보다 길었어요\"</li></ul><p>이런 호소를 들으면 저는 간 기능과 응고 능력을 한 번에 평가합니다.</p>"},
{"heading":"외래에서 확인하는 검사","html":"<ul><li><strong>PT/INR</strong> — 응고 인자 활동성</li><li><strong>혈소판</strong> — 비장 비대·골수 영향</li><li><strong>알부민</strong> — 간 합성능 종합 지표</li><li><strong>간 효소</strong> — ALT·AST·ALP·GGT</li><li><strong>빌리루빈</strong> — 황달 동반 여부</li><li><strong>비타민 K 의심 시</strong> — 식이력·만성 설사·항생제 사용</li><li><strong>혈액학적 평가</strong> — Hb, 적혈구 형태(필요 시)</li></ul>"},
{"heading":"흔한 원인별 흐름","html":"<table><thead><tr><th>원인</th><th>패턴</th></tr></thead><tbody><tr><td>간경변</td><td>INR ↑, 혈소판 ↓, 알부민 ↓, 영상에서 간경변 소견</td></tr><tr><td>혈소판 감소 (혈액 질환)</td><td>INR 정상, 혈소판 매우 낮음, 다른 혈구 이상 동반 가능</td></tr><tr><td>비타민 K 부족</td><td>INR ↑, 다른 간 기능 정상, 식이·만성 설사 이력</td></tr><tr><td>항응고제 영향</td><td>INR ↑, 와파린·DOAC 복용력</td></tr><tr><td>약물 (aspirin·NSAIDs)</td><td>혈소판 기능 영향, 검사 수치 거의 정상</td></tr></tbody></table>"},
{"heading":"즉시 외래·응급실 신호","html":"<ul><li>출혈이 멈추지 않거나 30분 이상 지속</li><li>토혈·흑변 — 위장관 출혈 의심</li><li>의식 변화 동반</li><li>심한 두통 + 시야 변화 — 뇌출혈 가능성</li><li>대량 출혈 후 어지럼·창백</li></ul>"},
{"heading":"외래 진행 흐름","html":"<ol><li>증상 시작 시기·빈도·강도 청취</li><li>약물 이력 — 항응고제, aspirin, NSAIDs, 한약</li><li>식이·간 질환 이력 확인</li><li>혈액 검사 — PT/INR, 혈소판, 간 기능</li><li>이상 시 영상(복부 초음파)</li><li>원인에 따라 비타민 K 보충, 약 조정, 간 평가 진행</li></ol>"},
],
"faqs":[
("멍이 자주 드는데 간 때문일까요?","간 기능 검사로 평가 가능. 다만 다른 원인이 더 흔하니 종합 검사가 필요해요."),
("응급실 가야 하나요?","출혈이 멎지 않거나 토혈·흑변·의식 변화 동반 시 즉시 응급실. 일반 멍은 외래에서 충분."),
("비타민 K 영양제 먹어도 되나요?","원인이 확인되기 전엔 자가 복용 권장 안 됨. 와파린 복용 환자는 비타민 K가 약효 떨어뜨림."),
]},

{"slug":"다리부종", "is_cc":True, "hub_path":CC_HUB, "hub_label":CC_LBL, "section":CC_SEC,
"title":"양쪽 다리 부종", "h1":"\"다리가 자주 붓고 양말 자국이 깊게 남아요\"",
"desc":"양쪽 다리 부종이 외래에서 호소되면 간경변·심부전·신증후군·정맥부전·갑상선 등을 종합 평가합니다.",
"keywords":"부종, 다리부종, 알부민, 심부전, 간경변",
"tags":[("부종",),("알부민",),("간경변",)],
"tldr":"양쪽 다리가 함께 붓고 양말 자국이 깊게 남는 부종은 간경변·심부전·신증후군·정맥부전·갑상선 기능 등 여러 원인이 있습니다. 외래에서 첫 단계는 알부민·신기능·간 기능·심장 평가입니다. 한쪽만 부으면 정맥혈전·림프부종을 먼저 의심합니다.",
"sections":[
{"heading":"양쪽 vs 한쪽","html":"<ul><li><strong>양쪽 부종</strong> — 전신 질환 (간·심·신·갑상선·약물). 외래에서 평가.</li><li><strong>한쪽 부종</strong> — 정맥혈전·림프부종·국소 감염. 즉시 평가, 응급 가능.</li></ul>"},
{"heading":"외래 평가","html":"<ul><li>혈액 검사 — 알부민, 간 기능, BUN/Cr, 갑상선(TSH)</li><li>소변 검사 — 단백뇨(신증후군 평가)</li><li>심장 — 흉부 X선, 필요 시 심초음파</li><li>복부 초음파 — 간·복수 평가</li><li>약물 검토 — 칼슘 차단제(암로디핀 등), NSAIDs, 일부 당뇨약</li></ul>"},
{"heading":"흔한 원인","html":"<table><thead><tr><th>원인</th><th>단서</th></tr></thead><tbody><tr><td>간경변·복수</td><td>알부민 ↓, 간 기능 이상, 복부 팽만</td></tr><tr><td>심부전</td><td>호흡곤란, 야간 호흡곤란, BNP ↑</td></tr><tr><td>신증후군</td><td>단백뇨 ≥ 3.5 g/일, 알부민 ↓</td></tr><tr><td>정맥부전</td><td>저녁 악화, 거상으로 호전</td></tr><tr><td>약물</td><td>칼슘 차단제 시작 시기와 일치</td></tr><tr><td>갑상선 기능 저하</td><td>TSH ↑, 점액부종</td></tr></tbody></table>"},
{"heading":"외래 진행 흐름","html":"<ol><li>부종 시작·악화 패턴 청취</li><li>혈액·소변 검사</li><li>심·간·신 영상 평가 (필요 시)</li><li>원인 별 치료 — 이뇨제, 알부민 보충, 압박 스타킹, 약 조정</li></ol>"},
],
"faqs":[
("부종이 있는데 물을 줄여야 하나요?","원인이 확인된 후 결정. 나트륨 줄이는 게 더 효과적이에요. 자가 수분 제한은 권하지 않습니다."),
("약국에서 이뇨제 사서 먹어도 되나요?","원인을 모르고 이뇨제 사용은 신기능·전해질 이상 위험. 외래 평가 후 처방이 안전."),
("한쪽만 갑자기 부었어요","정맥혈전 의심. 응급실에서 도플러 초음파 평가."),
]},

{"slug":"만성-가려움증", "is_cc":True, "hub_path":CC_HUB, "hub_label":CC_LBL, "section":CC_SEC,
"title":"만성 가려움증", "h1":"\"전신이 자꾸 가려운데 발진은 없어요\"",
"desc":"발진 없는 만성 가려움증은 담즙정체·만성 신부전·갑상선·혈액 질환·임신 등 전신 원인 가능성. 외래에서 첫 단계.",
"keywords":"가려움증, pruritus, 담즙정체, PBC",
"tags":[("가려움증",),("pruritus",),("담즙정체",)],
"tldr":"발진 없는 만성 가려움증(pruritus)은 담즙정체(PBC·PSC·간경변), 만성 신부전, 갑상선·혈액 질환, 임신(ICP) 같은 전신 원인을 시사합니다. 일반 항히스타민제가 잘 안 듣는 패턴이 특징적입니다. 외래에서 첫 검사 — ALP·GGT·총담즙산·갑상선·신기능.",
"sections":[
{"heading":"발진 없는 가려움 — 외래 평가","html":"<ul><li>ALP·GGT·총담즙산 — 담즙정체</li><li>AMA — PBC</li><li>TSH — 갑상선</li><li>CBC, ferritin — 빈혈·혈액 질환</li><li>BUN/Cr — 신기능</li><li>HCV·HIV (위험군)</li><li>임신 시 ICP 평가</li></ul>"},
{"heading":"흔한 원인","html":"<table><thead><tr><th>원인</th><th>특징</th></tr></thead><tbody><tr><td>PBC</td><td>중년 여성, ALP·AMA ↑</td></tr><tr><td>PSC</td><td>IBD 동반, MRCP 진단</td></tr><tr><td>간경변</td><td>장기 가려움, 다른 합병증 동반</td></tr><tr><td>만성 신부전</td><td>요독성 가려움</td></tr><tr><td>임신 ICP</td><td>3분기 손·발 가려움, 총담즙산 ↑</td></tr><tr><td>혈액 질환</td><td>다발성 골수종, 폴리시테미아</td></tr><tr><td>건조 피부</td><td>특히 노인, 보습으로 호전</td></tr></tbody></table>"},
{"heading":"외래 진행 흐름","html":"<ol><li>가려움 부위·시간·강도 청취</li><li>피부 검진 (발진 유무)</li><li>혈액 검사 패키지</li><li>원인 평가 후 약물 — 보습, cholestyramine, sertraline, naltrexone 순.</li></ol>"},
],
"faqs":[
("연고만 발라도 되나요?","원인 평가가 우선. 단순 건조 가려움이라면 보습으로 충분."),
("항히스타민제가 안 들어요","담즙정체·요독성 가려움은 항히스타민에 잘 안 듣습니다. 다른 약물 옵션 검토."),
("임신 중인데 갑자기 가려워요","3분기 손·발바닥 가려움 + 야간 악화는 ICP 의심. 산과·간내과 평가.")
]},

{"slug":"거미혈관-수장홍반", "is_cc":True, "hub_path":CC_HUB, "hub_label":CC_LBL, "section":CC_SEC,
"title":"피부에 거미줄 같은 혈관·손바닥 빨간 증상", "h1":"\"가슴이나 얼굴에 거미줄 같은 혈관이 생겼어요\"",
"desc":"거미혈관(spider angioma)·수장 홍반(palmar erythema)은 간경변의 흔한 피부 소견. 호르몬 변화와 정상 변종 가능성도.",
"keywords":"거미혈관, 수장홍반, 간경변, 신체검진",
"tags":[("거미혈관",),("수장홍반",),("간경변",)],
"tldr":"가슴·얼굴·팔 위쪽에 거미줄 같은 작은 혈관(거미혈관, spider angioma), 손바닥이 평소보다 빨간(수장 홍반, palmar erythema)은 만성 간 질환의 흔한 피부 소견입니다. 다만 임신·갑상선·정상 변종에서도 보일 수 있어 단독으로 진단하지 않습니다. 외래에서 다른 간 단서와 함께 평가합니다.",
"sections":[
{"heading":"거미혈관 — 무엇인가","html":"<ul><li>중심 동맥점 + 거미줄 같은 작은 혈관이 방사상으로 퍼짐</li><li>가슴 위쪽·얼굴·팔·등 (상대정맥 영역) 우세</li><li>중심을 누르면 색이 사라지고 떼면 다시 채워짐</li><li>5개 이상이면 간경변 의심도 올라감</li><li>임신·경구피임약·갑상선기능항진에서도 가능</li><li>건강한 사람의 약 10~15%에서도 1~2개</li></ul>"},
{"heading":"수장 홍반","html":"<ul><li>손바닥 가장자리(특히 엄지·새끼손가락 옆)가 빨간 양상</li><li>간경변·임신·갑상선·류마티스에서 보임</li><li>증상은 없고 외관 변화만</li></ul>"},
{"heading":"외래에서 보는 평가","html":"<ul><li>다른 간 단서 — 황달, 복수, 비장 비대, 정맥류 출혈 이력</li><li>혈액 검사 — ALT·AST·알부민·INR·혈소판</li><li>영상 — 복부 초음파, Fibroscan</li><li>임신·갑상선·호르몬 가능성 평가</li></ul>"},
{"heading":"외래 진행 흐름","html":"<ol><li>피부 소견 시기·개수 확인</li><li>다른 간 단서 청취·검진</li><li>혈액·영상 검사</li><li>간 질환 확인 시 정기 추적 시작</li></ol>"},
],
"faqs":[
("거미혈관이 하나 있는데 간 질환인가요?","한두 개는 정상인도 있어요. 5개 이상 또는 빠르게 늘면 평가."),
("임신 중 생기는 건 위험한가요?","임신 자체로 자주 생깁니다. 출산 후 사라지면 안전 신호."),
("수장 홍반이 갑자기 생겼어요","간·갑상선·임신·류마티스 모두 평가. 혈액 검사로 시작.")
]},

{"slug":"검은변-피섞임", "is_cc":True, "hub_path":CC_HUB, "hub_label":CC_LBL, "section":CC_SEC,
"title":"검은변·피섞인 변·토혈", "h1":"\"검은 변이 나오거나 토할 때 피가 섞여 나와요\"",
"desc":"검은변(melena)·토혈은 위장관 출혈의 신호. 정맥류 출혈, 위·십이지장 궤양, 위염 등 응급 평가가 필요한 패턴.",
"keywords":"멜레나, 토혈, 정맥류, 응급",
"tags":[("멜레나",),("토혈",),("정맥류",),("응급",)],
"tldr":"검은변(melena, 끈적한 검은 타르 같은 변), 토혈(피 또는 커피 찌꺼기 같은 토함), 변에 선홍색 피 섞임은 모두 위장관 출혈 신호로 <strong>즉시 응급실 평가</strong>가 필요합니다. 간경변·정맥류 환자에서는 특히 응급 신호 — 첫 24시간이 결과를 결정합니다. 검은변이 의심되면 \"기다리지 말고 가세요\"가 외래 표준 안내입니다.",
"sections":[
{"heading":"색·형태가 알려주는 것","html":"<table><thead><tr><th>형태</th><th>출혈 부위</th></tr></thead><tbody><tr><td>검은 타르 같은 변 (melena)</td><td>상부 위장관(식도·위·십이지장)</td></tr><tr><td>커피 찌꺼기 같은 토함</td><td>위(소화된 피)</td></tr><tr><td>선홍색 토혈</td><td>식도·위 (활동성 출혈)</td></tr><tr><td>대변에 선홍색 피</td><td>하부 위장관 (대장·항문)</td></tr><tr><td>검붉은 변</td><td>중하부 위장관</td></tr></tbody></table>"},
{"heading":"흔한 원인 — 간 질환 관련","html":"<ul><li><strong>식도·위 정맥류 출혈</strong> — 간경변에서 응급. 6주 사망률 15~20%.</li><li><strong>위염·궤양</strong> — 알코올·NSAIDs·항응고제 사용자에서 흔함.</li><li><strong>Portal hypertensive gastropathy</strong> — 간경변에서 만성 출혈.</li><li><strong>Mallory-Weiss tear</strong> — 심한 구토 후 식도-위 접합부 열상.</li></ul>"},
{"heading":"응급 시 — 외래·응급실","html":"<ol><li>활력 징후 — 혈압·맥박·의식</li><li>혈액 검사 — Hb, 응고, 간 기능</li><li>긴급 EGD(상부 위장관 내시경) — 24시간 내</li><li>활동성 정맥류 출혈 — 결찰 + 혈관수축제(테르리프레신·옥트레오타이드) + 예방적 항생제</li><li>안정화 후 평가·치료</li></ol>"},
{"heading":"\"검은변 같은데 약 부작용 아닐까요?\"","html":"<ul><li>철분제·비스무스 — 변 색을 진하게 만들지만 멜레나의 점착성·악취 패턴은 아님</li><li>야채(시금치·블루베리) — 일시적</li><li>구분 어려우면 응급실에서 잠혈검사로 확인</li><li>의심되면 \"기다리지 말고 가세요\"가 안전</li></ul>"},
],
"faqs":[
("검은변 한 번이었는데 다시 정상이에요","한 번이라도 외래·응급실 평가가 안전. 출혈이 멈췄어도 원인 평가 필요."),
("간경변 환자인데 토혈했어요","정맥류 출혈 가능성. 즉시 응급실, 응급실 도착 전까지 누워서 호흡 안정."),
("아스피린 복용 중인데 검은변","NSAIDs·아스피린 관련 위장관 출혈 가능. 즉시 응급실, 약 중단 여부는 응급실에서 결정.")
]},
]

# === Phase 3: Updates 10개 ===
UPD_HUB, UPD_LBL, UPD_SEC = "/updates/", "최신 지견", "최신 지견"

UPDATES = [
{"slug":"EMERALD-1-TACE-durva-bev-Lancet-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"EMERALD-1 — TACE + durvalumab + bevacizumab (Lancet 2024)", "h1":"EMERALD-1 — 중간기 간암에 TACE + 면역치료 + 항혈관 조합",
"desc":"중간기 간세포암(BCLC B)의 표준이 TACE 단독에서 TACE + durvalumab + bevacizumab로 바뀌는 출발점. Lancet 2024.",
"keywords":"EMERALD-1, TACE, durvalumab, bevacizumab, HCC",
"tags":[("EMERALD-1",),("TACE",),("durvalumab",),("bevacizumab",)],
"tldr":"중간기 간세포암(BCLC B)에서 TACE 단독으로 진행을 막아온 약 20년 동안 의미 있는 변화가 없었습니다. <strong>EMERALD-1 시험(Lancet 2024)</strong>은 TACE에 durvalumab + bevacizumab을 결합한 군이 TACE 단독 군 대비 <strong>무진행 생존(PFS)을 의미 있게 연장(15.0 vs 8.2개월)</strong>했음을 보여 BCLC B의 첫 번째 standard-shifting 시험으로 자리잡았습니다. 한국 보험 적용은 곧 따라올 가능성이 있습니다.",
"sections":[
{"heading":"배경","html":"<p>중간기(BCLC B) 간암은 절제·소작이 어렵고 진행기는 아닌 단계로, 약 20년간 TACE 단독이 표준이었습니다. 그러나 TACE만으로는 의미 있는 OS 향상이 없었고 반복 시술의 한계도 명확했습니다. 면역치료가 진행기에서 효과를 보인 IMbrave150(2020) 이후 그 효과를 중간기로 가져오자는 흐름이 EMERALD-1의 출발점입니다.</p>"},
{"heading":"설계","html":"<ul><li>616명, 절제·소작 불가능 BCLC B 또는 LRT 후보 환자</li><li>Arm 1: TACE + durvalumab + bevacizumab</li><li>Arm 2: TACE + durvalumab 단독</li><li>Arm 3: TACE + placebo</li><li>1차 평가 — PFS (Arm 1 vs Arm 3)</li><li>Durvalumab — anti-PD-L1, Bevacizumab — anti-VEGF</li></ul>"},
{"heading":"결과","html":"<ul><li>PFS 중앙값 — Arm 1: 15.0개월, Arm 3: 8.2개월 (HR 0.77, P=0.032)</li><li>Durvalumab 단독 추가는 placebo 대비 의미 있는 차이 없음</li><li>객관적 반응률(ORR) — Arm 1에서 더 높음</li><li>OS 데이터 — 추적 중. 향후 update 예정.</li><li>안전성 — 면역 관련 부작용, 출혈 위험 (베바시주맙). 식도정맥류 평가 사전 필수.</li></ul>"},
{"heading":"단호한 임상 의견","html":"<p>저는 이 결과를 \"중간기 간암의 분기점\"이라고 봅니다. 20년 동안 단일 표준이었던 TACE에 면역치료가 결합되는 첫 무작위 근거입니다. 다만 OS 데이터가 아직 미성숙해 \"바뀐다\"고 단정하기는 이른 단계. 한국 보험 적용 결정에는 시간이 좀 더 필요할 듯합니다. 그동안 임상시험 참여를 적극 검토하는 것이 합리적입니다.</p>"},
{"heading":"한국 임상에서의 의미","html":"<ul><li>한국 KLCA-NCC는 EMERALD-1 결과 반영 검토 중</li><li>보험 적용 결정에 1~2년 소요 예상</li><li>임상시험 참여 — 서울대·삼성·아산·세브란스 등 활발</li><li>식도정맥류 사전 평가 필수 (베바시주맙 출혈 위험)</li></ul>"},
],
"refs":["Lencioni R, et al. Transarterial chemoembolization combined with durvalumab plus bevacizumab in unresectable hepatocellular carcinoma (EMERALD-1): a randomised, placebo-controlled, phase 3 study. <em>Lancet</em> 2024."]},

{"slug":"CheckMate-9DW-nivo-ipi-Lancet-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"CheckMate 9DW — Nivolumab + Ipilimumab 1차 (Lancet 2024)", "h1":"CheckMate 9DW — 진행기 간암 1차에서 nivo+ipi vs sorafenib/lenvatinib",
"desc":"진행기 간세포암 1차 치료로 nivolumab + ipilimumab이 sorafenib/lenvatinib 대비 OS 우월. Lancet 2024/2025.",
"keywords":"CheckMate 9DW, nivolumab, ipilimumab, HCC, 1차",
"tags":[("nivolumab",),("ipilimumab",),("HCC",),("1차치료",)],
"tldr":"진행기 간세포암(BCLC C)의 1차 면역치료 옵션이 atezo+bev(IMbrave150), durva+treme(HIMALAYA STRIDE)에 이어 <strong>nivolumab + ipilimumab(CheckMate 9DW, Lancet 2024)</strong>이 추가되었습니다. Sorafenib/lenvatinib 대비 OS 중앙값 23.7 vs 20.6개월로 의미 있는 연장. 1차 면역치료 옵션 다양화로 환자별 맞춤 선택이 가능해졌습니다.",
"sections":[
{"heading":"설계와 결과","html":"<ul><li>668명 진행기 HCC 환자 1차</li><li>Arm 1: Nivolumab + Ipilimumab → maintenance nivolumab</li><li>Arm 2: Sorafenib 또는 Lenvatinib</li><li>OS 중앙값 — 23.7 vs 20.6개월 (HR 0.79)</li><li>ORR — Arm 1에서 더 높음</li><li>면역 관련 부작용 — Arm 1에서 높지만 관리 가능</li></ul>"},
{"heading":"AtezoBev·STRIDE·Nivo+Ipi — 어떻게 선택하나","html":"<table><thead><tr><th>옵션</th><th>적합 환자</th></tr></thead><tbody><tr><td>AtezoBev</td><td>출혈 위험 낮음, 식도정맥류 안정</td></tr><tr><td>STRIDE (durva+treme)</td><td>출혈 위험 큰 환자 (정맥류 활동)</td></tr><tr><td>Nivo+Ipi</td><td>새 옵션, 더 깊은 반응 기대 환자</td></tr></tbody></table>"},
{"heading":"한국에서의 적용","html":"<p>2026년 5월 현재 nivo+ipi는 한국에서 일부 적응증으로 보험 적용. 1차로의 확대는 의료기관 결정·보험 심사에 따라 진행 중. 임상시험 참여도 활발.</p>"},
],
"refs":["Galle PR, et al. Nivolumab plus ipilimumab as first-line treatment for unresectable HCC (CheckMate 9DW). <em>Lancet</em> 2024/2025."]},

{"slug":"LEAP-012-TACE-pembro-lenva-Lancet-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"LEAP-012 — TACE + Pembrolizumab + Lenvatinib (Lancet 2024)", "h1":"LEAP-012 — 중간기 간암에 TACE + 면역치료 + TKI 조합 두 번째 근거",
"desc":"중간기 간세포암에서 TACE + pembrolizumab + lenvatinib 조합이 TACE 단독 대비 PFS 의미 있게 연장. EMERALD-1과 함께 BCLC B 표준 변화의 두 번째 근거.",
"keywords":"LEAP-012, pembrolizumab, lenvatinib, TACE",
"tags":[("LEAP-012",),("pembrolizumab",),("lenvatinib",)],
"tldr":"EMERALD-1에 이어 중간기 간세포암에서 TACE + 면역치료 조합의 두 번째 무작위 근거입니다. <strong>TACE + pembrolizumab + lenvatinib</strong> 조합이 TACE 단독 대비 PFS를 의미 있게 연장(14.6 vs 10.0개월)했습니다. 두 시험이 같은 방향으로 결과를 낸 것은 BCLC B 표준 변화의 강한 신호입니다.",
"sections":[
{"heading":"설계","html":"<ul><li>480명 BCLC B HCC 환자</li><li>Arm 1: TACE + pembrolizumab + lenvatinib</li><li>Arm 2: TACE + 단독 (또는 + placebo)</li><li>1차 평가 — PFS·OS</li></ul>"},
{"heading":"결과","html":"<ul><li>PFS 중앙값 — 14.6 vs 10.0개월 (HR 0.66, P&lt;0.001)</li><li>OS — 추적 중, 일부 호전 경향</li><li>부작용 — 면역치료 + lenvatinib 조합으로 부작용 관리 필요</li></ul>"},
{"heading":"의미","html":"<p>EMERALD-1과 LEAP-012는 \"TACE + 면역치료 + 항혈관/TKI\" 조합의 효과를 두 번째로 확인. 단일 시험이 아닌 두 시험의 일치가 BCLC B 표준 변화의 근거로 의미 있습니다.</p>"},
],
"refs":["Llovet JM, et al. Transarterial chemoembolization with pembrolizumab plus lenvatinib for unresectable HCC (LEAP-012). <em>Lancet</em> 2024."]},

{"slug":"ESSENCE-survodutide-MASH-Lancet-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"Survodutide — GLP-1/Glucagon dual agonist (Lancet 2024)", "h1":"Survodutide — GLP-1/Glucagon 이중 작용제의 MASH 임상시험",
"desc":"GLP-1과 글루카곤 수용체를 동시 작용하는 survodutide의 MASH 2상 — 위약 대비 NASH 호전과 섬유화 호전 모두 보임.",
"keywords":"survodutide, GLP-1, glucagon, MASH",
"tags":[("survodutide",),("GLP-1",),("MASH",)],
"tldr":"<strong>Survodutide(BI 456906)</strong>는 GLP-1과 글루카곤 수용체를 동시 활성화하는 이중 작용제로, 2024년 NEJM/Lancet에서 발표된 2상 시험에서 NASH 환자의 약 80%에서 NASH 호전(섬유화 악화 없이) + 60%에서 섬유화 호전을 보고했습니다. Resmetirom·semaglutide와 함께 MASH 약물 시대를 여는 신약 후보입니다.",
"sections":[
{"heading":"메커니즘","html":"<ul><li>GLP-1 작용 — 인슐린 분비·식욕 억제·체중 감량</li><li>Glucagon 작용 — 간 지방 분해 직접 효과</li><li>둘의 동시 작용으로 체중 감량 + 간 지방 감소 + 인슐린 감수성 개선</li></ul>"},
{"heading":"결과","html":"<ul><li>2상 — MASH F2-F3 환자 295명</li><li>48주 — NASH 호전 약 60~80% (위약 약 14%)</li><li>섬유화 호전 — 약 40~60%</li><li>체중 감량 약 14~17%</li><li>부작용 — 오심·구토(GLP-1 흔한), 다른 안전성 양호</li></ul>"},
{"heading":"의미","html":"<p>Resmetirom (MAESTRO-NASH 2024)이 NASH 약물 시대의 첫 승인 약이라면, survodutide·efruxifermin·tirzepatide 등이 그 뒤를 잇는 후보들. 한국 임상시험 참여 검토 가치 큼.</p>"},
],
"refs":["Sanyal AJ, et al. Survodutide in metabolic dysfunction-associated steatohepatitis with fibrosis. <em>NEJM/Lancet</em> 2024."]},

{"slug":"MASLD-nomenclature-AASLD-EASL-2023", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"MASLD 새 명명 — NAFLD를 대체 (Hepatology 2023)", "h1":"MASLD·MASH·MetALD — NAFLD/NASH 명명을 대체한 새 표준",
"desc":"AASLD·EASL·ALEH의 Delphi 합의로 NAFLD → MASLD, NASH → MASH로 명명 변경. MetALD 새 카테고리 도입.",
"keywords":"MASLD, MASH, MetALD, NAFLD",
"tags":[("MASLD",),("MASH",),("MetALD",)],
"tldr":"2023년 AASLD·EASL·ALEH의 Delphi 합의로 30년간 쓰인 NAFLD/NASH 명명이 <strong>MASLD(Metabolic dysfunction-Associated Steatotic Liver Disease)·MASH</strong>로 바뀌었습니다. \"비-알코올성\"이라는 부정적 정의 대신 \"대사 이상 동반\"이라는 적극적 진단 기준을 사용하고, 적당량 음주 + 대사 위험 동반은 <strong>MetALD</strong>로 별도 분류했습니다. 한국 KASL도 2024년 새 명명 채택.",
"sections":[
{"heading":"왜 명명을 바꿨나","html":"<ul><li>\"Non-alcoholic\"이 stigma·잘못된 메시지</li><li>대사 위험 인자에 기반한 정의가 더 정확</li><li>알코올 + 대사 동반(MetALD)을 별도로 분류해 진료 흐름 명확</li><li>국제 표준화 — 30개국 200+ 전문가 Delphi 합의</li></ul>"},
{"heading":"새 진단 기준","html":"<ul><li><strong>MASLD</strong> — 영상·조직 지방간 + 최소 1개 대사 위험 인자 (비만·당뇨·전당뇨·고혈압·고지혈증)</li><li><strong>MASH</strong> — MASLD + 조직에서 풍선화·염증</li><li><strong>MetALD</strong> — MASLD + 적당량 음주(남 140~350 g/주, 여 70~210 g/주)</li><li><strong>ALD</strong> — 의미 있는 음주 (위 한계 초과)</li></ul>"},
{"heading":"임상적 의미","html":"<ul><li>기존 NAFLD 환자 대부분이 새 정의에서도 MASLD에 해당 — 코드 전환은 매끄러움</li><li>MetALD 새 카테고리 — 두 원인 동시 관리</li><li>유전·임상 연구·치료 시험 — 새 정의로 진행 중</li><li>한국 KASL 가이드라인 2024 채택</li></ul>"},
],
"refs":["Rinella ME, et al. A multisociety Delphi consensus statement on new fatty liver disease nomenclature. <em>Hepatology</em> 2023.","Chan WK, et al. Asian Pacific Association for the Study of the Liver position paper on MASLD/MetALD. <em>Hepatol Int</em> 2024."]},

{"slug":"Bepirovirsen-HBV-Lancet-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"Bepirovirsen — B형간염 antisense oligonucleotide (Lancet 2024)", "h1":"Bepirovirsen — B형간염의 functional cure 도전",
"desc":"HBV RNA를 분해하는 antisense oligonucleotide bepirovirsen. B-Clear 시험에서 HBsAg 소실 약 9~10%, 새 시대의 첫 후보.",
"keywords":"bepirovirsen, HBV, functional cure, ASO",
"tags":[("bepirovirsen",),("functional cure",),("HBV",)],
"tldr":"<strong>Bepirovirsen</strong>은 HBV mRNA를 직접 분해하는 antisense oligonucleotide(ASO)로, B형간염의 functional cure(HBsAg 소실)를 노리는 첫 새 약입니다. B-Clear 시험(Lancet 2023/2024)에서 24주 치료 후 HBsAg 소실이 약 9~10%에서 보고되었습니다. 표준 항바이러스제(entecavir·TAF)에 추가로 사용했을 때의 효과가 가장 큰 그룹은 HBsAg quant 낮은 환자.",
"sections":[
{"heading":"메커니즘","html":"<ul><li>HBV mRNA에 결합하는 antisense oligonucleotide</li><li>HBsAg 등 HBV 단백질 생성 차단</li><li>주 1회 피하 주사</li></ul>"},
{"heading":"결과","html":"<ul><li>B-Clear — 24주 치료, 1차 평가 HBsAg + HBV DNA 음전</li><li>HBsAg 소실 — 약 9~10% (위약 0)</li><li>HBsAg quant 낮은 환자에서 가장 효과적</li><li>부작용 — ALT 상승, 주사 부위 반응</li></ul>"},
{"heading":"의미","html":"<p>B형간염은 30년 동안 \"바이러스 억제는 가능하나 완치 불가능\"이었습니다. Bepirovirsen은 functional cure 가능성을 보여 첫 후보로 자리잡았으며, 다른 ASO·siRNA(예: JNJ-3989)와 함께 \"5년 내 functional cure 30%\" 목표의 시작점입니다.</p>"},
],
"refs":["Yuen MF, et al. Efficacy and safety of bepirovirsen in chronic hepatitis B (B-Clear). <em>NEJM/Lancet</em> 2024."]},

{"slug":"MAESTRO-NASH-resmetirom-3년-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"MAESTRO-NASH 3년 확장 — Resmetirom 장기 안전성·효과", "h1":"Resmetirom 3년 데이터 — 첫 MASH 약의 장기 효과 확인",
"desc":"MAESTRO-NASH 3년 추적 — Resmetirom(thyroid hormone β receptor agonist)이 NASH·섬유화 호전을 3년 유지하고 안전성 양호.",
"keywords":"resmetirom, MASH, 3년 추적, MAESTRO",
"tags":[("resmetirom",),("MASH",),("MAESTRO-NASH",)],
"tldr":"<strong>Resmetirom</strong>(Rezdiffra)은 2024년 미국 FDA가 승인한 첫 MASH 치료제로, thyroid hormone β receptor agonist 메커니즘으로 간 지방 분해를 직접 유도합니다. MAESTRO-NASH 1년 결과로 승인을 받았고, 2024년 후속 발표된 3년 데이터에서 NASH 호전·섬유화 호전이 지속 유지되며 새로운 안전성 우려는 없음이 확인되었습니다.",
"sections":[
{"heading":"메커니즘","html":"<ul><li>Thyroid hormone receptor β 선택적 작용</li><li>간 지방 분해·콜레스테롤 감소</li><li>중추 신경·심장에 미치는 영향 적음</li><li>경구 1일 1회</li></ul>"},
{"heading":"3년 추적 결과","html":"<ul><li>NASH 호전(섬유화 악화 없이) — 약 30%에서 유지</li><li>섬유화 호전 — 약 25%에서 유지</li><li>안전성 — 위장 부작용, 일부 갑상선 미세 변화. 새 안전성 우려 없음</li><li>심혈관 — LDL·중성지방 감소 효과 함께</li></ul>"},
{"heading":"적응증과 한국","html":"<ul><li>FDA 승인 — F2-F3 MASH (간생검 또는 비침습 단서)</li><li>한국 — 2026년 5월 현재 임상 단계, 곧 도입 예상</li><li>비용·보험 — 미국에서 비싼 편(연 약 5만 달러), 한국 도입 시 보험 적용 결정 필요</li></ul>"},
],
"refs":["Harrison SA, et al. A phase 3, randomized, controlled trial of resmetirom in NASH (MAESTRO-NASH). <em>NEJM</em> 2024.","Harrison SA, et al. 3-year results from MAESTRO-NASH. <em>Hepatology</em> 2024/2025."]},

{"slug":"Baveno-VII-recompensation-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"Baveno VII — 비대상성 → 재대상화 임상 정의 (J Hepatol 2022/2024)", "h1":"Baveno VII — 비대상성 간경변의 재대상화 정의와 임상 적용",
"desc":"Baveno VII 합의에서 처음으로 \"재대상화(recompensation)\"의 임상 정의 제시. 원인 치료 + 합병증 1년 무발생 + 간 기능 개선.",
"keywords":"Baveno VII, recompensation, 재대상화, 간경변",
"tags":[("Baveno VII",),("recompensation",),("간경변",)],
"tldr":"<strong>Baveno VII 합의(2022)</strong>에서 처음으로 비대상성 간경변의 <strong>재대상화(recompensation)</strong>가 임상 정의되었습니다. 세 조건을 모두 충족 — (1) 원인 질환의 효과적 치료(B형간염 항바이러스제, 알코올 금주, MASH 체중 감량 등), (2) 합병증(복수·정맥류 출혈·간성혼수)이 12개월 이상 재발 없음, (3) 간 기능의 지속적 개선. 이 정의는 한국 KASL·일본 JSH도 채택하여 임상 결정에 영향을 주고 있습니다.",
"sections":[
{"heading":"왜 재대상화 정의가 필요했나","html":"<ul><li>비대상성 = 영구 불가역이라는 옛 통념과 달리, 원인 치료 후 일부 환자에서 간 기능이 의미 있게 회복</li><li>이런 환자가 이식 명단에서 제외(delisting)될 수도 있는데 임상 정의가 없었음</li><li>표준 정의로 임상 결정·연구의 일관성 확보</li></ul>"},
{"heading":"3대 기준","html":"<ol><li><strong>원인 치료의 지속적 효과</strong> — B형간염 DNA 검출 한계 이하, 알코올성에서 1년 이상 금주, MASH에서 7~10% 체중 감량.</li><li><strong>합병증 12개월 무발생</strong> — 복수·정맥류 출혈·간성혼수가 12개월 이상 재발 없음.</li><li><strong>간 기능 개선 지속</strong> — Child-Pugh A로 회복, 알부민·INR·빌리루빈 정상화.</li></ol>"},
{"heading":"한국에서의 적용","html":"<ul><li>B형간염 + 비대상성 환자에서 entecavir·TAF로 가장 흔한 패턴</li><li>알코올성에서 1년 이상 금주 후</li><li>이식 명단 delisting 결정에 사용</li><li>다만 간경변 자체가 사라진 것은 아님 — 평생 추적·간암 검진 유지</li></ul>"},
],
"refs":["de Franchis R, et al. Baveno VII — Renewing consensus in portal hypertension. <em>J Hepatol</em> 2022.","D'Amico G, et al. Clinical states of cirrhosis and competing risks. <em>J Hepatol</em> 2018."]},

{"slug":"AI-CT-HCC-validation-Hepatology-2024", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"AI 기반 CT 간세포암 진단 — 다기관 검증 (Hepatology 2024)", "h1":"AI CT HCC 진단 — 다기관·다국가 검증으로 임상 적용 가까워짐",
"desc":"동적 CT 영상에서 HCC를 자동 진단하는 AI 알고리즘의 대규모 다기관·다국가 검증. 영상 전문의 수준 진단 정확도.",
"keywords":"AI, CT, HCC, 진단, 영상의학",
"tags":[("AI",),("CT",),("HCC",),("영상의학",)],
"tldr":"동적 CT 영상에서 간세포암을 자동으로 진단·분류하는 AI 모델들이 대규모 다기관·다국가 검증을 거치며 임상 적용에 가까워지고 있습니다. 한국·미국·EU·일본 다기관 데이터로 학습·검증된 모델은 영상 전문의 수준의 진단 정확도(AUC 0.95+)를 보이며, LI-RADS LR-3/4/5 분류 자동화도 일부 진행 중입니다.",
"sections":[
{"heading":"AI 진단의 임상 가치","html":"<ul><li>영상 전문의 부족 의료기관에서 1차 검토 도구</li><li>LI-RADS 분류 일관성 — 사람마다 다른 판독을 표준화</li><li>대규모 검진 데이터에서 결절 검출</li><li>후속 평가 우선순위 결정</li></ul>"},
{"heading":"한계와 주의","html":"<ul><li>학습 데이터 편향 — 다양한 인구·기기에서 검증 필요</li><li>LI-RADS 회색지대(LR-3·LR-4)에서 정확도 약함</li><li>임상 결정은 영상의·간내과 의사 최종 판단</li><li>FDA·EMA 승인은 부분적 — 의사 보조 도구로 위치</li></ul>"},
{"heading":"한국 임상에서의 의미","html":"<p>서울대·아산·삼성·세브란스 등에서 자체 AI 모델 개발·임상 적용 진행. 일부 의료기관은 LI-RADS 분류 자동화 도구를 영상의학과 임상에 통합. 환자 입장에서는 \"AI가 판독한 결과\"가 표시되는 보고서를 보게 될 가능성이 늘어남.</p>"},
],
"refs":["Multi-institutional validation studies of AI for HCC diagnosis. <em>Hepatology</em> 2024.","Shin H, et al. AI-based CT model for HCC in chronic hepatitis B. <em>J Hepatol</em> 2025."]},

{"slug":"IMbrave050-adjuvant-atezo-bev-Lancet-2023", "is_update":True, "hub_path":UPD_HUB, "hub_label":UPD_LBL, "section":UPD_SEC,
"title":"IMbrave050 — 근치 치료 후 보조 면역치료 (Lancet 2023)", "h1":"IMbrave050 — 절제·소작 후 보조 atezo+bev의 첫 양성 결과",
"desc":"고위험 절제·소작 후 atezolizumab + bevacizumab 12개월이 재발 없는 생존(RFS)을 의미 있게 연장한 첫 양성 보조 면역치료 시험. Lancet 2023.",
"keywords":"IMbrave050, adjuvant, atezolizumab, 절제후",
"tags":[("IMbrave050",),("adjuvant",),("HCC",)],
"tldr":"<strong>IMbrave050(Lancet 2023)</strong>은 간세포암 절제·소작 후 재발 위험이 높은 환자에서 보조 면역치료(adjuvant immunotherapy)가 처음으로 양성 결과를 보인 시험입니다. Atezolizumab + bevacizumab 12개월이 active surveillance 대비 무재발 생존(RFS)을 의미 있게 연장(HR 0.72). 절제·소작 후 \"기다리는 것\"이 표준이었던 흐름을 바꿀 가능성이 있는 결과로, 한국 임상 적용은 보험·접근성 결정 후 정해질 예정입니다.",
"sections":[
{"heading":"배경","html":"<p>간세포암은 절제·소작 후에도 5년 재발률이 약 60~70%로 매우 높습니다. 그동안 \"근치 치료 후 추적\"이 유일한 표준이었고 sorafenib·peretinoin 등 보조 치료 시도는 모두 실패했습니다. IMbrave050은 첫 양성 보조 시험으로 의미가 큽니다.</p>"},
{"heading":"설계와 결과","html":"<ul><li>668명 고위험 절제·소작 후 환자</li><li>Arm 1: Atezo + Bev 12개월</li><li>Arm 2: Active surveillance</li><li>1차 평가 — RFS</li><li>RFS HR 0.72 (P=0.012)</li><li>안전성 — 면역 관련 부작용, 출혈 위험. 식도정맥류 평가 사전 필수.</li><li>OS — 추적 중. 미성숙.</li></ul>"},
{"heading":"적응증 — 누가 고위험인가","html":"<ul><li>크기 ≥ 5 cm 또는 다발성</li><li>미세혈관 침범 (병리에서 확인)</li><li>위성 결절</li><li>저분화도</li><li>혈청 표지자 상승</li></ul>"},
{"heading":"단호한 의견","html":"<p>저는 이 결과를 신중하게 봅니다. RFS 차이는 있지만 OS 데이터가 아직 미성숙해 \"전체 환자에서 표준 변경\"이라고 단정하기 어렵습니다. 부작용·비용·환자 부담을 감안하면 진정 고위험 환자에 한정해 적용하는 것이 합리적입니다. 한국 보험 적용은 OS 데이터 + 비용 효율 분석 이후 결정될 가능성이 큽니다.</p>"},
],
"refs":["Qin S, et al. Adjuvant atezolizumab plus bevacizumab in HCC after curative treatment (IMbrave050). <em>Lancet</em> 2023.","Sangro B, et al. Editorial: The promise and challenges of adjuvant immunotherapy in HCC. <em>J Hepatol</em> 2024."]},
]

if __name__ == "__main__":
    write_pages(CC + UPDATES)
