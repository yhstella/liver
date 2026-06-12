#!/usr/bin/env python3
"""
inject_jsonld.py — Inject standardized Article + MedicalWebPage + FAQPage JSON-LD
into every detail page. Idempotent — uses a marker comment so it can be re-run safely.

For each detail page:
- Article (datePublished/dateModified from git, author=신현재, publisher=Hepatology Note)
- MedicalWebPage (medicalAudience=Patient/MedicalProfessional)
- FAQPage IF the page has <details><summary>...</summary><p>...</p></details> blocks
- BreadcrumbList (홈 > 대주제 > 현재)

Marker: <!-- jsonld:auto:start --> ... <!-- jsonld:auto:end -->

Skip: home, 8 hubs, /CC/, /updates/, /케이스/, /keywords/, /소개/, /연구/, /논문/, /guide/.
But /CC/, /updates/, /케이스/ subpages ARE included (detail pages within those sections).
"""
import json
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://drshin.kr"

HUBS_8 = {"간암", "간경화", "B형간염", "C형간염", "지방간", "간수치", "자가면역간질환", "간양성종양"}
LEGACY_REDIRECTS = {"자가면역간염"}  # 옛 hub. redirect-only — JSON-LD 주입 안 함.
SECTION_HUBS = {"updates", "케이스", "CC", "keywords", "소개", "연구"}
EXCLUDE_DIRS = {".git", ".tools", "node_modules", "assets", "guide", "논문", "private-figures"}

MARKER_START = "<!-- jsonld:auto:start -->"
MARKER_END = "<!-- jsonld:auto:end -->"


