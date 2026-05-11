#!/usr/bin/env python3
"""Rewrite paths in private-figures/db/manifest.csv to match new structure."""
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'private-figures' / 'manifest.csv'

text = SRC.read_text(encoding='utf-8-sig')
lines = text.splitlines()
out_lines = [lines[0]]
n = 0

OLD_PREFIX = 'drshin.kr/private-figures/hepatology-image-database/all-images/'
NEW_PREFIX = 'private-figures/db/'

for line in lines[1:]:
    if not line.strip():
        out_lines.append(line)
        continue
    row = next(csv.reader(io.StringIO(line)))
    if len(row) < 9:
        out_lines.append(line)
        continue
    old_local = row[7]
    if OLD_PREFIX in old_local:
        new_local = old_local.replace(OLD_PREFIX, NEW_PREFIX)
        new_local = new_local.replace('\\', '/')
        row[7] = new_local
        n += 1
    row[8] = ''  # drop thumb_path
    buf = io.StringIO()
    csv.writer(buf, quoting=csv.QUOTE_MINIMAL).writerow(row)
    out_lines.append(buf.getvalue().rstrip('\r\n'))

SRC.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
print(f'rewrote {n} rows in {SRC}')

# Verify
rows = list(csv.reader(SRC.open(encoding='utf-8')))
print(f'total rows: {len(rows)-1}')
print(f'sample local_path: {rows[1][7]}')
print(f'sample local_path: {rows[10][7]}')
