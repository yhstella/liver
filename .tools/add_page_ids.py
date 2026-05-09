"""Assign sequential X-Y page IDs to topic pages based on series hub order.

Series:
  1 = 간암      (hub: /간암/)
  2 = 간경화    (hub: /간경화/)
  3 = B형간염   (hub: /B형간염/)
  4 = 지방간    (hub: /지방간/)
  5 = 간수치    (hub: /간수치/)
  6 = updates   (hub: /updates/)

For each topic page found in a hub's <ul class="topic-list">, insert
<span class="page-id">[X-Y]</span> at the end of the breadcrumb.
Idempotent — replaces existing .page-id span if present.

Cross-series pages get their canonical ID from the FIRST hub that lists them
(processed in series 1..6 order).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SERIES = [
    (1, "간암"),
    (2, "간경화"),
    (3, "B형간염"),
    (4, "지방간"),
    (5, "간수치"),
    (6, "updates"),
]

PAGE_ID_RE = re.compile(r'\s*<span class="page-id">\[?[\d\-]+\]?</span>')


def extract_topic_slugs(hub_path: Path) -> list[str]:
    """Return slugs in order from the hub's topic-list (or main updates list)."""
    if not hub_path.exists():
        return []
    text = hub_path.read_text(encoding="utf-8")
    # Look for hrefs inside <a href="/SLUG/"> within topic-list
    # Updates hub has different structure; handle separately.
    if hub_path.parent.name == "updates":
        # Match /updates/{slug}/ links
        slugs = re.findall(r'href="/updates/([^/"]+)/"', text)
        # Dedupe preserving order
        seen = set()
        out = []
        for s in slugs:
            if s not in seen:
                seen.add(s)
                out.append("updates/" + s)
        return out
    # Standard hub: extract from topic-list
    m = re.search(r'<ul class="topic-list">(.*?)</ul>', text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    slugs = re.findall(r'href="/([^/"][^"]*?)/"', block)
    seen = set()
    out = []
    for s in slugs:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


def page_path_for(slug: str) -> Path:
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    if slug.startswith("케이스/"):
        return ROOT / "케이스" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


def insert_page_id(html_path: Path, page_id: str) -> bool:
    if not html_path.exists():
        return False
    text = html_path.read_text(encoding="utf-8")
    # Find first <nav class="crumb">...</nav> (or <nav class="crumb">...<span>...</span>)
    crumb_re = re.compile(r'(<nav class="crumb">.*?</nav>)', re.DOTALL)
    m = crumb_re.search(text)
    if not m:
        return False
    crumb = m.group(1)
    # Strip any existing page-id span inside the crumb
    crumb_clean = PAGE_ID_RE.sub("", crumb)
    # Insert page-id just before the closing </nav>
    new_crumb = crumb_clean.replace(
        "</nav>", f' <span class="page-id">{page_id}</span></nav>', 1
    )
    if new_crumb == crumb:
        return False
    new_text = text[:m.start()] + new_crumb + text[m.end():]
    html_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    assigned: dict[str, str] = {}
    for series_num, series_name in SERIES:
        if series_name == "updates":
            hub = ROOT / "updates" / "index.html"
        else:
            hub = ROOT / series_name / "index.html"
        slugs = extract_topic_slugs(hub)
        idx = 0
        for slug in slugs:
            if slug in assigned:
                continue
            idx += 1
            page_id = f"{series_num}-{idx}"
            assigned[slug] = page_id

    n_ok = 0
    for slug, pid in assigned.items():
        path = page_path_for(slug)
        if insert_page_id(path, pid):
            n_ok += 1
            print(f"  [{pid}] {slug}")
        else:
            print(f"  skip {slug} (no crumb or no page)")

    print(f"Done. {n_ok} pages tagged.")


if __name__ == "__main__":
    main()
