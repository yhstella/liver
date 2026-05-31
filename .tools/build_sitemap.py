#!/usr/bin/env python3
"""
build_sitemap.py — Sitemap index + 5 child sitemaps generator.

출력:
  /sitemap.xml             ← sitemap index (검색엔진이 처음 보는 파일)
  /sitemap-core.xml        ← home + 8 hub + 7 섹션 랜딩
  /sitemap-detail.xml      ← 대주제-세부 detail 페이지
  /sitemap-updates.xml     ← Updates 논문 노트
  /sitemap-cases.xml       ← 케이스
  /sitemap-cc.xml          ← CC(주증상) 페이지

규칙:
- 모든 index.html을 순회
- /guide/, /.tools/, /논문/(redirect) 제외
- lastmod = git 최신 commit 일자 (없으면 mtime)
- priority: 홈 1.0, 대주제 hub·섹션 랜딩 0.9, updates detail 0.8,
  detail 0.7, CC 0.7, 케이스 0.6
- changefreq: 홈/Updates 섹션 weekly, 그 외 monthly
"""
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://drshin.kr"

EXCLUDE_DIRS = {".git", ".tools", "node_modules", "assets", "guide", "논문"}
EXCLUDE_SLUGS = {"자가면역간염"}  # legacy redirect — sitemap에서 제외
HUBS_8 = {"간암", "간경화", "B형간염", "C형간염", "지방간", "간수치", "자가면역간질환", "간양성종양"}
SECTION_LANDINGS = {"updates", "케이스", "CC", "keywords", "소개", "연구"}


def is_noindex_or_draft(path: Path) -> bool:
    """robots noindex 메타 또는 DRAFT 주석이 있으면 sitemap 제외 대상."""
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:4096]
    except Exception:
        return False
    if "noindex" in head.lower():
        return True
    if "<!-- DRAFT" in head or "<!--DRAFT" in head:
        return True
    return False


def git_last_modified(path: Path) -> str:
    """Get last commit date for path, ISO YYYY-MM-DD. Falls back to mtime."""
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


def url_for(rel_dir: Path) -> str:
    if str(rel_dir) == ".":
        return f"{SITE}/"
    parts = rel_dir.parts
    encoded = "/".join(quote(p, safe="") for p in parts)
    return f"{SITE}/{encoded}/"


def categorize(rel_dir: Path) -> tuple[str, float, str]:
    """Return (bucket, priority, changefreq).

    bucket ∈ {"core", "detail", "updates", "cases", "cc"}.
    """
    if str(rel_dir) == ".":
        return ("core", 1.0, "weekly")
    parts = rel_dir.parts
    first = parts[0]
    depth = len(parts)

    # 섹션 랜딩 (updates/, 케이스/, CC/, keywords/, 소개/, 연구/)
    if depth == 1 and first in SECTION_LANDINGS:
        cf = "weekly" if first == "updates" else "monthly"
        return ("core", 0.9, cf)

    # 8 대주제 hub
    if depth == 1 and first in HUBS_8:
        return ("core", 0.9, "monthly")

    # 섹션 하위 페이지
    if first == "updates":
        return ("updates", 0.8, "monthly")
    if first == "케이스":
        return ("cases", 0.6, "monthly")
    if first == "CC":
        return ("cc", 0.7, "monthly")

    # 그 외 depth=1 = 대주제-세부 detail 페이지
    if depth == 1:
        return ("detail", 0.7, "monthly")

    # fallback
    return ("detail", 0.6, "monthly")


def collect_pages():
    """Yield (bucket, url, lastmod, priority, changefreq) for every index.html."""
    pages = []
    for path in ROOT.rglob("index.html"):
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if any(p.startswith(".") for p in parts):
            continue
        # legacy redirect 페이지는 sitemap에서 제외
        if len(parts) == 2 and parts[0] in EXCLUDE_SLUGS:
            continue
        # noindex robots 메타 또는 DRAFT 주석 있으면 sitemap 제외
        if is_noindex_or_draft(path):
            continue
        rel_dir = path.parent.relative_to(ROOT)
        url = url_for(rel_dir)
        lastmod = git_last_modified(path)
        bucket, priority, changefreq = categorize(rel_dir)
        pages.append((bucket, url, lastmod, priority, changefreq))
    pages.sort(key=lambda x: (x[0], x[1] != f"{SITE}/", x[1]))
    return pages


def render_urlset(entries: list[tuple[str, str, float, str]]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, lastmod, priority, changefreq in entries:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority:.1f}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_sitemap_index(child_files: list[tuple[str, str]]) -> str:
    """child_files = [(filename, lastmod), ...] for each non-empty child."""
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for fname, lastmod in child_files:
        lines.append("  <sitemap>")
        lines.append(f"    <loc>{SITE}/{fname}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </sitemap>")
    lines.append("</sitemapindex>")
    return "\n".join(lines) + "\n"


BUCKET_FILES = {
    "core": "sitemap-core.xml",
    "detail": "sitemap-detail.xml",
    "updates": "sitemap-updates.xml",
    "cases": "sitemap-cases.xml",
    "cc": "sitemap-cc.xml",
}


def main():
    pages = collect_pages()

    # bucket으로 분리
    by_bucket: dict[str, list[tuple[str, str, float, str]]] = {b: [] for b in BUCKET_FILES}
    for bucket, url, lastmod, priority, changefreq in pages:
        by_bucket[bucket].append((url, lastmod, priority, changefreq))

    # 각 child sitemap 작성 + child의 lastmod (가장 최근 페이지 lastmod) 계산
    child_meta: list[tuple[str, str]] = []
    for bucket, fname in BUCKET_FILES.items():
        entries = by_bucket[bucket]
        out_path = ROOT / fname
        if not entries:
            # 비면 파일 삭제 (이전 잔재 방지)
            if out_path.exists():
                out_path.unlink()
            continue
        xml = render_urlset(entries)
        out_path.write_text(xml, encoding="utf-8")
        latest_lastmod = max(e[1] for e in entries)
        child_meta.append((fname, latest_lastmod))
        print(f"  {fname}: {len(entries)} URLs (lastmod {latest_lastmod})")

    # index 작성
    index_xml = render_sitemap_index(child_meta)
    (ROOT / "sitemap.xml").write_text(index_xml, encoding="utf-8")
    total = sum(len(v) for v in by_bucket.values())
    print(f"Wrote sitemap.xml index ({len(child_meta)} children, {total} URLs total).")


if __name__ == "__main__":
    main()
