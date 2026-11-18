"""Render entry.png: a one-page newspaper of Tuesday 17 November 2026.

Flat editorial layout drawn with Pillow at 2x and downsampled for clean edges.
Run: python tools/render_entry.py
"""

from __future__ import annotations

import os
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
S = 2  # supersample factor

PAPER = (246, 243, 235)
INK = (21, 22, 25)
BODY = (58, 60, 64)
RED = (170, 40, 32)
MUTED = (124, 119, 110)
RULE = (198, 191, 177)
STEEL = (120, 143, 163)
SEA = (218, 225, 229)
SMOKE = (146, 144, 138)
SAND = (226, 220, 206)

FONT_DIR = r"C:\Windows\Fonts"
SERIF_B = os.path.join(FONT_DIR, "georgiab.ttf")
SERIF = os.path.join(FONT_DIR, "georgia.ttf")
SERIF_I = os.path.join(FONT_DIR, "georgiai.ttf")
SANS_B = os.path.join(FONT_DIR, "segoeuib.ttf")
SANS_SB = os.path.join(FONT_DIR, "seguisb.ttf")
SANS = os.path.join(FONT_DIR, "segoeui.ttf")


def font(path: str, size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, max(6, int(round(size * S))))


def sp(text: str) -> str:
    """Letterspaced caps for kickers."""
    return "\u2009".join(text)


def tw(d: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> float:
    box = d.textbbox((0, 0), text, font=f)
    return (box[2] - box[0]) / S


def wrap(d, text: str, f, max_w: float):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tw(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, text, f, x, y, max_w, leading, color=INK, max_lines=None):
    lines = wrap(d, text, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x * S, y * S), ln, font=f, fill=color)
        y += leading
    return y


def text(d, x, y, s, f, color=INK):
    d.text((x * S, y * S), s, font=f, fill=color)


def hline(d, x0, x1, y, color=RULE, width=1.0):
    d.line([(x0 * S, y * S), (x1 * S, y * S)], fill=color, width=max(1, int(width * S)))


def vline(d, x, y0, y1, color=RULE, width=1.0):
    d.line([(x * S, y0 * S), (x * S, y1 * S)], fill=color, width=max(1, int(width * S)))


def rect(d, box, fill=None, outline=None, width=1.0):
    d.rectangle([v * S for v in box], fill=fill, outline=outline,
                width=max(1, int(width * S)))


def poly(d, pts, fill=None, outline=None):
    d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)


def line(d, pts, color=INK, width=1.0):
    d.line([(x * S, y * S) for x, y in pts], fill=color, width=max(1, int(width * S)))


def dot(d, cx, cy, r, fill=RED):
    d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=fill)


# --------------------------------------------------------------------------- type

F_KICK = font(SANS_B, 8.6)
F_RAILK = font(SANS_B, 8.4)
F_LEAD = font(SERIF_B, 35)
F_RAIL = font(SERIF_B, 21)
F_TILE = font(SERIF_B, 18.5)
F_BRIEF = font(SANS_SB, 11.2)
F_DEK = font(SANS, 11)
F_DEK_S = font(SANS, 10)
F_STAT = font(SANS_B, 27)
F_STAT_BIG = font(SANS_B, 30)
F_STATLBL = font(SANS, 7.8)
F_FOOT = font(SANS, 8.6)
F_DECK = font(SERIF_I, 12.4)

M = 28
CW = W - 2 * M


# ---------------------------------------------------------------- lead picture

