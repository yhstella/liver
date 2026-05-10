"""Replace medical abbreviations with Korean names + drug spelling change.
First-occurrence-per-page replacement to keep documents readable.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Order matters — longer patterns first
ABBR_MAP = [
    # Drug spelling — global replace (no parentheses needed)
    ("엔테카비르", "엔테카비어", False),
    ("테노포비르", "테노포비어", False),
    # Drug abbreviation → first occurrence Korean(EN)
    (r"(?<![A-Za-z])ETV(?![A-Za-z])", "엔테카비어(ETV)", True),
    (r"(?<![A-Za-z])TDF(?![A-Za-z])", "테노포비어 DF(TDF)", True),
    (r"(?<![A-Za-z])TAF(?![A-Za-z])", "테노포비어 AF(TAF)", True),
    # Medical abbreviations — first occurrence Korean(EN)
    (r"\bSBP\b", "자발성 세균성 복막염(SBP)", True),
    (r"\bAIH\b", "자가면역간염(AIH)", True),
    (r"\bAZA\b", "아자티오프린(AZA)", True),
    (r"\bMMF\b", "마이코페놀레이트(MMF)", True),
    (r"\bDAA\b", "직접 작용 항바이러스제(DAA)", True),
    (r"\bTIPS\b", "경경정맥 간내 문맥대정맥 단락술(TIPS)", True),
    (r"\bLDLT\b", "생체 간이식(LDLT)", True),
    (r"\bDDLT\b", "뇌사자 간이식(DDLT)", True),
    (r"\bKONOS\b", "한국 장기이식관리센터(KONOS)", True),
    (r"\bRFA\b", "고주파열치료술(RFA)", True),
    (r"\bPBC\b", "원발담즙성담관염(PBC)", True),
    (r"\bPSC\b", "원발경화담관염(PSC)", True),
    (r"\bAMA\b", "항미토콘드리아항체(AMA)", True),
    (r"\bANA\b", "항핵항체(ANA)", True),
    (r"\bASMA\b", "항평활근항체(ASMA)", True),
    (r"\bMRCP\b", "자기공명담췌관조영(MRCP)", True),
    (r"\bMRE\b", "자기공명탄성영상(MRE)", True),
    (r"\bSVR12\b", "지속바이러스반응(SVR12)", True),
    (r"\bSVR\b", "지속바이러스반응(SVR)", True),
    (r"\bHCC\b", "간세포암(HCC)", True),
    (r"\bCHB\b", "만성 B형간염(CHB)", True),
    (r"\bHBIG\b", "B형간염 면역글로불린(HBIG)", True),
    (r"\bMASH\b", "대사이상지방간염(MASH)", True),
    (r"\bMASLD\b", "대사이상지방간질환(MASLD)", True),
    (r"\bMetALD\b", "대사·알코올 동반(MetALD)", True),
    (r"\bNASH\b", "비알코올성 지방간염(NASH)", True),
    (r"\bNAFLD\b", "비알코올성 지방간질환(NAFLD)", True),
    (r"\bSBRT\b", "정위적 체부 방사선치료(SBRT)", True),
    (r"\bTACE\b", "경동맥화학색전술(TACE)", True),
    (r"\bTARE\b", "경동맥방사선색전술(TARE)", True),
    (r"\bICI\b", "면역관문억제제(ICI)", True),
    (r"\bMSM\b", "동성간 성접촉(MSM)", True),
    (r"\bHEV\b", "E형간염바이러스(HEV)", True),
    (r"\bCEUS\b", "조영초음파(CEUS)", True),
    (r"\bAFP\b", "알파태아단백(AFP)", True),
]


def process(text: str) -> str:
    # Mask sensitive sections
    masks = {"i": 0, "list": []}

    def mask(pattern, t):
        def store(m):
            masks["list"].append(m.group(0))
            i = masks["i"]
            masks["i"] += 1
            return f"\x00MASK{i}\x00"
        return re.sub(pattern, store, t, flags=re.DOTALL)

    out = text
    out = mask(r"<head>.*?</head>", out)
    out = mask(r"<script[^>]*>.*?</script>", out)
    out = mask(r"<style[^>]*>.*?</style>", out)
    out = mask(r"<code[^>]*>.*?</code>", out)
    out = mask(r"<a [^>]*>", out)
    out = mask(r'class="[^"]*"', out)

    for pat, repl, first_only in ABBR_MAP:
        if first_only:
            out = re.sub(pat, repl, out, count=1)
        else:
            out = re.sub(pat, repl, out)

    for i, m in enumerate(masks["list"]):
        out = out.replace(f"\x00MASK{i}\x00", m)
    return out


def main():
    n = 0
    for p in ROOT.rglob("index.html"):
        parts = p.parts
        if any(x in parts for x in ("private-figures", "assets", ".tools",
                                     "node_modules", "keywords", "guide")):
            continue
        text = p.read_text(encoding="utf-8")
        new = process(text)
        if new != text:
            p.write_text(new, encoding="utf-8")
            n += 1
    print(f"Updated {n} pages")


if __name__ == "__main__":
    main()
