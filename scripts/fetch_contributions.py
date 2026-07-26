"""Scrape the public contribution calendar. No token, no API quota.

Fails loudly rather than writing an empty calendar, so a markup change on GitHub's
side leaves the last good data (and therefore the last good graph) in place.
"""
import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USER = "LikithSh3tty"
URL = f"https://github.com/users/{USER}/contributions"
OUT = Path("data/contributions.json")


def parse_days(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    cells = soup.select("[data-date][data-level]")
    if not cells:
        raise ValueError(
            "No day cells found. GitHub likely changed the calendar markup; "
            "update the selector in parse_days()."
        )
    # Tooltips carry the real counts; data-level is only a 0-4 bucket.
    counts = {}
    for tip in soup.find_all("tool-tip"):
        ref = tip.get("for")
        if not ref:
            continue
        m = re.match(r"\s*(\d+)", tip.get_text())
        counts[ref] = int(m.group(1)) if m else 0

    days = [
        {
            "date": c["data-date"],
            "level": int(c["data-level"]),
            "count": counts.get(c.get("id"), 0),
        }
        for c in cells
    ]
    return sorted(days, key=lambda d: d["date"])


def compute_stats(days: list[dict]) -> dict:
    total = sum(d["count"] for d in days)
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    current = 0
    for d in reversed(days):
        if d["count"] == 0:
            break
        current += 1
    best = max(days, key=lambda d: d["count"]) if days else {"date": "", "count": 0}
    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
    }


if __name__ == "__main__":
    resp = requests.get(URL, timeout=30, headers={"User-Agent": f"{USER}-profile-art"})
    resp.raise_for_status()
    try:
        days = parse_days(resp.text)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

    if not 300 <= len(days) <= 400:
        print(f"ERROR: implausible day count {len(days)}; refusing to write.", file=sys.stderr)
        raise SystemExit(1)

    stats = compute_stats(days)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(
        json.dumps({"days": days, "stats": stats}, indent=1), encoding="utf-8"
    )
    print(f"wrote {OUT} — {len(days)} days, {stats['total']} contributions")
