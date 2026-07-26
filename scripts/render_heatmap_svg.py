"""contributions.json -> animated 53x7 heatmap SVG."""
import json
from datetime import date

from scripts.svg_panel import DIM, FG, panel_close, panel_open

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
# GitHub's data-level only ever reaches 4, so the legend stops there rather than
# advertising a colour the grid can never contain.
LEGEND_LEVELS = 5

W = 860
CELL, GAP = 11, 3
PITCH = CELL + GAP
PAD, GUTTER, TOP = 20, 30, 34
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def build_svg(days: list[dict], stats: dict) -> str:
    h = TOP + 7 * PITCH + 46
    out = [panel_open(W, h, "contribution heatmap")]
    out.append(
        "  <style>\n"
        "    .d { opacity: 0; animation: pop .3s ease-out forwards; }\n"
        "    @keyframes pop { from { opacity: 0; transform: translateY(-3px); }\n"
        "                     to   { opacity: 1; transform: translateY(0); } }\n"
        "  </style>\n"
    )

    # GitHub's calendar always begins on a Sunday; align rows to weekday anyway
    # so a mid-week start would still land correctly.
    first = date.fromisoformat(days[0]["date"])
    offset = (first.weekday() + 1) % 7

    seen_months = set()
    labels = []
    for i, day in enumerate(days):
        slot = i + offset
        week, wd = slot // 7, slot % 7
        x = PAD + GUTTER + week * PITCH
        y = TOP + wd * PITCH
        delay = (week + wd) * 0.012  # diagonal reveal
        out.append(
            f'  <rect class="d" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" '
            f'width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[day["level"]]}">'
            f'<title>{day["count"]} on {day["date"]}</title></rect>\n'
        )
        m = date.fromisoformat(day["date"]).month
        if m not in seen_months and wd == 0:
            seen_months.add(m)
            labels.append((x, MONTHS[m - 1]))

    out.append(
        f'  <g font-family="SFMono-Regular,Consolas,monospace" font-size="9" fill="{DIM}">\n'
    )
    for x, name in labels:
        out.append(f'    <text x="{x}" y="{TOP - 8}">{name}</text>\n')
    for wd, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'    <text x="{PAD}" y="{TOP + wd * PITCH + CELL - 1}">{name}</text>\n')

    lx = W - PAD - LEGEND_LEVELS * PITCH - 66
    ly = TOP + 7 * PITCH + 16
    out.append(f'    <text x="{lx}" y="{ly + CELL - 2}">Less</text>\n')
    out.append(
        f'    <text x="{lx + 30 + LEGEND_LEVELS * PITCH + 4}" y="{ly + CELL - 2}">More</text>\n'
    )
    out.append("  </g>\n")
    for i in range(LEGEND_LEVELS):
        out.append(
            f'  <rect class="lg" x="{lx + 30 + i * PITCH}" y="{ly}" width="{CELL}" '
            f'height="{CELL}" rx="2" fill="{PALETTE[i]}"/>\n'
        )

    out.append(
        f'  <text x="{PAD}" y="{ly + CELL - 2}" '
        f'font-family="SFMono-Regular,Consolas,monospace" font-size="11" fill="{FG}">'
        f'{stats["total"]:,} contributions in the last year '
        f'· {stats["longest_streak"]}-day longest streak</text>\n'
    )
    out.append(panel_close())
    return "".join(out)


if __name__ == "__main__":
    with open("data/contributions.json", encoding="utf-8") as fh:
        data = json.load(fh)
    svg = build_svg(data["days"], data["stats"])
    with open("contrib-heatmap.svg", "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote contrib-heatmap.svg ({len(svg)} bytes)")
