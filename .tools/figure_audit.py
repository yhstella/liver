"""Audit each page for inline figures (svg.fig, <figure><img>, <img>) to find pages
that need more topic-specific diagrams."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIRS = {"private-figures", "assets", ".tools", "node_modules"}


def main():
    rows = []
    for p in sorted(ROOT.rglob("index.html")):
        parts = p.parts
        if any(x in SKIP_DIRS for x in parts):
            continue
        text = p.read_text(encoding="utf-8")
        svg_fig = len(re.findall(r'<svg[^>]*class="[^"]*\bfig\b', text))
        svg_any = len(re.findall(r'<svg\b', text))
        img_in_fig = len(re.findall(r'<figure[^>]*>\s*<img', text))
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        rel = rel.replace("/index.html", "").replace("index.html", "(home)")
        rows.append((rel, svg_fig, svg_any, img_in_fig))

    rows.sort(key=lambda r: (r[1] + r[3], r[0]))
    print(f'{"PAGE":<55} {"svg.fig":>8} {"any svg":>8} {"img-fig":>8}')
    print("-" * 84)
    for r in rows:
        print(f"{r[0]:<55} {r[1]:>8} {r[2]:>8} {r[3]:>8}")
    print("-" * 84)
    print(f"Total {len(rows)} pages")
    print(f"Pages with 0 svg.fig: {sum(1 for r in rows if r[1]==0)}")
    print(f"Pages with 1 svg.fig: {sum(1 for r in rows if r[1]==1)}")
    print(f"Pages with >=2 svg.fig: {sum(1 for r in rows if r[1]>=2)}")


if __name__ == "__main__":
    main()
