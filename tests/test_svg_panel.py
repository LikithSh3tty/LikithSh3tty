from scripts.svg_panel import panel_close, panel_open


def test_panel_open_sets_viewbox_and_dark_background():
    svg = panel_open(860, 200, "title")
    assert 'viewBox="0 0 860 200"' in svg
    assert "#0d1117" in svg
    assert "#30363d" in svg


def test_panel_close_closes_the_svg():
    assert panel_close().strip() == "</svg>"
