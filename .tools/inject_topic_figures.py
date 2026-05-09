"""For pages without real figures yet, inject 1-2 images from medicine-topics
by category match. Filters out figures with low-quality captions or supplemental
sub-figures. Uses globally-unique selection so each figure appears on only one
page.
"""
from __future__ import annotations
import csv
import html as htmllib
import re
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
MEDTOPICS = ROOT / "private-figures" / "medicine-topics"
ASSETS = ROOT / "assets" / "img" / "topics"

OPEN = "<!-- topicfig -->"
CLOSE = "<!-- /topicfig -->"
BLOCK_RE = re.compile(re.escape(OPEN) + r".*?" + re.escape(CLOSE), re.DOTALL)

# Slug → preferred topic categories (in order)
SLUG_TOPICS = {
    "B형간염": ["viral-hepatitis-hbv-hcv"],
    "B형간염-간암검진": ["viral-hepatitis-hbv-hcv", "diagnostics-biomarkers-imaging-ai"],
    "B형간염-재활성화": ["viral-hepatitis-hbv-hcv"],
    "PIVKA-II-간암마커": ["diagnostics-biomarkers-imaging-ai", "hcc-oncology-immunotherapy"],
    "알파태아단백": ["diagnostics-biomarkers-imaging-ai", "hcc-oncology-immunotherapy"],
    "간수치-종류-차이": ["diagnostics-biomarkers-imaging-ai"],
    "간암-BCLC병기": ["hcc-oncology-immunotherapy"],
    "간암-치료-선택": ["hcc-oncology-immunotherapy"],
    "간암-면역치료-1차": ["hcc-oncology-immunotherapy"],
    "간암-식이-일상": ["hcc-oncology-immunotherapy"],
    "간암-진단-첫외래": ["hcc-oncology-immunotherapy", "diagnostics-biomarkers-imaging-ai"],
    "대사이상지방간-MASLD": ["masld-mash-nafld-metabolic"],
    "지방간-lean-MASLD": ["masld-mash-nafld-metabolic"],
    "지방간-간암": ["masld-mash-nafld-metabolic", "hcc-oncology-immunotherapy"],
    "지방간염-MASH": ["masld-mash-nafld-metabolic"],
    "updates/HIMALAYA-durvalumab-tremelimumab-NEJM-Evid-2022": ["hcc-oncology-immunotherapy"],
    "updates/IMbrave150-atezolizumab-bevacizumab-NEJM-2020": ["hcc-oncology-immunotherapy"],
    "updates/preemptive-TIPS-식도정맥류-출혈": ["cirrhosis-portal-hypertension"],
    "updates/Shin-AI-CT-HCC-CHB-JHep-2025": ["diagnostics-biomarkers-imaging-ai", "hcc-oncology-immunotherapy"],
}

# Filename / title patterns that indicate non-public / supplemental / personal items
SKIP_PATTERNS = [
    "not_for_submit", "Supp", "supplement", "_BW",
    "면허증", "서명", "signature", "CV", "이력서",
    "수정", "_바탕", "background", "_data_", "raw_",
]

# Already-handled slugs (skip)
SKIP_SLUGS = {"연구", "소개", "논문", "guide", "updates-index", "케이스",
              "B형간염", "간경화", "간암", "지방간", "간수치"}


def esc(s: str) -> str:
    return htmllib.escape(s or "")


def is_useful_caption(title: str, source_path: str) -> bool:
    if not title:
        return True  # empty caption OK; we'll show figure without caption
    for p in SKIP_PATTERNS:
        if p.lower() in title.lower() or p.lower() in source_path.lower():
            return False
    # Reject titles that are mostly technical (e.g., 전부 알파벳+숫자만)
    if len(title) < 4:
        return False
    # Reject obviously raw filenames
    if re.fullmatch(r"[\w\d_\-]+", title) and "_" in title and len(title) > 30:
        return False
    return True


