"""Project cards and buttons for the profile README (GitHub allows no CSS, so they are drawn as SVG).

Run from the repo root:  python tools/make_cards.py
Writes assets/cards/<id>.svg and assets/cards/<id>-<button>.svg (Spanish),
and the same under assets/en/cards (English) and assets/ca/cards (Catalan).
"""
import base64
import io
import os
from xml.sax.saxutils import escape

from PIL import Image, ImageFont

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'SFMono-Regular', monospace"

CARD_W, CARD_H = 600, 300        # the card's drawing units
CARD_PX = 410                    # how wide the README shows it
BTN_W, BTN_H = 280, 64           # the button's drawing units
BTN_PX = 200                     # how wide the README shows it
CARD_PX_H = round(CARD_PX * CARD_H / CARD_W)      # 205: the card's height on screen
PAD = 32                         # the card's inner margin

# A phone shows the card at the width of the column (about 308px) and the
# buttons at their own 200px, one per line. A wide screen puts the buttons
# beside the card, which only fits from GitHub's 1280px breakpoint up: below
# that the column is too narrow and they drop underneath, where a tall button
# would leave a 160px hole. So that is where the two versions swap.
NARROW = '(max-width: 1279px)'

# one colour per technology, the same on every card
TECH = {
    'React': '#61DAFB', 'TypeScript': '#5B9BE6', 'Laravel': '#FF5A4F', 'MySQL': '#5E9BD6',
    'Godot': '#6FA8DC', 'Supabase': '#3FCF8E', 'PostgreSQL': '#7A9CF0', 'Electron': '#7CC4D0',
    'AI Agents': '#FB923C', 'SvelteKit': '#FF6A3D', 'MapLibre': '#38BDF8', 'Web Workers': '#A78BFA',
    'Next.js': '#E5E7EB', 'Drizzle': '#C5F74F', 'JavaScript': '#F7DF1E', 'Node.js': '#7CC46A',
    'WebSocket': '#C4B5FD', 'GDScript': '#9DB8E0', 'Python': '#FFD43B',
}

