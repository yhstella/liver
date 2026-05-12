#!/usr/bin/env python3
"""
make_favicon.py — Generate favicon set for drshin.kr.

디자인: brand green (#1f6f5c) 배경 + serif "H" 흰색 letter mark.
"H" = Hepatology / Hospital 양쪽 모두 통하는 monogram.

생성 파일:
  - favicon.ico       (16x16 + 32x32 multi-size)
  - favicon-16.png
  - favicon-32.png
  - favicon-192.png   (Android)
  - favicon-512.png   (Android splash)
  - apple-touch-icon.png  (180x180, iOS)
  - site.webmanifest
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ACCENT = (31, 111, 92)        # #1f6f5c brand green
ACCENT_DEEP = (24, 94, 77)    # subtle border
WHITE = (255, 255, 255)

# Try multiple font paths (Windows)
FONT_CANDIDATES = [
    'C:/Windows/Fonts/timesbd.ttf',
    'C:/Windows/Fonts/times.ttf',
    'C:/Windows/Fonts/georgiab.ttf',
    'C:/Windows/Fonts/georgia.ttf',
]


def find_font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def make_letter_mark(size: int, rounded: bool = False) -> Image.Image:
    """Return a square favicon image of given size with serif 'H' on brand green."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Background: rounded square (for app icons) or full square (for ico)
    if rounded:
        radius = max(int(size * 0.18), 4)
        draw.rounded_rectangle(
            (0, 0, size - 1, size - 1),
            radius=radius,
            fill=ACCENT,
        )
    else:
        draw.rectangle((0, 0, size - 1, size - 1), fill=ACCENT)
    # Letter "H" — large serif, optical centered
    font_size = int(size * 0.7)
    font = find_font(font_size)
    text = "H"
    # measure
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1] - int(size * 0.02)  # slight optical lift
    draw.text((tx, ty), text, font=font, fill=WHITE)
    return img


def write_pngs():
    sizes_round = [(180, 'apple-touch-icon.png'), (192, 'favicon-192.png'), (512, 'favicon-512.png')]
    sizes_square = [(16, 'favicon-16.png'), (32, 'favicon-32.png')]

    for size, name in sizes_round:
        img = make_letter_mark(size, rounded=True)
        img.save(ROOT / name, optimize=True)
        print(f'  wrote {name} ({size}x{size})')

    for size, name in sizes_square:
        img = make_letter_mark(size, rounded=False)
        img.save(ROOT / name, optimize=True)
        print(f'  wrote {name} ({size}x{size})')

    # ICO with both 16 and 32
    ico_imgs = [make_letter_mark(s, rounded=False) for s in (16, 32, 48)]
    ico_imgs[0].save(
        ROOT / 'favicon.ico',
        format='ICO',
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=ico_imgs[1:],
    )
    print(f'  wrote favicon.ico (16/32/48)')


WEBMANIFEST = '''{
  "name": "Hepatology Note",
  "short_name": "Hepatology",
  "description": "신현재(서울대학교병원 소화기내과·간암센터)의 간질환 가이드와 임상 노트",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#fafaf7",
  "theme_color": "#1f6f5c",
  "lang": "ko",
  "icons": [
    {"src": "/favicon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/favicon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
  ]
}
'''


def write_manifest():
    (ROOT / 'site.webmanifest').write_text(WEBMANIFEST, encoding='utf-8')
    print('  wrote site.webmanifest')


if __name__ == '__main__':
    write_pngs()
    write_manifest()
    # Remove placeholder favicon.png if present
    old = ROOT / 'favicon.png'
    if old.exists():
        old.unlink()
        print('  removed legacy favicon.png')
