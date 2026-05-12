"""Build 작성일 (publish dates) for all 세부주제/사례/최신지견 pages + add 최근 작성글 box to main index.

- Date range: 2025-01-01 to 2026-05-10 (random per page, deterministic seeded by slug)
- Updates pages: 작성일 must be after paper publication year (parsed from slug suffix)
- Updates published_time meta + JSON-LD datePublished + visible 작성일 markup
- Main index.html gets top-5 recent posts box with 'New' badges (top 2)
"""
import os
import re
import json
import random
import hashlib
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(r"C:\Users\R\Dropbox\drshin.kr")

START = date(2025, 1, 1)
END = date(2026, 5, 10)

HUB_SLUGS = {
    "간암", "간경화", "B형간염", "지방간", "간수치",
    "C형간염", "자가면역간염", "간양성종양",
    "CC", "케이스", "updates", "keywords", "guide",
    "소개", "논문", "연구",
    "assets", "private-figures", "tag", ".tools", ".git",
}

CATEGORY_LABEL = {"세부주제": "세부주제", "사례": "사례", "최신지견": "최신 지견"}
CATEGORY_HREF_PREFIX = {
    "세부주제": "/{slug}/",
    "사례": "/케이스/{slug}/",
    "최신지견": "/updates/{slug}/",
}


def page_seed(slug):
    return int(hashlib.md5(slug.encode("utf-8")).hexdigest()[:8], 16)


def random_date(slug, min_date=START, max_date=END):
    rng = random.Random(page_seed(slug))
    span = max(0, (max_date - min_date).days)
    return min_date + timedelta(days=rng.randint(0, span))


def updates_min_date(slug):
    """For updates pages, constrain 작성일 >= paper year (Jan 1)."""
    m = re.search(r"-(\d{4})$", slug)
    if not m:
        return START
    year = int(m.group(1))
    if year < 2025:
        return START
    return date(min(year, END.year), 1, 1)


def korean_date(d):
    return f"{d.year}년 {d.month}월 {d.day}일"


def collect_pages():
    pages = []
    # 세부주제: root level non-hub folders
    for p in ROOT.iterdir():
        if not p.is_dir() or p.name.startswith("."):
            continue
        if p.name in HUB_SLUGS:
            continue
        idx = p / "index.html"
        if idx.exists():
            pages.append(("세부주제", p.name, idx))
    # 사례: /케이스/{slug}/
    cases_dir = ROOT / "케이스"
    if cases_dir.exists():
        for p in cases_dir.iterdir():
            if not p.is_dir():
                continue
            idx = p / "index.html"
            if idx.exists():
                pages.append(("사례", p.name, idx))
    # 최신지견: /updates/{slug}/
    updates_dir = ROOT / "updates"
    if updates_dir.exists():
        for p in updates_dir.iterdir():
            if not p.is_dir():
                continue
            idx = p / "index.html"
            if idx.exists():
                pages.append(("최신지견", p.name, idx))
    return pages


PUBLISH_DATE_BLOCK_RE = re.compile(
    r"\n?<p class=\"publish-date\">[^<]*(?:<time[^>]*>[^<]*</time>)?[^<]*</p>", re.DOTALL
)


def inject_date(html_path, d):
    """Inject visible 작성일 + update meta + JSON-LD datePublished."""
    html = html_path.read_text(encoding="utf-8")
    iso = d.isoformat()
    iso_full = f"{iso}T09:00:00+09:00"
    display = korean_date(d)
    visible = f'\n<p class="publish-date">작성일 <time datetime="{iso}">{display}</time></p>'

    # 1) Update meta tag <meta property="article:published_time" content="...">
    if 'property="article:published_time"' in html:
        html = re.sub(
            r'<meta property="article:published_time" content="[^"]*">',
            f'<meta property="article:published_time" content="{iso_full}">',
            html,
        )
    else:
        # Insert near other og: tags (after og:url)
        html = re.sub(
            r'(<meta property="og:url"[^>]*>)',
            r'\1\n<meta property="article:published_time" content="' + iso_full + '">',
            html, count=1,
        )

    # 2) Update JSON-LD datePublished (preserve dateModified)
    # Pattern: "datePublished":"YYYY-MM-DDTHH:MM:SS+09:00"
    html = re.sub(
        r'"datePublished":"[^"]*"',
        f'"datePublished":"{iso_full}"',
        html,
    )

    # 3) Inject/replace visible 작성일 markup right after first </h1>
    # Remove existing publish-date block if present
    html = PUBLISH_DATE_BLOCK_RE.sub("", html)
    # Insert after first </h1>
    html, n = re.subn(r"(</h1>)", r"\1" + visible, html, count=1)
    if n == 0:
        # No </h1> found (rare); skip visible insertion
        print(f"  [WARN] no </h1> in {html_path.relative_to(ROOT)}, skipped visible inject")

    html_path.write_text(html, encoding="utf-8")


def extract_title(html_path):
    html = html_path.read_text(encoding="utf-8")
    m = re.search(r"<title>([^<]+)</title>", html)
    if not m:
        return html_path.parent.name
    title = m.group(1)
    # Strip " — Hepatology Note" suffix
    title = re.sub(r"\s*—\s*Hepatology Note\s*$", "", title)
    return title.strip()


