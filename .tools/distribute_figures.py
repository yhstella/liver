"""Globally distribute private-figures images: each image used at most ONCE,
each page gets up to 3 different images.

Sources:
  - private-figures/paper-figures/{doi}/   (per-paper, source_pages mapping)
  - private-figures/medicine-topics/{cat}/ (Shin research figures by topic)
  - private-figures/by-page/{slug}/         (curated per-page real images)

Filters:
  - Web-friendly only (.png, .jpg, .jpeg, .gif, .webp, real .svg)
  - Reject placeholder SVG study cards (contain 'drshin.kr study figure')
  - Reject bad captions (raw filenames, supplementary, personal)

Allocation strategy (greedy):
  1. Paper-figures → assigned exclusively to corresponding update page(s)
  2. Build remaining pool, dedup by sha1
  3. For each page (deficit-first ordering), pull up to 3 figures from pool
     ranked by topic-category match
  4. Inject inline at <h2> boundaries
"""
from __future__ import annotations
import csv
import hashlib
import html as htmllib
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
PRIV = ROOT / "private-figures"
MEDTOPICS = PRIV / "medicine-topics"
BYPAGE = PRIV / "by-page"
PAPER_DIR = PRIV / "paper-figures"
ASSETS = ROOT / "assets" / "img" / "shared"

OPEN = "<!-- fig -->"
CLOSE = "<!-- /fig -->"
BLOCK_RE = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.DOTALL)

PLACEHOLDER_SIG = "drshin.kr study figure"
WEB_EXTS = (".png", ".jpg", ".jpeg", ".gif", ".webp")

# Bad caption patterns
BAD_CAPTION_PATTERNS = [
    "not_for_submit", "Supp", "supplement", "_BW", "_바탕", "_data_",
    "면허증", "서명", "signature", "CV", "이력서",
    "raw_", "DF & DF_R", "_보고", "_세미나", "그림1", "그림2", "그림3",
    "Rplot", "figure-1", "figure-2", "figure-3", "Forest1", "Forest2", "Forest3",
    "fig1", "fig2", "fig3", "Fig1", "Fig2", "Fig3", "FigureS",
    "Figure 1", "Figure 2", "Figure 3", "Figure 4", "Figure 5",
    "PROFILE", "_2_", "_3_", "_4_", "_5_",
    "graphical_abstract_230",  # raw export filename pattern
    "이정훈", "신현재 약력", "박사 학위",
]


def esc(s: str) -> str:
    return htmllib.escape(s or "")


def is_real_svg(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:600]
        return PLACEHOLDER_SIG not in head
    except Exception:
        return False


def good_caption(title: str, source_path: str = "") -> bool:
    if not title:
        return False
    s = title.strip()
    # Pure number-like or 1-2 char
    if len(s) < 5:
        return False
    for p in BAD_CAPTION_PATTERNS:
        if p in title or p in source_path:
            return False
    # Mostly underscore/dash technical filename
    if re.fullmatch(r"[\w\d\s\-_.]+", s) and ("_" in s and len(s) > 25):
        return False
    return True


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    h.update(path.read_bytes())
    return h.hexdigest()


