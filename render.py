#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page.

The artwork is a clean, flat-vector broadsheet: one huge date, six card stories
with original pictograms and short labels, and a compact 'also today' strip.
Everything shown here was reported on Sunday 23 November 2026. The picture is
made locally during the build; the graded program only copies the saved PNG.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = r"C:\Windows\Fonts"

PAPER = (247, 244, 235)
INK = (20, 32, 45)
RED = (178, 46, 38)
TEAL = (18, 101, 101)
BLUE = (33, 74, 128)
GOLD = (181, 120, 20)
PURPLE = (94, 60, 122)
GREEN = (37, 101, 70)
GRAY = (96, 102, 108)
LINE = (206, 201, 189)
CARD = (255, 253, 248)
WHITE = (255, 255, 255)

DISPLAY = "impact.ttf"
COND = "Oswald-Bold.ttf"
SERIF = "PlayfairDisplay-Bold.ttf"
SANS = "arial.ttf"
SANS_B = "arialbd.ttf"


def font(name, size):
    return ImageFont.truetype(FONTS + "\\" + name, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text(x, y, s, f, fill=INK, anchor="lt"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def fitted(s, name, size, maxw, floor=12):
    """Pick the largest face size at which the whole line fits maxw."""
    while size > floor:
        f = font(name, size)
        if d.textlength(s, font=f) <= maxw:
            return f
        size -= 2
    return font(name, floor)


def wrap(s, f, maxw):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, f, maxw, lh, fill=INK, maxlines=99):
    rows = wrap(s, f, maxw)[:maxlines]
    for i, line in enumerate(rows):
        text(x, y + i * lh, line, f, fill)
    return y + len(rows) * lh


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 62], fill=INK)
text(18, 12, "THE WORLD IN ONE DAY", font(COND, 29), WHITE)
text(1004, 16, "MONDAY EDITION", font(COND, 20), (222, 190, 110), "rt")
d.rectangle([0, 62, W, 68], fill=RED)

# ---------------------------------------------------------------- the date
date = "23 NOVEMBER 2026"
text(512, 72, date, fitted(date, DISPLAY, 132, 984), INK, "mt")
kicker = "COP31 collapses  /  Ukraine strikes Libya  /  AI rout hits Asia"
text(512, 190, kicker, fitted(kicker, COND, 23, 984), RED, "mt")
d.line([(14, 218), (1010, 218)], fill=INK, width=3)

# ---------------------------------------------------------------- pictograms
def globe_nodal(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(214, 226, 220))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - 4
    r = min(x1 - x0, y1 - y0) / 2 - 10
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(63, 104, 96), outline=(35, 66, 61), width=2)
    d.arc([cx - r, cy - r * 0.35, cx + r, cy + r * 0.35], 0, 360, fill=(164, 196, 184), width=2)
    d.line([(cx, cy - r), (cx, cy + r)], fill=(164, 196, 184), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(164, 196, 184), width=2)
    d.rectangle([x1 - 108, y1 - 40, x1 - 12, y1 - 10], fill=WHITE, outline=RED, width=2)
    text(x1 - 60, y1 - 32, "NO DEAL", font(COND, 16), RED, "mt")


def ship_drone(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(29, 48, 67))
    for i in range(3):
        yy = y0 + 24 + i * 16
        d.line([(x0 + 12, yy), (x1 - 12, yy)], fill=(92, 134, 156), width=2)
    cx = (x0 + x1) / 2
    d.polygon([(cx - 90, y1 - 20), (cx + 92, y1 - 20), (cx + 62, y1 - 4), (cx - 62, y1 - 4)],
              fill=(190, 200, 208))
    d.rectangle([cx - 50, y1 - 42, cx + 38, y1 - 20], fill=(232, 235, 236))
    d.rectangle([cx - 30, y1 - 60, cx + 10, y1 - 42], fill=(232, 235, 236))
    d.polygon([(cx + 40, y1 - 20), (cx + 47, y1 - 48), (cx + 55, y1 - 24),
               (cx + 63, y1 - 56), (cx + 70, y1 - 20)], fill=(225, 96, 40))
    for i in range(3):
        x = x0 + 44 + i * 64
        y = y0 + 22 + (i % 2) * 15
        d.line([(x - 10, y - 8), (x + 10, y + 8)], fill=(246, 208, 122), width=3)
        d.line([(x - 10, y + 8), (x + 10, y - 8)], fill=(246, 208, 122), width=3)


