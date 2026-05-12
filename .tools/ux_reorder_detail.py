#!/usr/bin/env python3
"""
UX: Reorder detail page blocks for better reading flow.

현재 순서: H1 → publish-date → db-figure → tag-row → TLDR → SVG/body
개선 순서: H1 → tag-row → TLDR → db-figure → SVG/body
         + publish-date → 본문 끝(author-mini 직전) 이동

이유: 환자가 페이지 도달 즉시 핵심 요약(TLDR)을 봐야 하는데,
큰 figure가 사이를 가로막아 도달 지연.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Detail page indicators
HUBS = {'간암','간경화','B형간염','C형간염','지방간','간수치','자가면역간염','간양성종양'}
SECT = {'CC','updates','케이스','keywords','소개','연구','guide','논문','assets','.tools','.git','private-figures'}


def gather_detail_pages():
    targets = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith('.') or d.name in HUBS or d.name in SECT:
            continue
        idx = d / 'index.html'
        if idx.exists():
            text = idx.read_text(encoding='utf-8')
            # detail page = has <article> + <h1> + (tag-row OR tldr)
            if '<article>' in text and '<h1' in text and ('tag-row' in text or 'tldr' in text):
                targets.append(d.name)
    return targets


# Pattern 1: extract db-figure block
DB_FIG = re.compile(
    r'<!--\s*db-figure:auto:start\s*-->.*?<!--\s*db-figure:auto:end\s*-->\s*\n?',
    re.DOTALL,
)

# Pattern 2: extract tag-row block
TAG_ROW = re.compile(
    r'<!--\s*tags\s*-->\s*\n?<p class="tag-row">.*?</p>\s*\n?<!--\s*/tags\s*-->\s*\n?',
    re.DOTALL,
)
# fallback (no comment markers)
TAG_ROW_BARE = re.compile(r'<p class="tag-row">.*?</p>\s*\n?', re.DOTALL)

# Pattern 3: extract TLDR block
TLDR = re.compile(r'<div class="tldr"[^>]*>.*?</div>\s*\n?', re.DOTALL)

# Pattern 4: extract publish-date block
PUB_DATE = re.compile(r'<p class="publish-date">.*?</p>\s*\n?', re.DOTALL)


def reorder_page(path: Path) -> tuple[bool, str]:
    text = path.read_text(encoding='utf-8')
    orig = text

    # Extract blocks
    fig_m = DB_FIG.search(text)
    fig_block = fig_m.group(0) if fig_m else ''
    if fig_m:
        text = text[:fig_m.start()] + text[fig_m.end():]

    tag_m = TAG_ROW.search(text)
    if tag_m:
        tag_block = tag_m.group(0)
        text = text[:tag_m.start()] + text[tag_m.end():]
    else:
        # bare pattern
        tag_m = TAG_ROW_BARE.search(text)
        tag_block = tag_m.group(0) if tag_m else ''
        if tag_m:
            text = text[:tag_m.start()] + text[tag_m.end():]

    tldr_m = TLDR.search(text)
    tldr_block = tldr_m.group(0) if tldr_m else ''
    if tldr_m:
        text = text[:tldr_m.start()] + text[tldr_m.end():]

    pub_m = PUB_DATE.search(text)
    pub_block = pub_m.group(0) if pub_m else ''
    if pub_m:
        text = text[:pub_m.start()] + text[pub_m.end():]

    if not (fig_block or tag_block or tldr_block):
        return False, 'no blocks to reorder'

    # Build target order: tag → tldr → fig
    target_order = ''
    if tag_block:
        target_order += tag_block.rstrip() + '\n'
    if tldr_block:
        target_order += tldr_block.rstrip() + '\n\n'
    if fig_block:
        target_order += fig_block.rstrip() + '\n\n'

    # Insert right after </h1>
    h1_m = re.search(r'</h1>\s*\n?', text)
    if not h1_m:
        return False, 'no </h1>'
    text = text[:h1_m.end()] + target_order + text[h1_m.end():]

    # Re-insert publish-date near author-mini (or before </article>)
    if pub_block:
        # Look for author-mini block — insert publish-date BEFORE it
        author_m = re.search(r'<aside[^>]*class="[^"]*author-mini[^"]*"|<div[^>]*class="author-mini"|<!--\s*author:auto:start\s*-->', text)
        if author_m:
            insertion = pub_block.rstrip() + '\n\n'
            text = text[:author_m.start()] + insertion + text[author_m.start():]
        else:
            # fallback: before </article>
            close_m = re.search(r'</article>', text)
            if close_m:
                text = text[:close_m.start()] + pub_block.rstrip() + '\n' + text[close_m.start():]

    if text == orig:
        return False, 'no change after reorder'
    path.write_text(text, encoding='utf-8')
    return True, 'reordered'


def main():
    targets = gather_detail_pages()
    print(f'found {len(targets)} detail pages')
    n_changed = 0
    for slug in targets:
        path = ROOT / slug / 'index.html'
        ok, msg = reorder_page(path)
        if ok:
            n_changed += 1
    print(f'\nreordered: {n_changed} / {len(targets)}')


if __name__ == '__main__':
    main()
