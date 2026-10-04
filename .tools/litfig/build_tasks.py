import json, re, collections, os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SCR = ROOT / 'private-figures/figpool'
pool = json.load(open(SCR / 'pool.json', encoding='utf-8'))
for p in pool:
    if p['pmcid'] in ('PMC8279539', 'PMC7865804'):
        p['usable'] = False; p['excluded'] = 'mis-cited paper'
json.dump(pool, open(SCR / 'pool.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

SKIP = {'guide', 'keywords', '논문', '자가면역간염', '문의', '단상', '소개', '연구', 'private-figures', '.tools', 'assets', '.git'}
HUBS = {'간암': 'hcc', '간경화': 'cirrhosis', 'B형간염': 'hbv', 'C형간염': 'hcv', '지방간': 'masld', '간수치': 'lft', '자가면역간질환': 'autoimmune', '간양성종양': 'benign'}
KW = [('hcc', r'간암|HCC|간세포암|TACE|색전|BCLC|AFP|PIVKA|LR[-_]?\d|결절|면역치료|atezo|STRIDE|IMbrave|HIMALAYA|렌바|소라페닙|lenvatinib|sorafenib|절제|소작|이식|전이|SBRT|방사선|EMERALD|TALENTOP|LEAP'),
      ('hbv', r'B형|HBV|HBe|HBs|HDV|D형|항바이러스|TAF|TDF|ETV|bepirovirsen|siRNA'),
      ('hcv', r'C형|HCV|DAA|SVR'),
      ('cirrhosis', r'간경변|간경화|복수|정맥류|SBP|간성|MELD|TIPS|Baveno|문맥|혈소판|근감소|Recompensation|저나트륨|tolvaptan|간신|Sarcopenia'),
      ('masld', r'지방간|MASLD|MASH|NASH|GLP|위고비|마운자로|tirzepatide|semaglutide|resmetirom|비만|Lean|MetALD|SGLT|Retatrutide|EFX'),
      ('autoimmune', r'자가면역|AIH|PBC|PSC|담관염|IgG4|overlap'),
      ('benign', r'혈관종|낭종|FNH|선종|adenoma|hamartoma|NRH|fat-sparing|양성'),
      ('lft', r'간수치|ALT|AST|빌리루빈|ALP|GGT|DILI|약물성|보충제|운동|근육|PEth|알코올|음주|검진|간생검|검사')]
pages = []
for f in sorted(Path('.').rglob('index.html')):
    parts = f.parts
    if any(x in SKIP for x in parts) or len(parts) < 2:
        continue
    if len(parts) == 2 and parts[0] in HUBS:
        continue
    s = f.read_text(encoding='utf-8', errors='ignore')
    if 'http-equiv="refresh"' in s:
        continue
    rel = '/'.join(parts[:-1])
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    title = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else rel
    crumb = re.search(r'<nav class="crumb">(.*?)</nav>', s, re.S)
    hubs = [HUBS[h] for h in re.findall(r'href="/([^"/]+)/"', crumb.group(1)) if h in HUBS] if crumb else []
    kind = 'case' if parts[0] == '케이스' else 'cc' if parts[0] == 'CC' else 'update' if parts[0] == 'updates' else 'detail'
    topic = hubs[0] if hubs else None
    if not topic:
        for t, pat in KW:
            if re.search(pat, rel + ' ' + title, re.I):
                topic = t; break
    a0 = s.find('<article'); a1 = s.find('references-block') if 'references-block' in s else s.find('</article>')
    art = s[a0:a1]
    h2 = [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<h2[^>]*>(.*?)</h2>', art, re.S)]
    h2 = [x for x in h2 if x and x not in ('References', '자주 묻는 질문', '관련 글')]
    first = re.search(r'<p>(.*?)</p>', art, re.S)
    pages.append(dict(page=rel, kind=kind, topic=topic or 'misc', title=title, h2=h2[:14],
                      intro=re.sub(r'<[^>]+>', '', first.group(1))[:220] if first else '',
                      draft=bool(re.search(r'<!--\s*DRAFT', s[:8000])),
                      has_paper_fig=('/assets/img/papers/' in s) or ('paper-figure:auto' in s)))
print('pages', len(pages)); print(sorted(collections.Counter((p['topic'], p['kind']) for p in pages).items()))
json.dump(pages, open(SCR / 'pages.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

FT = {'hcc': ['hcc', 'imaging'], 'cirrhosis': ['cirrhosis_portal_htn', 'acute_liver_failure_transplant'], 'hbv': ['hbv'], 'hcv': ['hcv'],
      'masld': ['masld_mash'], 'lft': ['liver_tests_diagnostics'], 'autoimmune': ['autoimmune_cholestatic'], 'benign': ['benign_liver_lesions', 'imaging']}
page_topic = {p['page']: p['topic'] for p in pages}
for t, fts in FT.items():
    pg = [p for p in pages if p['topic'] == t or (t == 'lft' and p['topic'] == 'misc')]
    figs = []
    for f in pool:
        if not f['usable']:
            continue
        cited_pages = [c.replace(chr(92), '/') for c in f.get('cited_by', [])]
        if f['topic'] in fts or (f['topic'] == 'cited' and any(page_topic.get(c) == t or (t == 'lft' and page_topic.get(c) == 'misc') for c in cited_pages)):
            g = {k: f.get(k) for k in ['id', 'thumb', 'kind', 'license', 'credit', 'article', 'label', 'caption', 'visual', 'label_ko', 'w', 'h']}
            g['cited_by'] = cited_pages
            figs.append(g)
    json.dump(dict(topic=t, pages=pg, figures=figs), open(SCR / f'figpool/task_{t}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(t, 'pages', len(pg), 'figs', len(figs))