def bridge(d, canvas, x, y, w, h):
    """Duotone drawing of the Kerch Bridge: two decks, one span broken into the strait."""
    SKY = (26, 36, 47)
    DEEP = (14, 24, 33)
    LIGHT = (232, 230, 220)
    CABLE = (140, 163, 184)
    INK2 = (232, 230, 220)
    water = y + h * 0.70
    rect(d, (x, y, x + w, y + h), SKY)
    rect(d, (x, water, x + w, y + h), DEEP)

    # distant shores
    poly(d, [(x, water), (x + w * 0.18, water - 8), (x + w * 0.31, water),
             (x + w * 0.31, water)], fill=(45, 59, 73))
    poly(d, [(x + w * 0.74, water), (x + w * 0.88, water - 10), (x + w, water - 4),
             (x + w, water)], fill=(45, 59, 73))

    deck_y = y + h * 0.52
    for sx, ex, pylon in ((x + 1, x + w * 0.395, x + w * 0.27),
                          (x + w * 0.605, x + w - 1, x + w * 0.73)):
        # deck slab: a filled bar reads better than a single line
        rect(d, (sx, deck_y, ex, deck_y + 4.5), fill=LIGHT)
        px, ptop = pylon, deck_y - 52
        line(d, [(px, ptop), (px, water)], LIGHT, 3.4)
        line(d, [(px - 6, ptop), (px + 6, ptop)], LIGHT, 2.6)
        for i in range(8):
            t = i / 7
            line(d, [(px, ptop + 4), (px + (ex - px) * (0.16 + 0.84 * t), deck_y - 1)],
                 CABLE, 1.15)
            line(d, [(px, ptop + 4), (px - (px - sx) * (0.16 + 0.84 * t), deck_y - 1)],
                 CABLE, 1.05)
        for q in (0.16, 0.5, 0.84):
            qx = sx + (ex - sx) * q
            line(d, [(qx, deck_y + 5), (qx, water + 5)], LIGHT, 2.6)

    gap_l, gap_r = x + w * 0.375, x + w * 0.625

    # broken ends: torn slabs, the right one sagging toward the water
    poly(d, [(gap_l - 4, deck_y), (gap_l + 13, deck_y + 2), (gap_l + 9, deck_y + 10),
             (gap_l - 4, deck_y + 5)], fill=INK2)
    poly(d, [(gap_r + 4, deck_y), (gap_r - 13, deck_y + 2), (gap_r - 9, deck_y + 10),
             (gap_r + 4, deck_y + 5)], fill=INK2)

    # the fallen span, half sunk
    poly(d, [(x + w * 0.437, water + 2), (x + w * 0.545, water - 20),
             (x + w * 0.585, water - 13), (x + w * 0.503, water + 6),
             (x + w * 0.458, water + 6)],
         fill=(206, 204, 194), outline=LIGHT)
    line(d, [(x + w * 0.452, water + 3), (x + w * 0.552, water - 16)], (150, 150, 142), 0.8)
    line(d, [(x + w * 0.470, water + 4), (x + w * 0.570, water - 14)], (150, 150, 142), 0.8)
    for i in range(3):
        line(d, [(x + w * (0.385 + i * 0.018), water + 4),
                 (x + w * (0.415 + i * 0.018), water + 4)], CABLE, 0.9)

    # dark smoke rising from the gap: a narrow base that spreads as it climbs
    plume = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plume)
    rng = random.Random(5)
    cx = (gap_l + gap_r) / 2 - x
    for i in range(11):
        rx = cx + rng.uniform(-6, 8) + i * 3.4
        ry = h * 0.47 - i * 8.6
        rr = 5.5 + i * 2.0
        alpha = max(14, 110 - i * 9)
        col = (196, 194, 186) if i < 5 else (160, 160, 154)
        pd.ellipse([(rx - rr) * S, (ry - rr) * S, (rx + rr) * S, (ry + rr) * S],
                   fill=col + (alpha,))
    canvas.paste(plume, (int(x * S), int(y * S)), plume)

    # fire at the break
    fx, fy = gap_l + 4, deck_y - 1
    poly(d, [(fx - 4, fy), (fx, fy - 11), (fx + 2, fy - 5), (fx + 5, fy - 12),
             (fx + 6, fy)], fill=(214, 92, 46))
    poly(d, [(fx - 2, fy - 1), (fx, fy - 7), (fx + 3, fy - 1)], fill=(232, 166, 80))
    # rubble in the water below the gap
    for dx, dy, s_ in ((0.46, 2, 3.4), (0.51, 6, 2.4), (0.56, 1, 2.0)):
        poly(d, [(x + w * dx, water + dy), (x + w * dx + s_, water + dy - 2.5),
                 (x + w * dx + s_ * 1.6, water + dy + 1.4)],
             fill=(120, 118, 112))

    # drones above
    for (dx, dy) in ((x + w * 0.10, y + h * 0.16), (x + w * 0.185, y + h * 0.30),
                     (x + w * 0.64, y + h * 0.13)):
        line(d, [(dx - 8, dy), (dx + 8, dy)], LIGHT, 2.0)
        for o in (-8, -2.6, 2.6, 8):
            line(d, [(dx + o, dy - 2.2), (dx + o, dy + 2.2)], LIGHT, 1.0)
        line(d, [(dx - 3.5, dy - 11), (dx - 7.5, dy - 17)], LIGHT, 0.9)
        line(d, [(dx + 3.5, dy - 11), (dx + 7.5, dy - 17)], LIGHT, 0.9)
    for i in range(8):
        t = i / 8
        dot(d, x + w * 0.03 + w * 0.26 * t, y + h * 0.06 + h * 0.22 * t, 1.1,
            (120, 140, 158))

    text(d, x + 10, water + 9, sp("KERCH STRAIT"), F_STATLBL, (168, 184, 198))
    cap = "Crimea"
    text(d, x + w - 12 - tw(d, cap, F_STATLBL), water + 9, cap, F_STATLBL, (168, 184, 198))


