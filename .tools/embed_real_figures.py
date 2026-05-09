"""Embed REAL figures (not placeholder SVG study cards) from
private-figures/by-page/{slug}/ into the corresponding website pages,
distributed inline between content sections.

A figure file is treated as "real" if:
  - extension is .png, .jpg, .jpeg, .gif, .webp (raster images), OR
  - it's an .svg whose first ~200 chars do NOT contain the placeholder marker
    "drshin.kr study figure" (which means it's a real illustration, e.g.
    detailed anatomy SVG or PubChem chemical structure).

Placeholder SVG study cards (the small ~2KB schematic cards that all look
similar across pages) are excluded.

Inline placement: distributed between top-level <h2> sections of the article
body, never bunched at the end. Idempotent via <!-- realfig --> markers.
"""
from __future__ import annotations
import html as htmllib
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
PRIV = ROOT / "private-figures" / "by-page"
ASSETS = ROOT / "assets" / "img" / "figures"

OPEN = "<!-- realfig -->"
CLOSE = "<!-- /realfig -->"
BLOCK_RE = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.DOTALL)

# Pages whose figures we want to skip (handled by paper-figures pipeline)
PAPER_FIG_PAGES = {
    "updates/Shin-CIK-HCC-CII-2026",
    "updates/Shin-HBeAg-seroclearance-HCC-JHepR-2024",
    "updates/Shin-HCC-Guidelines-Review-JLC-2025",
    "updates/Ahn-Aspirin-HCC-MASLD-CMH-2026",
    "updates/Shin-COVID-HBV-NK-IN-2023",
}

PLACEHOLDER_SIG = "drshin.kr study figure"


def esc(s: str) -> str:
    return htmllib.escape(s or "")


def is_real_figure(path: Path) -> bool:
    ext = path.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        return True
    if ext == ".svg":
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:600]
            return PLACEHOLDER_SIG not in head
        except Exception:
            return False
    return False


def parse_readme(md_text: str) -> list[dict]:
    figs = []
    blocks = re.split(r"(?m)^## Figure\s+\d+\s*$", md_text)
    for block in blocks[1:]:
        d: dict[str, str] = {}
        for raw in block.splitlines():
            line = raw.strip()
            if not line.startswith("- "):
                continue
            line = line[2:].strip()
            for key, slot in (
                ("Local:", "local"),
                ("Topic:", "topic"),
                ("Source:", "source"),
                ("License:", "license"),
                ("Author/credit:", "credit"),
            ):
                if line.startswith(key):
                    d[slot] = line[len(key):].strip()
                    break
        if d.get("local"):
            figs.append(d)
    return figs


def page_path_for(slug: str) -> Path:
    if slug == "index":
        return ROOT / "index.html"
    if slug == "updates-index":
        return ROOT / "updates" / "index.html"
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


def asset_url(slug: str, fname: str) -> str:
    return "/" + "/".join(quote(p, safe="") for p in ("assets", "img", "figures", slug, fname))


def figure_html(slug: str, f: dict, src: Path) -> str:
    fname = f.get("local", "")
    dst_dir = ASSETS / slug
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / fname
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    url = asset_url(slug, fname)
    topic = esc(f.get("topic", ""))
    source = f.get("source", "")
    credit = esc(f.get("credit", ""))
    parts = []
    if topic:
        parts.append(topic)
    extras = []
    if credit and credit not in ("PubChem", ""):
        extras.append(credit)
    if source:
        extras.append(f'<a href="{esc(source)}" target="_blank" rel="noopener">출처</a>')
    if extras:
        parts.append('<span class="fig-meta">· ' + " · ".join(extras) + '</span>')
    cap = " ".join(parts)
    return (
        f'<figure class="real-fig">'
        f'<img src="{url}" alt="{topic}" loading="lazy">'
        f'<figcaption>{cap}</figcaption>'
        f'</figure>'
    )


