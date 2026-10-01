"""Renderers for the SVGs that change with your GitHub activity."""
import math
import random

from neon import *  # noqa: F401,F403
from neon import _n

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DASH = "--"
FLAME = "M0 -24C7 -13 13 -7 11 4C10 13 3 18 0 18C-5 18 -11 12 -11 4C-11 -3 -7 -7 -4 -13C-2 -9 -1 -7 1 -7C3 -13 0 -17 0 -24Z"


def fmt(v):
    return DASH if v is None else f"{v:,}"


def _glyph_commit(cx, cy, col):
    return (f'<g transform="translate({cx} {cy})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round">'
            '<circle r="6"/><path d="M-14 0H-6M6 0H14"/></g>')


def _glyph_pr(cx, cy, col):
    return (f'<g transform="translate({cx} {cy})" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round">'
            '<circle cx="-7" cy="-8" r="3.2"/><circle cx="-7" cy="9" r="3.2"/><circle cx="8" cy="9" r="3.2"/>'
            '<path d="M-7 -4.8V5.8M-7 -1Q-7 4 8 5.6"/></g>')


def _glyph_star(cx, cy, col):
    pts = []
    for k in range(10):
        r = 12 if k % 2 == 0 else 5.2
        a = -math.pi / 2 + k * math.pi / 5
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{col}"/>'


def _glyph_repo(cx, cy, col):
    return (f'<g transform="translate({cx} {cy})" fill="none" stroke="{col}" stroke-width="2" stroke-linejoin="round">'
            '<path d="M-9 -11H7Q10 -11 10 -8V10H-6Q-9 10 -9 7Z"/><path d="M-9 7Q-9 4 -6 4H10"/><path d="M-3 -5H4" stroke-linecap="round"/></g>')


def stats(d):
    W, H = 900, 446
    b = [panel(W, H, CYAN)]

    def big(cx, cy, value, label, sub, col):
        s = fit("orb", value, 50, 230, 1)
        return (glow_text("orb", value, s, cx, cy, col, "middle", 1, "g8", ".5")
                + txt("raj", label, 15, cx, cy + 32, TEXT, "middle", 4)
                + txt("mono", sub, 14, cx, cy + 56, DIM, "middle", .5))

    b.append(big(160, 150, fmt(d.get("total")), "TOTAL CONTRIBUTIONS", d.get("since_label", ""), CYAN))
    b.append(big(740, 150, fmt(d.get("longest")), "LONGEST STREAK", d.get("longest_range", ""), MAG))
    cx, cy = 450, 134
    v = fmt(d.get("cur"))
    b.append(f'<circle cx="{cx}" cy="{cy}" r="82" fill="{YEL}" opacity=".07" filter="url(#g16)">{blink(lo=.04, hi=.16, dur=4)}</circle>'
             f'<circle cx="{cx}" cy="{cy}" r="66" fill="{BG}" stroke="{YEL}" stroke-opacity=".35" stroke-width="2"/>'
             f'<circle cx="{cx}" cy="{cy}" r="66" fill="none" stroke="{YEL}" stroke-width="5" stroke-linecap="round" stroke-dasharray="60 355" filter="url(#g3)">'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="5s" repeatCount="indefinite"/></circle>'
             f'<circle cx="{cx}" cy="{cy}" r="57" fill="none" stroke="{CYAN}" stroke-opacity=".3" stroke-dasharray="2 6"/>'
             f'<g transform="translate({cx} {cy - 40}) scale(.7)"><g>'
             '<animateTransform attributeName="transform" type="scale" values="1 1;1.08 .93;.95 1.08;1 1" dur="1.2s" repeatCount="indefinite"/>'
             f'<path d="{FLAME}" fill="#ff7a1a"/><g transform="scale(.66)"><path d="{FLAME}" fill="#ffd23a"/></g></g></g>')
    b.append(glow_text("orb", v, fit("orb", v, 44, 90, 0), cx, cy + 30, YEL, "middle", 0, "g8", ".5"))
    b.append(txt("raj", "CURRENT STREAK", 15, cx, cy + 100, YEL, "middle", 4))
    b.append(txt("mono", d.get("cur_range", ""), 14, cx, cy + 122, DIM, "middle", .5))
    b.append(f'<rect x="60" y="283" width="{W - 120}" height="1" fill="url(#neon)" opacity=".6"/>')

    cols = [(_glyph_commit, fmt(d.get("commits")), "COMMITS / 12 MO", CYAN),
            (_glyph_pr, fmt(d.get("prs")), "PULL REQUESTS", MAG),
            (_glyph_star, fmt(d.get("stars")), "STARS EARNED", YEL),
            (_glyph_repo, fmt(d.get("repos")), "PUBLIC REPOS", VIO)]
    for i, (g, val, lab, col) in enumerate(cols):
        x = 112 + i * 225
        b.append(f'<path d="{cut_rect(x - 24, 306, 48, 48, 9)}" fill="{col}" fill-opacity=".08" stroke="{col}" stroke-opacity=".7"/>')
        b.append(g(x, 330, col))
        b.append(glow_text("orb", val, fit("orb", val, 30, 170, 1), x, 386, col, "middle", 1, "g8", ".4"))
        b.append(txt("raj", lab, 13, x, 408, TEXT, "middle", 3))
    b.append(txt("mono", d.get("updated_label", "// awaiting first sync"), 12, W - 30, H - 12, DIM, "end", .5))
    return svg(W, H, "".join(b), "", "GitHub stats: contributions, current and longest streak, commits, pull requests, stars and repositories")


