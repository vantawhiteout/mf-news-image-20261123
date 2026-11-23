#!/usr/bin/env python3
"""Compose a one-page picture of Monday 23 November 2026's world news.

The sheet is built from scratch with flat shapes and hand-picked type: a very
large date, six regional story panels with small original pictograms, and a
short extra-news band. Only the standard Pillow toolkit is used, locally, while
the entry is being developed. The graded program merely publishes the PNG.
"""

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
TYPE_DIR = r"C:\Windows\Fonts"

CREAM = (247, 244, 235)
CHARCOAL = (20, 32, 45)
CRIMSON = (178, 46, 38)
OCEAN = (33, 74, 128)
FOREST = (37, 101, 70)
LAGOON = (18, 101, 101)
ASH = (96, 102, 108)
RULE = (206, 201, 189)
WHITE = (255, 255, 255)
PANEL = (255, 253, 248)


def face(filename, pixels):
    return ImageFont.truetype(TYPE_DIR + "\\" + filename, pixels)


HEAVY = "impact.ttf"
CAPS = "Oswald-Bold.ttf"
BOOK = "PlayfairDisplay-Bold.ttf"
BODY = "arial.ttf"


class Sheet:
    """A tiny drawing surface with clipping for the little illustrations."""

    def __init__(self):
        self.canvas = Image.new("RGB", (SIDE, SIDE), CREAM)
        self.pen = ImageDraw.Draw(self.canvas)

    def say(self, x, y, words, font, color=CHARCOAL, anchor="lt"):
        self.pen.text((x, y), words, font=font, fill=color, anchor=anchor)

    def fill(self, bounds, color, border=None, thickness=1):
        self.pen.rectangle(bounds, fill=color, outline=border, width=thickness)

    def rule(self, start, end, color, thickness=2):
        self.pen.line([start, end], fill=color, width=thickness)

    def shape(self, points, color):
        self.pen.polygon(points, fill=color)

    def disc(self, bounds, color, edge=None, width=1):
        self.pen.ellipse(bounds, fill=color, outline=edge, width=width)

    def fit(self, words, filename, pixels, room):
        n = pixels
        while n > 12:
            font = face(filename, n)
            if self.pen.textlength(words, font=font) <= room:
                return font
            n -= 2
        return face(filename, 12)

    def split(self, words, font, room):
        rows, current = [], ""
        for word in words.split():
            trial = (current + " " + word).strip()
            if self.pen.textlength(trial, font=font) <= room or not current:
                current = trial
            else:
                rows.append(current)
                current = word
        if current:
            rows.append(current)
        return rows

    def block(self, x, y, words, font, room, gap, color=CHARCOAL, cap=99):
        rows = self.split(words, font, room)[:cap]
        for k, row in enumerate(rows):
            self.say(x, y + k * gap, row, font, color)
        return y + len(rows) * gap

    def panel(self, painter, bounds):
        l, t, r, b = (int(v) for v in bounds)
        tile = Image.new("RGB", (r - l, b - t), CREAM)
        previous = self.pen
        self.pen = ImageDraw.Draw(tile)
        painter(0, 0, r - l, b - t)
        self.pen = previous
        self.canvas.paste(tile, (l, t))

    # -------------------------------------------------- six original icons
    def icon_climate(self, l, t, r, b):
        self.fill((l, t, r, b), (214, 226, 220))
        cx, cy = (l + r) / 2, (t + b) / 2 - 4
        rad = min(r - l, b - t) / 2 - 10
        self.disc((cx-rad, cy-rad, cx+rad, cy+rad), (63,104,96), (35,66,61), 2)
        self.pen.arc((cx-rad, cy-rad*.35, cx+rad, cy+rad*.35), 0, 360,
                     fill=(164,196,184), width=2)
        self.rule((cx, cy-rad), (cx, cy+rad), (164,196,184), 2)
        self.rule((cx-rad, cy), (cx+rad, cy), (164,196,184), 2)
        self.fill((r-108, b-40, r-12, b-10), WHITE, CRIMSON, 2)
        self.say(r-60, b-32, "NO DEAL", face(CAPS,16), CRIMSON, "mt")

    def icon_ship(self, l, t, r, b):
        self.fill((l, t, r, b), (29,48,67))
        for k in range(3):
            y = t + 24 + k*16
            self.rule((l+12, y), (r-12, y), (92,134,156), 2)
        cx = (l+r)/2
        self.shape([(cx-90,b-20),(cx+92,b-20),(cx+62,b-4),(cx-62,b-4)], (190,200,208))
        self.fill((cx-50,b-42,cx+38,b-20), (232,235,236))
        self.fill((cx-30,b-60,cx+10,b-42), (232,235,236))
        self.shape([(cx+40,b-20),(cx+47,b-48),(cx+55,b-24),
                    (cx+63,b-56),(cx+70,b-20)], (225,96,40))
        for k in range(3):
            x, y = l+44+k*64, t+22+(k % 2)*15
            self.rule((x-10,y-8),(x+10,y+8), (246,208,122), 3)
            self.rule((x-10,y+8),(x+10,y-8), (246,208,122), 3)

    def icon_tanker(self, l, t, r, b):
        self.fill((l, t, r, b), (29,42,62))
        self.rule((l+10,t+22),(r-10,t+22), (96,157,175), 3)
        cx = (l+r)/2
        self.shape([(cx-104,b-34),(cx+108,b-34),(cx+84,b-14),(cx-80,b-14)], (178,70,44))
        self.fill((cx-84,b-62,cx+88,b-34), (198,92,62))
        for k in range(4):
            x = cx-70+k*44
            self.fill((x,b-70,x+28,b-62), (232,210,180))
        self.shape([(cx-44,b-70),(cx-28,b-92),(cx-8,b-70),
                    (cx+10,b-100),(cx+30,b-70)], (240,158,54))
        self.shape([(cx-18,b-70),(cx-2,b-84),(cx+16,b-70)], (249,218,130))
        self.rule((l+10,b-6),(r-10,b-6), (96,157,175), 3)

    def icon_market(self, l, t, r, b):
        self.fill((l, t, r, b), (24,43,66))
        for k in range(4):
            y = t+18+k*18
            self.rule((l+16,y),(r-16,y), (62,86,112), 1)
        dots = [(l+24,t+24),(l+70,t+40),(l+116,t+30),
                (l+162,t+60),(l+208,t+48),(l+258,t+82)]
        self.pen.line(dots, fill=(242,118,96), width=5, joint="curve")
        for px, py in dots:
            self.disc((px-4,py-4,px+4,py+4), (250,198,118))
        self.fill((r-74,t+12,r-14,t+48), (238,204,120))
        self.say(r-44,t+30,"AI",face(CAPS,22),CHARCOAL,"mm")

    def icon_factory(self, l, t, r, b):
        self.fill((l, t, r, b), (36,44,56))
        self.fill((l+34,b-56,r-34,b-8), (126,131,136))
        for k in range(5):
            x = l+46+k*((r-l-92)/5)
            self.fill((x,b-78,x+20,b-56), (174,178,180))
        for k, hgt in enumerate((34,52,40,62)):
            x = l+64+k*52
            self.shape([(x-16,b-78),(x,b-78-hgt),(x+16,b-78)], (238,140,52))
            self.shape([(x-8,b-78),(x,b-78-hgt+12),(x+8,b-78)], (250,208,118))

    def icon_clinic(self, l, t, r, b):
        self.fill((l, t, r, b), (23,46,48))
        self.fill((l+36,t+26,r-36,b-8), (226,231,226))
        self.fill(((l+r)/2-8,t+44,(l+r)/2+8,b-8), (74,129,112))
        self.fill((l+48,t+44,r-48,t+60), (74,129,112))
        self.disc((r-92,t+14,r-48,t+58), (206,74,62))
        self.fill((r-72,t+22,r-68,t+50), WHITE)
        self.fill((r-84,t+34,r-56,t+38), WHITE)

    def save(self, path):
        self.canvas.save(path, format="PNG", optimize=True)


