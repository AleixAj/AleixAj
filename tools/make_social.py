"""Social preview images (1280x640) for the project repos.

Run from the repo root:  python tools/make_social.py
Writes assets/social/<repo>.png, one per featured project.

GitHub has no API for this: upload each file by hand in
Settings - General - Social preview of its repository. The image is what
shows up when the repo link is shared on LinkedIn, X, Slack or Discord;
without it GitHub sends a generic grey card.

Same design language as the cards in the README, drawn with Pillow at 2x
and scaled down, since there is no SVG renderer on this machine.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from make_cards import PROJECTS, TECH, localized, rgb

S = 2                      # supersampling
W, H = 1280 * S, 640 * S
OUT = 'assets/social'

BOLD = 'C:/Windows/Fonts/segoeuib.ttf'
SEMI = 'C:/Windows/Fonts/seguisb.ttf'
BOOK = 'C:/Windows/Fonts/segoeui.ttf'
MONOB = 'C:/Windows/Fonts/consolab.ttf'
MONO = 'C:/Windows/Fonts/consola.ttf'


def font(path, size):
    return ImageFont.truetype(path, size * S)


def background(accent):
    """Vertical gradient, faint grid and the accent glow of the card."""
    y = np.linspace(0, 1, H)[:, None]
    top, bottom = np.array(rgb('#0D1424')), np.array(rgb('#070B16'))
    column = top + (bottom - top) * y                      # (H, 3)
    img = np.repeat(column[:, None, :], W, axis=1)         # (H, W, 3)

    yy, xx = np.mgrid[0:H, 0:W]
    for cx, cy, radius, colour, strength in ((0.90, -0.05, 0.42, accent, .26),
                                             (0.02, 1.05, 0.34, '#A855F7', .14)):
        d = np.hypot(xx - cx * W, yy - cy * H) / (radius * W)
        glow = np.exp(-(d * 1.6) ** 2)[:, :, None] * strength
        img = img * (1 - glow) + np.array(rgb(colour)) * glow

    base = Image.fromarray(img.astype('uint8'), 'RGB')
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(grid)
    for x in range(0, W, 40 * S):
        g.line([(x, 0), (x, H)], fill=(255, 255, 255, 9), width=S)
    for y in range(0, H, 40 * S):
        g.line([(0, y), (W, y)], fill=(255, 255, 255, 9), width=S)
    base = Image.alpha_composite(base.convert('RGBA'), grid)

    # the accent strip along the top edge, fading out at both ends
    strip = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    s = ImageDraw.Draw(strip)
    r, g_, b = rgb(accent)
    for x in range(W):
        fade = 1 - abs(x / W - .5) * 2
        s.line([(x, 0), (x, 5 * S)], fill=(r, g_, b, int(255 * fade ** .6)))
    return Image.alpha_composite(base, strip)


def tracked(draw, xy, text, fnt, fill, tracking):
    """Pillow has no letter-spacing, so place one character at a time."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + tracking * S
    return x


def pills(tint, ink, tags, x0, y, size):
    """The tinted body goes on the overlay, the dot and the label on top."""
    x = x0
    fnt = font(SEMI, size)
    h = 56 * S
    for tag in tags:
        colour = TECH[tag]
        r, g, b = rgb(colour)
        w = 34 * S + fnt.getlength(tag) + 22 * S
        tint.rounded_rectangle([x, y, x + w, y + h], radius=h // 2,
                               fill=(r, g, b, 30), outline=(r, g, b, 115), width=round(1.5 * S))
        cy = y + h / 2
        ink.ellipse([x + 18 * S - 5 * S, cy - 5 * S, x + 18 * S + 5 * S, cy + 5 * S], fill=colour)
        ink.text((x + 34 * S, cy), tag, font=fnt, fill=colour, anchor='lm')
        x += w + 16 * S
    return x


def pill_width(tags, size):
    fnt = font(SEMI, size)
    return sum(56 * S + fnt.getlength(t) for t in tags) + 16 * S * (len(tags) - 1)


def card(p):
    accent = p['accent']
    r, g, b = rgb(accent)
    img = background(accent)
    # Pillow's draw overwrites pixels instead of blending them, so everything
    # translucent is drawn on its own layer and composited.
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tint = ImageDraw.Draw(layer)

    # logo
    tile, lx, ly = 168 * S, 84 * S, 96 * S
    tint.rounded_rectangle([lx, ly, lx + tile, ly + tile], radius=34 * S,
                           fill=(11, 18, 34, 235), outline=(r, g, b, 110), width=round(1.5 * S))

    # tech pills, shrunk a little if the row would not fit
    size = next((s for s in (32, 30, 28) if pill_width(p['tags'], s) <= 1112 * S), 28)

    # the divider above the footer, fading out at both ends
    for x in range(84 * S, 1196 * S):
        fade = 1 - abs((x - 84 * S) / (1112 * S) - .5) * 2
        tint.line([(x, 500 * S), (x, 500 * S + round(1.5 * S))], fill=(r, g, b, int(130 * fade ** .8)))

    ink_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ink = ImageDraw.Draw(ink_layer)
    pills(tint, ink, p['tags'], 84 * S, 402 * S, size)

    img = Image.alpha_composite(img, layer)
    logo = Image.open(os.path.join('assets', p['logo'])).convert('RGBA')
    logo.thumbnail((tile - 28 * S, tile - 28 * S), Image.LANCZOS)
    img.paste(logo, (lx + (tile - logo.width) // 2, ly + (tile - logo.height) // 2), logo)
    img = Image.alpha_composite(img, ink_layer)

    d = ImageDraw.Draw(img)
    tx = lx + tile + 48 * S
    d.text((tx, 186 * S), p['name'], font=font(BOLD, 82), fill='#FFFFFF', anchor='ls')
    tracked(d, (tx + 2 * S, 206 * S), p['kind'], font(MONOB, 27), accent, 3)
    for i, line in enumerate(p['desc']):
        d.text((84 * S, (312 + i * 46) * S), line, font=font(BOOK, 34), fill='#CBD5E1', anchor='ls')
    d.text((84 * S, 548 * S), p['repo'].replace('https://', ''), font=font(MONO, 26), fill='#64748B', anchor='ls')
    d.text((1196 * S, 548 * S), 'aleixaj.com', font=font(MONOB, 26), fill=accent, anchor='rs')

    return img.convert('RGB').resize((W // S, H // S), Image.LANCZOS)


os.makedirs(OUT, exist_ok=True)
for project in PROJECTS:
    p = localized(project, 'en')
    name = p['repo'].rstrip('/').rsplit('/', 1)[-1]
    path = f'{OUT}/{name}.png'
    card(p).save(path, optimize=True)
    print(f'{path}  {os.path.getsize(path) // 1024} KB')