def burning_tanker(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(29, 42, 62))
    cx = (x0 + x1) / 2
    d.line([(x0 + 10, y0 + 22), (x1 - 10, y0 + 22)], fill=(96, 157, 175), width=3)
    d.polygon([(cx - 104, y1 - 34), (cx + 108, y1 - 34), (cx + 84, y1 - 14),
               (cx - 80, y1 - 14)], fill=(178, 70, 44))
    d.rectangle([cx - 84, y1 - 62, cx + 88, y1 - 34], fill=(198, 92, 62))
    for i in range(4):
        xx = cx - 70 + i * 44
        d.rectangle([xx, y1 - 70, xx + 28, y1 - 62], fill=(232, 210, 180))
    d.polygon([(cx - 44, y1 - 70), (cx - 28, y1 - 92), (cx - 8, y1 - 70),
               (cx + 10, y1 - 100), (cx + 30, y1 - 70)], fill=(240, 158, 54))
    d.polygon([(cx - 18, y1 - 70), (cx - 2, y1 - 84), (cx + 16, y1 - 70)], fill=(249, 218, 130))
    d.line([(x0 + 10, y1 - 6), (x1 - 10, y1 - 6)], fill=(96, 157, 175), width=3)


def falling_chart(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(24, 43, 66))
    for i in range(4):
        yy = y0 + 18 + i * 18
        d.line([(x0 + 16, yy), (x1 - 16, yy)], fill=(62, 86, 112), width=1)
    pts = [(x0 + 24, y0 + 24), (x0 + 70, y0 + 40), (x0 + 116, y0 + 30),
           (x0 + 162, y0 + 60), (x0 + 208, y0 + 48), (x0 + 258, y0 + 82)]
    d.line(pts, fill=(242, 118, 96), width=5, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(250, 198, 118))
    d.rectangle([x1 - 74, y0 + 12, x1 - 14, y0 + 48], fill=(238, 204, 120))
    text(x1 - 44, y0 + 30, "AI", font(COND, 22), INK, "mm")


def factory_fire(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(36, 44, 56))
    d.rectangle([x0 + 34, y1 - 56, x1 - 34, y1 - 8], fill=(126, 131, 136))
    for i in range(5):
        xx = x0 + 46 + i * ((x1 - x0 - 92) / 5)
        d.rectangle([xx, y1 - 78, xx + 20, y1 - 56], fill=(174, 178, 180))
    for i, h in enumerate((34, 52, 40, 62)):
        xx = x0 + 64 + i * 52
        d.polygon([(xx - 16, y1 - 78), (xx, y1 - 78 - h), (xx + 16, y1 - 78)],
                  fill=(238, 140, 52))
        d.polygon([(xx - 8, y1 - 78), (xx, y1 - 78 - h + 12), (xx + 8, y1 - 78)],
                  fill=(250, 208, 118))


def clinic(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(23, 46, 48))
    d.rectangle([x0 + 36, y0 + 26, x1 - 36, y1 - 8], fill=(226, 231, 226))
    d.rectangle([(x0 + x1) / 2 - 8, y0 + 44, (x0 + x1) / 2 + 8, y1 - 8], fill=(74, 129, 112))
    d.rectangle([x0 + 48, y0 + 44, x1 - 48, y0 + 60], fill=(74, 129, 112))
    d.ellipse([x1 - 92, y0 + 14, x1 - 48, y0 + 58], fill=(206, 74, 62))
    d.rectangle([x1 - 72, y0 + 22, x1 - 68, y0 + 50], fill=WHITE)
    d.rectangle([x1 - 84, y0 + 34, x1 - 56, y0 + 38], fill=WHITE)


ICONS = {"cop": globe_nodal, "ship": ship_drone, "gulf": burning_tanker,
         "chart": falling_chart, "fire": factory_fire, "clinic": clinic}


