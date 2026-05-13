#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent.parent
PRIVATE = ROOT / "private-figures"
CANONICAL_MANIFEST = PRIVATE / "manifest.csv"
PERSONAL_MANIFEST = PRIVATE / "personal-web-figures" / "manifest.csv"
AUDIT = PRIVATE / "visual-label-audit"
FONT = Path("C:/Windows/Fonts/malgun.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/malgunbd.ttf")


VISUAL_LABEL_KO = {
    "radiology_ct_mri": "CT/MRI 영상",
    "ultrasound_elastography": "초음파/탄성도 영상",
    "endoscopy": "내시경 사진",
    "histology_pathology": "조직병리 현미경 사진",
    "gross_pathology": "육안 병리/표본 사진",
    "survival_curve": "Kaplan-Meier/생존곡선",
    "statistical_plot": "통계 그래프/forest plot",
    "algorithm_flowchart": "진단·치료 알고리즘/flowchart",
    "mechanism_diagram": "기전/병태생리 도식",
    "virology_diagram": "바이러스 구조/lifecycle 도식",
    "serology_lab": "혈청표지자/검사·분자실험 결과",
    "treatment_schema": "치료 전략/약제/시술 schema",
    "text_table_slide": "표/텍스트 중심 슬라이드",
    "anatomy_diagram": "해부학/혈관·담도 도식",
    "diet_lifestyle": "식이·운동·생활습관 이미지",
    "clinical_photo": "임상 사진",
    "nonmedical_context": "비의학/맥락용 이미지",
    "table": "표/요약표",
    "unknown": "분류 불확실",
}


TOPIC_LABEL_KO = {
    "hcc": "간세포암/간암",
    "hbv": "B형간염",
    "hcv": "C형간염",
    "hdv": "D형간염",
    "viral_hepatitis": "바이러스 간염",
    "masld_mash": "MASLD/MASH/지방간",
    "cirrhosis_portal_htn": "간경변/문맥고혈압",
    "autoimmune_cholestatic": "자가면역·담즙정체 간질환",
    "benign_liver_lesions": "양성 간병변",
    "liver_tests_diagnostics": "간수치/진단/섬유화 평가",
    "acute_liver_failure_transplant": "급성간부전/간이식",
    "anatomy_intervention": "간 해부/시술",
    "general_hepatology": "일반 간질환",
}


TOPIC_RULES = [
    ("hcc", [
        "hepatocellular", "hcc", "간세포암", "간암", "bclc", "li-rads", "lirads",
        "atezolizumab", "bevacizumab", "durvalumab", "tremelimumab", "sorafenib",
        "lenvatinib", "tace", "radioembolization", "y90", "ablation", "rfa", "mwa",
    ]),
    ("hbv", ["hepatitis b", "hbv", "hbsag", "hbeag", "anti-hbc", "anti-hbs", "cccdna", "b형간염", "b型肝炎", "乙型肝炎"]),
    ("hcv", ["hepatitis c", "hcv", "anti-hcv", "ns3", "ns5a", "ns5b", "daa", "svr", "c형간염", "c型肝炎", "丙型肝炎"]),
    ("hdv", ["hepatitis d", "hdv", "delta hepatitis", "d형간염"]),
    ("masld_mash", ["masld", "nafld", "nash", "mash", "steatosis", "steatohepatitis", "fatty liver", "지방간", "ballooning", "resmetirom", "semaglutide", "glp-1"]),
    ("cirrhosis_portal_htn", ["cirrhosis", "portal hypertension", "varices", "varix", "ascites", "paracentesis", "tips", "encephalopathy", "hepatorenal", "meld", "child-pugh", "간경변", "복수", "정맥류", "문맥"]),
    ("autoimmune_cholestatic", ["autoimmune hepatitis", "aih", "primary biliary", "pbc", "primary sclerosing", "psc", "cholangitis", "igG4", "igg4", "담관염", "자가면역", "pbc", "psc"]),
    ("benign_liver_lesions", ["hemangioma", "fnh", "focal nodular", "adenoma", "hca", "cyst", "focal fat", "혈관종", "간선종", "낭종"]),
    ("liver_tests_diagnostics", ["fib-4", "fibroscan", "elastography", "liver stiffness", "bilirubin", "alp", "ggt", "ast", "alt", "biopsy", "metavir", "ishak", "간수치", "빌리루빈"]),
    ("acute_liver_failure_transplant", ["acute liver failure", "aclf", "transplant", "king's college", "liver transplantation", "간이식", "급성간부전"]),
    ("anatomy_intervention", ["portal vein", "hepatic artery", "bile duct", "liver anatomy", "hepatic vein", "간동맥", "문맥", "담도", "해부"]),
]


