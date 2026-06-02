#!/usr/bin/env python3
"""모든 콘텐츠 페이지에 표준 disclaimer 일괄 보강.

카테고리별 텍스트:
  - detail/CC/updates: 일반 의료 정보 disclaimer
  - 케이스: 익명화 + 가이드라인 예시 disclaimer
삽입 위치: </article> 직전 → </main> 직전 fallback. 이미 있으면 skip.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DISC_DETAIL = '<p class="disclaimer">본 콘텐츠는 일반적 의료 정보 제공을 목적으로 하며, 개별 진료를 대체하지 않습니다. 증상이나 검사 결과 해석, 치료 결정은 반드시 진료를 통해 의료진과 상의하시기 바랍니다.</p>'
DISC_CASE = '<p class="disclaimer" style="margin-top:48px">이 사례는 표준 진료 흐름을 보여주기 위해 구성한 교육용 예시이며, 특정 환자의 기록이 아닙니다. 실제 진료는 개인의 상태에 따라 달라집니다.</p>'

HUB_DIRS = {'간암','간경화','B형간염','지방간','간수치','C형간염','자가면역간질환','간양성종양','케이스','CC','updates','keywords','assets','guide','소개','연구','논문','search','.tools','.git','.github','private-figures','node_modules'}


def detail_pages():
    for p in ROOT.iterdir():
        if p.is_dir() and p.name not in HUB_DIRS and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx, 'detail'


def sub_pages(sub: str, kind: str):
    base = ROOT / sub
    if not base.exists():
        return
    for p in base.iterdir():
        if p.is_dir() and not p.name.startswith('.'):
            idx = p / 'index.html'
            if idx.exists():
                yield idx, kind


def inject(text: str, snippet: str) -> tuple[str, bool]:
    if 'class="disclaimer"' in text:
        return text, False
    # Try inserting before </article>
    if '</article>' in text:
        return text.replace('</article>', f'\n{snippet}\n</article>', 1), True
    # Fallback: before </main>
    if '</main>' in text:
        return text.replace('</main>', f'\n{snippet}\n</main>', 1), True
    return text, False


def main():
    hit = 0
    by_kind = {}
    pages = list(detail_pages()) + list(sub_pages('케이스', 'case')) + list(sub_pages('CC', 'cc')) + list(sub_pages('updates', 'update'))
    for f, kind in pages:
        txt = f.read_text(encoding='utf-8')
        snippet = DISC_CASE if kind == 'case' else DISC_DETAIL
        new, changed = inject(txt, snippet)
        if changed:
            f.write_text(new, encoding='utf-8')
            hit += 1
            by_kind[kind] = by_kind.get(kind, 0) + 1
    print(f'Injected disclaimer on {hit} pages')
    for k, v in by_kind.items():
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