def find_h2_positions(text: str) -> list[int]:
    """Return positions of <h2 ...> openings inside <article> body."""
    # Restrict to inside <main> (or <article>)
    main_start = text.find("<main")
    if main_start < 0:
        main_start = 0
    refs = text.find('<section class="references-block">', main_start)
    end = refs if refs > 0 else text.find("</main>", main_start)
    if end < 0:
        end = len(text)
    positions = []
    # Skip <h2> inside <details>/<summary> etc.; just take all top-level h2 in main
    for m in re.finditer(r"<h2\b", text[main_start:end]):
        positions.append(main_start + m.start())
    return positions


def inject(html_path: Path, slug: str, figs_html: list[str]) -> bool:
    text = html_path.read_text(encoding="utf-8")
    text = BLOCK_RE.sub("", text).rstrip() + "\n"
    if not figs_html:
        html_path.write_text(text, encoding="utf-8")
        return False

    h2_positions = find_h2_positions(text)
    insertions: list[tuple[int, str]] = []

    if len(h2_positions) >= 2:
        # Skip first h2 so figures don't appear right at top
        usable = h2_positions[1:]
        n = len(figs_html)
        if n <= len(usable):
            stride = max(1, len(usable) // n)
            for i, fh in enumerate(figs_html):
                pos_idx = min(i * stride, len(usable) - 1)
                insertions.append((usable[pos_idx], fh))
        else:
            for i, pos in enumerate(usable):
                insertions.append((pos, figs_html[i]))
            # leftover: before references
            ref_pos = text.find('<section class="references-block">')
            if ref_pos < 0:
                ref_pos = text.find("</main>")
            if ref_pos > 0:
                for fh in figs_html[len(usable):]:
                    insertions.append((ref_pos, fh))
    else:
        ref_pos = text.find('<section class="references-block">')
        if ref_pos < 0:
            ref_pos = text.find("</main>")
        if ref_pos < 0:
            return False
        for fh in figs_html:
            insertions.append((ref_pos, fh))

    insertions.sort(key=lambda x: x[0], reverse=True)
    for pos, fh in insertions:
        wrapped = f"\n{OPEN}\n{fh}\n{CLOSE}\n\n"
        text = text[:pos] + wrapped + text[pos:]

    html_path.write_text(text, encoding="utf-8")
    return True


def process(slug: str, sub: Path):
    if slug in PAPER_FIG_PAGES:
        return None
    readme = sub / "README.md"
    if not readme.exists():
        return None
    figs = parse_readme(readme.read_text(encoding="utf-8"))
    real_figs_html: list[str] = []
    skipped_placeholder = 0
    for f in figs:
        local = f.get("local", "")
        if not local:
            continue
        src = sub / local
        if not src.exists():
            continue
        if not is_real_figure(src):
            skipped_placeholder += 1
            continue
        real_figs_html.append(figure_html(slug, f, src))
    page = page_path_for(slug)
    if not page.exists():
        return None
    return slug, page, real_figs_html, skipped_placeholder


def main():
    n_real_pages = 0
    n_no_real = 0
    skipped_total = 0
    for entry in sorted(PRIV.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name == "updates":
            for sub in sorted(entry.iterdir()):
                if not sub.is_dir():
                    continue
                slug = f"updates/{sub.name}"
                r = process(slug, sub)
                if r is None:
                    continue
                slug, page, real_figs, skp = r
                skipped_total += skp
                if inject(page, slug, real_figs):
                    n_real_pages += 1
                    print(f"  +{len(real_figs)} real (skip {skp} placeholder): {slug}")
                else:
                    n_no_real += 1
                    print(f"  0 real (skip {skp} placeholder): {slug}")
        else:
            r = process(entry.name, entry)
            if r is None:
                continue
            slug, page, real_figs, skp = r
            skipped_total += skp
            if inject(page, slug, real_figs):
                n_real_pages += 1
                print(f"  +{len(real_figs)} real (skip {skp} placeholder): {slug}")
            else:
                n_no_real += 1
                print(f"  0 real (skip {skp} placeholder): {slug}")
    print(f"Done. {n_real_pages} pages got real figures, {n_no_real} pages had only placeholders, {skipped_total} placeholder figs skipped total.")


if __name__ == "__main__":
    main()