# ------------------------------------------------------------------- stories

def kicker(d, x, y, s, color=RED, f=F_KICK):
    text(d, x, y, sp(s), f, color)
    return y + 13


def rail_story(d, x, y, w, kick, head, dek):
    y = kicker(d, x, y, kick)
    y = draw_wrapped(d, head, F_RAIL, x, y, w, 22.5, INK, 3)
    draw_wrapped(d, dek, F_DEK_S, x, y + 3, w, 13.4, BODY, 4)


def stat_tile(d, x, y, w, stat, statlbl, kick, head, dek, graphic=None, gw=0):
    text(d, x, y - 4, stat, F_STAT, RED)
    text(d, x, y + 23, sp(statlbl), F_STATLBL, MUTED)
    body_w = w - (gw + 12 if graphic else 0)
    ty = y + 42
    ty = kicker(d, x, ty, kick)
    ty = draw_wrapped(d, head, F_TILE, x, ty - 1, body_w, 20.5, INK, 2)
    draw_wrapped(d, dek, F_DEK_S, x, ty + 2, body_w, 13, BODY, 2)
    if graphic:
        graphic(d, x + w - gw, y - 2, gw, 76)


def nvidia_chart(d, x, y, w, h):
    base = y + h - 12
    slot = w / 2
    for i, (val, fill, lbl) in enumerate(((57.0, STEEL, "57"), (115.8, INK, "115.8"))):
        bh = (h - 26) * (val / 115.8)
        bw = slot * 0.46
        bx = x + i * slot + (slot - bw) / 2
        rect(d, (bx, base - bh, bx + bw, base), fill=fill)
        text(d, bx + bw / 2 - tw(d, lbl, F_STATLBL) / 2, base - bh - 9, lbl,
             F_STATLBL, INK)
    hline(d, x, x + w, base, INK, 1.0)
    text(d, x, base + 3, sp("FY26"), F_STATLBL, MUTED)
    text(d, x + slot, base + 3, sp("FY27"), F_STATLBL, MUTED)


def measles_stamp(d, x, y, w, h):
    rect(d, (x + 2, y + 12, x + w, y + 42), outline=RED, width=1.8)
    label = sp("REVOKED")
    lb = font(SANS_B, 10)
    text(d, x + 2 + (w - 2 - tw(d, label, lb)) / 2, y + 21, label, lb, RED)
    big = font(SERIF_B, 40)
    text(d, x + w / 2 - tw(d, "3", big) / 2, y + 48, "3", big, RED)
    text(d, x + w / 2 - tw(d, sp("COUNTRIES"), F_STATLBL) / 2, y + 92,
         sp("COUNTRIES"), F_STATLBL, MUTED)


