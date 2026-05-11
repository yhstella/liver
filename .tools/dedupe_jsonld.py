#!/usr/bin/env python3
"""
dedupe_jsonld.py — Remove legacy hand-written JSON-LD blocks that duplicate
the auto-injected JSON-LD.

Pattern:
- Each affected page has two <script type="application/ld+json">...</script>
  blocks. The legacy one appears BEFORE the <!-- jsonld:auto:start --> marker.
- The auto block (between markers) is a strict superset (MedicalWebPage +
  Article + BreadcrumbList + FAQPage + Person + WebSite).

Fix: remove every <script type="application/ld+json">...</script> that is
NOT enclosed by the auto markers. Pages without an auto block are left alone
(no dedup risk).

Idempotent. Re-runnable.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", ".tools", "assets", "guide", "node_modules"}

SCRIPT_RE = re.compile(
    r'<script\s+type="application/ld\+json">.*?</script>\s*',
    re.DOTALL,
)
AUTO_BLOCK_RE = re.compile(
    r'<!--\s*jsonld:auto:start\s*-->.*?<!--\s*jsonld:auto:end\s*-->',
    re.DOTALL,
)


def dedupe(text: str) -> tuple[str, int]:
    """Return (new_text, n_removed)."""
    auto = AUTO_BLOCK_RE.search(text)
    if not auto:
        return text, 0  # no auto block, leave alone

    auto_start, auto_end = auto.span()

    # Iterate scripts; keep ones inside auto block, drop the rest
    removed = 0
    out_parts: list[str] = []
    cursor = 0
    for m in SCRIPT_RE.finditer(text):
        s, e = m.span()
        inside_auto = auto_start <= s and e <= auto_end
        if inside_auto:
            continue
        # this is a legacy block — remove it
        out_parts.append(text[cursor:s])
        cursor = e
        removed += 1
    if removed == 0:
        return text, 0
    out_parts.append(text[cursor:])
    new_text = "".join(out_parts)
    return new_text, removed


def main() -> None:
    total_pages = 0
    total_blocks = 0
    changed_files: list[str] = []
    for path in ROOT.rglob("index.html"):
        parts = path.relative_to(ROOT).parts
        if any(p in EXCLUDE_DIRS for p in parts):
            continue
        if any(p.startswith(".") for p in parts):
            continue
        text = path.read_text(encoding="utf-8")
        new_text, removed = dedupe(text)
        if removed:
            path.write_text(new_text, encoding="utf-8")
            total_pages += 1
            total_blocks += removed
            changed_files.append(str(path.relative_to(ROOT)))
    print(f"Cleaned {total_pages} pages, removed {total_blocks} legacy JSON-LD blocks.")
    for f in changed_files[:20]:
        print(f"  {f}")
    if len(changed_files) > 20:
        print(f"  ... and {len(changed_files) - 20} more")


if __name__ == "__main__":
    main()
