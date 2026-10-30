"""Phone versions of the header and the three panels.

Run from the repo root:  python tools/make_narrow.py
Writes assets/narrow/<header|stack|career|education>.svg and the same under
assets/en/narrow and assets/ca/narrow.

Why they exist: the wide panels are 1200px of artwork and the header is 1280px.
GitHub caps an image at the column width, which on a phone is about 308px, so
their 15-17px text ends up at 4px and nobody can read it. These are the same
panels redrawn for a single column; the README picks them with
<picture media="(max-width: 620px)"> and falls back to the wide ones elsewhere.
"""
import os
from xml.sax.saxutils import escape

from PIL import ImageFont

from make_sections import (CAREER, CAREER_CA, CAREER_EN, EDUCATION, EDUCATION_CA, EDUCATION_EN,
                           FONT, GROUPS, MONO, frame, icon, translated)

W = 420
LANGS = ('es', 'en', 'ca')

# Bold text is wider than regular at the same size, so each weight is measured
# with its own font: measuring a bold job title with the regular one is how a
# line ends up running off the panel.
FACES = {'regular': 'C:/Windows/Fonts/segoeui.ttf', 'bold': 'C:/Windows/Fonts/segoeuib.ttf'}
try:
    MEASURE = {(weight, size): ImageFont.truetype(path, size)
               for weight, path in FACES.items() for size in range(10, 29)}
except OSError:
    MEASURE = {}


def fits(text, size, limit, weight='regular'):
    font = MEASURE.get((weight, round(size)))
    if font:
        width = font.getlength(text) * 1.04      # a Mac falls back to Helvetica Neue, a bit wider
    else:
        width = len(text) * size * (0.60 if weight == 'bold' else 0.56)
    return width <= limit


def wrap_to(text, size, limit, weight='regular'):
    """Break text into as many lines as it needs. It never drops a word: the
    panel grows instead, which is better than losing half a job title."""
    lines, cur = [], ''
    for word in text.split():
        trial = f'{cur} {word}'.strip()
        if cur and not fits(trial, size, limit, weight):
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ---------- technologies ----------
def stack(lang):
    colw, gap, x0 = 176, 14, 26
    title, sub = {'es': ('Tecnologías', 'LO QUE USO CADA DÍA'), 'en': ('Tech stack', 'WHAT I USE EVERY DAY'),
                  'ca': ('Tecnologies', 'EL QUE FAIG SERVIR CADA DIA')}[lang]
    out = [f'  <text x="26" y="52" font-family="{FONT}" font-size="25" font-weight="700" fill="#FFFFFF">{title}</text>',
           f'  <text x="26" y="76" font-family="{MONO}" font-size="12" fill="#94A3B8" letter-spacing="1.2">{sub}</text>']
    y = 100
    for row in (GROUPS[:2], GROUPS[2:]):
        h = 54 + max(len(items) for _, _, items in row) * 38 + 10
        for gi, (titles, gc, items) in enumerate(row):
            gtitle = titles[LANGS.index(lang)]
            x = x0 + gi * (colw + gap)
            out.append(f'  <rect x="{x}" y="{y}" width="{colw}" height="{h}" rx="16" fill="#0B1222" fill-opacity=".7" stroke="{gc}" stroke-opacity=".22"/>')
            out.append(f'  <rect x="{x + 16}" y="{y + 18}" width="18" height="3" rx="1.5" fill="{gc}"/>')
            out.append(f'  <text x="{x + 16}" y="{y + 42}" font-family="{MONO}" font-size="12" font-weight="700" fill="{gc}" letter-spacing="1.2">{escape(gtitle)}</text>')
            for i, (slug, name, c) in enumerate(items):
                iy = y + 56 + i * 38
                out.append(f'  <rect x="{x + 14}" y="{iy}" width="30" height="30" rx="9" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".35"/>')
                out.append('  ' + icon(slug, x + 21, iy + 7, 16, c))
                out.append(f'  <text x="{x + 52}" y="{iy + 20}" font-family="{FONT}" font-size="15" font-weight="600" fill="#E2E8F0">{escape(name)}</text>')
        y += h + gap
    return frame(W, y + 8, '\n'.join(out))


