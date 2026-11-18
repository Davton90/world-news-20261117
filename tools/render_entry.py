"""Render entry.png: one image summing up the world news of Tuesday 17 November 2026.

Hand-set editorial layout, drawn with Pillow at 2x and downsampled for clean edges.
Run: python tools/render_entry.py
"""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
S = 2  # supersample factor

BG = (7, 11, 18)
CARD = (14, 22, 34)
CARD2 = (16, 25, 38)
BORDER = (30, 42, 58)
WHITE = (245, 247, 250)
MUTED = (152, 167, 187)
DIM = (110, 128, 150)
ACCENT = (255, 106, 69)
STEEL = (104, 128, 160)
LIGHT = (222, 230, 241)

FONT_DIR = r"C:\Windows\Fonts"
BLACK = os.path.join(FONT_DIR, "seguibl.ttf")
BOLD = os.path.join(FONT_DIR, "segoeuib.ttf")
SEMI = os.path.join(FONT_DIR, "seguisb.ttf")
REG = os.path.join(FONT_DIR, "segoeui.ttf")


def font(path: str, size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, max(6, int(round(size * S))))


F_DATE = font(BLACK, 72)
F_MAST = font(BOLD, 18)
F_SUB = font(REG, 16)
F_TICK = font(SEMI, 17)
F_FOOT = font(REG, 14)


def sp(text: str, tracking: int = 2) -> str:
    return ("".join(ch + " " * tracking for ch in text)).rstrip()


def text_w(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> float:
    box = d.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


def wrap(d, text: str, f, max_w: float):
    words, lines, cur = text.split(), [], ""
    limit = max_w * S
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(d, trial, f) <= limit or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(d, text: str, path: str, size: float, max_w: float):
    """Return a font at the largest size <= size that fits max_w (1x units)."""
    f = font(path, size)
    while text_w(d, text, f) > max_w * S and f.size > 8 * S:
        f = ImageFont.truetype(path, f.size - 1)
    return f


def card(d, box, radius=16, fill=CARD, outline=BORDER, width=2):
    x0, y0, x1, y1 = [v * S for v in box]
    d.rounded_rectangle([x0, y0, x1, y1], radius=radius * S, fill=fill,
                        outline=outline, width=int(width * S))


def line(d, pts, color, width=3):
    d.line([(x * S, y * S) for x, y in pts], fill=color, width=max(1, int(width * S)))


def ellipse(d, box, fill=None, outline=None, width=2):
    d.ellipse([v * S for v in box], fill=fill, outline=outline,
              width=max(1, int(width * S)))


def arc(d, box, start, end, color, width=3):
    d.arc([v * S for v in box], start, end, fill=color, width=max(1, int(width * S)))


def poly(d, pts, fill=None, outline=None, width=2):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline,
              width=max(1, int(width * S)))


# --------------------------------------------------------------------------- icons


def icon_target(d, x, y, s=46):
    """A crosshair with a drone above it: strikes on US radar in Bahrain."""
    cx, cy = x + s * 0.44, y + s * 0.58
    r = s * 0.30
    ellipse(d, [cx - r, cy - r, cx + r, cy + r], outline=ACCENT, width=3)
    ellipse(d, [cx - r * 0.34, cy - r * 0.34, cx + r * 0.34, cy + r * 0.34], fill=ACCENT)
    for a, b in (((cx - r * 1.55, cy), (cx - r * 1.12, cy)),
                 ((cx + r * 1.12, cy), (cx + r * 1.55, cy)),
                 ((cx, cy - r * 1.55), (cx, cy - r * 1.12)),
                 ((cx, cy + r * 1.12), (cx, cy + r * 1.55))):
        line(d, [a, b], LIGHT, 3)
    # drone above, small and clean
    dx, dy = cx, y + s * 0.16
    line(d, [(dx - s * 0.16, dy), (dx + s * 0.16, dy)], LIGHT, 2)
    for ox in (-0.16, 0.16):
        ellipse(d, [dx + s * ox - s * 0.045, dy - s * 0.045,
                    dx + s * ox + s * 0.045, dy + s * 0.045], fill=LIGHT)
    ellipse(d, [dx - s * 0.04, dy - s * 0.04, dx + s * 0.04, dy + s * 0.04], fill=ACCENT)


