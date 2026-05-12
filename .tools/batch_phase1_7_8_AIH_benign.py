#!/usr/bin/env python3
"""Phase 1.7+1.8: 자가면역간염 + 간양성종양 — 5+5 each."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gen_draft_pages import write_pages

AIH_HUB, AIH_LBL, AIH_SEC = "/자가면역간염/", "자가면역간염", "자가면역간염"

AIH = [
{"slug":"자가면역간염-PBC-overlap", "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"AIH·PBC overlap 증후군", "h1":"AIH·PBC overlap 증후군 — 두 자가면역 간 질환의 동반",
"desc":"AIH와 PBC가 함께 있는 overlap 증후군. Paris criteria 기반 진단과 UDCA + 면역억제 병합 치료.",
"keywords":"AIH, PBC, overlap, UDCA",
"tags":[("AIH",),("PBC",),("overlap",)],
"tldr":"<strong>AIH-PBC overlap 증후군</strong>은 자가면역 간염(AIH)과 원발성 담즙성 담관염(PBC)의 특징이 한 환자에서 동시에 나타나는 상태입니다. 전체 PBC 환자의 약 5~10%, AIH 환자의 약 5%에서 보고됩니다. Paris criteria로 진단하며, 치료는 PBC에 대한 UDCA + AIH에 대한 면역억제(스테로이드 + 아자티오프린)를 병합합니다. 단독 질환보다 진행이 빠를 수 있어 적극적 관리가 필요합니다.",
"sections":[
{"heading":"Paris criteria — 진단 기준","html":"<p>AIH·PBC 각각 3개 항목 중 최소 2개씩 충족 시 overlap으로 분류합니다.</p><ul><li><strong>AIH 항목</strong>: (1) ALT ≥ 정상 상한 5배, (2) IgG ≥ 정상 상한 2배 또는 ASMA 양성, (3) 조직에서 moderate-severe interface hepatitis.</li><li><strong>PBC 항목</strong>: (1) ALP ≥ 정상 상한 2배 또는 GGT ≥ 5배, (2) AMA 양성, (3) 조직에서 담관 손상(florid duct lesion).</li></ul>"},
{"heading":"치료 — 병합","html":"<ul><li><strong>UDCA 13~15 mg/kg/일</strong> — PBC 표준. 모든 환자에서 시작.</li><li><strong>Prednisolone + Azathioprine</strong> — AIH 표준. ALT·IgG·interface hepatitis 의미 있으면 추가.</li><li>UDCA 단독으로 시작 후 12개월 반응 평가 → 부족하면 면역억제 추가하는 접근도 일부에서 사용.</li><li>한국 환자에서 NUDT15 확인 (AZA 골수억제 위험).</li></ul>"},
{"heading":"예후와 추적","html":"<p>치료 반응 좋으면 단독 질환과 비슷한 예후이나, 일부에서는 더 빠른 섬유화 진행이 보고됩니다. ALT·IgG·ALP·GGT 모두 정상화 + 임상 안정이 목표입니다. 약 중단은 매우 신중 — 재발률이 매우 높음.</p>"}],
"faqs":[("AMA 양성인데 AIH 진단을 받았어요. Overlap인가요?","ALP·GGT도 함께 의미 있게 오르고 조직 소견이 동반되면 overlap 가능. 단순 AMA 양성만으로는 overlap 진단 안 됨."),
("UDCA만 먹어도 되나요?","AIH 활성이 의미 있으면 면역억제 추가가 표준. UDCA 단독으로 시작 후 평가하는 패턴도 있어요."),
("Overlap 환자도 약 중단이 가능한가요?","매우 신중. 재발률이 단독 AIH보다도 높을 수 있어 대부분 평생 유지.")],
"refs":["Boberg KM, et al. Overlap syndromes: the International Autoimmune Hepatitis Group position statement on a controversial issue. <em>J Hepatol</em> 2011."]},

{"slug":"자가면역간염-임신", "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"AIH와 임신", "h1":"자가면역간염 환자의 임신 — 약물 전환과 임신 중·후 관리",
"desc":"AIH 환자의 임신 계획·임신 중·산후 관리. Azathioprine 유지 가능, mycophenolate 금기. 산후 재발 위험 30~50%.",
"keywords":"AIH, 임신, azathioprine, mycophenolate",
"tags":[("AIH",),("임신",),("azathioprine",)],
"tldr":"AIH 여성도 안전하게 임신·출산이 가능합니다. 핵심은 (1) 임신 전 6개월 이상 안정 유지 후 계획, (2) <strong>azathioprine은 유지 가능</strong>, <strong>mycophenolate는 절대 금기</strong>(태아 기형), (3) 임신 중 정기 ALT·IgG 추적, (4) <strong>산후 30~50%에서 재발</strong>해 분만 후 추적 강화입니다. 산과·간내과 협진이 표준.",
"sections":[
{"heading":"임신 전 — 약 조정","html":"<ul><li><strong>Mycophenolate (MMF)</strong> — 절대 금기. 최소 6주 전 중단 후 다른 약으로 전환.</li><li><strong>Azathioprine</strong> — 유지 가능. 임신 안전성 자료 풍부.</li><li><strong>Prednisolone</strong> — 유지 가능, 저용량.</li><li><strong>Tacrolimus</strong> — 유지 가능, 일부.</li><li>6개월 이상 안정 유지 후 임신 계획 권장.</li></ul>"},
{"heading":"임신 중 추적","html":"<ul><li>각 3분기마다 ALT·IgG·간 기능</li><li>임신 중 약 60~70%에서 자연 호전 (면역계 변화) — 약 감량 가능</li><li>일부에서 악화 — 약 증량 또는 입원</li><li>산과 협진으로 분만법 일반 적응증으로 결정</li></ul>"},
{"heading":"산후 — 재발 흔함","html":"<ul><li>분만 후 1~6개월에 30~50% 재발</li><li>분만 후 1·3·6개월 ALT·IgG 추적 표준</li><li>재발 시 즉시 약 증량</li><li>모유 수유 — azathioprine·prednisolone 모두 안전(소량 분비)</li></ul>"}],
"faqs":[("MMF를 먹고 있는데 임신해도 되나요?","임신 6주 전 다른 약(AZA·tacrolimus)으로 전환 후 임신 계획."),
("임신 중 ALT가 떨어졌어요. 약을 끊어도 되나요?","자연 호전이지 완치 아닙니다. 자가 중단 위험."),
("산후 우울증과 AIH 재발이 헷갈리는데","산후 ALT·IgG 검사로 객관적으로 평가. 정신과·간내과 협진이 도움.")],
"refs":["EASL Clinical Practice Guidelines: AIH. <em>J Hepatol</em> 2015.","Westbrook RH, et al. Outcomes of pregnancy in women with AIH. <em>J Hepatol</em> 2012."]},

{"slug":"자가면역간염-스테로이드-부작용", "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"스테로이드 부작용 관리", "h1":"AIH 치료 중 스테로이드 부작용 — 모니터와 대처",
"desc":"Prednisolone 장기 사용의 부작용(당뇨·고혈압·골다공증·백내장·감염·인지) 모니터 일정과 대처. Budesonide·azathioprine 단독 전환 시점.",
"keywords":"스테로이드, prednisolone, 부작용, budesonide",
"tags":[("스테로이드",),("부작용",),("budesonide",)],
"tldr":"AIH 치료의 핵심 약 prednisolone은 효과적이지만 장기 사용 시 당뇨·고혈압·골다공증·백내장·감염·인지 영향 등 부작용이 있습니다. 부작용 최소화 전략은 (1) 빠르게 5 mg 이하로 감량, (2) azathioprine 단독으로 전환, (3) 비간경변 환자에서 budesonide로 전환, (4) 정기 모니터입니다.",
"sections":[
{"heading":"흔한 부작용과 모니터","html":"<table><thead><tr><th>부작용</th><th>발현 시점</th><th>모니터</th></tr></thead><tbody><tr><td>당뇨·고혈당</td><td>수주</td><td>HbA1c 3개월, 혈당</td></tr><tr><td>고혈압</td><td>수주~수개월</td><td>월 1회</td></tr><tr><td>골다공증</td><td>3~6개월</td><td>DEXA baseline + 1~2년</td></tr><tr><td>백내장</td><td>1년 이상</td><td>1년 1회 안과</td></tr><tr><td>감염 위험</td><td>지속</td><td>증상 발생 시 빠른 평가, 백신 챙기기</td></tr><tr><td>체중·외모 변화</td><td>수개월</td><td>환자 상담</td></tr><tr><td>기분·수면</td><td>수주</td><td>주관 호소 청취</td></tr></tbody></table>"},
{"heading":"대처 전략","html":"<ul><li><strong>가능한 빨리 5 mg 이하로 감량</strong> — 부작용 의미 있게 줄어듬.</li><li><strong>Azathioprine 단독 유지로 전환</strong> — 관해 도달 후 6~12개월.</li><li><strong>Budesonide 9 mg</strong> — 비간경변 환자에서 prednisolone 대안. 전신 부작용 적음. 간경변에서는 금기.</li><li><strong>칼슘·비타민 D 보충 + DEXA</strong> — 골다공증 예방.</li><li><strong>예방접종</strong> — 인플루엔자·폐렴구균·코로나19. 생백신은 감량 후.</li></ul>"},
{"heading":"한국 진료 현장","html":"<ul><li>외래에서 가장 자주 호소되는 부작용 — 체중 증가, 둥근 얼굴, 기분 변화</li><li>환자에게 \"이건 일시적이고 약 줄이면 호전된다\"는 메시지 + 가능한 빠른 감량</li><li>당뇨 가족력·전당뇨 환자는 시작 전 평가</li><li>골밀도는 폐경 여성·고령 남성 우선 baseline</li></ul>"}],
"faqs":[("스테로이드 부작용이 너무 심해요","빠른 감량 가능 여부 진료의와 상의. 일부는 budesonide·azathioprine 단독으로 전환 가능."),
("Budesonide가 prednisolone보다 무조건 좋나요?","비간경변에서는 전신 부작용 적어 유리. 간경변에서는 효과 떨어지고 사용 금기."),
("스테로이드 끊으면 부작용 다 사라지나요?","대부분 호전. 골다공증·백내장은 일부 잔존. 그래서 시작부터 예방.")],
"refs":["EASL Clinical Practice Guidelines: AIH.","Manns MP, et al. Budesonide induces remission more effectively than prednisone in a controlled trial of patients with autoimmune hepatitis. <em>Gastroenterology</em> 2010."]},

{"slug":"자가면역간염-소아청소년", "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"소아·청소년 AIH", "h1":"소아·청소년 자가면역간염 — 더 공격적, ASC overlap 흔함",
"desc":"소아·청소년 AIH의 특징 — 성인보다 빠른 진행, 자가면역성 경화성 담관염(ASC) overlap 흔함. 진단·치료의 차이.",
"keywords":"소아 AIH, 청소년, ASC, 경화성담관염",
"tags":[("소아 AIH",),("청소년",),("ASC",)],
"tldr":"소아·청소년 AIH는 성인보다 <strong>더 공격적</strong>이고 <strong>자가면역성 경화성 담관염(ASC)과 동반</strong>되는 경우가 흔합니다(약 30~50%). MRCP로 담관 평가가 진단의 표준이며, 치료는 성인과 비슷한 스테로이드 + 아자티오프린이지만 ASC 동반 시 UDCA도 추가합니다. 사춘기 환자의 약 복용 순응도가 큰 임상 과제입니다.",
"sections":[
{"heading":"성인과 다른 점","html":"<ul><li>진단 시 50% 이상이 비대상성 간경변까지 진행되어 있음</li><li>ASC overlap이 30~50%로 매우 흔함 — 모든 환자에서 MRCP 권고</li><li>Anti-LKM-1 양성(type 2 AIH)이 성인보다 많음</li><li>치료 반응은 좋으나 약 중단 후 재발률 더 높음</li><li>사춘기 순응도가 큰 변수</li></ul>"},
{"heading":"치료","html":"<ul><li>Prednisolone + Azathioprine (성인과 동일)</li><li>ASC 동반 시 UDCA 추가</li><li>한국에서 NUDT15 검사 — 골수억제 위험 평가</li><li>학교·심리 지원</li><li>장기 추적 — 성장·골격·생식 영향 평가</li></ul>"},
{"heading":"한국 진료","html":"<ul><li>소아청소년과·간내과 협진이 표준</li><li>이행기(transition) 외래 — 18~21세에 성인 외래로 점진 이행</li><li>학교 결석·체육 활동 등 일상 적응 지원</li></ul>"}],
"faqs":[("소아 AIH는 평생 약을 먹어야 하나요?","평생은 아니지만 장기 유지가 표준. 일부 환자에서 약 중단 가능."),
("아이가 약을 빠뜨려요","흔한 문제. 가족 협력·앱·간호사 상담 등 도구 활용.")],
"refs":["Mieli-Vergani G, et al. Autoimmune hepatitis in children: an update. <em>J Pediatr Gastroenterol Nutr</em> 2018."]},

{"slug":"자가면역간염-급성간부전", "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"급성 발현 AIH와 간부전", "h1":"급성 발현 AIH — 급성 간부전으로 오는 형태",
"desc":"AIH가 급성 간염·간부전으로 처음 발견되는 경우. 빠른 진단과 면역억제 + 이식 평가 동시 진행.",
"keywords":"급성 간부전, AIH, 이식",
"tags":[("급성 간부전",),("AIH",),("이식",)],
"tldr":"AIH의 약 10~25%는 급성 간염 또는 급성 간부전 형태로 발현합니다. 황달·심한 ALT 상승·응고 이상이 빠르게 진행하며, 빠른 진단과 면역억제 시작이 핵심입니다. 일부 환자는 면역억제 반응 없이 진행해 응급 이식이 필요합니다.",
"sections":[
{"heading":"임상 양상","html":"<ul><li>급성 황달·피로·식욕 부진</li><li>ALT 500~3000, AST 비슷</li><li>빌리루빈 5~20, INR 1.5 이상</li><li>일부에서 간성혼수·복수 동반</li><li>진단 — 다른 급성 간염 원인 배제 후 ANA·SMA·LKM·IgG·조직</li></ul>"},
{"heading":"치료","html":"<ul><li>입원 + 입원 환경 면역억제 시작 — 고용량 prednisolone (1~2 mg/kg)</li><li>2주 내 임상 반응 없으면 이식 평가</li><li>King's College criteria 등 이식 적응증 평가</li><li>일부에서 빠르게 호전하면 외래 추적으로 전환</li></ul>"},
{"heading":"예후","html":"<p>빠른 면역억제 시작 시 70~80%에서 회복. 반응 없으면 이식 적응증. King's College criteria 비-아세트아미노펜 기준 (INR > 6.5 또는 INR > 3.5 + bilirubin > 17.5 + 나이 > 40 등)이 적용됩니다.</p>"}],
"faqs":[("급성으로 발현된 AIH도 평생 약을 먹나요?","급성기 회복 후에도 maintenance가 표준. 일부에서 약 중단 시도 가능."),
("이식 받으면 AIH가 다시 생기나요?","이식 후 재발 약 20~40%. 면역억제 조정으로 대응.")],
"refs":["Stravitz RT, Lee WM. Acute liver failure. <em>Lancet</em> 2019.","Czaja AJ. Acute and acute severe (fulminant) autoimmune hepatitis. <em>Dig Dis Sci</em> 2013."]},

# Cases AIH
{"slug":"AIH-PBC-overlap-진단", "is_case":True, "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"ALT·ALP 모두 상승 + AMA 양성", "h1":"40대 여성 ALT 250 + ALP 480 + AMA·ANA 모두 양성 — Overlap",
"desc":"중년 여성에서 ALT·ALP 동시 상승 + AMA·ANA 모두 양성. 조직 검사로 PBC + AIH 특징 확인 후 overlap 진단 + 병합 치료 사례.",
"keywords":"overlap, AMA, ANA, UDCA",
"tags":[("overlap",),("AMA",),("UDCA",)],
"case_intro":"45세 여성, 3개월 피로감 + 약한 가려움. 검사 — ALT 250, AST 180, ALP 480, GGT 320, IgG 28 g/L, IgM 약간 상승. ANA 1:160, AMA 양성, ASMA 1:80. 다른 간 질환 마커 음성.",
"sections":[
{"heading":"진단","html":"<p>Paris criteria — AIH 항목 3개 중 3개(ALT 5배+, IgG·자가항체, 조직 interface) 충족, PBC 항목 3개 중 3개(ALP 2배+, AMA, 조직) 충족 — overlap 확진. 조직 — interface hepatitis + florid duct lesion 모두 보임.</p>"},
{"heading":"치료","html":"<p>UDCA 13 mg/kg + prednisolone 30 mg + azathioprine 50 mg 시작. 6주 후 ALT 60, ALP 230. 3개월 후 ALT·ALP·IgG 모두 정상화. Prednisolone 감량 시작.</p>"},
],
"teaching":["<strong>Overlap은 단독 질환보다 진단 어렵고 진행 빠를 수 있음</strong>","<strong>UDCA + 면역억제 병합이 표준</strong>","<strong>한국 환자에서 NUDT15 검사 후 AZA 시작</strong>","<strong>임상 안정 후에도 평생 유지 일반적</strong>"]},

{"slug":"AIH-임신중-약물전환", "is_case":True, "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"MMF에서 AZA로 — 임신 계획", "h1":"임신 계획 환자의 MMF → AZA 전환",
"desc":"안정기 AIH 환자가 임신 계획 6개월 전 MMF 중단 + AZA로 전환. 임신·산후 안정 유지 사례.",
"keywords":"임신, MMF, AZA",
"tags":[("임신",),("MMF",),("AZA",)],
"case_intro":"32세 여성, AIH 6년 안정. MMF 1.5 g/일 + prednisolone 5 mg/일 유지. 결혼 후 임신 계획.",
"sections":[
{"heading":"전환","html":"<p>MMF는 임신 절대 금기. 6주 전 중단 + AZA 75 mg/일로 전환. 6주에 ALT·IgG 안정 확인 후 임신 시도 권유.</p>"},
{"heading":"임신·산후","html":"<p>임신 3개월에 임신 확인. 3분기 ALT 약간 상승(45) — 모니터, 약 유지. 자연 분만. 산후 3개월에 ALT 65로 재발 신호 — prednisolone 일시 증량(15 mg)으로 호전. 6개월 후 안정. 모유 수유 지속.</p>"},
],
"teaching":["<strong>MMF는 임신 금기, AZA·prednisolone은 안전</strong>","<strong>임신 6주~6개월 전 약 전환 + 안정 확인</strong>","<strong>산후 30~50%에서 재발 — 분만 후 1·3·6개월 추적</strong>","<strong>모유 수유 가능 (AZA·prednisolone 모두 안전)</strong>"]},

{"slug":"AIH-스테로이드-당뇨발생", "is_case":True, "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"AIH 치료 6개월에 스테로이드 유발 당뇨", "h1":"Prednisolone 6개월 — 스테로이드 유발 당뇨",
"desc":"전당뇨 가족력 환자에서 AIH 치료 중 prednisolone 유발 당뇨 발생. Budesonide 전환 + 메트포민으로 관리한 사례.",
"keywords":"스테로이드, 당뇨, budesonide",
"tags":[("스테로이드",),("당뇨",),("budesonide",)],
"case_intro":"58세 남성, 전당뇨 가족력. AIH 치료 prednisolone 20 mg + AZA 100 mg 6개월. ALT·IgG 안정. 정기 검사에서 HbA1c 7.6 (이전 5.9). 공복혈당 165.",
"sections":[
{"heading":"평가와 결정","html":"<p>스테로이드 유발 당뇨로 진단. 옵션 — (1) prednisolone 감량 강화, (2) budesonide 전환, (3) 당뇨약 추가.</p>"},
{"heading":"진행","html":"<p>비간경변 + AIH 안정 유지 → budesonide 9 mg 전환 + 메트포민 500 mg 시작. 3개월 후 HbA1c 6.5, ALT 정상 유지. Budesonide는 9 → 6 → 3 mg으로 감량 진행.</p>"},
],
"teaching":["<strong>전당뇨·당뇨 가족력 환자는 스테로이드 시작 전 평가</strong>","<strong>Budesonide가 prednisolone 대안 — 비간경변 환자</strong>","<strong>당뇨약과 면역억제 병용 안전</strong>","<strong>스테로이드 부작용은 시작 시점부터 예방·모니터</strong>"]},

{"slug":"AIH-소아청소년-진단", "is_case":True, "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"13세 소녀 ALT 600 — ASC overlap 진단", "h1":"13세 소녀의 급성 ALT 상승 — AIH + ASC overlap",
"desc":"13세 여학생에서 급성 ALT 상승 + IgG 상승 + LKM-1 양성. MRCP에서 담관 변형 확인 후 ASC overlap 진단.",
"keywords":"소아 AIH, ASC, LKM-1",
"tags":[("소아 AIH",),("ASC",),("LKM-1",)],
"case_intro":"13세 여학생. 3주 피로·황달·식욕 부진. 검사 — ALT 620, AST 480, 빌리루빈 6.5, IgG 32 g/L (정상 ≤ 16). ANA 1:80, ASMA 1:40, anti-LKM-1 1:160(type 2 AIH). MRCP에서 간내 담관 비대칭·협착 — ASC overlap.",
"sections":[
{"heading":"진단","html":"<p>Type 2 AIH (anti-LKM-1 양성, 소아에서 흔함) + ASC overlap. 조직 — interface hepatitis + 담관 주위 섬유화.</p>"},
{"heading":"치료","html":"<p>소아과·간내과 협진. Prednisolone 1 mg/kg 시작 + UDCA. NUDT15 정상 확인 후 AZA 25 mg 시작 후 증량. 6주 후 ALT 80, 빌리루빈 1.5. 학교 결석 2주 후 복귀. 6개월 후 안정.</p>"},
],
"teaching":["<strong>소아 AIH는 ASC overlap이 흔함</strong> — 모든 환자에서 MRCP 권고","<strong>Type 2 AIH (LKM-1+)는 소아에서 흔하고 더 공격적</strong>","<strong>학교·심리 지원이 임상 결과에 영향</strong>","<strong>한국 NUDT15 평가 후 AZA 시작</strong>"]},

{"slug":"AIH-급성간부전", "is_case":True, "hub_path":AIH_HUB, "hub_label":AIH_LBL, "section":AIH_SEC,
"title":"급성 간부전으로 첫 진단된 AIH", "h1":"황달·간성혼수로 입원 — AIH 급성 간부전, 면역억제로 회복",
"desc":"40대 여성에서 급성 황달·간성혼수로 응급 입원. AIH 진단 후 고용량 스테로이드로 2주 안에 회복, 이식 회피 사례.",
"keywords":"급성간부전, AIH, 스테로이드",
"tags":[("급성간부전",),("AIH",)],
"case_intro":"42세 여성. 3주 피로 후 급성 황달·졸음. 응급실 — INR 2.8, 빌리루빈 18, ALT 1850, AST 1240, 암모니아 110. 다른 급성 간염 원인(바이러스·약물·아세트아미노펜) 모두 음성. ANA 1:320, IgG 38 g/L.",
"sections":[
{"heading":"진단·즉시 치료","html":"<p>임상·혈청학으로 AIH 강하게 의심. 조직 검사 위험으로 보류. Methylprednisolone 1 mg/kg/일 정맥 + 입원 환경 모니터링.</p>"},
{"heading":"경과","html":"<p>3일째 ALT 1850 → 920, 빌리루빈 18 → 14, INR 2.8 → 1.9. 7일째 임상 호전, 졸음 사라짐. 2주째 ALT 220, 경구 prednisolone 60 mg/일로 전환. NUDT15 확인 후 AZA 추가. 4주째 외래 전환. 이식 명단 등록은 시작했었으나 호전으로 미루지 않고 보류.</p>"},
],
"teaching":["<strong>AIH는 급성 발현이 10~25%</strong>","<strong>다른 급성 간염 원인 배제 + 자가항체 + IgG로 진단 시작</strong>","<strong>빠른 면역억제 + 이식 평가 동시 진행</strong>","<strong>2주 내 반응 평가 — 호전 없으면 이식 진행</strong>","<strong>King's College criteria 등 이식 적응증 평가</strong>"]},
]

# === 간양성종양 ===
BEN_HUB, BEN_LBL, BEN_SEC = "/간양성종양/", "간 양성종양", "간 양성종양"

BEN = [
{"slug":"간양성종양-담관과오종", "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"담관 과오종(bile duct hamartoma)", "h1":"담관 과오종 — 작은 양성 결절들로 자주 헷갈리는 영상 패턴",
"desc":"Von Meyenburg complex(담관 과오종) — 무수한 작은 양성 담관 기형. 영상에서 다발성 작은 결절로 보여 전이암·림프종과 헷갈릴 수 있음.",
"keywords":"담관과오종, von Meyenburg, 양성종양",
"tags":[("담관과오종",),("Von Meyenburg",)],
"tldr":"<strong>Von Meyenburg complex(담관 과오종)</strong>은 작은 양성 담관 기형이 간 전체에 무수히 분포한 상태입니다. 부검 시리즈에서 약 1%에서 발견되며 대부분 평생 무증상. 영상에서 5~15 mm 작은 결절들이 양엽에 다발성으로 보여 종종 전이암·림프종으로 오해되지만, MRCP에서 담관과의 미세 연결과 T2 매우 고신호가 특징입니다.",
"sections":[
{"heading":"영상 특징","html":"<ul><li>5~15 mm 작은 결절들이 간 전체에 다발성</li><li>T2 강조 영상 매우 고신호 (\"검은 별 빛나는 하늘\" 패턴)</li><li>동맥기 조영 없음</li><li>MRCP에서 일부는 담관과 연결</li><li>CT보다 MRI가 진단에 결정적</li></ul>"},
{"heading":"감별","html":"<table><thead><tr><th>감별</th><th>구분 포인트</th></tr></thead><tbody><tr><td>다발성 단순 낭종</td><td>크기 더 크고 매끈한 벽</td></tr><tr><td>전이암</td><td>동맥기 가장자리 조영, washout</td></tr><tr><td>림프종</td><td>동맥기 균일 조영, 림프절 동반</td></tr><tr><td>다낭성 간질환</td><td>훨씬 큰 낭종들, ADPKD 동반 흔함</td></tr></tbody></table>"},
{"heading":"관리","html":"<p>대부분 평생 무증상이고 악성 변화 위험 없음 — 추적 종료 가능. 다만 일부에서 콜란지오카르시노마(드물게 보고)·반복 담관염 보고. 영상에서 비전형 변화 시 재평가.</p>"}],
"faqs":[("CT에서 \"간에 결절이 많다\"고 들었는데 위험한가요?","MRI(특히 MRCP)로 평가가 결정적. 담관과오종이 확인되면 안전."),
("악성으로 변할 수 있나요?","극히 드뭅니다. 일률적 평생 추적 권장 안 됨.")],
"refs":["Lev-Toaff AS, et al. The radiologic and pathologic spectrum of biliary hamartomas. <em>AJR Am J Roentgenol</em> 1995."]},

{"slug":"간양성종양-국소지방-변화", "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"국소 지방 침착·국소 지방 저하", "h1":"국소 지방 침착(focal fat deposition)과 국소 지방 저하(focal sparing)",
"desc":"지방간 배경에서 일부 부위만 지방 적은 \"섬\"(focal sparing)이나, 정상 간 배경에서 일부 부위만 지방이 많은(focal fat deposition) 패턴. 종양으로 오해되기 쉬운 영상 변종.",
"keywords":"국소지방, focal fat, sparing",
"tags":[("focal fat",),("focal sparing",)],
"tldr":"지방간 환자 일부에서 간 안의 특정 부위만 지방이 적게 쌓이거나(focal sparing), 정상 간에서 특정 부위만 지방이 많이 쌓이는(focal fat deposition) 패턴이 보일 수 있습니다. 동맥기·정맥기에 종양처럼 보일 수 있어 종종 평가 대상이 됩니다. <strong>MRI in-phase·out-of-phase 영상</strong>에서 신호 변화로 진단할 수 있어 추가 시술 없이 안전하게 분류됩니다.",
"sections":[
{"heading":"흔한 위치","html":"<ul><li>Focal sparing — 담낭와 주변, S4 (호기성 간동맥 또는 위장 정맥 유입)</li><li>Focal fat deposition — 같은 위치들에서 반대 패턴, 또는 인슐린 영향 부위</li><li>대부분 경계가 매끈하지 않고 \"세그먼트 같은\" 모양</li></ul>"},
{"heading":"진단 — MRI in/out of phase","html":"<p>MRI에서 in-phase는 정상으로, out-of-phase에서는 지방 부위 신호가 떨어집니다. 이 신호 변화 패턴이 결정적. 별도 시술 불필요.</p>"},
{"heading":"의미","html":"<p>임상 의미 없음. 추가 추적 불필요. 종양으로 오해되어 생검까지 가는 일이 가끔 있어 \"고려된 감별 진단\"으로 기억해 둘 가치 있음.</p>"}],
"faqs":[("지방간 환자에게 결절이 있다고 들었어요","focal sparing/deposition일 가능성. MRI로 평가."),
("추적이 필요한가요?","일반적으로 필요 없음.")],
"refs":["Hamer OW, et al. Fatty liver: imaging patterns and pitfalls. <em>Radiographics</em> 2006."]},

{"slug":"간양성종양-NRH", "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"결절성 재생 과형성(NRH)", "h1":"결절성 재생 과형성(NRH) — 자가면역·혈관 질환에서의 양성 결절",
"desc":"Nodular regenerative hyperplasia(NRH) — 자가면역 질환·혈관 질환에서 발생. 영상에서 다발 결절·문맥압 항진을 동반할 수 있음.",
"keywords":"NRH, 결절성재생과형성, 자가면역",
"tags":[("NRH",),("자가면역",),("문맥압항진",)],
"tldr":"<strong>결절성 재생 과형성(NRH, nodular regenerative hyperplasia)</strong>은 간 전체에 작은 양성 재생 결절들이 광범위하게 분포한 상태입니다. 자가면역 질환(SLE·RA·관절류마티스)·혈액 질환·일부 약물에서 발생합니다. 흔히 비대상성 합병증 없이도 <strong>비간경변성 문맥압 항진</strong>을 일으켜 정맥류·복수 위험을 가져옵니다.",
"sections":[
{"heading":"발생 배경","html":"<ul><li>자가면역 — SLE, 류마티스 관절염, AIH</li><li>혈액 질환 — 골수증식성 질환, lymphoma</li><li>약물 — Azathioprine·6-thioguanine·항암제 일부</li><li>심혈관 — Budd-Chiari, 간정맥 폐쇄</li><li>HIV·면역결핍</li></ul>"},
{"heading":"진단","html":"<p>영상으로는 간경변과 비슷해 보일 수 있어 조직이 진단 결정. 특징적 소견 — 결절 사이 압축 + 위축 + 미세 재생 결절. 비간경변성 문맥압 항진의 흔한 원인.</p>"},
{"heading":"관리","html":"<ul><li>원인 평가·교정</li><li>약물 NRH (AZA 등) — 약 변경 검토</li><li>문맥압 항진 합병증 관리 (정맥류 결찰·예방)</li><li>간 기능 추적</li><li>드물게 이식 적응증</li></ul>"}],
"faqs":[("NRH는 간암으로 변하나요?","악성 변화 위험은 일반 인구 수준."),
("간경변과 어떻게 다른가요?","결절 자체는 비슷할 수 있으나 조직학적 구조 차이. 원인·진행 패턴 다름.")],
"refs":["Hartleb M, et al. Nodular regenerative hyperplasia: evolving concepts on underdiagnosed cause of portal hypertension. <em>World J Gastroenterol</em> 2011."]},

{"slug":"간양성종양-임신중", "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"임신 중 간 양성종양의 변화", "h1":"임신 중 간 양성종양 — 변화 패턴과 관리",
"desc":"임신 중 호르몬 변화로 일부 양성종양(혈관종·HCA)이 커지거나 출혈 위험 증가. 임신 전·중 평가와 관리.",
"keywords":"임신, 혈관종, HCA, 양성종양",
"tags":[("임신",),("혈관종",),("HCA",)],
"tldr":"임신 중 호르몬(에스트로겐) 변화로 일부 간 양성종양에 변화가 옵니다. <strong>혈관종</strong>은 약간 커질 수 있으나 대부분 안전, <strong>HCA(간세포 선종)</strong>는 임신 중 출혈 위험이 의미 있게 증가해 임신 계획 단계에서 평가가 필요합니다. <strong>FNH·낭종</strong>은 일반적으로 임신과 무관하게 안전합니다.",
"sections":[
{"heading":"종양별 임신 영향","html":"<table><thead><tr><th>종양</th><th>임신 영향</th><th>관리</th></tr></thead><tbody><tr><td>혈관종</td><td>약간 커질 수 있음, 10 cm↑ 거대 혈관종은 신중</td><td>대부분 안전. 거대 혈관종 산과 협진</td></tr><tr><td>FNH</td><td>거의 변화 없음</td><td>일반 임신 진행</td></tr><tr><td>단순 낭종</td><td>거의 변화 없음</td><td>일반 임신 진행</td></tr><tr><td>HCA</td><td>출혈 위험 ↑ — 특히 5 cm 이상</td><td>임신 전 5 cm↑ 절제 검토. 임신 중 정기 영상.</td></tr></tbody></table>"},
{"heading":"임신 계획 단계","html":"<ul><li>모든 알려진 간 결절 영상 평가</li><li>HCA 5 cm 이상 — 임신 전 절제 권장</li><li>거대 혈관종 — 분만법 산과·외과 협진</li><li>경구피임약 사용 환자에서 HCA 평가 (피임약과 HCA 연관)</li></ul>"},
{"heading":"임신 중 발견","html":"<ul><li>임신 중 새 결절 — 산과·간내과 협진</li><li>가돌리늄 조영제 회피, 가능하면 비조영 MRI</li><li>출산 후 동적 영상으로 확진</li></ul>"}],
"faqs":[("혈관종이 있는데 임신해도 되나요?","대부분 안전. 10 cm 이상은 산과·외과 평가."),
("HCA 진단 받았는데 임신 계획 중이에요","5 cm 이상이면 임신 전 절제 권장. 5 cm 미만은 정기 영상 + 피임약 중단.")],
"refs":["EASL Clinical Practice Guidelines on the management of benign liver tumours. <em>J Hepatol</em> 2016."]},

{"slug":"간양성종양-경구피임약", "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"경구피임약과 간 양성종양", "h1":"경구피임약 사용 여성에서의 간 양성종양 평가",
"desc":"장기 경구피임약 사용과 HCA 위험 — 5년 이상 복용 시 위험 의미 있게 상승. 결절 발견 시 평가와 피임약 중단 결정.",
"keywords":"경구피임약, HCA, 호르몬",
"tags":[("경구피임약",),("HCA",)],
"tldr":"경구피임약(특히 5년 이상 장기 사용, 고용량 에스트로겐) 사용자에서 <strong>HCA(간세포 선종)</strong> 위험이 의미 있게 올라갑니다. 검진에서 간 결절이 발견된 경구피임약 사용 여성은 적극적 평가가 필요합니다. 진단 후에는 피임약 중단을 권하며, 일부 HCA는 중단만으로 크기가 줄거나 사라집니다.",
"sections":[
{"heading":"위험과 진단","html":"<ul><li>경구피임약 5년 이상 사용 — HCA 위험 약 10배 상승</li><li>고용량 에스트로겐 제제가 더 위험</li><li>최근 저용량 제제는 위험 일부 감소</li><li>검진에서 간 결절 발견 시 — 동적 CT 또는 EOB-MRI로 분류</li><li>FNH·HCA 감별이 가장 중요 (EOB 흡수가 결정적)</li></ul>"},
{"heading":"진단 후 — 피임약 중단","html":"<p>HCA로 진단되면 경구피임약 중단을 강하게 권합니다. 일부 환자에서 6~12개월 후 크기 감소·소실(특히 H-HCA, I-HCA). 다른 피임 방법(자궁내장치·구리·차단법 등)으로 전환.</p>"},
{"heading":"절제 적응증","html":"<ul><li>5 cm 이상 — 출혈·악성 변화 위험</li><li>남성 환자 — 거의 모든 경우 (남성 HCA는 악성 변화 위험 높음)</li><li>β-catenin 양성형 — 악성 변화 위험 높음</li><li>임신 계획 — 5 cm 미만이라도 검토</li><li>피임약 중단 후 12개월 후에도 안 줄어드는 경우</li></ul>"}],
"faqs":[("경구피임약을 끊으면 HCA가 사라지나요?","일부에서 줄거나 사라집니다(30~50%). 6~12개월 후 영상으로 평가."),
("다른 피임법으로 어떻게 전환하나요?","산부인과 상의. 자궁내장치·구리·차단법 등 안전한 대안 많음.")],
"refs":["Bioulac-Sage P, et al. Hepatocellular adenoma management and phenotypic classification. <em>Hepatology</em> 2009."]},

# Cases
{"slug":"NRH-진단", "is_case":True, "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"SLE 환자의 비간경변성 정맥류", "h1":"SLE + AZA 10년 — 정맥류 출혈로 발견된 NRH",
"desc":"SLE로 AZA 10년 복용 중인 환자에서 갑작스러운 정맥류 출혈. 영상에서 간경변 의심됐으나 조직에서 NRH 확진 사례.",
"keywords":"NRH, SLE, AZA, 정맥류",
"tags":[("NRH",),("SLE",),("AZA",)],
"case_intro":"42세 여성. SLE 15년, AZA 100 mg + 하이드록시클로로퀸 유지. 자가면역 안정. 갑작스러운 토혈로 응급실 — 식도정맥류 출혈. EGD에서 grade 3 정맥류, 결찰.",
"sections":[
{"heading":"평가","html":"<p>간 기능 정상 (ALT·AST 정상, 알부민 4.2, INR 1.0). 영상에서 간 표면 결절성 — 간경변 의심. 그러나 만성 간염 원인(바이러스·자가면역·MASLD·알코올) 모두 음성. 간 생검 — 결절 사이 압축 + 미세 재생 결절 + 간경변성 섬유성 띠 없음. <strong>NRH 진단</strong>.</p>"},
{"heading":"관리","html":"<p>NRH 원인 — 장기 AZA 의심. 류마티스내과와 상의 후 AZA → MMF 전환. 정맥류 결찰 반복 + 비선택적 베타차단제. 1년 후 정맥류 안정, NRH 진행 멈춤.</p>"},
],
"teaching":["<strong>비간경변성 문맥압 항진 — NRH 의심</strong>","<strong>장기 AZA·6-TG 사용 환자에서 발생 가능</strong>","<strong>SLE·RA 등 자가면역에서도 발생</strong>","<strong>약 변경이 진행 차단 가능</strong>","<strong>합병증 관리는 간경변과 비슷</strong>"]},

{"slug":"임신중-혈관종확대", "is_case":True, "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"임신 중 8 cm → 11 cm 혈관종", "h1":"임신 중 호르몬 영향으로 커진 거대 혈관종 — 산과·외과 협진",
"desc":"임신 전 8 cm 혈관종을 가진 30대 환자에서 임신 32주에 11 cm로 확대. 산과·외과 협진으로 안전한 분만 진행 사례.",
"keywords":"임신, 혈관종, 거대혈관종",
"tags":[("임신",),("혈관종",)],
"case_intro":"31세 여성, 임신 32주. 임신 전 우엽 8 cm 혈관종(임신 계획 시 평가, 추적). 이번 임신 32주 영상에서 11 cm로 확대. 우상복부 둔통 호소.",
"sections":[
{"heading":"평가","html":"<p>비조영 MRI — 전형적 혈관종 패턴, 출혈·파열 신호 없음. 산과 — 정상 분만 진행 가능 평가. 외과 — 분만 시 외상·파열 회피, 자연분만 시 압박 회피 자세 권유.</p>"},
{"heading":"분만과 산후","html":"<p>자연분만 안전 진행. 산후 6개월 — 혈관종 9 cm로 일부 호전(호르몬 영향 감소). 통증 호전. 추적 1년 후 8.5 cm 안정.</p>"},
],
"teaching":["<strong>임신 중 혈관종 약간 커질 수 있음 — 대부분 안전</strong>","<strong>10 cm 이상 거대 혈관종은 산과·외과 협진</strong>","<strong>가돌리늄 회피, 비조영 MRI 가능</strong>","<strong>출산 후 호르몬 정상화로 일부 호전 흔함</strong>"]},

{"slug":"bile-duct-hamartoma-우연발견", "is_case":True, "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"건강검진 다발성 결절 — 담관 과오종", "h1":"검진 CT에서 \"다발성 결절\" 보고 — MRI에서 담관 과오종 확진",
"desc":"건강검진 복부 CT에서 \"간 전체 다발성 결절, 전이암 감별 필요\" 보고. MRCP로 담관 과오종(Von Meyenburg complex)으로 확진 사례.",
"keywords":"담관과오종, Von Meyenburg, MRCP",
"tags":[("담관과오종",),("MRCP",)],
"case_intro":"55세 남성, 무증상. 건강검진 CT에서 \"간 양엽에 다발성 5~12 mm 결절, 전이 감별 필요\" 보고. 다른 원발암 의심 소견 없음. 종양표지자 정상.",
"sections":[
{"heading":"평가","html":"<p>EOB-MRI + MRCP — 결절들이 T2 매우 고신호, 일부에서 담관과 미세 연결. 담관 과오종(Von Meyenburg complex)으로 진단.</p>"},
{"heading":"안내","html":"<p>환자에게 \"양성·평생 안전\" 설명. 추적 종료. \"검진에서 또 다발성 결절이 보일 수 있는데, 이 진단입니다\"라는 안내 자료 제공.</p>"},
],
"teaching":["<strong>다발성 작은 결절 — 담관 과오종 항상 감별</strong>","<strong>CT보다 MRI가 결정적</strong>","<strong>대부분 평생 무증상·안전</strong>","<strong>환자에게 명확한 안내 — 향후 검진 혼란 예방</strong>"]},

{"slug":"경구피임약-HCA의심", "is_case":True, "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"경구피임약 8년 + 6 cm 결절 — HCA 절제", "h1":"경구피임약 8년 사용 + 6 cm HCA — 절제 결정",
"desc":"경구피임약 장기 사용 여성에서 검진 발견 6 cm HCA. 피임약 중단 6개월에도 크기 변화 없어 절제 결정 사례.",
"keywords":"경구피임약, HCA, 절제",
"tags":[("경구피임약",),("HCA",)],
"case_intro":"33세 여성. 경구피임약 8년 복용. 검진 영상에서 우엽 6 cm 결절. EOB-MRI에서 간담도기 흡수 약하고 일부 부분, 동맥기 균일 조영, capsule. HCA 강하게 의심.",
"sections":[
{"heading":"평가와 결정","html":"<p>6 cm — 출혈·악성 변화 위험 증가. 다학제적 논의 — (1) 피임약 중단 + 6개월 영상 추적, (2) 절제. 환자는 임신 계획 있어 절제 선호.</p>"},
{"heading":"진행","html":"<p>피임약 중단. 6개월 추적 — 6 cm로 변화 없음. 외과 협진 — 우엽 분절 절제. 병리 — Inflammatory subtype HCA, β-catenin 음성. R0 절제. 1년 후 임신 시도 시작.</p>"},
],
"teaching":["<strong>경구피임약 5년 이상 + HCA — 강한 연관</strong>","<strong>5 cm 이상은 절제 적응증</strong>","<strong>피임약 중단으로 일부 줄어들지만 모두는 아님</strong>","<strong>임신 계획 환자는 절제 우선 검토</strong>","<strong>아형 평가 (β-catenin)가 악성 변화 위험 결정</strong>"]},

{"slug":"focal-fat-sparing-PET", "is_case":True, "hub_path":BEN_HUB, "hub_label":BEN_LBL, "section":BEN_SEC,
"title":"지방간 환자의 PET 양성 부위 — Focal sparing", "h1":"PET-CT 양성 부위가 종양 의심됐으나 — Focal fat sparing",
"desc":"지방간 환자의 다른 암 추적 중 발견된 간 부위 FDG 섭취 증가. 종양 의심됐으나 MRI에서 focal fat sparing으로 확진 사례.",
"keywords":"focal sparing, PET, MRI",
"tags":[("focal sparing",),("PET",)],
"case_intro":"62세 남성, 지방간 + 폐암 수술 후 추적. PET-CT에서 간 S4에 FDG 섭취 약간 증가 부위 발견. 전이 의심.",
"sections":[
{"heading":"평가","html":"<p>EOB-MRI in-phase·out-of-phase — 그 부위가 지방 신호 적음(주변 지방간 배경에서 \"섬\"처럼). 동맥기 조영 패턴 정상. Focal fat sparing으로 진단.</p>"},
{"heading":"안내","html":"<p>전이 가능성 배제. 추가 추적은 일반 폐암 추적 일정 그대로. \"PET 양성이라도 항상 종양은 아니다\" 환자 안내.</p>"},
],
"teaching":["<strong>지방간 환자에서 focal sparing/deposition은 PET·CT 가양성 흔함</strong>","<strong>MRI in/out of phase가 결정적</strong>","<strong>전형적 위치(S4·담낭와 주변) 기억</strong>","<strong>다른 암 추적 시 가양성 평가에 시간·비용 소모 — 미리 인지하면 절감</strong>"]},
]

if __name__ == "__main__":
    write_pages(AIH + BEN)
