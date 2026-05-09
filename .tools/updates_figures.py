"""Per-paper inline SVG figures for /updates/ pages.

For each paper slug, defines a topic-specific SVG visualizing the key result
(survival benefit, hazard ratio, primary endpoint, mechanism, etc.).

Inserted just before the </article> closing tag (i.e., after all note-sections,
before references). Marker-wrapped for idempotent re-runs.
"""

UPDATES_FIGURES = {
    # === Shin first-author papers ===
    "Shin-CIK-HCC-CII-2026": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="CIK 보조요법 9년 장기 무재발 생존 — RCT 연장 추적">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">CIK 보조요법 9년 장기 무재발 생존 (RCT 연장)</text>
<line x1="60" y1="180" x2="700" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<line x1="60" y1="50" x2="60" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<text x="48" y="184" text-anchor="end" font-size="11" fill="#5a5a5a">0%</text>
<text x="48" y="120" text-anchor="end" font-size="11" fill="#5a5a5a">50%</text>
<text x="48" y="60" text-anchor="end" font-size="11" fill="#5a5a5a">100% 무재발</text>
<text x="370" y="200" text-anchor="middle" font-size="11" fill="#5a5a5a">시간 (년)</text>
<g font-size="11" fill="#5a5a5a">
<text x="120" y="195" text-anchor="middle">0</text><text x="220" y="195" text-anchor="middle">2</text>
<text x="320" y="195" text-anchor="middle">4</text><text x="420" y="195" text-anchor="middle">6</text>
<text x="520" y="195" text-anchor="middle">8</text><text x="620" y="195" text-anchor="middle">9</text>
</g>
<path d="M120 50 L160 75 L210 105 L270 130 L340 142 L420 152 L500 158 L600 164 L660 167" fill="none" stroke="#1f6f5c" stroke-width="3"/>
<path d="M120 50 L160 90 L210 120 L270 145 L340 158 L420 168 L500 173 L600 176 L660 178" fill="none" stroke="#c9542b" stroke-width="3" stroke-dasharray="6 4"/>
<rect x="500" y="55" width="14" height="3" fill="#1f6f5c"/>
<text x="520" y="60" font-size="12" fill="#1f6f5c" font-weight="600">CIK 보조</text>
<rect x="500" y="73" width="14" height="3" fill="#c9542b"/>
<text x="520" y="78" font-size="12" fill="#c9542b" font-weight="600">대조군</text>
</svg>
<p class="fig-caption">9년 연장 추적에서 CIK 보조군의 무재발 이득이 후기까지 유지됩니다. (도식적 표현)</p>''',

    "Shin-AI-CT-HCC-CHB-JHep-2025": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AI-CT 모델의 HCC 위험 stratification — CHB 환자">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">AI-CT 위험 점수에 따른 HCC 누적 발생률 (CHB)</text>
<line x1="60" y1="180" x2="700" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<line x1="60" y1="50" x2="60" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<text x="48" y="184" text-anchor="end" font-size="11" fill="#5a5a5a">0%</text>
<text x="48" y="120" text-anchor="end" font-size="11" fill="#5a5a5a">15%</text>
<text x="48" y="60" text-anchor="end" font-size="11" fill="#5a5a5a">30% HCC</text>
<text x="370" y="200" text-anchor="middle" font-size="11" fill="#5a5a5a">시간 (년)</text>
<g font-size="11" fill="#5a5a5a">
<text x="120" y="195" text-anchor="middle">0</text><text x="240" y="195" text-anchor="middle">2</text>
<text x="360" y="195" text-anchor="middle">4</text><text x="480" y="195" text-anchor="middle">6</text>
<text x="600" y="195" text-anchor="middle">8</text>
</g>
<path d="M120 178 L210 165 L300 145 L390 120 L480 90 L580 60" fill="none" stroke="#c9542b" stroke-width="3"/>
<text x="600" y="55" font-size="11" fill="#c9542b" font-weight="600">AI 고위험</text>
<path d="M120 178 L210 175 L300 170 L390 162 L480 152 L580 138" fill="none" stroke="#fbbf24" stroke-width="3"/>
<text x="600" y="135" font-size="11" fill="#a16207" font-weight="600">중위험</text>
<path d="M120 178 L210 178 L300 177 L390 175 L480 172 L580 168" fill="none" stroke="#1f6f5c" stroke-width="3"/>
<text x="600" y="165" font-size="11" fill="#1f6f5c" font-weight="600">저위험</text>
</svg>
<p class="fig-caption">AI-CT 점수가 임상 위험 인자 단독보다 HCC 발생을 잘 stratification합니다. (도식적 표현)</p>''',

    "Shin-Antiviral-CV-CHB-JMV-2024": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="항바이러스제 치료에 따른 CHB 환자 심혈관 사건 감소">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">CHB 환자 항바이러스 치료의 심혈관 사건 영향</text>
<g text-anchor="middle">
<rect x="100" y="60" width="160" height="120" rx="8" fill="#fecaca" stroke="#b91c1c" stroke-width="2"/>
<text x="180" y="92" font-size="13" font-weight="700" fill="#b91c1c">미치료군</text>
<text x="180" y="124" font-size="22" font-weight="700" fill="#b91c1c">기준</text>
<text x="180" y="156" font-size="11" fill="#b91c1c">CV 사건 위험</text>
<text x="320" y="125" font-size="22" fill="#5a5a5a">→</text>
<rect x="380" y="60" width="160" height="120" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="460" y="92" font-size="13" font-weight="700" fill="#15803d">치료군</text>
<text x="460" y="128" font-size="20" font-weight="700" fill="#15803d">aHR &lt;1</text>
<text x="460" y="156" font-size="11" fill="#15803d">CV 사건 ↓</text>
</g>
<text x="20" y="195" font-size="11" fill="#5a5a5a">바이러스 억제 → 만성 염증 감소 → 죽상동맥경화·심혈관 위험 감소 가설 지지</text>
</svg>
<p class="fig-caption">항바이러스 치료가 간 외 합병증(심혈관)에도 보호 효과를 시사합니다.</p>''',

    "Shin-COVID-HBV-NK-IN-2023": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="만성 B형간염 환자에서 COVID-19 후 NK 세포 기능 변화">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">CHB 환자 COVID-19 회복 후 NK 세포 변화</text>
<g text-anchor="middle">
<rect x="60" y="60" width="160" height="100" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="2"/>
<text x="140" y="86" font-size="12" font-weight="600" fill="#1a1a1a">건강 대조군</text>
<text x="140" y="120" font-size="20" font-weight="700" fill="#1f6f5c">정상</text>
<text x="140" y="142" font-size="11" fill="#5a5a5a">NK 활성</text>
<rect x="280" y="60" width="160" height="100" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="360" y="86" font-size="12" font-weight="600" fill="#a16207">CHB (COVID 전)</text>
<text x="360" y="120" font-size="20" font-weight="700" fill="#a16207">기저 ↓</text>
<text x="360" y="142" font-size="11" fill="#a16207">NK 활성 약화</text>
<rect x="500" y="60" width="180" height="100" rx="8" fill="#fecaca" stroke="#b91c1c" stroke-width="2"/>
<text x="590" y="86" font-size="12" font-weight="600" fill="#b91c1c">CHB (COVID 후)</text>
<text x="590" y="120" font-size="18" font-weight="700" fill="#b91c1c">추가 감소</text>
<text x="590" y="142" font-size="11" fill="#b91c1c">회복 지연</text>
</g>
<text x="20" y="190" font-size="11" fill="#5a5a5a">COVID-19 회복 후 CHB 환자의 NK 세포 기능 회복이 건강 대조보다 지연 — 면역 취약성 시사</text>
</svg>
<p class="fig-caption">바이러스 감염 후 면역 회복 패턴이 CHB 환자에서 다르게 나타납니다.</p>''',

    "Shin-ETV-TAF-RCT-GnL-2026": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="엔테카비르 vs TAF 무작위 비교 — 바이러스 억제와 안전성">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">ETV vs TAF RCT — 효능 동등, 신·골 안전성 차이</text>
<g text-anchor="middle">
<rect x="40" y="60" width="280" height="50" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="2"/>
<text x="180" y="80" font-size="13" font-weight="700" fill="#1f6f5c">바이러스 억제 (HBV DNA &lt;LLOQ)</text>
<text x="180" y="100" font-size="13" fill="#1f6f5c">ETV ≈ TAF (비열등)</text>
<rect x="40" y="120" width="280" height="50" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="180" y="140" font-size="13" font-weight="700" fill="#15803d">ALT 정상화</text>
<text x="180" y="160" font-size="13" fill="#15803d">ETV ≈ TAF</text>
<rect x="380" y="60" width="300" height="50" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="530" y="80" font-size="13" font-weight="700" fill="#a16207">eGFR 변화</text>
<text x="530" y="100" font-size="13" fill="#a16207">TAF 친화적 (소폭 우세)</text>
<rect x="380" y="120" width="300" height="50" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="530" y="140" font-size="13" font-weight="700" fill="#a16207">골밀도</text>
<text x="530" y="160" font-size="13" fill="#a16207">TAF 친화적</text>
</g>
<text x="20" y="200" font-size="11" fill="#5a5a5a">바이러스 억제 효능은 비슷, 신·골 안전성에서 TAF 일부 우세 — 환자 동반질환에 따라 약 선택</text>
</svg>
<p class="fig-caption">효능은 비슷하지만 신·골 동반 위험에서 약 선택이 달라집니다.</p>''',

    "Shin-HBeAg-seroclearance-HCC-JHepR-2024": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="HBeAg seroclearance 후에도 HCC 위험 지속">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">HBeAg seroclearance 후 HCC 누적 발생률</text>
<line x1="60" y1="180" x2="700" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<line x1="60" y1="50" x2="60" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<text x="48" y="184" text-anchor="end" font-size="11" fill="#5a5a5a">0%</text>
<text x="48" y="120" text-anchor="end" font-size="11" fill="#5a5a5a">10%</text>
<text x="48" y="60" text-anchor="end" font-size="11" fill="#5a5a5a">20% HCC</text>
<g font-size="11" fill="#5a5a5a">
<text x="120" y="195" text-anchor="middle">0</text><text x="240" y="195" text-anchor="middle">3</text>
<text x="360" y="195" text-anchor="middle">6</text><text x="480" y="195" text-anchor="middle">9</text>
<text x="600" y="195" text-anchor="middle">12 (년)</text>
</g>
<path d="M120 180 L240 168 L360 152 L480 132 L600 110" fill="none" stroke="#c9542b" stroke-width="3"/>
<text x="610" y="105" font-size="11" fill="#c9542b" font-weight="600">간경변(+)</text>
<path d="M120 180 L240 178 L360 174 L480 168 L600 158" fill="none" stroke="#1f6f5c" stroke-width="3"/>
<text x="610" y="160" font-size="11" fill="#1f6f5c" font-weight="600">간경변(−)</text>
<text x="20" y="205" font-size="11" fill="#5a5a5a">seroclearance 후에도 간경변 동반 시 HCC 위험 지속 — 평생 검진 필요 근거</text>
</svg>
<p class="fig-caption">HBeAg seroclearance ≠ HCC 위험 소실. 간경변 동반 환자는 평생 검진을 유지합니다.</p>''',

    "Shin-HCC-Guidelines-Review-JLC-2025": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="주요 HCC 가이드라인 — KLCA-NCC, BCLC, AASLD 비교">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">주요 HCC 가이드라인 비교 (KLCA·BCLC·AASLD)</text>
<rect x="20" y="50" width="160" height="40" fill="#f3f1ec" stroke="#cbd5e1"/>
<text x="100" y="75" text-anchor="middle" font-size="12" font-weight="700">항목</text>
<rect x="180" y="50" width="170" height="40" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="2"/>
<text x="265" y="75" text-anchor="middle" font-size="12" font-weight="700" fill="#1f6f5c">KLCA-NCC</text>
<rect x="350" y="50" width="180" height="40" fill="#fef3c7" stroke="#a16207"/>
<text x="440" y="75" text-anchor="middle" font-size="12" font-weight="700" fill="#a16207">BCLC</text>
<rect x="530" y="50" width="170" height="40" fill="#fef3c7" stroke="#a16207"/>
<text x="615" y="75" text-anchor="middle" font-size="12" font-weight="700" fill="#a16207">AASLD</text>
<g font-size="12">
<rect x="20" y="90" width="160" height="32" fill="#fff" stroke="#cbd5e1"/><text x="100" y="111" text-anchor="middle">진행기 절제·SBRT</text>
<rect x="180" y="90" width="170" height="32" fill="#e8f3ef" stroke="#1f6f5c"/><text x="265" y="111" text-anchor="middle" fill="#1f6f5c">적극 인정</text>
<rect x="350" y="90" width="180" height="32" fill="#fff" stroke="#cbd5e1"/><text x="440" y="111" text-anchor="middle">제한적</text>
<rect x="530" y="90" width="170" height="32" fill="#fff" stroke="#cbd5e1"/><text x="615" y="111" text-anchor="middle">제한적</text>
<rect x="20" y="122" width="160" height="32" fill="#fff" stroke="#cbd5e1"/><text x="100" y="143" text-anchor="middle">LDLT 기준</text>
<rect x="180" y="122" width="170" height="32" fill="#e8f3ef" stroke="#1f6f5c"/><text x="265" y="143" text-anchor="middle" fill="#1f6f5c">확장 기준 활용</text>
<rect x="350" y="122" width="180" height="32" fill="#fff" stroke="#cbd5e1"/><text x="440" y="143" text-anchor="middle">Milan/UCSF</text>
<rect x="530" y="122" width="170" height="32" fill="#fff" stroke="#cbd5e1"/><text x="615" y="143" text-anchor="middle">Milan</text>
<rect x="20" y="154" width="160" height="32" fill="#fff" stroke="#cbd5e1"/><text x="100" y="175" text-anchor="middle">병용 (TACE+SBRT)</text>
<rect x="180" y="154" width="170" height="32" fill="#e8f3ef" stroke="#1f6f5c"/><text x="265" y="175" text-anchor="middle" fill="#1f6f5c">선호</text>
<rect x="350" y="154" width="180" height="32" fill="#fff" stroke="#cbd5e1"/><text x="440" y="175" text-anchor="middle">신중</text>
<rect x="530" y="154" width="170" height="32" fill="#fff" stroke="#cbd5e1"/><text x="615" y="175" text-anchor="middle">신중</text>
</g>
<text x="20" y="208" font-size="11" fill="#5a5a5a">한국 KLCA-NCC는 단일 알고리즘이 아닌 다학제 옵션 확장 — 임상 현장 다양성 반영</text>
</svg>
<p class="fig-caption">KLCA-NCC는 BCLC를 토대로 하되 한국 임상에 맞춰 옵션을 더 넓게 둡니다.</p>''',

    "Shin-TDF-ETV-TAF-switch-HCC-HepRes-2024": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ETV/TAF에서 TDF로 switch — HCC 위험 변화">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">항바이러스제 switch와 HCC 위험</text>
<g text-anchor="middle">
<rect x="20" y="60" width="200" height="100" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="120" y="86" font-size="13" font-weight="700" fill="#a16207">ETV 또는 TAF 유지</text>
<text x="120" y="115" font-size="22" font-weight="700" fill="#a16207">기준</text>
<text x="120" y="140" font-size="11" fill="#a16207">HCC 위험</text>
<text x="260" y="115" font-size="22" fill="#5a5a5a">→</text>
<rect x="300" y="60" width="200" height="100" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="400" y="86" font-size="13" font-weight="700" fill="#15803d">TDF로 switch</text>
<text x="400" y="115" font-size="22" font-weight="700" fill="#15803d">aHR &lt;1</text>
<text x="400" y="140" font-size="11" fill="#15803d">HCC 위험 ↓</text>
<rect x="540" y="60" width="160" height="100" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="2"/>
<text x="620" y="86" font-size="12" font-weight="600">신·골 부담</text>
<text x="620" y="115" font-size="18" font-weight="700" fill="#c9542b">↑ 일부</text>
<text x="620" y="140" font-size="11" fill="#5a5a5a">trade-off</text>
</g>
<text x="20" y="190" font-size="11" fill="#5a5a5a">TDF의 잠재적 HCC 보호 효과 vs 신·골 부담 — 환자 위험 인자에 따라 약 선택</text>
</svg>
<p class="fig-caption">switch 결정은 HCC 위험 인자와 신·골 동반 위험을 함께 고려합니다.</p>''',

    # === Other major papers ===
    "Ahn-Aspirin-HCC-MASLD-CMH-2026": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="MASLD 환자에서 아스피린 사용과 HCC 위험">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">MASLD 환자 아스피린과 HCC 위험 (cohort)</text>
<g text-anchor="middle">
<rect x="60" y="60" width="240" height="100" rx="8" fill="#fecaca" stroke="#b91c1c" stroke-width="2"/>
<text x="180" y="88" font-size="13" font-weight="700" fill="#b91c1c">아스피린 미사용</text>
<text x="180" y="120" font-size="24" font-weight="700" fill="#b91c1c">기준</text>
<text x="180" y="146" font-size="11" fill="#b91c1c">HCC 발생률</text>
<text x="340" y="115" font-size="20" fill="#5a5a5a">→</text>
<rect x="400" y="60" width="280" height="100" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="540" y="88" font-size="13" font-weight="700" fill="#15803d">저용량 아스피린</text>
<text x="540" y="122" font-size="22" font-weight="700" fill="#15803d">aHR &lt;1</text>
<text x="540" y="146" font-size="11" fill="#15803d">HCC 위험 감소 (관찰적)</text>
</g>
<text x="20" y="190" font-size="11" fill="#5a5a5a">MASLD에서 아스피린의 chemopreventive 가능성 — RCT 검증 필요. 출혈 위험과 trade-off 고려.</text>
</svg>
<p class="fig-caption">관찰 연구에서 시그널 — RCT 확증 필요한 단계입니다.</p>''',

    "Chung-SGLT2-Liver-MR-Hepatology-2024": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="SGLT2 억제제의 간 보호 효과 — Mendelian randomization">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">SGLT2 억제제 — Mendelian randomization 인과 추정</text>
<g text-anchor="middle">
<rect x="20" y="60" width="180" height="60" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="2"/>
<text x="110" y="84" font-size="12" font-weight="600">SGLT2 표적 변이</text>
<text x="110" y="106" font-size="11" fill="#5a5a5a">유전적 instrument</text>
<text x="220" y="98" font-size="22" fill="#5a5a5a">→</text>
<rect x="250" y="60" width="180" height="60" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="340" y="84" font-size="12" font-weight="600" fill="#a16207">대사·당뇨 표지</text>
<text x="340" y="106" font-size="11" fill="#a16207">HbA1c·BMI·혈압</text>
<text x="450" y="98" font-size="22" fill="#5a5a5a">→</text>
<rect x="480" y="60" width="220" height="60" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="590" y="84" font-size="12" font-weight="700" fill="#15803d">간 결과</text>
<text x="590" y="106" font-size="11" fill="#15803d">MASLD↓ · 간경변·HCC↓</text>
<text x="60" y="160" font-size="12" fill="#1a1a1a">→ 인과 효과: SGLT2 억제 ≈ 간 보호 시그널</text>
<text x="60" y="184" font-size="11" fill="#5a5a5a">관찰 confounding을 줄인 추정. 실제 SGLT2i 사용군 RCT와 일관됨.</text>
</g>
</svg>
<p class="fig-caption">유전 instrument를 활용한 인과 추정에서 SGLT2 억제의 간 보호 효과가 시사됩니다.</p>''',

    "GLP1RA-small-molecule-orforglipron": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="경구 GLP-1RA orforglipron — 주사형 대비 편의성과 효능">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">Orforglipron — 경구 small-molecule GLP-1RA</text>
<g text-anchor="middle">
<rect x="20" y="60" width="220" height="100" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="130" y="86" font-size="13" font-weight="700" fill="#a16207">주사형 (semaglutide)</text>
<text x="130" y="115" font-size="13" fill="#a16207">주 1회 피하주사</text>
<text x="130" y="138" font-size="13" fill="#a16207">peptide · 보관 까다로움</text>
<text x="270" y="115" font-size="22" fill="#5a5a5a">→</text>
<rect x="300" y="60" width="380" height="100" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="490" y="86" font-size="13" font-weight="700" fill="#15803d">Orforglipron — 경구 small-molecule</text>
<text x="490" y="115" font-size="13" fill="#15803d">매일 1회 알약</text>
<text x="490" y="138" font-size="13" fill="#15803d">단백질 분해 영향 적음 · 음식·물 자유</text>
</g>
<text x="20" y="190" font-size="11" fill="#5a5a5a">phase 3 결과 체중·HbA1c 감소가 주사형과 비슷한 수준 — MASLD/MASH 적용 가능성</text>
</svg>
<p class="fig-caption">경구화는 GLP-1RA 보급의 큰 장벽을 낮춥니다.</p>''',

    "GLP1RA-알코올성-간질환-ALD": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="GLP-1RA의 알코올 사용 감소와 ALD 적응 가능성">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">GLP-1RA — 알코올 사용 감소 시그널과 ALD 적응 가능성</text>
<g text-anchor="middle">
<rect x="20" y="60" width="200" height="80" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="2"/>
<text x="120" y="86" font-size="13" font-weight="700">기전 가설</text>
<text x="120" y="108" font-size="11" fill="#5a5a5a">중추 보상 회로</text>
<text x="120" y="124" font-size="11" fill="#5a5a5a">→ 음주 욕구 감소</text>
<text x="240" y="105" font-size="22" fill="#5a5a5a">→</text>
<rect x="270" y="60" width="180" height="80" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="360" y="86" font-size="13" font-weight="700" fill="#a16207">관찰 연구</text>
<text x="360" y="108" font-size="11" fill="#a16207">알코올 사용 감소</text>
<text x="360" y="124" font-size="11" fill="#a16207">cohort 시그널</text>
<text x="470" y="105" font-size="22" fill="#5a5a5a">→</text>
<rect x="500" y="60" width="200" height="80" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="2"/>
<text x="600" y="86" font-size="13" font-weight="700" fill="#1f6f5c">ALD 적응 가능성</text>
<text x="600" y="108" font-size="11" fill="#1f6f5c">RCT 진행 중</text>
<text x="600" y="124" font-size="11" fill="#1f6f5c">임상 적용 미정</text>
</g>
<text x="20" y="170" font-size="11" fill="#5a5a5a">기존 알코올 사용 장애 약물(naltrexone·acamprosate)의 한계 보완 가능성</text>
<text x="20" y="190" font-size="11" fill="#5a5a5a">금주 + 영양 지원이 여전히 표준 — GLP-1RA는 보조 옵션 후보</text>
</svg>
<p class="fig-caption">예방·치료 측면에서 새로운 가능성. 표준은 여전히 금주와 영양 지원입니다.</p>''',

    "MAESTRO-NASH-resmetirom-NEJM-2024": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="MAESTRO-NASH RCT — resmetirom phase 3 1차 종결점 결과">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">MAESTRO-NASH — resmetirom phase 3 (1차 종결점)</text>
<g text-anchor="middle">
<rect x="40" y="60" width="200" height="120" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="2"/>
<text x="140" y="86" font-size="12" font-weight="600">위약</text>
<text x="140" y="115" font-size="20" font-weight="700" fill="#5a5a5a">~10%</text>
<text x="140" y="135" font-size="11" fill="#5a5a5a">NASH 해소</text>
<text x="140" y="158" font-size="11" fill="#5a5a5a">~14% 섬유화 호전</text>
<rect x="260" y="60" width="200" height="120" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="2"/>
<text x="360" y="86" font-size="12" font-weight="600" fill="#a16207">resmetirom 80mg</text>
<text x="360" y="115" font-size="20" font-weight="700" fill="#a16207">~25%</text>
<text x="360" y="135" font-size="11" fill="#a16207">NASH 해소</text>
<text x="360" y="158" font-size="11" fill="#a16207">~24% 섬유화 호전</text>
<rect x="480" y="60" width="200" height="120" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="580" y="86" font-size="12" font-weight="600" fill="#15803d">resmetirom 100mg</text>
<text x="580" y="115" font-size="20" font-weight="700" fill="#15803d">~30%</text>
<text x="580" y="135" font-size="11" fill="#15803d">NASH 해소</text>
<text x="580" y="158" font-size="11" fill="#15803d">~26% 섬유화 호전</text>
</g>
<text x="20" y="200" font-size="11" fill="#5a5a5a">FDA 가속승인 (2024) — MASH F2-F3에 대한 첫 표적 치료. Liver-targeted thyroid hormone β-agonist.</text>
</svg>
<p class="fig-caption">위약 대비 NASH 해소·섬유화 호전 모두 통계적 유의 — MASH 약물치료 시대의 시작.</p>''',
}
