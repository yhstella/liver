"""Inject actual paper figures from private-figures/paper-figures into the
website pages listed in each paper's `source_pages`.

For each paper:
  - Read paper.json (DOI, figures list with captions, source_pages)
  - Copy figure files (.jpg/.png) to assets/img/papers/{paper-folder}/
  - Inject inline <figure> blocks into each source page
  - Position: distributed through the article body (between sections)

Replaces my earlier generic <!-- update-fig --> placeholder SVGs with real
paper figures. Idempotent via <!-- paper-figs --> markers.
"""
from __future__ import annotations
import html as htmllib
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
PAPER_DIR = ROOT / "private-figures" / "paper-figures"
ASSETS_DIR = ROOT / "assets" / "img" / "papers"

OPEN = "<!-- paper-figs -->"
CLOSE = "<!-- /paper-figs -->"
BLOCK_RE = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.DOTALL)
# Strip my earlier generated update-fig blocks too
LEGACY_RE = re.compile(r"<!-- update-fig -->.*?<!-- /update-fig -->\s*", re.DOTALL)

# Section dividers used by note-section / case-section / h2 markers
SECTION_RE = re.compile(
    r'(<div class="note-section">|<div class="case-section">|<h2[^>]*>)',
    re.DOTALL,
)


def esc(s: str) -> str:
    return htmllib.escape(s or "")


def asset_url(folder: str, fname: str) -> str:
    return "/" + "/".join(quote(p, safe="") for p in ("assets", "img", "papers", folder, fname))


def copy_figs(paper_folder: Path, asset_folder: Path) -> None:
    asset_folder.mkdir(parents=True, exist_ok=True)
    for f in paper_folder.iterdir():
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            dst = asset_folder / f.name
            if not dst.exists() or f.stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(f, dst)


def figure_card(folder: str, fig: dict) -> str:
    fname = fig.get("local_file", "")
    label = esc(fig.get("label", "").rstrip("."))
    caption = esc(fig.get("caption", ""))
    url = asset_url(folder, fname)
    cap_html = f"<strong>{label}</strong> {caption}" if label else caption
    return (
        f'<figure class="paper-fig">'
        f'<img src="{url}" alt="{caption}" loading="lazy">'
        f'<figcaption>{cap_html}</figcaption>'
        f'</figure>'
    )


def figures_block(figs: list[dict], folder: str, source_url: str = "") -> str:
    if not figs:
        return ""
    cards = "\n".join(figure_card(folder, f) for f in figs)
    return cards


def find_section_positions(text: str) -> list[int]:
    """Return character positions of section dividers in the article body."""
    positions = []
    for m in SECTION_RE.finditer(text):
        positions.append(m.start())
    return positions


