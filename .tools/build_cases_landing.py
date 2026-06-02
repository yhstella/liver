"""Rebuild /케이스/index.html with all 35 cases grouped by series."""
import os, sys, html as htmllib
sys.path.insert(0, os.path.dirname(__file__))
from pathlib import Path
import build_cases as bc1
import build_cases_other as bc2

ROOT = Path(__file__).resolve().parent.parent
def esc(s): return htmllib.escape(s or "")

# Series 1 (간암) cases come from build_cases.py (CASES list)
SERIES_GROUPS = [
    ("간암", "1", "/간암/", []),
    ("간경화", "2", "/간경화/", []),
    ("B형 간염", "3", "/B형간염/", []),
    ("지방간", "4", "/지방간/", []),
    ("간수치 이상", "5", "/간수치/", []),
    ("C형 간염", "6", "/C형간염/", []),
    ("자가면역간염", "7", "/자가면역간염/", []),
    ("간 양성종양", "8", "/간양성종양/", []),
]

# Group 간암 cases (1-12 to 1-26)
for i, c in enumerate(bc1.CASES):
    pid = f"1-{12 + i}"
    SERIES_GROUPS[0][3].append({
        "slug": c["slug"], "title": c["title"], "intro": c["intro"], "page_id": pid,
    })

# Group other series cases by their declared series
series_to_idx = {"간암": 0, "간경화": 1, "B형간염": 2, "지방간": 3, "간수치": 4}
for c in bc2.CASES:
    idx = series_to_idx.get(c["series"])
    if idx is None:
        continue
    SERIES_GROUPS[idx][3].append({
        "slug": c["slug"], "title": c["title"], "intro": c["intro"], "page_id": c["page_id"],
    })

# C형 간염 + 자가면역간염 케이스 (manually listed since not in bc1/bc2)
SERIES_GROUPS[5][3].extend([
    {"slug": "anti-HCV양성-첫발견", "title": "anti-HCV 양성 첫 발견 — RNA 확인부터 DAA까지",
     "intro": "<p>54세 여성, 직장 검진에서 anti-HCV(+) 첫 발견.</p>", "page_id": "6-4"},
    {"slug": "C형간염-간경변-새결절", "title": "C형간염 DAA 완치 5년 후 새 결절 발견",
     "intro": "<p>67세 남성, DAA SVR 5년 후 정기 EOB-MRI에서 1.4 cm 결절.</p>", "page_id": "6-5"},
])
SERIES_GROUPS[6][3].extend([
    {"slug": "AIH-첫진단-여성", "title": "젊은 여성의 AIH 첫 진단 — induction과 첫 6개월",
     "intro": "<p>32세 여성, ALT 380, IgG 28, ANA/ASMA 양성으로 AIH 진단.</p>", "page_id": "7-4"},
    {"slug": "AIH-약중단-재발", "title": "AIH 약 중단 시도 후 재발 — 재시작과 평생 유지 결정",
     "intro": "<p>45세 여성, AIH 진단 5년 후 약 중단 시도 → 6개월 시점 재발.</p>", "page_id": "7-5"},
])
SERIES_GROUPS[7][3].extend([
    {"slug": "큰낭종-bleomycin-경화요법", "title": "12 cm 단순 낭종 — bleomycin 경화요법",
     "intro": "<p>58세 여성, 12.5 cm 단순 낭종 + 압박 증상 → PAS(블레오마이신).</p>", "page_id": "8-5"},
])


def render_landing():
    sections_html = ""
    total_cases = 0
    for label, num, hub_url, items in SERIES_GROUPS:
        if not items:
            continue
        total_cases += len(items)
        rows = []
        for c in items:
            # Strip everything after em-dash for cleaner card title
            clean_title = c["title"].split(" — ")[0].strip()
            rows.append(
                f'<a href="/케이스/{c["slug"]}/" class="case-row">'
                f'<span class="page-id">{c["page_id"]}</span>'
                f'<div class="body"><h3>{esc(clean_title)}</h3></div></a>'
            )
        sections_html += (
            f'<section class="case-series-section" data-series="{num}" style="margin:32px 0">'
            f'<h2 style="font-family:\'Times New Roman\',Georgia,serif;font-size:20px;letter-spacing:-0.01em;font-weight:600;margin:0 0 6px;border-bottom:1px solid var(--line);padding-bottom:8px">'
            f'<a href="{hub_url}" style="color:var(--fg);text-decoration:none">{esc(label)} 사례</a>'
            f'<span style="font-size:12px;color:var(--muted);font-weight:400;margin-left:10px">{len(items)}편</span>'
            f'</h2>'
            f'<div class="case-list" style="border-top:0;margin-top:14px">'
            + "\n".join(rows) +
            f'</div></section>'
        )

    NAV = '''<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></nav></div></header>'''
    FOOTER = '''<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>'''

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>임상 케이스 모음 — Hepatology Note</title>
<meta name="description" content="간 질환 진료에서 자주 마주치는 상황을 가이드라인 적용 예시로 구성한 교육용 케이스 {total_cases}편. 간암·간경화·B형간염·지방간·간수치 이상 시리즈별 정리.">
<link rel="canonical" href="https://drshin.kr/케이스/">
<meta property="og:type" content="website">
<meta property="og:title" content="임상 케이스 모음 — {total_cases}편">
<meta property="og:description" content="시리즈별 임상 케이스 노트.">
<meta property="og:url" content="https://drshin.kr/케이스/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=3">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=3">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=3">
<link rel="manifest" href="/site.webmanifest?v=3">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>케이스</span></nav>

<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:32px;letter-spacing:-0.02em;font-weight:600;margin:8px 0 8px">임상 사례 모음</h1>
<p class="intro" id="introMsg">외래에서 자주 만나는 임상 사례를 단계별 결정 흐름과 함께 정리한 노트입니다. 총 {total_cases}편.</p>
<div id="filterBar" style="display:none;margin:12px 0 24px;padding:10px 14px;background:var(--accent-soft);border-radius:8px;font-size:14px;color:var(--accent)">
  <span id="filterLabel"></span>
  <a href="/케이스/" style="margin-left:12px;color:var(--accent);text-decoration:underline">전체 보기</a>
</div>

{sections_html}

<script>
(function(){{
  var params = new URLSearchParams(location.search);
  var s = params.get('series');
  if (!s) return;
  var sections = document.querySelectorAll('.case-series-section');
  var labels = {{'1':'간암','2':'간경화','3':'B형 간염','4':'지방간','5':'간수치 이상','6':'C형 간염','7':'자가면역간염','8':'간 양성종양'}};
  var visibleCount = 0;
  sections.forEach(function(sec){{
    if (sec.dataset.series === s) {{
      visibleCount++;
    }} else {{
      sec.style.display = 'none';
    }}
  }});
  if (visibleCount > 0 && labels[s]) {{
    var bar = document.getElementById('filterBar');
    var lbl = document.getElementById('filterLabel');
    lbl.textContent = labels[s] + ' 사례만 보고 있습니다.';
    bar.style.display = 'block';
  }}
}})();
</script>

<p class="disclaimer" style="margin-top:48px">이 사례는 표준 진료 흐름을 보여주기 위해 구성한 교육용 예시이며, 특정 환자의 기록이 아닙니다. 실제 진료는 개인의 상태에 따라 달라집니다.</p>
</main>

{FOOTER}
</body>
</html>
'''
    out = ROOT / "케이스" / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out} - {total_cases} cases across {sum(1 for g in SERIES_GROUPS if g[3])} series")


if __name__ == "__main__":
    render_landing()
