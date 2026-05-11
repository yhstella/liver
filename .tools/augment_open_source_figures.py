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
import shutil
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "private-figures" / "manifest.csv"
PRIVATE_DB = ROOT / "private-figures" / "db"
ASSETS_DB = ROOT / "assets" / "img" / "db"
AUDIT_DIR = ROOT / "private-figures" / "open-license-audit"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
EUTILS_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EUTILS_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
PMC_ARTICLE = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
USER_AGENT = "drshin-open-license-figure-augment/1.1 (personal educational hepatology archive)"

FONT = Path("C:/Windows/Fonts/malgun.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/malgunbd.ttf")

MANIFEST_FIELDS = [
    "image_id",
    "topics",
    "keywords",
    "meaning_ko",
    "local_path",
    "value_score",
    "source_file",
    "context_excerpt",
]

ALLOWED_LICENSE_PARTS = [
    "cc0",
    "public domain",
    "cc by",
    "cc-by",
    "cc by-sa",
    "cc-by-sa",
    "gfdl",
]

DISALLOWED_LICENSE_PARTS = [
    "noncommercial",
    "non-commercial",
    "cc by-nc",
    "cc-by-nc",
    "by-nc",
    "no derivatives",
    "cc by-nd",
    "cc-by-nd",
    "by-nd",
]

TITLE_EXCLUDE = [
    "animal",
    "rat",
    "mouse",
    "mice",
    "goat",
    "sheep",
    "dog",
    "cat",
    "horse",
    "equine",
    "pig",
    "bird",
    "snail",
    "hyena",
    "map",
    "flag",
    "logo",
    "icon",
    "emblem",
    "stamp",
    "coin",
    "airport",
    "aircraft",
    "restaurant facade",
    "facade",
    "museum",
    "painting",
    "poster",
    "cartoon",
    "esophageal stricture",
    "stricture dilation",
    "gene therapy",
]


@dataclass
class Candidate:
    source: str
    topic: str
    topics: str
    keywords: str
    meaning_ko: str
    title: str
    caption: str
    image_url: str
    source_url: str
    license_text: str
    author: str
    credit: str
    query: str