VISUAL_TEXT_RULES = [
    ("survival_curve", ["kaplan", "survival", "overall survival", "progression-free", "pfs", "os curve", "hazard ratio", "log-rank"]),
    ("statistical_plot", ["forest plot", "odds ratio", "hazard ratio", "confidence interval", "auc", "roc", "volcano", "p value", "regression", "nomogram"]),
    ("algorithm_flowchart", ["algorithm", "flow chart", "flowchart", "criteria", "guideline", "decision", "management", "diagnostic approach", "treatment algorithm", "screening process"]),
    ("treatment_schema", ["atezolizumab", "bevacizumab", "durvalumab", "tremelimumab", "resmetirom", "sorafenib", "lenvatinib", "tace", "tips", "ablation", "radioembolization", "transplant", "immune checkpoint"]),
    ("virology_diagram", ["virus", "viral", "virion", "life cycle", "lifecycle", "replication", "cccDNA", "capsid", "envelope", "polymerase", "hbsag", "ns5a"]),
    ("serology_lab", ["serology", "hbsag", "anti-hbs", "anti-hbc", "hbeag", "anti-hcv", "rna", "pcr", "rapid test", "assay", "elisa", "western blot", "immunoblot", "gel", "qpcr"]),
    ("radiology_ct_mri", ["ct", "computed tomography", "mri", "magnetic resonance", "arterial phase", "portal venous", "washout", "li-rads", "contrast-enhanced"]),
    ("ultrasound_elastography", ["ultrasound", "ultrasonography", "sonography", "elastography", "fibroscan", "shear wave", "ceus"]),
    ("endoscopy", ["endoscopy", "gastroscopy", "varices", "banding", "esophageal", "gastric varices", "red wale"]),
    ("histology_pathology", ["histology", "micrograph", "biopsy", "h&e", "stain", "pathology", "fibrosis", "mallory", "ballooning"]),
    ("gross_pathology", ["gross", "specimen", "autopsy", "resected", "macroscopic"]),
    ("anatomy_diagram", ["anatomy", "portal vein", "hepatic artery", "bile duct", "lobule", "vascular anatomy"]),
    ("diet_lifestyle", ["diet", "mediterranean", "food", "exercise", "walking", "weight loss", "lifestyle", "beer", "turmeric", "licorice", "glycyrrhiza"]),
    ("table", ["table ", "baseline characteristics", "characteristics of", "multivariate", "univariate"]),
    ("text_table_slide", ["slide", "seminar", "lecture", "baseline characteristics", "table ", "supplementary table"]),
    ("clinical_photo", ["patient", "symptom", "abdominal pain", "ascites", "distension", "fever", "fatigue", "vomiting", "jaundice", "clinical photo"]),
    ("nonmedical_context", ["flag", "portrait", "professor", "snu", "snuh", "snu h", "seoul national", "bangladesh", "sudan", "germany", "india", "united kingdom", "american flag"]),
]


