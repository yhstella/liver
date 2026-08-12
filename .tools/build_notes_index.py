#!/usr/bin/env python3
"""
build_notes_index.py — 단상(/단상/) 랜딩의 글 목록을 자동 생성.

- 단상/<슬러그>/index.html 을 훑어 제목·날짜·발췌를 뽑는다.
- noindex 또는 <!-- DRAFT --> 가 있는 글은 목록에서 제외 (초안 보관용).
- 랜딩의 <!-- notes-list:auto:start --> ~ end 사이를 갈아끼운다.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = ROOT / "단상"
START = "<!-- notes-list:auto:start -->"
END = "<!-- notes-list:auto:end -->"

H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
TIME_RE = re.compile(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})"')
LEDE_RE = re.compile(r'<p class="note-lede">(.*?)</p>', re.S)
TAG_RE = re.compile(r"<[^>]+>")


def strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub("", s)).strip()


def is_draft(html: str) -> bool:
    if "<!-- DRAFT -->" in html:
        return True
    m = re.search(r'<meta\s+name="robots"\s+content="([^"]*)"', html, re.I)
    return bool(m and "noindex" in m.group(1).lower())


def collect():
    items = []
    if not NOTES.exists():
        return items
    for d in NOTES.iterdir():
        if not d.is_dir() or d.name.startswith("."):
            continue
        idx = d / "index.html"
        if not idx.exists():
            continue
        html = idx.read_text(encoding="utf-8")
        if is_draft(html):
            continue
        h1 = H1_RE.search(html)
        t = TIME_RE.search(html)
        lede = LEDE_RE.search(html)
        items.append({
            "slug": d.name,
            "title": strip_tags(h1.group(1)) if h1 else d.name,
            "date": t.group(1) if t else "",
            "lede": strip_tags(lede.group(1)) if lede else "",
        })
    items.sort(key=lambda x: (x["date"], x["slug"]), reverse=True)
    return items


def render(items) -> str:
    if not items:
        return ('<p class="notes-empty" style="color:var(--muted);font-size:14.5px;'
                'margin:32px 0 0">아직 쓴 글이 없습니다.</p>')
    out = ['<ul class="notes-list">']
    for it in items:
        y, m, dd = (it["date"].split("-") + ["", "", ""])[:3] if it["date"] else ("", "", "")
        datetxt = f"{y}년 {int(m)}월 {int(dd)}일" if y else ""
        out.append("  <li>")
        out.append(f'    <a href="/단상/{it["slug"]}/"><h3>{it["title"]}</h3></a>')
        if it["lede"]:
            out.append(f'    <p>{it["lede"]}</p>')
        if datetxt:
            out.append(f'    <time datetime="{it["date"]}">{datetxt}</time>')
        out.append("  </li>")
    out.append("</ul>")
    return "\n".join(out)


def main():
    landing = NOTES / "index.html"
    if not landing.exists():
        print("  단상/index.html 없음 — 건너뜀")
        return
    html = landing.read_text(encoding="utf-8")
    if START not in html or END not in html:
        print("  notes-list 마커 없음 — 건너뜀")
        return
    items = collect()
    body = render(items)
    new = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        START + "\n" + body + "\n" + END,
        html,
        flags=re.S,
    )
    if new != html:
        landing.write_text(new, encoding="utf-8")
        print(f"  단상 목록 갱신: {len(items)}편")
    else:
        print(f"  단상 목록 변동 없음 ({len(items)}편)")


if __name__ == "__main__":
    main()
