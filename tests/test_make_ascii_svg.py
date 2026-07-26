from PIL import Image

from scripts.make_ascii_svg import (
    CHAR_H,
    CHAR_W,
    COLS,
    RAMP,
    brightness_to_glyph,
    image_to_rows,
    rows_for_image,
)


def test_white_maps_to_space_and_black_to_densest():
    assert brightness_to_glyph(255) == " "
    assert brightness_to_glyph(0) == RAMP[-1]


def test_ramp_starts_with_space():
    assert RAMP[0] == " "


def test_image_to_rows_returns_exact_grid():
    img = Image.new("L", (200, 200), color=255)
    rows = image_to_rows(img, cols=100, rows=53)
    assert len(rows) == 53
    assert all(len(r) == 100 for r in rows)


def test_blank_white_image_produces_only_spaces():
    img = Image.new("L", (200, 200), color=255)
    assert set("".join(image_to_rows(img, 100, 53))) == {" "}


def test_row_count_preserves_source_aspect():
    """Character cells are 6x10, so a square source needs ~1.67x more columns
    than rows. Ignoring this stretches the face horizontally."""
    square = Image.new("L", (400, 400))
    rows = rows_for_image(square)
    rendered_aspect = (COLS * CHAR_W) / (rows * CHAR_H)
    assert abs(rendered_aspect - 1.0) < 0.03


def test_tall_source_gets_proportionally_more_rows():
    tall = Image.new("L", (300, 600))
    wide = Image.new("L", (600, 300))
    assert rows_for_image(tall) > rows_for_image(wide)