TOPICS = [
    {
        "topic": "autoimmune_cholestatic",
        "topics": "autoimmune_cholestatic;imaging;pathology",
        "meaning_ko": "AIH/PBC/PSC 같은 자가면역·담즙정체성 간질환의 병리, 담도 영상, 진단 개념을 보여주는 open-license figure",
        "keywords": [
            "autoimmune hepatitis histology interface hepatitis",
            "primary biliary cholangitis histology florid duct lesion",
            "primary sclerosing cholangitis cholangiogram",
            "primary sclerosing cholangitis CT",
            "primary sclerosing cholangitis MRCP",
            "자가면역간염 조직 interface hepatitis",
            "원발담즙성담관염 병리",
            "原発性胆汁性胆管炎 病理",
            "原发性胆汁性胆管炎 病理",
            "colangitis biliar primaria histología",
            "cholangite biliaire primitive histologie",
            "primär sklerosierende Cholangitis Cholangiogramm",
            "первичный склерозирующий холангит холангиограмма",
        ],
        "commons_categories": [
            "Category:Primary sclerosing cholangitis",
            "Category:CT images of primary sclerosing cholangitis",
        ],
        "pmc_terms": [
            "primary sclerosing cholangitis MRCP figure",
            "autoimmune hepatitis histology figure",
            "primary biliary cholangitis histology figure",
        ],
        "caption_terms": ["autoimmune", "hepatitis", "biliary", "cholangitis", "psc", "pbc", "histology", "mrcp", "cholangiogram"],
        "max": 14,
    },
    {
        "topic": "masld_mash",
        "topics": "masld_mash;pathology;imaging",
        "meaning_ko": "MASLD/MASH의 지방증, ballooning, 섬유화, 초음파 소견, 식습관·운동 개념을 보여주는 open-license figure",
        "keywords": [
            "hepatic steatosis ultrasound",
            "fatty liver ultrasound",
            "steatohepatitis histology ballooning hepatocyte",
            "fatty liver histology steatosis",
            "MASH fibrosis histology",
            "FibroScan liver elastography",
            "Mediterranean diet plate vegetables olive oil",
            "지방간 초음파",
            "지방간 조직 소견",
            "脂肪肝 超音波",
            "脂肪肝 组织学",
            "hígado graso ecografía",
            "foie gras échographie",
            "Fettleber Ultraschall",
            "жировая болезнь печени ультразвук",
        ],
        "commons_categories": [
            "Category:Ultrasound images of fatty liver",
            "Category:Fatty liver",
        ],
        "pmc_terms": [
            "MASH histology ballooning hepatocyte figure",
            "metabolic dysfunction-associated steatotic liver disease histology figure",
            "liver steatosis ultrasound figure",
        ],
        "caption_terms": ["steatosis", "steatohepatitis", "mash", "nash", "ballooning", "fibrosis", "ultrasound", "elastography"],
        "max": 18,
    },
    {
        "topic": "cirrhosis_portal_htn",
        "topics": "cirrhosis_portal_htn;imaging;anatomy_intervention",
        "meaning_ko": "간경변, 문맥고혈압, 복수, 정맥류, TIPS, 간성뇌증의 임상·영상·시술 개념을 보여주는 open-license figure",
        "keywords": [
            "esophageal varices endoscopy banding",
            "gastric varices endoscopy",
            "ascites ultrasound paracentesis",
            "TIPS procedure portal hypertension",
            "portal hypertension collateral circulation",
            "hepatic encephalopathy ammonia",
            "간경변 복수 초음파",
            "식도정맥류 내시경 결찰",
            "門脈圧亢進症 食道静脈瘤",
            "腹水 超音波",
            "门静脉高压 食管静脉曲张",
            "ascitis ecografía paracentesis",
            "hypertension portale varices oesophagiennes",
            "портальная гипертензия варикоз",
        ],
        "commons_categories": [
            "Category:Ultrasound images of cirrhosis",
            "Category:Ultrasound images of livers",
            "Category:Esophageal varices",
            "Category:Endoscopic images of esophageal varices",
            "Category:CT images of esophageal varices",
            "Category:Ascites",
            "Category:Ultrasound images of ascites",
            "Category:Transjugular intrahepatic portosystemic shunt",
        ],
        "pmc_terms": [
            "portal hypertension varices endoscopy figure open access",
            "TIPS portal hypertension figure",
            "ascites paracentesis ultrasound figure",
        ],
        "caption_terms": ["varices", "portal", "hypertension", "ascites", "paracentesis", "tips", "cirrhosis", "encephalopathy"],
        "max": 14,
    },
    {
        "topic": "imaging",
        "topics": "imaging;anatomy_intervention;pathology",
        "meaning_ko": "간 초음파, CT/MRI, 혈관종·낭종·FNH·간선종, 간생검/해부 구조를 설명하는 open-license figure",
        "keywords": [
            "hepatic hemangioma ultrasound",
            "liver hemangioma CT MRI",
            "focal nodular hyperplasia MRI liver",
            "hepatic adenoma MRI",
            "liver cyst ultrasound",
            "liver biopsy histology",
            "liver anatomy portal vein hepatic artery",
            "간 혈관종 초음파",
            "간 낭종 초음파",
            "肝血管腫 超音波",
            "肝囊肿 超声",
            "hemangioma hepático ecografía",
            "hémangiome hépatique échographie",
            "Leberhämangiom Ultraschall",
        ],
        "commons_categories": [
            "Category:Ultrasound images of hepatic hemangioma",
            "Category:Ultrasound images of liver cysts",
            "Category:Ultrasound images of normal livers",
            "Category:Ultrasound images of livers",
        ],
        "pmc_terms": [
            "hepatic hemangioma ultrasound figure",
            "focal nodular hyperplasia MRI figure",
            "hepatic adenoma MRI figure",
        ],
        "caption_terms": ["hemangioma", "fnh", "adenoma", "cyst", "ultrasound", "mri", "ct", "biopsy", "liver"],
        "max": 16,
    },
    {
        "topic": "viral_hepatitis",
        "topics": "viral_hepatitis;pathology",
        "meaning_ko": "HBV/HCV/HDV의 바이러스 구조, life cycle, serology, 치료·예방 개념을 보여주는 open-license figure",
        "keywords": [
            "hepatitis B virus life cycle",
            "HBV replication cccDNA figure",
            "hepatitis C virus life cycle",
            "HCV replication cycle",
            "hepatitis D virus",
            "B형간염 생활사",
            "C형간염 생활사",
            "B型肝炎ウイルス ライフサイクル",
            "乙型肝炎病毒 生命周期",
            "virus de la hepatitis B ciclo de vida",
            "Virus de l'hépatite C cycle de vie",
        ],
        "commons_categories": [
            "Category:Hepatitis B virus",
            "Category:Hepatitis C virus",
        ],
        "pmc_terms": [
            "hepatitis B virus life cycle figure",
            "hepatitis C virus replication cycle figure",
        ],
        "caption_terms": ["hepatitis", "hbv", "hcv", "hdv", "virus", "replication", "life cycle", "cccDNA", "serology"],
        "max": 8,
    },
    {
        "topic": "hcc",
        "topics": "hcc;imaging;pathology",
        "meaning_ko": "간세포암의 CT/MRI, 동맥기 조영증강·washout, 병기와 치료 결과를 설명하는 open-license figure",
        "keywords": [
            "hepatocellular carcinoma CT arterial phase washout",
            "hepatocellular carcinoma MRI washout",
            "hepatocellular carcinoma histology",
            "BCLC staging hepatocellular carcinoma",
            "atezolizumab bevacizumab survival curve hepatocellular carcinoma",
            "간세포암 CT 동맥기 washout",
            "肝細胞癌 CT 動脈相 washout",
            "肝细胞癌 CT 动脉期 washout",
            "carcinome hépatocellulaire scanner phase artérielle",
            "carcinoma hepatocelular TC fase arterial",
        ],
        "commons_categories": [
            "Category:Hepatocellular carcinoma",
            "Category:CT images of hepatocellular carcinoma",
            "Category:Ultrasound images of hepatocellular carcinoma",
            "Category:Histopathology of hepatocellular carcinoma",
            "Category:Gross pathology of hepatocellular carcinoma",
            "Category:MRI of hepatocellular carcinoma",
        ],
        "pmc_terms": [
            "hepatocellular carcinoma arterial phase washout figure",
            "atezolizumab bevacizumab hepatocellular carcinoma survival curve figure",
            "BCLC staging hepatocellular carcinoma figure",
        ],
        "caption_terms": ["hepatocellular", "carcinoma", "hcc", "washout", "arterial", "bclc", "survival", "atezolizumab", "bevacizumab"],
        "max": 10,
    },
]


