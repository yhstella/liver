#!/usr/bin/env python3
"""Slim assets/img/concepts/ to only files referenced in HTML."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONCEPTS = ROOT / 'assets' / 'img' / 'concepts'

# Collect all referenced paths
used = set()
for p in ROOT.rglob('*.html'):
    if any(part.startswith('.') for part in p.relative_to(ROOT).parts):
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'assets/img/concepts/[^"\')\s]+', text):
        used.add(m.group(0))
print(f'used: {len(used)} paths')

# Delete unused files
deleted = 0
kept = 0
for f in CONCEPTS.rglob('*'):
    if not f.is_file():
        continue
    rel = str(f.relative_to(ROOT)).replace('\\', '/')
    if rel in used:
        kept += 1
    else:
        f.unlink()
        deleted += 1
print(f'kept: {kept}, deleted: {deleted}')

# Remove empty subdirs
for d in sorted(CONCEPTS.rglob('*'), key=lambda p: -len(p.parts)):
    if d.is_dir() and not any(d.iterdir()):
        d.rmdir()
        print(f'  removed empty dir: {d.relative_to(ROOT)}')
