"""Regenerate every static SVG in ../assets  (python scripts/build_assets.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dynamic_assets as dyn
import static_assets as st

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:28s}{len(content) / 1024:7.1f} KB")


if __name__ == "__main__":
    write("header.svg", st.header())
    write("titles.svg", st.titles())
    write("divider.svg", st.divider())
    for i, (slug, title, sub) in enumerate([
        ("about", "ABOUT_ME", "whoami"),
        ("stack", "TECH_STACK", "loadout"),
        ("projects", "FEATURED_PROJECTS", "./projects"),
        ("cp", "COMPETITIVE_CODING", "solve()"),
        ("learning", "CURRENTLY_LEARNING", "ps -a"),
        ("stats", "SYSTEM_STATS", "live feed"),
        ("connect", "CONNECT", "open channel"),
    ], start=1):
        write(f"h-{slug}.svg", st.section_header(i, title, sub))
    write("about.svg", st.about())
    write("stack.svg", st.stack())
    for slug, content in st.projects():
        write(f"{slug}.svg", content)
    write("cp.svg", st.cp())
    write("learning.svg", st.learning())
    write("btn-codeforces.svg", st.button("CODEFORCES", "codeforces", 250, st.CYAN))
    write("btn-leetcode.svg", st.button("LEETCODE", "leetcode", 250, st.YEL))
    write("btn-email.svg", st.button("GMAIL", "gmail", 250, st.MAG))
    write("btn-linkedin.svg", st.button("LINKEDIN", "linkedin", 250, st.CYAN))
    write("footer.svg", st.footer())
    # dynamic files: only create placeholders when missing (the workflow owns them)
    for name, fn in [("stats.svg", dyn.stats), ("langs.svg", dyn.langs), ("heatmap.svg", dyn.heatmap)]:
        if not os.path.exists(os.path.join(OUT, name)):
            write(name, fn({}))
