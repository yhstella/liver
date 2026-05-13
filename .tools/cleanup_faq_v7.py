#!/usr/bin/env python3
"""cleanup_faq_v7.py — 잔여 한국·반말 마무리 + 부드러운 톤 보강."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXACT = [
    # 한국 → 국내 (잔여)
    ("한국은 anti-HCV", "국내에서는 anti-HCV"),
    ("한국은 2017년부터", "국내에서는 2017년부터"),
    ("한국 기준 남성", "국내 기준 남성"),
    ("한국·미국·유럽", "국내·미국·유럽"),
    # 반말 → 격식체 (답변 안에서만 매핑)
    ("한두 개는 정상인도 있어요.", "한두 개는 정상인에서도 보일 수 있습니다."),
    ("운동이 오히려 피로를 완화한다는 연구들이 있어요.",
     "운동이 오히려 피로를 완화한다는 연구들이 보고됩니다."),
    ("UDCA 단독으로 시작 후 평가하는 패턴도 있어요.",
     "UDCA 단독으로 시작한 뒤 평가하는 패턴도 있습니다."),
    # 너무 터스한 답변 보강
    ("자연 호전이지 완치 아닙니다. 자가 중단 위험합니다.",
     "자연스러운 호전이지 완치는 아닙니다. 임의로 약을 중단하시면 산후에 반등할 위험이 있어 지속해야 합니다."),
    ("RNA 음성 상태여도 마찬가지.",
     "RNA 음성 상태여도 마찬가지입니다."),
    ("대부분 안전합니다. 10 cm 이상은 산과·외과 평가합니다.",
     "대부분 안전합니다. 10 cm 이상의 큰 혈관종은 산과·외과와 함께 평가합니다."),
    ("5 cm 이상이면 임신 전 절제 권장됩니다. 5 cm 미만은 정기 영상 + 피임약 중단합니다.",
     "5 cm 이상이면 임신 전 절제를 권장합니다. 5 cm 미만은 정기 영상 추적과 함께 피임약을 중단합니다."),
    # 부드러운 안내 — "환자분"
    ("5개 이상 또는 빠르게 늘면 평가합니다.",
     "5개 이상이거나 빠르게 늘어나면 외래에서 평가합니다."),
    ("간·갑상선·임신·류마티스 모두 평가합니다.",
     "간·갑상선·임신 여부·류마티스 등을 함께 평가합니다."),
    # 표기 일관성
    (" 가속화됩니다", "이 가속화됩니다"),
    # 안전망
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
    print(f"v7 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