# ---------- timelines ----------
def timeline(title, sub, rows):
    rail, x1 = 34, 56
    text_w = W - x1 - 22
    head = [f'  <text x="26" y="52" font-family="{FONT}" font-size="25" font-weight="700" fill="#FFFFFF">{escape(title)}</text>',
            f'  <text x="26" y="76" font-family="{MONO}" font-size="12" fill="#94A3B8" letter-spacing="1.2">{escape(sub)}</text>']
    dots, body, y = [], [], 104
    for period, role, place, c, desc in rows:
        body.append(f'  <text x="{x1}" y="{y + 12}" font-family="{MONO}" font-size="12" font-weight="700" fill="{c}" letter-spacing="1">{escape(period)}</text>')
        dots.append(f'  <circle cx="{rail}" cy="{y + 7}" r="11" fill="{c}" fill-opacity=".15"/>'
                    f'<circle cx="{rail}" cy="{y + 7}" r="5" fill="{c}" stroke="#070B16" stroke-width="2"/>')
        ry = y + 38
        for line in wrap_to(role, 17, text_w, 'bold'):
            body.append(f'  <text x="{x1}" y="{ry}" font-family="{FONT}" font-size="17" font-weight="700" fill="#FFFFFF">{escape(line)}</text>')
            ry += 22
        body.append(f'  <text x="{x1}" y="{ry}" font-family="{FONT}" font-size="14" font-weight="600" fill="{c}">{escape(place)}</text>')
        for line in wrap_to(desc, 14, text_w) if desc else []:
            ry += 20
            body.append(f'  <text x="{x1}" y="{ry}" font-family="{FONT}" font-size="14" fill="#94A3B8">{escape(line)}</text>')
        y = ry + 28
    rail_line = f'  <rect x="{rail - 1}" y="104" width="2" height="{y - 132}" fill="#334155"/>'
    return frame(W, y - 4, '\n'.join(head + [rail_line] + dots + body), glow='12%')


# ---------- header ----------
HEADER = {
    'es': ('HOLA, SOY', 'Más de 5 años llevando software',
           'a producción: web, escritorio, juegos e IA.'),
    'en': ('HI, I\u2019M', '5+ years shipping software to production:',
           'web, desktop, games and AI.'),
    'ca': ('HOLA, SÓC', 'Més de 5 anys portant programari',
           'a producció: web, escriptori, jocs i IA.'),
}


# the same six the wide header lists, on two lines because they do not fit on one
TECH_LINES = ('JavaScript · TypeScript · PHP', 'React · Laravel · Three.js')


