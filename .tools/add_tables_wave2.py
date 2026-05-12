#!/usr/bin/env python3
"""Wave 2: 나머지 20 zero-table pages에 표 추가."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

T = {
    "B형간염-D형간염-HDV": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">D형간염(HDV) 검사·치료 — 핵심 정리</caption>
<thead><tr><th>항목</th><th>내용</th></tr></thead>
<tbody>
<tr><td>대상</td><td>HBsAg(+) 모든 환자 (1회는 anti-HDV 검사 권장)</td></tr>
<tr><td>초기 선별</td><td>anti-HDV total IgG</td></tr>
<tr><td>활동 감염 확인</td><td>HDV RNA PCR (anti-HDV 양성 시)</td></tr>
<tr><td>표준 치료</td><td>Pegylated IFN-α 48주 (지속 응답 ~25–30%)</td></tr>
<tr><td>신약</td><td>Bulevirtide (entry inhibitor, 유럽 승인. 한국 미도입)</td></tr>
<tr><td>임상 의미</td><td>HBV 단독 대비 간경변·HCC 진행 약 3배 빠름</td></tr>
</tbody></table>''',

    "B형간염-Occult-잠복감염": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">Occult B형간염(OBI) — 진단·임상 의의</caption>
<thead><tr><th>항목</th><th>내용</th></tr></thead>
<tbody>
<tr><td>정의</td><td>HBsAg 음성 + 혈청/간 HBV DNA 양성</td></tr>
<tr><td>혈청학 흔한 패턴</td><td>anti-HBc 양성 (anti-HBs ±)</td></tr>
<tr><td>검출 한계</td><td>혈청 HBV DNA &lt;200 IU/mL — 고감도 PCR 필요</td></tr>
<tr><td>임상 위험</td><td>면역억제 시 재활성화, 수혈/장기이식 시 감염원</td></tr>
<tr><td>모니터링 대상</td><td>항암·rituximab·이식 환자에서 HBV DNA + ALT 추적</td></tr>
<tr><td>예방 약물</td><td>고위험 면역억제 시 TDF/ETV 사전 투여</td></tr>
</tbody></table>''',

    "B형간염-소아청소년-치료": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">소아·청소년 HBV — 연령별 치료 접근</caption>
<thead><tr><th>연령</th><th>치료 적응</th><th>1차 약물</th></tr></thead>
<tbody>
<tr><td>&lt;2세</td><td>거의 안 함 (면역관용기, 자연 ALT 변동)</td><td>관찰</td></tr>
<tr><td>2–11세</td><td>ALT &gt;2× 상한 + HBV DNA ≥2,000 IU/mL 지속</td><td>ETV (≥2세), IFN 검토</td></tr>
<tr><td>12–17세</td><td>성인 기준 적용</td><td>TDF (12세 ≥35 kg), ETV, TAF (≥12세)</td></tr>
<tr><td>모자감염 영아</td><td>고바이러스혈증 산모 자녀 = 즉시 HBIG + 백신</td><td>치료 아닌 예방</td></tr>
<tr><td>치료 모니터</td><td>3개월 ALT·HBV DNA, 1년 anti-HBe seroconv</td><td>—</td></tr>
</tbody></table>''',

    "C형간염-HIV-동반": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">HIV-HCV 동시 감염 — DAA와 ART 상호작용</caption>
<thead><tr><th>DAA regimen</th><th>안전 ART</th><th>피해야 할 ART</th></tr></thead>
<tbody>
<tr><td>SOF/VEL</td><td>대부분 안전 (DTG, RAL, BIC, RPV, TAF)</td><td>Efavirenz (VEL 농도 ↓)</td></tr>
<tr><td>SOF/LDV</td><td>안전 (대부분)</td><td>TDF + atazanavir/r 또는 ritonavir-boosted PI 동시 사용 시 신장 모니터</td></tr>
<tr><td>GLE/PIB</td><td>안전 (DTG, RAL, RPV)</td><td>Efavirenz, EVG/c, ATV, DRV, LPV (효과 ↓)</td></tr>
<tr><td>SOF/VEL/VOX</td><td>안전 (대부분)</td><td>Efavirenz, NVP, ETV (VOX ↓)</td></tr>
<tr><td>완치 후 추적</td><td>매년 anti-HCV·HIV·STD 패키지</td><td>—</td></tr>
</tbody></table>''',

    "C형간염-임신수유": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">임신·수유 단계별 HCV 관리</caption>
<thead><tr><th>시기</th><th>치료·검사</th><th>비고</th></tr></thead>
<tbody>
<tr><td>임신 전</td><td>DAA 치료 완료 권장</td><td>완치 후 6개월 피임 (RBV 사용 시 6개월)</td></tr>
<tr><td>임신 중</td><td>DAA 일반적으로 미권장</td><td>SOF + ledipasvir 임상 자료 누적 중</td></tr>
<tr><td>출산</td><td>제왕절개 의무 아님</td><td>HCV RNA 고농도 + HIV 동시감염 시 검토</td></tr>
<tr><td>모자감염률</td><td>약 5% (HCV RNA 양성 산모)</td><td>HIV 동시감염 시 10–20%로 ↑</td></tr>
<tr><td>수유</td><td>일반적으로 안전</td><td>유두 손상·출혈 시 일시 중단</td></tr>
<tr><td>영아 검사</td><td>18개월 anti-HCV (그 이전은 모체 항체 잔존)</td><td>고위험 영아는 2개월 HCV RNA</td></tr>
</tbody></table>''',

    "C형간염-재감염-위험군": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">DAA 완치 후 재감염 — 위험군과 권고</caption>
<thead><tr><th>위험군</th><th>재감염률 (연간)</th><th>추적 권고</th></tr></thead>
<tbody>
<tr><td>일반 인구</td><td>&lt;0.5%</td><td>증상·간기능 이상 시 검사</td></tr>
<tr><td>주사 약물 사용자</td><td>5–10%</td><td>매년 HCV RNA + 위해감소 교육</td></tr>
<tr><td>HIV 동시감염 MSM</td><td>3–8%</td><td>6개월마다 HCV RNA + STD 패키지</td></tr>
<tr><td>혈액투석</td><td>1–3%</td><td>매년 HCV RNA + 감염관리 점검</td></tr>
<tr><td>교정시설</td><td>3–5%</td><td>출소 시 검사 + 위해감소 연결</td></tr>
</tbody></table>''',

    "간경변-수면-가려움증": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">간질환 가려움증(pruritus) — 단계별 치료</caption>
<thead><tr><th>단계</th><th>약물</th><th>주의·비고</th></tr></thead>
<tbody>
<tr><td>일반 관리</td><td>저자극 보습제 + 미온 샤워</td><td>매일 시작</td></tr>
<tr><td>1차 약물</td><td>Cholestyramine 4 g 1–4회/일</td><td>다른 약과 4시간 간격</td></tr>
<tr><td>2차</td><td>Rifampicin 150–300 mg 1–2회/일</td><td>간독성 모니터, ALT 4주마다</td></tr>
<tr><td>3차</td><td>Naltrexone 12.5–50 mg/일</td><td>아편 사용 환자 금기</td></tr>
<tr><td>4차</td><td>Sertraline 75–100 mg/일</td><td>SSRI, 점진적 증량</td></tr>
<tr><td>난치성</td><td>UV-B 광선치료, MARS, 간이식 검토</td><td>특수 센터</td></tr>
</tbody></table>''',

    "간경변-여행-항공-주의": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">간경변 환자 여행 — 사전 체크리스트</caption>
<thead><tr><th>항목</th><th>대상성 (Child A)</th><th>비대상성 (Child B·C)</th></tr></thead>
<tbody>
<tr><td>항공 여행</td><td>일반적으로 가능</td><td>의료진 상담 후 결정. 산소포화도 모니터.</td></tr>
<tr><td>고지대 (&gt;2500 m)</td><td>주의 — 간뇌증 악화 가능</td><td>권장하지 않음</td></tr>
<tr><td>예방접종</td><td>A·B형 간염, 폐렴구균, 인플루엔자, COVID</td><td>좌동 + 가능하면 출발 4주 전 완료</td></tr>
<tr><td>설사 예방</td><td>물·음식 위생 (감염 → SBP 위험)</td><td>광범위 항생제 처방 동반 (출발 전 상의)</td></tr>
<tr><td>약 지참</td><td>2배 분량 + 영문 처방전</td><td>좌동 + 응급연락처</td></tr>
<tr><td>DVT 예방</td><td>장시간 비행 시 압박스타킹·수분</td><td>이뇨제 사용 중이면 탈수 주의</td></tr>
</tbody></table>''',

    "간경변-피로감-증상관리": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">간경변 피로감 — 원인별 평가</caption>
<thead><tr><th>의심 원인</th><th>핵심 검사</th><th>중재</th></tr></thead>
<tbody>
<tr><td>빈혈</td><td>CBC, 페리틴, B12, 엽산</td><td>철 보충 신중 (간 부담), B12·엽산 보충</td></tr>
<tr><td>전해질 이상 (저나트륨)</td><td>Na, 삼투압</td><td>수분 제한, tolvaptan 검토</td></tr>
<tr><td>잠복 간성혼수</td><td>혈중 암모니아, 인지 검사</td><td>락툴로스, rifaximin</td></tr>
<tr><td>근감소증</td><td>BIA·DXA, 근력</td><td>단백 1.2–1.5 g/kg, 저항운동</td></tr>
<tr><td>갑상선 기능 저하</td><td>TSH, FT4</td><td>치료 시작 (자가면역 동반 흔함)</td></tr>
<tr><td>우울·수면장애</td><td>PHQ-9, 수면 일지</td><td>SSRI (sertraline), CBT</td></tr>
</tbody></table>''',

    "간수치-소아청소년-기준": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">소아·청소년 ALT — 연령·성별 정상 상한</caption>
<thead><tr><th>연령·성별</th><th>ALT 상한 (U/L)</th><th>비고</th></tr></thead>
<tbody>
<tr><td>0–12개월</td><td>약 60</td><td>생후 1–2개월 일시적 ↑ 흔함</td></tr>
<tr><td>1–9세</td><td>약 30</td><td>—</td></tr>
<tr><td>10–17세 남</td><td>약 25</td><td>NASPGHAN 권고</td></tr>
<tr><td>10–17세 여</td><td>약 22</td><td>NASPGHAN 권고</td></tr>
<tr><td>비만 동반</td><td>위 기준 동일</td><td>지속 ↑ 시 MASLD 평가</td></tr>
<tr><td>중요 감별</td><td>지속 ALT ↑ 시 B/C형간염, 윌슨, 자가면역, α1AT 결핍 검사</td><td>—</td></tr>
</tbody></table>''',

    "간암-방사선색전술": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">방사선색전술(TARE, Y-90) — 적응·금기</caption>
<thead><tr><th>항목</th><th>내용</th></tr></thead>
<tbody>
<tr><td>핵심 적응</td><td>BCLC B–C, 문맥혈전 동반 HCC, TACE 실패</td></tr>
<tr><td>병기 분포</td><td>단일 큰 종양 또는 문맥침범 (segmental 가능)</td></tr>
<tr><td>간 기능</td><td>Child-Pugh A, B7 일부 (B8–C 금기)</td></tr>
<tr><td>사전 평가</td><td>Tc-99m MAA 스캔으로 폐 션트 평가 (&lt;20%)</td></tr>
<tr><td>주요 부작용</td><td>피로 (30–50%), 복통, 발열, 방사선 간염, 방사선 폐렴</td></tr>
<tr><td>금기</td><td>폐 션트 &gt;20%, 비교정 위장관 션트, 비대상성 간경변</td></tr>
<tr><td>TACE와 비교</td><td>비슷한 효과, 부작용 ↓·1회 입원 짧음, 비용 ↑</td></tr>
</tbody></table>''',

    "간양성종양-NRH": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">결절성 재생증식(NRH) — 다른 결절과 감별</caption>
<thead><tr><th>특징</th><th>NRH</th><th>FNH</th><th>HCC</th></tr></thead>
<tbody>
<tr><td>크기</td><td>1–3 mm 다발</td><td>2–5 cm 단일</td><td>다양</td></tr>
<tr><td>분포</td><td>간 전체 미만성</td><td>국소</td><td>국소</td></tr>
<tr><td>중심 흉터</td><td>없음</td><td>있음 (특징)</td><td>없음</td></tr>
<tr><td>MRI/CT 조영</td><td>특이 패턴 없음</td><td>동맥기 강한 조영, 지연기 isointense</td><td>동맥기 ↑, 지연기 washout</td></tr>
<tr><td>AFP</td><td>정상</td><td>정상</td><td>↑ 가능</td></tr>
<tr><td>임상 의의</td><td>문맥고혈압 원인 (간기능은 보존)</td><td>관찰</td><td>치료 필요</td></tr>
<tr><td>흔한 배경</td><td>자가면역질환, 약물(thiopurine), HIV</td><td>OCP 무관</td><td>간경변·만성 간염</td></tr>
</tbody></table>''',

    "간양성종양-국소지방-변화": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">국소 지방 변화 vs HCC — 영상 감별 포인트</caption>
<thead><tr><th>영상 특징</th><th>Focal fat / focal sparing</th><th>HCC</th></tr></thead>
<tbody>
<tr><td>경계</td><td>지도형(geographic), 모호</td><td>구상, 비교적 명확</td></tr>
<tr><td>전형적 위치</td><td>4번 분절, 담낭 주변, 문맥 분지부</td><td>어디든</td></tr>
<tr><td>혈관 변형</td><td>없음 (혈관이 정상 통과)</td><td>종양 효과로 변위</td></tr>
<tr><td>MRI in/out-of-phase</td><td>지방은 out-of-phase에서 신호 ↓</td><td>변화 없음</td></tr>
<tr><td>조영증강 패턴</td><td>정상 간실질과 동일</td><td>동맥기 ↑, 지연기 washout</td></tr>
<tr><td>AFP·PIVKA-II</td><td>정상</td><td>↑ 가능</td></tr>
<tr><td>추적</td><td>1년 영상 (변화 거의 없음)</td><td>치료 필요</td></tr>
</tbody></table>''',

    "자가면역간염-PBC-overlap": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">AIH-PBC overlap — Paris 진단 기준 (2/3 충족)</caption>
<thead><tr><th>축</th><th>PBC 항목 (2/3)</th><th>AIH 항목 (2/3)</th></tr></thead>
<tbody>
<tr><td>1</td><td>ALP ≥2× ULN 또는 GGT ≥5× ULN</td><td>ALT ≥5× ULN</td></tr>
<tr><td>2</td><td>AMA 양성</td><td>IgG ≥2× ULN 또는 anti-SMA(+) 또는 anti-LKM-1(+)</td></tr>
<tr><td>3</td><td>간 생검 — 화환형(florid) 담관 손상</td><td>간 생검 — interface hepatitis</td></tr>
<tr><td>충족 기준</td><td colspan="2">PBC 2/3 + AIH 2/3 동시 만족 시 overlap 진단</td></tr>
<tr><td>표준 치료</td><td colspan="2">UDCA 13–15 mg/kg/일 + 면역억제 (prednisolone ± AZA)</td></tr>
<tr><td>모니터링</td><td colspan="2">3개월 ALT·ALP, 6개월 IgG·AMA</td></tr>
</tbody></table>''',

    "자가면역간염-급성간부전": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">AIH 동반 급성간부전 — 치료 분기점</caption>
<thead><tr><th>임상 양상</th><th>대응</th></tr></thead>
<tbody>
<tr><td>INR &lt;1.5, 간뇌증 없음</td><td>스테로이드 시도 (Pred 40–60 mg/일), 5–7일 반응 모니터</td></tr>
<tr><td>INR ≥1.5, 간뇌증 없음 (ALI)</td><td>스테로이드 + 면역억제 (AZA, MMF 검토), 이식센터 의뢰</td></tr>
<tr><td>간뇌증 동반 (ALF)</td><td>스테로이드 효과 제한적, 즉시 이식 평가</td></tr>
<tr><td>King's College 기준 충족</td><td>응급 이식 등록</td></tr>
<tr><td>스테로이드 부작용</td><td>감염 (특히 진균), 출혈, 패혈증 → 광범위 항생제 + PPI 동반</td></tr>
<tr><td>치료 무반응</td><td>3–5일 내 INR·빌리루빈 호전 없으면 이식 우선</td></tr>
</tbody></table>''',

    "자가면역간염-소아청소년": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">소아 AIH — 성인과 다른 점</caption>
<thead><tr><th>항목</th><th>소아 AIH</th><th>성인과 비교</th></tr></thead>
<tbody>
<tr><td>발현 양상</td><td>급성·전격성 비중 ↑ (30–40%)</td><td>성인은 만성형 우세</td></tr>
<tr><td>유형 분포</td><td>Type 2 (anti-LKM-1) 비중 ↑</td><td>성인은 Type 1 우세</td></tr>
<tr><td>PSC overlap (ASC)</td><td>약 50%에서 MRCP 이상 → 모든 소아 AIH MRCP 권장</td><td>성인 PSC overlap &lt;10%</td></tr>
<tr><td>1차 치료</td><td>Pred 1–2 mg/kg/일 (최대 60 mg) + AZA 1–2 mg/kg</td><td>성인은 30–40 mg에서 시작</td></tr>
<tr><td>관해 후 약 중단</td><td>2–3년 관해 + 정상 IgG + 정상 생검 시 시도</td><td>성인은 평생 유지 우세</td></tr>
<tr><td>장기 합병증</td><td>성장 지연, 골다공증, 사춘기 지연</td><td>—</td></tr>
</tbody></table>''',

    "지방간-비만수술": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">비만대사 수술 — MASLD/MASH에 미치는 효과</caption>
<thead><tr><th>변화 항목</th><th>수술 후 효과 (1–5년)</th></tr></thead>
<tbody>
<tr><td>지방증(steatosis)</td><td>70–90% 호전</td></tr>
<tr><td>지방간염(MASH)</td><td>50–80% 관해</td></tr>
<tr><td>섬유화</td><td>약 30–40% 호전 (F2 이상)</td></tr>
<tr><td>대표 적응 BMI</td><td>≥35 + MASH/섬유화 또는 ≥40</td></tr>
<tr><td>주의 사항</td><td>간경변 환자에서 출혈·간기능 악화 위험 ↑ → Child-Pugh A에 한정 검토</td></tr>
<tr><td>수술 종류</td><td>슬리브 위절제 (가장 흔함), 위우회 (당뇨 동반 시 우선)</td></tr>
<tr><td>장기 약물 단축</td><td>당뇨·고혈압 약 감량/중단 흔함</td></tr>
</tbody></table>''',

    "지방간-소아청소년-MASLD": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">소아·청소년 MASLD — 진단·관리 핵심</caption>
<thead><tr><th>항목</th><th>내용</th></tr></thead>
<tbody>
<tr><td>유병률</td><td>비만 소아의 25–40%</td></tr>
<tr><td>선별 검사</td><td>비만 + ≥9세 → ALT (남 &gt;25, 여 &gt;22 시 검사)</td></tr>
<tr><td>1차 검사</td><td>ALT·AST·γ-GT + 초음파 + 다른 원인 배제</td></tr>
<tr><td>섬유화 평가</td><td>FibroScan (≥6 kPa 의심), 의심 강하면 생검</td></tr>
<tr><td>기준 약</td><td>현재 소아 승인 약물 없음 — 생활습관이 1차</td></tr>
<tr><td>생활 목표</td><td>체중 7–10% 감량, 가당음료 ↓, 신체활동 ↑</td></tr>
<tr><td>추적</td><td>3–6개월 ALT·체중·BMI percentile, 1년 영상</td></tr>
</tbody></table>''',

    "지방간-수면무호흡-OSA": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">OSA와 MASLD — 양방향 관계</caption>
<thead><tr><th>항목</th><th>내용</th></tr></thead>
<tbody>
<tr><td>유병률</td><td>MASLD 환자의 약 50%에서 OSA 동반</td></tr>
<tr><td>병태 연결고리</td><td>간헐 저산소 → 산화스트레스 → 간 염증·섬유화</td></tr>
<tr><td>선별 도구</td><td>STOP-BANG (≥3점 의심), Epworth sleepiness scale</td></tr>
<tr><td>확진</td><td>polysomnography (수면다원검사)</td></tr>
<tr><td>치료</td><td>CPAP 1차, 체중 감량, 옆자세 수면</td></tr>
<tr><td>CPAP 효과</td><td>ALT·인슐린저항·간섬유화 호전 일부 보고</td></tr>
<tr><td>OSA 미치료 시</td><td>심혈관·당뇨·간섬유화 위험 모두 ↑</td></tr>
</tbody></table>''',

    "지방간-심혈관-CVD": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">MASLD — 심혈관 위험도 stratification</caption>
<thead><tr><th>위험 단계</th><th>지표</th><th>관리 전략</th></tr></thead>
<tbody>
<tr><td>저위험</td><td>F0–F1, 대사위험 0–1개, 정상 지질</td><td>생활습관 + 1년 추적</td></tr>
<tr><td>중간위험</td><td>F2 + 당뇨/고혈압 동반</td><td>스타틴 시작, BP·HbA1c 목표 강화</td></tr>
<tr><td>고위험</td><td>F3–F4 또는 ASCVD 점수 ≥7.5%</td><td>스타틴 강화, GLP-1·SGLT2 (당뇨), 아스피린 검토</td></tr>
<tr><td>매우 고위험</td><td>이전 심근경색/뇌졸중 또는 F4 + 당뇨</td><td>LDL &lt;55 목표, PCSK9 검토</td></tr>
<tr><td>스타틴 안전성</td><td>MASLD에서 안전 (오히려 간 위험 ↓)</td><td>ALT &lt;3× ULN이면 시작·지속</td></tr>
<tr><td>주된 사망원인</td><td>MASLD 환자에서 심혈관 사망 &gt; 간 사망</td><td>심혈관 관리가 더 큰 영향</td></tr>
</tbody></table>''',
}

def main():
    changed = 0
    for slug, html in T.items():
        idx = ROOT / slug / 'index.html'
        if not idx.exists():
            print(f'  MISSING: {slug}')
            continue
        text = idx.read_text(encoding='utf-8')
        if '<table' in text:
            print(f'  SKIP (has table): {slug}')
            continue
        m = re.search(r'(class="tldr">[^<]*(?:<[^/]+>[^<]*</[^>]+>[^<]*)*?</div>)', text)
        if m:
            pos = m.end()
            new = text[:pos] + '\n\n' + html + '\n' + text[pos:]
        else:
            m = re.search(r'<h2', text)
            if not m:
                print(f'  no h2: {slug}')
                continue
            new = text[:m.start()] + html + '\n\n' + text[m.start():]
        idx.write_text(new, encoding='utf-8')
        changed += 1
        print(f'  + {slug}')
    print(f'\nTables added: {changed}')


if __name__ == '__main__':
    main()
