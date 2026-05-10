#!/usr/bin/env python3
"""
build_sitemap.py — Generate /sitemap.xml from all index.html files.

- 모든 index.html을 순회하여 URL 생성
- /guide/, /.tools/, /논문/(redirect) 등은 제외
- lastmod = 파일의 git 최신 commit 일자 (없으면 mtime)
- priority = 홈 1.0, 대주제 hub 0.9, detail 0.7, 케이스 0.6, updates detail 0.7
- changefreq = 홈 weekly, hub monthly, detail monthly
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://drshin.kr"

EXCLUDE_DIRS = {".git", ".tools", "node_modules", "assets", "guide", "논문"}
EXCLUDE_FILES = set()


def git_last_modified(path: Path) -> str:
    """Get last commit date for path, ISO format YYYY-MM-DD. Falls back to mtime."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
        out = result.stdout.strip()
        if out:
            return out.split("T")[0]
    except Exception:
        pass
    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return ts.strftime("%Y-%m-%d")


HUBS_8 = {"간암", "간경화", "B형간염", "C형간염", "지방간", "간수치", "자가면역간염", "간양성종양"}
SECTION_HUBS = {"updates", "케이스", "CC", "keywords", "소개", "연구"}


def categorize(rel_path: str) -> tuple[float, str]:
    """Return (priority, changefreq) based on URL pattern."""
    if rel_path == "/":
        return (1.0, "weekly")
    parts = rel_path.strip("/").split("/")
    depth = len([p for p in parts if p])
    first = parts[0] if parts else ""
    # Section hubs (updates/케이스/CC/keywords/소개/연구)
    if depth == 1 and first in SECTION_HUBS:
        return (0.9, "weekly" if first == "updates" else "monthly")
    # 8 대주제 hub
    if depth == 1 and first in HUBS_8:
        return (0.9, "monthly")
    # Top-level detail page (대주제-부주제 slug, 깊이 1)
    if depth == 1:
        return (0.7, "monthly")
    # Sub pages under section hubs
    if first == "케이스":
        return (0.6, "monthly")
    if first == "updates":
        return (0.8, "monthly")  # 논문 노트는 인덱스 가치 높음
    if first == "CC":
        return (0.7, "monthly")
    return (0.7, "monthly")


def url_for(rel_dir: Path) -> str:
    """Convert directory path relative to ROOT into a public URL."""
    if str(rel_dir) == ".":
        return f"{SITE}/"
    parts = rel_dir.parts
    encoded = "/".join(quote(p, safe="") for p in parts)
    return f"{SITE}/{encoded}/"


def collect_pages():
    """Yield (url, lastmod, priority, changefreq) for every index.html."""
    pages = []
    for path in ROOT.rglob("index.html"):
        # Skip excluded
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if any(p.startswith(".") for p in parts):
            continue
        rel_dir = path.parent.relative_to(ROOT)
        url = url_for(rel_dir)
        lastmod = git_last_modified(path)
        # Build URL path for categorize
        if str(rel_dir) == ".":
            url_path = "/"
        else:
            url_path = "/" + "/".join(rel_dir.parts) + "/"
        priority, changefreq = categorize(url_path)
        pages.append((url, lastmod, priority, changefreq))
    # Sort: home first, then by URL
    pages.sort(key=lambda x: (x[0] != f"{SITE}/", x[0]))
    return pages


def render_sitemap(pages):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod, priority, changefreq in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority:.1f}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    pages = collect_pages()
    xml = render_sitemap(pages)
    out = ROOT / "sitemap.xml"
    out.write_text(xml, encoding="utf-8")
    print(f"Wrote {out} with {len(pages)} URLs.")


if __name__ == "__main__":
    main()
