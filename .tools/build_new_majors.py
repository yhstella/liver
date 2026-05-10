"""Generate hub + subtopic + case pages for two new 대주제:
  6. C형 간염 (page-id 6-1 ~)
  7. 자가면역간염 (page-id 7-1 ~)

Series numbering note: existing 'updates' was 6 — moved to no-number ('Updates').
New 6 = C형 간염, new 7 = 자가면역간염.
"""
import os, sys, html as htmllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def esc(s): return htmllib.escape(s or "")

NAV = '''<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></nav></div></header>'''
FOOTER = '''<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>'''


def render_topic_page(slug, title, page_id, series_label, series_url, tldr, sections,
                      faq=None, refs=None, pid_links=None):
    sections_html = "\n".join(f'<h2>{esc(h)}</h2>\n{body}' for h, body in sections)
    faq_html = ""
    if faq:
        items = "".join(
            f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
            for q, a in faq
        )
        faq_html = f'<h2>자주 묻는 질문</h2>\n<section class="faq-block">{items}</section>'
    refs_html = ""
    if refs:
        items = "".join(f'<li>{r}</li>' for r in refs)
        refs_html = f'<section class="references-block"><h2>References</h2><ol class="references">{items}</ol></section>'
    canon = f"https://drshin.kr/{slug}/"
    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Hepatology Note</title>
<meta name="description" content="{esc(title)} — {esc(series_label)} 세부주제.">
<link rel="canonical" href="{canon}">
<meta name="author" content="신현재">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
</head>
<body>
{NAV}
<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="{series_url}">{esc(series_label)}</a> › <span>{esc(title.split(" — ")[0])}</span> <span class="page-id">{page_id}</span></nav>
<article>
<h1>{esc(title)}</h1>
<div class="tldr"><strong>핵심 요약</strong>{tldr}</div>

{sections_html}

{faq_html}
{refs_html}
</article>
</main>
{FOOTER}
</body>
</html>
'''
    out = ROOT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote: /{slug}/ [{page_id}]")


def render_hub(slug, label, num, intro, topics, cases=None):
    cases = cases or []
    topic_rows = "".join(
        f'<li class="published"><a href="/{t["slug"]}/"><span class="num">{t["pid"]}</span><div class="body"><h3>{esc(t["title"])}</h3><p>{esc(t.get("desc",""))}</p></div><span class="status published">읽기 →</span></a></li>'
        for t in topics
    )
    case_cta = ""
    if cases:
        case_cta = f'''
<a href="/케이스/" style="display:flex;align-items:center;justify-content:space-between;margin:32px 0;padding:18px 24px;background:var(--accent-soft);border:1px solid var(--accent);border-radius:10px;text-decoration:none;color:var(--fg);transition:background .15s">
  <div>
    <strong style="display:block;color:var(--accent);font-size:14px;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:4px">{esc(label)} 케이스</strong>
    <span style="font-size:15px;color:var(--fg)">{esc(label)} 임상 시나리오 {len(cases)}편</span>
  </div>
  <span style="color:var(--accent);font-size:18px;font-weight:600">→</span>
</a>'''
    n_topics = len(topics)
    canon = f"https://drshin.kr/{slug}/"
    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(label)} — Hepatology Note</title>
<meta name="description" content="{esc(label)} 대주제 — {esc(intro)}">
<link rel="canonical" href="{canon}">
<meta name="author" content="신현재">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(label)}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
</head>
<body>
{NAV}
<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>{esc(label)}</span></nav>
<p class="series-label">대주제 {num}</p>
<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:34px;letter-spacing:-0.025em;font-weight:600;margin:0 0 12px">{esc(label)}</h1>
<p class="series-intro">{intro}</p>
<div class="series-meta">
  <span>세부주제 {n_topics}편</span>
  <span>· 케이스 {len(cases)}편</span>
</div>

<ul class="topic-list">
{topic_rows}
</ul>
{case_cta}
</main>
{FOOTER}
</body>
</html>
'''
    out = ROOT / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote hub: /{slug}/ [대주제 {num}]")


