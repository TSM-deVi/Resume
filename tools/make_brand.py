# -*- coding: utf-8 -*-
"""
Slash brand assets — "Midnight vault with gilded ledger"
Renders og-image.png + the full favicon set straight from TTFs (no font install).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

PF = os.path.join(FONTS, "PlayfairDisplay.ttf")
PFI = os.path.join(FONTS, "PlayfairDisplay-Italic.ttf")
INTER = os.path.join(FONTS, "Inter.ttf")


def ensure_fonts():
    """Fetch the TTFs on first run — nothing needs installing system-wide."""
    import urllib.request
    base = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
    need = {
        PF:    base + "playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf",
        PFI:   base + "playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf",
        INTER: base + "inter/Inter%5Bopsz,wght%5D.ttf",
    }
    os.makedirs(FONTS, exist_ok=True)
    for path, url in need.items():
        if os.path.exists(path):
            continue
        print("качаю", os.path.basename(path))
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(path, "wb").write(urllib.request.urlopen(req, timeout=60).read())

# ── Slash tokens ──
OBSIDIAN = (8, 8, 10)
ONYX = (4, 4, 6)
GRAPHITE = (28, 29, 34)
SLATE = (46, 48, 56)
STEEL = (119, 122, 136)
FOG = (145, 148, 161)
MIST = (172, 175, 185)
BONE = (226, 227, 233)
WHITE = (255, 255, 255)
COPPER = (204, 145, 102)
GILD_1 = (174, 147, 87)
GILD_2 = (255, 240, 204)


def font(path, size, weight=None):
    f = ImageFont.truetype(path, size)
    if weight is not None:
        try:
            axes = f.get_variation_axes()
            vals = []
            for ax in axes:
                tag = ax.get("name", b"")
                tag = tag.decode() if isinstance(tag, bytes) else str(tag)
                vals.append(weight if "eight" in tag or "wght" in tag.lower() else ax["default"])
            f.set_variation_by_axes(vals)
        except Exception:
            pass
    return f


def gilded_gradient(w, h):
    """103deg gold→cream→gold→transparent, as an RGBA strip."""
    grad = Image.new("RGBA", (w, h))
    px = grad.load()
    stops = [(0.0, GILD_1, 255), (0.40, GILD_2, 255), (0.70, GILD_1, 255), (1.0, (189, 157, 79), 0)]
    for x in range(w):
        t = x / max(w - 1, 1)
        for i in range(len(stops) - 1):
            t0, c0, a0 = stops[i]
            t1, c1, a1 = stops[i + 1]
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0) if t1 > t0 else 0
                col = tuple(round(c0[j] + (c1[j] - c0[j]) * k) for j in range(3))
                a = round(a0 + (a1 - a0) * k)
                break
        for y in range(h):
            px[x, y] = col + (a,)
    return grad


# ══════════════════════════════════════════════════════════
#  OG IMAGE — 1200 × 630
# ══════════════════════════════════════════════════════════
def make_og():
    W, H = 1200, 630
    S = 2                      # supersample
    img = Image.new("RGB", (W * S, H * S), OBSIDIAN)
    d = ImageDraw.Draw(img)

    PAD = 80 * S

    f_eyebrow = font(INTER, 22 * S, 600)
    f_name = font(PF, 104 * S, 400)
    f_name_i = font(PFI, 104 * S, 400)
    f_sub = font(INTER, 27 * S, 300)
    f_stat = font(PF, 54 * S, 400)
    f_cap = font(INTER, 19 * S, 400)
    f_url = font(INTER, 19 * S, 500)

    y = PAD

    # eyebrow — copper, the only chromatic punctuation
    d.text((PAD, y), "DEVOPS ENGINEER", font=f_eyebrow, fill=COPPER)
    y += 52 * S

    # display name — didone, white, italic surname
    part1, part2 = "Иванов ", "Темир"
    d.text((PAD, y), part1, font=f_name, fill=WHITE)
    w1 = d.textlength(part1, font=f_name)
    d.text((PAD + w1, y), part2, font=f_name_i, fill=WHITE)
    y += 140 * S

    d.text((PAD, y), "Kubernetes · GitLab CI/CD · Terraform · Observability",
           font=f_sub, fill=MIST)
    y += 62 * S

    # hairline
    d.line([(PAD, y), (W * S - PAD, y)], fill=GRAPHITE, width=1 * S)
    y += 44 * S

    # ledger stats — serif numerals, sans captions
    stats = [("12+", "сервисов в K8s"), ("100%", "CI/CD покрытие"), ("99.9%", "uptime")]
    x = PAD
    for val, cap in stats:
        d.text((x, y), val, font=f_stat, fill=WHITE)
        d.text((x, y + 70 * S), cap, font=f_cap, fill=FOG)
        x += max(d.textlength(val, font=f_stat), d.textlength(cap, font=f_cap)) + 62 * S

    d.text((PAD, H * S - PAD - 20 * S), "tsm-devi.github.io/Resume", font=f_url, fill=STEEL)

    # ── gilded chart, bottom-right — the one sanctioned use of the gradient ──
    cx0, cy0 = int(W * S * 0.60), int(H * S * 0.52)
    cw, ch = int(W * S * 0.30), int(H * S * 0.26)
    pts_norm = [(0, .26), (.05, .23), (.10, .28), (.15, .21), (.20, .24), (.25, .19),
                (.30, .30), (.35, .25), (.40, .52), (.45, .31), (.50, .26), (.55, .22),
                (.60, .27), (.65, .20), (.70, .24), (.75, .29), (.80, .21), (.85, .44),
                (.90, .27), (.95, .20), (1.0, .16)]
    pts = [(cx0 + px * cw, cy0 + py / .60 * ch) for px, py in pts_norm]

    # soft area under the curve — faded downward so it reads as glow, not a block
    area_mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(area_mask).polygon(pts + [(pts[-1][0], cy0 + ch), (pts[0][0], cy0 + ch)], fill=255)
    fade_full = Image.new("L", img.size, 0)
    col = Image.new("L", (cw, ch))
    cp = col.load()
    for yy in range(ch):
        v = int(52 * (1 - yy / max(ch - 1, 1)) ** 1.5)
        for xx in range(cw):
            cp[xx, yy] = v
    fade_full.paste(col, (cx0, cy0))
    area_mask = Image.composite(fade_full, Image.new("L", img.size, 0), area_mask)
    img.paste(Image.new("RGB", img.size, GILD_1), (0, 0), area_mask)

    # the line itself, painted through the gilded gradient
    line_mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(line_mask).line(pts, fill=255, width=3 * S, joint="curve")
    grad = gilded_gradient(cw, 1).resize((cw, ch + 4 * S))
    full = Image.new("RGBA", img.size, (0, 0, 0, 0))
    full.paste(grad, (cx0, cy0 - 2 * S))
    img.paste(full.convert("RGB"), (0, 0), Image.composite(line_mask, Image.new("L", img.size, 0),
                                                           full.getchannel("A").point(lambda a: 255 if a else 0)))

    img = img.resize((W, H), Image.LANCZOS)
    p = os.path.join(OUT, "og-image.png")
    img.save(p, optimize=True)
    print(f"og-image.png      {os.path.getsize(p):>8,} bytes")


# ══════════════════════════════════════════════════════════
#  FAVICONS
# ══════════════════════════════════════════════════════════
def make_icon(size, mark):
    """mark: 'full' → TS<M monogram · 'compact' → chevron only"""
    S = 8 if size <= 64 else 4
    n = size * S
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # obsidian disc + gilded ring — gold reads on both light and dark tab bars
    # thinner ring at small sizes so the monogram gets the room
    ring = max(int(n * (0.040 if size <= 64 else 0.055)), 2)
    d.ellipse([0, 0, n - 1, n - 1], fill=OBSIDIAN + (255,))
    d.ellipse([ring // 2, ring // 2, n - 1 - ring // 2, n - 1 - ring // 2],
              outline=GILD_1 + (255,), width=ring)

    # Draw the mark on its own layer, then scale it to fit inside the ring
    # with real breathing room — measuring beats guessing at font sizes.
    layer = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    if mark == "full":
        wt = 600 if size <= 64 else 500      # heavier strokes survive downscaling
        f = font(PF, int(n * 0.34), wt)
        fc = font(PF, int(n * 0.38), wt)
        left, chev, right = "TS", "‹", "M"
        wl = ld.textlength(left, font=f)
        wc = ld.textlength(chev, font=fc)
        wr = ld.textlength(right, font=f)
        x = (n - (wl + wc + wr)) / 2
        y = n * 0.5
        ld.text((x, y), left, font=f, fill=BONE + (255,), anchor="lm")
        ld.text((x + wl, y), chev, font=fc, fill=GILD_2 + (255,), anchor="lm")
        ld.text((x + wl + wc, y), right, font=f, fill=BONE + (255,), anchor="lm")
        fit = 0.72 if size <= 64 else 0.60   # small icons need every pixel
    else:
        # A drawn chevron survives 16px; a serif glyph turns to mush.
        w = max(int(n * 0.11), 2)
        cx, cy = n / 2, n / 2
        dx, dy = n * 0.14, n * 0.20
        ld.line([(cx + dx * 0.6, cy - dy), (cx - dx, cy), (cx + dx * 0.6, cy + dy)],
                fill=GILD_2 + (255,), width=w, joint="curve")
        fit = 0.42

    bbox = layer.getbbox()
    if bbox:
        mark_img = layer.crop(bbox)
        mw, mh = mark_img.size
        scale = min(n * fit / mw, n * fit / mh)
        mark_img = mark_img.resize((max(int(mw * scale), 1), max(int(mh * scale), 1)), Image.LANCZOS)
        img.alpha_composite(mark_img, ((n - mark_img.width) // 2, (n - mark_img.height) // 2))

    return img.resize((size, size), Image.LANCZOS)


def make_favicons():
    targets = [
        ("favicon-512.png", 512, "full"),
        ("apple-touch-icon.png", 180, "full"),
        ("favicon-32.png", 32, "full"),
        ("favicon-16.png", 16, "full"),
    ]
    for name, size, mark in targets:
        im = make_icon(size, mark)
        if name == "apple-touch-icon.png":       # iOS masks corners itself, needs opaque
            bg = Image.new("RGB", im.size, OBSIDIAN)
            bg.paste(im, (0, 0), im)
            im = bg
        p = os.path.join(OUT, name)
        im.save(p, optimize=True)
        print(f"{name:<22} {size:>4}px  {os.path.getsize(p):>8,} bytes")

    ico = make_icon(64, "full")
    p = os.path.join(OUT, "favicon.ico")
    ico.save(p, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print(f"{'favicon.ico':<22} multi  {os.path.getsize(p):>8,} bytes")


if __name__ == "__main__":
    ensure_fonts()
    make_og()
    make_favicons()
    print("\nвсё в", OUT)
