"""Build /keywords/index.html — keyword index with filterable page list.

URL pattern: /keywords/?k=BCLC → highlights pages tagged with that keyword.
Client-side filter via URLSearchParams (no JS framework).
"""
from __future__ import annotations
import html as htmllib
import json
import re
import sys, os
from collections import Counter
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
from page_keywords import PAGE_KEYWORDS

ROOT = Path(__file__).resolve().parent.parent


def esc(s: str) -> str:
    return htmllib.escape(s or "")


def page_path(slug: str) -> Path:
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    if slug.startswith("케이스/"):
        return ROOT / "케이스" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


def page_url(slug: str) -> str:
    if slug.startswith("updates/") or slug.startswith("케이스/"):
        first, rest = slug.split("/", 1)
        return "/" + quote(first, safe="") + "/" + quote(rest, safe="") + "/"
    return "/" + quote(slug, safe="") + "/"


def get_h1_title(text: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.DOTALL)
    if not m:
        return ""
    raw = re.sub(r"<[^>]+>", "", m.group(1))
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw.split(" — ")[0].strip()


def get_page_id(text: str) -> str:
    m = re.search(r'<span class="page-id">([^<]+)</span>', text)
    return m.group(1).strip() if m else ""


def main():
    pages = []
    for slug, kws in PAGE_KEYWORDS.items():
        p = page_path(slug)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        title = get_h1_title(text)
        title = re.sub(r"\([^()]+\)", "", title).strip()
        pid = get_page_id(text)
        pages.append({
            "slug": slug,
            "title": title,
            "url": page_url(slug),
            "pid": pid,
            "keywords": kws,
        })

    # Keyword frequencies
    kw_counts = Counter()
    for p in pages:
        for k in p["keywords"]:
            kw_counts[k] += 1
    kw_sorted = sorted(kw_counts.items(), key=lambda x: (-x[1], x[0]))

    # Build HTML
    chip_html = "".join(
        f'<button class="kw-chip" data-kw="{esc(k)}">{esc(k)}<span class="kw-count">{n}</span></button>'
        for k, n in kw_sorted
    )

    rows_html = "".join(
        f'<li class="kw-page" data-keywords="{esc("|".join(p["keywords"]))}">'
        f'<a href="{p["url"]}">{esc(p["title"])}</a>'
        f'<span class="kw-pid">{esc(p["pid"])}</span>'
        f'<span class="kw-tags">{"".join(f"<em>{esc(k)}</em>" for k in p["keywords"])}</span>'
        f'</li>'
        for p in sorted(pages, key=lambda x: x["pid"] or "z")
    )

    page_html = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>키워드 색인 — Hepatology Note</title>
<meta name="description" content="키워드로 페이지 찾기.">
<link rel="canonical" href="https://drshin.kr/keywords/">
<meta name="robots" content="noindex,follow">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#1f6f5c">
<link rel="stylesheet" href="/style.css">
<style>
.kw-chips{{display:flex;flex-wrap:wrap;gap:6px;margin:18px 0 28px}}
.kw-chip{{display:inline-flex;align-items:center;gap:5px;padding:5px 12px;background:#f3f1ec;border:1px solid var(--line);border-radius:99px;color:var(--fg);text-decoration:none;font-size:13px;cursor:pointer;font-family:inherit;transition:background .12s,border-color .12s}}
.kw-chip:hover{{background:var(--accent-soft);border-color:var(--accent);color:var(--accent)}}
.kw-chip.active{{background:var(--accent);border-color:var(--accent);color:#fff}}
.kw-chip.active .kw-count{{color:rgba(255,255,255,0.85)}}
.kw-count{{font-size:11px;color:var(--muted);font-variant-numeric:tabular-nums}}
.kw-list{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.kw-page{{padding:14px 4px;border-bottom:1px solid var(--line);display:grid;grid-template-columns:1fr auto;gap:8px 12px;align-items:baseline}}
.kw-page.hide{{display:none}}
.kw-page a{{color:var(--fg);text-decoration:none;font-weight:500;font-size:15.5px}}
.kw-page a:hover{{color:var(--accent)}}
.kw-pid{{font-family:'JetBrains Mono','SF Mono',Consolas,monospace;font-size:11px;color:#8a6d3b;background:#fdf6e3;padding:1px 7px;border-radius:4px;border:1px solid #f0e3c0;letter-spacing:0.02em;font-weight:500;justify-self:end}}
.kw-tags{{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:5px}}
.kw-tags em{{font-style:normal;font-size:11px;color:var(--muted);background:#f5f5ee;padding:2px 8px;border-radius:99px;border:1px solid var(--line)}}
.kw-empty{{padding:32px 20px;text-align:center;color:var(--muted);font-size:14px}}
</style>
</head>
<body>
<header class="site-header">
  <div class="inner">
    <a href="/" class="brand-mark">Hepatology Note</a>
    <nav class="site-nav"><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a></nav>
  </div>
</header>

<main class="wrap">
<nav class="crumb"><a href="/">홈</a> › <span>키워드</span></nav>

<h1 style="font-family:'Times New Roman',Georgia,serif;font-size:30px;font-weight:600;letter-spacing:-0.02em;margin:8px 0 8px">키워드 색인</h1>
<p class="intro" style="margin:6px 0 18px">키워드를 클릭하면 그 키워드가 달린 페이지만 보입니다. 다시 클릭하면 전체 보기로 돌아갑니다.</p>

<div class="kw-chips" id="kwChips">{chip_html}</div>

<ul class="kw-list" id="kwList">
{rows_html}
</ul>

<div class="kw-empty" id="kwEmpty" style="display:none">선택한 키워드가 달린 페이지가 없습니다.</div>
</main>

<footer class="site-footer">
  <div class="inner">
    <div class="col"><strong>Hepatology Note</strong><p style="margin:4px 0 0;color:var(--muted);font-size:13px">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과</p></div>
    <div class="col"><strong>안내</strong><a href="/소개/">소개</a><a href="/연구/">연구</a><a href="/updates/">Updates</a></div>
    <div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div>
  </div>
</footer>

<script>
(function(){{
  var chips = document.querySelectorAll('.kw-chip');
  var list = document.getElementById('kwList');
  var empty = document.getElementById('kwEmpty');
  var current = null;

  function applyFilter(kw){{
    if (kw === current) {{ kw = null; }}
    current = kw;
    chips.forEach(function(c){{
      c.classList.toggle('active', kw && c.dataset.kw === kw);
    }});
    var rows = list.querySelectorAll('.kw-page');
    var visible = 0;
    rows.forEach(function(r){{
      var keywords = (r.dataset.keywords || '').split('|');
      var match = !kw || keywords.indexOf(kw) >= 0;
      r.classList.toggle('hide', !match);
      if (match) visible++;
    }});
    empty.style.display = (kw && visible === 0) ? 'block' : 'none';
    if (kw) {{
      history.replaceState(null, '', '?k=' + encodeURIComponent(kw));
    }} else {{
      history.replaceState(null, '', location.pathname);
    }}
  }}

  chips.forEach(function(c){{
    c.addEventListener('click', function(){{ applyFilter(c.dataset.kw); }});
  }});

  // Apply ?k= from URL on load
  var params = new URLSearchParams(location.search);
  var initial = params.get('k');
  if (initial) applyFilter(initial);
}})();
</script>
</body>
</html>
'''
    out = ROOT / "keywords" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page_html, encoding="utf-8")
    print(f"Wrote {out} - {len(pages)} pages, {len(kw_sorted)} keywords")


if __name__ == "__main__":
    main()
