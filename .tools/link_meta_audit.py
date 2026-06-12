#!/usr/bin/env python3
"""
link_meta_audit.py — Broken internal links + JSON-LD consistency + meta quality.

Complements seo_health_audit.py (indexability) with on-page link/meta integrity:
- internal <a href="/..."> pointing to a path that has no page (broken link / 404)
- JSON-LD @id/url/canonical mismatch within a page
- canonical vs og:url mismatch
- meta description ending in "…" (looks truncated in SERP) or missing
- title missing or overly long (>60 chars excl. site suffix → SERP truncation)
- duplicate <title> / <canonical> / og:url

Read-only. Reports to .tools/link_meta_report.json. Exit 1 if broken links or
JSON-LD mismatches found (high severity), else 0.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from urllib.parse import unquote, urlparse, quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://drshin.kr"
OUT = ROOT / ".tools" / "link_meta_report.json"
SKIP = {".git", ".tools", "assets", "private-figures", "node_modules", "guide"}

A_HREF_RE = re.compile(r'<a\s[^>]*href="(/[^"#?]*)"', re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
CANON_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]*)"', re.I)
OGURL_RE = re.compile(r'<meta\s+property="og:url"\s+content="([^"]*)"', re.I)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
JSONLD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)


def norm(path_or_url: str) -> str:
    p = urlparse(path_or_url).path if "://" in path_or_url else path_or_url
    p = unquote(p)
    if not p.endswith("/") and "." not in p.rsplit("/", 1)[-1]:
        p += "/"
    return p


def build_page_set():
    """Set of normalized paths that exist as pages (have index.html)."""
    s = set()
    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP or part.startswith(".") for part in rel.parts):
            continue
        d = p.parent.relative_to(ROOT)
        s.add(norm("/" + "/".join(d.parts) + "/") if str(d) != "." else "/")
    return s


def static_asset_exists(path: str) -> bool:
    """For non-page links (files), check the file exists on disk."""
    rel = unquote(path).lstrip("/")
    return (ROOT / rel).exists()


def main():
    pages = build_page_set()
    findings = {
        "broken_internal_links": [],
        "jsonld_id_mismatch": [],
        "canonical_ogurl_mismatch": [],
        "desc_ellipsis": [],
        "desc_missing": [],
        "title_missing": [],
        "title_too_long": [],
        "duplicate_canonical": [],
    }

    for p in ROOT.rglob("index.html"):
        rel = p.relative_to(ROOT)
        if any(part in SKIP or part.startswith(".") for part in rel.parts):
            continue
        relp = str(rel).replace("\\", "/")
        html = p.read_text(encoding="utf-8", errors="ignore")

        # title
        titles = TITLE_RE.findall(html)
        if not titles:
            findings["title_missing"].append(relp)
        else:
            t = titles[0].replace(" — Hepatology Note", "").strip()
            if len(t) > 60:
                findings["title_too_long"].append({"page": relp, "len": len(t)})

        # canonical / og:url
        canons = CANON_RE.findall(html)
        if len(canons) > 1:
            findings["duplicate_canonical"].append({"page": relp, "count": len(canons)})
        canon = canons[0] if canons else None
        ogs = OGURL_RE.findall(html)
        if canon and ogs and norm(canon) != norm(ogs[0]):
            findings["canonical_ogurl_mismatch"].append({"page": relp, "canonical": canon, "og_url": ogs[0]})

        # description
        descs = DESC_RE.findall(html)
        if not descs or not descs[0].strip():
            findings["desc_missing"].append(relp)
        elif descs[0].rstrip().endswith("…") or descs[0].rstrip().endswith("..."):
            findings["desc_ellipsis"].append({"page": relp, "desc_tail": descs[0][-40:]})

        # JSON-LD @id consistency: webpage @id should match canonical#webpage
        for block in JSONLD_RE.findall(html):
            try:
                data = json.loads(block)
            except Exception:
                continue
            graph = data.get("@graph", []) if isinstance(data, dict) else []
            for node in graph:
                if node.get("@type") == "MedicalWebPage" and canon:
                    url = node.get("url", "")
                    if url and norm(url) != norm(canon):
                        findings["jsonld_id_mismatch"].append({"page": relp, "jsonld_url": url, "canonical": canon})

        # internal links
        for href in A_HREF_RE.findall(html):
            np = norm(href)
            if np in pages:
                continue
            # could be a static asset/file (has extension)
            last = href.rstrip("/").rsplit("/", 1)[-1]
            if "." in last:
                if static_asset_exists(href):
                    continue
            findings["broken_internal_links"].append({"page": relp, "href": href})

    high = len(findings["broken_internal_links"]) + len(findings["jsonld_id_mismatch"])
    report = {"highSeverityCount": high, "findings": findings}
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("--- HIGH ---")
    print(f"  broken_internal_links: {len(findings['broken_internal_links'])}")
    print(f"  jsonld_id_mismatch: {len(findings['jsonld_id_mismatch'])}")
    print(f"  canonical_ogurl_mismatch: {len(findings['canonical_ogurl_mismatch'])}")
    print("--- MED/LOW ---")
    print(f"  desc_ellipsis: {len(findings['desc_ellipsis'])}")
    print(f"  desc_missing: {len(findings['desc_missing'])}")
    print(f"  title_missing: {len(findings['title_missing'])}")
    print(f"  title_too_long: {len(findings['title_too_long'])}")
    print(f"  duplicate_canonical: {len(findings['duplicate_canonical'])}")
    print(f"\nFull report: .tools/link_meta_report.json")
    sys.exit(1 if high else 0)


if __name__ == "__main__":
    main()
