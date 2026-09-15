#!/usr/bin/env python3
"""
inject_analytics.py — GA4(Google Analytics 4) 태그를 모든 공개 페이지 <head>에 넣는다.

MEASUREMENT_ID 를 채우기 전에는 아무것도 하지 않는다.
검수 전 초안(DRAFT 주석 또는 noindex,nofollow)에는 넣지 않고, 이미 있으면 뺀다.

Marker: <!-- ga4:auto:start --> ... <!-- ga4:auto:end -->
Idempotent. rebuild_seo.py 에서 호출된다.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", ".tools", "node_modules", "assets"}

MARKER_START = "<!-- ga4:auto:start -->"
MARKER_END = "<!-- ga4:auto:end -->"

# === GA4 속성의 측정 ID (예: "G-ABC123DEF4") ===
MEASUREMENT_ID = ""

DRAFT_RE = re.compile(r'<!--\s*DRAFT|<meta\s+name="robots"\s+content="noindex,nofollow"', re.I)
BLOCK_RE = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\n?", re.S)


def render_block(mid: str) -> str:
    # 광고 신호·Google 신호는 끈다(환자 사이트 — 방문 통계만 필요)
    return (
        f"{MARKER_START}\n"
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={mid}"></script>\n'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
        f"gtag('js',new Date());gtag('config','{mid}',"
        "{allow_google_signals:false,allow_ad_personalization_signals:false});</script>\n"
        f"{MARKER_END}\n"
    )


def main():
    mid = MEASUREMENT_ID.strip()
    if not re.fullmatch(r"G-[A-Z0-9]{6,12}", mid or ""):
        print("GA4 측정 ID 미설정 — 건너뜀 (.tools/inject_analytics.py 의 MEASUREMENT_ID 입력)")
        return
    block = render_block(mid)
    added = removed = 0
    for path in ROOT.rglob("index.html"):
        parts = path.relative_to(ROOT).parts
        if any(p in EXCLUDE_DIRS for p in parts) or any(p.startswith(".") for p in parts):
            continue
        html = path.read_text(encoding="utf-8")
        is_draft = bool(DRAFT_RE.search(html[:8000]))
        if is_draft:
            new = BLOCK_RE.sub("", html)
            if new != html:
                removed += 1
        elif MARKER_START in html:
            new = BLOCK_RE.sub(block, html, count=1)
        else:
            new = html.replace("</head>", block + "</head>", 1)
        if new != html:
            path.write_text(new, encoding="utf-8")
            if not is_draft:
                added += 1
    print(f"GA4 {mid}: {added} pages updated, {removed} draft pages cleaned")


if __name__ == "__main__":
    main()
