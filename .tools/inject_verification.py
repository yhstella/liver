#!/usr/bin/env python3
"""
inject_verification.py — Inject Google/Naver/Bing verification meta tags
into <head> of every page. Currently placeholders; replace VALUES below
once you have real codes from Search Console / Naver Webmaster / Bing.

Marker: <!-- verify:auto:start --> ... <!-- verify:auto:end -->
Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", ".tools", "node_modules", "assets"}

MARKER_START = "<!-- verify:auto:start -->"
MARKER_END = "<!-- verify:auto:end -->"

# === FILL IN AFTER REGISTRATION ===
GOOGLE_CODE = ""   # e.g. "abc123XYZ..."
NAVER_CODE  = ""   # e.g. "xyz789ABC..."
BING_CODE   = ""   # e.g. "1A2B3C..."

def render_block() -> str:
    parts = [MARKER_START]
    if GOOGLE_CODE:
        parts.append(f'<meta name="google-site-verification" content="{GOOGLE_CODE}">')
    if NAVER_CODE:
        parts.append(f'<meta name="naver-site-verification" content="{NAVER_CODE}">')
    if BING_CODE:
        parts.append(f'<meta name="msvalidate.01" content="{BING_CODE}">')
    parts.append(MARKER_END)
    return "\n".join(parts)


def inject(html: str, block: str) -> str:
    if MARKER_START in html and MARKER_END in html:
        return re.sub(
            re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
            block,
            html, count=1, flags=re.S,
        )
    return html.replace("</head>", f"{block}\n</head>", 1)


def main():
    block = render_block()
    if not (GOOGLE_CODE or NAVER_CODE or BING_CODE):
        print("No verification codes set - skipping. Edit .tools/inject_verification.py and re-run.")
        return
    n = 0
    for path in ROOT.rglob("index.html"):
        rel = path.relative_to(ROOT)
        parts = rel.parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if any(p.startswith(".") for p in parts):
            continue
        html = path.read_text(encoding="utf-8")
        new_html = inject(html, block)
        if new_html != html:
            path.write_text(new_html, encoding="utf-8")
            n += 1
    print(f"Injected verification meta on {n} pages.")


if __name__ == "__main__":
    main()
