#!/usr/bin/env python3
"""모든 페이지 헤더 직후에 hub-bar (8 대주제 + CC + Updates) 삽입.

idempotent: 이미 있으면 갱신, 없으면 삽입.
마커: <!-- hub-bar:auto:start --> ... <!-- hub-bar:auto:end -->
현재 페이지가 어느 hub면 해당 항목에 active 클래스.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HUBS = [
    ('/간암/', '간암'),
    ('/간경화/', '간경화'),
    ('/B형간염/', 'B형 간염'),
    ('/지방간/', '지방간'),
    ('/간수치/', '간수치'),
    ('/C형간염/', 'C형 간염'),
    ('/자가면역간염/', '자가면역간염'),
    ('/간양성종양/', '간 양성종양'),
    ('/CC/', '증상별'),
    ('/updates/', '최신 지견'),
]

MARK_START = '<!-- hub-bar:auto:start -->'
MARK_END = '<!-- hub-bar:auto:end -->'
BLOCK_RE = re.compile(rf'{re.escape(MARK_START)}.*?{re.escape(MARK_END)}\s*', re.DOTALL)
HEADER_END_RE = re.compile(r'(</header>\s*)')

# URL 인코드 안 된 한글 경로도 active 매칭에 사용
HUB_DETECT = {
    '간암': '/간암/',
    '간경변': '/간경화/',  # 간경변- 슬러그도 간경화 hub
    '간경화': '/간경화/',
    'B형간염': '/B형간염/',
    '가족-B형간염': '/B형간염/',
    'A형간염': '/B형간염/',  # 임시
    'C형간염': '/C형간염/',
    '자가면역간염': '/자가면역간염/',
    '지방간': '/지방간/',
    '지방간염': '/지방간/',
    '대사이상지방간': '/지방간/',
    '간양성종양': '/간양성종양/',
    '간수치': '/간수치/',
    'ALP-GGT': '/간수치/',
    'PIVKA-II': '/간수치/',
    '알부민-PT': '/간수치/',
    '약물성-간손상': '/간수치/',
    '알파태아단백': '/간암/',
    '알코올성-간질환': '/간경화/',
    '빌리루빈': '/간수치/',
    '술-안마셔도': '/지방간/',
    '간섬유화스캔': '/간수치/',
    '간생검': '/간수치/',
}


def detect_hub(rel_path: str) -> str | None:
    """주어진 url path가 어느 hub에 속하는지 추론."""
    if rel_path.startswith('/케이스/'):
        return None  # 케이스는 active 안 함 (다양한 hub mix)
    if rel_path == '/' or rel_path == '/index.html':
        return None
    # 1차: hub 자체
    for href, _ in HUBS:
        if rel_path == href:
            return href
    # 2차: detail slug → hub
    # /간암-진단-첫외래/ → /간암/
    slug = rel_path.strip('/').split('/')[0]
    for prefix, hub_href in HUB_DETECT.items():
        if slug == prefix or slug.startswith(prefix + '-'):
            return hub_href
    if slug.startswith('CC/'):
        return '/CC/'
    if slug.startswith('updates/'):
        return '/updates/'
    if rel_path.startswith('/케이스'):
        return None
    return None


def build_bar(active_href: str | None) -> str:
    items = []
    for href, label in HUBS:
        cls = ' class="active"' if href == active_href else ''
        items.append(f'<a href="{href}"{cls}>{label}</a>')
    return (
        f'{MARK_START}\n'
        '<nav class="hub-bar" aria-label="주제별 메뉴">\n'
        '  <div class="inner">'
        + ''.join(items) +
        '</div>\n'
        '</nav>\n'
        f'{MARK_END}'
    )


SKIP_DIRS = {'.git', '.tools', 'node_modules', 'private-figures', 'assets'}


def url_path_for_file(file_path: Path) -> str:
    rel = file_path.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('/index.html')] + '/'
    return '/' + rel


def main():
    pages = 0
    for p in ROOT.rglob('*.html'):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
            continue
        text = p.read_text(encoding='utf-8')
        if '</header>' not in text:
            continue
        url = url_path_for_file(p)
        active = detect_hub(url)
        bar = build_bar(active)
        if MARK_START in text:
            new = BLOCK_RE.sub(bar + '\n', text)
        else:
            new = HEADER_END_RE.sub(r'\1' + bar + '\n', text, count=1)
        if new != text:
            p.write_text(new, encoding='utf-8')
            pages += 1
    print(f'Pages updated: {pages}')


if __name__ == '__main__':
    main()
