"""Per-case inline SVG figures for build_cases.py.

Each entry: slug → dict with `after` (which section index, 0-based, the figure
appears after) and `svg` (raw SVG markup including caption paragraph).

Designed to be visually consistent with existing svg.fig diagrams in topic
pages: 720px wide, simple shapes, accent color #1f6f5c.
"""

CASE_FIGURES = {
    # CASE 1: After "검사 — 위험 인자부터" — show how the diagnosis pivots
    "건강검진-우연발견-1cm결절": {
        "after": 1,
        "svg": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="평범한 검진 결과가 위험 평가의 출발점으로 바뀌는 흐름">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">결절 평가의 시각이 어떻게 바뀌는가</text>
<rect x="10" y="56" width="200" height="100" rx="10" fill="#fff" stroke="#bcbcb0" stroke-width="2"/>
<text x="110" y="92" text-anchor="middle" font-size="13" font-weight="600" fill="#1a1a1a">건강검진 한 줄</text>
<text x="110" y="116" text-anchor="middle" font-size="12" fill="#5a5a5a">"우엽 1cm 저에코 결절"</text>
<text x="110" y="138" text-anchor="middle" font-size="12" fill="#5a5a5a">위험 인자 미상</text>
<path d="M218 106 L268 106" stroke="#5a5a5a" stroke-width="2.5" marker-end="url(#a1)"/>
<defs><marker id="a1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#5a5a5a"/></marker></defs>
<rect x="270" y="56" width="200" height="100" rx="10" fill="#fef3e0" stroke="#b8650a" stroke-width="2"/>
<text x="370" y="92" text-anchor="middle" font-size="13" font-weight="600" fill="#b8650a">혈액검사 추가</text>
<text x="370" y="116" text-anchor="middle" font-size="12" fill="#5a5a5a">HBsAg 양성 새로 확인</text>
<text x="370" y="138" text-anchor="middle" font-size="12" fill="#5a5a5a">HBV DNA 12,000</text>
<path d="M478 106 L528 106" stroke="#5a5a5a" stroke-width="2.5" marker-end="url(#a1)"/>
<rect x="530" y="56" width="180" height="100" rx="10" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="2"/>
<text x="620" y="92" text-anchor="middle" font-size="13" font-weight="600" fill="#1f6f5c">평가 시각 전환</text>
<text x="620" y="116" text-anchor="middle" font-size="12" fill="#5a5a5a">간세포암 1순위로</text>
<text x="620" y="138" text-anchor="middle" font-size="12" fill="#5a5a5a">→ 영상 정밀화</text>
</svg>
<p class="fig-caption">위험 인자가 새로 발견되면 같은 결절을 보는 시각이 완전히 달라집니다.</p>''',
    },

    # CASE 2: After "첫 만남" — 6개월 검진 timeline with new lesion
    "B형간염-검진-새결절": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="10년 정기 검진 중 이번 회차에 새 결절 발견">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">10년 6개월 정기 검진 — 이번 회차에 새 결절</text>
<line x1="40" y1="100" x2="690" y2="100" stroke="#cbd5e1" stroke-width="2"/>
<g font-size="11" fill="#5a5a5a" text-anchor="middle">
<circle cx="80" cy="100" r="6" fill="#1f6f5c"/><text x="80" y="128">9년 전</text>
<circle cx="180" cy="100" r="6" fill="#1f6f5c"/><text x="180" y="128">7년 전</text>
<circle cx="280" cy="100" r="6" fill="#1f6f5c"/><text x="280" y="128">5년 전</text>
<circle cx="380" cy="100" r="6" fill="#1f6f5c"/><text x="380" y="128">3년 전</text>
<circle cx="480" cy="100" r="6" fill="#1f6f5c"/><text x="480" y="128">1년 전</text>
<circle cx="580" cy="100" r="6" fill="#1f6f5c"/><text x="580" y="128">6개월 전</text>
<circle cx="660" cy="100" r="11" fill="#c9542b" stroke="#fff" stroke-width="2"/><text x="660" y="80" font-weight="700" fill="#c9542b">이번</text><text x="660" y="128" font-weight="600" fill="#c9542b">2.1cm 신생</text>
</g>
<text x="40" y="58" font-size="11" fill="#5a5a5a">초음파 + AFP + PIVKA-II — 매번 정상</text>
<text x="40" y="160" font-size="11" fill="#5a5a5a">TDF 복용 · HBV DNA 불검출 유지</text>
</svg>
<p class="fig-caption">정상이 누적되어도 어느 회차에서 발견됩니다. 그래서 6개월 주기를 평생 유지합니다.</p>''',
    },

    # CASE 3: After "첫 만남" — AFP trend
    "AFP상승-영상음성": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="AFP 6→48→350 ng/mL 점진적 상승">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">AFP 추세 (지난 1년)</text>
<line x1="60" y1="180" x2="700" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<line x1="60" y1="50" x2="60" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<text x="48" y="184" text-anchor="end" font-size="11" fill="#5a5a5a">0</text>
<text x="48" y="120" text-anchor="end" font-size="11" fill="#5a5a5a">200</text>
<text x="48" y="60" text-anchor="end" font-size="11" fill="#5a5a5a">400 ng/mL</text>
<line x1="55" y1="120" x2="65" y2="120" stroke="#5a5a5a"/>
<line x1="55" y1="60" x2="65" y2="60" stroke="#5a5a5a"/>
<rect x="120" y="176" width="80" height="4" fill="#1f6f5c"/>
<text x="160" y="170" text-anchor="middle" font-size="12" fill="#1a1a1a">6</text>
<text x="160" y="200" text-anchor="middle" font-size="11" fill="#5a5a5a">12개월 전</text>
<rect x="280" y="166" width="80" height="14" fill="#fbbf24"/>
<text x="320" y="160" text-anchor="middle" font-size="12" fill="#1a1a1a">48</text>
<text x="320" y="200" text-anchor="middle" font-size="11" fill="#5a5a5a">6개월 전</text>
<rect x="440" y="68" width="80" height="112" fill="#c9542b"/>
<text x="480" y="60" text-anchor="middle" font-size="13" font-weight="700" fill="#c9542b">350</text>
<text x="480" y="200" text-anchor="middle" font-size="11" fill="#5a5a5a">현재</text>
<text x="560" y="115" font-size="12" fill="#5a5a5a">추세 ≫ 절대값</text>
<text x="560" y="135" font-size="12" fill="#5a5a5a">→ EOB-MRI</text>
</svg>
<p class="fig-caption">AFP 절대값보다 추세가 의미를 가지는 경우가 많습니다.</p>''',
    },

    # CASE 4: After "첫 만남" — LI-RADS 5단계
    "LR3-모호결절-추적": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="LI-RADS 분류 — 본 환자는 LR-3 회색지대">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">LI-RADS 5단계 — 본 환자는 LR-3 회색지대</text>
<g font-size="13" text-anchor="middle">
<rect x="20" y="60" width="130" height="80" rx="8" fill="#dcfce7" stroke="#15803d" stroke-width="1.5"/>
<text x="85" y="92" font-weight="700" fill="#15803d">LR-1</text>
<text x="85" y="115" font-size="11" fill="#15803d">확실히 양성</text>
<rect x="160" y="60" width="130" height="80" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="1.5"/>
<text x="225" y="92" font-weight="700" fill="#a16207">LR-2</text>
<text x="225" y="115" font-size="11" fill="#a16207">양성 가능성 큼</text>
<rect x="300" y="48" width="130" height="92" rx="8" fill="#fed7aa" stroke="#c2410c" stroke-width="3"/>
<text x="365" y="84" font-weight="700" fill="#c2410c">LR-3</text>
<text x="365" y="105" font-size="11" fill="#c2410c">중등도 의심</text>
<text x="365" y="124" font-size="11" font-weight="700" fill="#c2410c">▼ 본 환자</text>
<rect x="440" y="60" width="130" height="80" rx="8" fill="#fecaca" stroke="#b91c1c" stroke-width="1.5"/>
<text x="505" y="92" font-weight="700" fill="#b91c1c">LR-4</text>
<text x="505" y="115" font-size="11" fill="#b91c1c">HCC 가능성 큼</text>
<rect x="580" y="60" width="130" height="80" rx="8" fill="#7f1d1d" stroke="#7f1d1d" stroke-width="1.5"/>
<text x="645" y="92" font-weight="700" fill="#fff">LR-5</text>
<text x="645" y="115" font-size="11" fill="#fff">확실한 HCC</text>
</g>
</svg>
<p class="fig-caption">LR-3은 위험 인자에 따라 추적 또는 정밀 평가를 결정하는 단계입니다.</p>''',
    },

    # CASE 5: After "첫 만남" — PIVKA-II 위양성 원인
    "PIVKAII-와파린-위양성": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="PIVKA-II 위양성을 일으키는 흔한 원인">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">PIVKA-II 위양성을 일으키는 원인</text>
