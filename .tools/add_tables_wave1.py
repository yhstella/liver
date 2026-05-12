#!/usr/bin/env python3
"""Wave 1: 0-table detail 페이지에 임상 표 1개씩 추가.

각 슬러그별로 페이지 주제에 맞는 표 HTML을 작성.
삽입 위치: TLDR 다음, 첫 <h2> 직전.
이미 표 있는 페이지는 skip.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 페이지별 표 HTML — 각 표는 임상 합리적 내용으로 직접 작성
TABLES = {
    "간암-식이-일상": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">간암 환자 식이 — 권장과 회피</caption>
<thead><tr><th>분류</th><th>권장</th><th>회피·주의</th></tr></thead>
<tbody>
<tr><td>단백질</td><td>체중 kg당 1.2–1.5 g (식물성·유제품 우선)</td><td>가공육, 과다한 적색육</td></tr>
<tr><td>탄수화물</td><td>통곡물, 콩류, 채소·과일</td><td>정제 탄수, 과당 음료, 과일 주스</td></tr>
<tr><td>지방</td><td>올리브유, 등푸른 생선(주 2–3회), 견과류</td><td>포화지방·트랜스지방 과다</td></tr>
<tr><td>음료</td><td>커피 2–4잔/일 (간 보호 효과 일부 보고)</td><td>알코올 일체, 고당분 음료</td></tr>
<tr><td>보충제·한약</td><td>의료진과 상의 후 결정</td><td>녹용·홍삼 포함 한약 (한국 DILI 30–40%)</td></tr>
<tr><td>운동</td><td>유산소 주 5회·30분 + 저항운동 주 2–3회</td><td>복수 심한 시기·치료 직후 강도 ↓</td></tr>
</tbody></table>''',

    "지방간-MetALD": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">2023 새 명칭 — 음주량 기준 분류</caption>
<thead><tr><th>분류</th><th>주간 음주량</th><th>대사 위험인자</th></tr></thead>
<tbody>
<tr><td>MASLD</td><td>여성 &lt;140 g · 남성 &lt;210 g</td><td>≥1개 (BMI·당뇨·고혈압·이상지질혈증 등)</td></tr>
<tr><td><strong>MetALD</strong></td><td>여성 140–350 g · 남성 210–420 g</td><td>≥1개 (MASLD와 동일)</td></tr>
<tr><td>ALD</td><td>여성 &gt;350 g · 남성 &gt;420 g</td><td>위험인자 무관</td></tr>
<tr><td>NAFLD (이전 명칭)</td><td>유의미한 음주 배제</td><td>요구 안 됨</td></tr>
</tbody></table>
<p class="fig-caption" style="font-size:12.5px;color:var(--muted);margin-top:-8px">대사이상 + 중간 정도 음주가 동반된 영역이 MetALD. 분자량 1잔(소주 1잔 ≈ 알코올 8 g, 맥주 500mL ≈ 16 g).</p>''',

    "간수치-AST-우세-원인": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">AST 우세 패턴 (AST/ALT 비) — 감별진단</caption>
<thead><tr><th>AST/ALT 비</th><th>원인 카테고리</th><th>대표 진단·검사</th></tr></thead>
<tbody>
<tr><td>&gt;2.0</td><td>알코올성 간 손상</td><td>음주력, GGT 상승, MCV ↑</td></tr>
<tr><td>&gt;1.0 + LDH·CK ↑</td><td>근육 기원 (운동·스타틴·근염)</td><td>CK, aldolase, 근전도</td></tr>
<tr><td>&gt;1.0 + 황달·복수</td><td>진행된 간경변</td><td>알부민·PT, 영상</td></tr>
<tr><td>매우 ↑ (&gt;1000)</td><td>허혈성 간 손상 / 급성 간염</td><td>혈역학, 바이러스 panel</td></tr>
<tr><td>&gt;1.0 + 용혈</td><td>적혈구 기원</td><td>빌리루빈·LDH·hapto</td></tr>
</tbody></table>''',

    "자가면역간염-임신": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">AIH 약물 — 임신 단계별 안전성</caption>
<thead><tr><th>약물</th><th>임신 전·중</th><th>수유</th><th>비고</th></tr></thead>
<tbody>
<tr><td>Prednisolone</td><td>안전 (저용량 유지)</td><td>안전</td><td>유지 5–10 mg 권장</td></tr>
<tr><td>Azathioprine</td><td>대체로 안전 (FDA D, 그러나 임상 사용 안전 증거 많음)</td><td>안전 (소량 분비)</td><td>임신 중 지속 가능</td></tr>
<tr><td>MMF (mycophenolate)</td><td><strong>금기</strong> (기형 위험)</td><td>금기</td><td>임신 6주 전 중단 + AZA 전환</td></tr>
<tr><td>Tacrolimus·Cyclosporine</td><td>필요 시 사용 가능</td><td>주의 (소량 분비)</td><td>혈중 농도 모니터</td></tr>
<tr><td>UDCA (overlap)</td><td>안전</td><td>안전</td><td>PBC overlap에 흔히 병용</td></tr>
</tbody></table>''',

    "간양성종양-경구피임약": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">OCP와 간 양성종양 — 위험 단계와 권고</caption>
<thead><tr><th>병변</th><th>OCP 관련성</th><th>OCP 중단 권고</th><th>크기 변화 모니터</th></tr></thead>
<tbody>
<tr><td>혈관종 (hemangioma)</td><td>약함</td><td>일반적으로 불필요</td><td>5 cm 이상 시 1년 추적</td></tr>
<tr><td>FNH</td><td>없음 (관련 없음)</td><td>불필요</td><td>1년 영상</td></tr>
<tr><td><strong>간 선종(HCA)</strong></td><td><strong>강함</strong> (5–10년 사용 시 위험 ↑)</td><td><strong>권장</strong></td><td>중단 후 6개월 영상</td></tr>
<tr><td>HCA β-catenin (+) 아형</td><td>관련 없으나 악성 위험 ↑</td><td>크기 무관 절제 검토</td><td>3개월 영상</td></tr>
</tbody></table>''',

    "간경변-감염-SBP-예방": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">자발성 세균성 복막염(SBP) 예방 — 1차 vs 2차</caption>
<thead><tr><th>예방 단계</th><th>적응 기준</th><th>표준 약물</th><th>기간</th></tr></thead>
<tbody>
<tr><td><strong>1차 예방</strong></td><td>복수 단백 &lt;1.5 g/dL + (Child-Pugh ≥9 또는 빌리루빈 ≥3 또는 BUN/Cr 상승)</td><td>Norfloxacin 400 mg/일 (Ciprofloxacin 대체)</td><td>위험인자 지속 동안</td></tr>
<tr><td>입원 환자 단기</td><td>정맥류 출혈</td><td>Ceftriaxone 1 g/일</td><td>7일</td></tr>
<tr><td><strong>2차 예방</strong></td><td>SBP 1회 이상 기왕력</td><td>Norfloxacin 400 mg/일</td><td>간이식까지 평생</td></tr>
<tr><td>예방 중 발열·복통</td><td>brake-through 의심</td><td>광범위 항생제 + 진단적 천자</td><td>—</td></tr>
</tbody></table>''',

    "C형간염-DAA-실패-재치료": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">DAA 실패 후 재치료 — 1차 regimen에 따라</caption>
<thead><tr><th>1차 실패 regimen</th><th>재치료 권고</th><th>치료 기간</th></tr></thead>
<tbody>
<tr><td>SOF/LDV, SOF/VEL, SOF + DCV</td><td>SOF/VEL/VOX</td><td>12주</td></tr>
<tr><td>GLE/PIB</td><td>SOF/VEL/VOX ± Ribavirin</td><td>12–16주</td></tr>
<tr><td>SOF/VEL/VOX 실패 (드뭄)</td><td>SOF + GLE/PIB ± Ribavirin (전문의 협진)</td><td>16–24주</td></tr>
<tr><td>NS5A 내성 변이 (+)</td><td>SOF + GLE/PIB + Ribavirin (검토)</td><td>16–24주</td></tr>
<tr><td>간경변 동반</td><td>위 regimen + Ribavirin 추가</td><td>+4–8주 연장</td></tr>
</tbody></table>
<p class="fig-caption" style="font-size:12.5px;color:var(--muted);margin-top:-8px">SOF/VEL/VOX = sofosbuvir/velpatasvir/voxilaprevir, GLE/PIB = glecaprevir/pibrentasvir. 한국 급여 기준 확인 필요.</p>''',

    "B형간염-결혼-임신": '''<table><caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">임신 단계별 — HBV 감염 산모 관리</caption>
<thead><tr><th>시기</th><th>핵심 결정</th><th>표준 권고</th></tr></thead>
<tbody>
<tr><td>임신 전</td><td>약 결정·예방접종</td><td>고바이러스혈증이면 TDF 시작. 배우자·자녀 anti-HBs 확인 + 백신.</td></tr>
<tr><td>1–2 삼분기</td><td>모니터링</td><td>ALT·HBV DNA 12주 간격. ETV·TAF는 데이터 적음 → TDF 우선.</td></tr>
<tr><td>3 삼분기 (28주∼)</td><td>모자감염 예방</td><td>HBV DNA ≥200,000 IU/mL이면 TDF 추가 또는 유지.</td></tr>
<tr><td>출산 직후 신생아</td><td>수직감염 차단</td><td>HBIG + 백신 12시간 내. 후속 백신 1·6개월.</td></tr>
<tr><td>출산 후 산모</td><td>약 지속·중단 결정</td><td>치료 적응 있으면 지속. 예방 목적이었다면 출산 후 4–12주에 중단 + 모니터.</td></tr>
<tr><td>수유</td><td>안전 평가</td><td>TDF 수유 시 안전. HBIG·백신 완료된 영아는 수유 가능.</td></tr>
</tbody></table>''',
}

# 삽입 위치 — TLDR 다음 첫 <h2> 직전
INSERT_RE = re.compile(r'(</div>\s*\n*)(\s*<h2)', re.MULTILINE)  # </div> after TLDR


def main():
    changed = 0
    for slug, table_html in TABLES.items():
        idx = ROOT / slug / 'index.html'
        if not idx.exists():
            print(f'  MISSING: {slug}')
            continue
        text = idx.read_text(encoding='utf-8')
        if '<table' in text:
            # 이미 표 있는 페이지: 다시 한 번 검사 (변환 후 채워졌을 수 있음)
            print(f'  SKIP (has table): {slug}')
            continue

        # TLDR </div> 다음 첫 <h2> 직전에 삽입
        m = re.search(r'(class="tldr">[^<]*(?:<[^/]+>[^<]*</[^>]+>[^<]*)*?</div>)', text)
        if m:
            insert_pos = m.end()
            new_text = text[:insert_pos] + '\n\n' + table_html + '\n' + text[insert_pos:]
        else:
            # Fallback: 첫 <h2> 직전
            m = re.search(r'<h2', text)
            if not m:
                print(f'  no h2/tldr: {slug}')
                continue
            new_text = text[:m.start()] + table_html + '\n\n' + text[m.start():]

        idx.write_text(new_text, encoding='utf-8')
        changed += 1
        print(f'  + {slug}')

    print(f'\nTables added: {changed}')


if __name__ == '__main__':
    main()