# ------------------------------------------------------------------------ page

def page(path: str) -> None:
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    rect(d, (0, 0, W, 6), fill=RED)
    text(d, M, 23, sp("THE WORLD IN ONE PICTURE"), F_KICK, RED)
    right = sp("25 STORIES  ·  SIX CONTINENTS  ·  REPORTED THAT DAY")
    text(d, W - M - tw(d, right, F_KICK), 23, right, F_KICK, MUTED)
    hline(d, M, W - M, 38, INK, 1.4)

    name = "Tuesday 17 November 2026"
    f = font(SERIF_B, 60)
    while tw(d, name, f) > CW - 6:
        f = ImageFont.truetype(SERIF_B, f.size - 2)
    text(d, M, 47, name, f, INK)

    text(d, M, 116,
         "War in the Gulf and on the Kerch Bridge, a measles setback in the Americas,",
         F_DECK, BODY)
    text(d, M, 131,
         "Nvidia's doubled sales, and a climate draft that speeds the exit from fossil fuels.",
         F_DECK, BODY)
    hline(d, M, W - M, 152, INK, 2.0)

    # ---- lead
    lx, lw = M, 604
    bridge(d, img, lx, 162, lw, 142)
    text(d, lx, 308, "A span of the road bridge, damaged on Monday, fell into the strait on Tuesday.",
         font(SERIF_I, 8.6), MUTED)
    y = kicker(d, lx, 326, "EUROPE  ·  UKRAINE WAR")
    y = draw_wrapped(d, "Kerch Bridge hit again as a road span falls",
                     F_LEAD, lx, y, lw, 37.5, INK, 2)
    draw_wrapped(d, "Ukrainian drones struck the bridge to Crimea for a second day, killing two "
                    "people; Russia closed the crossing. Russian missiles damaged two bridges in Kyiv.",
                 F_DEK, lx, y + 7, lw, 15, BODY, 3)

    vline(d, 656, 160, 452, RULE, 1.2)

    # ---- rail
    rx, rw = 680, W - M - 680
    rail_story(d, rx, 160, rw, "MIDDLE EAST  ·  IRAN WAR",
               "Bahrain downs drones aimed at a US base",
               "Iran's Guards say they hit a US radar at Sheikh Isa; American jets struck Qeshm "
               "Island at least six times.")
    hline(d, rx, W - M, 300, RULE, 1.0)
    rail_story(d, rx, 314, rw, "ASIA  ·  DIPLOMACY",
               "Trump brings the Quad back to Manila",
               "The US, India, Japan and Australia agreed critical-minerals deals at ASEAN; Trump "
               "meets Xi in Shenzhen next.")
    hline(d, M, W - M, 462, INK, 1.6)

    # ---- number-led tiles: three columns, two rows
    cols = 3
    gap = 26
    cw = (CW - gap * (cols - 1)) / cols
    rows = [
        ("$115.8bn", "QUARTERLY SALES", "BUSINESS  ·  MARKETS",
         "Nvidia doubles sales, and keeps its old boss out",
         "First results since Jensen Huang resigned; the board says it will not reinstate him.",
         nvidia_chart),
        ("5,700", "US MEASLES CASES", "AMERICAS  ·  HEALTH",
         "America loses its measles-free status",
         "PAHO also revoked Mexico's and Bolivia's; US cases passed 5,700 this year.",
         measles_stamp),
        ("37", "FACTORIES SHUT", "ASIA  ·  LABOUR",
         "Bangladesh police tear-gas garment workers",
         "Workers seeking ৳30,000 a month, up from ৳12,500, shut plants across Dhaka.",
         None),
        ("19", "KILLED", "EUROPE  ·  DISASTER",
         "Russian military plane crashes in Siberia",
         "An An-12 came down near Kemerovo with 19 aboard; a fault is suspected.",
         None),
        ("224", "SENTENCED", "AFRICA  ·  JUSTICE",
         "Guinea jails 224 in a gold-mining crackdown",
         "A Conakry court tried more than 1,000 people over illegal mining in Siguiri.",
         None),
        ("$120bn", "ADAPTATION GOAL", "GLOBAL  ·  CLIMATE",
         "COP31 draft urges a faster exit from fossil fuels",
         "The text calls for an immediate transition and tripled adaptation finance by 2035.",
         None),
    ]
    for i, (stat, lbl, kick, head, dek, graphic) in enumerate(rows):
        r, c = divmod(i, cols)
        x = M + c * (cw + gap)
        y = 476 + r * 126
        stat_tile(d, x, y, cw, stat, lbl, kick, head, dek,
                  graphic=graphic, gw=78 if graphic else 0)
        if c:
            vline(d, x - gap / 2, y - 2, y + 116, RULE, 0.9)
    hline(d, M, W - M, 726, INK, 1.6)
    also = sp("ALSO ON THE DAY")
    text(d, M, 731, also, F_KICK, RED)
    hline(d, M + tw(d, also, F_KICK) + 12, W - M, 738, RULE, 0.9)

    # ---- briefs: four columns, three rows
    briefs = [
        ("EUROPE", "Prague train collision injures 46"),
        ("EUROPE", "UK sanctions eight settler builders and Tzav 9"),
        ("EUROPE", "Five held in North Macedonia over Iran-linked plot"),
        ("EUROPE", "Serbia's student movement takes its seats"),
        ("ASIA", "Mongolia's president resigns over graft claims"),
        ("ASIA", "Xi meets Chile's Kast on APEC's sidelines"),
        ("ASIA", "France and Malaysia sign a rare-earths partnership"),
        ("ASIA", "Awami League mobs burn a police station in Tungipara"),
        ("AMERICAS", "Peltola takes Alaska's Senate seat from Sullivan"),
        ("AMERICAS", "Haitians march for Salvadoran anti-gang troops"),
        ("AMERICAS", "Canada and China agree further tariff cuts"),
        ("MARKETS", "Dow falls 849 points as software stocks slide"),
        ("MIDDLE EAST", "Israeli strikes kill five in Gaza despite the ceasefire"),
        ("MIDDLE EAST", "Settlers kill a 72-year-old woman near Jericho"),
        ("OCEANIA", "Magnitude 6.6 quake shakes Indonesia's Tual"),
        ("SPORT", "Haaland's 96th-minute penalty seals Norway 3-2"),
    ]
    bw = (CW - gap * 3) / 4
    for i, (kick, head) in enumerate(briefs):
        c, r = i % 4, i // 4
        x = M + c * (bw + gap)
        yy = 748 + r * 44
        text(d, x, yy, sp(kick), F_STATLBL, RED)
        draw_wrapped(d, head, F_BRIEF, x, yy + 10, bw, 12.6, INK, 2)
        if c:
            vline(d, x - gap / 2, yy - 1, yy + 34, RULE, 0.8)
    hline(d, M, W - M, 926, RULE, 1.0)

    # ---- footer
    text(d, M, 934, "Every story happened, or was first reported, on Tuesday 17 November 2026.",
         F_FOOT, BODY)
    right = sp("SOURCES: AP · REUTERS · AFP · BBC · AL JAZEERA · XINHUA · WIKIPEDIA")
    text(d, W - M - tw(d, right, F_FOOT), 934, right, F_FOOT, MUTED)

    fields = sp("CONFLICT · DIPLOMACY · POLITICS · MARKETS · HEALTH · CLIMATE · DISASTER · JUSTICE · SPORT")
    text(d, M, 956, fields, F_STATLBL, INK)

    img = img.resize((W, H), Image.LANCZOS)
    img.save(path, optimize=True)


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(here, "entry.png")
    page(out)
    print(out, os.path.getsize(out))
