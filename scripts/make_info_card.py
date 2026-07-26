"""Hand-authored neofetch-style info card.

Regenerate only when the bio changes. The contribution graph already carries the
numbers, so this card is for the things numbers cannot say.
"""
from scripts.svg_panel import DIM, FG, panel_close, panel_open

# GitHub Primer accents. Real neofetch colours each key differently rather than
# painting the whole card one hue.
CORAL, ORANGE, YELLOW = "#ff7b72", "#ffa657", "#e3b341"
GREEN, BLUE, PURPLE = "#7ee787", "#79c0ff", "#d2a8ff"
SWATCHES = [CORAL, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

W, PAD, LINE = 490, 22, 19
USER, HOST = "likith", "github"

ROWS = [
    (BLUE, "Now", "M.Sc. Artificial Intelligence & ML"),
    (None, "", "CHRIST (Deemed to be University), Bengaluru"),
    (PURPLE, "Role", "Fullstack + AI builder"),
    (GREEN, "Learning", "LangGraph · agentic AI · applied ML"),
    (ORANGE, "Stack", "React · JavaScript · Python · FastAPI"),
    (None, "", "Firebase/Supabase · LangChain/LangGraph · n8n"),
    (YELLOW, "Shipped", "CloudNest · Agenvo · Grid0pt"),
    (CORAL, "Contact", "likithshetty188@gmail.com"),
    (PURPLE, "Ethos", "Polished, end-to-end projects,"),
    (None, "", "shipped alongside coursework"),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    h = PAD * 2 + LINE * (len(ROWS) + 3) + 14
    out = [panel_open(W, h, "info card")]
    out.append(
        "  <style>\n"
        "    .ln { opacity: 0; animation: in .38s ease-out forwards; }\n"
        "    @keyframes in { from { opacity: 0; transform: translateX(-6px); }\n"
        "                    to   { opacity: 1; transform: translateX(0); } }\n"
        "  </style>\n"
    )
    out.append(
        '  <g font-family="SFMono-Regular,Consolas,Liberation Mono,monospace" font-size="12">\n'
    )

    # user@host, two-tone the way a real prompt reads.
    y = PAD + LINE
    out.append(
        f'    <text class="ln" style="animation-delay:0s" x="{PAD}" y="{y}" font-weight="600">'
        f'<tspan fill="{GREEN}">{USER}</tspan>'
        f'<tspan fill="{DIM}">@</tspan>'
        f'<tspan fill="{BLUE}">{HOST}</tspan></text>\n'
    )
    y += LINE
    out.append(
        f'    <text class="ln" style="animation-delay:.06s" x="{PAD}" y="{y}" '
        f'fill="{DIM}">{"─" * 44}</text>\n'
    )

    for i, (colour, key, val) in enumerate(ROWS):
        y += LINE
        d = 0.12 + i * 0.06
        if key:
            out.append(
                f'    <text class="ln" style="animation-delay:{d:.2f}s" x="{PAD}" y="{y}" '
                f'fill="{colour}">{esc(key)}</text>\n'
            )
        out.append(
            f'    <text class="ln" style="animation-delay:{d:.2f}s" x="{PAD + 80}" y="{y}" '
            f'fill="{FG}">{esc(val)}</text>\n'
        )
    out.append("  </g>\n")

    # The colour blocks neofetch prints under the info block.
    y += LINE + 4
    for i, colour in enumerate(SWATCHES):
        out.append(
            f'  <rect class="ln" style="animation-delay:{0.12 + len(ROWS) * 0.06:.2f}s" '
            f'x="{PAD + i * 20}" y="{y}" width="14" height="10" rx="2" fill="{colour}"/>\n'
        )

    out.append(panel_close())
    return "".join(out)


if __name__ == "__main__":
    with open("info-card.svg", "w", encoding="utf-8") as fh:
        fh.write(build_svg())
    print("wrote info-card.svg")
