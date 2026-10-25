#!/usr/bin/env python3
"""Count the words in every archived chapter snapshot, for real, and cache the result.

Why. BOOK_HISTORY.md used to take its word counts by scraping them out of session
transcripts, and that was wrong three different ways. A line like

    16_Release.docx   8326   5   38 paras /  2668 words <<<

states the chapter at 8,326 and flags a 2,668-word section inside it. Reading the number
nearest "words" recorded Release losing two thirds of itself on 23 September, which never
happened. Reading the largest number instead swept in unrelated figures and had Codex
holding a 16,000-word chapter. Reading the first number was better and still wrong on lines
that lead with a paragraph count.

There is no need to guess. ARCHIVE/manuscript_backups holds 355 dated snapshots and 5,744
actual chapter files. Opening them and counting is slower than a regular expression and it
is correct, which settles it.

The cache. Counting every file takes a few minutes, and the backup runs hourly, so the
result is kept in snapshot_wordcounts.json and only files whose size or timestamp changed
are recounted. The cache is committed: it is derived, but it is the evidence behind every
figure in the history, and regenerating it from scratch on another machine would take the
same few minutes.

Usage: python PROVENANCE/tools/snapshot_wordcounts.py [--rebuild]
"""
from __future__ import annotations

import datetime
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.dirname(HERE)
REPO = os.path.dirname(PROV)
ARCHIVE = os.path.join(REPO, "ARCHIVE", "manuscript_backups")
LIVE = os.path.join(os.path.dirname(REPO), "MANUSCRIPT")
CACHE = os.path.join(PROV, "snapshot_wordcounts.json")

# 2026-09-23_092942, 2026-10-05_1204_ch2_proposals_in_markup - the date is the prefix
DATED = re.compile(r"^(\d{4}-\d{2}-\d{2})")
CHAPTER = re.compile(r"^([0-2]\d)_([A-Za-z_]+)\.docx$")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def count(path):
    """Words in a .docx, counted the same way the claim document counts them."""
    try:
        from docx import Document
        return sum(len(p.text.split()) for p in Document(path).paragraphs)
    except Exception:
        return None


def main() -> int:
    rebuild = "--rebuild" in sys.argv
    cache = {}
    if os.path.exists(CACHE) and not rebuild:
        try:
            cache = json.load(io.open(CACHE, encoding="utf-8"))
        except ValueError:
            cache = {}

    files = []
    for d in sorted(os.listdir(ARCHIVE)) if os.path.isdir(ARCHIVE) else []:
        m = DATED.match(d)
        full = os.path.join(ARCHIVE, d)
        if not m or not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if CHAPTER.match(f):
                files.append((m.group(1), os.path.join(full, f)))
    # the live folder counts as today's snapshot, so the series reaches the present
    if os.path.isdir(LIVE):
        today = datetime.date.today().isoformat()
        for f in sorted(os.listdir(LIVE)):
            if CHAPTER.match(f):
                files.append((today, os.path.join(LIVE, f)))

    fresh, counted = {}, 0
    for day, path in files:
        try:
            st = os.stat(path)
        except OSError:
            continue
        key = os.path.relpath(path, os.path.dirname(REPO)).replace("\\", "/")
        sig = "%d:%d" % (st.st_size, int(st.st_mtime))
        old = cache.get(key)
        if old and old.get("sig") == sig:
            fresh[key] = old
            continue
        w = count(path)
        if w is None:
            continue
        m = CHAPTER.match(os.path.basename(path))
        fresh[key] = {"sig": sig, "day": day, "num": m.group(1),
                      "name": m.group(2), "words": w}
        counted += 1

    text = json.dumps(fresh, indent=0, sort_keys=True)
    old_text = io.open(CACHE, encoding="utf-8").read() if os.path.exists(CACHE) else ""
    if text != old_text:
        io.open(CACHE, "w", encoding="utf-8", newline="\n").write(text)
    print("snapshot word counts: %d files, %d recounted this run%s"
          % (len(fresh), counted, "" if text != old_text else " (unchanged)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
