#!/usr/bin/env python3
"""cleanup_detail_body_v3.py — 잔여 명사 종결 추가 정정."""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB_SLUGS = {
    '간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간염','자가면역간질환','간양성종양',
    'CC','케이스','updates','keywords','assets','guide','소개','연구','논문','search'
}

NOUN_TO_VERB = {
    "적응증": "적응증입니다",
    "상태": "상태입니다",
    "저하": "저하됩니다",
    "보임": "보입니다",
    "추가": "추가합니다",
    "어려움": "어렵습니다",
    "확진": "확진합니다",
    "복용": "복용합니다",
    "외래": "외래로 와주세요",
    "검진": "검진합니다",
    "병용": "병용합니다",
    "운동": "운동합니다",
    "전이": "전이됩니다",
    "재시작": "재시작합니다",
    "이행": "이행합니다",
    "변환": "변환됩니다",
    "예측": "예측합니다",
    "분리": "분리합니다",
    "표준치": "표준치입니다",
    "수치": "수치입니다",
    "처방": "처방합니다",
    "투여": "투여합니다",
    "효능": "효능이 있습니다",
    "감별점": "감별 포인트입니다",
    "안내": "안내드립니다",
    "확보": "확보합니다",
    "진단": "진단합니다",
    "회수": "회수됩니다",
    "분석": "분석합니다",
    "해석": "해석합니다",
    "보존": "보존합니다",
    "측정": "측정합니다",
    "정의": "정의합니다",
    "비교": "비교합니다",
    "선별": "선별합니다",
    "예방접종": "예방접종을 합니다",
    "권리": "권리입니다",
    "단서": "단서입니다",
    "지표": "지표입니다",
    "근거": "근거입니다",
    "다양": "다양합니다",
    "유효": "유효합니다",
    "동기화": "동기화합니다",
    "정리": "정리합니다",
    "마무리": "마무리합니다",
    "예시": "예시입니다",
    "결과": "결과입니다",
    "특징": "특징입니다",
    "기준": "기준입니다",
    "안전성": "안전성이 보고됩니다",
    "위험성": "위험성이 있습니다",
    "다름": "다릅니다",
    "맞춤": "맞춥니다",
    "회의": "회의합니다",
    "전송": "전송합니다",
    "재투여": "재투여합니다",
    "공통": "공통입니다",
}

# 추가 phrase
PHRASES = [
    # 이중 동사 안전망
    ("합니다입니다", "합니다"),
    ("됩니다입니다", "됩니다"),
    ("입니다입니다", "입니다"),
    ("됩니다됩니다", "됩니다"),
    ("합니다합니다", "합니다"),
    ("입니다 입니다", "입니다"),
    # awkward "환자분이 환자분이"
    ("환자분이 환자분이", "환자분이"),
    ("환자분의 환자분의", "환자분의"),
    # spaces
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
    print(f"v3 cleanup: {pages_updated} pages, {total_fixes} fixes")


if __name__ == "__main__":
    main()