def build_recent_posts_box(top5):
    """top5: list of (cat, slug, title, date)"""
    items = []
    for i, (cat, slug, title, d) in enumerate(top5):
        href = CATEGORY_HREF_PREFIX[cat].format(slug=slug)
        is_new = i < 2  # Top 2 get NEW badge
        new_html = '<span class="recent-new">NEW</span>' if is_new else ""
        cat_html = f'<span class="recent-cat recent-cat-{cat}">{CATEGORY_LABEL[cat]}</span>'
        date_html = f'<time class="recent-date" datetime="{d.isoformat()}">{korean_date(d)}</time>'
        items.append(
            f'  <li>{new_html}{cat_html}<a class="recent-link" href="{href}">{title}</a>{date_html}</li>'
        )
    body = "\n".join(items)
    return f"""<section class="recent-posts" aria-label="최근 작성글">
  <h2 class="recent-posts-title">최근 작성글</h2>
  <ul class="recent-posts-list">
{body}
  </ul>
</section>
"""


def update_main_index(top5):
    main = ROOT / "index.html"
    html = main.read_text(encoding="utf-8")
    box = build_recent_posts_box(top5)

    # Remove existing recent-posts section if present
    html = re.sub(
        r'<section class="recent-posts"[\s\S]*?</section>\s*',
        "",
        html,
    )
    # Insert before <div class="series-grid ...">
    html, n = re.subn(
        r'(<div class="series-grid[^"]*">)',
        box + r"\1",
        html,
        count=1,
    )
    if n == 0:
        print("  [WARN] series-grid anchor not found in main index.html")
    main.write_text(html, encoding="utf-8")


CSS_BLOCK = """
/* publish-date (작성일) — 2026-05-12 */
.publish-date{font-size:13px;color:var(--muted);margin:6px 0 18px;letter-spacing:0.02em;font-weight:400}
.publish-date time{color:var(--muted)}
@media (max-width:680px){.publish-date{font-size:12.5px;margin:4px 0 16px}}
/* 최근 작성글 box */
.recent-posts{margin:32px 0 28px;padding:18px 22px 14px;background:#fff;border:1px solid var(--line);border-radius:12px}
.recent-posts-title{font-size:15.5px;margin:0 0 12px;color:var(--accent);letter-spacing:0.02em}
.recent-posts-list{list-style:none;padding:0;margin:0}
.recent-posts-list li{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px dashed var(--line);font-size:14.5px;line-height:1.5}
.recent-posts-list li:last-child{border-bottom:0}
.recent-new{display:inline-block;background:var(--accent);color:#fff;font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:4px;letter-spacing:0.05em;flex-shrink:0}
.recent-cat{display:inline-block;font-size:11.5px;padding:2px 8px;background:#f3f1ec;border:1px solid var(--line);border-radius:99px;color:var(--muted);flex-shrink:0;letter-spacing:0.02em}
.recent-cat-사례{background:#f6efe6;border-color:#d8c8a8}
.recent-cat-최신지견{background:#eaf1ee;border-color:#a8c8b8}
.recent-link{flex:1;color:#222;text-decoration:none;border-bottom:1px solid transparent;transition:border-color .12s,color .12s;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.recent-link:hover{color:var(--accent);border-bottom-color:var(--accent)}
.recent-date{font-size:12px;color:var(--muted);flex-shrink:0;letter-spacing:0.02em;font-variant-numeric:tabular-nums}
@media (max-width:680px){
  .recent-posts{padding:14px 16px 10px;margin:24px 0 20px}
  .recent-posts-list li{font-size:13.5px;gap:8px;flex-wrap:wrap}
  .recent-cat,.recent-new{font-size:10.5px}
  .recent-link{flex:1 1 100%;order:3;white-space:normal}
  .recent-date{order:4;flex-shrink:0;font-size:11.5px}
}
/* end 작성일 / 최근 작성글 */
"""


def update_css():
    css_path = ROOT / "style.css"
    css = css_path.read_text(encoding="utf-8")
    # Remove existing block (guarded by markers)
    css = re.sub(
        r'\n/\* publish-date \(작성일\)[\s\S]*?/\* end 작성일 / 최근 작성글 \*/\n',
        "\n",
        css,
    )
    # Append new block
    if not css.endswith("\n"):
        css += "\n"
    css += CSS_BLOCK
    css_path.write_text(css, encoding="utf-8")


def main():
    pages = collect_pages()
    print(f"Total pages found: {len(pages)}")
    by_cat = {}
    for cat, slug, _ in pages:
        by_cat[cat] = by_cat.get(cat, 0) + 1
    for k, v in sorted(by_cat.items()):
        print(f"  {k}: {v}")

    # Inject dates
    results = []
    for cat, slug, path in pages:
        min_d = updates_min_date(slug) if cat == "최신지견" else START
        d = random_date(slug, min_date=min_d, max_date=END)
        inject_date(path, d)
        results.append((cat, slug, path, d))

    # Top 5 by date desc (with title)
    results.sort(key=lambda x: x[3], reverse=True)
    top5 = []
    for cat, slug, path, d in results[:5]:
        title = extract_title(path)
        top5.append((cat, slug, title, d))

    print("\nTop 5 most recent:")
    for i, (cat, slug, title, d) in enumerate(top5):
        marker = "[NEW]" if i < 2 else "     "
        print(f"  {marker} {d} | {cat:8s} | {title}")

    # Update main index + CSS
    update_main_index(top5)
    update_css()
    print("\n[OK] Main index + CSS updated.")


if __name__ == "__main__":
    main()
