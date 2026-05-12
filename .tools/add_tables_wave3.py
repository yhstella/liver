#!/usr/bin/env python3
"""Wave 3: 1-table 페이지에 두 번째 표 추가 — 명확한 비교/분류 가치 있는 페이지 한정."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

T = {
    "B형간염-HBeAg-양성-음성": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">HBeAg 상태별 치료 적응증</caption>
<thead><tr><th>HBeAg 상태</th><th>치료 시작 기준</th><th>지속·중단 기준</th></tr></thead>
<tbody>
<tr><td>HBeAg(+) (면역활성기)</td><td>HBV DNA ≥20,000 IU/mL + ALT &gt;ULN 또는 섬유화</td><td>HBeAg seroconv + DNA(−) 후 12개월 consolidation</td></tr>
<tr><td>HBeAg(−) (면역회피기)</td><td>HBV DNA ≥2,000 IU/mL + ALT &gt;ULN 또는 섬유화</td><td>대체로 평생 (HBsAg loss 시 중단 검토)</td></tr>
<tr><td>면역관용기 (HBeAg+, ALT 정상)</td><td>일반적으로 치료 안 함</td><td>6–12개월 ALT·DNA 추적</td></tr>
<tr><td>비활성 보균자 (HBeAg−, DNA 낮음)</td><td>치료 불필요</td><td>6–12개월 추적, HCC 검진</td></tr>
<tr><td>간경변 동반</td><td>HBeAg 무관, DNA 검출되면 즉시 시작</td><td>평생 지속</td></tr>
</tbody></table>''',

    "B형간염-백신": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">HBV 백신 — 무반응자(non-responder) 관리</caption>
<thead><tr><th>상황</th><th>대응</th></tr></thead>
<tbody>
<tr><td>1차 3회 접종 후 anti-HBs &lt;10 mIU/mL</td><td>3회 재접종 (booster series)</td></tr>
<tr><td>재접종 후도 무반응</td><td>true non-responder — 더 이상 추가 접종 불필요</td></tr>
<tr><td>이중 용량 접종 (Engerix-B 40 μg)</td><td>고위험·면역억제 환자: 0–1–2–6개월</td></tr>
<tr><td>HepB-CpG (Heplisav-B)</td><td>2회 접종 (0, 1개월), 무반응자에 효과</td></tr>
<tr><td>의료종사자 무반응</td><td>HBIG 2회 (24시간 + 1개월) — 노출 시 권고</td></tr>
<tr><td>면역억제 시 anti-HBs 유지</td><td>매년 anti-HBs 측정, &lt;10이면 booster</td></tr>
</tbody></table>''',

    "C형간염-신부전-치료": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">신기능별 DAA 약제 선택</caption>
<thead><tr><th>eGFR (mL/min)</th><th>1차 권장 regimen</th><th>주의사항</th></tr></thead>
<tbody>
<tr><td>≥30</td><td>SOF/VEL 또는 GLE/PIB</td><td>일반 용량</td></tr>
<tr><td>15–29</td><td>GLE/PIB 또는 SOF/VEL (단기 안전)</td><td>SOF 장기 사용 시 신독성 모니터</td></tr>
<tr><td>&lt;15 (HD 포함)</td><td>GLE/PIB (12주)</td><td>SOF는 가능하면 회피, 부득이 시 단기</td></tr>
<tr><td>혈액투석 중</td><td>GLE/PIB 100/40 mg × 12주</td><td>투석 일정과 무관하게 매일</td></tr>
<tr><td>이식 후</td><td>SOF/VEL 또는 GLE/PIB</td><td>면역억제제 농도 모니터</td></tr>
</tbody></table>''',

    "간경변-혈소판감소": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">TPO-RA — 시술 전 혈소판 보강</caption>
<thead><tr><th>약물</th><th>용량·스케줄</th><th>목표</th></tr></thead>
<tbody>
<tr><td>Avatrombopag</td><td>혈소판 40–50 K: 60 mg/일 × 5일 / &lt;40 K: 40 mg/일 × 5일</td><td>시술 5–8일 전 시작, 목표 ≥50 K</td></tr>
<tr><td>Lusutrombopag</td><td>3 mg/일 × 7일</td><td>시술 9–13일 전 시작, 목표 ≥50 K</td></tr>
<tr><td>혈소판 수혈</td><td>1단위/10 kg</td><td>응급 시 즉각 (TPO-RA 효과는 5–7일 필요)</td></tr>
<tr><td>금기</td><td>혈전 위험 (문맥혈전·이전 VTE)</td><td>대체로 단기 사용은 안전하나 평가 필요</td></tr>
<tr><td>일반 출혈 위험</td><td>혈소판 &lt;30 K이면 출혈 위험 ↑</td><td>침습 시술 전 보강 권장</td></tr>
</tbody></table>''',

    "간수치-검진주기-결정": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">위험도별 간 검진 주기</caption>
<thead><tr><th>대상</th><th>주기</th><th>핵심 검사</th></tr></thead>
<tbody>
<tr><td>일반 성인 (저위험)</td><td>2년</td><td>국가검진 ALT + 본인 인지 위험 시 추가</td></tr>
<tr><td>대사위험 ≥1 (당뇨·BMI≥25·이상지질)</td><td>1년</td><td>ALT·AST·γGT, FIB-4 계산</td></tr>
<tr><td>B형간염 비활성 보균</td><td>6–12개월</td><td>ALT, HBV DNA, AFP, 초음파</td></tr>
<tr><td>간경변 (모든 원인)</td><td>6개월</td><td>AFP + 초음파 (KLCA-NCC: AFP + PIVKA-II + 초음파)</td></tr>
<tr><td>B형간염 + 위험 (가족력·40세↑·남)</td><td>6개월</td><td>좌동</td></tr>
<tr><td>이식 후</td><td>3개월</td><td>면역억제제 농도 + 간기능</td></tr>
</tbody></table>''',

    "간암-TACE-종류-결정": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">cTACE vs DEB-TACE — 임상 선택</caption>
<thead><tr><th>항목</th><th>cTACE (lipiodol)</th><th>DEB-TACE</th></tr></thead>
<tbody>
<tr><td>약물 전달</td><td>유리 doxorubicin + lipiodol</td><td>DC bead 안에 doxorubicin 결합</td></tr>
<tr><td>약물 농도 곡선</td><td>피크 후 빠르게 ↓</td><td>천천히 지속 방출 (60일)</td></tr>
<tr><td>전신 부작용</td><td>높음 (탈모·구토·골수억제)</td><td>낮음</td></tr>
<tr><td>치료 효과 (생존)</td><td>대등</td><td>대등</td></tr>
<tr><td>비용</td><td>저렴</td><td>높음</td></tr>
<tr><td>한국 급여</td><td>적용</td><td>일부 적용 (조건부)</td></tr>
<tr><td>큰 종양 (&gt;5 cm)</td><td>다회 분할 가능, 영상 추적 용이</td><td>1회 치료 효과적</td></tr>
</tbody></table>''',

    "간암-소작술-RFA-MWA": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">RFA vs MWA — 기술적 비교</caption>
<thead><tr><th>항목</th><th>RFA (고주파)</th><th>MWA (마이크로웨이브)</th></tr></thead>
<tbody>
<tr><td>에너지원</td><td>460–500 kHz 전류</td><td>900–2450 MHz 전자기파</td></tr>
<tr><td>치료 시간</td><td>10–30분/회</td><td>5–10분/회</td></tr>
<tr><td>최대 ablation 직경</td><td>3.5–4 cm (단일 probe)</td><td>5–6 cm (단일 probe)</td></tr>
<tr><td>혈관 효과 (heat sink)</td><td>혈관 근접 시 효과 ↓</td><td>덜 영향 받음</td></tr>
<tr><td>다발 종양</td><td>여러 probe 가능</td><td>여러 probe + 단일 ablation 큼</td></tr>
<tr><td>국소재발률</td><td>약 8–15%</td><td>약 5–10%</td></tr>
<tr><td>비용</td><td>저렴</td><td>비교적 비쌈</td></tr>
<tr><td>적응</td><td>&lt;3 cm, 2개 이하</td><td>≤5 cm 단일, 다발 가능</td></tr>
</tbody></table>''',

    "간암-SBRT-양성자": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">SBRT vs 양성자 — HCC 적용 비교</caption>
<thead><tr><th>항목</th><th>SBRT (X-선)</th><th>양성자 치료</th></tr></thead>
<tbody>
<tr><td>물리 특성</td><td>입구·출구선량 있음</td><td>Bragg peak — 종양 너머 선량 거의 없음</td></tr>
<tr><td>적응</td><td>3–5 cm 이하, 혈관 근접</td><td>5 cm 이상, 간 기능 보존 더 필요할 때</td></tr>
<tr><td>치료 횟수</td><td>3–10회 분할</td><td>10–15회 분할</td></tr>
<tr><td>국소 통제율 (2년)</td><td>85–95%</td><td>90–95%</td></tr>
<tr><td>비표적 간 보호</td><td>일부 (10 Gy 이내 간 부피 제한)</td><td>매우 우수</td></tr>
<tr><td>비용</td><td>SBRT &lt; 양성자</td><td>약 2–3배 높음</td></tr>
<tr><td>한국 급여</td><td>일부 (조건부)</td><td>제한적 — 일부 센터·소아·재발</td></tr>
</tbody></table>''',

    "간양성종양-혈관종": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">혈관종 — 영상 진단과 추적</caption>
<thead><tr><th>크기·상황</th><th>표준 검사</th><th>추적 주기</th></tr></thead>
<tbody>
<tr><td>&lt;3 cm 전형적</td><td>초음파 + CT 또는 MRI 한 번</td><td>5년 후 1회 (변화 거의 없음)</td></tr>
<tr><td>3–10 cm 전형적</td><td>MRI (T2 강한 신호 + 주변 nodular 조영증강)</td><td>1년 후 1회, 안정 시 종결</td></tr>
<tr><td>&gt;10 cm (거대)</td><td>MRI 확진</td><td>1년 영상 + 증상 모니터</td></tr>
<tr><td>영상 비전형</td><td>MRI 또는 조영초음파 (CEUS)</td><td>HCC 배제까지 6개월</td></tr>
<tr><td>임신 계획</td><td>크기 변화 가능 — 임신 중 1회 영상</td><td>출산 후 3개월 영상</td></tr>
<tr><td>증상·출혈·꼬임</td><td>응급 평가</td><td>색전·절제 검토</td></tr>
</tbody></table>''',

    "자가면역간염-스테로이드-부작용": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">스테로이드 — 시기별 모니터링</caption>
<thead><tr><th>기간</th><th>주요 모니터링</th><th>예방 약물</th></tr></thead>
<tbody>
<tr><td>치료 시작</td><td>혈당·BP·HbA1c, 안과(녹내장·백내장), 골밀도</td><td>칼슘 1000–1200 mg + Vit D 800–2000 IU/일</td></tr>
<tr><td>1–3개월</td><td>혈당 4주, BP 매주, ALT 4주</td><td>비스포스포네이트 (T-score ≤-1.5)</td></tr>
<tr><td>3–12개월</td><td>HbA1c·BP 분기, DEXA 6–12개월</td><td>위장 보호 (PPI), AZA 추가로 스테로이드 감량</td></tr>
<tr><td>&gt;1년</td><td>안과 연 1회, 골밀도 1–2년</td><td>전체 약 감량 전략 (AZA 단독 유지 고려)</td></tr>
<tr><td>중단 시</td><td>HPA axis 평가 (필요 시 cortisol)</td><td>점진적 감량 (5 mg/주)</td></tr>
<tr><td>응급 상황</td><td>감염·외상·수술 시 stress dose</td><td>—</td></tr>
</tbody></table>''',

    "지방간-SGLT2-GLP1": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">SGLT2-i vs GLP-1 RA — MASLD 측면 비교</caption>
<thead><tr><th>항목</th><th>SGLT2 inhibitor</th><th>GLP-1 RA</th></tr></thead>
<tbody>
<tr><td>대표 약물</td><td>Empagliflozin, Dapagliflozin</td><td>Semaglutide, Tirzepatide</td></tr>
<tr><td>체중 감량</td><td>2–4 kg</td><td>5–15 kg (tirzepatide 더 큼)</td></tr>
<tr><td>간 지방 감소</td><td>약 25–35%</td><td>약 40–50%</td></tr>
<tr><td>MASH 관해 자료</td><td>표적 임상 일부</td><td>semaglutide phase 3 양성</td></tr>
<tr><td>섬유화 개선</td><td>일부 보고</td><td>tirzepatide 일부 양성 데이터</td></tr>
<tr><td>심혈관 효과</td><td>심부전·신장 보호</td><td>ASCVD 위험 ↓</td></tr>
<tr><td>주요 부작용</td><td>비뇨생식기 감염, DKA (당뇨)</td><td>오심·구토·췌장염</td></tr>
<tr><td>한국 급여 (당뇨)</td><td>적용</td><td>적용 (제한 조건)</td></tr>
</tbody></table>''',

    "지방간-신약-resmetirom": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">Resmetirom — MAESTRO-NASH 핵심 결과</caption>
<thead><tr><th>endpoint (54주)</th><th>위약</th><th>Resmetirom 80 mg</th><th>Resmetirom 100 mg</th></tr></thead>
<tbody>
<tr><td>MASH 관해 (섬유화 악화 없이)</td><td>10%</td><td>26%</td><td>30%</td></tr>
<tr><td>섬유화 ≥1단계 호전 (MASH 악화 없이)</td><td>14%</td><td>24%</td><td>26%</td></tr>
<tr><td>LDL-콜레스테롤 변화</td><td>+0%</td><td>−14%</td><td>−16%</td></tr>
<tr><td>간 지방 (MRI-PDFF) 감소 ≥30%</td><td>14%</td><td>50%</td><td>59%</td></tr>
<tr><td>주요 부작용</td><td colspan="3">설사 (27% vs 16%), 오심 (20% vs 11%)</td></tr>
<tr><td>FDA 승인</td><td colspan="3">2024년 3월 (MASH + F2–F3, 가속 승인)</td></tr>
<tr><td>한국 도입</td><td colspan="3">2026년 현재 미승인</td></tr>
</tbody></table>''',

    "지방간염-MASH": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">생검 — NAS score와 섬유화 stage</caption>
<thead><tr><th>요소</th><th>점수</th><th>설명</th></tr></thead>
<tbody>
<tr><td>지방증</td><td>0–3</td><td>0=&lt;5%, 1=5–33%, 2=34–66%, 3=&gt;66%</td></tr>
<tr><td>소엽 염증</td><td>0–3</td><td>200× 시야당 염증 focus</td></tr>
<tr><td>풍선변성</td><td>0–2</td><td>0=없음, 1=일부, 2=많음</td></tr>
<tr><td>NAS 합계</td><td>0–8</td><td>≥4 + 풍선변성 ≥1 = MASH</td></tr>
<tr><td>섬유화 F0</td><td>—</td><td>없음</td></tr>
<tr><td>섬유화 F1</td><td>—</td><td>지대 주변 또는 정맥 주변</td></tr>
<tr><td>섬유화 F2</td><td>—</td><td>유의미 (significant)</td></tr>
<tr><td>섬유화 F3</td><td>—</td><td>가교 (bridging)</td></tr>
<tr><td>섬유화 F4</td><td>—</td><td>간경변</td></tr>
</tbody></table>''',

    "간양성종양-담관과오종": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">담관과오종(BDH) — 영상·감별</caption>
<thead><tr><th>특징</th><th>BDH</th><th>전이성 결절</th><th>간낭종</th></tr></thead>
<tbody>
<tr><td>크기</td><td>&lt;15 mm 다발 (전형)</td><td>다양</td><td>다양</td></tr>
<tr><td>분포</td><td>양엽 미만성</td><td>다발 가능</td><td>국소·다발</td></tr>
<tr><td>초음파</td><td>저에코 작은 결절</td><td>저에코 결절</td><td>무에코 (anechoic)</td></tr>
<tr><td>CT 조영</td><td>조영증강 미미</td><td>조영증강 명확</td><td>조영증강 없음</td></tr>
<tr><td>MRI T2</td><td>고신호, 분명한 경계</td><td>중등도 신호</td><td>매우 고신호</td></tr>
<tr><td>MRCP</td><td>담관과 연결 (특징)</td><td>비연결</td><td>비연결</td></tr>
<tr><td>임상 의의</td><td>증상 없음, 추적 불필요</td><td>원발 평가 필요</td><td>관리</td></tr>
</tbody></table>''',
}

H2_RE = re.compile(r'<h2[^>]*>')


def main():
    changed = 0
    for slug, html in T.items():
        idx = ROOT / slug / 'index.html'
        if not idx.exists():
            print(f'  MISSING: {slug}')
            continue
        text = idx.read_text(encoding='utf-8')
        # Insert before second H2 (after first H2 section)
        h2s = list(H2_RE.finditer(text))
        if len(h2s) < 2:
            # Fallback: insert before related-auto or disclaimer
            m = re.search(r'<aside class="related-auto"|<p class="disclaimer"', text)
            if not m:
                print(f'  no insertion point: {slug}')
                continue
            insert_pos = m.start()
        else:
            insert_pos = h2s[1].start()
        new = text[:insert_pos] + html + '\n\n' + text[insert_pos:]
        idx.write_text(new, encoding='utf-8')
        changed += 1
        print(f'  + {slug}')
    print(f'\nSecond tables added: {changed}')


if __name__ == '__main__':
    main()
