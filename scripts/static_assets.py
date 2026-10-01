"""Renderers for the hand-authored, never-changing SVG assets."""
import random

from neon import *  # noqa: F401,F403
from neon import _n

NAME = "HARSHIL SHAH"
ROLES = ["FULL-STACK DEVELOPER", "COMPETITIVE PROGRAMMER", "CSE STUDENT", "MERN STACK BUILDER"]
ACCENTS = [CYAN, MAG, YEL, VIO]


# ------------------------------------------------------------------ header
def _skyline(rng, y0, x0, x1, hmin, hmax, fill, rim, win_p, centre_dip=True):
    out, x = [], x0
    while x < x1:
        w = rng.randint(28, 64)
        f = min(1.0, abs(x + w / 2 - 600) / 380) if centre_dip else 1.0
        h = int(hmin + f * rng.random() * (hmax - hmin))
        if centre_dip and abs(x + w / 2 - 600) < 150:
            h = 10
        top = y0 - h
        out.append(f'<rect x="{x}" y="{top}" width="{w - 3}" height="{h + 2}" fill="{fill}"/>')
        out.append(f'<rect x="{x}" y="{top}" width="{w - 3}" height="1.3" fill="{rim}" opacity=".55"/>')
        if rng.random() < .25 and h > 50:   # antenna with beacon
            ax = x + w // 2
            out.append(f'<rect x="{ax}" y="{top - 16}" width="1.2" height="16" fill="{fill}"/>'
                       f'<circle cx="{ax + .6}" cy="{top - 17}" r="1.8" fill="#ff2040">{blink(lo=.1, dur=rng.uniform(1.2, 2.4), begin=rng.uniform(0, 2))}</circle>')
        for wx in range(x + 5, x + w - 8, 8):
            for wy in range(top + 7, y0 - 4, 9):
                if rng.random() < win_p:
                    col = rng.choice([CYAN, CYAN, MAG, YEL])
                    anim = blink(lo=.15, dur=rng.uniform(2, 6), begin=rng.uniform(0, 5)) if rng.random() < .08 else ""
                    out.append(f'<rect x="{wx}" y="{wy}" width="3" height="4" fill="{col}" opacity=".8">{anim}</rect>'
                               if anim else f'<rect x="{wx}" y="{wy}" width="3" height="4" fill="{col}" opacity=".7"/>')
        x += w
    return "".join(out)


