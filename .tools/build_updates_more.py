"""Add 10 first-author paper notes + 4 topic review notes to /updates/."""
import sys, os, html as htmllib, re
sys.path.insert(0, os.path.dirname(__file__))
from build_articles import svg_table, svg_checklist, svg_compare_two, svg_flow_arrows, svg_progression_bar
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def esc(s): return htmllib.escape(s or "")

NAV = '''<header class="site-header">
  <div class="inner">
    <a href="/" class="brand-mark">Hepatology<em> Note</em></a>
    <nav class="site-nav">
      <a href="/소개/">소개</a>
      <a href="/연구/">연구</a>
      <a href="/updates/" class="active">Updates</a>
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

UPDATE_STYLE = '''<style>
.cite-banner{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:16px 0 24px;font-size:14px;line-height:1.65}
.cite-banner strong{display:block;font-size:11px;color:var(--muted);letter-spacing:0.08em;margin-bottom:4px}
.cite-banner .extlink{display:inline-block;margin-top:6px;color:var(--accent);font-size:12.5px;text-decoration:none}
.cite-banner .extlink:hover{text-decoration:underline}
.author-badge{display:inline-block;background:var(--accent);color:#fff;font-size:11px;padding:3px 10px;border-radius:99px;letter-spacing:0.05em;font-weight:600;margin-bottom:10px}
.note-section{margin:36px 0}
.note-section h2{font-family:'Times New Roman',Georgia,serif;font-size:20px;letter-spacing:-0.01em;font-weight:600;margin:0 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}
.note-section h2 .label{font-family:Pretendard,sans-serif;display:inline-block;font-size:11px;color:var(--accent);background:var(--accent-soft);padding:2px 8px;border-radius:99px;margin-right:8px;letter-spacing:0.06em;vertical-align:middle;font-weight:600}
.bottom-line{background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:14px 18px;margin:24px 0;font-size:15px;line-height:1.7}
.bottom-line strong{color:var(--accent);display:block;font-size:12px;letter-spacing:0.06em;margin-bottom:4px}
.fig-link-box{background:#fafaf7;border:1px dashed var(--line);border-radius:8px;padding:14px 18px;margin:20px 0;font-size:14px;line-height:1.65;text-align:center}
.fig-link-box a{color:var(--accent);font-weight:600;text-decoration:none}
.fig-link-box a:hover{text-decoration:underline}
.fig-link-box small{display:block;color:var(--muted);font-size:12px;margin-top:4px}
</style>'''

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


def render_note(spec):
    """Render a paper note. spec keys: slug, h1, description, last_crumb, cite, cite_link, author_note (optional),
    tldr, sections [(label, h2_text, body_html_or_svg)], refs, related, fig_link (optional)."""
    slug = spec["slug"]
    h1 = spec["h1"]
    description = spec["description"]
    last_crumb = spec["last_crumb"]
    cite = spec["cite"]
    cite_link = spec["cite_link"]
    author_note = spec.get("author_note", "")
    tldr = spec["tldr"]
    sections = spec["sections"]  # list of (label, h2_text, body_html)
    refs = spec["refs"]
    related = spec.get("related", [])
    fig_link = spec.get("fig_link", "")
    published = "2026-05-09"

    canonical = f"https://drshin.kr/updates/{slug}/"
    related_html = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for u, t in related)
    refs_html = render_refs(refs)

    sections_html = []
    for label, h2_text, body in sections:
        sections_html.append(
            f'<div class="note-section"><h2><span class="label">{esc(label)}</span>{esc(h2_text)}</h2>\n{body}\n</div>'
        )
    body_html = "\n\n".join(sections_html)

    badge_html = f'<span class="author-badge">{esc(author_note)}</span>' if author_note else ''
    fig_link_html = f'<div class="fig-link-box"><a href="{esc(fig_link)}" target="_blank" rel="noopener">출판사 페이지에서 원문 figure 보기 ↗</a><small>저작권상 figure는 직접 게재할 수 없어 링크로 안내드립니다</small></div>' if fig_link else ''

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
<meta property="article:published_time" content="{published}">
<meta property="article:section" content="최신 지견">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=3">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=3">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=3">
<link rel="manifest" href="/site.webmanifest?v=3">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"ScholarlyArticle","@id":"{canonical}#webpage","url":"{canonical}","name":"{esc(h1)}","description":"{esc(description)}","inLanguage":"ko","datePublished":"{published}","author":{{"@id":"https://drshin.kr/#author"}},"isPartOf":{{"@id":"https://drshin.kr/#website"}},"citation":"{esc(cite)}"}},
{{"@type":"Person","@id":"https://drshin.kr/#author","name":"신현재","jobTitle":"서울대학교병원 소화기내과 · 간암센터","worksFor":{{"@type":"Hospital","name":"서울대학교병원","url":"https://www.snuh.org/"}},"image":"https://drshin.kr/assets/img/author/drshin.jpg","url":"https://drshin.kr/소개/"}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},{{"@type":"ListItem","position":2,"name":"최신 지견","item":"https://drshin.kr/updates/"}},{{"@type":"ListItem","position":3,"name":"{esc(last_crumb)}","item":"{canonical}"}}]}}
]}}
</script>
{UPDATE_STYLE}
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="/updates/">최신 지견</a> › <span>{esc(last_crumb)}</span></nav>
<article>
{badge_html}
<h1>{esc(h1)}</h1>

<div class="cite-banner">
<strong>원문</strong>
{cite}
<a href="{cite_link}" class="extlink" target="_blank" rel="noopener">출판사 페이지에서 원문 보기 ↗</a>
</div>

<div class="tldr"><strong>한 문단 요약</strong>{tldr}</div>

{fig_link_html}

{body_html}

{refs_html}

{AUTHOR_BOX}

<aside class="related"><h2>같이 읽으면 좋은 글</h2><ul>{related_html}</ul></aside>

<p class="disclaimer">본 노트는 일반적 의료 정보 제공이며, 진료 결정의 단일 근거가 되지 않습니다.</p>
</article>
</main>

{FOOTER}
</body>
</html>
'''
    out = ROOT / "updates" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: updates/{slug}")


# === 10 First-author papers from CV ===
FIRST_AUTHOR = []

FIRST_AUTHOR.append({
    "slug": "Shin-AI-CT-HCC-CHB-JHep-2025",
    "h1": "AI 영상 바이오마커 — 만성 B형간염 환자의 간세포암 예측",
    "description": "Shin H et al. J Hepatol 2025. CT 기반 영상 바이오마커를 활용한 AI 모델로 만성 B형간염 환자의 간세포암 발생 위험 예측.",
    "last_crumb": "AI CT-based HCC prediction (Shin)",
    "author_note": "본인 1저자 연구",
    "cite": "Shin H, Hur MH, Song BG, et al. AI model using CT-based imaging biomarkers to predict hepatocellular carcinoma in patients with chronic hepatitis B. <em>J Hepatol</em>. 2025;82(6):1080–1088.",
    "cite_link": "https://doi.org/10.1016/j.jhep.2024.12.029",
    "tldr": "만성 B형간염 환자에서 간세포암(HCC) 위험 예측은 임상에서 가장 자주 다루는 결정 중 하나예요. 이 연구는 정기 검진에서 이미 촬영하는 CT 영상의 정량적 바이오마커를 AI 모델로 분석해 개별 환자의 HCC 발생 위험을 예측합니다. 추가 검사 없이 기존 영상 데이터로 위험 계층화가 가능하다는 점이 임상적 의미예요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>만성 B형간염 환자는 평생 HCC 검진이 필요하지만 모든 환자가 같은 위험은 아닙니다. 위험을 잘 분류하면 고위험 환자엔 더 자주, 저위험 환자엔 부담을 줄여 검진 자원을 효율적으로 쓸 수 있어요. 기존 위험 점수(REACH-B, mPAGE-B 등)는 임상·검사 변수만 사용하는데, 영상에서 추가 정보를 끌어낼 수 있을까가 질문입니다.</p>"),
        ("APPROACH", "접근 방식",
         "<p>CT 영상에서 정량적 바이오마커(간 부피·표면 결절성·비장 부피·문맥압 추정 등)를 자동 추출해 AI 모델 학습에 사용합니다. 이런 영상 마커는 사람 눈으로 보는 정성적 판독보다 객관적이고 시간 추세 비교가 쉬워요. 모델은 영상 + 임상 변수를 통합해 개별 환자 위험을 출력합니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>이 모델이 외래에 적용되면 \"이번 검진에서 다음 6개월·1년 위험은 얼마인가\"를 더 정확히 답할 수 있게 됩니다. 다만 외부 검증, 다른 인종·지역으로의 일반화, 임상 워크플로 통합은 후속 연구가 필요해요. AI 영상 바이오마커는 hepatology 임상 결정 지원의 다음 세대로 활발히 연구되고 있는 분야입니다.</p>"),
    ],
    "refs": [
        ("Shin H, Hur MH, Song BG, et al. AI model using CT-based imaging biomarkers to predict hepatocellular carcinoma in patients with chronic hepatitis B. <em>J Hepatol</em>. 2025;82(6):1080–1088.", "10.1016/j.jhep.2024.12.029", "39710148"),
        ("Korean Liver Cancer Association (KLCA), National Cancer Center (NCC). 2022 KLCA-NCC Korea Practice Guidelines for the Management of Hepatocellular Carcinoma. <em>J Liver Cancer</em>. 2023;23(1):1–120.", "10.17998/jlc.2022.11.07", None),
        ("Singal AG, Llovet JM, Yarchoan M, et al. AASLD Practice Guidance on prevention, diagnosis, and treatment of hepatocellular carcinoma. <em>Hepatology</em>. 2023;78(6):1922–1965.", "10.1097/HEP.0000000000000466", "37199193"),
    ],
    "related": [
        ("/B형간염-간암검진/", "B형간염 환자가 6개월마다 간암 검진을 받아야 하는 이유"),
        ("/간암-재발-추적/", "간암 재발 추적 — 첫 5년의 일정"),
    ],
    "fig_link": "https://www.journal-of-hepatology.eu/article/S0168-8278(24)02790-8/fulltext",
})

