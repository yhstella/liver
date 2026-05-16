#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEARCH_INDEX = ROOT / "search-index.json"
OUT = ROOT / "private-figures" / "page-image-generation-v2"
PROMPT_DIR = OUT / "detail-prompts"
IMAGE_DIR = OUT / "images-detail"
PUBLIC_DIR = ROOT / "assets" / "img" / "page-generated-v2" / "detail"
PILOT_MANIFEST = OUT / "pilot_manifest.csv"


CATEGORY1 = {
    "hcc": {
        "ko": "간암",
        "style": "oncologic hepatology, radiology and treatment decision support, restrained navy and arterial red",
        "top": "one clear HCC concept: imaging, tumor burden, staging, or treatment choice",
        "lower": "one focused teaching figure: procedure, systemic therapy, follow-up, or risk stratification",
    },
    "viral": {
        "ko": "바이러스간염",
        "style": "clean virology and clinical laboratory style, cool blue with amber viral accents",
        "top": "virus-liver interaction, serology, antiviral suppression, or transmission context",
        "lower": "one focused teaching figure: marker pattern, medication choice, pregnancy, reactivation, or cure pathway",
    },
    "masld": {
        "ko": "지방간·대사질환",
        "style": "metabolic hepatology, warm liver gold, teal diagnostics, light lifestyle context",
        "top": "steatosis, metabolic risk, MASH, fibrosis, or treatment pathway",
        "lower": "one focused teaching figure: diet, weight loss, medication, FibroScan, or comorbidity risk",
    },
    "cirrhosis": {
        "ko": "간경변·문맥고혈압",
        "style": "chronic liver disease, portal venous anatomy, calm serious clinical tone",
        "top": "cirrhosis severity, portal hypertension, or major complication",
        "lower": "one focused teaching figure: ascites, varices, encephalopathy, renal syndrome, nutrition, or transplant",
    },
    "diagnostics": {
        "ko": "간수치·진단검사",
        "style": "precise outpatient diagnostics, lab tubes, ultrasound, chart shapes, clean white and teal",
        "top": "diagnostic pattern recognition using labs, imaging, elastography, or biopsy",
        "lower": "one focused teaching figure: AST/ALT/ALP/GGT pattern, bilirubin, synthetic function, tumor marker, or biopsy",
    },
    "autoimmune": {
        "ko": "자가면역·담즙정체",
        "style": "immune-mediated hepatology, antibody motifs, bile ducts, histology pink-purple accents",
        "top": "immune attack, bile duct inflammation, or autoimmune diagnostic framework",
        "lower": "one focused teaching figure: histology, autoantibodies, steroid therapy, overlap, pregnancy, or flare",
    },
    "benign": {
        "ko": "간 양성종양",
        "style": "reassuring radiology comparison, benign lesion morphology, cool diagnostic navy and soft teal",
        "top": "benign liver lesion imaging differentiation",
        "lower": "one focused teaching figure: hemangioma, cyst, FNH, adenoma, hormone/pregnancy, or rare lesion",
    },
    "general": {
        "ko": "기타 간질환·상황별 주제",
        "style": "practical hepatology outpatient care, medication safety, alcohol, acute illness, balanced clinical tone",
        "top": "one clear practical hepatology scenario",
        "lower": "one focused teaching figure: medication injury, alcohol-related injury, jaundice, special situation, or follow-up",
    },
}


HUB_URLS = {
    "/B형간염/",
    "/C형간염/",
    "/간양성종양/",
    "/간경화/",
    "/간수치/",
    "/간암/",
    "/자가면역간질환/",
    "/지방간/",
}


CURATED_KEYWORDS = {
    "간암-BCLC병기": ["BCLC", "ECOG", "Child-Pugh", "종양부담", "치료알고리즘"],
    "간암-TACE-종류-결정": ["TACE", "cTACE", "DEB-TACE", "간동맥", "종양혈관"],
    "간암-면역치료-1차": ["atezolizumab", "bevacizumab", "durvalumab", "tremelimumab", "생존곡선"],
    "간암-소작술-RFA-MWA": ["RFA", "MWA", "초음파유도", "소작범위", "종양크기"],
    "간암-SBRT-양성자": ["SBRT", "양성자치료", "방사선선량", "종양표적", "정상간보존"],
    "간암-간이식": ["Milan criteria", "downstaging", "간이식", "재발위험", "대기자관리"],
    "B형간염-재활성화": ["HBV reactivation", "면역억제", "rituximab", "HBsAg", "예방항바이러스제"],
    "B형간염-항바이러스제-비교": ["TAF", "TDF", "entecavir", "신기능", "골밀도"],
    "B형간염-백신": ["HBsAg", "anti-HBs", "백신", "면역형성", "추가접종"],
    "C형간염-완치-DAA": ["DAA", "SVR12", "HCV RNA", "간섬유화", "재감염"],
    "지방간-음식": ["지중해식단", "당분음료", "체중감량", "단백질", "커피"],
    "간경변-복수": ["복수", "나트륨제한", "이뇨제", "천자", "SBP"],
    "간경변-간성혼수": ["간성혼수", "암모니아", "lactulose", "rifaximin", "유발인자"],
    "PBC-원발성담즙성담관염": ["PBC", "AMA", "ALP", "UDCA", "담관손상"],
    "약물성-간손상-DILI": ["DILI", "약물력", "RUCAM", "간세포형", "담즙정체형"],
}