PROJECTS = [
    dict(id='obsidian', name='Obsidian', logo='obsidian.png', accent='#E8B04B', kind='E-commerce full-stack',
         desc=['Tienda de streetwear con catálogo en Laravel, login', 'Sanctum, carrito sincronizado y pedidos reales.'],
         kind_en='Full-stack e-commerce',
         desc_en=['Streetwear store with a Laravel catalogue, Sanctum', 'login, synced cart and real orders.'],
         tags=['React', 'TypeScript', 'Laravel', 'MySQL'], repo='https://github.com/AleixAj/obsidian',
         kind_ca='E-commerce full-stack',
         desc_ca=['Botiga de streetwear amb catàleg en Laravel, login', 'Sanctum, cistella sincronitzada i comandes reals.'],
         labels_en={'Ver demo': 'Live demo'},
         labels_ca={'Ver demo': 'Veure demo'},
         buttons=[('demo', 'Ver demo', 'https://obsidian.aleixaj.com'), ('code', 'GitHub', 'https://github.com/AleixAj/obsidian')]),
    dict(id='orbex', name='Orbex', logo='orbex.png', accent='#A78BFA', kind='Juego móvil · Google Play',
         desc=['Arcade estilo Zuma: 10 mundos y 80 niveles en pixel', 'art hecho a mano, ranking online y antitrampas.'],
         kind_en='Mobile game · Google Play',
         desc_en=['Zuma-style arcade: 10 worlds and 80 levels in', 'handmade pixel art, online leaderboard and anti-cheat.'],
         tags=['Godot', 'GDScript', 'Python', 'Supabase', 'PostgreSQL'], repo='https://github.com/AleixAj/orbex-web',
         kind_ca='Joc mòbil · Google Play',
         desc_ca=['Arcade estil Zuma: 10 mons i 80 nivells en pixel', 'art fet a mà, rànquing en línia i antitrampes.'],
         labels_en={'Jugar': 'Play'},
         labels_ca={},
         buttons=[('play', 'Google Play', 'https://play.google.com/store/apps/details?id=com.aleix.orbex'), ('game', 'Jugar', 'https://kylen02.itch.io/orbex')]),
    dict(id='nexus', name='NEXUS', logo='nexus.png', accent='#F97316', kind='Asistente de IA · Windows',
         desc=['Agente con 46 herramientas, voz, frase de activación', 'sin conexión y fondo de escritorio animado.'],
         kind_en='AI assistant · Windows',
         desc_en=['Agent with 46 tools, voice, offline wake word', 'and an animated desktop wallpaper.'],
         tags=['Electron', 'TypeScript', 'React', 'AI Agents'], repo='https://github.com/AleixAj/nexus',
         kind_ca='Assistent d’IA · Windows',
         desc_ca=['Agent amb 46 eines, veu, frase d’activació', 'sense connexió i fons d’escriptori animat.'],
         labels_en={'Descargar': 'Download'},
         labels_ca={'Descargar': 'Descarregar'},
         buttons=[('download', 'Descargar', 'https://github.com/AleixAj/nexus/releases/latest/download/NEXUS-Setup.exe'), ('code', 'GitHub', 'https://github.com/AleixAj/nexus')]),
    dict(id='waymark', name='Waymark', logo='waymark.png', accent='#38BDF8', kind='Fotos de viaje en 3D',
         desc=['Lee el GPS de tus fotos, detecta los viajes por su', 'cuenta y los pone en un globo 3D. Sin servidor.'],
         kind_en='Travel photos in 3D',
         desc_en=['Reads the GPS in your photos, detects your trips on', 'its own and plots them on a 3D globe. No server.'],
         tags=['SvelteKit', 'TypeScript', 'MapLibre', 'Web Workers'], repo='https://github.com/AleixAj/waymark',
         kind_ca='Fotos de viatge en 3D',
         desc_ca=['Llegeix el GPS de les fotos, detecta els viatges', 'tot sol i els situa en un globus 3D. Sense servidor.'],
         labels_en={'Ver demo': 'Live demo'},
         labels_ca={'Ver demo': 'Veure demo'},
         buttons=[('demo', 'Ver demo', 'https://waymark.aleixaj.com'), ('code', 'GitHub', 'https://github.com/AleixAj/waymark')]),
    dict(id='nadir', name='Nadir', logo='nadir.png', accent='#F0602C', kind='Monitor de precios',
         desc=['Compara tiendas, guarda el histórico y te avisa por', 'email cuando baja del precio que quieres.'],
         kind_en='Price tracker',
         desc_en=['Compares stores, keeps the price history and emails', 'you when it drops below your target price.'],
         tags=['Next.js', 'TypeScript', 'PostgreSQL', 'Drizzle'], repo='https://github.com/AleixAj/nadir',
         kind_ca='Monitor de preus',
         desc_ca=['Compara botigues, guarda l’històric i t’avisa per', 'correu quan baixa per sota del preu que vols.'],
         labels_en={'Ver demo': 'Live demo'},
         labels_ca={'Ver demo': 'Veure demo'},
         buttons=[('demo', 'Ver demo', 'https://nadir.aleixaj.com'), ('code', 'GitHub', 'https://github.com/AleixAj/nadir')]),
    dict(id='kylenchat', name='Kylen Chat', logo='kylenchat.png', accent='#A970FF', kind='App para streamers',
         desc=['El chat de Twitch transparente encima del juego,', 'con emotes de 7TV, BTTV y FFZ y perfiles por juego.'],
         kind_en='App for streamers',
         desc_en=['Transparent Twitch chat on top of your game, with', '7TV, BTTV and FFZ emotes and per-game profiles.'],
         tags=['Electron', 'JavaScript', 'Node.js', 'WebSocket'], repo='https://github.com/AleixAj/kylenchat',
         kind_ca='App per a streamers',
         desc_ca=['El xat de Twitch transparent damunt del joc, amb', 'emotes de 7TV, BTTV i FFZ i perfils per a cada joc.'],
         labels_en={'Descargar': 'Download'},
         labels_ca={'Descargar': 'Descarregar'},
         buttons=[('download', 'Descargar', 'https://github.com/AleixAj/kylenchat/releases/latest/download/KylenChat-Setup.exe'), ('code', 'GitHub', 'https://github.com/AleixAj/kylenchat')]),
]


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def logo_data(name, size=192):
    im = Image.open(os.path.join('assets', name)).convert('RGBA')
    im.thumbnail((size, size), Image.LANCZOS)
    c = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    c.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im)
    b = io.BytesIO()
    c.save(b, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()


# the tags are Segoe UI Semibold, so measure the real text with it at each size
try:
    PILL_FONTS = {s: ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf', s) for s in (15, 16, 17)}
except OSError:
    PILL_FONTS = {}


def pill_w(text, size=17):
    # 25px from the edge to the text (the dot sits in there) and 12px after it.
    # 4% extra on the text because on a Mac it falls back to Helvetica Neue,
    # which is a bit wider than Segoe UI.
    font = PILL_FONTS.get(size)
    if font:
        text_w = font.getlength(text) * 1.04
    else:
        # no Segoe UI on this machine: rough guess per letter (capitals are wider)
        text_w = sum(9.4 if c.isupper() else 4.2 if c in ' .ijl' else 7.4 for c in text) * size / 15
    return round(25 + text_w + 12)


def pill_size(tags, gap=9):
    """Largest tag size whose row still fits inside the card."""
    limit = CARD_W - PAD
    for size in (17, 16, 15):
        if PAD + sum(pill_w(t, size) for t in tags) + gap * (len(tags) - 1) <= limit:
            return size
    raise ValueError(f'tags do not fit on one row even at 15px: {tags}')


try:
    DESC_FONT = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 21)
except OSError:
    DESC_FONT = None


def check_room(p):
    """Stop a description or an eyebrow that would run off the card."""
    room = CARD_W - PAD * 2
    for line in p['desc']:
        if DESC_FONT and DESC_FONT.getlength(line) * 1.04 > room:
            raise ValueError(f"{p['id']}: this line is too long for the card: {line!r}")
    # the eyebrow is monospaced: 18px glyphs are 0.6em wide, plus its tracking
    if len(p['kind']) * (18 * 0.6 + 1.4) > CARD_W - 150 - PAD:
        raise ValueError(f"{p['id']}: this label is too long for the card: {p['kind']!r}")


def card(p):
    check_room(p)
    W, H = CARD_W, CARD_H
    a = p['accent']
    size = pill_size(p['tags'])
    tags, x = [], PAD
    for t in p['tags']:
        c, w = TECH[t], pill_w(t, size)
        tags.append(f'<rect x="{x}" y="234" width="{w}" height="36" rx="18" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".45"/>'
                    f'<circle cx="{x + 15}" cy="252" r="3.5" fill="{c}"/>'
                    f'<text x="{x + 25}" y="{258 if size > 15 else 257}" font-family="{FONT}" font-size="{size}" font-weight="600" fill="{c}">{escape(t)}</text>')
        x += w + 9
    desc = ''.join(f'<text x="32" y="{173 + i * 30}" font-family="{FONT}" font-size="21" fill="#CBD5E1">{escape(l)}</text>' for i, l in enumerate(p['desc']))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D1424"/><stop offset="1" stop-color="#070B16"/></linearGradient>
    <radialGradient id="glow" cx="88%" cy="0%" r="70%"><stop offset="0" stop-color="{a}" stop-opacity=".30"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
    <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset=".5" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
    <clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22"/></clipPath>
    <clipPath id="logo"><rect x="34" y="34" width="84" height="84" rx="16"/></clipPath>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#fff" stroke-opacity=".035"/></pattern>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#grid)"/>
    <rect width="{W}" height="{H}" fill="url(#glow)"/>
    <rect x="80" y="0" width="{W - 160}" height="2" fill="url(#edge)"/>
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{a}" stroke-opacity=".28" stroke-width="1.5"/>
  <rect x="28" y="28" width="96" height="96" rx="20" fill="#0B1222" stroke="{a}" stroke-opacity=".35"/>
  <image x="34" y="34" width="84" height="84" href="{logo_data(p['logo'])}" clip-path="url(#logo)"/>
  <text x="148" y="74" font-family="{FONT}" font-size="33" font-weight="700" fill="#FFFFFF" letter-spacing="-.5">{escape(p['name'])}</text>
  <text x="150" y="109" font-family="{MONO}" font-size="18" font-weight="700" fill="{a}" letter-spacing="1.4">{escape(p['kind'].upper())}</text>
  {desc}
  {''.join(tags)}
</svg>
'''


ICONS = {
    'demo': '<path d="M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18zM3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9M12 3C9.5 5.6 8.2 8.6 8.2 12s1.3 6.4 3.8 9"/>',
    # the GitHub mark, filled with the stroke colour
    'code': '<path stroke="none" fill="COL" d="M12 1.5a10.5 10.5 0 0 0-3.32 20.46c.53.1.72-.23.72-.5v-1.86c-2.93.64-3.55-1.24-3.55-1.24-.48-1.22-1.17-1.54-1.17-1.54-.96-.66.07-.64.07-.64 1.06.07 1.61 1.09 1.61 1.09.94 1.61 2.47 1.15 3.07.88.1-.68.37-1.15.67-1.41-2.34-.27-4.8-1.17-4.8-5.2 0-1.15.41-2.09 1.08-2.83-.11-.27-.47-1.34.1-2.79 0 0 .88-.28 2.89 1.08a10 10 0 0 1 5.26 0c2-1.36 2.88-1.08 2.88-1.08.58 1.45.22 2.52.11 2.79.67.74 1.08 1.68 1.08 2.83 0 4.04-2.47 4.93-4.81 5.19.38.33.71.97.71 1.96v2.9c0 .28.19.61.73.5A10.5 10.5 0 0 0 12 1.5z"/>',
    'download': '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    'play': '<path d="M5 3.5v17l15-8.5z"/>',
    'game': '<path d="M7 9v6M4 12h6M15.5 10.5h.01M18 13.5h.01M6 5h12a4 4 0 0 1 4 4v6a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V9a4 4 0 0 1 4-4z"/>',
}


def button(p, kind, label, primary, tall=False):
    """The drawing is always 280x64 units wide; `tall` only pads it vertically.

    A tall button is as high as the card it sits next to, with the button
    itself centred, so on a wide screen the two
    buttons line up beside the card instead of hanging off its bottom edge.
    The phone gets the plain one. Both are served from the same <picture>, and
    neither carries a width attribute: the browser takes the size from the file,
    which is the only way one element can be two sizes.
    """
    W, H = BTN_W, BTN_H
    a = p['accent']
    r, g, b = rgb(a)
    # dark text on light accents, white on the rest
    ink = '#0B1020' if (r * .299 + g * .587 + b * .114) > 150 else '#FFFFFF'
    fill = f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="16" fill="url(#f)"/>' if primary else \
           f'<rect x="4.75" y="4.75" width="{W - 9.5}" height="{H - 9.5}" rx="15.25" fill="#0B1222" stroke="{a}" stroke-opacity=".55" stroke-width="1.5"/>'
    col = ink if primary else '#E2E8F0'
    tw = len(label) * 11.4
    x0 = (W - (24 + 12 + tw)) / 2
    body = f'''{fill}
  <g transform="translate({x0:.0f} 20)" fill="none" stroke="{col if not primary else ink}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[kind].replace('COL', col if not primary else ink)}</g>
  <text x="{x0 + 36:.0f}" y="40" font-family="{FONT}" font-size="20" font-weight="700" fill="{col}">{escape(label)}</text>'''
    if tall:
        # 287 units tall is 205px once 280 units are drawn at 200px, the height
        # of a 600x300 card shown at 410px
        vh = round(H * CARD_PX_H / (BTN_PX * H / W))      # units that render as the card's height
        size = f'width="{BTN_PX}" height="{CARD_PX_H}" viewBox="0 0 {W} {vh}"'
        content = f'<g transform="translate(0 {(vh - H) / 2})">{body}</g>'
    else:
        size = f'width="{BTN_PX}" height="{round(BTN_PX * H / W)}" viewBox="0 0 {W} {H}"'
        content = body
    return f'''<svg xmlns="http://www.w3.org/2000/svg" {size}>
  <defs><linearGradient id="f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity=".78"/></linearGradient></defs>
  {content}
</svg>
'''


def localized(p, lang):
    if lang == 'es':
        return p
    labels = p[f'labels_{lang}']
    return dict(p, kind=p[f'kind_{lang}'], desc=p[f'desc_{lang}'],
                buttons=[(k, labels.get(l, l), u) for k, l, u in p['buttons']])


for lang, OUT in (('es', 'assets/cards'), ('en', 'assets/en/cards'), ('ca', 'assets/ca/cards')):
    projects = [localized(p, lang) for p in PROJECTS]
    os.makedirs(OUT, exist_ok=True)
    for p in projects:
        open(f"{OUT}/{p['id']}.svg", 'w', encoding='utf8').write(card(p))
        for i, (kind, label, _) in enumerate(p['buttons']):
            open(f"{OUT}/{p['id']}-{kind}.svg", 'w', encoding='utf8').write(button(p, kind, label, i == 0))
            open(f"{OUT}/{p['id']}-{kind}-tall.svg", 'w', encoding='utf8').write(button(p, kind, label, i == 0, tall=True))

    # The README block, one project per row: its card, then its own buttons.
    # Two projects per row would put four buttons under two cards, and a phone,
    # which stacks everything into one column, then shows the four in a heap
    # with no way to tell which card each belongs to.
    #
    # The widths are in pixels, not percentages: GitHub caps an image at the
    # column width but never scales a smaller one up, so on a phone the card
    # drops to 308px and is still readable, instead of being squeezed to 150px.
    rows = []
    for p in projects:
        buttons = ' '.join(
            f'<a href="{u}"><picture><source media="{NARROW}" srcset="{OUT}/{p["id"]}-{k}.svg">'
            f'<img src="{OUT}/{p["id"]}-{k}-tall.svg" alt="{escape(p["name"])}: {escape(l)}"></picture></a>'
            for k, l, u in p['buttons'])
        alt = escape(f'{p["name"]} · {p["kind"]}: {" ".join(p["desc"])}')
        rows.append(f'<p align="center">\n'
                    f'  <a href="{p["repo"]}"><img src="{OUT}/{p["id"]}.svg" width="{CARD_PX}" alt="{alt}"></a>\n'
                    f'  {buttons}\n'
                    f'</p>')
    open(f'tools/projects.{lang}.html', 'w', encoding='utf8').write('\n\n'.join(rows) + '\n')
print('ok', len(PROJECTS), 'cards')
