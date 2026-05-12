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
ACCENT = (31, 111, 92)        # #1f6f5c brand green
WHITE = (255, 255, 255)
SUPER = 4                      # supersampling factor for smooth edges

# --- Liver silhouette path (quadratic Beziers, normalized 0..100) ---
# 정면(anterior) 시점 — 화면 좌측이 환자의 우엽(큰 lobe, ~70% 폭), 우측이 좌엽(작은 lobe).
# 위쪽 능선: 큰 봉우리 → V notch (falciform) → 작은 봉우리 → 우측면.
# Each segment: (start, control, end) — chained head-to-tail.
LIVER_PATH = [
    # 1) 좌측 끝(우엽 외측 뾰족한 점) → 위로 큰 곡선 → 우엽 정상
    ((4, 56), (8, 14), (44, 16)),
    # 2) 우엽 정상 → notch 좌측면 (서서히 내려옴)
    ((44, 16), (52, 22), (54, 30)),
    # 3) Falciform V-notch (좁고 또렷하게)
    ((54, 30), (58, 40), (62, 30)),
    # 4) notch 우측 → 좌엽 정상 (작은 봉우리)
    ((62, 30), (70, 18), (80, 24)),
    # 5) 좌엽 정상 → 우측 어깨 (더 빨리 떨어짐)
    ((80, 24), (94, 30), (92, 48)),
    # 6) 우측면 → 우하단 (커브 안쪽으로)
    ((92, 48), (86, 68), (68, 78)),
    # 7) 하단 곡선 (우→좌, 살짝 처짐)
    ((68, 78), (38, 86), (14, 74)),
    # 8) 좌하단 → 좌측 끝 복귀
    ((14, 74), (0, 66), (4, 56)),
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


def make_liver_mark(size: int, rounded: bool = False, scale: float = 0.66) -> Image.Image:
    """Render brand-green tile with white liver silhouette, supersampled then downscaled."""
    big = size * SUPER
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if rounded:
        radius = max(int(big * 0.18), 4)
        draw.rounded_rectangle((0, 0, big - 1, big - 1), radius=radius, fill=ACCENT)
    else:
        draw.rectangle((0, 0, big - 1, big - 1), fill=ACCENT)
    poly = liver_polygon(big, scale=scale, dy=big * 0.01)  # slight optical lift
    draw.polygon(poly, fill=WHITE)
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
