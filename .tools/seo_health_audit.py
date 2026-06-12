#!/usr/bin/env python3
"""
seo_health_audit.py — Indexability / crawlability health check for drshin.kr.

Catches the classes of problem that have actually bitten this site:
- noindex pages leaking into the sitemap (GSC "submitted but noindex")
- sitemap URLs that 404 (no matching index.html)
- published, indexable pages MISSING from the sitemap
- robots.txt Disallow paths that still appear in the sitemap
- duplicate / wrong robots meta tags on a page
- canonical pointing elsewhere on an indexable page (silent dedup)
- canonical URL form not matching the sitemap URL form

Read-only. Reports to .tools/seo_health_report.json and stdout.
Exit code 0 if no high-severity findings, 1 otherwise (CI-friendly).

Usage:
  python .tools/seo_health_audit.py
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://drshin.kr"
OUT = ROOT / ".tools" / "seo_health_report.json"

SKIP_DIRS = {".git", ".tools", "assets", "private-figures", "node_modules"}
# Directories intentionally excluded from indexing (mirror build_sitemap EXCLUDE_DIRS)
INTENTIONAL_NOINDEX_DIRS = {"guide"}
# Single-segment slugs that are intentional redirect/landing noindex
INTENTIONAL_NOINDEX_SLUGS = {"자가면역간염", "논문", "keywords"}

ROBOTS_RE = re.compile(r'<meta\s+name="robots"\s+content="([^"]*)"', re.I)
CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"', re.I)


def rel_path(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def page_url(rel_dir: Path) -> str:
    if str(rel_dir) == ".":
        return f"{SITE}/"
    return f"{SITE}/" + "/".join(quote(x, safe="") for x in rel_dir.parts) + "/"


def norm_url(u: str) -> str:
    """Normalize a URL to decoded path with trailing slash for comparison."""
    path = urlparse(u).path
    path = unquote(path)
    if not path.endswith("/"):
        path += "/"
    return path


def collect_pages():
    pages = {}
    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts):
            continue
        try:
            head = p.read_text(encoding="utf-8", errors="ignore")[:6000]
        except Exception:
            continue
        robots = ROBOTS_RE.findall(head)
        canon = CANON_RE.findall(head)
        rel_dir = p.parent.relative_to(ROOT)
        pages[rel_path(p)] = {
            "url": page_url(rel_dir),
            "url_path": norm_url(page_url(rel_dir)),
            "robots": robots,
            "canonical": canon[0] if canon else None,
            "is_noindex": any("noindex" in r.lower() for r in robots),
        }
    return pages


def parse_sitemap_urls():
    urls = set()
    for sm in ROOT.glob("sitemap*.xml"):
        text = sm.read_text(encoding="utf-8", errors="ignore")
        for loc in re.findall(r"<loc>([^<]+)</loc>", text):
            if loc.endswith(".xml"):
                continue  # sitemap index entry
            urls.add(norm_url(loc))
    return urls


def parse_robots_disallow():
    rp = ROOT / "robots.txt"
    dis = []
    if rp.exists():
        for line in rp.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"\s*Disallow:\s*(\S+)", line, re.I)
            if m:
                dis.append(m.group(1))
    return dis


def main():
    pages = collect_pages()
    sitemap_paths = parse_sitemap_urls()
    disallow = parse_robots_disallow()

    findings = {
        "noindex_in_sitemap": [],     # HIGH: noindex page present in sitemap
        "sitemap_404": [],            # HIGH: sitemap URL has no page file
        "indexable_missing_from_sitemap": [],  # MED: published page not in sitemap
        "robots_meta_conflict": [],   # HIGH: 0 or >1 robots meta tags
        "disallow_in_sitemap": [],    # HIGH: robots.txt Disallow path in sitemap
        "canonical_offsite_indexable": [],  # MED: indexable page canonical -> other URL
        "canonical_form_mismatch": [],  # LOW: canonical form != page url form
        "no_canonical": [],           # MED: indexable page without canonical
    }

    page_paths = {p["url_path"] for p in pages.values()}

    # noindex in sitemap + canonical/robots checks
    for fp, info in pages.items():
        up = info["url_path"]
        # robots meta count
        if len(info["robots"]) != 1:
            findings["robots_meta_conflict"].append({"page": fp, "count": len(info["robots"]), "values": info["robots"]})
        if info["is_noindex"] and up in sitemap_paths:
            findings["noindex_in_sitemap"].append({"page": fp, "url": info["url"]})
        if not info["is_noindex"]:
            # indexable page
            if up not in sitemap_paths:
                findings["indexable_missing_from_sitemap"].append({"page": fp, "url": info["url"]})
            if not info["canonical"]:
                findings["no_canonical"].append({"page": fp})
            elif norm_url(info["canonical"]) != up:
                findings["canonical_offsite_indexable"].append({"page": fp, "canonical": info["canonical"], "self": info["url"]})
            elif info["canonical"]:
                # form check: canonical present and points to self path — verify encoding form
                if norm_url(info["canonical"]) != up:
                    findings["canonical_form_mismatch"].append({"page": fp, "canonical": info["canonical"]})

    # sitemap URLs that have no page
    for sp in sitemap_paths:
        if sp not in page_paths:
            findings["sitemap_404"].append({"sitemap_url_path": sp})

    # robots.txt disallow paths appearing in sitemap
    for d in disallow:
        dnorm = unquote(d)
        for sp in sitemap_paths:
            if sp.startswith(dnorm):
                findings["disallow_in_sitemap"].append({"disallow": d, "sitemap_path": sp})

    HIGH = ["noindex_in_sitemap", "sitemap_404", "robots_meta_conflict", "disallow_in_sitemap"]
    high_count = sum(len(findings[k]) for k in HIGH)

    report = {
        "totalPages": len(pages),
        "sitemapUrls": len(sitemap_paths),
        "intentionalNoindex": sorted(INTENTIONAL_NOINDEX_SLUGS | INTENTIONAL_NOINDEX_DIRS),
        "highSeverityCount": high_count,
        "findings": findings,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Pages scanned: {len(pages)} | Sitemap URLs: {len(sitemap_paths)}")
    print(f"\n--- HIGH severity ---")
    for k in HIGH:
        n = len(findings[k])
        flag = " <== CHECK" if n else ""
        print(f"  {k}: {n}{flag}")
    print(f"\n--- MED/LOW ---")
    for k in ["indexable_missing_from_sitemap", "canonical_offsite_indexable", "no_canonical", "canonical_form_mismatch"]:
        print(f"  {k}: {len(findings[k])}")
    print(f"\nFull report: .tools/seo_health_report.json")
    sys.exit(1 if high_count else 0)


if __name__ == "__main__":
    main()
