"""Build /연구/index.html from pubs.json (CV publications data)."""
import json, html as htmllib, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / ".tools" / "pubs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pubs_sheet = data["Publications"]
header = pubs_sheet[0]
rows = pubs_sheet[1:]

# Column indices
COL = {h: i for i, h in enumerate(header)}

def esc(s): return htmllib.escape(s or "")

def highlight_shin(authors):
    """Bold 'Shin H' in author list."""
    return re.sub(r'\b(Shin H)\b', r'<strong>\1</strong>', esc(authors))

def parse_authors_from_citation(citation, title):
    """Citation format: 'Author1, Author2, ... Title. Journal. Year...'
    Authors part is everything before the title."""
    if title in citation:
        authors = citation.split(title)[0].strip().rstrip(".").strip()
        return authors
    return ""

def if_class(if_val):
    try:
        v = float(if_val)
        if v >= 20: return "if-very-high"
        if v >= 10: return "if-high"
        if v >= 5: return "if-mid"
        return "if-low"
    except (ValueError, TypeError):
        return "if-low"

def role_badge(role):
    if role == "주저자":
        return '<span class="role-badge role-lead">주저자</span>'
    if role == "공저자":
        return '<span class="role-badge role-co">공저자</span>'
    return '<span class="role-badge role-other">commentary</span>'

# Group by role
groups = {"주저자": [], "공저자": [], "기타": []}
for r in rows:
    role = r[COL["역할"]]
    groups[role].append(r)

# Sort within each group: newest first (year desc, then month)
month_order = {m: i for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}
def sort_key(r):
    try: y = -int(r[COL["출판연도"]])
    except: y = 0
    m = month_order.get(r[COL["월"]], 99)
    return (y, m)
for k in groups:
    groups[k].sort(key=sort_key)

# Stats
total = len(rows)
n_lead = len(groups["주저자"])
n_co = len(groups["공저자"])
n_other = len(groups["기타"])

# Compute IFs
def get_if(r):
    try: return float(r[COL["Impact Factor"]])
    except (ValueError, TypeError): return 0.0
all_if = [get_if(r) for r in rows]
total_if = sum(all_if)
avg_if = total_if / total if total else 0
max_if = max(all_if) if all_if else 0
lead_if_total = sum(get_if(r) for r in groups["주저자"])
lead_if_avg = lead_if_total / n_lead if n_lead else 0

