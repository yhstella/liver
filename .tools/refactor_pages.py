"""End-to-end page refactor pass:

1. Clean clutter
   - Remove SERIES XX pill labels from topic pages (keep only on series hubs)
   - Remove author-box from topic pages (keep on home / 소개)
   - Remove existing hand-curated "관련 가이드" / "관련 케이스" / "같이 읽으면" sections
   - Strip Korean parens expansions inside the breadcrumb final segment

2. Inject per-page keyword tag chips just under H1
   - Visible as small chips for visitor scannability
   - Also as <meta name="keywords">

3. Inject auto-generated "관련 글" section at end of <main>
   - Top 4 pages by Jaccard keyword overlap

Idempotent: uses <!-- tags --> ... <!-- /tags --> and
<!-- related --> ... <!-- /related --> markers.
"""
from __future__ import annotations
import html as htmllib
import re
import sys, os
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(__file__))
from page_keywords import PAGE_KEYWORDS

ROOT = Path(__file__).resolve().parent.parent

# Pages that are hubs / admin — preserve author-box, series labels here
HUB_PAGES = {
    "(home)", "소개", "연구", "논문", "guide", "updates",
    "간암", "간경화", "B형간염", "지방간", "간수치", "케이스",
}

TAGS_OPEN = "<!-- tags -->"
TAGS_CLOSE = "<!-- /tags -->"
TAGS_RE = re.compile(re.escape(TAGS_OPEN) + r".*?" + re.escape(TAGS_CLOSE), re.DOTALL)

REL_OPEN = "<!-- related -->"
REL_CLOSE = "<!-- /related -->"
REL_RE = re.compile(re.escape(REL_OPEN) + r".*?" + re.escape(REL_CLOSE), re.DOTALL)


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
    return raw


def get_page_id(text: str) -> str:
    m = re.search(r'<span class="page-id">([^<]+)</span>', text)
    return m.group(1).strip() if m else ""


# === Cleanup ===
SERIES_LABEL_RE = re.compile(r'<p class="series-label">[^<]*</p>\s*', re.DOTALL)
AUTHOR_BOX_RE = re.compile(r'<aside class="author-box">.*?</aside>\s*', re.DOTALL)
RELATED_ASIDE_RE = re.compile(r'<aside class="related">.*?</aside>\s*', re.DOTALL)
# Hand-curated "관련 케이스" boxes I added earlier (style attribute marker)
RELATED_CASE_BOX_RE = re.compile(
    r'<section style="margin:48px 0 32px;padding:18px 22px;background:#f5f9f7;border-radius:8px">\s*'
    r'<h2[^>]*>관련 케이스</h2>.*?</section>\s*',
    re.DOTALL,
)


def simplify_breadcrumb(text: str) -> str:
    """Strip Korean parens expansions in the final breadcrumb segment.
    Example: <span>BCLC(Barcelona Clinic Liver Cancer) 병기</span> →
             <span>BCLC 병기</span>"""
    def fix(m):
        inner = m.group(1)
        cleaned = re.sub(r"\([^()]+\)", "", inner)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return f"<span>{cleaned}</span>"
    # Only the LAST <span>...</span> inside the crumb (the page title segment)
    crumb_re = re.compile(r'(<nav class="crumb">.*?</nav>)', re.DOTALL)
    def replace_crumb(m):
        cr = m.group(1)
        # Find last <span>...</span> NOT page-id
        spans = list(re.finditer(r"<span(?![^>]*class)([^>]*)>([^<]+)</span>", cr))
        if not spans:
            return cr
        last = spans[-1]
        cleaned = re.sub(r"\([^()]+\)", "", last.group(2))
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        new_span = f"<span{last.group(1)}>{cleaned}</span>"
        return cr[:last.start()] + new_span + cr[last.end():]
    return crumb_re.sub(replace_crumb, text)


def cleanup(text: str, slug: str) -> str:
    is_hub = slug in HUB_PAGES
    text = simplify_breadcrumb(text)
    if not is_hub:
        text = SERIES_LABEL_RE.sub("", text)
        text = AUTHOR_BOX_RE.sub("", text)
        text = RELATED_ASIDE_RE.sub("", text)
        text = RELATED_CASE_BOX_RE.sub("", text)
    return text