FIRST_AUTHOR.append({
    "slug": "Ahn-Aspirin-HCC-MASLD-CMH-2026",
    "h1": "아스피린과 MASLD 환자의 간세포암 위험 — 유전 위험 분석 포함",
    "description": "Ahn J, Hur MH, Shin H et al. Clin Mol Hepatol 2026. MASLD 환자에서 아스피린 사용과 HCC 위험의 nationwide cohort + 유전 위험 분석.",
    "last_crumb": "Aspirin & HCC in MASLD (Ahn)",
    "author_note": "본인 공동 1저자 연구",
    "cite": "Ahn J, Hur MH, Shin H, et al. Aspirin and HCC risk in MASLD: Nationwide cohort study with genetic risk analysis. <em>Clin Mol Hepatol</em>. 2026;32(1):339–352.",
    "cite_link": "https://doi.org/10.3350/cmh.2025.0528",
    "tldr": "아스피린의 HCC 예방 효과는 여러 코호트에서 시사됐지만 MASLD 환자에서의 효과는 데이터가 적었어요. 이 연구는 한국 nationwide 코호트에서 MASLD 환자의 아스피린 사용과 HCC 위험을 평가하면서 유전적 위험(PRS)에 따라 효과가 달라지는지를 함께 봤습니다. \"누가 더 이득을 보는가\"의 정밀의학 접근이 핵심이에요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>MASLD는 전 세계에서 가장 흔한 만성 간 질환이고 HCC 발생도 늘어나고 있어요. 아스피린은 저렴하고 광범위하게 사용되는 약물이라 HCC 화학예방 효과가 입증되면 임상 영향이 매우 큽니다. 그러나 출혈 위험이 있어 \"누구에게 권할 것인가\"가 결정적이에요. 유전 위험 점수(PRS)가 효과 예측의 단서가 될 수 있다는 게 이 연구의 가설입니다.</p>"),
        ("APPROACH", "접근 방식",
         "<p>한국 nationwide 코호트에서 MASLD 환자를 추적하며 아스피린 사용군 vs 비사용군의 HCC 발생을 비교합니다. 동시에 다유전자 위험 점수(polygenic risk score)로 환자를 위험 계층으로 나눠 아스피린 효과의 차이를 평가합니다. 교란 변수(연령·성별·동반 질환·다른 약물)는 propensity score 매칭 등으로 보정합니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>HCC 화학예방 약물의 임상 도입에는 \"누구에게 처방할 것인가\"의 정밀화가 필요합니다. 단순 위험-이득 평균이 아니라 환자별 위험 인자(유전·임상)를 반영한 맞춤 결정이 향후 MASLD 진료의 방향이 될 것이에요. 이 연구는 그 방향의 한 갈래로 의미가 있습니다.</p>"),
    ],
    "refs": [
        ("Ahn J, Hur MH, Shin H, et al. Aspirin and HCC risk in MASLD: Nationwide cohort study with genetic risk analysis. <em>Clin Mol Hepatol</em>. 2026;32(1):339–352.", "10.3350/cmh.2025.0528", "41287437"),
        ("Simon TG, Ma Y, Ludvigsson JF, et al. Association Between Aspirin Use and Risk of Hepatocellular Carcinoma. <em>JAMA Oncol</em>. 2018;4(12):1683–1690.", "10.1001/jamaoncol.2018.4154", "30286235"),
    ],
    "related": [
        ("/지방간-간암/", "지방간이 간암으로 가는 길"),
        ("/대사이상지방간-MASLD/", "NAFLD가 MASLD로 바뀐 이유"),
    ],
    "fig_link": "https://www.e-cmh.org/journal/view.php?doi=10.3350/cmh.2025.0528",
})