MANUAL_VISUAL_OVERRIDES = {
    # Contact-sheet verified corrections. These images carried broad lecture
    # context terms, so visual classification needs a human-fixed label.
    "img_00054": "mechanism_diagram",
    "img_00085": "algorithm_flowchart",
    "img_00210": "mechanism_diagram",
    "img_00224": "algorithm_flowchart",
    "img_00234": "text_table_slide",
    "img_00235": "text_table_slide",
    "img_00236": "treatment_schema",
    "img_00335": "text_table_slide",
    "img_00366": "treatment_schema",
    "img_00369": "treatment_schema",
    "img_00443": "text_table_slide",
    "img_00459": "statistical_plot",
    "img_00461": "statistical_plot",
    "img_00520": "treatment_schema",
    "img_00524": "text_table_slide",
    "img_00618": "clinical_photo",
    "img_00621": "clinical_photo",
    "img_00622": "clinical_photo",
    "img_00623": "clinical_photo",
    "img_00717": "histology_pathology",
    "img_00723": "statistical_plot",
    "img_00724": "statistical_plot",
    "img_00751": "text_table_slide",
    "img_00832": "mechanism_diagram",
    "img_00995": "text_table_slide",
    "img_01409": "text_table_slide",
    "img_01469": "text_table_slide",
    "img_01652": "statistical_plot",
    "img_02561": "algorithm_flowchart",
    "img_02684": "treatment_schema",
    "img_02693": "text_table_slide",
    "img_02804": "clinical_photo",
    "img_03617": "mechanism_diagram",
    "img_03627": "mechanism_diagram",
    "img_03637": "endoscopy",
    "img_03642": "endoscopy",
    "img_03757": "endoscopy",
    "img_03758": "endoscopy",
    "img_03760": "endoscopy",
    "img_03761": "endoscopy",
    "img_03770": "radiology_ct_mri",
    "img_03817": "endoscopy",
    "img_03818": "histology_pathology",
    "img_03821": "mechanism_diagram",
    "img_03833": "endoscopy",
    "img_03840": "histology_pathology",
    "img_03842": "anatomy_diagram",
    "img_03853": "radiology_ct_mri",
    "img_03854": "radiology_ct_mri",
    "img_03883": "histology_pathology",
    "img_03884": "ultrasound_elastography",
    "img_03886": "clinical_photo",
    "img_03887": "histology_pathology",
    "img_03906": "gross_pathology",
    "pwf_00012": "gross_pathology",
    "pwf_00042": "algorithm_flowchart",
    "pwf_00044": "statistical_plot",
    "pwf_00047": "algorithm_flowchart",
    "pwf_00049": "statistical_plot",
    "pwf_00050": "statistical_plot",
    "pwf_00056": "algorithm_flowchart",
    "pwf_00057": "treatment_schema",
    "pwf_00062": "statistical_plot",
    "pwf_00063": "algorithm_flowchart",
    "pwf_00087": "virology_diagram",
    "pwf_00101": "histology_pathology",
    "pwf_00103": "histology_pathology",
    "pwf_00104": "histology_pathology",
    "pwf_00106": "statistical_plot",
    "pwf_00107": "algorithm_flowchart",
    "pwf_00108": "statistical_plot",
    "pwf_00109": "statistical_plot",
    "pwf_00111": "statistical_plot",
    "pwf_00112": "statistical_plot",
    "pwf_00114": "statistical_plot",
    "pwf_00115": "histology_pathology",
    "pwf_00119": "statistical_plot",
    "pwf_00120": "statistical_plot",
    "pwf_00121": "histology_pathology",
    "pwf_00128": "mechanism_diagram",
    "pwf_00148": "statistical_plot",
    "pwf_00149": "radiology_ct_mri",
    "pwf_00175": "radiology_ct_mri",
    "pwf_00197": "mechanism_diagram",
}

MANUAL_VISUAL_OVERRIDES.update({
    "img_00020": "survival_curve",
    "img_00021": "mechanism_diagram",
    "img_00103": "histology_pathology",
    "img_00106": "histology_pathology",
    "img_00111": "histology_pathology",
    "img_00112": "histology_pathology",
    "img_00113": "histology_pathology",
    "img_00355": "gross_pathology",
    "img_00357": "mechanism_diagram",
    "img_00324": "text_table_slide",
    "img_00326": "text_table_slide",
    "img_00329": "text_table_slide",
    "img_00358": "treatment_schema",
    "img_00365": "treatment_schema",
    "img_00368": "treatment_schema",
    "img_00371": "statistical_plot",
    "img_00372": "statistical_plot",
    "img_00558": "radiology_ct_mri",
    "img_00565": "text_table_slide",
    "img_00566": "treatment_schema",
    "img_00666": "radiology_ct_mri",
    "img_00667": "clinical_photo",
    "img_00710": "histology_pathology",
    "img_00711": "histology_pathology",
    "img_00741": "nonmedical_context",
    "img_00996": "clinical_photo",
    "img_01028": "statistical_plot",
    "img_01035": "text_table_slide",
    "img_01051": "anatomy_diagram",
    "img_01206": "mechanism_diagram",
    "img_01247": "text_table_slide",
    "img_01250": "text_table_slide",
    "img_01251": "text_table_slide",
    "img_01253": "text_table_slide",
    "img_01254": "text_table_slide",
    "img_01259": "text_table_slide",
    "img_01260": "text_table_slide",
    "img_01265": "text_table_slide",
    "img_01268": "text_table_slide",
    "img_01270": "text_table_slide",
    "img_01271": "text_table_slide",
    "img_01272": "text_table_slide",
    "img_01273": "text_table_slide",
    "img_01274": "text_table_slide",
    "img_01276": "text_table_slide",
    "img_01279": "text_table_slide",
    "img_01283": "text_table_slide",
    "img_01284": "text_table_slide",
    "img_01286": "text_table_slide",
    "img_01288": "text_table_slide",
    "img_01289": "text_table_slide",
    "img_01291": "text_table_slide",
    "img_01292": "text_table_slide",
    "img_01293": "text_table_slide",
    "img_01295": "text_table_slide",
    "img_01297": "text_table_slide",
    "img_01298": "text_table_slide",
    "img_01479": "text_table_slide",
    "img_01589": "virology_diagram",
    "img_01604": "endoscopy",
    "img_01608": "gross_pathology",
    "img_01683": "text_table_slide",
    "img_01722": "clinical_photo",
    "img_01767": "histology_pathology",
    "img_01768": "histology_pathology",
    "img_02361": "mechanism_diagram",
    "img_02448": "ultrasound_elastography",
    "img_02454": "radiology_ct_mri",
    "img_02481": "nonmedical_context",
    "img_02486": "mechanism_diagram",
    "img_02549": "nonmedical_context",
    "img_02555": "anatomy_diagram",
    "img_02556": "anatomy_diagram",
    "img_02557": "anatomy_diagram",
    "img_02675": "diet_lifestyle",
    "img_02699": "clinical_photo",
    "img_02702": "clinical_photo",
    "img_02710": "text_table_slide",
    "img_02774": "histology_pathology",
    "img_02824": "nonmedical_context",
    "img_03515": "mechanism_diagram",
    "img_03528": "statistical_plot",
    "img_03546": "nonmedical_context",
    "img_03547": "nonmedical_context",
    "img_03550": "nonmedical_context",
    "img_03557": "gross_pathology",
    "img_03565": "diet_lifestyle",
    "img_03567": "histology_pathology",
    "img_03570": "clinical_photo",
    "img_03588": "clinical_photo",
    "img_03744": "endoscopy",
    "img_03746": "endoscopy",
    "img_03777": "endoscopy",
    "img_03780": "endoscopy",
    "img_03829": "gross_pathology",
    "img_03831": "gross_pathology",
    "img_03890": "anatomy_diagram",
    "img_03893": "endoscopy",
    "img_03894": "endoscopy",
    "pwf_00001": "algorithm_flowchart",
    "pwf_00032": "histology_pathology",
    "pwf_00038": "clinical_photo",
    "pwf_00123": "statistical_plot",
    "pwf_00160": "mechanism_diagram",
})