<rect x="10" y="56" width="340" height="36" fill="#fef3c7" stroke="#a16207" stroke-width="1.5"/>
<text x="180" y="80" text-anchor="middle" font-size="13" font-weight="700" fill="#a16207">와파린 ✓ 본 환자</text>
<rect x="10" y="98" width="340" height="36" fill="#fff" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="180" y="122" text-anchor="middle" font-size="13" fill="#1a1a1a">DOAC (아픽사반·다비가트란 등)</text>
<rect x="10" y="140" width="340" height="36" fill="#fff" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="180" y="164" text-anchor="middle" font-size="13" fill="#1a1a1a">광범위 항생제 (장내균 변화)</text>
<rect x="10" y="182" width="340" height="32" fill="#fff" stroke="#cbd5e1" stroke-width="1.5"/>
<text x="180" y="204" text-anchor="middle" font-size="13" fill="#1a1a1a">비타민 K 결핍 / 폐쇄성 황달</text>
<g transform="translate(370 56)">
<rect x="0" y="0" width="340" height="158" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="1.5"/>
<text x="170" y="32" text-anchor="middle" font-size="13" font-weight="700" fill="#1f6f5c">기전</text>
<text x="20" y="62" font-size="12" fill="#1a1a1a">비타민 K 의존 carboxylation 차단</text>
<text x="20" y="86" font-size="12" fill="#1a1a1a">↓</text>
<text x="20" y="108" font-size="12" fill="#1a1a1a">des-γ-carboxy prothrombin 증가</text>
<text x="20" y="132" font-size="12" fill="#1a1a1a">↓</text>
<text x="20" y="154" font-size="12" fill="#c9542b" font-weight="700">PIVKA-II 측정값 위양성 상승</text>
</g>
<text x="370" y="208" font-size="11" fill="#5a5a5a">→ 영상으로 종양 배제가 표준</text>
</svg>
<p class="fig-caption">위양성 의심이라도 영상으로 종양을 배제하는 것이 표준 흐름입니다.</p>''',
    },

    # CASE 6: After "첫 만남" — MASLD → HCC 진행
    "MASLD-HCC-비만당뇨": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="MASLD에서 간세포암까지의 진행 경로">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">MASLD → HCC 경로 (이 환자는 MASH F3에서 발견)</text>
<defs><marker id="a6" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#5a5a5a"/></marker></defs>
<g font-size="12" text-anchor="middle">
<rect x="10" y="60" width="120" height="80" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>
<text x="70" y="92" font-weight="600">MASLD</text>
<text x="70" y="116" font-size="11" fill="#5a5a5a">단순 지방간</text>
<path d="M138 100 L168 100" stroke="#5a5a5a" stroke-width="2" marker-end="url(#a6)"/>
<rect x="172" y="60" width="120" height="80" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="1.5"/>
<text x="232" y="92" font-weight="600" fill="#a16207">MASH</text>
<text x="232" y="116" font-size="11" fill="#a16207">지방간염</text>
<path d="M300 100 L330 100" stroke="#5a5a5a" stroke-width="2" marker-end="url(#a6)"/>
<rect x="334" y="60" width="120" height="80" rx="8" fill="#fed7aa" stroke="#c2410c" stroke-width="3"/>
<text x="394" y="86" font-weight="700" fill="#c2410c">F3 섬유화</text>
<text x="394" y="106" font-size="11" fill="#c2410c">진행 섬유화</text>
<text x="394" y="126" font-size="10" font-weight="700" fill="#c2410c">▼ 본 환자</text>
<path d="M462 100 L492 100" stroke="#5a5a5a" stroke-width="2" marker-end="url(#a6)"/>
<rect x="496" y="60" width="100" height="80" rx="8" fill="#fecaca" stroke="#b91c1c" stroke-width="1.5"/>
<text x="546" y="92" font-weight="600" fill="#b91c1c">간경변</text>
<text x="546" y="116" font-size="11" fill="#b91c1c">F4</text>
<path d="M604 100 L634 100" stroke="#5a5a5a" stroke-width="2" marker-end="url(#a6)"/>
<rect x="638" y="60" width="72" height="80" rx="8" fill="#7f1d1d" stroke="#7f1d1d" stroke-width="1.5"/>
<text x="674" y="100" font-weight="700" fill="#fff">HCC</text>
</g>
<text x="20" y="170" font-size="11" fill="#5a5a5a">비만·당뇨 누적은 비-간경변 단계에서도 일부 HCC 발생 가능 — 위험 인자 누적 시 적극 검진</text>
</svg>
<p class="fig-caption">F2-F3 단계에서도 검진을 적극 검토하는 이유입니다.</p>''',
    },

    # CASE 7: After "결정 인자 분석" — 절제 vs 소작 결정 트리
    "BCLC-A-단일3cm-절제vs소작": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3cm 단일 종양에서 절제와 고주파열치료술 사이 결정 인자">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">3cm 단일 — 두 옵션이 비슷할 때 결정 인자</text>