def compact_slug(value: str) -> str:
    value = value.strip("/")
    mapping = {
        "B형간염": "hbv",
        "C형간염": "hcv",
        "A형간염": "hav",
        "D형간염": "hdv",
        "간암": "hcc",
        "간경변": "cirrhosis",
        "간경화": "cirrhosis",
        "지방간": "masld",
        "간수치": "lft",
        "간섬유화스캔": "fibroscan",
        "자가면역간염": "aih",
        "간양성종양": "benign",
        "약물성": "dili",
        "알코올성": "alcohol",
        "빌리루빈": "bilirubin",
        "알부민": "albumin",
        "간생검": "biopsy",
        "식도정맥류": "varices",
        "복수": "ascites",
        "간성혼수": "encephalopathy",
        "간이식": "transplant",
    }
    for src, dst in mapping.items():
        value = value.replace(src, dst)
    value = re.sub(r"[^A-Za-z0-9가-힣]+", "-", value).strip("-").lower()
    value = re.sub(r"-+", "-", value)
    return value[:46]


def classify_category1(text: str) -> str:
    # Use URL/title-leading disease family first. Search-index keywords often contain
    # related conditions, so broad-body matching can pollute categories.
    head = " ".join(text.split()[:8])
    if any(x in head for x in ["자가면역간염", "AIH", "PBC", "원발성담즙성담관염"]):
        return "autoimmune"
    if any(x in head for x in ["간수치", "ALP", "GGT", "AST", "ALT", "빌리루빈", "알부민", "PIVKA", "알파태아단백", "간생검", "간섬유화스캔"]):
        return "diagnostics"
    if any(x in head for x in ["간양성종양", "혈관종", "FNH", "Adenoma", "간선종", "간낭종", "담관과오종", "NRH", "국소지방"]):
        return "benign"
    if any(x in head for x in ["B형간염", "C형간염", "A형간염", "D형간염", "HBV", "HCV", "HAV", "HDV"]):
        return "viral"
    if any(x in head for x in ["지방간", "MASLD", "MASH", "MetALD", "알코올성-간질환"]):
        return "masld"
    if any(x in head for x in ["간경변", "간경화"]):
        return "cirrhosis"
    if any(x in head for x in ["간암", "간세포암"]):
        return "hcc"

    if any(x in text for x in ["자가면역간염", "AIH", "PBC", "UDCA", "overlap", "스테로이드", "아자티오프린"]):
        return "autoimmune"
    if any(x in text for x in ["간수치", "AST", "ALT", "GGT", "ALP", "빌리루빈", "알부민", "PT", "간생검", "Fibroscan", "PIVKA", "AFP"]):
        return "diagnostics"
    if any(x in text for x in ["간양성종양", "혈관종", "FNH", "Adenoma", "adenoma", "간선종", "간낭종", "담관과오종", "NRH", "국소지방"]):
        return "benign"
    if any(x in text for x in ["간암", "간세포암", "BCLC", "TACE", "RFA", "MWA", "SBRT", "방사선색전술"]):
        return "hcc"
    if any(x in text for x in ["B형간염", "C형간염", "A형간염", "D형간염", "HBV", "HCV", "HAV", "HDV", "DAA", "HBsAg", "HBeAg"]):
        return "viral"
    if any(x in text for x in ["지방간", "MASLD", "MASH", "MetALD", "SGLT2", "GLP", "resmetirom", "비만수술", "수면무호흡"]):
        return "masld"
    if any(x in text for x in ["간경변", "간경화", "Child-Pugh", "MELD", "식도정맥류", "복수", "SBP", "간성혼수", "간신증후군", "혈소판감소", "근감소증"]):
        return "cirrhosis"
    return "general"


