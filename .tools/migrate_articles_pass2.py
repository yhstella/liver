"""Pass 2 cleanup: og:site_name, crumb second link to series hub, BreadcrumbList."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARTICLE_TO_SERIES = {
    "간수치-높음": ("간수치", "간수치 이상"),
    "간수치-종류-차이": ("간수치", "간수치 이상"),
    "간섬유화스캔-수치": ("간수치", "간수치 이상"),
    "지방간-정밀검사": ("지방간", "지방간"),
    "대사이상지방간-MASLD": ("지방간", "지방간"),
    "술-안마셔도-지방간": ("지방간", "지방간"),
    "지방간-치료": ("지방간", "지방간"),
    "지방간-음식": ("지방간", "지방간"),
    "지방간-회복-6개월": ("지방간", "지방간"),
    "알파태아단백": ("간암", "간암"),
    "지방간-간암": ("간암", "간암"),
    "B형간염-간암검진": ("간암", "간암"),
    "B형간염-평생약": ("B형간염", "B형 간염"),
    "B형간염-검사결과": ("B형간염", "B형 간염"),
    "B형간염-결혼-임신": ("B형간염", "B형 간염"),
    "가족-B형간염-검사": ("B형간염", "B형 간염"),
    "C형간염-완치-DAA": ("B형간염", "B형 간염"),
}

def cleanup(slug):
    p = ROOT / slug / "index.html"
    if not p.exists():
        return
    h = p.read_text(encoding="utf-8")
    orig = h

    series_slug, series_display = ARTICLE_TO_SERIES[slug]

    # 1) og:site_name → "Hepatology Note"
    h = re.sub(
        r'<meta property="og:site_name" content="[^"]*"',
        '<meta property="og:site_name" content="Hepatology Note"',
        h
    )

    # 2) crumb: replace second link "간 건강 가이드" with series hub link
    h = re.sub(
        r'<nav class="crumb"><a href="/">홈</a> › <a href="/">간 건강 가이드</a> › ',
        f'<nav class="crumb"><a href="/">홈</a> › <a href="/{series_slug}/">{series_display}</a> › ',
        h
    )
    # And the simpler variant if any:
    h = re.sub(
        r'<nav class="crumb"><a href="/">홈</a> › <span>간 건강 가이드</span>',
        f'<nav class="crumb"><a href="/">홈</a> › <a href="/{series_slug}/">{series_display}</a>',
        h
    )

    # 3) JSON-LD BreadcrumbList: change second item "간 건강 가이드" → series hub
    h = re.sub(
        r'\{"@type":"ListItem","position":2,"name":"간 건강 가이드","item":"https://drshin.kr/"\}',
        f'{{"@type":"ListItem","position":2,"name":"{series_display}","item":"https://drshin.kr/{series_slug}/"}}',
        h
    )

    if h != orig:
        p.write_text(h, encoding="utf-8")
        print(f"  cleaned: {slug}")
    else:
        print(f"  no change: {slug}")

print("Pass 2 cleanup...\n")
for slug in ARTICLE_TO_SERIES:
    cleanup(slug)
print("\nDone.")