<rect x="280" y="46" width="160" height="48" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="2"/>
<text x="360" y="76" text-anchor="middle" font-size="13" font-weight="700" fill="#1f6f5c">단일 ≤3cm + Child-Pugh A</text>
<line x1="240" y1="118" x2="200" y2="148" stroke="#5a5a5a" stroke-width="1.5"/>
<line x1="360" y1="118" x2="360" y2="148" stroke="#5a5a5a" stroke-width="1.5"/>
<line x1="480" y1="118" x2="520" y2="148" stroke="#5a5a5a" stroke-width="1.5"/>
<text x="360" y="115" text-anchor="middle" font-size="12" fill="#5a5a5a">결정 인자</text>
<rect x="60" y="148" width="280" height="80" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>
<text x="200" y="172" text-anchor="middle" font-size="13" font-weight="700" fill="#1a1a1a">위치</text>
<text x="200" y="194" text-anchor="middle" font-size="11" fill="#5a5a5a">S7/S8 횡격막 가까움</text>
<text x="200" y="212" text-anchor="middle" font-size="11" font-weight="700" fill="#1f6f5c">→ 소작 어려움 / 절제 우세</text>
<rect x="252" y="148" width="216" height="80" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>
<text x="360" y="172" text-anchor="middle" font-size="13" font-weight="700" fill="#1a1a1a">간 기능</text>
<text x="360" y="194" text-anchor="middle" font-size="11" fill="#5a5a5a">HVPG &lt; 10, 잔간 65%</text>
<text x="360" y="212" text-anchor="middle" font-size="11" font-weight="700" fill="#1f6f5c">→ 절제 안전</text>
<rect x="380" y="148" width="280" height="80" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>
<text x="520" y="172" text-anchor="middle" font-size="13" font-weight="700" fill="#1a1a1a">환자 요인</text>
<text x="520" y="194" text-anchor="middle" font-size="11" fill="#5a5a5a">60세, 동반질환 적음</text>
<text x="520" y="212" text-anchor="middle" font-size="11" font-weight="700" fill="#1f6f5c">→ 회복 빠른 복강경</text>
</svg>
<p class="fig-caption">5년 생존이 비슷할 때 결정은 위치·간 기능·환자 요인의 조합으로 갈립니다.</p>''',
    },

    # CASE 8: After "결정 흐름" — 3개 결절 단일 회기 RFA
    "BCLC-A-다발3개-소작": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="3개 결절을 한 회기에 모두 소작하는 schematic">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">3개 결절 · 단일 회기 다중 RFA</text>
<path d="M120 80 C 80 80, 60 130, 100 170 L 280 180 C 340 175, 360 130, 320 80 Z" fill="#fef3e0" stroke="#b8650a" stroke-width="2"/>
<text x="200" y="200" text-anchor="middle" font-size="11" fill="#b8650a">우엽</text>
<path d="M340 80 C 380 80, 400 130, 360 170 L 540 180 C 600 175, 620 130, 580 80 Z" fill="#fef3e0" stroke="#b8650a" stroke-width="2"/>
<text x="460" y="200" text-anchor="middle" font-size="11" fill="#b8650a">좌엽</text>
<circle cx="170" cy="120" r="14" fill="#c9542b" stroke="#fff" stroke-width="2"/>
<text x="170" y="124" text-anchor="middle" font-size="11" font-weight="700" fill="#fff">1.8</text>
<circle cx="260" cy="140" r="12" fill="#c9542b" stroke="#fff" stroke-width="2"/>
<text x="260" y="144" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">1.5</text>
<circle cx="430" cy="125" r="10" fill="#c9542b" stroke="#fff" stroke-width="2"/>
<text x="430" y="129" text-anchor="middle" font-size="10" font-weight="700" fill="#fff">1.2</text>
<line x1="170" y1="60" x2="170" y2="106" stroke="#1f6f5c" stroke-width="3"/>
<line x1="260" y1="60" x2="260" y2="128" stroke="#1f6f5c" stroke-width="3"/>
<line x1="430" y1="60" x2="430" y2="115" stroke="#1f6f5c" stroke-width="3"/>
<text x="20" y="50" font-size="11" fill="#1f6f5c">RFA 바늘 (단일 회기)</text>
<text x="650" y="100" text-anchor="end" font-size="11" fill="#5a5a5a">3개 모두 BCLC A 기준 안</text>
<text x="650" y="120" text-anchor="end" font-size="11" fill="#5a5a5a">시술시간 1.5시간</text>
<text x="650" y="140" text-anchor="end" font-size="11" font-weight="700" fill="#1f6f5c">합병증 없이 종료</text>
</svg>
<p class="fig-caption">다발성 BCLC A에서 단일 회기 다중 RFA가 환자 부담을 크게 줄입니다.</p>''',
    },

    # CASE 9: After "평가" — TACE bridging → LDLT timeline
    "ChildB-단일4cm-이식": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="평가에서 LDLT까지 2개월 timeline">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">평가 → bridging TACE → LDLT (2개월)</text>
