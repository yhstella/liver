"""Remove all appended <!-- page-figures --> ... <!-- /page-figures --> blocks.

The earlier embed_page_figures.py appended generic SVG study cards at the end
of every page. They were repetitive and disconnected from page content.
This script removes them. Topic-specific inline diagrams (svg.fig elements
already in page bodies) are untouched.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BLOCK_RE = re.compile(
    r"\s*<!-- page-figures -->.*?<!-- /page-figures -->\s*",
    re.DOTALL,
)


def main():
    n = 0
    for path in ROOT.rglob("index.html"):
        # Skip any path inside private-figures or assets
        parts = path.parts
        if any(p in ("private-figures", "assets", ".tools", "node_modules") for p in parts):
            continue
        text = path.read_text(encoding="utf-8")
        if "<!-- page-figures -->" not in text:
            continue
        new_text = BLOCK_RE.sub("\n", text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            n += 1
            rel = path.relative_to(ROOT)
            print(f"  cleaned: {rel}")
    print(f"Done. {n} pages cleaned.")


if __name__ == "__main__":
    main()
