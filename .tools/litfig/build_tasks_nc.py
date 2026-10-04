import json, os, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SCR = ROOT / 'private-figures/figpool'
pool = json.load(open(SCR / 'pool.json', encoding='utf-8'))
for p in pool:
    if p.get('pmcid') in ('PMC6580775',):          # 오인용이던 췌장암 논문
        p['usable'] = False; p['excluded'] = 'mis-cited paper'
json.dump(pool, open(SCR / 'pool.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
pages = json.load(open(SCR / 'pages.json', encoding='utf-8'))
page_topic = {p['page']: p['topic'] for p in pages}
# 이미 넣은 그림
for p in pages:
    s = open(f"{p['page']}/index.html", encoding='utf-8').read()
    p['existing_figures'] = re.findall(r'<!-- paper-figure:auto:start ([^ ]+) -->', s)
    p['limit'] = 2 if p['kind'] == 'detail' else 1
    p['slots_left'] = max(0, p['limit'] - len(p['existing_figures']))

GROUPS = {
    'nc_hcc': dict(topics={'hcc'}, fig_topics={'hcc', 'imaging'}),
    'nc_viral': dict(topics={'hbv', 'hcv'}, fig_topics={'hbv', 'hcv'}),
    'nc_cirr_masld': dict(topics={'cirrhosis', 'masld'}, fig_topics={'cirrhosis_portal_htn', 'masld_mash', 'acute_liver_failure_transplant'}),
    'nc_other': dict(topics={'lft', 'misc', 'autoimmune', 'benign'}, fig_topics={'liver_tests_diagnostics', 'autoimmune_cholestatic', 'benign_liver_lesions'}),
}
GUIDE_TOPIC = {'PMC9597235': 'nc_hcc', 'PMC13430407': 'nc_viral', 'PMC13430321': 'nc_viral'}
for g, cfg in GROUPS.items():
    pg = [p for p in pages if p['topic'] in cfg['topics'] and p['slots_left'] > 0]
    figs = []
    for f in pool:
        if not (f.get('usable') and f.get('nc')):
            continue
        cited = f.get('cited_by') or []
        ok = f['topic'] in cfg['fig_topics'] or GUIDE_TOPIC.get(f.get('pmcid')) == g or \
             any(page_topic.get(c) in cfg['topics'] for c in cited)
        if ok:
            d = {k: f.get(k) for k in ['id', 'thumb', 'kind', 'license', 'credit', 'article', 'label', 'caption', 'visual', 'label_ko', 'w', 'h']}
            d['cited_by'] = cited
            d['no_derivatives'] = 'ND' in (f.get('license') or '').upper()
            figs.append(d)
    json.dump(dict(group=g, pages=pg, figures=figs), open(SCR / f'task_{g}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(g, 'pages with free slots', len(pg), 'NC figs', len(figs))
