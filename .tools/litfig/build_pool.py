import csv, io, json, os, re, time, urllib.request, urllib.parse, urllib.error, hashlib
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SCR = ROOT / 'private-figures/figpool'
OUT = SCR; (OUT / 'thumbs').mkdir(parents=True, exist_ok=True)
OA_DIR = Path('private-figures/paper-oa'); OA_DIR.mkdir(parents=True, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}


def get(url, t=40):
    for k in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and k < 5:
                time.sleep(4 * (k + 1)); continue
            raise
        except Exception:
            if k < 5:
                time.sleep(4 * (k + 1)); continue
            raise


def lic_short(t):
    s = (t or '').lower()
    m = re.search(r'creativecommons\.org/(licenses|publicdomain)/([a-z\-]+)/(\d\.\d)', s)
    if m:
        kind, code, ver = m.groups()
        if kind == 'publicdomain' or code == 'zero':
            return 'CC0'
        return f'CC {code.upper()} {ver}'
    for pat, name in [('by-nc-nd', 'CC BY-NC-ND'), ('by-nc-sa', 'CC BY-NC-SA'), ('by-nc', 'CC BY-NC'), ('non-commercial', 'CC BY-NC'),
                      ('share alike 4.0', 'CC BY-SA 4.0'), ('share alike 3.0', 'CC BY-SA 3.0'), ('share alike 2.5', 'CC BY-SA 2.5'), ('share alike 2.0', 'CC BY-SA 2.0'),
                      ('cc0', 'CC0'), ('public domain', 'Public domain'), ('no known copyright', 'No known copyright restrictions'),
                      ('attribution 4.0', 'CC BY 4.0'), ('attribution 3.0', 'CC BY 3.0'), ('attribution 2.5', 'CC BY 2.5'), ('attribution 2.0', 'CC BY 2.0'),
                      ('cc by 4.0', 'CC BY 4.0'), ('cc by 3.0', 'CC BY 3.0'), ('cc by 2.0', 'CC BY 2.0')]:
        if pat in s:
            return name
    return 'UNKNOWN'


def usable(ls):
    return ls != 'UNKNOWN' and 'NC' not in ls and 'ND' not in ls


pool = []
# 1) personal-web-figures (PMC OA + Wikimedia)
for r in csv.DictReader(io.open('private-figures/personal-web-figures/manifest.csv', encoding='utf-8-sig')):
    ls = lic_short(r['license_text'])
    pool.append(dict(id=r['figure_id'], src=r['local_path'], kind=r['source_kind'], pmcid=r['pmcid'], doi=r['doi'],
                     article=r['article_title'], label=r['figure_label'], caption=(r['caption'] or r['figure_title'])[:500],
                     visual=r['visual_type'], topic=r['primary_topic'] or r['topic'], label_ko=r['label_ko'],
                     license=ls, usable=usable(ls), source_url=r['source_url']))
# 2) open-license-audit (Wikimedia, db 폴더 안)
for r in csv.DictReader(io.open('private-figures/open-license-audit/all-open-license-current.csv', encoding='utf-8-sig')):
    sf = dict(kv.split('=', 1) for kv in r['source_file'].split('|')[1:] if '=' in kv)
    ls = lic_short(sf.get('license', ''))
    pool.append(dict(id=r['image_id'], src=r['local_path'], kind='wikimedia_commons', pmcid='', doi='', article='', label='',
                     caption=r['context_excerpt'][:500], visual='', topic=r['topics'].split(';')[0], label_ko=r['meaning_ko'],
                     license=ls, usable=usable(ls), source_url=sf.get('url', ''), author=sf.get('author', '')[:200]))

