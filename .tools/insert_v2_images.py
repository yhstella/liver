#!/usr/bin/env python3
"""Insert v2 top and lower images into pages, idempotent.

Independently checks for top vs lower markup — can fill in a missing one.
"""
import json, pathlib, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
import argparse
ap = argparse.ArgumentParser()
ap.add_argument('--map', default='.tools/page_image_mapping_v2.json',
                help='mapping JSON path (relative to repo root)')
args = ap.parse_args()
with open(ROOT / args.map, encoding='utf-8') as f:
    mapping = json.load(f)


def process_page(html_path: pathlib.Path, top_src, lower_src):
    text = html_path.read_text(encoding='utf-8')
    has_top = 'page-image:auto:start' in text
    has_lower = 'page-image-lower:auto:start' in text
    changed_top = changed_lower = False

    if not has_top and top_src:
        top_html = (
            '\n<!-- page-image:auto:start -->\n'
            f'<figure class="page-top-image" aria-hidden="true">'
            f'<img src="{top_src}" alt="" loading="eager" fetchpriority="high">'
            f'</figure>\n'
            '<!-- page-image:auto:end -->'
        )
        m = re.search(r'(<div class="tldr[^"]*"[^>]*>.*?</div>)', text, re.DOTALL)
        if m:
            text = text[:m.end()] + top_html + text[m.end():]
            changed_top = True
        else:
            m = re.search(r'(<p class="publish-date">.*?</p>)', text, re.DOTALL)
            if m:
                text = text[:m.end()] + top_html + text[m.end():]
                changed_top = True
            else:
                m = re.search(r'<h1[^>]*>.*?</h1>', text, re.DOTALL)
                if m:
                    text = text[:m.end()] + top_html + text[m.end():]
                    changed_top = True

    if not has_lower and lower_src:
        lower_html = (
            '\n<!-- page-image-lower:auto:start -->\n'
            f'<figure class="page-lower-image" aria-hidden="true">'
            f'<img src="{lower_src}" alt="" loading="lazy">'
            f'</figure>\n'
            '<!-- page-image-lower:auto:end -->\n'
        )
        h2_positions = [m.start() for m in re.finditer(r'<h2[^>]*>', text)]
        if len(h2_positions) >= 4:
            target_idx = h2_positions[len(h2_positions) // 2]
        elif len(h2_positions) >= 3:
            target_idx = h2_positions[-2]
        elif len(h2_positions) >= 2:
            target_idx = h2_positions[-1]
        elif len(h2_positions) == 1:
            target_idx = h2_positions[0]
        else:
            target_idx = None
        if target_idx is not None:
            text = text[:target_idx] + lower_html + text[target_idx:]
            changed_lower = True

    if changed_top or changed_lower:
        html_path.write_text(text, encoding='utf-8')
    return changed_top, changed_lower


added_top = added_lower = skipped = 0
for url, info in mapping.items():
    slug = url.strip('/')
    p = ROOT / f'{slug}/index.html'
    if not p.exists():
        print(f'MISSING HTML: {url}')
        continue
    top_ok = info.get('top')
    lower_ok = info.get('lower')
    ct, cl = process_page(p, top_ok, lower_ok)
    if ct:
        added_top += 1
    if cl:
        added_lower += 1
    if not ct and not cl:
        skipped += 1

print(f'Added top: {added_top}, Added lower: {added_lower}, Already complete: {skipped}')
