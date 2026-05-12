"""Article builder. Reads ARTICLES dict and emits full HTML pages.
Each entry: slug, h1, description, series_slug, series_display, last_crumb,
tldr, sections [(h2, body_html)], faq [(q, a)], refs [(text, doi, pmid)],
svgs [svg_html], related [(url, title)], topic_short.
"""
import html as htmllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV = '''<header class="site-header">
  <div class="inner">
    <a href="/" class="brand-mark">Hepatology Note</a>
    <nav class="site-nav">
      <a href="/소개/">소개</a>
      <a href="/연구/">연구</a>
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

AUTHOR_BOX = '''<aside class="author-box">
<img class="author-photo" src="/assets/img/author/drshin.jpg" alt="" loading="lazy">
<div class="author-info">
<p><strong>서울대학교병원 소화기내과 · 간암센터</strong></p>
<p class="muted">간암·간경변·만성 간질환 진료. 대한간학회 정회원.</p>
<p><a href="/소개/" class="more">소개 보기 →</a></p>
</div>
</aside>'''

def esc(s): return htmllib.escape(s or "")

def render_refs(refs):
    out = ['<section class="references-block">', '<h2>References</h2>', '<ol class="references">']
    for r in refs:
        text = r[0]
        doi = r[1] if len(r) > 1 else None
        pmid = r[2] if len(r) > 2 else None
        line = f'<li>{text}'
        links = []
        if doi: links.append(f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener">DOI</a>')
        if pmid: links.append(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" rel="noopener">PMID {pmid}</a>')
        if links: line += ' ' + ' · '.join(links)
        line += '</li>'
        out.append(line)
    out.append('</ol></section>')
    return "\n".join(out)

def render_faq(faq):
    out = ['<section class="faq" id="faq">', '<h2>자주 묻는 질문</h2>']
    for q, a in faq:
        out.append(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>')
    out.append('</section>')
    return "\n".join(out)

def render_faq_jsonld(faq):
    items = []
    for q, a in faq:
        # JSON-escape: replace " with \"
        q_esc = q.replace('"', '\\"')
        # Strip HTML tags from answer for JSON
        import re as _re
        a_plain = _re.sub(r'<[^>]+>', '', a).replace('"', '\\"').strip()
        items.append(f'{{"@type":"Question","name":"{q_esc}","acceptedAnswer":{{"@type":"Answer","text":"{a_plain}"}}}}')
    return '{"@type":"FAQPage","mainEntity":[' + ','.join(items) + ']}'

def render_related(related):
    items = '\n'.join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for u, t in related)
    return f'<aside class="related"><h2>같이 읽으면 좋은 글</h2><ul>{items}</ul></aside>'

def render_article(spec):
    slug = spec["slug"]
    h1 = spec["h1"]
    description = spec["description"]
    series_slug = spec["series_slug"]
    series_display = spec["series_display"]
    last_crumb = spec["last_crumb"]
    tldr = spec["tldr"]
    sections = spec["sections"]
    faq = spec.get("faq", [])
    refs = spec.get("refs", [])
    svgs = spec.get("svgs", [])
    related = spec.get("related", [])
    published = spec.get("published", "2026-05-09")
    section_label = spec.get("section_label", series_display)
    medical_about = spec.get("about", series_display)

    canonical = f"https://drshin.kr/{slug}/"
    series_url = f"https://drshin.kr/{series_slug}/"

    # Build sections HTML, interleaving SVGs after first 2 sections if available
    body_parts = [f'<div class="tldr"><strong>핵심 요약</strong>{tldr}</div>']
    for i, (h2, body) in enumerate(sections):
        body_parts.append(f'<h2>{esc(h2)}</h2>\n{body}')
        # Insert SVGs at meaningful spots: after section 1 (svg[0]) and after section 3 (svg[1])
        if i == 0 and len(svgs) >= 1:
            body_parts.append(svgs[0])
        elif i == 2 and len(svgs) >= 2:
            body_parts.append(svgs[1])
    body_html = '\n\n'.join(body_parts)

    faq_html = render_faq(faq) if faq else ''
    faq_jsonld = render_faq_jsonld(faq) if faq else ''
    refs_html = render_refs(refs) if refs else ''
    related_html = render_related(related) if related else ''

    jsonld_graph = [
        f'{{"@type":"MedicalWebPage","@id":"{canonical}#webpage","url":"{canonical}","name":"{esc(h1)}","description":"{esc(description)}","inLanguage":"ko","datePublished":"{published}","dateModified":"{published}","lastReviewed":"{published}","audience":{{"@type":"MedicalAudience","audienceType":"Patient"}},"about":{{"@type":"MedicalCondition","name":"{esc(medical_about)}"}},"specialty":"Hepatology","author":{{"@id":"https://drshin.kr/#author"}},"reviewedBy":{{"@id":"https://drshin.kr/#author"}},"isPartOf":{{"@id":"https://drshin.kr/#website"}}}}',
        '{"@type":"Person","@id":"https://drshin.kr/#author","name":"신현재","jobTitle":"서울대학교병원 소화기내과 · 간암센터","worksFor":{"@type":"Hospital","name":"서울대학교병원","url":"https://www.snuh.org/"},"image":"https://drshin.kr/assets/img/author/drshin.jpg","url":"https://drshin.kr/소개/"}',
    ]
    if faq_jsonld:
        jsonld_graph.append(faq_jsonld)
    jsonld_graph.append(f'{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},{{"@type":"ListItem","position":2,"name":"{esc(series_display)}","item":"{series_url}"}},{{"@type":"ListItem","position":3,"name":"{esc(last_crumb)}","item":"{canonical}"}}]}}')

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(h1)} — Hepatology Note</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="신현재">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(h1)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta property="article:author" content="신현재">
<meta property="article:published_time" content="{published}">
<meta property="article:modified_time" content="{published}">
<meta property="article:section" content="{esc(section_label)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{','.join(jsonld_graph)}
]}}
</script>
<style>
svg.fig{{display:block;width:100%;height:auto;max-width:720px;margin:20px auto;background:#fff;border:1px solid var(--line);border-radius:8px}}
svg.fig text{{font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR",sans-serif}}
.fig-caption{{font-size:12.5px;color:var(--muted);text-align:center;margin:-12px 0 24px;letter-spacing:0.01em}}
</style>
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="/{series_slug}/">{esc(series_display)}</a> › <span>{esc(last_crumb)}</span></nav>
<article>
<h1>{esc(h1)}</h1>
{body_html}

{faq_html}

{refs_html}

{AUTHOR_BOX}

{related_html}

<p class="disclaimer">본 콘텐츠는 일반적 의료 정보 제공을 목적으로 하며, 개별 진료를 대체하지 않습니다. 증상이나 검사 결과 해석, 치료 결정은 반드시 진료를 통해 의료진과 상의하시기 바랍니다.</p>
</article>
</main>

{FOOTER}
</body>
</html>
'''
    out = ROOT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: {slug} ({len(html)} bytes)")

# === Reusable SVG helpers ===
def svg_stage_progression(stages, caption=""):
    """Horizontal stages with arrows. stages = [(label, sublabel, emphasized)]."""
    n = len(stages)
    box_w = 120
    gap = 20
    total = n * box_w + (n - 1) * gap
    start_x = (720 - total) // 2
    boxes = []
    arrows = []
    for i, (lbl, sub, em) in enumerate(stages):
        x = start_x + i * (box_w + gap)
        cls = "box-em" if em else "box"
        boxes.append(f'<rect x="{x}" y="40" width="{box_w}" height="100" rx="8" class="{cls}"/>')
        boxes.append(f'<text x="{x+box_w//2}" y="80" text-anchor="middle" class="label-em" font-size="15">{esc(lbl)}</text>')
        if sub:
            boxes.append(f'<text x="{x+box_w//2}" y="105" text-anchor="middle" class="label-sm" font-size="11">{esc(sub)}</text>')
        if i < n - 1:
            ax = x + box_w
            arrows.append(f'<path d="M{ax} 90 L{ax+gap} 90" stroke="#5a5a5a" stroke-width="1.5" marker-end="url(#arr)"/>')
    cap = f'<p class="fig-caption">{esc(caption)}</p>' if caption else ''
    return f'''<svg class="fig" viewBox="0 0 720 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(caption or "diagram")}">
<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#5a5a5a"/></marker></defs>
<style>.box{{fill:#fff;stroke:#e5e3dc;stroke-width:1.5}}.box-em{{fill:#e8f3ef;stroke:#1f6f5c;stroke-width:1.5}}.label-em{{fill:#1f6f5c;font-weight:600}}.label-sm{{fill:#5a5a5a}}</style>
{chr(10).join(boxes + arrows)}
</svg>{cap}'''

def svg_table(title, headers, rows, caption=""):
    """SVG table. Used for grading systems etc."""
    col_w = 720 // len(headers)
    row_h = 32
    n_rows = len(rows)
    h = 60 + (n_rows + 1) * row_h
    parts = [f'<text x="20" y="28" class="title" font-size="15" font-weight="600" fill="#1f6f5c">{esc(title)}</text>']
    # Header row
    y = 50
    for i, hd in enumerate(headers):
        x = i * col_w
        parts.append(f'<rect x="{x}" y="{y}" width="{col_w}" height="{row_h}" fill="#f3f1ec" stroke="#e5e3dc"/>')
        parts.append(f'<text x="{x+col_w//2}" y="{y+row_h//2+5}" text-anchor="middle" font-size="13" font-weight="600" fill="#1a1a1a">{esc(hd)}</text>')
    # Data rows
    for ri, row in enumerate(rows):
        y_row = 50 + (ri + 1) * row_h
        for i, cell in enumerate(row):
            x = i * col_w
            parts.append(f'<rect x="{x}" y="{y_row}" width="{col_w}" height="{row_h}" fill="#fff" stroke="#e5e3dc"/>')
            parts.append(f'<text x="{x+col_w//2}" y="{y_row+row_h//2+5}" text-anchor="middle" font-size="12.5" fill="#2a2a2a">{esc(cell)}</text>')
    cap = f'<p class="fig-caption">{esc(caption)}</p>' if caption else ''
    return f'''<svg class="fig" viewBox="0 0 720 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(caption or title)}">
{chr(10).join(parts)}
</svg>{cap}'''

def svg_checklist(title, items, caption=""):
    """Vertical checklist with checkmarks/dots."""
    h = 50 + len(items) * 30
    parts = [f'<text x="20" y="28" font-size="15" font-weight="600" fill="#1f6f5c">{esc(title)}</text>']
    for i, item in enumerate(items):
        y = 60 + i * 30
        parts.append(f'<circle cx="32" cy="{y-4}" r="4" fill="#1f6f5c"/>')
        parts.append(f'<text x="48" y="{y}" font-size="13.5" fill="#2a2a2a">{esc(item)}</text>')
    cap = f'<p class="fig-caption">{esc(caption)}</p>' if caption else ''
    return f'''<svg class="fig" viewBox="0 0 720 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(caption or title)}">
{chr(10).join(parts)}
</svg>{cap}'''

