# -*- coding: utf-8 -*-
"""
Brand assets for the AuthKit direction — "frosted glass cathedral at midnight".

Renders og-image.png and the full favicon set straight from TTFs, so nothing
has to be installed system-wide. Palette and geometry are the constants below.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

GROTESK = os.path.join(FONTS, "Manrope.ttf")   # Space Grotesk has no Cyrillic
INTER = os.path.join(FONTS, "Inter.ttf")

# ── AuthKit tokens ──
CANVAS = (5, 6, 15)
PLATE = (47, 52, 62)
FOG = (157, 167, 186)
MOON = (199, 211, 234)
FROST = (209, 228, 250)
ICE = (216, 236, 248)
SKY_END = (152, 192, 239)
VIOLET = (102, 58, 243)
VIOLET_LT = (138, 104, 247)
BLUEPRINT = (182, 217, 252)


def ensure_fonts():
    import urllib.request
    base = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
    need = {
        GROTESK: base + "manrope/Manrope%5Bwght%5D.ttf",
        INTER:   base + "inter/Inter%5Bopsz,wght%5D.ttf",
    }
    os.makedirs(FONTS, exist_ok=True)
    for path, url in need.items():
        if os.path.exists(path):
            continue
        print("fetching", os.path.basename(path))
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(path, "wb").write(urllib.request.urlopen(req, timeout=60).read())


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            axes = f.get_variation_axes()
            vals = []
            for ax in axes:
                nm = ax.get("name", b"")
                nm = nm.decode() if isinstance(nm, bytes) else str(nm)
                vals.append(weight if "eight" in nm or "wght" in nm.lower() else ax["default"])
            f.set_variation_by_axes(vals)
        except Exception:
            pass
    return f


def tracked(draw, xy, text, fnt, fill, tracking=0):
    """Draw text with letter-spacing; Pillow has no tracking of its own."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x - xy[0]


def tracked_width(draw, text, fnt, tracking=0):
    return sum(draw.textlength(c, font=fnt) for c in text) + tracking * max(len(text) - 1, 0)


def skywash(w, h):
    """The #d8ecf8 → #98c0ef vertical wash used on the largest type."""
    g = Image.new("RGB", (1, max(h, 1)))
    px = g.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(round(ICE[i] + (SKY_END[i] - ICE[i]) * t) for i in range(3))
    return g.resize((w, h))


def gradient_text(base, xy, text, fnt, tracking=0):
    """Paint text with the skywash by masking a gradient through the glyphs."""
    d = ImageDraw.Draw(base)
    w = int(tracked_width(d, text, fnt, tracking)) + 4
    asc, desc = fnt.getmetrics()
    h = asc + desc
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    tracked(md, (0, 0), text, fnt, 255, tracking)
    base.paste(skywash(w, h), (int(xy[0]), int(xy[1])), mask)
    return w


