#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: one 1536x1536 newspaper front page
summing up the world news of Thursday 19 November 2026.

Deterministic: no randomness, no timestamps, no network, no AI image
generator, no copyrighted images. Everything is drawn with PIL from the
verified facts in RESEARCH.md. Run: python3 gen_image.py [out.png]
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1536, 1536
PAPER = (247, 243, 230)      # warm newsprint
CARD = (255, 255, 255)
INK = (24, 24, 28)
NAVY = (26, 40, 72)
RED = (178, 34, 22)
GRAY = (98, 98, 102)
RULE = (214, 208, 190)
GOLD = (198, 160, 72)

FONTS = {
    "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}


def load(kind, size):
    return ImageFont.truetype(FONTS[kind], size)


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap into lines that fit max_w pixels."""
    out, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def headline_font(draw, text, sizes, max_w):
    """Biggest serif-bold size in `sizes` whose text fits max_w."""
    for size in sizes:
        fnt = load("serif_b", size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
    return load("serif_b", sizes[-1])


def summary_font(draw, text, sizes, max_w, max_lines):
    """Biggest sans size in `sizes` whose wrap stays within max_lines."""
    for size in sizes:
        fnt = load("sans", size)
        if len(wrap_text(draw, text, fnt, max_w)) <= max_lines:
            return fnt
    return load("sans", sizes[-1])


def spaced(draw, xy, text, fnt, fill, gap=5):
    """Draw text with extra space between letters (kicker style)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + gap
    return x


# ------------------------------------------------------------------ stories
LEAD = {
    "kicker": "DIPLOMACY · SHENZHEN — LEAD STORY",
    "headline": "THREE LEADERS, ONE",
    "headline2": "'PEACE DECLARATION'",
    "summary": (
        "Xi, Trump and Putin met for the first time as a trio and declared "
        "that 'a nuclear war cannot be won and must never be fought'. The "
        "declaration named no plan for Ukraine or Iran."
    ),
    "source": "REUTERS · WALL STREET JOURNAL",
}

CARDS = [
    {
        "kicker": "JUSTICE · THE HAGUE",
        "headline": "MYANMAR GUILTY OF GENOCIDE",
        "summary": "The World Court ruled Myanmar committed genocide against "
                   "the Rohingya in 2017 — the first state ever held "
                   "responsible. About 10,000 were killed.",
        "source": "REUTERS · CNN",
        "color": (34, 84, 120),
        "icon": "scales",
    },
    {
        "kicker": "UKRAINE · RUSSIA",
        "headline": "KERCH BRIDGE HIT AGAIN",
        "summary": "Ukraine struck the bridge's rail section with Neptune "
                   "missiles, halting trains days after the road span "
                   "collapsed into the sea.",
        "source": "CNN · INSTITUTE FOR THE STUDY OF WAR",
        "color": (178, 34, 22),
        "icon": "bridge",
    },
    {
        "kicker": "MARKETS · NEW YORK",
        "headline": "ANTHROPIC'S $81BN DEBUT",
        "summary": "The Claude maker's shares began trading on Nasdaq at "
                   "$83 — the largest IPO ever — and closed at $97 after "
                   "touching $115.",
        "source": "REUTERS · WALL STREET JOURNAL",
        "color": (15, 118, 110),
        "icon": "chart",
    },
    {
        "kicker": "ARCTIC · COPENHAGEN",
        "headline": "GREENLAND DEAL PASSES 109–0",
        "summary": "Denmark's parliament approved the US–Denmark–Greenland "
                   "security pact, easing months of tension over Trump's "
                   "push to take the island.",
        "source": "ASSOCIATED PRESS · AL JAZEERA",
        "color": (30, 58, 95),
        "icon": "globe",
    },
    {
        "kicker": "MIDDLE EAST · GAZA",
        "headline": "GAZA TANK RAID ENDS",
        "summary": "Israel said it concluded its first tank raid beyond the "
                   "ceasefire's Yellow Line since the 2025 truce, aimed at "
                   "a Hamas tunnel near Nuseirat.",
        "source": "REUTERS · AGENCE FRANCE-PRESSE",
        "color": (146, 64, 14),
        "icon": "tank",
    },
    {
        "kicker": "SOUTH ASIA · DHAKA",
        "headline": "BANGLADESH IN FLAMES",
        "summary": "Bombs, arson and clashes hit 28 districts in ten days "
                   "of Awami League protests; Muhammad Yunus's ancestral "
                   "home was torched. Four killed since 14 November.",
        "source": "REUTERS · THE BUSINESS STANDARD",
        "color": (109, 40, 217),
        "icon": "flame",
    },
]


# ------------------------------------------------------------------ icons
def draw_glyph(draw, kind, box, color):
    """White geometric glyph on a coloured rounded square."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=color)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w = (255, 255, 255)
    if kind == "scales":
        draw.line([(cx, cy - 24), (cx, cy + 24)], fill=w, width=5)
        draw.line([(cx - 24, cy - 15), (cx + 24, cy - 15)], fill=w, width=5)
        for dx in (-24, 24):
            draw.line([(cx + dx, cy - 15), (cx + dx - 11, cy + 3)], fill=w, width=3)
            draw.line([(cx + dx, cy - 15), (cx + dx + 11, cy + 3)], fill=w, width=3)
            draw.arc([cx + dx - 11, cy - 3, cx + dx + 11, cy + 15], 0, 180,
                     fill=w, width=3)
        draw.line([(cx - 18, cy + 24), (cx + 18, cy + 24)], fill=w, width=5)
    elif kind == "bridge":
        draw.rectangle([cx - 30, cy - 24, cx - 21, cy + 18], fill=w)
        draw.rectangle([cx + 21, cy - 24, cx + 30, cy + 18], fill=w)
        draw.line([(cx - 26, cy - 24), (cx, cy + 3)], fill=w, width=3)
        draw.line([(cx + 26, cy - 24), (cx, cy + 3)], fill=w, width=3)
        draw.rectangle([cx - 33, cy + 3, cx - 9, cy + 12], fill=w)
        draw.rectangle([cx + 9, cy + 3, cx + 33, cy + 12], fill=w)
        draw.line([(cx - 30, cy + 26), (cx + 30, cy + 26)], fill=w, width=3)
    elif kind == "chart":
        for i, h in enumerate((15, 27, 21, 36)):
            bx = cx - 30 + i * 17
            draw.rectangle([bx, cy + 18 - h, bx + 11, cy + 18], fill=w)
        draw.line([(cx - 33, cy - 24), (cx + 30, cy - 30)], fill=(245, 197, 66),
                  width=5)
        draw.polygon([(cx + 30, cy - 30), (cx + 18, cy - 30), (cx + 30, cy - 18)],
                     fill=(245, 197, 66))
    elif kind == "globe":
        draw.ellipse([cx - 27, cy - 27, cx + 27, cy + 27], outline=w, width=5)
        draw.ellipse([cx - 12, cy - 27, cx + 12, cy + 27], outline=w, width=3)
        draw.line([(cx - 27, cy), (cx + 27, cy)], fill=w, width=3)
        draw.arc([cx - 27, cy - 14, cx + 27, cy + 14], 200, 340, fill=w, width=3)
        draw.arc([cx - 27, cy - 14, cx + 27, cy + 14], 20, 160, fill=w, width=3)
    elif kind == "tank":
        draw.rectangle([cx - 30, cy - 12, cx + 24, cy + 9], fill=w)
        draw.rectangle([cx - 12, cy - 24, cx + 12, cy - 12], fill=w)
        draw.line([(cx + 12, cy - 20), (cx + 33, cy - 20)], fill=w, width=5)
        for dx in (-21, -6, 9, 24):
            draw.ellipse([cx + dx - 6, cy + 12, cx + dx + 6, cy + 24], fill=w)
    elif kind == "flame":
        draw.polygon([(cx, cy - 30), (cx + 12, cy - 9), (cx + 24, cy + 3),
                      (cx + 18, cy + 24), (cx - 18, cy + 24), (cx - 24, cy + 3),
                      (cx - 12, cy - 9)], fill=w)
        draw.ellipse([cx - 9, cy + 3, cx + 9, cy + 21], fill=color)


def draw_summit_panel(draw, box):
    """Geometric scene: three leaders seated around a round table."""
    x0, y0, x1, y1 = box
    sky = (203, 220, 238)
    floor = (226, 214, 188)
    draw.rectangle(box, fill=sky)
    # sun and skyline
    draw.ellipse([x1 - 87, y0 + 18, x1 - 36, y0 + 69], fill=(245, 197, 66))
    for bx, bh in ((x0 + 21, 51), (x0 + 66, 78), (x0 + 117, 42)):
        draw.rectangle([bx, y0 + 177 - bh, bx + 36, y0 + 177], fill=(168, 186, 205))
    draw.rectangle([x0, y0 + 177, x1, y1], fill=floor)
    # round table
    tx, ty = (x0 + x1) // 2, y0 + 252
    draw.ellipse([tx - 144, ty - 27, tx + 144, ty + 27], fill=(122, 72, 44))
    draw.ellipse([tx - 144, ty - 27, tx + 144, ty + 27], outline=(90, 52, 30),
                 width=3)
    draw.rectangle([tx - 15, ty + 18, tx + 15, y1 - 12], fill=(90, 52, 30))
    # three seated figures: head + shoulders, in three colours
    figures = [
        (tx - 111, (178, 34, 22)),   # left
        (tx, (26, 40, 72)),          # centre
        (tx + 111, (15, 118, 110)),  # right
    ]
    for fx, col in figures:
        draw.ellipse([fx - 23, y0 + 78, fx + 23, y0 + 123], fill=(232, 196, 160))
        draw.pieslice([fx - 23, y0 + 78, fx + 23, y0 + 123], 180, 360, fill=(60, 60, 60))
        draw.polygon([(fx - 39, y0 + 192), (fx - 21, y0 + 129), (fx + 21, y0 + 129),
                      (fx + 39, y0 + 192)], fill=col)
        draw.polygon([(fx - 9, y0 + 132), (fx, y0 + 150), (fx + 9, y0 + 132)],
                     fill=(255, 255, 255))
    # small flags on the table
    for fx, col in ((tx - 51, (178, 34, 22)), (tx + 33, (26, 40, 72))):
        draw.line([(fx, ty - 51), (fx, ty - 18)], fill=(60, 60, 60), width=3)
        draw.polygon([(fx, ty - 51), (fx + 24, ty - 44), (fx, ty - 36)], fill=col)
    # caption strip
    draw.rectangle([x0, y1 - 39, x1, y1], fill=(24, 24, 28))
    draw.text((x0 + 15, y1 - 32), "SHENZHEN · THE FIRST TRILATERAL SUMMIT",
              font=load("sans_b", 18), fill=(255, 255, 255))


# ------------------------------------------------------------------ build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 42
    CW = W - 2 * M

    # outer frame
    d.rectangle([15, 15, W - 16, H - 16], outline=INK, width=3)

    # ---- masthead
    y = 39
    spaced(d, (M, y), "WORLD NEWS  ·  ONE DAY IN ONE IMAGE",
           load("sans_b", 23), RED, gap=5)
    y += 45
    d.text((M, y), "THURSDAY, 19 NOVEMBER 2026", font=load("serif_b", 75),
           fill=NAVY)
    y += 102
    d.text((M, y), "Seven stories that defined the day — verified against "
                   "independent reporting.",
           font=load("sans", 26), fill=GRAY)
    y += 42
    d.line([(M, y), (W - M, y)], fill=INK, width=5)
    d.line([(M, y + 9), (W - M, y + 9)], fill=INK, width=2)

    # ---- lead story
    ly, lh = 252, 354
    d.text((M, ly), LEAD["kicker"], font=load("sans_b", 21), fill=RED)
    hf = headline_font(d, LEAD["headline2"], [60, 57, 54], 900)
    d.text((M, ly + 36), LEAD["headline"], font=hf, fill=INK)
    d.text((M, ly + 36 + 69), LEAD["headline2"], font=hf, fill=INK)
    s_lines = wrap_text(d, LEAD["summary"], load("sans", 27), 900)
    sy = ly + 198
    for ln in s_lines:
        d.text((M, sy), ln, font=load("sans", 27), fill=INK)
        sy += 36
    d.text((M, ly + lh - 33), LEAD["source"], font=load("sans_b", 20), fill=GRAY)
    draw_summit_panel(d, (984, ly, W - M, ly + lh))

    # ---- divider
    dy = ly + lh + 21
    d.line([(M, dy), (W - M, dy)], fill=RULE, width=3)

    # ---- grid of six cards
    gy = dy + 24
    card_w, card_h, gap = 714, 234, 18
    for i, c in enumerate(CARDS):
        row, col = divmod(i, 2)
        x = M + col * (card_w + gap)
        yy = gy + row * (card_h + gap)
        d.rounded_rectangle((x, yy, x + card_w, yy + card_h), radius=12,
                            fill=CARD, outline=RULE, width=2)
        d.rectangle([x + 12, yy, x + card_w - 12, yy + 8], fill=c["color"])
        draw_glyph(d, c["icon"], (x + 21, yy + 24, x + 105, yy + 108),
                   c["color"])
        d.text((x + 123, yy + 24), c["kicker"], font=load("sans_b", 18),
               fill=c["color"])
        hf = headline_font(d, c["headline"], [32, 30, 29, 27, 26],
                           card_w - 144)
        d.text((x + 123, yy + 51), c["headline"], font=hf, fill=INK)
        sf = summary_font(d, c["summary"], [21, 20], card_w - 42, 3)
        s_lines = wrap_text(d, c["summary"], sf, card_w - 42)
        syy = yy + 117
        for ln in s_lines[:3]:
            d.text((x + 21, syy), ln, font=sf, fill=INK)
            syy += 27
        d.text((x + 21, yy + card_h - 27), c["source"],
               font=load("sans_b", 17), fill=GRAY)

    # ---- footer
    fy = gy + 3 * card_h + 2 * gap + 21
    d.line([(M, fy), (W - M, fy)], fill=INK, width=3)
    f1 = ("Sources: Reuters · Wall Street Journal · CNN · Associated Press · "
          "Al Jazeera · Agence France-Presse · The Business Standard")
    f2 = ("Every fact checked against at least two independent reports. "
          "News of Thursday, 19 November 2026.")
    d.text((M, fy + 15), f1, font=load("sans", 20), fill=INK)
    d.text((M, fy + 45), f2, font=load("sans", 20), fill=GRAY)
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    im = build()
    im.save(out, optimize=True)
    print(f"saved {out}: {im.size} {os.path.getsize(out)} bytes")