<line x1="40" y1="100" x2="690" y2="100" stroke="#5a5a5a" stroke-width="2"/>
<g text-anchor="middle">
<circle cx="80" cy="100" r="9" fill="#1f6f5c"/>
<text x="80" y="80" font-size="12" font-weight="700" fill="#1f6f5c">D0</text>
<text x="80" y="128" font-size="11" fill="#5a5a5a">단일 4cm HCC</text>
<text x="80" y="144" font-size="11" fill="#5a5a5a">Child-Pugh B7</text>
<circle cx="220" cy="100" r="9" fill="#fbbf24"/>
<text x="220" y="80" font-size="12" font-weight="700" fill="#a16207">2주</text>
<text x="220" y="128" font-size="11" fill="#5a5a5a">다학제 평가 적합</text>
<text x="220" y="144" font-size="11" fill="#5a5a5a">정신건강 평가 통과</text>
<circle cx="370" cy="100" r="9" fill="#fbbf24"/>
<text x="370" y="80" font-size="12" font-weight="700" fill="#a16207">3주</text>
<text x="370" y="128" font-size="11" fill="#5a5a5a">Bridging TACE</text>
<text x="370" y="144" font-size="11" fill="#5a5a5a">종양 진행 억제</text>
<circle cx="520" cy="100" r="9" fill="#fbbf24"/>
<text x="520" y="80" font-size="12" font-weight="700" fill="#a16207">4주</text>
<text x="520" y="128" font-size="11" fill="#5a5a5a">LDLT 기증자 적합</text>
<text x="520" y="144" font-size="11" fill="#5a5a5a">(50대 형)</text>
<circle cx="660" cy="100" r="11" fill="#1f6f5c" stroke="#fff" stroke-width="2"/>
<text x="660" y="80" font-size="12" font-weight="700" fill="#1f6f5c">2개월</text>
<text x="660" y="128" font-size="11" font-weight="700" fill="#1f6f5c">LDLT 시행</text>
<text x="660" y="144" font-size="11" fill="#5a5a5a">합병증 없음</text>
</g>
</svg>
<p class="fig-caption">한국은 LDLT 비율이 70%로 가족 기증자 평가가 빠르게 진행됩니다.</p>''',
    },

    # CASE 10: After "결정" — TACE 4-6주 평가 반복 schematic
    "BCLC-B-다발성-TACE": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="좌·우엽 분리 TACE + 잔존 부위 추가 시술">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">양엽 4개 결절 — 분리 시행 + 4-6주 평가 + 반복</text>
<defs><marker id="a10" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#5a5a5a"/></marker></defs>
<g font-size="12" text-anchor="middle">
<rect x="10" y="56" width="120" height="80" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>
<text x="70" y="84" font-weight="600">우엽 TACE</text>
<text x="70" y="104" font-size="11" fill="#5a5a5a">결절 3개</text>
<text x="70" y="122" font-size="11" fill="#5a5a5a">1차 회기</text>
<path d="M138 96 L168 96" stroke="#5a5a5a" stroke-width="2" marker-end="url(#a10)"/>
<rect x="172" y="56" width="120" height="80" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>
<text x="232" y="84" font-weight="600">좌엽 TACE</text>
<text x="232" y="104" font-size="11" fill="#5a5a5a">결절 1개</text>
<text x="232" y="122" font-size="11" fill="#5a5a5a">4주 후</text>
<path d="M300 96 L330 96" stroke="#5a5a5a" stroke-width="2" marker-end="url(#a10)"/>
<rect x="334" y="56" width="160" height="80" rx="8" fill="#fef3c7" stroke="#a16207" stroke-width="1.5"/>
<text x="414" y="84" font-weight="600" fill="#a16207">4-6주 영상 평가</text>
<text x="414" y="104" font-size="11" fill="#a16207">3개 완전 괴사</text>
<text x="414" y="122" font-size="11" font-weight="700" fill="#c9542b">1개 잔존</text>
<path d="M502 96 L532 96" stroke="#5a5a5a" stroke-width="2" marker-end="url(#a10)"/>
<rect x="536" y="56" width="170" height="80" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="1.5"/>
<text x="621" y="84" font-weight="600" fill="#1f6f5c">잔존부위 추가 TACE</text>
<text x="621" y="104" font-size="11" fill="#5a5a5a">3개월 시점</text>
<text x="621" y="122" font-size="11" fill="#1f6f5c">→ 6개월 완전 괴사</text>
</g>
<text x="20" y="170" font-size="11" fill="#5a5a5a">Post-embolization syndrome (발열·복통) 2-3일은 정상 경과로 자가 회복</text>
</svg>
<p class="fig-caption">TACE는 한 번에 끝나지 않을 수 있어 4-6주 평가 후 반복 여부를 결정합니다.</p>''',
    },

    # CASE 11: After "결정" — TACE→SBRT→다운스테이징 timeline
    "큰종양-TACE-SBRT-결합": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="8cm 큰 종양 TACE+SBRT 결합 결과 timeline">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">8cm 큰 종양 — TACE+SBRT 결합 후 다운스테이징</text>
