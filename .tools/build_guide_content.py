"""Render plaintext guide HTML reflecting new 6-series IA."""
import json
import html as htmllib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 6 series + 10 topics each (mirrors build_series_hubs.py)
SERIES = {
    "간암": ("01", [
        ("간암 진단을 받았을 때, 첫 외래에서 결정되는 것", "/간암-진단-첫외래/"),
        ("BCLC 병기와 치료 옵션 — 무엇이 어떤 환자에게", None),
        ("절제술 vs 색전술 vs 방사선 — 선택의 기준", "/간암-치료-선택/"),
        ("면역치료 1차 시대 — atezolizumab+bevacizumab과 그 이후", "/간암-면역치료-1차/"),
        ("간이식 — 적응증과 대기 기간", "/간암-간이식/"),
        ("AFP(알파태아단백) — 정상범위와 간암 의심 기준", "/알파태아단백/"),
        ("B형간염 환자가 6개월마다 간암 검진을 받아야 하는 이유", "/B형간염-간암검진/"),
        ("지방간에서 간암까지 — 비알코올성 간질환의 간암 위험", "/지방간-간암/"),
        ("간암 재발 추적 — 첫 5년의 일정", "/간암-재발-추적/"),
        ("간암 환자가 알아야 할 식이·일상", "/간암-식이-일상/"),
    ]),
    "간경화": ("02", [
        ("대상성 vs 비대상성 간경변", "/간경변-대상성-비대상성/"),
        ("Child-Pugh와 MELD — 점수가 의미하는 것", "/간경변-Child-Pugh-MELD/"),
        ("식도정맥류 — 첫 신호와 예방적 결찰", "/간경변-식도정맥류/"),
        ("복수 — 단계별 관리", "/간경변-복수/"),
        ("간성혼수 — 외래에서 알아채는 신호", "/간경변-간성혼수/"),
        ("간신증후군 — 진단과 즉각 대응", "/간경변-간신증후군/"),
        ("간경변 영양·근감소증 관리", "/간경변-영양-근감소증/"),
        ("간이식 평가 — 누가, 언제 시작하나", "/간경변-간이식-평가/"),
        ("간경변 환자가 피해야 할 약·영양제", "/간경변-약물-주의/"),
        ("간기능검사가 정상인데 간경변? — 진행된 간경변의 함정", "/간경변-정상수치-함정/"),
    ]),
    "B형간염": ("03", [
        ("B형간염 약을 평생 먹어야 하나", "/B형간염-평생약/"),
        ("B형간염 검사 결과지 해석", "/B형간염-검사결과/"),
        ("B형간염 보균자와 결혼·임신·수유", "/B형간염-결혼-임신/"),
        ("가족 중 B형간염 환자가 있다면 받아야 할 검사 3가지", "/가족-B형간염-검사/"),
        ("B형간염 백신 — 누가, 언제, 몇 번", "/B형간염-백신/"),
        ("HBeAg 양성 vs 음성 — 무엇이 다른가", "/B형간염-HBeAg-양성-음성/"),
        ("항바이러스제 비교 — TDF · TAF · ETV", "/B형간염-항바이러스제-비교/"),
        ("B형간염 functional cure — 어디까지 와 있나", "/B형간염-functional-cure/"),
        ("항암치료·면역억제제와 B형간염 재활성화", "/B형간염-재활성화/"),
        ("C형간염 DAA 8주 완치", "/C형간염-완치-DAA/"),
    ]),
    "지방간": ("04", [
        ("NAFLD가 MASLD로 바뀐 이유", "/대사이상지방간-MASLD/"),
        ("술 안 마시는데 지방간", "/술-안마셔도-지방간/"),
        ("지방간 치료 — 운동·식이·약물", "/지방간-치료/"),
        ("지방간에 좋은 음식·피해야 할 음식", "/지방간-음식/"),
        ("지방간 회복 6개월 패턴", "/지방간-회복-6개월/"),
        ("지방간 정밀검사 — FIB-4·Fibroscan·MRE", "/지방간-정밀검사/"),
        ("lean MASLD — 마른 사람의 지방간", "/지방간-lean-MASLD/"),
        ("resmetirom과 차세대 지방간 약물", "/지방간-신약-resmetirom/"),
        ("지방간염(MASH) — 단순 지방간과 무엇이 다른가", "/지방간염-MASH/"),
        ("SGLT2·GLP-1 작용제와 지방간", "/지방간-SGLT2-GLP1/"),
    ]),
    "간수치": ("05", [
        ("건강검진 간수치(AST·ALT) 높음, 첫 단계", "/간수치-높음/"),
        ("AST·ALT·GGT 차이", "/간수치-종류-차이/"),
        ("Fibroscan 수치 읽는 법 — F0부터 F4까지", "/간섬유화스캔-수치/"),
        ("빌리루빈 — 직접·간접 차이", "/빌리루빈-직접-간접/"),
        ("알부민·PT — 간 합성능 보는 방법", "/알부민-PT-간합성능/"),
        ("ALP·GGT — 담도 vs 간세포 손상", "/ALP-GGT-담도-간세포/"),
        ("약물·영양제·한약 — 간 손상 가능성 점검", "/약물성-간손상-DILI/"),
        ("간수치 정상인데도 간경변일 수 있다", "/간경변-정상수치-함정/"),
        ("PIVKA-II — 간암 종양표지자의 또 다른 축", "/PIVKA-II-간암마커/"),
        ("간생검 — 언제 필요한가", "/간생검-언제-필요한가/"),
    ]),
    "최신 지견": ("06", [
        ("MAESTRO-NASH — resmetirom NEJM 2024", "/updates/MAESTRO-NASH-resmetirom-NEJM-2024/"),
        ("IMbrave150 — atezo+bev NEJM 2020", "/updates/IMbrave150-atezolizumab-bevacizumab-NEJM-2020/"),
        ("HIMALAYA — durva+treme NEJM Evid 2022", "/updates/HIMALAYA-durvalumab-tremelimumab-NEJM-Evid-2022/"),
        ("Pan TDF for HBV in pregnancy NEJM 2016", "/updates/Pan-TDF-pregnancy-HBV-NEJM-2016/"),
        ("Newsome semaglutide NASH NEJM 2021", "/updates/Newsome-semaglutide-NASH-NEJM-2021/"),
        ("Baveno VII portal hypertension J Hepatol 2022", "/updates/Baveno-VII-portal-hypertension-J-Hepatol-2022/"),
    ]),
}