def req_bytes(url: str, delay: float, timeout: int = 25) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read()
    if delay:
        time.sleep(delay)
    return data


def req_json(url: str, delay: float) -> dict:
    return json.loads(req_bytes(url, delay).decode("utf-8"))


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def slug(value: str) -> str:
    value = re.sub(r"^File:", "", value, flags=re.I)
    value = re.sub(r"\.[A-Za-z0-9]{2,5}$", "", value)
    value = re.sub(r"[^A-Za-z0-9가-힣一-龥ぁ-ゟ゠-ヿ]+", "-", value).strip("-").lower()
    return value[:80] or "figure"


def license_ok(text: str) -> bool:
    low = re.sub(r"\s+", " ", (text or "").lower())
    if any(part in low for part in DISALLOWED_LICENSE_PARTS):
        return False
    return any(part in low for part in ALLOWED_LICENSE_PARTS)


def title_ok(text: str) -> bool:
    low = text.lower()
    return not any(term in low for term in TITLE_EXCLUDE)


def manifest_rows() -> list[dict[str, str]]:
    with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def existing_hashes(rows: list[dict[str, str]]) -> set[str]:
    hashes: set[str] = set()
    for row in rows:
        path = ROOT / row.get("local_path", "")
        if path.exists() and path.is_file():
            try:
                hashes.add(hashlib.sha1(path.read_bytes()).hexdigest())
            except OSError:
                pass
    return hashes


def candidate_title_key(title: str) -> str:
    title = re.sub(r"^File:", "", clean_text(title), flags=re.I).lower()
    title = re.sub(r"\.(jpg|jpeg|png|svg|gif|webp|tif|tiff)$", "", title)
    return re.sub(r"[^a-z0-9가-힣一-龥ぁ-ゟ゠-ヿ]+", "-", title).strip("-")


def source_title_key(row: dict[str, str]) -> str:
    excerpt = row.get("context_excerpt", "")
    title = excerpt.split("|", 1)[0].strip()
    return candidate_title_key(title)