def classify_category2(cat: str, text: str) -> str:
    head = " ".join(text.split()[:8])
    if cat == "hcc":
        if any(x in head for x in ["TACE", "색전", "RFA", "MWA", "소작", "SBRT", "방사선"]): return "국소치료"
        if any(x in head for x in ["면역", "atezo", "bev", "전신"]): return "전신치료"
        if any(x in head for x in ["수술", "절제", "이식"]): return "수술·이식"
        if any(x in head for x in ["BCLC", "병기"]): return "병기·위험도"
        if any(x in head for x in ["진단", "검진", "AFP", "PIVKA", "첫외래", "가족력"]): return "진단·감시"
        if any(x in text for x in ["TACE", "색전", "RFA", "MWA", "소작", "SBRT", "방사선"]): return "국소치료"
        if any(x in text for x in ["면역", "atezo", "bev", "전신"]): return "전신치료"
        if any(x in text for x in ["수술", "절제", "이식"]): return "수술·이식"
        if any(x in text for x in ["BCLC", "병기"]): return "병기·위험도"
        if any(x in text for x in ["진단", "검진", "AFP", "PIVKA", "첫외래", "가족력"]): return "진단·감시"
        return "추적·일상관리"
    if cat == "viral":
        if any(x in text for x in ["C형", "HCV", "DAA", "SVR"]): return "C형간염 진단·DAA"
        if any(x in text for x in ["A형", "HAV", "D형", "HDV"]): return "A형·D형·특수 바이러스"
        if any(x in head for x in ["백신", "재활성화", "항바이러스", "수술전", "신기능", "평생약", "functional"]): return "B형간염 치료·예방"
        if any(x in head for x in ["결혼", "임신", "가족", "소아청소년"]): return "B형간염 가족·임신·소아"
        if any(x in text for x in ["백신", "재활성화", "항바이러스", "수술전", "신기능", "평생약", "functional"]): return "B형간염 치료·예방"
        if any(x in text for x in ["결혼", "임신", "가족", "소아청소년"]): return "B형간염 가족·임신·소아"
        return "B형간염 혈청표지자·자연사"
    if cat == "masld":
        if any(x in text for x in ["정밀검사", "Fibroscan", "섬유화"]): return "섬유화 위험층화"
        if any(x in text for x in ["SGLT2", "GLP", "resmetirom", "비만수술"]): return "약물·수술치료"
        if any(x in text for x in ["음식", "치료", "회복", "운동"]): return "생활치료·체중감량"
        if any(x in text for x in ["간암", "심혈관", "수면무호흡", "소아청소년"]): return "동반질환·장기위험"
        return "정의·표현형"
    if cat == "cirrhosis":
        if any(x in head for x in ["정맥류", "문맥", "혈소판"]): return "문맥고혈압"
        if any(x in head for x in ["복수", "SBP", "감염"]): return "복수·감염"
        if any(x in head for x in ["간성혼수", "간신"]): return "뇌·신장 합병증"
        if any(x in head for x in ["영양", "근감소", "피로", "가려움", "수면"]): return "영양·증상관리"
        if any(x in head for x in ["Child", "MELD", "대상성", "정상수치"]): return "중증도·예후"
        if any(x in text for x in ["정맥류", "문맥", "혈소판"]): return "문맥고혈압"
        if any(x in text for x in ["복수", "SBP", "감염"]): return "복수·감염"
        if any(x in text for x in ["간성혼수", "간신"]): return "뇌·신장 합병증"
        if any(x in text for x in ["영양", "근감소", "피로", "가려움", "수면"]): return "영양·증상관리"
        if any(x in text for x in ["Child", "MELD", "대상성", "정상수치"]): return "중증도·예후"
        return "이식·안전·생활"
    if cat == "diagnostics":
        if any(x in text for x in ["AST", "ALT", "GGT", "ALP", "운동", "임신", "소아"]): return "효소 패턴"
        if any(x in text for x in ["빌리루빈", "알부민", "PT", "합성능"]): return "빌리루빈·간합성능"
        if any(x in text for x in ["Fibroscan", "생검", "섬유화"]): return "섬유화·조직검사"
        if any(x in text for x in ["AFP", "PIVKA"]): return "종양표지자"
        return "검진·추적전략"
    if cat == "autoimmune":
        if any(x in text for x in ["PBC", "overlap"]): return "PBC·overlap"
        if any(x in text for x in ["치료", "약중단", "스테로이드"]): return "AIH 치료·부작용"
        if any(x in text for x in ["임신", "소아", "급성"]): return "특수상황"
        return "AIH 진단"
    if cat == "benign":
        if any(x in text for x in ["혈관종", "낭종"]): return "혈관종·낭종"
        if any(x in text for x in ["FNH", "Adenoma", "선종"]): return "FNH·선종"
        if any(x in text for x in ["임신", "경구피임약"]): return "호르몬·임신"
        if any(x in text for x in ["NRH", "담관과오종", "국소지방"]): return "드문 병변"
        return "영상감별"
    if any(x in text for x in ["약물", "DILI"]): return "약물성 간손상"
    if any(x in text for x in ["알코올"]): return "알코올 관련 간질환"
    return "상황별 간질환"


