# -*- coding: utf-8 -*-
"""
Hero atmosphere for the dope.security direction.

The reference site leans on a full-bleed twilight photograph — that image is
where most of its richness lives. We have no photograph, so we render one:
a violet dusk over a dark horizon, with a single signal trace crossing it.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

W, H = 2400, 1350
random.seed(7)

VIOLET = (175, 80, 255)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(stops):
    """stops: [(pos 0..1, (r,g,b)), ...]"""
    img = Image.new("RGB", (1, H))
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0) if t1 > t0 else 0
                px[0, y] = lerp(c0, c1, k)
                break
    return img.resize((W, H))


def noise(ow, oh, blur):
    """Cheap fractal noise. Cloud banks are wide and flat, so ow >> oh."""
    small = Image.new("L", (max(ow, 2), max(oh, 2)))
    sp = small.load()
    for y in range(small.height):
        for x in range(small.width):
            sp[x, y] = random.randint(0, 255)
    return small.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur))


def build():
    # ── 1. Dusk gradient. Muted — a real twilight is mostly blue-black,
    #       violet only smoulders in a narrow band near the horizon. ──
    sky = vertical_gradient([
        (0.00, (6, 6, 10)),
        (0.30, (11, 10, 20)),
        (0.52, (24, 16, 40)),
        (0.68, (46, 26, 68)),
        (0.79, (74, 40, 100)),
        (0.86, (38, 22, 52)),
        (0.93, (13, 11, 16)),
        (1.00, (9, 9, 9)),
    ])

    # ── 2. Cloud banks — wide and flat, stacked octaves ──
    clouds = Image.new("L", (W, H), 0)
    for ow, oh, blur, weight in [(9, 3, 60, 1.0), (18, 5, 30, .70),
                                 (38, 9, 14, .45), (72, 16, 6, .26)]:
        clouds = ImageChops.add(clouds, noise(ow, oh, blur).point(
            lambda v, w=weight: int(v * w)))
    # push contrast so banks actually read as structure
    clouds = clouds.point(lambda v: max(0, min(255, int((v - 118) * 2.4 + 96))))

    band = Image.new("L", (1, H))
    bp = band.load()
    for y in range(H):
        t = y / (H - 1)
        if t < .40:
            v = (t / .40) ** 2.2 * 90
        elif t < .82:
            v = 90 + (t - .40) / .42 * 165
        else:
            v = max(0, 255 - (t - .82) / .18 * 255)
        bp[0, y] = int(max(0, min(255, v)))
    clouds = ImageChops.multiply(clouds, band.resize((W, H)))
    clouds = clouds.filter(ImageFilter.GaussianBlur(5))

    # bright edges lit from below, dark undersides — that's what makes cloud
    sky = Image.composite(Image.new("RGB", (W, H), (138, 96, 176)), sky,
                          clouds.point(lambda v: int(v * .50)))
    sky = ImageChops.multiply(
        sky, Image.merge("RGB", tuple(
            ImageChops.invert(clouds).point(lambda v: 150 + v * 105 // 255)
            for _ in range(3))))

    # ── 3. Horizon bloom, restrained ──
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse(
        [int(W * .18), int(H * .72), int(W * .92), int(H * .88)], fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(190))
    sky = Image.composite(Image.new("RGB", (W, H), (150, 84, 200)), sky,
                          glow.point(lambda v: int(v * .20)))

    # ── 4. Stars, only up top where the sky stays dark ──
    stars = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(stars)
    for _ in range(420):
        x = random.randint(0, W - 1)
        y = random.randint(0, int(H * .52))
        r = random.choice([1, 1, 1, 2])
        fade = 1 - (y / (H * .52))
        sd.ellipse([x, y, x + r, y + r], fill=int(random.randint(70, 210) * fade))
    stars = stars.filter(ImageFilter.GaussianBlur(.6))
    sky = Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), sky, stars)

    # ── 5. One signal trace. Short, faint, tapering — a light in transit,
    #       not a scratch across the negative. ──
    trace = Image.new("L", (W, H), 0)
    td = ImageDraw.Draw(trace)
    x0, y0 = int(W * .46), int(H * .30)
    x1, y1 = int(W * .82), int(H * .18)
    steps = 160
    for i in range(steps):
        t = i / (steps - 1)
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        td.ellipse([x, y, x + 1.6, y + 1.6], fill=int(14 + 120 * t ** 2.2))
    trace = trace.filter(ImageFilter.GaussianBlur(1.4))
    halo = trace.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 1.1))
    sky = Image.composite(Image.new("RGB", (W, H), (214, 186, 244)), sky, halo)
    sky = Image.composite(Image.new("RGB", (W, H), (246, 238, 255)), sky, trace)
    head = Image.new("L", (W, H), 0)
    ImageDraw.Draw(head).ellipse([x1 - 3, y1 - 3, x1 + 3, y1 + 3], fill=230)
    sky = Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), sky,
                          head.filter(ImageFilter.GaussianBlur(6)))

    # ── 6. Vignette + bottom fade so page copy can sit on it ──
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-int(W * .28), -int(H * .40),
                                 int(W * 1.28), int(H * 1.30)], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(260))
    sky = Image.composite(sky, Image.new("RGB", (W, H), (9, 9, 9)), vig)

    fade = Image.new("L", (1, H))
    fp = fade.load()
    for y in range(H):
        t = y / (H - 1)
        fp[0, y] = 255 if t < .74 else int(max(0, 255 * (1 - (t - .74) / .26)))
    sky = Image.composite(sky, Image.new("RGB", (W, H), (9, 9, 9)), fade.resize((W, H)))

    # ── 7. Film grain ──
    grain = noise(W // 3, H // 3, .4).point(lambda v: 118 + (v - 128) // 7)
    sky = ImageChops.overlay(sky, Image.merge("RGB", (grain, grain, grain)))

    p = os.path.join(OUT, "hero-sky.jpg")
    sky.save(p, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"hero-sky.jpg  {W}x{H}  {os.path.getsize(p):,} bytes")


if __name__ == "__main__":
    build()