def existing_source_keys(rows: list[dict[str, str]]) -> set[str]:
    keys: set[str] = set()
    for row in rows:
        if "open-license" not in row.get("source_file", ""):
            continue
        key = source_title_key(row)
        if key:
            keys.add(key)
    return keys


def dedupe_open_license_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    kept: list[dict[str, str]] = []
    removed: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        if "open-license" not in row.get("source_file", ""):
            kept.append(row)
            continue
        key = source_title_key(row)
        if key and key in seen:
            removed.append(row)
            continue
        if key:
            seen.add(key)
        kept.append(row)
    return kept, removed


def remove_invalid_open_license_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    kept: list[dict[str, str]] = []
    removed: list[dict[str, str]] = []
    for row in rows:
        if "open-license" not in row.get("source_file", ""):
            kept.append(row)
            continue
        title = row.get("context_excerpt", "").split("|", 1)[0]
        if not title_ok(title):
            removed.append(row)
            continue
        kept.append(row)
    return kept, removed


def quarantine_row_files(rows: list[dict[str, str]]) -> None:
    rejected = AUDIT_DIR / "rejected-duplicates"
    rejected.mkdir(parents=True, exist_ok=True)
    for row in rows:
        src = ROOT / row.get("local_path", "")
        if src.exists() and src.is_file():
            dst = rejected / src.name
            if dst.exists():
                dst = rejected / f"{src.stem}-{row.get('image_id', 'dup')}{src.suffix}"
            shutil.move(str(src), str(dst))
        asset = ASSETS_DB / src.parent.name / src.name
        if asset.exists() and asset.is_file():
            asset.unlink()


def next_image_number(rows: list[dict[str, str]]) -> int:
    nums = []
    for row in rows:
        m = re.search(r"img_(\d+)", row.get("image_id", ""))
        if m:
            nums.append(int(m.group(1)))
    return max(nums or [0]) + 1


def commons_search(query: str, delay: float, limit: int = 25) -> list[dict]:
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
    url = f"{COMMONS_API}?{urllib.parse.urlencode(params)}"
    payload = req_json(url, delay)
    pages = payload.get("query", {}).get("pages", {})
    return sorted(pages.values(), key=lambda p: p.get("index", 999))


def commons_category_files(category: str, delay: float, limit: int = 35) -> list[dict]:
    params = {
        "action": "query",
        "format": "json",
        "list": "categorymembers",
        "cmtitle": category,
        "cmnamespace": "6",
        "cmlimit": str(limit),
        "origin": "*",
    }
    url = f"{COMMONS_API}?{urllib.parse.urlencode(params)}"
    payload = req_json(url, delay)
    titles = [p["title"] for p in payload.get("query", {}).get("categorymembers", []) if p.get("title")]
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
    url = f"{COMMONS_API}?{urllib.parse.urlencode(params)}"
    payload = req_json(url, delay)
    pages = payload.get("query", {}).get("pages", {})
    return sorted(pages.values(), key=lambda p: p.get("title", ""))


def commons_candidates(config: dict, delay: float) -> list[Candidate]:
    out: list[Candidate] = []
    sources: list[tuple[str, list[dict]]] = []
    for category in config["commons_categories"]:
        try:
            sources.append((category, commons_category_files(category, delay)))
        except Exception:
            continue
    for query in config["keywords"]:
        try:
            sources.append((query, commons_search(query, delay)))
        except Exception:
            continue
    seen_titles: set[str] = set()
    for query, pages in sources:
        for page in pages:
            title = page.get("title", "")
            if not title or title in seen_titles or not title_ok(title):
                continue
            seen_titles.add(title)
            info = (page.get("imageinfo") or [{}])[0]
            mime = info.get("mime", "")
            if mime not in {"image/jpeg", "image/png", "image/webp", "image/svg+xml"}:
                continue
            meta = info.get("extmetadata", {})
            license_text = clean_text(meta.get("LicenseShortName", {}).get("value", ""))
            usage_terms = clean_text(meta.get("UsageTerms", {}).get("value", ""))
            license_combined = " ".join(x for x in [license_text, usage_terms] if x)
            if not license_ok(license_combined):
                continue
            description = clean_text(meta.get("ImageDescription", {}).get("value", ""))
            image_url = info.get("thumburl") or info.get("url", "")
            if not image_url:
                continue
            out.append(
                Candidate(
                    source="wikimedia_commons",
                    topic=config["topic"],
                    topics=config["topics"],
                    keywords=";".join(config["keywords"][:8]),
                    meaning_ko=config["meaning_ko"],
                    title=title,
                    caption=description or title,
                    image_url=image_url,
                    source_url=info.get("descriptionurl", ""),
                    license_text=license_combined,
                    author=clean_text(meta.get("Artist", {}).get("value", "")),
                    credit=clean_text(meta.get("Credit", {}).get("value", "")),
                    query=query,
                )
            )
    return out


