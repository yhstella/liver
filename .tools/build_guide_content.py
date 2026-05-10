"""Render plaintext guide HTML reflecting current IA.

Writes to .tools/guide_content.html which then gets encrypted by build_guide.js
into guide/index.html.

Reads page_keywords.py as authoritative slug list.
"""
from __future__ import annotations
import html as htmllib
import re
import sys, os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from page_keywords import PAGE_KEYWORDS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / ".tools" / "guide_content.html"


def esc(s: str) -> str:
    return htmllib.escape(s or "")


def page_path(slug: str) -> Path:
    if slug == "index":
        return ROOT / "index.html"
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    if slug.startswith("케이스/"):
        return ROOT / "케이스" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


def page_url(slug: str) -> str:
    from urllib.parse import quote
    if slug == "index":
        return "/"
    if "/" in slug:
        first, rest = slug.split("/", 1)
        return "/" + quote(first, safe="") + "/" + quote(rest, safe="") + "/"
    return "/" + quote(slug, safe="") + "/"


def get_h1(text: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    if not m:
        return ""
    raw = re.sub(r"<[^>]+>", "", m.group(1))
    return re.sub(r"\s+", " ", raw).strip().split(" — ")[0]


def get_page_id(text: str) -> str:
    m = re.search(r'<span class="page-id">([^<]+)</span>', text)
    return m.group(1).strip() if m else ""


def page_meta(slug: str) -> dict:
    p = page_path(slug)
    if not p.exists():
        return {"slug": slug, "title": slug, "pid": "", "exists": False}
    text = p.read_text(encoding="utf-8")
    return {
        "slug": slug,
        "title": get_h1(text),
        "pid": get_page_id(text),
        "url": page_url(slug),
        "kw": PAGE_KEYWORDS.get(slug, []),
        "exists": True,
    }


# === Major topics (대주제) and their pages ===
MAJOR_TOPICS = [
    ("간암", "1", [
        # Topics (1-1 ~ 1-11)
        "간암-진단-첫외래", "간암-BCLC병기", "간암-치료-선택",
        "간암-면역치료-1차", "간암-간이식", "알파태아단백",
        "B형간염-간암검진", "지방간-간암", "간암-재발-추적",
        "간암-식이-일상", "간암-방사선색전술",
    ], [
        # Cases (1-12 ~ 1-26)
        "케이스/건강검진-우연발견-1cm결절", "케이스/B형간염-검진-새결절",
        "케이스/AFP상승-영상음성", "케이스/LR3-모호결절-추적",
        "케이스/PIVKAII-와파린-위양성", "케이스/MASLD-HCC-비만당뇨",
        "케이스/BCLC-A-단일3cm-절제vs소작", "케이스/BCLC-A-다발3개-소작",
        "케이스/ChildB-단일4cm-이식", "케이스/BCLC-B-다발성-TACE",
        "케이스/큰종양-TACE-SBRT-결합", "케이스/문맥침범-AtezoBev",
        "케이스/정맥류출혈이력-STRIDE", "케이스/다운스테이징-이식전환",
        "케이스/절제후-2년재발",
    ]),
    ("간경화", "2", [
        "간경변-대상성-비대상성", "간경변-Child-Pugh-MELD",
        "간경변-식도정맥류", "간경변-복수", "간경변-간성혼수",
        "간경변-간신증후군", "간경변-영양-근감소증",
        "간경변-간이식-평가", "간경변-약물-주의", "간경변-정상수치-함정",
    ], [
        "케이스/첫-식도정맥류-출혈", "케이스/복수-SBP-진단치료",
        "케이스/간성혼수-첫발생", "케이스/ChildC-이식대기",
        "케이스/간경변-새결절-평가",
    ]),
    ("B형 간염", "3", [
        "B형간염-평생약", "B형간염-검사결과", "B형간염-결혼-임신",
        "가족-B형간염-검사", "B형간염-백신",
        "B형간염-HBeAg-양성-음성", "B형간염-항바이러스제-비교",
        "B형간염-functional-cure", "B형간염-재활성화", "C형간염-완치-DAA",
    ], [
        "케이스/직장검진-HBsAg양성", "케이스/임신중-HBsAg발견",
        "케이스/항암치료전-재활성화예방", "케이스/ETV-TAF-전환",
        "케이스/HBeAg-seroclearance-약중단",
    ]),
    ("지방간", "4", [
        "대사이상지방간-MASLD", "술-안마셔도-지방간", "지방간-치료",
        "지방간-음식", "지방간-회복-6개월", "지방간-정밀검사",
        "지방간-lean-MASLD", "지방간-신약-resmetirom",
        "지방간염-MASH", "지방간-SGLT2-GLP1",
    ], [
        "케이스/검진ALT상승-MASLD진단", "케이스/MASLD-F2-GLP1시작",
        "케이스/MASH-F3-당뇨-종합관리", "케이스/lean-MASLD-비만없음",
        "케이스/resmetirom-신약시작",
    ]),
    ("간수치 이상", "5", [
        "간수치-높음", "간수치-종류-차이", "간섬유화스캔-수치",
        "빌리루빈-직접-간접", "알부민-PT-간합성능", "ALP-GGT-담도-간세포",
        "약물성-간손상-DILI", "PIVKA-II-간암마커", "간생검-언제-필요한가",
    ], [
        "케이스/검진ALT상승-원인감별", "케이스/자가면역간염-첫진단",
        "케이스/약물성간손상-항결핵제", "케이스/독성간염-야생버섯",
        "케이스/보충제-ALT상승",
    ]),
    ("C형 간염", "6", [
        "C형간염-진단", "C형간염-완치-DAA", "C형간염-완치후-추적",
    ], [
        "케이스/anti-HCV양성-첫발견", "케이스/C형간염-간경변-새결절",
    ]),
    ("자가면역간염", "7", [
        "자가면역간염-진단", "자가면역간염-치료", "자가면역간염-약중단",
    ], [
        "케이스/AIH-첫진단-여성", "케이스/AIH-약중단-재발",
    ]),
    ("간 양성종양", "8", [
        "간양성종양-진단", "간양성종양-낭종-관리", "간양성종양-혈관종", "간양성종양-FNH-Adenoma",
    ], [
        "케이스/큰낭종-bleomycin-경화요법",
    ]),
]

UPDATES_LIST = [s for s in PAGE_KEYWORDS if s.startswith("updates/")]

CC_LIST = [
    "CC/검진-혹-발견", "CC/지방간-진단", "CC/지방간-심함", "CC/간-통증",
    "CC/간수치-상승", "CC/황달", "CC/B형간염-진단", "CC/C형간염-진단",
    "CC/자가면역간염-의심", "CC/간섬유화-진단", "CC/복부-팽만-복수",
    "CC/AFP-상승", "CC/약물-간손상", "CC/가족-B형간염", "CC/음주-간걱정",
    "CC/피로-식욕부진",
]


def render_topic_card(meta: dict) -> str:
    if not meta["exists"]:
        return (
            f'<div class="card"><div class="card-head"><span class="slug">{esc(meta["slug"])}</span></div>'
            f'<h3 style="color:#c9542b">⚠ 페이지 없음</h3></div>'
        )
    pid = meta.get("pid", "")
    pid_html = f'<span class="slug">{esc(pid)}</span>' if pid else ""
    kw_html = "".join(f'<em>{esc(k)}</em> ' for k in meta.get("kw", []))
    return (
        f'<div class="card">'
        f'<div class="card-head">{pid_html}'
        f'<a href="{meta["url"]}" class="visit" target="_blank">방문 ↗</a></div>'
        f'<h3>{esc(meta["title"])}</h3>'
        f'<div class="block"><strong>키워드</strong><div style="margin-top:4px">{kw_html}</div></div>'
        f'</div>'
    )


def render_section(major: tuple) -> str:
    label, num, topics, cases = major
    topic_metas = [page_meta(s) for s in topics]
    case_metas = [page_meta(s) for s in cases]
    n_topics = sum(1 for m in topic_metas if m["exists"])
    n_cases = sum(1 for m in case_metas if m["exists"])

    topic_cards = "".join(render_topic_card(m) for m in topic_metas)
    case_cards = "".join(render_topic_card(m) for m in case_metas)

    return f'''
<section>
<h2>{esc(num)}. {esc(label)} <span class="count">{n_topics}편 + 케이스 {n_cases}편</span></h2>

<h3 style="font-size:14px;color:var(--muted);letter-spacing:0.04em;text-transform:uppercase;margin:16px 0 10px">세부주제</h3>
<div class="cards">{topic_cards}</div>

{f'<h3 style="font-size:14px;color:var(--muted);letter-spacing:0.04em;text-transform:uppercase;margin:24px 0 10px">케이스</h3><div class="cards">{case_cards}</div>' if case_metas else ''}
</section>
'''


def render_overview() -> str:
    n_topics = sum(1 for major in MAJOR_TOPICS for s in major[2] if page_meta(s)["exists"])
    n_cases = sum(1 for major in MAJOR_TOPICS for s in major[3] if page_meta(s)["exists"])
    n_updates = sum(1 for s in UPDATES_LIST if page_meta(s)["exists"])
    return f'''
<section class="overview">
<h2>현황</h2>
<div class="stats">
<div><strong>{len(MAJOR_TOPICS)}</strong><span>대주제</span></div>
<div><strong>{n_topics}</strong><span>세부주제</span></div>
<div><strong>{n_cases}</strong><span>케이스</span></div>
<div><strong>{n_updates}</strong><span>최신 지견</span></div>
</div>

<h3 style="font-size:14px;color:var(--muted);letter-spacing:0.04em;text-transform:uppercase;margin:18px 0 8px">용어</h3>
<ul class="convention">
<li><strong>대주제</strong>(major topic) — 간암/간경화/B형 간염/지방간/간수치 이상</li>
<li><strong>세부주제</strong>(subtopic) — 각 대주제 내 토픽 페이지</li>
<li><strong>케이스</strong>(case) — 각 대주제 내 임상 시나리오 (가상·익명화)</li>
<li><strong>최신 지견</strong>(updates) — 별도 관리. 본인 1저자 + 주요 가이드라인·RCT</li>
<li><strong>page-id</strong> — <code>1-1</code> 형식. 첫 숫자는 대주제 번호</li>
</ul>
</section>
'''


def render_updates() -> str:
    cards = "".join(render_topic_card(page_meta(s)) for s in sorted(UPDATES_LIST, key=lambda s: page_meta(s).get("pid", "z")))
    return f'''
<section>
<h2>최신 지견 <span class="count">{len(UPDATES_LIST)}편</span></h2>
<div class="cards">{cards}</div>
</section>
'''


def main():
    parts = [render_overview()]
    for major in MAJOR_TOPICS:
        parts.append(render_section(major))
    parts.append(render_updates())
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
