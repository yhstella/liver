"""Updates - 5 new paper notes (J Hepatol·NEJM·Lancet·Gastroenterology·Gut·Hepatology)."""
import sys, os, html as htmllib
sys.path.insert(0, os.path.dirname(__file__))
from build_articles import svg_table, svg_checklist, svg_compare_two
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
svg.fig{display:block;width:100%;height:auto;max-width:720px;margin:20px auto;background:#fff;border:1px solid var(--line);border-radius:8px}
svg.fig text{font-family:"Pretendard","Apple SD Gothic Neo","Noto Sans KR",sans-serif}
.fig-caption{font-size:12.5px;color:var(--muted);text-align:center;margin:-12px 0 24px;letter-spacing:0.01em}
.cite-banner{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:16px 0 24px;font-size:14px;line-height:1.65}
.cite-banner strong{display:block;font-size:11px;color:var(--muted);letter-spacing:0.08em;margin-bottom:4px}
.cite-banner .extlink{display:inline-block;margin-top:6px;color:var(--accent);font-size:12.5px;text-decoration:none}
.cite-banner .extlink:hover{text-decoration:underline}
.note-section{margin:36px 0}
.note-section h2{font-family:'Times New Roman',Georgia,serif;font-size:20px;letter-spacing:-0.01em;font-weight:600;margin:0 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}
.note-section h2 .label{font-family:Pretendard,sans-serif;display:inline-block;font-size:11px;color:var(--accent);background:var(--accent-soft);padding:2px 8px;border-radius:99px;margin-right:8px;letter-spacing:0.06em;vertical-align:middle;font-weight:600}
.bottom-line{background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:0 8px 8px 0;padding:14px 18px;margin:24px 0;font-size:15px;line-height:1.7}
.bottom-line strong{color:var(--accent);display:block;font-size:12px;letter-spacing:0.06em;margin-bottom:4px}
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

def render_update(spec):
    slug = spec["slug"]
    h1 = spec["h1"]
    description = spec["description"]
    last_crumb = spec["last_crumb"]
    cite = spec["cite"]  # full citation text
    cite_link = spec["cite_link"]  # publisher URL
    tldr = spec["tldr"]
    background = spec["background"]
    methods_intro = spec["methods_intro"]
    methods_bullets = spec["methods_bullets"]
    findings_intro = spec["findings_intro"]
    findings_svg = spec["findings_svg"]
    critique = spec["critique"]
    bottom_line = spec["bottom_line"]
    extra_svg = spec.get("extra_svg", "")
    refs = spec["refs"]
    related = spec["related"]
    published = "2026-05-09"

    canonical = f"https://drshin.kr/updates/{slug}/"
    methods_html = "".join(f'<li>{b}</li>' for b in methods_bullets)
    related_html = "".join(f'<li><a href="{esc(u)}">{esc(t)}</a></li>' for u, t in related)

    refs_html = render_refs(refs)

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
<meta property="article:section" content="최신 지견">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"ScholarlyArticle","@id":"{canonical}#webpage","url":"{canonical}","name":"{esc(h1)}","description":"{esc(description)}","inLanguage":"ko","datePublished":"{published}","dateModified":"{published}","author":{{"@id":"https://drshin.kr/#author"}},"isPartOf":{{"@id":"https://drshin.kr/#website"}},"citation":"{esc(cite)}"}},
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
<h1>{esc(h1)}</h1>
<p class="meta">서울대학교병원 소화기내과 · 작성 {published} · 검토 {published}</p>

<div class="cite-banner">
<strong>원문</strong>
{cite}
<a href="{cite_link}" class="extlink" target="_blank" rel="noopener">출판사 페이지에서 원문 보기 ↗</a>
</div>

<div class="tldr"><strong>한 문단 요약</strong>{tldr}</div>

<div class="note-section">
<h2><span class="label">BACKGROUND</span>왜 의미 있는 결과인가</h2>
{background}
</div>

<div class="note-section">
<h2><span class="label">METHODS</span>시험 설계</h2>
{methods_intro}
<ul>{methods_html}</ul>
</div>

<div class="note-section">
<h2><span class="label">FINDINGS</span>핵심 수치</h2>
{findings_intro}
{findings_svg}
{extra_svg}
</div>

<div class="note-section">
<h2><span class="label">CRITIQUE</span>해석할 때 고려할 점</h2>
<ul>
{"".join(f'<li>{c}</li>' for c in critique)}
</ul>
</div>

<div class="bottom-line">
<strong>BOTTOM LINE</strong>
{bottom_line}
</div>

{refs_html}

{AUTHOR_BOX}