def pmc_esearch(term: str, delay: float, retmax: int) -> list[str]:
    params = {
        "db": "pmc",
        "term": f"({term}) AND open access[filter]",
        "retmax": str(retmax),
        "retmode": "json",
        "sort": "relevance",
    }
    url = f"{EUTILS_SEARCH}?{urllib.parse.urlencode(params)}"
    payload = req_json(url, delay)
    return payload.get("esearchresult", {}).get("idlist", [])


def xml_text(elem: ET.Element | None) -> str:
    if elem is None:
        return ""
    return clean_text(" ".join(elem.itertext()))


def pmc_license_ok(root: ET.Element) -> tuple[bool, str]:
    chunks: list[str] = []
    for lic in root.findall(".//license"):
        chunks.append(lic.attrib.get("{http://www.w3.org/1999/xlink}href", ""))
        chunks.append(lic.attrib.get("license-type", ""))
        chunks.append(xml_text(lic))
    text = " ".join(chunks)
    return license_ok(text), clean_text(text)


def pmc_article_candidates(config: dict, pmc_id: str, delay: float) -> list[Candidate]:
    params = {"db": "pmc", "id": pmc_id, "retmode": "xml"}
    url = f"{EUTILS_FETCH}?{urllib.parse.urlencode(params)}"
    try:
        xml = req_bytes(url, delay, timeout=35)
        root = ET.fromstring(xml)
    except Exception:
        return []
    ok, license_text = pmc_license_ok(root)
    if not ok:
        return []
    pmcid_num = xml_text(root.find(".//article-id[@pub-id-type='pmc']")) or pmc_id
    pmcid = f"PMC{pmcid_num}" if not str(pmcid_num).startswith("PMC") else str(pmcid_num)
    article_title = xml_text(root.find(".//article-title"))
    doi = xml_text(root.find(".//article-id[@pub-id-type='doi']"))
    caption_terms = [t.lower() for t in config["caption_terms"]]
    out: list[Candidate] = []
    for fig in root.findall(".//fig"):
        caption = xml_text(fig.find("caption"))
        label = xml_text(fig.find("label"))
        sig = f"{label} {caption}".lower()
        if not any(t in sig for t in caption_terms):
            continue
        graphics = fig.findall(".//graphic")
        for graphic in graphics[:2]:
            href = graphic.attrib.get("{http://www.w3.org/1999/xlink}href", "")
            if not href:
                continue
            urls = []
            base = PMC_ARTICLE.format(pmcid=pmcid)
            for ext in ["", ".jpg", ".jpeg", ".png", ".gif", ".tif"]:
                urls.append(f"{base}bin/{href}{ext}")
            out.append(
                Candidate(
                    source="pmc_open_access",
                    topic=config["topic"],
                    topics=config["topics"],
                    keywords=";".join(config["keywords"][:8]),
                    meaning_ko=config["meaning_ko"],
                    title=f"{pmcid} {label} {article_title}",
                    caption=caption[:1500],
                    image_url="|".join(urls),
                    source_url=base,
                    license_text=license_text,
                    author="PMC Open Access article authors",
                    credit=article_title,
                    query=doi or pmcid,
                )
            )
    return out


def pmc_candidates(config: dict, delay: float, article_limit: int) -> list[Candidate]:
    out: list[Candidate] = []
    seen: set[str] = set()
    for term in config["pmc_terms"]:
        try:
            ids = pmc_esearch(term, delay, article_limit)
        except Exception:
            continue
        for pmc_id in ids:
            if pmc_id in seen:
                continue
            seen.add(pmc_id)
            out.extend(pmc_article_candidates(config, pmc_id, delay))
    return out


