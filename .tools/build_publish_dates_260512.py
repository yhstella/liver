"""Build 작성일 (publish dates) for all 세부주제/사례/최신지견 pages + add 최근 작성글 box to main index.

- 기존 페이지: article:published_time 메타가 있으면 그것을 사용
- 신규 페이지 (article:published_time 없음): TODAY 사용
  → 새 글 작성 시 자동으로 홈 '최근 작성글' 상단에 올라감
- Updates pages: 작성일 must be after paper publication year (parsed from slug suffix)
- Updates published_time meta + JSON-LD datePublished + visible 작성일 markup
- Main index.html gets top-5 recent posts box with 'New' badges (top 2, dynamic by JS)

레거시: 한 번 backfill로 채워진 page는 article:published_time이 이미 있으므로 안정.
"""
import os
import re
import json
import hashlib
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 신규 페이지 fallback 날짜 — 스크립트 실행 시점의 오늘
TODAY = date.today()

HUB_SLUGS = {
    "간암", "간경화", "B형간염", "지방간", "간수치",
    "C형간염", "자가면역간질환", "간양성종양",
    "자가면역간염",  # legacy redirect — '최근 작성글'에 노출 금지
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


def korean_date(d):
    # Year wrapped in <span class="y"> so mobile CSS can hide it
    return f'<span class="y">{d.year}년 </span>{d.month}월 {d.day}일'


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
    """top5: list of (cat, slug, title, date). NEW 뱃지는 JS가 datetime 기준 ≤31일에 동적 부여."""
    items = []
    for cat, slug, title, d in top5:
        href = CATEGORY_HREF_PREFIX[cat].format(slug=slug)
        cat_html = f'<span class="recent-cat recent-cat-{cat}">{CATEGORY_LABEL[cat]}</span>'
        date_html = f'<time class="recent-date" datetime="{d.isoformat()}">{korean_date(d)}</time>'
        items.append(
            f'  <li>{cat_html}<a class="recent-link" href="{href}">{title}</a>{date_html}</li>'
        )
    body = "\n".join(items)
    return f"""<section class="recent-posts" aria-label="최근 작성글">
  <h2 class="recent-posts-title">최근 작성글</h2>
  <ul class="recent-posts-list">
{body}
  </ul>
  <script>
  (function(){{
    var NOW = Date.now();
    var WINDOW_MS = 31 * 24 * 60 * 60 * 1000;
    document.querySelectorAll('.recent-posts-list li').forEach(function(li){{
      var t = li.querySelector('time.recent-date');
      if(!t) return;
      var iso = t.getAttribute('datetime');
      if(!iso) return;
      var d = new Date(iso + 'T00:00:00').getTime();
      if(isNaN(d)) return;
      if(NOW - d <= WINDOW_MS){{
        if(!li.querySelector('.recent-new')){{
          var span = document.createElement('span');
          span.className = 'recent-new';
          span.textContent = 'NEW';
          var link = li.querySelector('.recent-link');
          if(link && link.nextSibling){{
            link.parentNode.insertBefore(span, link.nextSibling);
          }}
        }}
      }}
    }});
  }})();
  </script>
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
  .recent-posts{padding:14px 14px 10px;margin:24px 0 20px}
  .recent-posts-list li{font-size:13px;gap:6px;flex-wrap:nowrap}
  .recent-cat{font-size:10px;padding:1px 6px}
  .recent-new{font-size:9.5px;padding:1px 5px}
  .recent-link{flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .recent-date{font-size:10.5px;flex-shrink:0}
  .recent-date .y{display:none}
}
@media (max-width:380px){
  .recent-posts-list li{gap:5px;font-size:12.5px}
  .recent-date{display:none}
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


EXISTING_DATE_RE = re.compile(
    r'<meta property="article:published_time" content="(\d{4}-\d{2}-\d{2})'
)


def read_existing_date(html_path):
    """기존 article:published_time 값을 date로 반환 (없으면 None)."""
    try:
        text = html_path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = EXISTING_DATE_RE.search(text)
    if not m:
        return None
    try:
        y, mo, d = m.group(1).split("-")
        return date(int(y), int(mo), int(d))
    except Exception:
        return None


def main():
    pages = collect_pages()
    print(f"Total pages found: {len(pages)}")
    by_cat = {}
    for cat, slug, _ in pages:
        by_cat[cat] = by_cat.get(cat, 0) + 1
    for k, v in sorted(by_cat.items()):
        print(f"  {k}: {v}")

    # Inject dates — 기존 article:published_time이 있으면 그것을 사용,
    # 없으면 (신규 페이지) TODAY로 자동 설정 → 홈 '최근 작성글' 상단에 자동 노출.
    results = []
    new_dates_assigned = 0
    for cat, slug, path in pages:
        existing = read_existing_date(path)
        if existing is not None:
            d = existing
            # 기존 publish-date <p> visible markup이 없으면 보강 (idempotent)
            text = path.read_text(encoding="utf-8")
            if 'class="publish-date"' not in text:
                inject_date(path, d)
        else:
            d = TODAY  # 신규 페이지: 오늘 날짜 자동 부여
            inject_date(path, d)
            new_dates_assigned += 1
            print(f"  [NEW] {cat}/{slug} → {d} (today)")
        results.append((cat, slug, path, d))
    print(f"  ({new_dates_assigned} pages newly tagged with today's date)")

    # Top 5 by date desc (with title)
    results.sort(key=lambda x: x[3], reverse=True)
    top5 = []
    for cat, slug, path, d in results[:5]:
        title = extract_title(path)
        top5.append((cat, slug, title, d))

    print("\nTop 5 most recent:")
    for i, (cat, slug, title, d) in enumerate(top5):
        marker = "[NEW]" if i < 2 else "     "
        try:
            print(f"  {marker} {d} | {cat:8s} | {title}")
        except UnicodeEncodeError:
            # cp949 콘솔에서 em-dash 등 unicode 문자 fallback
            safe = title.encode('cp949', errors='replace').decode('cp949')
            print(f"  {marker} {d} | {cat:8s} | {safe}")

    # Update main index + CSS
    update_main_index(top5)
    update_css()
    print("\n[OK] Main index + CSS updated.")


if __name__ == "__main__":
    main()
