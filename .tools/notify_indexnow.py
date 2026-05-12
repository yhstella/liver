#!/usr/bin/env python3
"""
notify_indexnow.py — Notify search engines (Bing, Naver, Yandex, Seznam)
of new/updated pages via IndexNow protocol.

사용:
  # 모든 sitemap URL 일괄 통보
  python .tools/notify_indexnow.py --all

  # 특정 슬러그 목록 통보
  python .tools/notify_indexnow.py --slugs 간암-소작술-RFA-MWA C형간염-DAA-실패-재치료

Google은 IndexNow 미지원 — GSC '색인 생성 요청' 수동.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
HOST = 'drshin.kr'
KEY = '0dc68f8425625ecdc6192101e8ab0321'
KEY_LOCATION = f'https://{HOST}/{KEY}.txt'

# Single endpoint propagates to all participating engines (Bing, Yandex, Naver, Seznam)
ENDPOINTS = [
    'https://api.indexnow.org/IndexNow',
    'https://searchadvisor.naver.com/indexnow',  # Naver explicit
]


def all_urls_from_sitemaps() -> list[str]:
    urls = set()
    for sm in ROOT.glob('sitemap*.xml'):
        if sm.name == 'sitemap.xml':
            continue  # index, not URL list
        text = sm.read_text(encoding='utf-8')
        for m in re.finditer(r'<loc>([^<]+)</loc>', text):
            urls.add(m.group(1))
    return sorted(urls)


def slugs_to_urls(slugs: list[str]) -> list[str]:
    return [f'https://{HOST}/{quote(s, safe="-/.")}/' for s in slugs]


def submit(urls: list[str], dry_run: bool = False) -> None:
    if not urls:
        print('no URLs to submit')
        return
    # IndexNow accepts max 10,000 URLs per request
    payload = {
        'host': HOST,
        'key': KEY,
        'keyLocation': KEY_LOCATION,
        'urlList': urls,
    }
    data = json.dumps(payload).encode('utf-8')
    print(f'submitting {len(urls)} URLs to IndexNow…')
    if dry_run:
        print('  (dry-run, not sent)')
        for u in urls[:5]:
            print(f'    {u}')
        if len(urls) > 5:
            print(f'    … + {len(urls) - 5} more')
        return
    for endpoint in ENDPOINTS:
        try:
            req = urllib.request.Request(
                endpoint,
                data=data,
                headers={
                    'Content-Type': 'application/json; charset=utf-8',
                    'Host': endpoint.split('//')[1].split('/')[0],
                },
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f'  ✓ {endpoint} → HTTP {resp.status}')
        except urllib.error.HTTPError as e:
            print(f'  ✗ {endpoint} → HTTP {e.code} {e.reason}')
            try:
                print(f'    body: {e.read().decode()[:200]}')
            except Exception:
                pass
        except Exception as e:
            print(f'  ✗ {endpoint} → {type(e).__name__}: {e}')


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--all', action='store_true', help='submit all URLs from sitemap children')
    g.add_argument('--slugs', nargs='+', help='specific slugs to notify (e.g. 간암-소작술-RFA-MWA)')
    g.add_argument('--urls', nargs='+', help='full URLs to notify')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    if args.all:
        urls = all_urls_from_sitemaps()
    elif args.slugs:
        urls = slugs_to_urls(args.slugs)
    else:
        urls = args.urls

    submit(urls, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