def header(lang):
    hello, line1, line2 = HEADER[lang]
    h, cx = 424, 210
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">
  <defs>
    <radialGradient id="glow" cx="50%" cy="22%" r="62%">
      <stop offset="0" stop-color="#22d3ee" stop-opacity=".34"/>
      <stop offset=".5" stop-color="#0f172a" stop-opacity=".2"/>
      <stop offset="1" stop-color="#020617" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="violet" cx="88%" cy="92%" r="52%">
      <stop offset="0" stop-color="#a855f7" stop-opacity=".22"/>
      <stop offset="1" stop-color="#a855f7" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="core" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset=".25" stop-color="#a5f3fc"/>
      <stop offset=".6" stop-color="#22d3ee" stop-opacity=".55"/>
      <stop offset="1" stop-color="#22d3ee" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="line" x1="0" x2="1">
      <stop offset="0" stop-color="#22d3ee" stop-opacity="0"/>
      <stop offset=".5" stop-color="#22d3ee" stop-opacity=".9"/>
      <stop offset="1" stop-color="#22d3ee" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#22d3ee" stroke-opacity=".06"/>
    </pattern>
    <clipPath id="frame"><rect width="{W}" height="{h}" rx="22"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{h}" fill="#020617"/>
    <rect width="{W}" height="{h}" fill="url(#grid)"/>
    <rect width="{W}" height="{h}" fill="url(#glow)"/>
    <rect width="{W}" height="{h}" fill="url(#violet)"/>
    <g fill="#e2e8f0">
      <circle cx="54" cy="44" r="1.2" opacity=".6"><animate attributeName="opacity" values=".2;.8;.2" dur="4s" repeatCount="indefinite"/></circle>
      <circle cx="366" cy="60" r="1.4" opacity=".7"><animate attributeName="opacity" values=".3;.9;.3" dur="3.5s" repeatCount="indefinite"/></circle>
      <circle cx="384" cy="206" r="1" opacity=".5"/>
      <circle cx="36" cy="188" r="1.1" opacity=".5"><animate attributeName="opacity" values=".6;.2;.6" dur="6s" repeatCount="indefinite"/></circle>
    </g>
    <g transform="translate({cx} 92)">
      <circle r="74" fill="none" stroke="#22d3ee" stroke-opacity=".18"/>
      <g>
        <circle r="60" fill="none" stroke="#22d3ee" stroke-opacity=".55" stroke-width="2" stroke-dasharray="76 20 26 20"/>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="24s" repeatCount="indefinite"/>
      </g>
      <g>
        <circle r="44" fill="none" stroke="#a855f7" stroke-opacity=".6" stroke-width="2" stroke-dasharray="38 16 9 16"/>
        <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="16s" repeatCount="indefinite"/>
      </g>
      <g>
        <ellipse rx="96" ry="28" fill="none" stroke="#e2e8f0" stroke-opacity=".12" transform="rotate(-18)"/>
        <circle cx="96" cy="0" r="3.5" fill="#fbbf24" transform="rotate(-18)"/>
        <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="30s" repeatCount="indefinite"/>
      </g>
      <circle r="28" fill="url(#core)"><animate attributeName="r" values="25;31;25" dur="4s" repeatCount="indefinite"/></circle>
      <circle r="7" fill="#ffffff"/>
    </g>
    <text x="{cx}" y="208" text-anchor="middle" fill="#22d3ee" font-family="{MONO}" font-size="13" letter-spacing="4.5">{escape(hello)}</text>
    <text x="{cx}" y="254" text-anchor="middle" fill="#ffffff" font-family="{FONT}" font-size="42" font-weight="700" letter-spacing="-1">Aleix Auqué</text>
    <text x="{cx}" y="285" text-anchor="middle" fill="#22d3ee" font-family="{FONT}" font-size="19" font-weight="600">Software Developer · Full-stack</text>
    <text x="{cx}" y="318" text-anchor="middle" fill="#cbd5e1" font-family="{FONT}" font-size="16">{escape(line1)}</text>
    <text x="{cx}" y="340" text-anchor="middle" fill="#cbd5e1" font-family="{FONT}" font-size="16">{escape(line2)}</text>
    <path d="M90 360 H330" stroke="url(#line)" stroke-width="2"/>
    <text x="{cx}" y="382" text-anchor="middle" fill="#94a3b8" font-family="{MONO}" font-size="12.5" letter-spacing=".5">{TECH_LINES[0]}</text>
    <text x="{cx}" y="404" text-anchor="middle" fill="#94a3b8" font-family="{MONO}" font-size="12.5" letter-spacing=".5">{TECH_LINES[1]}</text>
  </g>
  <rect x=".75" y=".75" width="{W - 1.5}" height="{h - 1.5}" rx="21.25" fill="none" stroke="#22d3ee" stroke-opacity=".25" stroke-width="1.5"/>
</svg>
'''


TITLES = {
    'es': (('Trayectoria', 'MÁS DE 5 AÑOS EN PRODUCCIÓN'), ('Formación', 'TÉCNICO SUPERIOR · BOOTCAMPS')),
    'en': (('Experience', '5+ YEARS SHIPPING TO PRODUCTION'), ('Education', 'HIGHER VOCATIONAL DEGREE · BOOTCAMPS')),
    'ca': (('Trajectòria', 'MÉS DE 5 ANYS EN PRODUCCIÓ'), ('Formació', 'TÈCNIC SUPERIOR · BOOTCAMPS')),
}
ROWS = {
    'es': (CAREER, EDUCATION),
    'en': (translated(CAREER, CAREER_EN), translated(EDUCATION, EDUCATION_EN)),
    'ca': (translated(CAREER, CAREER_CA), translated(EDUCATION, EDUCATION_CA)),
}

for lang in LANGS:
    out = 'assets/narrow' if lang == 'es' else f'assets/{lang}/narrow'
    os.makedirs(out, exist_ok=True)
    (career_t, education_t) = TITLES[lang]
    career_rows, education_rows = ROWS[lang]
    open(f'{out}/header.svg', 'w', encoding='utf8').write(header(lang))
    open(f'{out}/stack.svg', 'w', encoding='utf8').write(stack(lang))
    open(f'{out}/career.svg', 'w', encoding='utf8').write(timeline(*career_t, career_rows))
    open(f'{out}/education.svg', 'w', encoding='utf8').write(timeline(*education_t, education_rows))
print('ok')
