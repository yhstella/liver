#!/usr/bin/env python3
"""
migrate_AIH_to_autoimmune.py — 자가면역간염 → 자가면역간질환 hub rename + PBC 추가.

One-shot 마이그레이션 스크립트. 다음을 처리합니다:
  1. 새 hub 폴더 (자가면역간질환/) 생성 + 새 hub index.html 작성
  2. 옛 hub (자가면역간염/) → meta-refresh redirect 페이지로 교체
  3. 모든 AIH 세부페이지의 breadcrumb 갱신
     (<a href="/자가면역간염/">자가면역간염</a> → <a href="/자가면역간질환/">자가면역간질환</a>)
  4. article:section meta 갱신 (자가면역간염 → 자가면역간질환)
  5. 홈 series-tile 갱신 (label + href)
  6. 홈 meta description/og 갱신

WARNING: idempotent하지 않음. 한 번만 실행.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_HUB = ROOT / "자가면역간염"
NEW_HUB = ROOT / "자가면역간질환"

OLD_SLUG = "자가면역간염"
NEW_SLUG = "자가면역간질환"

# 옛 hub URL은 두 가지 형식이 섞여 있음
URL_PATTERNS = [
    ('/자가면역간염/', '/자가면역간질환/'),
    ('/%EC%9E%90%EA%B0%80%EB%A9%B4%EC%97%AD%EA%B0%84%EC%97%BC/',
     '/%EC%9E%90%EA%B0%80%EB%A9%B4%EC%97%AD%EA%B0%84%EC%A7%88%ED%99%98/'),
]


NEW_HUB_HTML = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>자가면역간질환 — Hepatology Note</title>
<meta name="description" content="자가면역간질환 대주제 — 자가면역간염(AIH)·원발성담즙성담관염(PBC)·overlap 증후군. 4축 진단(ALT·자가항체·IgG·조직), UDCA·면역억제 치료, 약 중단 결정, 임신·소아 등 특수상황까지 정리합니다.">
<link rel="canonical" href="https://drshin.kr/자가면역간질환/">
<meta name="author" content="신현재">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="자가면역간질환">
<meta property="og:url" content="https://drshin.kr/자가면역간질환/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=3">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=3">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=3">
<link rel="manifest" href="/site.webmanifest?v=3">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
<!-- verify:auto:start -->
<meta name="google-site-verification" content="x7NwlcpE-hA8N6Lf1h_i2wKk2RAiSDvv4wUXxV-CwRE">
<meta name="naver-site-verification" content="a978f4b99a9b45749c235f674d9ab6d31950470a">
<!-- verify:auto:end -->
<script src="/assets/js/search.js" defer></script>
</head>
<body>
<a class="skip-link" href="#content">본문 바로가기</a>
<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><form id="site-search" role="search" autocomplete="off" onsubmit="return false">
        <span class="search-icon" aria-hidden="true"><svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="9" r="6"/><line x1="13.5" y1="13.5" x2="17.5" y2="17.5"/></svg></span>
        <input class="search-input" type="search" placeholder="검색" aria-label="사이트 검색">
        <div class="search-panel">
          <div class="search-hits"></div>
          <ul class="search-results" role="listbox"></ul>
          <div class="search-status">↑↓ 이동 · Enter 열기 · Esc 닫기</div>
        </div>
      </form><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a>
      <a href="/keywords/">키워드</a></nav></div></header>
<main id="content" class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>자가면역간질환</span></nav>
<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:34px;letter-spacing:-0.025em;font-weight:600;margin:0 0 12px">자가면역간질환</h1>
<div class="series-meta"><span>세부주제 9편 · 사례 7편</span></div>
<p class="series-intro">자가면역으로 발생하는 간 질환 — 자가면역간염(AIH)·원발성담즙성담관염(PBC)·overlap 증후군을 다룹니다. 4축 진단(ALT·IgG·자가항체·조직), 표준 면역억제·UDCA 치료, 약 중단 결정, 임신·소아·급성 발현 등 특수 상황까지.</p>

<ul class="topic-list">
  <h3 class="cluster-header">자가면역간염(AIH)</h3>
  <li class="published"><a href="/자가면역간염-진단/"><span class="num">01</span><div class="body"><h3>AIH 진단</h3><p>ALT·IgG·자가항체·조직 4축, 다른 원인 배제, Simplified score</p></div><span class="status published">읽기 →</span></a></li>
  <li class="published"><a href="/자가면역간염-치료/"><span class="num">02</span><div class="body"><h3>AIH 표준 치료</h3><p>Induction → maintenance → 감량, 부작용 모니터링</p></div><span class="status published">읽기 →</span></a></li>
  <li class="published"><a href="/자가면역간염-약중단/"><span class="num">03</span><div class="body"><h3>AIH 약 중단</h3><p>2년 안정 + 조직 호전 시 검토, 재발 50-80%</p></div><span class="status published">읽기 →</span></a></li>
  <li class="published">
    <a href="/자가면역간염-스테로이드-부작용/"><span class="num">06</span>
      <div class="body">
        <h3>스테로이드 부작용 관리</h3>
        <p>Budesonide 전환과 모니터 일정</p>
      </div>
      <span class="status published">읽기 →</span>
    </a>
  </li>

  <h3 class="cluster-header">원발성담즙성담관염(PBC)</h3>
  <li class="published">
    <a href="/PBC-원발성담즙성담관염/"><span class="num">09</span>
      <div class="body">
        <h3>PBC 진단과 치료</h3>
        <p>AMA·ALP 진단, UDCA 1차 + obeticholic acid 2차, 가려움증 관리</p>
      </div>
      <span class="status published">읽기 →</span>
    </a>
  </li>
  <li class="published">
    <a href="/자가면역간염-PBC-overlap/"><span class="num">04</span>
      <div class="body">
        <h3>AIH·PBC overlap 증후군</h3>
        <p>Paris criteria + UDCA + 면역억제 병합</p>
      </div>
      <span class="status published">읽기 →</span>
    </a>
  </li>

  <h3 class="cluster-header">특수상황</h3>
  <li class="published">
    <a href="/자가면역간염-임신/"><span class="num">05</span>
      <div class="body">
        <h3>AIH와 임신</h3>
        <p>AZA 유지, MMF 금기, 산후 30~50% 재발</p>
      </div>
      <span class="status published">읽기 →</span>
    </a>
  </li>
  <li class="published">
    <a href="/자가면역간염-소아청소년/"><span class="num">07</span>
      <div class="body">
        <h3>소아·청소년 AIH</h3>
        <p>ASC overlap이 흔함, MRCP 필수</p>
      </div>
      <span class="status published">읽기 →</span>
    </a>
  </li>
  <li class="published">
    <a href="/자가면역간염-급성간부전/"><span class="num">08</span>
      <div class="body">
        <h3>급성 발현 AIH</h3>
        <p>빠른 면역억제 + 이식 평가 동시 진행</p>
      </div>
      <span class="status published">읽기 →</span>
    </a>
  </li>
</ul>

<a href="/케이스/" style="display:flex;align-items:center;justify-content:space-between;margin:32px 0;padding:18px 24px;background:var(--accent-soft);border:1px solid var(--accent);border-radius:10px;text-decoration:none;color:var(--fg);transition:background .15s">
  <div>
    <strong style="display:block;color:var(--accent);font-size:14px;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px">자가면역간질환 케이스</strong>
  </div>
  <span style="color:var(--accent);font-size:18px;font-weight:600">→</span>
</a>
<h2 style="margin-top:64px;font-size:14px;letter-spacing:0.1em;color:var(--muted);text-transform:uppercase;border-bottom:1px solid var(--line);padding-bottom:8px;font-weight:600">다른 주제</h2>
<div class="series-grid">
  <a href="/간암/" class="series-tile"><h3>간암</h3><p>BCLC 병기, 절제·색전·면역치료 선택, 간이식, 검진과 재발.</p></a>
  <a href="/간경화/" class="series-tile"><h3>간경화</h3><p>대상성·비대상성, Child-Pugh·MELD, 정맥류·복수·간성혼수 관리.</p></a>
  <a href="/B형간염/" class="series-tile"><h3>B형 간염</h3><p>약 시작·중단, 검사결과 해석, 가족 검사, 임신·수유, 항바이러스제.</p></a>
  <a href="/지방간/" class="series-tile"><h3>지방간</h3><p>MASLD 새 명명, 정밀검사, 운동·식이·약물, lean MASLD.</p></a>
  <a href="/간수치/" class="series-tile"><h3>간수치 이상</h3><p>ALT·AST·GGT 차이, 빌리루빈·알부민·PT, 약물성 간 손상.</p></a>
  <a href="/C형간염/" class="series-tile"><h3>C형 간염</h3><p>anti-HCV에서 HCV RNA, DAA 8주 완치, SVR 후 평생 추적.</p></a>
  <a href="/간양성종양/" class="series-tile"><h3>간 양성종양</h3><p>혈관종·낭종·FNH·선종 감별, 큰 증상 낭종의 경화요법.</p></a>
</div>
</main>
<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a>
      <a href="/keywords/">키워드</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>
</body>
</html>
'''

REDIRECT_HTML = '''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>자가면역간질환 — Hepatology Note</title>
<meta http-equiv="refresh" content="0; url=/자가면역간질환/">
<link rel="canonical" href="https://drshin.kr/자가면역간질환/">
<meta name="robots" content="noindex,follow">
<script>location.replace("/자가면역간질환/");</script>
</head>
<body>
<p>이 페이지는 <a href="/자가면역간질환/">자가면역간질환</a> 으로 이동했습니다.</p>
</body>
</html>
'''


def write_new_hub():
    NEW_HUB.mkdir(parents=True, exist_ok=True)
    (NEW_HUB / "index.html").write_text(NEW_HUB_HTML, encoding="utf-8")
    print(f"[OK] new hub: {NEW_HUB}/index.html")


def write_redirect():
    """옛 hub를 redirect 페이지로 교체."""
    (OLD_HUB / "index.html").write_text(REDIRECT_HTML, encoding="utf-8")
    print(f"[OK] redirect at {OLD_HUB}/index.html")


def update_detail_breadcrumbs():
    """모든 AIH 세부페이지 (자가면역간염-*) 의 breadcrumb 갱신.

    Crumb 패턴: <a href="/자가면역간염/">자가면역간염</a>
    → <a href="/자가면역간질환/">자가면역간질환</a>
    """
    pages_updated = 0
    for slug_dir in ROOT.glob("자가면역간염-*"):
        idx = slug_dir / "index.html"
        if not idx.exists():
            continue
        text = idx.read_text(encoding="utf-8")
        original = text

        # 1. breadcrumb hub link
        text = re.sub(
            r'<a href="/자가면역간염/">자가면역간염</a>',
            '<a href="/자가면역간질환/">자가면역간질환</a>',
            text,
        )
        # 2. article:section meta
        text = text.replace(
            'property="article:section" content="자가면역간염"',
            'property="article:section" content="자가면역간질환"',
        )
        if text != original:
            idx.write_text(text, encoding="utf-8")
            pages_updated += 1
            print(f"  [crumb] {slug_dir.name}")
    print(f"[OK] {pages_updated} AIH detail pages updated.")


def update_cc_and_case_breadcrumbs():
    """CC, 케이스 페이지 중 breadcrumb이 자가면역간염을 가리키는 경우 갱신."""
    pages_updated = 0
    for sub in ["CC", "케이스"]:
        sub_root = ROOT / sub
        if not sub_root.exists():
            continue
        for idx in sub_root.rglob("index.html"):
            text = idx.read_text(encoding="utf-8")
            original = text
            text = re.sub(
                r'<a href="/자가면역간염/">자가면역간염</a>',
                '<a href="/자가면역간질환/">자가면역간질환</a>',
                text,
            )
            text = text.replace(
                'property="article:section" content="자가면역간염"',
                'property="article:section" content="자가면역간질환"',
            )
            if text != original:
                idx.write_text(text, encoding="utf-8")
                pages_updated += 1
                print(f"  [crumb] {sub}/{idx.parent.name}")
    print(f"[OK] {pages_updated} CC/case pages updated.")


def update_homepage():
    """홈 series-tile, meta description, og:description, JSON-LD."""
    home = ROOT / "index.html"
    text = home.read_text(encoding="utf-8")
    original = text

    # meta description
    text = text.replace(
        '간암·간경화·B형간염·C형간염·지방간·간수치 이상·자가면역간염·간 양성종양',
        '간암·간경화·B형간염·C형간염·지방간·간수치 이상·자가면역간질환·간 양성종양',
    )
    # og:description
    text = text.replace(
        '간 질환 8 대주제(간암·간경화·B/C형간염·지방간·간수치·자가면역간염·간 양성종양)',
        '간 질환 8 대주제(간암·간경화·B/C형간염·지방간·간수치·자가면역간질환·간 양성종양)',
    )
    # series-tile (label + href)
    text = re.sub(
        r'<a href="/자가면역간염/" class="series-tile">\s*<h3>자가면역간염</h3>',
        '<a href="/자가면역간질환/" class="series-tile">\n    <h3>자가면역간질환</h3>',
        text,
    )

    if text != original:
        home.write_text(text, encoding="utf-8")
        print(f"[OK] homepage updated")
    else:
        print(f"[skip] homepage already current")


def main():
    print("=" * 60)
    print("AIH → 자가면역간질환 hub migration")
    print("=" * 60)
    print()
    write_new_hub()
    update_detail_breadcrumbs()
    update_cc_and_case_breadcrumbs()
    update_homepage()
    write_redirect()
    print()
    print("Migration complete. Next steps:")
    print("  1. python .tools/inject_hub_bar.py   # 모든 페이지 hub-bar 새 hub 반영")
    print("  2. python .tools/inject_jsonld.py    # JSON-LD breadcrumb 재생성")
    print("  3. python .tools/rebuild_seo.py      # sitemap·search·llms 일괄 갱신")


if __name__ == "__main__":
    main()
