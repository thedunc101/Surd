#!/usr/bin/env python3
"""What each model SAID it was doing, per day, across all three transcript folders.

Why this exists. BOOK_HISTORY.md derives its figures, its reviews and its decisions, but
the account of what a day was FOR is written by hand. Those accounts were first written
from the structured record alone, and they were wrong in the same way every time: the
structured record is mostly Claude, because Claude works through tools that measure and
leave a trace. Grok drafted roughly a third of the book and left almost nothing in it.
Codex delivered the assessments the book was steered by and showed up only as review
files.

So the accounts have to be written against the transcripts, and the transcripts are far too
large to read. This prints the one line from each assistant turn where the model says what
it is about to do or has just done, which is enough to reconstruct a day and small enough
to read thirty-one of them.

It prints. It writes nothing, and it is not part of the hourly backup - it is run by hand
before writing or revising an account in BOOK_HISTORY_NOTES.md.

    python PROVENANCE/tools/session_digest.py                 # every day, 10 lines each
    python PROVENANCE/tools/session_digest.py --per 25         # more per day
    python PROVENANCE/tools/session_digest.py --day 2026-10-09 # one day, everything

No chapter prose is printed. Only the opening line of an assistant turn survives, and
code fences, tool blocks, tables, quotations and indented material are dropped - which is
what manuscript text in a transcript looks like.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.dirname(HERE)

# Same three folders the history reads, and the same reason for the split: Claude and Codex
# date each turn on its role header, Grok dates a block of turns with a heading of its own.
SESSIONS = (("03_Grok_sessions", "Grok"),
            ("02_Codex_sessions", "Codex"),
            ("01_Claude_Code_sessions", "Claude"))

ROLE = re.compile(r"^#{2,3}\s+(USER|ASSISTANT|BOT)\b")
DATE = re.compile(r"(\d{4}-\d{2}-\d{2})T\d\d:\d\d")
# anchored at both ends, so a line of prose opening "## Fri, Sep 18 examples of..." is not
# read as a heading and does not redate everything after it
GROK_DAY = re.compile(
    r"^##[ \t]+\w{3},[ \t]+(\w{3})\w*[ \t]+(\d{1,2})"
    r"(?:[ \t]+\d{1,2}:\d{2}[ \t]*[AaPp]\.?[Mm]\.?)?[ \t]*$")
MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
          "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
YEAR0 = 2026

# machinery, quoted material and manuscript text, none of which is the model talking
NOISE = re.compile(r"^\s*(\*\*\[tool|```|\||<|>|-{3,}|#|\d+\s*\||\[|\*\s|\d+\.\s|\$|PS |C:\\)")
OPENER = re.compile(r"^(\*\*)?[A-Z\u201c\u2018]")
# Grok's assistant is a general-purpose one and its transcript carries the operations app
# and the agent swarm beside the novel. Those days reach back to 1 September, before the
# book existed. Drop the other work rather than the whole file.
OTHER_WORK = re.compile(
    r"business_app|Turso|Tkinter|Instagram|merchant of record|\bMoR\b|swarm|OPEN\.md|"
    r"App\\\d|Models Scout|Brunei|gate_server|ntfy|OpenRouter", re.I)
FIRST_DAY = "2026-09-18"      # the day the book started

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def collect(last_day):
    """{day: {tool: [(filename, statement), ...]}}"""
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for folder, tool in SESSIONS:
        for path in sorted(glob.glob(os.path.join(PROV, folder, "*.md"))):
            if "raw_rows" in path:
                continue
            day, take, gyear, gmon = "", False, YEAR0, 0
            try:
                fh = io.open(path, encoding="utf-8", errors="replace")
            except OSError:
                continue
            for ln in fh:
                g = GROK_DAY.match(ln)
                mon = MONTHS.get(g.group(1).lower()) if g else None
                if mon:
                    # the headings carry no year, so it is carried forward: the year only
                    # changes where the month goes backwards, December into January
                    if gmon and mon < gmon:
                        gyear += 1
                    gmon = mon
                    day = "%04d-%02d-%02d" % (gyear, mon, int(g.group(2)))
                    take = False
                    continue
                r = ROLE.match(ln)
                if r:
                    d = DATE.search(ln)
                    if d:
                        day = d.group(1)
                    take = r.group(1) in ("ASSISTANT", "BOT")
                    continue
                if not (take and day):
                    continue
                s = ln.strip()
                if len(s) < 50 or NOISE.match(s) or not OPENER.match(s):
                    continue
                if not (FIRST_DAY <= day <= last_day) or OTHER_WORK.search(s):
                    continue
                by[day][tool].append((os.path.basename(path)[:34], s[:190]))
                take = False      # one statement per turn, the opening one
    return by


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--per", type=int, default=10,
                    help="statements shown per tool per day, spread evenly (default 10)")
    ap.add_argument("--day", help="one day only, YYYY-MM-DD, and show everything")
    ap.add_argument("--width", type=int, default=150, help="truncate each line (default 150)")
    a = ap.parse_args()

    # The history lags a day behind on purpose: an account written at midday describes half
    # a day. Asking for today explicitly overrides that.
    last = a.day or (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    by = collect(max(last, a.day or last))

    days = [a.day] if a.day else sorted(by)
    for day in days:
        tools = by.get(day)
        if not tools:
            print("\n=== %s  (nothing)" % day)
            continue
        print("\n=== %s  (%d statements)" % (day, sum(len(v) for v in tools.values())))
        for folder, tool in SESSIONS:
            rows = tools.get(tool, [])
            if not rows:
                continue
            print("  -- %s: %d" % (tool, len(rows)))
            show = rows if a.day else rows[::max(1, len(rows) // a.per)][:a.per]
            for f, s in show:
                print(("     [%s] %s" % (f, s))[:a.width])
    return 0


if __name__ == "__main__":
    sys.exit(main())
