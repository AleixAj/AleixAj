"""Project cards and buttons for the profile README (GitHub allows no CSS, so they are drawn as SVG).

Run from the repo root:  python tools/make_cards.py
Writes assets/cards/<id>.svg and assets/cards/<id>-<button>.svg
"""
import base64
import io
import os
from xml.sax.saxutils import escape

from PIL import Image

OUT = 'assets/cards'
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'SFMono-Regular', monospace"

# one colour per technology, the same on every card
TECH = {
    'React': '#61DAFB', 'TypeScript': '#5B9BE6', 'Laravel': '#FF5A4F', 'MySQL': '#5E9BD6',
    'Godot': '#6FA8DC', 'Supabase': '#3FCF8E', 'PostgreSQL': '#7A9CF0', 'Electron': '#7CC4D0',
    'AI Agents': '#FB923C', 'SvelteKit': '#FF6A3D', 'MapLibre': '#38BDF8', 'Web Workers': '#A78BFA',
    'Next.js': '#E5E7EB', 'Drizzle': '#C5F74F', 'JavaScript': '#F7DF1E', 'Node.js': '#7CC46A',
    'WebSocket': '#C4B5FD', 'GDScript': '#9DB8E0',
}

PROJECTS = [
    dict(id='obsidian', name='Obsidian', logo='obsidian.png', accent='#E8B04B', kind='E-COMMERCE FULL-STACK',
         desc=['Tienda de streetwear con catálogo en Laravel, login', 'Sanctum, carrito sincronizado y pedidos reales.'],
         tags=['React', 'TypeScript', 'Laravel', 'MySQL'], repo='https://github.com/AleixAj/obsidian',
         buttons=[('demo', 'Ver demo', 'https://obsidian.aleixaj.com'), ('code', 'Código', 'https://github.com/AleixAj/obsidian')]),
    dict(id='orbex', name='Orbex', logo='orbex.png', accent='#A78BFA', kind='JUEGO MÓVIL · GOOGLE PLAY',
         desc=['Arcade estilo Zuma: 10 mundos y 80 niveles en pixel', 'art hecho a mano, ranking online y anti-trampas.'],
         tags=['Godot', 'GDScript', 'Supabase', 'PostgreSQL'], repo='https://github.com/AleixAj/orbex-web',
         buttons=[('play', 'Google Play', 'https://play.google.com/store/apps/details?id=com.aleix.orbex'), ('game', 'Jugar', 'https://kylen02.itch.io/orbex')]),
    dict(id='nexus', name='NEXUS', logo='nexus.png', accent='#F97316', kind='ASISTENTE DE IA · WINDOWS',
         desc=['Agente con 46 herramientas, voz, frase de activación', 'sin conexión y fondo de escritorio animado.'],
         tags=['Electron', 'TypeScript', 'React', 'AI Agents'], repo='https://github.com/AleixAj/nexus',
         buttons=[('download', 'Descargar', 'https://github.com/AleixAj/nexus/releases/latest/download/NEXUS-Setup.exe'), ('code', 'Código', 'https://github.com/AleixAj/nexus')]),
    dict(id='waymark', name='Waymark', logo='waymark.png', accent='#38BDF8', kind='FOTOS DE VIAJE EN 3D',
         desc=['Lee el GPS de tus fotos, detecta los viajes solo y', 'los pone en un globo 3D. Sin servidor.'],
         tags=['SvelteKit', 'TypeScript', 'MapLibre', 'Web Workers'], repo='https://github.com/AleixAj/waymark',
         buttons=[('demo', 'Ver demo', 'https://waymark.aleixaj.com'), ('code', 'Código', 'https://github.com/AleixAj/waymark')]),
    dict(id='nadir', name='Nadir', logo='nadir.png', accent='#F0602C', kind='MONITOR DE PRECIOS',
         desc=['Compara tiendas, guarda el histórico y te avisa por', 'email cuando baja del precio que quieres.'],
         tags=['Next.js', 'TypeScript', 'PostgreSQL', 'Drizzle'], repo='https://github.com/AleixAj/nadir',
         buttons=[('demo', 'Ver demo', 'https://nadir.aleixaj.com'), ('code', 'Código', 'https://github.com/AleixAj/nadir')]),
    dict(id='kylenchat', name='Kylen Chat', logo='kylenchat.png', accent='#A970FF', kind='APP PARA STREAMERS',
         desc=['El chat de Twitch transparente encima del juego,', 'con emotes de 7TV, BTTV y FFZ y perfiles por juego.'],
         tags=['Electron', 'JavaScript', 'Node.js', 'WebSocket'], repo='https://github.com/AleixAj/kylenchat',
         buttons=[('download', 'Descargar', 'https://github.com/AleixAj/kylenchat/releases/latest/download/KylenChat-Setup.exe'), ('code', 'Código', 'https://github.com/AleixAj/kylenchat')]),
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


def pill_w(text):
    # Segoe UI semibold at 15px: capitals are wider than the rest, plus the padding
    return round(sum(10.6 if c.isupper() else 4.6 if c in ' .ijl' else 8.4 for c in text) + 36)


def card(p):
    W, H = 600, 300
    a = p['accent']
    tags, x = [], 32
    for t in p['tags']:
        c, w = TECH[t], pill_w(t)
        tags.append(f'<rect x="{x}" y="236" width="{w}" height="32" rx="16" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".45"/>'
                    f'<circle cx="{x + 15}" cy="252" r="3.5" fill="{c}"/>'
                    f'<text x="{x + 25}" y="257" font-family="{FONT}" font-size="15" font-weight="600" fill="{c}">{escape(t)}</text>')
        x += w + 9
    desc = ''.join(f'<text x="32" y="{174 + i * 29}" font-family="{FONT}" font-size="20" fill="#CBD5E1">{escape(l)}</text>' for i, l in enumerate(p['desc']))
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
  <text x="150" y="108" font-family="{MONO}" font-size="15" font-weight="700" fill="{a}" letter-spacing="1.6">{escape(p['kind'])}</text>
  <circle cx="548" cy="58" r="20" fill="{a}" fill-opacity=".12" stroke="{a}" stroke-opacity=".4"/>
  <path d="M541 65l14-14M545 51h10v10" fill="none" stroke="{a}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  {desc}
  {''.join(tags)}
</svg>
'''


ICONS = {
    'demo': '<path d="M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18zM3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9M12 3C9.5 5.6 8.2 8.6 8.2 12s1.3 6.4 3.8 9"/>',
    'code': '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/>',
    'download': '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    'play': '<path d="M5 3.5v17l15-8.5z"/>',
    'game': '<path d="M7 9v6M4 12h6M15.5 10.5h.01M18 13.5h.01M6 5h12a4 4 0 0 1 4 4v6a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V9a4 4 0 0 1 4-4z"/>',
}


def button(p, kind, label, primary):
    W, H = 280, 64
    a = p['accent']
    r, g, b = rgb(a)
    # dark text on light accents, white on the rest
    ink = '#0B1020' if (r * .299 + g * .587 + b * .114) > 150 else '#FFFFFF'
    fill = f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="16" fill="url(#f)"/>' if primary else \
           f'<rect x="4.75" y="4.75" width="{W - 9.5}" height="{H - 9.5}" rx="15.25" fill="#0B1222" stroke="{a}" stroke-opacity=".55" stroke-width="1.5"/>'
    col = ink if primary else '#E2E8F0'
    tw = len(label) * 10.2
    x0 = (W - (24 + 12 + tw)) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs><linearGradient id="f" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{a}" stop-opacity=".78"/></linearGradient></defs>
  {fill}
  <g transform="translate({x0:.0f} 20)" fill="none" stroke="{col if not primary else ink}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g>
  <text x="{x0 + 36:.0f}" y="39" font-family="{FONT}" font-size="18" font-weight="700" fill="{col}">{escape(label)}</text>
</svg>
'''


os.makedirs(OUT, exist_ok=True)
for p in PROJECTS:
    open(f"{OUT}/{p['id']}.svg", 'w', encoding='utf8').write(card(p))
    for i, (kind, label, _) in enumerate(p['buttons']):
        open(f"{OUT}/{p['id']}-{kind}.svg", 'w', encoding='utf8').write(button(p, kind, label, i == 0))

# the README block, two projects per row
rows = []
for i in range(0, len(PROJECTS), 2):
    pair = PROJECTS[i:i + 2]
    cards = '\n  '.join(f'<a href="{p["repo"]}"><img src="{OUT}/{p["id"]}.svg" width="49%" alt="{escape(p["name"])}"></a>' for p in pair)
    btns = '\n  &nbsp;&nbsp;\n  '.join(' '.join(f'<a href="{u}"><img src="{OUT}/{p["id"]}-{k}.svg" width="23.5%" alt="{escape(p["name"])}: {escape(l)}"></a>' for k, l, u in p['buttons']) for p in pair)
    rows.append(f'<p align="center">\n  {cards}\n  <br>\n  {btns}\n</p>')
open('tools/projects.html', 'w', encoding='utf8').write('\n\n'.join(rows) + '\n')
print('ok', len(PROJECTS), 'cards')
