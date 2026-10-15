# -*- coding: utf-8 -*-
"""
Brand assets: og-image.png and the favicon set, rendered straight from TTFs,
so nothing has to be installed system-wide. Palette and geometry are the
constants below — the same tokens as style.css.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# Geist и Geist Mono несут кириллицу — имя на обложке не уйдёт в запасной шрифт.
GEIST = os.path.join(FONTS, "Geist.ttf")
MONO = os.path.join(FONTS, "GeistMono.ttf")

# ── Graphite tokens — те же значения, что в style.css ──
CANVAS = (14, 16, 17)       # --canvas  #0e1011
PANEL = (21, 24, 25)        # карточка: --plate .32 поверх --canvas
CHIP = (29, 33, 34)         # джоба пайплайна: на тон светлее карточки
FOG = (141, 148, 143)       # --fog     #8d948f
MOON = (196, 201, 197)      # --moon    #c4c9c5
FROST = (225, 228, 225)     # --frost   #e1e4e1
ICE = (238, 240, 238)       # --ice     #eef0ee
ACCENT = (79, 174, 124)     # --accent  #4fae7c
ACCENT_LT = (108, 196, 147) # --accent-lt #6cc493
OK, OK_LT = ACCENT, ACCENT_LT


def ensure_fonts():
    import urllib.request
    base = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
    need = {
        GEIST: base + "geist/Geist%5Bwght%5D.ttf",
        MONO:  base + "geistmono/GeistMono%5Bwght%5D.ttf",
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


def panel(img, box, radius):
    """Плоская карточка: ровная заливка и волосяная граница, как .hero-cta."""
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(box, radius=radius, fill=PANEL + (255,))
    d.rounded_rectangle(box, radius=radius, outline=ICE + (26,), width=max(radius // 18, 1))


# ══════════════════════════════════════════════════════════
#  OG IMAGE — 1200 × 630
# ══════════════════════════════════════════════════════════
def make_og():
    W, H = 1200, 630
    S = 2
    img = Image.new("RGB", (W * S, H * S), CANVAS)

    def px(v):
        return int(v * S)

    d = ImageDraw.Draw(img)
    dA = ImageDraw.Draw(img, "RGBA")
    PAD = px(72)

    f_eyebrow = font(MONO, px(17), 500)
    f_name = font(GEIST, px(84), 700)
    f_sub = font(GEIST, px(21), 400)
    f_stat = font(GEIST, px(44), 600)
    f_cap = font(GEIST, px(17), 400)
    f_url = font(GEIST, px(18), 500)
    f_mono = font(MONO, px(23), 500)
    f_tag = font(MONO, px(17), 500)

    # ── eyebrow ──
    y = px(76)
    dA.ellipse([PAD, y + px(5), PAD + px(8), y + px(13)], fill=ACCENT_LT + (255,))
    tracked(d, (PAD + px(20), y), "DEVOPS / PLATFORM ENGINEER", f_eyebrow, ACCENT_LT,
            tracking=px(1.6))

    # ── name, stacked like the hero; solid, no wash ──
    y = px(110)
    d.text((PAD, y), "Иванов", font=f_name, fill=ICE)
    d.text((PAD, y + px(90)), "Темир", font=f_name, fill=ICE)

    # ── subtitle ──
    y = px(322)
    d.text((PAD, y), "Kubernetes · GitLab CI/CD · Terraform · Observability",
           font=f_sub, fill=MOON)

    # ── hairline ──
    y = px(376)
    dA.line([(PAD, y), (px(616), y)], fill=ICE + (30,), width=S)

    # ── stats ──
    y = px(406)
    stats = [("63 VM", "контуры DEV/INF/PROD"), ("70+", "сервисов в работе"), ("100%", "CI/CD покрытие")]
    x = PAD
    for val, cap in stats:
        d.text((x, y), val, font=f_stat, fill=ICE)
        d.text((x, y + px(56)), cap, font=f_cap, fill=FOG)
        x += max(d.textlength(val, font=f_stat), d.textlength(cap, font=f_cap)) + px(32)

    # ── url ──
    y = px(534)
    dA.ellipse([PAD, y + px(7), PAD + px(8), y + px(15)], fill=ACCENT_LT + (255,))
    d.text((PAD + px(20), y), "tsm-devi.github.io/Resume", font=f_url, fill=FOG)

    # ══ pipeline panel ══
    # Граф в стиле GitLab: стадии колонками, джобы со статусом, по три стадии
    # в ряд — шесть колонок с читаемыми названиями в карточку 468px не влезают.
    box = (px(660), px(96), px(1128), px(534))
    panel(img, box, radius=px(18))
    d = ImageDraw.Draw(img)
    dA = ImageDraw.Draw(img, "RGBA")

    ix, iy = px(660 + 28), px(96 + 26)
    x_end = px(1128 - 28)

    def passed(cx, cy, r):
        """Значок «пройдено»: зелёный круг с тёмной галочкой."""
        dA.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT + (255,))
        dA.line([(cx - r * .42, cy + r * .02), (cx - r * .1, cy + r * .34),
                 (cx + r * .45, cy - r * .3)],
                fill=CANVAS + (255,), width=max(int(r * .25), 1), joint="curve")

    def manual(cx, cy, r):
        """Ручная джоба (prod), как на сайте: серое кольцо и ▶, центр тяжести — в центре."""
        dA.ellipse([cx - r, cy - r, cx + r, cy + r], outline=FOG + (255,), width=max(int(r * .23), 1))
        dA.polygon([(cx - r * .17, cy - r * .32), (cx - r * .17, cy + r * .32), (cx + r * .35, cy)],
                   fill=FOG + (255,))

    # Статус пайплайна — бейдж «passed», как в GitLab; справа число джоб.
    pill_txt = "passed"
    pw = d.textlength(pill_txt, font=f_tag)
    p_x0, p_y0, p_y1 = ix, iy - px(6), iy + px(24)
    p_x1 = int(p_x0 + px(12 + 16 + 8) + pw + px(12))
    p_cy = (p_y0 + p_y1) // 2
    dA.rounded_rectangle([p_x0, p_y0, p_x1, p_y1], radius=(p_y1 - p_y0) // 2,
                         fill=OK + (40,), outline=OK_LT + (120,), width=max(S, 1))
    passed(p_x0 + px(12 + 8), p_cy, px(8))
    d.text((p_x0 + px(12 + 16 + 8), p_cy), pill_txt, font=f_tag, fill=OK_LT, anchor="lm")
    d.text((x_end, p_cy), "10 jobs", font=f_tag, fill=FOG, anchor="rm")

    dA.line([(ix, px(96 + 68)), (x_end, px(96 + 68))],
            fill=ICE + (24,), width=S)

    # ── стадии и джобы: сжатая версия пайплайна с сайта ──
    stages = [("lint", ["hadolint", "yamllint"]), ("build", ["docker"]),
              ("test", ["pytest", "coverage"]), ("scan", ["trivy", "gitleaks"]),
              ("push", ["harbor"]), ("deploy", ["dev", "prod"])]
    MANUAL = {"prod"}                             # ручной запуск — ждёт кнопки ▶
    f_job = font(MONO, px(16), 500)
    f_stage = font(MONO, px(16), 400)
    gap = px(14)                                  # зазор между колонками, в нём связка
    col_w = (x_end - ix - 2 * gap) // 3
    chip_h, chip_gap, label_h = px(40), px(10), px(30)
    rows = [px(215), px(215 + 148)]               # два ряда по 120px и 28px между ними
    for i, (name, jobs) in enumerate(stages):
        row, col = divmod(i, 3)
        x0, y0 = ix + col * (col_w + gap), rows[row]
        d.text((x0 + px(2), y0), name, font=f_stage, fill=FOG)
        for k, job in enumerate(jobs):
            cy = y0 + label_h + k * (chip_h + chip_gap)
            dA.rounded_rectangle([x0, cy, x0 + col_w, cy + chip_h], radius=chip_h // 2,
                                 fill=CHIP + (255,), outline=ICE + (26,), width=max(S, 1))
            (manual if job in MANUAL else passed)(x0 + px(13 + 9), cy + chip_h // 2, px(9))
            d.text((x0 + px(13 + 18 + 9), cy + chip_h // 2), job, font=f_job, fill=MOON, anchor="lm")
        if col < 2:                               # связка к соседу по ряду — у первой джобы
            ly = y0 + label_h + chip_h // 2
            dA.line([(x0 + col_w, ly), (x0 + col_w + gap, ly)], fill=OK_LT + (255,), width=px(2))

    img = img.resize((W, H), Image.LANCZOS)
    p = os.path.join(OUT, "og-image.png")
    img.save(p, optimize=True)
    print(f"og-image.png      {os.path.getsize(p):>8,} bytes")


# ══════════════════════════════════════════════════════════
#  FAVICONS — TS‹M monogram on a graphite disc
# ══════════════════════════════════════════════════════════
def make_icon(size):
    S = 8 if size <= 64 else 4
    n = size * S
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    ring = max(int(n * (0.040 if size <= 64 else 0.055)), 2)
    d.ellipse([0, 0, n - 1, n - 1], fill=CANVAS + (255,))
    d.ellipse([ring // 2, ring // 2, n - 1 - ring // 2, n - 1 - ring // 2],
              outline=ACCENT_LT + (255,), width=ring)

    layer = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    wt = 700 if size <= 64 else 600
    f = font(GEIST, int(n * 0.34), wt)
    left, chev, right = "TS", "‹", "M"
    wl = ld.textlength(left, font=f)
    wc = ld.textlength(chev, font=f)
    wr = ld.textlength(right, font=f)
    x = (n - (wl + wc + wr)) / 2
    y = n * 0.5
    ld.text((x, y), left, font=f, fill=ICE + (255,), anchor="lm")
    ld.text((x + wl, y), chev, font=f, fill=ACCENT_LT + (255,), anchor="lm")
    ld.text((x + wl + wc, y), right, font=f, fill=ICE + (255,), anchor="lm")

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