def font(size: int, bold: bool = False):
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def image_features(path: Path) -> dict[str, float | int | str]:
    try:
        im = Image.open(path)
        im = ImageOps.exif_transpose(im.convert("RGB"))
        w, h = im.size
        small = im.resize((96, 96), Image.Resampling.LANCZOS)
        gray = small.convert("L")
        stat = ImageStat.Stat(small)
        mean_r, mean_g, mean_b = stat.mean
        sat = ImageStat.Stat(small.convert("HSV").getchannel("S")).mean[0]
        val = ImageStat.Stat(small.convert("HSV").getchannel("V")).mean[0]
        entropy = gray.entropy()
        edge = ImageStat.Stat(gray.filter(ImageFilter.FIND_EDGES)).mean[0]
        pixels = list(small.getdata())
        n = max(1, len(pixels))
        white = sum(1 for r, g, b in pixels if r > 235 and g > 235 and b > 235) / n
        dark = sum(1 for r, g, b in pixels if r < 45 and g < 45 and b < 45) / n
        pink = sum(1 for r, g, b in pixels if r > 150 and b > 110 and g < 170 and r > g * 1.08) / n
        red_orange = sum(1 for r, g, b in pixels if r > 130 and g < 120 and b < 110) / n
        grayscale = sum(1 for r, g, b in pixels if max(r, g, b) - min(r, g, b) < 18) / n
        return {
            "width": w,
            "height": h,
            "aspect": round(max(w / max(h, 1), h / max(w, 1)), 2),
            "mean_r": round(mean_r, 1),
            "mean_g": round(mean_g, 1),
            "mean_b": round(mean_b, 1),
            "saturation": round(sat, 1),
            "brightness": round(val, 1),
            "entropy": round(entropy, 2),
            "edge": round(edge, 1),
            "white_ratio": round(white, 3),
            "dark_ratio": round(dark, 3),
            "pink_ratio": round(pink, 3),
            "red_orange_ratio": round(red_orange, 3),
            "grayscale_ratio": round(grayscale, 3),
            "image_error": "",
        }
    except Exception as exc:
        return {
            "width": 0,
            "height": 0,
            "aspect": 0,
            "mean_r": 0,
            "mean_g": 0,
            "mean_b": 0,
            "saturation": 0,
            "brightness": 0,
            "entropy": 0,
            "edge": 0,
            "white_ratio": 0,
            "dark_ratio": 0,
            "pink_ratio": 0,
            "red_orange_ratio": 0,
            "grayscale_ratio": 0,
            "image_error": str(exc),
        }


def text_scores(text: str, rules: list[tuple[str, list[str]]]) -> Counter:
    low = text.lower()
    scores = Counter()
    for label, terms in rules:
        for term in terms:
            if term.lower() in low:
                scores[label] += 1
    return scores