def esc(s): return htmllib.escape(s or "")

# Compute counts
total_topics = sum(len(s[1]) for s in SERIES.values())
total_published = sum(1 for s in SERIES.values() for t in s[1] if t[1])
total_draft = total_topics - total_published

parts = []

# Overview
parts.append(f"""
<section class="overview">
  <h2>사이트 한눈에</h2>
  <div class="stats">
    <div><strong>{len(SERIES)}</strong><span>시리즈</span></div>
    <div><strong>{total_topics}</strong><span>계획 토픽</span></div>
    <div><strong style="color:var(--accent)">{total_published}</strong><span>게시됨</span></div>
    <div><strong style="color:#c9542b">{total_draft}</strong><span>준비 중</span></div>
  </div>
  <ul class="convention">
    <li>브랜드: <strong>Hepatology Note</strong> · 한국어 부제 "간질환 가이드와 임상 노트"</li>
    <li>저자 표기: 글마다 photo + "서울대학교병원 소화기내과 · 간암센터" (이름·직책 단어 없음)</li>
    <li>JSON-LD Person.name = "신현재" 유지 (E-E-A-T 신호, 검색·LLM 인용용)</li>
    <li>새 페이지: <code>/소개/</code> (학력·경력·진료분야), <code>/논문/</code> (대표 논문 — 입력 대기)</li>
  </ul>
""")

# Migration map
parts.append("""
  <div class="alert" style="border-left-color:var(--accent);background:var(--accent-soft)">
    <strong style="color:var(--accent)">2026-05-08 리브랜드 완료</strong>
    <p>"간 건강 가이드" → "Hepatology Note"로 브랜드 변경. 17개 기존 글이 새 6 시리즈 IA로 이주됨. villagebaby.kr 잔재 일괄 정리. 모든 글 byline에서 "글쓴이 신현재", "진료조교수" 표현 제거.</p>
  </div>
</section>
""")