def render_pub(r):
    role = r[COL["역할"]]
    year = r[COL["출판연도"]]
    month = r[COL["월"]]
    journal = r[COL["저널명"]]
    vol = r[COL["권"]]
    issue = r[COL["호"]]
    pages = r[COL["쪽수"]]
    title = r[COL["논문명"]]
    citation = r[COL["서지정보"]]
    if_val = r[COL["Impact Factor"]]
    doi = r[COL["DOI"]]
    pmid = r[COL["PMID"]]

    authors = parse_authors_from_citation(citation, title)
    authors_html = highlight_shin(authors)

    journal_line_parts = [f'<em>{esc(journal)}</em>']
    if year: journal_line_parts.append(f'{esc(year)}')
    if vol:
        vol_part = esc(vol)
        if issue: vol_part += f'({esc(issue)})'
        if pages: vol_part += f':{esc(pages)}'
        journal_line_parts.append(vol_part)
    journal_line = ' · '.join(journal_line_parts)

    if_html = ""
    if if_val:
        if_html = f'<span class="if-badge {if_class(if_val)}">IF {esc(if_val)}</span>'

    links = []
    if doi:
        links.append(f'<a href="https://doi.org/{esc(doi)}" target="_blank" rel="noopener">DOI</a>')
    if pmid:
        links.append(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{esc(pmid)}/" target="_blank" rel="noopener">PMID {esc(pmid)}</a>')
    links_html = ' · '.join(links)

    return f'''<article class="pub-card">
  <div class="pub-meta">
    {role_badge(role)}
    {if_html}
    <span class="pub-year">{esc(year)} {esc(month)}</span>
  </div>
  <h3 class="pub-title">{esc(title)}</h3>
  <p class="pub-authors">{authors_html}</p>
  <p class="pub-journal">{journal_line}</p>
  <p class="pub-links">{links_html}</p>
</article>'''

def render_group(title, items, intro=""):
    if not items: return ""
    cards = "\n".join(render_pub(r) for r in items)
    intro_html = f'<p class="group-intro">{intro}</p>' if intro else ''
    return f'''<section class="pub-group">
<h2 class="group-title">{esc(title)} <span class="group-count">{len(items)}편</span></h2>
{intro_html}
<div class="pub-grid">
{cards}
</div>
</section>'''

NAV = '''<header class="site-header">
  <div class="inner">
    <a href="/" class="brand-mark">Hepatology<em> Note</em></a>
    <nav class="site-nav">
      <a href="/소개/">소개</a>
      <a href="/연구/" class="active">연구</a>
      <a href="/updates/">Updates</a>
    </nav>
  </div>
</header>'''

FOOTER = '''<footer class="site-footer">
  <div class="inner">
    <div class="col">
      <strong>Hepatology Note</strong>
      <p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p>
    </div>
    <div class="col">
      <strong>안내</strong>
      <a href="/소개/">소개</a>
      <a href="/연구/">연구</a>
      <a href="/updates/">Updates</a>
    </div>
    <div class="col">
      <strong>외부 링크</strong>
      <a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a>
    </div>
    <div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div>
  </div>
</footer>'''

PAGE_STYLE = '''<style>
.research-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:24px 0 40px}
.research-stats > div{background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 14px;text-align:center}
.research-stats strong{display:block;font-size:28px;font-weight:700;color:var(--accent);letter-spacing:-0.02em}
.research-stats span{font-size:12px;color:var(--muted);letter-spacing:0.04em}

.pub-group{margin:48px 0}
.group-title{font-family:'Times New Roman',Georgia,serif;font-size:22px;letter-spacing:-0.01em;font-weight:600;margin:0 0 6px;border-bottom:2px solid var(--line);padding-bottom:8px}
.group-count{display:inline-block;background:var(--accent-soft);color:var(--accent);font-size:13px;padding:2px 10px;border-radius:99px;font-weight:600;margin-left:8px;vertical-align:middle}
.group-intro{font-size:14px;color:var(--muted);margin:8px 0 18px;line-height:1.7}

.pub-grid{display:flex;flex-direction:column;gap:14px}
.pub-card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 20px;transition:border-color .15s}
.pub-card:hover{border-color:var(--accent)}
.pub-meta{display:flex;gap:8px;align-items:center;margin-bottom:8px;font-size:12px;flex-wrap:wrap}
.pub-year{color:var(--muted);letter-spacing:0.02em;margin-left:auto}

.role-badge{display:inline-block;font-size:11px;padding:2px 9px;border-radius:99px;letter-spacing:0.05em;font-weight:600;text-transform:uppercase}
.role-lead{background:var(--accent);color:#fff}
.role-co{background:#e8f3ef;color:var(--accent)}
.role-other{background:#f3f1ec;color:var(--muted)}

.if-badge{display:inline-block;font-size:11px;padding:2px 9px;border-radius:99px;font-weight:600;letter-spacing:0.02em;font-family:'Times New Roman',Georgia,serif}
.if-very-high{background:#fce7e0;color:#c9542b}
.if-high{background:#fef3e0;color:#b8650a}
.if-mid{background:#e8f3ef;color:var(--accent)}
.if-low{background:#f3f1ec;color:var(--muted)}

.pub-title{margin:4px 0 8px;font-size:16px;line-height:1.45;font-weight:600;letter-spacing:-0.005em;color:var(--fg)}
.pub-authors{margin:0 0 4px;font-size:13.5px;color:var(--muted);line-height:1.55}
.pub-authors strong{color:var(--fg);font-weight:600}
.pub-journal{margin:0 0 6px;font-size:13.5px;color:#2a2a2a;line-height:1.55}
.pub-journal em{font-style:italic;font-weight:600}
.pub-links{margin:0;font-size:12.5px;display:flex;gap:12px}
.pub-links a{color:var(--accent);text-decoration:none}
.pub-links a:hover{text-decoration:underline}

.research-intro{font-size:16px;line-height:1.7;color:#2a2a2a;margin:8px 0 24px;max-width:640px}

@media (max-width: 600px) {
  .research-stats{grid-template-columns:repeat(2,1fr)}
  .pub-meta .pub-year{margin-left:0;flex-basis:100%}
}
</style>'''

LEAD_INTRO = "1저자 또는 공동 1저자로 주도한 연구. J Hepatol·Hepatology·Clinical and Molecular Hepatology 등 hepatology 주요 저널 중심."
CO_INTRO = "공저자로 참여한 다기관 연구·코호트 분석·메타분석. SNUH 간센터 및 외부 협력 그룹과 함께 진행."
OTHER_INTRO = "초청 commentary 등."

body_groups = (
    render_group("주저자 — 1저자 / 공동 1저자", groups["주저자"], LEAD_INTRO) +
    "\n\n" +
    render_group("공저자", groups["공저자"], CO_INTRO) +
    "\n\n" +
    render_group("기타 — Commentary", groups["기타"], OTHER_INTRO)
)

html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>연구 — Hepatology Note</title>
<meta name="description" content="신현재 — 대표 연구 논문. 주저자 {n_lead}편 + 공저자 {n_co}편 + commentary {n_other}편 (누적 IF {total_if:.0f}).">
<link rel="canonical" href="https://drshin.kr/연구/">
<meta name="author" content="신현재">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="연구 — Hepatology Note">
<meta property="og:description" content="주저자 {n_lead}편 + 공저자 {n_co}편 + commentary {n_other}편 (누적 IF {total_if:.0f}).">
<meta property="og:url" content="https://drshin.kr/연구/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"CollectionPage","@id":"https://drshin.kr/연구/#webpage","url":"https://drshin.kr/연구/","name":"연구","description":"신현재의 대표 연구 논문 {total}편","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}},"isPartOf":{{"@id":"https://drshin.kr/#website"}}}},
{{"@type":"Person","@id":"https://drshin.kr/#author","name":"신현재","jobTitle":"서울대학교병원 소화기내과 · 간암센터","worksFor":{{"@type":"Hospital","name":"서울대학교병원","url":"https://www.snuh.org/"}},"image":"https://drshin.kr/assets/img/author/drshin.jpg","url":"https://drshin.kr/소개/"}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},{{"@type":"ListItem","position":2,"name":"연구","item":"https://drshin.kr/연구/"}}]}}
]}}
</script>
{PAGE_STYLE}
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>연구</span></nav>