# === Slug → preferred topic categories
def slug_categories(slug: str) -> list[str]:
    # Order = priority
    if slug.startswith("케이스/"):
        cs = slug.split("/", 1)[1]
        if any(x in cs for x in ("자가면역", "약물성", "독성", "보충제", "DILI")):
            return ["cholestasis-autoimmune-dili", "diagnostics-biomarkers-imaging-ai", "other-hepatology"]
        if any(x in cs for x in ("정맥류", "복수", "SBP", "간성혼수", "ChildC", "이식")):
            return ["cirrhosis-portal-hypertension", "hcc-oncology-immunotherapy"]
        if any(x in cs for x in ("HBsAg", "HBeAg", "B형간염", "ETV-TAF", "임신중", "재활성화", "seroclearance")):
            return ["viral-hepatitis-hbv-hcv", "diagnostics-biomarkers-imaging-ai"]
        if any(x in cs for x in ("MASLD", "MASH", "GLP1", "lean", "resmetirom", "당뇨")):
            return ["masld-mash-nafld-metabolic", "diagnostics-biomarkers-imaging-ai"]
        if "ALT" in cs and "MASLD" not in cs:
            return ["diagnostics-biomarkers-imaging-ai", "cholestasis-autoimmune-dili"]
        # default: HCC case
        return ["hcc-oncology-immunotherapy", "diagnostics-biomarkers-imaging-ai"]
    if slug.startswith("updates/"):
        u = slug.split("/", 1)[1]
        if any(x in u for x in ("HBV", "HBeAg", "TDF", "TAF", "ETV", "Antiviral", "COVID")):
            return ["viral-hepatitis-hbv-hcv", "diagnostics-biomarkers-imaging-ai"]
        if any(x in u for x in ("MASLD", "MASH", "NASH", "Aspirin", "GLP1", "SGLT2", "resmetirom", "PEth", "ALD", "semaglutide", "orforglipron")):
            return ["masld-mash-nafld-metabolic", "diagnostics-biomarkers-imaging-ai"]
        if any(x in u for x in ("HCC", "CIK", "atezolizumab", "HIMALAYA", "IMbrave", "Guidelines", "AI-CT")):
            return ["hcc-oncology-immunotherapy", "diagnostics-biomarkers-imaging-ai"]
        if any(x in u for x in ("Baveno", "TIPS", "portal", "정맥류")):
            return ["cirrhosis-portal-hypertension"]
        return ["hcc-oncology-immunotherapy", "diagnostics-biomarkers-imaging-ai"]
    # Topic pages
    if slug.startswith("간암-") or slug == "간암" or slug == "알파태아단백" or slug == "PIVKA-II-간암마커":
        return ["hcc-oncology-immunotherapy", "diagnostics-biomarkers-imaging-ai"]
    if slug.startswith("간경변-") or slug == "간경화":
        return ["cirrhosis-portal-hypertension", "hcc-oncology-immunotherapy"]
    if slug.startswith("B형간염") or slug.startswith("C형간염") or slug.startswith("가족-B형간염"):
        return ["viral-hepatitis-hbv-hcv", "diagnostics-biomarkers-imaging-ai"]
    if (slug.startswith("지방간") or slug == "대사이상지방간-MASLD" or slug == "술-안마셔도-지방간"
            or slug == "지방간염-MASH"):
        return ["masld-mash-nafld-metabolic", "diagnostics-biomarkers-imaging-ai"]
    if slug.startswith("간수치") or slug in ("ALP-GGT-담도-간세포", "빌리루빈-직접-간접",
                                            "알부민-PT-간합성능", "약물성-간손상-DILI",
                                            "간섬유화스캔-수치", "간생검-언제-필요한가"):
        return ["diagnostics-biomarkers-imaging-ai", "cholestasis-autoimmune-dili"]
    if slug == "index":
        return ["other-hepatology", "diagnostics-biomarkers-imaging-ai"]
    return []


# === Pool builder
def build_pool() -> list[dict]:
    pool: list[dict] = []
    seen_sha1: set[str] = set()

    # 1. medicine-topics
    with (MEDTOPICS / "manifest.csv").open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            ext = row.get("ext", "").lower()
            if ext not in WEB_EXTS and ext != ".svg":
                continue
            src = MEDTOPICS / row.get("dest_file", "")
            if not src.exists():
                continue
            if ext == ".svg" and not is_real_svg(src):
                continue
            title = row.get("source_title", "")
            sp = row.get("source_path", "")
            if not good_caption(title, sp):
                continue
            sha = row.get("sha1", "")
            if not sha:
                sha = sha1_file(src)
            if sha in seen_sha1:
                continue
            seen_sha1.add(sha)
            try:
                score = float(row.get("score", "0") or 0)
            except ValueError:
                score = 0.0
            pool.append({
                "source": "medicine-topics",
                "src_path": src,
                "fname": src.name,
                "caption": title,
                "topic": row.get("topic", ""),
                "score": score,
                "sha1": sha,
                "origin": sp,
            })

    # 2. by-page real images (PNG/JPG only, web-friendly)
    for sub in BYPAGE.iterdir():
        if not sub.is_dir():
            continue
        readme = sub / "README.md"
        if not readme.exists():
            continue
        md = readme.read_text(encoding="utf-8")
        figs = []
        for block in re.split(r"(?m)^## Figure\s+\d+\s*$", md)[1:]:
            d = {}
            for raw in block.splitlines():
                line = raw.strip()
                if not line.startswith("- "):
                    continue
                line = line[2:].strip()
                for key, slot in (("Local:", "local"), ("Topic:", "topic"),
                                  ("Source:", "source"), ("Author/credit:", "credit")):
                    if line.startswith(key):
                        d[slot] = line[len(key):].strip()
                        break
            if d.get("local"):
                figs.append(d)
        for f in figs:
            local = f.get("local", "")
            src = sub / local
            if not src.exists():
                continue
            ext = src.suffix.lower()
            if ext not in WEB_EXTS:
                if ext == ".svg" and not is_real_svg(src):
                    continue
                if ext != ".svg":
                    continue
            sha = sha1_file(src)
            if sha in seen_sha1:
                continue
            seen_sha1.add(sha)
            topic = f.get("topic", "")
            credit = f.get("credit", "")
            # Categorize by-page figures
            cat = ""
            slug_lower = sub.name.lower()
            if "hbv" in slug_lower or "B형" in sub.name or "hbeag" in slug_lower:
                cat = "viral-hepatitis-hbv-hcv"
            elif "hcc" in slug_lower or "간암" in sub.name or "afp" in slug_lower or "pivka" in slug_lower:
                cat = "hcc-oncology-immunotherapy"
            elif "간경" in sub.name or "정맥류" in sub.name or "복수" in sub.name:
                cat = "cirrhosis-portal-hypertension"
            elif "지방간" in sub.name or "MASLD" in sub.name or "MASH" in sub.name:
                cat = "masld-mash-nafld-metabolic"
            else:
                cat = "diagnostics-biomarkers-imaging-ai"
            pool.append({
                "source": "by-page",
                "src_path": src,
                "fname": local,
                "caption": topic,
                "credit": credit,
                "topic": cat,
                "score": 50.0,  # high: hand-curated
                "sha1": sha,
                "origin": f.get("source", ""),
            })

    return pool


