#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEARCH_INDEX = ROOT / "search-index.json"
OUT = ROOT / "private-figures" / "page-image-generation-v2"
PUBLIC = ROOT / "assets" / "img" / "page-generated-v2"


PILOT_URLS = [
    "/간암-치료-선택/",
    "/B형간염-검사결과/",
    "/지방간-정밀검사/",
    "/간경변-식도정맥류/",
    "/간섬유화스캔-수치/",
    "/자가면역간염-진단/",
    "/간양성종양-진단/",
]


CATEGORY_STYLES = {
    "hcc": {
        "ko": "간암",
        "category2": "진단·치료 의사결정",
        "category3": "절제·색전·방사선·전신치료 선택",
        "palette": "deep navy, arterial red, warm amber, clean white",
        "top": "radiology-forward oncologic editorial image with a liver CT/MRI focal lesion and treatment decision cues",
        "lower": "specific HCC treatment figure, showing liver tumor and locoregional/systemic treatment paths without heavy text",
    },
    "hbv": {
        "ko": "B형간염",
        "category2": "혈청표지자·자연사",
        "category3": "HBsAg·HBeAg·anti-HBs 검사결과 해석",
        "palette": "clinical blue, violet, white, small amber accents",
        "top": "HBV virions and hepatocyte lifecycle with cccDNA concept, clean molecular-medical style",
        "lower": "serology interpretation figure using tubes, marker bands, and timeline-like visual structure",
    },
    "masld": {
        "ko": "지방간",
        "category2": "섬유화 위험층화",
        "category3": "Fibroscan·FIB-4 정밀검사 대상",
        "palette": "sage green, soft yellow fat droplets, teal, white",
        "top": "metabolic liver disease image with fatty liver, fibrosis gradient, obesity/diabetes cues, hopeful tone",
        "lower": "FibroScan or ultrasound elastography figure measuring liver stiffness in MASLD",
    },
    "cirrhosis": {
        "ko": "간경변",
        "category2": "문맥고혈압 합병증",
        "category3": "식도정맥류와 출혈 예방",
        "palette": "slate blue, venous blue, muted red, parchment white",
        "top": "cirrhotic nodular liver with portal vein pressure and esophageal varices concept, serious but calm",
        "lower": "endoscopy-like esophageal varices band ligation or portal hypertension figure, medically recognizable",
    },
    "lft": {
        "ko": "간수치·진단검사",
        "category2": "섬유화 검사",
        "category3": "Fibroscan kPa 수치 해석",
        "palette": "teal, cyan, white, laboratory gray",
        "top": "diagnostic testing image with liver stiffness, lab dashboard, ultrasound probe, clean precision mood",
        "lower": "elastography result figure with liver, probe, stiffness wave, simple graph; no fake readable text",
    },
    "autoimmune": {
        "ko": "자가면역간염",
        "category2": "면역·조직 진단",
        "category3": "ALT·IgG·자가항체·조직 4축 진단",
        "palette": "deep plum, immune violet, teal, pale pink pathology",
        "top": "immune cells and antibodies targeting hepatocytes, with subtle portal inflammation/pathology texture",
        "lower": "histology-inspired interface hepatitis figure with antibody and IgG visual cues, elegant and accurate",
    },
    "benign": {
        "ko": "간 양성종양",
        "category2": "영상 감별",
        "category3": "혈관종·FNH·선종·낭종 감별",
        "palette": "calm navy, soft teal, pale green, warm beige",
        "top": "calm radiology comparison image of benign liver lesions on MRI/ultrasound, reassuring clinical tone",
        "lower": "multi-panel benign lesion figure showing hemangioma, cyst, FNH-like central scar, adenoma risk cue",
    },
}


PILOT_MAP = {
    "/간암-치료-선택/": ("hcc", ["절제술", "TACE", "SBRT", "면역치료", "BCLC"]),
    "/B형간염-검사결과/": ("hbv", ["HBsAg", "HBeAg", "anti-HBs", "anti-HBc", "HBV DNA"]),
    "/지방간-정밀검사/": ("masld", ["MASLD", "Fibroscan", "FIB-4", "MASH", "대사위험"]),
    "/간경변-식도정맥류/": ("cirrhosis", ["식도정맥류", "문맥고혈압", "내시경", "출혈", "베타차단제"]),
    "/간섬유화스캔-수치/": ("lft", ["Fibroscan", "kPa", "간섬유화", "FIB-4", "공복검사"]),
    "/자가면역간염-진단/": ("autoimmune", ["ALT", "IgG", "ANA", "ASMA", "간생검"]),
    "/간양성종양-진단/": ("benign", ["혈관종", "FNH", "간선종", "간낭종", "MRI"]),
}


def slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9가-힣]+", "-", text).strip("-")
    return text[:48]


def prompt(kind: str, style: dict, title: str, keywords: list[str]) -> str:
    aspect = "16:9 horizontal hero image" if kind == "top" else "4:3 educational figure"
    subject = style[kind]
    return f"""Use case: scientific-educational
Asset type: drshin.kr {kind} image pilot, {aspect}, no watermark
Page title: {title}
Category path: {style['ko']} - {style['category2']} - {style['category3']}
Keywords: {', '.join(keywords)}
Visual direction: {subject}
Style: premium medical editorial illustration with selective realistic medical texture, {style['palette']}; varied composition; visually beautiful enough for a physician-authored patient guide.
Medical specificity: show the actual disease concept or clinical tool. This must not look like a generic liver icon or summary slide.
Composition: one dominant meaningful medical scene, carefully lit, layered depth, crisp details, generous breathing room for responsive web layout.
Text policy: avoid readable text except tiny abstract marks; no fake labels, no logo, no brand name.
Avoid: repeated template layout, cartoonish clipart, gray gradient background, decorative-only shapes, gore, identifiable patient face, hospital branding.
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "prompts").mkdir(exist_ok=True)
    (OUT / "images").mkdir(exist_ok=True)
    (PUBLIC / "pilot").mkdir(parents=True, exist_ok=True)

    data = json.loads(SEARCH_INDEX.read_text(encoding="utf-8-sig"))
    by_url = {item["u"]: item for item in data}
    rows = []
    for i, url in enumerate(PILOT_URLS, 1):
        item = by_url[url]
        cat, keywords = PILOT_MAP[url]
        style = CATEGORY_STYLES[cat]
        base = f"pilot-{i:02d}-{cat}-{slug(item['t'])}"
        for kind in ["top", "lower"]:
            p = prompt(kind, style, item["t"], keywords)
            (OUT / "prompts" / f"{base}-{kind}.txt").write_text(p, encoding="utf-8")
        rows.append({
            "pilot_id": f"pilot-{i:02d}",
            "page_url": url,
            "title": item["t"],
            "category1": style["ko"],
            "category2": style["category2"],
            "category3": style["category3"],
            "keywords": ";".join(keywords),
            "top_prompt": f"private-figures/page-image-generation-v2/prompts/{base}-top.txt",
            "lower_prompt": f"private-figures/page-image-generation-v2/prompts/{base}-lower.txt",
            "top_image": f"private-figures/page-image-generation-v2/images/{base}-top.png",
            "lower_image": f"private-figures/page-image-generation-v2/images/{base}-lower.png",
            "public_top_image": f"/assets/img/page-generated-v2/pilot/{base}-top.png",
            "public_lower_image": f"/assets/img/page-generated-v2/pilot/{base}-lower.png",
            "base_name": base,
        })

    fields = list(rows[0].keys())
    with (OUT / "pilot_manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (OUT / "pilot_manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "style_masters.json").write_text(json.dumps(CATEGORY_STYLES, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Page Image Generation v2 Pilot\n\n"
        "This is the replacement pilot for the rejected v1 placeholder images.\n"
        "The pilot uses seven representative detail pages, one per major topic family.\n\n"
        "Files for Claude:\n"
        "- `pilot_manifest.csv` / `pilot_manifest.json`: page, category, keyword, prompt, and image paths.\n"
        "- `style_masters.json`: category-level visual style masters.\n"
        "- `prompts/*.txt`: exact generation prompts.\n"
        "- `images/*.png`: generated pilot images after image generation is complete.\n\n"
        "Important: v1 under `private-figures/page-image-generation/` is rejected and should not be used for the site.\n",
        encoding="utf-8",
    )
    print(json.dumps({"pilot_pages": len(rows), "expected_images": len(rows) * 2, "out": str(OUT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
