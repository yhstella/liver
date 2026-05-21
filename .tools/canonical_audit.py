import os, re, urllib.parse
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
canonicals = {}
duplicates = defaultdict(list)
mismatches = []
no_canon = []

SKIP = ('assets', 'private-figures', '.git', 'guide', '.tools')

for root, dirs, files in os.walk(ROOT):
    rel = os.path.relpath(root, ROOT).replace('\\', '/')
    if any(rel.startswith(s) or '/' + s in '/' + rel for s in SKIP):
        continue
    if 'index.html' not in files:
        continue
    fp = os.path.join(root, 'index.html')
    rel_dir = rel if rel != '.' else ''
    expected = '/' + rel_dir + '/' if rel_dir else '/'
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        head = f.read(4000)
    m = re.search(r'<link rel="canonical" href="([^"]+)"', head)
    if not m:
        no_canon.append(fp)
        continue
    canon = m.group(1)
    canonicals[fp] = canon
    duplicates[canon].append(fp)
    canon_path = urllib.parse.urlparse(canon).path
    canon_path_decoded = urllib.parse.unquote(canon_path)
    if canon_path_decoded != expected:
        mismatches.append((fp, expected, canon, canon_path_decoded))

import json
with open(os.path.join(ROOT, '.tools', 'audit_report.json'), 'w', encoding='utf-8') as rf:
    json.dump({
        'no_canon': [os.path.relpath(f, ROOT).replace('\\', '/') for f in no_canon],
        'duplicates': {c: [os.path.relpath(f, ROOT).replace('\\', '/') for f in fps] for c, fps in duplicates.items() if len(fps) > 1},
        'mismatches': [{'file': os.path.relpath(fp, ROOT).replace('\\', '/'), 'expected': exp, 'canonical': canon, 'decoded': dec} for fp, exp, canon, dec in mismatches],
    }, rf, ensure_ascii=False, indent=2)

print('TOTAL pages with index.html:', len(canonicals) + len(no_canon))
print('With canonical:', len(canonicals))
print('Without canonical:', len(no_canon))
for f in no_canon:
    print('  NO_CANONICAL:', f)
print()
print('=== Duplicate canonicals (multiple files -> same URL) ===')
dup_count = 0
for c, fps in duplicates.items():
    if len(fps) > 1:
        dup_count += 1
        print(c)
        for f in fps:
            print(' ', os.path.relpath(f, ROOT))
print('Duplicate canonical groups:', dup_count)
print()
print('=== Path/canonical mismatches ===')
for fp, exp, canon, canon_dec in mismatches:
    print('FILE:', os.path.relpath(fp, ROOT))
    print('  EXPECTED PATH:', exp)
    print('  CANONICAL URL:', canon)
    print('  DECODED PATH :', canon_dec)
print('TOTAL MISMATCHES:', len(mismatches))