def inject_figures(html_path: Path, paper_folder_name: str, paper_data: dict) -> bool:
    text = html_path.read_text(encoding="utf-8")

    # Strip earlier legacy update-fig blocks
    text = LEGACY_RE.sub("", text)
    # Strip existing paper-figs block
    text = BLOCK_RE.sub("", text).rstrip() + "\n"

    figs = paper_data.get("figures", [])
    if not figs:
        return False

    # For updates pages: distribute one figure between each pair of note-sections.
    # If more sections than figures, place all figures evenly. If more figures
    # than slots, append remaining at end before references.
    section_positions = []
    for m in re.finditer(r'<div class="note-section">|<div class="case-section">', text):
        section_positions.append(m.start())

    # Distribute strategy:
    # - For each figure_i, insert before section_positions[ slot_i ] where slot is
    #   chosen to evenly spread. We avoid the very first section so the article
    #   opens with text first.
    n_secs = len(section_positions)
    n_figs = len(figs)

    insertions = []  # (position, html)

    if n_secs >= 2:
        # Spread figures across sections starting from section 1 (skip section 0)
        usable = section_positions[1:]
        if not usable:
            usable = section_positions
        if n_figs <= len(usable):
            # Evenly choose len(figs) positions from usable
            stride = max(1, len(usable) // n_figs)
            for i, fig in enumerate(figs):
                pos_idx = min(i * stride, len(usable) - 1)
                pos = usable[pos_idx]
                insertions.append((pos, figure_card(paper_folder_name, fig)))
        else:
            # More figures than sections — put one per section, rest at end
            for i, pos in enumerate(usable):
                insertions.append((pos, figure_card(paper_folder_name, figs[i])))
            # Remaining figures go before references-block or </article>
            ref_pos = text.find('<section class="references-block">')
            if ref_pos < 0:
                ref_pos = text.find("</article>")
            if ref_pos > 0:
                for fig in figs[len(usable):]:
                    insertions.append((ref_pos, figure_card(paper_folder_name, fig)))
    else:
        # No sections found — put all figures before references / </article>
        ref_pos = text.find('<section class="references-block">')
        if ref_pos < 0:
            ref_pos = text.find("</article>")
        if ref_pos < 0:
            ref_pos = text.find("</main>")
        if ref_pos < 0:
            return False
        for fig in figs:
            insertions.append((ref_pos, figure_card(paper_folder_name, fig)))

    # Apply insertions in reverse order to keep positions valid
    insertions.sort(key=lambda x: x[0], reverse=True)
    new_text = text
    for pos, fig_html in insertions:
        wrapped = f"\n{OPEN}\n{fig_html}\n{CLOSE}\n\n"
        new_text = new_text[:pos] + wrapped + new_text[pos:]

    if new_text == text:
        return False
    html_path.write_text(new_text, encoding="utf-8")
    return True


SKIP_PAGES = {"연구/index.html"}  # Publication list — figures don't fit inline


def main():
    # Phase 1: gather all papers grouped by source page
    page_papers: dict[str, list[tuple[str, dict]]] = {}
    n_papers = 0
    for paper_folder in sorted(PAPER_DIR.iterdir()):
        if not paper_folder.is_dir():
            continue
        pj = paper_folder / "paper.json"
        if not pj.exists():
            continue
        data = json.loads(pj.read_text(encoding="utf-8"))
        if data.get("status") != "downloaded":
            continue
        figs = data.get("figures", [])
        if not figs:
            continue

        asset_folder = ASSETS_DIR / paper_folder.name
        copy_figs(paper_folder, asset_folder)
        n_papers += 1

        for src_page in data.get("source_pages", []):
            if src_page in SKIP_PAGES:
                continue
            page_papers.setdefault(src_page, []).append((paper_folder.name, data))

    # Phase 2: clean any prior paper-figs from skipped pages too
    for skip_page in SKIP_PAGES:
        p = ROOT / skip_page
        if p.exists():
            t = p.read_text(encoding="utf-8")
            new = LEGACY_RE.sub("", BLOCK_RE.sub("", t)).rstrip() + "\n"
            if new != t:
                p.write_text(new, encoding="utf-8")
                print(f"  cleaned: {skip_page}")

    # Phase 3: inject all of each page's papers in one pass
    n_pages = 0
    for src_page, papers in page_papers.items():
        page_path = ROOT / src_page
        if not page_path.exists():
            print(f"  ! page missing: {src_page}")
            continue
        if inject_all(page_path, papers):
            n_pages += 1
            total_figs = sum(len(p[1].get("figures", [])) for p in papers)
            print(f"  ok [{len(papers)} papers, {total_figs} figs]: {src_page}")
        else:
            print(f"  skip (no insertion point): {src_page}")

    print(f"Done. {n_papers} papers, {n_pages} page injections.")


def inject_all(html_path: Path, papers: list[tuple[str, dict]]) -> bool:
    """Inject all figures from `papers` into one page in a single pass."""
    text = html_path.read_text(encoding="utf-8")
    text = LEGACY_RE.sub("", text)
    text = BLOCK_RE.sub("", text).rstrip() + "\n"

    # Build flat list of (paper_folder, fig) tuples
    flat_figs: list[tuple[str, dict]] = []
    for folder, data in papers:
        for fig in data.get("figures", []):
            flat_figs.append((folder, fig))

    if not flat_figs:
        return False

    # Find note-section / case-section positions
    section_positions = [
        m.start() for m in re.finditer(
            r'<div class="note-section">|<div class="case-section">', text
        )
    ]

    insertions: list[tuple[int, str]] = []
    if len(section_positions) >= 2:
        usable = section_positions[1:]  # skip first section
        if not usable:
            usable = section_positions
        if len(flat_figs) <= len(usable):
            stride = max(1, len(usable) // len(flat_figs))
            for i, (folder, fig) in enumerate(flat_figs):
                pos_idx = min(i * stride, len(usable) - 1)
                insertions.append((usable[pos_idx], figure_card(folder, fig)))
        else:
            # More figures than usable slots — one per slot, rest at end
            for i, pos in enumerate(usable):
                folder, fig = flat_figs[i]
                insertions.append((pos, figure_card(folder, fig)))
            ref_pos = text.find('<section class="references-block">')
            if ref_pos < 0:
                ref_pos = text.find("</article>")
            if ref_pos > 0:
                for folder, fig in flat_figs[len(usable):]:
                    insertions.append((ref_pos, figure_card(folder, fig)))
    else:
        ref_pos = text.find('<section class="references-block">')
        if ref_pos < 0:
            ref_pos = text.find("</article>")
        if ref_pos < 0:
            ref_pos = text.find("</main>")
        if ref_pos < 0:
            return False
        for folder, fig in flat_figs:
            insertions.append((ref_pos, figure_card(folder, fig)))

    insertions.sort(key=lambda x: x[0], reverse=True)
    new_text = text
    for pos, fig_html in insertions:
        wrapped = f"\n{OPEN}\n{fig_html}\n{CLOSE}\n\n"
        new_text = new_text[:pos] + wrapped + new_text[pos:]

    if new_text == text:
        return False
    html_path.write_text(new_text, encoding="utf-8")
    return True


if __name__ == "__main__":
    main()