def infer_visual_type(text: str, feats: dict) -> tuple[str, int, list[str]]:
    reasons: list[str] = []
    scores = text_scores(text, VISUAL_TEXT_RULES)
    for k, v in scores.items():
        if v:
            reasons.append(f"text:{k}={v}")

    # Actual-image heuristics. These intentionally override generic source labels.
    pink = float(feats["pink_ratio"])
    red = float(feats["red_orange_ratio"])
    gray = float(feats["grayscale_ratio"])
    dark = float(feats["dark_ratio"])
    white = float(feats["white_ratio"])
    sat = float(feats["saturation"])
    edge = float(feats["edge"])

    if red > 0.16 and sat > 62:
        scores["endoscopy"] += 4
        reasons.append(f"visual:red_orange={red}")
    if pink > 0.24:
        scores["histology_pathology"] += 4
        reasons.append(f"visual:pink={pink}")
    if sat > 105 and white < 0.08 and red < 0.14:
        scores["histology_pathology"] += 4
        reasons.append(f"visual:fluorescent_micrograph={sat}/{white}")
    if gray > 0.72 and dark > 0.20:
        scores["radiology_ct_mri"] += 4
        reasons.append(f"visual:gray_dark={gray}/{dark}")
    if gray > 0.88 and white < 0.25 and sat < 32:
        scores["radiology_ct_mri"] += 5
        reasons.append(f"visual:grayscale_scan={gray}")
    if gray > 0.60 and dark > 0.35 and "ultrasound" in text.lower():
        scores["ultrasound_elastography"] += 4
        reasons.append("visual+text:ultrasound")
    if white > 0.48:
        scores["text_table_slide"] += 2
        reasons.append(f"visual:white_slide={white}")
    if white > 0.58 and edge > 10:
        scores["text_table_slide"] += 3
        if any(t in text.lower() for t in ["algorithm", "flowchart", "flow chart", "criteria", "guideline", "decision"]):
            scores["algorithm_flowchart"] += 4
        if any(t in text.lower() for t in ["kaplan", "survival", "hazard ratio", "forest", "auc", "roc", "odds ratio", "p value"]):
            scores["statistical_plot"] += 3
        reasons.append(f"visual:white_texty={white}")
    if sat > 75 and white > 0.30 and scores["virology_diagram"]:
        scores["virology_diagram"] += 2
        reasons.append("visual:color_diagram")
    if not scores:
        return "unknown", 35, ["no strong text/visual signal"]

    # If actual pixel evidence says image/photo, do not let surrounding lecture text
    # overrule it as a treatment schema.
    low = text.lower()
    if scores["nonmedical_context"] >= 2:
        label, score = "nonmedical_context", scores["nonmedical_context"]
    elif scores["diet_lifestyle"] >= 1 and any(t in low for t in ["mediterranean", "food", "exercise", "walking", "weight loss", "lifestyle", "beer", "turmeric", "licorice", "glycyrrhiza"]):
        label, score = "diet_lifestyle", scores["diet_lifestyle"]
    elif white > 0.58 and edge > 10:
        if scores["survival_curve"] >= 1:
            label, score = "survival_curve", scores["survival_curve"] + 2
        elif scores["statistical_plot"] >= 1:
            label, score = "statistical_plot", scores["statistical_plot"] + 2
        elif scores["algorithm_flowchart"] >= 1:
            label, score = "algorithm_flowchart", scores["algorithm_flowchart"] + 2
        elif scores["virology_diagram"] >= 2:
            label, score = "virology_diagram", scores["virology_diagram"]
        elif scores["serology_lab"] >= 2:
            label, score = "serology_lab", scores["serology_lab"]
        else:
            label, score = "text_table_slide", scores["text_table_slide"]
    elif red > 0.16 and sat > 62 and any(t in low for t in ["endoscopy", "gastroscopy", "varices", "banding", "esophageal", "gastric"]):
        label, score = "endoscopy", scores["endoscopy"]
    elif pink > 0.20:
        label, score = "histology_pathology", scores["histology_pathology"]
    elif sat > 105 and white < 0.08 and red < 0.14:
        label, score = "histology_pathology", scores["histology_pathology"]
    elif gray > 0.86 and white < 0.25 and sat < 32:
        label, score = "radiology_ct_mri", scores["radiology_ct_mri"]
    elif gray > 0.70 and dark > 0.16 and any(t in low for t in ["ct", "computed tomography", "mri", "arterial", "portal venous", "washout", "scan"]):
        label, score = "radiology_ct_mri", scores["radiology_ct_mri"]
    elif gray > 0.58 and dark > 0.28 and any(t in low for t in ["ultrasound", "ultrasonography", "sonography", "elastography", "fibroscan", "ceus"]):
        label, score = "ultrasound_elastography", scores["ultrasound_elastography"]
    elif scores["clinical_photo"] >= 2 and white < 0.45 and sat > 18 and scores["algorithm_flowchart"] == 0:
        label, score = "clinical_photo", scores["clinical_photo"]
    else:
        label, score = scores.most_common(1)[0]
        if label == "treatment_schema" and white > 0.48 and scores["algorithm_flowchart"] < scores["treatment_schema"] + 2:
            label = "text_table_slide"
            score = scores[label]
        elif label == "treatment_schema" and scores["clinical_photo"] >= 1 and sat > 20 and gray < 0.75:
            label = "clinical_photo"
            score = scores[label]
    confidence = min(95, 45 + score * 10)
    # Distinguish CT/MRI from US when text explicitly says US.
    if label == "radiology_ct_mri" and any(t in low for t in ["ultrasound", "ultrasonography", "sonography", "elastography", "fibroscan", "ceus"]):
        label = "ultrasound_elastography"
        confidence = max(confidence, 75)
    return label, confidence, reasons[:6]