def download_candidate(candidate: Candidate, delay: float) -> bytes | None:
    urls = candidate.image_url.split("|")
    for url in urls:
        if not url:
            continue
        try:
            return req_bytes(url, delay, timeout=18)
        except Exception:
            continue
    return None


def image_stats(data: bytes) -> tuple[Image.Image | None, int]:
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
    except Exception:
        return None, -100
    width, height = im.size
    area = width * height
    if width < 300 or height < 200 or area < 80_000:
        return im, -100
    rgb = im.convert("RGB")
    small = rgb.resize((96, 96), Image.Resampling.LANCZOS).convert("L")
    entropy = small.entropy()
    edge = ImageStat.Stat(small.filter(ImageFilter.FIND_EDGES)).mean[0]
    score = 50
    if area >= 1_000_000:
        score += 24
    elif area >= 350_000:
        score += 15
    else:
        score += 5
    ratio = max(width / max(height, 1), height / max(width, 1))
    if ratio > 4.6:
        score -= 25
    if entropy >= 5:
        score += 15
    elif entropy < 2.4:
        score -= 20
    if edge >= 20:
        score += 8
    return im, score


def save_image(im: Image.Image, dest_base: Path) -> Path:
    if im.mode in {"RGBA", "LA"}:
        dest = dest_base.with_suffix(".png")
        im.save(dest)
        return dest
    dest = dest_base.with_suffix(".jpg")
    rgb = ImageOps.exif_transpose(im.convert("RGB"))
    rgb.save(dest, "JPEG", quality=92, optimize=True)
    return dest


def add_row(rows: list[dict[str, str]], row: dict[str, str]) -> None:
    rows.append({field: row.get(field, "") for field in MANIFEST_FIELDS})


def write_manifest(rows: list[dict[str, str]]) -> None:
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def copy_to_assets(local_path: str) -> None:
    src = ROOT / local_path
    if not src.exists():
        return
    topic = src.parent.name
    dst_dir = ASSETS_DB / topic
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_dir / src.name)


