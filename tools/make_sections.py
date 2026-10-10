"""Technologies, career and education panels for the profile README (drawn as SVG: GitHub allows no CSS).

Run from the repo root:  python tools/make_sections.py
Writes the Spanish panels to assets/, the English ones to assets/en/ and the Catalan ones to assets/ca/.
Icons: Simple Icons (CC0), saved in tools/icons.
"""
import os
import re
import textwrap
from xml.sax.saxutils import escape

FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'SFMono-Regular', monospace"
CYAN, VIOLET = '#22D3EE', '#A855F7'


def icon(slug, x, y, size, color):
    d = re.search(r' d="([^"]+)"', open(f'tools/icons/{slug}.svg', encoding='utf8').read()).group(1)
    return f'<path transform="translate({x} {y}) scale({size / 24})" fill="{color}" d="{d}"/>'


def frame(w, h, body, glow='88%'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D1424"/><stop offset="1" stop-color="#070B16"/></linearGradient>
    <radialGradient id="g1" cx="{glow}" cy="0%" r="60%"><stop offset="0" stop-color="{CYAN}" stop-opacity=".16"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx="0%" cy="100%" r="55%"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".12"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
    <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#fff" stroke-opacity=".03"/></pattern>
    <clipPath id="c"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="24"/></clipPath>
  </defs>
  <g clip-path="url(#c)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/><rect width="{w}" height="{h}" fill="url(#grid)"/>
    <rect width="{w}" height="{h}" fill="url(#g1)"/><rect width="{w}" height="{h}" fill="url(#g2)"/>
    <rect x="120" y="0" width="{w - 240}" height="2" fill="url(#edge)"/>
  </g>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="24" fill="none" stroke="{CYAN}" stroke-opacity=".22" stroke-width="1.5"/>
{body}
</svg>
'''


# ---------- technologies ----------
GROUPS = [
    (('LENGUAJES', 'LANGUAGES', 'LLENGUATGES'), '#F7DF1E', [('javascript', 'JavaScript', '#F7DF1E'), ('typescript', 'TypeScript', '#3178C6'), ('php', 'PHP', '#8892BF'),
                              ('mysql', 'SQL', '#4479A1'), ('html5', 'HTML', '#E34F26'), ('css', 'CSS', '#663399')]),
    (('FRONTEND', 'FRONTEND', 'FRONTEND'), '#61DAFB', [('react', 'React', '#61DAFB'), ('nextdotjs', 'Next.js', '#FFFFFF'), ('svelte', 'Svelte', '#FF3E00'),
                             ('threedotjs', 'Three.js', '#FFFFFF'), ('tailwindcss', 'Tailwind CSS', '#06B6D4'), ('electron', 'Electron', '#47848F')]),
    (('BACKEND Y DATOS', 'BACKEND & DATA', 'BACKEND I DADES'), '#FF2D20', [('laravel', 'Laravel', '#FF2D20'), ('nodedotjs', 'Node.js', '#5FA04E'), ('postgresql', 'PostgreSQL', '#4169E1'),
                                    ('mysql', 'MySQL', '#4479A1'), ('supabase', 'Supabase', '#3FCF8E')]),
    (('HERRAMIENTAS', 'TOOLS', 'EINES'), '#A855F7', [('git', 'Git', '#F05032'), ('vite', 'Vite', '#9135FF'), ('vitest', 'Vitest', '#6E9F18'),
                                 ('cloudflare', 'Cloudflare', '#F38020'), ('godotengine', 'Godot', '#478CBF'), ('claude', 'Claude Code', '#D97757')]),
]


def stack(lang):
    W, H, colw, x0 = 1200, 500, 270, 48
    title, sub = {'es': ('Tecnologías', 'LO QUE USO CADA DÍA'), 'en': ('Tech stack', 'WHAT I USE EVERY DAY'),
                  'ca': ('Tecnologies', 'EL QUE FAIG SERVIR CADA DIA')}[lang]
    out = [f'  <text x="48" y="64" font-family="{FONT}" font-size="30" font-weight="700" fill="#FFFFFF">{title}</text>',
           f'  <text x="1152" y="62" text-anchor="end" font-family="{MONO}" font-size="14" fill="#94A3B8" letter-spacing="1.5">{sub}</text>']
    for gi, (titles, gc, items) in enumerate(GROUPS):
        title = titles[('es', 'en', 'ca').index(lang)]
        x = x0 + gi * (colw + 16)
        out.append(f'  <rect x="{x}" y="96" width="{colw}" height="{H - 132}" rx="18" fill="#0B1222" fill-opacity=".7" stroke="{gc}" stroke-opacity=".22"/>')
        out.append(f'  <rect x="{x + 20}" y="120" width="22" height="3" rx="1.5" fill="{gc}"/>')
        out.append(f'  <text x="{x + 20}" y="146" font-family="{MONO}" font-size="14" font-weight="700" fill="{gc}" letter-spacing="2">{escape(title)}</text>')
        for i, (slug, name, c) in enumerate(items):
            y = 170 + i * 46
            out.append(f'  <rect x="{x + 18}" y="{y}" width="36" height="36" rx="10" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".35"/>')
            out.append('  ' + icon(slug, x + 26, y + 8, 20, c))
            out.append(f'  <text x="{x + 68}" y="{y + 24}" font-family="{FONT}" font-size="18" font-weight="600" fill="#E2E8F0">{escape(name)}</text>')
    return frame(W, H, '\n'.join(out))


# ---------- timelines ----------
CAREER = [
    ('ENE 2026 – HOY', 'Desarrollo de producto y formación', 'Proyectos propios', '#22D3EE',
     'Productos propios de la idea a producción, sobre todo Orbex, publicado en Google Play.'),
    ('AGO 2025 – ENE 2026', 'Desarrollador de software', 'Grup Romeu', '#A855F7',
     'Full-stack con PHP y JavaScript: aplicación interna para gestionar material quirúrgico.'),
    ('MAY 2023 – ABR 2025', 'Desarrollador de software', 'Nemon', '#F97316',
     'Soluciones a medida para distribuidoras de electricidad y gas sobre un framework propio en PHP.'),
    ('NOV 2019 – ABR 2023', 'Release Manager y Desarrollador', 'VIEWNEXT', '#3B82F6',
     'Releases en grandes empresas: Salesforce (Nestlé), Copado (CaixaBank) y Jenkins (Naturgy).'),
    ('FEB – JUN 2018', 'Desarrollador de software (prácticas)', 'C. R. Pantà de Riudecanyes', '#10B981',
     '400 h manteniendo y mejorando software de gestión de usuarios y base de datos.'),
]
EDUCATION = [
    ('MAY 2025', 'Bootcamp Frontend Developer', 'Lemoncoders', '#22D3EE', 'JavaScript, TypeScript, HTML, CSS y React.'),
    ('JUL – SEP 2019', 'Bootcamp PHP', 'Fundació Esplai', '#8892BF', '275 h presenciales: PHP y Laravel.'),
    ('ABR – JUN 2019', 'Bootcamp Java', 'Fundació Esplai', '#F97316', '275 h presenciales: Java y SQL.'),
    ('2015 – 2018', 'CFGS Desarrollo de Aplicaciones Web (DAW)', 'INS Baix Camp', '#A855F7', 'Ciclo formativo de grado superior.'),
    ('2008 – 2014', 'ESO y Bachillerato Tecnológico', 'INS Domènech i Montaner', '#64748B', ''),
]


def timeline(title, sub, rows):
    W, step, top = 1200, 88, 116
    # the last entry only needs room for its own lines
    last = 30 + 24 * len(textwrap.wrap(rows[-1][4], 100)[:2])
    H = top + step * (len(rows) - 1) + last + 34
    out = [f'  <text x="48" y="64" font-family="{FONT}" font-size="30" font-weight="700" fill="#FFFFFF">{escape(title)}</text>',
           f'  <text x="1152" y="62" text-anchor="end" font-family="{MONO}" font-size="14" fill="#94A3B8" letter-spacing="1.5">{escape(sub)}</text>',
           f'  <rect x="279" y="{top}" width="2" height="{step * (len(rows) - 1) + 20}" fill="#334155"/>']
    for i, (period, role, place, c, desc) in enumerate(rows):
        y = top + i * step
        out.append(f'  <text x="252" y="{y + 18}" text-anchor="end" font-family="{MONO}" font-size="14" font-weight="700" fill="{c}" letter-spacing="1">{escape(period)}</text>')
        out.append(f'  <circle cx="280" cy="{y + 13}" r="13" fill="{c}" fill-opacity=".15"/>')
        out.append(f'  <circle cx="280" cy="{y + 13}" r="6" fill="{c}" stroke="#070B16" stroke-width="2"/>')
        out.append(f'  <text x="312" y="{y + 20}" font-family="{FONT}" font-size="21" font-weight="700" fill="#FFFFFF">{escape(role)}'
                   f'<tspan dx="10" fill="#64748B" font-weight="400">·</tspan><tspan dx="10" fill="{c}" font-weight="600">{escape(place)}</tspan></text>')
        for j, line in enumerate(textwrap.wrap(desc, 100)[:2]):
            out.append(f'  <text x="312" y="{y + 48 + j * 24}" font-family="{FONT}" font-size="17" fill="#94A3B8">{escape(line)}</text>')
    return frame(W, H, '\n'.join(out), glow='12%')


CAREER_EN = [
    ('JAN 2026 – NOW', 'Product development and training', 'Own projects',
     'Taking my own products from idea to production, most notably Orbex, published on Google Play.'),
    ('AUG 2025 – JAN 2026', 'Software Developer', 'Grup Romeu',
     'Full-stack development with PHP and JavaScript: an internal app for managing surgical equipment.'),
    ('MAY 2023 – APR 2025', 'Software Developer', 'Nemon',
     'Custom solutions for electricity and gas distributors, built on an in-house PHP framework.'),
    ('NOV 2019 – APR 2023', 'Release Manager and Developer', 'VIEWNEXT',
     'Release management for large clients: Salesforce (Nestlé), Copado (CaixaBank) and Jenkins (Naturgy).'),
    ('FEB – JUN 2018', 'Software Developer (internship)', 'C. R. Pantà de Riudecanyes',
     '400 hours maintaining and improving user-management and database software.'),
]
EDUCATION_EN = [
    ('MAY 2025', 'Frontend Developer Bootcamp', 'Lemoncoders', 'JavaScript, TypeScript, HTML, CSS and React.'),
    ('JUL – SEP 2019', 'PHP Bootcamp', 'Fundació Esplai', '275 on-site hours: PHP and Laravel.'),
    ('APR – JUN 2019', 'Java Bootcamp', 'Fundació Esplai', '275 on-site hours: Java and SQL.'),
    ('2015 – 2018', 'Higher Technician in Web Application Development (DAW)', 'INS Baix Camp', 'Two-year higher vocational training programme.'),
    ('2008 – 2014', 'Secondary Education and Technology Baccalaureate', 'INS Domènech i Montaner', ''),
]

CAREER_CA = [
    ('GEN. 2026 – ARA', 'Desenvolupament de producte i formació', 'Projectes propis',
     'Productes propis de la idea a producció, sobretot Orbex, publicat a Google Play.'),
    ('AG. 2025 – GEN. 2026', 'Desenvolupador de programari', 'Grup Romeu',
     'Full-stack amb PHP i JavaScript: aplicació interna per gestionar material quirúrgic.'),
    ('MAIG 2023 – ABR. 2025', 'Desenvolupador de programari', 'Nemon',
     'Solucions a mida per a distribuïdores d’electricitat i gas sobre un framework propi en PHP.'),
    ('NOV. 2019 – ABR. 2023', 'Release Manager i desenvolupador', 'VIEWNEXT',
     'Releases per a grans empreses: Salesforce (Nestlé), Copado (CaixaBank) i Jenkins (Naturgy).'),
    ('FEBR. – JUNY 2018', 'Desenvolupador de programari (pràctiques)', 'C. R. Pantà de Riudecanyes',
     '400 h mantenint i millorant programari de gestió d’usuaris i base de dades.'),
]
EDUCATION_CA = [
    ('MAIG 2025', 'Bootcamp Frontend Developer', 'Lemoncoders', 'JavaScript, TypeScript, HTML, CSS i React.'),
    ('JUL. – SET. 2019', 'Bootcamp PHP', 'Fundació Esplai', '275 h presencials: PHP i Laravel.'),
    ('ABR. – JUNY 2019', 'Bootcamp Java', 'Fundació Esplai', '275 h presencials: Java i SQL.'),
    ('2015 – 2018', 'CFGS Desenvolupament d’Aplicacions Web (DAW)', 'INS Baix Camp', 'Cicle formatiu de grau superior.'),
    ('2008 – 2014', 'ESO i Batxillerat Tecnològic', 'INS Domènech i Montaner', ''),
]


def translated(rows, texts):
    # same colours as the Spanish rows, translated text
    return [(period, role, place, row[3], desc) for row, (period, role, place, desc) in zip(rows, texts)]


open('assets/stack.svg', 'w', encoding='utf8').write(stack('es'))
open('assets/career.svg', 'w', encoding='utf8').write(timeline('Trayectoria', 'MÁS DE 5 AÑOS EN PRODUCCIÓN', CAREER))
open('assets/education.svg', 'w', encoding='utf8').write(timeline('Formación', 'TÉCNICO SUPERIOR · BOOTCAMPS', EDUCATION))
os.makedirs('assets/en', exist_ok=True)
open('assets/en/stack.svg', 'w', encoding='utf8').write(stack('en'))
open('assets/en/career.svg', 'w', encoding='utf8').write(timeline('Experience', '5+ YEARS SHIPPING TO PRODUCTION', translated(CAREER, CAREER_EN)))
open('assets/en/education.svg', 'w', encoding='utf8').write(timeline('Education', 'HIGHER VOCATIONAL DEGREE · BOOTCAMPS', translated(EDUCATION, EDUCATION_EN)))
os.makedirs('assets/ca', exist_ok=True)
open('assets/ca/stack.svg', 'w', encoding='utf8').write(stack('ca'))
open('assets/ca/career.svg', 'w', encoding='utf8').write(timeline('Trajectòria', 'MÉS DE 5 ANYS EN PRODUCCIÓ', translated(CAREER, CAREER_CA)))
open('assets/ca/education.svg', 'w', encoding='utf8').write(timeline('Formació', 'TÈCNIC SUPERIOR · BOOTCAMPS', translated(EDUCATION, EDUCATION_CA)))
print('ok')