PALETTE = [CYAN, MAG, YEL, VIO, "#00ff9c", "#ff7a1a"]


def langs(d):
    rows = (d.get("langs") or [])[:6]
    placeholder = not rows
    n = len(rows)
    W, H = 900, (170 if placeholder else 96 + n * 44 + 10)
    b = [panel(W, H, MAG),
         txt("orbb", "LANGUAGES BY SHARE", 15, 40, 50, MAG, "start", 4),
         txt("mono", "// bytes across public repositories", 14, W - 40, 50, DIM, "end", .5),
         f'<rect x="40" y="62" width="{W - 80}" height="1" fill="{MAG}" opacity=".4"/>']
    bx, bw = 250, 500
    for i, (name, pct) in enumerate(rows):
        y = 86 + i * 44
        col = PALETTE[i % len(PALETTE)]
        fw = max(16, bw * pct / 100)
        b.append(f'<rect x="40" y="{y + 3}" width="8" height="8" fill="{col}"/>')
        b.append(txt("rajb", name.upper(), fit("rajb", name.upper(), 16, 170, 2), 60, y + 14, TEXT, "start", 2))
        b.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="16" fill="#0a0d1f" stroke="{col}" stroke-opacity=".35"/>')
        b.append(f'<rect x="{bx}" y="{y}" width="{fw:.0f}" height="16" fill="{col}" opacity=".9"/>')
        for sx in range(bx + 10, bx + int(fw), 10):   # segmented look
            b.append(f'<rect x="{sx}" y="{y}" width="2" height="16" fill="{BG}" opacity=".55"/>')
        b.append(f'<clipPath id="c{i}"><rect x="{bx}" y="{y}" width="{fw:.0f}" height="16"/></clipPath>'
                 f'<g clip-path="url(#c{i})"><rect y="{y}" width="50" height="16" fill="#fff" opacity=".45">'
                 f'<animate attributeName="x" values="{bx - 50};{bx + fw:.0f}" dur="{3 + i * .5:.1f}s" begin="-{i * .8:.1f}s" repeatCount="indefinite"/></rect></g>')
        b.append(txt("mono", f"{pct:.1f}%", 16, W - 40, y + 14, col, "end", 1))
    if placeholder:
        b.append(txt("mono", "// counting bytes... awaiting first sync", 18, 450, 120, CYAN, "middle", 1))
    return svg(W, H, "".join(b), "", "Languages by share of code: " + (", ".join(f"{a} {p:.0f}%" for a, p in rows) or "not yet counted"))


