"""Remove byline meta line (작성자·작성시간·검토시간) from all article HTML + builder templates."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# HTML pattern: <p class="meta">서울대학교병원 소화기내과 · 작성 YYYY-MM-DD · 검토 YYYY-MM-DD</p>
PATTERN = re.compile(
    r'<p class="meta">서울대학교병원 소화기내과(?:\s*·\s*간암센터)?\s*·\s*작성[^<]*</p>\s*\n?'
)
# Old format with "신현재" if any remained
PATTERN2 = re.compile(
    r'<p class="meta">[^<]*신현재[^<]*</p>\s*\n?'
)

n = 0
for p in ROOT.rglob("index.html"):
    s = str(p).replace("\\","/")
    if "/.git/" in s or "/.tools/" in s:
        continue
    text = p.read_text(encoding="utf-8")
    orig = text
    text = PATTERN.sub('', text)
    text = PATTERN2.sub('', text)
    if text != orig:
        p.write_text(text, encoding="utf-8")
        n += 1
        rel = p.relative_to(ROOT)
        print(f"  removed byline: {rel}")
print(f"\nTotal: {n} articles updated.")

# Update builder NAV/FOOTER doesn't include byline (it's per-article body)
# Update build_articles.py to not generate byline line
ba = ROOT / ".tools" / "build_articles.py"
ba_text = ba.read_text(encoding="utf-8")
old_meta = '<p class="meta">서울대학교병원 소화기내과 · 작성 {published} · 검토 {published}</p>'
if old_meta in ba_text:
    ba_text = ba_text.replace(old_meta + '\n\n', '')
    ba_text = ba_text.replace(old_meta + '\n', '')
    ba_text = ba_text.replace(old_meta, '')
    ba.write_text(ba_text, encoding="utf-8")
    print("  updated build_articles.py")

bu = ROOT / ".tools" / "build_updates.py"
bu_text = bu.read_text(encoding="utf-8")
if old_meta in bu_text:
    bu_text = bu_text.replace(old_meta + '\n\n', '')
    bu_text = bu_text.replace(old_meta + '\n', '')
    bu_text = bu_text.replace(old_meta, '')
    bu.write_text(bu_text, encoding="utf-8")
    print("  updated build_updates.py")
