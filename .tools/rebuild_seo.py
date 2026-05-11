#!/usr/bin/env python3
"""
rebuild_seo.py — Master script: regenerate all auto-injected SEO/GEO assets.

Run this after content changes:
  python .tools/rebuild_seo.py

Order matters: JSON-LD must run BEFORE sitemap (so dates are accurate)
and BEFORE llms.txt (so author/dateModified are picked up).
"""
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("PYTHONIOENCODING", "utf-8")

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / ".tools"

STEPS = [
    ("Inject author-box on detail pages",   "inject_author_box.py"),
    ("Inject JSON-LD on detail pages",      "inject_jsonld.py"),
    ("Dedupe legacy JSON-LD blocks",        "dedupe_jsonld.py"),
    ("Inject verification meta (if any)",   "inject_verification.py"),
    ("Generate sitemap.xml index + children", "build_sitemap.py"),
    ("Generate llms.txt + llms-full.txt",    "build_llms.py"),
]


def main():
    for label, script in STEPS:
        print(f"\n=== {label} ===")
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, str(TOOLS / script)],
            cwd=ROOT, env=env,
        )
        if result.returncode != 0:
            print(f"FAILED: {script}")
            sys.exit(1)
    print("\nAll SEO/GEO assets rebuilt.")


if __name__ == "__main__":
    main()
