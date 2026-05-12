#!/usr/bin/env python3
"""Related-auto block 누락 페이지 일괄 보강 (간단 버전).

전략:
  1. 모든 detail/case/update/cc 페이지 메타데이터 (path, title, hub, page-id) 수집
  2. 각 페이지의 hub와 같은 hub 내 sibling 4개를 랜덤 추출 (현재 페이지 제외)
  3. <aside class="related-auto"> ... </aside> 형식으로 삽입
삽입 위치: </article> 직전 (있으면), 또는 disclaimer 직전, 또는 </main> 직전
이미 있으면 skip.
"""
import re
import random
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
random.seed(42)  # 결정론적 출력

HUB_DIRS = {'간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','간양성종양','케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search','.tools','.git','.github','private-figures','node_modules'}
HUB_BY_HREF = {'/간암/': '간암', '/간경화/': '간경화', '/B형간염/': 'B형간염', '/지방간/': '지방간',
               '/간수치/': '간수치', '/C형간염/': 'C형간염', '/자가면역간염/': '자가면역간염', '/간양성종양/': '간양성종양'}

CRUMB_RE = re.compile(r'<nav class="crumb">.*?<a href="(/[^/]+/)"[^>]*>[^<]*</a>', re.DOTALL)
H1_RE = re.compile(r'<h1[^>]*>([^<]+)</h1>')
PID_RE = re.compile(r'<span class="page-id">([^<]+)</span>')


def gather():
    """Return list of {path, url, h1, hub, pid, kind}."""
    items = []

    def add(idx: Path, kind: str, base_url_dir: str = ''):
        txt = idx.read_text(encoding='utf-8')
        h1m = H1_RE.search(txt)
        if not h1m:
            return
        h1 = h1m.group(1).strip()
        # Determine hub
        if kind == 'detail':
            cm = CRUMB_RE.search(txt)
            hub = HUB_BY_HREF.get(cm.group(1)) if cm else None
        elif kind == 'case':
            cm = CRUMB_RE.search(txt)
            hub = HUB_BY_HREF.get(cm.group(1)) if cm else None
        elif kind == 'cc':
            hub = None
        else:
            hub = None
        pidm = PID_RE.search(txt)
        pid = pidm.group(1) if pidm else ''
        slug = idx.parent.name
        url = f'/{base_url_dir}{slug}/' if base_url_dir else f'/{slug}/'
        items.append({'path': idx, 'url': url, 'h1': h1, 'hub': hub, 'pid': pid, 'kind': kind})

    # Detail pages
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in HUB_DIRS and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                add(idx, 'detail')

    for sub, kind in [('케이스', 'case'), ('CC', 'cc'), ('updates', 'update')]:
        base = ROOT / sub
        if base.exists():
            for p in base.iterdir():
                if p.is_dir() and not p.name.startswith('.'):
                    idx = p / 'index.html'
                    if idx.exists():
                        add(idx, kind, f'{sub}/')
    return items


def pick_related(item, pool):
    """4개 추출: same hub > 3 + same kind > 1 (다양성)."""
    candidates = [x for x in pool if x['path'] != item['path']]
    same_hub = [x for x in candidates if x.get('hub') and x['hub'] == item.get('hub')]
    same_kind = [x for x in candidates if x['kind'] == item['kind'] and x not in same_hub]
    picks = []
    if same_hub:
        random.shuffle(same_hub)
        picks.extend(same_hub[:3])
    if same_kind and len(picks) < 4:
        random.shuffle(same_kind)
        for x in same_kind:
            if x not in picks:
                picks.append(x)
            if len(picks) >= 4:
                break
    if len(picks) < 4:
        rest = [x for x in candidates if x not in picks]
        random.shuffle(rest)
        picks.extend(rest[:4 - len(picks)])
    return picks[:4]


def make_block(picks):
    lines = []
    for x in picks:
        href = urllib.parse.quote(x['url'], safe='/-_·')
        pid = f' <span class="rel-pid">{x["pid"]}</span>' if x['pid'] else ''
        lines.append(f'<li><a href="{href}">{x["h1"]}</a>{pid}</li>')
    return ('<aside class="related-auto"><h2>관련 글</h2><ul>'
            + ''.join(lines) + '</ul></aside>\n<!-- /related -->')


def has_related(txt: str) -> bool:
    return 'related-auto' in txt or '<!-- /related -->' in txt


def inject(text: str, block: str) -> tuple[str, bool]:
    if has_related(text):
        return text, False
    # Try: before disclaimer
    if 'class="disclaimer"' in text:
        # insert block right before disclaimer
        idx = text.find('<p class="disclaimer"')
        if idx > 0:
            return text[:idx] + block + '\n' + text[idx:], True
    if '</article>' in text:
        return text.replace('</article>', f'\n{block}\n</article>', 1), True
    if '</main>' in text:
        return text.replace('</main>', f'\n{block}\n</main>', 1), True
    return text, False


def main():
    items = gather()
    print(f'Gathered: {len(items)} pages')
    hit = 0
    by_kind = {}
    for item in items:
        txt = item['path'].read_text(encoding='utf-8')
        if has_related(txt):
            continue
        picks = pick_related(item, items)
        if not picks:
            continue
        block = make_block(picks)
        new, changed = inject(txt, block)
        if changed:
            item['path'].write_text(new, encoding='utf-8')
            hit += 1
            by_kind[item['kind']] = by_kind.get(item['kind'], 0) + 1
    print(f'Injected related-auto on {hit} pages')
    for k, v in by_kind.items():
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