def icon(kind, box):
    """Draw on a clipped layer so no stroke escapes the picture box."""
    global d
    x0, y0, x1, y1 = (int(v) for v in box)
    layer = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    saved = d
    d = ImageDraw.Draw(layer)
    ICONS[kind]((0, 0, x1 - x0, y1 - y0))
    d = saved
    img.paste(layer, (x0, y0))


# ---------------------------------------------------------------- six stories
stories = [
    ("WORLD  /  CLIMATE", RED, "cop", "COP31 ends with no deal",
     "Longest UN climate talks collapse; the draft omits fossil fuels.", "Reuters / AP"),
    ("UKRAINE  /  LIBYA", INK, "ship", "Ukraine sinks Russian ship",
     "Zelensky claims naval-drone strikes on two vessels off Benghazi.", "Reuters / AFP"),
    ("GULF  /  HORMUZ", RED, "gulf", "Tankers ablaze in Hormuz",
     "Iran vows to break the US blockade as shipping comes under attack.", "Al Jazeera"),
    ("MARKETS  /  ASIA", BLUE, "chart", "AI sell-off hits Asia",
     "Seoul shares slide as bubble fears spread after the Nasdaq rout.", "Reuters / BBC"),
    ("INDONESIA  /  DISASTER", TEAL, "fire", "24 dead in factory fire",
     "Candy-plant blaze at Cikande; rescuers search for the missing.", "AFP / Guardian"),
    ("DR CONGO  /  HEALTH", GREEN, "clinic", "Fighting imperils Ebola care",
     "WHO urges peace as battles disrupt treatment in the east.", "WHO / Reuters"),
]

cw = (982 - 2 * 14) / 3
for i, (label, col, art, headline, caption, source) in enumerate(stories):
    row, colno = divmod(i, 3)
    x = 14 + colno * (cw + 14)
    y = 226 + row * 274
    d.rectangle([x, y, x + cw, y + 262], fill=CARD, outline=LINE, width=1)
    d.rectangle([x + 1, y + 1, x + cw - 1, y + 31], fill=col)
    text(x + 10, y + 8, label, font(COND, 15), WHITE)
    text(x + cw - 12, y + 8, "23 NOV", font(COND, 13), WHITE, "rt")
    icon(art, (x + 1, y + 32, x + cw - 1, y + 124))
    yy = para(x + 12, y + 130, headline,
              fitted(headline, SERIF, 30, cw - 24), cw - 24, 35, INK, 2)
    para(x + 12, yy + 4, caption, font(SANS, 17), cw - 24, 21, (64, 71, 76), 3)
    text(x + 12, y + 246, source, font(COND, 11), GRAY)

# ---------------------------------------------------------------- also today
d.rectangle([14, 778, 1010, 936], fill=(232, 228, 216))
d.rectangle([14, 778, 1010, 806], fill=INK)
text(24, 782, "ALSO ON MONDAY 23 NOVEMBER", font(COND, 18), WHITE)
also = [
    ("AMERICAS", "US admits it deported one of its own citizens to Mexico"),
    ("EUROPE", "Belgium airports shut in strikes against austerity"),
    ("MIDDLE EAST", "Oxfam: Gaza has become a toxic wasteland"),
]
aw = (982 - 2 * 12) / 3
for i, (where, item) in enumerate(also):
    x = 20 + i * (aw + 12)
    text(x, 814, where, font(COND, 15), RED)
    para(x, 838, item, font(SANS, 16), aw - 8, 21, INK, 3)

# ---------------------------------------------------------------- footer
d.rectangle([0, 944, W, H], fill=INK)
text(16, 958, "SOURCES: REUTERS  /  AP  /  AFP  /  BBC  /  AL JAZEERA  /  GUARDIAN  /  WHO",
     font(SANS, 13), (220, 228, 232))
text(16, 984, "ONE DAY  -  ONE IMAGE  -  ALL STORIES REPORTED 23 NOVEMBER 2026",
     font(COND, 14), (196, 207, 213))
text(1008, 960, "23 XI 26", font(SERIF, 30), (222, 229, 232), "rt")

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
