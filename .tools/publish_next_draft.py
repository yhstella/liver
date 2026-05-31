#!/usr/bin/env python3
"""
publish_next_draft.py — Move the oldest draft in updates/ to published state.

Triggered by the weekly auto-publish routine. Idempotent enough to retry safely.

Behavior:
- Scan updates/<slug>/index.html for pages with BOTH:
  - <meta name="robots" content="noindex,nofollow">
  - <!-- DRAFT ... --> comment
- Pick the OLDEST by git-tracked creation time (mtime fallback).
- In that file:
  - robots → "index,follow,max-image-preview:large"
  - Drop the <!-- DRAFT ... --> comment
  - Update publish-date in HTML + datePublished/dateModified/lastReviewed in JSON-LD
- In updates/index.html: prepend a <li class="published"> entry, pulling
  title from <h1> and a one-line citation from <div class="cite-banner">.
- Exit 0 with stdout JSON {slug, title, publishedAt, queueRemaining}.
- Exit 2 if queue empty (queueRemaining=0, no slug).
- Exit 1 on unexpected error.

Usage:
  python .tools/publish_next_draft.py                # publish next
  python .tools/publish_next_draft.py --dry-run      # report next without writing
  python .tools/publish_next_draft.py --list         # list queue
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPDATES = ROOT / 'updates'
INDEX = UPDATES / 'index.html'
KST = timezone(timedelta(hours=9))

DRAFT_COMMENT_RE = re.compile(r'<!--\s*DRAFT[^>]*-->\s*\n?', re.IGNORECASE)
ROBOTS_NOINDEX_RE = re.compile(
    r'<meta\s+name="robots"\s+content="noindex,nofollow">',
    re.IGNORECASE,
)
ROBOTS_INDEX = '<meta name="robots" content="index,follow,max-image-preview:large">'
H1_RE = re.compile(r'<h1[^>]*>(.+?)</h1>', re.IGNORECASE | re.DOTALL)
CITE_RE = re.compile(
    r'<div\s+class="cite-banner">.*?<strong>[^<]*</strong>\s*(.+?)(?:<a |</div>)',
    re.IGNORECASE | re.DOTALL,
)
PUBLISH_DATE_RE = re.compile(
    r'<p\s+class="publish-date">.*?<time\s+datetime="[^"]*">.*?</time>.*?</p>',
    re.IGNORECASE | re.DOTALL,
)
JSONLD_DATE_KEYS = ('datePublished', 'dateModified', 'lastReviewed')


def is_draft(text: str) -> bool:
    if not ROBOTS_NOINDEX_RE.search(text):
        return False
    if not DRAFT_COMMENT_RE.search(text):
        return False
    return True


def git_first_commit_epoch(path: Path) -> float:
    """Return epoch seconds of the file's first commit, or mtime fallback."""
    try:
        out = subprocess.run(
            ['git', 'log', '--diff-filter=A', '--follow', '--format=%ct', '--', str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
        lines = [l for l in out.stdout.strip().split('\n') if l]
        if lines:
            return float(lines[-1])
    except Exception:
        pass
    return path.stat().st_mtime


def list_queue():
    queue = []
    if not UPDATES.exists():
        return queue
    for sub in UPDATES.iterdir():
        if not sub.is_dir():
            continue
        idx = sub / 'index.html'
        if not idx.exists():
            continue
        try:
            text = idx.read_text(encoding='utf-8')
        except Exception:
            continue
        if is_draft(text):
            queue.append((git_first_commit_epoch(idx), sub.name, idx))
    queue.sort()
    return queue


def extract_title(text: str) -> str:
    m = H1_RE.search(text)
    if not m:
        return ''
    return re.sub(r'<[^>]+>', '', m.group(1)).strip()


def extract_citation(text: str) -> str:
    m = CITE_RE.search(text)
    if not m:
        return ''
    cite = re.sub(r'<[^>]+>', '', m.group(1))
    cite = re.sub(r'\s+', ' ', cite).strip().rstrip('.')
    return cite[:160] + ('…' if len(cite) > 160 else '')


def publish_one(slug: str, idx: Path, now_kst: datetime) -> dict:
    text = idx.read_text(encoding='utf-8')

    # 1. flip robots
    text = ROBOTS_NOINDEX_RE.sub(ROBOTS_INDEX, text, count=1)

    # 2. drop DRAFT comment
    text = DRAFT_COMMENT_RE.sub('', text, count=1)

    # 3. publish-date in HTML
    date_iso = now_kst.strftime('%Y-%m-%d')
    date_kor = f'<span class="y">{now_kst.year}년 </span>{now_kst.month}월 {now_kst.day}일'
    publish_html = (
        f'<p class="publish-date">작성일 <time datetime="{date_iso}">'
        f'{date_kor}</time></p>'
    )
    if PUBLISH_DATE_RE.search(text):
        text = PUBLISH_DATE_RE.sub(publish_html, text, count=1)

    # 4. JSON-LD datePublished/dateModified/lastReviewed
    iso_full = now_kst.strftime('%Y-%m-%dT%H:%M:%S+09:00')
    for key in ('datePublished', 'dateModified'):
        text = re.sub(
            rf'"{key}":"[^"]*"',
            f'"{key}":"{iso_full}"',
            text,
        )
    text = re.sub(
        r'"lastReviewed":"[^"]*"',
        f'"lastReviewed":"{date_iso}"',
        text,
    )

    idx.write_text(text, encoding='utf-8', newline='')

    # 5. updates/index.html: prepend <li class="published">
    title = extract_title(text)
    cite = extract_citation(text)
    li = (
        f'<li class="published"><a href="/updates/{slug}/">'
        f'<span class="num">{now_kst.year}·{now_kst.month}</span>'
        f'<div class="body"><h3>{title}</h3><p>{cite}</p></div>'
        f'<span class="status published">읽기 →</span></a></li>'
    )
    if INDEX.exists():
        idx_text = INDEX.read_text(encoding='utf-8')
        marker = '<ul class="topic-list" style="margin:24px 0 56px">'
        if marker in idx_text:
            idx_text = idx_text.replace(marker, marker + '\n' + li, 1)
            INDEX.write_text(idx_text, encoding='utf-8', newline='')

    return {
        'slug': slug,
        'title': title,
        'publishedAt': iso_full,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()

    queue = list_queue()

    if args.list:
        for epoch, slug, _ in queue:
            d = datetime.fromtimestamp(epoch, tz=KST).strftime('%Y-%m-%d')
            print(f'{d}  {slug}')
        print(f'\nqueueRemaining={len(queue)}')
        return

    if not queue:
        sys.stdout.write(json.dumps({'queueRemaining': 0, 'message': 'queue is empty — agent should draft a new article from scratch'}, ensure_ascii=False))
        sys.stdout.write('\n')
        sys.exit(2)

    _, slug, idx = queue[0]
    now_kst = datetime.now(KST)

    if args.dry_run:
        sys.stdout.write(json.dumps({'wouldPublish': slug, 'queueRemaining': len(queue), 'dryRun': True}, ensure_ascii=False))
        sys.stdout.write('\n')
        return

    info = publish_one(slug, idx, now_kst)
    info['queueRemaining'] = len(queue) - 1
    sys.stdout.write(json.dumps(info, ensure_ascii=False))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
