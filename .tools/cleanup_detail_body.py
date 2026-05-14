#!/usr/bin/env python3
"""
cleanup_detail_body.py — 모든 세부페이지 본문(FAQ 외)의 비문·불친절 톤을 일괄 정정.

대상 영역: <article>...</article> 안에서
  - <section class="faq-block"> 제외 (별도 cleanup_faq_*.py로 처리)
  - <section class="references-block"> 제외 (학술 인용)
  - <svg>...</svg> 제외
  - <table>...</table> 제외 (표는 컴팩트 톤 유지)
  - <script>...</script> 제외

처리 패턴:
  1. 명사 종결 비문 → 동사형 (가능. → 가능합니다. 등 60+ 매핑)
  2. 짧은 관련 phrase 정정 (특정 컨텍스트)
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB_SLUGS = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','자가면역간질환','간양성종양',
    'CC','케이스','updates','keywords','assets','guide','소개','연구','논문','search'
}

# 명사 → 동사형 (FAQ cleanup 매핑 + 추가)
NOUN_TO_VERB = {
    "가능": "가능합니다",
    "불가능": "불가능합니다",
    "필요": "필요합니다",
    "불필요": "불필요합니다",
    "권장": "권장됩니다",
    "권고": "권고됩니다",
    "금기": "금기입니다",
    "시작": "시작합니다",
    "중단": "중단합니다",
    "유지": "유지합니다",
    "검토": "검토합니다",
    "고려": "고려합니다",
    "평가": "평가합니다",
    "확인": "확인합니다",
    "시행": "시행합니다",
    "회피": "회피합니다",
    "선호": "선호됩니다",
    "선택": "선택합니다",
    "모니터링": "모니터링합니다",
    "병행": "병행합니다",
    "관찰": "관찰합니다",
    "추적": "추적합니다",
    "충분": "충분합니다",
    "동등": "동등합니다",
    "적용": "적용합니다",
    "준수": "준수합니다",
    "제한": "제한됩니다",
    "적합": "적합합니다",
    "배제": "배제합니다",
    "판단": "판단합니다",
    "결정": "결정합니다",
    "감소": "감소합니다",
    "증가": "증가합니다",
    "호전": "호전됩니다",
    "정상화": "정상화됩니다",
    "발견": "발견됩니다",
    "보고": "보고됩니다",
    "위험": "위험합니다",
    "도움": "도움이 됩니다",
    "의심": "의심합니다",
    "사용": "사용합니다",
    "표준": "표준입니다",
    "안전": "안전합니다",
    "효과적": "효과적입니다",
    "흔함": "흔합니다",
    "드뭄": "드뭅니다",
    "효과": "효과가 있습니다",
    "원인": "원인입니다",
    "필수": "필수입니다",
    "예방": "예방합니다",
    "차이": "차이가 있습니다",
    "패턴": "패턴입니다",
    "옵션": "옵션입니다",
    "신호": "신호입니다",
    "가속": "가속됩니다",
    "악화": "악화될 수 있습니다",
    "재발": "재발할 수 있습니다",
    "감별": "감별합니다",
    "조정": "조정합니다",
    "회복": "회복됩니다",
    "변화": "변화합니다",
    "안정": "안정됩니다",
    "동반": "동반됩니다",
    "포함": "포함됩니다",
    "지속": "지속됩니다",
    "회의": "회의를 합니다",
    "분류": "분류합니다",
    "대응": "대응합니다",
    "전환": "전환합니다",
    "활용": "활용합니다",
    "보충": "보충합니다",
    "유리": "유리합니다",
    "잔존": "잔존합니다",
    "감량": "감량합니다",
    "교정": "교정합니다",
    "협진": "협진합니다",
    "안내": "안내합니다",
    "도입": "도입됩니다",
    "재시작": "재시작합니다",
    "허용": "허용됩니다",
    "불응": "불응합니다",
}

# 정확 phrase 정정 (자주 등장하는 awkward 패턴)
PHRASE_REPLACEMENTS = [
    # "X 가치 있습니다" 류
    (" 가치 있습니다.", " 가치가 있습니다."),
    # 이중 동사 안전망
    ("합니다입니다", "합니다"),
    ("됩니다입니다", "됩니다"),
    ("됩니다됩니다", "됩니다"),
    ("합니다합니다", "합니다"),
    # "한국" → "국내" 또는 제거 (안전한 패턴만)
    ("한국 음주 평가", "국내 음주 평가"),
    ("한국에서는 ", "국내에서는 "),
    ("한국에서 ", "국내에서 "),
    # "강력한 권고/권장됩니다" → "강력하게 권고/권장됩니다"
    ("강력한 권고됩니다", "강력하게 권고됩니다"),
    ("강력한 권장됩니다", "강력하게 권장됩니다"),
    ("적극적 권장됩니다", "적극적으로 권장됩니다"),
    ("적극 권장됩니다", "적극적으로 권장됩니다"),
    ("일반적 권장됩니다", "일반적으로 권장됩니다"),
    # "안 됩니다" 자연화
    (" 권장 안 됩니다", " 권장되지 않습니다"),
    (" 권고 안 됩니다", " 권고되지 않습니다"),
    (" 추천 안 됩니다", " 추천되지 않습니다"),
    # 잘못된 띄어쓰기
    ("  ", " "),
]


def fix_noun_endings(text: str) -> tuple[str, int]:
    """명사 종결 → 동사형."""
    fixes = 0
    for noun, verb in NOUN_TO_VERB.items():
        # 패턴: 앞에 공백·한글이 오고 뒤에 마침표 후 공백/태그 boundary
        rx = re.compile(rf'((?<=[\s가-힣]){re.escape(noun)})\.(?=\s|<)')
        new_text, n = rx.subn(rf'\1{verb[len(noun):]}.', text)
        if n > 0:
            text = new_text
            fixes += n
    return text, fixes


def apply_phrases(text: str) -> tuple[str, int]:
    fixes = 0
    for old, new in PHRASE_REPLACEMENTS:
        if old != new and old in text:
            n = text.count(old)
            text = text.replace(old, new)
            fixes += n
    return text, fixes


# Skip 패턴 — 이 영역들은 건드리지 않음
SKIP_BLOCKS = [
    re.compile(r'<section class="faq-block">.*?</section>', re.DOTALL),
    re.compile(r'<section class="references-block">.*?</section>', re.DOTALL),
    re.compile(r'<svg.*?</svg>', re.DOTALL),
    re.compile(r'<table.*?</table>', re.DOTALL),
    re.compile(r'<script.*?</script>', re.DOTALL),
    re.compile(r'<style.*?</style>', re.DOTALL),
    re.compile(r'<!-- jsonld:auto:start -->.*?<!-- jsonld:auto:end -->', re.DOTALL),
    re.compile(r'<head.*?</head>', re.DOTALL),
]

ARTICLE_RE = re.compile(r'(<article[^>]*>)(.*?)(</article>)', re.DOTALL)


def process_body(body: str) -> tuple[str, int]:
    """body 안에서 skip blocks를 보존하고 나머지에만 cleanup 적용."""
    # Strategy: 모든 skip block을 placeholder로 치환 → cleanup → 복원
    placeholders = []

    def stash(m):
        placeholders.append(m.group(0))
        return f'\x00PLACEHOLDER_{len(placeholders)-1}\x00'

    work = body
    for rx in SKIP_BLOCKS:
        work = rx.sub(stash, work)

    fixes = 0
    work, n = fix_noun_endings(work)
    fixes += n
    work, n = apply_phrases(work)
    fixes += n

    # Restore placeholders
    def restore(m):
        idx = int(m.group(1))
        return placeholders[idx]
    work = re.sub(r'\x00PLACEHOLDER_(\d+)\x00', restore, work)

    return work, fixes


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    m = ARTICLE_RE.search(text)
    if not m:
        return 0
    pre, body, post = m.groups()
    new_body, fixes = process_body(body)
    if fixes > 0:
        new_text = text[:m.start(2)] + new_body + text[m.end(2):]
        path.write_text(new_text, encoding="utf-8")
    return fixes


def main():
    pages_updated = 0
    total_fixes = 0
    for p in sorted(ROOT.glob("*/index.html")):
        if p.parent.name in HUB_SLUGS or p.parent.name.startswith('.'):
            continue
        n = process_file(p)
        if n > 0:
            pages_updated += 1
            total_fixes += n
            print(f"  [{n:3d}] {p.parent.name}")
    print()
    print(f"세부페이지 본문 cleanup: {pages_updated} 페이지, 총 {total_fixes} 건 수정")


if __name__ == "__main__":
    main()
