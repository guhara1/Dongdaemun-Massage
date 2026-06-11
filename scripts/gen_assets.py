#!/usr/bin/env python3
"""간다 GO 브랜드 아이콘·OG 이미지 생성 스크립트 (Pillow 필요).

usage: python3 scripts/gen_assets.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

NAVY = (10, 17, 32)        # #0a1120
GOLD = (200, 162, 94)      # #c8a25e
IVORY = (233, 215, 171)    # #e9d7ab

SERIF = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
SANS = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"


def monogram(size: int) -> Image.Image:
    """골드 링 안의 세리프 G 모노그램."""
    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, s - 1, s - 1], fill=NAVY)
    ring_w = max(scale, int(s * 0.045))
    pad = ring_w // 2 + scale
    d.ellipse([pad, pad, s - 1 - pad, s - 1 - pad], outline=GOLD, width=ring_w)
    inner = int(s * 0.085)
    d.ellipse([inner, inner, s - 1 - inner, s - 1 - inner],
              outline=GOLD + (90,), width=max(scale, int(s * 0.012)))
    font = ImageFont.truetype(SERIF, int(s * 0.52))
    bbox = d.textbbox((0, 0), "G", font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((s - w) / 2 - bbox[0], (s - h) / 2 - bbox[1]), "G", font=font, fill=IVORY)
    return img.resize((size, size), Image.LANCZOS)


def og_image() -> Image.Image:
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    # 미세한 상하 그라데이션
    for y in range(H):
        t = y / H
        c = tuple(int(a + (b - a) * t) for a, b in zip((13, 22, 40), NAVY))
        d.line([(0, y), (W, y)], fill=c)
    # 골드 테두리 프레임
    d.rectangle([28, 28, W - 29, H - 29], outline=GOLD, width=3)
    d.rectangle([40, 40, W - 41, H - 41], outline=GOLD + (0,) if False else (90, 75, 45), width=1)
    # 모노그램
    mark = monogram(150)
    img.paste(mark, (W // 2 - 75, 92), mark)
    # 타이포 (시스템에 한글 폰트가 없어 라틴 브랜딩 사용)
    title = ImageFont.truetype(SERIF, 110)
    sub = ImageFont.truetype(SANS, 34)
    small = ImageFont.truetype(SANS, 30)

    def center(text, font, y, fill):
        bbox = d.textbbox((0, 0), text, font=font)
        d.text(((W - (bbox[2] - bbox[0])) / 2 - bbox[0], y), text, font=font, fill=fill)

    center("GANDA GO", title, 270, IVORY)
    center("DONGDAEMUN  PREMIUM  VISITING  SPA", sub, 415, GOLD)
    # 구분선
    d.line([(W / 2 - 180, 480), (W / 2 + 180, 480)], fill=(90, 75, 45), width=2)
    center("24H  ·  0508-202-4719", small, 505, (200, 200, 210))
    return img


def main():
    og_image().save(os.path.join(ASSETS, "og-image.png"))
    for size, name in [
        (512, "icon-512.png"),
        (192, "icon-192.png"),
        (180, "apple-touch-icon.png"),
        (32, "favicon-32.png"),
        (16, "favicon-16.png"),
    ]:
        monogram(size).save(os.path.join(ASSETS, name))
    monogram(48).save(
        os.path.join(ROOT, "favicon.ico"),
        sizes=[(16, 16), (32, 32), (48, 48)],
    )
    print("assets generated")


if __name__ == "__main__":
    main()