def svg_flow_arrows(steps, caption="", title=""):
    """Process flow with prominent colored arrows. steps=[(label,sublabel,color)]."""
    n = len(steps)
    box_w = min(130, (700 - (n-1)*40) // n)
    arrow_w = 40
    total_w = n * box_w + (n - 1) * arrow_w
    start_x = (720 - total_w) // 2
    title_h = 35 if title else 0
    h = 180 + title_h
    colors = {
        'normal': ('#fff', '#bcbcb0', '#1a1a1a'),
        'accent': ('#e8f3ef', '#1f6f5c', '#1f6f5c'),
        'warn':   ('#fef3e0', '#b8650a', '#b8650a'),
        'danger': ('#fce7e0', '#c9542b', '#c9542b'),
    }
    parts = []
    if title:
        parts.append(f'<text x="20" y="26" font-size="15" font-weight="700" fill="#1f6f5c">{esc(title)}</text>')
    box_y = 50 + title_h
    for i, step in enumerate(steps):
        label = step[0]
        sublabel = step[1] if len(step) > 1 else ''
        color_key = step[2] if len(step) > 2 else 'normal'
        x = start_x + i * (box_w + arrow_w)
        bg, border, txt = colors.get(color_key, colors['normal'])
        parts.append(f'<rect x="{x}" y="{box_y}" width="{box_w}" height="100" rx="10" fill="{bg}" stroke="{border}" stroke-width="2.5"/>')
        parts.append(f'<text x="{x+box_w//2}" y="{box_y+45}" text-anchor="middle" font-size="14" font-weight="700" fill="{txt}">{esc(label)}</text>')
        if sublabel:
            parts.append(f'<text x="{x+box_w//2}" y="{box_y+70}" text-anchor="middle" font-size="11" fill="#5a5a5a">{esc(sublabel)}</text>')
        if i < n - 1:
            ax = x + box_w + 6
            ay = box_y + 50
            parts.append(f'<path d="M{ax} {ay} L{ax+arrow_w-12} {ay}" stroke="#5a5a5a" stroke-width="3" marker-end="url(#bigarr)" fill="none"/>')
    cap = f'<p class="fig-caption">{esc(caption)}</p>' if caption else ''
    return f'''<svg class="fig" viewBox="0 0 720 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(caption or title or "flow")}">
<defs><marker id="bigarr" markerWidth="12" markerHeight="12" refX="10" refY="3" orient="auto"><path d="M0,0 L0,6 L10,3 z" fill="#5a5a5a"/></marker></defs>
{chr(10).join(parts)}
</svg>{cap}'''


def svg_progression_bar(stages, caption="", title=""):
    """Horizontal progression bar with colored segments."""
    title_h = 35 if title else 0
    h = 130 + title_h
    bar_y = 40 + title_h
    bar_h = 56
    total_w = 660
    start_x = 30
    seg_w = total_w // len(stages)
    colors = ['#e8f3ef', '#fff8e0', '#fef3e0', '#fce7e0', '#f3d4c0']
    border_colors = ['#1f6f5c', '#a88a3a', '#b8650a', '#c9542b', '#8b3d1c']
    parts = []
    if title:
        parts.append(f'<text x="20" y="26" font-size="15" font-weight="700" fill="#1f6f5c">{esc(title)}</text>')
    for i, stage in enumerate(stages):
        label = stage[0]
        sublabel = stage[1] if len(stage) > 1 else ''
        x = start_x + i * seg_w
        ci = min(i, len(colors) - 1)
        parts.append(f'<rect x="{x}" y="{bar_y}" width="{seg_w}" height="{bar_h}" fill="{colors[ci]}" stroke="{border_colors[ci]}" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+seg_w//2}" y="{bar_y+bar_h//2-2}" text-anchor="middle" font-size="14" font-weight="700" fill="{border_colors[ci]}">{esc(label)}</text>')
        if sublabel:
            parts.append(f'<text x="{x+seg_w//2}" y="{bar_y+bar_h//2+18}" text-anchor="middle" font-size="11" fill="#5a5a5a">{esc(sublabel)}</text>')
    arrow_y = bar_y + bar_h + 22
    parts.append(f'<line x1="30" y1="{arrow_y}" x2="685" y2="{arrow_y}" stroke="#5a5a5a" stroke-width="1.5" marker-end="url(#progarr)"/>')
    parts.append(f'<text x="690" y="{arrow_y+5}" text-anchor="end" font-size="11" fill="#5a5a5a">→ 진행</text>')
    cap = f'<p class="fig-caption">{esc(caption)}</p>' if caption else ''
    return f'''<svg class="fig" viewBox="0 0 720 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(caption or title or "progression")}">
<defs><marker id="progarr" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#5a5a5a"/></marker></defs>
{chr(10).join(parts)}
</svg>{cap}'''


def svg_compare_two(title_a, items_a, title_b, items_b, caption=""):
    """Two-column comparison cards."""
    h = 60 + max(len(items_a), len(items_b)) * 26 + 40
    parts = [f'<text x="180" y="32" text-anchor="middle" font-size="15" font-weight="600" fill="#1f6f5c">{esc(title_a)}</text>',
             f'<text x="540" y="32" text-anchor="middle" font-size="15" font-weight="600" fill="#1f6f5c">{esc(title_b)}</text>',
             f'<rect x="20" y="48" width="320" height="{h-60}" rx="8" fill="#e8f3ef" stroke="#1f6f5c" stroke-width="1.5"/>',
             f'<rect x="380" y="48" width="320" height="{h-60}" rx="8" fill="#fff" stroke="#e5e3dc" stroke-width="1.5"/>']
    for i, item in enumerate(items_a):
        y = 78 + i * 26
        parts.append(f'<text x="40" y="{y}" font-size="13" fill="#1a1a1a">• {esc(item)}</text>')
    for i, item in enumerate(items_b):
        y = 78 + i * 26
        parts.append(f'<text x="400" y="{y}" font-size="13" fill="#1a1a1a">• {esc(item)}</text>')
    cap = f'<p class="fig-caption">{esc(caption)}</p>' if caption else ''
    return f'''<svg class="fig" viewBox="0 0 720 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(caption or title_a + ' vs ' + title_b)}">
{chr(10).join(parts)}
</svg>{cap}'''

# === Articles ===
ARTICLES = []

# 02 — 간경화 series — 9 remaining drafts to publish

# 02-2: Child-Pugh와 MELD
ARTICLES.append({
    "slug": "간경변-Child-Pugh-MELD",
    "h1": "Child-Pugh와 MELD — 두 점수가 의미하는 것",
    "description": "간경변 환자에서 사용하는 두 가지 주요 점수 — Child-Pugh와 MELD의 구성·용도·한계를 정리합니다. 어떤 상황에서 어느 점수가 쓰이는지.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "Child-Pugh와 MELD",
    "section_label": "간경화", "about": "간경변",
    "tldr": "Child-Pugh는 간경변의 <em>중증도와 합병증</em>을 보고, MELD는 <em>3개월 사망 위험과 간이식 우선순위</em>를 봅니다. 둘은 보완 관계로 함께 사용합니다. Child-Pugh A·B·C는 5년 생존율 약 90%·70%·30%, MELD 15 이상이면 간이식 평가가 본격화됩니다.",
    "sections": [
        ("Child-Pugh — 가장 오래 쓰인 점수",
         "<p>1964년 Child-Turcotte가, 1972년 Pugh가 정맥류 출혈 수술 위험을 예측하기 위해 만든 점수입니다. 5가지 항목을 1·2·3점으로 채점합니다.</p><ul><li><strong>빌리루빈</strong>: &lt;2 / 2–3 / &gt;3 mg/dL</li><li><strong>알부민</strong>: &gt;3.5 / 2.8–3.5 / &lt;2.8 g/dL</li><li><strong>PT(INR)</strong>: &lt;1.7 / 1.7–2.3 / &gt;2.3</li><li><strong>복수</strong>: 없음 / 약함 / 중등도-중증</li><li><strong>간성혼수</strong>: 없음 / Grade 1–2 / Grade 3–4</li></ul><p>합산하여 5–6점은 <strong>Class A</strong>, 7–9점은 <strong>Class B</strong>, 10–15점은 <strong>Class C</strong>입니다.</p>"),
        ("MELD — 사망 위험을 수치로 보는 점수",
         "<p>2002년 미국에서 간이식 우선순위를 객관화하기 위해 도입되었습니다. 빌리루빈·INR·크레아티닌 세 가지 검사 수치를 로그 변환한 공식으로 6–40점을 산출합니다. 2016년부터는 나트륨을 추가한 <strong>MELD-Na</strong>가 표준이며, 2023년부터 미국은 성별 보정한 <strong>MELD 3.0</strong>을 사용합니다.</p><p>MELD는 3개월 사망 위험과 거의 직결됩니다. MELD 15 미만이면 3개월 사망률 5% 미만, MELD 25 이상이면 25% 이상으로 가파르게 올라갑니다.</p>"),
        ("두 점수의 사용 맥락이 다릅니다",
         "<p>임상에서는 둘을 다른 목적으로 씁니다.</p><ul><li><strong>Child-Pugh</strong> — 외래에서 간경변 환자의 전체적인 중증도를 빠르게 가늠. 정맥류 예방·항암치료 적응 여부·약물 용량 조절 결정 시.</li><li><strong>MELD</strong> — 간이식 대기명단 우선순위. 한국 KONOS도 MELD 기준. 응급도 평가.</li></ul><p>한 환자에게 두 점수가 동시에 매겨집니다. Child-Pugh A에 MELD 12면 비교적 안정적, Child-Pugh C에 MELD 30이면 중환자.</p>"),
        ("점수가 가지는 한계",
         "<p>두 점수 모두 한계가 있습니다.</p><ul><li><strong>Child-Pugh</strong>: 복수·간성혼수의 채점이 의료진 판단에 따라 다르고, 빌리루빈·알부민이 영양 상태 등 다른 요인에 영향을 받습니다.</li><li><strong>MELD</strong>: 신기능·간 합성능에 의존해 복수·간성혼수·정맥류 출혈은 직접 반영하지 않습니다. MELD가 낮은데도 사망 위험이 큰 환자(낮은 알부민, 반복 SBP, 난치성 복수)가 있어 'MELD-purgatory'라고도 불립니다.</li></ul><p>최근에는 ALBI score, MELD 3.0, sarcopenia 보정 등이 보완 도구로 추가됩니다.</p>"),
        ("환자에게 의미하는 것",
         "<p>외래에서 \"Child-Pugh A예요\" 또는 \"MELD 18입니다\"라는 말을 들으면, 단순한 등급 자체보다 <strong>그 점수에서 어떤 결정이 따르는가</strong>를 보세요.</p><ul><li>Child-Pugh A → 대상성, 절제·간암 치료 가능</li><li>Child-Pugh B → 합병증 관리 강화, 간이식 평가 시작</li><li>Child-Pugh C, MELD 15 이상 → 간이식 등록 본격 검토</li></ul><p>점수는 라벨이 아니라 <em>다음 단계의 결정을 위한 정보</em>입니다. 또 시간에 따라 변합니다 — 원인 치료(B형간염 항바이러스제, 금주 등)로 점수가 호전되어 등급이 내려가는 환자가 외래에서 적지 않습니다.</p>"),
    ],
    "faq": [
        ("MELD 점수가 14인데 간이식 후보가 되나요?",
         "<p>MELD 15가 이식 이득(survival benefit)이 약물·관찰을 넘어서는 통상 임계값입니다. MELD 14 이하라면 합병증 관리·원인 치료·정기 추적에 우선순위를 두고, 이식 평가 자체는 시작할 수 있어도 등록 가산 시점은 미루는 경우가 많습니다. 다만 점수에 잘 반영되지 않는 합병증 — 난치성 복수, 반복 정맥류 출혈, 반복 SBP, 간폐증후군 등 — 이 있으면 MELD가 낮아도 별도로 등록 우선순위 가산을 받기도 합니다. 한국 KONOS는 이런 예외 상황에 대한 별도 가산 점수 제도를 운영합니다.</p>"),
        ("Child-Pugh와 MELD가 일치하지 않을 때는?",
         "<p>임상에서 자주 마주칩니다. 두 점수가 보는 축이 다르기 때문입니다. Child-Pugh B인데 MELD 8인 환자는 신기능과 INR은 잘 보존됐지만 복수·간성혼수 같은 합병증이 점수를 끌어올린 경우입니다. 반대로 Child-Pugh A인데 MELD 18로 높은 환자는 복수·정맥류 출혈은 없지만 빌리루빈·신기능이 급격히 나빠지는 환자입니다. 외래에서는 두 점수 중 더 나쁜 신호를 우선해 평가하고, 합병증 종류와 빈도, 영양 상태, 근감소증 여부, 원인 질환의 활성도까지 함께 봐서 다음 단계(추적 강도 강화, 이식 평가 시작, 약물 조정)를 결정합니다.</p>"),
        ("MELD가 좋아지면 이식 대기에서 빠지나요?",
         "<p>점수 호전으로 우선순위가 낮아질 수는 있지만 곧바로 대기명단에서 빠지지는 않습니다. 한국 KONOS는 정기적인 MELD 재측정과 함께 임상 경과(합병증 빈도·영양 상태·전체 생존 예측)를 종합 평가합니다. 원인 치료가 잘 되어 점수가 일시적으로 좋아져도, 간경변 자체가 사라진 것은 아니므로 등록 유지하면서 추적하는 경우가 많습니다. 점수가 지속적으로 개선되고 합병증이 1년 이상 재발하지 않으면 임상적 재대상화 평가에 따라 등록 보류를 검토할 수 있습니다.</p>"),
        ("Child-Pugh는 한 번 매기면 끝인가요?",
         "<p>아닙니다. 외래마다 다시 채점하는 동적 지표입니다. B형간염에서 항바이러스제로 바이러스가 억제되거나, 알코올성에서 금주에 성공하거나, MASH에서 체중 감량으로 ALT·알부민·간섬유화가 호전되면 Class B에서 A로 내려가는 환자가 외래에서 흔합니다. 반대로 합병증이 새로 등장하거나 음주 재개·약물 부작용 등으로 단계가 올라가기도 합니다. 5개 항목 중 복수와 간성혼수의 채점이 의료진 판단에 따라 다소 다를 수 있어, 진료의가 일관되게 평가하는 것이 중요합니다.</p>"),
        ("MELD-Na와 MELD 3.0의 차이는?",
         "<p>MELD-Na는 기존 MELD에 혈청 나트륨(Na)을 추가해 정확도를 높인 버전(2016년 도입)입니다. 저나트륨혈증이 간경변에서 흔하고 사망 위험과 연관되기 때문입니다. MELD 3.0(2023년 미국 도입)은 MELD-Na에 알부민과 성별 보정을 추가한 가장 최신 버전으로, 이전 버전들이 여성 환자의 사망 위험을 과소평가했던 점을 보완했습니다. 한국 KONOS는 2026년 현재 MELD-Na를 표준으로 사용하며, MELD 3.0 도입은 검토 중입니다. 환자 입장에서는 어느 버전이든 점수 자체보다 \"이식 우선순위에 어떻게 반영되는지\"를 진료의에게 확인하는 것이 중요합니다.</p>"),
    ],
    "refs": [
        ("Pugh RN, Murray-Lyon IM, Dawson JL, et al. Transection of the oesophagus for bleeding oesophageal varices. <em>Br J Surg</em>. 1973;60(8):646–649.", "10.1002/bjs.1800600817", "4541913"),
        ("Wiesner R, Edwards E, Freeman R, et al. Model for end-stage liver disease (MELD) and allocation of donor livers. <em>Gastroenterology</em>. 2003;124(1):91–96.", "10.1053/gast.2003.50016", "12512033"),
        ("Kim WR, Mannalithara A, Heimbach JK, et al. MELD 3.0: The Model for End-Stage Liver Disease Updated for the Modern Era. <em>Gastroenterology</em>. 2021;161(6):1887–1895.", "10.1053/j.gastro.2021.08.050", "34481845"),
        ("D'Amico G, Garcia-Tsao G, Pagliaro L. Natural history and prognostic indicators of survival in cirrhosis: a systematic review of 118 studies. <em>J Hepatol</em>. 2006;44(1):217–231.", "10.1016/j.jhep.2005.10.013", "16298014"),
        ("European Association for the Study of the Liver. EASL Clinical Practice Guidelines on the management of decompensated cirrhosis. <em>J Hepatol</em>. 2018;69(2):406–460.", "10.1016/j.jhep.2018.03.024", None),
    ],
    "svgs": [
        svg_table("Child-Pugh 점수표 (5–6 = A · 7–9 = B · 10–15 = C)",
                  ["항목", "1점", "2점", "3점"],
                  [["빌리루빈 (mg/dL)", "<2", "2–3", ">3"],
                   ["알부민 (g/dL)", ">3.5", "2.8–3.5", "<2.8"],
                   ["PT (INR)", "<1.7", "1.7–2.3", ">2.3"],
                   ["복수", "없음", "약함", "중등도–중증"],
                   ["간성혼수", "없음", "Grade 1–2", "Grade 3–4"]],
                  caption="Child-Pugh 5개 항목 — 채점 합계로 A/B/C 분류"),
        svg_table("MELD 점수와 임상 의미",
                  ["MELD 점수", "3개월 사망률(추정)", "임상 단계"],
                  [["6–9", "1–2%", "대상성, 외래 추적"],
                   ["10–14", "5–10%", "이식 평가 시작 검토"],
                   ["15–19", "10–20%", "이식 등록 본격화"],
                   ["20–29", "20–50%", "고위험, 우선 배정"],
                   ["≥30", ">50%", "응급 / 중환자실"]],
                  caption="MELD 점수와 3개월 사망 위험 — 한국 KONOS도 MELD 기준 우선순위"),
    ],
    "related": [
        ("/간경변-대상성-비대상성/", "대상성 vs 비대상성 간경변 — 어디서 갈라지나"),
        ("/간경변-복수/", "복수 — 단계별 관리"),
        ("/간경변-간이식-평가/", "간이식 평가 — 누가, 언제 시작하나"),
    ],
})

# 02-3: 식도정맥류
ARTICLES.append({
    "slug": "간경변-식도정맥류",
    "h1": "식도정맥류 — 첫 신호와 예방적 결찰",
    "description": "간경변 환자에서 식도정맥류는 어떻게 형성되고 어떤 신호를 보내는가. 검진 주기, 베타차단제와 내시경 결찰의 1차·2차 예방을 정리합니다.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "식도정맥류",
    "section_label": "간경화", "about": "식도정맥류",
    "tldr": "식도정맥류는 간경변에서 문맥압이 올라가 식도 점막 아래 정맥이 부풀어 오른 상태입니다. 한 번 출혈하면 6주 사망률 15–20%로 가장 위험한 합병증 중 하나입니다. <em>중·대형 정맥류는 출혈 전에 비선택적 베타차단제 또는 내시경 결찰로 1차 예방</em>합니다. 출혈 후에는 두 가지를 병행하는 2차 예방이 필수입니다.",
    "sections": [
        ("왜 식도에 정맥류가 생기는가",
         "<p>간경변에서 간 안의 혈류 저항이 올라가면 문맥압(portal pressure)이 상승합니다. 우회로(collateral)로 혈액이 빠지는데, 그중 가장 임상적으로 중요한 곳이 <strong>식도와 위의 점막 아래 정맥</strong>입니다. 압력을 받아 정맥이 부풀고 얇아지면 사소한 자극에도 터질 수 있습니다.</p><p>HVPG(간정맥압 차)가 10 mmHg 이상이면 임상적 의미 있는 문맥압항진(CSPH), 12 mmHg 이상에서 정맥류 출혈 위험이 본격화됩니다.</p>"),
        ("정맥류 등급과 출혈 위험",
         "<p>내시경 소견에 따라 분류합니다.</p><ul><li><strong>F1 (소형)</strong> — 직선형, 누른 자국 사라짐</li><li><strong>F2 (중형)</strong> — 부분 굴곡, 누른 자국 남음</li><li><strong>F3 (대형)</strong> — 굵은 굴곡, 식도 내강의 1/3 이상 차지</li></ul><p>여기에 적색징후(red color sign)가 있으면 출혈 임박. 1년 출혈 위험은 소형 5%, 중형 10–15%, 대형(특히 적색징후 동반) 30% 이상입니다.</p>"),
        ("검진 주기 — 누가 언제 받아야 하나",
         "<p>간경변 진단 시 모든 환자에게 한 번 내시경 검진이 권장됩니다. 이후 추적은 다음에 따릅니다.</p><ul><li>대상성 간경변, 정맥류 없음 → 2–3년 후 재검 (Baveno VII)</li><li>대상성, 소형 정맥류 → 1–2년 후 재검</li><li>비대상성 진입 또는 정맥류 진행 가능 인자 (지속 음주 등) → 매년</li><li>중·대형 정맥류 → 검진보다 1차 예방 시작</li></ul><p>최근에는 일부 대상성 환자에서 Baveno 기준(혈소판 ≥ 150,000 + LSM ≤ 20 kPa)에 해당하면 내시경을 생략할 수 있다는 권고가 추가되었습니다.</p>"),
        ("1차 예방 — 출혈 전 무엇을 하나",
         "<p>중·대형 정맥류 또는 적색징후가 있는 소형 정맥류 환자는 둘 중 하나를 선택합니다.</p><ul><li><strong>비선택적 베타차단제(NSBB)</strong> — 카베디롤(권장, 6.25–12.5 mg) 또는 프로프라놀롤(20–80 mg×2). 심박수가 안정 시 55–60bpm이 되도록 적정. 문맥압 자체를 낮춤.</li><li><strong>내시경 정맥류 결찰술(EVL)</strong> — 2–4주 간격으로 정맥류가 사라질 때까지 반복. 이후 6–12개월마다 추적.</li></ul><p>두 방법의 출혈 예방 효과는 비슷합니다. NSBB는 심혈관 보호 효과 부수적, EVL은 결찰 부위 궤양·통증 등 부작용. 환자 선호와 동반 질환에 따라 결정합니다.</p>"),
        ("출혈했을 때와 2차 예방",
         "<p>토혈·흑변이 보이면 즉시 응급실로. 응급 대응:</p><ul><li>혈역학적 안정화, 좁은 범위 수혈 (Hb 7 g/dL 목표)</li><li>출혈 의심 시 즉시 vasoactive (테르리프레신 또는 옥트레오타이드) 투여</li><li>예방적 항생제 (세프트리악손) — 출혈성 간경변에서 SBP·재출혈 감소</li><li>12시간 내 응급 내시경 → 정맥류 결찰</li></ul><p>출혈에서 회복되면 <strong>2차 예방</strong>으로 NSBB + EVL을 <em>둘 다</em> 시행합니다. 한 가지만으로는 1년 재출혈률 60%를 충분히 못 막습니다. 또한 TIPS(경경정맥 간내 문맥전신 단락술)가 고위험 환자에서 조기에 고려됩니다.</p>"),
    ],
    "faq": [
        ("위정맥류는 식도정맥류와 다른가요?",
         "<p>네, 임상적으로 별개로 다룹니다. 위에 발생하는 정맥류(GOV1·GOV2·IGV)는 위치와 분포에 따라 분류되며 일반적으로 식도정맥류용 결찰술(EVL)이 잘 듣지 않습니다. 1차 시도는 시아노아크릴레이트(글루) 주입이며, 효과가 부족하거나 재출혈 위험이 높으면 BRTO(역행성 정맥류 폐쇄술)나 TIPS를 고려합니다. 위정맥류는 식도정맥류보다 출혈 빈도는 낮지만 한 번 출혈하면 양이 많고 사망률이 더 높아 다학제 진료가 권장됩니다.</p>"),
        ("베타차단제를 먹으면 평생 먹어야 하나요?",
         "<p>비대상성 간경변에서는 일반적으로 평생 유지합니다. 비선택적 베타차단제(NSBB)는 정맥류 출혈 예방뿐 아니라 문맥압 자체를 낮춰 비대상성 진입을 늦춘다는 데이터가 PREDESCI 연구에서 확인되었기 때문입니다. 다만 혈압이 너무 낮아지거나(수축기 90 미만), 심박수가 55 이하로 떨어지거나, 신기능이 급격히 나빠지면 일시 중단·감량을 검토합니다. 카베디롤이 프로프라놀롤보다 적정·내약성이 좋아 최근 1차로 권장됩니다. 천식·COPD 중증 환자, 진행된 심부전 환자에서는 사용 신중.</p>"),
        ("정맥류가 사라지면 더 이상 추적 안 해도 되나요?",
         "<p>아닙니다. 결찰술로 사라진 정맥류는 시간이 지나면 재발할 수 있어 정기 내시경 추적이 필수입니다. 표준 일정은 결찰 직후 6개월 → 1년 → 이후 1-2년 간격이며, 재발 시 다시 결찰합니다. 또한 결찰 후에도 NSBB는 지속하는 경우가 많습니다 — 두 가지를 함께 하는 것이 단독보다 재출혈 예방에 우월하기 때문입니다. 추적 중 새 정맥류가 발견되거나 적색징후가 나타나면 일정을 앞당깁니다.</p>"),
        ("정맥류가 있는데 무서워서 음식도 못 먹겠어요.",
         "<p>일반적인 식사로 정맥류가 터지는 일은 거의 없습니다. 식도정맥류는 음식의 압력보다 문맥압 항진과 정맥벽의 약함이 출혈의 원인입니다. 다만 매우 단단한 음식(딱딱한 빵 가장자리, 단단한 과자류, 견과류 큰 조각)은 천천히 잘 씹어 드시고, 알코올과 NSAIDs(이부프로펜·디클로페낙)는 반드시 피해야 합니다. 둘 다 점막을 자극하고 출혈 위험을 높입니다. 식이 자체보다 베타차단제 복용·정기 내시경 추적·간 기능 유지가 출혈 예방의 핵심입니다.</p>"),
        ("간경변 진단 받았는데 정맥류 검사를 꼭 받아야 하나요?",
         "<p>대부분의 간경변 환자에서 한 번은 권장됩니다. 다만 2022년 Baveno VII 합의에서 \"검진 생략 가능\" 기준이 제시되었습니다 — 간섬유화 측정값(LSM) 20 kPa 이하 + 혈소판 150,000 이상이면 정맥류가 출혈 위험이 있을 만큼 클 가능성이 매우 낮아 내시경을 생략할 수 있습니다(Anticipate 알고리즘). 이 기준에 해당하지 않거나, 비대상성 단계 진입, 음주 지속, 간 기능 악화 신호가 있으면 표준 일정대로 내시경 검진을 받아야 합니다.</p>"),
    ],
    "refs": [
        ("de Franchis R, Bosch J, Garcia-Tsao G, Reiberger T, Ripoll C; Baveno VII Faculty. Baveno VII — Renewing consensus in portal hypertension. <em>J Hepatol</em>. 2022;76(4):959–974.", "10.1016/j.jhep.2021.12.022", "35120736"),
        ("Garcia-Tsao G, Abraldes JG, Berzigotti A, Bosch J. Portal hypertensive bleeding in cirrhosis: Risk stratification, diagnosis, and management. <em>Hepatology</em>. 2017;65(1):310–335.", "10.1002/hep.28906", "27786365"),
        ("Villanueva C, Albillos A, Genescà J, et al. β blockers to prevent decompensation of cirrhosis in patients with clinically significant portal hypertension (PREDESCI). <em>Lancet</em>. 2019;393(10181):1597–1608.", "10.1016/S0140-6736(18)31875-0", "30910320"),
        ("Korean Association for the Study of the Liver. KASL clinical practice guidelines for liver cirrhosis: Varices, hepatic encephalopathy, and related complications. <em>Clin Mol Hepatol</em>. 2020;26(2):83–127.", "10.3350/cmh.2019.0010n", None),
    ],
    "svgs": [
        svg_table("정맥류 등급과 1년 출혈 위험",
                  ["등급", "내시경 소견", "1년 출혈 위험"],
                  [["F1 소형", "직선, 누른 자국 사라짐", "약 5%"],
                   ["F2 중형", "부분 굴곡, 누른 자국 남음", "10–15%"],
                   ["F3 대형", "굵은 굴곡, 식도 1/3 이상", "20–30%+"],
                   ["+ 적색징후", "어느 등급에서도 위험 가산", "위험 ≥ 2배"]],
                  caption="등급에 적색징후 동반 여부를 함께 봐서 1차 예방 결정"),
        svg_compare_two("비선택적 베타차단제 (NSBB)",
                        ["카베디롤 6.25–12.5 mg 또는 프로프라놀롤 20–80mg×2",
                         "심박수 55–60bpm 목표 적정",
                         "문맥압 자체를 낮춤",
                         "심혈관 보호 부수 효과",
                         "천식·서맥 환자엔 주의"],
                        "내시경 정맥류 결찰 (EVL)",
                        ["2–4주 간격으로 반복 결찰",
                         "정맥류 사라질 때까지 진행",
                         "이후 6–12개월 추적 내시경",
                         "결찰 부위 궤양·통증 가능",
                         "급성 출혈에서도 표준 치료"],
                        caption="중·대형 정맥류의 1차 예방 — 두 옵션의 효과는 비슷, 환자 상황에 따라 선택"),
    ],
    "related": [
        ("/간경변-대상성-비대상성/", "대상성 vs 비대상성 간경변 — 어디서 갈라지나"),
        ("/간경변-복수/", "복수 — 단계별 관리"),
        ("/간경변-Child-Pugh-MELD/", "Child-Pugh와 MELD — 두 점수가 의미하는 것"),
    ],
})

# 02-4: 복수
ARTICLES.append({
    "slug": "간경변-복수",
    "h1": "복수 — 단계별 관리와 흔한 합병증",
    "description": "간경변에서 복수의 단계별 진단·치료(식이 나트륨·이뇨제·천자), SBP 예방, 난치성 복수의 옵션(반복 천자·TIPS·간이식)을 정리합니다.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "복수",
    "section_label": "간경화", "about": "복수",
    "tldr": "복수는 비대상성 간경변의 가장 흔한 첫 신호입니다. Grade 1–3로 분류하고 식이 나트륨 제한 + 이뇨제(스피로놀락톤·푸로세미드)로 시작합니다. 천자(paracentesis)는 진단과 치료에 모두 쓰이며, 난치성 복수는 반복 천자·TIPS·간이식까지 단계적으로 갑니다. SBP(자발성 세균성 복막염)는 한 번이라도 있었다면 평생 항생제 예방이 필요합니다.",
    "sections": [
        ("복수 등급",
         "<p>임상에서 보이는 정도에 따라 분류합니다.</p><ul><li><strong>Grade 1 (경증)</strong> — 초음파에서만 확인. 신체검사로 거의 안 보임.</li><li><strong>Grade 2 (중등도)</strong> — 배가 균등하게 부풀고 체중 증가. 일상에 불편.</li><li><strong>Grade 3 (중증)</strong> — 배가 팽팽하게 늘어나고 호흡 곤란. 즉시 치료 필요.</li></ul><p>복수가 처음 발견되면 항상 <strong>진단적 천자</strong>를 합니다. 단순 간경변성 복수인지, SBP인지, 악성인지를 구별하기 위함입니다.</p>"),
        ("진단적 천자에서 무엇을 보나",
         "<p>복수액에서 다음을 검사합니다.</p><ul><li>다형핵 백혈구 수 (PMN) — 250개/μL 이상이면 SBP 진단</li><li>총 단백·알부민 — SAAG (혈청-복수 알부민 차) 1.1 g/dL 이상이면 문맥압 항진성</li><li>배양 — 균 동정</li><li>세포검사 (악성 의심 시)</li></ul><p>단순 간경변성 복수는 SAAG ≥ 1.1, 단백 &lt; 2.5, PMN &lt; 250.</p>"),
        ("1차 치료 — 식이와 이뇨제",
         "<p>대부분의 Grade 2 복수는 외래에서 관리됩니다.</p><ul><li><strong>나트륨 제한</strong> — 하루 5 g 이하 (소금 = 나트륨×2.5). 병원식 또는 영양사 교육이 도움.</li><li><strong>이뇨제 시작</strong> — 스피로놀락톤 100 mg/일 단독, 또는 푸로세미드 40 mg과 100:40 비율로 병용.</li><li><strong>적정</strong> — 5–7일 간격으로 두 약을 비례 증량 (스피로놀락톤 최대 400, 푸로세미드 최대 160). 체중 감소 0.5 kg/일 (말초부종 동반 시 1 kg/일) 목표.</li></ul><p>수분 제한은 혈청 나트륨 125 mEq/L 미만일 때만 권장합니다.</p>"),
        ("Grade 3 또는 난치성 복수",
         "<p>Grade 3 복수에서는 <strong>대량 천자(LVP)</strong>로 즉시 5 L 이상을 빼냅니다. 5 L 이상 빼면 알부민 6–8 g/L of removed ascites 보충이 필수 (post-paracentesis circulatory dysfunction 예방).</p><p>난치성 복수(refractory ascites) — 최대 용량 이뇨제로도 안 빠지거나, 이뇨제 부작용으로 못 쓰는 경우 — 의 옵션:</p><ul><li>반복 LVP + 알부민 보충</li><li><strong>TIPS</strong> — 간 내 문맥-전신 단락. 복수 호전 우수하나 간성혼수 위험 가산</li><li><strong>간이식</strong> — 근본 치료</li></ul>"),
        ("자발성 세균성 복막염(SBP)",
         "<p>복수액에 세균이 자라는 합병증으로 30일 사망률이 약 20%에 달합니다. 모든 입원 간경변·복수 환자에서 진단적 천자로 PMN을 확인합니다.</p><ul><li><strong>치료</strong> — 3세대 세팔로스포린(세포탁심·세프트리악손) 5–7일. 알부민 1.5 g/kg D1 + 1 g/kg D3 — 신부전 예방·생존율 개선.</li><li><strong>2차 예방</strong> — 한 번이라도 SBP가 있었다면 노르플록사신 400 mg/일 평생 (또는 시프로플록사신, 트리메토프림-설파메톡사졸).</li><li><strong>1차 예방</strong> — 복수 단백 &lt; 1.5 g/dL + 진행된 간경변(Child ≥ 9, 빌리루빈 ≥ 3, 신기능 저하 등) 시 권장.</li></ul>"),
    ],
    "faq": [
        ("복수가 빠지면 이뇨제를 끊어도 되나요?",
         "<p>대부분 끊지 않고 유지하거나 감량합니다. 갑자기 끊으면 복수 재발률이 매우 높기 때문입니다. 복수가 잘 조절되면 우선 푸로세미드를 줄이고 스피로놀락톤은 더 오래 유지하는 식으로 단계적으로 감량합니다. 동시에 식이 나트륨 제한(5 g/일 이하)은 평생 유지가 표준입니다. 이뇨제 감량 후에도 체중·복부 둘레·전해질을 정기 추적하며, 재발 신호(체중 1 kg 이상 증가, 복부 팽만, 다리 부종)가 보이면 즉시 외래 진료가 필요합니다.</p>"),
        ("복수에 좋은 음식이 따로 있나요?",
         "<p>특정 음식보다 \"나트륨 줄이기\"가 가장 강력한 식이 개입입니다. 한국 식단에서 나트륨이 많은 항목은 국·찌개·라면·김치·젓갈·가공육·과자류이며, 이를 줄이는 것만으로 복수 조절이 의미 있게 좋아집니다. 외식 시에는 국물을 절반 이하만 드시고, 양념·소스를 따로 받아 본인이 양을 조절하세요. 단백질은 충분히(체중 kg당 1.2-1.5 g) 섭취해야 근감소증을 예방합니다 — 단백 제한은 옛 권고로 폐기됐습니다. 영양사 교육이 있는 병원이면 적극 활용을 권합니다.</p>"),
        ("천자는 자주 받아도 안전한가요?",
         "<p>적절히 시행하면 비교적 안전합니다. 합병증은 약 1% 미만(천자 부위 출혈, 장기 손상)이고 적절한 응고 상태에서는 더 낮습니다. 5 L 이상 빼는 대량 천자(LVP)에서는 빼낸 복수액 1 L당 알부민 6-8 g을 함께 정맥 주입해 천자 후 순환 부전(post-paracentesis circulatory dysfunction)과 신부전을 예방합니다. 난치성 복수에서 2-3주 간격 반복 천자가 표준이지만, 천자 의존도가 너무 높아지면 TIPS 시술이나 간이식 평가를 고려합니다.</p>"),
        ("물을 많이 마시면 안 좋은가요?",
         "<p>나트륨 제한이 우선이고, 일반적인 수분 섭취(1-1.5 L/일)는 큰 문제가 되지 않습니다. 수분 제한은 혈청 나트륨이 125 mEq/L 미만으로 낮아지는 저나트륨혈증(dilutional hyponatremia)이 있을 때만 권장됩니다. 저나트륨혈증은 진행된 간경변에서 흔하고 사망 위험과 연관되므로 정기 검사로 추적합니다. 수분과 함께 알코올·과일주스(과당)·탄산음료도 제한 대상입니다 — 알코올은 절대 금주, 과당 음료는 추가 칼로리·인슐린 저항성으로 간 부담을 가중합니다.</p>"),
        ("복수 때문에 호흡이 답답해요. 어떻게 해야 하나요?",
         "<p>Grade 3 중증 복수의 흔한 증상으로, 횡격막을 위로 밀어 폐 확장이 제한된 상태입니다. 외래 또는 응급실에서 대량 천자(LVP)로 5 L 이상을 빼면 빠르게 호전됩니다. 호흡곤란이 심해지거나 안정 시에도 숨이 차면 기다리지 말고 내원하세요 — 간폐증후군(hepatopulmonary syndrome), 간성 흉수(hepatic hydrothorax), 폐색전 등 다른 원인이 있을 수도 있어 산소포화도 측정과 흉부 영상이 필요합니다. 간성 흉수는 흉수 천자가 추가로 필요할 수 있습니다.</p>"),
    ],
    "refs": [
        ("Aithal GP, Palaniyappan N, China L, et al. Guidelines on the management of ascites in cirrhosis. <em>Gut</em>. 2021;70(1):9–29.", "10.1136/gutjnl-2020-321790", "33067334"),
        ("European Association for the Study of the Liver. EASL Clinical Practice Guidelines for the management of patients with decompensated cirrhosis. <em>J Hepatol</em>. 2018;69(2):406–460.", "10.1016/j.jhep.2018.03.024", None),
        ("Sort P, Navasa M, Arroyo V, et al. Effect of intravenous albumin on renal impairment and mortality in patients with cirrhosis and spontaneous bacterial peritonitis. <em>N Engl J Med</em>. 1999;341(6):403–409.", "10.1056/NEJM199908053410603", "10432325"),
        ("Runyon BA. Introduction to the revised AASLD Practice Guideline management of adult patients with ascites due to cirrhosis 2012. <em>Hepatology</em>. 2013;57(4):1651–1653.", "10.1002/hep.26359", "23463403"),
    ],
    "svgs": [
        svg_table("복수 등급과 단계별 치료",
                  ["등급", "임상 소견", "1차 치료"],
                  [["1 (경증)", "초음파에서만 확인", "원인 치료, 추적"],
                   ["2 (중등도)", "배 부풂, 체중 증가", "Na 제한 + 이뇨제 외래"],
                   ["3 (중증)", "팽팽한 복부, 호흡곤란", "대량 천자 + 알부민 보충"]],
                  caption="복수 등급에 따른 단계별 접근"),
        svg_table("이뇨제 적정 — 5–7일 간격 비례 증량",
                  ["스피로놀락톤", "푸로세미드", "체중 감소 목표"],
                  [["100 mg", "40 mg", "0.5 kg/일 (부종 시 1 kg)"],
                   ["200 mg", "80 mg", "유지/증량 결정"],
                   ["300 mg", "120 mg", "최대 용량 근접"],
                   ["400 mg", "160 mg", "최대치 — 난치성 평가"]],
                  caption="100:40 비율 유지 권장 — 부족 시 단계별 증량"),
    ],
    "related": [
        ("/간경변-대상성-비대상성/", "대상성 vs 비대상성 간경변 — 어디서 갈라지나"),
        ("/간경변-식도정맥류/", "식도정맥류 — 첫 신호와 예방적 결찰"),
        ("/간경변-간신증후군/", "간신증후군 — 진단과 즉각 대응"),
    ],
})

# 02-5: 간성혼수
ARTICLES.append({
    "slug": "간경변-간성혼수",
    "h1": "간성혼수 — 외래에서 알아채는 신호와 일상 관리",
    "description": "간성혼수의 4단계(West Haven), 외래에서 가족이 먼저 알아채는 변화, 흔한 유발 요인, 락툴로스·리팍시민 치료를 정리합니다.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "간성혼수",
    "section_label": "간경화", "about": "간성혼수",
    "tldr": "간성혼수는 간경변에서 암모니아 등 신경독성 물질이 뇌에 영향을 주어 일어나는 인지·의식 변화입니다. <em>가족이 먼저 알아채는</em> 수면-각성 패턴 역전, 손떨림, 계산 곤란이 첫 신호입니다. 락툴로스가 1차 약물, 재발 시 리팍시민을 추가합니다. 한 번 발생하면 평생 예방이 표준이며 유발 요인(감염·출혈·변비·약물)의 점검이 핵심입니다.",
    "sections": [
        ("간성혼수의 단계 — West Haven 분류",
         "<p>임상 단계로 나누어 분류합니다.</p><ul><li><strong>Minimal HE / Grade 0</strong> — 진료실 평가로는 정상. 정신측정 검사로만 보임. 운전·복잡 작업에서 위험 증가.</li><li><strong>Grade 1</strong> — 수면 패턴 변화, 집중력 저하, 가벼운 인지 둔화. 가족이 \"평소와 다르다\"는 말을 처음 함.</li><li><strong>Grade 2</strong> — 시간·장소 혼동, 부적절한 행동, 손떨림(asterixis), 졸음.</li><li><strong>Grade 3</strong> — 깊은 졸음·자극 반응 가능하나 명료성 떨어짐. 의식 흐림.</li><li><strong>Grade 4</strong> — 혼수, 자극에도 반응 없음.</li></ul><p>임상에서는 가족의 변화 관찰이 진단보다 빠를 때가 많습니다. 평소와 다른 패턴이 의사소통의 결정적 단서입니다.</p>"),
        ("외래에서 가족이 먼저 알아채는 변화",
         "<p>다음 중 어느 하나라도 새로 보이면 외래에 알리세요.</p><ul><li>낮에는 졸리고 밤에 깨어 활동 (수면-각성 역전)</li><li>대화 중 단어 못 찾음, 반응이 느려짐</li><li>잔돈 계산이 안 됨, 약 복용 시간 잊음</li><li>운전 중 사고가 늘거나 길을 헷갈림</li><li>손떨림 (asterixis) — 손목을 뒤로 젖히면 새가 날갯짓하듯 떨림</li><li>이전과 다른 짜증·우울·둔감</li></ul><p>이 신호는 응급실 수준은 아니지만 외래에서 평가가 필요한 단계입니다. 진행되면 의식 저하로 갑니다.</p>"),
        ("흔한 유발 요인 — 무엇이 \"불을 댕기는가\"",
         "<p>간성혼수는 보통 유발 요인이 있습니다. 첫 평가에서 다음을 모두 점검합니다.</p><ul><li><strong>감염</strong> — SBP, 폐렴, 요로감염 (가장 흔함)</li><li><strong>위장관 출혈</strong> — 정맥류 출혈이 대표적</li><li><strong>전해질 이상</strong> — 저나트륨, 저칼륨 (이뇨제 과용)</li><li><strong>변비</strong> — 장내 암모니아 흡수 증가</li><li><strong>약물</strong> — 진정제(벤조다이아제핀, 마약성 진통제), 일부 항히스타민</li><li><strong>탈수</strong> — 설사, 구토</li><li><strong>고단백 식사</strong> (드물지만 가능)</li></ul><p>유발 요인을 먼저 잡으면 약물 치료와 함께 빠르게 호전됩니다.</p>"),
        ("치료 — 락툴로스와 리팍시민",
         "<p>두 약물이 표준입니다.</p><ul><li><strong>락툴로스</strong> — 1차 약물. 비흡수성 이당으로 장내에서 산성화시켜 암모니아를 가두고 배설. 하루 2–3회 묽은 변(soft stool 2–3회/일) 보도록 용량 적정. 보통 하루 30–60 mL.</li><li><strong>리팍시민</strong> — 비흡수성 항생제. 락툴로스만으로 재발하는 환자에게 추가. 550 mg ×2 회/일. 6개월 추적 시 재발 위험 약 50% 감소.</li></ul><p>두 약물은 서로 보완 관계로, 함께 사용하는 것이 단독보다 우월합니다.</p>"),
        ("재발 예방과 일상 관리",
         "<p>한 번이라도 간성혼수가 있었던 환자는 평생 예방 치료를 합니다.</p><ul><li>락툴로스 +/- 리팍시민 지속</li><li>유발 요인 회피 — 진정제 가급적 피함, 변비 예방, 탈수 주의</li><li>충분한 단백 섭취 (체중당 1.2–1.5 g/일) — 과거의 \"단백 제한\" 권고는 폐기됨. 식물성·유제품 단백이 동물성보다 유리.</li><li>가족 교육 — 초기 신호 알아채기, 응급 시 대응</li></ul><p>운전·고소 작업·전기 작업 등은 minimal HE에서도 사고 위험이 있어 평가 후 결정합니다.</p>"),
    ],
    "faq": [
        ("암모니아 수치가 정상이면 간성혼수가 아닌가요?",
         "<p>아닙니다. 혈중 암모니아는 진단의 결정적 지표가 아니라 보조적 지표일 뿐입니다. 임상 증상(수면-각성 패턴 변화, 손떨림, 인지 둔화, 시·공간 혼동)이 진단의 우선순위입니다. 암모니아 수치는 채혈 방법(지혈대 사용·운반 지연), 식이, 약물, 신기능에 따라 변동이 크고, 같은 환자에서도 시기에 따라 다릅니다. 외래에서는 가족이 알아챈 변화·손떨림(asterixis)·정신측정 검사(stroop test 등)가 더 중요한 진단 도구입니다.</p>"),
        ("락툴로스를 먹으면 설사를 너무 자주 해요.",
         "<p>락툴로스 적정 용량의 목표는 \"묽은 변(soft stool) 하루 2-3회\"입니다. 설사가 더 자주 나오거나 물 같은 변이 나오면 용량을 줄이세요 — 너무 많으면 탈수·전해질 이상으로 오히려 간성혼수가 악화됩니다. 반대로 변이 너무 적으면 효과가 부족합니다. 보통 하루 30-60 mL로 시작해 변 횟수에 맞춰 조정하며, 단맛·끈적임이 부담되면 분유·과일주스에 섞거나 차게 드시면 도움이 됩니다. 용량 조정은 진료의와 상의해서 결정합니다.</p>"),
        ("리팍시민이 항생제라는데 장기 복용해도 괜찮나요?",
         "<p>리팍시민은 거의 흡수되지 않는 비흡수성 항생제로, 장에서만 작용하고 전신 혈류로 들어가지 않아 일반 항생제 부작용(신장·간 독성, 약물 상호작용)이 매우 적습니다. 장기 복용의 안전성은 임상시험과 실세계 데이터로 확인되었습니다(Bass NEJM 2010, Sharma 2013). 다만 일부 환자에서 메스꺼움·복부 불편이 있을 수 있고, 매우 드물게 클로스트리듐 디피실 감염 사례 보고가 있습니다. 락툴로스만으로 재발이 잦은 환자에서 추가하면 6개월 추적 시 재발 위험이 약 50% 감소합니다.</p>"),
        ("간성혼수가 한번 왔는데 또 올까요?",
         "<p>예방 치료 없이는 1년 내 재발률이 약 40-50%로 매우 높습니다. 그래서 한 번이라도 간성혼수가 있었던 환자는 락툴로스+리팍시민 병합 예방을 평생 유지하는 것이 표준입니다. 재발 위험을 더 높이는 인자: 감염(특히 SBP), 위장관 출혈, 변비, 탈수, 전해질 이상, 진정제·마약성 진통제 사용. 이런 유발 요인을 피하는 일상 관리가 약물 못지않게 중요합니다. 경증 재발이 잦으면 단백 섭취 패턴(식물성·유제품 우선), 야식 습관, 운동, 가족 교육을 다시 점검합니다.</p>"),
        ("운전을 해도 되나요?",
         "<p>한 번이라도 간성혼수가 있었던 환자는 운전을 신중히 결정해야 합니다. 외관상 정상으로 보여도 minimal HE(아주 경한 단계)에서 반응 시간 저하, 주의력 분산, 공간 판단 오류로 사고 위험이 일반인보다 의미 있게 높다는 연구가 있습니다(Bajaj 등 다수 보고). 정신측정 검사(stroop test, paper-pencil 검사)로 minimal HE를 평가받고, 결과에 따라 운전·고소 작업·전기 작업 등을 결정하세요. 가족이 동승했을 때 평소와 다른 운전 패턴을 알아챈다면 그것도 중요한 신호입니다.</p>"),
    ],
    "refs": [
        ("Vilstrup H, Amodio P, Bajaj J, et al. Hepatic encephalopathy in chronic liver disease: 2014 Practice Guideline by the American Association for the Study of Liver Diseases and the European Association for the Study of the Liver. <em>Hepatology</em>. 2014;60(2):715–735.", "10.1002/hep.27210", "25042402"),
        ("Bass NM, Mullen KD, Sanyal A, et al. Rifaximin treatment in hepatic encephalopathy. <em>N Engl J Med</em>. 2010;362(12):1071–1081.", "10.1056/NEJMoa0907893", "20335583"),
        ("Sharma BC, Sharma P, Lunia MK, Srivastava S, Goyal R, Sarin SK. A randomized, double-blind, controlled trial comparing rifaximin plus lactulose with lactulose alone in treatment of overt hepatic encephalopathy. <em>Am J Gastroenterol</em>. 2013;108(9):1458–1463.", "10.1038/ajg.2013.219", "23877348"),
        ("Korean Association for the Study of the Liver. KASL clinical practice guidelines for liver cirrhosis: Varices, hepatic encephalopathy, and related complications. <em>Clin Mol Hepatol</em>. 2020;26(2):83–127.", "10.3350/cmh.2019.0010n", None),
    ],
    "svgs": [
        svg_table("West Haven 등급",
                  ["Grade", "임상 양상", "가족이 알아채는 신호"],
                  [["0 / minimal", "정상으로 보임", "정신측정·운전 평가에서만"],
                   ["1", "수면 변화·집중 저하", "\"평소와 다르다\" 첫 인상"],
                   ["2", "시·공간 혼동, 손떨림", "대화 곤란, 부적절 행동"],
                   ["3", "깊은 졸음, 의식 흐림", "흔들어도 멍한 상태"],
                   ["4", "혼수", "자극에 반응 없음"]],
                  caption="외래에서 자주 마주치는 단계는 1–2 — 가족 관찰이 결정적"),
        svg_checklist("간성혼수 유발 요인 점검 체크리스트",
                      ["감염 — 발열·복통·기침·소변 통증",
                       "위장관 출혈 — 토혈·흑변",
                       "전해질 이상 — 이뇨제 과용·설사",
                       "변비 — 3일 이상 배변 없음",
                       "신규 약물 — 진정제·마약성 진통제·항히스타민",
                       "탈수 — 설사·구토 후 수분 부족"],
                      caption="첫 평가에서 모두 점검 — 유발 요인 제거가 약물보다 결정적"),
    ],
    "related": [
        ("/간경변-대상성-비대상성/", "대상성 vs 비대상성 간경변 — 어디서 갈라지나"),
        ("/간경변-약물-주의/", "간경변 환자가 피해야 할 약·영양제"),
        ("/간경변-영양-근감소증/", "간경변 영양·근감소증 관리"),
    ],
})

# 02-6: 간신증후군
ARTICLES.append({
    "slug": "간경변-간신증후군",
    "h1": "간신증후군 — 진단과 즉각 대응",
    "description": "간신증후군(HRS-AKI)의 새 분류와 진단 기준, 알부민·혈관수축제(테르리프레신·노르에피네프린) 1차 치료, 간이식 평가까지를 정리합니다.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "간신증후군",
    "section_label": "간경화", "about": "간신증후군",
    "tldr": "간신증후군(HRS)은 진행된 간경변에서 신장 자체 병변 없이 신기능이 빠르게 떨어지는 합병증입니다. <em>알부민 부하 → 진단 확인 → 즉시 혈관수축제(테르리프레신 우선)</em> 흐름이 표준입니다. 한 달 내 사망률이 50%를 넘는 응급 상황으로, 결국 <strong>간이식</strong>이 가장 강력한 근본 치료입니다. 2015년 이후 \"HRS-AKI / HRS-NAKI\" 새 분류가 사용됩니다.",
    "sections": [
        ("HRS는 무엇이고 어떻게 진단하나",
         "<p>간경변에서 콩팥은 구조적으로 정상이지만, 강한 혈관 확장으로 신혈류가 떨어지면서 기능이 망가지는 상태입니다. 진단은 <strong>배제 진단</strong>입니다.</p><ul><li>간경변 + 복수</li><li>혈청 크레아티닌 ≥ 1.5 mg/dL 또는 ICA-AKI 기준 충족 (48시간 내 ≥ 0.3 또는 7일 내 50% 증가)</li><li>이뇨제 중단 + 알부민 1 g/kg/일 (최대 100 g/일) ×2일 부하 후에도 호전 없음</li><li>쇼크 없음, 신독성 약물 사용력 없음</li><li>신장 실질 질환 소견 없음 (단백뇨 &lt; 500 mg/일, 정상 초음파)</li></ul><p>2015년부터 \"HRS-1\"은 \"HRS-AKI\"로, \"HRS-2\"는 \"HRS-NAKI\"(non-AKI, 만성)로 명칭이 바뀌었습니다.</p>"),
        ("HRS-AKI vs HRS-NAKI",
         "<p>두 형태의 임상 양상이 다릅니다.</p><ul><li><strong>HRS-AKI (옛 HRS-1)</strong> — 급격하게 진행. 보통 SBP 등 감염이나 출혈 등 유발 요인 후 며칠 사이에 발생. 치료 안 하면 한 달 내 사망률 50–80%. 응급 치료 대상.</li><li><strong>HRS-NAKI (옛 HRS-2)</strong> — 서서히 진행. 난치성 복수와 함께 보임. 예후는 HRS-AKI보다 낫지만 결국 간이식 후보.</li></ul>"),
        ("1차 치료 — 알부민 + 혈관수축제",
         "<p>HRS-AKI 진단이 확인되면 즉시 시작합니다.</p><ul><li><strong>알부민</strong> — 1 g/kg D1 (최대 100 g) → 20–40 g/일 유지</li><li><strong>테르리프레신</strong> — 1 mg/4–6시간 정주, 반응에 따라 2 mg/4시간까지 증량 (3–14일)</li><li>대안: 노르에피네프린 정주 (중환자실), 또는 미도드린+옥트레오타이드 (테르리프레신 미가용 시)</li></ul><p>완전 반응(크레아티닌 정상화) 약 30–50%, 부분 반응까지 합치면 50–60%. 반응한 환자도 재발 가능하므로 추적이 필요합니다. 2022년 미국 FDA가 테르리프레신을 HRS-1 적응증으로 승인하여 한국에서도 보험 승인 진행 중입니다.</p>"),
        ("어떤 환자에게 효과가 좋은가",
         "<p>치료 반응을 예측하는 인자:</p><ul><li>치료 시작 시점 크레아티닌이 낮을수록 (조기 시작이 핵심)</li><li>SBP 등 명확한 유발 요인이 있고 그게 잘 잡히는 경우</li><li>높은 평균 동맥압 반응 (테르리프레신 시작 후 MAP 5 mmHg 이상 상승)</li><li>치료 전 빌리루빈이 너무 높지 않음</li></ul><p>반대로 다발 장기부전(ACLF), 매우 높은 빌리루빈, 인공호흡기 의존 환자에서는 약물 단독으론 한계.</p>"),
        ("간이식과 보조 치료",
         "<p>간이식이 가장 결정적인 치료입니다. HRS-AKI 환자는 MELD 점수가 자동으로 올라가 우선 배정 대상이 되며, 이식 후 약 80%에서 신기능이 회복됩니다. 다만 치료 전 1–2주 이상 신부전 지속 시 신장 회복이 떨어져 간-신 동시 이식이 검토되기도 합니다.</p><p>보조 치료:</p><ul><li>혈액투석 — 일부 환자에서 이식까지의 가교</li><li>TIPS — 일부에서 시도되나 일반적이지 않음</li><li>유발 요인 (감염, 출혈) 강력 치료</li><li>신독성 약물 회피 — NSAIDs, 아미노글리코사이드, ACE inhibitor</li></ul>"),
    ],
    "faq": [
        ("크레아티닌이 1.5인데 무조건 HRS인가요?",
         "<p>아닙니다. HRS는 배제 진단이라 다른 신장 손상 원인을 모두 배제해야 진단합니다. 흔한 다른 원인: 탈수·이뇨제 과다(가장 흔함), 신독성 약물(NSAIDs, 아미노글리코사이드, 일부 조영제), 패혈증 동반 신장 손상, 폐쇄성 요로 질환, 신장 자체 질환(사구체신염·당뇨병성 신증). 1단계는 이뇨제 중단 + 알부민 1 g/kg/일(최대 100 g) ×2일 부하입니다. 부하 후에도 크레아티닌이 호전되지 않고 다른 원인이 모두 배제되면 그제야 HRS-AKI로 진단합니다.</p>"),
        ("HRS-AKI에서 회복하면 정상으로 돌아가나요?",
         "<p>치료 반응이 좋으면 신기능이 정상화되거나 거의 정상으로 돌아갑니다. 테르리프레신+알부민 표준 치료에서 완전 반응 약 30-50%, 부분 반응까지 합치면 약 50-60%입니다. 다만 간경변 자체가 그대로 남아 있는 한 재발 위험이 높아(1년 내 재발 약 50%), 간이식 평가가 강력히 권장됩니다. 회복 후에도 NSAIDs·신독성 약물 회피, 감염 조기 치료, 정기 신기능 추적이 필수이며, 이뇨제 재시작은 신중히 결정합니다.</p>"),
        ("테르리프레신은 한국에서 쓸 수 있나요?",
         "<p>한국은 그동안 옥트레오타이드+미도드린이 주로 쓰였으나 최근 테르리프레신 도입이 진행 중이며, 일부 의료기관에서 사용 가능합니다. 2022년 미국 FDA가 CONFIRM 시험(Wong NEJM 2021) 근거로 테르리프레신을 HRS-1(현 HRS-AKI) 적응증으로 승인하면서 국제적 표준이 더 명확해졌습니다. 테르리프레신을 쓸 수 없는 상황에서는 노르에피네프린(중환자실)이나 옥트레오타이드+미도드린 조합이 대안입니다. 진료의에게 본인 의료기관의 약물 가용성과 보험 상황을 확인하세요.</p>"),
        ("HRS이면 무조건 간이식 받아야 하나요?",
         "<p>이식이 가장 강력한 근본 치료지만 모든 환자에서 즉시 필요한 것은 아닙니다. 약물 치료(테르리프레신+알부민)에 반응해 신기능이 회복되면 이식 시기를 늦추거나 안정 후 일반 일정으로 평가할 수 있습니다. 다만 HRS-AKI 자체가 이식 우선순위에 가산되는 강력한 신호이므로 진단 시점부터 평가를 시작하는 것이 표준입니다. 이식 전 신부전이 1-2주 이상 지속되면 신장 회복이 떨어져 간-신 동시 이식이 검토되기도 합니다.</p>"),
        ("HRS이 한 번 회복되면 다시 안 오나요?",
         "<p>재발률이 매우 높습니다. 1년 내 재발 약 50%, 특히 첫 6개월이 가장 위험합니다. 재발 위험을 높이는 인자: 잔존 간경변 진행, 새 감염(SBP·폐렴·요로감염), NSAIDs·신독성 약물 사용, 탈수, 이뇨제 과다 사용. 회복 후에도 정기 신기능 추적(BUN·크레아티닌·전해질·소변검사 매 1-3개월), 신독성 약물 점검, 감염 조기 평가, 간 기능 추적이 필수이며, 이식 평가는 회복 후에도 지속하는 것이 일반적입니다.</p>"),
    ],
    "refs": [
        ("Angeli P, Garcia-Tsao G, Nadim MK, Parikh CR. News in pathophysiology, definition and classification of hepatorenal syndrome: A step beyond the International Club of Ascites (ICA) consensus document. <em>J Hepatol</em>. 2019;71(4):811–822.", "10.1016/j.jhep.2019.07.002", "31302175"),
        ("Wong F, Pappas SC, Curry MP, et al. Terlipressin plus Albumin for the Treatment of Type 1 Hepatorenal Syndrome (CONFIRM). <em>N Engl J Med</em>. 2021;384(9):818–828.", "10.1056/NEJMoa2008290", "33657294"),
        ("Cavallin M, Piano S, Romano A, et al. Terlipressin given by continuous intravenous infusion versus intravenous boluses in the treatment of hepatorenal syndrome. <em>Hepatology</em>. 2016;63(3):983–992.", "10.1002/hep.28396", "26659927"),
        ("European Association for the Study of the Liver. EASL Clinical Practice Guidelines for the management of patients with decompensated cirrhosis. <em>J Hepatol</em>. 2018;69(2):406–460.", "10.1016/j.jhep.2018.03.024", None),
    ],
    "svgs": [
        svg_table("HRS-AKI 진단 기준 (ICA 2015)",
                  ["조건", "기준"],
                  [["기저 질환", "간경변 + 복수"],
                   ["AKI 기준", "Cr ≥ 0.3 mg/dL 증가 (48h) 또는 50% 증가 (7일)"],
                   ["반응 검사", "이뇨제 중단 + 알부민 1 g/kg ×2일 후 호전 없음"],
                   ["배제 1", "쇼크 없음, 신독성 약물 없음"],
                   ["배제 2", "단백뇨 <500 mg/일, 신장 초음파 정상"]],
                  caption="배제 진단 — 모든 항목을 충족해야 HRS-AKI"),
        svg_table("HRS-AKI 치료 흐름",
                  ["단계", "약물", "용량"],
                  [["1단계", "알부민 부하", "1 g/kg D1 → 20–40 g/일 유지"],
                   ["2단계", "테르리프레신 정주", "1 mg/4–6h, 반응 시 2 mg/4h까지"],
                   ["대안", "노르에피네프린 (ICU)", "0.5–3 mg/h, MAP 목표 ≥85"],
                   ["대안", "미도드린 + 옥트레오타이드", "테르리프레신 미가용 시"],
                   ["근본", "간이식 평가 시작", "MELD 자동 가산, 우선 배정"]],
                  caption="조기 시작이 반응률을 결정 — 진단 즉시 1단계 시작"),
    ],
    "related": [
        ("/간경변-복수/", "복수 — 단계별 관리"),
        ("/간경변-간이식-평가/", "간이식 평가 — 누가, 언제 시작하나"),
        ("/간경변-Child-Pugh-MELD/", "Child-Pugh와 MELD — 두 점수가 의미하는 것"),
    ],
})

# 02-7: 영양·근감소증
ARTICLES.append({
    "slug": "간경변-영양-근감소증",
    "h1": "간경변 영양·근감소증 — 단백 제한은 옛말입니다",
    "description": "간경변 환자의 적정 단백·열량 섭취, 야식의 의미, sarcopenia 진단과 운동 권고를 정리합니다. \"단백 제한\"의 옛 권고가 왜 폐기됐는지.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "영양·근감소증",
    "section_label": "간경화", "about": "간경변 영양 결핍",
    "tldr": "간경변에서 \"단백질 제한\"은 옛 권고로 이미 폐기되었습니다. 오히려 <em>체중당 단백 1.2–1.5 g, 열량 30–35 kcal/일</em>이 표준이며, 근감소증(sarcopenia)이 있으면 더 적극적으로 보충합니다. 야식(취침 전 간식)은 야간 단식 시간을 줄여 근육 분해를 막는 의미 있는 개입입니다. 식물성·유제품 단백이 동물성보다 유리합니다.",
    "sections": [
        ("\"단백 제한\"이 왜 폐기됐나",
         "<p>과거에는 간성혼수 위험을 줄이려고 단백 제한을 권했습니다. 그러나 최근 연구에서:</p><ul><li>단백 제한은 간성혼수 빈도를 줄이지 못함</li><li>오히려 근감소증·영양실조를 가속화</li><li>근육이 줄면 암모니아 처리 능력이 떨어져 간성혼수가 악화</li></ul><p>2014년 ISHEN 합의 이후 단백 제한은 권장되지 않으며, ESPEN 2019 가이드라인도 동일 입장입니다.</p>"),
        ("권장 섭취 — 단백·열량",
         "<p>간경변 환자의 표준 권고:</p><ul><li><strong>열량</strong>: 30–35 kcal/kg(이상 체중)/일</li><li><strong>단백</strong>: 1.2–1.5 g/kg/일 (대상성·비대상성 모두)</li><li><strong>식이 횟수</strong>: 하루 4–6회 소량으로 분할 + 취침 전 간식</li></ul><p>예: 체중 60 kg → 열량 1800–2100 kcal, 단백 72–90 g (계란 약 12개 단백질 분량). 특정 음식만으로 채우기 어려우므로 주식+반찬+간식의 조합이 권장됩니다.</p>"),
        ("야식(취침 전 간식)의 의미",
         "<p>간경변 환자는 6–8시간 단식만으로도 \"가속 굶주림\" 상태가 됩니다 (정상인보다 단식 적응이 빠름). 근육 단백이 분해되어 에너지원으로 쓰입니다.</p><ul><li>취침 전 200–250 kcal 간식 → 야간 단식 시간 단축 → 근육 분해 감소</li><li>탄수화물 + 일부 단백 권장 (예: 우유 한 잔 + 빵, 그릭 요거트, 두유 + 견과류)</li><li>간성혼수 회피 위해 동물성 단백보다 식물성·유제품 우선</li></ul><p>임상시험에서 야식만으로도 6개월 후 근육량 보존이 확인되었습니다.</p>"),
        ("근감소증 — 어떻게 알아채나",
         "<p>간경변 환자의 30–70%가 근감소증을 가집니다. 진단:</p><ul><li><strong>CT 기반</strong> — L3 추체 단면적의 골격근 지수(SMI). 가장 정확하나 측정 필요</li><li><strong>임상</strong> — 종아리 둘레, 손악력, 일어서기 속도</li><li><strong>SARC-F 설문</strong> — 5문항 간이 평가</li></ul><p>근감소증이 있으면 간이식 후 합병증·사망률이 높아져 별도 평가 대상이 됩니다.</p>"),
        ("운동과 단백 보충",
         "<p>운동:</p><ul><li>유산소 + 저항 운동 병행. 주 3–5회, 30분 이상</li><li>비대상성·복수 환자도 가능한 범위에서 — 가벼운 걷기·실내 자전거</li><li>피로·복부 불편 없이 가능한 강도부터</li></ul><p>단백 보충제:</p><ul><li>식이로 부족하면 BCAA(가지사슬 아미노산) 보충 — 몇몇 RCT에서 합병증 감소·생존 개선</li><li>유청 단백, 식물성 단백 보충제 사용 가능</li></ul>"),
    ],
    "faq": [
        ("간성혼수가 있어도 단백을 먹어야 하나요?",
         "<p>네. 과거의 \"단백 제한\" 권고는 폐기되었습니다(2014 ISHEN 합의). 단백 제한이 간성혼수 빈도를 줄이지 못하고 오히려 근감소증을 가속화해 장기적으로 간성혼수 위험을 높인다는 데이터가 누적되었기 때문입니다. 급성 간성혼수 발생 직후 1-2일은 일시적으로 줄일 수 있지만, 회복기·예방기에는 정상 권장량(1.2-1.5 g/kg/일)을 유지합니다. 식물성·유제품 단백이 동물성보다 분지쇄 아미노산(BCAA) 비율이 높고 암모니아 부담이 적어 더 안전합니다.</p>"),
        ("야식이 살찌게 하지 않나요?",
         "<p>총 열량을 늘리는 것이 아니라 분배를 바꾸는 것입니다. 저녁 식사를 평소보다 조금 줄이고 취침 전 200-250 kcal를 두는 식으로 조정하면 총 칼로리는 같거나 적습니다. 야식의 핵심은 \"야간 단식 시간 단축\"입니다 — 간경변 환자는 6-8시간 단식만으로도 \"가속 굶주림\" 상태가 되어 근육 단백이 분해되기 시작합니다. 야식으로 단식 시간을 4-5시간으로 줄이면 근육량 보존 효과가 임상시험에서 확인되었습니다(Tsien 2012). 우유+빵, 그릭 요거트+견과류 같은 간단한 조합으로 충분합니다.</p>"),
        ("BCAA 보충제는 효과가 있나요?",
         "<p>분지쇄 아미노산(BCAA: 류신·이소류신·발린) 보충은 일부 환자에서 합병증 감소·근육량 보존·생존 개선 효과가 보고됩니다(이탈리아·일본 RCT 다수). 효과가 가장 잘 나타나는 그룹은 식이 단백 섭취가 부족한 비대상성 환자, 근감소증이 있는 환자, 야식이 어려운 환자입니다. 한국에서 보험 적용 여부는 제품·적응증에 따라 다릅니다. 식이로 단백 권장량을 충분히 채우는 환자에서는 추가 이득이 명확하지 않아 식이 평가가 우선이며, 모든 환자에 일률적으로 권하지 않습니다.</p>"),
        ("간경변인데 운동해도 되나요?",
         "<p>일반적으로 권장됩니다. 운동은 단순 보조가 아니라 \"근감소증 예방·치료\"의 핵심으로, 간이식 후 합병증·사망률을 의미 있게 줄입니다. 표준 권고: 유산소 운동 주 5회·30분 가벼운 강도(빠르게 걷기·실내 자전거) + 저항 운동 주 2-3회(큰 근육군 위주). 비대상성·복수 시기에도 가능한 범위에서 — 산책·계단 오르기·앉아서 하는 저항 운동도 도움. 정맥류가 있을 때 무거운 역기 같은 발살바 동작은 피하고, 운동 시작 전 진료의와 상의해 강도를 정하세요.</p>"),
        ("계란을 매일 먹어도 되나요?",
         "<p>괜찮습니다. 계란은 단백·콜린·비타민 D·B12가 풍부하고 가격·접근성도 좋아 간경변 환자에 매우 적합한 식품입니다. \"계란이 콜레스테롤을 올린다\"는 우려는 일반인에서도 과거의 권고로, 최근 가이드라인은 일반 인구에서 하루 1-2개를 안전하게 봅니다. 간경변 환자는 오히려 단백·열량 부족이 더 큰 위험이므로 계란 섭취가 도움이 됩니다. 단, 날계란은 살모넬라 위험으로 면역저하 환자에서는 익혀 드세요. 수란·반숙·완숙 모두 가능합니다.</p>"),
    ],
    "refs": [
        ("Plauth M, Bernal W, Dasarathy S, et al. ESPEN guideline on clinical nutrition in liver disease. <em>Clin Nutr</em>. 2019;38(2):485–521.", "10.1016/j.clnu.2018.12.022", "30712783"),
        ("Tandon P, Montano-Loza AJ, Lai JC, Dasarathy S, Merli M. Sarcopenia and frailty in decompensated cirrhosis. <em>J Hepatol</em>. 2021;75 Suppl 1:S147–S162.", "10.1016/j.jhep.2021.01.025", "34039486"),
        ("Tsien CD, McCullough AJ, Dasarathy S. Late evening snack: exploiting a period of anabolic opportunity in cirrhosis. <em>J Gastroenterol Hepatol</em>. 2012;27(3):430–441.", "10.1111/j.1440-1746.2011.06951.x", "21916988"),
        ("European Association for the Study of the Liver. EASL Clinical Practice Guidelines on nutrition in chronic liver disease. <em>J Hepatol</em>. 2019;70(1):172–193.", "10.1016/j.jhep.2018.06.024", None),
    ],
    "svgs": [
        svg_table("간경변 환자 표준 영양 권고",
                  ["항목", "권고량 (이상 체중당)", "예 (60 kg)"],
                  [["총 열량", "30–35 kcal/kg/일", "1800–2100 kcal/일"],
                   ["단백질", "1.2–1.5 g/kg/일", "72–90 g/일"],
                   ["식이 횟수", "하루 4–6회 + 야식", "3끼 + 간식 + 취침 전"],
                   ["나트륨", "복수 시 5 g/일 이하", "국·찌개 줄이기"]],
                  caption="단백 제한은 옛 권고 — 현재는 적극 보충이 표준"),
        svg_checklist("취침 전 간식 (야간 단식 단축) — 권장 200–250 kcal",
                      ["우유 한 잔 + 식빵 한 쪽",
                       "그릭 요거트 + 견과류 한 줌",
                       "두유 + 통곡물 시리얼",
                       "삶은 계란 1개 + 바나나",
                       "BCAA 보충제 (식이 부족 시)"],
                      caption="식물성·유제품 단백 우선 — 동물성 단백보다 간성혼수 위험 낮음"),
    ],
    "related": [
        ("/간경변-간성혼수/", "간성혼수 — 외래에서 알아채는 신호와 일상 관리"),
        ("/간경변-약물-주의/", "간경변 환자가 피해야 할 약·영양제"),
        ("/간경변-복수/", "복수 — 단계별 관리"),
    ],
})

# 02-8: 간이식 평가
ARTICLES.append({
    "slug": "간경변-간이식-평가",
    "h1": "간이식 평가 — 누가, 언제 시작하나",
    "description": "간이식 적응증, MELD 임계값, KONOS 등록, 살아있는 기증자 이식, 평가 흐름과 추적 일정을 정리합니다.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "간이식 평가",
    "section_label": "간경화", "about": "간이식",
    "tldr": "간이식은 비대상성 간경변의 근본 치료입니다. <em>MELD ≥ 15</em>가 일반적인 평가 시작 임계값이며, 한국은 KONOS 등록 후 MELD 기반 우선순위를 받습니다. 뇌사자 이식 외에 한국은 살아있는 기증자(생체) 이식이 활발해 평균 대기 기간이 짧은 편입니다. 평가는 다학제로 1–2주 안에 진행됩니다.",
    "sections": [
        ("간이식이 필요한 환자",
         "<p>다음 중 하나에 해당하면 평가를 시작합니다.</p><ul><li>비대상성 간경변(복수·정맥류 출혈·간성혼수·황달 중 하나 이상)</li><li>MELD 점수 ≥ 15</li><li>난치성 복수, 반복 SBP, 반복 정맥류 출혈, 반복 간성혼수</li><li>간세포암 — Milan criteria 또는 한국 기준 충족</li><li>급성 간부전 (King's College / Clichy 기준)</li><li>대사 질환 (윌슨병, 알파-1 항트립신 결핍 등)</li></ul><p>간세포암은 별도 기준이 있어, 간기능이 좋아도 종양 부담에 따라 이식 적응이 됩니다.</p>"),
        ("MELD와 KONOS 우선순위",
         "<p>한국은 KONOS(Korean Network for Organ Sharing)를 통해 뇌사자 이식이 배정됩니다. 우선순위는 다음을 기반으로:</p><ul><li>MELD 점수 (높을수록 우선)</li><li>응급도 (status 1A — 급성 간부전 등 최우선)</li><li>등록 기간 (동일 점수에서 오래된 등록 우선)</li><li>혈액형 일치</li></ul><p>MELD 15 이상이면 이식 이득(survival benefit)이 약물·관찰보다 명확해지는 일반 임계값입니다. 그 미만에서는 이식 위험이 이득을 상회할 수 있어 평가만 하고 등록은 미루기도 합니다.</p>"),
        ("뇌사자 이식 vs 생체 이식",
         "<p>두 경로의 비교:</p><ul><li><strong>뇌사자 이식</strong> — KONOS 대기. 한국은 뇌사자 기증이 적어 평균 대기 기간이 길고, 대기 중 사망률이 의미 있음.</li><li><strong>생체 이식</strong> — 가족 등 살아있는 기증자의 간 일부(보통 우엽)를 이식. 한국은 생체 이식 비율이 세계 최고 수준 (전체 간이식의 약 70%). 대기 시간이 짧고 일정 조정 가능.</li></ul><p>생체 이식은 기증자 수술 위험(사망률 약 0.2%)이 있어 기증자 동의·평가가 까다롭게 진행됩니다.</p>"),
        ("이식 전 평가 — 무엇을 보나",
         "<p>다학제 평가가 1–2주 안에 진행됩니다.</p><ul><li><strong>의학적</strong> — 심혈관(심초음파·관상동맥 평가), 폐(폐기능·CT), 신장(eGFR·단백뇨), 감염(B/C형 간염, HIV, CMV, EBV), 영양·근감소증</li><li><strong>외과적</strong> — 영상(혈관 해부, 종양 위치), 이식외과 수술 결정</li><li><strong>심리·사회</strong> — 이식 후 평생 면역억제제 복용 가능성, 가족 지원, 음주력</li><li><strong>치과</strong> — 감염 원인 제거</li><li><strong>금주 평가</strong> — 알코올성에서 보통 6개월 금주 권고</li></ul>"),
        ("이식 후 — 무엇이 달라지나",
         "<p>이식 후 5년 생존율은 70–80% (간세포암 동반 시 다소 낮음). 생존을 결정하는 요소:</p><ul><li>면역억제제 평생 복용 — 타크롤리무스 위주, 부작용(신독성, 당뇨, 감염, 종양) 모니터링</li><li>거부 반응 — 첫 1년 가장 위험, 정기 추적</li><li>원인 질환 재발 — B형간염은 항바이러스제 평생, MASH·알코올성은 생활 관리</li><li>감염 예방 — 백신, 위생, 일부 음식 회피</li></ul><p>이식은 끝이 아니라 새로운 종류의 추적의 시작입니다.</p>"),
    ],
    "faq": [
        ("MELD가 14인데 이식 평가를 시작해도 되나요?",
         "<p>네, 평가는 시작할 수 있습니다. 평가 절차(다학제 검사, 심혈관·호흡·신장·감염·심리·치과 평가)는 1-2주에서 수 개월이 걸리므로, MELD가 더 오르기 전 미리 시작하면 등록 시점에 신속하게 진행됩니다. 등록 자체는 보통 MELD 15 이상에서 본격화하지만, 난치성 복수·반복 SBP·반복 정맥류 출혈 같은 합병증이 있으면 MELD 14에서도 등록 가산 점수를 받을 수 있습니다. 한국 KONOS는 이런 예외 상황에 대한 별도 평가 제도를 운영합니다.</p>"),
        ("생체 이식 기증자는 위험하지 않나요?",
         "<p>기증자 사망률은 약 0.2%로 매우 낮으나 0이 아닙니다. 합병증 가능성은 약 20-30%로 대부분 경증·일과성(상처 통증, 일시적 담즙 누출, 감염)이지만, 약 1-2%에서 재수술이 필요한 중증 합병증이 발생합니다. 이 때문에 기증자 평가가 매우 까다롭게 진행됩니다 — 의학적(간 부피·기능·혈관 해부), 외과적(수술 위험), 심리적(자발성·강요 여부·이식 후 적응) 모든 측면에서 다학제 평가를 거치며, 기증자 본인이 언제든 결정을 철회할 권리가 보장됩니다. 한국은 생체 이식이 활발해 평가 경험이 풍부한 의료기관이 많습니다.</p>"),
        ("알코올성 간경변인데 이식 받을 수 있나요?",
         "<p>받을 수 있습니다. 한국·미국·유럽 모두 6개월 금주가 통상 조건이지만 절대적 기준은 아니며, 일부 응급 상황(급성 알코올성 간염 + 간부전)에서는 더 짧은 금주 후에도 이식이 가능하다는 합의가 최근 발표되었습니다. 평가에서 중요한 것은 단순 금주 기간이 아니라 음주 재발 위험입니다 — 정신건강의학·중독 전문 평가, 가족·사회적 지원, 재활 프로그램 참여 의지를 종합 평가합니다. 이식 후에도 평생 절대 금주가 권고되며, 음주 재발 시 이식간 손상이 가속화되므로 사후 추적이 매우 중요합니다.</p>"),
        ("이식 후 면역억제제는 평생 먹어야 하나요?",
         "<p>네, 평생입니다. 다만 시간이 지나며 용량이 점진적으로 감소하고 일부 약은 단순화됩니다. 일반적으로 1차 약은 타크롤리무스(또는 사이클로스포린)이며, 초기 1년은 스테로이드·마이코페놀레이트와 병합하다가 안정되면 단일 또는 2제 요법으로 줄입니다. HCC로 이식받은 환자에서는 mTOR 억제제(시롤리무스·에베롤리무스)가 종양 재발을 줄일 수 있다는 데이터로 후기에 전환하기도 합니다. 자가 중단·임의 감량은 거부반응을 유발하므로 절대 금지입니다.</p>"),
        ("간이식 후 다시 술을 마실 수 있나요?",
         "<p>알코올성 간경변으로 이식받은 환자는 절대 금주가 권고됩니다. 음주 재개 시 이식간이 빠르게 손상되고 재이식 후보가 되기 어렵습니다. 알코올 외 원인으로 이식받은 환자도 \"안전한 음주량\"은 없습니다 — 이식 면역억제제와 알코올의 상호작용, 간 회복기의 취약성, 심혈관·종양 위험 가산을 고려할 때 모든 이식 환자에서 절제 또는 절대 금주를 권합니다. 사회적 행사 등 불가피한 상황에서는 무알코올 옵션을 미리 준비하고, 가족·친지의 이해를 구하는 것이 도움이 됩니다.</p>"),
    ],
    "refs": [
        ("Martin P, DiMartini A, Feng S, Brown R Jr, Fallon M. Evaluation for liver transplantation in adults: 2013 practice guideline by the AASLD and the American Society of Transplantation. <em>Hepatology</em>. 2014;59(3):1144–1165.", "10.1002/hep.26972", "24716201"),
        ("European Association for the Study of the Liver. EASL Clinical Practice Guidelines: Liver transplantation. <em>J Hepatol</em>. 2016;64(2):433–485.", "10.1016/j.jhep.2015.10.006", None),
        ("Lee SG. A complete treatment of adult living donor liver transplantation: a review of surgical technique and current updates from 1991 initial experiences. <em>Am J Transplant</em>. 2015;15(1):17–38.", "10.1111/ajt.12907", "25358749"),
        ("Korean Network for Organ Sharing (KONOS). Annual Data Report. Korean Society for Transplantation.", None, None),
    ],
    "svgs": [
        svg_table("간이식 평가 시작 임계값",
                  ["적응증", "구체 기준"],
                  [["비대상성 간경변", "복수·정맥류 출혈·간성혼수·황달"],
                   ["MELD 점수", "≥ 15 (이식 이득 임계값)"],
                   ["반복 합병증", "난치성 복수·반복 SBP·재발 출혈"],
                   ["간세포암", "Milan / 한국 기준 충족"],
                   ["급성 간부전", "King's College 또는 Clichy 기준"]],
                  caption="하나라도 충족하면 평가 시작"),
        svg_table("뇌사자 이식 vs 생체 이식 (한국)",
                  ["항목", "뇌사자 이식", "생체 이식"],
                  [["대기 기간", "평균 길음", "수 주~수 개월"],
                   ["우선순위", "MELD 기반 KONOS", "기증자 평가 후"],
                   ["기증자 위험", "해당 없음", "사망률 ≈ 0.2%"],
                   ["국내 비율", "약 30%", "약 70%"],
                   ["일정", "예측 어려움", "조정 가능"]],
                  caption="한국은 생체 이식이 세계 최고 수준 — 평균 대기 짧음"),
    ],
    "related": [
        ("/간경변-Child-Pugh-MELD/", "Child-Pugh와 MELD — 두 점수가 의미하는 것"),
        ("/간경변-대상성-비대상성/", "대상성 vs 비대상성 간경변 — 어디서 갈라지나"),
        ("/간경변-간신증후군/", "간신증후군 — 진단과 즉각 대응"),
    ],
})

# 02-9: 약물 주의
ARTICLES.append({
    "slug": "간경변-약물-주의",
    "h1": "간경변 환자가 피해야 할 약·영양제 — 외래에서 점검하는 목록",
    "description": "간경변 환자에서 신독성·간성혼수·출혈을 유발할 수 있는 약물 카테고리(NSAIDs·일부 항생제·진정제·한약·건강기능식품)를 정리합니다.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "약물 주의",
    "section_label": "간경화", "about": "약물성 간 손상",
    "tldr": "간경변 환자는 약물 대사·배설이 떨어지고 신기능이 약합니다. <em>NSAIDs(이부프로펜·디클로페낙)</em>는 신독성과 출혈로 가장 위험하고, <em>벤조다이아제핀·마약성 진통제</em>는 간성혼수를 유발합니다. 한약·건강기능식품 일부도 약물성 간 손상의 흔한 원인입니다. 외래에서 복용 중인 모든 제품을 사진으로 정리해 보여주는 것이 첫 단계입니다.",
    "sections": [
        ("왜 간경변에서는 약이 다른가",
         "<p>간경변에서는 다음 변화가 동시에 일어납니다.</p><ul><li>간 대사 능력 감소 → 약물 농도 상승</li><li>알부민 감소 → 단백 결합 약물의 유리 분획 증가</li><li>문맥-전신 단락 → 1차 통과 효과 감소</li><li>신기능 저하 → 신배설 약물 축적</li><li>응고 인자 부족 → 출혈 위험 증가</li></ul><p>이 모든 변화가 결합해 일반인에게 안전한 약이 간경변 환자에게는 위험할 수 있습니다.</p>"),
        ("절대 피해야 할 약 — NSAIDs",
         "<p>이부프로펜, 디클로페낙, 메페남산 등 비스테로이드성 항염제는 다음 이유로 위험합니다.</p><ul><li>신혈류 감소 → 급성 신부전, 간신증후군 유발</li><li>위장관 출혈 위험 증가 (정맥류 환자에서 특히)</li><li>복수 악화 (나트륨·물 저류)</li></ul><p>대안: 아세트아미노펜(타이레놀) — 하루 2 g 이하면 비교적 안전. 단, 알코올성 간질환에서는 1 g 이하 권장.</p>"),
        ("간성혼수를 유발하는 약",
         "<p>다음은 잠재 간성혼수 환자에서 유발 요인이 됩니다.</p><ul><li><strong>벤조다이아제핀</strong> — 알프라졸람·디아제팜 등 수면제·진정제. 가능하면 회피, 불가피하면 옥사제팜·로라제팜처럼 간 대사 의존 적은 약 단기간만.</li><li><strong>마약성 진통제</strong> — 코데인·트라마돌·옥시코돈. 변비 + 진정으로 이중 위험.</li><li><strong>일부 항히스타민</strong> — 1세대(클로르페니라민, 디펜히드라민) 진정 효과로 위험. 2세대 위주.</li></ul><p>수면 문제로 진정제를 처방받았다면 진료 시 알리세요.</p>"),
        ("한약·건강기능식품의 위험",
         "<p>한국에서 약물성 간 손상의 가장 흔한 원인 중 하나입니다.</p><ul><li>한약재 — 백선·유근피·하수오 등이 보고된 사례</li><li>녹차 추출물 (특히 catechin 농축물) — 일부 사례에서 급성 간염</li><li>가르시니아·녹용·관절 영양제 일부 — 보고 있음</li><li>'간 영양제'를 표방하는 다수 제품 — 검증되지 않은 성분</li></ul><p>외래에서 \"이건 한약/영양제니까 약이 아니다\"라는 인식이 가장 위험합니다. 모두 약처럼 작용할 수 있습니다.</p>"),
        ("외래에서 점검하는 방법",
         "<p>다음을 매 외래에 가져오세요.</p><ul><li>처방약 — 약 봉투 또는 사진</li><li>OTC 약 — 두통약, 소화제, 종합감기약</li><li>건강기능식품 전부 — 비타민·미네랄·홍삼·한약 포함</li><li>최근 3개월 간 새로 시작한 모든 약</li></ul><p>이 점검만으로도 약물성 간 손상 원인을 30–50%에서 찾아냅니다.</p>"),
    ],
    "faq": [
        ("타이레놀이 간에 안 좋다는데 정말 먹어도 되나요?",
         "<p>네, 적절한 용량 내에서는 간경변 환자에서도 NSAIDs보다 안전한 1차 진통제입니다. 안전 용량 기준: 일반 성인 하루 4 g 이하, 간경변·고령·저체중·만성 음주 환자는 하루 2 g 이하로 더 보수적으로. 타이레놀이 위험한 상황은 대부분 \"한 번에 7.5 g 이상 과량\" 또는 \"만성 4 g 이상 + 알코올 동반\"입니다. 외래에서는 약 봉투를 가져와 \"종합감기약·소화제 등에 들어있는 아세트아미노펜 함량\"을 함께 점검합니다 — 여러 약에 중복으로 들어가 있어 본인도 모르게 과량이 되는 경우가 흔합니다.</p>"),
        ("스타틴이 간에 나쁘다는데 끊어야 하나요?",
         "<p>대부분의 경우 끊지 않습니다. 오히려 대상성 간경변에서 스타틴 사용이 문맥압 감소·간경변 진행 지연·간세포암 위험 감소와 연관된다는 연구가 누적되었습니다(Simon Hepatology 2016 등). 비대상성 간경변에서는 약물 농도 상승과 근육 부작용(횡문근융해) 위험이 약간 증가해 신중히 결정합니다 — 일반적으로 저용량부터 시작하고 ALT·CK를 추적합니다. 본인이 자가 중단하는 것이 가장 위험합니다 — 심혈관 이득을 잃기 때문입니다. 간 검사 이상 신호가 있으면 진료의와 상의해서 결정하세요.</p>"),
        ("녹차나 홍삼은 안전한가요?",
         "<p>일반적인 녹차·홍삼 음용은 대부분 안전합니다. 위험한 것은 \"농축 추출물 보충제\"입니다. 녹차 catechin 농축 보충제(EGCG 고용량)는 급성 간염 사례가 누적되어 미국 FDA가 경고를 발령했습니다. 홍삼은 사례 보고가 일부 있으나 빈도는 낮습니다. 한국에서는 한약·건강기능식품이 약물성 간 손상의 30-40%를 차지하므로 \"이건 자연이라 안전하다\"는 인식이 가장 위험합니다. 새로 시작하는 모든 보충제는 외래에 알리고, 시작 1-3개월 시점 ALT 추적이 권장됩니다.</p>"),
        ("관절염약을 끊으면 통증이 너무 심해요. 대안은?",
         "<p>1차 대안: 아세트아미노펜(2 g/일 이하), 국소 도포제(디클로페낙 겔·캡사이신), 물리치료, 운동치료, 체중 감량. 통증이 더 심하면 트라마돌을 신중히 검토 — 진정 효과로 간성혼수 위험이 있어 저용량부터 시작하고 변비 동반 시 더 주의합니다. 마약성 진통제(코데인·옥시코돈)는 가급적 회피. NSAIDs(이부프로펜·디클로페낙·메페남산)는 간경변에서 신독성·복수 악화·정맥류 출혈 위험이 의미 있게 증가하므로 단기간이라도 회피가 원칙입니다. 통증 클리닉 협진이 도움이 되는 경우가 많습니다.</p>"),
        ("약 부작용으로 간수치가 올랐을 때 그 약을 다시 먹어도 되나요?",
         "<p>일반적으로 같은 약 재투여(re-challenge)는 권장되지 않습니다. 재투여 시 더 심한 손상(rechallenge severity)이 보고되며, 일부에서 급성 간부전으로 이어진 사례가 있어 윤리적·임상적으로 신중합니다. 같은 계열 다른 약(class switch)은 일부 가능 — 예: amoxicillin/clavulanate로 간 손상 후 다른 항생제 계열로 전환. 그러나 일부 약물(아세트아미노펜 과량 후, 일부 한약 후)은 같은 계열도 회피합니다. 약물성 간 손상 의심 시 진료의가 RUCAM 점수로 인과관계를 평가하고 재투여 여부를 결정합니다.</p>"),
    ],
    "refs": [
        ("Lewis JH, Stine JG. Review article: prescribing medications in patients with cirrhosis - a practical guide. <em>Aliment Pharmacol Ther</em>. 2013;37(12):1132–1156.", "10.1111/apt.12324", "23638982"),
        ("Chalasani NP, Maddur H, Russo MW, Wong RJ, Reddy KR. ACG Clinical Guideline: Diagnosis and Management of Idiosyncratic Drug-Induced Liver Injury. <em>Am J Gastroenterol</em>. 2021;116(5):878–898.", "10.14309/ajg.0000000000001259", "33929376"),
        ("European Association for the Study of the Liver. EASL Clinical Practice Guidelines: Drug-induced liver injury. <em>J Hepatol</em>. 2019;70(6):1222–1261.", "10.1016/j.jhep.2019.02.014", None),
        ("Suk KT, Kim DJ, Kim CH, et al. A prospective nationwide study of drug-induced liver injury in Korea. <em>Am J Gastroenterol</em>. 2012;107(9):1380–1387.", "10.1038/ajg.2012.138", "22733302"),
    ],
    "svgs": [
        svg_table("간경변에서 위험한 약 카테고리",
                  ["카테고리", "예", "주된 위험"],
                  [["NSAIDs", "이부프로펜·디클로페낙", "신독성, 출혈, 복수"],
                   ["벤조다이아제핀", "알프라졸람·디아제팜", "간성혼수"],
                   ["마약성 진통제", "코데인·옥시코돈", "변비 + 진정 → 혼수"],
                   ["1세대 항히스타민", "클로르페니라민", "진정 효과"],
                   ["일부 한약·건기식", "백선·녹차 농축", "약물성 간 손상"]],
                  caption="외래에서 처방·복용 점검 시 우선 확인 카테고리"),
        svg_checklist("매 외래마다 가져올 것",
                      ["처방약 — 약 봉투 또는 사진",
                       "OTC 약 — 두통약·소화제·감기약 모두",
                       "건강기능식품 전부 — 비타민·홍삼·한약 포함",
                       "최근 3개월 새 시작한 모든 제품",
                       "최근 한약·민간요법 — 본인이 \"약\"으로 안 보는 것까지"],
                      caption="이 점검만으로 약물성 원인을 30–50%에서 찾음"),
    ],
    "related": [
        ("/간경변-간성혼수/", "간성혼수 — 외래에서 알아채는 신호와 일상 관리"),
        ("/간수치-높음/", "건강검진 간수치(AST·ALT) 높음, 첫 단계로 무엇을 봐야 할까"),
        ("/간경변-영양-근감소증/", "간경변 영양·근감소증 — 단백 제한은 옛말입니다"),
    ],
})

# 02-10: 정상수치 함정
ARTICLES.append({
    "slug": "간경변-정상수치-함정",
    "h1": "간기능검사가 정상인데 간경변? — 진행된 간경변의 함정",
    "description": "간기능검사가 정상으로 보이는 간경변이 왜 존재하는지, 영상·섬유화 평가가 왜 필요한지를 정리합니다. \"수치 정상 = 간 건강\"의 오해.",
    "series_slug": "간경화", "series_display": "간경화", "last_crumb": "정상 수치 함정",
    "section_label": "간경화", "about": "잠재 간경변",
    "tldr": "간기능검사(AST·ALT·빌리루빈·알부민)가 \"정상\"이어도 진행된 간경변일 수 있습니다. 간세포가 이미 많이 손상된 단계에서는 오히려 효소가 새로 \"새어 나올 만큼\" 남지 않아 수치가 낮게 측정됩니다. <em>혈소판 감소·INR 상승·영상에서의 간 모양 변화·섬유화 검사</em>가 함께 봐야 하는 이유입니다. 단순 혈액검사 정상으로 안심하지 마세요.",
    "sections": [
        ("왜 간경변에서 수치가 정상으로 나올까",
         "<p>일반인의 직관과 반대 현상이 일어납니다.</p><ul><li>간세포가 손상되면 AST·ALT가 혈액으로 새어 나옴 → 수치 상승</li><li>그러나 진행된 간경변에서는 살아있는 간세포가 줄어들어 \"새어 나올 효소 자체\"가 줄어듦</li><li>결과: 손상은 진행되었는데 수치는 오히려 정상 또는 낮은 정상</li></ul><p>이 \"burnt-out\" 패턴은 특히 알코올성 간경변과 진행된 MASH 간경변에서 흔합니다.</p>"),
        ("어떤 신호가 \"숨은 간경변\"을 의심하게 하나",
         "<p>수치만으로는 안 보이지만 다음이 있다면 의심합니다.</p><ul><li><strong>혈소판 감소</strong> — &lt; 150,000/μL. 비장 비대로 인한 lien-itis. 가장 민감한 1차 신호.</li><li><strong>알부민 감소</strong> — &lt; 3.5 g/dL. 합성능 저하.</li><li><strong>PT/INR 상승</strong> — &gt; 1.1. 응고 인자 합성 저하.</li><li><strong>AST/ALT &gt; 1.5</strong> — 일반적인 간세포 손상에서는 ALT가 더 높지만, 진행된 간경변에서 비율이 역전.</li><li><strong>총 빌리루빈 1.2 이상</strong> — 정상 상한 부근에서도 의미.</li></ul><p>FIB-4 score(나이·AST·ALT·혈소판)가 자동 계산되어 1.30 이하면 안전, 2.67 초과면 진행 간경변 가능성 높음.</p>"),
        ("영상에서 보이는 간경변의 신호",
         "<p>혈액검사가 모호할 때 영상이 결정적입니다.</p><ul><li><strong>초음파</strong> — 간 표면 거칠음, 비대칭 비대(좌엽 비대), 비장 비대, 우회혈관 발달</li><li><strong>CT/MRI</strong> — 결절성 표면, 우엽 위축 + 좌엽·미엽 비대, 비장 비대, 정맥류, 복수</li><li><strong>Fibroscan</strong> — LSM &gt; 12.5 kPa면 간경변 가능성 높음 (원인 질환별로 임계값 다름)</li></ul><p>영상은 한 번 정상이어도 진행된 간경변이 있을 수 있어, 임상 의심이 있으면 추가 평가합니다.</p>"),
        ("누구에서 \"숨은 간경변\"을 더 의심해야 하나",
         "<p>다음 인자가 있으면 적극적 평가가 권장됩니다.</p><ul><li>오랜 음주력 (남성 일주일 14잔, 여성 7잔 이상)</li><li>비만·당뇨·고지혈증의 병발 (특히 50세 이상)</li><li>가족력 (B형간염, 진행된 간질환)</li><li>설명되지 않는 혈소판 감소 또는 비장 비대</li><li>피로·식욕부진·체중감소가 새로 시작</li></ul><p>이 인자가 있는데 단순 \"간수치 정상\"이라는 말만 듣고 추적 없이 지나는 것이 가장 흔한 함정입니다.</p>"),
        ("외래에서 무엇을 추가로 평가하나",
         "<p>의심이 있을 때:</p><ul><li>혈액 — 혈소판, 알부민, PT, 빌리루빈</li><li>FIB-4 자동 계산 (혈액검사로 가능)</li><li>복부 초음파</li><li>Fibroscan 또는 ARFI 같은 비침습 섬유화 검사</li><li>필요 시 CT/MRI</li><li>드물게 간생검</li></ul><p>이 패키지로 진행된 간경변의 약 90%가 진단됩니다. 비침습 검사들이 발달해 간생검의 필요성은 점차 줄어듭니다.</p>"),
    ],
    "faq": [
        ("간수치가 정상이면 안 봐도 되는 거 아닌가요?",
         "<p>아닙니다. 진행된 간경변에서는 살아있는 간세포가 줄어 \"새어 나올 효소 자체\"가 적어지므로 AST·ALT가 오히려 정상 범위로 측정될 수 있습니다(burnt-out cirrhosis 패턴). 알코올성과 진행된 MASH 간경변에서 흔합니다. 위험 인자(오랜 음주력, 비만+당뇨+고지혈증, B/C형 간염, 가족력)가 있는 환자라면 간수치 정상으로 안심하지 말고 추가 평가 — 혈소판·알부민·PT·FIB-4 자동 계산, 복부 초음파, Fibroscan — 가 필요합니다. 단순 \"간수치 정상\"으로 추적 없이 지나는 것이 가장 흔한 임상 함정입니다.</p>"),
        ("FIB-4가 2.0이에요. 위험한가요?",
         "<p>1.30-2.67은 회색지대로, 단독으로 결정짓지 않고 추가 평가가 필요합니다. 다음 단계는 Fibroscan 또는 복부 초음파입니다. Fibroscan에서 8 kPa 미만이면 진행성 섬유화 가능성이 낮고, 12 kPa 이상이면 진행성 섬유화 의심으로 정밀 평가합니다(MASLD 기준). 회색지대 수치도 시간 추이가 중요합니다 — 1년 후 재측정에서 떨어지면 호전, 올라가면 진행을 의미. 동시에 위험 인자(체중·당뇨·음주·B/C형 간염)도 함께 평가합니다.</p>"),
        ("Fibroscan에서 12 kPa이 나왔어요. 간경변인가요?",
         "<p>원인 질환별로 임계값이 다릅니다. MASLD에서는 12 kPa이 진행성 섬유화 의심선(F3 이상 가능)이고, 알코올성에서는 약 17-20 kPa이 간경변 의심, B형간염에서는 11 kPa 이상이 의심선입니다. 단일 값으로 단정하지 말고 임상 — 위험 인자, 영상 소견, 혈액 검사, 임상 증상 — 와 함께 봐야 정확합니다. Fibroscan 검사 자체도 측정 조건(공복 3시간 이상, 안정 자세)에 따라 변동이 있어, 모호한 값은 1-3개월 후 재측정하거나 MRE·간생검을 추가합니다.</p>"),
        ("초음파가 정상이면 간경변이 아닌 거죠?",
         "<p>아닙니다. 초음파의 간경변 진단 민감도는 약 70%로, 초기 간경변에서는 정상으로 보일 수 있습니다. 특히 표면 변화나 비장 비대가 아직 두드러지지 않은 단계에서 초음파만으로는 놓칠 수 있습니다. 의심이 있으면 동적 CT 또는 MRI(특히 Gd-EOB-MRI)를 추가하면 더 민감하며, Fibroscan·MRE 같은 비침습 섬유화 평가가 보완 도구로 쓰입니다. 또한 초음파 시행자의 경험과 환자의 체형(비만·복부 가스)이 결과에 영향을 주므로, 모호한 경우 다른 검사로 보완합니다.</p>"),
        ("혈소판이 130,000인데 검사받아야 하나요?",
         "<p>혈소판 감소가 새로 발견되었거나 다른 위험 인자(음주 이력, 비만+당뇨, B/C형 간염 가족력, 피로·식욕부진 등)가 있으면 평가가 필요합니다. 비장 비대로 인한 lien-itis는 진행 간경변의 가장 민감한 1차 신호이지만, 혈소판 감소의 다른 원인 — 약물(헤파린·일부 항생제), 골수 질환, 면역성 혈소판 감소증, 비타민 결핍 — 도 함께 평가합니다. 일반적으로 복부 초음파, FIB-4 자동 계산, 그리고 혈액 추적(CBC·간기능·영양 상태)을 시작 패키지로 합니다.</p>"),
    ],
    "refs": [
        ("Castera L, Friedrich-Rust M, Loomba R. Noninvasive Assessment of Liver Disease in Patients With Nonalcoholic Fatty Liver Disease. <em>Gastroenterology</em>. 2019;156(5):1264–1281.e4.", "10.1053/j.gastro.2018.12.036", "30660725"),
        ("Berzigotti A, Tsochatzis E, Boursier J, et al. EASL Clinical Practice Guidelines on non-invasive tests for evaluation of liver disease severity and prognosis. <em>J Hepatol</em>. 2021;75(3):659–689.", "10.1016/j.jhep.2021.05.025", "34166721"),
        ("Sterling RK, Lissen E, Clumeck N, et al. Development of a simple noninvasive index to predict significant fibrosis in patients with HIV/HCV coinfection. <em>Hepatology</em>. 2006;43(6):1317–1325.", "10.1002/hep.21178", "16729309"),
        ("D'Amico G, Garcia-Tsao G, Pagliaro L. Natural history and prognostic indicators of survival in cirrhosis: a systematic review of 118 studies. <em>J Hepatol</em>. 2006;44(1):217–231.", "10.1016/j.jhep.2005.10.013", "16298014"),
    ],
    "svgs": [
        svg_table("\"수치 정상 간경변\"의 단서",
                  ["검사", "정상 범위", "간경변 의심 신호"],
                  [["혈소판", "150–400 ×10³", "< 150 (가장 민감)"],
                   ["알부민", "3.5–5.0 g/dL", "< 3.5"],
                   ["PT (INR)", "0.9–1.1", "> 1.1"],
                   ["AST/ALT 비율", "보통 ALT > AST", "AST/ALT > 1.5"],
                   ["FIB-4 (자동 계산)", "<1.30", "≥ 2.67 정밀검사 대상"]],
                  caption="간기능검사(AST·ALT·빌리루빈)가 정상이어도 위 신호 있으면 평가"),
        svg_checklist("진행된 간경변을 더 의심해야 할 인자",
                      ["오랜 음주력 (남 ≥14잔/주, 여 ≥7잔/주)",
                       "비만 + 당뇨 + 고지혈증 동반 (50세 이상)",
                       "B형/C형 간염 가족력",
                       "설명 안 되는 혈소판 감소·비장 비대",
                       "피로·식욕부진·체중 감소가 새로 시작"],
                      caption="이런 인자가 있는데 \"수치 정상\"으로 안심하면 가장 흔한 함정"),
    ],
    "related": [
        ("/간수치-높음/", "건강검진 간수치(AST·ALT) 높음, 첫 단계로 무엇을 봐야 할까"),
        ("/간섬유화스캔-수치/", "Fibroscan(간섬유화 스캔) 수치 읽는 법 — F0부터 F4까지"),
        ("/지방간-정밀검사/", "지방간 진단 후, 섬유화 정밀검사가 필요한 사람은 누구인가"),
    ],
})

# === Build all ===
print(f"Building {len(ARTICLES)} articles...\n")
for spec in ARTICLES:
    render_article(spec)
print("\nDone.")
