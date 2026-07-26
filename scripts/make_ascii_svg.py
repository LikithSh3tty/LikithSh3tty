"""Prepped PNG -> self-typing monochrome ASCII portrait SVG."""
from PIL import Image

from scripts.svg_panel import FG, panel_close, panel_open

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense)
COLS = 100
CHAR_W, CHAR_H = 6, 10   # monospace glyph box at font-size 10
PAD = 16


def brightness_to_glyph(value: int) -> str:
    """255 (white) -> ' ', 0 (black) -> densest glyph."""
    idx = int((255 - value) / 256 * len(RAMP))
    return RAMP[min(idx, len(RAMP) - 1)]


def rows_for_image(img: Image.Image, cols: int = COLS) -> int:
    """Row count that renders the source at its true aspect ratio.

    Character cells are taller than they are wide, so a grid with equal rows and
    columns is far wider than it is tall. Deriving rows from the source aspect is
    what stops the face being stretched horizontally.
    """
    w, h = img.size
    return max(1, round(cols * CHAR_W * h / (CHAR_H * w)))


def image_to_rows(img: Image.Image, cols: int = COLS, rows: int | None = None) -> list[str]:
    if rows is None:
        rows = rows_for_image(img, cols)
    small = img.convert("L").resize((cols, rows), Image.LANCZOS)
    px = small.load()
    return ["".join(brightness_to_glyph(px[x, y]) for x in range(cols)) for y in range(rows)]


def build_svg(rows: list[str]) -> str:
    grid_w, grid_h = COLS * CHAR_W, len(rows) * CHAR_H
    w, h = grid_w + 2 * PAD, grid_h + 2 * PAD
    out = [panel_open(w, h, "ASCII portrait")]
    out.append("  <defs>\n")
    for i in range(len(rows)):
        # Each row rides its own left-to-right wipe, staggered top to bottom.
        out.append(
            f'    <clipPath id="w{i}"><rect x="{PAD}" y="0" width="0" height="{h}">'
            f'<animate attributeName="width" from="0" to="{grid_w}" dur="0.45s" '
            f'begin="{i * 0.04:.3f}s" fill="freeze"/></rect></clipPath>\n'
        )
    out.append("  </defs>\n")
    out.append(
        f'  <g font-family="SFMono-Regular,Consolas,Liberation Mono,monospace" '
        f'font-size="{CHAR_H}" fill="{FG}" xml:space="preserve">\n'
    )
    for i, row in enumerate(rows):
        safe = row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y = PAD + (i + 1) * CHAR_H
        out.append(f'    <text x="{PAD}" y="{y}" clip-path="url(#w{i})">{safe}</text>\n')
    out.append("  </g>\n")
    out.append(panel_close())
    return "".join(out)


if __name__ == "__main__":
    img = Image.open("source-prepped.png")
    rows = image_to_rows(img)
    svg = build_svg(rows)
    with open("ascii-portrait.svg", "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"wrote ascii-portrait.svg — {COLS}x{len(rows)} grid, {len(svg)} bytes")
