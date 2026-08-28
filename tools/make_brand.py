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
MONO = os.path.join(FONTS, "JetBrainsMono.ttf")

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
OK = (38, 150, 132)
OK_LT = (63, 191, 164)


def ensure_fonts():
    import urllib.request
    base = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
    need = {
        GROTESK: base + "manrope/Manrope%5Bwght%5D.ttf",
        INTER:   base + "inter/Inter%5Bopsz,wght%5D.ttf",
        MONO:    base + "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
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


def glass(img, box, radius, blur=26, tint=(199, 211, 234), alpha=15):
    """Frosted panel: blur what's behind it, then a whisper of light on top.

    Same trick as the site's backdrop-filter — the elevation comes from an
    inset highlight along the top edge, never from a drop shadow.
    """
    x0, y0, x1, y1 = box
    region = img.crop(box).filter(ImageFilter.GaussianBlur(blur))
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=255)
    holder = img.copy()
    holder.paste(region, (x0, y0))
    img.paste(Image.composite(holder, img, mask), (0, 0))

    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(box, radius=radius, fill=tint + (alpha,))
    d.rounded_rectangle(box, radius=radius, outline=BLUEPRINT + (48,), width=max(radius // 18, 1))
    # inset frost highlight — top edge only, so the panel reads as lit from above
    hi = Image.new("L", img.size, 0)
    hd = ImageDraw.Draw(hi)
    hd.rounded_rectangle(box, radius=radius, outline=255, width=max(radius // 18, 1))
    hd.rectangle([x0, y0 + (y1 - y0) // 3, x1, y1], fill=0)
    hi = hi.filter(ImageFilter.GaussianBlur(1))
    img.paste(Image.composite(Image.new("RGB", img.size, ICE), img,
                              hi.point(lambda v: int(v * .40))), (0, 0))


# ══════════════════════════════════════════════════════════
#  OG IMAGE — 1200 × 630
# ══════════════════════════════════════════════════════════
def make_og():
    W, H = 1200, 630
    S = 2
    img = Image.new("RGB", (W * S, H * S), CANVAS)

    def px(v):
        return int(v * S)

    # ── blueprint grid, fading toward the edges ──
    grid = Image.new("RGB", img.size, CANVAS)
    gd = ImageDraw.Draw(grid)
    step = px(44)
    for x in range(0, W * S, step):
        gd.line([(x, 0), (x, H * S)], fill=(20, 24, 38), width=1)
    for y in range(0, H * S, step):
        gd.line([(0, y), (W * S, y)], fill=(20, 24, 38), width=1)
    fade = Image.new("L", img.size, 0)
    ImageDraw.Draw(fade).ellipse(
        [px(-120), px(-220), px(W + 120), px(H + 60)], fill=255)
    fade = fade.filter(ImageFilter.GaussianBlur(180))
    img = Image.composite(grid, img, fade)

    # ── violet bloom behind the name ──
    bloom = Image.new("L", img.size, 0)
    ImageDraw.Draw(bloom).ellipse(
        [px(-60), px(-300), px(760), px(360)], fill=255)
    bloom = bloom.filter(ImageFilter.GaussianBlur(200))
    img = Image.composite(Image.new("RGB", img.size, VIOLET), img,
                          bloom.point(lambda v: int(v * .38)))

    # ── aurora ribbon sweeping under the panel ──
    aur = Image.new("L", img.size, 0)
    ImageDraw.Draw(aur).ellipse([px(560), px(120), px(1320), px(430)], fill=255)
    aur = aur.filter(ImageFilter.GaussianBlur(150))
    img = Image.composite(Image.new("RGB", img.size, VIOLET_LT), img,
                          aur.point(lambda v: int(v * .22)))

    d = ImageDraw.Draw(img)
    dA = ImageDraw.Draw(img, "RGBA")
    PAD = px(72)

    f_eyebrow = font(INTER, px(19), 600)
    f_name = font(GROTESK, px(82), 600)
    f_sub = font(INTER, px(21), 400)
    f_stat = font(GROTESK, px(44), 600)
    f_cap = font(INTER, px(17), 400)
    f_url = font(INTER, px(18), 500)
    f_mono = font(MONO, px(24), 500)
    f_tag = font(MONO, px(17), 500)

    # ── eyebrow ──
    y = px(74)
    dA.ellipse([PAD, y + px(6), PAD + px(8), y + px(14)], fill=VIOLET_LT + (255,))
    tracked(d, (PAD + px(20), y), "MIDDLE+ DEVOPS ENGINEER", f_eyebrow, BLUEPRINT, tracking=px(2.6))

    # ── name, stacked like the hero ──
    y = px(112)
    gradient_text(img, (PAD, y), "Иванов", f_name)
    gradient_text(img, (PAD, y + px(88)), "Темир", f_name)

    # ── subtitle ──
    y = px(322)
    d.text((PAD, y), "Kubernetes · GitLab CI/CD · Terraform · Observability",
           font=f_sub, fill=MOON)

    # ── hairline ──
    y = px(376)
    dA.line([(PAD, y), (px(616), y)], fill=BLUEPRINT + (36,), width=S)

    # ── stats ──
    y = px(406)
    stats = [("63 VM", "контуры DEV/INF/PROD"), ("70+", "сервисов в работе"), ("100%", "CI/CD покрытие")]
    x = PAD
    for val, cap in stats:
        gradient_text(img, (x, y), val, f_stat)
        d.text((x, y + px(56)), cap, font=f_cap, fill=FOG)
        x += max(tracked_width(d, val, f_stat), d.textlength(cap, font=f_cap)) + px(32)

    # ── url ──
    y = px(534)
    dA.ellipse([PAD, y + px(7), PAD + px(8), y + px(15)], fill=VIOLET_LT + (255,))
    d.text((PAD + px(20), y), "tsm-devi.github.io/Resume", font=f_url, fill=FOG)

    # ══ pipeline panel ══
    box = (px(660), px(96), px(1128), px(534))
    glass(img, box, radius=px(18))
    d = ImageDraw.Draw(img)
    dA = ImageDraw.Draw(img, "RGBA")

    ix, iy = px(660 + 28), px(96 + 26)
    d.text((ix, iy), "// pipeline", font=f_tag, fill=BLUEPRINT)

    # "passing" pill, teal — the site's success state
    pill_txt = "passing"
    pw = d.textlength(pill_txt, font=f_tag)
    p_x1, p_y0 = px(1128 - 28), iy - px(6)
    p_x0, p_y1 = int(p_x1 - pw - px(24)), iy + px(24)
    dA.rounded_rectangle([p_x0, p_y0, p_x1, p_y1], radius=px(11),
                         fill=OK + (46,), outline=OK_LT + (110,), width=max(S, 1))
    d.text((p_x0 + px(12), iy), pill_txt, font=f_tag, fill=OK_LT)

    dA.line([(ix, px(96 + 68)), (px(1128 - 28), px(96 + 68))],
            fill=BLUEPRINT + (30,), width=S)

    # ── six stages, chained ──
    # tools come from the data-tip on each stage in index.html — real stack,
    # not decoration
    stages = [("lint", "hadolint"), ("build", "docker"), ("test", "pytest"),
              ("scan", "trivy"), ("push", "harbor"), ("deploy", "argocd")]
    cx = ix + px(17)
    top = px(218)
    stepy = px(55)
    r = px(15)

    glow = Image.new("L", img.size, 0)
    gl = ImageDraw.Draw(glow)
    for i in range(len(stages)):
        cy = top + i * stepy
        gl.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(px(9)))
    img = Image.composite(Image.new("RGB", img.size, OK_LT), img,
                          glow.point(lambda v: int(v * .30)))
    d = ImageDraw.Draw(img)
    dA = ImageDraw.Draw(img, "RGBA")

    for i, (name, tool) in enumerate(stages):
        cy = top + i * stepy
        if i:
            dA.line([(cx, cy - stepy + r + px(3)), (cx, cy - r - px(3))],
                    fill=OK_LT + (150,), width=max(px(2), 1))
        dA.ellipse([cx - r, cy - r, cx + r, cy + r],
                   fill=OK + (60,), outline=OK_LT + (255,), width=max(px(2), 1))
        # tick
        dA.line([(cx - px(6), cy), (cx - px(1.5), cy + px(4.5)),
                 (cx + px(6.5), cy - px(5))],
                fill=ICE + (255,), width=max(px(2), 1), joint="curve")
        d.text((cx + px(34), cy), name, font=f_mono, fill=FROST, anchor="lm")
        d.text((px(1128 - 28), cy), tool, font=f_tag, fill=FOG, anchor="rm")

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