sheet = Sheet()

# masthead and date -----------------------------------------------------------
sheet.fill((0,0,SIDE,62), CHARCOAL)
sheet.say(18,12,"THE WORLD IN ONE DAY", face(CAPS,29), WHITE)
sheet.say(1004,16,"MONDAY EDITION", face(CAPS,20), (222,190,110), "rt")
sheet.fill((0,62,SIDE,68), CRIMSON)
headline_date = "23 NOVEMBER 2026"
sheet.say(512,72,headline_date,
          sheet.fit(headline_date,HEAVY,132,984), CHARCOAL, "mt")
deck = "COP31 collapses  /  Ukraine strikes Libya  /  AI rout hits Asia"
sheet.say(512,190,deck, sheet.fit(deck,CAPS,23,984), CRIMSON, "mt")
sheet.rule((14,218),(1010,218), CHARCOAL, 3)

# the six main stories --------------------------------------------------------
stories = [
    dict(tag="WORLD  /  CLIMATE", tint=CRIMSON, art=Sheet.icon_climate,
         title="COP31 ends with no deal",
         note="Longest UN climate talks collapse; the draft omits fossil fuels.",
         credit="Reuters / AP"),
    dict(tag="UKRAINE  /  LIBYA", tint=CHARCOAL, art=Sheet.icon_ship,
         title="Ukraine sinks Russian ship",
         note="Zelensky claims naval-drone strikes on two vessels off Benghazi.",
         credit="Reuters / AFP"),
    dict(tag="GULF  /  HORMUZ", tint=CRIMSON, art=Sheet.icon_tanker,
         title="Tankers ablaze in Hormuz",
         note="Iran vows to break the US blockade as shipping comes under attack.",
         credit="Al Jazeera"),
    dict(tag="MARKETS  /  ASIA", tint=OCEAN, art=Sheet.icon_market,
         title="AI sell-off hits Asia",
         note="Seoul shares slide as bubble fears spread after the Nasdaq rout.",
         credit="Reuters / BBC"),
    dict(tag="INDONESIA  /  DISASTER", tint=LAGOON, art=Sheet.icon_factory,
         title="24 dead in factory fire",
         note="Candy-plant blaze at Cikande; rescuers search for the missing.",
         credit="AFP / Guardian"),
    dict(tag="DR CONGO  /  HEALTH", tint=FOREST, art=Sheet.icon_clinic,
         title="Fighting imperils Ebola care",
         note="WHO urges peace as battles disrupt treatment in the east.",
         credit="WHO / Reuters"),
]