def infer_topic(text: str, old_topics: str, visual_type: str) -> tuple[str, list[str], int, list[str]]:
    scores = text_scores(text, TOPIC_RULES)
    old = [x.strip() for x in old_topics.split(";") if x.strip()]
    for topic in old:
        if topic in TOPIC_LABEL_KO:
            scores[topic] += 1
    if "hbv_lifecycle" in old_topics:
        scores["hbv"] += 3
    if "hcv_daa" in old_topics:
        scores["hcv"] += 3
    if "hcc_" in old_topics:
        scores["hcc"] += 3
    if "benign" in old_topics:
        scores["benign_liver_lesions"] += 3
    if not scores:
        return "general_hepatology", old[:2], 35, ["no topic signal"]
    primary, score = scores.most_common(1)[0]
    topics = [primary]
    for topic, s in scores.most_common():
        if topic != primary and s >= max(2, score - 2):
            topics.append(topic)
    # Coarse old topic aliases.
    topics = ["viral_hepatitis" if t in {"hbv", "hcv", "hdv"} else t for t in topics]
    deduped: list[str] = []
    for t in topics:
        if t not in deduped:
            deduped.append(t)
    if visual_type in {"radiology_ct_mri", "ultrasound_elastography"} and "imaging" not in deduped:
        deduped.append("imaging")
    if visual_type in {"histology_pathology", "gross_pathology"} and "pathology" not in deduped:
        deduped.append("pathology")
    if visual_type in {"anatomy_diagram", "treatment_schema"} and "anatomy_intervention" not in deduped:
        deduped.append("anatomy_intervention")
    confidence = min(95, 45 + score * 8)
    return primary, deduped[:5], confidence, [f"topic:{k}={v}" for k, v in scores.most_common(5)]


def keyword_terms(text: str, visual_type: str, primary_topic: str, revised_topics: list[str]) -> list[str]:
    low = text.lower()
    terms = []
    base = [visual_type, primary_topic] + revised_topics
    for b in base:
        if b and b not in terms:
            terms.append(b)
    candidates = [
        "hcc", "bclc", "li-rads", "washout", "arterial phase", "tace", "atezolizumab", "bevacizumab",
        "hbv", "hbsag", "hbeag", "anti-hbc", "cccDNA", "hcv", "daa", "svr", "ns5a", "ns5b",
        "masld", "mash", "steatosis", "ballooning", "fibrosis", "resmetirom", "semaglutide",
        "cirrhosis", "portal hypertension", "varices", "ascites", "tips", "hepatic encephalopathy", "hrs",
        "aih", "pbc", "psc", "igg4", "cholangitis", "hemangioma", "fnh", "adenoma", "cyst",
        "fibroscan", "elastography", "bilirubin", "alp", "ggt", "biopsy", "transplant", "aclf",
        "ultrasound", "ct", "mri", "histology", "endoscopy", "kaplan-meier", "survival curve", "algorithm", "forest plot",
    ]
    for term in candidates:
        if term.lower() in low and term not in terms:
            terms.append(term)
    return terms[:24]


def row_text(collection: str, row: dict[str, str]) -> str:
    if collection == "canonical_db":
        return " ".join([
            row.get("image_id", ""),
            row.get("topics", ""),
            row.get("keywords", ""),
            row.get("meaning_ko", ""),
            row.get("source_file", ""),
            row.get("context_excerpt", ""),
            row.get("local_path", ""),
        ])
    return " ".join([
        row.get("figure_id", ""),
        row.get("topic", ""),
        row.get("subtopic", ""),
        row.get("meaning_ko", ""),
        row.get("article_title", ""),
        row.get("figure_label", ""),
        row.get("figure_title", ""),
        row.get("caption", ""),
        row.get("query", ""),
        row.get("local_path", ""),
    ])