# === Paper-figures direct assignment (to update pages only)
def collect_paper_figures() -> dict[str, list[dict]]:
    """Returns {update_slug: [fig_dict, ...]}. Each fig copied to assets."""
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
        # Find the update source page (skip 연구/)
        update_slugs = []
        for sp in data.get("source_pages", []):
            if sp.startswith("updates/"):
                update_slugs.append(sp.replace("/index.html", ""))
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
                "asset_subdir": f"papers/{paper_folder.name}",
            })
    return result


# === Page list (from page_keywords)
def all_pages() -> list[str]:
    import sys, os
    sys.path.insert(0, str(ROOT / ".tools"))
    from page_keywords import PAGE_KEYWORDS
    return list(PAGE_KEYWORDS.keys())


def page_path(slug: str) -> Path:
    if slug == "index":
        return ROOT / "index.html"
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    if slug.startswith("케이스/"):
        return ROOT / "케이스" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


# === Asset copy + URL
def asset_url(subdir: str, fname: str) -> str:
    return "/" + "/".join(quote(p, safe="") for p in ("assets", "img", subdir, fname))


def copy_asset(src: Path, subdir: str, fname: str) -> str:
    dst_dir = ROOT / "assets" / "img" / subdir
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / fname
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    return asset_url(subdir, fname)


# === Inject
def find_h2_positions(text: str) -> list[int]:
    main_start = text.find("<main")
    if main_start < 0:
        main_start = 0
    refs = text.find('<section class="references-block">', main_start)
    end = refs if refs > 0 else text.find("</main>", main_start)
    if end < 0:
        end = len(text)
    return [main_start + m.start() for m in re.finditer(r"<h2\b", text[main_start:end])]


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


# === Main
def main():
    pages = all_pages()
    # Phase 1: paper-figures direct allocation
    paper_assigned: dict[str, list[str]] = {}
    paper_used_count = 0
    for upd_slug, figs in collect_paper_figures().items():
        if upd_slug not in pages:
            # not in our keywords pool — still allocate
            pages_set = set(pages)
            if upd_slug not in pages_set:
                continue
        htmls = []
        for fig in figs:
            url = copy_asset(fig["src_path"], fig["asset_subdir"], fig["fname"])
            htmls.append(figure_html(url, fig["caption"], fig.get("label", "")))
            paper_used_count += 1
        paper_assigned[upd_slug] = htmls

    # Phase 2: build remaining pool (medicine-topics + by-page)
    pool = build_pool()
    # Sort pool: high score first
    pool.sort(key=lambda x: -x["score"])

    # Phase 3: greedy allocation, max 3 per page
    page_assigned: dict[str, list[str]] = defaultdict(list)
    used_sha1: set[str] = set()
    # Use deficit-first ordering across multiple passes
    for pass_n in range(3):  # try to give each page up to 3 figs
        for slug in pages:
            if slug in paper_assigned:
                # paper-figures already saturate this page
                continue
            if len(page_assigned[slug]) >= 3:
                continue
            cats = slug_categories(slug)
            if not cats:
                continue
            # Find best unused image matching one of the preferred cats
            best_idx = None
            best_score = -1
            for cat in cats:
                for i, item in enumerate(pool):
                    if item["sha1"] in used_sha1:
                        continue
                    if item["topic"] != cat:
                        continue
                    if item["score"] > best_score:
                        best_score = item["score"]
                        best_idx = i
                        break  # take first (highest-scored) in this cat
                if best_idx is not None:
                    break
            if best_idx is None:
                continue
            item = pool[best_idx]
            used_sha1.add(item["sha1"])
            url = copy_asset(item["src_path"], "shared", item["fname"])
            page_assigned[slug].append(figure_html(url, item["caption"]))

    # Phase 4: inject into pages
    n_pages = 0
    n_figs = 0
    for slug in pages:
        path = page_path(slug)
        if not path.exists():
            continue
        if slug in paper_assigned:
            htmls = paper_assigned[slug]
        else:
            htmls = page_assigned.get(slug, [])
        if not htmls:
            continue
        if inject(path, htmls):
            n_pages += 1
            n_figs += len(htmls)

    print(f"Done. {n_pages} pages got figures. Total {n_figs} placements.")
    print(f"  paper-figures: {paper_used_count} placements across {len(paper_assigned)} update pages")
    print(f"  pool: {len(pool)} images, {len(used_sha1)} used")


if __name__ == "__main__":
    main()
