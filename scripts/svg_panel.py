"""Shared chrome so every SVG looks identical on light and dark GitHub themes.

GitHub renders READMEs on white for light-theme visitors and #0d1117 for dark-theme
ones. A `prefers-color-scheme` query inside an SVG loaded through <img> resolves
against the visitor's OS setting rather than their GitHub theme, so it desyncs. Each
SVG therefore paints its own dark panel and depends on nothing outside the file.
"""

BG = "#0d1117"
BORDER = "#30363d"
FG = "#c9d1d9"
DIM = "#8b949e"


def panel_open(width: int, height: int, title: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
     viewBox="0 0 {width} {height}" role="img" aria-label="{title}">
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10"
        fill="{BG}" stroke="{BORDER}"/>
'''


def panel_close() -> str:
    return "</svg>\n"