def row_visual_text(collection: str, row: dict[str, str]) -> str:
    """Text used only for visual-form classification.

    Existing topic/keyword columns are deliberately excluded because this script
    is meant to correct them; using them here makes old mistakes self-reinforce.
    """
    if collection == "canonical_db":
        return " ".join([
            row.get("meaning_ko", ""),
            row.get("source_file", ""),
            row.get("context_excerpt", ""),
            row.get("local_path", ""),
        ])
    return " ".join([
        row.get("article_title", ""),
        row.get("figure_label", ""),
        row.get("figure_title", ""),
        row.get("caption", ""),
        row.get("local_path", ""),
    ])


def relabel_row(collection: str, row: dict[str, str]) -> dict[str, str]:
    local = row.get("local_path", "")
    path = ROOT / local
    feats = image_features(path)
    text = clean_text(row_text(collection, row))
    visual_text = clean_text(row_visual_text(collection, row))
    old_topics = row.get("topics") or row.get("topic") or ""
    visual_type, visual_conf, visual_reasons = infer_visual_type(visual_text, feats)
    row_id = row.get("image_id") or row.get("figure_id") or ""
    if row_id in MANUAL_VISUAL_OVERRIDES:
        visual_type = MANUAL_VISUAL_OVERRIDES[row_id]
        visual_conf = max(visual_conf, 90)
        visual_reasons.append(f"manual_override:{visual_type}")
    primary_topic, revised_topics, topic_conf, topic_reasons = infer_topic(text, old_topics, visual_type)
    keywords = keyword_terms(text, visual_type, primary_topic, revised_topics)
    confidence = min(visual_conf, topic_conf)
    reasons = visual_reasons + topic_reasons
    mismatch = ""
    old_primary = old_topics.split(";")[0] if old_topics else ""
    old_alias = old_primary
    if old_primary in {"hcc_systemic_trial", "hcc_imaging_pathology"}:
        old_alias = "hcc"
    if old_primary in {"hbv_lifecycle_serology", "hcv_daa_lifecycle"}:
        old_alias = "viral_hepatitis"
    if old_primary and old_alias not in revised_topics and primary_topic not in old_primary:
        mismatch = f"old={old_primary};new={primary_topic}"
        confidence = min(confidence, 60)
    if visual_type == "unknown" or confidence < 60 or feats.get("image_error"):
        needs_review = "yes"
    elif mismatch:
        needs_review = "maybe"
    else:
        needs_review = "no"
    label_ko = f"{TOPIC_LABEL_KO.get(primary_topic, primary_topic)} - {VISUAL_LABEL_KO.get(visual_type, visual_type)}"
    return {
        "collection": collection,
        "id": row_id,
        "local_path": local,
        "old_topics": old_topics,
        "old_keywords": row.get("keywords") or row.get("query") or "",
        "visual_type": visual_type,
        "primary_topic": primary_topic,
        "revised_topics": ";".join(revised_topics),
        "revised_keywords": ";".join(keywords),
        "label_ko": label_ko,
        "label_confidence": str(confidence),
        "needs_review": needs_review,
        "mismatch_flag": mismatch,
        "reason": " | ".join(reasons),
        "width": str(feats["width"]),
        "height": str(feats["height"]),
        "pink_ratio": str(feats["pink_ratio"]),
        "grayscale_ratio": str(feats["grayscale_ratio"]),
        "white_ratio": str(feats["white_ratio"]),
        "dark_ratio": str(feats["dark_ratio"]),
        "source_text_excerpt": text[:360],
    }


LABEL_FIELDS = [
    "collection",
    "id",
    "local_path",
    "old_topics",
    "old_keywords",
    "visual_type",
    "primary_topic",
    "revised_topics",
    "revised_keywords",
    "label_ko",
    "label_confidence",
    "needs_review",
    "mismatch_flag",
    "reason",
    "width",
    "height",
    "pink_ratio",
    "grayscale_ratio",
    "white_ratio",
    "dark_ratio",
    "source_text_excerpt",
]


