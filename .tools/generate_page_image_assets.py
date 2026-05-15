#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
SEARCH_INDEX = ROOT / "search-index.json"
OUT = ROOT / "private-figures" / "page-image-generation"
ASSET_OUT = ROOT / "assets" / "img" / "page-generated"
FONT = Path("C:/Windows/Fonts/malgun.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/malgunbd.ttf")


CATEGORY1 = {
    "hcc": {
        "ko": "간암",
        "slug": "hcc",
        "palette": ["#122642", "#1f6f8b", "#f2b35d", "#f06a55"],
        "visual": "liver tumor, arterial imaging, treatment decision, concise oncologic mood",
    },
    "viral_hepatitis": {
        "ko": "바이러스 간염",
        "slug": "viral-hepatitis",
        "palette": ["#183153", "#2d9cdb", "#7c5cff", "#ffcf56"],
        "visual": "virus particles, serology markers, antiviral suppression, clean infectious disease mood",
    },
    "masld_mash": {
        "ko": "지방간·대사질환",
        "slug": "masld-mash",
        "palette": ["#234236", "#40a66b", "#f4c95d", "#ef7b45"],
        "visual": "fat droplets, metabolic organs, lifestyle and fibrosis risk, warm metabolic mood",
    },
    "cirrhosis_portal_htn": {
        "ko": "간경변·문맥고혈압",
        "slug": "cirrhosis-portal-htn",
        "palette": ["#26364f", "#5f7ea3", "#c77d57", "#d9c9a3"],
        "visual": "fibrotic liver texture, portal venous flow, complications, sober chronic disease mood",
    },
    "liver_tests_diagnostics": {
        "ko": "간수치·진단검사",
        "slug": "liver-tests-diagnostics",
        "palette": ["#172d3a", "#42a7a1", "#78c6e7", "#f2d56b"],
        "visual": "laboratory tubes, ultrasound probes, charts, diagnostic pathway, precise clinical mood",
    },
    "autoimmune_cholestatic": {
        "ko": "자가면역·담즙정체",
        "slug": "autoimmune-cholestatic",
        "palette": ["#2a2340", "#8b6fd8", "#3cb6a3", "#f4a6b7"],
        "visual": "antibodies, bile ducts, immune inflammation, elegant immunology mood",
    },
    "benign_liver_lesions": {
        "ko": "간 양성종양·국소병변",
        "slug": "benign-liver-lesions",
        "palette": ["#203047", "#6ba4b8", "#8ccf8f", "#e7b46a"],
        "visual": "focal liver lesion, imaging comparison, low-risk follow-up, calm radiology mood",
    },
    "general_hepatology": {
        "ko": "일반 간질환·특수상황",
        "slug": "general-hepatology",
        "palette": ["#28313f", "#6c8fb5", "#e4a857", "#a7c4a0"],
        "visual": "clinical context, medication safety, acute liver injury, practical outpatient mood",
    },
}


SECONDARY = {
    "hcc": [
        ("diagnosis_screening", "진단·검진", ["진단", "검진", "AFP", "PIVKA", "첫외래", "가족력"]),
        ("staging_risk", "병기·위험도", ["BCLC", "병기", "혈관침범", "가이드라인"]),
        ("locoregional_treatment", "국소치료", ["TACE", "색전", "소작", "RFA", "MWA", "SBRT", "방사선"]),
        ("systemic_treatment", "전신치료", ["면역", "atezo", "bev", "durva", "tremel", "lenva", "sorafenib"]),
        ("surgery_transplant", "수술·이식", ["절제", "수술", "간이식", "이식"]),
        ("followup_lifestyle", "추적·일상", ["재발", "추적", "식이", "일상"]),
    ],
    "viral_hepatitis": [
        ("hbv_natural_history", "B형간염 자연사", ["B형", "HBV", "HBeAg", "functional", "occult"]),
        ("hbv_treatment_prevention", "B형간염 치료·예방", ["TAF", "TDF", "엔테카", "백신", "재활성화", "수술전"]),
        ("hbv_family_pregnancy", "B형간염 가족·임신", ["가족", "결혼", "임신", "수유", "소아"]),
        ("hcv_diagnosis_treatment", "C형간염 진단·DAA", ["C형", "HCV", "DAA", "SVR", "RNA"]),
        ("hcv_special", "C형간염 특수상황", ["신부전", "HIV", "재감염", "재치료", "임신"]),
        ("acute_delta", "A형·D형·급성간염", ["A형", "HAV", "D형", "HDV", "급성"]),
    ],
    "masld_mash": [
        ("definition_risk", "정의·위험층화", ["MASLD", "MASH", "lean", "MetALD", "정의"]),
        ("fibrosis_diagnosis", "섬유화·정밀검사", ["Fibroscan", "섬유화", "정밀", "MASH"]),
        ("lifestyle_weight", "식이·운동·체중", ["음식", "식이", "운동", "회복", "비만"]),
        ("metabolic_drugs", "대사약물·신약", ["SGLT2", "GLP", "resmetirom", "신약"]),
        ("complications", "합병증·장기위험", ["간암", "심혈관", "수면무호흡", "소아"]),
    ],
    "cirrhosis_portal_htn": [
        ("severity_scores", "중증도 점수", ["Child", "MELD", "대상성", "비대상성"]),
        ("portal_hypertension", "문맥고혈압·정맥류", ["정맥류", "문맥", "TIPS", "혈소판"]),
        ("ascites_infection", "복수·감염", ["복수", "SBP", "감염", "항생제"]),
        ("encephalopathy_renal", "간성혼수·신장", ["간성혼수", "간신", "HRS", "수면"]),
        ("nutrition_symptom", "영양·증상관리", ["영양", "근감소", "가려움", "피로"]),
        ("transplant_safety", "이식·약물·여행", ["간이식", "약물", "여행", "항공"]),
    ],
    "liver_tests_diagnostics": [
        ("enzyme_pattern", "효소 패턴", ["AST", "ALT", "GGT", "ALP", "운동"]),
        ("bilirubin_synthesis", "빌리루빈·합성능", ["빌리루빈", "알부민", "PT", "합성능"]),
        ("fibrosis_biopsy", "섬유화·생검", ["Fibroscan", "FIB-4", "간생검", "섬유화"]),
        ("tumor_marker", "종양표지자", ["AFP", "PIVKA", "종양표지자"]),
        ("special_population", "특수상황 수치", ["임신", "소아", "검진주기"]),
    ],
    "autoimmune_cholestatic": [
        ("aih_diagnosis", "자가면역간염 진단", ["진단", "ALT", "IgG", "자가항체", "AIH"]),
        ("aih_treatment", "자가면역간염 치료", ["치료", "스테로이드", "아자티오프린", "약중단"]),
        ("overlap_pbc", "PBC·overlap", ["PBC", "overlap", "UDCA", "담즙정체"]),
        ("special_situation", "임신·소아·급성", ["임신", "소아", "급성간부전"]),
    ],
    "benign_liver_lesions": [
        ("diagnosis_imaging", "영상진단", ["진단", "MRI", "CT", "초음파"]),
        ("hemangioma_cyst", "혈관종·낭종", ["혈관종", "낭종"]),
        ("fnh_adenoma", "FNH·선종", ["FNH", "선종", "adenoma"]),
        ("hormone_pregnancy", "호르몬·임신", ["임신", "경구피임약"]),
        ("rare_lesion", "드문 병변", ["NRH", "담관과오종", "국소지방"]),
    ],
    "general_hepatology": [
        ("drug_alcohol", "약물·알코올", ["약물", "DILI", "알코올"]),
        ("acute_special", "급성·특수상황", ["급성", "황달", "간부전"]),
        ("patient_context", "외래 상황", ["검진", "상담", "주의"]),
    ],
}


