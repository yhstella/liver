#!/usr/bin/env python3
"""
cleanup_faq_v4.py — FAQ 잔여 비문 정정 4차.

처리:
  - "안전.", "표준.", "효과적.", "있음.", "상의." 등 잔여 명사·형용사 종결
  - "한국 표준" → "국내 표준" 또는 그냥 "표준"
  - 그 외 컨텍스트별 다듬기
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXACT = [
    # "안전." → "안전합니다." (위험성 안내 톤 유지)
    ("외래·응급실 평가가 안전.", "외래나 응급실 평가를 받으시는 게 안전합니다."),
    ("위생적 성접촉이 안전.", "위생적인 성접촉이 안전합니다."),
    ("줄이는 것이 안전.", "줄이시는 것이 안전합니다."),
    # "표준." → "표준입니다."
    ("한국 표준.", "국내 표준입니다."),
    ("이 한국 표준", "이 국내 표준"),
    ("면역억제 추가가 표준.", "면역억제 추가가 표준입니다."),
    ("maintenance가 표준.", "유지 치료가 표준입니다."),
    ("이 표준.", "이 표준입니다."),
    ("가 표준.", "가 표준입니다."),
    # "상의."
    ("진료의와 상의.", "진료의와 상의해주세요."),
    # "효과적."
    ("만성화 예방에 효과적.", "만성화 예방에 효과적입니다."),
    ("에 효과적.", "에 효과적입니다."),
    ("이 효과적.", "이 효과적입니다."),
    # "있음."
    ("ART 조정이 필요할 수 있음.", "ART 조정이 필요할 수 있습니다."),
    ("수 있음.", "수 있습니다."),
    ("우려가 있음.", "우려가 있습니다."),
    ("가능성이 있음.", "가능성이 있습니다."),
    ("위험이 있음.", "위험이 있습니다."),
    # "가능성."
    (" 가능성.", "가능성이 있습니다."),
    # "신호.", "원칙.", "옵션." 등
    ("첫 신호.", "첫 신호입니다."),
    ("주된 원칙.", "주된 원칙입니다."),
    ("일반적인 옵션.", "일반적인 옵션입니다."),
    ("표준 옵션.", "표준 옵션입니다."),
    # "감별.", "조정.", "회복.", "정상." 등
    ("로 감별.", "로 감별합니다."),
    ("필요 감별.", "필요한 감별이 있습니다."),
    ("필요한 조정.", "필요한 조정을 합니다."),
    ("후 회복.", "후 회복됩니다."),
    ("재 정상.", "재 정상화됩니다."),
    # "차이.", "정도.", "수준.", "기본."
    ("의 차이.", "의 차이가 있습니다."),
    ("의 정도.", "의 정도입니다."),
    ("수준.", "수준입니다."),
    ("의 기본.", "의 기본 원칙입니다."),
    # "미만.", "미승인."
    ("0.1% 미만.", "0.1% 미만으로 알려져 있습니다."),
    ("국내 미승인.", "국내 미승인 상태입니다."),
    ("한국 미승인", "국내 미승인"),
    # "상승." 컨텍스트
    (" ALT 상승.", " ALT 상승이 있습니다."),
    # 잔여 "안정.", "검사." 같은 단순 verb-able
    (" 안정.", " 안정 상태입니다."),
    (" 검사.", " 검사를 시행합니다."),
    # 부드러운 안내
    ("환자분이 환자분이", "환자분이"),
    ("환자분의 환자분의", "환자분의"),
    # "한국" 잔여
    ("한국 미만으로", "국내 미만으로"),
    ("한국 표준", "국내 표준"),
    # 부정문 자연화
    (" 권고 안 됩니다", " 권고되지 않습니다"),
    (" 추천 안 됩니다", " 추천되지 않습니다"),
    # "X에서 — Y" 같은 텔레그래픽 일부
]

REGEX = [
    # "있음." → "있습니다." (단독 패턴)
    (re.compile(r'(?<=[\s가-힣])있음\.(?=\s|$|<)'), '있습니다.'),
    # "수 있음." 정리
    (re.compile(r'수\s*있음\.(?=\s|$|<)'), '수 있습니다.'),
    # 이중 동사 안전망
    (re.compile(r'(합니다|됩니다|입니다)입니다\b'), r'\1'),
    # "X합니다 X합니다" 같은 중복 문장 (가끔 발생)
    # (회피 — 컨텍스트 의존)
    # 중복 공백 정리
    (re.compile(r'  +'), ' '),
]

FAQ_BLOCK_RE = re.compile(
    r'(<section class="faq-block">)(.*?)(</section>)',
    re.DOTALL,
)


def process(text: str) -> tuple[str, int]:
    fixes = 0
    for old, new in EXACT:
        if old != new and old in text:
            n = text.count(old)
            text = text.replace(old, new)
            fixes += n
    for rx, repl in REGEX:
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
    print(f"v4 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
