#!/usr/bin/env python3
"""cleanup_faq_v6.py — 잔여 FAQ 비문 final cleanup."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXACT = [
    # 1차 옵션 — list context
    ("글레카프레비르/피브렌타스비르가 1차 옵션.",
     "글레카프레비르/피브렌타스비르가 1차 옵션입니다."),
    # 기본 검사 set
    ("초음파가 기본.", "초음파가 기본 set입니다."),
    # 차이
    ("조직학적 구조 차이.", "조직학적 구조에 차이가 있습니다."),
    # 활용
    (" 도구 활용.", " 같은 도구를 활용합니다."),
    # 계획
    ("으로 전환 후 임신 계획.",
     "으로 전환하신 뒤 임신을 계획해주세요."),
    # 감량
    (" 후 점진적 감량.", " 후 점진적으로 감량합니다."),
    # 재발 (list 마지막 항목)
    ("진짜 AIH 재발.", "진짜 AIH 재발일 가능성도 검토합니다."),
    # 가속
    ("간 손상 가속.", "간 손상이 가속될 수 있습니다."),
    # 시간 — 회식 안내
    ("회식 후 보충 회복 시간.",
     "회식 후에는 충분한 회복 시간을 두는 것이 좋습니다."),
    # 아님 — verb ending
    ("단독 진단 아님.", "단독 진단의 근거는 아닙니다."),
    # 추가 nouns
    (" 신호.", " 신호입니다."),
    (" 의심.", " 의심합니다."),
    (" 우선.", " 우선합니다."),
    (" 원칙.", " 원칙입니다."),
    (" 상승.", " 상승할 수 있습니다."),
    (" 회복.", " 회복됩니다."),
    (" 조정.", " 조정합니다."),
    (" 정상.", " 정상입니다."),
    (" 결정적.", " 결정적입니다."),
    (" 기본.", " 기본 원칙입니다."),
    (" 대응.", " 대응합니다."),
    (" 문제.", " 문제가 됩니다."),
    (" 유리.", " 유리합니다."),
    (" 잔존.", " 잔존합니다."),
    (" 예방.", " 예방합니다."),
    (" 위험.", " 위험합니다."),
    (" 도움.", " 도움이 됩니다."),
    (" 감량.", " 감량합니다."),
    (" 영향.", " 영향이 있습니다."),
    (" 함께.", " 함께 합니다."),
    # Safety
]

REGEX = [
    (re.compile(r'(합니다|됩니다|입니다)입니다\b'), r'\1'),
    (re.compile(r'합니다입니다'), '합니다'),
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
    print(f"v6 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
