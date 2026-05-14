#!/usr/bin/env python3
"""각 hub 페이지에 '이 카테고리의 최근 업데이트' 미니 박스 자동 주입.

- hub 페이지의 topic-list에서 detail 페이지 URL을 추출
- 각 detail 페이지의 article:published_time 읽기
- 최근 3편 (descending) 선택
- hub의 series-intro 직후에 idempotent 박스로 주입/갱신
- 마커: <!-- hub-recent:auto:start --> ... <!-- hub-recent:auto:end -->

재실행 안전. 새 페이지 추가 후 다시 돌리면 자동 갱신.
"""
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parent.parent

HUBS = [
    '간암', '간경화', 'B형간염', '지방간',
    '간수치', 'C형간염', '자가면역간질환', '간양성종양',
]

PUB_RE = re.compile(r'<meta property="article:published_time" content="([^"]+)"')
H1_RE = re.compile(r'<h1[^>]*>(.+?)</h1>', re.DOTALL)
CRUMB_LABEL_RE = re.compile(r'<nav class="crumb">.*?›\s*<span>([^<]+)</span>', re.DOTALL)
TOPIC_LIST_HREF_RE = re.compile(r'<ul class="topic-list">(.+?)</ul>', re.DOTALL)
HREF_RE = re.compile(r'<a href="(/[^"#?]+/)"')
MARKER_RE = re.compile(
    r'<!--\s*hub-recent:auto:start\s*-->.*?<!--\s*hub-recent:auto:end\s*-->\s*',
    re.DOTALL,
)
SERIES_INTRO_RE = re.compile(r'(<p class="series-intro">.*?</p>\s*)', re.DOTALL)


def strip_tags(s: str) -> str:
    return re.sub(r'<[^>]+>', '', s).strip()


def parse_pub(s: str):
    if not s:
        return None
    s = s.strip()
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def short_title(html_text: str) -> str:
    m = CRUMB_LABEL_RE.search(html_text)
    if m:
        return strip_tags(m.group(1))
    m = H1_RE.search(html_text)
    if m:
        return strip_tags(m.group(1))
    return ''


def fmt_date(dt: datetime) -> str:
    return f'{dt.year}.{dt.month:02d}.{dt.day:02d}'


def is_recent(dt: datetime, now: datetime, days: int = 31) -> bool:
    return (now - dt) <= timedelta(days=days)


def build_box(items, now):
    """items = [(url, title, dt)]; renders the auto-marked box."""
    lis = []
    for url, title, dt in items:
        is_new = is_recent(dt, now)
        new_chip = '<span class="new">NEW</span>' if is_new else ''
        lis.append(
            f'  <li><a href="{url}">{title}</a>'
            f'<time class="date" datetime="{dt.date().isoformat()}">{fmt_date(dt)}</time>'
            f'{new_chip}</li>'
        )
    inner = '\n'.join(lis)
    return (
        '<!-- hub-recent:auto:start -->\n'
        '<aside class="hub-recent" aria-label="이 카테고리의 최근 업데이트">\n'
        '<h2 class="hub-recent-title">최근 업데이트</h2>\n'
        '<ul class="hub-recent-list">\n'
        f'{inner}\n'
        '</ul>\n'
        '</aside>\n'
        '<!-- hub-recent:auto:end -->\n'
    )


def process_hub(hub: str, now: datetime) -> bool:
    hub_path = ROOT / hub / 'index.html'
    if not hub_path.exists():
        print(f'  skip {hub}: hub page missing')
        return False
    html = hub_path.read_text(encoding='utf-8')

    # topic-list에서 URL 추출
    m = TOPIC_LIST_HREF_RE.search(html)
    if not m:
        print(f'  skip {hub}: no topic-list')
        return False
    urls = HREF_RE.findall(m.group(1))

    items = []
    for url in urls:
        # /B형간염-평생약/ → B형간염-평생약/index.html
        slug = url.strip('/')
        page_path = ROOT / slug / 'index.html'
        if not page_path.exists():
            continue
        page_html = page_path.read_text(encoding='utf-8')
        pubm = PUB_RE.search(page_html)
        if not pubm:
            continue
        dt = parse_pub(pubm.group(1))
        if not dt:
            continue
        title = short_title(page_html)
        if not title:
            continue
        items.append((url, title, dt))

    items.sort(key=lambda x: x[2], reverse=True)
    items = items[:3]
    if not items:
        print(f'  skip {hub}: no dated items found')
        return False

    box = build_box(items, now)

    # 기존 marker 블록 제거
    new_html = MARKER_RE.sub('', html)

    # series-intro 직후 위치에 주입; 없으면 첫 topic-list 직전
    if SERIES_INTRO_RE.search(new_html):
        new_html = SERIES_INTRO_RE.sub(lambda m: m.group(1) + '\n' + box, new_html, count=1)
    else:
        new_html = re.sub(
            r'(<ul class="topic-list">)',
            box + r'\1',
            new_html,
            count=1,
        )

    if new_html == html:
        return False
    hub_path.write_text(new_html, encoding='utf-8')
    return True


def main():
    now = datetime.now(timezone(timedelta(hours=9)))
    changed = 0
    for hub in HUBS:
        if process_hub(hub, now):
            print(f'  [ok] {hub}')
            changed += 1
        else:
            print(f'  [--] {hub} (no change)')
    print(f'{changed}/{len(HUBS)} hubs updated')


if __name__ == '__main__':
    main()
