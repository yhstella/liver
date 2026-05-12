#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import math
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "private-figures" / "personal-web-figures"
IMG_DIR = OUT / "images"
THUMB_DIR = OUT / "thumbs"
MANIFEST = OUT / "manifest.csv"
CONTACT = OUT / "contact-sheet.jpg"
INDEX = OUT / "index.html"
SUMMARY = OUT / "summary.json"
QUERY_PLAN = OUT / "multilingual-query-plan.json"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
EUTILS_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EUTILS_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PMC_ARTICLE = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
USER_AGENT = "drshin-personal-hepatology-figure-archive/1.0 (personal study archive)"

FONT = Path("C:/Windows/Fonts/malgun.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/malgunbd.ttf")

FIELDS = [
    "figure_id",
    "topic",
    "subtopic",
    "meaning_ko",
    "local_path",
    "thumb_path",
    "source_kind",
    "source_url",
    "pmcid",
    "doi",
    "article_title",
    "figure_label",
    "figure_title",
    "caption",
    "license_text",
    "rights_note",
    "query",
    "width",
    "height",
    "score",
    "sha1",
    "date_collected",
]


TOPICS = [
    {
        "topic": "hcc_systemic_trial",
        "subtopic": "HCC systemic therapy, survival curves, BCLC, treatment algorithms",
        "meaning_ko": "간세포암 전신치료, 생존곡선, BCLC 병기와 치료 선택을 공부하기 위한 figure",
        "max": 28,
        "queries": [
            "hepatocellular carcinoma atezolizumab bevacizumab survival curve",
            "hepatocellular carcinoma durvalumab tremelimumab survival curve",
            "hepatocellular carcinoma nivolumab ipilimumab survival curve",
            "hepatocellular carcinoma lenvatinib sorafenib overall survival",
            "hepatocellular carcinoma BCLC treatment algorithm",
            "hepatocellular carcinoma TACE ablation radioembolization algorithm",
            "간세포암 아테졸리주맙 베바시주맙 생존곡선",
            "肝細胞癌 アテゾリズマブ ベバシズマブ 生存曲線",
            "肝细胞癌 阿替利珠单抗 贝伐珠单抗 生存曲线",
            "carcinome hépatocellulaire atézolizumab bevacizumab survie",
        ],
        "caption_terms": [
            "hepatocellular", "hcc", "atezolizumab", "bevacizumab", "durvalumab",
            "tremelimumab", "nivolumab", "ipilimumab", "lenvatinib", "sorafenib",
            "survival", "kaplan", "overall survival", "progression-free", "bclc",
            "tace", "ablation", "radioembolization", "treatment algorithm",
        ],
        "commons_categories": [
            "Category:Hepatocellular carcinoma",
            "Category:CT images of hepatocellular carcinoma",
            "Category:Ultrasound images of hepatocellular carcinoma",
            "Category:Histopathology of hepatocellular carcinoma",
        ],
    },
    {
        "topic": "hcc_imaging_pathology",
        "subtopic": "HCC CT/MRI/US, arterial enhancement, washout, pathology",
        "meaning_ko": "간암의 동맥기 조영증강, washout, 초음파/CT/MRI, 병리 소견을 공부하기 위한 figure",
        "max": 24,
        "queries": [
            "hepatocellular carcinoma arterial phase washout CT MRI figure",
            "hepatocellular carcinoma contrast enhanced ultrasound figure",
            "hepatocellular carcinoma histology gross pathology figure",
            "LI-RADS hepatocellular carcinoma arterial phase washout figure",
            "간세포암 CT MRI 동맥기 washout",
            "肝細胞癌 CT MRI 動脈相 washout",
            "肝细胞癌 CT MRI 动脉期 washout",
            "carcinoma hepatocelular fase arterial lavado",
        ],
        "caption_terms": ["hcc", "hepatocellular", "carcinoma", "arterial", "washout", "li-rads", "ultrasound", "ct", "mri", "histology", "pathology"],
        "commons_categories": [
            "Category:CT images of hepatocellular carcinoma",
            "Category:Ultrasound images of hepatocellular carcinoma",
            "Category:Histopathology of hepatocellular carcinoma",
            "Category:Gross pathology of hepatocellular carcinoma",
        ],
    },
    {
        "topic": "hbv_lifecycle_serology",
        "subtopic": "HBV lifecycle, cccDNA, serology, natural history, functional cure",
        "meaning_ko": "B형간염 life cycle, cccDNA, 혈청표지자, 자연사, functional cure 개념 figure",
        "max": 22,
        "queries": [
            "hepatitis B virus life cycle cccDNA figure",
            "hepatitis B serology interpretation HBsAg anti-HBs anti-HBc figure",
            "chronic hepatitis B natural history HBeAg phases figure",
            "hepatitis B functional cure HBsAg loss figure",
            "B형간염 생활사 cccDNA 혈청표지자",
            "B型肝炎ウイルス ライフサイクル cccDNA",
            "乙型肝炎病毒 生命周期 cccDNA",
        ],
        "caption_terms": ["hepatitis b", "hbv", "hbsag", "hbeag", "anti-hbc", "cccDNA", "life cycle", "replication", "serology", "functional cure"],
        "commons_categories": ["Category:Hepatitis B virus"],
    },
    {
        "topic": "hcv_daa_lifecycle",
        "subtopic": "HCV lifecycle, direct-acting antivirals, SVR, retreatment",
        "meaning_ko": "C형간염 life cycle, DAA 표적, SVR, 재치료 전략을 공부하기 위한 figure",
        "max": 18,
        "queries": [
            "hepatitis C virus life cycle direct acting antiviral figure",
            "HCV replication cycle NS3 NS5A NS5B figure",
            "hepatitis C DAA treatment algorithm SVR figure",
            "C형간염 DAA 생활사 SVR",
            "C型肝炎ウイルス DAA ライフサイクル",
            "丙型肝炎病毒 DAA 生命周期",
        ],
        "caption_terms": ["hepatitis c", "hcv", "daa", "direct-acting", "ns3", "ns5a", "ns5b", "svr", "replication", "life cycle"],
        "commons_categories": ["Category:Hepatitis C virus"],
    },
    {
        "topic": "masld_mash",
        "subtopic": "MASLD/MASH pathogenesis, histology, fibrosis, drugs, lifestyle",
        "meaning_ko": "MASLD/MASH의 병태생리, 조직 소견, 섬유화, 약물·식이·운동 치료 figure",
        "max": 28,
        "queries": [
            "MASH NASH pathogenesis histology ballooning fibrosis figure",
            "metabolic dysfunction-associated steatotic liver disease treatment algorithm figure",
            "resmetirom MASH trial histology fibrosis figure",
            "GLP-1 semaglutide MASH liver fat figure",
            "fatty liver ultrasound steatosis figure",
            "Mediterranean diet MASLD figure",
            "지방간 MASH 병리 ballooning fibrosis",
            "脂肪肝 MASH 病理 線維化",
            "脂肪肝 MASH 纤维化 组织学",
            "hígado graso MASH fibrosis histología",
        ],
        "caption_terms": ["masld", "nafld", "nash", "mash", "steatosis", "steatohepatitis", "ballooning", "fibrosis", "resmetirom", "semaglutide", "glp-1", "diet", "exercise", "ultrasound"],
        "commons_categories": ["Category:Fatty liver", "Category:Ultrasound images of fatty liver"],
    },
    {
        "topic": "cirrhosis_portal_htn",
        "subtopic": "cirrhosis, portal hypertension, varices, ascites, TIPS, HE, HRS",
        "meaning_ko": "간경변, 문맥고혈압, 정맥류, 복수, TIPS, 간성뇌증, HRS figure",
        "max": 30,
        "queries": [
            "portal hypertension esophageal varices endoscopy banding figure",
            "cirrhosis ascites paracentesis ultrasound figure",
            "TIPS portal hypertension procedure figure",
            "hepatic encephalopathy ammonia pathogenesis figure",
            "hepatorenal syndrome pathophysiology treatment figure",
            "Baveno VII portal hypertension decompensation figure",
            "간경변 문맥고혈압 식도정맥류 복수 TIPS",
            "門脈圧亢進症 食道静脈瘤 腹水 TIPS",
            "门静脉高压 食管静脉曲张 腹水 TIPS",
            "hypertension portale varices ascite TIPS",
        ],
        "caption_terms": ["cirrhosis", "portal hypertension", "varices", "banding", "ascites", "paracentesis", "tips", "hepatic encephalopathy", "hepatorenal", "baveno"],
        "commons_categories": [
            "Category:Esophageal varices",
            "Category:Endoscopic images of esophageal varices",
            "Category:CT images of esophageal varices",
            "Category:Ascites",
            "Category:Ultrasound images of ascites",
            "Category:Ultrasound images of cirrhosis",
            "Category:Transjugular intrahepatic portosystemic shunt",
        ],
    },
    {
        "topic": "autoimmune_cholestatic",
        "subtopic": "AIH, PBC, PSC, IgG4-SC, overlap",
        "meaning_ko": "자가면역간염, PBC, PSC, IgG4 담관염, overlap의 병리·영상·치료 알고리즘 figure",
        "max": 22,
        "queries": [
            "autoimmune hepatitis histology interface hepatitis treatment algorithm figure",
            "primary biliary cholangitis florid duct lesion histology figure",
            "primary sclerosing cholangitis MRCP cholangiogram figure",
            "IgG4 sclerosing cholangitis imaging figure",
            "AIH PBC overlap diagnostic criteria figure",
            "자가면역간염 PBC PSC 병리 MRCP",
            "自己免疫性肝炎 PBC PSC 病理 MRCP",
            "自身免疫性肝炎 PBC PSC 病理 MRCP",
        ],
        "caption_terms": ["autoimmune hepatitis", "aih", "primary biliary", "pbc", "primary sclerosing", "psc", "igg4", "overlap", "interface", "florid duct", "mrcp", "cholangiogram"],
        "commons_categories": [
            "Category:Primary sclerosing cholangitis",
            "Category:CT images of primary sclerosing cholangitis",
        ],
    },
    {
        "topic": "benign_liver_lesions",
        "subtopic": "hemangioma, FNH, hepatocellular adenoma, cysts, focal fat",
        "meaning_ko": "혈관종, FNH, 간선종, 간낭종, focal fat 등 양성 간병변 감별 figure",
        "max": 24,
        "queries": [
            "hepatic hemangioma ultrasound CT MRI figure",
            "focal nodular hyperplasia MRI hepatobiliary phase figure",
            "hepatocellular adenoma MRI subtype figure",
            "liver cyst ultrasound figure",
            "focal fat sparing liver ultrasound MRI figure",
            "간 혈관종 FNH 간선종 MRI 초음파",
            "肝血管腫 FNH 肝細胞腺腫 MRI 超音波",
            "肝血管瘤 FNH 肝细胞腺瘤 MRI 超声",
        ],
        "caption_terms": ["hemangioma", "fnh", "focal nodular", "adenoma", "hca", "liver cyst", "hepatic cyst", "focal fat", "ultrasound", "mri", "ct"],
        "commons_categories": [
            "Category:Ultrasound images of hepatic hemangioma",
            "Category:Ultrasound images of liver cysts",
            "Category:Ultrasound images of livers",
        ],
    },
    {
        "topic": "liver_tests_diagnostics",
        "subtopic": "LFT, bilirubin, ALP/GGT, elastography, biopsy, fibrosis scores",
        "meaning_ko": "간수치, 빌리루빈, ALP/GGT, FIB-4, elastography, 간생검 결과 해석 figure",
        "max": 18,
        "queries": [
            "FIB-4 liver fibrosis elastography algorithm figure",
            "transient elastography liver stiffness figure",
            "bilirubin metabolism direct indirect jaundice figure",
            "cholestatic liver enzymes ALP GGT algorithm figure",
            "liver biopsy fibrosis staging figure",
            "간수치 빌리루빈 ALP GGT FIB-4 FibroScan",
            "肝機能検査 ビリルビン ALP GGT FIB-4",
            "肝功能检查 胆红素 ALP GGT FIB-4",
        ],
        "caption_terms": ["fib-4", "fibrosis", "elastography", "fibroscan", "liver stiffness", "bilirubin", "alp", "ggt", "jaundice", "biopsy", "ishak", "metavir"],
        "commons_categories": [
            "Category:Ultrasound images of livers",
        ],
    },
    {
        "topic": "acute_liver_failure_transplant",
        "subtopic": "ALF, ACLF, liver failure, transplant criteria",
        "meaning_ko": "급성간부전, ACLF, 간이식 평가와 예후 점수 figure",
        "max": 12,
        "queries": [
            "acute liver failure management algorithm figure",
            "acute-on-chronic liver failure ACLF pathophysiology figure",
            "King's College criteria acute liver failure figure",
            "liver transplantation MELD allocation figure",
            "급성간부전 ACLF 간이식 MELD",
            "急性肝不全 ACLF 肝移植 MELD",
            "急性肝衰竭 ACLF 肝移植 MELD",
        ],
        "caption_terms": ["acute liver failure", "alf", "aclf", "king's college", "transplant", "meld", "liver failure", "prognosis"],
        "commons_categories": [],
    },
]


