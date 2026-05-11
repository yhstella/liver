#!/usr/bin/env python3
"""Phase 1.2: 간경화 hub — 4 remaining topics + 5 cases."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gen_draft_pages import write_pages

HUB = "/간경화/"
HUB_LABEL = "간경화"
SECTION = "간경화"

SPECS = [
# Topic 2: 간경변-감염-SBP-예방
{
"slug": "간경변-감염-SBP-예방", "hub_path": HUB, "hub_label": HUB_LABEL, "section": SECTION,
"title": "자발성 세균성 복막염(SBP) 예방", "h1": "자발성 세균성 복막염(SBP) — 예방과 평생 관리",
"desc": "복수가 있는 간경변 환자의 흔하고 치명적 합병증인 자발성 세균성 복막염(SBP). 첫 발생 위험군과 평생 예방 항생제(norfloxacin·ciprofloxacin·trimethoprim-sulfamethoxazole) 사용.",
"keywords": "SBP, 자발성세균성복막염, 복수, 간경변, 항생제예방",
"tags": [("SBP",), ("복수",), ("간경변",), ("항생제예방",)],
"tldr": "<strong>자발성 세균성 복막염(SBP)</strong>은 복수가 있는 간경변 환자에서 발생하는 복강 내 감염으로, 사망률이 약 20~30%로 매우 높습니다. 일단 한 번 발생하면 1년 내 재발률이 약 70%에 달해 평생 예방 항생제가 표준입니다. 첫 SBP 환자, 단백 농도가 낮은 복수, 위장관 출혈 후 단기 예방이 3대 적응증입니다.",
"sections": [
{"heading":"무엇이고 왜 위험한가","html":"<p>간경변으로 복수가 차면 그 복수 안에 세균이 자라기 쉬운 환경이 만들어집니다. 다른 명확한 감염 원인(천공·농양 등) 없이 복수액에 세균이 증식하는 상태가 SBP입니다. 진단 기준은 복수액의 호중구 ≥ 250/mm³.</p><p>가장 무서운 점은 증상이 비특이적이라는 것입니다 — 발열·복통이 명확하지 않은 환자도 많고, 인지 변화·신기능 악화만 처음 신호로 올 수 있습니다. 그래서 비대상성 간경변 환자가 갑자기 상태가 나빠지면 복수액 천자가 1차 평가입니다.</p>"},
{"heading":"평생 예방이 필요한 그룹","html":"<ul><li><strong>SBP 기왕력</strong> — 1년 내 재발 70%. 평생 norfloxacin 400 mg/day 또는 ciprofloxacin 500 mg/day, trimethoprim-sulfamethoxazole 1정.</li><li><strong>복수 단백 ≤ 1.5 g/dL + 추가 위험 인자</strong>(혈청 Na ≤ 130, Cr ≥ 1.2, Child-Pugh ≥ 9, 빌리루빈 ≥ 3) — 1차 예방.</li><li><strong>위장관 출혈</strong> — 정맥류 출혈 시 7일간 ceftriaxone 또는 norfloxacin 단기 예방.</li></ul>"},
{"heading":"치료 시작 — 의심 즉시 광범위 항생제","html":"<p>SBP 의심이면 복수액 천자로 호중구 측정 + 배양 후 즉시 광범위 항생제 시작(결과 기다리지 않음). 표준은 cefotaxime 또는 ceftriaxone. 신기능 보호를 위해 알부민 1.5 g/kg(첫날) + 1 g/kg(3일째) 정맥 주입이 표준 — 알부민이 빠진 SBP 치료는 신부전·사망 위험이 의미 있게 큼.</p>"},
{"heading":"한국 진료 현장","html":"<ul><li>장기 norfloxacin 사용 중 내성 균주 발생이 점차 늘어 cephalosporin 내성 SBP도 보고됨. 반복 SBP에서는 균 배양·감수성 결과 따라 항생제 변경.</li><li>복수 천자는 진단·치료 모두에서 핵심이지만 환자가 거부하는 경우가 흔합니다. 「복수 있는 모든 입원 환자는 24시간 내 천자」가 가이드라인 권고임을 설명드립니다.</li><li>SBP 한 번 발생하면 간이식 평가 시작이 표준입니다 — 1년 사망률 60~70%로 자연 경과가 매우 나쁨.</li></ul>"},
],
"faqs":[
("SBP에 걸리면 항상 복통이 있나요?","아닙니다. 약 30%는 복통이 거의 없고 발열도 없습니다. 비특이적 인지 변화·신기능 악화·식욕 부진만 첫 신호일 수 있어 복수 있는 환자가 \"왠지 안 좋다\"는 변화가 있으면 복수 천자가 표준입니다."),
("평생 항생제를 먹는 게 안전한가요?","장기 norfloxacin 사용은 검증된 표준 치료이며 SBP 재발·사망을 의미 있게 줄입니다. 내성균·C. difficile 위험을 고려해 정기 추적과 다른 감염 의심 시 평가를 합니다. 자가 중단 위험이 크니 진료의와 상의 후 결정.") ,
("간이식을 받으면 항생제를 끊을 수 있나요?","네. 이식 후 복수가 사라지면 SBP 위험도 사라져 예방 항생제를 중단합니다. 다만 면역억제제 사용으로 다른 감염 위험은 새로 생깁니다."),
("SBP 한 번 걸렸으면 정말 모두 이식 평가를 하나요?","KASL·AASLD 모두 SBP 발생을 이식 평가 적응증으로 권고합니다. MELD 점수와 별개로 1년 사망률이 매우 높아 평가를 시작합니다."),
],
"refs":["Runyon BA. Management of adult patients with ascites due to cirrhosis: update 2012. <em>Hepatology</em> 2013.","Sort P, et al. Effect of intravenous albumin on renal impairment and mortality in patients with cirrhosis and SBP. <em>NEJM</em> 1999.","EASL Clinical Practice Guidelines for decompensated cirrhosis. <em>J Hepatol</em> 2018."],
},
# Topic 3: 간경변-피로감-증상관리
{
"slug": "간경변-피로감-증상관리", "hub_path": HUB, "hub_label": HUB_LABEL, "section": SECTION,
"title": "간경변 환자의 만성 피로감", "h1": "간경변 환자의 만성 피로감 — 원인과 대처",
"desc": "간경변 환자의 약 60-80%가 호소하는 피로감. 빈혈·근감소증·간성혼수 잠재·우울·갑상선 기능·수면 무호흡 등 흔한 원인 평가와 대처.",
"keywords": "피로, 간경변, 근감소증, 수면, 우울",
"tags":[("피로",),("간경변",),("근감소증",),("수면",)],
"tldr":"피로감은 간경변 환자에게 가장 흔한 증상 중 하나로, 60~80%가 호소합니다. 단순히 \"간 때문에 피곤하다\"로 끝나는 것이 아니라 빈혈, 근감소증, 우울·불안, 수면 무호흡, 갑상선 기능 저하, 잠재성 간성혼수처럼 다룰 수 있는 원인이 많습니다. 환자분의 \"피곤해요\" 호소를 빠르게 일축하지 말고 한 번은 원인을 훑어보는 것이 중요합니다.",
"sections":[
{"heading":"피로감의 흔한 원인 — 외래에서 체크하는 순서","html":"<ol><li><strong>빈혈</strong> — Hb, ferritin, B12. 위장관 출혈·만성 염증·비장 비대 모두 빈혈 원인.</li><li><strong>잠재성 간성혼수</strong> — 명확한 인지 변화가 없는 환자에서도 minimal hepatic encephalopathy로 피로·집중력 저하 가능. 암모니아·신경심리 검사.</li><li><strong>근감소증(sarcopenia)</strong> — 근육량 감소로 일상 활동 피로 가산. 운동·단백 섭취 평가.</li><li><strong>우울·불안</strong> — 만성 질환에서 매우 흔함. PHQ-9 같은 짧은 평가.</li><li><strong>수면 무호흡·불면</strong> — 간경변에서 수면 질 저하 흔함. 코골이·아침 두통.</li><li><strong>갑상선 기능</strong> — TSH 한 번은 측정 가치 있음.</li><li><strong>약물 부작용</strong> — 베타차단제·이뇨제·수면제 등.</li></ol>"},
{"heading":"검사 평가","html":"<p>한 번에 챙길 검사 — CBC, ferritin, B12, folate, TSH, electrolytes, 알부민·PT·INR, 암모니아(임상 의심 시). 영상으로 비장 크기·복수 평가. 필요 시 신경심리 검사(PHES, 한국에서 EncephalApp Stroop·MoCA로 일부 대체).</p>"},
{"heading":"대처","html":"<ul><li><strong>가역 원인 교정</strong> — 빈혈 교정(원인 별), TSH 이상 시 갑상선 보충, 우울증 평가·치료.</li><li><strong>운동·재활</strong> — 매주 5회 30분 가벼운 유산소 + 주 2~3회 저항 운동. 근감소증 동반 환자에서 특히 효과.</li><li><strong>영양</strong> — 단백 1.2~1.5 g/kg/일, 야식으로 야간 단식 단축.</li><li><strong>잠재성 간성혼수 의심 시</strong> — 락툴로오스·rifaximin 시도 후 증상 변화 평가.</li><li><strong>수면 위생</strong> — 일정한 수면 시간, 카페인·알코올 제한. 코골이·무호흡 의심 시 수면다원검사.</li></ul>"},
],
"faqs":[
("\"간이 안 좋으니까 피곤한 거다\"로 받아들여야 하나요?","꼭 그렇지 않습니다. 빈혈·갑상선·우울·수면 무호흡처럼 다룰 수 있는 원인이 환자의 30~50%에서 발견됩니다. 한 번은 평가해 볼 가치가 있습니다."),
("피곤한데 운동하기가 힘듭니다","처음에는 짧게(10분 산책)부터 시작합니다. 운동이 오히려 피로를 완화한다는 연구들이 있어요. 강도보다 꾸준함이 핵심입니다."),
("커피는 마셔도 되나요?","간경변 환자에서도 적당량 커피는 안전하고 일부 연구는 간 보호 효과까지 보고합니다. 다만 카페인이 수면에 영향을 주면 오후 이후 피하시는 게 좋습니다."),
("영양제로 도움이 될까요?","빈혈·B12·비타민 D 부족이 확인되면 보충이 도움 됩니다. 일률적인 \"간 영양제\"는 효과 근거가 약하고 일부는 간 손상 위험이 있어 진료의와 상의 후 결정하세요."),
],
"refs":["Newton JL, et al. Fatigue and autonomic dysfunction in cirrhosis. <em>Liver Int</em> 2008.","Bajaj JS. Minimal hepatic encephalopathy: a vehicle for accidents and traffic violations. <em>Am J Gastroenterol</em> 2007.","Tandon P, et al. Sarcopenia and frailty in decompensated cirrhosis. <em>J Hepatol</em> 2021."],
},
# Topic 4: 간경변-수면-가려움증
{
"slug": "간경변-수면-가려움증", "hub_path": HUB, "hub_label": HUB_LABEL, "section": SECTION,
"title": "간경변 환자의 수면 장애와 가려움증", "h1": "간경변 환자의 수면 장애와 가려움증 — 두 가지 흔한 비특이 증상",
"desc": "간경변 환자가 자주 호소하는 두 가지 비특이 증상 — 수면 장애와 가려움증. 원인 평가와 단계별 대처(수면 위생, rifaximin, cholestyramine, naltrexone, sertraline).",
"keywords":"수면장애, 가려움증, pruritus, 간경변, rifaximin",
"tags":[("수면장애",),("가려움증",),("간경변",)],
"tldr":"환자분들이 \"간 때문에 잠을 못 자고 가려워요\"라고 하시면 두 가지 흔한 합병증을 떠올립니다. <strong>수면 장애</strong>는 잠재성 간성혼수, 우울, 수면 무호흡과 연결되어 있고, <strong>가려움증(pruritus)</strong>은 담즙정체 또는 요독 환경에서 발생합니다. 두 증상 모두 단계적 평가와 약물 옵션이 있어 \"어쩔 수 없다\"로 끝낼 일이 아닙니다.",
"sections":[
{"heading":"수면 장애 — 원인과 평가","html":"<p>간경변 환자의 약 50~70%가 수면 장애를 호소합니다. 가장 흔한 패턴은 <strong>야간 각성 증가 + 낮 졸음</strong>으로 정상적인 일주기 리듬이 깨진 양상입니다.</p><ul><li><strong>잠재성 간성혼수</strong> — 멜라토닌 대사 변화로 일주기 리듬 교란. 락툴로오스·rifaximin 시도가 도움될 수 있음.</li><li><strong>수면 무호흡</strong> — 비만 동반 시 특히. 수면다원검사 검토.</li><li><strong>야간 가려움증</strong> — 잠을 깨우는 원인. 가려움증 자체 치료가 수면 회복으로 이어짐.</li><li><strong>야간 빈뇨</strong> — 이뇨제 야간 복용 패턴 조정. 가능하면 오후에 마지막 복용.</li><li><strong>우울·불안</strong> — 일찍 깸·중간 각성 패턴.</li></ul>"},
{"heading":"가려움증(Pruritus) — 단계적 약물","html":"<p>간경변·담즙정체 환자의 가려움증은 일반 항히스타민제(zyrtec 등)에 잘 듣지 않습니다. 단계적 접근:</p><ol><li><strong>피부 보습·미온수 목욕</strong> — 비누 줄이고 보습제. 자극 옷감 회피.</li><li><strong>Cholestyramine</strong> — 담즙산 흡착. PBC·PSC 가려움증 1차. 다른 약과 4시간 간격 복용.</li><li><strong>Rifaximin</strong> — 일부 보고에서 효과. 동시에 잠재성 간성혼수에도 효과.</li><li><strong>Sertraline (SSRI)</strong> — 75~100 mg/일. 항우울·항가려움 동시 효과.</li><li><strong>Naltrexone</strong> — 오피오이드 길항. 효과적이나 금단 유사 증상으로 시작 시 신중.</li><li><strong>Rifampin</strong> — 일부 효과. 간 효소 영향 모니터.</li></ol>"},
{"heading":"수면제 사용의 함정","html":"<p>벤조디아제핀(zolpidem 포함 일부)은 간경변에서 간성혼수 유발 위험이 있어 사용에 신중합니다. 비대상성 환자에서는 일반 수면제보다 가려움증·수면 무호흡 같은 근본 원인 치료가 우선입니다. 수면 위생·짧은 낮잠 회피·일정한 기상 시간이 약보다 먼저 시도하는 단계입니다.</p>"},
],
"faqs":[
("가려움증이 너무 심해 잠을 못 자요","cholestyramine 또는 sertraline부터 시도 가능합니다. 동시에 보습·미온수 목욕 같은 피부 관리. 가려움증은 단계적으로 약을 바꾸며 효과 보는 환자가 많아 한 번에 포기하지 마세요."),
("멜라토닌은 도움이 되나요?","일부 환자에서 수면 시작·일주기 리듬에 도움이 됩니다. 간경변에서 안전성 자료는 제한적이지만 단기 사용은 일반적으로 안전합니다. 진료의와 상의 후 시작하세요."),
("수면제 처방 받아도 되나요?","비대상성 환자에서는 신중해야 합니다. 벤조디아제핀은 간성혼수 위험이 있어 피하는 게 좋고, 짧은 작용 비-벤조 수면제도 최소 용량·단기로만 시도합니다. 우선 가려움증·잠재성 간성혼수 같은 원인 치료가 우선입니다."),
("가려움증은 간 이식하면 사라지나요?","대부분 사라집니다. 담즙정체가 해결되면 가려움증은 며칠~몇 주 안에 호전됩니다. 이식 후 면역억제제로 인한 새로운 피부 증상은 별도 평가."),
],
"refs":["European Association for the Study of the Liver. EASL Clinical Practice Guidelines: management of cholestatic liver diseases. <em>J Hepatol</em> 2009/2017.","Mayo MJ, et al. Sertraline as a first-line treatment for cholestatic pruritus. <em>Hepatology</em> 2007.","Bajaj JS, et al. Rifaximin in chronic hepatic encephalopathy. <em>NEJM</em> 2010."],
},
# Topic 5: 간경변-여행-항공-주의
{
"slug": "간경변-여행-항공-주의", "hub_path": HUB, "hub_label": HUB_LABEL, "section": SECTION,
"title": "간경변 환자의 여행과 항공기 탑승", "h1": "간경변 환자의 여행과 항공기 탑승 — 안전한 준비",
"desc": "비대상성 간경변 환자도 안전하게 여행을 다닐 수 있습니다. 출발 전 점검, 비행 중 주의, 예방접종, 응급 시 연락 방법을 정리합니다.",
"keywords":"여행, 항공, 간경변, 예방접종, 응급",
"tags":[("여행",),("항공",),("간경변",),("예방접종",)],
"tldr":"간경변이 있다고 해서 여행이 금지되는 건 아닙니다. 다만 비대상성(복수·간성혼수·정맥류 출혈 이력)인 경우 일정과 준비가 더 중요합니다. 출발 전 예방접종, 약 처방 준비, 여행지 의료기관 정보, 비행 중 수분·움직임 관리, 응급 시 연락 방법을 미리 정리해 두면 대부분 안전하게 다닐 수 있습니다.",
"sections":[
{"heading":"출발 전 점검 (1~2주 전)","html":"<ul><li><strong>약 처방 — 여행 기간의 1.5배</strong> 복용분과 분실 대비분. 항바이러스제·이뇨제·락툴로오스·항생제 예방.</li><li><strong>영문 진단서·약 목록</strong> — 세관·응급 상황 대비.</li><li><strong>예방접종</strong> — A형간염·인플루엔자·폐렴구균 기본. 여행지에 따라 황열·장티푸스 등 추가.</li><li><strong>치과 점검</strong> — 비대상성에서는 치과 응급 처치가 어려우므로 사전 검진.</li><li><strong>여행자 보험</strong> — 만성 질환 보장 여부 명시. 의료 후송(medevac) 옵션 검토.</li></ul>"},
{"heading":"비행 중 주의","html":"<ul><li><strong>탈수 회피</strong> — 물 자주 마시고 알코올·과당 음료 피하기.</li><li><strong>2시간마다 일어나서 움직이기</strong> — 정맥혈전 위험 감소.</li><li><strong>압박 스타킹</strong> — 정맥류·복수 있는 환자는 정맥혈전 위험이 높아 고려.</li><li><strong>이뇨제·기타 약은 정시 복용</strong> — 시차에도 약 간격은 가능한 유지.</li><li><strong>혈관압박·복부 압박 피하기</strong> — 너무 꽉 끼는 옷·벨트.</li></ul>"},
{"heading":"비대상성 환자의 추가 고려","html":"<p>복수·간성혼수 이력·정맥류 출혈 이력이 있는 환자는 출발 전 다학제 평가가 안전합니다.</p><ul><li><strong>복수가 빠르게 늘고 있다면 출발 연기</strong> — 비행 중 응급 천자 불가능.</li><li><strong>최근 정맥류 출혈 이력</strong> — 3개월 이내라면 장거리 여행 피하시고 진료의와 상의.</li><li><strong>간성혼수 이력</strong> — 락툴로오스·rifaximin 충분히 가져가고 가족·동행자가 인지 변화 신호를 알도록.</li><li><strong>응급 의료기관 위치</strong> — 출발 전 여행지 의료 인프라 확인.</li></ul>"},
{"heading":"한국 진료 현장에서 자주 받는 질문","html":"<ul><li><strong>\"고도가 높으면 간이 더 나빠지나요?\"</strong> — 일반적인 항공기 객실 기압은 약 2,400 m 산속과 비슷. 간경변 자체로 객실 환경이 의미 있게 악화시키지는 않습니다. 다만 산소 분압이 약간 낮아 간폐증후군이 있는 환자는 산소 사용을 고려.</li><li><strong>\"백신 부작용이 더 클까요?\"</strong> — 비대상성에서 면역 반응이 약해 부작용 자체는 일반인과 비슷하거나 적습니다. 다만 백신 효과도 약해 일부에서 항체가 잘 안 생깁니다.</li><li><strong>\"여행 중 응급 상황 대비\"</strong> — 약 목록·영문 진단서·복용 중 항바이러스제 이름을 종이에도 준비. 가족·동행자에게 응급 신호 교육.</li></ul>"},
],
"faqs":[
("복수가 있어도 비행기 탈 수 있나요?","대상성에서 잘 조절된 복수라면 가능합니다. 빠르게 차오르는 중이거나 호흡곤란 있는 비대상성 복수에서는 출발 전 천자·평가가 필요합니다."),
("정맥류 결찰 후 얼마 만에 여행 가능한가요?","최근 결찰 시술이라면 2~3주 회복 기간을 두고 첫 추적 내시경에서 안정 확인 후 출발이 안전합니다. 첫 출혈 이력은 3~6개월 후가 일반적입니다."),
("항공기에서 약 시간이 시차로 어긋나면 어떻게 하나요?","항바이러스제처럼 매일 한 번 복용하는 약은 시차에 맞춰 점진 조정 가능합니다. 12시간 이상 시차는 1~2일에 걸쳐 1~2시간씩 옮기는 게 안전합니다."),
("여행자 보험 가입 시 간경변을 어떻게 신고하나요?","사실대로 신고하세요. 일부 보험은 만성 질환 보장에 제한이 있지만, 신고하지 않으면 사후 청구가 거절될 수 있습니다. 의료 후송(medevac) 옵션을 별도로 추가하는 것을 권합니다."),
],
"refs":["AASLD/IDSA Travel medicine for patients with chronic liver disease.","ICTR practical recommendations for travel in chronic liver disease.","대한간학회 환자 교육 자료."],
},
# === Cases 5 ===
{
"slug":"혈소판저하-romiplostim", "is_case":True, "hub_path":HUB, "hub_label":HUB_LABEL, "section":SECTION,
"title":"혈소판 25,000에서 치과 발치 — TPO 작용제 사용", "h1":"혈소판 25,000에서의 응급 치과 발치 — TPO 작용제로 안전 마진 확보",
"desc":"비대상성 간경변 환자에서 혈소판 25,000으로 인한 치과 발치 지연. 시술 전 avatrombopag 5일로 89,000까지 상승 후 안전 시행한 사례.",
"keywords":"혈소판감소, TPO작용제, avatrombopag, 치과",
"tags":[("혈소판감소",),("TPO작용제",),("치과",)],
"case_intro":"61세 남성. 알코올성 간경변(Child-Pugh B7) 환자로 우측 어금니 충치로 인한 발치가 필요한 상황. 정기 검사에서 혈소판 25,000/μL로 확인되어 치과에서 발치 거부. 응고 검사 PT INR 1.6, 알부민 3.1.",
"sections":[
{"heading":"평가와 결정","html":"<p>다학제 협의: (1) 발치 자체는 의학적으로 필요(통증·감염 위험), (2) 25,000은 자발성 출혈 임계 가까움, (3) 일반 혈소판 수혈은 일시적·반복 시 동종면역. <strong>Avatrombopag</strong>(경구 TPO 작용제) 시술 5일 전부터 시작.</p>"},
{"heading":"경과","html":"<p>Avatrombopag 60 mg/일 × 5일. 시술 당일 혈소판 89,000으로 상승. 치과에서 안전하게 발치 시행, 시술 후 출혈 없음. 시술 후 14일 째 혈소판 32,000으로 다시 감소(예상된 경과).</p>"},
],
"teaching":[
"<strong>혈소판 50,000 미만에서 시술 전 단기 TPO 작용제 사용이 한국 보험 적응증</strong>. 만성 사용이 아니라 시술 전 5~7일 시점에 시작.",
"<strong>혈소판 수혈 대비 장점</strong> — 동종면역 위험 없음, 반복 가능, 외래 복용 편리.",
"<strong>주의사항</strong> — 시작 전 비장 혈전·다른 혈전 위험 평가. 정기 혈소판 추적 필수.",
"<strong>치과 시술도 출혈 위험 시술</strong>. 발치·임플란트·치주 수술은 50,000 이상이 일반적 기준.",
],
},
{
"slug":"반복SBP-예방요법", "is_case":True, "hub_path":HUB, "hub_label":HUB_LABEL, "section":SECTION,
"title":"반복 SBP — 평생 예방 항생제 시작", "h1":"6개월에 두 번째 SBP — 평생 예방 항생제와 이식 평가",
"desc":"비대상성 간경변 환자의 두 번째 자발성 세균성 복막염. Norfloxacin 평생 예방 시작과 동시에 간이식 평가 진행.",
"keywords":"SBP, 예방항생제, norfloxacin, 간이식",
"tags":[("SBP",),("예방항생제",),("간이식",)],
"case_intro":"68세 여성. C형간염 간경변(Child-Pugh B9) 환자로 복수 동반. 6개월 전 첫 SBP로 입원 후 회복. 이번 발열·인지 변화로 다시 응급실 내원. 복수 천자에서 호중구 480, 배양 E.coli.",
"sections":[
{"heading":"치료","html":"<p>입원 즉시 ceftriaxone + 알부민 1.5 g/kg 첫날 + 1 g/kg 3일째. 5일째 임상 호전. 복수 천자 호중구 120으로 감소 확인 후 항생제 총 10일 완료. 퇴원.</p>"},
{"heading":"퇴원 후 — 평생 예방과 이식 평가","html":"<p>Norfloxacin 400 mg/일 평생 처방. 동시에 간이식 평가 진행 — 검사 시작 8주에 완료, MELD 18, KONOS 등록.</p>"},
],
"teaching":[
"<strong>두 번째 SBP는 평생 예방 항생제의 강한 적응증</strong>. 재발 시 사망률 30~50%.",
"<strong>SBP는 그 자체로 이식 평가 적응증</strong>. MELD와 무관하게 평가 시작이 표준.",
"<strong>알부민 보충이 신부전·사망 줄임</strong> — 첫날 1.5 g/kg + 3일째 1 g/kg.",
"<strong>균 감수성에 따라 항생제 변경 가능</strong> — quinolone 내성 균주가 늘어 cephalosporin·carbapenem 사용 케이스가 증가.",
],
},
{
"slug":"저나트륨혈증-tolvaptan", "is_case":True, "hub_path":HUB, "hub_label":HUB_LABEL, "section":SECTION,
"title":"Na 125 저나트륨혈증과 tolvaptan", "h1":"비대상성 간경변에서 저나트륨혈증 124 — Tolvaptan으로 정상화",
"desc":"이뇨제 조정에도 저나트륨혈증 124가 지속되는 비대상성 간경변 환자. Tolvaptan 시작 후 안전하게 132로 상승한 사례.",
"keywords":"저나트륨혈증, tolvaptan, 복수, 간경변",
"tags":[("저나트륨혈증",),("tolvaptan",),("복수",)],
"case_intro":"72세 남성. 비대상성 간경변, 복수로 furosemide 40 mg + spironolactone 100 mg 복용 중. 정기 검사에서 Na 124, 두통·식욕 부진. 수분 제한 1 L/일 시도했으나 변화 없음.",
"sections":[
{"heading":"평가와 결정","html":"<p>희석성 저나트륨혈증(dilutional hyponatremia) — 자유수 보유 과다. 수분 제한·이뇨제 조정으로 호전 없을 때 <strong>tolvaptan</strong>(vaptan, V2 수용체 길항제) 검토. 한국 보험 적용은 SIADH·심부전 적응증이 우선, 간경변에서는 의료기관 판단으로 사용 가능.</p>"},
{"heading":"경과","html":"<p>Tolvaptan 7.5 mg/일 시작. 입원 환경에서 첫 24시간 Na 점진 상승(124 → 128), 너무 빠른 상승 회피 위해 면밀 모니터. 4일째 132 도달, 두통·식욕 호전. 외래에서 3주 더 지속 후 Na 안정 유지되며 중단 시도.</p>"},
],
"teaching":[
"<strong>저나트륨혈증은 단순 \"수분 제한\"만으로는 안 풀리는 경우가 많음</strong>. Tolvaptan은 자유수 배설을 늘려 효과적.",
"<strong>너무 빠른 교정은 osmotic demyelination syndrome 위험</strong>. 첫 24시간 8 mEq 이내 상승이 안전 마진.",
"<strong>Tolvaptan은 입원 환경에서 시작·monitor</strong>. 외래에서 자가 시작은 권장 안 됨.",
"<strong>간경변에서 저나트륨혈증은 사망 예측 인자</strong>. MELD-Na로 이식 우선순위 평가."],
},
{
"slug":"Sarcopenia-운동개선", "is_case":True, "hub_path":HUB, "hub_label":HUB_LABEL, "section":SECTION,
"title":"근감소증과 운동·영양 개입 — 12개월 추적", "h1":"간경변 + 근감소증 환자의 운동·영양 개입 12개월 — Frailty 호전",
"desc":"비대상성 간경변 + sarcopenia 진단된 환자의 12개월 운동·단백 보충 프로그램. Frailty score 호전과 일상 기능 개선 사례.",
"keywords":"근감소증, sarcopenia, 운동, 영양",
"tags":[("근감소증",),("운동",),("영양",)],
"case_intro":"66세 여성. NASH 기반 비대상성 간경변(Child-Pugh A6, MELD 14). 정기 평가에서 근육량 감소(L3 CT의 SMI 32 cm²/m²) + 근력 저하(악력 13 kg). Liver Frailty Index 4.6.",
"sections":[
{"heading":"개입","html":"<p>물리치료사와 영양사 협진:</p><ul><li>주 3회 저항 운동 (다리·복근·등 위주, 가벼운 무게)</li><li>주 5회 가벼운 유산소 30분</li><li>단백 섭취 1.5 g/kg/일 목표, 식사 5회 분산 + 야간 단백 간식</li><li>BCAA 보충제 식간 (1일 12 g)</li></ul>"},
{"heading":"6개월·12개월 결과","html":"<p>6개월 — 악력 13 → 17 kg, Liver Frailty Index 4.6 → 3.8. SMI 약간 개선. 일상 활동(계단 오르기, 장보기)이 의미 있게 편해짐.</p><p>12개월 — 악력 19 kg 유지, Liver Frailty Index 3.4. MELD 변화 없음(14). 환자 본인 \"피곤함이 줄었다\"는 주관 보고.</p>"},
],
"teaching":[
"<strong>운동·영양 개입은 간경변에서 효과 있음</strong>. \"간이 안 좋아서 운동 못한다\"는 옛 통념과 달리 적극적 프로그램이 frailty·이식 후 결과 모두 개선.",
"<strong>단백 1.2~1.5 g/kg가 표준</strong>. 옛 \"단백 제한\" 권고는 폐기.",
"<strong>야간 단백 간식이 근육 분해 줄임</strong>. 우유·요거트·견과류로 200~250 kcal.",
"<strong>BCAA 보충은 식이 단백 부족한 환자에서 효과</strong>. 일률적 권고는 아니나 케이스별 검토.",
"<strong>운동을 못하는 정도라면 침상 저항 운동부터</strong>. \"걸을 수 없으니 운동 못한다\"는 환자도 누워서 가능한 동작이 있음.",
],
},
{
"slug":"Recompensation-바이러스억제후", "is_case":True, "hub_path":HUB, "hub_label":HUB_LABEL, "section":SECTION,
"title":"비대상성 → 재대상화 — B형간염 항바이러스 3년 후", "h1":"비대상성 간경변 환자의 재대상화 — Entecavir 3년 후 Child-Pugh 회복",
"desc":"Child-Pugh B9 비대상성 환자에서 entecavir로 HBV DNA 완전 억제 3년 후 임상적 재대상화 (Child-Pugh A5) 달성. Baveno VII 정의 충족 사례.",
"keywords":"재대상화, recompensation, B형간염, entecavir",
"tags":[("재대상화",),("B형간염",),("entecavir",)],
"case_intro":"55세 남성. 만성 B형간염 + 비대상성 간경변(Child-Pugh B9, MELD 16)으로 진단. 복수·식도정맥류 결찰 이력. Entecavir 0.5 mg 시작.",
"sections":[
{"heading":"치료 경과","html":"<p>Entecavir 시작 후:</p><ul><li>3개월 — HBV DNA log 6 → 2.5 감소, ALT 정상화</li><li>1년 — HBV DNA 검출 한계 이하, 복수 호전, 이뇨제 감량</li><li>2년 — 정맥류 추적 EGD에서 정맥류 안정, Child-Pugh B7</li><li>3년 — Child-Pugh A5, MELD 9, 복수·정맥류 출혈 1년 이상 재발 없음, 알부민·INR·빌리루빈 모두 호전. 영상에서 비장 비대 일부 호전, Fibroscan 38 → 21 kPa.</li></ul>"},
{"heading":"Baveno VII 재대상화 기준 충족","html":"<ul><li>원인 질환 효과적 치료 (HBV DNA 억제) ✓</li><li>합병증 1년 이상 재발 없음 ✓</li><li>간 기능 지속적 개선 ✓</li></ul><p>임상적으로 재대상화로 분류. 다만 간경변 자체가 사라진 것은 아니므로 6개월 간암 검진은 평생 유지.</p>"},
],
"teaching":[
"<strong>비대상성 = 영구 불가역 아님</strong>. 원인 치료로 일부 환자가 재대상화 도달.",
"<strong>Baveno VII이 명확한 정의를 제시</strong> — 원인 치료 + 합병증 1년 무발생 + 간 기능 개선.",
"<strong>B형간염 환자에서 가장 흔한 패턴</strong>. 알코올성에서는 1년 이상 금주가 비슷한 효과.",
"<strong>재대상화 후에도 정기 추적·간암 검진 유지</strong>. 간경변 자체가 사라진 것은 아님.",
"<strong>일부 환자는 이식 대기 명단에서 제외(delisting)도 가능</strong>. 다학제 평가로 결정.",
],
},
]

if __name__ == "__main__":
    write_pages(SPECS)
