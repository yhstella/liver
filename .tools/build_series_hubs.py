"""Generate 6 series hub pages from topic spec.
Existing articles are linked; missing topics are shown as 준비 중 placeholders.
"""
import html as htmllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Topic spec: (number, title, slug-or-None-for-draft, one-line-description)
SERIES = {
    "간암": {
        "num": "01",
        "intro": "간암 진단 직후의 의사결정부터 BCLC 병기, 절제·색전·면역치료의 선택, 간이식 적응증, 검진과 재발 추적까지. 외래에서 환자분께 단계별로 설명드리는 흐름 그대로 정리합니다.",
        "topics": [
            (1, "간암 진단을 받았을 때, 첫 외래에서 결정되는 것", None,
             "병기 평가, 추가 영상, 치료팀 구성 — 첫 만남에서 무엇이 결정되는지"),
            (2, "BCLC 병기와 치료 옵션 — 무엇이 어떤 환자에게", None,
             "0·A·B·C·D 단계별 표준치료와 한국 임상에서의 적용"),
            (3, "절제술 vs 색전술 vs 방사선 — 선택의 기준", None,
             "종양 위치·간 기능·환자 상태가 만드는 선택의 분기점"),
            (4, "면역치료 1차 시대 — atezolizumab+bevacizumab과 그 이후", None,
             "IMbrave150 이후 1차 옵션의 변화, 적응증과 부작용"),
            (5, "간이식 — 적응증과 대기 기간", None,
             "Milan / UCSF criteria, 한국의 KONOS 배정, 살아있는 기증자"),
            (6, "AFP(알파태아단백) — 정상범위와 간암 의심 기준", "/알파태아단백/",
             "AFP 단독 상승의 의미, 간암 검진에서의 역할"),
            (7, "B형간염 환자가 6개월마다 간암 검진을 받아야 하는 이유", "/B형간염-간암검진/",
             "종양 배가시간과 6개월 주기의 근거, 초음파+AFP+PIVKA-II 조합"),
            (8, "지방간에서 간암까지 — 비알코올성 간질환의 간암 위험", "/지방간-간암/",
             "MASLD-MASH-간경변-간암 경로와 검진 시작 시점"),
            (9, "간암 재발 추적 — 첫 5년의 일정", None,
             "치료 후 영상·종양표지자 일정, 재발 패턴별 대응"),
            (10, "간암 환자가 알아야 할 식이·일상", None,
             "치료 중 영양 관리, 술·약·영양제 점검"),
        ],
    },
    "간경화": {
        "num": "02",
        "intro": "대상성 vs 비대상성의 분기, Child-Pugh·MELD 점수의 의미, 식도정맥류·복수·간성혼수·간신증후군 같은 합병증의 첫 신호와 관리, 간이식 대상자 평가까지. 외래에서 자주 받는 질문 중심으로 정리합니다.",
        "topics": [
            (1, "대상성 vs 비대상성 간경변 — 어디서 갈라지는가", None,
             "복수·정맥류 출혈·간성혼수·황달의 첫 등장이 만드는 단계 변화"),
            (2, "Child-Pugh와 MELD — 점수가 의미하는 것", None,
             "두 점수의 사용 맥락 차이, 한계, 환자에게 설명하는 법"),
            (3, "식도정맥류 — 첫 신호와 예방적 결찰", None,
             "내시경 검진 주기, 1·2·3차 예방의 차이"),
            (4, "복수 — 단계별 관리", None,
             "식이·이뇨제·천자, SBP 예방, 난치성 복수의 옵션"),
            (5, "간성혼수 — 외래에서 알아채는 신호", None,
             "수면 패턴 변화, 손떨림, 가족이 먼저 알아채는 변화"),
            (6, "간신증후군 — 진단과 즉각 대응", None,
             "AKI 기준, 알부민+terlipressin/노르에피네프린, 간이식 brigade"),
            (7, "간경변 영양·근감소증(sarcopenia) 관리", None,
             "단백질 섭취·야식·운동 — 흔한 오해와 실제 권고"),
            (8, "간이식 평가 — 누가, 언제 시작하나", None,
             "MELD 임계값, 동시 평가, KONOS 등록의 흐름"),
            (9, "간경변 환자가 피해야 할 약·영양제", None,
             "NSAIDs, 일부 한약·건강기능식품, 진정제 — 외래에서 점검하는 목록"),
            (10, "간기능검사가 정상인데 간경변? — 진행된 간경변의 함정", None,
             "혈액검사 정상범위에 가려진 간경변, 영상·섬유화 평가의 역할"),
        ],
    },
    "B형간염": {
        "num": "03",
        "intro": "치료 시작 기준과 중단 조건, 검사결과 해석, 가족 검사, 결혼·임신·수유, 항바이러스제 선택과 functional cure까지. 외래에서 가장 자주 받는 질문 중심으로 정리합니다.",
        "topics": [
            (1, "B형간염 약을 평생 먹어야 하나요? — 치료 시작 기준과 중단 조건", "/B형간염-평생약/",
             "HBV DNA·ALT 기준, TDF·TAF·ETV 비교, 임의 중단 위험"),
            (2, "B형간염 검사 결과지 해석 — HBsAg·HBeAg·anti-HBs", "/B형간염-검사결과/",
             "5개 표지자 의미와 조합별 해석표"),
            (3, "B형간염 보균자와 결혼·임신·수유", "/B형간염-결혼-임신/",
             "HBIG+백신 수직감염 예방, TDF 임신 안전성"),
            (4, "가족 중 B형간염 환자가 있다면 받아야 할 검사 3가지", "/가족-B형간염-검사/",
             "HBsAg·anti-HBs·anti-HBc, PEP, 자녀 예방"),
            (5, "B형간염 백신 — 누가, 언제, 몇 번", None,
             "성인·소아 일정, 무반응자 대응, 면역저하 상태에서의 boost"),
            (6, "HBeAg 양성 vs 음성 — 무엇이 다른가", None,
             "두 phase의 자연사 차이, 치료 적응증·기간의 차이"),
            (7, "항바이러스제 비교 — TDF · TAF · ETV", None,
             "신기능·골밀도 차이, 임신·수유, 약가, 전환의 기준"),
            (8, "B형간염 functional cure — 어디까지 와 있나", None,
             "siRNA·capsid inhibitor·면역조절제 임상의 현 위치"),
            (9, "항암치료·면역억제제와 B형간염 재활성화", None,
             "재활성화 위험 분류, 예방적 항바이러스제, 모니터링"),
            (10, "C형간염은 약으로 완치됩니다 — DAA 치료 8주 완치율 97%", "/C형간염-완치-DAA/",
             "마비렛·엡클루사 비교, SVR12 완치 기준 — C형 단독 글, 참고용"),
        ],
    },
    "지방간": {
        "num": "04",
        "intro": "NAFLD→MASLD 명명 변경부터 단순 지방간과 지방간염의 분기, 정밀검사 흐름, 운동·식이·약물의 효과, 회복 6개월 패턴까지. 환자 입장에서 매 단계 무엇이 의미 있는지 정리합니다.",
        "topics": [
            (1, "NAFLD가 MASLD로 바뀐 이유 — 새 진단명이 의미하는 것", "/대사이상지방간-MASLD/",
             "MASLD·MASH 새 명칭 배경, 진단 기준 변화"),
            (2, "술을 전혀 안 마시는데 지방간이라고요? — 비음주성 지방간의 원인", "/술-안마셔도-지방간/",
             "인슐린 저항성, 과당, 수면 무호흡 등"),
            (3, "지방간 치료 — 운동·식이·약물, 무엇이 얼마나 효과 있나", "/지방간-치료/",
             "체중 5%·7%·10% 감량의 효과 차이, 약물 옵션"),
            (4, "지방간에 좋은 음식·피해야 할 음식 — 커피는 정말 효과가 있을까", "/지방간-음식/",
             "지중해식 식단, 커피·오메가-3 효과"),
            (5, "지방간 회복, 6개월 후 어떻게 달라지나 — 단계별 변화", "/지방간-회복-6개월/",
             "체중 감량에 따른 지방 감소 시점, 섬유화 역전 가능성"),
            (6, "지방간 진단 후, 섬유화 정밀검사가 필요한 사람은 누구인가", "/지방간-정밀검사/",
             "FIB-4, Fibroscan, MRE — 단계별 평가 흐름"),
            (7, "lean MASLD — 마른 사람의 지방간", None,
             "정상 BMI에서의 지방간, 동양인 cut-off, 위험 인자 점검"),
            (8, "resmetirom과 차세대 지방간 약물", None,
             "MAESTRO 시험 결과, 적응증, 한국 보험 현황"),
            (9, "지방간염(MASH) — 단순 지방간과 무엇이 다른가", None,
             "조직 변화, 진행 위험, 진단·치료의 분기점"),
            (10, "SGLT2·GLP-1 작용제와 지방간", None,
             "당뇨 동반 환자의 지방간 호전, 비당뇨 환자에서의 가능성"),
        ],
    },
    "간수치": {
        "num": "05",
        "intro": "AST·ALT·GGT의 차이부터 빌리루빈·알부민·PT 같은 합성능 지표, AFP·PIVKA-II 종양표지자, Fibroscan 수치까지. 결과지 한 줄을 어떻게 읽는지를 정리합니다.",
        "topics": [
            (1, "건강검진 간수치(AST·ALT) 높음, 첫 단계로 무엇을 봐야 할까", "/간수치-높음/",
             "정상 범위, 흔한 원인 5가지, 재검 시점"),
            (2, "AST·ALT·GGT 차이 — 어느 수치가 어떤 간 문제를 의미하나", "/간수치-종류-차이/",
             "세 효소의 출처, 비율 패턴, GGT 단독 상승의 의미"),
            (3, "Fibroscan(간섬유화 스캔) 수치 읽는 법 — F0부터 F4까지", "/간섬유화스캔-수치/",
             "kPa 값 해석, CAP 지방량 수치"),
            (4, "빌리루빈 — 직접·간접 빌리루빈의 차이", None,
             "용혈성·간세포성·담도성을 가르는 패턴"),
            (5, "알부민·PT(INR) — 간의 합성능을 보는 방법", None,
             "간 기능을 가장 직접적으로 보는 두 수치의 의미와 시간"),
            (6, "ALP·GGT — 담도 막힘 vs 간세포 손상", None,
             "두 수치의 조합으로 담도 vs 간세포를 어떻게 가르나"),
            (7, "약물·영양제·한약 — 간 손상 가능성 점검", None,
             "외래에서 자주 만나는 간독성 원인, 사진으로 정리하는 법"),
            (8, "간수치가 정상인데도 간경변일 수 있다 — 진행된 간경변의 함정", None,
             "혈액검사가 안심을 주지 못하는 상황과 영상 평가의 역할"),
            (9, "PIVKA-II — 간암 종양표지자의 또 다른 축", None,
             "AFP와의 보완 관계, 와파린 복용의 영향"),
            (10, "간생검 — 언제 필요한가", None,
             "비침습 검사로 결정 못하는 상황, 합병증과 대안"),
        ],
    },
}

