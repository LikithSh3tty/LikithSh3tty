"""Hand-authored neofetch-style info card.

Regenerate only when the bio changes. The contribution graph already carries the
numbers, so this card is for the things numbers cannot say.
"""
from scripts.svg_panel import DIM, FG, panel_close, panel_open

ACCENT = "#39d353"
W, PAD, LINE = 490, 22, 19
TITLE = "likith@github"

ROWS = [
    ("Now", "M.Sc. Artificial Intelligence & ML"),
    ("", "CHRIST (Deemed to be University), Bengaluru"),
    ("Role", "Fullstack + AI builder"),
    ("Learning", "LangGraph · agentic AI · applied ML"),
    ("Stack", "React · JavaScript · Python · FastAPI"),
    ("", "Firebase/Supabase · LangChain/LangGraph · n8n"),
    ("Shipped", "CloudNest · Agenvo · Grid0pt"),
    ("Contact", "likithshetty188@gmail.com"),
    ("Ethos", "Polished, end-to-end projects,"),
    ("", "shipped alongside coursework"),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
    h = PAD * 2 + LINE * (len(ROWS) + 2) + 8
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
    y = PAD + LINE
    out.append(
        f'    <text class="ln" style="animation-delay:0s" x="{PAD}" y="{y}" '
        f'fill="{ACCENT}" font-weight="600">{TITLE}</text>\n'
    )
    y += LINE
    out.append(
        f'    <text class="ln" style="animation-delay:.06s" x="{PAD}" y="{y}" '
        f'fill="{DIM}">{"─" * 44}</text>\n'
    )
    for i, (key, val) in enumerate(ROWS):
        y += LINE
        d = 0.12 + i * 0.06
        if key:
            out.append(
                f'    <text class="ln" style="animation-delay:{d:.2f}s" x="{PAD}" y="{y}" '
                f'fill="{ACCENT}">{esc(key)}</text>\n'
            )
        out.append(
            f'    <text class="ln" style="animation-delay:{d:.2f}s" x="{PAD + 80}" y="{y}" '
            f'fill="{FG}">{esc(val)}</text>\n'
        )
    out.append("  </g>\n")
    out.append(panel_close())
    return "".join(out)


if __name__ == "__main__":
    with open("info-card.svg", "w", encoding="utf-8") as fh:
        fh.write(build_svg())
    print("wrote info-card.svg")