def git_dates(path: Path):
    """(datePublished, dateModified) ISO. Falls back to now if no git history."""
    try:
        first = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cI", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        ).stdout.strip().split("\n")[-1]
        last = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if first and last:
            return first, last
    except Exception:
        pass
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    return now, now


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.description = ""
        self.canonical = ""
        self.keywords = ""

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            if d.get("name") == "description":
                self.description = d.get("content", "")
            elif d.get("name") == "keywords":
                self.keywords = d.get("content", "")
        elif tag == "link" and d.get("rel") == "canonical":
            self.canonical = d.get("href", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def extract_h1(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return ""
    inner = re.sub(r"<[^>]+>", "", m.group(1))
    return inner.strip()


def extract_breadcrumb_hub(html: str) -> tuple[str, str] | None:
    """Extract (hub_name, hub_url) from breadcrumb if present.
    Looks for: <nav class="crumb"><a href="/">홈</a> › <a href="/HUB/">HUB</a> › ..."""
    m = re.search(r'<nav class="crumb">.*?</nav>', html, re.S)
    if not m:
        return None
    crumb = m.group(0)
    # Find all internal <a> links (including home href="/")
    links = re.findall(r'<a href="(/[^"]*)"[^>]*>([^<]+)</a>', crumb)
    # Exclude home (href="/") from hub candidates
    hub_links = [(h, n) for (h, n) in links if h != "/"]
    if not hub_links:
        return None
    # Last hub link is the immediate parent (hub)
    href, name = hub_links[-1]
    return name.strip(), SITE + href


def extract_faqs(html: str):
    """Extract FAQ Q/A pairs from <details><summary>Q</summary><p>A</p></details>."""
    faqs = []
    # Match details blocks (non-greedy)
    for m in re.finditer(
        r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*(.*?)</details>",
        html, re.S
    ):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        # Answer: take all text inside (strip tags), preserve sentences
        a_html = m.group(2)
        a = re.sub(r"<[^>]+>", " ", a_html)
        a = re.sub(r"\s+", " ", a).strip()
        if q and a and len(a) > 10:
            faqs.append((q, a))
    return faqs


def url_for_page(rel_dir: Path) -> str:
    if str(rel_dir) == ".":
        return f"{SITE}/"
    parts = rel_dir.parts
    encoded = "/".join(quote(p, safe="") for p in parts)
    return f"{SITE}/{encoded}/"


def is_detail_page(rel_dir: Path) -> bool:
    """True if this is a detail (sub) page that should get JSON-LD."""
    if str(rel_dir) == ".":
        return False  # home
    parts = rel_dir.parts
    first = parts[0]
    # 8 hubs themselves — skip (they have own setup)
    if len(parts) == 1 and first in HUBS_8:
        return False
    # Section hubs themselves — skip
    if len(parts) == 1 and first in SECTION_HUBS:
        return False
    # Legacy hub redirects — skip
    if len(parts) == 1 and first in LEGACY_REDIRECTS:
        return False
    # Section sub pages: include (CC/X, updates/X, 케이스/X)
    if first in SECTION_HUBS:
        return True
    # Top-level detail (대주제-부주제 single-segment slug)
    if len(parts) == 1:
        return True
    # Anything else (shouldn't happen often)
    return True


def determine_hub(rel_dir: Path, html: str):
    """Return (hub_name, hub_url) for breadcrumb. Falls back to home."""
    bc = extract_breadcrumb_hub(html)
    if bc:
        return bc
    parts = rel_dir.parts
    first = parts[0] if parts else ""
    # Section hub
    if first in SECTION_HUBS:
        names = {
            "CC": "증상별 안내",
            "updates": "최신 지견",
            "케이스": "케이스",
            "소개": "소개",
            "연구": "연구",
            "keywords": "키워드",
        }
        return names.get(first, first), f"{SITE}/{quote(first, safe='')}/"
    # 8 hubs by slug prefix
    for hub in HUBS_8:
        if first.startswith(hub):
            return hub, f"{SITE}/{quote(hub, safe='')}/"
    return "Hepatology Note", f"{SITE}/"


def build_jsonld(rel_dir: Path, html: str):
    p = HeadParser()
    p.feed(html)
    title = (p.title or "").replace(" — Hepatology Note", "").strip()
    h1 = extract_h1(html)
    name = h1 or title or rel_dir.name
    description = p.description.strip()
    canonical = p.canonical or url_for_page(rel_dir)
    keywords = [k.strip() for k in p.keywords.split(",") if k.strip()] if p.keywords else []
    abs_path = ROOT / rel_dir / "index.html"
    date_published, date_modified = git_dates(abs_path)
    hub_name, hub_url = determine_hub(rel_dir, html)
    faqs = extract_faqs(html)

    page_id = canonical + "#webpage"
    article_id = canonical + "#article"

    graph = []

    # MedicalWebPage (covers WebPage role + medical context)
    medical_page = {
        "@type": "MedicalWebPage",
        "@id": page_id,
        "url": canonical,
        "name": name,
        "headline": name,
        "description": description,
        "inLanguage": "ko",
        "isPartOf": {"@id": f"{SITE}/#website"},
        "datePublished": date_published,
        "dateModified": date_modified,
        "primaryImageOfPage": {"@type": "ImageObject", "url": f"{SITE}/assets/img/author/drshin.jpg"},
        "author": {"@id": f"{SITE}/#author"},
        "publisher": {"@id": f"{SITE}/#author"},
        "audience": [
            {"@type": "MedicalAudience", "audienceType": "Patient"},
            {"@type": "MedicalAudience", "audienceType": "MedicalResearcher"},
        ],
        "lastReviewed": date_modified.split("T")[0],
        "reviewedBy": {"@id": f"{SITE}/#author"},
    }
    if keywords:
        medical_page["keywords"] = ", ".join(keywords)
    graph.append(medical_page)

    # Article (parallel; helpful for non-medical search)
    graph.append({
        "@type": "Article",
        "@id": article_id,
        "headline": name,
        "description": description,
        "inLanguage": "ko",
        "datePublished": date_published,
        "dateModified": date_modified,
        "author": {"@id": f"{SITE}/#author"},
        "publisher": {"@id": f"{SITE}/#author"},
        "image": f"{SITE}/assets/img/author/drshin.jpg",
        "mainEntityOfPage": {"@id": page_id},
        "isPartOf": {"@id": f"{SITE}/#website"},
    })

    # BreadcrumbList
    breadcrumb_items = [
        {"@type": "ListItem", "position": 1, "name": "홈", "item": f"{SITE}/"},
    ]
    if hub_name and hub_url and hub_url != f"{SITE}/":
        breadcrumb_items.append(
            {"@type": "ListItem", "position": 2, "name": hub_name, "item": hub_url}
        )
        breadcrumb_items.append(
            {"@type": "ListItem", "position": 3, "name": name, "item": canonical}
        )
    else:
        breadcrumb_items.append(
            {"@type": "ListItem", "position": 2, "name": name, "item": canonical}
        )
    graph.append({"@type": "BreadcrumbList", "itemListElement": breadcrumb_items})

    # FAQPage (if FAQs detected)
    if faqs:
        graph.append({
            "@type": "FAQPage",
            "@id": canonical + "#faq",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs
            ],
        })

    # Person (author) — keep ID-only reference plus minimal definition
    graph.append({
        "@type": "Person",
        "@id": f"{SITE}/#author",
        "name": "신현재",
        "alternateName": "Hyun Jae Shin",
        "jobTitle": "서울대학교병원 소화기내과 · 간암센터",
        "worksFor": {
            "@type": "Hospital",
            "name": "서울대학교병원",
            "url": "https://www.snuh.org/",
        },
        "url": f"{SITE}/소개/",
        "image": f"{SITE}/assets/img/author/drshin.jpg",
        "sameAs": [
            "https://www.snuh.org/blog/83759/philosophy.do",
            "https://scholar.google.com/citations?user=-0ZNZw0AAAAJ",
        ],
    })

    # WebSite reference
    graph.append({
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "url": f"{SITE}/",
        "name": "Hepatology Note",
        "inLanguage": "ko",
        "publisher": {"@id": f"{SITE}/#author"},
    })

    payload = {"@context": "https://schema.org", "@graph": graph}
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


_VOLATILE_FIELDS_RE = re.compile(
    r'"(?:datePublished|dateModified|lastReviewed)":"[^"]*"'
)


def _strip_volatile(jsonld_str: str) -> str:
    """JSON-LD에서 매 빌드마다 흔들릴 수 있는 timestamp 필드를 normalize.

    같은 콘텐츠라면 datePublished/dateModified/lastReviewed만 다른 경우 동일한
    것으로 취급한다. datePublished는 git first-commit 추적(rename·history 변동)에
    따라 흔들릴 수 있는데, 이 변동이 idempotent 비교를 깨면 본문이 그대로인데도
    JSON-LD 블록 전체가 교체되고 dateModified까지 갱신돼, sitemap lastmod가
    사이트 전체에서 한 날짜로 점프하는 문제가 생긴다(healthpick GSC 사고와 동일
    메커니즘). 세 날짜 필드를 모두 normalize해서 "본문이 같으면 날짜 변동은 무시,
    기존 블록 보존"이 되도록 한다.
    """
    return _VOLATILE_FIELDS_RE.sub('""', jsonld_str)


def inject(html: str, jsonld: str) -> str:
    """Insert or replace marker block before </head>.

    Idempotent: 콘텐츠가 같고 dateModified/lastReviewed만 바뀌었다면
    기존 블록을 그대로 두어 commit noise 방지.
    """
    block = f"{MARKER_START}\n<script type=\"application/ld+json\">{jsonld}</script>\n{MARKER_END}"
    if MARKER_START in html and MARKER_END in html:
        # 기존 JSON-LD 추출해서 콘텐츠 비교 (volatile 필드 제외)
        existing_match = re.search(
            re.escape(MARKER_START)
            + r"\s*<script[^>]*>(.*?)</script>\s*"
            + re.escape(MARKER_END),
            html, re.S,
        )
        if existing_match:
            existing_jsonld = existing_match.group(1)
            if _strip_volatile(existing_jsonld) == _strip_volatile(jsonld):
                # 콘텐츠 동일 — 기존 블록 유지 (dateModified 보존)
                return html
        # 콘텐츠가 실제로 다름 — 새 블록으로 교체
        return re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            block,
            html, count=1, flags=re.S,
        )
    # 마커 없음 — </head> 직전에 새로 삽입
    return html.replace("</head>", f"{block}\n</head>", 1)


def main():
    n_inject = 0
    n_skip = 0
    for path in ROOT.rglob("index.html"):
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            n_skip += 1
            continue
        if any(p.startswith(".") for p in parts):
            n_skip += 1
            continue
        rel_dir = path.parent.relative_to(ROOT)
        if not is_detail_page(rel_dir):
            n_skip += 1
            continue
        try:
            html = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ! read fail {path}: {e}")
            continue
        jsonld = build_jsonld(rel_dir, html)
        new_html = inject(html, jsonld)
        if new_html != html:
            path.write_text(new_html, encoding="utf-8")
            n_inject += 1
    print(f"Injected/updated JSON-LD on {n_inject} detail pages. Skipped {n_skip}.")


if __name__ == "__main__":
    main()