def category3(cat: str, cat2: str, title: str, keywords: list[str]) -> str:
    if keywords:
        return "·".join(keywords[:3])
    return title[:24]


def keywords_for(item: dict, cat: str) -> list[str]:
    url_key = item["u"].strip("/")
    if url_key in CURATED_KEYWORDS:
        return CURATED_KEYWORDS[url_key]

    raw = []
    if item.get("k"):
        raw.extend([x.strip() for x in item["k"].split(",") if x.strip()])

    text = " ".join([item.get("t", ""), item.get("tl", ""), item.get("d", "")])
    candidates = [
        "HBsAg", "HBeAg", "anti-HBs", "anti-HBc", "HBV DNA", "HCV RNA", "DAA", "SVR12",
        "TAF", "TDF", "entecavir", "Fibroscan", "FIB-4", "MASH", "MASLD", "MetALD",
        "AST", "ALT", "GGT", "ALP", "빌리루빈", "알부민", "PT", "AFP", "PIVKA-II",
        "BCLC", "TACE", "RFA", "MWA", "SBRT", "간이식", "면역치료", "CT", "MRI",
        "Child-Pugh", "MELD", "복수", "식도정맥류", "SBP", "간성혼수", "간신증후군",
        "AIH", "IgG", "ANA", "ASMA", "PBC", "UDCA", "스테로이드", "아자티오프린",
        "혈관종", "FNH", "간선종", "간낭종", "NRH", "DILI", "약물력", "알코올",
        "임신", "소아청소년", "가족력", "백신", "재활성화", "간섬유화", "생활치료",
    ]
    for c in candidates:
        if c.lower() in text.lower() and c not in raw:
            raw.append(c)

    defaults = {
        "hcc": ["간세포암", "CT/MRI", "BCLC", "치료선택", "추적"],
        "viral": ["혈청표지자", "바이러스량", "항바이러스제", "간섬유화", "추적검사"],
        "masld": ["지방간", "대사위험", "간섬유화", "체중감량", "생활치료"],
        "cirrhosis": ["간경변", "문맥고혈압", "합병증", "MELD", "추적관리"],
        "diagnostics": ["AST/ALT", "GGT/ALP", "빌리루빈", "Fibroscan", "추적검사"],
        "autoimmune": ["자가항체", "IgG", "간생검", "면역억제", "재발"],
        "benign": ["초음파", "CT/MRI", "혈관종", "FNH", "추적"],
        "general": ["문진", "검사패턴", "원인평가", "생활요인", "추적"],
    }
    for d in defaults[cat]:
        if d not in raw:
            raw.append(d)
    return raw[:5]


def visual_focus(cat: str, cat2: str, keywords: list[str]) -> str:
    k = " ".join(keywords)
    if any(x in k for x in ["CT", "MRI", "AFP", "PIVKA", "BCLC", "혈관종", "FNH", "간선종", "간낭종"]):
        return "radiology-focused liver figure with small diagnostic panels"
    if any(x in k for x in ["Fibroscan", "간섬유화", "FIB-4"]):
        return "elastography probe, shear waves, and fibrosis gradient"
    if any(x in k for x in ["HBsAg", "HBeAg", "HBV", "HCV", "DAA", "SVR"]):
        return "virus, hepatocyte, laboratory marker, and treatment pathway"
    if any(x in k for x in ["TACE", "RFA", "MWA", "SBRT", "간이식"]):
        return "procedure-centered liver treatment figure"
    if any(x in k for x in ["복수", "식도정맥류", "SBP", "간성혼수", "간신"]):
        return "cirrhosis complication mechanism figure"
    if any(x in k for x in ["IgG", "ANA", "ASMA", "PBC", "UDCA", "스테로이드"]):
        return "immune cells, antibodies, bile ducts, and histology texture"
    if any(x in k for x in ["음식", "체중감량", "생활치료", "알코올"]):
        return "metabolic lifestyle and liver health figure"
    return CATEGORY1[cat]["lower"]