FIRST_AUTHOR.append({
    "slug": "Chung-SGLT2-Liver-MR-Hepatology-2024",
    "h1": "SGLT2 억제제와 간 합병증 — Mendelian Randomization + 코호트",
    "description": "Chung SW, Moon HS, Shin H et al. Hepatology 2024. SGLT2 억제와 간질환 관련 합병증의 인과관계를 mendelian randomization과 인구 기반 코호트로 분석.",
    "last_crumb": "SGLT2 & liver complications (Chung)",
    "author_note": "본인 공동 1저자 연구",
    "cite": "Chung SW, Moon HS, Shin H, et al. Inhibition of sodium-glucose cotransporter-2 and liver-related complications in individuals with diabetes: A mendelian randomization and population-based cohort study. <em>Hepatology</em>. 2024;80(3):633–648.",
    "cite_link": "https://doi.org/10.1097/HEP.0000000000000837",
    "tldr": "SGLT2 억제제(다파글리플로진·엠파글리플로진 등)는 당뇨·심부전·신장 보호 효과로 잘 알려져 있고, 지방간에도 도움이 된다는 관찰 연구가 누적되고 있어요. 이 연구는 mendelian randomization(유전 변이 기반 인과 추론)과 nationwide 코호트를 결합해 SGLT2 억제와 간 합병증의 인과관계를 평가합니다. 관찰 연구의 교란을 줄이는 강력한 디자인이에요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>관찰 연구는 \"SGLT2 사용자가 간 합병증이 적다\"를 보여주지만 이게 약 자체 효과인지, 처방되는 환자의 특성 때문인지 가리기 어렵습니다(confounding by indication). Mendelian randomization은 SGLT2 표적 유전자 변이를 도구 변수로 사용해 자연 실험처럼 인과를 추정합니다. 코호트와 결합하면 강력한 증거가 돼요.</p>"),
        ("APPROACH", "접근 방식",
         "<p>SLC5A2 유전자(SGLT2 표적) 변이를 도구로 사용해 평생 SGLT2 활성 차이가 간 합병증 발생에 미치는 영향을 추정합니다. 동시에 한국 당뇨 코호트에서 실제 SGLT2 처방군의 간 결과를 분석합니다. 두 접근이 일치하면 인과 신호가 강해집니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>당뇨 동반 MASLD 환자에서 SGLT2 억제제를 1차로 고려하는 임상 흐름의 근거가 강해집니다. 비당뇨 MASLD에서의 효과는 별도 연구가 필요하지만, 당뇨 + MASLD 환자에서는 단순 혈당 조절 외 간 보호 이득이 있는 것으로 임상에 반영됩니다.</p>"),
    ],
    "refs": [
        ("Chung SW, Moon HS, Shin H, et al. Inhibition of sodium-glucose cotransporter-2 and liver-related complications in individuals with diabetes. <em>Hepatology</em>. 2024;80(3):633–648.", "10.1097/HEP.0000000000000837", "38466796"),
        ("Kahl S, Gancheva S, Straßburger K, et al. Empagliflozin Effectively Lowers Liver Fat Content in Well-Controlled Type 2 Diabetes. <em>Diabetes Care</em>. 2020;43(2):298–305.", "10.2337/dc19-0641", "31540903"),
    ],
    "related": [
        ("/지방간-SGLT2-GLP1/", "SGLT2·GLP-1 작용제와 지방간"),
        ("/지방간-신약-resmetirom/", "지방간 신약 — resmetirom과 다음 세대"),
    ],
    "fig_link": "https://journals.lww.com/hep/abstract/2024/09000/inhibition_of_sodium_glucose_cotransporter_2_and.10.aspx",
})

FIRST_AUTHOR.append({
    "slug": "Shin-Antiviral-CV-CHB-JMV-2024",
    "h1": "B형간염 항바이러스제의 대사 효과와 심혈관 위험",
    "description": "Shin H et al. J Med Virol 2024. 만성 B형간염 환자에서 항바이러스제의 대사 효과·심혈관 위험 비교 분석.",
    "last_crumb": "Antiviral CV risk in CHB (Shin)",
    "author_note": "본인 1저자 연구",
    "cite": "Shin H, Lim GS, Yoon JW, et al. Metabolic Effects and Cardiovascular Disease Risks of Antiviral Treatments in Patients with Chronic Hepatitis B. <em>J Med Virol</em>. 2024;96(7):e29760.",
    "cite_link": "https://doi.org/10.1002/jmv.29760",
    "tldr": "B형간염 항바이러스제(TDF·TAF·ETV)는 평생 복용이 일반적이라 약물 자체의 장기 대사·심혈관 영향이 임상적으로 중요해요. 특히 TDF는 신·골 부담 외에도 일부 대사 변화가 보고되어 왔고, TAF는 다른 패턴을 보입니다. 이 연구는 한국 환자에서 항바이러스제 종류별 대사 변화와 심혈관 위험을 비교 분석합니다.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>B형간염은 평생 항바이러스제를 복용하는 만성 질환이라 약물의 비-간 외 영향이 누적됩니다. TDF는 일부 환자에서 LDL 콜레스테롤 감소·체중 감소가 보고되는 반면, TAF는 그런 효과가 적거나 반대 방향이라는 데이터가 있어 임상에서 약 선택에 영향을 줄 수 있어요.</p>"),
        ("APPROACH", "접근 방식",
         "<p>한국 환자 코호트에서 항바이러스제 종류별 대사 지표(지질·체중·혈당·혈압) 변화와 심혈관 사건(심근경색·뇌졸중·심부전 등) 발생률을 비교합니다. 약 시작 전후 변화와 약 종류별 차이를 분석합니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>항바이러스제 선택 시 효과·신·골 외에도 대사·심혈관 영향을 고려해야 한다는 근거가 되며, 환자별 동반 질환에 따른 약 선택의 정밀화에 기여합니다. TDF→TAF 전환 결정에도 영향을 줄 수 있어요.</p>"),
    ],
    "refs": [
        ("Shin H, Lim GS, Yoon JW, et al. Metabolic Effects and Cardiovascular Disease Risks of Antiviral Treatments in Patients with Chronic Hepatitis B. <em>J Med Virol</em>. 2024;96(7):e29760.", "10.1002/jmv.29760", "38940453"),
    ],
    "related": [
        ("/B형간염-항바이러스제-비교/", "항바이러스제 비교 — TDF · TAF · ETV"),
        ("/B형간염-평생약/", "B형간염 약을 평생 먹어야 하나"),
    ],
    "fig_link": "https://onlinelibrary.wiley.com/doi/10.1002/jmv.29760",
})

FIRST_AUTHOR.append({
    "slug": "Shin-HBeAg-seroclearance-HCC-JHepR-2024",
    "h1": "조기 HBeAg 혈청전환과 HCC·간경변 위험의 연관성 부재",
    "description": "Shin H et al. JHEP Rep 2024. 치료 중 조기 HBeAg 혈청전환과 HCC/비대상성 간경변 발생의 연관성 분석.",
    "last_crumb": "Early HBeAg seroclearance (Shin)",
    "author_note": "본인 1저자 연구",
    "cite": "Shin H, Choi WM, Kim SU, et al. Lack of Association between Early On-Treatment HBeAg-Seroclearance and Development of Hepatocellular Carcinoma or Decompensated Liver Cirrhosis. <em>JHEP Rep</em>. 2024;6(7):101089.",
    "cite_link": "https://doi.org/10.1016/j.jhepr.2024.101089",
    "tldr": "HBeAg 혈청전환은 B형간염 치료의 좋은 신호로 여겨지지만, 치료 \"중\"에 일찍 일어난 혈청전환이 장기 임상 결과(HCC·비대상성)와 직접 연관되는지는 확실하지 않았어요. 이 연구는 다국가 코호트에서 조기 혈청전환 vs 비전환 환자의 HCC·비대상성 발생을 비교했고, 의미 있는 차이가 없음을 보고했습니다. \"혈청전환 = 안전\"으로 단정할 수 없다는 임상 메시지에요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>HBeAg 혈청전환은 B형간염 치료 효과의 marker로 사용되며 일부에서 \"치료 중단 검토 가능\"의 신호로도 해석됩니다. 그러나 진행된 간 손상이 이미 있는 환자에서 단순 혈청전환만으로 HCC·간경변 위험이 의미 있게 줄어드는지는 데이터가 일관적이지 않았어요.</p>"),
        ("APPROACH", "접근 방식",
         "<p>여러 센터의 만성 B형간염 환자 코호트에서 치료 시작 후 일정 시점(예: 2-3년) 내 HBeAg 혈청전환이 일어난 그룹 vs 비전환 그룹의 장기 HCC·비대상성 간경변 발생률을 비교합니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>조기 HBeAg 혈청전환만 보고 추적 강도를 늦추면 안 된다는 것이 임상 메시지입니다. 항바이러스제 유지·간세포암 검진·합병증 평가는 혈청전환 여부와 무관하게 가이드라인에 따라 지속해야 합니다.</p>"),
    ],
    "refs": [
        ("Shin H, Choi WM, Kim SU, et al. Lack of Association between Early On-Treatment HBeAg-Seroclearance and Development of Hepatocellular Carcinoma or Decompensated Liver Cirrhosis. <em>JHEP Rep</em>. 2024;6(7):101089.", "10.1016/j.jhepr.2024.101089", "38974365"),
    ],
    "related": [
        ("/B형간염-HBeAg-양성-음성/", "HBeAg 양성 vs 음성 — 무엇이 다른가"),
        ("/B형간염-검사결과/", "B형간염 검사 결과지 해석"),
    ],
    "fig_link": "https://www.jhep-reports.eu/article/S2589-5559(24)00118-7/fulltext",
})

