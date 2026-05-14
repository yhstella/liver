#!/usr/bin/env python3
"""cleanup_detail_body_v2.py — 본문 잔여 비문 정정 (v1 후속)."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB_SLUGS = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','자가면역간질환','간양성종양',
    'CC','케이스','updates','keywords','assets','guide','소개','연구','논문','search'
}

NOUN_TO_VERB = {
    "경우": "경우입니다",
    "진행": "진행합니다",
    "검사": "검사합니다",
    "상승": "상승합니다",
    "일부": "일부입니다",
    "아님": "아닙니다",
    "우선": "우선합니다",
    "위주": "위주로 드세요",
    "신중": "신중하게 결정합니다",
    "점검": "점검합니다",
    "치료": "치료합니다",
    "원칙": "원칙입니다",
    "옵션": "한 옵션입니다",
    "기본": "기본입니다",
    "필수": "필수입니다",
    "유리": "유리합니다",
    "가능성": "가능성이 있습니다",
    "주의": "주의해야 합니다",
    "회복": "회복됩니다",
    "동일": "동일합니다",
    "유사": "유사합니다",
    "변화": "변할 수 있습니다",
    "대응": "대응합니다",
    "활용": "활용합니다",
    "참여": "참여합니다",
    "준비": "준비합니다",
    "참고": "참고해주세요",
    "교정": "교정합니다",
    "보충": "보충합니다",
    "조정": "조정합니다",
    "관리": "관리합니다",
    "이상": "이상입니다",
    "음성": "음성입니다",
    "양성": "양성입니다",
    "정상": "정상입니다",
    "분류": "분류합니다",
    "다양": "다양합니다",
}

# Specific phrases (안전한 정정)
PHRASES = [
    # 이중 동사 안전망
    ("합니다입니다", "합니다"),
    ("됩니다입니다", "됩니다"),
    ("입니다입니다", "입니다"),
    # 자주 등장
    (" 가치 있습니다.", " 가치가 있습니다."),
    # 콤마 + 명사 종결
    (",  ,", ","),
    ("  ", " "),
]

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


def fix_noun_endings(text: str) -> tuple[str, int]:
    fixes = 0
    for noun, verb in NOUN_TO_VERB.items():
        rx = re.compile(rf'((?<=[\s가-힣]){re.escape(noun)})\.(?=\s|<)')
        new_text, n = rx.subn(rf'\1{verb[len(noun):]}.', text)
        if n > 0:
            text = new_text
            fixes += n
    return text, fixes


def apply_phrases(text: str) -> tuple[str, int]:
    fixes = 0
    for old, new in PHRASES:
        if old != new and old in text:
            n = text.count(old)
            text = text.replace(old, new)
            fixes += n
    return text, fixes


def process_body(body: str) -> tuple[str, int]:
    placeholders = []
    def stash(m):
        placeholders.append(m.group(0))
        return f'\x00P_{len(placeholders)-1}\x00'
    work = body
    for rx in SKIP_BLOCKS:
        work = rx.sub(stash, work)
    fixes = 0
    work, n = fix_noun_endings(work); fixes += n
    work, n = apply_phrases(work); fixes += n
    def restore(m):
        return placeholders[int(m.group(1))]
    work = re.sub(r'\x00P_(\d+)\x00', restore, work)
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
    print(f"v2 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