CONTROLLED_TERMS = [
    "B형간염", "HBV DNA", "HBsAg", "HBeAg", "anti-HBs", "anti-HBc", "TDF", "TAF", "엔테카비르",
    "백신", "재활성화", "임신·수유", "C형간염", "anti-HCV", "HCV RNA", "DAA", "SVR", "재치료",
    "간세포암", "BCLC", "AFP", "PIVKA-II", "초음파", "CT", "MRI", "TACE", "RFA", "MWA",
    "방사선색전술", "SBRT", "면역치료", "atezolizumab", "bevacizumab", "간이식", "재발",
    "MASLD", "MASH", "Fibroscan", "FIB-4", "비만", "당뇨", "고지혈증", "식이·운동",
    "GLP-1RA", "SGLT2", "resmetirom", "MetALD", "알코올", "간경변", "Child-Pugh", "MELD",
    "문맥고혈압", "식도정맥류", "복수", "SBP", "간성혼수", "간신증후군", "혈소판감소",
    "근감소증", "AST", "ALT", "GGT", "ALP", "빌리루빈", "알부민", "PT", "간생검",
    "자가면역간염", "AIH", "IgG", "ANA", "ASMA", "스테로이드", "아자티오프린", "PBC",
    "UDCA", "overlap", "혈관종", "FNH", "간선종", "간낭종", "담관과오종", "NRH",
    "약물성간손상", "DILI", "황달", "A형간염", "HAV", "D형간염", "HDV",
]


GENERIC_FILLERS = {
    "hcc": ["간세포암", "CT", "MRI", "BCLC", "치료선택"],
    "viral_hepatitis": ["바이러스", "혈청표지자", "PCR", "항바이러스제", "추적검사"],
    "masld_mash": ["지방간", "대사위험", "섬유화", "체중감량", "식이·운동"],
    "cirrhosis_portal_htn": ["간경변", "문맥고혈압", "합병증", "MELD", "추적관리"],
    "liver_tests_diagnostics": ["AST", "ALT", "GGT", "빌리루빈", "Fibroscan"],
    "autoimmune_cholestatic": ["자가항체", "IgG", "담즙정체", "스테로이드", "UDCA"],
    "benign_liver_lesions": ["초음파", "CT", "MRI", "추적", "양성병변"],
    "general_hepatology": ["문진", "검사", "약물", "생활습관", "추적"],
}


VISUAL_TYPE_BY_KEYWORD = [
    ("radiology_ct_mri", ["CT", "MRI", "영상", "LI-RADS", "진단", "검진", "재발", "혈관침범", "양성종양", "혈관종", "FNH", "선종", "낭종"]),
    ("ultrasound_elastography", ["초음파", "Fibroscan", "FIB-4", "섬유화", "간섬유화", "정밀검사"]),
    ("virology_diagram", ["HBV", "HCV", "HAV", "HDV", "B형간염", "C형간염", "A형간염", "D형간염", "cccDNA", "viral", "바이러스"]),
    ("serology_lab", ["HBsAg", "HBeAg", "anti-HBs", "anti-HBc", "anti-HCV", "HBV DNA", "HCV RNA", "PCR", "AFP", "PIVKA", "AST", "ALT", "GGT", "ALP", "빌리루빈", "알부민", "PT", "IgG", "ANA", "ASMA"]),
    ("treatment_schema", ["치료", "약", "TAF", "TDF", "엔테카비르", "DAA", "SVR", "스테로이드", "아자티오프린", "UDCA", "resmetirom", "GLP", "SGLT2", "면역치료", "atezolizumab", "bevacizumab"]),
    ("procedure_intervention", ["TACE", "RFA", "MWA", "색전", "소작", "방사선색전술", "SBRT", "간이식", "절제", "수술", "TIPS", "생검"]),
    ("lifestyle_metabolic", ["식이", "운동", "체중", "비만", "당뇨", "고지혈증", "알코올", "수면", "음식"]),
    ("histology_pathology", ["조직", "생검", "MASH", "AIH", "PBC", "담즙정체", "섬유화", "간선종", "NRH"]),
    ("clinical_context", ["임신", "수유", "소아", "가족", "여행", "피로", "가려움", "황달", "복수", "간성혼수"]),
]


