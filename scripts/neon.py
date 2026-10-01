"""neon.py - tiny SVG toolkit for the cyberpunk profile README.

All lettering is converted to vector outlines with fontTools, so the SVGs look
identical everywhere (GitHub blocks external fonts inside images).
Fonts in scripts/fonts are Orbitron, Rajdhani and Share Tech Mono (SIL OFL).
"""
import json
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))

FONT_FILES = {
    "orb": "orbitron-latin-900-normal.woff",    # big titles
    "orbb": "orbitron-latin-700-normal.woff",   # headings, numbers
    "raj": "rajdhani-latin-600-normal.woff",    # labels
    "rajb": "rajdhani-latin-700-normal.woff",
    "body": "rajdhani-latin-500-normal.woff",   # prose
    "mono": "share-tech-mono-latin-400-normal.woff",  # terminal text
}
_FONTS, _REG = {}, {}


def _font(k):
    if k not in _FONTS:
        f = TTFont(os.path.join(HERE, "fonts", FONT_FILES[k]))
        _FONTS[k] = (f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _FONTS[k]


def _n(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def _glyph(cm, ch):
    return cm.get(ord(ch)) or cm.get(32)


def width(fk, text, size, ls=0.0):
    gs, cm, upm = _font(fk)
    s = size / upm
    return sum(gs[_glyph(cm, c)].width * s + ls for c in text) - ls if text else 0.0


def txt(fk, text, size, x, y, fill, anchor="start", ls=0.0, extra=""):
    """Lettering as vectors; y is the baseline. Flat fills reuse glyphs via <use>."""
    gs, cm, upm = _font(fk)
    s = size / upm
    w = width(fk, text, size, ls)
    cx = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
    if not fill.startswith("url("):
        uses = []
        for ch in text:
            g = _glyph(cm, ch)
            gid = f"{fk}-{ord(ch):x}"
            if gid not in _REG:
                p = SVGPathPen(gs, ntos=lambda v: str(int(round(v))))
                gs[g].draw(p)
                _REG[gid] = p.getCommands()
            if _REG[gid]:
                uses.append(f'<use href="#{gid}" transform="translate({_n(cx)} {_n(y)}) scale({s:.4f} {-s:.4f})"/>')
            cx += gs[g].width * s + ls
        return f'<g fill="{fill}" {extra}>{"".join(uses)}</g>' if uses else ""
    pen = SVGPathPen(gs, ntos=_n)
    for ch in text:
        g = _glyph(cm, ch)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        cx += gs[g].width * s + ls
    d = pen.getCommands()
    return f'<path d="{d}" fill="{fill}" {extra}/>' if d else ""


def wrap(fk, text, size, maxw, ls=0.0):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if cur and width(fk, t, size, ls) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = t
    return lines + ([cur] if cur else [])


def para(fk, text, size, x, y, maxw, lh, fill, ls=0.0):
    lines = wrap(fk, text, size, maxw, ls)
    return "".join(txt(fk, l, size, x, y + i * lh, fill, "start", ls) for i, l in enumerate(lines)), len(lines)


def fit(fk, text, size, maxw, ls=0.0):
    w = width(fk, text, size, ls)
    return size if w <= maxw else size * maxw / w


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


ICONS = json.load(open(os.path.join(HERE, "icons.json")))
ICONS["db"] = "M12 2C7.6 2 4 3.3 4 5s3.6 3 8 3 8-1.3 8-3-3.6-3-8-3zM4 8v4c0 1.7 3.6 3 8 3s8-1.3 8-3V8c0 1.7-3.6 3-8 3S4 9.7 4 8zm0 7v4c0 1.7 3.6 3 8 3s8-1.3 8-3v-4c0 1.7-3.6 3-8 3s-8-1.3-8-3z"

# ------------------------------------------------------------------ palette
BG, PANEL = "#05060f", "#0a0d1f"
CYAN, MAG, YEL, VIO = "#00f0ff", "#ff2bd6", "#fcee0a", "#8a3dff"
TEXT, DIM = "#d6ecff", "#6b7aa8"

COMMON = f"""
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAG}"/></linearGradient>
<linearGradient id="neonV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{MAG}"/></linearGradient>
<linearGradient id="panel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d1128"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MAG}"/><stop offset="1" stop-color="{MAG}" stop-opacity="0"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".28"/></pattern>
<filter id="g3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="g8" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="g16" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>
"""


def svg(w, h, body, defs="", title=""):
    glyphs = "".join(f'<path id="{i}" d="{d}"/>' for i, d in _REG.items())
    _REG.clear()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f"<defs>{COMMON}{defs}{glyphs}</defs>{body}</svg>")


def glow_text(fk, text, size, x, y, fill, anchor="start", ls=0.0, blur="g8", op=".55"):
    """Neon lettering: blurred halo underneath, crisp text on top."""
    return (txt(fk, text, size, x, y, fill if not fill.startswith("url(") else CYAN, anchor, ls,
                f'opacity="{op}" filter="url(#{blur})"')
            + txt(fk, text, size, x, y, fill, anchor, ls))


def cut_rect(x, y, w, h, c=14):
    """Rectangle with two chamfered corners (top-left, bottom-right)."""
    return (f"M{x + c} {y}H{x + w}V{y + h - c}L{x + w - c} {y + h}H{x}V{y + c}Z")


def panel(w, h, accent=CYAN, c=16):
    """Dark chamfered plate with a neon rim and corner ticks."""
    d = cut_rect(1.5, 1.5, w - 3, h - 3, c)
    return (f'<path d="{d}" fill="url(#panel)"/>'
            f'<path d="{d}" fill="none" stroke="{accent}" stroke-opacity=".18" stroke-width="5" filter="url(#g3)"/>'
            f'<path d="{d}" fill="none" stroke="{accent}" stroke-opacity=".85" stroke-width="1.4"/>'
            f'<path d="{d}" fill="url(#scan)" opacity=".5"/>'
            f'<rect x="{w - 46}" y="1.5" width="30" height="3" fill="{MAG}"/>'
            f'<rect x="16" y="{h - 4.5}" width="30" height="3" fill="{CYAN}"/>')


def icon(name, cx, cy, size, fill):
    return (f'<g transform="translate({_n(cx - size / 2)} {_n(cy - size / 2)}) scale({size / 24:.3f})">'
            f'<path d="{ICONS[name]}" fill="{fill}"/></g>')


def blink(attr="opacity", lo=.3, hi=1, dur=2.0, begin=0.0):
    return f'<animate attributeName="{attr}" values="{lo};{hi};{lo}" dur="{dur}s" begin="-{begin:.1f}s" repeatCount="indefinite"/>'


def divider_line(cx, y, half):
    return (f'<rect x="{cx - half}" y="{y - .7}" width="{half - 14}" height="1.4" fill="url(#fadeL)"/>'
            f'<rect x="{cx + 14}" y="{y - .7}" width="{half - 14}" height="1.4" fill="url(#fadeR)"/>'
            f'<path d="M{cx - 9} {y}L{cx} {y - 6}L{cx + 9} {y}L{cx} {y + 6}Z" fill="{YEL}">{blink(lo=.55, dur=2.4)}</path>')
