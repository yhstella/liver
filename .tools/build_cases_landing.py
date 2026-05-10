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
    ("B형간염", "3", "/B형간염/", []),
    ("지방간", "4", "/지방간/", []),
    ("간수치 이상", "5", "/간수치/", []),
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
            f'<section style="margin:32px 0">'
            f'<h2 style="font-family:\'Times New Roman\',Georgia,serif;font-size:20px;letter-spacing:-0.01em;font-weight:600;margin:0 0 6px;border-bottom:1px solid var(--line);padding-bottom:8px">'
            f'<a href="{hub_url}" style="color:var(--fg);text-decoration:none">{esc(label)} 케이스</a>'
            f'<span style="font-size:12px;color:var(--muted);font-weight:400;margin-left:10px">{len(items)}편 · {num}-시리즈</span>'
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
<meta name="description" content="외래에서 자주 만나는 임상 시나리오 {total_cases}편. 간암·간경화·B형간염·지방간·간수치 이상 시리즈별 케이스 노트.">
<link rel="canonical" href="https://drshin.kr/케이스/">
<meta property="og:type" content="website">
<meta property="og:title" content="임상 케이스 모음 — {total_cases}편">
<meta property="og:description" content="시리즈별 임상 케이스 노트.">
<meta property="og:url" content="https://drshin.kr/케이스/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>케이스</span></nav>

<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:32px;letter-spacing:-0.02em;font-weight:600;margin:8px 0 8px">임상 케이스 모음</h1>
<p class="intro">외래에서 자주 만나는 임상 시나리오를 풀어 정리한 케이스 노트입니다. 시리즈별로 진단부터 치료·합병증까지 단계별 결정 흐름을 따라갑니다. 총 {total_cases}편.</p>

{sections_html}

<p class="disclaimer" style="margin-top:48px">본 케이스들은 외래에서 자주 만나는 임상 시나리오를 익명화하여 재구성한 교육 자료입니다. 환자 식별 정보는 모두 변경되었으며, 임상 결정은 표준 가이드라인의 한 예시일 뿐 개별 환자에 그대로 적용되지 않습니다.</p>
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