@dataclass
class Candidate:
    source_kind: str
    topic: str
    subtopic: str
    meaning_ko: str
    title: str
    caption: str
    image_urls: list[str]
    source_url: str
    pmcid: str = ""
    doi: str = ""
    article_title: str = ""
    figure_label: str = ""
    license_text: str = ""
    query: str = ""


def req_bytes(url: str, delay: float = 0.0, timeout: int = 35) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read()
    if delay:
        time.sleep(delay)
    return data


def req_json(url: str, delay: float = 0.0) -> dict:
    return json.loads(req_bytes(url, delay).decode("utf-8"))


def clean(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def path_slug(value: str) -> str:
    value = re.sub(r"^File:", "", clean(value), flags=re.I)
    value = re.sub(r"\.[A-Za-z0-9]{2,5}$", "", value)
    value = re.sub(r"[^A-Za-z0-9가-힣一-龥ぁ-ゟ゠-ヿ]+", "-", value).strip("-").lower()
    return value[:72] or "figure"


def text_key(value: str) -> str:
    value = clean(value).lower()
    value = re.sub(r"\.(jpg|jpeg|png|svg|gif|webp|tif|tiff)$", "", value)
    return re.sub(r"[^a-z0-9가-힣一-龥ぁ-ゟ゠-ヿ]+", "-", value).strip("-")


def score_caption(caption: str, terms: list[str]) -> int:
    low = caption.lower()
    hits = sum(1 for term in terms if term.lower() in low)
    value_terms = ["kaplan", "survival", "algorithm", "pathway", "mechanism", "life cycle", "histology", "ct", "mri", "ultrasound", "endoscopy", "treatment", "diagnosis"]
    value_hits = sum(1 for term in value_terms if term in low)
    return hits * 18 + value_hits * 8


def xml_text(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return clean(" ".join(elem.itertext()))


def pmc_esearch(term: str, delay: float, retmax: int) -> list[str]:
    params = {
        "db": "pmc",
        "term": f"({term}) AND open access[filter]",
        "retmax": str(retmax),
        "retmode": "json",
        "sort": "relevance",
    }
    url = f"{EUTILS_SEARCH}?{urllib.parse.urlencode(params)}"
    try:
        payload = req_json(url, delay)
    except Exception:
        return []
    return payload.get("esearchresult", {}).get("idlist", [])


def pmc_license(root: ET.Element) -> str:
    chunks = []
    for lic in root.findall(".//license"):
        chunks.append(lic.attrib.get("{http://www.w3.org/1999/xlink}href", ""))
        chunks.append(lic.attrib.get("license-type", ""))
        chunks.append(xml_text(lic))
    return clean(" ".join(chunks))


def pmc_candidates(cfg: dict, delay: float, article_limit: int) -> list[Candidate]:
    out: list[Candidate] = []
    seen_articles: set[str] = set()
    terms = cfg["caption_terms"]
    for query in cfg["queries"]:
        ids = pmc_esearch(query, delay, article_limit)
        for pmc_id in ids:
            if pmc_id in seen_articles:
                continue
            seen_articles.add(pmc_id)
            params = {"db": "pmc", "id": pmc_id, "retmode": "xml"}
            url = f"{EUTILS_FETCH}?{urllib.parse.urlencode(params)}"
            try:
                root = ET.fromstring(req_bytes(url, delay, timeout=45))
            except Exception:
                continue
            pmcid_num = xml_text(root.find(".//article-id[@pub-id-type='pmc']")) or pmc_id
            pmcid = f"PMC{pmcid_num}" if not pmcid_num.startswith("PMC") else pmcid_num
            article_title = xml_text(root.find(".//article-title"))
            doi = xml_text(root.find(".//article-id[@pub-id-type='doi']"))
            license_text = pmc_license(root)
            article_url = PMC_ARTICLE.format(pmcid=pmcid)
            instance_bin = f"https://pmc.ncbi.nlm.nih.gov/articles/instance/{pmcid_num}/bin/"
            for fig in root.findall(".//fig"):
                label = xml_text(fig.find("label"))
                caption = xml_text(fig.find("caption"))
                if score_caption(f"{article_title} {label} {caption}", terms) < 28:
                    continue
                graphics = fig.findall(".//graphic")
                for graphic in graphics[:2]:
                    href = graphic.attrib.get("{http://www.w3.org/1999/xlink}href", "")
                    if not href:
                        continue
                    href_stem = re.sub(r"\.(jpg|jpeg|png|gif|tif|tiff)$", "", href, flags=re.I)
                    image_urls = [f"{instance_bin}{href_stem}{ext}" for ext in [".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff"]]
                    out.append(
                        Candidate(
                            source_kind="pmc_open_access",
                            topic=cfg["topic"],
                            subtopic=cfg["subtopic"],
                            meaning_ko=cfg["meaning_ko"],
                            title=f"{pmcid} {label} {article_title}",
                            caption=caption,
                            image_urls=image_urls,
                            source_url=article_url,
                            pmcid=pmcid,
                            doi=doi,
                            article_title=article_title,
                            figure_label=label,
                            license_text=license_text,
                            query=query,
                        )
                    )
    return out


def commons_pages_for_query(query: str, delay: float, limit: int = 25) -> list[dict]:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|mime|size|sha1|extmetadata",
        "iiurlwidth": "1800",
        "origin": "*",
    }
    try:
        payload = req_json(f"{COMMONS_API}?{urllib.parse.urlencode(params)}", delay)
    except Exception:
        return []
    return sorted(payload.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 999))