def make_contact_sheet(rows: list[dict[str, str]], out: Path) -> None:
    font = ImageFont.truetype(str(FONT), 13) if FONT.exists() else ImageFont.load_default()
    font_b = ImageFont.truetype(str(FONT_BOLD), 13) if FONT_BOLD.exists() else font
    items = []
    for row in rows:
        path = ROOT / row["local_path"]
        try:
            im = Image.open(path).convert("RGB")
            im.thumbnail((220, 145), Image.Resampling.LANCZOS)
            items.append((row, im.copy()))
        except Exception:
            continue
    if not items:
        return
    cols = 5
    cell_w, cell_h = 250, 205
    sheet = Image.new("RGB", (cols * cell_w, math.ceil(len(items) / cols) * cell_h), (246, 248, 247))
    d = ImageDraw.Draw(sheet)
    for i, (row, im) in enumerate(items):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h
        sheet.paste(im, (x + (cell_w - im.width) // 2, y + 8))
        d.text((x + 10, y + 158), row["image_id"], font=font_b, fill=(20, 34, 40))
        d.text((x + 10, y + 176), row["topics"][:36], font=font, fill=(72, 84, 91))
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, "JPEG", quality=88)


def audit_current(rows: list[dict[str, str]]) -> dict:
    all_topics = Counter()
    primary = Counter()
    for row in rows:
        ts = [t.strip() for t in row.get("topics", "").split(";") if t.strip()]
        for t in ts:
            all_topics[t] += 1
        if ts:
            primary[ts[0]] += 1
    assets = {}
    for d in sorted(ASSETS_DB.glob("*")):
        if d.is_dir():
            assets[d.name] = len(list(d.glob("*.*")))
    return {"manifest_rows": len(rows), "topics_all": dict(all_topics), "topics_primary": dict(primary), "assets_db_files": assets}


def keyword_plan() -> dict:
    return {
        cfg["topic"]: {
            "priority_reason": cfg["meaning_ko"],
            "languages": {
                "en": [q for q in cfg["keywords"] if re.search(r"[A-Za-z]", q)][:6],
                "ko_ja_zh_es_fr_de_ru": [q for q in cfg["keywords"] if not q.isascii() or any(x in q for x in ["hígado", "foie", "Leber", "порт"])],
            },
            "commons_categories": cfg["commons_categories"],
            "pmc_terms": cfg["pmc_terms"],
        }
        for cfg in TOPICS
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Augment drshin.kr hepatology figure DB with open-license web images.")
    parser.add_argument("--target", type=int, default=50)
    parser.add_argument("--delay", type=float, default=0.35)
    parser.add_argument("--copy-assets", action="store_true")
    parser.add_argument("--pmc-article-limit", type=int, default=3)
    parser.add_argument("--skip-pmc", action="store_true")
    args = parser.parse_args()

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    rows = manifest_rows()
    start_audit = audit_current(rows)
    hashes = existing_hashes(rows)
    source_keys = existing_source_keys(rows)
    next_num = next_image_number(rows)
    new_rows: list[dict[str, str]] = []
    per_topic = Counter()

    (AUDIT_DIR / "open_license_keyword_plan.json").write_text(
        json.dumps(keyword_plan(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if args.target > 0:
        for config in TOPICS:
            topic = config["topic"]
            candidates = commons_candidates(config, args.delay)
            if not args.skip_pmc:
                candidates.extend(pmc_candidates(config, args.delay, args.pmc_article_limit))
            print(f"{topic}: candidates {len(candidates)}", flush=True)
            for candidate in candidates:
                if len(new_rows) >= args.target or per_topic[topic] >= config["max"]:
                    break
                data = download_candidate(candidate, args.delay)
                if not data:
                    continue
                title_key = candidate_title_key(candidate.title)
                if title_key and title_key in source_keys:
                    continue
                sha1 = hashlib.sha1(data).hexdigest()
                if sha1 in hashes:
                    continue
                im, score = image_stats(data)
                if im is None or score < 45:
                    continue
                image_id = f"img_{next_num:05d}"
                next_num += 1
                dest_base = PRIVATE_DB / topic / image_id
                dest_base.parent.mkdir(parents=True, exist_ok=True)
                dest = save_image(im, dest_base)
                local_path = dest.relative_to(ROOT).as_posix()
                source_file = (
                    f"open-license|source={candidate.source}|license={candidate.license_text}|"
                    f"url={candidate.source_url}|author={candidate.author}|credit={candidate.credit}"
                )
                context_excerpt = f"{candidate.title} | {candidate.caption[:1000]} | query={candidate.query}"
                row = {
                    "image_id": image_id,
                    "topics": candidate.topics,
                    "keywords": candidate.keywords,
                    "meaning_ko": candidate.meaning_ko,
                    "local_path": local_path,
                    "value_score": str(score),
                    "source_file": source_file,
                    "context_excerpt": context_excerpt,
                }
                add_row(rows, row)
                add_row(new_rows, row)
                hashes.add(sha1)
                per_topic[topic] += 1
                if args.copy_assets:
                    copy_to_assets(local_path)
                if title_key:
                    source_keys.add(title_key)
            if len(new_rows) >= args.target:
                break

    rows, removed_dupes = dedupe_open_license_rows(rows)
    rows, removed_invalid = remove_invalid_open_license_rows(rows)
    quarantine_row_files(removed_dupes + removed_invalid)
    write_manifest(rows)
    today = date.today().isoformat()
    new_csv = AUDIT_DIR / f"new-open-license-{today}.csv"
    with new_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(new_rows)
    contact = AUDIT_DIR / f"contact-sheet-open-license-{today}.jpg"
    make_contact_sheet(new_rows, contact)
    all_open = [row for row in rows if "open-license" in row.get("source_file", "")]
    all_csv = AUDIT_DIR / "all-open-license-current.csv"
    with all_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(all_open)
    all_contact = AUDIT_DIR / "contact-sheet-open-license-current.jpg"
    make_contact_sheet(all_open, all_contact)
    summary = {
        "date": today,
        "added": len(new_rows),
        "added_by_primary_topic": dict(per_topic),
        "removed_duplicate_open_license_rows": len(removed_dupes),
        "removed_invalid_open_license_rows": len(removed_invalid),
        "before": start_audit,
        "after": audit_current(rows),
        "new_manifest": str(new_csv),
        "contact_sheet": str(contact),
        "all_open_license_rows": len(all_open),
        "all_open_license_manifest": str(all_csv),
        "all_open_license_contact_sheet": str(all_contact),
        "keyword_plan": str(AUDIT_DIR / "open_license_keyword_plan.json"),
    }
    (AUDIT_DIR / f"summary-open-license-{today}.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
