#!/usr/bin/env python3
"""gen.py — draws entry.png: a broadsheet sports back page for
Tuesday 24 November 2026.

Pillow + Python standard library only. System fonts only, no network,
no downloaded images. Fully deterministic: no randomness, no clock —
repeat runs are byte-identical.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 24, 32)
DARKRED = (120, 14, 22)
GREY = (84, 80, 72)
RULE = (30, 30, 30)
BOX = (255, 252, 244)
GOLD = (196, 148, 32)
PITCH = (36, 110, 52)
PITCH2 = (44, 128, 62)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def centre(d, cx, y, text, font, fill=INK):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)
    return y + font.size


def left(d, x, y, text, font, fill=INK):
    d.text((x, y), text, font=font, fill=fill)
    return y + font.size


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, maxw, fill=INK, leading=6):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += font.size + leading
    return y


def ball(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 250, 248),
              outline=INK, width=3)
    d.regular_polygon((cx, cy, r * 0.42), 5, fill=INK)
    for a in range(0, 360, 72):
        import math
        x2 = cx + (r * 0.95) * math.cos(math.radians(a - 90))
        y2 = cy + (r * 0.95) * math.sin(math.radians(a - 90))
        x1 = cx + (r * 0.42) * math.cos(math.radians(a - 90))
        y1 = cy + (r * 0.42) * math.sin(math.radians(a - 90))
        d.line([x1, y1, x2, y2], fill=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 118], fill=INK)
    centre(d, W // 2, 16, "THE BACK PAGE", F(SERIF_B, 62), fill=PAPER)
    centre(d, W // 2, 88, "TUESDAY 24 NOVEMBER 2026  •  FOOTBALL SPECIAL",
           F(SANS_B, 19), fill=(232, 200, 120))
    d.rectangle([0, 118, W, 124], fill=RED)

    # ---------- kicker ----------
    centre(d, W // 2, 138, "CHAMPIONS LEAGUE RETURNS TONIGHT",
           F(SANS_B, 34), fill=RED)
    centre(d, W // 2, 178, "Matchday 5 — nine games across Europe",
           F(SERIF, 21), fill=GREY)
    d.line([36, 214, W - 36, 214], fill=RULE, width=2)

    # ---------- lead story: Brentford 4-0 Everton ----------
    lx = 36
    left(d, lx, 228, "MONDAY NIGHT FOOTBALL", F(SANS_B, 17), fill=DARKRED)
    left(d, lx, 254, "BEES RUN RIOT", F(SERIF_B, 54))
    left(d, lx, 316, "IN WEST LONDON", F(SERIF_B, 54))

    # scoreboard box
    d.rectangle([lx, 388, 600, 500], fill=INK)
    centre(d, (lx + 600) // 2, 402, "BRENTFORD  4 — 0  EVERTON",
           F(SANS_B, 33), fill=PAPER)
    centre(d, (lx + 600) // 2, 448,
           "Lewis-Potter 2 • Janelt 67' • Carvalho 90'",
           F(SANS, 20), fill=(232, 200, 120))

    body = ("Brentford dismantled ten-man Everton 4-0 at the Gtech "
            "Community Stadium to climb into the Premier League top six. "
            "Keane Lewis-Potter struck a quickfire brace, captain Vitaly "
            "Janelt curled in a 30-yard rocket and Fabio Carvalho tapped "
            "home the fourth — spoiling David Moyes' record-breaking "
            "593rd match in charge of the Toffees.")
    para(d, lx, 518, body, F(SERIF, 20), 564, leading=7)

    # ---------- right column: tonight's fixtures ----------
    rx = 636
    d.rectangle([rx, 228, W - 36, 690], fill=BOX, outline=RULE, width=2)
    centre(d, (rx + W - 36) // 2, 242, "TONIGHT IN EUROPE",
           F(SANS_B, 23), fill=RED)
    centre(d, (rx + W - 36) // 2, 274, "CHAMPIONS LEAGUE • MD5",
           F(SANS_B, 15), fill=GREY)
    d.line([rx + 16, 302, W - 52, 302], fill=RULE, width=1)
    fixtures = [
        ("18:45", "Galatasaray v Aston Villa"),
        ("18:45", "Bodo/Glimt v LASK Linz"),
        ("21:00", "Arsenal v Dortmund"),
        ("21:00", "Man City v Napoli"),
        ("21:00", "Real Madrid v PSV"),
        ("21:00", "Feyenoord v Porto"),
        ("21:00", "RB Leipzig v Lens"),
        ("21:00", "Como v AEK Athens"),
        ("21:00", "Slovan v Real Betis"),
    ]
    fy = 316
    for ko, fx in fixtures:
        left(d, rx + 18, fy, ko, F(SANS_B, 17), fill=DARKRED)
        left(d, rx + 84, fy, fx, F(SANS, 17))
        fy += 30
    d.line([rx + 16, fy + 2, W - 52, fy + 2], fill=RULE, width=1)
    para(d, rx + 18, fy + 14,
         "PSG and Real Madrid lead the league phase on 12 points; "
         "Arsenal sit third on 10.", F(SERIF, 17), 316, leading=5)

    # ---------- pitch strip with ball ----------
    py = 706
    d.rectangle([36, py, W - 36, py + 64], fill=PITCH)
    for i in range(9):
        if i % 2 == 0:
            d.rectangle([36 + i * 106, py, 36 + (i + 1) * 106, py + 64],
                        fill=PITCH2)
    d.rectangle([36, py, W - 36, py + 64], outline=INK, width=2)
    d.ellipse([W // 2 - 30, py + 2, W // 2 + 30, py + 62],
              outline=(245, 245, 240), width=3)
    ball(d, W // 2, py + 32, 24)

    # ---------- injury blow box ----------
    by = 792
    d.rectangle([36, by, W - 36, by + 106], fill=(252, 246, 232),
                outline=RED, width=3)
    left(d, 56, by + 12, "OSIMHEN RULED OUT", F(SANS_B, 26), fill=RED)
    para(d, 56, by + 48,
         "Galatasaray lose star striker Victor Osimhen to injury before "
         "Aston Villa's visit to Istanbul — a huge blow on a huge night.",
         F(SERIF, 19), 920, leading=5)

    # ---------- monday results strip ----------
    ry = 906
    d.rectangle([0, ry, W, H], fill=INK)
    centre(d, W // 2, ry + 12, "MONDAY AROUND EUROPE", F(SANS_B, 19),
           fill=(232, 200, 120))
    centre(d, W // 2, ry + 42,
           "Monza 3-0 Fiorentina  •  Levante 1-1 Elche  •  "
           "Al Hilal 2-2 Neftchi", F(SANS, 19), fill=PAPER)
    centre(d, W // 2, ry + 72,
           "U-17 World Cup: Spain 15-0 Fiji — the rout of the day",
           F(SANS, 19), fill=PAPER)

    img.save("entry.png", format="PNG")


if __name__ == "__main__":
    main()