# ══════════════════════════════════════════════════════════
#  OG IMAGE — 1200 × 630
# ══════════════════════════════════════════════════════════
def make_og():
    W, H = 1200, 630
    S = 2
    img = Image.new("RGB", (W * S, H * S), CANVAS)

    # blueprint grid, fading toward the edges
    grid = Image.new("RGB", img.size, CANVAS)
    gd = ImageDraw.Draw(grid)
    step = 88 * S // 2
    for x in range(0, W * S, step):
        gd.line([(x, 0), (x, H * S)], fill=(20, 24, 38), width=1)
    for y in range(0, H * S, step):
        gd.line([(0, y), (W * S, y)], fill=(20, 24, 38), width=1)
    fade = Image.new("L", img.size, 0)
    ImageDraw.Draw(fade).ellipse(
        [-int(W * S * .1), -int(H * S * .35), int(W * S * 1.1), int(H * S * 1.05)], fill=255)
    fade = fade.filter(ImageFilter.GaussianBlur(180))
    img = Image.composite(grid, img, fade)

    # violet bloom anchoring the top
    bloom = Image.new("L", img.size, 0)
    ImageDraw.Draw(bloom).ellipse(
        [int(W * S * .18), -int(H * S * .45), int(W * S * .95), int(H * S * .55)], fill=255)
    bloom = bloom.filter(ImageFilter.GaussianBlur(210))
    img = Image.composite(Image.new("RGB", img.size, VIOLET), img,
                          bloom.point(lambda v: int(v * .34)))

    d = ImageDraw.Draw(img)
    PAD = 84 * S

    f_eyebrow = font(INTER, 21 * S, 600)
    f_name = font(GROTESK, 94 * S, 500)
    f_sub = font(INTER, 27 * S, 400)
    f_stat = font(GROTESK, 50 * S, 500)
    f_cap = font(INTER, 19 * S, 400)
    f_url = font(INTER, 19 * S, 500)

    y = PAD
    tracked(d, (PAD, y), "DEVOPS ENGINEER", f_eyebrow, BLUEPRINT, tracking=2.4 * S)
    y += 54 * S

    gradient_text(img, (PAD, y), "Иванов Темир", f_name)
    y += 128 * S

    d.text((PAD, y), "Kubernetes · GitLab CI/CD · Terraform · Observability",
           font=f_sub, fill=FOG)
    y += 60 * S

    d.line([(PAD, y), (W * S - PAD, y)], fill=(31, 37, 54), width=1 * S)
    y += 46 * S

    stats = [("12+", "сервисов в K8s"), ("100%", "CI/CD покрытие"), ("99.9%", "uptime СУБД")]
    x = PAD
    for val, cap in stats:
        gradient_text(img, (x, y), val, f_stat)
        d.text((x, y + 66 * S), cap, font=f_cap, fill=FOG)
        x += max(tracked_width(d, val, f_stat), d.textlength(cap, font=f_cap)) + 66 * S

    d.ellipse([PAD, H * S - PAD - 14 * S, PAD + 9 * S, H * S - PAD - 5 * S], fill=VIOLET_LT)
    d.text((PAD + 22 * S, H * S - PAD - 20 * S), "tsm-devi.github.io/Resume",
           font=f_url, fill=FOG)

    img = img.resize((W, H), Image.LANCZOS)
    p = os.path.join(OUT, "og-image.png")
    img.save(p, optimize=True)
    print(f"og-image.png      {os.path.getsize(p):>8,} bytes")


# ══════════════════════════════════════════════════════════
#  FAVICONS — TS‹M monogram on a midnight disc
# ══════════════════════════════════════════════════════════
def make_icon(size):
    S = 8 if size <= 64 else 4
    n = size * S
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    ring = max(int(n * (0.040 if size <= 64 else 0.055)), 2)
    d.ellipse([0, 0, n - 1, n - 1], fill=CANVAS + (255,))
    d.ellipse([ring // 2, ring // 2, n - 1 - ring // 2, n - 1 - ring // 2],
              outline=BLUEPRINT + (255,), width=ring)

    layer = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    wt = 600 if size <= 64 else 500
    f = font(GROTESK, int(n * 0.34), wt)
    left, chev, right = "TS", "‹", "M"
    wl = ld.textlength(left, font=f)
    wc = ld.textlength(chev, font=f)
    wr = ld.textlength(right, font=f)
    x = (n - (wl + wc + wr)) / 2
    y = n * 0.5
    ld.text((x, y), left, font=f, fill=FROST + (255,), anchor="lm")
    ld.text((x + wl, y), chev, font=f, fill=VIOLET_LT + (255,), anchor="lm")
    ld.text((x + wl + wc, y), right, font=f, fill=FROST + (255,), anchor="lm")

    fit = 0.72 if size <= 64 else 0.60
    bbox = layer.getbbox()
    if bbox:
        mark = layer.crop(bbox)
        mw, mh = mark.size
        sc = min(n * fit / mw, n * fit / mh)
        mark = mark.resize((max(int(mw * sc), 1), max(int(mh * sc), 1)), Image.LANCZOS)
        img.alpha_composite(mark, ((n - mark.width) // 2, (n - mark.height) // 2))

    return img.resize((size, size), Image.LANCZOS)


def make_favicons():
    for name, size in [("favicon-512.png", 512), ("apple-touch-icon.png", 180),
                       ("favicon-32.png", 32), ("favicon-16.png", 16)]:
        im = make_icon(size)
        if name == "apple-touch-icon.png":      # iOS masks corners itself
            bg = Image.new("RGB", im.size, CANVAS)
            bg.paste(im, (0, 0), im)
            im = bg
        p = os.path.join(OUT, name)
        im.save(p, optimize=True)
        print(f"{name:<22} {size:>4}px  {os.path.getsize(p):>8,} bytes")

    p = os.path.join(OUT, "favicon.ico")
    make_icon(64).save(p, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print(f"{'favicon.ico':<22} multi  {os.path.getsize(p):>8,} bytes")


if __name__ == "__main__":
    ensure_fonts()
    make_og()
    make_favicons()
    print("\nout:", OUT)
