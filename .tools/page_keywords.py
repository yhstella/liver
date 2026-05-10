"""Per-page keywords (5 each) for related-page lookup.

Vocabulary is intentionally compact — ~50 canonical terms cover the site.
Keywords are matched as exact strings for related-page Jaccard overlap.

Each page has exactly 5 keywords.
"""
from __future__ import annotations

# === Canonical vocabulary (groups; not enforced, just for human reference) ===
DISEASES = ["간세포암", "간경변", "B형간염", "C형간염", "MASLD", "MASH", "약물성간손상",
            "지방간", "급성간부전", "자가면역간염"]
STAGING = ["BCLC", "Child-Pugh", "MELD", "F2섬유화", "비대상성", "대상성"]
TREATMENT = [
    "절제", "고주파열치료술", "TACE", "TARE", "SBRT", "양성자치료", "면역치료",
    "atezolizumab+bevacizumab", "STRIDE", "sorafenib", "lenvatinib",
    "간이식", "LDLT", "다운스테이징",
    "TDF", "TAF", "엔테카비르", "DAA", "sofosbuvir",
    "GLP-1RA", "SGLT2", "resmetirom", "지중해식",
    "스테로이드", "아자티오프린", "ursodeoxycholic acid",
]
BIOMARKERS = [
    "AFP", "PIVKA-II", "ALT", "AST", "GGT", "ALP", "빌리루빈", "알부민", "PT", "INR",
    "HBV DNA", "HBsAg", "HBeAg", "anti-HBs", "anti-HBe", "anti-HCV", "FIB-4", "Fibroscan",
    "혈소판", "IgG", "ANA", "ASMA",
]
MODALITIES = ["초음파", "CT", "MRI", "EOB-MRI", "CEUS", "LI-RADS", "간생검"]
MGMT = ["검진", "추적", "재발", "백신", "가족검사", "임신·수유", "식이·운동", "다학제"]
COMPLICATIONS = ["정맥류", "복수", "간성혼수", "간신증후군", "SBP", "문맥압항진"]
TOPICS = ["면역", "한국가이드라인", "PMC OA", "MR연구", "RCT"]


