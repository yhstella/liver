#!/usr/bin/env python3
"""
cleanup_faq_v3.py — FAQ 톤·문법 정정 3차 (잔여 비문 처리).

처리:
  - 위험·도움·의심·관리 등 추가 명사 종결 → 자연스러운 동사형
  - 컨텍스트별 specific phrase 정정
  - 부드러운 안내 톤 보강
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 구체적인 phrase 단위 정정 (자연스러운 한국어로)
EXACT = [
    # 위험. → 위험합니다.
    ("일부에서는 알코올성 간 손상이 가산되어 위험.",
     "일부에서는 알코올성 간 손상이 가산되어 위험합니다."),
    ("이뇨제 사용은 신기능·전해질 이상 위험.",
     "이뇨제 사용은 신기능·전해질 이상의 위험이 있습니다."),
    ("의 위험.", "의 위험이 있습니다."),  # generic
    # 도움.
    ("어려운 케이스에서 도움.", "어려운 케이스에서 도움이 됩니다."),
    ("것이 도움.", "것이 도움이 됩니다."),
    ("도움 받을 수 있습니다", "도움을 받으실 수 있습니다"),
    # 의심.
    ("ICP 의심.", "ICP를 의심합니다."),
    ("강하게 알코올 의심.", "강하게 알코올 원인을 의심합니다."),
    ("ICP 의심 — ", "ICP를 의심합니다 — "),
    # 관리.
    ("같은 피부 관리.", "같은 피부 관리도 함께 합니다."),
    ("피부 관리.", "피부 관리도 함께 합니다."),
    # 검사.
    (" 검사 가치.", " 검사를 해볼 가치가 있습니다."),
    # 안정. (drug 안정 의미)
    ("의 안정.", "의 안정이 우선입니다."),
    # 예방.
    ("성공한 예방.", "성공한 예방입니다."),
    # 재발.
    ("의 재발.", "이/가 재발할 수 있습니다."),
    # 자주 보이는 부자연 패턴
    ("권장 안 됩니다.", "권장되지 않습니다."),
    ("필요 없습니다.", "필요하지 않습니다."),
    ("주의가 필요합니다 —", "다음 사항에 주의해주세요 —"),
    # 명사 종결 "보유" 등
    ("평생 면역 보유, 추가 조치 불필요합니다.",
     "한 번 감염 후에는 평생 면역이 형성되어 추가 조치가 필요 없습니다."),
    ("평생 면역 보유", "평생 면역이 형성됩니다"),
    # "신고가 의무입니다" (이미 자연)
    # 톤 부드러움
    ("환자분이 직접 할 일은 없으며", "환자분이 직접 하실 일은 없으며"),
    ("진료의가 처리합니다", "진료의가 처리해드립니다"),
    # 자주 등장하는 nominal list pattern
    # ", X 가능," → ", X이/가 가능하며,"  (너무 컨텍스트 다양해 회피)
]

# 정규식 기반 fallback (구체적 phrase에 매치되지 않은 잔여)
REGEX = [
    # 안내 톤
    (re.compile(r'권고됩니다\.(\s|$)'), r'권고됩니다.\1'),
    # 단순 noun 종결 잔여 — 매우 일반적인 안전한 변환
    (re.compile(r'(?<=[\s가-힣])(필수)\.(?=\s|$|<)'), r'\1입니다.'),
    (re.compile(r'(?<=[\s가-힣])(주의)\.(?=\s|$|<)'), r'\1해야 합니다.'),
    # "X 안 됩니다" 가독성
    (re.compile(r'권장 안 됩니다'), '권장되지 않습니다'),
    # 마침표 두 번 등 공백 정리
    (re.compile(r'\.\.'), '.'),
    (re.compile(r'\.,'), '.'),
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
    print(f"v3 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
