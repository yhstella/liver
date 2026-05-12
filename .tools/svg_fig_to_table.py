#!/usr/bin/env python3
"""inline SVG class='fig' 표 그림을 HTML <table>로 변환.

SVG 구조 가정:
  <svg class="fig" viewBox="..." aria-label="...">
    <text ...>제목</text>                                  ← 첫 번째 text (선택)
    <rect x="X" y="Y" width="W" height="H" fill="HEX"/>   ← 셀 배경
    <text x="..." y="..." ...>셀 내용</text>                ← 셀 내용
    ...
  </svg>
  <p class="fig-caption">캡션</p>

알고리즘:
  1. rect 요소 추출 (좌표 + fill)
  2. text 요소 추출 (좌표 + 내용)
  3. text가 어느 rect 안에 위치하는지 매칭
  4. Y 좌표로 row 그룹핑 (±5px 허용)
  5. fill=#f3f1ec ⇒ header row 표시
  6. caption은 <table> 위에 표시 또는 caption 태그

변환 실패 케이스(병합 셀, 비-그리드 SVG)는 SVG 그대로 보존.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','간양성종양',
    '케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search',
    '.tools','.git','.github','private-figures','node_modules',
}

SVG_RE = re.compile(
    r'<svg class="fig"[^>]*?(?:aria-label="([^"]*)")?[^>]*>(.*?)</svg>(\s*<p class="fig-caption">([^<]*)</p>)?',
    re.DOTALL,
)

RECT_RE = re.compile(
    r'<rect\s+x="([\d.]+)"\s+y="([\d.]+)"\s+width="([\d.]+)"\s+height="([\d.]+)"[^>]*?fill="([^"]+)"',
    re.IGNORECASE,
)

TEXT_RE = re.compile(
    r'<text\s+x="([\d.]+)"\s+y="([\d.]+)"[^>]*?(?:font-weight="(\d+)")?[^>]*?>([^<]*)</text>',
    re.IGNORECASE,
)


def parse_svg(svg_body: str):
    rects = []
    for m in RECT_RE.finditer(svg_body):
        rects.append({
            'x': float(m.group(1)),
            'y': float(m.group(2)),
            'w': float(m.group(3)),
            'h': float(m.group(4)),
            'fill': m.group(5).lower(),
        })
    texts = []
    for m in TEXT_RE.finditer(svg_body):
        texts.append({
            'x': float(m.group(1)),
            'y': float(m.group(2)),
            'bold': bool(m.group(3) and int(m.group(3)) >= 600),
            'text': m.group(4).strip(),
        })
    return rects, texts


def find_containing_rect(text: dict, rects: list) -> dict | None:
    """text의 (x, y)가 어느 rect 안에 위치하는지 (text-anchor는 보통 middle이므로 y 기준만 정확)."""
    for r in rects:
        # y로 row 식별, x는 rect 범위 내인지
        if r['y'] <= text['y'] <= r['y'] + r['h']:
            if r['x'] - 2 <= text['x'] <= r['x'] + r['w'] + 2:
                return r
    return None


def convert(svg_inner: str, caption: str = '') -> str | None:
    rects, texts = parse_svg(svg_inner)
    if not rects:
        return None

    # Build cell map: (rect_x, rect_y) -> text
    cell_map = {}
    title = ''
    for t in texts:
        # 첫 번째 text는 SVG 안에 있지 않으면 제목 (y가 가장 작거나 rect 위쪽)
        rect = find_containing_rect(t, rects)
        if rect is None:
            if not title and t['bold']:
                title = t['text']
            continue
        key = (round(rect['x']), round(rect['y']))
        prev = cell_map.get(key, '')
        cell_map[key] = (prev + ' ' + t['text']).strip() if prev else t['text']

    # Group rects by Y (rows)
    rows = {}
    for r in rects:
        y = round(r['y'])
        rows.setdefault(y, []).append(r)
    ordered_ys = sorted(rows.keys())
    if not ordered_ys:
        return None

    # Each row: sort by x
    grid = []
    header_ys = set()
    for y in ordered_ys:
        row_rects = sorted(rows[y], key=lambda r: r['x'])
        is_header = any('f3f1ec' in r['fill'] for r in row_rects)
        if is_header:
            header_ys.add(y)
        row_cells = []
        for r in row_rects:
            key = (round(r['x']), y)
            row_cells.append(cell_map.get(key, ''))
        grid.append((y, is_header, row_cells))

    if len(grid) < 2:
        return None  # 표로서 의미 없는 SVG

    # Check column count consistency (allow ±1)
    col_counts = [len(g[2]) for g in grid]
    if max(col_counts) - min(col_counts) > 1:
        return None  # 비균일 그리드, 자동 변환 위험

    # Build HTML table
    lines = ['<table>']
    if title:
        lines.append(f'<caption style="caption-side:top;text-align:left;font-weight:600;color:var(--accent);font-size:14px;margin-bottom:6px">{title}</caption>')
    in_thead = False
    in_tbody = False
    for y, is_header, cells in grid:
        cells_html = [c.replace('&lt;', '&lt;').replace('&gt;', '&gt;') for c in cells]
        if is_header:
            if not in_thead:
                lines.append('<thead>')
                in_thead = True
            row_html = ''.join(f'<th>{c}</th>' for c in cells_html)
            lines.append(f'<tr>{row_html}</tr>')
        else:
            if in_thead:
                lines.append('</thead>')
                in_thead = False
            if not in_tbody:
                lines.append('<tbody>')
                in_tbody = True
            row_html = ''.join(f'<td>{c}</td>' for c in cells_html)
            lines.append(f'<tr>{row_html}</tr>')
    if in_thead:
        lines.append('</thead>')
    if in_tbody:
        lines.append('</tbody>')
    lines.append('</table>')
    if caption:
        lines.append(f'<p class="fig-caption" style="font-size:12.5px;color:var(--muted);margin-top:-8px">{caption}</p>')
    return '\n'.join(lines)


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in EXCLUDE and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx


def main():
    converted_total = 0
    pages_changed = 0
    failed = []
    for f in detail_pages():
        text = f.read_text(encoding='utf-8')
        new = text
        page_converted = 0
        for m in list(SVG_RE.finditer(text)):
            svg_inner = m.group(2)
            caption = m.group(4) or ''
            html = convert(svg_inner, caption=caption)
            if html is None:
                failed.append((f.parent.name, m.group(1) or '(no label)'))
                continue
            full = m.group(0)
            new = new.replace(full, html, 1)
            page_converted += 1
        if new != text:
            f.write_text(new, encoding='utf-8')
            pages_changed += 1
            converted_total += page_converted
            print(f'  {f.parent.name}: {page_converted} svg→table')

    print(f'\nPages changed: {pages_changed}')
    print(f'SVG converted: {converted_total}')
    if failed:
        print(f'\nFailed conversions ({len(failed)}):')
        for slug, label in failed[:20]:
            print(f'  {slug}: {label}')


if __name__ == '__main__':
    main()