LEVELS = ["#111735", "#0a4d66", "#08a7c4", "#00f0ff", "#ff7bf0"]


def heatmap(d):
    weeks = d.get("weeks")
    W, H = 900, 240
    c, g, x0, y0 = 12, 3, 84, 94
    placeholder = not weeks
    if placeholder:
        weeks = [[(None, 0)] * 7 for _ in range(53)]
    mx = max((cnt for wk in weeks for _, cnt in wk), default=0)
    total = d.get("year_total")
    defs = ('<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    b = [panel(W, H, CYAN),
         txt("orbb", "CONTRIBUTION MATRIX", 15, 40, 50, CYAN, "start", 4),
         txt("mono", (f"{total:,} contributions in the past year" if total is not None else "// the past year, day by day"), 14, W - 40, 50, DIM, "end", .5),
         f'<rect x="40" y="62" width="{W - 80}" height="1" fill="{CYAN}" opacity=".4"/>']
    rng = random.Random(5)
    prev, last_x = None, -99
    for ci, wk in enumerate(weeks):
        x = x0 + ci * (c + g)
        first = wk[0][0]
        if first:
            m = int(first[5:7]) - 1
            if m != prev:
                if ci < len(weeks) - 2 and x - last_x >= 40:
                    b.append(txt("mono", MONTHS[m].upper(), 11, x, 84, DIM, "start", 1))
                    last_x = x
                prev = m
        for ri, (_, cnt) in enumerate(wk):
            lvl = 0 if cnt <= 0 or mx == 0 else max(1, min(4, math.ceil(4 * cnt / mx)))
            y = y0 + ri * (c + g)
            if lvl == 4 and rng.random() < .4:
                b.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" rx="2" fill="{LEVELS[4]}">'
                         f'<animate attributeName="fill" values="{LEVELS[4]};#ffffff;{LEVELS[4]}" dur="{rng.uniform(2, 5):.1f}s" begin="-{rng.uniform(0, 4):.1f}s" repeatCount="indefinite"/></rect>')
            else:
                b.append(f'<rect x="{x}" y="{y}" width="{c}" height="{c}" rx="2" fill="{LEVELS[lvl]}"/>')
    for ri, lab in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(txt("mono", lab, 10, x0 - 8, y0 + ri * (c + g) + 10, DIM, "end", .5))
    gw = 53 * (c + g)
    b.append(f'<clipPath id="gridclip"><rect x="{x0}" y="{y0}" width="{gw}" height="{7 * (c + g)}"/></clipPath>'
             f'<g clip-path="url(#gridclip)"><rect y="{y0}" width="110" height="{7 * (c + g)}" fill="url(#beam)">'
             f'<animate attributeName="x" values="{x0 - 110};{x0 + gw}" dur="6s" repeatCount="indefinite"/></rect></g>')
    ly = H - 34
    lx = W - 40 - 5 * (c + 4) - 56
    b.append(txt("mono", "LESS", 10, lx, ly + 10, DIM, "end", 1))
    for i in range(5):
        b.append(f'<rect x="{lx + 10 + i * (c + 4)}" y="{ly}" width="{c}" height="{c}" rx="2" fill="{LEVELS[i]}"/>')
    b.append(txt("mono", "MORE", 10, lx + 16 + 5 * (c + 4), ly + 10, DIM, "start", 1))
    if placeholder:
        b.append(f'<rect x="240" y="118" width="420" height="52" fill="{BG}" fill-opacity=".92" stroke="{CYAN}" stroke-opacity=".6"/>'
                 + txt("mono", "// compiling contribution matrix...", 18, 450, 150, CYAN, "middle", 1))
    return svg(W, H, "".join(b), defs, "Contribution heatmap for the past year")
