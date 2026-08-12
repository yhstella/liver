#!/usr/bin/env python3
"""
new_note.py — 단상 글 하나를 새로 만든다. 기본은 noindex 초안.

  python .tools/new_note.py "슬러그" "제목" "한 줄 요약"
  python .tools/new_note.py --publish "슬러그"     # 초안 → 공개 전환

초안(noindex)일 동안은 /단상/ 목록과 sitemap에 나오지 않는다.
글을 다 쓰고 --publish 를 준 뒤 rebuild_seo.py 를 돌리면 목록에 올라간다.
"""
import sys
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "단상"

TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — 단상 — Hepatology Note</title>
<meta name="description" content="{lede}">
<link rel="canonical" href="https://drshin.kr/단상/{slug}/">
<meta name="author" content="신현재">
<meta name="robots" content="noindex,nofollow">
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{lede}">
<meta property="og:url" content="https://drshin.kr/단상/{slug}/">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="Hepatology Note">
<meta property="og:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<meta property="article:published_time" content="{iso}T09:00:00+09:00">
<meta name="twitter:card" content="summary">
<meta name="twitter:image" content="https://drshin.kr/assets/img/author/drshin.jpg">
<link rel="icon" href="/favicon.ico?v=3" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=3">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png?v=3">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=3">
<link rel="manifest" href="/site.webmanifest?v=3">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context":"https://schema.org","@graph":[
{{"@type":"BlogPosting","@id":"https://drshin.kr/단상/{slug}/#post","url":"https://drshin.kr/단상/{slug}/","headline":"{title}","description":"{lede}","inLanguage":"ko","datePublished":"{iso}T09:00:00+09:00","dateModified":"{iso}T09:00:00+09:00","author":{{"@id":"https://drshin.kr/#author"}},"publisher":{{"@id":"https://drshin.kr/#author"}},"isPartOf":{{"@id":"https://drshin.kr/단상/#blog"}}}},
{{"@type":"Person","@id":"https://drshin.kr/#author","name":"신현재","jobTitle":"서울대학교병원 소화기내과 · 간암센터","worksFor":{{"@type":"Hospital","name":"서울대학교병원","url":"https://www.snuh.org/"}},"image":"https://drshin.kr/assets/img/author/drshin.jpg","url":"https://drshin.kr/소개/"}},
{{"@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"홈","item":"https://drshin.kr/"}},{{"@type":"ListItem","position":2,"name":"단상","item":"https://drshin.kr/단상/"}},{{"@type":"ListItem","position":3,"name":"{title}","item":"https://drshin.kr/단상/{slug}/"}}]}}
]}}
</script>
<!-- verify:auto:start -->
<meta name="google-site-verification" content="x7NwlcpE-hA8N6Lf1h_i2wKk2RAiSDvv4wUXxV-CwRE">
<meta name="naver-site-verification" content="a978f4b99a9b45749c235f674d9ab6d31950470a">
<!-- verify:auto:end -->
<script src="/assets/js/search.js" defer></script>
</head>
<body>
<!-- DRAFT -->
<a class="skip-link" href="#content">본문 바로가기</a>
<header class="site-header">
  <div class="inner">
    <a href="/" class="brand-mark">Hepatology<em> Note</em></a>
    <nav class="site-nav">
      <a href="/소개/">소개</a>
      <a href="/연구/">연구</a>
      <a href="/단상/" class="active">단상</a>
      <a href="/updates/">Updates</a>
      <a href="/keywords/">키워드</a>
    </nav>
  </div>
</header>

<!-- hub-bar:auto:start -->
<!-- hub-bar:auto:end -->
<main id="content" class="wrap">
<nav class="crumb"><a href="/">홈</a> › <a href="/단상/">단상</a> › <span>{title}</span></nav>
<article class="note">
<h1>{title}</h1>
<p class="publish-date"><time datetime="{iso}"><span class="y">{y}년 </span>{m}월 {d}일</time></p>
<p class="note-lede">{lede}</p>

<p>여기부터 본문.</p>

</article>

<p class="note-foot" style="color:var(--muted);font-size:13px;margin-top:48px">이 글은 개인적인 생각이며 의학적 조언이 아닙니다.</p>
</main>

<footer class="site-footer">
  <div class="inner">
    <div class="col">
      <strong>Hepatology Note</strong>
      <p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p>
    </div>
    <div class="col">
      <strong>안내</strong>
      <a href="/소개/">소개</a>
      <a href="/연구/">연구</a>
      <a href="/단상/">단상</a><a href="/문의/">문의</a>
    </div>
    <div class="col">
      <strong>외부 링크</strong>
      <a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개</a>
    </div>
    <div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div>
  </div>
</footer>
</body>
</html>
"""


def publish(slug: str) -> int:
    p = NOTES / slug / "index.html"
    if not p.exists():
        print(f"없는 글: {slug}")
        return 1
    s = p.read_text(encoding="utf-8")
    s = s.replace('<meta name="robots" content="noindex,nofollow">',
                  '<meta name="robots" content="index,follow,max-image-preview:large">')
    s = s.replace("<!-- DRAFT -->\n", "")
    p.write_text(s, encoding="utf-8")
    print(f"published: /단상/{slug}/ (run rebuild_seo.py)")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] == "--publish":
        if len(args) < 2:
            print(__doc__)
            return 1
        return publish(args[1])
    if len(args) < 2:
        print(__doc__)
        return 1
    slug, title = args[0], args[1]
    lede = args[2] if len(args) > 2 else ""
    d = date.today()
    target = NOTES / slug
    if target.exists():
        print(f"이미 있습니다: {target}")
        return 1
    target.mkdir(parents=True)
    html = TEMPLATE.format(
        slug=slug, title=title, lede=lede,
        iso=d.isoformat(), y=d.year, m=d.month, d=d.day,
    )
    (target / "index.html").write_text(html, encoding="utf-8")
    print(f"draft created: 단상/{slug}/index.html (noindex)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