def distinct_visual_identity(item: dict, cat: str, cat2: str, keywords: list[str]) -> tuple[str, str, str]:
    title = item.get("t", "")
    url = item.get("u", "")
    k = " ".join(keywords)

    if "C형간염-2025" in url:
        return (
            "single HCV RNA timeline ribbon fading after DAA tablets",
            "cool white clinic, violet HCV particles, one teal timeline curve",
            "minimal horizontal timeline with one liver silhouette; not a multi-panel guideline poster",
        )
    if "functional-cure" in url:
        return (
            "one hepatocyte nucleus with shrinking cccDNA ring and HBsAg particles fading",
            "deep indigo nucleus, amber HBV particles, small green anti-HBs glow",
            "molecular close-up; no treatment dashboard and no many lab tubes",
        )
    if "항바이러스제-비교" in url:
        return (
            "three simple antiviral tablets on a renal-bone safety balance",
            "clean white, blue kidney, ivory bone, amber liver",
            "one balanced scale composition; avoid adding virus lifecycle panels",
        )
    if "신기능-약물선택" in url:
        return (
            "kidney and liver connected by a single drug-selection pathway",
            "white nephrology clinic, blue kidney, warm liver, teal decision path",
            "one kidney-liver scene with clean empty space for eGFR overlay",
        )
    if "완치후-추적" in url:
        return (
            "healthy post-SVR liver with a surveillance calendar arc",
            "soft blue, pale violet residual risk dots, warm healthy liver",
            "one follow-up timeline; avoid repeating DAA pill eradication scene",
        )
    if "SBRT" in url or "양성자" in url:
        return (
            "focused radiation beam conforming around one liver tumor",
            "dark treatment room, cyan beam, amber isodose glow, red tumor",
            "single beam-planning scene; no surgery or catheter elements",
        )
    if "소작술" in url or "RFA" in title or "MWA" in title:
        return (
            "one ablation needle creating a clean spherical safety margin around a small tumor",
            "ultrasound gray, warm liver, orange ablation zone",
            "single procedure close-up; no split-screen comparison unless lower image",
        )
    if "간이식" in url:
        return (
            "transplant selection silhouette: donor liver and tumor-burden criteria zone",
            "calm surgical blue, warm donor liver, restrained green eligibility ring",
            "one transplant pathway image; no operating-room crowd",
        )
    if "Child-Pugh" in url or "MELD" in url:
        return (
            "simple severity score board made of five organ/function tokens around one cirrhotic liver",
            "slate blue, muted gold, clinical white",
            "single score dashboard with blank label spaces; no dense table",
        )
    if "간신증후군" in url:
        return (
            "liver-kidney hemodynamic axis with narrowed renal blood flow",
            "deep venous blue, pale kidney cyan, warm cirrhotic liver",
            "one liver-kidney scene; no broad complication collage",
        )
    if "SGLT2" in url or "GLP" in url:
        return (
            "metabolic drug effect triangle linking liver fat, weight, and glucose",
            "fresh teal, soft green, warm liver gold",
            "one clean metabolic triangle; no food plate and no many organs",
        )
    if "resmetirom" in url:
        return (
            "THR-beta liver-targeting concept with liver fat droplets shrinking",
            "deep teal, violet thyroid-receptor motif, golden fat droplets",
            "one receptor-to-liver scene; no generic FibroScan panel",
        )
    if "간암검진" in url or ("AFP" in k and "검진" in k and "간세포암" in k):
        return (
            "ultrasound surveillance arc with one AFP blood-drop cue for HBV-related HCC screening",
            "clean white, pale ultrasound blue, warm liver, tiny crimson AFP cue",
            "single surveillance scene; no HBV serology matrix and no virus field",
        )

    return (
        "one dominant page-specific medical subject",
        "category palette with one contrasting accent",
        "single-scene composition with at most three meaningful elements",
    )


