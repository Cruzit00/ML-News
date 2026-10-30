#!/usr/bin/env python3
"""Turn a finished digest into a post for the website.

Usage:
    python3 scripts/publish_digest.py digest.md [--date YYYY-MM-DD]

digest.md is the whole digest as Markdown, starting with the
"# ☭ ML Morning Digest — <weekday, date>" heading (the same text posted to
Discord, before it is split into messages). The script writes
_posts/<date>-ml-morning-digest.md and prints its path. Committing and
pushing that file publishes it: GitHub Pages rebuilds the site on its own.
"""
import argparse
import datetime
import json
import pathlib
import re
import sys
import zoneinfo

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("digest", type=pathlib.Path)
    parser.add_argument("--date", help="YYYY-MM-DD; defaults to today in America/Chicago")
    args = parser.parse_args()

    tz = zoneinfo.ZoneInfo("America/Chicago")
    day = (datetime.date.fromisoformat(args.date) if args.date
           else datetime.datetime.now(tz).date())

    lines = args.digest.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        sys.exit("digest is empty")

    title = f"ML Morning Digest — {day:%A, %B} {day.day}, {day.year}"
    if lines[0].startswith("# "):
        title = lines.pop(0)[2:].strip()
    body = "\n".join(lines).strip()

    # Drop the "(story 2, cont.)" labels used to split long stories across
    # Discord messages; on the web each story reads as one piece.
    body = re.sub(r"^\s*\*{0,2}_?\(story \d+, cont\.?\)_?\*{0,2}\s*\n", "", body,
                  flags=re.IGNORECASE | re.MULTILINE)

    # The first non-empty line is the friendly intro; use it as the summary.
    summary = next((l.strip() for l in body.splitlines() if l.strip()), "")

    front = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"date: {day.isoformat()} 07:00:00 -0500",
        f"summary: {json.dumps(summary, ensure_ascii=False)}",
        "---",
        "",
    ]
    out = ROOT / "_posts" / f"{day.isoformat()}-ml-morning-digest.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(front) + f"# {title}\n\n{body}\n", encoding="utf-8")
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
