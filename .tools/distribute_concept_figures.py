"""Replace research-related shared figures with relevant hepatology-web-concepts
images. Each image used at most once. Pages get up to 3 different figures.

Sources:
  - private-figures/hepatology-web-concepts/by-topic/{folder}/  (concept figures)
  - private-figures/paper-figures/{doi}/                        (PMC OA, kept for update pages)
  - assets/img/web/mediterranean-diet-pyramid.jpg              (web-fetched, manually placed)

Replaces all <!-- fig --> blocks (from distribute_figures.py).
"""
from __future__ import annotations
import hashlib
import html as htmllib
import json
import re
import shutil
import sys, os
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
PRIV = ROOT / "private-figures"
WEB_CONCEPTS = PRIV / "hepatology-web-concepts" / "by-topic"
PAPER_DIR = PRIV / "paper-figures"
ASSETS_CONCEPTS = ROOT / "assets" / "img" / "concepts"

OPEN = "<!-- fig -->"
CLOSE = "<!-- /fig -->"
BLOCK_RE = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.DOTALL)
WEB_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")

sys.path.insert(0, str(ROOT / ".tools"))
from page_keywords import PAGE_KEYWORDS


def esc(s: str) -> str:
    return htmllib.escape(s or "")


def clean_caption(fname: str) -> str:
    name = fname
    name = re.sub(r"^\d+-", "", name)
    name = re.sub(r"-[0-9a-f]{6,}\.[a-z]+$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\.(svg|tiff|png|jpg|jpeg|gif)(?=-|$)", "", name, flags=re.IGNORECASE)
    name = name.replace("-", " ").strip()
    # Capitalize first letter
    if name:
        name = name[0].upper() + name[1:]
    return name


def sha1_file(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


# Slug → preferred concept folders (priority order)
def slug_concept_folders(slug: str) -> list[str]:
    if slug.startswith("케이스/"):
        cs = slug.split("/", 1)[1]
        if any(x in cs for x in ("자가면역", "약물성간손상", "독성간염", "보충제")):
            return ["dili-toxins", "liver-tests-biomarkers"]
        if any(x in cs for x in ("정맥류", "복수", "SBP", "간성혼수", "ChildC", "이식", "간경변")):
            return ["liver-anatomy", "liver-histology", "hcc-liver-cancer"]
        if any(x in cs for x in ("HBsAg", "HBeAg", "B형간염", "ETV-TAF", "임신중", "재활성화", "seroclearance", "C형간염")):
            return ["viral-hepatitis", "liver-anatomy"]
        if any(x in cs for x in ("MASLD", "MASH", "GLP1", "lean", "resmetirom", "당뇨")):
            return ["metabolic-therapeutics", "liver-anatomy"]
        if "ALT" in cs:
            return ["liver-tests-biomarkers", "dili-toxins"]
        # default HCC case
        return ["hcc-liver-cancer", "liver-anatomy"]
    if slug.startswith("updates/"):
        u = slug.split("/", 1)[1]
        if any(x in u for x in ("HBV", "HBeAg", "TDF", "TAF", "ETV", "Antiviral", "COVID", "B형")):
            return ["viral-hepatitis"]
        if any(x in u for x in ("MASLD", "MASH", "NASH", "Aspirin", "GLP1", "SGLT2", "resmetirom", "PEth", "ALD", "semaglutide", "orforglipron")):
            return ["metabolic-therapeutics"]
        if any(x in u for x in ("HCC", "CIK", "atezolizumab", "HIMALAYA", "IMbrave", "Guidelines", "AI-CT")):
            return ["hcc-liver-cancer"]
        if any(x in u for x in ("Baveno", "TIPS", "portal", "정맥류")):
            return ["liver-anatomy"]
        return ["hcc-liver-cancer"]
    # Topic pages
    if slug == "약물성-간손상-DILI":
        return ["dili-toxins", "liver-tests-biomarkers"]
    if slug.startswith("간암-") or slug == "간암" or slug == "알파태아단백" or slug == "PIVKA-II-간암마커":
        return ["hcc-liver-cancer", "liver-anatomy"]
    if slug.startswith("간경변-") or slug == "간경화":
        return ["liver-anatomy", "liver-histology", "hcc-liver-cancer"]
    if slug.startswith("B형간염") or slug.startswith("가족-B형간염"):
        return ["viral-hepatitis", "liver-anatomy"]
    if slug.startswith("C형간염"):
        return ["viral-hepatitis"]
    if (slug.startswith("지방간") or slug == "대사이상지방간-MASLD" or slug == "술-안마셔도-지방간"
            or slug == "지방간염-MASH"):
        return ["metabolic-therapeutics", "liver-anatomy"]
    if slug == "간섬유화스캔-수치" or slug == "간생검-언제-필요한가":
        return ["liver-histology", "liver-tests-biomarkers"]
    if slug.startswith("간수치") or slug in ("ALP-GGT-담도-간세포", "빌리루빈-직접-간접",
                                            "알부민-PT-간합성능"):
        return ["liver-tests-biomarkers", "liver-anatomy"]
    if slug == "index":
        return ["liver-anatomy"]
    return ["liver-anatomy"]


def page_path(slug: str) -> Path:
    if slug == "index":
        return ROOT / "index.html"
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    if slug.startswith("케이스/"):
        return ROOT / "케이스" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


def asset_url(*parts: str) -> str:
    return "/" + "/".join(quote(p, safe="") for p in parts)


def copy_to(src: Path, dst_dir: Path, fname: str) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / fname
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)