def commons_pages_for_category(category: str, delay: float, limit: int = 30) -> list[dict]:
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": category,
        "cmnamespace": "6",
        "cmlimit": str(limit),
        "origin": "*",
    }
    try:
        payload = req_json(f"{COMMONS_API}?{urllib.parse.urlencode(params)}", delay)
    except Exception:
        return []
    titles = [m["title"] for m in payload.get("query", {}).get("categorymembers", []) if m.get("title")]
    if not titles:
        return []
    params = {
        "action": "query",
        "format": "json",
        "titles": "|".join(titles[:50]),
        "prop": "imageinfo",
        "iiprop": "url|mime|size|sha1|extmetadata",
        "iiurlwidth": "1800",
        "origin": "*",
    }
    try:
        payload = req_json(f"{COMMONS_API}?{urllib.parse.urlencode(params)}", delay)
    except Exception:
        return []
    return sorted(payload.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("title", ""))


def commons_candidates(cfg: dict, delay: float) -> list[Candidate]:
    out: list[Candidate] = []
    seen: set[str] = set()
    sources = [(cat, commons_pages_for_category(cat, delay)) for cat in cfg["commons_categories"]]
    sources.extend((query, commons_pages_for_query(query, delay)) for query in cfg["queries"])
    for query, pages in sources:
        for page in pages:
            title = page.get("title", "")
            if not title or title in seen:
                continue
            seen.add(title)
            info = (page.get("imageinfo") or [{}])[0]
            if info.get("mime") not in {"image/jpeg", "image/png", "image/webp", "image/svg+xml"}:
                continue
            meta = info.get("extmetadata", {})
            desc = clean(meta.get("ImageDescription", {}).get("value", ""))
            search_text = f"{title} {desc}"
            if score_caption(search_text, cfg["caption_terms"]) < 18:
                continue
            license_text = clean(" ".join([
                meta.get("LicenseShortName", {}).get("value", ""),
                meta.get("UsageTerms", {}).get("value", ""),
            ]))
            image_url = info.get("thumburl") or info.get("url", "")
            if not image_url:
                continue
            out.append(
                Candidate(
                    source_kind="wikimedia_commons",
                    topic=cfg["topic"],
                    subtopic=cfg["subtopic"],
                    meaning_ko=cfg["meaning_ko"],
                    title=title,
                    caption=desc or title,
                    image_urls=[image_url],
                    source_url=info.get("descriptionurl", ""),
                    license_text=license_text,
                    query=query,
                )
            )
    return out


