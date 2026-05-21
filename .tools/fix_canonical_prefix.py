"""
Fix canonical/og:url/JSON-LD references that miss a /prefix/ segment.

For each subfolder under PARENT (e.g. 'updates' or 'CC'), find any literal
occurrence of 'https://drshin.kr/<slug>/' (without the prefix) and rewrite to
'https://drshin.kr/<PARENT>/<slug>/'. Idempotent: already-correct files match
nothing because their URLs contain '<PARENT>/'.
"""
import os, sys, re, urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def fix_under(parent):
    parent_dir = os.path.join(ROOT, parent)
    if not os.path.isdir(parent_dir):
        print(f'SKIP: {parent_dir} not found')
        return 0, 0
    fixed_files = 0
    total_replacements = 0
    for name in sorted(os.listdir(parent_dir)):
        sub = os.path.join(parent_dir, name)
        idx = os.path.join(sub, 'index.html')
        if not os.path.isfile(idx):
            continue
        slug = name
        slug_enc = urllib.parse.quote(slug, safe='-_.~')
        with open(idx, 'r', encoding='utf-8') as f:
            content = f.read()
        variants = {slug, slug_enc}
        total = 0
        new_content = content
        for v in variants:
            bare = f'https://drshin.kr/{v}/'
            good = f'https://drshin.kr/{parent}/{v}/'
            c = new_content.count(bare)
            if c:
                new_content = new_content.replace(bare, good)
                total += c
        count = total
        if count == 0:
            continue
        with open(idx, 'w', encoding='utf-8', newline='') as f:
            f.write(new_content)
        print(f'FIXED  {parent}/{slug}/index.html  ({count} occurrences)')
        fixed_files += 1
        total_replacements += count
    return fixed_files, total_replacements

if __name__ == '__main__':
    parents = sys.argv[1:] or ['updates', 'CC']
    grand_files = 0
    grand_repl = 0
    for p in parents:
        f, r = fix_under(p)
        grand_files += f
        grand_repl += r
        print(f'  → {p}: {f} files, {r} replacements')
    print(f'\nTOTAL: {grand_files} files modified, {grand_repl} replacements')
