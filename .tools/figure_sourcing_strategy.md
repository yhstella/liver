# Figure sourcing strategy — drshin.kr

목적: 환자 입장에서 보았을 때, 페이지 내용과 직접 연관된 figure만 두는 것이 원칙. 일반 anatomy, 단순 virion, 무관한 ultrasound 같은 "공간 채우기" 그림은 제거.

---

## Tier 1 — Custom inline SVG (최우선, 안전성·유연성 모두 1위)

각 페이지 주제에 정확히 맞는 인포그래픽을 직접 작성.

장점:
- 라이선스 0, 저작권 분쟁 없음
- 한국어 텍스트, 환자 친화 어휘 직접 통제
- 색상은 brand `#1f6f5c` 기준 + 단계별 색조(green/yellow/orange/red)
- 작은 파일 크기, 반응형, 검색엔진 친화적
- viewBox 720×N (가로 720 기준)

표준 패턴:
- `<svg class="fig" viewBox="0 0 720 280" role="img" aria-label="...">`
- `<text font-size="15" font-weight="600" fill="#1f6f5c">` 제목
- `font-size="11"` 본문, `font-size="10"` 캡션
- 단계별 박스: rounded rect (rx="8") + 색상 단계 (#d1fae5 → #fef3c7 → #fed7aa → #fecaca)

이미 적용된 사례 (참고 캐논):
- 8 hub 페이지 전체 (간암, 간경화, B형간염, C형간염, 지방간, 간수치, 자가면역간염, 간양성종양)
- 간암-BCLC병기 (5단계 비교 + 생존율)
- 자가면역간염-진단 (Simplified score 4축)
- C형간염-진단 (RNA 분기)
- 빌리루빈-직접-간접 (대사 흐름 + 막힘 패턴)
- 알코올성-간질환 (4단계 스펙트럼)
- 간양성종양-혈관종 (동적 조영 4단계 패턴)

---

## Tier 2 — Servier Medical Art (CC BY 4.0)

URL: https://smart.servier.com/

라이선스: CC BY 4.0 — 상업적 사용 가능, attribution 필요.

활용:
- 해부학 일러스트 (간 분엽, 담관, 간소엽)
- 세포 수준 일러스트 (간세포, Kupffer cell, stellate cell)
- 시술/장비 일러스트 (TIPS, ablation probe, FibroScan probe)
- PowerPoint·SVG 양 형식 모두 다운로드 가능

attribution 표준:
```html
<figcaption>이미지 출처: Servier Medical Art (CC BY 4.0)</figcaption>
```

또는 footer에서 일괄 attribution.

미사용. 향후 토픽별 인포그래픽 보완 시 활용 가능.

---

## Tier 3 — Wikimedia Commons

URL: https://commons.wikimedia.org/

라이선스: 파일별로 다름 (CC0, CC BY, CC BY-SA 4.0, public domain 등) — 반드시 개별 확인.

활용 사례:
- 식도정맥류 결찰술 사진 (`/assets/img/web/esophageal-varices-banding.png`, Kel898 CC BY-SA 4.0)
- 복수 천자 도식 (Cancer Research UK CC BY-SA 4.0)

체크리스트:
- 라이선스 명시 + 작성자명 attribution
- CC BY-SA는 상업적 사용 가능, 단 같은 라이선스로 재배포

---

## Tier 4 — PubMed Central Open Access (PMC OA)

URL: https://www.ncbi.nlm.nih.gov/pmc/

라이선스: 논문별로 다름 — open access 라이선스(CC BY 등) 확인 필수.

활용:
- updates/ 페이지의 시험 결과 그림 (Kaplan-Meier curve, forest plot)
- 직접 인용 + figure caption + 원논문 링크

---

## Tier 5 — NIH BioArt / CDC Public Health Image Library (PHIL)

URL: https://bioart.niaid.nih.gov/, https://phil.cdc.gov/

라이선스: 대부분 public domain (US Federal Government 작품).

활용:
- HCV/HBV virion 일러스트 (다만 단순 virion은 환자 페이지에서 가치 낮음 — Tier 1 선호)
- 백신 접종 사진
- 공중보건 캠페인 자료

---

## "이 figure를 둘 것인가?" 결정 기준 (UX 관점)

페이지 내용과 figure의 관계를 다음 4가지 중 하나로 분류:

1. **직접 설명** — figure가 본문에서 다루는 개념·구조·과정을 직접 보여줌. 예: "BCLC 5단계" 페이지의 BCLC 표.
2. **임상 사진 보조** — 실제 시술/소견 사진. 예: 식도정맥류 결찰 사진, 동적 CT 영상.
3. **추상적 비유** — 일반인 이해를 돕는 비유 그림. 예: "간 = 화학공장" 일러스트. 신중히.
4. **공간 채우기** — 무관한 anatomy/virion. **즉시 제거**.

기본 원칙:
- page-photo (auto-injected by `embed_page_figures.py`)는 hub·detail마다 자동 표시 — 별도 figure 추가 시 redundant 여부 확인.
- 인라인 SVG가 이미 있으면 generic figure 추가는 보통 redundant.
- 환자가 figure를 보고 "이게 내 상황과 어떤 관련이 있나?"를 1초 안에 파악 못하면 제거.

---

## 작업 패턴 (검수자용)

페이지 figure 점검 시:
```
1. Grep으로 real-fig 또는 svg.fig 패턴 모든 사용 위치 파악
2. 각 figure를 page-photo와 비교 — duplication 여부
3. figure caption의 의미가 본문 섹션과 일치하는지 확인
4. 무관 figure는 제거, 유관하지만 generic은 inline SVG로 대체 검토
```

자주 보이는 anti-pattern:
- "Hepatic structure IT" — 간 단면 일러스트가 영양·식도정맥류 페이지에 박혀있음 (무관)
- "HBV virion" — B형간염 모든 페이지에 동일 그림 (redundant)
- "Liver vascular anatomy" — 복수·간성혼수 페이지에 generic anatomy (무관)
- 작가명만 들어간 빈 caption — `<figcaption></figcaption>` (제거)

---

## 향후 보강 후보 (2026-05-11 기준)

inline SVG가 아직 없는 detail 페이지 중 우선순위 높은 것:
- 자가면역간염-진단/치료/약중단 ✅ (완료)
- 간양성종양-진단/혈관종/FNH-Adenoma/낭종-관리 ✅ (완료)
- C형간염-진단/완치후-추적 ✅ (완료)
- 알코올성-간질환 ✅ (완료)
- A형간염 ✅ (완료)
- 간암-BCLC병기 ✅ (완료)
- 빌리루빈-직접-간접 ✅ (완료)

다음 우선순위:
- 간경변-Child-Pugh-MELD (점수표 자체가 visualization 대상)
- 간경변-식도정맥류 (이미 banding 사진 있음 — 추가 필요성 낮음)
- 간암-치료-선택 (BCLC 단계별 결정 트리)
- 지방간-정밀검사 (FIB-4 → Fibroscan → MRE 단계)