def data_layer_for(item: dict, cat: str, cat2: str, keywords: list[str]) -> tuple[str, str, str]:
    title = item.get("t", "")
    url = item.get("u", "")
    k = " ".join(keywords)

    if "면역치료" in title or "atezolizumab" in k or "bevacizumab" in k:
        return (
            "source-backed KM-style survival/response curve, regimen comparison, adverse-event monitoring cue",
            "landmark trial or guideline source required before exact curve/number overlay",
            "leave clean space for deterministic curve/axis overlay; do not let image model invent trial labels",
        )
    if "BCLC" in title or "BCLC" in k:
        return (
            "BCLC decision grid: tumor burden, performance status, liver function, treatment branch",
            "current BCLC/AASLD/EASL/KASL guideline source required for exact stage labels",
            "use image as clinical background plus clean algorithm zones; exact labels should be added later",
        )
    if "TACE" in title or "TACE" in k:
        return (
            "angiographic tumor blush, hepatic artery map, cTACE versus DEB-TACE material comparison",
            "interventional oncology review/guideline source for exact indications and selection criteria",
            "avoid fake labels; reserve small inset for source-checked comparison caption",
        )
    if "SBRT" in title or "양성자" in title:
        return (
            "radiation treatment planning data: tumor target, dose falloff, normal-liver sparing, fractionation concept",
            "radiation oncology guideline or page source needed for exact dose/fraction and indication claims",
            "show dose-isodose structure visually; exact Gy/fraction labels should be deterministic overlay",
        )
    if "소작" in title or "RFA" in title or "MWA" in title:
        return (
            "ablation planning data: tumor size, ablation margin, ultrasound guidance, RFA versus MWA energy zone",
            "guideline/page source needed for exact size thresholds and margin targets",
            "reserve space for source-checked size/margin annotation; do not invent numbers in the image",
        )
    if "간이식" in title:
        return (
            "transplant selection data: Milan/downstaging concept, tumor burden, liver reserve, waiting-list pathway",
            "transplant guideline or page source needed for exact criteria and downstaging definitions",
            "use visual criteria zones; exact Milan/downstaging labels should be deterministic overlay",
        )
    if "functional cure" in title:
        return (
            "HBV functional cure data: HBsAg decline, anti-HBs emergence, HBV DNA suppression, finite-treatment research pathway",
            "HBV guideline/trial source needed for exact response rates and investigational therapy labels",
            "show marker trajectories visually; exact trial numbers and drug names should be overlay/caption",
        )
    if "항바이러스제 비교" in title or "신기능" in title:
        return (
            "HBV antiviral selection data: viral suppression, renal function, bone safety, pregnancy/age context, TDF versus TAF versus ETV",
            "guideline/page source needed for exact renal cutoff and safety statements",
            "show drug-selection axes visually; exact eGFR/bone labels should be deterministic overlay",
        )
    if "간암검진" in url or ("AFP" in k and "검진" in k and "간세포암" in k):
        return (
            "HBV-related HCC surveillance data: ultrasound interval, AFP trend, cirrhosis/family-risk context",
            "guideline/page source needed for exact surveillance interval and risk-group boundaries",
            "show ultrasound and AFP as visual cues only; exact interval and risk labels should be deterministic overlay/caption",
        )
    if "HBV" in k or "HBsAg" in k or "HBeAg" in k or "B형간염" in title:
        return (
            "HBV serology matrix, HBV DNA trend, treatment/prevention risk pathway",
            "guideline or page source needed for exact monitoring intervals and treatment thresholds",
            "image model should render markers as visual bands; exact serology text belongs in caption/overlay",
        )
    if "HCV" in k or "DAA" in k or "C형간염" in title:
        if "완치후-추적" in url or "완치 후" in title or "추적" in title:
            return (
                "post-SVR follow-up data: residual HCC risk, fibrosis/cirrhosis status, surveillance calendar",
                "guideline/page source needed for exact follow-up intervals and risk stratification",
                "show a simple follow-up arc and residual-risk dots; exact interval labels should be overlay/caption",
            )
        return (
            "HCV RNA decline and SVR12 endpoint timeline",
            "guideline or page source needed for exact regimen duration and population-specific data",
            "use a source-backed timeline concept; add exact SVR/time labels outside the generated image",
        )
    if "PBC" in k or "UDCA" in k or "AIH" in k or "IgG" in k:
        return (
            "autoimmune/cholestatic diagnostic data: antibody pattern, ALP/IgG trend, histology cue, treatment response",
            "guideline/page source needed for diagnostic criteria and biochemical response thresholds",
            "use generated image for pathology/immune scene; exact criteria in caption or overlay",
        )
    if "간신증후군" in title:
        return (
            "hepatorenal syndrome data: cirrhosis/ascites context, creatinine trajectory, vasoconstrictor plus albumin pathway, transplant bridge",
            "guideline/page source needed for exact diagnostic criteria and treatment thresholds",
            "show kidney-liver hemodynamic mechanism; exact creatinine/albumin criteria should be overlay/caption",
        )
    if cat == "masld":
        if "SGLT2" in title or "GLP" in title:
            return (
                "metabolic drug data: weight, HbA1c, liver fat, cardiovascular risk, fibrosis-risk trend",
                "trial/guideline source needed for exact effect size and indication boundaries",
                "show multi-endpoint trend structure; exact percentages and drug labels should be overlay/caption",
            )
        if "resmetirom" in title:
            return (
                "MASH drug-response data: THR-beta liver targeting, liver fat reduction, MASH resolution/fibrosis improvement endpoints",
                "trial/guideline source needed for exact endpoint rates and eligibility criteria",
                "use endpoint panels visually; exact trial values should be deterministic overlay",
            )
    if "Fibroscan" in k or "FIB-4" in k or "섬유화" in k:
        return (
            "risk stratification using FIB-4 and elastography stiffness zones",
            "guideline or page source needed for numeric cutoffs by context",
            "show zones visually; add exact kPa/FIB-4 numbers as deterministic overlay if used",
        )
    if "AFP" in k or "PIVKA" in k or "알파태아단백" in title:
        return (
            "AFP/PIVKA-II trend, HCC surveillance context, false-positive caution",
            "guideline/page source needed for surveillance interval and marker interpretation",
            "leave room for deterministic trend line and caption rather than generated tiny numbers",
        )
    if "ALP" in k or "GGT" in k or "빌리루빈" in k:
        return (
            "lab-pattern comparison: hepatocellular versus cholestatic injury, R-ratio concept if sourced",
            "page/source needed for exact ULN-based formula and interpretation thresholds",
            "show lab pattern shapes visually; exact formula should be added as overlay or nearby HTML",
        )
    if "Child-Pugh" in k or "MELD" in k or "복수" in k or "간성혼수" in k:
        return (
            "cirrhosis severity/complication data: ascites grade, encephalopathy trigger pathway, MELD/Child components",
            "guideline/page source needed for exact scoring criteria and management thresholds",
            "render mechanism and score components visually; exact score tables should be deterministic",
        )
    if "DILI" in k or "RUCAM" in k:
        return (
            "DILI causality timeline, exposure/dechallenge pattern, hepatocellular versus cholestatic pattern",
            "RUCAM or guideline source needed for exact scoring and R-ratio thresholds",
            "image should reserve space for deterministic timeline/checklist overlay",
        )
    if cat == "masld":
        return (
            "metabolic risk data: weight-loss target, diet pattern, fibrosis risk, cardiometabolic comorbidity",
            "guideline/page source needed for numeric weight-loss or cutoff claims",
            "show behavior/data relationship visually; add exact percent/cutoff as overlay if used",
        )
    return (
        "page-specific clinical data cue to be sourced before exact numeric rendering",
        "local page, lecture material, guideline, or landmark paper source required",
        "avoid invented text/numbers; use clean visual space for deterministic annotation",
    )