# 3) 사이트가 인용한 CC BY 논문의 그림
cited = json.load(open(SCR / 'cited_oa.json', encoding='utf-8'))
pm_pages = json.load(open(SCR / 'cited_pmids.json', encoding='utf-8'))
for pmid, v in cited.items():
    if not v.get('pmcid') or (v.get('license') or '').lower() not in ('cc by', 'cc0', 'cc by-sa'):
        continue
    pmc = v['pmcid']; d = OA_DIR / pmc; d.mkdir(exist_ok=True)
    try:
        html = get(f'https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/').decode('utf-8', 'replace')
        xml = get(f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML', 60).decode('utf-8', 'replace')
    except Exception as e:
        print('skip', pmc, e); continue
    blobs = {u.rsplit('/', 1)[1]: u for u in set(re.findall(r'https://cdn\.ncbi\.nlm\.nih\.gov/pmc/blobs/[^"\s]+\.(?:jpg|png|gif)', html))}
    for i, f in enumerate(re.findall(r'<fig\b.*?</fig>', xml, re.S), 1):
        g = re.search(r'xlink:href="([^"]+)"', f)
        if not g:
            continue
        name = g.group(1).rsplit('/', 1)[-1]
        url = blobs.get(name) or next((u for k, u in blobs.items() if k.split('.')[0] == name.split('.')[0]), None)
        if not url:
            continue
        local = d / url.rsplit('/', 1)[1]
        if not local.exists():
            try:
                local.write_bytes(get(url)); time.sleep(0.4)
            except Exception as e:
                print(' img fail', url, e); continue
        lab = re.search(r'<label>(.*?)</label>', f, re.S); cap = re.search(r'<caption>(.*?)</caption>', f, re.S)
        pool.append(dict(id=f'oa_{pmc}_{i}', src=str(local).replace('\\', '/'), kind='pmc_open_access', pmcid=pmc, doi='',
                         article=v.get('title', ''), label=re.sub(r'<[^>]+>', '', lab.group(1)) if lab else f'Figure {i}',
                         caption=re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', cap.group(1))).strip()[:500] if cap else '',
                         visual='', topic='cited', label_ko='', license={'cc by': 'CC BY 4.0', 'cc0': 'CC0', 'cc by-sa': 'CC BY-SA 4.0'}[v['license'].lower()],
                         usable=True, source_url=f'https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/', cited_by=pm_pages.get(pmid, [])))
    print('cited paper', pmc, 'figs so far', sum(1 for p in pool if p['pmcid'] == pmc))

# 4) 저작자 정보: PMC → Europe PMC, Wikimedia → Commons API
pmcs = sorted({p['pmcid'] for p in pool if p['pmcid']})
meta = {}
for i in range(0, len(pmcs), 40):
    q = ' OR '.join(f'PMCID:{x}' for x in pmcs[i:i + 40])
    d = json.loads(get('https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&pageSize=100&query=' + urllib.parse.quote(q), 60))
    for r in d['resultList']['result']:
        meta[r.get('pmcid')] = dict(authors=r.get('authorString', ''), journal=(r.get('journalInfo', {}).get('journal', {}) or {}).get('isoabbreviation') or r.get('journalTitle', ''),
                                    year=r.get('pubYear', ''), title=r.get('title', ''), doi=r.get('doi', ''), eplicense=r.get('license', ''))
for p in pool:
    if p['pmcid'] and p['pmcid'] in meta:
        m = meta[p['pmcid']]
        a = [x.strip() for x in m['authors'].rstrip('.').split(',') if x.strip()]
        p['credit'] = f"{a[0] + (' 외' if len(a) > 1 else '') if a else ''}. {m['title'].rstrip('.')}. {m['journal']} {m['year']}".strip('. ')
        p['doi'] = p['doi'] or m['doi']
        # Europe PMC 라이선스로 재확인 (manifest와 다르면 보수적으로)
        el = (m.get('eplicense') or '').lower()
        if el and 'nc' in el and p['usable']:
            p['usable'] = False; p['license'] = el.upper()
titles = [p['source_url'].split('/wiki/')[1] for p in pool if p['kind'] == 'wikimedia_commons' and '/wiki/' in p['source_url']]
wmeta = {}
for i in range(0, len(titles), 40):
    q = '|'.join(urllib.parse.unquote(t) for t in titles[i:i + 40])
    d = json.loads(get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(dict(action='query', titles=q, prop='imageinfo', iiprop='extmetadata', format='json')), 60))
    for pg in d['query']['pages'].values():
        em = (pg.get('imageinfo') or [{}])[0].get('extmetadata', {})
        wmeta[pg['title'].replace(' ', '_')] = dict(artist=re.sub(r'<[^>]+>', '', em.get('Artist', {}).get('value', ''))[:120], lic=em.get('LicenseShortName', {}).get('value', ''))
for p in pool:
    if p['kind'] == 'wikimedia_commons' and '/wiki/' in p['source_url']:
        t = urllib.parse.unquote(p['source_url'].split('/wiki/')[1]).replace(' ', '_')
        w = wmeta.get(t, {})
        artist = (w.get('artist') or p.get('author') or '').strip()
        p['credit'] = f"{artist or 'Wikimedia Commons'}, Wikimedia Commons"
        if w.get('lic'):
            ls = lic_short(w['lic']) if lic_short(w['lic']) != 'UNKNOWN' else w['lic']
            p['license'] = ls; p['usable'] = usable(ls) or ls in ('Public domain', 'CC0', 'No known copyright restrictions')

# 5) 썸네일
ok = 0
for p in pool:
    if not os.path.exists(p['src']):
        p['usable'] = False; p['missing'] = True; continue
    th = OUT / 'thumbs' / (p['id'] + '.jpg')
    if not th.exists():
        try:
            im = Image.open(p['src']).convert('RGB'); p['w'], p['h'] = im.size; im.thumbnail((520, 520)); im.save(th, quality=80)
        except Exception as e:
            p['usable'] = False; p['broken'] = str(e); continue
    else:
        im = Image.open(p['src']); p['w'], p['h'] = im.size
    p['thumb'] = str(th).replace('\\', '/'); ok += 1
json.dump(pool, open(OUT / 'pool.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import collections
print('pool', len(pool), 'thumbs', ok, 'usable', sum(p['usable'] for p in pool))
print(collections.Counter((p['topic'], p['usable']) for p in pool).most_common())
print(collections.Counter(p['license'] for p in pool if p['usable']).most_common())