<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:32px;letter-spacing:-0.02em;font-weight:600;margin:8px 0 4px">연구</h1>
<p class="meta">Peer-reviewed publications · 대한간학회·SNUH 간센터 협력</p>

<p class="research-intro">간세포암(HCC)·만성 B형간염·MASLD를 중심으로 한 임상·역학 연구. 다기관 코호트, mendelian randomization, AI 기반 영상 예측 모델, 면역치료 결과 분석 등을 포괄.</p>

<div class="research-stats">
  <div><strong>{total}</strong><span>총 게재</span></div>
  <div><strong>{n_lead}</strong><span>주저자</span></div>
  <div><strong>{avg_if:.1f}</strong><span>평균 IF</span></div>
  <div><strong>{total_if:.0f}</strong><span>누적 IF</span></div>
</div>

{body_groups}

<aside style="background:#fff;border:1px solid var(--line);border-radius:10px;padding:18px 22px;margin:32px 0;font-size:14px;line-height:1.7">
  <strong style="display:block;font-size:13px;color:var(--muted);letter-spacing:0.06em;margin-bottom:6px">PUBMED 검색</strong>
  <p style="margin:0 0 6px"><a href="https://pubmed.ncbi.nlm.nih.gov/?term=Shin+H+Liver+Research+Institute+Seoul+National+University" target="_blank" rel="noopener">PubMed: Shin H + SNUH Liver Research Institute ↗</a></p>
  <p style="margin:0;color:var(--muted);font-size:13px">동명이인이 있을 수 있어 affiliation(SNUH Internal Medicine, Liver Research Institute) 확인 후 사용.</p>
</aside>

<p class="disclaimer">본 페이지는 학술 정보 제공 목적이며, 인용은 원 출처(저널·DOI)를 따라주시기 바랍니다.</p>
</main>

{FOOTER}
</body>
</html>
'''

out = ROOT / "연구" / "index.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html, encoding="utf-8")
print(f"Wrote {out} ({len(html)} bytes, {total} pubs)")
