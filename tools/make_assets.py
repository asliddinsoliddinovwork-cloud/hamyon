#!/usr/bin/env python3
"""Bir martalik yordamchi: favicon.ico, img/og.png va fonts/inter-*.woff fayllarini yasaydi.

Faqat belgi (icon) yoki skrinshot o'zgarganda qayta ishga tushiriladi.
Talab: Pillow, fontTools va tizimda o'rnatilgan Inter shrifti (OFL litsenziyasi).

    python3 tools/make_assets.py [/usr/share/fonts/opentype/inter]
"""
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
INTER = Path(sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/inter")
WEIGHTS = {400: "Inter-Regular.otf", 500: "Inter-Medium.otf", 600: "Inter-SemiBold.otf"}
# Lotin (o'zbek), kirill (rus) va saytda ishlatiladigan tinish belgilari
UNICODES = (
    list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + list(range(0x400, 0x460))
    + [0x2BB, 0x2BC, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0x2190, 0x2192, 0x20BD, 0x2116]
)


def fonts():
    out = ROOT / "fonts"
    out.mkdir(exist_ok=True)
    for weight, name in WEIGHTS.items():
        font = TTFont(INTER / name)
        opts = subset.Options()
        opts.layout_features = ["kern", "liga", "tnum", "calt", "ccmp", "locl", "mark", "mkmk"]
        opts.name_IDs = [1, 2, 4, 6]
        opts.notdef_outline = True
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=UNICODES)
        sub.subset(font)
        font.flavor = "woff"
        target = out / f"inter-{weight}.woff"
        font.save(target)
        print(f"  fonts/{target.name}  {target.stat().st_size / 1024:.1f} KB")


def favicon():
    icon = Image.open(ROOT / "app/icons/icon-192.png").convert("RGBA")
    icon.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"  favicon.ico  {(ROOT / 'favicon.ico').stat().st_size / 1024:.1f} KB")


def og_image():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(img)
    semi = lambda s: ImageFont.truetype(str(INTER / "Inter-SemiBold.otf"), s)
    reg = lambda s: ImageFont.truetype(str(INTER / "Inter-Regular.otf"), s)

    # Chapda: belgi, nom, shior
    icon = Image.open(ROOT / "app/icons/icon-512.png").convert("RGBA").resize((120, 120), Image.LANCZOS)
    mask = Image.new("L", (120, 120), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 119, 119), radius=27, fill=255)
    img.paste(icon, (80, 96), mask)
    d.text((80, 250), "Hamyon", font=semi(92), fill="#1D1D1F")
    d.text((82, 368), "Pulingiz qayerga", font=reg(40), fill="#86868B")
    d.text((82, 420), "ketayotganini biling.", font=reg(40), fill="#1D1D1F")
    d.text((82, 506), "Android · iPhone · hamyonapp.uz", font=reg(26), fill="#0E8A3E")

    # O'ngda: ilova skrinshoti telefon ramkasida (pastdan kesilgan)
    shot = Image.open(ROOT / "img/home.webp").convert("RGB")
    pw = 380
    ph = int(shot.height * pw / shot.width)
    shot = shot.resize((pw, ph), Image.LANCZOS)
    x, y, pad, r = 720, 70, 14, 58
    d.rounded_rectangle((x - pad, y - pad, x + pw + pad, H + 80), radius=r + pad, fill="#1D1D1F")
    screen = Image.new("RGB", (pw, H - y), "#EBEBEB")
    screen.paste(shot, (0, 44))
    m = Image.new("L", (pw, H - y), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, pw - 1, H - y + r), radius=r, fill=255)
    img.paste(screen, (x, y), m)
    d.rounded_rectangle((x + pw // 2 - 55, y + 12, x + pw // 2 + 55, y + 40), radius=14, fill="#000000")

    img.save(ROOT / "img/og.png", optimize=True)
    print(f"  img/og.png  {(ROOT / 'img/og.png').stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    print("Yozildi:")
    fonts()
    favicon()
    og_image()
