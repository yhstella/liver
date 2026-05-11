#!/usr/bin/env python3
"""Slim manifest.csv columns: 18 → 8 essential."""
import csv
import io
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'private-figures' / 'manifest.csv'

# Keep only essential columns
KEEP_COLS = [
    'image_id',
    'topics',
    'keywords',
    'meaning_ko',
    'local_path',
    'value_score',
    'source_file',
    'context_excerpt',
]


def main():
    text = SRC.read_text(encoding='utf-8-sig')
    lines = text.splitlines()
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return
    header = rows[0]
    # Strip BOM from first header if present
    if header[0].startswith('﻿'):
        header[0] = header[0].lstrip('﻿')
    idx_map = {col: header.index(col) for col in KEEP_COLS if col in header}
    print(f'kept columns: {list(idx_map.keys())}')

    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(KEEP_COLS)
    for row in rows[1:]:
        if not row or all(not c for c in row):
            continue
        new_row = []
        for col in KEEP_COLS:
            new_row.append(row[idx_map[col]] if col in idx_map else '')
        writer.writerow(new_row)
    SRC.write_text(out.getvalue(), encoding='utf-8')
    print(f'wrote {SRC} — {len(rows)-1} rows × {len(KEEP_COLS)} cols')
    # size
    print(f'file size: {SRC.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
