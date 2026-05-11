#!/usr/bin/env python3
"""
gen_draft_pages.py — Render new draft pages (DRAFT, noindex,nofollow)
from a content spec list. Used for Phase 1 batch authoring.

Each spec:
  {
    "slug": "간경변-혈소판감소",
    "hub_path": "/간경화/",         # parent hub URL
    "hub_label": "간경화",         # breadcrumb label
    "section": "간경화",             # article:section meta
    "title": "혈소판 감소",
    "h1": "간경변 환자의 혈소판 감소 — 원인과 임상 결정",
    "desc": "...",
    "keywords": "혈소판감소, 비장기능항진, 간경변",
    "tags": [("혈소판감소", "%ED%98%88%EC%86%8C%ED%8C%90%EA%B0%90%EC%86%8C"), ...],
    "tldr": "...",
    "sections": [("h2", "본문"), ("h2", "다음 섹션"), ...],
    "faqs": [(q, a), ...],
    "refs": ["...", "..."],
    "is_case": False,            # True → /케이스/{slug}/ path, different crumb
    "case_intro": None,          # only if is_case
  }
"""
from __future__ import annotations
from pathlib import Path
import html as htmllib
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent


def esc(s: str) -> str:
    return htmllib.escape(s or "", quote=False)


def tag_chip(label: str, key: str | None = None) -> str:
    k = key or quote(label, safe='')
    return f'<a href="/keywords/?k={k}" class="tag-chip">{esc(label)}</a>'


HEAD = """<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Hepatology Note</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{keywords}">
<meta name="robots" content="noindex,nofollow">
<link rel="canonical" href="https://drshin.kr/{slug_enc}/">
<meta name="author" content="신현재"><meta property="og:type" content="article">
<meta property="og:title" content="{og_title}"><meta property="og:url" content="https://drshin.kr/{slug_enc}/">
<meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="Hepatology Note">
<meta property="article:section" content="{section}">
<link rel="icon" href="/favicon.png"><link rel="stylesheet" href="/style.css">
<script src="/assets/js/figure-zoom.js" defer></script>
<!-- verify:auto:start -->
<meta name="google-site-verification" content="x7NwlcpE-hA8N6Lf1h_i2wKk2RAiSDvv4wUXxV-CwRE">
<meta name="naver-site-verification" content="a978f4b99a9b45749c235f674d9ab6d31950470a">
<!-- verify:auto:end -->
</head><body>
<header class="site-header"><div class="inner"><a href="/" class="brand-mark">Hepatology<em> Note</em></a><nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></nav></div></header>
<main class="wrap">
"""

FOOTER = """</main>
<footer class="site-footer"><div class="inner"><div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p></div><div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a><a href="/keywords/">키워드</a></div><div class="col"><strong>외부 링크</strong><a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개</a></div><div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div></div></footer>
</body></html>
"""


def render_detail(s: dict) -> str:
    slug = s["slug"]
    slug_enc = quote(slug, safe='')
    crumb = (
        f'<nav class="crumb"><a href="/">홈</a> › '
        f'<a href="{s["hub_path"]}">{esc(s["hub_label"])}</a> › '
        f'<span>{esc(s["title"])}</span></nav>\n'
    )

    head = HEAD.format(
        title=esc(s["title"]),
        desc=esc(s["desc"]),
        keywords=esc(s["keywords"]),
        og_title=esc(s.get("og_title") or s["title"]),
        slug_enc=slug_enc,
        section=esc(s["section"]),
    )

    body = [
        crumb,
        "<article>",
        f'<h1>{esc(s["h1"])}</h1>',
        "",
    ]

    if s.get("tags"):
        body.append('<p class="tag-row">' + "".join(tag_chip(t[0], t[1] if len(t) > 1 else None) for t in s["tags"]) + "</p>")
        body.append("")

    if s.get("tldr"):
        body.append(f'<div class="tldr"><strong>핵심 요약</strong>{s["tldr"]}</div>')
        body.append("")

    for sec in s.get("sections", []):
        body.append(f'<h2>{esc(sec["heading"])}</h2>')
        body.append(sec["html"])
        body.append("")

    if s.get("faqs"):
        body.append("<h2>자주 묻는 질문</h2>")
        body.append('<section class="faq-block">')
        for q, a in s["faqs"]:
            body.append(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>')
        body.append("</section>")
        body.append("")

    if s.get("refs"):
        body.append('<section class="references-block"><h2>References</h2><ol class="references">')
        for r in s["refs"]:
            body.append(f'<li>{r}</li>')
        body.append("</ol></section>")

    body.append("</article>")
    return head + "\n".join(body) + FOOTER


def render_case(s: dict) -> str:
    slug = s["slug"]
    path_slug = f'케이스/{slug}'
    slug_enc = quote(path_slug, safe='/')
    crumb = (
        f'<nav class="crumb"><a href="/">홈</a> › '
        f'<a href="{s["hub_path"]}">{esc(s["hub_label"])}</a> › '
        f'<a href="/케이스/">케이스</a> › '
        f'<span>{esc(s["title"])}</span></nav>\n'
    )

    head = HEAD.format(
        title=esc(s["title"]),
        desc=esc(s["desc"]),
        keywords=esc(s["keywords"]),
        og_title=esc(s.get("og_title") or s["title"]),
        slug_enc=slug_enc,
        section=esc(s["section"]),
    )

    body = [
        crumb,
        f'<h1>{esc(s["h1"])}</h1>',
        "",
    ]
    if s.get("tags"):
        body.append('<p class="tag-row">' + "".join(tag_chip(t[0], t[1] if len(t) > 1 else None) for t in s["tags"]) + "</p>")
        body.append("")

    if s.get("case_intro"):
        body.append(f'<div class="case-intro"><p>{s["case_intro"]}</p></div>')
        body.append("")

    for sec in s.get("sections", []):
        body.append('<div class="case-section">')
        body.append(f'<h2>{esc(sec["heading"])}</h2>')
        body.append(sec["html"])
        body.append("</div>")
        body.append("")

    if s.get("teaching"):
        body.append('<div class="case-section"><h2>Teaching Points</h2><ul>')
        for t in s["teaching"]:
            body.append(f'<li>{t}</li>')
        body.append("</ul></div>")

    body.append('<p class="case-disclaimer" style="margin-top:32px;padding:12px 16px;background:#f3f1ec;border-radius:6px;font-size:12.5px;color:var(--muted)">본 케이스는 진료 경험을 바탕으로 한 교육적 합성 시나리오로, 특정 환자의 정보가 아닙니다.</p>')

    return head + "\n".join(body) + FOOTER


def write_pages(specs: list[dict]) -> None:
    n = 0
    for s in specs:
        if s.get("is_case"):
            target = ROOT / "케이스" / s["slug"] / "index.html"
            html = render_case(s)
        elif s.get("is_update"):
            target = ROOT / "updates" / s["slug"] / "index.html"
            html = render_detail(s)
        elif s.get("is_cc"):
            target = ROOT / "CC" / s["slug"] / "index.html"
            html = render_detail(s)
        else:
            target = ROOT / s["slug"] / "index.html"
            html = render_detail(s)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print(f"  wrote {target.relative_to(ROOT)}")
        n += 1
    print(f"Total: {n} pages")