def download(candidate: Candidate, delay: float) -> bytes | None:
    for url in candidate.image_urls:
        try:
            return req_bytes(url, delay, timeout=25)
        except Exception:
            continue
    return None


def image_score(data: bytes) -> tuple[Image.Image | None, int]:
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:
        return None, -100
    w, h = im.size
    area = w * h
    if w < 260 or h < 180 or area < 70_000:
        return im, -100
    rgb = ImageOps.exif_transpose(im.convert("RGB"))
    small = rgb.resize((96, 96), Image.Resampling.LANCZOS).convert("L")
    entropy = small.entropy()
    edge = ImageStat.Stat(small.filter(ImageFilter.FIND_EDGES)).mean[0]
    score = 45
    if area >= 1_000_000:
        score += 24
    elif area >= 350_000:
        score += 15
    else:
        score += 6
    ratio = max(w / max(h, 1), h / max(w, 1))
    if ratio > 5.2:
        score -= 25
    if entropy >= 5:
        score += 14
    elif entropy < 2.1:
        score -= 24
    if edge > 18:
        score += 6
    return rgb, score


def save_image(im: Image.Image, dest_base: Path) -> Path:
    dest_base.parent.mkdir(parents=True, exist_ok=True)
    dest = dest_base.with_suffix(".jpg")
    im.save(dest, "JPEG", quality=92, optimize=True)
    return dest


