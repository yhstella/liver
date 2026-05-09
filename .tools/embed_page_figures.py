"""Embed per-page figures from private-figures/by-page into the public site.

For each by-page/{slug}/README.md, parses the figure list, copies the
referenced files into assets/img/figures/{slug}/, and inserts a
<section class="page-figures"> block into the corresponding HTML page.

Re-runnable: looks for <!-- page-figures --> ... <!-- /page-figures -->
markers and replaces the block in place.
"""
from __future__ import annotations
import html
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\R\Dropbox\drshin.kr")
PRIV = ROOT / "private-figures" / "by-page"
ASSETS_DIR = ROOT / "assets" / "img" / "figures"

OPEN_MARK = "<!-- page-figures -->"
CLOSE_MARK = "<!-- /page-figures -->"


def parse_readme(md_text: str) -> list[dict]:
    figs = []
    blocks = re.split(r"(?m)^## Figure\s+\d+\s*$", md_text)
    for block in blocks[1:]:
        d: dict[str, str] = {}
        for raw in block.splitlines():
            line = raw.strip()
            if not line.startswith("- "):
                if line == "":
                    continue
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


def page_path_for_slug(slug: str) -> Path:
    if slug == "index":
        return ROOT / "index.html"
    if slug == "updates-index":
        return ROOT / "updates" / "index.html"
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


def asset_url_for(slug: str, fname: str, src: Path) -> str | None:
    dst_dir = ASSETS_DIR / slug
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / fname
    if not src.exists():
        return None
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    # URL-encode each path segment so Korean slugs work
    from urllib.parse import quote
    return "/" + "/".join(
        quote(p, safe="") for p in ("assets", "img", "figures", slug, fname)
    )


def figures_block(figs: list[dict], slug: str, src_dir: Path) -> str:
    cards = []
    for f in figs:
        local = f.get("local", "")
        src_file = src_dir / local
        url = asset_url_for(slug, local, src_file)
        if not url:
            continue
        topic = html.escape(f.get("topic", ""))
        source = f.get("source", "")
        credit = html.escape(f.get("credit", ""))
        attribution_parts = []
        if credit:
            attribution_parts.append(credit)
        if source:
            attribution_parts.append(
                f'<a href="{html.escape(source)}" target="_blank" rel="noopener">출처</a>'
            )
        attribution = " · ".join(attribution_parts)
        cap = topic
        if attribution:
            cap += f' <span style="color:var(--muted)">· {attribution}</span>'
        cards.append(
            f'<figure class="page-figure-card">'
            f'<img src="{url}" alt="{topic}" loading="lazy">'
            f'<figcaption>{cap}</figcaption>'
            f'</figure>'
        )
    if not cards:
        return ""
    return (
        '<section class="page-figures">'
        '<h2 style="font-family:\'Times New Roman\',Georgia,serif;font-size:18px;'
        "margin:0 0 14px;color:var(--muted);letter-spacing:0.04em;"
        'text-transform:uppercase">관련 그림</h2>'
        '<div class="page-figure-grid">'
        + "".join(cards)
        + "</div></section>"
    )


def insert_into_page(html_path: Path, block: str) -> bool:
    text = html_path.read_text(encoding="utf-8")
    wrapped = f"{OPEN_MARK}\n{block}\n{CLOSE_MARK}"

    if OPEN_MARK in text and CLOSE_MARK in text:
        new_text = re.sub(
            re.escape(OPEN_MARK) + r".*?" + re.escape(CLOSE_MARK),
            wrapped.replace("\\", "\\\\"),
            text,
            count=1,
            flags=re.DOTALL,
        )
    else:
        # Prefer inserting before References section
        if '<section class="references-block">' in text:
            new_text = text.replace(
                '<section class="references-block">',
                f'{wrapped}\n\n<section class="references-block">',
                1,
            )
        elif "</main>" in text:
            new_text = text.replace("</main>", f"{wrapped}\n</main>", 1)
        else:
            return False

    if new_text == text:
        return False
    html_path.write_text(new_text, encoding="utf-8")
    return True


def process(slug: str, src_dir: Path) -> tuple[bool, int]:
    readme = src_dir / "README.md"
    if not readme.exists():
        return False, 0
    figs = parse_readme(readme.read_text(encoding="utf-8"))
    if not figs:
        return False, 0
    page_path = page_path_for_slug(slug)
    if not page_path.exists():
        print(f"  skip (no page): {slug}")
        return False, 0
    block = figures_block(figs, slug, src_dir)
    if not block:
        return False, 0
    ok = insert_into_page(page_path, block)
    if ok:
        print(f"  inserted {len(figs)}: {slug}")
    return ok, len(figs)


def main() -> None:
    n_pages = 0
    n_figs = 0
    if not PRIV.exists():
        print(f"Missing {PRIV}")
        return
    for entry in sorted(PRIV.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name == "updates":
            for sub in sorted(entry.iterdir()):
                if not sub.is_dir():
                    continue
                ok, k = process(f"updates/{sub.name}", sub)
                if ok:
                    n_pages += 1
                    n_figs += k
        else:
            ok, k = process(entry.name, entry)
            if ok:
                n_pages += 1
                n_figs += k
    print(f"Done. {n_pages} pages, {n_figs} figures.")


if __name__ == "__main__":
    main()
