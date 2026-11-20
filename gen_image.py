#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: one 1024x1024 newspaper front page
summing up the world news of Thursday 19 November 2026.

Deterministic: no randomness, no timestamps, no network, no AI image
generator, no copyrighted images. Everything is drawn with PIL from the
verified facts in RESEARCH.md. Run: python3 gen_image.py [out.png]
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
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


def spaced(draw, xy, text, fnt, fill, gap=3):
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
    draw.rounded_rectangle(box, radius=9, fill=color)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w = (255, 255, 255)
    if kind == "scales":
        draw.line([(cx, cy - 16), (cx, cy + 16)], fill=w, width=3)
        draw.line([(cx - 16, cy - 10), (cx + 16, cy - 10)], fill=w, width=3)
        for dx in (-16, 16):
            draw.line([(cx + dx, cy - 10), (cx + dx - 7, cy + 2)], fill=w, width=2)
            draw.line([(cx + dx, cy - 10), (cx + dx + 7, cy + 2)], fill=w, width=2)
            draw.arc([cx + dx - 7, cy - 2, cx + dx + 7, cy + 10], 0, 180,
                     fill=w, width=2)
        draw.line([(cx - 12, cy + 16), (cx + 12, cy + 16)], fill=w, width=3)
    elif kind == "bridge":
        draw.rectangle([cx - 20, cy - 16, cx - 14, cy + 12], fill=w)
        draw.rectangle([cx + 14, cy - 16, cx + 20, cy + 12], fill=w)
        draw.line([(cx - 17, cy - 16), (cx, cy + 2)], fill=w, width=2)
        draw.line([(cx + 17, cy - 16), (cx, cy + 2)], fill=w, width=2)
        draw.rectangle([cx - 22, cy + 2, cx - 6, cy + 8], fill=w)
        draw.rectangle([cx + 6, cy + 2, cx + 22, cy + 8], fill=w)
        draw.line([(cx - 20, cy + 17), (cx + 20, cy + 17)], fill=w, width=2)
    elif kind == "chart":
        for i, h in enumerate((10, 18, 14, 24)):
            bx = cx - 20 + i * 11
            draw.rectangle([bx, cy + 12 - h, bx + 7, cy + 12], fill=w)
        draw.line([(cx - 22, cy - 16), (cx + 20, cy - 20)], fill=(245, 197, 66),
                  width=3)
        draw.polygon([(cx + 20, cy - 20), (cx + 12, cy - 20), (cx + 20, cy - 12)],
                     fill=(245, 197, 66))
    elif kind == "globe":
        draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline=w, width=3)
        draw.ellipse([cx - 8, cy - 18, cx + 8, cy + 18], outline=w, width=2)
        draw.line([(cx - 18, cy), (cx + 18, cy)], fill=w, width=2)
        draw.arc([cx - 18, cy - 9, cx + 18, cy + 9], 200, 340, fill=w, width=2)
        draw.arc([cx - 18, cy - 9, cx + 18, cy + 9], 20, 160, fill=w, width=2)
    elif kind == "tank":
        draw.rectangle([cx - 20, cy - 8, cx + 16, cy + 6], fill=w)
        draw.rectangle([cx - 8, cy - 16, cx + 8, cy - 8], fill=w)
        draw.line([(cx + 8, cy - 13), (cx + 22, cy - 13)], fill=w, width=3)
        for dx in (-14, -4, 6, 16):
            draw.ellipse([cx + dx - 4, cy + 8, cx + dx + 4, cy + 16], fill=w)
    elif kind == "flame":
        draw.polygon([(cx, cy - 20), (cx + 8, cy - 6), (cx + 16, cy + 2),
                      (cx + 12, cy + 16), (cx - 12, cy + 16), (cx - 16, cy + 2),
                      (cx - 8, cy - 6)], fill=w)
        draw.ellipse([cx - 6, cy + 2, cx + 6, cy + 14], fill=color)