NAV = '''<header class="site-header">
  <div class="inner">
    <a href="/" class="brand-mark">Hepatology<em> Note</em></a>
    <nav class="site-nav">
      <a href="/소개/">소개</a>
      <a href="/논문/">논문</a>
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
      <a href="/논문/">논문</a>
      <a href="/updates/">Updates</a>
    </div>
    <div class="col">
      <strong>외부 링크</strong>
      <a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a>
    </div>
    <div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div>
  </div>
</footer>'''

ALL_SERIES = list(SERIES.keys())

def esc(s): return htmllib.escape(s or "")

def render_topics(topics):
    out = ['<ul class="topic-list">']
    for n, title, slug, desc in topics:
        if slug:
            out.append(f'  <li class="published">')
            out.append(f'    <a href="{esc(slug)}">')
            out.append(f'      <span class="num">{n:02d}</span>')
            out.append(f'      <div class="body">')
            out.append(f'        <h3>{esc(title)}</h3>')
            out.append(f'        <p>{esc(desc)}</p>')
            out.append(f'      </div>')
            out.append(f'      <span class="status published">읽기 →</span>')
            out.append(f'    </a>')
            out.append(f'  </li>')
        else:
            out.append(f'  <li class="draft">')
            out.append(f'    <a>')
            out.append(f'      <span class="num">{n:02d}</span>')
            out.append(f'      <div class="body">')
            out.append(f'        <h3>{esc(title)}</h3>')
            out.append(f'        <p>{esc(desc)}</p>')
            out.append(f'      </div>')
            out.append(f'      <span class="status draft">준비 중</span>')
            out.append(f'    </a>')
            out.append(f'  </li>')
    out.append('</ul>')
    return "\n".join(out)