FIRST_AUTHOR.append({
    "slug": "Shin-COVID-HBV-NK-IN-2023",
    "h1": "COVID-19 백신 접종 후 NK 세포 변화와 HBsAg 일시적 감소",
    "description": "Shin H et al. Immune Netw 2023. COVID-19 백신 접종이 만성 B형간염 환자의 NK 세포 동태와 HBsAg 농도에 미치는 영향.",
    "last_crumb": "COVID vaccine & HBsAg (Shin)",
    "author_note": "본인 1저자 연구",
    "cite": "Shin H, Lee HS, Noh JY, et al. COVID-19 Vaccination Alters NK Cell Dynamics and Transiently Reduces HBsAg Titers Among Patients With Chronic Hepatitis B. <em>Immune Netw</em>. 2023;23(5):e39.",
    "cite_link": "https://doi.org/10.4110/in.2023.23.e39",
    "tldr": "흥미로운 발견이에요. COVID-19 백신 접종이 만성 B형간염 환자의 NK 세포 동태를 변화시키고 HBsAg 농도를 일시적으로 줄였습니다. \"감염성 자극\"이 면역체계를 흔들어 잠복 바이러스 표지자에 영향을 줄 수 있다는 가설을 뒷받침하는 데이터입니다. 향후 면역 매개 functional cure 전략 개발에 단서가 될 수 있어요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>B형간염 functional cure(HBsAg 소실)는 현재 표준 치료로 도달률이 낮은데, 면역체계를 자극하면 도달률을 높일 수 있다는 가설이 있어요. COVID-19 백신은 mRNA 또는 단백 기반의 강력한 면역 자극이라, 우연한 \"자연 실험\"으로 면역과 HBV 표지자의 관계를 볼 기회가 됐습니다.</p>"),
        ("APPROACH", "접근 방식",
         "<p>COVID-19 백신 접종 전후로 만성 B형간염 환자의 NK 세포 표현형(CD56·CD16 등) 변화와 HBsAg 정량(quant) 변화를 추적합니다. 일반 인구의 백신 접종 후 면역 변화와 비교해 HBV 환자에서의 특이성을 확인합니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>HBsAg 감소가 일시적이지만 면역 매개로 일어났다는 점이 의미 있어요. 면역조절제(TLR 작용제, 면역체크포인트 억제 등)가 HBV functional cure 임상시험에서 활발히 연구 중인 배경과 연결됩니다. 다만 임상에서 \"COVID 백신으로 B형간염을 치료한다\"는 결론은 아니에요 — 표지자 변화의 일시성과 임상 중요성은 별개입니다.</p>"),
    ],
    "refs": [
        ("Shin H, Lee HS, Noh JY, et al. COVID-19 Vaccination Alters NK Cell Dynamics and Transiently Reduces HBsAg Titers Among Patients With Chronic Hepatitis B. <em>Immune Netw</em>. 2023;23(5):e39.", "10.4110/in.2023.23.e39", "37970236"),
    ],
    "related": [
        ("/B형간염-functional-cure/", "B형간염 functional cure — 어디까지 와 있나"),
        ("/B형간염-백신/", "B형간염 백신 — 누가, 언제, 몇 번"),
    ],
    "fig_link": "https://immunenetwork.org/DOIx.php?id=10.4110/in.2023.23.e39",
})

FIRST_AUTHOR.append({
    "slug": "Shin-CIK-HCC-CII-2026",
    "h1": "보조 CIK 면역치료의 9년 장기 추적 — HCC RCT 후속 데이터",
    "description": "Shin H et al. Cancer Immunol Immunother 2026. 간세포암 보조 CIK(cytokine-induced killer) 면역치료 RCT의 9년 연장 추적과 실세계 데이터.",
    "last_crumb": "CIK adjuvant in HCC (Shin)",
    "author_note": "본인 1저자 연구",
    "cite": "Shin H, Park Y, Song BG, et al. Adjuvant cytokine-induced killer cell immunotherapy in hepatocellular carcinoma: real-world data and 9-year extended follow-up of a randomized controlled trial. <em>Cancer Immunol Immunother</em>. 2026;75(2):55.",
    "cite_link": "https://doi.org/10.1007/s00262-026-04301-6",
    "tldr": "한국에서 개발·임상 적용된 CIK(cytokine-induced killer) 보조 면역치료의 장기 효과 데이터예요. 2014년 Lee 등이 보고한 phase 3 RCT의 9년 연장 추적과 실세계 데이터를 결합해 장기 재발·생존을 분석합니다. 한국에서 CIK가 임상 적용된 배경과 후속 면역치료 시대(atezo+bev) 와의 위치 정립에 기여하는 연구입니다.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>간세포암 근치 치료(절제·소작) 후 보조 면역치료의 효과는 오랫동안 미답의 영역이었어요. 2014년 한국에서 시행된 CIK 보조요법 phase 3 RCT(Lee et al)에서 무재발 생존 개선이 보고되며 한국 임상에 도입되었습니다. 그러나 IMbrave050(atezo+bev 보조) 시험 등 새로운 면역치료 보조요법이 등장하면서 CIK의 위치가 재정립이 필요한 시점입니다.</p>"),
        ("APPROACH", "접근 방식",
         "<p>원래 RCT 환자들의 9년 시점 장기 추적 데이터와 한국 실세계 cohort의 CIK 사용 환자 데이터를 결합해 재발·전체 생존·안전성을 평가합니다. 장기 추적은 CIK 효과의 지속성과 후기 안전성을 보여줍니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>CIK는 한국에서 도입·사용된 보조요법으로, 새 면역치료 시대에서 위치를 어떻게 잡을지가 임상 결정의 핵심입니다. 장기 데이터는 환자에게 상담할 때 \"이 치료의 5년·10년 효과\"를 답하는 근거가 되어요. 향후 atezo+bev 등과의 비교, 환자 선택 기준 정립이 후속 연구 과제입니다.</p>"),
    ],
    "refs": [
        ("Shin H, Park Y, Song BG, et al. Adjuvant cytokine-induced killer cell immunotherapy in hepatocellular carcinoma: real-world data and 9-year extended follow-up of a randomized controlled trial. <em>Cancer Immunol Immunother</em>. 2026;75(2):55.", "10.1007/s00262-026-04301-6", "41591582"),
        ("Lee JH, Lee JH, Lim YS, et al. Adjuvant immunotherapy with autologous cytokine-induced killer cells for hepatocellular carcinoma. <em>Gastroenterology</em>. 2015;148(7):1383–1391.", "10.1053/j.gastro.2015.02.055", "25747273"),
    ],
    "related": [
        ("/간암-면역치료-1차/", "면역치료 1차 시대 — atezo+bev과 그 이후"),
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선 — 선택의 기준"),
        ("/간암-재발-추적/", "간암 재발 추적 — 첫 5년의 일정"),
    ],
    "fig_link": "https://link.springer.com/article/10.1007/s00262-026-04301-6",
})

