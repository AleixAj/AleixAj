"""Technologies, career and education panels for the profile README (drawn as SVG: GitHub allows no CSS).

Run from the repo root:  python tools/make_sections.py
Icons: Simple Icons (CC0), saved in tools/icons.
"""
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
    ('LENGUAJES', '#F7DF1E', [('javascript', 'JavaScript', '#F7DF1E'), ('typescript', 'TypeScript', '#3178C6'), ('php', 'PHP', '#8892BF'),
                              ('mysql', 'SQL', '#4479A1'), ('html5', 'HTML', '#E34F26'), ('css', 'CSS', '#663399')]),
    ('FRONTEND', '#61DAFB', [('react', 'React', '#61DAFB'), ('nextdotjs', 'Next.js', '#FFFFFF'), ('svelte', 'Svelte', '#FF3E00'),
                             ('threedotjs', 'Three.js', '#FFFFFF'), ('tailwindcss', 'Tailwind CSS', '#06B6D4'), ('electron', 'Electron', '#47848F')]),
    ('BACKEND Y DATOS', '#FF2D20', [('laravel', 'Laravel', '#FF2D20'), ('nodedotjs', 'Node.js', '#5FA04E'), ('postgresql', 'PostgreSQL', '#4169E1'),
                                    ('mysql', 'MySQL', '#4479A1'), ('supabase', 'Supabase', '#3FCF8E')]),
    ('HERRAMIENTAS', '#A855F7', [('git', 'Git', '#F05032'), ('vite', 'Vite', '#9135FF'), ('vitest', 'Vitest', '#6E9F18'),
                                 ('cloudflare', 'Cloudflare', '#F38020'), ('godotengine', 'Godot', '#478CBF'), ('claude', 'Claude Code', '#D97757')]),
]


def stack():
    W, H, colw, x0 = 1200, 500, 270, 48
    out = ['  <text x="48" y="64" font-family="{}" font-size="30" font-weight="700" fill="#FFFFFF">Tecnologías</text>'.format(FONT),
           f'  <text x="1152" y="62" text-anchor="end" font-family="{MONO}" font-size="14" fill="#94A3B8" letter-spacing="1.5">LO QUE USO CADA DÍA</text>']
    for gi, (title, gc, items) in enumerate(GROUPS):
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
    ('AGO 2025 – ENE 2026', 'Desarrollador de Software', 'Grup Romeu', '#A855F7',
     'Full-stack con PHP y JavaScript: aplicación interna para gestionar material quirúrgico.'),
    ('MAY 2023 – ABR 2025', 'Desarrollador de Software', 'Nemon', '#F97316',
     'Soluciones a medida para distribuidoras de electricidad y gas sobre un framework propio en PHP.'),
    ('NOV 2019 – ABR 2023', 'Release Manager y Desarrollador', 'VIEWNEXT', '#3B82F6',
     'Releases en entornos corporativos: Salesforce (Nestlé), COPADO (CaixaBank), Bitbucket y Jenkins (Naturgy).'),
    ('FEB – JUN 2018', 'Desarrollador de Software (prácticas)', 'C. R. Pantà de Riudecanyes', '#10B981',
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
    W, step, top = 1200, 104, 120
    H = top + step * len(rows) + 10
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


open('assets/stack.svg', 'w', encoding='utf8').write(stack())
open('assets/career.svg', 'w', encoding='utf8').write(timeline('Trayectoria', 'MÁS DE 6 AÑOS EN PRODUCCIÓN', CAREER))
open('assets/education.svg', 'w', encoding='utf8').write(timeline('Formación', 'TÉCNICO SUPERIOR · BOOTCAMPS', EDUCATION))
print('ok')