<line x1="40" y1="120" x2="690" y2="120" stroke="#5a5a5a" stroke-width="2"/>
<g text-anchor="middle">
<circle cx="80" cy="120" r="9" fill="#1f6f5c"/>
<text x="80" y="100" font-size="12" font-weight="700" fill="#1f6f5c">시작</text>
<text x="80" y="148" font-size="11" font-weight="700" fill="#c9542b">8.2cm</text>
<text x="80" y="164" font-size="11" fill="#5a5a5a">AFP 850</text>
<circle cx="240" cy="120" r="9" fill="#fbbf24"/>
<text x="240" y="100" font-size="12" font-weight="700" fill="#a16207">TACE</text>
<text x="240" y="148" font-size="11" fill="#a16207">≈30% 위축</text>
<text x="240" y="164" font-size="11" fill="#5a5a5a">5주 후 SBRT 준비</text>
<circle cx="400" cy="120" r="9" fill="#fbbf24"/>
<text x="400" y="100" font-size="12" font-weight="700" fill="#a16207">SBRT</text>
<text x="400" y="148" font-size="11" fill="#a16207">3분할 고선량</text>
<text x="400" y="164" font-size="11" fill="#5a5a5a">3개월 후 평가</text>
<circle cx="560" cy="120" r="9" fill="#1f6f5c"/>
<text x="560" y="100" font-size="12" font-weight="700" fill="#1f6f5c">3개월</text>
<text x="560" y="148" font-size="11" fill="#1f6f5c">≈70% 위축</text>
<text x="560" y="164" font-size="11" fill="#5a5a5a">AFP 120</text>
<circle cx="680" cy="120" r="11" fill="#1f6f5c" stroke="#fff" stroke-width="2"/>
<text x="680" y="100" font-size="12" font-weight="700" fill="#1f6f5c">6개월</text>
<text x="680" y="148" font-size="11" font-weight="700" fill="#1f6f5c">이식 평가</text>
<text x="680" y="164" font-size="11" fill="#5a5a5a">AFP 45</text>
</g>
<text x="20" y="200" font-size="11" fill="#5a5a5a">큰 종양에서 TACE 단독·SBRT 단독 모두 한계 — 결합 치료가 국소 제어와 생존에 우수 (STRBED, TACE-HIGH)</text>
</svg>
<p class="fig-caption">결합 전략 + AFP 추세 감소가 다운스테이징 성공의 신호입니다.</p>''',
    },

    # CASE 12: After "결정" — atezo+bev 반응 timeline
    "문맥침범-AtezoBev": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="atezolizumab+bevacizumab 1차 — 9주/6개월/1년 반응 timeline">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">atezo+bev — 9주/6개월/1년 반응</text>
<line x1="40" y1="120" x2="690" y2="120" stroke="#5a5a5a" stroke-width="2"/>
<g text-anchor="middle">
<circle cx="80" cy="120" r="9" fill="#1f6f5c"/>
<text x="80" y="100" font-size="12" font-weight="700" fill="#1f6f5c">시작</text>
<text x="80" y="148" font-size="11" font-weight="700" fill="#c9542b">5cm + 문맥</text>
<text x="80" y="164" font-size="11" fill="#5a5a5a">AFP 1200</text>
<circle cx="220" cy="120" r="9" fill="#fbbf24"/>
<text x="220" y="100" font-size="12" font-weight="700" fill="#a16207">6주</text>
<text x="220" y="148" font-size="11" fill="#5a5a5a">경증 피로만</text>
<text x="220" y="164" font-size="11" fill="#5a5a5a">큰 부작용 없음</text>
<circle cx="370" cy="120" r="9" fill="#1f6f5c"/>
<text x="370" y="100" font-size="12" font-weight="700" fill="#1f6f5c">9주</text>
<text x="370" y="148" font-size="11" fill="#1f6f5c">≈30% 위축</text>
<text x="370" y="164" font-size="11" fill="#5a5a5a">AFP 340</text>
<circle cx="520" cy="120" r="9" fill="#1f6f5c"/>
<text x="520" y="100" font-size="12" font-weight="700" fill="#1f6f5c">6개월</text>
<text x="520" y="148" font-size="11" fill="#1f6f5c">≈50% 위축</text>
<text x="520" y="164" font-size="11" fill="#5a5a5a">갑상선 보충 시작</text>
<circle cx="670" cy="120" r="11" fill="#1f6f5c" stroke="#fff" stroke-width="2"/>
<text x="670" y="100" font-size="12" font-weight="700" fill="#1f6f5c">1년</text>
<text x="670" y="148" font-size="11" font-weight="700" fill="#1f6f5c">안정 반응 유지</text>
<text x="670" y="164" font-size="11" fill="#5a5a5a">AFP 65</text>
</g>
<text x="20" y="200" font-size="11" fill="#5a5a5a">9-12주 영상으로 첫 반응 평가 · AFP 추세 감소 = 좋은 반응 지표 · 면역 매개 부작용은 보충/스테로이드로 조절</text>
</svg>
<p class="fig-caption">IMbrave150 표준 흐름 — 첫 반응 평가 시점 9-12주가 분기점입니다.</p>''',
    },

    # CASE 13: After "결정" — STRIDE 결정 트리
    "정맥류출혈이력-STRIDE": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="베바시주맙 회피 환자에서 STRIDE 선택 결정 트리">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">BCLC C 1차 — 출혈 위험 환자에서 STRIDE</text>