# === Tag chips ===
def tag_chips_html(keywords: list[str]) -> str:
    if not keywords:
        return ""
    chips = "".join(
        f'<a href="/keywords/?k={quote(k)}" class="tag-chip">{esc(k)}</a>'
        for k in keywords
    )
    return f'{TAGS_OPEN}\n<p class="tag-row">{chips}</p>\n{TAGS_CLOSE}'


def insert_tags(text: str, keywords: list[str]) -> str:
    text = TAGS_RE.sub("", text)
    chips = tag_chips_html(keywords)
    if not chips:
        return text
    # Insert after first </h1>
    m = re.search(r"</h1>", text)
    if not m:
        return text
    return text[:m.end()] + "\n" + chips + "\n" + text[m.end():]


def update_meta_keywords(text: str, keywords: list[str]) -> str:
    if not keywords:
        return text
    kw_str = ", ".join(keywords)
    new_meta = f'<meta name="keywords" content="{esc(kw_str)}">'
    if re.search(r'<meta\s+name="keywords"', text):
        return re.sub(r'<meta\s+name="keywords"[^>]*>', new_meta, text, count=1)
    # Insert after <meta name="description"> if present
    m = re.search(r'<meta\s+name="description"[^>]*>', text)
    if m:
        return text[:m.end()] + "\n" + new_meta + text[m.end():]
    # Else after <title>
    m = re.search(r'</title>', text)
    if m:
        return text[:m.end()] + "\n" + new_meta + text[m.end():]
    return text


# === Related pages ===
def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def find_related(slug: str, top_n: int = 4) -> list[tuple[str, float]]:
    own = set(PAGE_KEYWORDS.get(slug, []))
    if not own:
        return []
    scored = []
    for other_slug, kw in PAGE_KEYWORDS.items():
        if other_slug == slug:
            continue
        s = jaccard(own, set(kw))
        if s > 0:
            scored.append((other_slug, s))
    scored.sort(key=lambda x: (-x[1], x[0]))
    return scored[:top_n]


def related_section_html(related: list[tuple[str, float]], titles: dict[str, tuple[str, str]]) -> str:
    if not related:
        return ""
    items = []
    for slug, _score in related:
        title, pid = titles.get(slug, (slug, ""))
        url = page_url(slug)
        pid_html = f' <span class="rel-pid">{esc(pid)}</span>' if pid else ""
        items.append(f'<li><a href="{url}">{esc(title)}</a>{pid_html}</li>')
    return (
        f"{REL_OPEN}\n"
        '<aside class="related-auto">'
        '<h2>관련 글</h2>'
        '<ul>' + "".join(items) + '</ul>'
        '</aside>\n'
        f"{REL_CLOSE}"
    )


def insert_related(text: str, html_block: str) -> str:
    text = REL_RE.sub("", text)
    if not html_block:
        return text
    # Insert before </main>
    if "</main>" in text:
        return text.replace("</main>", html_block + "\n</main>", 1)
    return text


def main():
    # Pass 1: read titles + page_ids for all known pages
    titles: dict[str, tuple[str, str]] = {}
    for slug in PAGE_KEYWORDS:
        p = page_path(slug)
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        title = get_h1_title(text)
        # Strip parens
        title = re.sub(r"\([^()]+\)", "", title)
        title = re.sub(r"\s+", " ", title).strip()
        # Strip after em-dash explanations (keep main title)
        title = title.split(" — ")[0].strip()
        pid = get_page_id(text)
        titles[slug] = (title, pid)

    n_pages = 0
    for slug, kw in PAGE_KEYWORDS.items():
        p = page_path(slug)
        if not p.exists():
            print(f"  ! missing: {slug}")
            continue
        text = p.read_text(encoding="utf-8")
        new_text = text

        # 1. Cleanup
        new_text = cleanup(new_text, slug)

        # 2. Meta keywords
        new_text = update_meta_keywords(new_text, kw)

        # 3. Tag chips below h1
        new_text = insert_tags(new_text, kw)

        # 4. Related glob
        related = find_related(slug, top_n=5)
        rel_html = related_section_html(related, titles)
        new_text = insert_related(new_text, rel_html)

        if new_text != text:
            p.write_text(new_text, encoding="utf-8")
            n_pages += 1
            print(f"  ok [{len(kw)} kw, {len(related)} rel]: {slug}")
    print(f"Done. {n_pages} pages refactored.")


if __name__ == "__main__":
    main()
