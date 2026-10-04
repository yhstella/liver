"""논문·오픈 라이선스 그림을 페이지에 넣는다. idempotent (paper-figure:auto 블록을 지우고 다시 넣음)."""
import glob, html, io, json, os, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
SCR = ROOT / 'private-figures/figpool'
DEST = Path('assets/img/figures'); DEST.mkdir(parents=True, exist_ok=True)
pool = {p['id']: p for p in json.load(open(SCR / 'pool.json', encoding='utf-8'))}
LIC_URL = {
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/', 'CC BY 3.0': 'https://creativecommons.org/licenses/by/3.0/',
    'CC BY 2.5': 'https://creativecommons.org/licenses/by/2.5/', 'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/',
    'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/', 'CC BY-SA 3.0': 'https://creativecommons.org/licenses/by-sa/3.0/',
    'CC BY-SA 2.5': 'https://creativecommons.org/licenses/by-sa/2.5/', 'CC BY-SA 2.0': 'https://creativecommons.org/licenses/by-sa/2.0/',
    'CC0': 'https://creativecommons.org/publicdomain/zero/1.0/',
    'CC BY-NC 4.0': 'https://creativecommons.org/licenses/by-nc/4.0/', 'CC BY-NC 3.0': 'https://creativecommons.org/licenses/by-nc/3.0/',
    'CC BY-NC-ND 4.0': 'https://creativecommons.org/licenses/by-nc-nd/4.0/',
    'CC BY-NC-SA 4.0': 'https://creativecommons.org/licenses/by-nc-sa/4.0/', 'CC BY-NC-SA 3.0': 'https://creativecommons.org/licenses/by-nc-sa/3.0/',
}
BLOCK_RE = re.compile(r'(?:\r?\n)?<!-- paper-figure:auto:start [^>]*-->.*?<!-- paper-figure:auto:end -->', re.S)
E = lambda s: html.escape(s or '', quote=True)

