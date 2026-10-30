# How this profile is built

GitHub allows no CSS in a README, so every piece of the profile that looks
designed is an SVG drawn by one of these scripts. Run them from the repo root;
they are deterministic, so running one twice changes nothing.

| Script | Writes | Run it after changing |
| --- | --- | --- |
| `make_cards.py` | `assets/cards/` (and `en`, `ca`) plus `tools/projects.*.html` | a project, its description, its tags or its buttons |
| `make_sections.py` | `assets/stack.svg`, `career.svg`, `education.svg` (and `en`, `ca`) | the tech list, a job or a course |
| `make_narrow.py` | `assets/narrow/` (and `en`, `ca`) | anything the two above draw: these are their phone versions |
| `make_lang.py` | `assets/lang-*.svg` | the language switch at the top |
| `make_social.py` | `assets/social/*.png` | a project, if you want its link preview updated |

`make_narrow.py` and `make_social.py` import the other two, so they rewrite
their output as well. After touching a project, the full pass is:

```
python tools/make_cards.py && python tools/make_narrow.py && python tools/make_social.py
```

Then paste `tools/projects.<lang>.html` into the matching README, between the
`Proyectos destacados` heading and the `Más proyectos…` line.

## Two things that are easy to break

**Sizes are in pixels, not percentages.** GitHub caps an image at the width of
its column but never scales a smaller one up. A card asked for at `410` is
410px on a desktop and 308px on a phone, which still reads; the same card at
`49%` would be 150px on a phone, where nothing inside it can be read. If you
add an image to the README, give it a pixel width.

**One project per row.** The card and its own two buttons go in the same
`<p>`. Two projects in one row would put four buttons under two cards, and a
phone, which stacks everything into one column, then shows the four in a heap
with no way to tell which card each belongs to.

## The phone versions

The header and the three panels are 1200-1280px of artwork. On a phone they
are drawn at 308px, which puts their text at 4px, so `make_narrow.py` redraws
them for one column and the README picks between them:

```html
<picture>
  <source media="(max-width: 620px)" srcset="assets/narrow/stack.svg">
  <img src="assets/stack.svg" width="100%" alt="…">
</picture>
```

The buttons use the same mechanism with a different breakpoint
(`max-width: 1279px`), because what decides there is not legibility but
whether the column is wide enough to fit the card and its buttons on one line,
and that only happens from GitHub's 1280px breakpoint up.

Two rules the markup has to follow:

- A `<picture>` at the top level of the document has to be on **one line**.
  Markdown treats the indented lines of a multi-line one as separate blocks and
  breaks the element apart. Inside a `<p align="center">` block it can span
  lines, which is why the panels are written that way and the header is not.
- The `<img>` fallback is the version a reader gets if `media` is ignored, so
  it is the wide one for the panels and the tall one for the buttons: the worst
  case is then small text or some empty space, never a broken layout.

## Fonts

The scripts measure text with Segoe UI from `C:/Windows/Fonts` to decide where
to break a line and how wide a tag pill is. On a machine without those fonts
the SVG scripts fall back to a rough estimate, which is good enough, but
`make_social.py` needs them and will stop.
