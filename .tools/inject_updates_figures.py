"""Inject paper-specific inline SVG figures into each /updates/{slug}/ page.

Insertion point: just before the first `<div class="note-section">` containing
"KEY POINT" or "임상 함의" — placing the figure between APPROACH and KEY POINT
so readers see the result visualization in the natural flow.

Falls back to inserting before <section class="references-block"> if no KEY
POINT section is found.

Idempotent — uses <!-- update-fig --> ... <!-- /update-fig --> markers.
"""
from __future__ import annotations
import re
import sys, os
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from updates_figures import UPDATES_FIGURES

ROOT = Path(__file__).resolve().parent.parent
UPDATES_DIR = ROOT / "updates"

OPEN = "<!-- update-fig -->"
CLOSE = "<!-- /update-fig -->"
BLOCK_RE = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.DOTALL)

KEYPOINT_RE = re.compile(
    r'(<div class="note-section">\s*<h2><span class="label">(?:KEY POINT|IMPACT|HOW TO USE|결론)</span>)',
    re.IGNORECASE,
)


def inject(html_path: Path, fig_html: str) -> bool:
    text = html_path.read_text(encoding="utf-8")
    wrapped = f"{OPEN}\n{fig_html}\n{CLOSE}"

    # Strip existing block first
    text = BLOCK_RE.sub("", text).rstrip() + "\n"

    # Try to insert before KEY POINT note-section
    m = KEYPOINT_RE.search(text)
    if m:
        new_text = text[:m.start()] + wrapped + "\n\n" + text[m.start():]
    elif '<section class="references-block">' in text:
        new_text = text.replace(
            '<section class="references-block">',
            f'{wrapped}\n\n<section class="references-block">',
            1,
        )
    elif "</article>" in text:
        new_text = text.replace("</article>", f"{wrapped}\n</article>", 1)
    else:
        return False

    if new_text == text:
        return False
    html_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    n_ok = 0
    n_skip = 0
    for slug, fig_html in UPDATES_FIGURES.items():
        path = UPDATES_DIR / slug / "index.html"
        if not path.exists():
            print(f"  ! missing page: {slug}")
            n_skip += 1
            continue
        if inject(path, fig_html):
            print(f"  ok: {slug}")
            n_ok += 1
        else:
            print(f"  skip (no insertion point): {slug}")
            n_skip += 1
    print(f"Done. {n_ok} injected, {n_skip} skipped.")


if __name__ == "__main__":
    main()