def icon_globe(d, x, y, s=46):
    """Globe with a route between two pins: the Manila and China summits."""
    cx, cy, r = x + s * 0.48, y + s * 0.52, s * 0.36
    ellipse(d, [cx - r, cy - r, cx + r, cy + r], outline=STEEL, width=3)
    ellipse(d, [cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=STEEL, width=2)
    line(d, [(cx - r, cy), (cx + r, cy)], STEEL, 2)
    # route over the top
    arc(d, [cx - r * 0.9, cy - r * 1.35, cx + r * 0.9, cy + r * 0.3], 200, 330, ACCENT, 3)
    for px, py in ((cx - r * 0.62, cy - r * 0.74), (cx + r * 0.60, cy - r * 0.80)):
        ellipse(d, [px - s * 0.045, py - s * 0.045, px + s * 0.045, py + s * 0.045],
                fill=ACCENT)


def icon_virus(d, x, y, s=46):
    """A virus particle beside a cracked shield: the lost measles-free status."""
    cx, cy, r = x + s * 0.42, y + s * 0.50, s * 0.22
    for i in range(12):
        a = math.radians(i * 30 + 8)
        x0, y0 = cx + math.cos(a) * r, cy + math.sin(a) * r
        x1, y1 = cx + math.cos(a) * (r + s * 0.12), cy + math.sin(a) * (r + s * 0.12)
        line(d, [(x0, y0), (x1, y1)], ACCENT, 2)
        ellipse(d, [x1 - s * 0.033, y1 - s * 0.033, x1 + s * 0.033, y1 + s * 0.033],
                fill=ACCENT)
    ellipse(d, [cx - r, cy - r, cx + r, cy + r], fill=(36, 22, 26), outline=ACCENT, width=3)
    ellipse(d, [cx - r * 0.40, cy - r * 0.40, cx + r * 0.40, cy + r * 0.40], fill=ACCENT)
    sx, sy = x + s * 0.80, y + s * 0.50
    poly(d, [(sx, sy - s * 0.26), (sx + s * 0.17, sy - s * 0.17), (sx + s * 0.13, sy + s * 0.12),
             (sx, sy + s * 0.26), (sx - s * 0.13, sy + s * 0.12), (sx - s * 0.17, sy - s * 0.17)],
         outline=STEEL, width=3)
    line(d, [(sx - s * 0.01, sy - s * 0.12), (sx + s * 0.06, sy - s * 0.01),
             (sx - s * 0.04, sy + s * 0.08)], ACCENT, 2)


def icon_chip(d, x, y, s=46):
    """A processor and a refused return arrow: Nvidia's board and its ex-CEO."""
    cx, cy, r = x + s * 0.46, y + s * 0.54, s * 0.24
    d.rounded_rectangle([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                        radius=5 * S, outline=LIGHT, width=3 * S)
    d.rounded_rectangle([(cx - r * 0.44) * S, (cy - r * 0.44) * S,
                         (cx + r * 0.44) * S, (cy + r * 0.44) * S],
                        radius=3 * S, fill=ACCENT)
    for i in (-0.55, 0.0, 0.55):
        off = r * i
        line(d, [(cx + off, cy - r), (cx + off, cy - r - s * 0.09)], STEEL, 3)
        line(d, [(cx + off, cy + r), (cx + off, cy + r + s * 0.09)], STEEL, 3)
        line(d, [(cx - r, cy + off), (cx - r - s * 0.09, cy + off)], STEEL, 3)
        line(d, [(cx + r, cy + off), (cx + r + s * 0.09, cy + off)], STEEL, 3)
    ax, ay = x + s * 0.84, y + s * 0.30
    arc(d, [ax - s * 0.13, ay - s * 0.13, ax + s * 0.13, ay + s * 0.13], 60, 300, LIGHT, 2)
    poly(d, [(ax - s * 0.14, ay - s * 0.18), (ax - s * 0.02, ay - s * 0.11),
             (ax - s * 0.13, ay - s * 0.02)], fill=LIGHT)
    line(d, [(ax - s * 0.13, ay + s * 0.13), (ax + s * 0.13, ay - s * 0.13)], ACCENT, 3)


def bridge_scene(d, x0, y0, x1, y1):
    """A long bridge over water with one span blown out and smoke rising from it."""
    w, h = x1 - x0, y1 - y0
    water = y0 + h * 0.78
    deck = y0 + h * 0.55

    # water: horizon, ripples, reflections
    line(d, [(x0, water), (x1, water)], (34, 50, 70), 2)
    for i, yy in enumerate((water + 12, water + 28, water + 44)):
        line(d, [(x0 + 12 + i * 18, yy), (x1 - 18 - i * 14, yy)], (26, 40, 58), 3)

    gap_l, gap_r = x0 + w * 0.44, x0 + w * 0.60

    # deck runs, piers, cables
    for a, b in ((x0 + 2, gap_l), (gap_r, x1 - 2)):
        line(d, [(a, deck), (b, deck)], LIGHT, 6)
        line(d, [(a, deck + 9), (b, deck + 9)], STEEL, 3)
        span = b - a
        n = max(2, int(span / 92))
        for i in range(n + 1):
            px = a + span * i / n
            line(d, [(px, deck + 9), (px, water + 10)], STEEL, 3)
    for tx in (x0 + w * 0.17, x0 + w * 0.83):
        line(d, [(tx, deck), (tx, y0 + h * 0.06)], LIGHT, 6)
        line(d, [(tx, y0 + h * 0.16), (tx - w * 0.045, y0 + h * 0.16)], LIGHT, 5)
        for k in range(6):
            f = k / 5
            yy = y0 + h * 0.07 + (deck - y0 - h * 0.07) * f
            line(d, [(tx + 3, yy), (tx + w * 0.105 * (1 - f) + 4, deck)], STEEL, 2)

    # the broken span: ragged stubs angled into the gap, debris below
    for sx, ang in ((gap_l, 1), (gap_r, -1)):
        line(d, [(sx, deck), (sx + ang * 14, deck + 14)], LIGHT, 6)
        line(d, [(sx + ang * 14, deck + 14), (sx + ang * 10, deck + 27)], LIGHT, 5)
        line(d, [(sx + ang * 10, deck + 27), (sx + ang * 21, deck + 34)], LIGHT, 4)
    for sx, sy in ((gap_l + 18, deck + 40), (gap_r - 24, deck + 48),
                   (x0 + w * 0.52, water + 4), (gap_l + 6, water + 16)):
        line(d, [(sx, sy), (sx + 13, sy + 8)], STEEL, 4)

    # blast: a burst of rays with a hot core, just above the deck
    bx, by = (gap_l + gap_r) / 2, deck - 2
    for i in range(10):
        a = math.radians(i * 36 + 12)
        r0, r1 = 20, (46 if i % 2 else 34)
        line(d, [(bx + math.cos(a) * r0, by + math.sin(a) * r0 * 0.8),
                 (bx + math.cos(a) * r1, by + math.sin(a) * r1 * 0.8)], ACCENT, 5)
    for r, col in ((26, (120, 36, 18)), (17, ACCENT), (9, (255, 190, 120)), (4, (255, 240, 210))):
        ellipse(d, [bx - r, by - r * 0.85, bx + r, by + r * 0.85], fill=col)
    for i in range(3):
        line(d, [(bx - 22 + i * 4, water + 14 + i * 12), (bx + 22 - i * 4, water + 14 + i * 12)],
             (120, 58, 34), 3)

    # smoke: a rising column, thinning as it climbs
    for ox, oy, rr, col in ((0, -20, 13, (40, 48, 60)), (7, -34, 11, (50, 59, 73)),
                            (-5, -47, 10, (50, 59, 73)), (3, -59, 8, (40, 48, 60)),
                            (-1, -70, 6, (50, 59, 73))):
        ellipse(d, [bx + ox - rr, deck + oy - rr, bx + ox + rr, deck + oy + rr], fill=col)


# --------------------------------------------------------------------------- layout


def build() -> Image.Image:
    img = Image.new("RGB", (W * S, H * S), BG)
    d = ImageDraw.Draw(img)

    for gx in range(0, W, 64):
        line(d, [(gx, 0), (gx, H)], (13, 19, 29), 1)
    for gy in range(0, H, 64):
        line(d, [(0, gy), (W, gy)], (13, 19, 29), 1)

    m = 40
    right = W - m

    # masthead
    d.text((m * S, 32 * S), sp("THE WORLD", 4), font=F_MAST, fill=MUTED)
    d.text((right * S - text_w(d, sp("TUESDAY", 4), F_MAST), 32 * S),
           sp("TUESDAY", 4), font=F_MAST, fill=MUTED)
    d.text((m * S, 58 * S), "17 NOVEMBER 2026", font=F_DATE, fill=WHITE)
    d.text((right * S - text_w(d, "the day's news in one image", F_SUB), 120 * S),
           "the day's news in one image", font=F_SUB, fill=DIM)
    line(d, [(m, 148), (m + 132, 148)], ACCENT, 4)
    line(d, [(m + 144, 148), (right, 148)], BORDER, 2)

    # hero
    hx0, hy0, hx1, hy1 = m, 170, 600, 600
    card(d, (hx0, hy0, hx1, hy1), radius=18)
    d.text(((hx0 + 24) * S, (hy0 + 20) * S), sp("EUROPE  ·  WAR", 3), font=F_TICK, fill=ACCENT)
    yy = hy0 + 56
    for ln in ("KERCH BRIDGE", "SPAN DESTROYED"):
        d.text(((hx0 + 24) * S, yy * S), ln, font=font(BLACK, 54), fill=WHITE)
        yy += 60
    yy += 4
    body = ("Ukraine hits Russia's only Crimea link a second night running; Moscow's "
            "missiles damage two Kyiv bridges and kill at least two.")
    for ln in wrap(d, body, F_SUB, hx1 - hx0 - 48):
        d.text(((hx0 + 24) * S, yy * S), ln, font=F_SUB, fill=MUTED)
        yy += 22
    bridge_scene(d, hx0 + 24, hy0 + 258, hx1 - 24, hy1 - 16)

    # right column
    r_tiles = [
        dict(kick="MIDDLE EAST", head=("IRAN HITS U.S.", "RADAR IN BAHRAIN"),
             sub="Third drone attack in days; Bahrain says air defenses intercepted it.",
             icon=icon_target),
        dict(kick="ASIA  ·  DIPLOMACY", head=("TRUMP IN MANILA,", "THEN CHINA"),
             sub="ASEAN and Quad summits; a first Xi–Putin–Trump meeting is next.",
             icon=icon_globe),
    ]
    rx0, rx1 = 620, right
    ty = hy0
    for t in r_tiles:
        card(d, (rx0, ty, rx1, ty + 206))
        t["icon"](d, rx0 + 20, ty + 18, 44)
        d.text(((rx0 + 78) * S, (ty + 24) * S), sp(t["kick"], 1), font=font(BOLD, 14), fill=ACCENT)
        yy = ty + 50
        hf = font(BLACK, 27)
        for ln in t["head"]:
            d.text(((rx0 + 78) * S, yy * S), ln, font=hf, fill=WHITE)
            yy += 31
        yy += 4
        for ln in wrap(d, t["sub"], font(REG, 15), rx1 - rx0 - 98):
            d.text(((rx0 + 78) * S, yy * S), ln, font=font(REG, 15), fill=MUTED)
            yy += 19
        ty += 218

    # bottom row
    bottom = [
        dict(kick="NORTH AMERICA  ·  HEALTH", head=("U.S. LOSES", "MEASLES-FREE", "STATUS"),
             sub="PAHO ends 26 years of elimination as outbreaks spread.",
             icon=icon_virus),
        dict(kick="TECHNOLOGY  ·  MARKETS", head=("NVIDIA SHUNS", "HUANG'S RETURN"),
             sub="Board rules out its ex-CEO as quarterly revenue beats forecasts.",
             icon=icon_chip),
    ]
    bw = (right - m - 2 * 16) // 3
    by0, by1 = 616, 912
    for i, t in enumerate(bottom):
        bx = m + i * (bw + 16)
        card(d, (bx, by0, bx + bw, by1))
        t["icon"](d, bx + 20, by0 + 20, 48)
        ff = fit(d, sp(t["kick"], 1), BOLD, 13, bw - 96)
        d.text(((bx + 80) * S, (by0 + 38) * S), sp(t["kick"], 1), font=ff, fill=ACCENT)
        yy = by0 + 84
        hf = font(BLACK, 29)
        for ln in t["head"]:
            d.text(((bx + 20) * S, yy * S), ln, font=hf, fill=WHITE)
            yy += 33
        yy += 8
        for ln in wrap(d, t["sub"], font(REG, 15), bw - 40):
            # last line keeps clear of the card edge
            d.text(((bx + 20) * S, yy * S), ln, font=font(REG, 15), fill=MUTED)
            yy += 19

    # elsewhere
    bx = m + 2 * (bw + 16)
    card(d, (bx, by0, bx + bw, by1), fill=CARD2)
    d.text(((bx + 20) * S, (by0 + 24) * S), sp("ELSEWHERE", 1), font=font(BOLD, 14), fill=ACCENT)
    notes = [
        ("LATIN AMERICA", "Chile's president, José Antonio Kast, meets Xi Jinping in Shenzhen."),
        ("AFRICA", "Nigeria's inflation eases to 14.1% as food prices slow."),
        ("PACIFIC", "Magnitude 6.6 quake off Indonesia's Tual, in the Banda Sea."),
    ]
    yy = by0 + 56
    for place, txt in notes:
        d.text(((bx + 20) * S, yy * S), place, font=font(SEMI, 12), fill=LIGHT)
        yy += 18
        for ln in wrap(d, txt, font(REG, 14), bw - 40):
            d.text(((bx + 20) * S, yy * S), ln, font=font(REG, 14), fill=MUTED)
            yy += 17
        yy += 14

    line(d, [(m, 934), (right, 934)], BORDER, 2)
    d.text((m * S, 950 * S),
           "World news of Tuesday 17 November 2026  ·  events as reported that day",
           font=F_FOOT, fill=DIM)

    return img.resize((W, H), Image.LANCZOS)


def main() -> None:
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "entry.png")
    build().save(out, "PNG", optimize=True)
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