FIRST_AUTHOR.append({
    "slug": "Shin-TDF-ETV-TAF-switch-HCC-HepRes-2024",
    "h1": "TDF·ETV에서 TAF로 전환 시 간세포암 위험 — 다기관 코호트",
    "description": "Shin H et al. Hepatol Res 2024. 근치 치료 후 TDF/ETV에서 TAF로 전환한 환자의 HCC 발생 위험 다기관 분석.",
    "last_crumb": "TDF/ETV → TAF and HCC (Shin)",
    "author_note": "본인 1저자 연구",
    "cite": "Shin H, Kim SU, Song BG, et al. Risk of hepatocellular carcinoma after curative treatment when switching from tenofovir disoproxil fumarate or entecavir to tenofovir alafenamide: a real-world multicenter cohort study. <em>Hepatol Res</em>. 2024;54(7):627–637.",
    "cite_link": "https://doi.org/10.1111/hepr.14021",
    "tldr": "TDF에서 TAF로 전환은 신·골 부담을 줄이기 위해 임상에서 자주 결정되는 변경입니다. 그런데 일부 연구에서 TDF 사용자 vs TAF 사용자의 HCC 위험이 다를 수 있다는 시사가 있었어요. 이 연구는 간암 근치 치료 후 항바이러스제를 전환한 환자에서 HCC 재발 위험이 어떻게 달라지는지를 다기관 코호트로 평가합니다.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>TDF에서 TAF로의 전환은 신·골 부담을 줄이려는 임상적 결정이지만, 일부 후향 연구에서 TDF 사용자의 HCC 위험이 더 낮을 가능성을 시사한 데이터가 있었어요. 이 \"TAF 전환이 HCC 위험을 높이는가\"는 환자에게 매일 답해야 하는 질문이 되었습니다. 특히 이미 간세포암 치료를 받은 고위험 환자에서 결정이 더 중요해요.</p>"),
        ("APPROACH", "접근 방식",
         "<p>한국 다기관 코호트에서 간세포암 근치 치료(절제·소작·이식) 후 TDF 또는 ETV로 치료 중이던 환자가 TAF로 전환한 그룹과 그대로 유지한 그룹을 비교해 HCC 재발 위험을 분석합니다. Propensity score 매칭 등으로 환자 특성 차이를 보정합니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>TAF 전환을 결정할 때 신·골 부담 감소의 이득과 잠재적 HCC 재발 위험을 함께 평가해야 한다는 임상 메시지가 됩니다. 환자별 위험 인자(연령, 신기능, 골밀도, 종양 위험)를 종합한 결정이 권장됩니다.</p>"),
    ],
    "refs": [
        ("Shin H, Kim SU, Song BG, et al. Risk of hepatocellular carcinoma after curative treatment when switching from tenofovir disoproxil fumarate or entecavir to tenofovir alafenamide: a real-world multicenter cohort study. <em>Hepatol Res</em>. 2024;54(7):627–637.", "10.1111/hepr.14021", "38300711"),
    ],
    "related": [
        ("/B형간염-항바이러스제-비교/", "항바이러스제 비교 — TDF · TAF · ETV"),
        ("/간암-재발-추적/", "간암 재발 추적 — 첫 5년의 일정"),
    ],
    "fig_link": "https://onlinelibrary.wiley.com/doi/10.1111/hepr.14021",
})

FIRST_AUTHOR.append({
    "slug": "Shin-ETV-TAF-RCT-GnL-2026",
    "h1": "ETV에서 TAF로 — 한국 다기관 RCT의 효능과 안전성",
    "description": "Shin H et al. Gut Liver 2026. 만성 B형간염 환자에서 엔테카비르(ETV)에서 TAF로의 전환 효과와 안전성을 평가한 한국 다기관 RCT.",
    "last_crumb": "ETV → TAF RCT (Shin)",
    "author_note": "본인 1저자 연구",
    "cite": "Shin H, Hur MH, Baek YH, et al. Efficacy and Safety of Switching from Entecavir to Tenofovir Alafenamide in Chronic Hepatitis B: A Multicenter Randomized Trial in Korea. <em>Gut and Liver</em>. 2026 (ahead of print).",
    "cite_link": "https://doi.org/10.5009/gnl250479",
    "tldr": "엔테카비르(ETV)는 강력한 효과로 한국에서 오래 1선 약물로 사용되어 왔는데, 신부전·골다공증·약물 상호작용 등으로 TAF로 전환을 고려하는 환자가 늘었습니다. \"전환해도 효과는 유지되는가?\"가 임상 질문이고, 이 연구는 한국 다기관 RCT로 이를 평가합니다. 후향 코호트가 아닌 randomized 설계라 인과적 결론에 더 가까워요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>ETV는 효과가 강력하지만 공복 복용 필요·라미부딘 내성에 약한 단점이 있어요. TAF는 식사 무관 복용·신·골 안전성 향상이 강점이지만 ETV에서 TAF로의 전환 효과는 RCT 데이터가 적었습니다. 후향 데이터는 일관적이지 않아 명확한 답이 필요했어요.</p>"),
        ("APPROACH", "접근 방식",
         "<p>한국 여러 의료기관에서 안정적으로 ETV 치료 중인 만성 B형간염 환자를 무작위로 ETV 유지 vs TAF 전환으로 배정하고 일정 기간 추적합니다. 1차 평가지표는 바이러스 억제 유지(HBV DNA 불검출), 2차는 ALT·신기능·골밀도·지질 등 안전성 지표예요.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>RCT 결과는 임상 권고를 만드는 가장 강력한 근거입니다. 전환의 효과·안전성이 확인되면 \"왜 ETV에서 TAF로 바꿔야 하는가\"의 결정이 더 명확해지고, 환자별 위험 인자(신기능·골밀도·복용 편의)에 따른 맞춤 결정이 가능해집니다.</p>"),
    ],
    "refs": [
        ("Shin H, Hur MH, Baek YH, et al. Efficacy and Safety of Switching from Entecavir to Tenofovir Alafenamide in Chronic Hepatitis B: A Multicenter Randomized Trial in Korea. <em>Gut and Liver</em>. 2026 (ahead of print).", "10.5009/gnl250479", "42015653"),
    ],
    "related": [
        ("/B형간염-항바이러스제-비교/", "항바이러스제 비교 — TDF · TAF · ETV"),
        ("/B형간염-평생약/", "B형간염 약을 평생 먹어야 하나"),
    ],
    "fig_link": "https://www.gutnliver.org/journal/view.html?doi=10.5009/gnl250479",
})