def load_figures_by_topic() -> dict[str, list[dict]]:
    by_t: dict[str, list[dict]] = {}
    with (MEDTOPICS / "manifest.csv").open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            ext = row.get("ext", "").lower()
            if ext not in (".png", ".jpg", ".jpeg", ".svg"):
                continue
            title = row.get("source_title", "")
            sp = row.get("source_path", "")
            if not is_useful_caption(title, sp):
                continue
            try:
                w = int(row.get("width", "0") or 0)
                h = int(row.get("height", "0") or 0)
            except ValueError:
                w = h = 0
            # Skip very tall/narrow technical SVG fragments
            if w and h and (w > 14000 or h > 14000):
                # Huge images — usually multi-panel; ok but expensive. Keep but downscale via CSS.
                pass
            row["score_f"] = float(row.get("score", "0") or 0)
            by_t.setdefault(row.get("topic", ""), []).append(row)
    for t in by_t:
        by_t[t].sort(key=lambda r: -r["score_f"])
    return by_t


def page_path_for(slug: str) -> Path:
    if slug == "index":
        return ROOT / "index.html"
    if slug.startswith("updates/"):
        return ROOT / "updates" / slug.split("/", 1)[1] / "index.html"
    return ROOT / slug / "index.html"


def asset_url(slug_safe: str, fname: str) -> str:
    return "/" + "/".join(quote(p, safe="") for p in ("assets", "img", "topics", slug_safe, fname))


def slug_safe(slug: str) -> str:
    return slug.replace("/", "_")


def figure_html(slug: str, fig_row: dict) -> str | None:
    dest_file = fig_row.get("dest_file", "")
    src = MEDTOPICS / dest_file
    if not src.exists():
        return None
    fname = src.name
    sslug = slug_safe(slug)
    dst_dir = ASSETS / sslug
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / fname
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
        shutil.copy2(src, dst)
    url = asset_url(sslug, fname)
    title = esc(fig_row.get("source_title", ""))
    sp = fig_row.get("source_path", "")
    # Extract paper folder name as origin hint
    parts = sp.split("/")
    origin = ""
    if len(parts) >= 2 and parts[0] == "0.Research":
        origin = parts[1].replace("_", " ")
    cap = title
    if origin:
        cap += f' <span class="fig-meta">· {esc(origin)}</span>'
    return (
        f'<figure class="real-fig">'
        f'<img src="{url}" alt="{title}" loading="lazy">'
        f'<figcaption>{cap}</figcaption>'
        f'</figure>'
    )


def has_real_figs(html_path: Path) -> bool:
    if not html_path.exists():
        return False
    text = html_path.read_text(encoding="utf-8")
    return ("<!-- realfig -->" in text or
            "<!-- paper-figs -->" in text)


def find_h2_positions(text: str) -> list[int]:
    main_start = text.find("<main")
    if main_start < 0:
        main_start = 0
    refs = text.find('<section class="references-block">', main_start)
    end = refs if refs > 0 else text.find("</main>", main_start)
    if end < 0:
        end = len(text)
    return [main_start + m.start() for m in re.finditer(r"<h2\b", text[main_start:end])]


def inject(html_path: Path, figs_html: list[str]) -> bool:
    text = html_path.read_text(encoding="utf-8")
    text = BLOCK_RE.sub("", text).rstrip() + "\n"
    if not figs_html:
        html_path.write_text(text, encoding="utf-8")
        return False
    h2_positions = find_h2_positions(text)
    insertions: list[tuple[int, str]] = []
    if len(h2_positions) >= 2:
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


def main():
    by_topic = load_figures_by_topic()
    used_sha1: set[str] = set()
    n_ok = 0
    for slug, topics in SLUG_TOPICS.items():
        if slug in SKIP_SLUGS:
            continue
        page = page_path_for(slug)
        if not page.exists():
            print(f"  ! missing: {slug}")
            continue
        # Try to pick 1-2 fresh figures across the preferred topics
        picks = []
        for topic in topics:
            for f in by_topic.get(topic, []):
                if f["sha1"] in used_sha1:
                    continue
                picks.append(f)
                used_sha1.add(f["sha1"])
                if len(picks) >= 2:
                    break
            if len(picks) >= 2:
                break
        figs_html = []
        for f in picks:
            fh = figure_html(slug, f)
            if fh:
                figs_html.append(fh)
        if not figs_html:
            print(f"  no figures available: {slug}")
            continue
        if inject(page, figs_html):
            n_ok += 1
            titles = [f.get("source_title", "?")[:40] for f in picks]
            print(f"  +{len(figs_html)}: {slug}  ←  {titles}")
        else:
            print(f"  inject fail: {slug}")
    print(f"Done. {n_ok} pages got topic figures.")


if __name__ == "__main__":
    main()
