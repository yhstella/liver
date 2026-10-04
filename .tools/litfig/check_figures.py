"""그림 블록 위치 점검 + 초안 유출 점검."""
import json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SKIP = {'.git', 'private-figures', '.tools', 'assets', 'node_modules'}
n, problems = 0, []
drafts = []
for f in sorted(Path('.').rglob('index.html')):
    if any(x in SKIP for x in f.parts):
        continue
    s = f.read_text(encoding='utf-8')
    page = '/'.join(f.parts[:-1])
    if re.search(r'<!--\s*DRAFT', s[:8000]):
        drafts.append(page)
    refs = s.find('references-block')
    for m in re.finditer(r'<!-- paper-figure:auto:start ([^ ]+) -->', s):
        n += 1
        before = s[:m.start()]
        if before.count('<details') > before.count('</details>'):
            problems.append((page, m.group(1), 'inside details'))
        if 0 <= refs < m.start():
            problems.append((page, m.group(1), 'after references'))
        if before.count('<table') > before.count('</table>'):
            problems.append((page, m.group(1), 'inside table'))
        if before.count('<ul') > before.count('</ul>') or before.count('<ol') > before.count('</ol>'):
            problems.append((page, m.group(1), 'inside list'))
        if before.count('<p>') + before.count('<p ') > before.count('</p>'):
            problems.append((page, m.group(1), 'inside paragraph'))
leak = []
for gen in ['sitemap.xml', 'search-index.json', 'updates.xml', 'llms.txt', 'llms-full.txt']:
    if os.path.exists(gen):
        g = open(gen, encoding='utf-8').read()
        for d in drafts:
            if d in g or d.replace('/', '%2F') in g:
                leak.append((gen, d))
print('figure blocks:', n, '| problems:', problems)
print('drafts:', len(drafts), '| leaks:', leak)
