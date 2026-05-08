"""Add References section to all existing 17 articles, before author-box."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# References per article: (text, doi-or-None, pmid-or-None, extra-link-or-None)
REFS = {
    "간수치-높음": [
        ("Kwo PY, Cohen SM, Lim JK. ACG Clinical Guideline: Evaluation of Abnormal Liver Chemistries. <em>Am J Gastroenterol</em>. 2017;112(1):18–35.", "10.1038/ajg.2016.517", "27995906", None),
        ("Newsome PN, Cramb R, Davison SM, et al. Guidelines on the management of abnormal liver blood tests. <em>Gut</em>. 2018;67(1):6–19.", "10.1136/gutjnl-2017-314924", "29122851", None),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines: management of nonalcoholic fatty liver disease. <em>Clin Mol Hepatol</em>. 2021;27(3):363–401.", "10.3350/cmh.2021.0178", "34159786", None),
        ("European Association for the Study of the Liver, et al. EASL-EASD-EASO Clinical Practice Guidelines on the management of metabolic dysfunction-associated steatotic liver disease (MASLD). <em>J Hepatol</em>. 2024;81(3):492–542.", "10.1016/j.jhep.2024.04.031", None, None),
    ],
    "간수치-종류-차이": [
        ("Kwo PY, Cohen SM, Lim JK. ACG Clinical Guideline: Evaluation of Abnormal Liver Chemistries. <em>Am J Gastroenterol</em>. 2017;112(1):18–35.", "10.1038/ajg.2016.517", "27995906", None),
        ("Botros M, Sikaris KA. The De Ritis ratio: the test of time. <em>Clin Biochem Rev</em>. 2013;34(3):117–130.", None, "24353357", None),
        ("Newsome PN, Cramb R, Davison SM, et al. Guidelines on the management of abnormal liver blood tests. <em>Gut</em>. 2018;67(1):6–19.", "10.1136/gutjnl-2017-314924", "29122851", None),
        ("Lala V, Zubair M, Minter DA. Liver Function Tests. StatPearls. 2024. Treasure Island (FL): StatPearls Publishing.", None, "29494096", None),
    ],
    "지방간-정밀검사": [
        ("Sterling RK, Lissen E, Clumeck N, et al. Development of a simple noninvasive index to predict significant fibrosis in patients with HIV/HCV coinfection. <em>Hepatology</em>. 2006;43(6):1317–1325.", "10.1002/hep.21178", "16729309", None),
        ("European Association for the Study of the Liver, et al. EASL-EASD-EASO Clinical Practice Guidelines on the management of MASLD. <em>J Hepatol</em>. 2024;81(3):492–542.", "10.1016/j.jhep.2024.04.031", None, None),
        ("Castera L, Friedrich-Rust M, Loomba R. Noninvasive Assessment of Liver Disease in Patients With Nonalcoholic Fatty Liver Disease. <em>Gastroenterology</em>. 2019;156(5):1264–1281.e4.", "10.1053/j.gastro.2018.12.036", "30660725", None),
        ("Rinella ME, Neuschwander-Tetri BA, Siddiqui MS, et al. AASLD Practice Guidance on the clinical assessment and management of nonalcoholic fatty liver disease. <em>Hepatology</em>. 2023;77(5):1797–1835.", "10.1097/HEP.0000000000000323", "36727674", None),
    ],
    "알파태아단백": [
        ("Korean Liver Cancer Association (KLCA), National Cancer Center (NCC). 2022 KLCA-NCC Korea Practice Guidelines for the Management of Hepatocellular Carcinoma. <em>J Liver Cancer</em>. 2023;23(1):1–120.", "10.17998/jlc.2022.11.07", None, None),
        ("Singal AG, Llovet JM, Yarchoan M, et al. AASLD Practice Guidance on prevention, diagnosis, and treatment of hepatocellular carcinoma. <em>Hepatology</em>. 2023;78(6):1922–1965.", "10.1097/HEP.0000000000000466", "37199193", None),
        ("European Association for the Study of the Liver. EASL Clinical Practice Guidelines: Management of hepatocellular carcinoma. <em>J Hepatol</em>. 2018;69(1):182–236.", "10.1016/j.jhep.2018.03.019", None, None),
        ("Marrero JA, Feng Z, Wang Y, et al. Alpha-fetoprotein, des-gamma carboxyprothrombin, and lectin-bound alpha-fetoprotein in early hepatocellular carcinoma. <em>Gastroenterology</em>. 2009;137(1):110–118.", "10.1053/j.gastro.2009.04.005", "19362088", None),
    ],
    "간섬유화스캔-수치": [
        ("Castera L, Forns X, Alberti A. Non-invasive evaluation of liver fibrosis using transient elastography. <em>J Hepatol</em>. 2008;48(5):835–847.", "10.1016/j.jhep.2008.02.008", "18334275", None),
        ("Boursier J, Zarski JP, de Ledinghen V, et al. Determination of reliability criteria for liver stiffness evaluation by transient elastography. <em>Hepatology</em>. 2013;57(3):1182–1191.", "10.1002/hep.25993", "22899556", None),
        ("European Association for the Study of the Liver, et al. EASL-EASD-EASO Clinical Practice Guidelines on the management of MASLD. <em>J Hepatol</em>. 2024;81(3):492–542.", "10.1016/j.jhep.2024.04.031", None, None),
        ("Eddowes PJ, Sasso M, Allison M, et al. Accuracy of FibroScan Controlled Attenuation Parameter and Liver Stiffness Measurement in Assessing Steatosis and Fibrosis in Patients With Nonalcoholic Fatty Liver Disease. <em>Gastroenterology</em>. 2019;156(6):1717–1730.", "10.1053/j.gastro.2019.01.042", "30689971", None),
    ],
    "대사이상지방간-MASLD": [
        ("Rinella ME, Lazarus JV, Ratziu V, et al. A multisociety Delphi consensus statement on new fatty liver disease nomenclature. <em>J Hepatol</em>. 2023;79(6):1542–1556.", "10.1016/j.jhep.2023.06.003", "37364790", None),
        ("Rinella ME, Neuschwander-Tetri BA, Siddiqui MS, et al. AASLD Practice Guidance on the clinical assessment and management of nonalcoholic fatty liver disease. <em>Hepatology</em>. 2023;77(5):1797–1835.", "10.1097/HEP.0000000000000323", "36727674", None),
        ("European Association for the Study of the Liver, et al. EASL-EASD-EASO Clinical Practice Guidelines on the management of MASLD. <em>J Hepatol</em>. 2024;81(3):492–542.", "10.1016/j.jhep.2024.04.031", None, None),
    ],
    "술-안마셔도-지방간": [
        ("Friedman SL, Neuschwander-Tetri BA, Rinella M, Sanyal AJ. Mechanisms of NAFLD development and therapeutic strategies. <em>Nat Med</em>. 2018;24(7):908–922.", "10.1038/s41591-018-0104-9", "29967350", None),
        ("Younossi ZM, Koenig AB, Abdelatif D, et al. Global epidemiology of nonalcoholic fatty liver disease — Meta-analytic assessment of prevalence, incidence, and outcomes. <em>Hepatology</em>. 2016;64(1):73–84.", "10.1002/hep.28431", "26707365", None),
        ("Rinella ME, Lazarus JV, Ratziu V, et al. A multisociety Delphi consensus statement on new fatty liver disease nomenclature. <em>J Hepatol</em>. 2023;79(6):1542–1556.", "10.1016/j.jhep.2023.06.003", "37364790", None),
        ("Eslam M, El-Serag HB, Francque S, et al. Metabolic (dysfunction)-associated fatty liver disease in individuals of normal weight. <em>Nat Rev Gastroenterol Hepatol</em>. 2022;19(10):638–651.", "10.1038/s41575-022-00635-5", "35710982", None),
    ],
    "지방간-치료": [
        ("Vilar-Gomez E, Martinez-Perez Y, Calzadilla-Bertot L, et al. Weight Loss Through Lifestyle Modification Significantly Reduces Features of Nonalcoholic Steatohepatitis. <em>Gastroenterology</em>. 2015;149(2):367–378.", "10.1053/j.gastro.2015.04.005", "25865049", None),
        ("Harrison SA, Bedossa P, Guy CD, et al. A Phase 3, Randomized, Controlled Trial of Resmetirom in NASH with Liver Fibrosis. <em>N Engl J Med</em>. 2024;390(6):497–509.", "10.1056/NEJMoa2309000", "38324483", None),
        ("Rinella ME, Neuschwander-Tetri BA, Siddiqui MS, et al. AASLD Practice Guidance on the clinical assessment and management of NAFLD. <em>Hepatology</em>. 2023;77(5):1797–1835.", "10.1097/HEP.0000000000000323", "36727674", None),
        ("Newsome PN, Buchholtz K, Cusi K, et al. A Placebo-Controlled Trial of Subcutaneous Semaglutide in Nonalcoholic Steatohepatitis. <em>N Engl J Med</em>. 2021;384(12):1113–1124.", "10.1056/NEJMoa2028395", "33185364", None),
    ],
    "지방간-음식": [
        ("Romero-Gómez M, Zelber-Sagi S, Trenell M. Treatment of NAFLD with diet, physical activity and exercise. <em>J Hepatol</em>. 2017;67(4):829–846.", "10.1016/j.jhep.2017.05.016", "28545937", None),
        ("Bischoff SC, Bernal W, Dasarathy S, et al. ESPEN practical guideline: Clinical nutrition in liver disease. <em>Clin Nutr</em>. 2020;39(12):3533–3562.", "10.1016/j.clnu.2020.09.001", "33213977", None),
        ("Wijarnpreecha K, Thongprayoon C, Ungprasert P. Coffee consumption and risk of nonalcoholic fatty liver disease: a systematic review and meta-analysis. <em>Eur J Gastroenterol Hepatol</em>. 2017;29(2):e8–e12.", "10.1097/MEG.0000000000000776", "27824658", None),
        ("European Association for the Study of the Liver, et al. EASL-EASD-EASO Clinical Practice Guidelines on the management of MASLD. <em>J Hepatol</em>. 2024;81(3):492–542.", "10.1016/j.jhep.2024.04.031", None, None),
    ],
    "지방간-간암": [
        ("Huang DQ, El-Serag HB, Loomba R. Global epidemiology of NAFLD-related HCC: trends, predictions, risk factors and prevention. <em>Nat Rev Gastroenterol Hepatol</em>. 2021;18(4):223–238.", "10.1038/s41575-020-00381-6", "33349658", None),
        ("Anstee QM, Reeves HL, Kotsiliti E, Govaere O, Heikenwalder M. From NASH to HCC: current concepts and future challenges. <em>Nat Rev Gastroenterol Hepatol</em>. 2019;16(7):411–428.", "10.1038/s41575-019-0145-7", "31028350", None),
        ("Korean Liver Cancer Association (KLCA), National Cancer Center (NCC). 2022 KLCA-NCC Korea Practice Guidelines for the Management of Hepatocellular Carcinoma. <em>J Liver Cancer</em>. 2023;23(1):1–120.", "10.17998/jlc.2022.11.07", None, None),
        ("Singal AG, Llovet JM, Yarchoan M, et al. AASLD Practice Guidance on prevention, diagnosis, and treatment of hepatocellular carcinoma. <em>Hepatology</em>. 2023;78(6):1922–1965.", "10.1097/HEP.0000000000000466", "37199193", None),
    ],
    "지방간-회복-6개월": [
        ("Vilar-Gomez E, Martinez-Perez Y, Calzadilla-Bertot L, et al. Weight Loss Through Lifestyle Modification Significantly Reduces Features of Nonalcoholic Steatohepatitis. <em>Gastroenterology</em>. 2015;149(2):367–378.", "10.1053/j.gastro.2015.04.005", "25865049", None),
        ("Promrat K, Kleiner DE, Niemeier HM, et al. Randomized controlled trial testing the effects of weight loss on nonalcoholic steatohepatitis. <em>Hepatology</em>. 2010;51(1):121–129.", "10.1002/hep.23276", "19827166", None),
        ("Romero-Gómez M, Zelber-Sagi S, Trenell M. Treatment of NAFLD with diet, physical activity and exercise. <em>J Hepatol</em>. 2017;67(4):829–846.", "10.1016/j.jhep.2017.05.016", "28545937", None),
    ],
    "B형간염-평생약": [
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None, None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. Update on prevention, diagnosis, and treatment of chronic hepatitis B: AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329", None),
        ("European Association for the Study of the Liver. EASL 2017 Clinical Practice Guidelines on the management of hepatitis B virus infection. <em>J Hepatol</em>. 2017;67(2):370–398.", "10.1016/j.jhep.2017.03.021", None, None),
        ("Buti M, Riveiro-Barciela M, Esteban R. Long-term safety and efficacy of nucleos(t)ide analogue therapy in hepatitis B. <em>Liver Int</em>. 2018;38 Suppl 1:84–89.", "10.1111/liv.13641", "29427498", None),
    ],
    "B형간염-검사결과": [
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None, None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329", None),
        ("World Health Organization. Guidelines on hepatitis B and C testing. Geneva: WHO; 2017.", None, None, "https://www.who.int/publications/i/item/9789241549981"),
        ("European Association for the Study of the Liver. EASL 2017 Clinical Practice Guidelines on the management of hepatitis B. <em>J Hepatol</em>. 2017;67(2):370–398.", "10.1016/j.jhep.2017.03.021", None, None),
    ],
    "B형간염-결혼-임신": [
        ("Pan CQ, Duan Z, Dai E, et al. Tenofovir to Prevent Hepatitis B Transmission in Mothers with High Viral Load. <em>N Engl J Med</em>. 2016;374(24):2324–2334.", "10.1056/NEJMoa1508660", "27305192", None),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None, None),
        ("Brown RS Jr, McMahon BJ, Lok AS, et al. Antiviral therapy in chronic hepatitis B viral infection during pregnancy: A systematic review and meta-analysis. <em>Hepatology</em>. 2016;63(1):319–333.", "10.1002/hep.28302", "26565396", None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329", None),
    ],
    "가족-B형간염-검사": [
        ("Schillie S, Vellozzi C, Reingold A, et al. Prevention of Hepatitis B Virus Infection in the United States: Recommendations of the Advisory Committee on Immunization Practices. <em>MMWR Recomm Rep</em>. 2018;67(1):1–31.", "10.15585/mmwr.rr6701a1", "29939980", None),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None, None),
        ("Terrault NA, Lok ASF, McMahon BJ, et al. AASLD 2018 hepatitis B guidance. <em>Hepatology</em>. 2018;67(4):1560–1599.", "10.1002/hep.29800", "29405329", None),
    ],
    "C형간염-완치-DAA": [
        ("AASLD-IDSA HCV Guidance Panel. Hepatitis C Guidance 2018 Update: AASLD-IDSA Recommendations for Testing, Managing, and Treating Hepatitis C Virus Infection. <em>Clin Infect Dis</em>. 2018;67(10):1477–1492.", "10.1093/cid/ciy585", "30215672", None),
        ("Korean Association for the Study of the Liver (KASL). 2020 KASL clinical practice guidelines for management of hepatitis C. <em>Clin Mol Hepatol</em>. 2020;26(2):83–127.", "10.3350/cmh.2020.0010", None, None),
        ("Zeuzem S, Foster GR, Wang S, et al. Glecaprevir-Pibrentasvir for 8 or 12 Weeks in HCV Genotype 1 or 3 Infection. <em>N Engl J Med</em>. 2018;378(4):354–369.", "10.1056/NEJMoa1702417", "29365309", None),
        ("Falade-Nwulia O, Suarez-Cuervo C, Nelson DR, et al. Oral Direct-Acting Agent Therapy for Hepatitis C Virus Infection: A Systematic Review. <em>Ann Intern Med</em>. 2017;166(9):637–648.", "10.7326/M16-2575", "28319996", None),
    ],
    "B형간염-간암검진": [
        ("Korean Liver Cancer Association (KLCA), National Cancer Center (NCC). 2022 KLCA-NCC Korea Practice Guidelines for the Management of Hepatocellular Carcinoma. <em>J Liver Cancer</em>. 2023;23(1):1–120.", "10.17998/jlc.2022.11.07", None, None),
        ("Singal AG, Llovet JM, Yarchoan M, et al. AASLD Practice Guidance on prevention, diagnosis, and treatment of hepatocellular carcinoma. <em>Hepatology</em>. 2023;78(6):1922–1965.", "10.1097/HEP.0000000000000466", "37199193", None),
        ("Korean Association for the Study of the Liver (KASL). KASL clinical practice guidelines for management of chronic hepatitis B. <em>Clin Mol Hepatol</em>. 2022;28(2):276–331.", "10.3350/cmh.2022.0084", None, None),
        ("Park JW, Chen M, Colombo M, et al. Global patterns of hepatocellular carcinoma management from diagnosis to death: the BRIDGE Study. <em>Liver Int</em>. 2015;35(9):2155–2166.", "10.1111/liv.12818", "25752327", None),
    ],
}

def render_refs(refs):
    out = ['<section class="references-block">', '<h2>References</h2>', '<ol class="references">']
    for text, doi, pmid, extra in refs:
        line = f'<li>{text}'
        links = []
        if doi:
            links.append(f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener">DOI</a>')
        if pmid:
            links.append(f'<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" rel="noopener">PMID {pmid}</a>')
        if extra:
            links.append(f'<a href="{extra}" target="_blank" rel="noopener">Link</a>')
        if links:
            line += ' ' + ' · '.join(links)
        line += '</li>'
        out.append(line)
    out.append('</ol>')
    out.append('</section>')
    return "\n".join(out)

print(f"Adding References to {len(REFS)} articles...\n")
for slug, refs in REFS.items():
    p = ROOT / slug / "index.html"
    if not p.exists():
        print(f"  SKIP (missing): {slug}")
        continue
    h = p.read_text(encoding="utf-8")

    if "references-block" in h:
        print(f"  already has refs: {slug}")
        continue

    refs_html = render_refs(refs)
    # Insert before <aside class="author-box">
    new_h = h.replace(
        '<aside class="author-box">',
        f'{refs_html}\n\n<aside class="author-box">',
        1
    )
    if new_h == h:
        print(f"  FAIL (no anchor): {slug}")
        continue

    p.write_text(new_h, encoding="utf-8")
    print(f"  added: {slug} ({len(refs)} refs)")

print("\nDone.")