# === Per-slug curated keywords (exactly 5 each) ===
PAGE_KEYWORDS: dict[str, list[str]] = {
    # === 간암 세부주제 (1-1 ~ 1-11) ===
    "간암-진단-첫외래": ["간세포암", "BCLC", "다학제", "검진", "Child-Pugh"],
    "간암-BCLC병기": ["BCLC", "간세포암", "Child-Pugh", "한국가이드라인", "절제"],
    "간암-치료-선택": ["간세포암", "절제", "고주파열치료술", "TACE", "BCLC"],
    "간암-면역치료-1차": ["면역치료", "atezolizumab+bevacizumab", "STRIDE", "간세포암", "정맥류"],
    "간암-간이식": ["간이식", "LDLT", "간세포암", "다운스테이징", "Child-Pugh"],
    "알파태아단백": ["AFP", "검진", "간세포암", "PIVKA-II", "B형간염"],
    "B형간염-간암검진": ["검진", "B형간염", "간세포암", "초음파", "AFP"],
    "지방간-간암": ["MASLD", "MASH", "간세포암", "검진", "Fibroscan"],
    "간암-재발-추적": ["재발", "간세포암", "추적", "EOB-MRI", "AFP"],
    "간암-식이-일상": ["식이·운동", "간세포암", "추적", "재발", "MASLD"],
    "간암-방사선색전술": ["TARE", "간세포암", "TACE", "다운스테이징", "BCLC"],

    # === 간암 케이스 (1-12 ~ 1-26) ===
    "케이스/건강검진-우연발견-1cm결절": ["검진", "B형간염", "BCLC", "고주파열치료술", "간세포암"],
    "케이스/B형간염-검진-새결절": ["검진", "B형간염", "간세포암", "절제", "EOB-MRI"],
    "케이스/AFP상승-영상음성": ["AFP", "EOB-MRI", "B형간염", "고주파열치료술", "간세포암"],
    "케이스/LR3-모호결절-추적": ["LI-RADS", "B형간염", "Fibroscan", "EOB-MRI", "추적"],
    "케이스/PIVKAII-와파린-위양성": ["PIVKA-II", "AFP", "B형간염", "검진", "EOB-MRI"],
    "케이스/MASLD-HCC-비만당뇨": ["MASLD", "MASH", "간세포암", "절제", "Fibroscan"],
    "케이스/BCLC-A-단일3cm-절제vs소작": ["BCLC", "절제", "고주파열치료술", "간세포암", "Child-Pugh"],
    "케이스/BCLC-A-다발3개-소작": ["BCLC", "고주파열치료술", "C형간염", "간세포암", "다운스테이징"],
    "케이스/ChildB-단일4cm-이식": ["Child-Pugh", "간이식", "LDLT", "TACE", "간세포암"],
    "케이스/BCLC-B-다발성-TACE": ["BCLC", "TACE", "간세포암", "B형간염", "다운스테이징"],
    "케이스/큰종양-TACE-SBRT-결합": ["TACE", "SBRT", "다운스테이징", "간이식", "간세포암"],
    "케이스/문맥침범-AtezoBev": ["면역치료", "atezolizumab+bevacizumab", "BCLC", "정맥류", "간세포암"],
    "케이스/정맥류출혈이력-STRIDE": ["STRIDE", "정맥류", "면역치료", "Child-Pugh", "간세포암"],
    "케이스/다운스테이징-이식전환": ["다운스테이징", "TACE", "SBRT", "간이식", "간세포암"],
    "케이스/절제후-2년재발": ["재발", "고주파열치료술", "C형간염", "추적", "간세포암"],

    # === 간경화 케이스 (2-11 ~ 2-15) ===
    "케이스/첫-식도정맥류-출혈": ["정맥류", "간경변", "B형간염", "Child-Pugh", "문맥압항진"],
    "케이스/복수-SBP-진단치료": ["복수", "SBP", "간경변", "비대상성", "Child-Pugh"],
    "케이스/간성혼수-첫발생": ["간성혼수", "간경변", "C형간염", "비대상성", "약물성간손상"],
    "케이스/ChildC-이식대기": ["Child-Pugh", "MELD", "간이식", "LDLT", "비대상성"],
    "케이스/간경변-새결절-평가": ["간경변", "EOB-MRI", "간세포암", "B형간염", "고주파열치료술"],

    # === B형간염 케이스 (3-11 ~ 3-15) ===
    "케이스/직장검진-HBsAg양성": ["B형간염", "HBsAg", "검진", "가족검사", "간세포암"],
    "케이스/임신중-HBsAg발견": ["B형간염", "임신·수유", "TDF", "HBV DNA", "가족검사"],
    "케이스/항암치료전-재활성화예방": ["B형간염", "면역치료", "엔테카비르", "anti-HBs", "HBV DNA"],
    "케이스/ETV-TAF-전환": ["엔테카비르", "TAF", "B형간염", "추적", "TDF"],
    "케이스/HBeAg-seroclearance-약중단": ["HBeAg", "B형간염", "TAF", "HBV DNA", "추적"],

    # === 지방간 케이스 (4-11 ~ 4-15) ===
    "케이스/검진ALT상승-MASLD진단": ["MASLD", "FIB-4", "Fibroscan", "ALT", "검진"],
    "케이스/MASLD-F2-GLP1시작": ["MASLD", "GLP-1RA", "MASH", "Fibroscan", "식이·운동"],
    "케이스/MASH-F3-당뇨-종합관리": ["MASH", "MASLD", "SGLT2", "GLP-1RA", "Fibroscan"],
    "케이스/lean-MASLD-비만없음": ["MASLD", "FIB-4", "Fibroscan", "지방간", "식이·운동"],
    "케이스/resmetirom-신약시작": ["resmetirom", "MASH", "MASLD", "Fibroscan", "RCT"],

    # === 간수치 이상 케이스 (5-10 ~ 5-14) ===
    "케이스/검진ALT상승-원인감별": ["ALT", "AST", "MASLD", "Fibroscan", "검진"],
    "케이스/자가면역간염-첫진단": ["자가면역간염", "ALT", "간생검", "스테로이드", "IgG"],
    "케이스/약물성간손상-항결핵제": ["약물성간손상", "ALT", "AST", "추적", "검진"],
    "케이스/독성간염-야생버섯": ["약물성간손상", "ALT", "급성간부전", "간이식", "AST"],
    "케이스/보충제-ALT상승": ["약물성간손상", "ALT", "AST", "추적", "검진"],

    # === 간경화 세부주제 (2-1 ~ 2-10) ===
    "간경변-대상성-비대상성": ["간경변", "대상성", "비대상성", "Child-Pugh", "MELD"],
    "간경변-Child-Pugh-MELD": ["Child-Pugh", "MELD", "간경변", "간이식", "알부민"],
    "간경변-식도정맥류": ["정맥류", "간경변", "문맥압항진", "비대상성", "Child-Pugh"],
    "간경변-복수": ["복수", "간경변", "비대상성", "SBP", "알부민"],
    "간경변-간성혼수": ["간성혼수", "간경변", "비대상성", "약물성간손상", "MELD"],
    "간경변-간신증후군": ["간신증후군", "간경변", "비대상성", "MELD", "복수"],
    "간경변-영양-근감소증": ["식이·운동", "간경변", "알부민", "비대상성", "Child-Pugh"],
    "간경변-간이식-평가": ["간이식", "MELD", "LDLT", "간경변", "Child-Pugh"],
    "간경변-약물-주의": ["간경변", "약물성간손상", "ALT", "PT", "비대상성"],
    "간경변-정상수치-함정": ["간경변", "ALT", "알부민", "Fibroscan", "혈소판"],

    # === B형간염 세부주제 (3-1 ~ 3-10) ===
    "B형간염-평생약": ["TDF", "TAF", "엔테카비르", "B형간염", "HBV DNA"],
    "B형간염-검사결과": ["B형간염", "HBsAg", "HBeAg", "HBV DNA", "ALT"],
    "B형간염-결혼-임신": ["B형간염", "임신·수유", "TDF", "가족검사", "HBV DNA"],
    "가족-B형간염-검사": ["가족검사", "B형간염", "HBsAg", "anti-HBs", "백신"],
    "B형간염-백신": ["백신", "B형간염", "anti-HBs", "가족검사", "HBsAg"],
    "B형간염-HBeAg-양성-음성": ["HBeAg", "B형간염", "HBV DNA", "ALT", "anti-HBe"],
    "B형간염-항바이러스제-비교": ["TDF", "TAF", "엔테카비르", "B형간염", "HBV DNA"],
    "B형간염-functional-cure": ["B형간염", "HBsAg", "면역치료", "HBV DNA", "anti-HBs"],
    "B형간염-재활성화": ["B형간염", "면역치료", "HBV DNA", "검진", "엔테카비르"],
    "C형간염-완치-DAA": ["C형간염", "DAA", "sofosbuvir", "검진", "간경변"],

    # === 지방간 세부주제 (4-1 ~ 4-10) ===
    "대사이상지방간-MASLD": ["MASLD", "MASH", "Fibroscan", "FIB-4", "식이·운동"],
    "술-안마셔도-지방간": ["MASLD", "지방간", "MASH", "식이·운동", "FIB-4"],
    "지방간-치료": ["MASLD", "GLP-1RA", "SGLT2", "resmetirom", "식이·운동"],
    "지방간-음식": ["식이·운동", "MASLD", "MASH", "지중해식", "지방간"],
    "지방간-회복-6개월": ["MASLD", "추적", "ALT", "Fibroscan", "식이·운동"],
    "지방간-정밀검사": ["FIB-4", "Fibroscan", "MASLD", "MASH", "간생검"],
    "지방간-lean-MASLD": ["MASLD", "지방간", "FIB-4", "식이·운동", "MASH"],
    "지방간-신약-resmetirom": ["resmetirom", "MASH", "MASLD", "Fibroscan", "RCT"],
    "지방간염-MASH": ["MASH", "MASLD", "Fibroscan", "FIB-4", "간생검"],
    "지방간-SGLT2-GLP1": ["SGLT2", "GLP-1RA", "MASLD", "MASH", "식이·운동"],

    # === 간수치 이상 세부주제 (5-1 ~ 5-9) ===
    "간수치-높음": ["ALT", "AST", "GGT", "약물성간손상", "MASLD"],
    "간수치-종류-차이": ["ALT", "AST", "GGT", "ALP", "빌리루빈"],
    "간섬유화스캔-수치": ["Fibroscan", "FIB-4", "MASH", "간경변", "MASLD"],
    "빌리루빈-직접-간접": ["빌리루빈", "ALT", "ALP", "간경변", "약물성간손상"],
    "알부민-PT-간합성능": ["알부민", "PT", "INR", "간경변", "Child-Pugh"],
    "ALP-GGT-담도-간세포": ["ALP", "GGT", "간경변", "빌리루빈", "약물성간손상"],
    "약물성-간손상-DILI": ["약물성간손상", "ALT", "AST", "간생검", "추적"],
    "PIVKA-II-간암마커": ["PIVKA-II", "AFP", "간세포암", "검진", "B형간염"],
    "간생검-언제-필요한가": ["간생검", "MASH", "약물성간손상", "자가면역간염", "Fibroscan"],

    # === 최신 지견 (6-1 ~ 6-20) ===
    "updates/Shin-ETV-TAF-RCT-GnL-2026": ["엔테카비르", "TAF", "B형간염", "RCT", "TDF"],
    "updates/Ahn-Aspirin-HCC-MASLD-CMH-2026": ["MASLD", "간세포암", "PMC OA", "MR연구", "MASH"],
    "updates/Shin-CIK-HCC-CII-2026": ["면역치료", "간세포암", "재발", "RCT", "한국가이드라인"],
    "updates/Shin-AI-CT-HCC-CHB-JHep-2025": ["B형간염", "검진", "간세포암", "CT", "PMC OA"],
    "updates/Shin-HCC-Guidelines-Review-JLC-2025": ["한국가이드라인", "BCLC", "간세포암", "면역치료", "PMC OA"],
    "updates/GLP1RA-알코올성-간질환-ALD": ["GLP-1RA", "지방간", "MASH", "식이·운동", "RCT"],
    "updates/Chung-SGLT2-Liver-MR-Hepatology-2024": ["SGLT2", "MASLD", "MR연구", "MASH", "PMC OA"],
    "updates/Shin-Antiviral-CV-CHB-JMV-2024": ["B형간염", "TDF", "엔테카비르", "TAF", "PMC OA"],
    "updates/Shin-HBeAg-seroclearance-HCC-JHepR-2024": ["HBeAg", "B형간염", "간세포암", "검진", "PMC OA"],
    "updates/Shin-TDF-ETV-TAF-switch-HCC-HepRes-2024": ["TDF", "엔테카비르", "TAF", "간세포암", "B형간염"],
    "updates/MAESTRO-NASH-resmetirom-NEJM-2024": ["resmetirom", "MASH", "RCT", "MASLD", "Fibroscan"],
    "updates/Shin-COVID-HBV-NK-IN-2023": ["B형간염", "면역치료", "PMC OA", "RCT", "검진"],
    "updates/GLP1RA-small-molecule-orforglipron": ["GLP-1RA", "MASLD", "RCT", "MASH", "식이·운동"],
    "updates/HIMALAYA-durvalumab-tremelimumab-NEJM-Evid-2022": ["STRIDE", "면역치료", "간세포암", "정맥류", "RCT"],
    "updates/Baveno-VII-portal-hypertension-J-Hepatol-2022": ["문맥압항진", "정맥류", "간경변", "한국가이드라인", "비대상성"],
    "updates/Newsome-semaglutide-NASH-NEJM-2021": ["GLP-1RA", "MASH", "RCT", "MASLD", "식이·운동"],
    "updates/IMbrave150-atezolizumab-bevacizumab-NEJM-2020": ["atezolizumab+bevacizumab", "면역치료", "간세포암", "RCT", "BCLC"],
    "updates/PEth-알코올-바이오마커": ["지방간", "MASH", "MASLD", "ALT", "약물성간손상"],
    "updates/Pan-TDF-pregnancy-HBV-NEJM-2016": ["TDF", "B형간염", "임신·수유", "가족검사", "HBV DNA"],
    "updates/preemptive-TIPS-식도정맥류-출혈": ["정맥류", "문맥압항진", "간경변", "비대상성", "Child-Pugh"],
}


def get(slug: str) -> list[str]:
    """Return keywords for a slug, or [] if not defined."""
    return PAGE_KEYWORDS.get(slug, [])


def all_pages() -> list[str]:
    return list(PAGE_KEYWORDS.keys())