def make_thumb(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    im.thumbnail((280, 190), Image.Resampling.LANCZOS)
    bg = Image.new("RGB", (280, 190), (246, 248, 247))
    bg.paste(im, ((280 - im.width) // 2, (190 - im.height) // 2))
    bg.save(dest, "JPEG", quality=86)


def load_manifest() -> list[dict[str, str]]:
    if not MANIFEST.exists():
        return []
    with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_manifest(rows: list[dict[str, str]]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def next_id(rows: list[dict[str, str]]) -> int:
    nums = []
    for row in rows:
        m = re.search(r"pwf_(\d+)", row.get("figure_id", ""))
        if m:
            nums.append(int(m.group(1)))
    return max(nums or [0]) + 1


def save_query_plan() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plan = {
        cfg["topic"]: {
            "subtopic": cfg["subtopic"],
            "meaning_ko": cfg["meaning_ko"],
            "queries": cfg["queries"],
            "caption_terms": cfg["caption_terms"],
            "commons_categories": cfg["commons_categories"],
        }
        for cfg in TOPICS
    }
    QUERY_PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")


def write_contact(rows: list[dict[str, str]]) -> None:
    font = ImageFont.truetype(str(FONT), 13) if FONT.exists() else ImageFont.load_default()
    font_b = ImageFont.truetype(str(FONT_BOLD), 13) if FONT_BOLD.exists() else font
    items = []
    for row in rows:
        p = ROOT / row["thumb_path"]
        try:
            im = Image.open(p).convert("RGB")
            items.append((row, im.copy()))
        except Exception:
            continue
    if not items:
        return
    cols = 4
    cell_w, cell_h = 320, 260
    sheet = Image.new("RGB", (cols * cell_w, math.ceil(len(items) / cols) * cell_h), (246, 248, 247))
    draw = ImageDraw.Draw(sheet)
    for i, (row, im) in enumerate(items):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h
        sheet.paste(im, (x + (cell_w - im.width) // 2, y + 8))
        draw.text((x + 12, y + 202), row["figure_id"], font=font_b, fill=(22, 35, 43))
        draw.text((x + 12, y + 222), row["topic"][:38], font=font, fill=(55, 70, 78))
        draw.text((x + 12, y + 240), row["figure_label"][:38], font=font, fill=(80, 92, 98))
    CONTACT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT, "JPEG", quality=88)


def write_index(rows: list[dict[str, str]]) -> None:
    topics = sorted({r["topic"] for r in rows})
    cards = []
    for r in rows:
        thumb = html.escape(r["thumb_path"].replace("private-figures/personal-web-figures/", ""))
        img = html.escape(r["local_path"].replace("private-figures/personal-web-figures/", ""))
        search = html.escape(" ".join([r["topic"], r["subtopic"], r["caption"], r["article_title"], r["figure_title"]]).lower())
        cards.append(
            f'''<article class="card" data-topic="{html.escape(r['topic'])}" data-search="{search}">
  <a href="{img}"><img src="{thumb}" alt="{html.escape(r['figure_id'])}"></a>
  <h2>{html.escape(r['figure_id'])} · {html.escape(r['topic'])}</h2>
  <p>{html.escape(r['figure_title'][:180])}</p>
  <p class="meta">{html.escape(r['source_kind'])}<br><a href="{html.escape(r['source_url'])}">source</a></p>
</article>'''
        )
    options = "\n".join(f'<option value="{html.escape(t)}">{html.escape(t)}</option>' for t in topics)
    INDEX.write_text(
        f"""<!doctype html>
<html lang="ko">
<meta charset="utf-8">
<title>Personal Web Hepatology Figures</title>
<style>
body{{font-family:system-ui,Malgun Gothic,sans-serif;margin:0;background:#f7f8f8;color:#18252b}}
header{{position:sticky;top:0;background:#ffffffe8;border-bottom:1px solid #dbe3df;padding:16px 20px;z-index:1}}
h1{{font-size:22px;margin:0 0 10px}}
.controls{{display:flex;gap:10px;flex-wrap:wrap}}
input,select{{font-size:14px;padding:8px 10px;border:1px solid #b8c6c1;border-radius:6px;background:white}}
input{{width:min(560px,78vw)}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px;padding:18px}}
.card{{background:white;border:1px solid #dbe3df;border-radius:8px;padding:10px}}
.card[hidden]{{display:none}}
img{{width:100%;height:190px;object-fit:contain;background:#eef2f0}}
h2{{font-size:14px;margin:9px 0 5px}}
p{{font-size:12px;line-height:1.4;margin:5px 0;color:#53636b}}
.meta{{color:#6a777d}}
a{{color:#1f6f8b}}
</style>
<header>
<h1>Personal Web Hepatology Figures</h1>
<div class="controls"><input id="q" type="text" placeholder="keyword, topic, caption"><select id="topic"><option value="">all topics</option>{options}</select></div>
</header>
<main>{''.join(cards)}</main>
<script>
const q=document.querySelector('#q'), topic=document.querySelector('#topic');
function apply(){{
  const query=q.value.trim().toLowerCase(), t=topic.value;
  document.querySelectorAll('.card').forEach(card=>{{
    const okQ=!query || card.dataset.search.includes(query);
    const okT=!t || card.dataset.topic===t;
    card.hidden=!(okQ&&okT);
  }});
}}
[q,topic].forEach(el=>el.addEventListener('input',apply));
apply();
</script>
</html>""",
        encoding="utf-8",
    )


def collect(target: int, delay: float, pmc_article_limit: int, skip_commons: bool, skip_pmc: bool) -> list[dict[str, str]]:
    OUT.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_manifest()
    seen_sha = {r["sha1"] for r in rows if r.get("sha1")}
    seen_title = {text_key(r.get("figure_title") or r.get("caption") or r.get("source_url", "")) for r in rows}
    n = next_id(rows)
    today = date.today().isoformat()
    added: list[dict[str, str]] = []
    per_topic = Counter(r["topic"] for r in rows)

    for cfg in TOPICS:
        if len(added) >= target:
            break
        candidates: list[Candidate] = []
        if not skip_pmc:
            candidates.extend(pmc_candidates(cfg, delay, pmc_article_limit))
        if not skip_commons:
            candidates.extend(commons_candidates(cfg, delay))
        candidates.sort(key=lambda c: score_caption(f"{c.title} {c.caption}", cfg["caption_terms"]), reverse=True)
        print(f"{cfg['topic']}: candidates {len(candidates)}", flush=True)
        for c in candidates:
            if len(added) >= target or per_topic[c.topic] >= cfg["max"]:
                break
            tkey = text_key(c.title or c.caption)
            if tkey and tkey in seen_title:
                continue
            data = download(c, delay)
            if not data:
                continue
            sha = hashlib.sha1(data).hexdigest()
            if sha in seen_sha:
                continue
            im, img_score = image_score(data)
            if im is None or img_score < 42:
                continue
            relevance = score_caption(f"{c.title} {c.caption}", cfg["caption_terms"])
            score = min(100, img_score + min(35, relevance))
            figure_id = f"pwf_{n:05d}"
            n += 1
            dest = save_image(im, IMG_DIR / c.topic / f"{figure_id}_{path_slug(c.title)}")
            thumb = THUMB_DIR / c.topic / f"{figure_id}.jpg"
            make_thumb(dest, thumb)
            row = {
                "figure_id": figure_id,
                "topic": c.topic,
                "subtopic": c.subtopic,
                "meaning_ko": c.meaning_ko,
                "local_path": dest.relative_to(ROOT).as_posix(),
                "thumb_path": thumb.relative_to(ROOT).as_posix(),
                "source_kind": c.source_kind,
                "source_url": c.source_url,
                "pmcid": c.pmcid,
                "doi": c.doi,
                "article_title": c.article_title,
                "figure_label": c.figure_label,
                "figure_title": clean(c.title),
                "caption": clean(c.caption)[:1800],
                "license_text": clean(c.license_text)[:900],
                "rights_note": "Personal study archive only. Do not reuse or publish without checking the source page and rights/licence.",
                "query": c.query,
                "width": str(im.width),
                "height": str(im.height),
                "score": str(score),
                "sha1": sha,
                "date_collected": today,
            }
            rows.append(row)
            added.append(row)
            per_topic[c.topic] += 1
            seen_sha.add(sha)
            if tkey:
                seen_title.add(tkey)
    write_manifest(rows)
    return added


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect important hepatology figures from web sources for personal study.")
    parser.add_argument("--target", type=int, default=80)
    parser.add_argument("--delay", type=float, default=0.2)
    parser.add_argument("--pmc-article-limit", type=int, default=4)
    parser.add_argument("--skip-commons", action="store_true")
    parser.add_argument("--skip-pmc", action="store_true")
    args = parser.parse_args()

    save_query_plan()
    added = collect(args.target, args.delay, args.pmc_article_limit, args.skip_commons, args.skip_pmc)
    rows = load_manifest()
    write_contact(rows)
    write_index(rows)
    summary = {
        "date": date.today().isoformat(),
        "added_this_run": len(added),
        "total_figures": len(rows),
        "by_topic": dict(Counter(r["topic"] for r in rows)),
        "manifest": str(MANIFEST),
        "contact_sheet": str(CONTACT),
        "index": str(INDEX),
        "query_plan": str(QUERY_PLAN),
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
