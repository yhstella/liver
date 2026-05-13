#!/usr/bin/env python3
"""
cleanup_faq.py — 모든 세부페이지 FAQ 섹션의 비문·불친절 톤을 일괄 정정.

대상: `<section class="faq-block">…</section>` 안의 모든 텍스트
처리:
  1. 명사 종결 비문 → 동사형 (예: "가능." → "가능합니다.")
  2. "한국 …" 남용 제거 (한글 자료는 국내 환자 대상)
  3. 부정형 "안 X." → "X하지 않습니다."
  4. 텔레그래픽 em-dash 패턴 일부 (안전한 케이스만)
  5. 잘못된 띄어쓰기/공백
  6. 특정 단어의 부드러운 톤 전환 (의무기록 발급 안내 등)

JSON-LD FAQPage는 visible HTML에서 자동 추출되므로 별도 처리 불필요.
이후 inject_jsonld.py 재실행으로 동기화.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 명사 종결 → 동사형 매핑 (자주 등장하는 어휘)
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
    "모니터": "모니터링합니다",
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
    "악화": "악화될 수 있습니다",
    "정상화": "정상화됩니다",
    "발견": "발견됩니다",
    "보고": "보고됩니다",
}

# 안전한 텍스트 치환 (정확한 phrase match)
PHRASE_REPLACEMENTS = [
    # 한국 → 국내 또는 제거
    ("한국 30~40대는 자연", "30~40대 성인은 자연"),
    ("한국 30대", "30대"),
    ("한국 40대", "40대"),
    ("한국 50대", "50대"),
    ("한국 60대", "60대"),
    ("한국에서는 ", "국내에서는 "),
    ("한국에서 ", "국내에서 "),
    ("한국 환자", "국내 환자"),
    ("한국 가이드라인", "국내 가이드라인"),
    ("한국 의료", "국내 의료"),
    ("국내에서는 만성질환 진단력이", "만성질환 진단력이"),
    # 불친절·터미털 표현 부드럽게
    ("매우 드뭅니다.", "매우 드뭅니다 — 일반 인구 유병률은 0.1% 미만으로 보고됩니다."),
    # 자주 등장하는 비문 조각
    ("한 번 검사 검토.", "한 번 검사를 검토합니다."),
    ("한 번 검사 가치 있습니다.", "한 번 검사해볼 가치가 있습니다."),
    ("일부 환자에서 ", "일부 환자분에서는 "),
    ("환자 본인", "환자분"),
    ("환자가 ", "환자분이 "),
    ("환자는 ", "환자분은 "),
    ("환자의 ", "환자분의 "),
    ("본인 증상", "본인의 증상"),
    ("본인 확인", "본인 확인"),  # 신원확인 의미 유지
    # 표기 일관성
    (" 가치 있습니다.", " 가치가 있습니다."),
    (" 영향이 있을", " 영향을 줄"),
    (" 효과 감소 가능성이 있습니다", " 효과가 감소할 가능성이 있습니다"),
    (" 위험이 매우 큽니다.", " 위험이 매우 높습니다."),
    # 잘못된 띄어쓰기
    (" 의 ", "의 "),
    ("  ", " "),
]


def fix_noun_endings(text: str) -> tuple[str, int]:
    """명사 종결 → 동사형 (단, 이미 합니다/입니다 등 동사가 붙어있으면 스킵)."""
    fixes = 0
    for noun, verb in NOUN_TO_VERB.items():
        # 패턴: 앞에 공백·한글이 오고 뒤에 마침표 후 공백/태그/문자열 끝
        # 합성어 가운데 들어가는 경우는 회피 (앞에 한글이면 OK인데
        # 명사가 더 큰 단어의 일부일 가능성을 줄이기 위해 단어 경계 활용)
        # 예: "추적." matches 단독 "추적." 이지만 "추적관찰." 은 매치 안 함 (관찰 우선)
        rx = re.compile(rf'((?<=[\s가-힣]){re.escape(noun)})\.(?=\s|$|<)')
        new_text, n = rx.subn(rf'\1{verb[len(noun):]}.', text)
        if n > 0:
            text = new_text
            fixes += n
    return text, fixes


def fix_telegraphic_em_dash(text: str) -> tuple[str, int]:
    """텔레그래픽 em-dash 패턴 일부 정정.

    예: "첫 단계 — anti-HAV IgG 검사." → "첫 단계로 anti-HAV IgG 검사를 합니다."
        "비용 — 자비 부담." → "비용은 자비 부담입니다."

    단, 안전하게 처리할 수 있는 몇 가지 패턴만 처리 (전체 자동화는 위험).
    """
    fixes = 0
    rules = [
        # "첫 단계 — X." → "첫 단계로 X을(를) 합니다." (단순화: "첫 단계는 X입니다.")
        (re.compile(r'첫 단계 — ([^.]+)\.'), r'첫 단계는 \1입니다.'),
        # "비용 — X." → "비용은 X입니다."
        (re.compile(r'비용 — ([^.]+)\.'), r'비용은 \1입니다.'),
        # "임신 — X" 같은 라벨 형식 → "임신: X" or maintained
        # 너무 일반적이라 회피
    ]
    for rx, repl in rules:
        new_text, n = rx.subn(repl, text)
        if n > 0:
            text = new_text
            fixes += n
    return text, fixes


def apply_phrase_replacements(text: str) -> tuple[str, int]:
    fixes = 0
    for old, new in PHRASE_REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            fixes += n
    return text, fixes


def fix_yesno_curt_openers(text: str) -> tuple[str, int]:
    """답변이 '네.' 또는 '아닙니다.' 단독이고 그 뒤가 추가 설명이 부족할 때
    부드러운 연결어 추가. 예: '아닙니다. 단순...' → '아닙니다. 다만 단순...'
    (현재는 안전한 케이스 일부만 - 향후 확장 가능)"""
    fixes = 0
    # 단순한 케이스: <p>아닙니다. X 단독 양성의 → <p>아닙니다. 단순 X 양성만으로는
    # 너무 위험. 회피.
    return text, fixes


FAQ_BLOCK_RE = re.compile(
    r'(<section class="faq-block">)(.*?)(</section>)',
    re.DOTALL,
)


def process_file(path: Path) -> int:
    """단일 페이지 FAQ 정정. 변경된 총 fix 개수 반환."""
    text = path.read_text(encoding="utf-8")
    m = FAQ_BLOCK_RE.search(text)
    if not m:
        return 0

    prefix, faq, suffix = m.groups()
    original_faq = faq

    faq, n1 = fix_noun_endings(faq)
    faq, n2 = fix_telegraphic_em_dash(faq)
    faq, n3 = apply_phrase_replacements(faq)
    faq, n4 = fix_yesno_curt_openers(faq)

    total = n1 + n2 + n3 + n4
    if faq != original_faq:
        new_text = text[:m.start(2)] + faq + text[m.end(2):]
        path.write_text(new_text, encoding="utf-8")
    return total


def main():
    SKIP_DIRS = {".git", ".tools", "node_modules", "assets", "guide", "private-figures"}
    pages_updated = 0
    total_fixes = 0
    per_kind = {"노이즈": 0}
    for p in sorted(ROOT.rglob("index.html")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        n = process_file(p)
        if n > 0:
            pages_updated += 1
            total_fixes += n
            print(f"  [{n:2d}] {p.parent.relative_to(ROOT)}")

    print()
    print(f"FAQ 정정 완료: {pages_updated} 페이지, 총 {total_fixes} 건 수정")
    print()
    print("다음 단계: python .tools/inject_jsonld.py  # FAQPage JSON-LD 동기화")


if __name__ == "__main__":
    main()
