#!/usr/bin/env python3
"""Insert top + lower images into /updates/ and /케이스/ pages.

Top image: after tldr or publish-date.
Lower image: at middle h2.

Idempotent: skips pages with existing page-image markers.
"""
import json, pathlib, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent
with open(ROOT / '.tools/updates_cases_image_mapping.json', encoding='utf-8') as f:
    mapping = json.load(f)


def insert_images(html_path, top_src, lower_src):
    p = pathlib.Path(html_path)
    text = p.read_text(encoding='utf-8')
    if 'page-top-image' in text or 'page-image:auto:start' in text:
        return 'SKIP'

    top_html = (
        '\n<!-- page-image:auto:start -->\n'
        f'<figure class="page-top-image" aria-hidden="true">'
        f'<img src="{top_src}" alt="" loading="eager" fetchpriority="high">'
        f'</figure>\n'
        '<!-- page-image:auto:end -->'
    )
    lower_html = (
        '\n<!-- page-image-lower:auto:start -->\n'
        f'<figure class="page-lower-image" aria-hidden="true">'
        f'<img src="{lower_src}" alt="" loading="lazy">'
        f'</figure>\n'
        '<!-- page-image-lower:auto:end -->\n'
    )

    new_text = text
    inserted_top = False

    # 1) Top image — after tldr div if present, else publish-date paragraph, else first h2 entry
    m = re.search(r'(<div class="tldr[^"]*"[^>]*>.*?</div>)', new_text, re.DOTALL)
    if m:
        new_text = new_text[:m.end()] + top_html + new_text[m.end():]
        inserted_top = True
    else:
        m = re.search(r'(<p class="publish-date">.*?</p>)', new_text, re.DOTALL)
        if m:
            new_text = new_text[:m.end()] + top_html + new_text[m.end():]
            inserted_top = True
        else:
            # Updates pages may not have publish-date. Insert before first <h2>.
            m = re.search(r'<h1[^>]*>.*?</h1>', new_text, re.DOTALL)
            if m:
                new_text = new_text[:m.end()] + top_html + new_text[m.end():]
                inserted_top = True

    h2_positions = [m.start() for m in re.finditer(r'<h2[^>]*>', new_text)]
    inserted_lower = False
    if len(h2_positions) >= 4:
        target_idx = h2_positions[len(h2_positions) // 2]
        new_text = new_text[:target_idx] + lower_html + new_text[target_idx:]
        inserted_lower = True
    elif len(h2_positions) >= 3:
        target_idx = h2_positions[-2]
        new_text = new_text[:target_idx] + lower_html + new_text[target_idx:]
        inserted_lower = True
    elif len(h2_positions) >= 2:
        target_idx = h2_positions[-1]
        new_text = new_text[:target_idx] + lower_html + new_text[target_idx:]
        inserted_lower = True
    elif len(h2_positions) == 1:
        # Single h2 — place lower image right after the first paragraph after h2 (i.e., before next p tag after h2)
        target_idx = h2_positions[0]
        new_text = new_text[:target_idx] + lower_html + new_text[target_idx:]
        inserted_lower = True

    p.write_text(new_text, encoding='utf-8')
    return f'OK (top={inserted_top},lower={inserted_lower})'


ok = skip = err = 0
no_top = no_lower = 0
for url, info in mapping.items():
    slug = url.strip('/')
    html = ROOT / f'{slug}/index.html'
    if not html.exists():
        print(f'MISSING HTML: {url}')
        err += 1
        continue
    try:
        result = insert_images(html, info['top'], info['lower'])
        if result == 'SKIP':
            skip += 1
        else:
            ok += 1
            if 'top=False' in result:
                no_top += 1
                print(f'  NO TOP {url}')
            if 'lower=False' in result:
                no_lower += 1
                print(f'  NO LOWER {url}')
    except Exception as e:
        err += 1
        print(f'ERROR {url}: {e}')

print(f'\nOK: {ok}, SKIP: {skip}, ERROR: {err}')
print(f'No top insertion: {no_top}, No lower insertion: {no_lower}')