def draw_summit_panel(draw, box):
    """Geometric scene: three leaders seated around a round table."""
    x0, y0, x1, y1 = box
    sky = (203, 220, 238)
    floor = (226, 214, 188)
    draw.rectangle(box, fill=sky)
    # sun and skyline
    draw.ellipse([x1 - 58, y0 + 12, x1 - 24, y0 + 46], fill=(245, 197, 66))
    for bx, bh in ((x0 + 14, 34), (x0 + 44, 52), (x0 + 78, 28)):
        draw.rectangle([bx, y0 + 118 - bh, bx + 24, y0 + 118], fill=(168, 186, 205))
    draw.rectangle([x0, y0 + 118, x1, y1], fill=floor)
    # round table
    tx, ty = (x0 + x1) // 2, y0 + 168
    draw.ellipse([tx - 96, ty - 18, tx + 96, ty + 18], fill=(122, 72, 44))
    draw.ellipse([tx - 96, ty - 18, tx + 96, ty + 18], outline=(90, 52, 30),
                 width=2)
    draw.rectangle([tx - 10, ty + 12, tx + 10, y1 - 8], fill=(90, 52, 30))
    # three seated figures: head + shoulders, in three colours
    figures = [
        (tx - 74, (178, 34, 22)),   # left
        (tx, (26, 40, 72)),         # centre
        (tx + 74, (15, 118, 110)),  # right
    ]
    for fx, col in figures:
        draw.ellipse([fx - 15, y0 + 52, fx + 15, y0 + 82], fill=(232, 196, 160))
        draw.pieslice([fx - 15, y0 + 52, fx + 15, y0 + 82], 180, 360, fill=(60, 60, 60))
        draw.polygon([(fx - 26, y0 + 128), (fx - 14, y0 + 86), (fx + 14, y0 + 86),
                      (fx + 26, y0 + 128)], fill=col)
        draw.polygon([(fx - 6, y0 + 88), (fx, y0 + 100), (fx + 6, y0 + 88)],
                     fill=(255, 255, 255))
    # small flags on the table
    for fx, col in ((tx - 34, (178, 34, 22)), (tx + 22, (26, 40, 72))):
        draw.line([(fx, ty - 34), (fx, ty - 12)], fill=(60, 60, 60), width=2)
        draw.polygon([(fx, ty - 34), (fx + 16, ty - 29), (fx, ty - 24)], fill=col)
    # caption strip
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(24, 24, 28))
    draw.text((x0 + 10, y1 - 21), "SHENZHEN · THE FIRST TRILATERAL SUMMIT",
              font=load("sans_b", 12), fill=(255, 255, 255))


# ------------------------------------------------------------------ build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    CW = W - 2 * M

    # outer frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # ---- masthead
    y = 26
    spaced(d, (M, y), "WORLD NEWS  ·  ONE DAY IN ONE IMAGE",
           load("sans_b", 15), RED, gap=3)
    y += 30
    d.text((M, y), "THURSDAY, 19 NOVEMBER 2026", font=load("serif_b", 50),
           fill=NAVY)
    y += 68
    d.text((M, y), "Seven stories that defined the day — verified against "
                   "independent reporting.",
           font=load("sans", 17), fill=GRAY)
    y += 28
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    d.line([(M, y + 6), (W - M, y + 6)], fill=INK, width=1)

    # ---- lead story
    ly, lh = 168, 236
    d.text((M, ly), LEAD["kicker"], font=load("sans_b", 14), fill=RED)
    hf = headline_font(d, LEAD["headline2"], [40, 38, 36], 600)
    d.text((M, ly + 24), LEAD["headline"], font=hf, fill=INK)
    d.text((M, ly + 24 + 46), LEAD["headline2"], font=hf, fill=INK)
    s_lines = wrap_text(d, LEAD["summary"], load("sans", 18), 600)
    sy = ly + 132
    for ln in s_lines:
        d.text((M, sy), ln, font=load("sans", 18), fill=INK)
        sy += 24
    d.text((M, ly + lh - 22), LEAD["source"], font=load("sans_b", 13), fill=GRAY)
    draw_summit_panel(d, (656, ly, W - M, ly + lh))

    # ---- divider
    dy = ly + lh + 14
    d.line([(M, dy), (W - M, dy)], fill=RULE, width=2)

    # ---- grid of six cards
    gy = dy + 16
    card_w, card_h, gap = 476, 156, 12
    for i, c in enumerate(CARDS):
        row, col = divmod(i, 2)
        x = M + col * (card_w + gap)
        yy = gy + row * (card_h + gap)
        d.rounded_rectangle((x, yy, x + card_w, yy + card_h), radius=8,
                            fill=CARD, outline=RULE, width=1)
        d.rectangle([x + 8, yy, x + card_w - 8, yy + 5], fill=c["color"])
        draw_glyph(d, c["icon"], (x + 14, yy + 16, x + 70, yy + 72),
                   c["color"])
        d.text((x + 82, yy + 16), c["kicker"], font=load("sans_b", 12),
               fill=c["color"])
        hf = headline_font(d, c["headline"], [21, 20, 19, 18, 17],
                           card_w - 96)
        d.text((x + 82, yy + 34), c["headline"], font=hf, fill=INK)
        sf = summary_font(d, c["summary"], [14, 13], card_w - 28, 3)
        s_lines = wrap_text(d, c["summary"], sf, card_w - 28)
        syy = yy + 78
        for ln in s_lines[:3]:
            d.text((x + 14, syy), ln, font=sf, fill=INK)
            syy += 18
        d.text((x + 14, yy + card_h - 18), c["source"],
               font=load("sans_b", 11), fill=GRAY)

    # ---- footer
    fy = gy + 3 * card_h + 2 * gap + 14
    d.line([(M, fy), (W - M, fy)], fill=INK, width=2)
    f1 = ("Sources: Reuters · Wall Street Journal · CNN · Associated Press · "
          "Al Jazeera · Agence France-Presse · The Business Standard")
    f2 = ("Every fact checked against at least two independent reports. "
          "News of Thursday, 19 November 2026.")
    d.text((M, fy + 10), f1, font=load("sans", 13), fill=INK)
    d.text((M, fy + 30), f2, font=load("sans", 13), fill=GRAY)
    return img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    im = build()
    im.save(out, optimize=True)
    print(f"saved {out}: {im.size} {os.path.getsize(out)} bytes")
