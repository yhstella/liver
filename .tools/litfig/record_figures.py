"""페이지에 실제로 들어간 paper-figure:auto 블록을 훑어 .tools/lit_figures.json 을 다시 만든다."""
import json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SCR = ROOT / 'private-figures/figpool'
pool = {p['id']: p for p in json.load(open(SCR / 'pool.json', encoding='utf-8'))}
SKIP = {'.git', 'private-figures', '.tools', 'assets', 'node_modules'}
figs = {}
for f in sorted(Path('.').rglob('index.html')):
    if any(x in SKIP for x in f.parts):
        continue
    page = '/'.join(f.parts[:-1])
    for fid in re.findall(r'<!-- paper-figure:auto:start ([^ ]+) -->', f.read_text(encoding='utf-8')):
        p = pool[fid]
        e = figs.setdefault(fid, dict(file=f'assets/img/figures/{fid}.jpg', license=p.get('license'), credit=p.get('credit'),
                                      source_url=p.get('source_url'), doi=p.get('doi', ''), pmcid=p.get('pmcid', ''),
                                      original_caption=p.get('caption', ''), pages=[]))
        e['pages'].append(page)
note = ('논문·오픈 라이선스 그림 사용 기록. 원본은 private-figures/(gitignore). 제3자 재수록 그림은 쓰지 않음. '
        'NC(비상업) 라이선스는 광고 없는 비상업 사이트라 사용(2026-09-28 저자 승인). ND 그림은 자르거나 고치지 않음(크기 축소만).')
json.dump(dict(note=note, figures=figs), open('.tools/lit_figures.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('figures', len(figs), 'placements', sum(len(v['pages']) for v in figs.values()))
