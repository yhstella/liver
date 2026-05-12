#!/usr/bin/env python3
"""모든 케이스 페이지에 '임상 트리비아' callout 추가.

각 슬러그별로 케이스 주제에 맞는 1-2 문장 트리비아.
삽입 위치: teaching-box 직전 (없으면 disclaimer 직전).
idempotent: 이미 있으면 갱신.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MARK_START = '<!-- case-pearl:auto:start -->'
MARK_END = '<!-- case-pearl:auto:end -->'
BLOCK_RE = re.compile(rf'{re.escape(MARK_START)}.*?{re.escape(MARK_END)}\s*', re.DOTALL)

TRIVIA = {
    # 간경변 / 합병증
    '첫-식도정맥류-출혈': '급성 정맥류 출혈 사망률은 항생제 도입 전 30–50%였지만 ceftriaxone 7일 + terlipressin·EVL 표준화 이후 약 15%로 떨어졌습니다. 항생제 단독 효과의 NNT는 22 — 입원 시 가장 효율 높은 개입 중 하나입니다.',
    '복수-SBP-진단치료': 'SBP 1차 항생제는 cefotaxime 2 g q8h. 알부민 1.5 g/kg 첫날 + 1 g/kg 3일째 추가하면 HRS·사망률을 30→10%로 낮춥니다 (Sort, NEJM 1999) — 단순 항생제 단독보다 큰 차이입니다.',
    '반복SBP-예방요법': '한 번 SBP 경험자의 1년 내 재발률은 약 70%. Norfloxacin 400 mg/일로 2차 예방하면 재발률 20%까지 떨어집니다. 간이식 평가의 강한 적응증 — 한 번 SBP만으로도 MELD-Na와 무관하게 이식 검토 권장.',
    '간성혼수-첫발생': '한국에서 rifaximin은 2018년 보험 적용. 첫 발생 시 lactulose 단독으로 시작하고 재발 시 rifaximin 병용이 표준. 비대상성 신호이므로 첫 episode부터 이식 평가 시작.',
    'Recompensation-바이러스억제후': 'HBV/HCV 억제 후 비대상성 환자의 약 30–50%가 5년 내 recompensation(복수·뇌증·정맥류 모두 6개월 이상 안정). Baveno VII에서 처음 공식 정의 — 이식 우선순위 재평가의 근거.',
    '정맥류출혈이력-STRIDE': 'STRIDE(2022 Baveno VII) = "decompensation 진행을 줄이는 모든 비-이식 개입". 비선택적 β-차단제 + HVPG 반응 ≥10% 감소가 핵심 지표. 한국에서는 HVPG 측정 가능 센터가 제한적이라 임상 적용에 한계.',
    '저나트륨혈증-tolvaptan': 'Tolvaptan은 한국에서 SIADH 적응으로 급여되지만 간경변 저나트륨혈증에는 까다로움. 처음 24시간 ≤8 mEq/L 교정 — 초과 시 osmotic demyelination(ODS) 위험. 안전한 영역이 좁은 약.',
    '간경변-새결절-평가': '간경변 환자에서 새로 보이는 1 cm 미만 결절은 90%가 비-악성(재생결절·dysplastic). 그러나 1 cm 이상이면 LI-RADS 평가로 LR-3 이상 가능성 ↑ — 크기가 결정적 기준.',
    '간기능회복-재절제': '간 절제 후 잔여 간은 4–8주에 원래의 60–80%까지 재생. 첫 절제 1년 후 작은 재발이면 잔여 간 충분 시 재절제 가능 — 5년 생존율 첫 절제와 비슷.',

    # HCC / 진단·치료
    '건강검진-우연발견-1cm결절': '1 cm 미만 결절은 위험군에서도 HCC 가능성 약 30%. KLCA-NCC와 AASLD 모두 3–6개월 단기 추적 권장. 1 cm 넘으면 영상 진단 적극 — 동맥기 증강 + washout 패턴이면 LR-5로 즉시 치료.',
    'AFP상승-영상음성': '활동성 간염·HBeAg(+)에서 AFP 50–200까지 만성적 상승 흔함 (위양성 30%). 영상이 깨끗하면 1–3개월 추적 + PIVKA-II 동반 확인이 표준. AFP 단독 ≥200이 지속되면 EOB-MRI까지.',
    'PIVKAII-와파린-위양성': 'PIVKA-II는 비타민 K 의존이라 와파린·DOAC 환자에서 거짓 상승. AFP는 영향 없음. 와파린 → DOAC 전환으로 PIVKA-II가 정상화되면 위양성 확정 — 한국 임상에서 흔히 놓치는 함정.',
    'LR3-모호결절-추적': 'LR-3 결절의 1년 내 HCC 진행률은 약 30%, LR-4는 70%. LR-3은 3–6개월 단기 추적이 표준이며, 2회 연속 안정이면 일반 추적으로 복귀. 추적 영상은 같은 modality로 (CT는 CT, MRI는 MRI).',
    'LR4-결절-추적': 'LR-4는 다학제 결정 사안. 위치·간기능·환자 선호에 따라 (1) 즉시 치료 (2) 생검 (3) 3개월 단기 추적 중 선택. KLCA-NCC는 LR-4도 LR-5처럼 치료 시작 가능 — 가이드라인 간 미세한 차이.',
    'BCLC-A-단일3cm-절제vs소작': '단일 ≤3 cm 절제와 RFA의 5년 생존율 비슷(약 60–70%). 위치(혈관·담관·복막 근접)·간 기능(Child A vs B7)·환자 동반질환이 결정. 일본 SURF 연구에서 RFA 비열등성 입증.',
    'BCLC-A-다발3개-소작': '"3개 이하 + 각각 ≤3 cm"이면 다발 ablation 가능 (BCLC 0/A 확장). 그러나 위치가 어렵거나 4개 이상이면 TACE로 전환. 한국 KLCA-NCC는 다발 ablation 적극 인정.',
    'BCLC-B-다발성-TACE': 'TACE 1회 PFS 약 6–8개월. "TACE refractory"는 2회 이상 후 4–6개월 내 재발 — 이때 면역치료(EMERALD-1 결과 적용) 또는 SBRT 전환 검토.',
    'ChildB-단일4cm-이식': 'Milan criteria(단일 ≤5 cm 또는 3개 ≤3 cm) + Child B = 절제 위험 ↑ → 이식 우선. 한국 KONOS는 MELD 우선이라 Child B(MELD 13–18)는 LDLT 검토.',
    'ChildC-이식대기': '한국 KONOS는 MELD ≥15부터 본격 등록. Child C라도 MELD 10대면 대기 시간 길어 LDLT(생체 기증) 의존도 ↑. 한국 간이식의 약 65%가 LDLT — 세계 최고 비율.',
    'HCC-림프절전이': '림프절 단독 전이는 BCLC C — 면역치료 1차(atezo+bev 또는 durva+treme) 표준. 일부 oligometastasis(단일 림프절)는 추가 SBRT로 국소 통제 가능.',
    'HCC-폐전이-단독': '폐 단독 oligometastasis(≤3개)이면 SBRT 추가가 OS 개선 데이터 일부 보고. 그러나 BCLC 기본 권고는 전신치료가 우선 — 다학제 결정 사안.',
    'MASLD-HCC-비만당뇨': '비간경변 MASLD에서도 HCC 가능 (전체의 약 20–30%). 그러나 비용 효율 검진은 어렵고, 한국 KLCA-NCC도 비간경변 MASLD 일률 검진 권고 없음 — 위험 layer(F3·당뇨·비만 동반)에 집중.',
    '다운스테이징-이식전환': 'BCLC B → Milan 충족까지 downstage(TACE 반복)되면 이식 가능 — UCSF down-staging protocol. 6개월 안정이 핵심 조건.',
    '소작후-2년재발-단일결절': 'RFA/MWA 후 5년 누적 재발률 50–70%. 대부분은 새 발생(de novo) — 같은 위치 국소 재발은 5–15%. 정기 검진 6개월 간격을 평생 유지가 핵심.',
    '절제후-2년재발': '절제 후 5년 재발률 50–70%, 평균 재발 시점 약 2년. 재발 시 잔여 간 기능 충분 + 단일 결절이면 재절제 또는 RFA. 면역치료 보조요법(IMbrave050)은 적응 제한적.',
    '큰종양-TACE-SBRT-결합': '5 cm 이상 단일 종양에서 TACE 단독은 효과 제한적. TACE + SBRT 콤보로 국소 통제율 약 85% (LEAP-012 등 데이터 누적 중). 한국 보험은 양쪽 모두 가능.',
    'AtezoBev-실패-2차치료': '면역치료(atezo+bev) 1차 실패 후 2차 옵션 = regorafenib, cabozantinib, ramucirumab(AFP ≥400). 직접 비교 데이터는 없어 부작용·환자 선호로 결정.',
    '문맥침범-AtezoBev': '문맥혈전 동반 HCC = 전형적 BCLC C. Atezo+bev는 IMbrave150에서 sorafenib 대비 OS 19.2 vs 13.4개월. 단, 정맥류 출혈 위험으로 사전 EGD 필수.',
    'B형간염-검진-새결절': 'B형간염 보균자에서 6개월 검진은 종양 배가시간(약 4–6개월)에 기반. 1 cm 미만 결절도 6개월 추적이면 LR-5 진단 시점에 평균 1.5 cm로 잡혀 — 조기 진단 핵심.',
    '경구피임약-HCA의심': 'OCP 5년 이상 사용 시 간 선종(HCA) 위험 약 5배. β-catenin 양성 아형은 악성 변환 위험 ↑로 크기 무관 절제 검토. OCP 중단만으로도 50%에서 6개월 내 크기 감소.',
    '간경변-새결절-평가': '간경변 환자의 새 결절은 LI-RADS로 평가. LR-5(동맥기 증강 + washout + ≥10 mm)면 생검 없이 치료. 한국 KLCA-NCC도 같은 영상 기준 채택 — 생검 회피로 출혈·전이 위험 ↓.',

    # B형간염
    'B형간염-Occult-항암치료': 'Occult HBV(HBsAg(−), anti-HBc(+))에서 rituximab 항암 시 재활성화율 약 10–20%, HBV DNA 양성이면 30–50%. anti-HBc(+) 모든 항암 환자에서 prophylaxis 권장 — TDF/ETV 항암 시작 1주 전부터 종료 후 12개월까지.',
    'B형간염-HDV-동반': '한국 HDV 유병률은 HBsAg(+) 중 약 1–3% (서구의 5–10%보다 낮음). 그러나 HDV 동반 시 간경변·HCC 진행 약 3배 빠름 — HBsAg(+) 모든 환자에서 평생 1회 anti-HDV 검사 권장.',
    'B형간염-소아청소년-치료시작': '소아 면역관용기(immune tolerance)에서 치료는 권장하지 않음 — 자연 ALT 변동 흔하고 약물 효과 제한적. 활성기 진입(ALT 지속 ↑ + HBV DNA ≥2,000) 후 시작.',
    'B형간염-수술전-예방': '대수술·항암·이식 환자에서 HBsAg + anti-HBc 1회 선별이 표준. HBsAg(+)이면 TDF/ETV 시작, anti-HBc(+) 단독이면 위험 stratify 후 결정. 미시행으로 인한 재활성화는 fulminant hepatic failure 사망 위험.',
    'B형간염-신기능저하-TAF전환': 'TDF의 신·골 부작용은 누적 — eGFR <50 또는 골밀도 T-score <−2.5면 TAF 전환. 한국에서 TAF 급여는 2018년부터 — 그 이전 ETV 환자는 신기능 정상이면 ETV 유지가 비용 효율적.',
    'ETV-TAF-전환': 'ETV → TAF 전환 RCT(한국, GnL 2026)에서 12개월 시점 HBV DNA 억제율 동등. 신기능·골밀도 우려 시 전환 합리적이지만 비용 차이 작지 않음(TAF 약 2배). 환자별 결정.',
    'HBeAg-seroclearance-약중단': 'HBeAg 소실 + HBV DNA(−) + ALT 정상을 12개월 consolidation 후 중단 시도 — 5년 재발률 약 30–50%. 한국 가이드라인은 중단 후 첫 3개월 매월 ALT·HBV DNA 추적 권장.',
    '항암치료전-재활성화예방': 'Rituximab 같은 강한 B세포 표적 치료에서 HBsAg(+) 환자의 재활성화율은 prophylaxis 없으면 30–60%. TDF/ETV로 1–2% 미만으로 떨어짐 — NNT 매우 낮음.',
    '직장검진-HBsAg양성': '한국 일반 인구 HBsAg(+) 약 3% (1980년대 8%에서 백신 정책으로 감소). 우연 발견 시 HBeAg·DNA·간기능·초음파 평가 → 치료 적응 여부 결정. 가족 검사 + 백신 동반 필수.',
    '임신중-HBsAg발견': '임신 28주에 HBV DNA ≥2×10⁵ IU/mL이면 모자감염 예방을 위해 TDF 추가 시작 권장. 출산 후 신생아는 12시간 내 HBIG + 백신. 한국 신생아 예방접종 적용으로 모자감염률 0.5% 미만.',

    # C형간염
    'anti-HCV양성-첫발견': 'anti-HCV 양성 후 HCV RNA(−)는 자연 완치(약 25%) 또는 위양성. RNA(+) 확진까지 진단 보류. 한국 HCV 유병률 약 0.6% — 미진단자 추정 약 15만 명, 1회 검진으로 발견되는 비율 늘고 있음.',
    'C형간염-DAA실패-재치료': '1차 DAA 실패 후 SOF/VEL/VOX 12주 → SVR 약 95%. 간경변 동반 시 ribavirin 추가 권장. 한국에서는 일부 보험 적용 제한 — 사전 평가 필요.',
    'C형간염-HIV동반-동시치료': 'HIV-HCV 동시감염에서 DAA 효과는 단독감염과 동일 (SVR ≥95%). 주요 함정은 ART와의 상호작용 — efavirenz는 대부분 DAA와 충돌. 동시 치료 가능 (한 외래에서 결정).',
    'C형간염-간경변-새결절': 'HCV SVR 후도 간경변이 잔존하면 HCC 위험 평생 지속 (연간 약 1–2%). 6개월 검진(초음파 + AFP) 평생 유지. SVR 자체가 HCC 위험을 완전히 제거하지 않음.',
    'C형간염-임신중-발견': '임신 중 DAA 안전성 데이터 부족 — 일반적으로 미권장. 모자감염률 5% (HCV RNA(+)), HIV 동시감염 시 10–20%로 ↑. 영아 검사는 18개월 anti-HCV 또는 2개월 RNA(고위험군).',
    'C형간염-재감염': 'DAA 완치 후 재감염률은 일반 인구 <0.5%, 주사 약물 사용자 5–10%/년, HIV 동시감염 MSM 3–8%/년. 위해감소 교육 + 매년 추적이 표준.',
    'C형간염-혈액투석-치료': '혈액투석 환자에서 GLE/PIB 12주(투석 일정 무관, 매일) → SVR 95%. SOF 기반 regimen은 신독성 우려로 회피 권장.',

    # MASLD / MASH
    '검진ALT상승-MASLD진단': '검진 ALT 상승의 70%가 MASLD. 진단 핵심: 초음파 echogenic + 대사위험 ≥1개 + 다른 원인 배제. AST/ALT >1이면 진행된 섬유화 의심 — Fibroscan으로 확인.',
    '검진ALT상승-원인감별': 'ALT >2× ULN 지속 시 단순 MASLD로 단정 금물. HBsAg·anti-HCV·자가면역(ANA·SMA·LKM)·Wilson(ceruloplasmin)·α1AT·셀리악 검사 1회는 표준. 보충제·한약 복용도 반드시 문진.',
    'lean-MASLD-비만없음': 'Lean MASLD(BMI <25)는 한국·일본에서 전체 MASLD의 약 20%. PNPLA3 rs738409 변이가 큰 기여 — 같은 BMI에서 동양인이 더 위험. 비만 없어도 F3 이상 진행 가능.',
    'MASLD-F2-GLP1시작': 'F2 이상 + 당뇨 동반 시 semaglutide 1.0 mg/주 또는 tirzepatide. 간 지방 약 40–50% 감소, MASH 관해 약 60%. 한국 급여는 당뇨 적응만 — MASLD 단독 처방 자비.',
    'MASH-F3-당뇨-종합관리': 'F3는 pre-cirrhosis — 5년 내 약 30%가 F4 진행. 강한 다중 개입 필요: 체중 10% 감량 + GLP-1 + 스타틴(CVD) + 당뇨 강화. 6개월마다 Fibroscan 추적.',
    'MASLD-비만수술-회복': '비만수술 후 1–5년 시점 MASH 관해 50–80%, 섬유화 호전 약 30–40%. Child A 간경변 환자에서도 안전성 데이터 누적 중 — 그러나 응고·출혈 위험으로 신중.',
    'MASLD-수면무호흡-CPAP개선': 'MASLD 환자의 약 50%에서 OSA 동반. CPAP 치료로 ALT·인슐린저항 호전 일부 보고. 야간 산소 desaturation이 간 섬유화의 독립적 위험 인자.',
    'MASLD-심혈관-종합관리': 'MASLD 환자 사망원인 1위는 간 합병증이 아닌 심혈관(약 40%). 따라서 LDL·BP·HbA1c 관리가 간만큼 중요. 스타틴은 MASLD에서 오히려 간 보호 — ALT 3× ULN 이하면 시작·지속.',
    'MASLD-청소년-가족력': '비만 청소년의 약 25–40%에 MASLD. 가족력 있으면 9세부터 ALT 선별(남 >25, 여 >22). 소아 승인 약 없음 — 체중 7–10% 감량 + 가당음료 ↓가 1차.',
    'MetALD-당뇨-음주': '2023 새 분류: 여 140–350 g/주, 남 210–420 g/주 + 대사위험 = MetALD. 알코올 단독(ALD)과 MASLD의 중간. 음주 줄이기 + 대사 관리 모두 필요 — 한쪽만 해결로는 불충분.',
    'resmetirom-신약시작': '2024년 3월 FDA 가속 승인 첫 MASH 약 (F2–F3). MAESTRO-NASH에서 MASH 관해 약 30% (위약 10%), 섬유화 1단계 호전 26%. 한국 미도입 — 2027–28년 예상.',

    # AIH / autoimmune
    'AIH-PBC-overlap-진단': 'Paris criteria: AIH 2/3 (ALT ≥5×, IgG ≥2× 또는 SMA(+), interface hepatitis) + PBC 2/3 (ALP ≥2× 또는 GGT ≥5×, AMA(+), florid duct lesion). 모두 충족 시 UDCA + 면역억제 병용.',
    'AIH-급성간부전': 'AIH 급성간부전(INR ≥1.5 + 간뇌증)에서 스테로이드 시도(5–7일) → 무반응 시 즉시 이식. 스테로이드 효과 없음에도 시간 끄는 것이 가장 위험한 함정.',
    'AIH-소아청소년-진단': '소아 AIH의 약 50%에서 MRCP 이상 → autoimmune sclerosing cholangitis(ASC). 따라서 모든 소아 AIH에서 진단 시 MRCP 1회 권장 — 성인은 PSC overlap <10%로 차이 큼.',
    'AIH-스테로이드-당뇨발생': '장기 스테로이드 환자의 약 30%에서 스테로이드 유발 당뇨. AZA 추가로 prednisolone 5–10 mg 유지(spareing)가 표준. 칼슘 + Vit D + DEXA 1년 추적 필수.',
    'AIH-약중단-재발': '3년 이상 관해 + 정상 IgG + 정상 생검 시 중단 시도 가능. 그러나 중단 후 재발률 50–90% — 평생 유지가 더 흔한 선택. 중단 시도는 환자와 충분한 상의 후.',
    'AIH-임신중-약물전환': 'MMF(mycophenolate)는 기형 위험 명확 — 임신 6주 전 중단 + AZA로 전환. AZA는 임신 D 등급이지만 임상에서 안전성 누적 — 지속 권장. Prednisolone 5–10 mg 유지도 안전.',
    'AIH-첫진단-여성': 'AIH 30–50대 여성 우세(F:M 4:1). Type 1(anti-SMA, anti-soluble liver antigen) 우세. IAIHG simplified score ≥6 = probable, ≥7 = definite — 한국 임상에서 가장 널리 사용.',
    '자가면역간염-첫진단': 'AIH 진단의 50%가 ALT 50–200 만성 상승으로 우연 발견. IgG 상승 + ANA/SMA(+) + 다른 원인 배제 + 생검(interface hepatitis)이 표준. 생검이 결정적 — 자가항체 음성도 약 15%.',

    # 간양성종양 / lesions
    '임신중-혈관종확대': '임신 중 호르몬 변화로 혈관종이 일시적으로 ↑ 가능(약 10–20%). 출산 후 대부분 원래 크기로 복귀. 임신 중 영상 1회(MRI) + 출산 후 3개월 추적.',
    'focal-fat-sparing-PET': '국소 지방 변화는 PET에서 위양성 흔함 — 정상 간실질도 18F-FDG 흡수 일정. MRI in/out-of-phase가 더 신뢰. CT 단독으로는 HCC 감별 어려워 MRI 권장.',
    'bile-duct-hamartoma-우연발견': '담관과오종(BDH) = 1.5 cm 미만 양엽 다발성 결절. MRCP에서 담관과 연결 — 결정적 진단 단서. 추적 불필요, 증상도 거의 없음. 전이성 결절과 가장 흔한 감별.',
    'NRH-진단': '결절성 재생증식(NRH)은 자가면역질환·HIV·thiopurine 사용자에서 흔함. 간기능은 보존되지만 비-경변성 문맥고혈압의 원인. 정맥류 평가 필수, 간이식까지 검토되는 경우 있음.',
    '큰낭종-bleomycin-경화요법': '5 cm 이상 증상있는 단순 낭종에서 bleomycin/ethanol 경화요법 → 약 70–80% 크기 ↓. 흡인만으로는 재발률 ↑. 다발성 PCLD는 다른 접근 필요.',

    # 간수치 / 검사
    'ALT일과성상승-격렬한운동': '격렬한 운동(마라톤·웨이트) 후 ALT 2–5× ULN까지 상승, CK 동반. 1–2주 휴식 후 정상화. AST/ALT >1 + CK ↑ 패턴 — 근육 기원 확인되면 추가 검사 불필요.',
    'AST우세-근육질환배제': 'AST/ALT >1이고 CK ≥1000이면 근육 기원 우선 — 횡문근융해, 다발근염, 스타틴 부작용. ALT는 근육에서 적게 발현 — AST 단독 ↑이면 거의 무조건 근육 평가.',
    '만성경증ALT상승-원인불명': 'ALT 40–80 만성 상승의 흔한 원인: MASLD > 음주 > 한약/보충제 > 갑상선·셀리악 > 자가면역. 1회는 ANA·anti-SMA·anti-LKM, ceruloplasmin, tTG-IgA까지 확장 검사.',
    '보충제-ALT상승': '한국 약물성 간 손상(DILI)의 30–40%가 한약·건강기능식품. 녹용·홍삼·관절약(글루코사민)·다이어트 보조제 흔함. ALT 정상화까지 평균 4–8주 — 재섭취는 금기.',
    '약물성간손상-항결핵제': 'INH·RIF·PZA 모두 간독성. 첫 2개월에 약 5–10%에서 ALT 상승, 약 1%에서 ALT >5× ULN. 첫 2개월은 2주마다 ALT 추적이 표준. ALT >5× 또는 >3× + 증상이면 약물 중단.',
    '독성간염-야생버섯': '아마니타(Amanita phalloides) 중독은 24–48시간 잠복기 후 급성 간부전. N-acetylcysteine + silibinin + 조기 이식 평가. 잠복기 때문에 환자도 의료진도 늦게 인지.',
    '임신중-ALT상승-감별': '임신 specific 원인: HELLP(혈소판 ↓ + 용혈), AFLP(저혈당 + 응고병증), 자간전증, 임신성 간내 담즙정체(가려움증 + 담즙산 ↑). 비-임신 원인(바이러스·자가면역)도 동시 평가.',
    '소아청소년-검진ALT상승': '소아 ALT 상한은 NASPGHAN 권고 — 남 25, 여 22 U/L (성인 40과 다름). 지속 상승 시 B/C형 간염·Wilson·자가면역·α1AT 결핍 1회 평가 표준.',

    # 기타 / 특수
    '혈소판저하-romiplostim': 'TPO-RA(avatrombopag, lusutrombopag)는 시술 5–8일 전 시작 → 혈소판 ≥50 K. Romiplostim도 같은 계열이지만 한국 간 시술 적응 미승인 — 혈액과 협진 후 off-label.',
    'Sarcopenia-운동개선': '간경변에서 sarcopenia 유병률 30–70%. SARC-F 또는 BIA로 선별. 단백 1.2–1.5 g/kg + 저녁 늦은 간식(밤 단식 피하기) + 저항 운동 주 2–3회. 6개월에 근육량 5–10% 회복 가능.',
    'B형간염-Occult-항암치료': 'Occult HBV(HBsAg(−), anti-HBc(+))에서 rituximab 항암 시 재활성화율 약 10–20%, HBV DNA 양성이면 30–50%. anti-HBc(+) 모든 항암 환자에서 prophylaxis 권장.',
}


CASE_DIR = ROOT / '케이스'


def make_block(slug: str, text: str) -> str:
    return (
        f'{MARK_START}\n'
        '<aside class="case-pearl">\n'
        '  <span class="case-pearl-label">임상 트리비아</span>\n'
        f'  <p>{text}</p>\n'
        '</aside>\n'
        f'{MARK_END}'
    )


def main():
    written = 0
    missing = []
    for slug, content in TRIVIA.items():
        idx = CASE_DIR / slug / 'index.html'
        if not idx.exists():
            missing.append(slug)
            continue
        text = idx.read_text(encoding='utf-8')
        block = make_block(slug, content)
        if MARK_START in text:
            new = BLOCK_RE.sub(block + '\n', text)
        else:
            # Insert before teaching-box, else before disclaimer, else before tags
            target = None
            for marker in ['<div class="teaching-box"',
                           '<p class="disclaimer"',
                           '<!-- tags -->']:
                i = text.find(marker)
                if i != -1:
                    target = i
                    break
            if target is None:
                continue
            new = text[:target] + block + '\n' + text[target:]
        if new != text:
            idx.write_text(new, encoding='utf-8')
            written += 1
    print(f'Pearl written: {written}')
    if missing:
        print(f'Missing slugs: {len(missing)}')
        for s in missing:
            print(f'  {s}')


if __name__ == '__main__':
    main()