def figure_html(url: str, caption: str, label: str = "") -> str:
    cap = caption.strip()
    if label:
        cap = f"<strong>{esc(label.rstrip('.'))}</strong> {esc(cap)}"
    else:
        cap = esc(cap)
    return (
        f'<figure class="real-fig">'
        f'<img src="{url}" alt="{esc(caption)}" loading="lazy">'
        f'<figcaption>{cap}</figcaption>'
        f'</figure>'
    )


def find_h2_positions(text: str) -> list[int]:
    main_start = text.find("<main")
    if main_start < 0:
        main_start = 0
    refs = text.find('<section class="references-block">', main_start)
    end = refs if refs > 0 else text.find("</main>", main_start)
    if end < 0:
        end = len(text)
    return [main_start + m.start() for m in re.finditer(r"<h2\b", text[main_start:end])]


def inject(html_path: Path, fig_htmls: list[str]) -> bool:
    if not html_path.exists():
        return False
    text = html_path.read_text(encoding="utf-8")
    text = BLOCK_RE.sub("", text).rstrip() + "\n"
    if not fig_htmls:
        html_path.write_text(text, encoding="utf-8")
        return False
    h2_positions = find_h2_positions(text)
    insertions: list[tuple[int, str]] = []
    if len(h2_positions) >= 2:
        usable = h2_positions[1:]
        if len(fig_htmls) <= len(usable):
            stride = max(1, len(usable) // len(fig_htmls))
            for i, fh in enumerate(fig_htmls):
                pos_idx = min(i * stride, len(usable) - 1)
                insertions.append((usable[pos_idx], fh))
        else:
            for i, pos in enumerate(usable):
                insertions.append((pos, fig_htmls[i]))
            ref_pos = text.find('<section class="references-block">')
            if ref_pos < 0:
                ref_pos = text.find("</main>")
            if ref_pos > 0:
                for fh in fig_htmls[len(usable):]:
                    insertions.append((ref_pos, fh))
    else:
        ref_pos = text.find('<section class="references-block">')
        if ref_pos < 0:
            ref_pos = text.find("</main>")
        if ref_pos < 0:
            return False
        for fh in fig_htmls:
            insertions.append((ref_pos, fh))
    insertions.sort(key=lambda x: x[0], reverse=True)
    for pos, fh in insertions:
        wrapped = f"\n{OPEN}\n{fh}\n{CLOSE}\n\n"
        text = text[:pos] + wrapped + text[pos:]
    html_path.write_text(text, encoding="utf-8")
    return True


def build_concept_pool() -> dict[str, list[dict]]:
    """Returns {folder: [items]} for hepatology-web-concepts."""
    pool: dict[str, list[dict]] = {}
    for folder in WEB_CONCEPTS.iterdir():
        if not folder.is_dir():
            continue
        items = []
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() not in WEB_EXTS:
                continue
            items.append({
                "src_path": f,
                "fname": f.name,
                "caption": clean_caption(f.name),
                "folder": folder.name,
                "sha1": sha1_file(f),
            })
        pool[folder.name] = items
    return pool


def collect_paper_figures() -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = defaultdict(list)
    if not PAPER_DIR.exists():
        return result
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
        update_slugs = [sp.replace("/index.html", "") for sp in data.get("source_pages", [])
                        if sp.startswith("updates/")]
        if not update_slugs:
            continue
        primary = update_slugs[0]
        for fig in figs:
            fname = fig.get("local_file", "")
            src = paper_folder / fname
            if not src.exists():
                continue
            result[primary].append({
                "src_path": src,
                "fname": fname,
                "caption": fig.get("caption", ""),
                "label": fig.get("label", ""),
                "asset_subdir": ROOT / "assets" / "img" / "papers" / paper_folder.name,
                "url_subdir": ("papers", paper_folder.name),
            })
    return result


def main():
    pages = list(PAGE_KEYWORDS.keys())
    pool = build_concept_pool()
    used_sha1: set[str] = set()
    page_assigned: dict[str, list[str]] = defaultdict(list)

    # Phase 1: paper-figures (specific update pages, exclusive)
    paper_assigned: dict[str, list[str]] = {}
    paper_count = 0
    for upd_slug, figs in collect_paper_figures().items():
        if upd_slug not in pages:
            continue
        htmls = []
        for fig in figs:
            asset_dir = fig["asset_subdir"]
            asset_dir.mkdir(parents=True, exist_ok=True)
            dst = asset_dir / fig["fname"]
            if not dst.exists() or fig["src_path"].stat().st_mtime > dst.stat().st_mtime:
                shutil.copy2(fig["src_path"], dst)
            url = asset_url("assets", "img", *fig["url_subdir"], fig["fname"])
            htmls.append(figure_html(url, fig["caption"], fig.get("label", "")))
            paper_count += 1
        paper_assigned[upd_slug] = htmls

    # Phase 2: 지방간-음식 keeps Mediterranean diet pyramid (web-fetched)
    if "지방간-음식" in pages:
        page_assigned["지방간-음식"].append(figure_html(
            "/assets/img/web/mediterranean-diet-pyramid.jpg",
            "Mediterranean diet food pyramid (Fundación Dieta Mediterránea, CC0)"
        ))

    # Phase 3: hepatology-web-concepts greedy allocation
    for pass_n in range(3):
        for slug in pages:
            if slug in paper_assigned:
                continue
            if len(page_assigned[slug]) >= 3:
                continue
            cats = slug_concept_folders(slug)
            picked = None
            for cat in cats:
                for item in pool.get(cat, []):
                    if item["sha1"] in used_sha1:
                        continue
                    picked = item
                    break
                if picked:
                    break
            if picked is None:
                continue
            used_sha1.add(picked["sha1"])
            copy_to(picked["src_path"], ASSETS_CONCEPTS / picked["folder"], picked["fname"])
            url = asset_url("assets", "img", "concepts", picked["folder"], picked["fname"])
            page_assigned[slug].append(figure_html(url, picked["caption"]))

    # Inject
    n_pages = 0
    n_figs = 0
    for slug in pages:
        path = page_path(slug)
        if not path.exists():
            continue
        htmls = paper_assigned.get(slug) or page_assigned.get(slug) or []
        if not htmls:
            continue
        if inject(path, htmls):
            n_pages += 1
            n_figs += len(htmls)

    total_pool = sum(len(v) for v in pool.values())
    print(f"Done. {n_pages} pages, {n_figs} placements")
    print(f"  paper-figures: {paper_count} (5 update pages)")
    print(f"  hepatology-web-concepts pool: {total_pool} images, {len(used_sha1)} used")


if __name__ == "__main__":
    main()