def render_case(slug, title, page_id, series_label, series_url, intro, sections,
                teaching, related, figure_html=""):
    sections_html = ""
    for idx, (h2, body) in enumerate(sections):
        sections_html += f'<div class="case-section"><h2>{esc(h2)}</h2>\n{body}\n</div>\n'
        if idx == 0 and figure_html:
            sections_html += figure_html + "\n"
    teach = "".join(f'<li>{esc(t)}</li>' for t in teaching)
    rel = "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in related)
    canon = f"https://drshin.kr/케이스/{slug}/"
    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Hepatology Note</title>
<meta name="description" content="{esc(title)} — {esc(series_label)} 임상 케이스 노트.">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:url" content="{canon}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
</head>
<body>
{NAV}
<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="{series_url}">{esc(series_label)}</a> › <a href="/케이스/">케이스</a> › <span>{esc(title)}</span> <span class="page-id">{page_id}</span></nav>
<h1>{esc(title)}</h1>
<div class="case-intro">
{intro}
</div>
{sections_html}
<div class="teaching-box">
<h2>Teaching points</h2>
<ul>{teach}</ul>
</div>
<aside class="related"><h2>관련 가이드</h2><ul>{rel}</ul></aside>
<p class="disclaimer" style="margin-top:48px">본 케이스는 외래에서 자주 만나는 임상 시나리오를 익명화하여 재구성한 교육 자료입니다.</p>
</main>
{FOOTER}
</body>
</html>
'''
    out = ROOT / "케이스" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"  wrote case: 케이스/{slug} [{page_id}]")


# ====================================================
# === 6. C형 간염 (Series 6)
# ====================================================
def build_c_hepatitis():
    series_label = "C형 간염"
    series_url = "/C형간염/"
    series_num = "6"

    # 6-1 진단·검사
    render_topic_page(
        "C형간염-진단", "C형 간염 진단 — anti-HCV에서 HCV RNA까지", "6-1", series_label, series_url,
        '<strong>anti-HCV 양성</strong>은 노출 표지자입니다. 현재 활동성 감염은 <strong>HCV RNA(PCR)</strong>로 확인합니다. RNA 양성이면 genotype 검사 후 DAA(direct-acting antiviral)로 8-12주 치료, 95% 이상 완치(SVR12)가 가능합니다. 자연 회복으로 anti-HCV는 양성이지만 RNA 음성인 경우도 있어 RNA 검사가 진단의 결정적 단계입니다.',
        sections=[
            ("anti-HCV 양성 = 감염 진행형은 아닙니다",
             "<p>anti-HCV는 과거 노출 또는 현재 감염을 의미하는 항체입니다. 양성 환자 약 25%는 자연 회복으로 RNA 음성 상태이며, 나머지 75%가 만성 감염(RNA 양성)입니다. 따라서 anti-HCV(+) 첫 발견 시 <strong>HCV RNA(PCR) 추가 검사</strong>가 필수 — 활동성 감염 여부를 가립니다.</p>"),
            ("진단 후 평가",
             "<p>RNA 양성 확인 시 다음을 평가합니다.</p>"
             "<ul>"
             "<li><strong>Genotype</strong> (1a/1b/2/3/4 등) — pangenotype DAA 시대에는 결정적이지 않지만 일부 약물 선택과 기간에 영향</li>"
             "<li><strong>간섬유화</strong> (Fibroscan, FIB-4) — 간경변 동반 여부가 치료 기간과 추적 강도에 결정적</li>"
             "<li><strong>HBV 동반 평가</strong> (HBsAg) — DAA 치료 중 HBV 재활성화 위험으로 사전 확인</li>"
             "<li><strong>신기능</strong>(eGFR) — 일부 DAA는 신기능 저하 환자에서 약물 선택 제한</li>"
             "</ul>"),
            ("간외 합병증 평가도 동시에",
             "<p>C형간염은 간뿐 아니라 다음 간외 합병증과 연관됩니다 — cryoglobulinemia, 림프증식성 질환, 신장 질환(MPGN), 인슐린 저항성, 우울증. 진단 시점에 단순 신체 검사·소변검사로 기초 평가를 함께 합니다. DAA 완치 후 대부분의 간외 합병증도 호전이 보고됩니다.</p>"),
        ],
        faq=[
            ("anti-HCV 양성인데 RNA 음성이면 안심해도 되나요?",
             "네, 자연 회복 또는 과거 치료로 완치된 상태입니다. 다만 RNA 검사가 1회 음성이라도 확실히 음성을 확인하려면 4-12주 후 한 번 더 RNA 검사를 권장합니다. 재감염 가능성이 있는 위험군(정맥주사 약물, 다파트너 등)에서는 정기 RNA 추적이 필요합니다."),
            ("간경변이 동반된 C형간염도 DAA로 완치 가능한가요?",
             "네, 가능합니다. SVR12 달성률은 간경변 동반에서도 90-95%로 높습니다. 다만 진행성 간경변(Child-Pugh B-C) 환자에서는 일부 protease inhibitor 함유 DAA(글레카프레비르 등)는 회피하고, sofosbuvir 기반 조합을 선택합니다. 완치 후에도 간경변과 그에 따른 HCC 위험은 평생 추적이 필요합니다."),
        ],
        refs=[
            'AASLD-IDSA. HCV Guidance: Recommendations for Testing, Managing, and Treating Hepatitis C. Updated 2023.',
            'KASL Clinical Practice Guidelines for Management of Hepatitis C. 2023.',
        ],
    )

    # 6-2 DAA 완치 (existing page — leave at /C형간염-완치-DAA/, just re-categorize keyword to series 6)
    # Hub will link to it.

    # 6-3 완치 후 평생 추적
    render_topic_page(
        "C형간염-완치후-추적", "DAA 완치(SVR) 후에도 추적이 필요한 이유", "6-3", series_label, series_url,
        'SVR(sustained virologic response) 달성은 \"바이러스 박멸\"이지만, <strong>간경변·진행 섬유화</strong>가 동반되었던 환자는 완치 후에도 <strong>평생 6개월 간암 검진</strong>이 필요합니다. SVR 후에도 HCC 발생률이 일반인보다 의미 있게 높기 때문입니다. 또한 재감염 가능성이 있는 위험군은 정기 RNA 추적이 필요합니다.',
        sections=[
            ("SVR ≠ HCC 위험 소실",
             "<p>여러 메타분석에서 DAA SVR 후에도 간경변·진행 섬유화 환자의 HCC 발생률이 연 1-3%로 보고됩니다. 일반인 대비 약 5-10배 높은 수치입니다. 따라서 <strong>치료 전 Fibroscan/생검에서 진행 섬유화(F3) 또는 간경변(F4)</strong>이 확인되었던 환자는 SVR 달성 후에도 6개월마다 초음파 + AFP 검진을 평생 유지합니다.</p>"),
            ("간 외 추적도 함께",
             "<p>C형간염 동반 합병증은 SVR 후 호전되지만 일부는 잔존합니다 — cryoglobulinemia 활동성, 신장 질환, 인슐린 저항성. 진단 시점 간외 합병증이 있었다면 6-12개월마다 평가합니다. SVR 후 ALT가 정상화되고 6개월 후에도 안정 유지되면 추가 RNA 측정은 필수가 아닙니다.</p>"),
            ("재감염 위험군은 별도 관리",
             "<p>정맥주사 약물 사용자, MSM, 다파트너 등 위험군은 SVR 후에도 재감염 가능성이 있어 1-2년마다 HCV RNA 검사가 권장됩니다. 재감염 시 다시 DAA로 치료하면 동일하게 95% 이상 완치 가능합니다.</p>"),
        ],
        faq=[
            ("SVR 달성 후 ALT가 정상이면 안심해도 되나요?",
             "활동성 바이러스는 사라졌지만 간 자체의 손상(섬유화·간경변)은 잔존합니다. ALT 정상은 좋은 신호이지만 간경변·진행 섬유화 환자는 평생 6개월 간암 검진이 필요합니다."),
        ],
        refs=[
            'Ioannou GN, et al. HCC Risk after DAA SVR. Hepatology 2018.',
            'KASL Clinical Practice Guidelines for HCC Surveillance after HCV Cure. 2024.',
        ],
    )

    # 6-4 case: anti-HCV 양성 첫 발견
    render_case(
        "anti-HCV양성-첫발견", "anti-HCV 양성 첫 발견 — RNA 확인부터 DAA까지", "6-4", series_label, series_url,
        '<p>54세 여성 환자입니다. 직장 건강검진에서 anti-HCV 양성이 처음 발견되어 외래에 내원하셨습니다. 무증상이며 음주력 거의 없음, 과거 수혈력은 1990년대 출산 시 1회 있으셨다고 합니다.</p>',
        sections=[
            ("진단 — RNA + Fibroscan",
             "<p>anti-HCV 양성은 노출 표지일 뿐 활동성 감염을 의미하지 않으므로 <strong>HCV RNA(PCR)</strong>를 시행하였습니다. 결과 4.2×10⁵ IU/mL로 활동성 감염 확인, genotype 1b로 동정되었습니다. Fibroscan 7.8 kPa, FIB-4 1.6, 간경변 소견 없음. ALT 78, AST 65, 혈소판 195 ×10³.</p>"),
            ("DAA 치료와 경과",
             "<p>비경변 genotype 1b 환자에서 <strong>glecaprevir/pibrentasvir 8주</strong>를 시작하였습니다. 8주 종료 후 12주 시점 HCV RNA 음성(SVR12) 확인 — 완치되었습니다. ALT는 28로 정상화, Fibroscan 5.5 kPa로 호전. 이후 1년에 1회 정기 검사로 재감염 모니터링 계획입니다.</p>"),
        ],
        teaching=[
            "anti-HCV(+) 첫 발견 시 HCV RNA(PCR)로 활동성 감염 여부 즉시 확인",
            "비경변 환자에서 pangenotype DAA 8주가 표준 (95% SVR)",
            "Fibroscan으로 간경변 동반 여부 평가 — 추적 강도 결정",
            "간경변 미동반 SVR 환자는 평생 검진 필요 없음 (재감염 위험군 제외)",
        ],
        related=[
            ("/C형간염-진단/", "C형간염 진단"),
            ("/C형간염-완치-DAA/", "C형간염 DAA 완치"),
            ("/C형간염-완치후-추적/", "DAA 완치 후 추적"),
        ],
    )

    # 6-5 case: 간경변 동반 + 완치 후 추적 중 새 결절
    render_case(
        "C형간염-간경변-새결절", "C형간염 DAA 완치 5년 후 새 결절 발견", "6-5", series_label, series_url,
        '<p>67세 남성 환자입니다. 과거 만성 C형간염으로 5년 전 DAA(sofosbuvir/velpatasvir 12주)로 SVR 달성하셨고, 당시 간경변(Fibroscan 19 kPa, Child-Pugh A) 동반으로 평생 6개월 간암 검진을 유지해 왔습니다. 이번 정기 EOB-MRI에서 우엽 S5에 1.4 cm 결절이 새로 발견되었습니다.</p>',
        sections=[
            ("정밀 평가",
             "<p>SVR 달성 후에도 간경변 환자는 평생 HCC 위험이 남습니다. EOB-MRI에서 동맥기 조영 증강 + 정맥기 washout + 간담도기 hypointensity로 LR-5(확실한 HCC)로 판정되었습니다. AFP 32, PIVKA-II 48.</p>"),
            ("결정과 경과",
             "<p>BCLC A기 단일 1.4 cm HCC, Child-Pugh A로 다학제에서 <strong>고주파열치료술</strong>을 결정하였습니다. 시술 합병증 없이 완전 괴사 확인. 1·3·6개월 영상 모두 정상, AFP·PIVKA-II 정상화. 향후 6개월마다 평생 추적 지속.</p>"),
        ],
        teaching=[
            "DAA SVR 달성 후에도 간경변 동반 환자는 평생 6개월 간암 검진",
            "SVR 후 HCC 발생률 연 1-3% — 일반인 대비 5-10배 높음",
            "정기 검진의 가치 — 1.4 cm 단일 결절은 RFA로 회복",
            "C형간염 검진은 \"평생\" 개념이 환자 동기 부여에 결정적",
        ],
        related=[
            ("/C형간염-완치후-추적/", "DAA 완치 후 추적"),
            ("/간암-진단-첫외래/", "간암 진단 첫 외래"),
            ("/B형간염-간암검진/", "간암 검진 (B형간염 페이지의 일반 검진 흐름)"),
        ],
    )

    # Hub
    render_hub("C형간염", "C형 간염", "6",
               "C형 간염은 anti-HCV 검사로 노출을 확인하고, HCV RNA(PCR)로 활동성을 확인합니다. DAA로 8-12주 치료 시 95% 이상 완치(SVR)가 가능한 시대가 되었습니다. 다만 간경변 동반 환자는 SVR 후에도 평생 간암 검진이 필요합니다.",
               topics=[
                   {"slug": "C형간염-진단", "pid": "6-1", "title": "C형 간염 진단 — anti-HCV에서 HCV RNA까지",
                    "desc": "anti-HCV 양성과 활동성 감염의 차이, RNA·genotype·섬유화 평가"},
                   {"slug": "C형간염-완치-DAA", "pid": "6-2", "title": "DAA 8주 완치",
                    "desc": "Pangenotype DAA로 95% 완치, 단순화된 치료 흐름"},
                   {"slug": "C형간염-완치후-추적", "pid": "6-3", "title": "SVR 후 평생 추적",
                    "desc": "간경변 동반 환자의 평생 HCC 검진과 재감염 모니터링"},
               ],
               cases=["6-4", "6-5"])


# ====================================================
# === 7. 자가면역간염 (Series 7)
# ====================================================
def build_aih():
    series_label = "자가면역간염"
    series_url = "/자가면역간염/"
    series_num = "7"

    render_topic_page(
        "자가면역간염-진단", "자가면역간염(AIH) 진단 — Simplified score와 조직", "7-1", series_label, series_url,
        '자가면역간염은 ALT 상승 + IgG 상승 + 자가항체(ANA, ASMA, anti-LKM) + 조직(interface hepatitis)의 조합으로 진단합니다. <strong>Simplified AIH score</strong>(Hennes 2008)로 6점 이상 probable, 7점 이상 definite. 다른 원인(바이러스·약물·자가면역 동반)을 반드시 배제해야 합니다.',
        sections=[
            ("진단의 4가지 축",
             "<p>AIH 진단은 단일 검사가 아닌 다음 4가지 축의 조합으로 결정됩니다.</p>"
             "<ul>"
             "<li><strong>임상</strong> — ALT/AST 상승, 무증상 또는 피로·황달, 다른 자가면역질환 동반(갑상선·셀리악 등)</li>"
             "<li><strong>혈청학</strong> — ANA ≥ 1:40, ASMA ≥ 1:40, anti-LKM ≥ 1:40, IgG 상승</li>"
             "<li><strong>조직</strong> — interface hepatitis, plasma cell infiltration, rosetting (생검 권장)</li>"
             "<li><strong>배제</strong> — HBV/HCV/HEV, 약물성, 윌슨병, hemochromatosis, NAFLD 등 모두 배제</li>"
             "</ul>"
             "<p>4가지 축을 종합한 Simplified AIH score(Hennes Hepatology 2008)로 점수화 — 6점 probable, 7점 이상 definite.</p>"),
            ("AIH 분류",
             "<p>주로 두 가지 유형으로 분류됩니다.</p>"
             "<ul>"
             "<li><strong>Type 1</strong> — ANA/ASMA 양성, 모든 연령, 가장 흔함 (90%)</li>"
             "<li><strong>Type 2</strong> — anti-LKM/anti-LC1 양성, 주로 소아·청소년, 더 진행적</li>"
             "</ul>"
             "<p>한국을 포함한 동아시아에서는 type 1이 압도적이며, 30-50대 여성에서 호발합니다.</p>"),
            ("PBC·PSC 중첩 평가",
             "<p>AIH가 PBC(primary biliary cholangitis) 또는 PSC(primary sclerosing cholangitis)와 중첩되는 \"overlap syndrome\"이 약 10%에서 보고됩니다. ALP·GGT가 상승하면 PBC overlap을 의심하고 anti-mitochondrial Ab(AMA)을 추가 평가합니다. 담관 영상(MRCP)으로 PSC 평가도 검토합니다.</p>"),
        ],
        faq=[
            ("ANA 양성이면 모두 자가면역간염인가요?",
             "아닙니다. ANA는 일반인구의 약 5-10%에서 양성이며, 단순 노화·다른 자가면역질환·일부 약물·바이러스 감염에서도 양성입니다. AIH 진단은 ANA 양성 + ALT 상승 + IgG 상승 + 조직 소견의 조합으로 결정됩니다. ANA 단독 양성은 진단을 의미하지 않습니다."),
            ("AIH는 평생 약을 먹어야 하나요?",
             "치료는 단계적 감량을 거치며 일부 환자에서는 약 중단 시도가 가능합니다. 표준은 prednisolone + azathioprine으로 6-12개월 안정 유도 후 점진적 감량. 2-3년 안정 후에도 약 중단 시 재발률이 50-80%로 높아 신중하게 결정합니다. 중단 후 재발 시 재시작 — 일부는 평생 저용량 유지가 안전한 옵션입니다."),
        ],
        refs=[
            'Hennes EM, et al. Simplified Criteria for the Diagnosis of Autoimmune Hepatitis. Hepatology 2008;48:169-176.',
            'AASLD Practice Guidance on Autoimmune Hepatitis. Hepatology 2020.',
        ],
    )

    render_topic_page(
        "자가면역간염-치료", "AIH 표준 치료 — prednisolone + azathioprine", "7-2", series_label, series_url,
        '표준 induction은 <strong>prednisolone 30-40 mg/day + azathioprine 50 mg/day</strong>이며, ALT 정상화 + IgG 정상화 시 점진적 감량합니다. 스테로이드 단독보다 병용이 부작용 누적이 적어 표준입니다. 안정 유지 후 약 중단 시도 시 재발률 50-80%로 신중한 결정이 필요합니다.',
        sections=[
            ("Induction — 첫 6개월",
             "<p>표준 시작 — <strong>prednisolone 30-40 mg/day(체중 0.5-1 mg/kg) + azathioprine 50 mg/day</strong> 동시 시작. Azathioprine 단독은 부작용 위험으로 시작하지 않으며, 스테로이드와 병용으로 4-8주 후 azathioprine 75-100 mg/day까지 증량합니다.</p>"
             "<p>치료 반응 평가 — ALT를 매월 추적, 4주 후 50% 이상 감소, 8-12주 내 정상화가 표준 반응입니다. IgG도 4-8주 내 호전이 표준입니다.</p>"),
            ("Maintenance — 약 감량",
             "<p>ALT/IgG가 정상화되면 prednisolone을 매주 5 mg씩 감량합니다. 8-10주 후 5-7.5 mg/day 유지 단계 도달. Azathioprine은 75-100 mg/day로 유지 — 단독 또는 저용량 prednisolone과 병용. 6개월간 안정 유지 후 prednisolone 추가 감량 또는 중단 검토.</p>"),
            ("부작용 모니터링",
             "<p>주요 모니터링 — 1) Azathioprine: TPMT(thiopurine methyltransferase) 활성도 사전 확인 (저활성 환자에서 골수 억제 위험), 매월 CBC·ALT 추적, 2) Prednisolone: 혈당·혈압·골밀도, 백내장·녹내장, 감염 위험. 장기 사용 시 Calcium·Vitamin D + 골밀도 평가 정기 시행.</p>"),
        ],
        faq=[
            ("스테로이드 부작용이 걱정됩니다. 약 양을 줄일 수 있나요?",
             "Azathioprine 병용으로 스테로이드를 빨리 감량하는 것이 표준입니다. 6-10주 안정 도달 후 prednisolone 5-7.5 mg/day까지 감량 가능 — 이 용량은 장기 부작용 위험이 의미 있게 줄어듭니다. 일부 환자에서는 azathioprine 단독으로 유지 전환 가능합니다."),
            ("AZA 못 먹는 환자는 어떻게 하나요?",
             "Azathioprine 부작용 또는 TPMT 결핍 환자는 다음 옵션을 검토합니다 — 1) MMF(mycophenolate mofetil) 1-2 g/day, 2) Cyclosporine, tacrolimus 등 calcineurin 억제제 (3차 옵션), 3) Budesonide(비-경변 환자에서 부작용 적은 스테로이드). 약 변경은 자가면역 전문의 협진으로 결정합니다."),
        ],
        refs=[
            'AASLD Practice Guidance on AIH. Hepatology 2020.',
            'EASL Clinical Practice Guidelines: Autoimmune Hepatitis. J Hepatol 2015;63:971-1004.',
        ],
    )

    render_topic_page(
        "자가면역간염-약중단", "AIH 약 중단 — 시기·재발 위험·재시작", "7-3", series_label, series_url,
        '안정 유지 환자에서 약 중단을 검토할 수 있지만 <strong>재발률 50-80%</strong>로 신중한 결정이 필요합니다. 권장 조건 — 2년 이상 ALT/IgG 정상 유지 + 조직 호전(가능한 경우 생검) + 환자가 정기 추적 동의. 중단 후 1·3·6·12개월 추적 + 재발 시 즉시 재시작이 표준입니다.',
        sections=[
            ("중단 가능성 평가",
             "<p>약 중단 검토는 다음 조건을 모두 충족할 때 신중하게 시작합니다.</p>"
             "<ol>"
             "<li>최소 <strong>24개월 이상</strong> 안정 — ALT 정상, IgG 정상</li>"
             "<li>현재 prednisolone 용량 ≤ 5 mg/day(또는 단독 azathioprine)</li>"
             "<li>가능한 경우 <strong>중단 전 간생검</strong>으로 조직학적 호전 확인 (잔존 활동성 시 재발 위험 매우 높음)</li>"
             "<li>환자가 1·3·6·12개월 정기 추적에 동의</li>"
             "</ol>"),
            ("중단 후 추적 일정",
             "<p>약 중단 후 추적 — 1·3·6·12개월에 ALT/AST/IgG, 이후 6개월마다 평생. <strong>ALT > 2-3×ULN 또는 IgG 상승</strong> 시 재발로 판단하고 즉시 약 재시작합니다. 일부 환자에서 ALT가 100-200 사이로 약간 상승하는 \"low-grade flare\"는 신중한 판단 — 짧은 prednisolone 부스트로 회복 가능한 경우도 있습니다.</p>"),
            ("재발 시 대응",
             "<p>재발 환자는 <strong>이전 induction 용량으로 prednisolone 재시작 + azathioprine 유지</strong>합니다. 재발 환자는 일반적으로 더 신중하게 약 감량하며, 재중단보다는 평생 저용량 유지를 권장하는 경우가 많습니다. 반복 재발 환자는 평생 maintenance를 표준으로 봅니다.</p>"),
        ],
        faq=[
            ("약 중단 시도가 위험한가요?",
             "재발률이 50-80%로 높지만 재발 시 신속히 재시작하면 대부분 다시 안정 유도가 가능합니다. 다만 \"안정→재발→재시작\"을 반복하면 누적 손상 위험이 있어, 반복 재발 환자는 평생 저용량 유지를 권장합니다."),
            ("임신 계획이 있는데 약을 끊어야 하나요?",
             "Azathioprine은 임신 안전성이 비교적 잘 입증된 약물(category D이지만 임상 데이터 양호)로 임신 중 유지 가능합니다. Mycophenolate는 임신 금기로 임신 계획 시 azathioprine으로 전환합니다. 약 중단보다 안정 유지가 임신 결과에 더 유리합니다."),
        ],
        refs=[
            'AASLD Practice Guidance on AIH. Hepatology 2020.',
            'Hartl J, et al. Patient selection and treatment outcomes in AIH. J Hepatol 2015.',
        ],
    )

    # 7-4 case: 첫 진단 (move existing 5-11 here logically)
    render_case(
        "AIH-첫진단-여성", "젊은 여성의 AIH 첫 진단 — induction과 첫 6개월", "7-4", series_label, series_url,
        '<p>32세 여성 환자입니다. 6개월 전부터 피로·식욕 부진이 있어 검사한 결과 ALT 380, AST 290, IgG 28 g/L(상승), ANA 1:640, ASMA 양성으로 외래에 의뢰되었습니다. 음주력 없음, 약물·보충제 복용 없음.</p>',
        sections=[
            ("진단 — Simplified AIH score",
             "<p>AIH를 의심하여 추가 평가를 시행하였습니다. 바이러스(HBV/HCV/HEV) 모두 음성, 윌슨병·hemochromatosis 배제. 간생검에서 interface hepatitis + plasma cell infiltration + rosetting 확인 — 전형적 AIH 조직 소견. Simplified AIH score 7점(definite)으로 AIH type 1 진단을 확정하였습니다.</p>"),
            ("치료와 경과",
             "<p>표준 induction으로 <strong>prednisolone 30 mg/day + azathioprine 50 mg/day</strong>를 시작하였습니다. 4주 후 ALT 95로 빠른 반응, 8주 후 ALT 35로 정상화. Prednisolone을 점진적으로 감량(매주 5 mg씩) 시작. <strong>6개월</strong> 시점 prednisolone 7.5 mg + azathioprine 75 mg 유지로 ALT 25, IgG 정상화 확인. 향후 1년 안정 시 prednisolone 추가 감량 검토 계획.</p>"),
        ],
        teaching=[
            "AIH 의심 단서: 젊은 여성 + ALT 상승 + IgG 상승 + ANA/ASMA 양성",
            "Simplified AIH score 7점 이상 = definite",
            "표준: prednisolone 30 mg + azathioprine 50 mg → 점진 감량",
            "ALT/IgG 정상화 후에도 점진적 감량으로 재발 예방",
        ],
        related=[
            ("/자가면역간염-진단/", "AIH 진단"),
            ("/자가면역간염-치료/", "AIH 표준 치료"),
            ("/자가면역간염-약중단/", "AIH 약 중단"),
        ],
    )

    # 7-5 case: 약 중단 후 재발
    render_case(
        "AIH-약중단-재발", "AIH 약 중단 시도 후 재발 — 재시작과 평생 유지 결정", "7-5", series_label, series_url,
        '<p>45세 여성 환자입니다. 5년 전 AIH 진단으로 prednisolone + azathioprine 표준 치료, 24개월 안정 유지 후 약 중단을 시도하셨습니다. 중단 후 6개월 시점 무증상이지만 ALT 220 / IgG 26으로 재발이 확인되었습니다.</p>',
        sections=[
            ("재발 평가와 재시작",
             "<p>중단 시도 6개월 시점 ALT 220 (3-5×ULN 영역), IgG 재상승으로 재발 진단. 추가 정밀 검사로 다른 원인 배제 후 <strong>이전 induction 용량(prednisolone 30 mg + azathioprine 75 mg)</strong>으로 재시작하였습니다. 4주 후 ALT 60, 8주 후 ALT 32로 다시 정상화 도달.</p>"),
            ("평생 유지 결정",
             "<p>재발 환자는 약 중단 위험이 더 높아 다학제·환자와 상의 후 <strong>평생 저용량 유지</strong>를 결정하였습니다 — prednisolone 5 mg/day + azathioprine 75 mg/day. 골밀도 평가 + Calcium·Vitamin D 보충, 6개월마다 ALT/IgG/혈당/혈압 추적. 1년 시점 안정 유지 — 환자분 일상 활동에 지장 없음.</p>"),
        ],
        teaching=[
            "AIH 약 중단 후 재발률 50-80% — 신중한 결정",
            "재발 시 즉시 이전 induction 용량으로 재시작",
            "반복 재발 위험 환자는 평생 저용량 유지가 표준 옵션",
            "장기 prednisolone 사용 환자는 골밀도·혈당 정기 평가 필수",
        ],
        related=[
            ("/자가면역간염-약중단/", "AIH 약 중단"),
            ("/자가면역간염-치료/", "AIH 표준 치료"),
        ],
    )

    # Hub
    render_hub("자가면역간염", "자가면역간염", "7",
               "자가면역간염(AIH)은 면역계가 간세포를 공격하는 만성 진행성 질환입니다. 30-50대 여성에서 호발하며, ALT 상승 + IgG 상승 + 자가항체 + 조직(interface hepatitis)의 조합으로 진단합니다. Prednisolone + azathioprine 표준 치료로 대부분 안정 유도가 가능하지만, 약 중단 후 재발률이 50-80%로 신중한 장기 관리가 필요합니다.",
               topics=[
                   {"slug": "자가면역간염-진단", "pid": "7-1", "title": "AIH 진단 — Simplified score와 조직",
                    "desc": "ALT·IgG·자가항체·조직 4축, 다른 원인 배제, PBC·PSC overlap"},
                   {"slug": "자가면역간염-치료", "pid": "7-2", "title": "표준 치료 — prednisolone + azathioprine",
                    "desc": "Induction → maintenance → 감량, 부작용 모니터링"},
                   {"slug": "자가면역간염-약중단", "pid": "7-3", "title": "약 중단 — 시기·재발·재시작",
                    "desc": "2년 안정 + 조직 호전 시 검토, 재발 50-80%"},
               ],
               cases=["7-4", "7-5"])


print("Building C형 간염 (대주제 6)...")
build_c_hepatitis()
print("\nBuilding 자가면역간염 (대주제 7)...")
build_aih()
print("\nDone.")
