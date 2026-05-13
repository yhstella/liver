#!/usr/bin/env python3
"""cleanup_faq_v5.py — 최종 비문 종결 마무리."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXACT = [
    # 결정적
    ("MRI(특히 MRCP)로 평가가 결정적.",
     "MRI(특히 MRCP)로 평가하는 것이 결정적입니다."),
    ("이 결정적.", "이 결정적입니다."),
    ("로 평가가 결정적.", "로 평가하는 것이 결정적입니다."),
    # 외래/응급실 — 리스트 끝 telegraphic
    ("시 즉시 외래.", "시 즉시 외래로 와주세요."),
    ("황달·피로·식욕 부진 시 즉시 외래.", "황달·피로·식욕 부진이 보이면 즉시 외래로 와주세요."),
    # 수집
    ("자료 수집.", "자료를 수집합니다."),
    ("통계·역학 자료 수집.", "통계·역학 자료를 수집하는 것입니다."),
    # 미승인
    ("국내 미승인.", "국내 미승인 상태입니다."),
    # 신호
    ("의 첫 신호.", "이/가 첫 신호입니다."),
    # 의심 (잔여)
    ("로 의심.", "을 의심합니다."),
    ("를 의심.", "를 의심합니다."),
    # 우선
    (" 처치 우선.", " 처치를 우선합니다."),
    ("이 우선.", "이 우선입니다."),
    # 응급실
    ("즉시 응급실.", "즉시 응급실로 가주세요."),
    # 떨어뜨림
    ("떨어뜨림.", "떨어뜨립니다."),
    # 원칙/옵션
    ("는 원칙.", "는 원칙입니다."),
    ("이 옵션.", "이 옵션입니다."),
    ("도 옵션.", "도 한 옵션입니다."),
    # 상승
    ("의 상승.", "이/가 상승합니다."),
    # 회복
    ("이 회복.", "이 회복됩니다."),
    # 조정
    ("의 조정.", "의 조정이 필요합니다."),
    # 정상
    ("이 정상.", "이 정상화됩니다."),
    # 기본/정도/차이
    ("이 기본.", "이 기본 원칙입니다."),
    (" 정도.", " 정도입니다."),
    # 안전 잔여
    (" 안전.", " 안전합니다."),
    # 상의
    (" 상의.", " 상의해주세요."),
    # 관리 잔여
    (" 관리.", " 관리합니다."),
    # 다름/사유/신중
    (" 다름.", " 다릅니다."),
    (" 사유.", " 사유입니다."),
    (" 신중.", " 신중하게 결정합니다."),
    # 대사증후군
    ("대사증후군.", "대사증후군으로 보는 경우가 많습니다."),
    # 안전망 — 이중 verb cleanup
]

REGEX = [
    (re.compile(r'(합니다|됩니다|입니다)입니다\b'), r'\1'),
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
    print(f"v5 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
