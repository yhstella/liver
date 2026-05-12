#!/usr/bin/env python3
"""Generate /updates/feed.xml (Atom) for the Updates section.

Atom feeds help news/Updates content get indexed faster, especially by
Google News, Bing, and AI search engines that prioritize recent items.
"""
from __future__ import annotations
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
UPDATES_DIR = ROOT / 'updates'
OUT = UPDATES_DIR / 'feed.xml'
SITE = 'https://drshin.kr'


def git_modified_iso(path: Path) -> str:
    try:
        out = subprocess.run(
            ['git', 'log', '-1', '--format=%cI', '--', str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return ts.isoformat()


def html_escape(s: str) -> str:
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;').replace("'", '&apos;'))


def extract_meta(p: Path) -> dict:
    text = p.read_text(encoding='utf-8', errors='ignore')
    title_m = re.search(r'<title>([^<]+)</title>', text)
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', text)
    h1_m = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    return {
        'title': (title_m.group(1).split(' — ')[0] if title_m else (h1_m.group(1) if h1_m else p.parent.name)),
        'description': desc_m.group(1) if desc_m else '',
    }


def main():
    entries = []
    for sub in sorted(UPDATES_DIR.iterdir()):
        if not sub.is_dir():
            continue
        idx = sub / 'index.html'
        if not idx.exists():
            continue
        meta = extract_meta(idx)
        slug = sub.name
        url = f"{SITE}/updates/{quote(slug, safe='-/.')}/"
        updated = git_modified_iso(idx)
        entries.append({
            'slug': slug,
            'url': url,
            'title': meta['title'],
            'summary': meta['description'],
            'updated': updated,
        })
    # sort newest first by updated date
    entries.sort(key=lambda e: e['updated'], reverse=True)
    # take latest 50
    entries = entries[:50]

    now = datetime.now(timezone.utc).isoformat()
    feed = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="ko">',
            f'  <title>Hepatology Note — 최신 지견</title>',
            f'  <link href="{SITE}/updates/" rel="alternate" type="text/html"/>',
            f'  <link href="{SITE}/updates/feed.xml" rel="self" type="application/atom+xml"/>',
            f'  <id>{SITE}/updates/</id>',
            f'  <updated>{now}</updated>',
            f'  <subtitle>주요 저널의 hepatology 최신 논문 요약 — 신현재(서울대학교병원 소화기내과·간암센터)</subtitle>',
            f'  <author><name>신현재</name><uri>{SITE}/소개/</uri></author>',
            f'  <generator>build_updates_rss.py</generator>',
            f'  <icon>{SITE}/favicon.png</icon>',
            ]
    for e in entries:
        feed.extend([
            '  <entry>',
            f'    <title>{html_escape(e["title"])}</title>',
            f'    <link href="{e["url"]}" rel="alternate" type="text/html"/>',
            f'    <id>{e["url"]}</id>',
            f'    <updated>{e["updated"]}</updated>',
            f'    <summary>{html_escape(e["summary"])}</summary>',
            f'    <author><name>신현재</name></author>',
            '  </entry>',
        ])
    feed.append('</feed>')
    OUT.write_text('\n'.join(feed) + '\n', encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)} — {len(entries)} entries')


if __name__ == '__main__':
    main()