<rect x="240" y="46" width="240" height="48" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="2"/>
<text x="360" y="76" text-anchor="middle" font-size="13" font-weight="700" fill="#1f6f5c">BCLC C 1차 면역치료 결정</text>
<line x1="300" y1="118" x2="180" y2="148" stroke="#5a5a5a" stroke-width="1.5"/>
<line x1="420" y1="118" x2="540" y2="148" stroke="#5a5a5a" stroke-width="1.5"/>
<text x="200" y="138" text-anchor="middle" font-size="11" fill="#5a5a5a">베바시주맙 안전</text>
<text x="520" y="138" text-anchor="middle" font-size="11" font-weight="700" fill="#c2410c">정맥류 출혈 이력</text>
<rect x="60" y="148" width="240" height="56" rx="8" fill="#fff" stroke="#bcbcb0" stroke-width="1.5"/>
<text x="180" y="174" text-anchor="middle" font-size="13" font-weight="600" fill="#1a1a1a">atezolizumab + bevacizumab</text>
<text x="180" y="194" text-anchor="middle" font-size="11" fill="#5a5a5a">IMbrave150 표준</text>
<rect x="420" y="148" width="240" height="56" rx="8" fill="#fed7aa" stroke="#c2410c" stroke-width="3"/>
<text x="540" y="174" text-anchor="middle" font-size="13" font-weight="700" fill="#c2410c">STRIDE (durva + treme)</text>
<text x="540" y="194" text-anchor="middle" font-size="11" font-weight="700" fill="#c2410c">▼ 본 환자 (HIMALAYA 근거)</text>
</svg>
<p class="fig-caption">트레멜리무맙 1회만 priming하여 면역 부작용 누적 부담을 줄입니다. 4년 생존 25%.</p>''',
    },

    # CASE 14: After "다운스테이징 시도" — 종양 크기 + AFP timeline
    "다운스테이징-이식전환": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="7cm → 4.5cm 다운스테이징과 AFP 추세 동반 감소">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">다운스테이징 — 종양 크기와 AFP가 함께 감소</text>
<line x1="60" y1="180" x2="700" y2="180" stroke="#5a5a5a" stroke-width="1.5"/>
<text x="50" y="184" text-anchor="end" font-size="11" fill="#5a5a5a">크기/AFP</text>
<g text-anchor="middle">
<circle cx="160" cy="180" r="40" fill="#fecaca" stroke="#b91c1c" stroke-width="1.5"/>
<text x="160" y="180" font-size="13" font-weight="700" fill="#b91c1c">7.0</text>
<text x="160" y="200" font-size="10" fill="#b91c1c">cm</text>
<text x="160" y="60" font-size="11" font-weight="700" fill="#5a5a5a">시작</text>
<text x="160" y="80" font-size="11" fill="#c9542b">AFP 1500</text>
<circle cx="350" cy="180" r="32" fill="#fed7aa" stroke="#c2410c" stroke-width="1.5"/>
<text x="350" y="180" font-size="13" font-weight="700" fill="#c2410c">5.5</text>
<text x="350" y="200" font-size="10" fill="#c2410c">cm</text>
<text x="350" y="60" font-size="11" font-weight="700" fill="#5a5a5a">TACE</text>
<text x="350" y="80" font-size="11" fill="#a16207">AFP 320</text>
<circle cx="540" cy="180" r="26" fill="#fef3c7" stroke="#a16207" stroke-width="1.5"/>
<text x="540" y="180" font-size="12" font-weight="700" fill="#a16207">4.5</text>
<text x="540" y="200" font-size="10" fill="#a16207">cm</text>
<text x="540" y="60" font-size="11" font-weight="700" fill="#5a5a5a">SBRT 후 3개월</text>
<text x="540" y="80" font-size="11" fill="#15803d">AFP 90</text>
<circle cx="660" cy="180" r="22" fill="#dcfce7" stroke="#15803d" stroke-width="2"/>
<text x="660" y="180" font-size="12" font-weight="700" fill="#15803d">4.2</text>
<text x="660" y="200" font-size="10" fill="#15803d">cm</text>
<text x="660" y="60" font-size="11" font-weight="700" fill="#1f6f5c">LDLT 후 병리</text>
<text x="660" y="80" font-size="11" fill="#15803d">Milan 안</text>
</g>
<line x1="60" y1="100" x2="200" y2="100" stroke="#cbd5e1" stroke-dasharray="4 3"/>
<text x="220" y="104" font-size="11" fill="#5a5a5a">Milan ≤5cm 기준선</text>
</svg>
<p class="fig-caption">다운스테이징 성공 환자의 이식 후 5년 생존은 직접 Milan 환자와 유사합니다.</p>''',
    },

    # CASE 15: After "재발 평가" — 절제 후 추적 + de novo
    "절제후-2년재발": {
        "after": 0,
        "svg": '''<svg class="fig" viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="절제 후 정기 추적 중 다른 위치에 새 결절 발생 (de novo)">
<text x="20" y="26" font-size="15" font-weight="600" fill="#1f6f5c">절제 후 추적 — 다른 위치 새 결절은 사실상 새 HCC</text>
<line x1="40" y1="100" x2="690" y2="100" stroke="#5a5a5a" stroke-width="2"/>
<g text-anchor="middle">
<circle cx="80" cy="100" r="9" fill="#1f6f5c"/>
<text x="80" y="80" font-size="12" font-weight="700" fill="#1f6f5c">절제</text>
<text x="80" y="128" font-size="11" fill="#5a5a5a">우엽 단일</text>
<text x="80" y="144" font-size="11" fill="#5a5a5a">병리 R0</text>
<circle cx="220" cy="100" r="8" fill="#15803d"/>
<text x="220" y="80" font-size="12" font-weight="700" fill="#15803d">6개월</text>
<text x="220" y="128" font-size="11" fill="#15803d">정상</text>
<circle cx="350" cy="100" r="8" fill="#15803d"/>
<text x="350" y="80" font-size="12" font-weight="700" fill="#15803d">1년</text>
<text x="350" y="128" font-size="11" fill="#15803d">정상</text>
<circle cx="480" cy="100" r="8" fill="#15803d"/>
<text x="480" y="80" font-size="12" font-weight="700" fill="#15803d">2년</text>
<text x="480" y="128" font-size="11" fill="#15803d">정상</text>
<circle cx="640" cy="100" r="13" fill="#c9542b" stroke="#fff" stroke-width="2"/>
<text x="640" y="80" font-size="12" font-weight="700" fill="#c9542b">2.5년</text>
<text x="640" y="128" font-size="11" font-weight="700" fill="#c9542b">좌엽 1.5cm</text>
<text x="640" y="144" font-size="11" fill="#c9542b">de novo (new primary)</text>
</g>
<text x="20" y="180" font-size="11" fill="#5a5a5a">절제 2년 이후 발견되는 "재발"은 대부분 새 결절 — 간경변 환자에서 평생 발생 가능 → 평생 검진</text>
</svg>
<p class="fig-caption">간경변 환자에서 새 결절은 평생 발생 가능합니다. 정기 검진을 평생 유지하는 이유입니다.</p>''',
    },
}