@dataclass
class PageTopic:
    idx: int
    url: str
    title: str
    tl: str
    description: str
    source_keywords: list[str]
    body_excerpt: str
    category1: str
    category2: str
    category3: str
    keywords: list[str]
    asset_id: str
    selected_keyword: str
    selected_candidate: str


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<script[\s\S]*?</script>", " ", value, flags=re.I)
    value = re.sub(r"<style[\s\S]*?</style>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def read_body_excerpt(url: str) -> str:
    rel = unquote(url.strip("/"))
    path = ROOT / rel / "index.html" if rel else ROOT / "index.html"
    if not path.exists():
        return ""
    text = clean_text(path.read_text(encoding="utf-8", errors="ignore"))
    return text[:2500]


def sha(text: str, n: int = 8) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]


def slug_ascii(text: str) -> str:
    low = text.lower()
    replacements = {
        "b형": "hbv", "c형": "hcv", "a형": "hav", "d형": "hdv",
        "간암": "hcc", "간경변": "cirrhosis", "간경화": "cirrhosis",
        "지방간": "fatty-liver", "자가면역": "autoimmune", "간수치": "lft",
        "간양성종양": "benign-lesion", "섬유화": "fibrosis", "검사": "test",
        "진단": "diagnosis", "치료": "treatment", "임신": "pregnancy",
        "백신": "vaccine", "정맥류": "varices", "복수": "ascites",
    }
    for k, v in replacements.items():
        low = low.replace(k, v)
    low = re.sub(r"[^a-z0-9]+", "-", low).strip("-")
    return low[:34] or sha(text, 8)


def classify_category1(text: str) -> str:
    t = text.lower()
    if any(x.lower() in t for x in ["간암", "hcc", "간세포암", "bclc", "pivka", "알파태아", "afp"]):
        if "간수치" not in t and "종양표지자" not in t:
            return "hcc"
    if any(x.lower() in t for x in ["b형", "c형", "a형", "d형", "hbv", "hcv", "hav", "hdv", "hepatitis", "daa", "hbsag", "hbeag", "anti-hcv"]):
        return "viral_hepatitis"
    if any(x.lower() in t for x in ["지방간", "masld", "mash", "nash", "metald", "sglt2", "glp", "resmetirom", "비만수술", "수면무호흡"]):
        return "masld_mash"
    if any(x.lower() in t for x in ["간경변", "간경화", "child", "meld", "정맥류", "복수", "sbp", "간성혼수", "간신", "혈소판", "문맥", "tips", "근감소"]):
        return "cirrhosis_portal_htn"
    if any(x.lower() in t for x in ["자가면역", "aih", "pbc", "overlap", "udca", "스테로이드", "아자티오프린"]):
        return "autoimmune_cholestatic"
    if any(x.lower() in t for x in ["간양성", "혈관종", "fnh", "선종", "낭종", "담관과오종", "nrh", "국소지방"]):
        return "benign_liver_lesions"
    if any(x.lower() in t for x in ["간수치", "ast", "alt", "ggt", "alp", "빌리루빈", "알부민", "pt", "fibroscan", "간생검", "pivka", "afp"]):
        return "liver_tests_diagnostics"
    return "general_hepatology"


def classify_category2(cat1: str, text: str) -> str:
    matches = []
    for slug, _label, terms in SECONDARY[cat1]:
        score = 0
        low = text.lower()
        for term in terms:
            if term.lower() in low:
                score += 1
        matches.append((score, slug))
    matches.sort(reverse=True)
    return matches[0][1] if matches and matches[0][0] > 0 else SECONDARY[cat1][0][0]


def category2_label(cat1: str, cat2: str) -> str:
    for slug, label, _terms in SECONDARY[cat1]:
        if slug == cat2:
            return label
    return cat2