def prompt_for(kind: str, row: dict) -> str:
    cat = CATEGORY1[row["category_code"]]
    role = "top hero" if kind == "top" else "middle-lower teaching"
    shape = "16:9 landscape" if kind == "top" else "4:3 landscape"
    specific = cat["top"] if kind == "top" else row["visual_focus"]
    return f"""Create one lightweight but high-quality medical image for drshin.kr.
Role: {role} image, {shape}.
Page: {row['title']}
Category: {row['category1']} - {row['category2']} - {row['category3']}
Keywords: {row['keywords']}
Core visual: {specific}.
Distinct identity: {row['distinct_subject']}
Palette/composition: {row['distinct_palette']}
Composition rule: {row['composition_rule']}
Data layer: {row['data_layer']}
Data source plan: {row['data_source_plan']}
Overlay plan: {row['overlay_plan']}
Style master: {cat['style']}.
Medical requirement: show a concrete hepatology concept, clinical tool, imaging finding, disease mechanism, or treatment scene. This must not become a generic liver icon or a text summary slide.
Data requirement: represent real clinical data structures such as trends, risk zones, survival curves, diagnostic pathways, or score components when relevant. Do not invent exact numbers, trial labels, axes, or thresholds. If exact labels or numeric values are needed, leave clean space for deterministic SVG/HTML/caption overlay.
Lightweight direction: simpler than the v2 pilot. Use one dominant scene and at most 2-3 meaningful visual elements. Prefer one strong object, one data-shape cue, and one clinical context cue.
Differentiation requirement: this image must look visibly different from other hepatology pages by changing the main object, camera angle, palette, and composition. Avoid default liver-with-many-icons layouts, repeated dashboard grids, and collage-like panels.
Text policy: avoid generated readable Korean or English text. Minimal source-checked labels should be added later as deterministic overlay, not hallucinated by the image model. No fake labels, no logos, no watermarks.
Safety/style: no gore, no identifiable patient face, no hospital branding, no exaggerated fear imagery.
"""