assign = []
for f in sorted(glob.glob(str(SCR / 'assign_*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for a in d.get('assignments', []):
        a['_src'] = Path(f).stem
        assign.append(a)
print('assignments loaded:', len(assign))
EXCLUDE = {'pwf_00001': '예전 BCLC 모식도(현재 기준과 다름)', 'pwf_00039': '중국어 라벨·오타', 'pwf_00125': 'CT에 병원명 표시',
           'oa_PMC5754852_2': '영국 기준 수치가 본문과 다름',
           'pwf_00135': '그림 안 오타(ACLP), ND라 고칠 수 없음', 'pwf_00128': '그림 안 오타 3곳', 'pwf_00124': '그림 안 오타(Propanolol)',
           'pwf_00170': '그림 안 오타(phophatase)', 'pwf_00153': 'EASL 2009 그림을 다시 그린 것으로 보임(제3자)'}
EXCLUDE_PAIR = {('케이스/건강검진-우연발견-1cm결절', 'pwf_00011'), ('ALP-GGT-담도-간세포', 'oa_PMC5754852_1'), ('빌리루빈-직접-간접', 'oa_PMC5754852_1'),
                ('CC/간섬유화-진단', 'pwf_00193')}
CROP = {'pwf_00151': 14, 'pwf_00152': 14, 'pwf_00154': 14}   # 위쪽 뷰어 툴바 제거(px)
before = len(assign)
assign = [a for a in assign if a['figure_id'] not in EXCLUDE and (a['page'].strip('/'), a['figure_id']) not in EXCLUDE_PAIR]
print('after review exclusions:', len(assign), '(removed', before - len(assign), ')')

# 검증: 그림 사용 가능 여부, 페이지 존재, 설명 규칙
problems, use_count, by_page = [], {}, {}
for a in assign:
    fid, page = a['figure_id'], a['page'].strip('/')
    f = pool.get(fid)
    if not f or not f.get('usable'):
        problems.append(('unusable', fid, page)); continue
    if not os.path.exists(f'{page}/index.html'):
        problems.append(('no page', fid, page)); continue
    cap = a.get('caption_ko', '')
    if '—' in cap or re.search(r'그림에서 보듯|위 그림|이 그림은', cap) or not cap:
        problems.append(('caption rule', fid, page, cap)); continue
    by_page.setdefault(page, [])
    if any(x['figure_id'] == fid for x in by_page[page]):
        continue
    use_count[fid] = use_count.get(fid, 0) + 1
    if use_count[fid] > 3:
        problems.append(('overused', fid, page)); continue
    by_page[page].append(a)
print('pages to update:', len(by_page), '| problems:', len(problems))
for p in problems[:30]:
    print('  ', p)


def web_image(fid):
    f = pool[fid]
    out = DEST / f'{fid}.jpg'
    if not out.exists():
        im = Image.open(f['src']).convert('RGB')
        if fid in CROP and 'ND' not in (f.get('license') or '').upper():
            im = im.crop((0, CROP[fid], im.width, im.height))
        if im.width > 1400:
            im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
        im.save(out, quality=85, optimize=True)
    w, h = Image.open(out).size
    return f'/assets/img/figures/{fid}.jpg', w, h


def credit_html(f):
    lic = f['license']
    lic_html = f'<a href="{LIC_URL[lic]}" target="_blank" rel="noopener license">{E(lic)}</a>' if lic in LIC_URL else E(lic)
    src = f.get('source_url') or (f'https://doi.org/{f["doi"]}' if f.get('doi') else '')
    who = E(f.get('credit') or f.get('article') or 'Wikimedia Commons')
    who_html = f'<a href="{E(src)}" target="_blank" rel="noopener">{who}</a>' if src else who
    return f'출처: {who_html} · {lic_html}' + (' · 일부 잘라냄' if f['id'] in CROP else '')


def fig_block(a):
    f = pool[a['figure_id']]
    src, w, h = web_image(a['figure_id'])
    cls = 'paper-fig lit-fig tall' if h > 1.3 * w else 'paper-fig lit-fig'   # 세로로 긴 표는 높이 제한을 풀어 글자가 읽히게
    return (f'\n<!-- paper-figure:auto:start {a["figure_id"]} -->\n<figure class="{cls}">\n'
            f'  <img src="{src}" alt="{E(a.get("alt_ko"))}" loading="lazy" width="{w}" height="{h}">\n'
            f'  <figcaption>{E(a["caption_ko"])}<span class="fig-credit">{credit_html(f)}</span></figcaption>\n'
            f'</figure>\n<!-- paper-figure:auto:end -->')


def insert_after_para(s, start):
    """start 이후 첫 </p> 뒤(바로 뒤에 page-top-image figure가 있으면 그 뒤)에 넣을 위치."""
    m = re.compile(r'</p>').search(s, start)
    if not m:
        return None
    # 다음 소제목·참고문헌 전에 문단이 없으면(목록·표만 있는 절) 첫 목록/표 뒤에 둔다
    stops = [x for x in (s.find('<h2', start), s.find('references-block', start)) if x != -1]
    limit = min(stops) if stops else len(s)
    if m.start() > limit:
        depth = 0
        for t in re.finditer(r'<(/?)(ul|ol|table)\b[^>]*>', s[start:limit]):
            depth += -1 if t.group(1) else 1
            if depth == 0 and t.group(1):
                return start + t.end()
        return start
    if '<details' in s[start:m.end()]:
        # 첫 문단이 접힌 상자(details) 안이면 펼치기 전엔 안 보이므로 소제목 바로 아래에 둔다
        return start
    pos = m.end()
    # 문단이 상자(div) 안에 있으면 상자 밖으로 뺀다 (케이스 페이지의 case-intro 등)
    for _ in range(2):
        close = re.match(r'\s*</div>', s[pos:])
        if not close:
            break
        pos += close.end()
    nxt = re.match(r'\s*(<!-- page-image:auto:start -->.*?<!-- page-image:auto:end -->|<figure class="page-top-image".*?</figure>)', s[pos:], re.S)
    if nxt:
        pos += nxt.end()
    return pos


done, skipped = 0, []
for page, items in by_page.items():
    path = f'{page}/index.html'
    s = io.open(path, encoding='utf-8', newline='').read()
    s = BLOCK_RE.sub('', s)
    a0 = s.find('<article'); a0 = a0 if a0 >= 0 else s.find('<main')
    placed = 0
    for a in items:
        target = a.get('after_h2', '__intro__')
        start = None
        if target != '__intro__':
            for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', s[a0:], re.S):
                if re.sub(r'<[^>]+>', '', m.group(1)).strip() == target.strip():
                    start = a0 + m.end(); break
            if start is None:
                skipped.append((page, a['figure_id'], 'h2 not found: ' + target[:40]))
        if start is None:
            h1 = re.search(r'</h1>', s[a0:])
            start = a0 + (h1.end() if h1 else 0)
            # 날짜·태그 줄은 건너뛴다
            while True:
                m = re.match(r'\s*<p class="(publish-date|tag-row)[^"]*">.*?</p>', s[start:], re.S)
                if not m:
                    break
                start += m.end()
        pos = insert_after_para(s, start)
        if pos is None:
            skipped.append((page, a['figure_id'], 'no paragraph')); continue
        s = s[:pos] + fig_block(a) + s[pos:]
        placed += 1
    if placed and '/assets/js/figure-zoom.js' not in s:
        s = s.replace('</head>', '<script src="/assets/js/figure-zoom.js" defer></script>\n</head>', 1)
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    done += placed
print('figures placed:', done, 'on', len(by_page), 'pages')
for x in skipped:
    print('  skip', x)

css = io.open('style.css', encoding='utf-8', newline='').read()
if '.lit-fig' not in css:
    css += '''
.paper-fig.lit-fig{max-width:720px;margin:26px auto}
.paper-fig.lit-fig figcaption{display:block;margin:10px 2px 0;font-size:13.5px;line-height:1.65;color:var(--fg)}
.paper-fig.lit-fig .fig-credit{display:block;margin-top:4px;font-size:11.5px;line-height:1.5;color:var(--muted);word-break:break-all}
.paper-fig.lit-fig .fig-credit a{color:var(--muted)}
.paper-fig.lit-fig img{max-height:560px;object-fit:contain}
'''
if '.paper-fig.lit-fig img{width:auto' not in css:
    css += '.paper-fig.lit-fig img{width:auto;max-width:100%;max-height:520px;margin:0 auto}' + chr(10)
if '.paper-fig.lit-fig.tall img' not in css:
    css += '.paper-fig.lit-fig.tall img{max-height:none}' + chr(10)
io.open('style.css', 'w', encoding='utf-8', newline='').write(css)
json.dump({'placed': done, 'pages': sorted(by_page), 'problems': problems, 'skipped': skipped}, open(SCR / 'apply_report.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