def header():
    W, H, HZ = 1200, 430, 300
    rng = random.Random(11)
    size = fit("orb", NAME, 88, 760, 6)
    sub = "FULL-STACK DEVELOPER  //  COMPETITIVE PROGRAMMER  //  CSE STUDENT"
    ssize = fit("rajb", sub, 21, 900, 5)
    tag = "Building web applications, solving problems, and constantly learning new technologies."
    boot = "> boot sequence // profile.init()"

    defs = f"""
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04040c"/><stop offset=".55" stop-color="#150834"/><stop offset="1" stop-color="#3a0b56"/></linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{YEL}"/><stop offset=".55" stop-color="#ff7a3d"/><stop offset="1" stop-color="{MAG}"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a0b4d"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<radialGradient id="scrim"><stop offset="0" stop-color="#04040c" stop-opacity=".78"/><stop offset="1" stop-color="#04040c" stop-opacity="0"/></radialGradient>
<radialGradient id="hglow"><stop offset="0" stop-color="{MAG}" stop-opacity=".55"/><stop offset="1" stop-color="{MAG}" stop-opacity="0"/></radialGradient>
"""
    b = [f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
    for _ in range(90):  # stars
        b.append(f'<circle cx="{rng.randint(0, W)}" cy="{rng.randint(0, HZ - 60)}" r="{rng.choice([.6, .8, 1.1])}" fill="#fff" opacity=".6">'
                 f'{blink(lo=.15, hi=.9, dur=rng.uniform(2, 6), begin=rng.uniform(0, 6))}</circle>')
    b.append(f'<ellipse cx="600" cy="{HZ}" rx="620" ry="120" fill="url(#hglow)">{blink(lo=.6, hi=1, dur=6)}</ellipse>')
    # retro sun with cut stripes
    b.append(f'<circle cx="600" cy="{HZ + 8}" r="64" fill="url(#sun)"/>')
    for k in range(6):
        b.append(f'<rect x="530" y="{248 + k * 11}" width="140" height="{1.2 + k * 1.1:.1f}" fill="#2a0b4d"/>')
    b.append(_skyline(rng, HZ, 0, W, 34, 125, "#0c0f2b", "#3a4dff", .18))
    b.append(_skyline(rng, HZ + 2, -10, W, 20, 70, "#06081a", MAG, .10))
    # floor
    b.append(f'<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>')
    for xb in range(-1400, 2600, 110):
        b.append(f'<line x1="600" y1="{HZ}" x2="{xb}" y2="{H}" stroke="{MAG}" stroke-opacity=".5" stroke-width="1"/>')
    n, dur = 8, 3.2
    for i in range(n):
        b.append(f'<rect x="0" y="{HZ}" width="{W}" height="1.6" fill="{CYAN}" opacity="0">'
                 f'<animate attributeName="y" values="{HZ};{H}" keyTimes="0;1" calcMode="spline" keySplines=".55 0 .95 .55" dur="{dur}s" begin="-{i * dur / n:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;.85;.85" keyTimes="0;.25;1" dur="{dur}s" begin="-{i * dur / n:.2f}s" repeatCount="indefinite"/></rect>')
    b.append(f'<rect y="{HZ - 1}" width="{W}" height="2" fill="{CYAN}" filter="url(#g3)"/><rect y="{HZ - .5}" width="{W}" height="1.2" fill="#fff" opacity=".9"/>')
    # title block
    b.append('<ellipse cx="600" cy="178" rx="560" ry="105" fill="url(#scrim)"/>')
    bw = width("mono", boot, 16, 1)
    b.append(txt("mono", boot, 16, 600, 78, CYAN, "middle", 1, 'opacity=".9"'))
    b.append(f'<rect x="{600 + bw / 2 + 6:.0f}" y="64" width="9" height="15" fill="{CYAN}">{blink(lo=0, hi=1, dur=1.1)}</rect>')
    b.append(divider_line(600, 98, 230))
    for dx, col in ((-3.5, MAG), (3.5, CYAN)):   # glitch ghosts
        b.append(f'<g transform="translate({dx} 0)" opacity=".85"><g>'
                 '<animateTransform attributeName="transform" type="translate" values="0 0;0 0;-6 1;5 -1;0 0;0 0;7 0;0 0" '
                 'keyTimes="0;.78;.79;.81;.83;.92;.93;1" dur="5.5s" repeatCount="indefinite"/>'
                 + txt("orb", NAME, size, 600, 170, col, "middle", 6) + "</g></g>")
    b.append(glow_text("orb", NAME, size, 600, 170, "#ffffff", "middle", 6, "g16", ".5"))
    b.append(txt("rajb", sub, ssize, 600, 208, TEXT, "middle", 5))
    b.append(txt("mono", tag, 15, 600, 238, DIM, "middle", .5))
    b.append(f'<rect width="{W}" height="{H}" fill="url(#scan)" opacity=".55"/>')
    b.append(f'<rect y="{H - 3}" width="{W}" height="3" fill="url(#neon)"/>')
    return svg(W, H, "".join(b), defs, f"{NAME.title()}: full-stack developer, competitive programmer and CSE student")


# ----------------------------------------------------- rotating role strip
def _cycle(i, n):
    t0, t1, e = i / n, (i + 1) / n, .02
    pts = [(0, 0), (t0, 0), (t0 + e, 1), (t1 - e, 1), (t1, 0), (1, 0)]
    kt, vs = [], []
    for k, v in pts:
        if kt and k < kt[-1]:
            k = kt[-1]
        kt.append(k)
        vs.append(v)
    return ";".join(f"{k:.3f}" for k in kt), ";".join(str(v) for v in vs)


def titles():
    W, H, dur = 900, 66, 12
    b = [panel(W, H, CYAN, 12)]
    b.append(txt("mono", "ROLE >", 15, 40, 40, MAG, "start", 2))
    for i, t in enumerate(ROLES):
        kt, vs = _cycle(i, len(ROLES))
        col = ACCENTS[i % 4]
        b.append(f'<g opacity="0"><animate attributeName="opacity" values="{vs}" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/>'
                 + glow_text("orbb", t, fit("orbb", t, 24, 640, 4), 450, 42, col, "middle", 4, "g8", ".6") + "</g>")
    b.append(f'<rect x="{W - 54}" y="26" width="10" height="16" fill="{CYAN}">{blink(lo=0, dur=1.1)}</rect>')
    return svg(W, H, "".join(b), "", " · ".join(r.title() for r in ROLES))


def divider():
    W, H = 900, 28
    b = [divider_line(450, 14, 420)]
    b.append(f'<rect y="12" width="70" height="4" fill="#fff" opacity="0" filter="url(#g3)">'
             f'<animate attributeName="x" values="30;800" dur="4s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="0;.8;0" dur="4s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "".join(b), "", "")


def section_header(idx, title, sub):
    W, H = 900, 70
    s = fit("orb", title, 27, 560, 3)
    b = [txt("mono", f"[{idx:02d}]", 18, 8, 42, MAG, "start", 1),
         glow_text("orb", title, s, 70, 43, CYAN, "start", 3, "g8", ".5"),
         txt("mono", f"// {sub}", 15, W - 8, 42, DIM, "end", 1),
         f'<rect x="8" y="58" width="{W - 16}" height="1.4" fill="url(#neon)" opacity=".9"/>',
         f'<rect x="8" y="55" width="46" height="7" fill="{MAG}"/>']
    return svg(W, H, "".join(b), "", title.replace("_", " "))


# ------------------------------------------------------------------- about
def about():
    W = 900
    rows = [("focus", "Full-Stack Web Development"),
            ("frontend", "React"),
            ("backend", "Node.js + Express.js"),
            ("databases", "MongoDB + SQL"),
            ("practice", "Data Structures & Algorithms in C++"),
            ("studying", "Operating Systems + Computer Networks"),
            ("building", "full-stack projects from scratch")]
    H = 120 + (len(rows) + 1) * 32
    b = [panel(W, H, CYAN)]
    for i, c in enumerate((MAG, YEL, CYAN)):
        b.append(f'<circle cx="{44 + i * 22}" cy="34" r="5.5" fill="{c}" opacity=".9"/>')
    b.append(txt("mono", "harshil@cyberdeck:/profile", 14, W - 40, 39, DIM, "end", 1))
    b.append(f'<rect x="30" y="52" width="{W - 60}" height="1" fill="{CYAN}" opacity=".25"/>')
    b.append(txt("mono", "$ whoami --verbose", 19, 40, 88, YEL, "start", 1))
    for i, (k, v) in enumerate(rows):
        y = 124 + i * 32
        b.append(txt("mono", f"{k:<10}", 18, 40, y, MAG, "start", .5))
        b.append(txt("mono", ":", 18, 168, y, DIM))
        b.append(txt("mono", v, 18, 190, y, TEXT, "start", .5))
    y = 124 + len(rows) * 32
    b.append(txt("mono", "$", 18, 40, y, YEL))
    b.append(f'<rect x="64" y="{y - 14}" width="10" height="18" fill="{CYAN}">{blink(lo=0, dur=1.1)}</rect>')
    return svg(W, H, "".join(b), "", "About: " + "; ".join(f"{k} {v}" for k, v in rows))


# ------------------------------------------------------------------- stack
def stack():
    W = 900
    rows = [("LANGUAGES", CYAN, [("c", "C"), ("cplusplus", "C++"), ("javascript", "JavaScript"), ("html5", "HTML5"), ("css3", "CSS3")]),
            ("FRONTEND", MAG, [("react", "React"), ("vite", "Vite")]),
            ("BACKEND", YEL, [("nodedotjs", "Node.js"), ("express", "Express.js")]),
            ("DATABASES", VIO, [("mongodb", "MongoDB"), ("db", "SQL")]),
            ("TOOLS", CYAN, [("git", "Git"), ("github", "GitHub"), ("visualstudiocode", "VS Code")])]
    rh = 84
    H = 40 + len(rows) * rh + 14
    b = [panel(W, H, MAG)]
    for r, (label, col, items) in enumerate(rows):
        cy = 40 + r * rh + rh / 2
        b.append(txt("orbb", label, 14, 40, cy + 5, col, "start", 3))
        b.append(f'<rect x="196" y="{cy - 26}" width="1.4" height="52" fill="{col}" opacity=".6"/>')
        for i, (ic, name) in enumerate(items):
            cx = 262 + i * 128
            b.append(f'<path d="{cut_rect(cx - 52, cy - 30, 104, 60, 9)}" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".5"/>')
            b.append(icon(ic, cx, cy - 8, 26, col))
            b.append(txt("raj", name, 14, cx, cy + 20, TEXT, "middle", 1))
        if r < len(rows) - 1:
            b.append(f'<rect x="30" y="{40 + (r + 1) * rh - 1}" width="{W - 60}" height="1" fill="{col}" opacity=".12"/>')
    b.append(f'<rect x="1" y="1" width="{W - 2}" height="3" fill="url(#neon)" opacity="0">'
             f'<animate attributeName="y" values="1;{H - 4}" dur="6s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values="0;.35;0" dur="6s" repeatCount="indefinite"/></rect>')
    alltxt = "; ".join(f"{l}: " + ", ".join(n for _, n in it) for l, _, it in rows)
    return svg(W, H, "".join(b), "", "Tech stack. " + alltxt)


# ---------------------------------------------------------------- projects
def project(num, title, desc, tech, accent):
    W = 900
    lines = wrap("body", desc, 19, 780)
    H = 100 + len(lines) * 26 + 62
    b = [panel(W, H, accent, 18)]
    b.append(glow_text("orb", f"{num:02d}", 46, 40, 74, accent, "start", 0, "g8", ".5"))
    b.append(txt("orb", title, fit("orb", title, 24, 640, 2), 118, 68, TEXT, "start", 2))
    b.append(f'<rect x="118" y="80" width="{W - 158}" height="1.2" fill="{accent}" opacity=".55"/>')
    for i, l in enumerate(lines):
        b.append(txt("body", l, 19, 40, 116 + i * 26, "#b8c7ea", "start", .3))
    x, y = 40, 116 + len(lines) * 26 + 18
    for t in tech:
        w = width("mono", t, 14, .5) + 28
        b.append(f'<path d="{cut_rect(x, y, w, 28, 7)}" fill="{accent}" fill-opacity=".1" stroke="{accent}" stroke-opacity=".75"/>')
        b.append(txt("mono", t, 14, x + w / 2, y + 19, accent, "middle", .5))
        x += w + 12
    b.append(f'<circle cx="{W - 36}" cy="34" r="4" fill="{accent}">{blink(lo=.2, dur=1.8, begin=num)}</circle>')
    return svg(W, H, "".join(b), "", f"{title}. {desc} Tech: {', '.join(tech)}.")


def projects():
    return [("project-gaming-tinder", project(1, "GAMING TINDER", "A full-stack application inspired by Tinder where users can swipe left or right on games and receive recommendations based on their preferences and swipe history.", ["React", "Node.js", "Express.js", "MongoDB"], CYAN)),
            ("project-product-gallery", project(2, "PRODUCT GALLERY", "A full-stack CRUD application for managing products with a React frontend and Node/Express backend.", ["React", "Node.js", "Express.js", "MongoDB"], MAG)),
            ("project-color-picker", project(3, "COLOR PICKER", "A React application for selecting and working with colors.", ["React", "JavaScript", "CSS"], YEL))]


# ------------------------------------------------------ competitive coding
def cp():
    W, H = 900, 170
    b = [panel(W, H, YEL)]
    code = ["while (alive) {", "    solve();", "    learn();", "}"]
    for i, l in enumerate(code):
        b.append(txt("mono", l, 20, 44, 62 + i * 28, [MAG, CYAN, CYAN, MAG][i], "start", .5))
    b.append(f'<rect x="64" y="{62 + 3 * 28 - 6}" width="10" height="18" fill="{YEL}">{blink(lo=0, dur=1.1)}</rect>')
    b.append(f'<rect x="420" y="30" width="1.4" height="110" fill="{YEL}" opacity=".5"/>')
    p, _ = para("body", "I regularly practice Data Structures & Algorithms and competitive programming.", 22, 452, 74, 400, 30, TEXT, .3)
    b.append(p)
    b.append(txt("mono", "language: C++   judges: Codeforces, LeetCode", 14, 452, 140, DIM, "start", .5))
    return svg(W, H, "".join(b), "", "Competitive programming: regular practice of data structures and algorithms in C++ on Codeforces and LeetCode.")


# ---------------------------------------------------------------- learning
def learning():
    W = 900
    items = ["Full-Stack Development with the MERN Stack", "REST APIs & Backend Architecture", "MongoDB & Database Design",
             "Data Structures & Algorithms", "Operating Systems", "Computer Networks",
             "Software Engineering & System Design fundamentals"]
    H = 96 + len(items) * 40
    b = [panel(W, H, VIO), txt("mono", "$ ps -a --learning", 17, 40, 50, YEL, "start", 1),
         txt("mono", f"{len(items)} processes running", 14, W - 40, 50, DIM, "end", 1),
         f'<rect x="30" y="64" width="{W - 60}" height="1" fill="{VIO}" opacity=".5"/>']
    bx, bw = 580, 260
    for i, t in enumerate(items):
        y = 100 + i * 40
        col = [CYAN, MAG][i % 2]
        b.append(f'<circle cx="46" cy="{y - 5}" r="4" fill="{col}">{blink(lo=.2, dur=1.6 + i * .2, begin=i * .3)}</circle>')
        b.append(txt("mono", f"{i + 1:02d}", 15, 64, y, DIM))
        b.append(txt("mono", t, fit("mono", t, 17, 470, .3), 100, y, TEXT, "start", .3))
        b.append(f'<rect x="{bx}" y="{y - 12}" width="{bw}" height="10" fill="#0a0d1f" stroke="{col}" stroke-opacity=".4"/>')
        d = 2.2 + i * .35
        b.append(f'<clipPath id="lc{i}"><rect x="{bx}" y="{y - 12}" width="{bw}" height="10"/></clipPath>'
                 f'<g clip-path="url(#lc{i})"><rect y="{y - 12}" width="70" height="10" fill="{col}" opacity=".85">'
                 f'<animate attributeName="x" values="{bx - 70};{bx + bw}" dur="{d:.2f}s" begin="-{i * .6:.1f}s" repeatCount="indefinite"/></rect></g>')
    return svg(W, H, "".join(b), "", "Currently learning: " + "; ".join(items))


# ----------------------------------------------------------------- buttons
def button(label, icon_name, w, accent):
    H = 56
    d = cut_rect(2, 2, w - 4, H - 4, 12)
    s = fit("orbb", label, 14, w - 96, 2)
    b = [f'<path d="{d}" fill="{accent}" fill-opacity=".08"/>',
         f'<path d="{d}" fill="none" stroke="{accent}" stroke-opacity=".3" stroke-width="5" filter="url(#g3)"/>',
         f'<path d="{d}" fill="none" stroke="{accent}" stroke-width="1.5"/>',
         icon(icon_name, 40, H / 2, 24, accent),
         txt("orbb", label, s, 64, H / 2 + s * .35, TEXT, "start", 2),
         f'<path d="M{w - 30} {H / 2 - 7}L{w - 22} {H / 2}L{w - 30} {H / 2 + 7}" fill="none" stroke="{accent}" stroke-width="2">'
         f'<animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></path>']
    return svg(w, H, "".join(b), "", label.title())


# ------------------------------------------------------------------ footer
def footer():
    W, H = 900, 150
    t = "LEARN  •  BUILD  •  SOLVE  •  REPEAT"
    s = fit("orb", t, 30, 800, 4)
    b = [divider_line(450, 22, 420),
         glow_text("orb", t, s, 450, 74, "url(#neon)", "middle", 4, "g16", ".7"),
         txt("mono", "// end of transmission. see you in the next commit.", 15, 450, 108, DIM, "middle", 1),
         f'<rect x="150" y="128" width="600" height="2" fill="url(#neon)" opacity=".8"/>',
         f'<rect y="125" width="60" height="8" fill="#fff" opacity="0" filter="url(#g3)">'
         '<animate attributeName="x" values="140;700" dur="3.5s" repeatCount="indefinite"/>'
         '<animate attributeName="opacity" values="0;.8;0" dur="3.5s" repeatCount="indefinite"/></rect>']
    return svg(W, H, "".join(b), "", "Learn, build, solve, repeat.")