def render_other_series(current):
    others = [s for s in ALL_SERIES if s != current] + ["updates"]
    items = []
    for s in others:
        if s == "updates":
            items.append('<a href="/updates/" class="series-tile"><span class="num">SERIES 06</span><h3>최신 지견</h3><p>의료진·전공의 대상 노트.</p></a>')
        else:
            num = SERIES[s]["num"]
            display = "B형 간염" if s == "B형간염" else ("간수치 이상" if s == "간수치" else s)
            items.append(f'<a href="/{s}/" class="series-tile"><span class="num">SERIES {num}</span><h3>{display}</h3><p>{esc(SERIES[s]["intro"][:60])}…</p></a>')
    return '<div class="series-grid">\n  ' + "\n  ".join(items) + '\n</div>'

def render_series(name, spec):
    num = spec["num"]
    display = "B형 간염" if name == "B형간염" else ("간수치 이상" if name == "간수치" else name)
    intro = spec["intro"]
    topics = spec["topics"]
    published_count = sum(1 for t in topics if t[2])
    draft_count = len(topics) - published_count

    title_full = f"{display} — Hepatology Note"
    desc_meta = f"{display} 시리즈 — {intro[:80]}…"
    canonical = f"https://drshin.kr/{name}/"

    html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title_full)}</title>