FIRST_AUTHOR.append({
    "slug": "Shin-HCC-Guidelines-Review-JLC-2025",
    "h1": "간세포암 글로벌 가이드라인 종합 정리 (2017-2024)",
    "description": "Shin H, Yu SJ. J Liver Cancer 2025. 2017-2024년 사이 발표된 주요 HCC 관리 가이드라인을 종합 비교한 review.",
    "last_crumb": "HCC global guidelines (Shin)",
    "author_note": "본인 1저자 review",
    "cite": "Shin H, Yu SJ. A concise review of updated global guidelines for the management of hepatocellular carcinoma: 2017-2024. <em>J Liver Cancer</em>. 2025;25(1):19–30.",
    "cite_link": "https://doi.org/10.17998/jlc.2025.02.03",
    "tldr": "최근 7년 동안 HCC 관리 가이드라인이 크게 업데이트되었어요. KLCA-NCC, AASLD, EASL, APASL 각 가이드라인의 진단·치료·검진 권고가 어떻게 진화했고 서로 어떻게 다른지를 정리한 review입니다. 임상 현장에서 \"어느 가이드라인을 따라야 하나\"의 혼란을 줄이는 데 도움이 됩니다.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>HCC는 면역치료 도입(IMbrave150 2020), BCLC 업데이트(2022), 새 진단 기준 등 큰 변화가 있어 가이드라인이 자주 바뀌었습니다. 한국·미국·유럽·아시아 가이드라인은 일부 일치하지만 일부 권고는 다르게 정리되어 있어 임상의가 \"무엇을 따를지\"가 헷갈릴 수 있어요.</p>"),
        ("APPROACH", "접근 방식",
         "<p>2017년 이후 발표·업데이트된 주요 가이드라인(KLCA-NCC 2022, AASLD 2023, EASL 2018, APASL 2017+update 등)을 진단·치료·검진 영역으로 나눠 비교합니다. 일치하는 권고와 다른 권고를 표로 정리하고, 차이의 임상적 의미를 논의합니다.</p>"),
        ("KEY POINT", "임상 함의",
         "<p>한국 환자에게는 KLCA-NCC가 1차 참고이지만, 다국적 임상시험·국제 학회 참여·해외 협진 시 다른 가이드라인 비교가 필요합니다. Review 논문은 이 비교를 빠르게 할 수 있는 reference가 되어 후속 임상 결정·연구 설계에 유용합니다.</p>"),
    ],
    "refs": [
        ("Shin H, Yu SJ. A concise review of updated global guidelines for the management of hepatocellular carcinoma: 2017-2024. <em>J Liver Cancer</em>. 2025;25(1):19–30.", "10.17998/jlc.2025.02.03", "39925090"),
    ],
    "related": [
        ("/간암-BCLC병기/", "BCLC 병기와 치료 옵션"),
        ("/간암-진단-첫외래/", "간암 진단을 받았을 때, 첫 외래에서 결정되는 것"),
        ("/간암-치료-선택/", "절제술 vs 색전술 vs 방사선"),
    ],
    "fig_link": "https://www.jlc.or.kr/journal/view.html?doi=10.17998/jlc.2025.02.03",
})

# === 4 Topic review notes ===
TOPICS = []

TOPICS.append({
    "slug": "PEth-알코올-바이오마커",
    "h1": "PEth (phosphatidylethanol) — 알코올 바이오마커의 새로운 표준",
    "description": "PEth(phosphatidylethanol)는 최근 임상에서 활용이 늘고 있는 알코올 섭취 객관적 바이오마커입니다. 검출 기간·민감도·임상 활용을 정리합니다.",
    "last_crumb": "PEth — alcohol biomarker",
    "cite": "Helander A, Hansson T. National harmonization of the alcohol biomarker PEth. <em>Lakartidningen</em>. 2013. (and multiple subsequent reviews)",
    "cite_link": "https://pubmed.ncbi.nlm.nih.gov/?term=phosphatidylethanol+alcohol+biomarker",
    "tldr": "환자가 \"술 안 마셨어요\"라고 하지만 임상이 의심될 때 객관적 평가가 필요해요. 기존 마커(GGT·AST/ALT 비율·MCV·CDT)는 민감도·특이도에 한계가 있는데, <em>PEth(phosphatidylethanol)</em>는 알코올 섭취 후 적혈구막에 형성되는 인지질로 약 2-3주 동안 검출되어 \"최근 음주\"의 객관적 지표가 됩니다. 알코올성 간 질환 진단·간이식 전 음주 평가·자가면역간염 감별 등에 활용도가 점차 확대되고 있어요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>알코올 섭취량 평가의 정확성은 임상에서 매우 중요합니다 — MASLD vs ALD 감별, MetALD 분류, 간이식 적응(6개월 금주 평가), 음주 재발 모니터링. 그러나 환자 자가 보고는 흔히 부정확해요. 기존 객관적 마커는 한계가 있습니다 — GGT는 비특이적, CDT는 일부 비음주 상황에서도 변동, MCV는 변화가 늦어 최근 음주 평가에 부적합.</p>"),
        ("APPROACH", "어떻게 측정하나",
         "<p>PEth는 알코올 섭취 후 적혈구막의 phosphatidylcholine이 ethanol과 반응해 형성되는 비정상 인지질입니다. 적혈구 수명에 따라 약 2-3주 동안 혈중에 존재해 \"최근 2-3주 음주\"의 객관적 지표가 됩니다. 16:0/18:1 PEth가 가장 흔히 측정되는 동족체이고, LC-MS/MS로 정량합니다.</p>"),
        ("FINDINGS", "임계값과 해석",
         "<p>일반적인 cutoff:</p>" + svg_progression_bar(
             [("< 20 ng/mL", "음주 X 또는 미량"),
              ("20-200", "경증·중등도 음주"),
              ("> 200", "유의미한 음주"),
              ("> 800", "과음 가능")],
             title="PEth 농도 해석 (16:0/18:1)",
             caption=""
         ) + "<p>다만 cutoff은 검사실·연구마다 약간씩 다를 수 있어 임상 적용 시 본인 의료기관 기준을 확인하세요. 위양성·위음성 가능성도 있어 단독 결정보다 임상 전체 그림과 함께 평가합니다.</p>"),
        ("CRITIQUE", "한계와 주의",
         "<ul><li>적혈구 관련 질환(빈혈·용혈·다혈증)에서 결과 해석에 영향 가능</li><li>PEth 형성에 개인차가 있어 같은 음주량에도 사람마다 다른 수치</li><li>한국에서 임상 검사로 가용한 의료기관이 제한적</li><li>비용·접근성 문제로 모든 환자에 일상적 시행은 어려움</li></ul>"),
        ("KEY POINT", "임상 활용",
         "<p>한국에서 PEth 검사 도입이 점차 확대되고 있고, 알코올성 간 질환·간이식 평가·자가면역간염 감별 등 객관적 음주 평가가 결정적인 임상 상황에서 활용됩니다. 환자에게 \"객관적으로 측정해서 평가하겠다\"는 메시지가 자가 보고의 정확성도 높여요.</p>"),
    ],
    "refs": [
        ("Helander A, Hansson T. National harmonization of the alcohol biomarker PEth. Multiple subsequent reviews and clinical guidelines.", None, None),
        ("Andresen-Streichert H, Müller A, Glahn A, Skopp G, Sterneck M. Alcohol Biomarkers in Clinical and Forensic Contexts. <em>Dtsch Arztebl Int</em>. 2018;115(18):309–315.", "10.3238/arztebl.2018.0309", "29807559"),
        ("Niemelä O. Biomarker-Based Approaches for Assessing Alcohol Use Disorders. <em>Int J Environ Res Public Health</em>. 2016;13(2):166.", "10.3390/ijerph13020166", "26828506"),
    ],
    "related": [
        ("/대사이상지방간-MASLD/", "NAFLD가 MASLD로 바뀐 이유"),
        ("/술-안마셔도-지방간/", "술 안 마시는데 지방간"),
        ("/간경변-약물-주의/", "간경변 환자가 피해야 할 약·영양제"),
    ],
})