width = (982 - 28) / 3
for index, story in enumerate(stories):
    row, col = divmod(index, 3)
    left = 14 + col * (width + 14)
    top = 226 + row * 274
    sheet.fill((left,top,left+width,top+262), PANEL, RULE, 1)
    sheet.fill((left+1,top+1,left+width-1,top+31), story["tint"])
    sheet.say(left+10,top+8,story["tag"], face(CAPS,15), WHITE)
    sheet.say(left+width-12,top+8,"23 NOV", face(CAPS,13), WHITE, "rt")
    sheet.panel(story["art"], (left+1,top+32,left+width-1,top+124))
    below = sheet.block(left+12, top+130, story["title"],
                        sheet.fit(story["title"],BOOK,30,width-24),
                        width-24, 35, CHARCOAL, 2)
    sheet.block(left+12, below+4, story["note"], face(BODY,17),
                width-24, 21, (64,71,76), 3)
    sheet.say(left+12,top+246,story["credit"], face(CAPS,11), ASH)

# smaller stories -------------------------------------------------------------
sheet.fill((14,778,1010,936), (232,228,216))
sheet.fill((14,778,1010,806), CHARCOAL)
sheet.say(24,782,"ALSO ON MONDAY 23 NOVEMBER", face(CAPS,18), WHITE)
extras = [
    ("AMERICAS", "US admits it deported one of its own citizens to Mexico"),
    ("EUROPE", "Belgium airports shut in strikes against austerity"),
    ("MIDDLE EAST", "Oxfam: Gaza has become a toxic wasteland"),
]
column = (982 - 24) / 3
for i, (place, item) in enumerate(extras):
    x = 20 + i*(column+12)
    sheet.say(x,814,place, face(CAPS,15), CRIMSON)
    sheet.block(x,838,item, face(BODY,16), column-8, 21, CHARCOAL, 3)

# footer ----------------------------------------------------------------------
sheet.fill((0,944,SIDE,SIDE), CHARCOAL)
sheet.say(16,958,"SOURCES: REUTERS  /  AP  /  AFP  /  BBC  /  AL JAZEERA  /  GUARDIAN  /  WHO",
          face(BODY,13), (220,228,232))
sheet.say(16,984,"ONE DAY  -  ONE IMAGE  -  ALL STORIES REPORTED 23 NOVEMBER 2026",
          face(CAPS,14), (196,207,213))
sheet.say(1008,960,"23 XI 26", face(BOOK,30), (222,229,232), "rt")

sheet.save("entry.png")
print("drew entry.png", sheet.canvas.size)
