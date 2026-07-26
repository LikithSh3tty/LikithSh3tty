from scripts.render_heatmap_svg import LEGEND_LEVELS, PALETTE, build_svg

DAYS = [{"date": f"2026-01-{d:02d}", "level": d % 5, "count": d} for d in range(1, 29)]
STATS = {
    "total": 406,
    "current_streak": 3,
    "longest_streak": 9,
    "best_day": {"date": "2026-01-28", "count": 28},
}


def test_emits_one_rect_per_day():
    assert build_svg(DAYS, STATS).count('class="d"') == len(DAYS)


def test_uses_only_palette_colours():
    svg = build_svg(DAYS, STATS)
    for level in {d["level"] for d in DAYS}:
        assert PALETTE[level] in svg


def test_total_appears_in_footer():
    assert "406 contributions" in build_svg(DAYS, STATS)


def test_animation_does_not_loop():
    svg = build_svg(DAYS, STATS)
    assert "forwards" in svg
    assert "infinite" not in svg


def test_legend_only_shows_reachable_levels():
    """GitHub's data-level tops out at 4, so a 6th swatch would advertise a
    colour that can never appear in the grid."""
    assert LEGEND_LEVELS == 5
    assert build_svg(DAYS, STATS).count('class="lg"') == LEGEND_LEVELS
