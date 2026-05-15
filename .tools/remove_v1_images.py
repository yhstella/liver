#!/usr/bin/env python3
"""Remove v1 image references from all HTML pages.

Strategy:
- Find any page-image:auto:start / page-image-lower:auto:start block whose src
  points to /assets/img/page-generated/ (v1).
- Remove the entire <!-- ... :start --> ... <!-- ... :end --> block.
- Keep blocks where src points to /assets/img/page-generated-v2/ (v2 high quality).
"""
import pathlib, re, sys, io, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = pathlib.Path(__file__).resolve().parent.parent


V1_PREFIX = '/assets/img/page-generated/'

TOP_BLOCK_RE = re.compile(
    r'\n?<!-- page-image:auto:start -->.*?<!-- page-image:auto:end -->',
    re.DOTALL,
)
LOWER_BLOCK_RE = re.compile(
    r'\n?<!-- page-image-lower:auto:start -->.*?<!-- page-image-lower:auto:end -->\n?',
    re.DOTALL,
)


def cleanup(path: pathlib.Path):
    text = path.read_text(encoding='utf-8')
    original = text

    # For each block, decide whether to remove
    def maybe_remove_top(m):
        block = m.group(0)
        # Only remove if it references v1
        if V1_PREFIX in block and '/page-generated-v2/' not in block:
            return ''  # remove entirely
        return block

    def maybe_remove_lower(m):
        block = m.group(0)
        if V1_PREFIX in block and '/page-generated-v2/' not in block:
            return ''
        return block

    text = TOP_BLOCK_RE.sub(maybe_remove_top, text)
    text = LOWER_BLOCK_RE.sub(maybe_remove_lower, text)

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


# Find all HTML files that mention page-image:auto
result = subprocess.run(
    ['git', 'grep', '-l', '-z', 'page-image:auto:start', 'HEAD'],
    capture_output=True, cwd=ROOT,
)
files = []
for entry in result.stdout.split(b'\x00'):
    if not entry:
        continue
    s = entry.decode('utf-8')
    # git grep with rev returns "HEAD:path", strip
    if s.startswith('HEAD:'):
        s = s[5:]
    files.append(s)

print(f'Files with image markup: {len(files)}')
changed = 0
for f in files:
    p = ROOT / f
    if not p.exists():
        continue
    if cleanup(p):
        changed += 1

print(f'Changed: {changed}')
