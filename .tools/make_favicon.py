#!/usr/bin/env python3
"""
make_favicon.py — Generate favicon set for drshin.kr.

Design: brand green (#1f6f5c) 배경 + simplified liver silhouette (white).
정면에서 본 단순화된 간 실루엣 (우엽 큰 lobe + 좌엽 작은 lobe + falciform notch).
같은 path를 inline SVG로도 노출 (`brand-mark-liver.svg`) — 메인 페이지에서 재사용.

생성 파일:
  - favicon.ico       (16x16 + 32x32 + 48x48 multi-size)
  - favicon-16.png
  - favicon-32.png
  - favicon-192.png   (Android)
  - favicon-512.png   (Android splash)
  - apple-touch-icon.png  (180x180, iOS)
  - site.webmanifest
  - assets/img/brand/liver-mark.svg   (inline SVG, currentColor)
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BRAND_GREEN = (31, 111, 92)   # #1f6f5c — kept for theme-color/manifest
LIVER_RED   = (166, 74, 58)   # #a64a3a — anatomical warm red-brown
LIVER_DEEP  = (130, 54, 42)   # #82362a — subtle darker shade for left-lobe accent
TILE_CREAM  = (250, 246, 238) # #faf6ee — warm cream tile bg
SUPER = 4                      # supersampling factor for smooth edges

# --- Liver silhouette path (quadratic Beziers, normalized 0..100) ---
# 아이콘 스타일 wedge: 좌상단 near-right-angle, 우측으로 tapering tip,
# 위쪽에 작은 falciform V-notch. 좌측 edge는 거의 수직, 상단은 거의 수평.
# Each segment: (start, control, end) — chained head-to-tail.
LIVER_PATH = [
    # 1) 상단 좌측 edge — 거의 수평
    ((6, 18), (28, 17), (52, 18)),
    # 2) Falciform V-notch (좁고 또렷하게)
    ((52, 18), (58, 26), (64, 19)),
    # 3) Notch 우측 → 우엽 어깨로 상승
    ((64, 19), (74, 21), (84, 28)),
    # 4) 우측 어깨 곡선
    ((84, 28), (94, 40), (94, 56)),
    # 5) 우측 tapering tip (좌엽 끝)
    ((94, 56), (90, 70), (76, 78)),
    # 6) 하단 곡선 (우→좌)
    ((76, 78), (44, 84), (22, 78)),
    # 7) 좌하단 둥글게
    ((22, 78), (10, 70), (8, 52)),
    # 8) 좌측 edge — 거의 수직, 상단 복귀
    ((8, 52), (6, 34), (6, 18)),
]


def bezier_quad(p0, p1, p2, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1.0 - t
        x = u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0]
        y = u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def liver_polygon(box: float, scale: float = 0.78, dx: float = 0.0, dy: float = 0.0):
    """Return list of (x,y) points for liver silhouette inside a `box` × `box` square."""
    raw = []
    for p0, p1, p2 in LIVER_PATH:
        seg = bezier_quad(p0, p1, p2, n=64)
        if raw:
            seg = seg[1:]
        raw.extend(seg)
    s = box * scale / 100.0
    ox = box * (1 - scale) / 2.0 + dx
    oy = box * (1 - scale) / 2.0 + dy
    return [(ox + x * s, oy + y * s) for x, y in raw]


def liver_svg_path(scale: float = 1.0, ox: float = 0.0, oy: float = 0.0) -> str:
    """Return SVG path 'd' attribute for the same liver shape (viewBox 0 0 100 100)."""
    parts = []
    first = True
    for p0, p1, p2 in LIVER_PATH:
        if first:
            parts.append(f"M {ox + p0[0]*scale:.2f} {oy + p0[1]*scale:.2f}")
            first = False
        parts.append(f"Q {ox + p1[0]*scale:.2f} {oy + p1[1]*scale:.2f} "
                     f"{ox + p2[0]*scale:.2f} {oy + p2[1]*scale:.2f}")
    parts.append("Z")
    return " ".join(parts)


def make_liver_mark(size: int, rounded: bool = False, scale: float = 0.74) -> Image.Image:
    """Cream tile + warm red liver silhouette. Supersampled then downscaled."""
    big = size * SUPER
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Tile background — warm cream, with a thin brand-green hairline ring for cohesion
    if rounded:
        radius = max(int(big * 0.20), 4)
        draw.rounded_rectangle((0, 0, big - 1, big - 1), radius=radius, fill=TILE_CREAM)
        # subtle brand-green ring (only on rounded/large versions, would be invisible at 16px)
        if size >= 96:
            ring_w = max(int(big * 0.012), 2)
            draw.rounded_rectangle(
                (ring_w // 2, ring_w // 2, big - 1 - ring_w // 2, big - 1 - ring_w // 2),
                radius=radius - ring_w // 2,
                outline=BRAND_GREEN,
                width=ring_w,
            )
    else:
        draw.rectangle((0, 0, big - 1, big - 1), fill=TILE_CREAM)
    poly = liver_polygon(big, scale=scale, dy=big * 0.005)
    draw.polygon(poly, fill=LIVER_RED)
    return img.resize((size, size), Image.LANCZOS)


def write_pngs():
    sizes_round = [(180, "apple-touch-icon.png"), (192, "favicon-192.png"), (512, "favicon-512.png")]
    sizes_square = [(16, "favicon-16.png"), (32, "favicon-32.png")]

    # Tiny sizes need a slightly bigger silhouette for legibility
    for size, name in sizes_round:
        img = make_liver_mark(size, rounded=True, scale=0.68)
        img.save(ROOT / name, optimize=True)
        print(f"  wrote {name} ({size}x{size})")

    for size, name in sizes_square:
        img = make_liver_mark(size, rounded=False, scale=0.74)
        img.save(ROOT / name, optimize=True)
        print(f"  wrote {name} ({size}x{size})")

    # ICO with 16/32/48
    ico_imgs = [
        make_liver_mark(16, rounded=False, scale=0.78),
        make_liver_mark(32, rounded=False, scale=0.74),
        make_liver_mark(48, rounded=False, scale=0.72),
    ]
    ico_imgs[0].save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)],
        append_images=ico_imgs[1:],
    )
    print("  wrote favicon.ico (16/32/48)")


def write_brand_svg():
    """Inline-friendly SVG that uses currentColor — suitable for header/hero marks."""
    out_dir = ROOT / "assets" / "img" / "brand"
    out_dir.mkdir(parents=True, exist_ok=True)
    d = liver_svg_path()
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" '
        'role="img" aria-label="liver">'
        f'<path d="{d}" fill="currentColor"/>'
        '</svg>\n'
    )
    (out_dir / "liver-mark.svg").write_text(svg, encoding="utf-8")
    print("  wrote assets/img/brand/liver-mark.svg")


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
    (ROOT / "site.webmanifest").write_text(WEBMANIFEST, encoding="utf-8")
    print("  wrote site.webmanifest")


if __name__ == "__main__":
    write_pngs()
    write_manifest()
    write_brand_svg()
    # Remove placeholder favicon.png if present
    old = ROOT / "favicon.png"
    if old.exists():
        old.unlink()
        print("  removed legacy favicon.png")
