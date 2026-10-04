"""NC(비상업) 라이선스 그림 후보 추가: 사이트가 인용한 NC 논문 + 국내 가이드라인 + personal-web-figures NC."""
import json, os, re, time, urllib.request, urllib.parse, urllib.error
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SCR = ROOT / 'private-figures/figpool'
OUT = SCR
OA_DIR = Path('private-figures/paper-oa')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'}


def get(url, t=60):
    for k in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and k < 5:
                time.sleep(5 * (k + 1)); continue
            raise
        except Exception:
            if k < 5:
                time.sleep(5 * (k + 1)); continue
            raise


pool = json.load(open(OUT / 'pool.json', encoding='utf-8'))
have = {p['id'] for p in pool}
# 1) 기존 pool 의 NC 항목을 사용 가능으로 (제3자 재수록 표시는 제외)
THIRD = re.compile(r'permission|reproduced|reprinted|©|copyright|adapted from|modified from', re.I)
for p in pool:
    lic = (p.get('license') or '').upper()
    if not p['usable'] and 'NC' in lic and not p.get('excluded') and not p.get('missing') and not p.get('broken'):
        if not THIRD.search(p.get('caption') or ''):
            p['usable'] = True; p['nc'] = True

# 2) NC 논문 목록: 사이트 인용 NC 논문 + 국내 가이드라인
cited = json.load(open(SCR / 'cited_oa.json', encoding='utf-8'))
pm_pages = json.load(open(SCR / 'cited_pmids.json', encoding='utf-8'))
targets = {}
for pmid, v in cited.items():
    lic = (v.get('license') or '').lower()
    if v.get('pmcid') and 'nc' in lic:
        targets[v['pmcid']] = dict(pmid=pmid, license=lic, cited_by=[c.replace(chr(92), '/') for c in pm_pages.get(pmid, [])], title=v.get('title', ''))
# 국내 가이드라인(사이트 인용 여부와 무관하게 후보로)
GUIDE = {'PMC9597235': 'KLCA-NCC 2022 HCC', 'PMC13430407': 'KASL-EALA 2026 CHB'}
for pmc in GUIDE:
    targets.setdefault(pmc, dict(pmid='', license='cc by-nc', cited_by=[], title=GUIDE[pmc]))
print('NC papers to fetch:', len(targets))

new = []
for pmc, v in targets.items():
    d = OA_DIR / pmc; d.mkdir(parents=True, exist_ok=True)
    try:
        html = get(f'https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/').decode('utf-8', 'replace')
        xml = get(f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmc}/fullTextXML', 90).decode('utf-8', 'replace')
    except Exception as e:
        print('skip', pmc, e); continue
    lic_m = re.search(r'<license[^>]*>(.*?)</license>', xml, re.S)
    lic_txt = re.sub(r'<[^>]+>', ' ', lic_m.group(1)) if lic_m else v['license']
    lic_url = re.search(r'creativecommons\.org/licenses/([a-z\-]+)/(\d\.\d)', (lic_m.group(0) if lic_m else '') + lic_txt)
    lic_short = f'CC {lic_url.group(1).upper()} {lic_url.group(2)}' if lic_url else v['license'].upper()
    if 'NC' not in lic_short.upper():
        continue
    blobs = {u.rsplit('/', 1)[1]: u for u in set(re.findall(r'https://cdn\.ncbi\.nlm\.nih\.gov/pmc/blobs/[^"\s]+\.(?:jpg|png|gif)', html))}
    n = 0
    for i, f in enumerate(re.findall(r'<fig\b.*?</fig>', xml, re.S), 1):
        fid = f'oa_{pmc}_{i}'
        if fid in have:
            continue
        g = re.search(r'xlink:href="([^"]+)"', f)
        if not g:
            continue
        name = g.group(1).rsplit('/', 1)[-1]
        url = blobs.get(name) or next((u for k, u in blobs.items() if k.split('.')[0] == name.split('.')[0]), None)
        if not url:
            continue
        cap = re.search(r'<caption>(.*?)</caption>', f, re.S); lab = re.search(r'<label>(.*?)</label>', f, re.S)
        cap_t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', cap.group(1))).strip() if cap else ''
        # 그림 자체의 저작권 고지(다른 출처 재수록)는 제외
        if THIRD.search(cap_t) or re.search(r'<permissions>|<copyright', f):
            continue
        local = d / url.rsplit('/', 1)[1]
        if not local.exists():
            try:
                local.write_bytes(get(url)); time.sleep(0.4)
            except Exception as e:
                print(' img fail', url, e); continue
        new.append(dict(id=fid, src=str(local).replace(chr(92), '/'), kind='pmc_open_access', pmcid=pmc, doi='', article=v['title'],
                        label=re.sub(r'<[^>]+>', '', lab.group(1)) if lab else f'Figure {i}', caption=cap_t[:600], visual='',
                        topic='cited_nc' if v['cited_by'] else 'guideline_nc', label_ko='', license=lic_short, usable=True, nc=True,
                        source_url=f'https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/', cited_by=v['cited_by']))
        n += 1
    print(pmc, lic_short, 'new figs', n, '|', v['title'][:60])

# 3) 저작자 정보
pmcs = sorted({p['pmcid'] for p in new})
meta = {}
for i in range(0, len(pmcs), 40):
    q = ' OR '.join(f'PMCID:{x}' for x in pmcs[i:i + 40])
    d = json.loads(get('https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=core&pageSize=100&query=' + urllib.parse.quote(q)))
    for r in d['resultList']['result']:
        meta[r.get('pmcid')] = r
for p in new:
    r = meta.get(p['pmcid'], {})
    a = [x.strip() for x in (r.get('authorString') or '').rstrip('.').split(',') if x.strip()]
    j = ((r.get('journalInfo') or {}).get('journal') or {}).get('isoabbreviation') or r.get('journalTitle', '')
    p['credit'] = f"{a[0] + (' 외' if len(a) > 1 else '') if a else ''}. {(r.get('title') or p['article']).rstrip('.')}. {j} {r.get('pubYear', '')}".strip('. ')
    p['doi'] = r.get('doi', '')
    th = OUT / 'thumbs' / (p['id'] + '.jpg')
    try:
        im = Image.open(p['src']).convert('RGB'); p['w'], p['h'] = im.size; im.thumbnail((520, 520)); im.save(th, quality=80); p['thumb'] = str(th).replace(chr(92), '/')
    except Exception as e:
        p['usable'] = False; p['broken'] = str(e)
pool += new
json.dump(pool, open(OUT / 'pool.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('new NC figs:', len(new), '| total NC usable:', sum(1 for p in pool if p.get('nc') and p['usable']))
