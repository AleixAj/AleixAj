"""Language switch buttons for the top of both READMEs (drawn as SVG: GitHub allows no CSS).

Run from the repo root:  python tools/make_lang.py
Writes assets/lang-<en|es|ca>.svg (not selected) and assets/lang-<en|es|ca>-on.svg (selected).
"""
FONT = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', Consolas, 'SFMono-Regular', monospace"

# 36x24 flags, drawn at the origin
FLAGS = {
    'en': '''<clipPath id="fc"><rect width="36" height="24" rx="5"/></clipPath>
    <clipPath id="fd"><path d="M18 12H36V24zM18 12V24H0zM18 12H0V0zM18 12V0H36z"/></clipPath>
    <g clip-path="url(#fc)">
      <rect width="36" height="24" fill="#012169"/>
      <path d="M0 0L36 24M36 0L0 24" stroke="#fff" stroke-width="4.8"/>
      <path d="M0 0L36 24M36 0L0 24" stroke="#C8102E" stroke-width="2.4" clip-path="url(#fd)"/>
      <path d="M18 0V24M0 12H36" stroke="#fff" stroke-width="8"/>
      <path d="M18 0V24M0 12H36" stroke="#C8102E" stroke-width="4.8"/>
    </g>''',
    'es': '''<clipPath id="fc"><rect width="36" height="24" rx="5"/></clipPath>
    <g clip-path="url(#fc)">
      <rect width="36" height="24" fill="#AA151B"/>
      <rect y="6" width="36" height="12" fill="#F1BF00"/>
    </g>''',
    # the senyera: four red stripes on yellow
    'ca': '''<clipPath id="fc"><rect width="36" height="24" rx="5"/></clipPath>
    <g clip-path="url(#fc)">
      <rect width="36" height="24" fill="#FCDD09"/>
      <path d="M0 4H36M0 9.33H36M0 14.67H36M0 20H36" stroke="#DA121A" stroke-width="2.67"/>
    </g>''',
}
NAMES = {'en': ('English', 'EN'), 'es': ('Español', 'ES'), 'ca': ('Català', 'CA')}


def button(lang, on):
    W, H = 220, 64
    name, code = NAMES[lang]
    if on:
        border = '<rect x="5" y="5" width="210" height="54" rx="27" fill="none" stroke="url(#ac)" stroke-width="2"/>'
        shadow = '<filter id="sh" x="-20%" y="-40%" width="140%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#22d3ee" flood-opacity=".35"/></filter>'
        body, ink, sub = 'url(#bg)', '#FFFFFF', '#22D3EE'
        mark = '<circle cx="186" cy="32" r="9" fill="url(#ac)"/><path d="M182 32.2l2.8 2.8 5.2-5.6" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        border = '<rect x="5" y="5" width="210" height="54" rx="27" fill="none" stroke="#334155" stroke-width="1.5"/>'
        shadow = ''
        body, ink, sub = '#0B1222', '#CBD5E1', '#64748B'
        mark = '<path d="M183 26l6 6-6 6" fill="none" stroke="#64748B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1426"/><stop offset="1" stop-color="#060a16"/></linearGradient>
    <linearGradient id="ac" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#a855f7"/></linearGradient>
    {shadow}
  </defs>
  <rect x="5" y="5" width="210" height="54" rx="27" fill="{body}"{' filter="url(#sh)"' if on else ''}/>
  {border}
  <g transform="translate(22 20)">
    {FLAGS[lang]}
    <rect width="36" height="24" rx="5" fill="none" stroke="#fff" stroke-opacity=".25"/>
  </g>
  <text x="72" y="31" font-family="{FONT}" font-size="17" font-weight="700" fill="{ink}">{name}</text>
  <text x="72" y="48" font-family="{MONO}" font-size="11" font-weight="700" fill="{sub}" letter-spacing="2">{code}</text>
  {mark}
</svg>
'''


for lang in NAMES:
    open(f'assets/lang-{lang}.svg', 'w', encoding='utf8').write(button(lang, False))
    open(f'assets/lang-{lang}-on.svg', 'w', encoding='utf8').write(button(lang, True))
print('ok')
