"""Inject <script src="/assets/js/figure-zoom.js" defer></script> into all article HTML head."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCRIPT_TAG = '<script src="/assets/js/figure-zoom.js" defer></script>'
ANCHOR = '<link rel="stylesheet" href="/style.css">'
NEW = ANCHOR + '\n' + SCRIPT_TAG

n = 0
for p in ROOT.rglob("index.html"):
    if "/.git/" in str(p).replace("\\","/") or "/.tools/" in str(p).replace("\\","/"):
        continue
    text = p.read_text(encoding="utf-8")
    if 'figure-zoom.js' in text:
        continue
    if ANCHOR in text:
        text = text.replace(ANCHOR, NEW, 1)
        p.write_text(text, encoding="utf-8")
        n += 1
        rel = p.relative_to(ROOT)
        print(f"  injected: {rel}")
print(f"\nTotal injected: {n}")
