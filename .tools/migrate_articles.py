"""Migrate 17 existing articles to new brand:
- New header (Hepatology Note + nav)
- New author-box (photo, no '글쓴이 신현재' formula, no '진료조교수')
- Updated meta byline
- Remove villagebaby leftovers (og:image, BreadcrumbList home)
- Update <title> tail
- Append site-footer
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARTICLE_SLUGS = [
    "간수치-높음", "간수치-종류-차이", "지방간-정밀검사", "알파태아단백",
    "간섬유화스캔-수치", "대사이상지방간-MASLD", "술-안마셔도-지방간",
    "지방간-치료", "지방간-음식", "지방간-간암", "지방간-회복-6개월",
    "B형간염-평생약", "B형간염-검사결과", "B형간염-결혼-임신",
    "가족-B형간염-검사", "C형간염-완치-DAA", "B형간염-간암검진",
]

NEW_HEADER = '''<header class="site-header">
  <div class="inner">
    <a href="/" class="brand-mark">Hepatology<em> Note</em></a>
    <nav class="site-nav">
      <a href="/소개/">소개</a>
      <a href="/논문/">논문</a>
      <a href="/updates/">Updates</a>
    </nav>
  </div>
</header>'''

NEW_FOOTER = '''<footer class="site-footer">
  <div class="inner">
    <div class="col">
      <strong>Hepatology Note</strong>
      <p style="margin:4px 0 0;color:var(--muted);font-size:13px;line-height:1.6">간질환 가이드와 임상 노트 · 서울대학교병원 소화기내과 · 간암센터</p>
    </div>
    <div class="col">
      <strong>안내</strong>
      <a href="/소개/">소개</a>
      <a href="/논문/">논문</a>
      <a href="/updates/">Updates</a>
    </div>
    <div class="col">
      <strong>외부 링크</strong>
      <a href="https://www.snuh.org/blog/83759/philosophy.do" target="_blank" rel="noopener">SNUH 의료진 소개 ↗</a>
    </div>
    <div class="copy" style="grid-column:1/-1">© 2026 drshin.kr</div>
  </div>
</footer>'''

NEW_AUTHOR_BOX = '''<aside class="author-box">
<img class="author-photo" src="/assets/img/author/drshin.jpg" alt="" loading="lazy">
<div class="author-info">
<p><strong>서울대학교병원 소화기내과 · 간암센터</strong></p>
<p class="muted">간암·간경변·만성 간질환 진료. 대한간학회 정회원.</p>
<p><a href="/소개/" class="more">소개 보기 →</a></p>
</div>
</aside>'''

def migrate(slug):
    p = ROOT / slug / "index.html"
    if not p.exists():
        print(f"  SKIP (missing): {slug}")
        return
    h = p.read_text(encoding="utf-8")
    orig_len = len(h)

    # 1) <title> tail: "— 신현재 (서울대병원)" → "— Hepatology Note"
    h = re.sub(
        r'(<title>[^<]*?) — 신현재 \(서울대병원\)</title>',
        r'\1 — Hepatology Note</title>',
        h
    )

    # 2) og:image: villagebaby.kr → author photo
    h = h.replace(
        'https://villagebaby.kr/heroimage.jpg',
        'https://drshin.kr/assets/img/author/drshin.jpg'
    )

    # 3) BreadcrumbList home: villagebaby.kr/ → drshin.kr/
    h = h.replace(
        '"item":"https://villagebaby.kr/"',
        '"item":"https://drshin.kr/"'
    )

    # 4) Replace header (handle both with/without villagebaby span)
    h = re.sub(
        r'<header class="site-header">.*?</header>',
        NEW_HEADER,
        h, count=1, flags=re.S
    )

    # 5) Replace meta byline: "글쓴이 신현재 (서울대병원 소화기내과) · 작성 ..." → "서울대학교병원 소화기내과 · 작성 ..."
    h = re.sub(
        r'<p class="meta">글쓴이 신현재 \(서울대병원 소화기내과\) · 작성',
        r'<p class="meta">서울대학교병원 소화기내과 · 작성',
        h
    )
    # Also handle a simpler variant if any:
    h = re.sub(
        r'<p class="meta">글쓴이 신현재 ',
        r'<p class="meta">서울대학교병원 소화기내과 ',
        h
    )

    # 6) Remove '진료조교수' word everywhere in body content
    h = h.replace('진료조교수', '')
    # Clean up double spaces or stray punctuation introduced
    h = re.sub(r'소화기내과\s+/\s*간암센터', '소화기내과 · 간암센터', h)
    h = re.sub(r'소화기내과\s+/\s+', '소화기내과 · ', h)

    # 7) Replace author-box: full block (greedy until </aside>)
    h = re.sub(
        r'<aside class="author-box">.*?</aside>',
        NEW_AUTHOR_BOX,
        h, count=1, flags=re.S
    )

    # 8) Append site-footer before </body> (if not already present)
    if 'class="site-footer"' not in h:
        h = h.replace('</body>', f'{NEW_FOOTER}\n</body>', 1)

    if h == p.read_text(encoding="utf-8"):
        print(f"  no change: {slug}")
        return

    p.write_text(h, encoding="utf-8")
    print(f"  migrated: {slug} ({orig_len} → {len(h)} bytes)")

print(f"Migrating {len(ARTICLE_SLUGS)} articles...\n")
for s in ARTICLE_SLUGS:
    migrate(s)
print("\nDone.")
