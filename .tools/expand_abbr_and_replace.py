"""For each page: expand English abbreviation on first occurrence with Korean expansion.
Also: 고주파소작 → 고주파열치료술 globally."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ABBR = {
    # Liver disease / staging
    'BCLC': 'Barcelona Clinic Liver Cancer',
    'HCC': '간세포암',
    'TACE': '경동맥화학색전술',
    'TARE': '방사선색전술',
    'SBRT': '체부 정위 방사선치료',
    'RFA': '고주파열치료술',
    'BRTO': '역행성 정맥류 폐쇄술',
    'TIPS': '경경정맥 간내 문맥전신 단락술',
    'LDLT': '살아있는 기증자 간이식',
    'KONOS': '한국 장기이식관리센터',
    # Fatty liver
    'MASLD': '대사이상 지방간질환',
    'MASH': '대사이상 지방간염',
    'NAFLD': '비알코올성 지방간질환',
    'NASH': '비알코올성 지방간염',
    # Hepatitis virus
    'HBV': 'B형간염 바이러스',
    'HCV': 'C형간염 바이러스',
    'HBsAg': 'B형간염 표면항원',
    'HBeAg': 'B형간염 e항원',
    'HBIG': 'B형간염 면역글로불린',
    'TDF': '테노포비르 디소프록실',
    'TAF': '테노포비르 알라페나미드',
    'ETV': '엔테카비르',
    'DAA': '직접 작용 항바이러스제',
    'SVR': '지속 바이러스 반응',
    # Tumor markers
    'AFP': '알파태아단백',
    'PIVKA-II': 'des-γ-carboxy prothrombin',
    # Scoring & metrics
    'MELD': 'Model for End-stage Liver Disease',
    'INR': 'International Normalized Ratio',
    'ALBI': 'albumin-bilirubin',
    'BMI': '체질량지수',
    'HbA1c': '당화혈색소',
    'FIB-4': 'Fibrosis-4',
    'CSPH': '임상적 의미 있는 문맥압항진',
    'HVPG': '간정맥압 차',
    # Liver enzymes / labs
    'ALT': '알라닌 아미노전이효소',
    'AST': '아스파르테이트 아미노전이효소',
    'GGT': '감마-글루타밀전이효소',
    'ALP': '알칼리성 인산분해효소',
    'PT': '프로트롬빈 시간',
    'CK': '크레아틴 키나아제',
    'LDH': '젖산탈수소효소',
    # Imaging
    'CT': '컴퓨터 단층촬영',
    'MRI': '자기공명 영상',
    'MRE': '자기공명 탄성영상',
    'CAP': 'controlled attenuation parameter',
    # Complications
    'SBP': '자발성 세균성 복막염',
    'HRS': '간신증후군',
    'AKI': '급성 신손상',
    'ICP': '임신성 간내 담즙 정체',
    # Liver disease entities
    'PBC': '원발성 담즙성 담관염',
    'PSC': '원발성 경화성 담관염',
    'DILI': '약물성 간 손상',
    # Alcohol
    'ALD': '알코올성 간 질환',
    'AUD': '알코올 사용 장애',
    'PEth': 'phosphatidylethanol',
    # Diabetes / metabolic
    'SGLT2': '나트륨-포도당 공동수송체-2',
    'GLP-1': '글루카곤 유사 펩타이드-1',
    # Drug classes / safety
    'NSAIDs': '비스테로이드성 항염제',
    'DOAC': '직접 경구 항응고제',
    'BCAA': '가지사슬 아미노산',
    # Cancer immunology
    'PD-L1': 'programmed death-ligand 1',
    'CTLA-4': 'cytotoxic T-lymphocyte-associated protein 4',
    'TKI': '티로신 키나아제 억제제',
    'VEGF': '혈관내피성장인자',
    'CIK': 'cytokine-induced killer cell',
    # General medical
    'ECOG': 'Eastern Cooperative Oncology Group',
    'COPD': '만성 폐쇄성 폐질환',
    'ICU': '중환자실',
    'AMA': '항미토콘드리아 항체',
    'ANCA': '항호중구 세포질 항체',
    # Societies
    'KASL': '대한간학회',
    'KLCA': '대한간암학회',
    'AASLD': '미국간질환학회',
    'EASL': '유럽간질환학회',
    'AGA': '미국소화기학회',
    'ASCO': '미국임상종양학회',
    'IDSA': '미국감염학회',
}

ABBR_KEYS = sorted(ABBR.keys(), key=len, reverse=True)

def mask_blocks(text):
    """Mask out script, style, references-block, title, and code spans."""
    blocks = []
    def replace_block(m):
        idx = len(blocks)
        blocks.append(m.group(0))
        return f'\x00BLK{idx}\x00'
    masked = text
    masked = re.sub(r'<script\b[^>]*>.*?</script>', replace_block, masked, flags=re.S)
    masked = re.sub(r'<style\b[^>]*>.*?</style>', replace_block, masked, flags=re.S)
    masked = re.sub(r'<section class="references-block">.*?</section>', replace_block, masked, flags=re.S)
    masked = re.sub(r'<title[^>]*>.*?</title>', replace_block, masked, flags=re.S)
    masked = re.sub(r'<code[^>]*>.*?</code>', replace_block, masked, flags=re.S)
    return masked, blocks

def restore(text, blocks):
    for i, b in enumerate(blocks):
        text = text.replace(f'\x00BLK{i}\x00', b)
    return text

def expand(html):
    # First: 고주파소작 → 고주파열치료술
    html = html.replace('고주파소작술', '고주파열치료술')
    html = html.replace('고주파소작', '고주파열치료술')

    # Then: per-page first-occurrence abbreviation expansion
    masked, blocks = mask_blocks(html)
    parts = re.split(r'(<[^>]*>|\x00BLK\d+\x00)', masked)
    seen = set()
    for i, part in enumerate(parts):
        if not part:
            continue
        if part.startswith('<') or part.startswith('\x00'):
            continue
        # This is text content
        for abbr in ABBR_KEYS:
            if abbr in seen:
                continue
            # Match: not preceded by alphanumeric, not followed by alphanumeric, not followed by '('
            pattern = re.compile(r'(?<![A-Za-z0-9])' + re.escape(abbr) + r'(?![A-Za-z0-9])(?!\s*\()')
            m = pattern.search(part)
            if m:
                exp = ABBR[abbr]
                part = part[:m.start()] + abbr + '(' + exp + ')' + part[m.end():]
                parts[i] = part
                seen.add(abbr)
    result = ''.join(parts)
    return restore(result, blocks)

# Process all article HTML files
n_changed = 0
n_total = 0
for p in ROOT.rglob('index.html'):
    s = str(p).replace('\\', '/')
    if '/.git/' in s or '/.tools/' in s:
        continue
    n_total += 1
    text = p.read_text(encoding='utf-8')
    new_text = expand(text)
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        n_changed += 1

print(f'Article HTML: {n_changed}/{n_total} files updated')

# Also update builder source files for the 고주파 replacement so future builds stay consistent
for fname in ['build_articles.py', 'build_s01.py', 'build_s03_s04.py', 'build_s05.py',
              'build_updates.py', 'build_updates_more.py', 'build_series_hubs.py',
              'build_research.py', 'add_legacy_svgs.py']:
    p = ROOT / '.tools' / fname
    if not p.exists():
        continue
    text = p.read_text(encoding='utf-8')
    new_text = text.replace('고주파소작술', '고주파열치료술').replace('고주파소작', '고주파열치료술')
    if new_text != text:
        p.write_text(new_text, encoding='utf-8')
        print(f'  updated builder: .tools/{fname}')

print('Done.')
