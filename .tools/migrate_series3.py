"""Series 3 (B형·C형) 6개 article 구조 통일 + References 추가."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# slug → (crumb series link slug, crumb series display, last crumb name)
S3 = {
    "B형간염-평생약": ("B형간염", "B형 간염", "약 평생 복용"),
    "B형간염-검사결과": ("B형간염", "B형 간염", "검사결과 해석"),
    "B형간염-결혼-임신": ("B형간염", "B형 간염", "결혼·임신·수유"),
    "가족-B형간염-검사": ("B형간염", "B형 간염", "가족 검사"),
    "B형간염-간암검진": ("간암", "간암", "B형 환자 간암 검진"),
    "C형간염-완치-DAA": ("B형간염", "B형 간염", "C형 DAA 완치"),
}

NEW_FOOTER = '''<footer class="site-footer">
  <div class="inner">
    <div class="col">
      <strong>Hepatology Note</strong>
      <p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p>
    </div>
    <div class="col">
      <strong>안내</strong>
      <a href="/소개/">소개</a>
      <a href="/논문/">논문</a>
      <a href="/updates/">Updates</a>
    </div>
    <div class="col">
      <strong>외부 링크</strong>
      <a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a>
    </div>
    <div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div>
  </div>
</footer>'''

NEW_AUTHOR_BOX = '''<aside class="author-box">
<img class="author-photo" src="/assets/img/author/drshin.jpg" alt="" loading="lazy">
<div class="author-info">
<p><strong>서울대학교병원 소화기내과 · 간암센터</strong></p>
<p class="muted">간암·간경변·만성 간질환 진료. 대한간학회 정회원.</p>
<p><a href="/소개/" class="more">소개 보기 →</a></p>
</div>
</aside>'''

# References from add_references.py
REFS = {
    "B형간염-평생약": [
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. Update on prevention, diagnosis, and treatment of chronic hepatitis B: AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329"),
        ("European Association for the Study of the Liver. EASL 2017 Clinical Practice Guidelines on the management of hepatitis B virus infection. <em>J Hepatol</em>. 2017;67(2):370–398.", "10.1016/j.jhep.2017.03.021", None),
        ("Buti M, Riveiro-Barciela M, Esteban R. Long-term safety and efficacy of nucleos(t)ide analogue therapy in hepatitis B. <em>Liver Int</em>. 2018;38 Suppl 1:84–89.", "10.1111/liv.13641", "29427498"),
    ],
    "B형간염-검사결과": [
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329"),
        ("European Association for the Study of the Liver. EASL 2017 Clinical Practice Guidelines on the management of hepatitis B. <em>J Hepatol</em>. 2017;67(2):370–398.", "10.1016/j.jhep.2017.03.021", None),
        ("Liaw YF, Chu CM. Hepatitis B virus infection. <em>Lancet</em>. 2009;373(9663):582–592.", "10.1016/S0140-6736(09)60207-5", "19217993"),
    ],
    "B형간염-결혼-임신": [
        ("Pan CQ, Duan Z, Dai E, et al. Tenofovir to Prevent Hepatitis B Transmission in Mothers with High Viral Load. <em>N Engl J Med</em>. 2016;374(24):2324–2334.", "10.1056/NEJMoa1508660", "27305192"),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None),
        ("Brown RS Jr, McMahon BJ, Lok AS, et al. Antiviral therapy in chronic hepatitis B viral infection during pregnancy: A systematic review and meta-analysis. <em>Hepatology</em>. 2016;63(1):319–333.", "10.1002/hep.28302", "26565396"),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329"),
    ],
    "가족-B형간염-검사": [
        ("Schillie S, Vellozzi C, Reingold A, et al. Prevention of Hepatitis B Virus Infection in the United States: Recommendations of the Advisory Committee on Immunization Practices. <em>MMWR Recomm Rep</em>. 2018;67(1):1–31.", "10.15585/mmwr.rr6701a1", "29939980"),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329"),
    ],
    "C형간염-완치-DAA": [
        ("AASLD-IDSA HCV Guidance Panel. Hepatitis C Guidance 2018 Update: AASLD-IDSA Recommendations for Testing, Managing, and Treating Hepatitis C Virus Infection. <em>Clin Infect Dis</em>. 2018;67(10):1477–1492.", "10.1093/cid/ciy585", "30215672"),
        ("Korean Association for the Study of the Liver (KASL). 2020 KASL clinical practice guidelines for management of hepatitis C. <em>Clin Mol Hepatol</em>. 2020;26(2):83–127.", "10.3350/cmh.2020.0010", None),
        ("Zeuzem S, Foster GR, Wang S, et al. Glecaprevir-Pibrentasvir for 8 or 12 Weeks in HCV Genotype 1 or 3 Infection. <em>N Engl J Med</em>. 2018;378(4):354–369.", "10.1056/NEJMoa1702417", "29365309"),
        ("Falade-Nwulia O, Suarez-Cuervo C, Nelson DR, et al. Oral Direct-Acting Agent Therapy for Hepatitis C Virus Infection: A Systematic Review. <em>Ann Intern Med</em>. 2017;166(9):637–648.", "10.7326/M16-2575", "28319996"),
    ],
    "B형간염-간암검진": [
        ("Korean Liver Cancer Association (KLCA), National Cancer Center (NCC). 2022 KLCA-NCC Korea Practice Guidelines for the Management of Hepatocellular Carcinoma. <em>J Liver Cancer</em>. 2023;23(1):1–120.", "10.17998/jlc.2022.11.07", None),
        ("Singal AG, Llovet JM, Yarchoan M, et al. AASLD Practice Guidance on prevention, diagnosis, and treatment of hepatocellular carcinoma. <em>Hepatology</em>. 2023;78(6):1922–1965.", "10.1097/HEP.0000000000000466", "37199193"),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None),
        ("Park JW, Chen M, Colombo M, et al. Global patterns of hepatocellular carcinoma management from diagnosis to death: the BRIDGE Study. <em>Liver Int</em>. 2015;35(9):2155–2166.", "10.1111/liv.12818", "25752327"),
    ],
}

def render_refs(refs):
    out = ['<section class="references-block">', '<h2>References</h2>', '<ol class="references">']
    for text, doi, pmid in refs:
        line = f'<li>{text}'
        links = []
        if doi:
            links.append(f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener">DOI</a>')
        if pmid:
            links.append(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" rel="noopener">PMID {pmid}</a>')
        if links:
            line += ' ' + ' · '.join(links)
        line += '</li>'
        out.append(line)
    out.append('</ol>')
    out.append('</section>')
    return "\n".join(out)

for slug, (series_slug, series_display, last_name) in S3.items():
    p = ROOT / slug / "index.html"
    if not p.exists():
        print(f"  SKIP: {slug}")
        continue
    h = p.read_text(encoding="utf-8")

    # 1) main class
    h = h.replace('<main class="article-wrap">', '<main class="wrap">')

    # 2) crumb: replace
    h = re.sub(
        r'<nav class="crumb"><a href="/">[^<]*</a> › [^<]*</nav>',
        f'<nav class="crumb"><a href="/">홈</a> › <a href="/{series_slug}/">{series_display}</a> › <span>{last_name}</span></nav>',
        h, count=1
    )

    # 3) Remove series-label (will be redundant with crumb)
    h = re.sub(r'<span class="series-label">[^<]*</span>\s*', '', h, count=1)

    # 4) meta byline: "신현재 · 서울대학교병원 소화기내과 · YYYY.MM.DD"
    h = re.sub(
        r'<p class="meta">신현재 · 서울대학교병원 소화기내과\s*· (\d{4})\.(\d{2})\.(\d{2})</p>',
        lambda m: f'<p class="meta">서울대학교병원 소화기내과 · 작성 {m.group(1)}-{m.group(2)}-{m.group(3)} · 검토 {m.group(1)}-{m.group(2)}-{m.group(3)}</p>',
        h
    )

    # 5) Wrap FAQ — find <h2>자주 묻는 질문</h2> followed by details, wrap until disclaimer
    # Easier approach: find "<h2>자주 묻는 질문</h2>" and inject `<section class="faq" id="faq">` before, close before disclaimer
    if '<h2>자주 묻는 질문</h2>' in h and '<section class="faq"' not in h:
        # Inject section open before h2
        h = h.replace(
            '<h2>자주 묻는 질문</h2>',
            '<section class="faq" id="faq">\n  <h2>자주 묻는 질문</h2>',
            1
        )
        # Inject section close before disclaimer (first <p class="disclaimer">)
        h = h.replace(
            '<p class="disclaimer">',
            '</section>\n\n<p class="disclaimer">',
            1
        )

    # 6) Replace related: <nav class="related"> ... </nav> → <aside class="related"> ... </aside> with ul without hub-list class
    h = re.sub(
        r'<nav class="related">\s*<h2>[^<]*</h2>\s*<ul class="hub-list">',
        '<aside class="related">\n<h2>같이 읽으면 좋은 글</h2>\n<ul>',
        h, count=1
    )
    # Close nav.related → close aside (find the last </nav> before </main>)
    h = h.replace('</ul>\n  </nav>\n</main>', '</ul>\n</aside>\n</main>', 1)
    h = h.replace('</ul>\n</nav>\n</main>', '</ul>\n</aside>\n</main>', 1)

    # Convert hub-list <li><a><h3>X</h3><p>Y</p></a></li> to simpler <li><a>X</a></li> (since aside.related uses simpler list)
    # Actually the new related style works with <li><a>X</a></li>. Let me convert:
    def convert_related_item(match):
        # extract h3 and href
        href = re.search(r'href="([^"]+)"', match.group(0))
        h3 = re.search(r'<h3>([^<]+)</h3>', match.group(0))
        if href and h3:
            return f'<li><a href="{href.group(1)}">{h3.group(1)}</a></li>'
        return match.group(0)

    h = re.sub(
        r'<li><a href="[^"]+"><h3>[^<]+</h3>\s*<p>[^<]*</p>\s*</a></li>',
        convert_related_item,
        h
    )

    # 7) Insert References + author-box before disclaimer
    if 'references-block' not in h:
        refs_html = render_refs(REFS[slug])
        h = h.replace(
            '<p class="disclaimer">',
            f'{refs_html}\n\n{NEW_AUTHOR_BOX}\n\n<p class="disclaimer">',
            1
        )

    # 8) Replace old footer (with 신현재 name in copyright) with new site-footer
    h = re.sub(
        r'<footer[^>]*>\s*<p>© 2026 간 건강 가이드 · 신현재 · 서울대학교병원 소화기내과</p>\s*</footer>',
        NEW_FOOTER,
        h
    )

    # 9) JSON-LD: Person jobTitle and BreadcrumbList — make sure consistent
    h = re.sub(
        r'"jobTitle":"서울대학교병원 소화기내과 ?"',
        '"jobTitle":"서울대학교병원 소화기내과 · 간암센터"',
        h
    )
    # Add image to Person if missing
    if '"@id":"https://drshin.kr/#author"' in h and 'image":"https://drshin.kr/assets/img/author/drshin.jpg"' not in h:
        h = re.sub(
            r'(\{"@type":"Person","@id":"https://drshin.kr/#author","name":"신현재"[^\}]*?)"url":"https://www.snuh.org',
            r'\1"image":"https://drshin.kr/assets/img/author/drshin.jpg","url":"https://www.snuh.org',
            h
        )

    # 10) <article> wrapper — Series 3 doesn't have it. Wrap content
    # Actually skip — body works without <article>

    # 11) Title cleanup — remove " | 신현재" suffix if present
    h = re.sub(r'(<title>[^<]*?) \| 신현재</title>', r'\1 — Hepatology Note</title>', h)

    p.write_text(h, encoding="utf-8")
    print(f"  rebuilt: {slug}")

print("\nDone.")