TOPICS.append({
    "slug": "preemptive-TIPS-식도정맥류-출혈",
    "h1": "Preemptive TIPS — 식도정맥류 출혈의 조기 개입",
    "description": "Preemptive(early) TIPS는 고위험 정맥류 출혈 환자에서 표준 약물·내시경 치료보다 24-72시간 내 시행 시 사망률을 줄인 패러다임 변화입니다.",
    "last_crumb": "Preemptive TIPS",
    "cite": "García-Pagán JC, Caca K, Bureau C, et al. Early use of TIPS in patients with cirrhosis and variceal bleeding. <em>N Engl J Med</em>. 2010;362(25):2370–2379.",
    "cite_link": "https://www.nejm.org/doi/full/10.1056/NEJMoa0910102",
    "tldr": "식도정맥류 출혈은 간경변 환자의 가장 위험한 합병증 중 하나로 6주 사망률이 약 15-20%였어요. 2010년 García-Pagán NEJM 연구가 \"고위험 환자에서 출혈 24-72시간 내 preemptive TIPS\"를 시행하면 표준 치료(약물 + 내시경)보다 사망률을 의미 있게 줄인다는 것을 보였습니다. Baveno VI(2015)·VII(2022) 합의에 반영되어 표준 치료의 일부가 되었어요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>식도정맥류 출혈의 표준 치료는 vasoactive 약물(테르리프레신·옥트레오타이드) + 응급 내시경 결찰 + 예방적 항생제 + 적정 수혈입니다. 그러나 고위험 환자(Child-Pugh C 또는 Child B + 활동성 출혈)에서는 표준 치료에도 6주 사망률이 30-50%로 매우 높았어요. \"더 일찍·더 적극적으로 개입할 수 있을까\"가 문제였습니다.</p>"),
        ("APPROACH", "Preemptive TIPS의 개념",
         "<p>TIPS(transjugular intrahepatic portosystemic shunt)는 간 안에 인공 단락을 만들어 문맥압을 낮추는 시술입니다. \"Preemptive\" 또는 \"early\" TIPS는 출혈이 잡힌 후 표준 2차 예방을 시작하는 게 아니라, <em>고위험 환자에서 출혈 후 24-72시간 내</em> 선제적으로 TIPS를 시행하는 전략이에요.</p>" + svg_flow_arrows(
             [("출혈 발생", "응급실", "danger"),
              ("표준 치료", "Vasoactive + EVL", "warn"),
              ("고위험 환자", "Child-C·B + 활동성", "warn"),
              ("24-72h 내 TIPS", "Preemptive", "accent"),
              ("사망률 ↓", "~50% 감소", "accent")],
             title="Preemptive TIPS 임상 흐름",
             caption=""
         )),
        ("FINDINGS", "결과",
         "<p>2010년 García-Pagán 시험은 고위험 환자에서 1년 생존을 표준 치료군 61% vs preemptive TIPS군 86%로 보고했어요(p=0.001). 이후 여러 후속 연구·메타분석이 이 효과를 확인했고, Baveno VI(2015) 합의에서 \"고위험 환자에서 preemptive TIPS 권장\"으로 반영되었습니다. Baveno VII(2022)은 환자 선택 기준을 더 정교화했어요.</p>"),
        ("CRITIQUE", "한계와 주의",
         "<ul><li>모든 출혈 환자에게 적용되지 않음 — 환자 선택이 결정적</li><li>TIPS 후 간성혼수 발생 위험 가산</li><li>시술 가용성·전문 인력이 의료기관마다 다름</li><li>고령·심한 동반 질환 환자에서 시술 위험 평가 필요</li><li>한국에서 적용되는 환자는 제한적이며 의료기관별로 도입 정도 다름</li></ul>"),
        ("KEY POINT", "임상 활용",
         "<p>고위험 환자(Child-Pugh C 10-13, 또는 Child B + 활동성 출혈)에서 TIPS 시술 가능한 의료기관이라면 preemptive TIPS를 검토합니다. 시기를 놓치면(72시간 후) 효과가 급감해 시기가 결정적이에요. 한국에서도 일부 대학병원에서 도입되어 있고, 향후 추가 적용 확대가 기대됩니다.</p>"),
    ],
    "refs": [
        ("García-Pagán JC, Caca K, Bureau C, et al. Early use of TIPS in patients with cirrhosis and variceal bleeding. <em>N Engl J Med</em>. 2010;362(25):2370–2379.", "10.1056/NEJMoa0910102", "20573925"),
        ("Lv Y, Zuo L, Zhu X, et al. Identifying optimal candidates for early TIPS among patients with cirrhosis and acute variceal bleeding. <em>Gut</em>. 2019;68(7):1297–1310.", "10.1136/gutjnl-2018-317057", "30415234"),
        ("de Franchis R, Bosch J, Garcia-Tsao G, et al. Baveno VII — Renewing consensus in portal hypertension. <em>J Hepatol</em>. 2022;76(4):959–974.", "10.1016/j.jhep.2021.12.022", "35120736"),
    ],
    "related": [
        ("/간경변-식도정맥류/", "식도정맥류 — 첫 신호와 예방적 결찰"),
        ("/간경변-Child-Pugh-MELD/", "Child-Pugh와 MELD"),
        ("/updates/Baveno-VII-portal-hypertension-J-Hepatol-2022/", "Baveno VII 합의"),
    ],
})

TOPICS.append({
    "slug": "GLP1RA-small-molecule-orforglipron",
    "h1": "GLP-1 RA 경구 small molecule — orforglipron과 차세대 옵션",
    "description": "Orforglipron 등 경구 small molecule GLP-1 RA가 phase 3 임상에서 주사형과 유사한 체중 감량·혈당 조절 효과를 보고하며 비만·당뇨·MASH 치료에 새 옵션이 되고 있습니다.",
    "last_crumb": "Oral GLP-1 RA",
    "cite": "Multiple phase 3 trials in 2024-2025 (NEJM, Lancet) on orforglipron and other oral small-molecule GLP-1 receptor agonists.",
    "cite_link": "https://pubmed.ncbi.nlm.nih.gov/?term=orforglipron",
    "tldr": "GLP-1 작용제(세마글루타이드·티르제파타이드 등)의 효과는 검증됐지만 모두 주사형이라 환자 부담·접근성 한계가 있었어요. <em>Orforglipron</em> 같은 경구 small molecule GLP-1 RA가 2024-2025 phase 3 시험에서 주사형과 비슷한 체중 감량·혈당 조절 효과를 보고하면서 \"매일 먹는 알약\"으로의 패러다임 전환이 가능해지고 있습니다. 비만·2형 당뇨·MASH에 모두 영향을 줄 수 있는 변화예요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>현재 GLP-1 작용제는 모두 펩타이드 기반이라 경구 흡수가 어렵습니다. 유일한 경구 옵션 리벨서스(oral semaglutide)는 흡수율이 매우 낮아 까다로운 복용법(공복·물 한 모금만·30분)이 필요해요. Small molecule GLP-1 RA는 펩타이드가 아닌 화학 합성 분자로 경구 흡수가 자연스럽고 일반 알약처럼 복용 가능합니다.</p>"),
        ("APPROACH", "Orforglipron의 임상 진전",
         "<p>Orforglipron(릴리)은 가장 진전된 small molecule GLP-1 RA로 phase 3 시험(ATTAIN, ACHIEVE 등)에서 비만·2형 당뇨 환자의 체중 감량·당화혈색소 감소를 평가했습니다. 결과는 주사형 세마글루타이드와 비슷한 수준이었어요(약 10-15% 체중 감량). 다른 small molecule(다누글리프론·레프글리프론 등)도 임상 개발 중입니다.</p>"),
        ("FINDINGS", "임상 함의",
         "<p>주사 거부감·복용 편의가 주요 장벽이었던 환자군이 GLP-1 효과를 누릴 수 있게 됩니다. 또한 약가가 주사형보다 낮아질 가능성도 있어 접근성 향상이 기대돼요. MASH에서도 SEMA-NASH·SYNERGY-NASH의 효과가 small molecule로 확장될 가능성이 큽니다.</p>"),
        ("CRITIQUE", "한계와 주의",
         "<ul><li>장기 안전성(특히 갑상선·췌장)은 주사형과 같은 우려가 있어 추적 필요</li><li>한국 도입·보험 적용 시점 미정</li><li>주사형 대비 위장관 부작용 패턴이 다를 수 있음</li><li>매일 복용 부담은 주 1회 주사에 비해 더 클 수 있음</li><li>약물 상호작용 평가가 더 복잡할 가능성</li></ul>"),
        ("KEY POINT", "임상 활용",
         "<p>아직 한국에서 처방 가능한 small molecule GLP-1 RA는 없지만 향후 1-2년 내 도입 가능성이 큽니다. 비만·당뇨·MASH 환자의 약물 옵션 지형이 다시 한 번 변할 수 있어 환자 상담 시 \"향후 옵션\"으로 언급할 가치가 있어요.</p>"),
    ],
    "refs": [
        ("Wharton S, Blevins T, Connery L, et al. Daily Oral GLP-1 Receptor Agonist Orforglipron for Adults with Obesity. <em>N Engl J Med</em>. 2023;389(10):877–888.", "10.1056/NEJMoa2302392", "37356073"),
        ("Frias JP, Hsia S, Eyde S, et al. Efficacy and safety of oral orforglipron in patients with type 2 diabetes. <em>Lancet</em>. 2023;402(10400):472–483.", "10.1016/S0140-6736(23)01302-8", "37369232"),
        ("Newsome PN, Buchholtz K, Cusi K, et al. A Placebo-Controlled Trial of Subcutaneous Semaglutide in NASH. <em>N Engl J Med</em>. 2021;384(12):1113–1124.", "10.1056/NEJMoa2028395", "33185364"),
    ],
    "related": [
        ("/지방간-SGLT2-GLP1/", "SGLT2·GLP-1 작용제와 지방간"),
        ("/지방간-신약-resmetirom/", "지방간 신약 — resmetirom과 다음 세대"),
        ("/updates/Newsome-semaglutide-NASH-NEJM-2021/", "Newsome semaglutide NASH NEJM 2021"),
    ],
})