<aside class="related"><h2>같이 읽으면 좋은 글</h2><ul>{related_html}</ul></aside>

<p class="disclaimer">본 노트는 일반적 의료 정보 제공이며, 진료 결정의 단일 근거가 되지 않습니다. 개별 환자 적용은 진료 의료진의 판단·해당 기관 가이드라인을 따릅니다.</p>
</article>
</main>

{FOOTER}
</body>
</html>
'''
    out = ROOT / "updates" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: updates/{slug} ({len(html)} bytes)")

UPDATES = []

# 1. IMbrave150
UPDATES.append({
    "slug": "IMbrave150-atezolizumab-bevacizumab-NEJM-2020",
    "h1": "IMbrave150 - atezolizumab+bevacizumab, 진행성 간암 1차 치료의 전환점",
    "description": "Finn SA et al. NEJM 2020. Phase 3 RCT, 501명 진행성 간세포암, atezo+bev이 sorafenib보다 OS·PFS 우월 - 8년간 1차 표준이었던 sorafenib을 교체.",
    "last_crumb": "IMbrave150",
    "cite": "Finn RS, Qin S, Ikeda M, et al. Atezolizumab plus Bevacizumab in Unresectable Hepatocellular Carcinoma. <em>N Engl J Med</em>. 2020;382(20):1894–1905.",
    "cite_link": "https://www.nejm.org/doi/full/10.1056/NEJMoa1915745",
    "tldr": "2020년 NEJM IMbrave150은 진행성 간세포암(BCLC C) 1차 치료의 표준을 sorafenib에서 <em>atezolizumab+bevacizumab</em>으로 바꾼 분기점입니다. 중앙 생존 19.2개월 vs sorafenib 13.4개월(HR 0.58), 객관적 반응률 27% vs 12%로 두 임계값을 모두 만족시켰습니다. 한국 보험에도 도입되어 적응증 환자에서 1차로 사용됩니다.",
    "background": "<p>2007년 sorafenib이 SHARP 시험으로 진행성 HCC 1차에 등록된 이후 8년간 단일 표준이었습니다. 중앙 생존은 약 10–12개월에 머물렀고, 면역치료(nivolumab, pembrolizumab) 단독 시도는 1차에서 sorafenib을 의미 있게 이기지 못했습니다. 면역치료 + 항혈관신생제(VEGF 차단) 조합이 종양 미세환경의 면역억제를 풀 수 있다는 가설로 IMbrave150이 디자인되었습니다.</p>",
    "methods_intro": "<p>다국가, open-label, phase 3 RCT.</p>",
    "methods_bullets": [
        "대상: 치료 경험 없는 진행성·전이성 또는 절제 불가능 HCC",
        "n: 501명 (atezo+bev 336, sorafenib 165, 2:1 배정)",
        "투약: 아테졸리주맙 1200 mg + 베바시주맙 15 mg/kg 3주마다 IV vs sorafenib 400 mg ×2/일 경구",
        "주된 평가지표: 전체 생존(OS), 무진행 생존(PFS) - co-primary",
        "중앙 추적: 8.6개월 (1차 분석), 15.6개월 (업데이트)",
    ],
    "findings_intro": "<p>두 1차 평가지표 모두 atezo+bev이 sorafenib보다 의미 있게 우월했습니다.</p>",
    "findings_svg": svg_table("IMbrave150 핵심 결과",
                              ["", "Atezo + Bev", "Sorafenib", "HR (95% CI)"],
                              [["중앙 OS (월)", "19.2", "13.4", "0.58 (0.42–0.79)"],
                               ["중앙 PFS (월)", "6.9", "4.3", "0.65 (0.53–0.81)"],
                               ["객관적 반응률", "27%", "12%", "p<0.001"],
                               ["완전 반응", "6%", "0%", "—"],
                               ["12개월 생존", "67%", "55%", "—"]],
                              caption="OS·PFS·반응률 모두 일관되게 우월"),
    "extra_svg": svg_checklist("주요 부작용 (≥grade 3)",
                                ["고혈압 - atezo+bev 15% vs sorafenib 12%",
                                 "단백뇨 - 3% vs 1%",
                                 "ALT 상승 - 4% vs 6%",
                                 "변비·설사 - 비슷",
                                 "출혈 - 7% (베바시주맙 위험)"],
                                caption="베바시주맙으로 인한 정맥류 출혈 위험 평가가 시작 전 필수"),
    "critique": [
        "치료 시작 전 정맥류 평가 (내시경) 필수 - 출혈 환자는 STRIDE(HIMALAYA) 대안",
        "Child-Pugh A 환자 대상 - B/C에서의 안전성·효과는 제한적",
        "B형간염 환자가 의미 있게 포함되어 한국 임상에 적용성 높음",
        "OS 이득은 명확하지만 일부 환자에서 면역 매개 부작용으로 중단",
        "후속 SHR-1210+rivoceranib 등 다른 면역+항혈관 조합도 1차로 추가됨",
    ],
    "bottom_line": "진행성 HCC 1차 치료가 8년 만에 바뀌었고, 면역치료 시대를 연 결정적 시험. 한국 임상에서도 출혈 위험·간 기능 평가 후 1차 표준으로 자리잡았습니다. 자세한 임상 적용은 <a href=\"/간암-면역치료-1차/\">면역치료 1차 시대</a> 참조.",
    "refs": [
        ("Finn RS, Qin S, Ikeda M, et al. Atezolizumab plus Bevacizumab in Unresectable Hepatocellular Carcinoma. <em>N Engl J Med</em>. 2020;382(20):1894–1905.", "10.1056/NEJMoa1915745", "32402160"),
        ("Cheng AL, Qin S, Ikeda M, et al. Updated efficacy and safety data from IMbrave150. <em>J Hepatol</em>. 2022;76(4):862–873.", "10.1016/j.jhep.2021.11.030", "34902530"),
        ("Llovet JM, Ricci S, Mazzaferro V, et al. Sorafenib in advanced hepatocellular carcinoma (SHARP). <em>N Engl J Med</em>. 2008;359(4):378–390.", "10.1056/NEJMoa0708857", "18650514"),
        ("Singal AG, Llovet JM, Yarchoan M, et al. AASLD Practice Guidance on prevention, diagnosis, and treatment of hepatocellular carcinoma. <em>Hepatology</em>. 2023;78(6):1922–1965.", "10.1097/HEP.0000000000000466", "37199193"),
        ("Korean Liver Cancer Association (KLCA), National Cancer Center (NCC). 2022 KLCA-NCC Korea Practice Guidelines. <em>J Liver Cancer</em>. 2023;23(1):1–120.", "10.17998/jlc.2022.11.07", None),
    ],
    "related": [
        ("/간암-면역치료-1차/", "면역치료 1차 시대 - atezo+bev과 그 이후"),
        ("/간암-BCLC병기/", "BCLC 병기와 치료 옵션"),
        ("/updates/HIMALAYA-durvalumab-tremelimumab-NEJM-Evid-2022/", "HIMALAYA - durvalumab+tremelimumab"),
    ],
})

# 2. HIMALAYA
UPDATES.append({
    "slug": "HIMALAYA-durvalumab-tremelimumab-NEJM-Evid-2022",
    "h1": "HIMALAYA - durvalumab+tremelimumab(STRIDE), HCC 1차의 두 번째 옵션",
    "description": "Abou-Alfa GK et al. NEJM Evid 2022. Phase 3 RCT, 1171명 진행성 HCC, durva+treme 단회 priming(STRIDE)이 sorafenib보다 OS 우월. 출혈 위험 환자의 atezo+bev 대안.",
    "last_crumb": "HIMALAYA",
    "cite": "Abou-Alfa GK, Lau G, Kudo M, et al. Tremelimumab plus Durvalumab in Unresectable Hepatocellular Carcinoma. <em>NEJM Evid</em>. 2022;1(8):EVIDoa2100070.",
    "cite_link": "https://evidence.nejm.org/doi/full/10.1056/EVIDoa2100070",
    "tldr": "2022년 NEJM Evid에 발표된 HIMALAYA는 진행성 HCC 1차에 <em>durvalumab(PD-L1) + tremelimumab(CTLA-4) 단회 priming</em> (STRIDE 요법)이 sorafenib보다 OS 우월(중앙 16.4 vs 13.8개월)임을 보였습니다. atezo+bev에 비해 베바시주맙 관련 출혈 위험이 없어 정맥류 출혈 이력 환자의 대안이 되었습니다.",
    "background": "<p>IMbrave150 후 atezo+bev이 1차 표준이 되었지만, 베바시주맙으로 인한 정맥류 출혈 위험이 있는 환자에서는 사용이 제한됩니다. 면역체크포인트 단일 또는 PD-(L)1 + CTLA-4 듀얼 차단이 다른 종양에서 효과를 보였고, HCC에서 STRIDE 요법(트레멜리무맙 1회 + 듀발루맙 유지)으로 디자인되었습니다.</p>",
    "methods_intro": "<p>다국가, open-label, phase 3 RCT, 4-arm.</p>",
    "methods_bullets": [
        "대상: 치료 경험 없는 진행성 HCC",
        "n: 1,171명 (STRIDE 393, 듀발루맙 단독 389, sorafenib 389)",
        "STRIDE: 트레멜리무맙 300 mg ×1 + 듀발루맙 1500 mg 4주마다",
        "주된 평가지표: 전체 생존(OS) - STRIDE vs sorafenib non-inferiority → superiority",
        "중앙 추적: 33.2개월 (최종 분석)",
    ],
    "findings_intro": "<p>STRIDE는 sorafenib에 우월, 듀발루맙 단독은 non-inferiority 충족.</p>",
    "findings_svg": svg_table("HIMALAYA 주요 결과",
                              ["", "STRIDE", "Durva 단독", "Sorafenib", "STRIDE vs Sora HR"],
                              [["중앙 OS (월)", "16.4", "16.6", "13.8", "0.78 (0.66–0.92)"],
                               ["객관적 반응률", "20.1%", "17.0%", "5.1%", "—"],
                               ["3년 OS", "30.7%", "24.7%", "20.2%", "—"],
                               ["4년 OS", "25.2%", "19.3%", "15.0%", "—"]],
                              caption="STRIDE의 'long-tail' 4년 생존 25%가 두드러짐"),
    "extra_svg": svg_compare_two("STRIDE의 강점",
                                  ["베바시주맙 없음 - 출혈 환자 가능",
                                   "트레멜리무맙 1회 - 면역 부작용 누적 적음",
                                   "유지요법 단순 (4주마다 1회 IV)",
                                   "장기 생존 'tail' 효과 명확"],
                                  "주의 사항",
                                  ["면역 매개 부작용 - 어느 장기든 가능",
                                   "병합 면역치료 누적 위험",
                                   "Child-Pugh A 환자 대상 데이터",
                                   "비용·접근성 (한국 보험 진행 중)"],
                                  caption="atezo+bev과 직접 비교 RCT는 없음 - 환자별 선택"),
    "critique": [
        "atezo+bev과 직접 비교 시험 부재",
        "Child-Pugh A 대상 - B/C에서 안전성 미평가",
        "트레멜리무mab 1회만 사용해 부작용 부담은 듀얼 면역 대비 적음",
        "ORR(20%)이 atezo+bev(27%)보다 낮으나 OS는 비슷",
        "출혈 위험·간기능 보전 환자에서의 위치가 점차 자리잡음",
    ],
    "bottom_line": "atezo+bev에 이은 두 번째 1차 옵션. 정맥류 출혈 이력 등 베바시주맙 회피가 필요한 환자, 또는 4년 이상의 'long survivor' 가능성을 중시할 때 선택. 한국 보험 진행 중이며 도입 후 두 1차 옵션의 환자별 선택 기준이 더 명확해질 것입니다.",
    "refs": [
        ("Abou-Alfa GK, Lau G, Kudo M, et al. Tremelimumab plus Durvalumab in Unresectable Hepatocellular Carcinoma. <em>NEJM Evid</em>. 2022;1(8):EVIDoa2100070.", "10.1056/EVIDoa2100070", None),
        ("Finn RS, Qin S, Ikeda M, et al. Atezolizumab plus Bevacizumab in Unresectable Hepatocellular Carcinoma. <em>N Engl J Med</em>. 2020;382(20):1894–1905.", "10.1056/NEJMoa1915745", "32402160"),
        ("Singal AG, Llovet JM, Yarchoan M, et al. AASLD Practice Guidance on prevention, diagnosis, and treatment of hepatocellular carcinoma. <em>Hepatology</em>. 2023;78(6):1922–1965.", "10.1097/HEP.0000000000000466", "37199193"),
        ("Yau T, Park JW, Finn RS, et al. Nivolumab versus sorafenib in advanced hepatocellular carcinoma (CheckMate 459). <em>Lancet Oncol</em>. 2022;23(1):77–90.", "10.1016/S1470-2045(21)00604-5", "34914889"),
    ],
    "related": [
        ("/간암-면역치료-1차/", "면역치료 1차 시대 - atezo+bev과 그 이후"),
        ("/간암-BCLC병기/", "BCLC 병기와 치료 옵션"),
        ("/updates/IMbrave150-atezolizumab-bevacizumab-NEJM-2020/", "IMbrave150 - atezo+bev"),
    ],
})

# 3. Pan CQ TDF pregnancy
UPDATES.append({
    "slug": "Pan-TDF-pregnancy-HBV-NEJM-2016",
    "h1": "TDF for HBV in pregnancy - 수직감염 차단의 표준화",
    "description": "Pan CQ et al. NEJM 2016. RCT, 200명 HBV DNA 고농도 임산부, 임신 30주부터 TDF가 영아 HBV 감염을 0%로 감소시킨 결정적 시험.",
    "last_crumb": "TDF in pregnancy (Pan)",
    "cite": "Pan CQ, Duan Z, Dai E, et al. Tenofovir to Prevent Hepatitis B Transmission in Mothers with High Viral Load. <em>N Engl J Med</em>. 2016;374(24):2324–2334.",
    "cite_link": "https://www.nejm.org/doi/full/10.1056/NEJMoa1508660",
    "tldr": "2016년 NEJM Pan CQ 시험은 HBV DNA가 200,000 IU/mL 이상인 산모에서 임신 30주부터 출산 후 4주까지 <em>TDF 투여로 영아 감염을 0%로 줄였습니다</em> (대조군 7%). HBIG+백신 표준에 더해 산모 항바이러스제가 추가되어 수직감염 차단의 표준이 자리잡힌 결정적 RCT.",
    "background": "<p>HBV 수직감염은 만성 보균자의 가장 흔한 감염 경로입니다. 출생 직후 HBIG+백신으로 90% 차단되지만, HBV DNA가 매우 높은 산모(> 200,000 IU/mL)에서는 여전히 5–10%에서 영아 감염이 발생했습니다. 임신 후반기 항바이러스제로 산모의 바이러스 부하를 낮추면 영아 감염을 더 줄일 수 있다는 가설이었고, 이전 후향 연구·소규모 RCT에서 시사적이었으나 결정적 RCT가 부족했습니다.</p>",
    "methods_intro": "<p>다기관 open-label RCT, 중국·미국.</p>",
    "methods_bullets": [
        "대상: HBeAg 양성 + HBV DNA > 200,000 IU/mL 임산부",
        "n: 200명 (TDF 100, 표준치료 100)",
        "투약: TDF 300 mg/일 임신 30~32주 시작 → 출산 후 4주 중단",
        "출생아 모두 HBIG + 백신 0/1/6개월 시행",
        "주된 평가지표: 28주 영아 HBsAg 양성률 (intention-to-treat)",
    ],
    "findings_intro": "<p>영아 감염률에서 극명한 차이.</p>",
    "findings_svg": svg_table("Pan CQ 시험 결과 (28주 영아 HBsAg 양성률)",
                              ["분석", "TDF군", "대조군", "p"],
                              [["ITT 분석", "5%", "18%", "0.007"],
                               ["프로토콜 준수 분석", "0%", "7%", "0.01"],
                               ["산모 출산시 HBV DNA", "<200,000 92%", "<200,000 6%", "—"],
                               ["분만방식별 차이", "유의미한 차이 없음", "—", "—"]],
                              caption="프로토콜 준수 시 영아 감염 0% - 임상에 빠르게 반영"),
    "extra_svg": svg_checklist("HBV 임신 표준 흐름 (Pan 이후)",
                                ["임신 초기 - HBsAg + HBV DNA 확인",
                                 "HBV DNA > 200,000 IU/mL이면 임신 28-32주 TDF 시작",
                                 "TDF 출산 후 4주 또는 12주까지 유지 (가이드라인별)",
                                 "출생 12시간 이내 HBIG + 백신 1차",
                                 "1·6개월 백신 완료, 9-12개월 anti-HBs 확인",
                                 "수유 가능 (TDF 모유 분비 미량)"],
                                caption="HBIG+백신만으로 부족한 환자에 산모 항바이러스제 추가"),
    "critique": [
        "단일 약물 (TDF) 평가 - TAF는 별도 임상 진행 중",
        "HBeAg 양성·고농도 환자가 대상 - HBeAg 음성·저농도에서 일반화는 신중",
        "치료 중단 후 산모 ALT flare 약 5-10% - 출산 후 추적 필수",
        "장기 영아 안전성 (성장·골 발달) 후속 연구에서 무이상 보고",
        "한국 산모에서도 광범위하게 적용되는 표준",
    ],
    "bottom_line": "HBV 수직감염 예방의 마지막 퍼즐. HBV DNA가 매우 높은 산모에서 영아 감염을 거의 0으로 만든 결정적 RCT로, KASL·AASLD·EASL 가이드라인 모두 표준으로 채택. 자세한 임상 적용은 <a href=\"/B형간염-결혼-임신/\">B형간염과 임신</a> 참조.",
    "refs": [
        ("Pan CQ, Duan Z, Dai E, et al. Tenofovir to Prevent Hepatitis B Transmission in Mothers with High Viral Load. <em>N Engl J Med</em>. 2016;374(24):2324–2334.", "10.1056/NEJMoa1508660", "27305192"),
        ("Brown RS Jr, McMahon BJ, Lok AS, et al. Antiviral therapy in chronic hepatitis B viral infection during pregnancy. <em>Hepatology</em>. 2016;63(1):319–333.", "10.1002/hep.28302", "26565396"),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329"),
    ],
    "related": [
        ("/B형간염-결혼-임신/", "B형간염 보균자와 결혼·임신·수유"),
        ("/B형간염-항바이러스제-비교/", "항바이러스제 비교 - TDF · TAF · ETV"),
        ("/B형간염-백신/", "B형간염 백신 - 누가, 언제, 몇 번"),
    ],
})

# 4. Newsome SEMA-NASH
UPDATES.append({
    "slug": "Newsome-semaglutide-NASH-NEJM-2021",
    "h1": "Semaglutide for NASH - GLP-1의 MASH 적응증 가능성",
    "description": "Newsome PN et al. NEJM 2021. Phase 2 RCT, 320명 NASH 환자, semaglutide 0.4 mg 매일이 NASH 해결 59% vs placebo 17% - GLP-1 작용제 MASH 효과의 결정적 첫 RCT.",
    "last_crumb": "Semaglutide for NASH",
    "cite": "Newsome PN, Buchholtz K, Cusi K, et al. A Placebo-Controlled Trial of Subcutaneous Semaglutide in Nonalcoholic Steatohepatitis. <em>N Engl J Med</em>. 2021;384(12):1113–1124.",
    "cite_link": "https://www.nejm.org/doi/full/10.1056/NEJMoa2028395",
    "tldr": "2021년 NEJM Newsome 시험은 <em>매일 피하주사 semaglutide 0.4 mg</em>이 NASH(F1-F3) 해결률을 위약 대비 의미 있게 높였음을 보였습니다 (59% vs 17%, 0.4 mg). 단 섬유화 호전은 일차 평가지표에서 통계적 유의성 부족. 후속 ESSENCE phase 3로 발전했고 2025년 결과로 MASH 적응증 추가 가능성이 큽니다.",
    "background": "<p>당뇨·비만 약물 GLP-1 작용제(semaglutide, liraglutide)는 체중 감량과 인슐린 감수성 개선으로 MASH에도 효과가 기대되었습니다. 소규모 시험(LEAN, 2016)에서 liraglutide가 NASH 해결을 보였고, semaglutide는 더 강력한 체중 감량으로 phase 2 확정 시험이 디자인되었습니다.</p>",
    "methods_intro": "<p>다국가, double-blind, placebo-controlled phase 2 RCT.</p>",
    "methods_bullets": [
        "대상: 조직학적 확진 NASH (NAS ≥4) + F1-F3 섬유화",
        "n: 320명 (semaglutide 0.1, 0.2, 0.4 mg/일 + 위약, 3:3:3:1)",
        "투약: 피하 매일 72주 (현재 위고비/오젬픽은 주 1회)",
        "주된 평가지표: 72주 시점 NASH 해결 + 섬유화 악화 없음",
        "주요 2차: ≥1단계 섬유화 호전 + NASH 악화 없음, 체중 변화",
    ],
    "findings_intro": "<p>NASH 해결은 의미 있게 개선, 섬유화 호전은 통계적 유의성 부족.</p>",
    "findings_svg": svg_table("Newsome SEMA-NASH 주요 결과 (72주)",
                              ["", "Placebo", "Sema 0.1 mg", "Sema 0.2 mg", "Sema 0.4 mg"],
                              [["NASH 해결", "17%", "40%", "36%", "59%"],
                               ["섬유화 호전", "33%", "43%", "40%", "43%"],
                               ["체중 변화", "-1.0%", "-5%", "-9%", "-13%"],
                               ["당화혈색소 변화", "+0.1%", "-0.4%", "-1.2%", "-1.4%"]],
                              caption="NASH 해결은 용량 의존적, 섬유화 호전은 통계적 유의성 부족"),
    "extra_svg": svg_compare_two("강점",
                                  ["NASH 해결률 우수 (59% vs 17%)",
                                   "체중 감량 13% (이전 약물 미달성)",
                                   "당뇨·비만 동반 환자에 일관된 이득",
                                   "심혈관 보호 효과 부수적"],
                                  "한계",
                                  ["섬유화 호전 1차 평가지표 미달성",
                                   "구역·구토 부작용 (시작·증량 시)",
                                   "F4 간경변 환자 미포함",
                                   "일일 피하주사 (현재는 주 1회 제형 표준)"],
                                  caption="후속 ESSENCE 시험으로 phase 3 발전"),
    "critique": [
        "Phase 2 - phase 3 재현이 필요했음 (ESSENCE 2025로 확인 진행)",
        "섬유화 호전 1차 평가지표 미달성이 약점",
        "피하 매일 - 현재 임상은 주 1회 (오젬픽·위고비) 제형이 표준",
        "F4 간경변 환자 미포함 - 안전성·효과 별도 평가 필요",
        "임상에서 당뇨·비만 적응증으로 이미 사용되며 MASH 이득 부수적으로 활용",
    ],
    "bottom_line": "GLP-1 작용제의 MASH 효과를 결정적으로 보여준 첫 phase 2 RCT. 후속 ESSENCE phase 3 결과(2025)로 MASH 적응증 추가 가능성이 큽니다. 자세한 임상 적용은 <a href=\"/지방간-SGLT2-GLP1/\">SGLT2·GLP-1 작용제와 지방간</a>·<a href=\"/지방간-신약-resmetirom/\">지방간 신약</a> 참조.",
    "refs": [
        ("Newsome PN, Buchholtz K, Cusi K, et al. A Placebo-Controlled Trial of Subcutaneous Semaglutide in Nonalcoholic Steatohepatitis. <em>N Engl J Med</em>. 2021;384(12):1113–1124.", "10.1056/NEJMoa2028395", "33185364"),
        ("Armstrong MJ, Gaunt P, Aithal GP, et al. Liraglutide safety and efficacy in patients with non-alcoholic steatohepatitis (LEAN). <em>Lancet</em>. 2016;387(10019):679–690.", "10.1016/S0140-6736(15)00803-X", "26608256"),
        ("Loomba R, Hartman ML, Lawitz EJ, et al. Tirzepatide for Metabolic Dysfunction-Associated Steatohepatitis with Liver Fibrosis. <em>N Engl J Med</em>. 2024;391(4):299–310.", "10.1056/NEJMoa2401943", "38856224"),
        ("Rinella ME, Neuschwander-Tetri BA, Siddiqui MS, et al. AASLD Practice Guidance on the clinical assessment and management of nonalcoholic fatty liver disease. <em>Hepatology</em>. 2023;77(5):1797–1835.", "10.1097/HEP.0000000000000323", "36727674"),
    ],
    "related": [
        ("/지방간-SGLT2-GLP1/", "SGLT2·GLP-1 작용제와 지방간"),
        ("/지방간-신약-resmetirom/", "지방간 신약 - resmetirom과 다음 세대"),
        ("/지방간염-MASH/", "지방간염(MASH)"),
    ],
})

# 5. Baveno VII
UPDATES.append({
    "slug": "Baveno-VII-portal-hypertension-J-Hepatol-2022",
    "h1": "Baveno VII - 문맥압항진의 새 합의",
    "description": "de Franchis R et al. J Hepatol 2022. Baveno VII 합의 - clinically significant portal hypertension(CSPH) 비침습 진단 기준, 식도정맥류 검진 생략 기준, 임상적 재대상화(recompensation) 정의 등을 표준화한 결정적 합의.",
    "last_crumb": "Baveno VII",
    "cite": "de Franchis R, Bosch J, Garcia-Tsao G, Reiberger T, Ripoll C; Baveno VII Faculty. Baveno VII - Renewing consensus in portal hypertension. <em>J Hepatol</em>. 2022;76(4):959–974.",
    "cite_link": "https://www.journal-of-hepatology.eu/article/S0168-8278(21)02299-6/fulltext",
    "tldr": "2022년 J Hepatol에 발표된 Baveno VII 합의는 간경변 임상 관리의 여러 표준을 재정의했습니다. 핵심: <em>비침습 검사(LSM, 혈소판)로 CSPH 진단 가능, 일부 환자에서 정맥류 내시경 검진 생략, 임상적 재대상화(recompensation) 정의 도입</em>. 외래 결정 흐름이 의미 있게 단순화됐습니다.",
    "background": "<p>Baveno 합의는 1990년부터 5–6년마다 갱신되는 문맥압항진 분야의 권위 합의입니다. 2015년 Baveno VI에서 'Baveno VI criteria'(LSM ≤20 kPa + 혈소판 ≥150,000)가 도입되어 정맥류 검진 생략 가능성이 제시되었고, 7년의 추가 임상 데이터·신약(NSBB의 더 적극적 사용)이 누적되어 Baveno VII로 발전했습니다.</p>",
    "methods_intro": "<p>합의 절차: 국제 hepatology·portal hypertension 전문가 패널의 modified Delphi.</p>",
    "methods_bullets": [
        "주제 영역: 위험 분류·CSPH 진단·1차 예방·급성 출혈·2차 예방·재대상화 등",
        "각 명제에 대해 합의 수준 평가",
        "주요 RCT(PREDESCI 등)와 코호트 데이터 통합",
        "이전 Baveno 합의와의 변화점 명시",
    ],
    "findings_intro": "<p>임상에 영향이 큰 핵심 권고:</p>",
    "findings_svg": svg_table("Baveno VII 주요 변화",
                              ["영역", "Baveno VI", "Baveno VII"],
                              [["CSPH 진단", "HVPG 측정 필요", "LSM ≥25 kPa 단독 가능 (특정 원인)"],
                               ["정맥류 검진 생략", "LSM <20 + PLT ≥150", "동일 + Anticipate 알고리즘 추가"],
                               ["1차 예방", "큰 정맥류만 NSBB", "CSPH 환자에 광범위 NSBB (PREDESCI)"],
                               ["권장 NSBB", "프로프라놀롤 위주", "카베디롤 우선"],
                               ["재대상화", "정의 없음", "임상적 정의 (3 합병증 1년+ 부재)"]],
                              caption="비침습 평가 활용·NSBB 적극 사용·재대상화 정의가 핵심 변화"),
    "extra_svg": svg_checklist("Baveno VII 임상적 재대상화(recompensation) 기준",
                                ["원인 질환 제거 또는 효과적 치료 (B형 항바이러스, 알코올 금주, MASH 체중감량)",
                                 "복수·정맥류 출혈·간성혼수가 1년 이상 재발 없음",
                                 "간 기능의 지속적 개선 (알부민·INR·빌리루빈)",
                                 "이뇨제·NSBB·락툴로스 의존도 감소",
                                 "3개 모두 충족 시 재대상화로 분류"],
                                caption="\"한 번 비대상성이면 끝\"이 아니라는 임상적 명문화"),
    "critique": [
        "비침습 진단 기준은 MASLD·B형간염에서 검증되었으나 다른 원인에서 추가 검증 필요",
        "PREDESCI를 근거로 한 광범위 NSBB 사용은 일부 환자에서 부작용 누적 우려",
        "재대상화 정의는 임상적이며 영상·HVPG 기반 객관적 정의는 향후 과제",
        "한국 임상에서 LSM 검사 가용성 차이로 권고 적용 일관성 도전",
        "Baveno VIII (2027 예정)에서 추가 갱신 예고",
    ],
    "bottom_line": "외래 간경변 환자 관리의 표준 변화. <strong>비침습 평가로 정맥류 검진 생략 가능, NSBB의 적극 사용, 재대상화 개념 도입</strong>이 임상 결정 흐름을 단순화·정교화했습니다. 자세한 임상 적용은 <a href=\"/간경변-식도정맥류/\">식도정맥류</a>·<a href=\"/간경변-대상성-비대상성/\">대상성 vs 비대상성</a> 참조.",
    "refs": [
        ("de Franchis R, Bosch J, Garcia-Tsao G, Reiberger T, Ripoll C; Baveno VII Faculty. Baveno VII - Renewing consensus in portal hypertension. <em>J Hepatol</em>. 2022;76(4):959–974.", "10.1016/j.jhep.2021.12.022", "35120736"),
        ("Villanueva C, Albillos A, Genescà J, et al. β blockers to prevent decompensation of cirrhosis in patients with clinically significant portal hypertension (PREDESCI). <em>Lancet</em>. 2019;393(10181):1597–1608.", "10.1016/S0140-6736(18)31875-0", "30910320"),
        ("Garcia-Tsao G, Abraldes JG, Berzigotti A, Bosch J. Portal hypertensive bleeding in cirrhosis: Risk stratification, diagnosis, and management. <em>Hepatology</em>. 2017;65(1):310–335.", "10.1002/hep.28906", "27786365"),
        ("D'Amico G, Bernardi M, Angeli P. Towards a new definition of decompensated cirrhosis. <em>J Hepatol</em>. 2022;76(1):202–207.", "10.1016/j.jhep.2021.06.018", "34157322"),
    ],
    "related": [
        ("/간경변-식도정맥류/", "식도정맥류 - 첫 신호와 예방적 결찰"),
        ("/간경변-대상성-비대상성/", "대상성 vs 비대상성 간경변 - 어디서 갈라지나"),
        ("/간경변-복수/", "복수 - 단계별 관리"),
    ],
})

print(f"Updates - building {len(UPDATES)} paper notes...")
for spec in UPDATES:
    render_update(spec)
print("Done.")
