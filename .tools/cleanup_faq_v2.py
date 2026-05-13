#!/usr/bin/env python3
"""
cleanup_faq_v2.py — FAQ v1 후속 정정.

v1에서 발생한 부작용 및 추가로 발견된 비문 패턴 처리:
  1. 이중 동사 (X합니다입니다 → X합니다)
  2. "더 강력한 권고됩니다" 류 형용사+동사 모순
  3. 부자연스러운 nominalization 일부 reword
  4. (1) (2) (3) 같은 list가 답변에 평문으로 끼어 있어 가독성 나쁜 케이스
  5. "한 번 X" 의 X가 동사인 경우 → "한 번은 X해보시는" 등
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 정확한 phrase 치환 (FAQ 블록 안에서만)
EXACT_REPLACEMENTS = [
    # 이중 동사 cleanup
    ("합니다입니다", "합니다"),
    ("됩니다입니다", "됩니다"),
    ("입니다입니다", "입니다"),
    ("합니다.입니다", "합니다."),
    # v1에서 부자연스럽게 변환된 케이스
    ("더 강력한 권고됩니다.", "더 강력하게 권고됩니다."),
    ("강력한 권고됩니다", "강력하게 권고됩니다"),
    ("적극적 권장됩니다", "적극적으로 권장됩니다"),
    ("적극적인 권장됩니다", "적극적으로 권장됩니다"),
    ("적극 권장됩니다", "적극적으로 권장됩니다"),
    ("일반적 권장됩니다", "일반적으로 권장됩니다"),
    ("강제 권장됩니다", "강제로 권장됩니다"),
    # 동사형 끝맺음이 더 자연스러운 경우
    ("권고됩니다.", "권고됩니다."),  # 정합성 유지용 (no-op)
    # 자주 등장하던 비문 잔여
    ("간 손상을 일으키고,", "간 손상을 일으키고"),
    ("DAA의 약물 대사에 영향을 줄 가능성이 있습니다.", "DAA의 약물 대사에 영향을 줄 가능성이 있습니다."),
    # "X 가치 있습니다" 류 (수치 명사) → "X해볼 가치가 있습니다"
    ("검사 가치", "검사 가치"),  # noop, 이미 변환됨
    # 부드러운 표현
    ("환자 식기·화장실 분리", "환자분의 식기·화장실 분리"),
    ("환자 식기", "환자분의 식기"),
    ("환자 동의 없이는", "환자분의 동의 없이는"),
    ("환자분이 동의 없이는", "환자분의 동의 없이는"),
    # 명사 단독 답변 → 부드러운 안내
    ("매우 드뭅니다. 일반 인구 유병률 0.1% 미만.",
     "매우 드뭅니다. 일반 인구 유병률은 0.1% 미만으로 보고됩니다."),
    ("이상적이며", "이상적이며,"),
    # 부정형 verb noun
    (" 가치 있습니다.", " 가치가 있습니다."),
    # 잘못된 의문문 단정 보강
    (" 영향이 있을 수 있습니다.", " 영향을 줄 수 있습니다."),
    # 잘못된 띄어쓰기·중복 띄어쓰기
    ("환자분 환자분", "환자분"),
    ("환자분이 환자분이", "환자분이"),
    ("일부 환자분에서는 일부 환자분에서는", "일부 환자분에서는"),
    # 위 v1에서 잘못 만든 패턴
    ("일부 환자분에서 ", "일부 환자분에서는 "),
    # 안내문 부드러움
    (" 가능. ", " 가능합니다. "),  # 잔여 사례
    # 너무 짧은 yes/no 답변 보강은 별도 처리
]

# 정규식 기반 정정
REGEX_FIXES = [
    # 명사 + 명사 + 입니다 (예: "권고됩니다입니다") — 이미 위에서 처리되지만 안전망
    (re.compile(r'(됩니다|합니다|입니다)입니다\b'), r'\1'),
    # "X.Y" — 한글 사이에 마침표 후 공백 없음 (가독성)
    (re.compile(r'([가-힣])\.([가-힣])'), r'\1. \2'),
    # 중복 공백
    (re.compile(r'  +'), ' '),
    # ", ," 잔여
    (re.compile(r',\s*,'), ','),
    # 단어 안에 ". "가 들어가서 깨진 경우는 회피 (위 fix만)
]


FAQ_BLOCK_RE = re.compile(
    r'(<section class="faq-block">)(.*?)(</section>)',
    re.DOTALL,
)


def process(text: str) -> tuple[str, int]:
    fixes = 0
    for old, new in EXACT_REPLACEMENTS:
        if old != new and old in text:
            n = text.count(old)
            text = text.replace(old, new)
            fixes += n
    for rx, repl in REGEX_FIXES:
        new_text, n = rx.subn(repl, text)
        if n > 0:
            text = new_text
            fixes += n
    return text, fixes


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    m = FAQ_BLOCK_RE.search(text)
    if not m:
        return 0
    prefix, faq, suffix = m.groups()
    original = faq
    faq, fixes = process(faq)
    if faq != original:
        new_text = text[:m.start(2)] + faq + text[m.end(2):]
        path.write_text(new_text, encoding="utf-8")
        return fixes
    return 0


def main():
    SKIP_DIRS = {".git", ".tools", "node_modules", "assets", "guide", "private-figures"}
    pages_updated = 0
    total_fixes = 0
    for p in sorted(ROOT.rglob("index.html")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        n = process_file(p)
        if n > 0:
            pages_updated += 1
            total_fixes += n
            print(f"  [{n:2d}] {p.parent.relative_to(ROOT)}")
    print()
    print(f"v2 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