TOPICS.append({
    "slug": "GLP1RA-알코올성-간질환-ALD",
    "h1": "GLP-1 RA와 알코올성 간 질환 — 새 적응증의 가능성",
    "description": "GLP-1 작용제가 음주 행동·알코올성 간 질환에 미치는 영향이 활발히 연구되고 있습니다. 음주 욕구 감소·간 보호 효과의 가능성과 현재 임상 진전.",
    "last_crumb": "GLP-1 RA in ALD",
    "cite": "Multiple recent trials and observational studies on GLP-1 receptor agonists and alcohol use disorder / alcoholic liver disease.",
    "cite_link": "https://pubmed.ncbi.nlm.nih.gov/?term=GLP-1+alcohol+use+disorder",
    "tldr": "GLP-1 작용제가 음주 행동·알코올성 간 질환에 영향을 줄 수 있다는 데이터가 빠르게 누적되고 있어요. 동물 모델에서 알코올 보상 회로(중뇌 도파민 시스템)에 작용하고, 임상 관찰 연구에서 GLP-1 사용자의 음주 감소·알코올 관련 입원 감소가 보고됩니다. \"비만 약\"이 \"음주 약\"이 될 수 있을지, 알코올성 간 질환의 새 옵션이 될지가 활발한 연구 영역이에요.",
    "sections": [
        ("BACKGROUND", "왜 의미 있는가",
         "<p>알코올 사용 장애·알코올성 간 질환의 약물 치료는 매우 제한적이에요. 디설피람·날트렉손·아캄프로세이트가 있지만 효과·내약성 한계가 있고, 알코올성 간경변 자체의 약물 치료는 사실상 부재합니다. GLP-1 작용제가 \"음주 욕구를 줄이고 간 보호 효과도 있다\"면 두 측면에서 동시에 기여할 수 있어요.</p>"),
        ("APPROACH", "기전과 증거",
         "<p>전임상 연구: 동물 모델에서 GLP-1 작용제가 알코올 자가 투여(self-administration)·선호도를 줄임. 중뇌 도파민(보상 회로)·시상하부(식욕)·인슐린 감수성 등 여러 경로 추정.</p><p>임상 관찰: 비만·당뇨로 GLP-1을 처방받은 환자가 동일 환자군 비사용자 대비 알코올 사용 장애 진단·알코올 관련 입원·간 합병증이 적다는 후향 데이터가 누적 (실세계 데이터 분석, 2023-2025).</p><p>임상시험 진행 중: 알코올 사용 장애·MASH·알코올성 간 질환 환자에서 GLP-1 RA의 효과를 직접 평가하는 RCT가 다수 진행되고 있습니다.</p>"),
        ("FINDINGS", "현재 임상 위치",
         "<p>아직 GLP-1 RA가 알코올 사용 장애·알코올성 간 질환의 적응증으로 승인된 약은 없습니다. 그러나 진행 중인 phase 2/3 시험 결과에 따라 향후 적응증 확대 가능성이 큽니다. 미국 등 일부 국가에서는 off-label 사용 보고가 늘고 있고, MetALD(MASLD + 음주) 환자에서 자연스러운 사용 시나리오가 형성되고 있어요.</p>"),
        ("CRITIQUE", "한계와 주의",
         "<ul><li>현재 임상 적응증 외 사용 — 효과·안전성 데이터 누적 중</li><li>알코올 사용 장애 약물치료의 표준은 여전히 정신건강의학 협진 + 인지행동 치료</li><li>알코올성 간 질환 환자에서 GLP-1 안전성(저혈당·체중 감소·근감소증)은 별도 평가 필요</li><li>음주 자체의 절대 회피·금주 결심이 가장 강력한 개입이라는 기본 원칙 변화 없음</li></ul>"),
        ("KEY POINT", "임상 활용",
         "<p>아직 일상 처방 단계는 아니지만, MetALD 환자(MASLD + 음주)에서 비만·당뇨 적응증으로 GLP-1을 처방하는 경우 부수적 음주 감소·간 보호 효과가 기대됩니다. 향후 1-3년 내 임상시험 결과에 따라 ALD·AUD 적응증 추가 가능성을 추적할 가치가 있어요.</p>"),
    ],
    "refs": [
        ("Wium-Andersen IK, Wium-Andersen MK, Fink-Jensen A, et al. Use of GLP-1 receptor agonists and subsequent risk of alcohol-related events. <em>JAMA Psychiatry</em>. 2025 (and related publications).", None, None),
        ("Klausen MK, Thomsen M, Wortwein G, Fink-Jensen A. The role of glucagon-like peptide 1 (GLP-1) in addictive disorders. <em>Br J Pharmacol</em>. 2022;179(4):625–641.", "10.1111/bph.15677", "34532853"),
        ("Leggio L, Hendershot CS, Farokhnia M, et al. GLP-1 receptor agonists and alcohol use disorder. <em>Nat Rev Gastroenterol Hepatol</em>. 2023.", None, None),
    ],
    "related": [
        ("/지방간-SGLT2-GLP1/", "SGLT2·GLP-1 작용제와 지방간"),
        ("/대사이상지방간-MASLD/", "NAFLD가 MASLD로 바뀐 이유"),
        ("/updates/GLP1RA-small-molecule-orforglipron/", "GLP-1 RA 경구 small molecule"),
    ],
})

ALL = FIRST_AUTHOR + TOPICS

print(f"Building {len(ALL)} new Updates pages ({len(FIRST_AUTHOR)} first-author + {len(TOPICS)} topics)...\n")
for spec in ALL:
    render_note(spec)
print("\nDone.")
