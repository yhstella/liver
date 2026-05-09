"""Build /연구/index.html from pubs.json - simple publication list, no IF/stats."""
import json, html as htmllib, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / ".tools" / "pubs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

pubs_sheet = data["Publications"]
header = pubs_sheet[0]
rows = pubs_sheet[1:]

COL = {h: i for i, h in enumerate(header)}

def esc(s): return htmllib.escape(s or "")

def highlight_shin(authors):
    return re.sub(r'\b(Shin H)\b', r'<strong>\1</strong>', esc(authors))

def parse_authors_from_citation(citation, title):
    if title in citation:
        authors = citation.split(title)[0].strip().rstrip(".").strip()
        return authors
    return ""

# Group by role
groups = {"주저자": [], "공저자": [], "기타": []}
for r in rows:
    role = r[COL["역할"]]
    groups[role].append(r)

month_order = {m: i for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}
def sort_key(r):
    try: y = -int(r[COL["출판연도"]])
    except: y = 0
    m = month_order.get(r[COL["월"]], 99)
    return (y, m)
for k in groups:
    groups[k].sort(key=sort_key)

def render_pub(r):
    year = r[COL["출판연도"]]
    month = r[COL["월"]]
    journal = r[COL["저널명"]]
    vol = r[COL["권"]]
    issue = r[COL["호"]]
    pages = r[COL["쪽수"]]
    title = r[COL["논문명"]]
    citation = r[COL["서지정보"]]
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

    links = []
    if doi:
        links.append(f'<a href="https://doi.org/{esc(doi)}" target="_blank" rel="noopener">DOI</a>')
    if pmid:
        links.append(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{esc(pmid)}/" target="_blank" rel="noopener">PMID {esc(pmid)}</a>')
    links_html = ' · '.join(links)

    return f'''<article class="pub-card">
  <p class="pub-year-line">{esc(year)} {esc(month)}</p>
  <h3 class="pub-title">{esc(title)}</h3>
  <p class="pub-authors">{authors_html}</p>
  <p class="pub-journal">{journal_line}</p>
  <p class="pub-links">{links_html}</p>
</article>'''

def render_group(title, items):
    if not items: return ""
    cards = "\n".join(render_pub(r) for r in items)
    return f'''<section class="pub-group">
<h2 class="group-title">{esc(title)}</h2>
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
.pub-group{margin:36px 0}
.group-title{font-family:'Times New Roman',Georgia,serif;font-size:20px;letter-spacing:-0.01em;font-weight:600;margin:0 0 16px;border-bottom:1px solid var(--line);padding-bottom:8px;color:var(--fg)}
.pub-grid{display:flex;flex-direction:column;gap:14px}
.pub-card{padding:14px 0;border-bottom:1px dotted #ece9e0}
.pub-card:last-child{border-bottom:0}
.pub-year-line{font-size:12px;color:var(--muted);letter-spacing:0.04em;margin:0 0 4px;font-family:'Times New Roman',Georgia,serif}
.pub-title{margin:2px 0 6px;font-size:15.5px;line-height:1.45;font-weight:600;letter-spacing:-0.005em;color:var(--fg)}
.pub-authors{margin:0 0 4px;font-size:13px;color:var(--muted);line-height:1.55}
.pub-authors strong{color:var(--fg);font-weight:600}
.pub-journal{margin:0 0 6px;font-size:13px;color:#2a2a2a;line-height:1.55}
.pub-journal em{font-style:italic;font-weight:600}
.pub-links{margin:0;font-size:12.5px;display:flex;gap:12px}
.pub-links a{color:var(--accent);text-decoration:none}
.pub-links a:hover{text-decoration:underline}
</style>'''

body_groups = (
    render_group("주저자", groups["주저자"]) +
    "\n\n" +
    render_group("공저자", groups["공저자"]) +
    "\n\n" +
    render_group("기타", groups["기타"])
)

html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>연구 — Hepatology Note</title>
<meta name="description" content="신현재 — peer-reviewed publications.">
<link rel="canonical" href="https://drshin.kr/연구/">
<meta name="author" content="신현재">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="연구 — Hepatology Note">
<meta property="og:description" content="신현재 — peer-reviewed publications.">
<meta property="og:url" content="https://drshin.kr/연구/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"CollectionPage","@id":"https://drshin.kr/연구/#webpage","url":"https://drshin.kr/연구/","name":"연구","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}},"isPartOf":{{"@id":"https://drshin.kr/#website"}}}},
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

<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:32px;letter-spacing:-0.02em;font-weight:600;margin:8px 0 24px">연구</h1>

{body_groups}

<p class="disclaimer" style="margin-top:48px">인용은 원 출처(저널·DOI)를 따라주시기 바랍니다.</p>
</main>

{FOOTER}
</body>
</html>
'''

out = ROOT / "연구" / "index.html"
out.write_text(html, encoding="utf-8")
print(f"Wrote {out} ({len(html)} bytes)")
