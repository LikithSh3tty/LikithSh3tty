import pytest

from scripts.fetch_contributions import compute_stats, parse_days

GOOD = """
<table class="ContributionCalendar-grid">
  <td class="ContributionCalendar-day" data-date="2026-01-01" data-level="0" id="a"></td>
  <td class="ContributionCalendar-day" data-date="2026-01-02" data-level="2" id="b"></td>
  <td class="ContributionCalendar-day" data-date="2026-01-03" data-level="4" id="c"></td>
</table>
<tool-tip for="a">No contributions on January 1st.</tool-tip>
<tool-tip for="b">7 contributions on January 2nd.</tool-tip>
<tool-tip for="c">21 contributions on January 3rd.</tool-tip>
"""


def test_parses_date_level_and_count():
    days = parse_days(GOOD)
    assert len(days) == 3
    assert days[0] == {"date": "2026-01-01", "level": 0, "count": 0}
    assert days[2] == {"date": "2026-01-03", "level": 4, "count": 21}


def test_empty_markup_raises_rather_than_returning_nothing():
    with pytest.raises(ValueError):
        parse_days("<html><body>no calendar here</body></html>")


def test_stats_counts_streaks_and_total():
    stats = compute_stats(parse_days(GOOD))
    assert stats["total"] == 28
    assert stats["longest_streak"] == 2
    assert stats["best_day"] == {"date": "2026-01-03", "count": 21}