# Series cards — show each series with all 10 topics, marked published/draft
for series_name, (num, topics) in SERIES.items():
    pub_count = sum(1 for t in topics if t[1])
    parts.append(f'<section class="series">\n')
    display = "B형 간염" if series_name == "B형간염" else ("간수치 이상" if series_name == "간수치" else series_name)
    series_url = "/updates/" if series_name == "최신 지견" else f"/{series_name}/"
    parts.append(f'  <h2>SERIES {num} · {esc(display)} <span class="count">{pub_count}/{len(topics)}</span></h2>\n')
    parts.append(f'  <p style="margin:0 0 14px;color:var(--muted);font-size:14px"><a href="{esc(series_url)}" target="_blank" rel="noopener" style="color:var(--accent);text-decoration:none">{esc(series_url)} 허브 페이지 ↗</a></p>\n')
    parts.append('  <div class="cards">\n')
    for i, (title, slug) in enumerate(topics, 1):
        parts.append('  <article class="card">\n')
        parts.append(f'    <div class="card-head">\n')
        parts.append(f'      <code class="slug">{i:02d}</code>\n')
        if slug:
            parts.append(f'      <a class="visit" href="{esc(slug)}" target="_blank" rel="noopener">열기 ↗</a>\n')
        else:
            parts.append(f'      <span class="status draft" style="font-size:11px;color:#c9542b;background:#fbe9e1;padding:2px 8px;border-radius:99px;letter-spacing:0.05em;font-weight:600">준비 중</span>\n')
        parts.append(f'    </div>\n')
        parts.append(f'    <h3>{esc(title)}</h3>\n')
        if slug:
            parts.append(f'    <p class="desc" style="color:var(--accent);font-size:12.5px;margin-top:8px"><code style="color:inherit;background:transparent;padding:0">{esc(slug)}</code></p>\n')
        parts.append('  </article>\n')
    parts.append('  </div>\n')
    parts.append('</section>\n')

# Coverage / next steps
parts.append("""
<section class="gaps">
  <h2>다음 작업 우선순위</h2>
  <p>토픽 본문 추가는 시리즈별로 batch 작성을 권장합니다. 한 시리즈 내에서 글이 모이면 cross-link이 풍부해지고, 검색에서 "topic cluster"로 인식됩니다.</p>
  <div class="gap-grid">
    <div>
      <strong>1순위 — 간경화 (10편 전부 신규)</strong>
      <ul>
        <li>현재 게시 0편 — 가장 비어 있는 시리즈</li>
        <li>외래 빈도 높은 토픽 (복수·정맥류·간성혼수)부터 권장</li>
        <li>5편 단위 batch 작성 권장</li>
      </ul>
    </div>
    <div>
      <strong>2순위 — 간암 (7편 신규)</strong>
      <ul>
        <li>현재 게시 3편 (AFP, B형 검진, 지방간→간암)</li>
        <li>BCLC 병기·치료 선택·면역치료 1차가 검색 수요 ↑</li>
      </ul>
    </div>
    <div>
      <strong>3순위 — 간수치 (7편 신규)</strong>
      <ul>
        <li>현재 게시 3편 (AST/ALT/GGT, Fibroscan)</li>
        <li>빌리루빈·알부민·PT는 간단한 글로 빠르게 채울 수 있음</li>
      </ul>
    </div>
    <div>
      <strong>4순위 — B형간염 (5편 신규)</strong>
      <ul>
        <li>현재 게시 5편 (포함 C형 1편)</li>
        <li>functional cure / 항암 시 재활성화는 의료진 검색에도 유리</li>
      </ul>
    </div>
    <div>
      <strong>5순위 — 지방간 (4편 신규)</strong>
      <ul>
        <li>현재 게시 6편 — 가장 채워진 시리즈</li>
        <li>resmetirom·MASH 본문 등 신약 토픽이 신선도 신호</li>
      </ul>
    </div>
    <div>
      <strong>병행 — 최신 지견 (Updates)</strong>
      <ul>
        <li>현재 0편</li>
        <li>의료진·SEO 양측에 유리. 학회 가이드라인 update가 검색 신선도 강함</li>
      </ul>
    </div>
  </div>
</section>

<section class="overview">
  <h2>알려진 이슈 / 향후 보강</h2>
  <ul class="convention">
    <li><strong>Series 3 (B형) 5개 글</strong>: tldr·FAQ가 비어있음. 본문은 충실하나 head JSON-LD에 FAQPage 누락. SEO 향상을 위해 5문항씩 보강 권장.</li>
    <li><strong>이미지·다이어그램</strong>: 글마다 SVG 다이어그램 2–3개 (예: MASLD progression, BCLC stages, HBV markers). 의학 저널 그림은 저작권 — 직접 SVG로 재구성 권장.</li>
    <li><strong>sitemap.xml / robots.txt</strong>: 미작성. 다음 단계에 Naver/Google 인증 메타와 함께 추가.</li>
    <li><strong>논문 페이지</strong>: <code>/논문/</code> 골격만 있음. PubMed ID 또는 인용정보 입력 후 자동 채움.</li>
    <li><strong>대표 og:image</strong>: 현재 모든 글이 author photo를 og:image로 사용. 글마다 hero 이미지가 생기면 페이지별로 갱신 권장.</li>
  </ul>
</section>
""")

content = "".join(parts)

out = ROOT / ".tools" / "guide_content.html"
out.write_text(content, encoding="utf-8")
print(f"Wrote {out} ({len(content)} bytes, {total_topics} topics, {total_published} published)")