def read_pilot_paths() -> dict[str, dict[str, Path]]:
    if not PILOT_MANIFEST.exists():
        return {}
    out: dict[str, dict[str, Path]] = {}
    with PILOT_MANIFEST.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            out[row["page_url"]] = {
                "top": ROOT / row["top_image"],
                "lower": ROOT / row["lower_image"],
            }
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    data = json.loads(SEARCH_INDEX.read_text(encoding="utf-8-sig"))
    detail = [x for x in data if x.get("c") == "detail"]
    pilot = read_pilot_paths()
    rows = []

    for idx, item in enumerate(detail, 1):
        text = " ".join([item.get("u", ""), item.get("t", ""), item.get("tl", ""), item.get("d", ""), item.get("k", "")])
        cat = classify_category1(text)
        cat2 = classify_category2(cat, text)
        keywords = keywords_for(item, cat)
        cat3 = category3(cat, cat2, item["t"], keywords)
        data_layer, data_source_plan, overlay_plan = data_layer_for(item, cat, cat2, keywords)
        distinct_subject, distinct_palette, composition_rule = distinct_visual_identity(item, cat, cat2, keywords)
        asset_id = f"d{idx:03d}-{cat}-{compact_slug(item['u'])}"
        row = {
            "detail_id": f"d{idx:03d}",
            "page_url": item["u"],
            "title": item["t"],
            "category_code": cat,
            "category1": CATEGORY1[cat]["ko"],
            "category2": cat2,
            "category3": cat3,
            "keywords": ";".join(keywords),
            "visual_focus": visual_focus(cat, cat2, keywords),
            "distinct_subject": distinct_subject,
            "distinct_palette": distinct_palette,
            "composition_rule": composition_rule,
            "data_layer": data_layer,
            "data_source_plan": data_source_plan,
            "overlay_plan": overlay_plan,
            "asset_id": asset_id,
            "top_prompt": f"private-figures/page-image-generation-v2/detail-prompts/{asset_id}-top.txt",
            "lower_prompt": f"private-figures/page-image-generation-v2/detail-prompts/{asset_id}-lower.txt",
            "top_image": f"private-figures/page-image-generation-v2/images-detail/{asset_id}-top.png",
            "lower_image": f"private-figures/page-image-generation-v2/images-detail/{asset_id}-lower.png",
            "public_top_image": f"/assets/img/page-generated-v2/detail/{asset_id}-top.png",
            "public_lower_image": f"/assets/img/page-generated-v2/detail/{asset_id}-lower.png",
            "status": "pending",
        }
        for kind in ("top", "lower"):
            (PROMPT_DIR / f"{asset_id}-{kind}.txt").write_text(prompt_for(kind, row), encoding="utf-8")

        top_target = IMAGE_DIR / f"{asset_id}-top.png"
        lower_target = IMAGE_DIR / f"{asset_id}-lower.png"
        pub_top = PUBLIC_DIR / f"{asset_id}-top.png"
        pub_lower = PUBLIC_DIR / f"{asset_id}-lower.png"
        if item["u"] in pilot:
            for kind, target, public_target in (("top", top_target, pub_top), ("lower", lower_target, pub_lower)):
                source = pilot[item["u"]][kind]
                if source.exists():
                    if not target.exists():
                        shutil.copy2(source, target)
                    if not public_target.exists():
                        shutil.copy2(source, public_target)

        # Keep public site-candidate copies in sync with the private generated
        # image database. Earlier batches sometimes copied only the private file.
        for private_target, public_target in ((top_target, pub_top), (lower_target, pub_lower)):
            if private_target.exists() and not public_target.exists():
                shutil.copy2(private_target, public_target)

        if top_target.exists() and lower_target.exists() and pub_top.exists() and pub_lower.exists():
            row["status"] = "generated"
        rows.append(row)

    fields = list(rows[0].keys())
    with (OUT / "detail_manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "detail_manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "style_masters_full.json").write_text(json.dumps(CATEGORY1, ensure_ascii=False, indent=2), encoding="utf-8")

    queue_rows = []
    for row in rows:
        for kind in ("top", "lower"):
            rel = row[f"{kind}_image"]
            if not (ROOT / rel).exists():
                queue_rows.append({
                    "detail_id": row["detail_id"],
                    "page_url": row["page_url"],
                    "title": row["title"],
                    "kind": kind,
                    "prompt_file": row[f"{kind}_prompt"],
                    "target_file": rel,
                    "public_file": row[f"public_{kind}_image"],
                    "category1": row["category1"],
                    "category2": row["category2"],
                    "keywords": row["keywords"],
                    "distinct_subject": row["distinct_subject"],
                    "distinct_palette": row["distinct_palette"],
                    "composition_rule": row["composition_rule"],
                    "data_layer": row["data_layer"],
                    "data_source_plan": row["data_source_plan"],
                    "overlay_plan": row["overlay_plan"],
                })
    qfields = list(queue_rows[0].keys()) if queue_rows else ["detail_id", "kind"]
    with (OUT / "generation_queue.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=qfields)
        writer.writeheader()
        writer.writerows(queue_rows)

    summary = {
        "detail_pages": len(rows),
        "generated_pages": sum(1 for r in rows if r["status"] == "generated"),
        "pending_pages": sum(1 for r in rows if r["status"] != "generated"),
        "pending_images": len(queue_rows),
        "manifest": str(OUT / "detail_manifest.csv"),
        "queue": str(OUT / "generation_queue.csv"),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
