#!/usr/bin/env python3
"""
translate_case_jargon.py — 81 case 페이지의 case-section 내러티브에서 의학 용어를
환자가 이해할 수 있는 한국어로 풀이/병기.

대상 섹션:
  - <div class="case-section">…</div>
  - <div class="case-intro">…</div> (있다면)

스킵 섹션:
  - <div class="teaching-box"> — 의료진용으로 jargon 유지
  - <aside class="case-pearl"> — 임상 트리비아, jargon 일부 유지
  - <section class="faq-block"> — 별도 cleanup 도구로 처리
  - <script type="application/ld+json"> — JSON-LD

처리 패턴:
  1. 복용 빈도 약어 풀이 (q4h, bid, tid, qid, qd, prn)
  2. 약물명 한글 병기 (lactulose → 락툴로오스(lactulose))
  3. 약어 풀이 (PPI → 위산 억제제(PPI))
  4. 단위·검사명 친화화 (NH3 → 암모니아 수치, K+ → 칼륨)
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 약물명: 영문 → 한글(영문) 형식. 첫 등장만 한글 추가 효과 + 추후 등장 시 그대로.
DRUGS = [
    ("lactulose", "락툴로오스(lactulose, 달콤한 시럽 형태로 장에서 암모니아를 빼냅니다)"),
    ("rifaximin", "리팍시민(rifaximin, 장에서만 작용하는 항생제)"),
    ("terlipressin", "터리프레신(terlipressin, 정맥류 출혈을 멈추는 혈관수축제)"),
    ("octreotide", "옥트레오타이드(octreotide, 정맥류 출혈을 멈추는 호르몬 유사 약물)"),
    ("spironolactone", "스피로노락톤(spironolactone, 복수에 쓰는 이뇨제)"),
    ("furosemide", "푸로세마이드(furosemide, 강한 이뇨제)"),
    ("propranolol", "프로프라놀롤(propranolol, 정맥류 예방용 베타차단제)"),
    ("carvedilol", "카르베디롤(carvedilol, 정맥류 예방용 베타차단제)"),
    ("entecavir", "엔테카비어(entecavir, B형간염 항바이러스제)"),
    ("tenofovir", "테노포비어(tenofovir, B형간염 항바이러스제)"),
    ("atezolizumab", "아테졸리주맙(atezolizumab, 면역치료제)"),
    ("bevacizumab", "베바시주맙(bevacizumab, 혈관 신생 억제제)"),
    ("durvalumab", "더발루맙(durvalumab, 면역치료제)"),
    ("tremelimumab", "트레멜리무맙(tremelimumab, 면역치료제)"),
    ("nivolumab", "니볼루맙(nivolumab, 면역치료제)"),
    ("pembrolizumab", "펨브롤리주맙(pembrolizumab, 면역치료제)"),
    ("lenvatinib", "렌바티닙(lenvatinib, 표적치료제)"),
    ("sorafenib", "소라페닙(sorafenib, 표적치료제)"),
    ("regorafenib", "레고라페닙(regorafenib, 표적치료제)"),
    ("cabozantinib", "카보잔티닙(cabozantinib, 표적치료제)"),
    ("ramucirumab", "라무시루맙(ramucirumab, 표적치료제)"),
    ("ipilimumab", "이필리무맙(ipilimumab, 면역치료제)"),
    ("rituximab", "리툭시맙(rituximab, B세포 표적 면역억제 약)"),
    ("prednisolone", "프레드니솔론(prednisolone, 스테로이드)"),
    ("azathioprine", "아자티오프린(azathioprine, 면역억제제)"),
    ("mycophenolate", "마이코페놀레이트(mycophenolate, 면역억제제)"),
    ("budesonide", "부데소나이드(budesonide, 국소 작용 스테로이드)"),
    ("tacrolimus", "타크롤리무스(tacrolimus, 면역억제제)"),
    ("ursodeoxycholic acid", "우르소데옥시콜산(UDCA, 담즙산 흐름 개선제)"),
    ("obeticholic acid", "오베티콜릭산(obeticholic acid, 담즙정체 치료제)"),
    ("resmetirom", "레스메티롬(resmetirom, MASH 표적 치료제)"),
    ("semaglutide", "세마글루타이드(semaglutide, GLP-1 비만·당뇨약)"),
    ("tirzepatide", "터제파타이드(tirzepatide, GLP-1/GIP 이중 작용 약)"),
    ("liraglutide", "리라글루타이드(liraglutide, GLP-1 약)"),
    ("amoxicillin-clavulanate", "아목시실린-클라불라네이트(항생제 조합)"),
    ("cholestyramine", "콜레스티라민(cholestyramine, 담즙산 결합제)"),
    ("avatrombopag", "아바트롬보팍(avatrombopag, 혈소판 상승제)"),
    ("lusutrombopag", "루수트롬보팍(lusutrombopag, 혈소판 상승제)"),
    ("ceftriaxone", "세프트리악손(ceftriaxone, 항생제)"),
    ("norfloxacin", "노르플록사신(norfloxacin, 예방용 항생제)"),
    ("midodrine", "미도드린(midodrine, 혈압을 올리는 약)"),
    ("albumin", "알부민(albumin, 혈장 단백질 보충제)"),
    ("tolvaptan", "톨밥탄(tolvaptan, 저나트륨혈증 교정 약)"),
]

# 약어: 한글 풀이 병기 (첫 등장 시 효과적)
ABBREVIATIONS = [
    # 약물 클래스
    (r'\bPPI\b(?!\s*-)', '위산 억제제(PPI)'),  # PIVKA-II 같은 합성어 회피
    (r'\bNSAIDs?\b', '소염진통제(NSAIDs)'),
    (r'\bDOAC\b', '직접 작용 항응고제(DOAC)'),
    (r'\bDAA\b', '직접 작용 항바이러스제(DAA)'),
    (r'\bART\b', '항레트로바이러스 치료(ART)'),
    (r'\bMMF\b', '마이코페놀레이트(MMF)'),
    (r'\bAZA\b', '아자티오프린(AZA)'),
    (r'\bTAF\b', '테노포비어 알라페나미드(TAF)'),
    (r'\bTDF\b', '테노포비어 디소프록실(TDF)'),
    (r'\bETV\b', '엔테카비어(ETV)'),
    (r'\bUDCA\b', '우르소데옥시콜산(UDCA)'),
    (r'\bOCA\b', '오베티콜릭산(OCA)'),
    (r'\bGLP-1\b', 'GLP-1(혈당·체중 조절 호르몬)'),
    (r'\bSGLT2\b', 'SGLT2(혈당 조절 약 계열)'),
    # 임상 약어
    (r'\bSBP\b(?!\s*-)', '복수 감염(SBP, 자발성 세균성 복막염)'),
    (r'\bHRS\b', '간신증후군(HRS)'),
    (r'\bHE\b(?![A-Za-z])', '간성혼수(HE)'),
    (r'\bACLF\b', '만성 간부전 위 급성 악화(ACLF)'),
    (r'\bALF\b(?![A-Za-z])', '급성 간부전(ALF)'),
    (r'\bTIPS\b', 'TIPS(경경정맥 간내 문맥-체순환 단락술)'),
    (r'\bRFA\b', '고주파 열치료(RFA)'),
    (r'\bMWA\b', '마이크로웨이브 열치료(MWA)'),
    (r'\bTACE\b', '경동맥화학색전술(TACE)'),
    (r'\bTARE\b', '경동맥방사선색전술(TARE)'),
    (r'\bSBRT\b', '정위적 체부 방사선치료(SBRT)'),
    (r'\bICI\b', '면역관문억제제(ICI)'),
    # Score
    (r'\bMELD\b', 'MELD 점수(말기 간 질환 중증도 점수)'),
    (r'\bChild-Pugh\b', 'Child-Pugh 점수(간 기능 중증도 점수)'),
    (r'\bBCLC\b', 'BCLC 병기(간세포암 병기 분류)'),
    # 검사
    (r'\bMRCP\b', '자기공명담췌관조영(MRCP)'),
    (r'\bICP\b(?![A-Za-z])', '임신성 간내 담즙정체(ICP)'),
    (r'\bMASLD\b', '대사이상지방간(MASLD)'),
    (r'\bMASH\b', '대사이상지방간염(MASH)'),
    (r'\bAIH\b', '자가면역간염(AIH)'),
    (r'\bPBC\b(?!\s*-)', '원발성담즙성담관염(PBC)'),
    (r'\bPSC\b', '원발성경화성담관염(PSC)'),
    (r'\bHCC\b', '간세포암(HCC)'),
    (r'\bHCA\b', '간세포선종(HCA)'),
    (r'\bFNH\b', 'FNH(국소 결절성 과증식)'),
    (r'\bHBV\b', 'B형간염 바이러스(HBV)'),
    (r'\bHCV\b', 'C형간염 바이러스(HCV)'),
    (r'\bHDV\b', 'D형간염 바이러스(HDV)'),
    (r'\bSVR\b(?:\d+)?', '지속바이러스반응(SVR, 완치)'),
    # 검사 수치 약어 (잘 안 알려진 것들)
    (r'\bNH3\b', '암모니아(NH3)'),
    (r'\bAFP\b', '알파태아단백(AFP)'),
    (r'\bPIVKA-II\b', 'PIVKA-II(간세포암 표지자)'),
    (r'\bALP\b', 'ALP(담도 지표 효소)'),
    (r'\bGGT\b', 'GGT(담도 지표 효소)'),
    (r'\bIgG\b', 'IgG(면역글로불린G)'),
    (r'\bIgM\b', 'IgM(면역글로불린M)'),
    (r'\bAMA\b', 'AMA(항미토콘드리아 항체)'),
    (r'\bANA\b', 'ANA(항핵항체)'),
    (r'\bASMA\b', 'ASMA(항평활근항체)'),
    (r'\bHBsAg\b', 'HBsAg(B형간염 표면 항원)'),
    (r'\banti-HBs\b', 'anti-HBs(B형간염 보호 항체)'),
    (r'\banti-HCV\b', 'anti-HCV(C형간염 항체)'),
    (r'\bHBeAg\b', 'HBeAg(B형간염 e 항원)'),
    (r'\banti-HBe\b', 'anti-HBe(B형간염 e 항체)'),
    (r'\banti-HBc\b', 'anti-HBc(B형간염 core 항체)'),
    (r'\bHBV DNA\b', 'HBV DNA(B형간염 바이러스 양)'),
    (r'\bHCV RNA\b', 'HCV RNA(C형간염 바이러스 양)'),
]

# 복용 빈도 약어 (라틴어 처방 표기) → 환자가 이해할 한국어
FREQUENCY = [
    (r'(\d+(?:\.\d+)?)\s*mL\s+q(\d+)h', r'\2시간마다 \1 mL'),
    (r'(\d+(?:\.\d+)?)\s*mg\s+q(\d+)h', r'\2시간마다 \1 mg'),
    (r'(\d+(?:\.\d+)?\s*(?:mg|mL))\s+bid\b', r'\1을 하루 두 번'),
    (r'(\d+(?:\.\d+)?\s*(?:mg|mL))\s+tid\b', r'\1을 하루 세 번'),
    (r'(\d+(?:\.\d+)?\s*(?:mg|mL))\s+qid\b', r'\1을 하루 네 번'),
    (r'(\d+(?:\.\d+)?\s*(?:mg|mL))\s+qd\b', r'\1을 하루 한 번'),
    (r'(\d+(?:\.\d+)?\s*(?:mg|mL))\s+prn\b', r'\1을 필요할 때'),
    # 단순 q4h/bid 등 (앞에 용량 없는 경우)
    (r'\bq(\d+)h\b', r'\1시간마다'),
    (r'\bbid\b', '하루 두 번'),
    (r'\btid\b', '하루 세 번'),
    (r'\bqid\b', '하루 네 번'),
]


def first_occurrence_replace(text: str, pattern: str, replacement: str) -> tuple[str, int]:
    """첫 occurrence만 replace (그 이후 등장은 그대로)."""
    rx = re.compile(pattern)
    m = rx.search(text)
    if m:
        new_text = text[:m.start()] + rx.sub(replacement, text[m.start():], count=1)
        return new_text, 1
    return text, 0


def process_case_section(faq: str) -> tuple[str, int]:
    """한 case-section 또는 case-intro 내용에 패턴 적용."""
    fixes = 0
    # 1. 빈도 약어 (먼저 처리 — 더 구체적)
    for pat, repl in FREQUENCY:
        new = re.sub(pat, repl, faq)
        if new != faq:
            fixes += len(re.findall(pat, faq))
            faq = new
    # 2. 약어 풀이 (첫 등장만)
    for pat, repl in ABBREVIATIONS:
        faq, n = first_occurrence_replace(faq, pat, repl)
        fixes += n
    # 3. 약물명 한글 병기 (첫 등장만)
    for drug_en, drug_full in DRUGS:
        # case-insensitive but preserve casing
        rx = re.compile(r'\b' + re.escape(drug_en) + r'\b', re.IGNORECASE)
        m = rx.search(faq)
        if m:
            faq = faq[:m.start()] + drug_full + faq[m.end():]
            fixes += 1
    return faq, fixes


SECTION_RE = re.compile(
    r'(<div class="case-(?:section|intro)"[^>]*>)(.*?)(</div>)',
    re.DOTALL,
)


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    total_fixes = 0

    def replace_section(m):
        nonlocal total_fixes
        prefix, content, suffix = m.groups()
        new_content, fixes = process_case_section(content)
        total_fixes += fixes
        return prefix + new_content + suffix

    new_text = SECTION_RE.sub(replace_section, text)

    if new_text != original:
        path.write_text(new_text, encoding="utf-8")
        return total_fixes
    return 0


def main():
    cases_dir = ROOT / "케이스"
    if not cases_dir.exists():
        print("케이스 폴더 없음")
        return

    pages_updated = 0
    total_fixes = 0
    for p in sorted(cases_dir.glob("*/index.html")):
        n = process_file(p)
        if n > 0:
            pages_updated += 1
            total_fixes += n
            print(f"  [{n:2d}] {p.parent.name}")

    print()
    print(f"케이스 jargon 번역 완료: {pages_updated} 페이지, 총 {total_fixes} 건 치환")


if __name__ == "__main__":
    main()
