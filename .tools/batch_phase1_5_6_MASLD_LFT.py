#!/usr/bin/env python3
"""Phase 1.5+1.6: 지방간 + 간수치 — 5+5 each = 20 pages."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from gen_draft_pages import write_pages

# === 지방간 ===
MAS_HUB, MAS_LBL, MAS_SEC = "/지방간/", "지방간", "지방간"

MASLD = [
{"slug":"지방간-소아청소년-MASLD", "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"소아·청소년 지방간(MASLD)", "h1":"소아·청소년 MASLD — 한국에서 빠르게 늘고 있는 진단",
"desc":"한국 소아·청소년의 비만 증가와 함께 늘고 있는 MASLD. 진단 기준, 생활습관 개입, 약물 옵션, 청소년기 추적의 중요성.",
"keywords":"소아 MASLD, 청소년 지방간, 비만, 생활습관",
"tags":[("소아 MASLD",),("청소년",),("비만",)],
"tldr":"한국 소아·청소년의 약 10~15%가 영상 또는 검사로 지방간 소견을 보입니다. 비만 + 식이·운동 부족이 가장 큰 원인이며, MASLD 진단 후 청소년기를 거치며 성인 간경변·간암으로 진행할 수 있어 조기 개입이 중요합니다. 첫 단계는 생활습관 — 체중 5~10% 감량 + 식이 + 운동. 약물(메트포민·비타민 E 일부)은 보조적입니다.",
"sections":[
{"heading":"진단 기준","html":"<ul><li>비만·과체중 + 영상에서 지방간 + ALT 상승</li><li>다른 간 질환 배제 (B형/C형, 자가면역, 윌슨, AAT 결핍)</li><li>NASPGHAN 기준 — ALT 상한이 성인보다 낮음(남아 26, 여아 22 U/L)</li><li>섬유화 평가 — Fibroscan, FIB-4(소아 검증 제한적)</li></ul>"},
{"heading":"치료의 핵심 — 생활습관","html":"<ul><li><strong>체중 5~10% 감량</strong> — 가장 강력한 개입. 간 지방·ALT 의미 있게 호전.</li><li>식이 — 가당 음료·과당 제한, 지중해식 패턴.</li><li>운동 — 주 5회 30분 이상.</li><li>가족 함께 — 청소년 혼자 식이 바꾸기 어려움.</li><li>학교·심리 지원 — 비만 관련 sigma 관리.</li></ul>"},
{"heading":"약물 — 일부 상황","html":"<ul><li>비타민 E — 비당뇨·고섬유화 청소년 일부에서 검토.</li><li>메트포민 — 인슐린 저항성 동반 시 (당뇨 전단계·당뇨).</li><li>GLP-1 작용제 — 12세 이상 비만 적응증으로 일부 도입.</li><li>resmetirom — 성인 적응증, 소아 자료 부족.</li></ul>"},
],
"faqs":[("소아 지방간은 어른 되면 사라지나요?","생활습관 개선 없이는 지속 또는 악화. 청소년기 개입이 평생 간 건강에 영향."),
("지방간이라고 들었는데 운동만 하면 되나요?","체중 감량이 가장 중요. 식이 + 운동을 함께. 가족 단위 개입이 효과적.")],
"refs":["NASPGHAN MASLD guidelines pediatric.","KASL Korean pediatric NAFLD guidelines."]},

{"slug":"지방간-수면무호흡-OSA", "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"수면 무호흡과 지방간", "h1":"수면 무호흡(OSA)과 지방간 — 양방향 악화의 고리",
"desc":"폐쇄성 수면 무호흡(OSA)이 지방간을 악화시키고, 지방간 동반 비만이 OSA를 악화시키는 양방향 관계. CPAP·체중 감량의 효과.",
"keywords":"수면무호흡, OSA, CPAP, 지방간",
"tags":[("수면무호흡",),("OSA",),("CPAP",)],
"tldr":"폐쇄성 수면 무호흡(OSA)과 지방간은 함께 가는 경우가 많습니다. 야간 저산소증 + 산화 스트레스 + 인슐린 저항성 가산으로 간섬유화가 빠르게 진행할 수 있습니다. 지방간 환자 중 약 30~40%에서 OSA 동반. CPAP 치료는 OSA 자체뿐 아니라 간 효소·간 지방에도 부분적 호전 효과가 보고됩니다.",
"sections":[
{"heading":"OSA가 지방간을 악화시키는 메커니즘","html":"<ul><li>야간 간헐적 저산소 → 산화 스트레스</li><li>교감신경 항진 → 인슐린 저항성</li><li>전신 염증 → 간내 염증</li><li>HIF-1α 활성화 → 간 섬유화</li></ul>"},
{"heading":"진단 — 누구를 의심하나","html":"<ul><li>코골이·낮 졸음·아침 두통</li><li>비만 + 큰 목둘레</li><li>고혈압·당뇨 동반</li><li>STOP-BANG 설문지 양성</li><li>수면다원검사 또는 가정용 수면 검사</li></ul>"},
{"heading":"치료 — CPAP과 체중 감량","html":"<ul><li>CPAP — OSA 1차 치료. 간 효소도 일부 호전 보고.</li><li>체중 감량 — OSA·지방간 동시 개선.</li><li>구강 내 장치·수술 — 일부.</li><li>약물(GLP-1 작용제) — 비만·당뇨 동반 시 양쪽 호전.</li></ul>"},
],
"faqs":[("코를 골면 무조건 OSA인가요?","아닙니다. 코골이는 OSA의 단서일 수는 있어도 단독 진단 아님. 낮 졸음·고혈압 등 함께 평가."),
("CPAP을 쓰면 간 수치가 좋아지나요?","일부 환자에서 ALT·간 지방 호전 보고. 다만 체중 감량과 함께해야 효과 큼.")],
"refs":["Mesarwi OA, et al. Sleep disordered breathing and NAFLD. <em>Hepatology</em> 2019."]},

{"slug":"지방간-MetALD", "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"MetALD — 대사 + 알코올 동반 지방간", "h1":"MetALD — 대사 위험과 적당량 음주가 만나는 지방간",
"desc":"2023년 새 명명에서 도입된 MetALD. 대사 위험(비만·당뇨) + 적당량 음주의 동반. 두 원인 동시 관리.",
"keywords":"MetALD, 알코올, MASLD, 대사",
"tags":[("MetALD",),("알코올",),("MASLD",)],
"tldr":"<strong>MetALD</strong>는 2023년 MASLD 새 명명에서 도입된 카테고리로, <strong>대사 위험(비만·당뇨·고지혈증·고혈압) + 적당량 음주</strong>가 동반된 지방간을 가리킵니다. 남성 주 140~350 g, 여성 70~210 g 알코올이 기준. MASLD 표준 관리 + 음주 절제·중단을 양쪽 모두 적용해야 진행을 늦출 수 있습니다.",
"sections":[
{"heading":"왜 별도 카테고리가 필요했나","html":"<p>예전 NAFLD 정의에서는 \"의미 있는 알코올\"이 있으면 NAFLD에서 제외되어 ALD로 분류됐습니다. 그런데 실제로는 비만·당뇨 + 적당량 음주가 함께 있는 환자가 많고, 두 원인이 가산적으로 작용해 진행을 빠르게 합니다. MetALD는 이런 환자를 별도로 분류해 두 원인을 모두 관리하자는 개념입니다.</p>"},
{"heading":"진단","html":"<ul><li>지방간 영상 또는 조직 소견</li><li>대사 위험 인자 최소 1개 (비만·당뇨·고혈압·고지혈증)</li><li>알코올 — 남성 주 140~350 g, 여성 70~210 g (한국 소주 환산: 남성 주 1.5~5병, 여성 1~3병)</li><li>이 범위 초과 시 ALD, 음주 미만 시 MASLD</li></ul>"},
{"heading":"관리 — 두 원인 모두","html":"<ul><li>체중 7~10% 감량 (MASLD 표준)</li><li>식이·운동</li><li>알코올 절제·중단 — 최우선</li><li>당뇨·고혈압·고지혈증 약물 관리</li><li>섬유화 진행 시 적극 추적</li></ul>"},
],
"faqs":[("적당량 음주는 안전한가요?","적당량이라도 대사 위험 동반 시 간 손상 가속. 가능하면 절주 또는 금주 권장."),
("한국 회식 문화에서 어떻게 절주하나요?","무알코올 옵션 미리 준비, 적은 양 천천히, 회식 후 보충 회복 시간. 동료·가족 이해 구하기.")],
"refs":["Rinella ME, et al. A multisociety Delphi consensus statement on new fatty liver disease nomenclature (MASLD/MetALD). <em>Hepatology</em> 2023."]},

{"slug":"지방간-심혈관-CVD", "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"지방간과 심혈관 질환", "h1":"지방간 환자의 첫 사망 원인은 심혈관 질환",
"desc":"MASLD 환자의 가장 흔한 사망 원인은 간 질환이 아닌 심혈관 질환. 동맥경화·관상동맥질환 위험 평가와 예방.",
"keywords":"심혈관, CVD, 동맥경화, 지방간",
"tags":[("심혈관",),("CVD",),("동맥경화",)],
"tldr":"MASLD 환자의 가장 흔한 사망 원인은 간 질환이 아니라 <strong>심혈관 질환</strong>입니다. MASLD 자체가 심혈관 위험 인자로 작용하고, 동반된 비만·당뇨·고혈압·고지혈증이 위험을 가산합니다. 지방간 진료 시 심혈관 평가를 함께하는 것이 표준이며, statin은 MASLD에서 안전하게 사용 가능합니다.",
"sections":[
{"heading":"왜 심혈관 위험이 올라가나","html":"<ul><li>MASLD 자체가 전신 염증·인슐린 저항성 마커</li><li>동반된 대사증후군이 동맥경화 가속</li><li>간에서 만들어지는 응고·염증 단백질 변화</li><li>유전 변이(PNPLA3) 일부에서 간 vs 심혈관 위험 분기</li></ul>"},
{"heading":"평가","html":"<ul><li>표준 심혈관 위험 평가 (혈압·지질·당뇨·흡연)</li><li>경동맥 초음파 또는 관상동맥 CT 칼슘 — 일부에서</li><li>ASCVD score 계산</li></ul>"},
{"heading":"관리 — 통합 접근","html":"<ul><li>Statin — MASLD에서 안전. ALT 상승은 일과성·치료 중단 사유 아님.</li><li>혈압 조절 — 130/80 목표</li><li>당뇨 관리 — 지방간 + 당뇨에서 GLP-1·SGLT2 우선</li><li>금연</li><li>체중 감량 — 두 위험 동시 개선</li></ul>"},
],
"faqs":[("지방간 환자가 statin을 먹어도 되나요?","네, 안전합니다. ALT 일과성 상승은 흔하나 임상 의미 적음. 심혈관 위험이 큰 환자는 statin 시작이 더 중요."),
("지방간 환자도 콜레스테롤 목표가 같나요?","고위험군 기준(LDL &lt; 70 또는 100) 적용. 일반 인구보다 적극적 관리.")],
"refs":["AHA Statement: Nonalcoholic Fatty Liver Disease and Cardiovascular Risk. <em>Hepatology</em> 2017."]},

{"slug":"지방간-비만수술", "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"비만 수술과 지방간 회복", "h1":"비만 수술(bariatric surgery)과 MASLD — 가장 강력한 체중 감량",
"desc":"고도 비만 MASLD 환자에서 비만 수술의 효과 — 체중 25~30% 감량과 동반된 MASH·간섬유화 호전. 적응증과 수술 후 추적.",
"keywords":"비만수술, bariatric, 위소매절제, MASH",
"tags":[("비만수술",),("MASH",)],
"tldr":"고도 비만(BMI ≥ 35) + MASLD 환자에서 비만 수술은 가장 강력한 체중 감량 + MASH 호전 옵션입니다. <strong>위소매절제술(sleeve gastrectomy)</strong>과 <strong>위우회술(Roux-en-Y gastric bypass)</strong>이 한국에서 가장 흔하며, 1년 후 체중 25~30% 감량과 함께 약 80%에서 NASH 호전·30~40%에서 섬유화 호전이 보고됩니다. 다만 간경변 동반·문맥압 항진 환자에서는 수술 위험이 커서 신중한 평가가 필요합니다.",
"sections":[
{"heading":"적응증","html":"<ul><li>BMI ≥ 35 + 대사 동반 질환 (당뇨·고혈압·MASLD)</li><li>BMI ≥ 30 + 조절 안 되는 당뇨 (한국 기준)</li><li>생활습관·약물로 6개월 이상 체중 감량 실패</li><li>비대상성 간경변·심한 문맥압 항진 — 위험 평가</li></ul>"},
{"heading":"수술 종류","html":"<ul><li>위소매절제술 — 한국에서 가장 흔함. 위 부피 75~80% 절제. 회복 빠름.</li><li>위우회술 — 흡수 + 부피 동시. 당뇨·MASLD 효과 더 큼.</li><li>조절성 위밴드 — 한국에서 감소 추세.</li></ul>"},
{"heading":"수술 후 — 간 질환 추적","html":"<ul><li>1년 내 체중 25~30% 감량 (TWL %)</li><li>ALT·간 지방 의미 있는 호전</li><li>NASH·섬유화 추적 — Fibroscan 1년 후</li><li>드물게 수술 후 급성 간 손상(특히 빠른 체중 감량) — 단백·영양 보충 중요</li><li>당뇨·고혈압 — 50~80%에서 해소 또는 약 감량</li></ul>"},
],
"faqs":[("간이 안 좋은데 비만 수술 받을 수 있나요?","간경변이 없으면 가능. 비대상성 간경변에서는 수술 위험이 매우 커 신중한 평가."),
("수술 후 영양 결핍 위험은 없나요?","비타민·미네랄 보충제 평생 복용이 표준. 정기 혈액 검사로 관리.")],
"refs":["Lassailly G, et al. Bariatric surgery provides long-term resolution of nonalcoholic steatohepatitis. <em>Gastroenterology</em> 2020."]},

# === Cases ===
{"slug":"MASLD-청소년-가족력", "is_case":True, "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"15세 학생 — 가족력 + 비만 + MASLD", "h1":"15세 학생의 검진 ALT 상승 — 가족력 + 비만에서의 MASLD",
"desc":"가족력(아버지 MASLD) + 비만이 있는 15세 학생에서 검진 ALT 상승. 가족 단위 생활습관 개입으로 6개월 후 호전된 사례.",
"keywords":"청소년 MASLD, 가족력, 생활습관",
"tags":[("청소년 MASLD",),("가족력",)],
"case_intro":"15세 남학생. 학교 신체검사에서 ALT 75, AST 50 발견. BMI 30, 가족력 — 아버지 MASLD + 당뇨, 어머니 비만. 다른 간 질환 마커 모두 음성. 영상에서 중등도 지방간.",
"sections":[
{"heading":"개입","html":"<p>가족 단위 상담 — 부모도 함께 식이·운동 개선. 학교 영양사 협진. 가당 음료·인스턴트 식품 줄이고 가족이 함께 주말 운동. 학생 본인 일주일에 3회 학교 후 운동 + 평일 30분 걷기.</p>"},
{"heading":"6개월 결과","html":"<p>체중 3 kg 감량(BMI 30 → 28). ALT 75 → 32(정상화), 지방간 영상 호전. 학생·가족 동기 유지. 1년 후 추적 예정.</p>"},
],
"teaching":["<strong>청소년 MASLD는 가족 단위 개입이 효과적</strong>","<strong>학교·영양사 협진</strong>","<strong>3~5% 체중 감량으로도 ALT 의미 있는 호전 가능</strong>","<strong>약물 시작 전 생활습관 6~12개월 시도</strong>","<strong>비만 stigma 관리 — 진료 톤이 중요</strong>"]},

{"slug":"MASLD-수면무호흡-CPAP개선", "is_case":True, "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"OSA 진단 후 CPAP — 간 효소도 호전", "h1":"중증 코골이·낮 졸음 환자 — OSA 진단 후 CPAP과 함께 ALT도 호전",
"desc":"심한 코골이·낮 졸음 + MASLD 환자에서 OSA 진단 후 CPAP 시작. 6개월에 OSA·낮 졸음·ALT 모두 호전한 사례.",
"keywords":"OSA, CPAP, MASLD",
"tags":[("OSA",),("CPAP",),("MASLD",)],
"case_intro":"52세 남성, BMI 32, 고혈압. 정기 검진에서 ALT 65, AST 48. 가족이 \"심하게 코고는데 자다가 숨이 멈추는 것 같다\"고 호소. STOP-BANG 6점.",
"sections":[
{"heading":"평가","html":"<p>수면다원검사 — AHI 35 (중증 OSA). MASLD 진단 — 영상 + 대사 위험 인자 충족.</p>"},
{"heading":"치료와 경과","html":"<p>CPAP 시작 + 체중 감량 프로그램. 6개월 — AHI 5 미만, 낮 졸음 호전. 체중 5 kg 감량. ALT 65 → 38 호전. 가족도 코골이로 인한 수면 방해 해결.</p>"},
],
"teaching":["<strong>MASLD 환자에서 OSA 평가는 의미 있는 추가</strong>","<strong>코골이·낮 졸음·고혈압 — STOP-BANG 한 번 적용</strong>","<strong>CPAP + 체중 감량이 양쪽 모두 개선</strong>","<strong>가족 평가도 함께 — 코골이 호소 자주</strong>"]},

{"slug":"MetALD-당뇨-음주", "is_case":True, "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"당뇨 + 매일 소주 한 잔 — MetALD", "h1":"당뇨 + 매일 음주 + 지방간 — MetALD로 분류, 두 원인 동시 관리",
"desc":"당뇨 + 비만 + 매일 소주 1~2잔(주 약 200 g) 환자. 단순 MASLD 또는 ALD가 아닌 MetALD로 분류 후 통합 관리한 사례.",
"keywords":"MetALD, 당뇨, 알코올",
"tags":[("MetALD",),("당뇨",),("알코올",)],
"case_intro":"58세 남성. 2형 당뇨 5년, BMI 29, 고혈압. 매일 저녁 소주 1.5잔 + 주말 회식 추가(주 약 200 g 알코올). 정기 검진 ALT 72, GGT 145, 영상에서 중등도 지방간.",
"sections":[
{"heading":"분류와 평가","html":"<p>대사 위험 인자(당뇨·비만·고혈압) + 알코올 주 200 g(MetALD 범위) = MetALD 분류. 단순 MASLD 또는 단순 ALD가 아닌 두 원인 모두 작용.</p>"},
{"heading":"관리","html":"<p>(1) 절주 — 환자 의지로 매일 음주 중단 시도, 주 회식 1회로 제한. (2) 당뇨 — metformin + GLP-1 작용제(semaglutide) 시작. (3) 체중 감량 6 kg. 12개월 후 — ALT 72 → 35, GGT 145 → 60, 당뇨 HbA1c 7.8 → 6.5.</p>"},
],
"teaching":["<strong>MetALD는 흔하지만 옛 NAFLD 정의로는 놓쳤던 그룹</strong>","<strong>두 원인 동시 관리가 핵심</strong>","<strong>한국 회식 문화에서 절주 어려움</strong> — 환자 의지·가족 지지 중요","<strong>GLP-1 작용제는 당뇨·비만·MASLD 동시 효과</strong>","<strong>GGT가 알코올 영향 잘 반영</strong> — 절주 모니터링 지표"]},

{"slug":"MASLD-비만수술-회복", "is_case":True, "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"BMI 42에서 위소매절제 — MASH 호전", "h1":"고도 비만 MASH 환자의 위소매절제 — 1년 후 NASH 호전",
"desc":"BMI 42 + MASH F3 + 당뇨 환자. 생활습관·약물 실패 후 위소매절제술 시행. 1년 후 25 kg 감량·NASH 해소·당뇨 호전.",
"keywords":"비만수술, sleeve gastrectomy, MASH",
"tags":[("비만수술",),("MASH",)],
"case_intro":"45세 여성. BMI 42, 당뇨·고혈압·고지혈증·수면 무호흡 동반. 간생검 — MASH NAS 6 (NASH activity), F3 섬유화. 생활습관·메트포민·GLP-1 6개월 시도 후 효과 미미.",
"sections":[
{"heading":"수술 결정","html":"<p>외과·내분비·간내과 협진. 위소매절제술(sleeve gastrectomy) 결정. 수술 전 영양 평가, 정신과 평가, 마취 위험 평가.</p>"},
{"heading":"수술 후 경과","html":"<p>6개월 — 17 kg 감량, ALT 95 → 38, HbA1c 8.2 → 6.0. CPAP 사용 중단(OSA 해소). 12개월 — 25 kg 감량(BMI 33), ALT 정상, HbA1c 5.8, 당뇨약 중단. Fibroscan 18 → 9 kPa.</p>"},
],
"teaching":["<strong>고도 비만 + MASH F3 — 비만 수술 강한 적응증</strong>","<strong>생활습관·약물 실패 후 검토</strong>","<strong>당뇨·OSA 동시 호전이 흔함</strong>","<strong>섬유화 호전은 시간 걸리나 의미 있는 회복 보고</strong>","<strong>수술 후 영양·비타민 평생 보충 필수</strong>"]},

{"slug":"MASLD-심혈관-종합관리", "is_case":True, "hub_path":MAS_HUB, "hub_label":MAS_LBL, "section":MAS_SEC,
"title":"MASLD + 협심증 — 통합 관리", "h1":"MASLD + 안정형 협심증 — Statin 시작과 통합 관리",
"desc":"MASLD + 관상동맥 협착 + 고지혈증 환자. ALT 상승 우려로 statin 미루던 환자에게 statin 시작 후 안전성 확인 사례.",
"keywords":"심혈관, statin, MASLD",
"tags":[("심혈관",),("statin",),("MASLD",)],
"case_intro":"61세 남성. MASLD 진단 3년, ALT 65로 약간 상승. 최근 흉통으로 관상동맥 CT — 좌전하행지 70% 협착. 심장내과 statin 권유했으나 \"간이 안 좋아서 못 먹는다\"고 거부. 간내과 협진.",
"sections":[
{"heading":"평가와 결정","html":"<p>MASLD에서 statin은 안전. ALT 상승 약간 있어도 statin 시작 가능. 심혈관 위험(ASCVD 25%)이 statin 부작용 우려보다 훨씬 큼.</p>"},
{"heading":"경과","html":"<p>Rosuvastatin 10 mg 시작. 6주 ALT 추적 — 65 → 70(약간 상승) → 12주 후 58로 감소. 6개월 LDL 162 → 78. 협심증 안정.</p>"},
],
"teaching":["<strong>MASLD 환자에서 statin은 안전 — \"간이 안 좋아서\"가 금기 아님</strong>","<strong>ALT 일과성 상승은 임상 의미 적음</strong>","<strong>심혈관 위험이 statin 부작용 우려보다 훨씬 큼</strong>","<strong>환자 설명 — \"심혈관 사망이 간 사망보다 흔하다\"</strong>","<strong>심장내과·간내과 협진 메시지 통일이 환자 신뢰 줌</strong>"]},
]

# === 간수치 ===
LFT_HUB, LFT_LBL, LFT_SEC = "/간수치/", "간수치 이상", "간수치 이상"

LFT = [
{"slug":"간수치-운동후-상승", "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"격렬한 운동 후 간수치 상승", "h1":"격렬한 운동 후 AST·ALT 상승 — 간 손상인가, 근육에서 온 것인가",
"desc":"마라톤·웨이트 트레이닝 후 일과성으로 오르는 AST·ALT. AST가 더 많이 오르는 근육 기원 패턴과 검사 시점 조정.",
"keywords":"운동, AST, ALT, CK, 근육",
"tags":[("운동",),("AST",),("CK",)],
"tldr":"격렬한 운동 — 마라톤, 헬스(특히 다리·등 같은 큰 근육군), 격투 운동 — 직후 24~72시간 사이에 AST·ALT가 일시적으로 오를 수 있습니다. 이때는 <strong>간 손상이 아니라 근육에서 빠져나온 효소</strong>로, AST가 ALT보다 더 많이 오르고 CK도 함께 오릅니다. 검사 1~2일 전 격렬한 운동을 피하는 것이 정확한 평가의 첫 단계입니다.",
"sections":[
{"heading":"왜 운동 후 간수치가 오르나","html":"<ul><li>AST와 ALT는 간뿐 아니라 근육에도 존재. AST는 근육에 더 풍부.</li><li>격렬한 운동으로 근육 미세 손상 → 효소 혈중 누출</li><li>마라톤 후 AST 300~500까지 오를 수 있음</li><li>일반 운동(걷기·가벼운 조깅)은 거의 영향 없음</li></ul>"},
{"heading":"감별 — 근육 기원 vs 간 기원","html":"<table><thead><tr><th>패턴</th><th>근육 기원</th><th>간 기원</th></tr></thead><tbody><tr><td>AST/ALT 비</td><td>대부분 1.5 이상 (AST 우세)</td><td>대부분 1 미만 (ALT 우세, 알코올은 예외)</td></tr><tr><td>CK</td><td>의미 있게 상승</td><td>정상</td></tr><tr><td>LDH</td><td>상승</td><td>약간 상승 또는 정상</td></tr><tr><td>회복 패턴</td><td>72시간 후 정상화</td><td>원인 따라 다양</td></tr></tbody></table>"},
{"heading":"평가 — 1주일 후 재검","html":"<p>운동 직후 검사에서 AST·ALT 상승 시 1~2주 휴식 후 재검. 정상으로 돌아오면 운동 기원. 지속 상승하면 다른 원인 평가(영상·바이러스·자가면역·약물).</p>"},
],
"faqs":[("마라톤 후 간수치 오른 게 평생 위험인가요?","아닙니다. 일과성 근육 기원으로 자연 회복. 다음 검사는 휴식 후."),
("운동 자체가 간에 나쁜가요?","아닙니다. 적절한 운동은 간 건강에 좋습니다. 격렬한 운동 직후 검사 타이밍만 조정.")],
"refs":["Pettersson J, et al. Muscular exercise can cause highly pathological liver function tests in healthy men. <em>Br J Clin Pharmacol</em> 2008."]},

{"slug":"간수치-임신중-변화", "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"임신 중 간수치 변화", "h1":"임신 중 간수치 — 정상 변동과 의심해야 하는 패턴",
"desc":"임신 중 ALP는 자연 상승(태반 기원), 알부민·빌리루빈은 약간 감소. AST/ALT·총담즙산이 의미 있게 오르면 임신성 간내 담즙 정체 등 평가.",
"keywords":"임신, 간수치, ALP, 담즙정체",
"tags":[("임신",),("간수치",),("ALP",)],
"tldr":"임신 중 간수치는 정상적인 변화가 일부 있습니다. <strong>ALP는 태반에서 만들어져 자연 상승</strong>(2~4배까지), 알부민은 혈장 부피 증가로 약간 감소합니다. 반면 <strong>AST·ALT·총담즙산은 임신 중에도 정상 범위 유지</strong>가 정상이라 이들이 오르면 임신성 간 합병증(임신성 간내 담즙 정체, HELLP, AFLP)을 의심합니다.",
"sections":[
{"heading":"임신 중 정상 변화","html":"<ul><li>ALP — 2~4배 상승 (태반 기원). 정상.</li><li>알부민 — 약 10~20% 감소.</li><li>총담즙산 — 정상 유지 (≤ 10 μmol/L).</li><li>AST·ALT — 정상 유지.</li><li>빌리루빈 — 약간 감소 또는 정상.</li></ul>"},
{"heading":"의심해야 할 패턴","html":"<table><thead><tr><th>패턴</th><th>의심</th></tr></thead><tbody><tr><td>가려움 + 총담즙산 ≥ 10</td><td>임신성 간내 담즙 정체(ICP)</td></tr><tr><td>고혈압 + 단백뇨 + 혈소판 감소 + AST/ALT ↑</td><td>HELLP 증후군</td></tr><tr><td>3분기 + 오심·황달 + 응고 이상</td><td>임신성 급성 지방간(AFLP)</td></tr><tr><td>1분기 심한 입덧 + ALT ↑</td><td>hyperemesis gravidarum 동반 간 영향</td></tr></tbody></table>"},
{"heading":"평가","html":"<p>의심 시 산과·간내과 협진. 영상(초음파, 필요 시 MRI 가능 — 가돌리늄 회피), 혈청학(바이러스, 자가면역), 응고 검사. ICP는 ursodeoxycholic acid로 치료, 심한 경우 조기 분만 검토.</p>"},
],
"faqs":[("임신 중 ALP가 두 배 올랐는데 위험한가요?","대부분 태반 기원으로 정상. 다른 수치와 함께 평가."),
("가려움이 심한데 검사 받아봐야 하나요?","손·발바닥 가려움이 야간에 심해지면 ICP 의심. 총담즙산 검사가 결정적.")],
"refs":["EASL Clinical Practice Guidelines on pregnancy-related liver disease. <em>J Hepatol</em> 2023."]},

{"slug":"간수치-검진주기-결정", "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"검진 주기 결정 — 위험 인자별", "h1":"간 검진 주기 — 위험 인자에 따라 다르게",
"desc":"일반인은 1~2년에 한 번, B형/C형간염은 6개월, 간경변은 6개월 영상 + 표지자, 가족력 있는 사람은 별도 평가.",
"keywords":"검진주기, 간암검진, 위험인자",
"tags":[("검진주기",),("간암검진",)],
"tldr":"간 검진 주기는 위험 인자에 따라 크게 다릅니다. <strong>일반인은 국가 검진(40세 이상 2년에 한 번)</strong>이면 충분하지만, <strong>만성 B형/C형간염·간경변·가족력·진행 섬유화</strong>가 있으면 6개월 간격 정기 검진(영상 + 종양표지자)이 표준입니다. 자기 위험 단계에 맞는 주기를 정하는 것이 비용 효율과 안전 사이의 균형입니다.",
"sections":[
{"heading":"위험 단계별 주기","html":"<table><thead><tr><th>위험 단계</th><th>주기·검사</th></tr></thead><tbody><tr><td>일반인 무위험</td><td>국가 검진 (40세 이상 2년 1회)</td></tr><tr><td>만성 B형/C형간염 (간경변 없음, 40세 이하)</td><td>6~12개월 ALT·DNA·영상</td></tr><tr><td>40세 이상 만성 B형/C형, 가족력</td><td>6개월 초음파 + AFP + PIVKA-II</td></tr><tr><td>간경변 (원인 무관)</td><td>6개월 영상 + 표지자, 정맥류 EGD 1~3년</td></tr><tr><td>진행 섬유화 F3</td><td>6~12개월 영상 + 표지자</td></tr><tr><td>MASLD F0-F2</td><td>1~2년 ALT·Fibroscan</td></tr><tr><td>DAA 완치 후 비간경변</td><td>일반 검진 수준</td></tr><tr><td>DAA 완치 후 F3-F4</td><td>6개월 영상 + 표지자 평생</td></tr></tbody></table>"},
{"heading":"왜 6개월 주기인가","html":"<p>간세포암 종양 배가시간이 평균 4~6개월. 6개월 검진은 작은 단계에서 발견 가능하게 해 줍니다. 3개월은 비용·환자 부담 대비 추가 이득이 적고, 12개월은 진행기 발견 위험이 의미 있게 늘어납니다.</p>"},
],
"faqs":[("6개월에 한 번이 부담스러워요","수술 가능한 단계에서 발견하는 것이 평생 가치 매우 큼. 외래 일정과 함께 미리 잡는 것이 도움."),
("초음파만으로 충분한가요?","B형간염·간경변에서는 초음파 + AFP + PIVKA-II 조합이 한국 표준.")],
"refs":["대한간암학회·국립암센터. 2022 한국 간세포암종 진료 가이드라인."]},

{"slug":"간수치-소아청소년-기준", "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"소아·청소년 간수치 정상 기준", "h1":"소아·청소년의 간수치 정상 범위 — 성인과 다르다",
"desc":"소아·청소년 ALT 상한은 성인보다 낮음(남아 26, 여아 22 U/L). MASLD 조기 발견·진단의 기준점.",
"keywords":"소아 ALT, 청소년 간수치, 정상 기준",
"tags":[("소아 ALT",),("청소년",)],
"tldr":"소아·청소년의 ALT 정상 상한은 성인(약 40 U/L)보다 낮은 <strong>남아 26 U/L, 여아 22 U/L</strong>입니다(NASPGHAN, NHANES 기반). 성인 기준 40을 적용하면 MASLD가 있는 소아를 놓치게 됩니다. 한국에서 학교 신체검사·소아과 검진에서 이 낮은 기준을 적용하는 것이 늘고 있습니다.",
"sections":[
{"heading":"왜 기준이 다른가","html":"<p>성인 ALT 상한 40 U/L은 1980년대 무증상 기증자 집단 평균으로 정해진 기준이라 비만·MASLD가 늘어난 현재에는 너무 높습니다. 무증상 정상 청소년의 95 percentile은 남아 26, 여아 22로 측정됩니다. 이 기준이 비만·MASLD 환자를 더 잘 잡아냅니다.</p>"},
{"heading":"임상 적용","html":"<ul><li>소아·청소년 ALT &gt; 26(남) 또는 &gt; 22(여) — MASLD 평가 시작</li><li>3개월 연속 상승 시 영상 + 가족력 평가</li><li>비만·당뇨 동반 시 적극 평가</li></ul>"},
],
"faqs":[("소아 ALT 30이면 정상인가요?","아닙니다. 소아 기준에서 약간 상승. 비만·가족력 있으면 평가."),
("어디서 소아 기준 검사를 받나요?","대학병원 소아청소년과·소아 소화기 전문 의료기관에서 이 기준 적용.")],
"refs":["Schwimmer JB, et al. SAFETY study: alanine aminotransferase cutoff values are set too high for reliable detection of pediatric chronic liver disease. <em>Gastroenterology</em> 2010."]},

{"slug":"간수치-AST-우세-원인", "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"AST > ALT 패턴의 원인", "h1":"AST가 ALT보다 더 오르는 패턴 — 알코올, 근육, 진행 섬유화",
"desc":"AST/ALT 비율이 1.5 이상인 패턴 — 알코올성 간염, 근육 손상, 진행 간경변, 일부 약물성, Wilson병의 단서.",
"keywords":"AST, ALT, 비율, 알코올",
"tags":[("AST",),("ALT",),("알코올",)],
"tldr":"AST가 ALT보다 더 많이 오르는 패턴(AST/ALT &gt; 1.5)은 몇 가지 특이적 원인을 시사합니다. 가장 흔한 것이 <strong>알코올성 간 손상</strong>(AST/ALT ≥ 2가 전형), 그다음 <strong>근육 기원</strong>(운동 후·근염), <strong>진행된 간경변</strong>, 일부 <strong>약물성</strong>·<strong>Wilson병</strong>. ALT 우세 패턴(바이러스성·MASLD·자가면역)과는 평가 방향이 다릅니다.",
"sections":[
{"heading":"AST > ALT 흔한 원인","html":"<ol><li><strong>알코올성 간염</strong> — AST/ALT ≥ 2가 전형. GGT 함께 상승.</li><li><strong>근육 손상</strong> — 운동·근염·심근 손상. CK·LDH 동반 상승.</li><li><strong>진행된 간경변</strong> — ALT 합성에 필요한 비타민 B6 결핍.</li><li><strong>약물성</strong> — 일부 약 (콜히친 등)에서 AST 우세.</li><li><strong>Wilson병</strong> — 35세 이하에서 의심 시 평가.</li><li><strong>심한 급성 간염 후기</strong> — 회복기에 AST가 더 오래 남음.</li></ol>"},
{"heading":"평가 흐름","html":"<ol><li>알코올 이력 — 가장 흔한 원인. 솔직한 음주력 확인.</li><li>CK·LDH — 근육 기원 배제.</li><li>영상 — 간경변 평가.</li><li>약물 이력.</li><li>35세 이하 + 비전형 — Wilson병 평가(세룰로플라스민·24시간 소변 구리).</li></ol>"},
],
"faqs":[("AST/ALT 2.5이면 알코올성인가요?","알코올성 가능성이 가장 높습니다. 다만 다른 원인도 확인이 필요해요. GGT도 함께 상승하면 강하게 알코올 의심."),
("근육 운동을 안 했는데 AST가 높아요","근염·심근 손상도 가능. CK 검사로 감별.")],
"refs":["Cohen JA, Kaplan MM. The SGOT/SGPT ratio--an indicator of alcoholic liver disease. <em>Dig Dis Sci</em> 1979.","Diehl AM, et al. Alcohol-like liver disease in nonalcoholics. <em>Gastroenterology</em> 1988."]},

# === Cases ===
{"slug":"ALT일과성상승-격렬한운동", "is_case":True, "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"마라톤 직후 AST 380 — 근육 기원", "h1":"마라톤 다음날 검진 AST 380 — 1주일 후 정상화",
"desc":"마라톤 완주 다음날 정기 검진에서 AST 380, ALT 95 발견. CK 4,500으로 근육 기원 확인 후 1주일 휴식 후 재검 정상화.",
"keywords":"운동, AST, CK",
"tags":[("운동",),("AST",),("CK",)],
"case_intro":"42세 남성, 마라톤 동호회. 풀코스 완주 다음날 정기 검진에서 AST 380, ALT 95, ALP 정상, 빌리루빈 정상. 환자는 \"평소 ALT는 25 정도인데 갑자기 왜?\"",
"sections":[
{"heading":"평가","html":"<p>AST/ALT 비 약 4. 운동 직후 시점. CK 추가 — 4,500. LDH 850. 근육 기원 강하게 의심. 영상 정상, 다른 간 질환 마커 정상.</p>"},
{"heading":"경과","html":"<p>1주일 휴식 권유 후 재검 — AST 32, ALT 28, CK 220 모두 정상. 진단 \"운동 후 일과성 간 효소 상승\". 향후 검진 1~2일 전 격렬한 운동 회피 안내.</p>"},
],
"teaching":["<strong>AST 우세 + CK 동반 — 근육 기원</strong>","<strong>운동 직후 검진은 위양성 흔함</strong>","<strong>1~2주 휴식 후 재검이 표준 평가</strong>","<strong>환자에게 안내 — 검진 1~2일 전 격렬한 운동 피하기</strong>"]},

{"slug":"임신중-ALT상승-감별", "is_case":True, "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"임신 32주 ALT 145 — ICP 진단", "h1":"임신 32주에 ALT 145 + 가려움 — 임신성 간내 담즙 정체(ICP) 진단",
"desc":"임신 3분기 손·발 가려움 + ALT 145 + 총담즙산 25 — 임신성 간내 담즙 정체로 진단 후 ursodeoxycholic acid 시작 사례.",
"keywords":"임신, ICP, 담즙정체, ursodeoxycholic",
"tags":[("임신",),("ICP",),("담즙정체",)],
"case_intro":"31세 여성, 임신 32주. 손바닥·발바닥 야간 가려움 시작, 잠 못 잠. 산과 의뢰 검사에서 ALT 145, AST 110, ALP 250, 총담즙산 25 (정상 ≤ 10). 다른 간 질환 마커 음성.",
"sections":[
{"heading":"진단","html":"<p>임신성 간내 담즙 정체(intrahepatic cholestasis of pregnancy, ICP) 진단. 한국 유병률 약 1~2%, 가족력 있는 경우 늘어남.</p>"},
{"heading":"치료","html":"<p>Ursodeoxycholic acid(UDCA) 시작 — 가려움 1주 안에 호전. 총담즙산 25 → 12. 산과·간내과 협진으로 분만 시점 결정 — 총담즙산이 ≥ 40으로 매우 높지 않아 정상 만삭(38주) 분만으로 계획.</p>"},
{"heading":"분만 후","html":"<p>분만 후 2주 — 간수치·총담즙산 정상화. UDCA 중단. 다음 임신 시 재발 위험 50~70% 안내.</p>"},
],
"teaching":["<strong>임신 3분기 가려움 — ICP 의심</strong>","<strong>총담즙산이 결정적 진단 마커</strong>","<strong>UDCA가 효과적</strong>","<strong>총담즙산 ≥ 40 — 조기 분만 검토</strong>","<strong>다음 임신에서 재발 흔함 — 미리 안내</strong>"]},

{"slug":"소아청소년-검진ALT상승", "is_case":True, "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"14세 학생 ALT 35 — 소아 기준으로 평가", "h1":"14세 학생 ALT 35 — 성인 기준에선 정상, 소아 기준으로는 평가 시작",
"desc":"14세 BMI 27 학생의 학교 검진 ALT 35. 성인 기준 정상이지만 소아 기준(남아 ≤ 26)으로는 의미 있는 상승. 평가 후 MASLD 진단.",
"keywords":"소아 ALT, 학교검진, MASLD",
"tags":[("소아 ALT",),("MASLD",)],
"case_intro":"14세 남학생. 학교 신체검사에서 ALT 35, AST 28. 성인 검진실에서는 \"정상\" 보고. 학부모가 가족력 (아버지 MASLD) + 비만으로 걱정해 소아과 의뢰.",
"sections":[
{"heading":"평가","html":"<p>BMI 27 (소아 비만 기준). 소아 ALT 정상 상한 26 초과로 의미 있는 상승. 다른 간 질환 마커 음성, 영상에서 경증 지방간. MASLD로 진단.</p>"},
{"heading":"개입","html":"<p>가족 단위 생활습관 개입 시작. 6개월 후 — 체중 4 kg 감량, ALT 35 → 22, 지방간 영상 호전.</p>"},
],
"teaching":["<strong>소아 ALT 정상 상한은 성인보다 낮음(남아 26, 여아 22)</strong>","<strong>학교 검진의 \"정상\" 판정도 소아 기준 다시 적용 의미 있음</strong>","<strong>가족력 + 비만 시 적극 평가</strong>","<strong>3~5% 체중 감량으로도 의미 있는 호전</strong>"]},

{"slug":"AST우세-근육질환배제", "is_case":True, "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"AST 250, ALT 60 — 다발성 근염 진단", "h1":"AST 250 + 근육 약화 — 다발성 근염 진단으로 이어진 사례",
"desc":"AST 우세 패턴(AST/ALT 4.2) + 점진적 근육 약화 호소. CK 8,500 + 근전도 + ANA로 다발성 근염 진단 후 류마티스내과 의뢰.",
"keywords":"AST, CK, 다발성근염",
"tags":[("AST",),("CK",),("근염",)],
"case_intro":"55세 여성. 6개월 동안 \"계단 오르기 힘들어진다\" 호소. 정기 검진 AST 250, ALT 60. 영상 정상, 바이러스·자가면역 마커 음성.",
"sections":[
{"heading":"평가","html":"<p>AST/ALT 비 4.2 — 근육 기원 의심. CK 측정 — 8,500. LDH 950. 근전도(EMG) — 근염 패턴. ANA·anti-Jo-1 양성.</p>"},
{"heading":"진단과 치료","html":"<p>다발성 근염(polymyositis) 진단. 류마티스내과 의뢰, 스테로이드 + 메토트렉세이트 시작. 6개월 후 CK 정상화, AST 정상화, 근력 호전.</p>"},
],
"teaching":["<strong>AST 단독 또는 우세 상승 — 근육 기원 의심</strong>","<strong>CK가 결정적</strong>","<strong>간이 아닌 다른 장기 질환의 단서</strong> — 자가면역 근염, 갑상선, 심근염","<strong>간내과 검사가 다른 진료과로의 의뢰 시점</strong>","<strong>모든 \"간수치\"가 간 문제는 아님</strong>"]},

{"slug":"만성경증ALT상승-원인불명", "is_case":True, "hub_path":LFT_HUB, "hub_label":LFT_LBL, "section":LFT_SEC,
"title":"3년간 ALT 55~70 유지 — 원인 평가 끝에 PNPLA3 유전 변이", "h1":"3년 ALT 60대 — 모든 검사 정상에서 PNPLA3 유전 변이 발견",
"desc":"40대 마른 환자에서 3년간 경증 ALT 상승 지속. 일반 검사·영상 모두 정상에서 유전 평가로 PNPLA3 동형접합 변이 확인 사례.",
"keywords":"원인불명, PNPLA3, lean MASLD",
"tags":[("PNPLA3",),("lean MASLD",)],
"case_intro":"45세 남성, BMI 23 (마름). 3년간 정기 검진에서 ALT 55~70 사이 유지. 음주 거의 없음. B형/C형/자가면역/Wilson·혈색소증·AAT 결핍 모두 음성. 영상에서 미세 지방간 의심.",
"sections":[
{"heading":"평가","html":"<p>흔한 원인 모두 음성. Fibroscan 7.8 kPa (경증 섬유화 가능성). 유전 평가 — PNPLA3 rs738409 GG (동형접합 변이, 위험 대립 유전자). 가족력 — 형 ALT 약간 상승.</p>"},
{"heading":"관리","html":"<p>Lean MASLD + PNPLA3 변이로 분류. 적극적 생활습관 — 운동·식이·금주 + 매년 ALT·Fibroscan 추적. 약물 시작 안 함. 3년 추적에서 안정.</p>"},
],
"teaching":["<strong>마른 환자의 만성 ALT 상승 — 유전 평가 의미 있음</strong>","<strong>PNPLA3 GG는 lean MASLD·간 질환 진행 위험 인자</strong>","<strong>가족력 함께 평가</strong>","<strong>적극 추적 + 생활습관이 핵심</strong>","<strong>모든 ALT 상승의 원인을 찾는 게 항상 가능한 건 아니다</strong>"]},
]

if __name__ == "__main__":
    write_pages(MASLD + LFT)