def derive_category3(title: str, keywords: list[str], cat2: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    short = title
    short = re.sub(r"^(.{2,28}?)[—-].*$", r"\1", short)
    if len(short) > 32:
        short = short[:32].rstrip() + "…"
    if not short and keywords:
        short = keywords[0]
    return short or cat2


def derive_keywords(item: dict, cat1: str, combined: str) -> list[str]:
    out: list[str] = []
    raw = item.get("k") or ""
    for part in re.split(r"[,;/]", raw):
        part = part.strip()
        if part and part not in out:
            out.append(part)
    low = combined.lower()
    for term in CONTROLLED_TERMS:
        if term.lower() in low and term not in out:
            out.append(term)
    for term in GENERIC_FILLERS[cat1]:
        if term not in out:
            out.append(term)
    return out[:5]


def visual_type_for_keyword(keyword: str, page_text: str, cat1: str) -> str:
    t = f"{keyword} {page_text}".lower()
    for vt, terms in VISUAL_TYPE_BY_KEYWORD:
        for term in terms:
            if term.lower() in t:
                return vt
    defaults = {
        "hcc": "radiology_ct_mri",
        "viral_hepatitis": "virology_diagram",
        "masld_mash": "lifestyle_metabolic",
        "cirrhosis_portal_htn": "ultrasound_elastography",
        "liver_tests_diagnostics": "serology_lab",
        "autoimmune_cholestatic": "histology_pathology",
        "benign_liver_lesions": "radiology_ct_mri",
        "general_hepatology": "clinical_context",
    }
    return defaults[cat1]


def choose_lower_keyword(title: str, keywords: list[str], cat1: str, combined: str) -> str:
    purpose_terms = {
        "treatment": ["치료", "약", "DAA", "TAF", "TDF", "TACE", "RFA", "면역", "스테로이드", "UDCA", "resmetirom"],
        "diagnosis": ["진단", "검사", "수치", "Fibroscan", "AFP", "PIVKA", "AST", "ALT", "CT", "MRI"],
        "lifestyle": ["음식", "식이", "운동", "비만", "알코올", "생활"],
        "risk": ["검진", "추적", "재발", "위험", "BCLC", "MELD"],
    }
    text = f"{title} {combined}"
    best = (0, 0, keywords[0])
    for i, kw in enumerate(keywords):
        score = 1
        vt = visual_type_for_keyword(kw, text, cat1)
        if vt in {"radiology_ct_mri", "treatment_schema", "procedure_intervention", "serology_lab", "ultrasound_elastography"}:
            score += 2
        for terms in purpose_terms.values():
            if any(t.lower() in text.lower() for t in terms) and any(t.lower() in kw.lower() for t in terms):
                score += 3
        if kw in {"간세포암", "B형간염", "C형간염", "MASLD", "간경변"}:
            score -= 1
        candidate = (score, -i, kw)
        if candidate > best:
            best = candidate
    return best[2]


def load_topics() -> list[PageTopic]:
    data = json.loads(SEARCH_INDEX.read_text(encoding="utf-8-sig"))
    details = [x for x in data if x.get("c") == "detail"]
    topics: list[PageTopic] = []
    for idx, item in enumerate(details, 1):
        body = read_body_excerpt(item["u"])
        combined = " ".join([item.get("t", ""), item.get("tl", ""), item.get("d", ""), item.get("k", ""), body])
        cat1 = classify_category1(combined)
        cat2 = classify_category2(cat1, combined)
        keywords = derive_keywords(item, cat1, combined)
        selected_kw = choose_lower_keyword(item.get("t", ""), keywords, cat1, combined)
        title = item.get("t") or item.get("tl") or item["u"].strip("/")
        asset_id = f"d{idx:03d}-{CATEGORY1[cat1]['slug']}-{slug_ascii(title)}"
        topics.append(PageTopic(
            idx=idx,
            url=item["u"],
            title=title,
            tl=item.get("tl", ""),
            description=item.get("d", ""),
            source_keywords=[x.strip() for x in re.split(r"[,;/]", item.get("k", "")) if x.strip()],
            body_excerpt=body[:900],
            category1=cat1,
            category2=cat2,
            category3=derive_category3(title, keywords, cat2),
            keywords=keywords,
            asset_id=asset_id,
            selected_keyword=selected_kw,
            selected_candidate="",
        ))
    return topics


def ensure_dirs() -> None:
    for p in [
        OUT / "prompts" / "top",
        OUT / "prompts" / "lower-candidates",
        OUT / "generated" / "top",
        OUT / "generated" / "lower",
        OUT / "generated" / "candidates",
        OUT / "contact-sheets",
        OUT / "style-masters",
        ASSET_OUT / "top",
        ASSET_OUT / "lower",
    ]:
        p.mkdir(parents=True, exist_ok=True)


def make_style_masters(topics: list[PageTopic]) -> dict:
    style = {
        "global": {
            "intent": "환자용 간질환 페이지에 쓰는 통일된 의료 일러스트/figure 스타일",
            "format": "상단이미지 16:9, 중하단이미지 4:3, 텍스트 최소화, 워터마크 없음",
            "rules": [
                "의학적 개념을 그림으로 보여준다. 요약 슬라이드처럼 문장을 많이 쓰지 않는다.",
                "과장된 공포감, 혈액/수술 장면의 과도한 사실감, 환자 얼굴 클로즈업을 피한다.",
                "각 이미지는 키워드 1개 이상을 시각적으로 드러내야 한다.",
            ],
        },
        "category1": {},
        "category2": {},
        "category3": {},
    }
    for cat1, data in CATEGORY1.items():
        style["category1"][cat1] = {
            "label_ko": data["ko"],
            "palette": data["palette"],
            "master_style": (
                f"{data['ko']} 계열. {data['visual']}. "
                "깨끗한 off-white 배경, 정교하지만 부담 없는 3D/벡터 혼합 의료 일러스트, "
                "소량의 실제 의학 figure 질감(영상, 검사, 도식)을 결합."
            ),
        }
    for cat1 in CATEGORY1:
        style["category2"][cat1] = {}
        for slug, label, terms in SECONDARY[cat1]:
            style["category2"][cat1][slug] = {
                "label_ko": label,
                "inherits": cat1,
                "emphasis_terms": terms,
                "master_style": (
                    f"{style['category1'][cat1]['master_style']} "
                    f"세부 강조: {label}. 핵심 요소는 {', '.join(terms[:5])}."
                ),
            }
    for topic in topics:
        style["category3"][topic.asset_id] = {
            "page_url": topic.url,
            "title": topic.title,
            "category1": topic.category1,
            "category2": topic.category2,
            "category3": topic.category3,
            "keywords": topic.keywords,
            "master_style": (
                f"{style['category2'][topic.category1][topic.category2]['master_style']} "
                f"이 페이지에서는 {topic.category3}를 중심으로, "
                f"{', '.join(topic.keywords)}를 시각적 단서로 사용."
            ),
        }
    (OUT / "style-masters" / "style_masters.json").write_text(
        json.dumps(style, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return style


def prompt_for_top(topic: PageTopic, style: dict) -> str:
    return f"""Use case: scientific-educational
Asset type: drshin.kr page top image, 16:9, no watermark
Page: {topic.title}
Category: {CATEGORY1[topic.category1]['ko']} - {category2_label(topic.category1, topic.category2)} - {topic.category3}
Keywords: {", ".join(topic.keywords)}
Style master: {style['category3'][topic.asset_id]['master_style']}
Primary request: Create a polished medical illustration that represents the page topic as a real visual concept, not a text-summary slide. Use liver anatomy, disease mechanism, imaging, procedure, lab, or lifestyle elements only when medically relevant.
Composition: clean clinical background, one dominant medical object, two or three small supporting visual cues, generous empty space for web layout.
Avoid: long text, fake journal screenshots, unreadable labels, gore, frightening patient imagery, logos, hospital branding.
"""


def prompt_for_candidate(topic: PageTopic, keyword: str, visual_type: str, style: dict) -> str:
    return f"""Use case: scientific-educational
Asset type: drshin.kr middle/lower candidate image, 4:3, no watermark
Page: {topic.title}
Candidate keyword: {keyword}
Visual type: {visual_type}
Category: {CATEGORY1[topic.category1]['ko']} - {category2_label(topic.category1, topic.category2)} - {topic.category3}
Style master: {style['category3'][topic.asset_id]['master_style']}
Primary request: Create one focused medical figure for the keyword. It should look like an actual figure or clinically meaningful illustration, not a page summary.
Avoid: excessive text, wrong anatomy, fake brand logos, realistic patient identity, decorative-only abstract shapes.
"""


def palette(cat1: str) -> list[str]:
    return CATEGORY1[cat1]["palette"]


def rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def canvas(w: int, h: int, cat1: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    scale = 2
    im = Image.new("RGBA", (w * scale, h * scale), (248, 250, 248, 255))
    draw = ImageDraw.Draw(im)
    pal = palette(cat1)
    for i in range(0, h * scale, 4):
        mix = i / max(1, h * scale)
        r = int(248 * (1 - mix) + rgba(pal[1])[0] * mix * 0.12)
        g = int(250 * (1 - mix) + rgba(pal[1])[1] * mix * 0.12)
        b = int(248 * (1 - mix) + rgba(pal[1])[2] * mix * 0.12)
        draw.rectangle([0, i, w * scale, i + 4], fill=(r, g, b, 255))
    return im, draw


def down(im: Image.Image, w: int, h: int) -> Image.Image:
    return im.resize((w, h), Image.Resampling.LANCZOS).convert("RGB")


def liver_shape(draw: ImageDraw.ImageDraw, cx: int, cy: int, s: int, fill: str, outline: str) -> None:
    pts = [
        (cx - 1.22 * s, cy - 0.10 * s), (cx - 0.88 * s, cy - 0.54 * s),
        (cx - 0.22 * s, cy - 0.60 * s), (cx + 0.54 * s, cy - 0.40 * s),
        (cx + 1.07 * s, cy - 0.04 * s), (cx + 0.90 * s, cy + 0.42 * s),
        (cx + 0.28 * s, cy + 0.55 * s), (cx - 0.42 * s, cy + 0.46 * s),
        (cx - 1.08 * s, cy + 0.22 * s),
    ]
    draw.polygon([(int(x), int(y)) for x, y in pts], fill=fill, outline=outline)
    draw.ellipse([cx - int(.18 * s), cy - int(.18 * s), cx + int(.28 * s), cy + int(.32 * s)], fill=fill, outline=outline)


def draw_ct(draw: ImageDraw.ImageDraw, x: int, y: int, r: int, cat1: str) -> None:
    pal = palette(cat1)
    draw.ellipse([x - r, y - r, x + r, y + r], fill="#151a22", outline=pal[1], width=max(2, r // 18))
    for a in range(0, 360, 45):
        rr = r * 0.64
        px = x + int(math.cos(math.radians(a)) * rr)
        py = y + int(math.sin(math.radians(a)) * rr)
        draw.ellipse([px - r // 12, py - r // 12, px + r // 12, py + r // 12], fill="#d5dde6")
    draw.ellipse([x - r // 3, y - r // 4, x + r // 2, y + r // 3], fill="#8e9aa8")
    draw.ellipse([x + r // 8, y - r // 12, x + r // 3, y + r // 8], fill=pal[2])


def draw_virus(draw: ImageDraw.ImageDraw, x: int, y: int, r: int, cat1: str) -> None:
    pal = palette(cat1)
    for a in range(0, 360, 30):
        x2 = x + int(math.cos(math.radians(a)) * r * 1.25)
        y2 = y + int(math.sin(math.radians(a)) * r * 1.25)
        draw.line([x, y, x2, y2], fill=pal[1], width=max(2, r // 15))
        draw.ellipse([x2 - r // 7, y2 - r // 7, x2 + r // 7, y2 + r // 7], fill=pal[2])
    draw.ellipse([x - r, y - r, x + r, y + r], fill=pal[1], outline=pal[0], width=max(2, r // 13))
    draw.ellipse([x - r // 2, y - r // 2, x + r // 2, y + r // 2], outline="#ffffff", width=max(2, r // 12))


def draw_lab(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, cat1: str, keyword: str = "") -> None:
    pal = palette(cat1)
    labels = [keyword[:7] if keyword else "ALT", "AST", "DNA"]
    for i, lab in enumerate(labels[:3]):
        xx = x + i * int(s * 0.42)
        draw.rounded_rectangle([xx, y, xx + int(s * .24), y + s], radius=s // 12, fill="#ffffff", outline=pal[0], width=3)
        draw.rectangle([xx + 4, y + int(s * .55), xx + int(s * .24) - 4, y + s - 6], fill=pal[(i + 1) % len(pal)])
        draw.text((xx - 2, y - int(s * .22)), lab, fill=pal[0], font=font(max(14, s // 8), True))


def draw_ultrasound(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, cat1: str) -> None:
    pal = palette(cat1)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill="#20242b", outline=pal[1], width=4)
    for i in range(18):
        yy = y + 14 + i * (h - 30) // 18
        draw.arc([x + 20, yy - 20, x + w - 20, yy + 55], 190, 350, fill="#6f7f87", width=1)
    draw.polygon([(x + w * .28, y + h * .78), (x + w * .48, y + h * .36), (x + w * .70, y + h * .78)], fill="#52626e")
    draw.ellipse([x + int(w * .42), y + int(h * .46), x + int(w * .58), y + int(h * .60)], outline=pal[2], width=5)


def draw_chart(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, cat1: str, curve: bool = True) -> None:
    pal = palette(cat1)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill="#ffffff", outline="#d4dde2", width=2)
    draw.line([x + 32, y + h - 30, x + w - 18, y + h - 30], fill="#6b7780", width=2)
    draw.line([x + 32, y + 20, x + 32, y + h - 30], fill="#6b7780", width=2)
    if curve:
        pts = []
        for i in range(7):
            pts.append((x + 36 + i * (w - 70) // 6, y + 35 + int((i / 6) ** 1.2 * (h - 75))))
        draw.line(pts, fill=pal[1], width=5, joint="curve")
        pts2 = [(px, py + 18 + i * 4) for i, (px, py) in enumerate(pts)]
        draw.line(pts2, fill=pal[3], width=4, joint="curve")
    else:
        for i in range(6):
            bh = int((.25 + .11 * i + (i % 2) * .15) * (h - 60))
            draw.rectangle([x + 45 + i * 30, y + h - 31 - bh, x + 65 + i * 30, y + h - 31], fill=pal[(i % 3) + 1])


def draw_antibody(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, cat1: str) -> None:
    pal = palette(cat1)
    for off in [-s // 3, 0, s // 3]:
        draw.line([x, y, x + off, y - s // 2], fill=pal[1], width=max(4, s // 14))
    draw.line([x, y, x, y + s // 2], fill=pal[1], width=max(4, s // 14))
    draw.ellipse([x - s // 5, y - s // 8, x + s // 5, y + s // 4], fill=pal[2])


def draw_procedure(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, cat1: str) -> None:
    pal = palette(cat1)
    liver_shape(draw, x, y, s, rgba(pal[3], 230), pal[0])
    draw.ellipse([x + s // 6, y - s // 5, x + s // 2, y + s // 8], fill=pal[0])
    draw.line([x - s, y + s // 2, x + s // 4, y - s // 14], fill=pal[1], width=max(5, s // 16))
    draw.ellipse([x + s // 4 - 8, y - s // 14 - 8, x + s // 4 + 8, y - s // 14 + 8], fill=pal[2])


def draw_lifestyle(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, cat1: str) -> None:
    pal = palette(cat1)
    draw.ellipse([x - s, y - s // 2, x - s // 3, y + s // 3], fill=pal[2], outline=pal[0], width=2)
    draw.ellipse([x - s // 4, y - s // 2, x + s // 2, y + s // 3], fill=pal[1], outline=pal[0], width=2)
    draw.line([x + s // 2, y + s // 2, x + s, y - s // 2], fill=pal[0], width=6)
    draw.ellipse([x + s - 8, y - s // 2 - 8, x + s + 8, y - s // 2 + 8], fill=pal[3])


def draw_histology(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, cat1: str) -> None:
    pal = palette(cat1)
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill="#fae7ef", outline=pal[3], width=3)
    for i in range(80):
        px = x + 8 + (i * 37) % max(1, w - 16)
        py = y + 8 + (i * 53) % max(1, h - 16)
        rr = 4 + (i % 5)
        draw.ellipse([px - rr, py - rr, px + rr, py + rr], fill=["#c17bb0", "#7b5eb8", "#e99ab1", "#ad6b87"][i % 4])
    for i in range(8):
        yy = y + 18 + i * h // 9
        draw.arc([x + 12, yy - 25, x + w - 10, yy + 40], 190, 350, fill="#d692b0", width=2)


def draw_clinical(draw: ImageDraw.ImageDraw, x: int, y: int, s: int, cat1: str) -> None:
    pal = palette(cat1)
    draw.ellipse([x - s // 4, y - s, x + s // 4, y - s // 2], fill="#e4b89c", outline=pal[0], width=2)
    draw.rounded_rectangle([x - s // 2, y - s // 2, x + s // 2, y + s // 2], radius=s // 5, fill="#eef3f5", outline=pal[1], width=3)
    draw.arc([x - s // 3, y - s // 3, x + s // 3, y + s // 2], 0, 180, fill=pal[3], width=5)


def draw_motif(draw: ImageDraw.ImageDraw, vt: str, x: int, y: int, w: int, h: int, cat1: str, keyword: str = "") -> None:
    cx, cy = x + w // 2, y + h // 2
    s = min(w, h) // 2
    if vt == "radiology_ct_mri":
        draw_ct(draw, cx, cy, s, cat1)
    elif vt == "ultrasound_elastography":
        draw_ultrasound(draw, x + 10, y + 18, w - 20, h - 36, cat1)
    elif vt == "virology_diagram":
        draw_virus(draw, cx, cy, int(s * .62), cat1)
    elif vt == "serology_lab":
        draw_lab(draw, x + 24, y + 44, int(h * .58), cat1, keyword)
    elif vt == "treatment_schema":
        draw_lab(draw, x + 22, y + 38, int(h * .5), cat1, keyword)
        draw_chart(draw, x + w // 2, y + 38, w // 2 - 20, h - 75, cat1, curve=False)
    elif vt == "procedure_intervention":
        draw_procedure(draw, cx, cy, int(s * .85), cat1)
    elif vt == "lifestyle_metabolic":
        draw_lifestyle(draw, cx, cy, int(s * .75), cat1)
    elif vt == "histology_pathology":
        draw_histology(draw, x + 12, y + 18, w - 24, h - 36, cat1)
    elif vt == "clinical_context":
        draw_clinical(draw, cx, cy + s // 5, int(s * .9), cat1)
    elif vt == "gross_pathology":
        liver_shape(draw, cx, cy, int(s * .85), "#b9804e", "#5c3929")
        for i in range(8):
            dx = int(math.cos(i * 1.7) * s * .45)
            dy = int(math.sin(i * 2.1) * s * .25)
            draw.ellipse([cx + dx - 12, cy + dy - 9, cx + dx + 12, cy + dy + 9], fill="#7b4a31")
    elif vt == "anatomy_diagram":
        liver_shape(draw, cx, cy, int(s * .85), "#e7b46a", "#26364f")
        draw.line([cx - s // 2, cy + s // 3, cx + s // 2, cy - s // 5], fill="#2878b5", width=7)
        draw.line([cx - s // 3, cy + s // 3, cx + s // 3, cy + s // 5], fill="#c54c4c", width=5)
    else:
        draw_chart(draw, x + 18, y + 28, w - 36, h - 56, cat1, curve=True)


def render_top(topic: PageTopic, out_path: Path) -> None:
    w, h = 1280, 720
    im, draw = canvas(w, h, topic.category1)
    sc = 2
    pal = palette(topic.category1)
    cx, cy = int(w * .58 * sc), int(h * .50 * sc)
    liver_shape(draw, cx, cy, 230 * sc, rgba(pal[3], 225), pal[0])
    # Category-specific supporting cues.
    vts = {
        "hcc": ["radiology_ct_mri", "procedure_intervention", "statistical_plot"],
        "viral_hepatitis": ["virology_diagram", "serology_lab", "treatment_schema"],
        "masld_mash": ["lifestyle_metabolic", "ultrasound_elastography", "histology_pathology"],
        "cirrhosis_portal_htn": ["ultrasound_elastography", "anatomy_diagram", "clinical_context"],
        "liver_tests_diagnostics": ["serology_lab", "ultrasound_elastography", "statistical_plot"],
        "autoimmune_cholestatic": ["histology_pathology", "mechanism_diagram", "serology_lab"],
        "benign_liver_lesions": ["radiology_ct_mri", "ultrasound_elastography", "anatomy_diagram"],
        "general_hepatology": ["clinical_context", "serology_lab", "lifestyle_metabolic"],
    }[topic.category1]
    draw_motif(draw, vts[0], 74 * sc, 112 * sc, 350 * sc, 300 * sc, topic.category1, topic.keywords[0])
    draw_motif(draw, vts[1], 860 * sc, 80 * sc, 300 * sc, 240 * sc, topic.category1, topic.keywords[1])
    draw_motif(draw, vts[2], 860 * sc, 405 * sc, 300 * sc, 220 * sc, topic.category1, topic.keywords[2])
    # Subtle exact keyword anchors.
    f = font(28 * sc, True)
    for i, kw in enumerate(topic.keywords[:3]):
        x = 72 * sc + i * 210 * sc
        y = 650 * sc
        draw.rounded_rectangle([x, y, x + 180 * sc, y + 42 * sc], radius=20 * sc, fill=(255, 255, 255, 210), outline=rgba(pal[1], 180), width=2 * sc)
        draw.text((x + 16 * sc, y + 7 * sc), kw[:10], font=f, fill=pal[0])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    down(im.filter(ImageFilter.UnsharpMask(radius=1, percent=110)), w, h).save(out_path, "WEBP", quality=88, method=6)


def render_candidate(topic: PageTopic, keyword: str, vt: str, out_path: Path) -> None:
    w, h = 960, 720
    im, draw = canvas(w, h, topic.category1)
    sc = 2
    pal = palette(topic.category1)
    draw_motif(draw, vt, 94 * sc, 85 * sc, 770 * sc, 470 * sc, topic.category1, keyword)
    f = font(34 * sc, True)
    draw.rounded_rectangle([80 * sc, 610 * sc, 880 * sc, 676 * sc], radius=28 * sc, fill=(255, 255, 255, 220), outline=rgba(pal[1], 190), width=3 * sc)
    draw.text((112 * sc, 626 * sc), keyword[:24], font=f, fill=pal[0])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    down(im.filter(ImageFilter.UnsharpMask(radius=1, percent=110)), w, h).save(out_path, "WEBP", quality=88, method=6)


def write_prompts_and_images(topics: list[PageTopic], style: dict) -> None:
    for topic in topics:
        top_prompt = prompt_for_top(topic, style)
        (OUT / "prompts" / "top" / f"{topic.asset_id}.txt").write_text(top_prompt, encoding="utf-8")
        top_private = OUT / "generated" / "top" / f"{topic.asset_id}-top.webp"
        top_public = ASSET_OUT / "top" / f"{topic.asset_id}-top.webp"
        render_top(topic, top_private)
        shutil.copyfile(top_private, top_public)

        candidate_dir = OUT / "generated" / "candidates" / topic.asset_id
        prompt_dir = OUT / "prompts" / "lower-candidates" / topic.asset_id
        prompt_dir.mkdir(parents=True, exist_ok=True)
        selected_path = ""
        for i, keyword in enumerate(topic.keywords, 1):
            vt = visual_type_for_keyword(keyword, topic.title + " " + topic.description, topic.category1)
            candidate_name = f"{i:02d}-{slug_ascii(keyword)}-{vt}.webp"
            candidate_path = candidate_dir / candidate_name
            render_candidate(topic, keyword, vt, candidate_path)
            (prompt_dir / f"{i:02d}-{slug_ascii(keyword)}-{vt}.txt").write_text(
                prompt_for_candidate(topic, keyword, vt, style), encoding="utf-8"
            )
            if keyword == topic.selected_keyword:
                selected_path = str(candidate_path)
                selected_name = f"{topic.asset_id}-lower.webp"
                lower_private = OUT / "generated" / "lower" / selected_name
                lower_public = ASSET_OUT / "lower" / selected_name
                shutil.copyfile(candidate_path, lower_private)
                shutil.copyfile(candidate_path, lower_public)
                topic.selected_candidate = str(candidate_path.relative_to(ROOT)).replace("\\", "/")
        if not selected_path:
            first = sorted(candidate_dir.glob("*.webp"))[0]
            selected_name = f"{topic.asset_id}-lower.webp"
            shutil.copyfile(first, OUT / "generated" / "lower" / selected_name)
            shutil.copyfile(first, ASSET_OUT / "lower" / selected_name)
            topic.selected_candidate = str(first.relative_to(ROOT)).replace("\\", "/")


def write_manifests(topics: list[PageTopic], style: dict) -> None:
    rows = []
    for topic in topics:
        rows.append({
            "page_url": topic.url,
            "title": topic.title,
            "category1": topic.category1,
            "category1_ko": CATEGORY1[topic.category1]["ko"],
            "category2": topic.category2,
            "category2_ko": category2_label(topic.category1, topic.category2),
            "category3": topic.category3,
            "keywords": ";".join(topic.keywords),
            "top_image_public": f"/assets/img/page-generated/top/{topic.asset_id}-top.webp",
            "lower_image_public": f"/assets/img/page-generated/lower/{topic.asset_id}-lower.webp",
            "lower_selected_keyword": topic.selected_keyword,
            "selected_candidate_private": topic.selected_candidate,
            "top_prompt": f"private-figures/page-image-generation/prompts/top/{topic.asset_id}.txt",
            "candidate_prompt_dir": f"private-figures/page-image-generation/prompts/lower-candidates/{topic.asset_id}/",
            "candidate_image_dir": f"private-figures/page-image-generation/generated/candidates/{topic.asset_id}/",
            "asset_id": topic.asset_id,
        })
    fields = list(rows[0].keys())
    with (OUT / "page_image_manifest.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (OUT / "page_image_manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    (ASSET_OUT / "manifest.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    category_rows = []
    for topic in topics:
        category_rows.append({
            "page_url": topic.url,
            "title": topic.title,
            "category1_ko": CATEGORY1[topic.category1]["ko"],
            "category2_ko": category2_label(topic.category1, topic.category2),
            "category3": topic.category3,
            "keywords": ";".join(topic.keywords),
        })
    with (OUT / "topic_categories.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(category_rows[0].keys()))
        w.writeheader()
        w.writerows(category_rows)


def make_contact_sheet(paths: list[Path], out_path: Path, labeler, cols: int = 5, max_items: int = 120) -> None:
    paths = paths[:max_items]
    if not paths:
        return
    cell_w, cell_h = 300, 230
    sheet = Image.new("RGB", (cols * cell_w, math.ceil(len(paths) / cols) * cell_h), (246, 248, 247))
    draw = ImageDraw.Draw(sheet)
    f = font(13)
    fb = font(14, True)
    for i, p in enumerate(paths):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h
        try:
            im = Image.open(p).convert("RGB")
            im.thumbnail((270, 162), Image.Resampling.LANCZOS)
            sheet.paste(im, (x + (cell_w - im.width) // 2, y + 8))
        except Exception:
            pass
        title, sub = labeler(p)
        draw.text((x + 12, y + 176), title[:30], font=fb, fill=(22, 35, 43))
        draw.text((x + 12, y + 196), sub[:36], font=f, fill=(66, 82, 90))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, "JPEG", quality=88)


def make_contact_sheets(topics: list[PageTopic]) -> None:
    top_paths = [OUT / "generated" / "top" / f"{t.asset_id}-top.webp" for t in topics]
    lower_paths = [OUT / "generated" / "lower" / f"{t.asset_id}-lower.webp" for t in topics]
    id_to_topic = {t.asset_id: t for t in topics}

    def label(p: Path):
        stem = p.stem.replace("-top", "").replace("-lower", "")
        t = id_to_topic.get(stem)
        if not t:
            return (stem, "")
        return (t.title, f"{CATEGORY1[t.category1]['ko']} / {t.selected_keyword}")

    make_contact_sheet(top_paths, OUT / "contact-sheets" / "top-images-contact-sheet.jpg", label, max_items=120)
    make_contact_sheet(lower_paths, OUT / "contact-sheets" / "lower-selected-contact-sheet.jpg", label, max_items=120)


def write_readme(topics: list[PageTopic]) -> None:
    total_candidates = len(topics) * 5
    readme = f"""# Page Image Generation

Generated: 2026-05-14

Scope: {len(topics)} detail pages from `search-index.json`.

For each detail page:

- 1 top image was generated.
- 5 middle/lower candidate images were generated, one per keyword.
- 1 candidate was selected as the final middle/lower image.

## Claude Entry Points

- `page_image_manifest.csv`: page-by-page mapping with categories, keywords, final image paths, and candidate directories.
- `page_image_manifest.json`: same mapping as JSON.
- `topic_categories.csv`: compact category/keyword table.
- `style-masters/style_masters.json`: category1/category2/category3 style masters.
- `prompts/top/`: top image prompts.
- `prompts/lower-candidates/`: keyword candidate prompts.
- `generated/top/`: {len(topics)} private top images.
- `generated/candidates/`: {total_candidates} keyword candidate images.
- `generated/lower/`: {len(topics)} selected lower images.
- `contact-sheets/`: visual review sheets.

## Public Asset Paths

Final selected images are also copied to:

- `/assets/img/page-generated/top/`
- `/assets/img/page-generated/lower/`
- `/assets/img/page-generated/manifest.json`

The page HTML was not modified in this pass. Use `page_image_manifest.csv` to wire these images into pages later.

## Naming

Each file begins with a stable detail index and category slug, for example:

`d001-autoimmune-cholestatic-autoimmune-treatment-top.webp`

The manifest is the source of truth when a filename is not human-readable enough.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    topics = load_topics()
    style = make_style_masters(topics)
    write_prompts_and_images(topics, style)
    write_manifests(topics, style)
    make_contact_sheets(topics)
    write_readme(topics)
    summary = {
        "detail_pages": len(topics),
        "top_images": len(topics),
        "lower_candidate_images": len(topics) * 5,
        "selected_lower_images": len(topics),
        "category1_counts": {},
        "output_root": str(OUT),
        "public_asset_root": str(ASSET_OUT),
    }
    for topic in topics:
        summary["category1_counts"][CATEGORY1[topic.category1]["ko"]] = summary["category1_counts"].get(CATEGORY1[topic.category1]["ko"], 0) + 1
    (OUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