def make_sheet(rows: list[dict[str, str]], out: Path, max_items: int = 240) -> None:
    rows = rows[:max_items]
    if not rows:
        return
    f = font(13)
    fb = font(13, True)
    cols = 5
    cell_w, cell_h = 280, 245
    sheet = Image.new("RGB", (cols * cell_w, math.ceil(len(rows) / cols) * cell_h), (246, 248, 247))
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(rows):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h
        p = ROOT / row["local_path"]
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((250, 165), Image.Resampling.LANCZOS)
            sheet.paste(im, (x + (cell_w - im.width) // 2, y + 8))
        except Exception:
            pass
        draw.text((x + 10, y + 178), row["id"][:28], font=fb, fill=(22, 35, 43))
        draw.text((x + 10, y + 196), row["visual_type"][:34], font=f, fill=(58, 72, 80))
        draw.text((x + 10, y + 214), row["primary_topic"][:34], font=f, fill=(58, 72, 80))
        if row["needs_review"] != "no":
            draw.text((x + 208, y + 178), row["needs_review"], font=fb, fill=(180, 70, 30))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "JPEG", quality=88)


def apply_canonical_labels(original_rows: list[dict[str, str]], labels: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for row in original_rows:
        label = labels.get(row["image_id"])
        if not label:
            out.append(row)
            continue
        new = dict(row)
        new["topics"] = label["revised_topics"]
        new["keywords"] = label["revised_keywords"]
        new["meaning_ko"] = label["label_ko"]
        out.append(new)
    return out


def apply_personal_labels(original_rows: list[dict[str, str]], labels: dict[str, dict[str, str]]) -> tuple[list[dict[str, str]], list[str]]:
    extra = ["visual_type", "primary_topic", "revised_topics", "revised_keywords", "label_ko", "label_confidence", "needs_review"]
    fields = list(original_rows[0].keys()) if original_rows else []
    for e in extra:
        if e not in fields:
            fields.append(e)
    out = []
    for row in original_rows:
        label = labels.get(row["figure_id"])
        new = dict(row)
        if label:
            new.update({e: label[e] for e in extra})
        out.append(new)
    return out, fields


def main() -> None:
    parser = argparse.ArgumentParser(description="Relabel DB/private figures by actual visual content.")
    parser.add_argument("--apply", action="store_true", help="Update manifest.csv files after creating backups.")
    args = parser.parse_args()

    AUDIT.mkdir(parents=True, exist_ok=True)
    canonical = read_csv(CANONICAL_MANIFEST)
    personal = read_csv(PERSONAL_MANIFEST)
    labels = []
    for row in canonical:
        labels.append(relabel_row("canonical_db", row))
    for row in personal:
        labels.append(relabel_row("personal_web", row))

    all_path = AUDIT / "all-private-images.visual-labels.csv"
    write_csv(all_path, labels, LABEL_FIELDS)
    db_labels = [r for r in labels if r["collection"] == "canonical_db"]
    personal_labels = [r for r in labels if r["collection"] == "personal_web"]
    write_csv(AUDIT / "db.visual-labels.csv", db_labels, LABEL_FIELDS)
    write_csv(AUDIT / "personal-web.visual-labels.csv", personal_labels, LABEL_FIELDS)

    review_rows = [r for r in labels if r["needs_review"] != "no"]
    make_sheet(review_rows, AUDIT / "needs-review-contact-sheet.jpg", max_items=260)
    for visual_type, count in Counter(r["visual_type"] for r in labels).most_common():
        subset = [r for r in labels if r["visual_type"] == visual_type]
        make_sheet(subset, AUDIT / "by-visual-type" / f"{visual_type}.jpg", max_items=220)

    if args.apply:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = AUDIT / "backups"
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CANONICAL_MANIFEST, backup / f"manifest.pre-visual-relabel.{stamp}.csv")
        shutil.copy2(PERSONAL_MANIFEST, backup / f"personal-web-manifest.pre-visual-relabel.{stamp}.csv")
        db_map = {r["id"]: r for r in db_labels}
        personal_map = {r["id"]: r for r in personal_labels}
        canonical_fields = ["image_id", "topics", "keywords", "meaning_ko", "local_path", "value_score", "source_file", "context_excerpt"]
        write_csv(CANONICAL_MANIFEST, apply_canonical_labels(canonical, db_map), canonical_fields)
        personal_rows, personal_fields = apply_personal_labels(personal, personal_map)
        write_csv(PERSONAL_MANIFEST, personal_rows, personal_fields)

    summary = {
        "total": len(labels),
        "canonical_db": len(db_labels),
        "personal_web": len(personal_labels),
        "visual_type_counts": dict(Counter(r["visual_type"] for r in labels).most_common()),
        "primary_topic_counts": dict(Counter(r["primary_topic"] for r in labels).most_common()),
        "needs_review": len(review_rows),
        "mismatch_flags": sum(1 for r in labels if r["mismatch_flag"]),
        "applied_to_manifests": bool(args.apply),
        "outputs": {
            "all_labels": str(all_path),
            "db_labels": str(AUDIT / "db.visual-labels.csv"),
            "personal_labels": str(AUDIT / "personal-web.visual-labels.csv"),
            "needs_review_contact_sheet": str(AUDIT / "needs-review-contact-sheet.jpg"),
        },
    }
    (AUDIT / "visual-label-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