<meta name="description" content="{esc(desc_meta)}">
<link rel="canonical" href="{canonical}">
<meta name="author" content="신현재">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title_full)}">
<meta property="og:description" content="{esc(desc_meta)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"CollectionPage","@id":"{canonical}#webpage","url":"{canonical}","name":"{esc(display)}","description":"{esc(intro)}","inLanguage":"ko","author":{{"@id":"https://drshin.kr/#author"}},"isPartOf":{{"@id":"https://drshin.kr/#website"}}}},
{{"@type":"Person","@id":"https://drshin.kr/#author","name":"신현재","jobTitle":"서울대학교병원 소화기내과 · 간암센터","worksFor":{{"@type":"Hospital","name":"서울대학교병원","url":"https://www.snuh.org/"}},"image":"https://drshin.kr/assets/img/author/drshin.jpg","url":"https://drshin.kr/소개/"}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},{{"@type":"ListItem","position":2,"name":"{esc(display)}","item":"{canonical}"}}]}}
]}}
</script>
</head>
<body>
{NAV}

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>{esc(display)}</span></nav>

<p class="series-label">SERIES {num}</p>
<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:34px;letter-spacing:-0.025em;font-weight:600;margin:0 0 12px">{esc(display)}</h1>
<p class="series-intro">{esc(intro)}</p>
<div class="series-meta">
  <span>총 {len(topics)} 토픽</span>
  <span>· 게시 {published_count}편</span>
  <span>· 준비 중 {draft_count}편</span>
</div>

{render_topics(topics)}

<h2 style="margin-top:64px;font-size:14px;letter-spacing:0.1em;color:var(--muted);text-transform:uppercase;border-bottom:1px solid var(--line);padding-bottom:8px;font-weight:600">다른 시리즈</h2>
{render_other_series(name)}

</main>

{FOOTER}
</body>
</html>
'''
    return html

for name, spec in SERIES.items():
    out = ROOT / name / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_series(name, spec), encoding="utf-8")
    print(f"  Wrote {out}")

print("Done.")
