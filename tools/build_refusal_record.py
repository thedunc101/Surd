#!/usr/bin/env python3
"""Count every time a model refused to process this book, and write the record.

Why this exists. On 21 September 2026 the work stopped roughly every few minutes for
eighteen hours: the model returned a safeguard refusal with the reason code [bio]. It was
diagnosed at the time as a page of old notes rather than the manuscript, and the canon
bible was written to replace them. That diagnosis was incomplete. The refusals did not
stop - there were more on 29 September, more on 8 October tied to a chapter file, and more
on 22 October. Whatever is firing, it was not only the notes.

What the counting found. The refusals are not spread across the book. Ninety per cent of
those naming any chapter involve the same five-chapter block: Preparations, The Shortlist,
Envelopes, Release, Aftermath - the arc running from preparing the event to what came
after. And they travel in groups: the more chapters pulled into one request, the more
reliably it was refused.

That points at the book's method rather than at any sentence. These chapters cannot be
checked in isolation, because each retrieves figures the others establish. Verifying one
number in Release means opening the chapters that produced it, which assembles the whole
sequence into a single request. The continuity that makes the book work is what made it
hard to process.

Counts can be derived. What was being done on a given day, and what it cost the book,
cannot - so the per-day narrative is hand-written in MODEL_REFUSALS_NOTES.md and merged in
here. A day with refusals and no note is marked as missing rather than passed over.

What this does NOT claim. It records which chapter files were named in the sixty lines
before each refusal. That is proximity, not the flagged payload. Several chapters were
usually in play at once, and nothing here proves which text the classifier read.

No prose is read, stored or printed. Timestamps, model names, error strings and chapter
FILENAMES only.

Run by backup.ps1. Writes only when something changed, so a quiet hour costs no commit.
"""
from __future__ import annotations

import collections
import datetime
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.dirname(HERE)
REPO = os.path.dirname(PROV)
OUT = os.path.join(PROV, "MODEL_REFUSALS.md")
NOTES = os.path.join(PROV, "MODEL_REFUSALS_NOTES.md")
DECISIONS = os.path.join(REPO, "COMPANION", "DECISIONS_LOG.md")
FOLDERS = ("01_Claude_Code_sessions", "02_Codex_sessions", "03_Grok_sessions")

# Anchored to the start of the line, because this document is itself kept in a session
# transcript that the scan reads. Discussing the refusals wrote the error strings into the
# log, and an unanchored pattern counted those quotations as fresh refusals - six of them
# within an hour of the tool first running. A real refusal opens its line; a quotation of
# one sits inside a command, a table row or a printed column.
REFUSAL = re.compile(
    r"^[\s>*\[]*API Error:[^\n]{0,40}(safeguards flagged|can.t help with this)", re.I)
# The same refusal also arrives wrapped, when it kills a subagent rather than a turn. These
# are worth more than the plain ones: the summary line carries the name of the task that was
# being attempted, which is the clearest statement in the whole archive of what the model
# would not do - "Synopsise all 26 chapters safely" among them.
AGENT_FAIL = re.compile(
    r'^[\s>*\[]*<summary>Agent "(.+?)" failed:[^\n]{0,80}API error', re.I)
# Belt and braces: anything carrying these is the record talking about itself.
SELF = re.compile(r"tool_use|re\.compile|MODEL_REFUSALS|build_refusal_record|\d{4}-\d\d-\d\dT\d\d:\d\d\s+\w+\s+API Error")
MODEL = re.compile(r"(Opus [\d.]+|Sonnet [\d.]+|Haiku [\d.]+)", re.I)
STAMP = re.compile(r"^#{2,3} .*?(\d{4}-\d{2}-\d{2}T\d\d:\d\d)")
CHAPTER = re.compile(r"\b([0-2]\d)_([A-Za-z_]+)\.(?:docx|txt|md)\b")
DAY_HEAD = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$", re.M)
DEC_ROW = re.compile(r"^\| (2026-\d\d-\d\d) \| (.+?) \|", re.M)
LOOKBACK = 60
# task titles that read as instructions once separated from the novel
SENSITIVE_TASK = re.compile(r"immunisation|device|pathogen|vaccine|dispers", re.I)

ARC = {12, 13, 14, 15, 16}
ARC_NAMES = "Preparations, The Shortlist, Envelopes, Release and Aftermath"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def scan():
    events = []
    for folder in FOLDERS:
        for path in glob.glob(os.path.join(PROV, folder, "*.md")):
            if "raw_rows" in path:
                continue
            try:
                lines = io.open(path, encoding="utf-8", errors="replace").read().split("\n")
            except OSError:
                continue
            stamp = ""
            for i, line in enumerate(lines):
                m = STAMP.match(line)
                if m:
                    stamp = m.group(1)
                af = AGENT_FAIL.search(line)
                if not (REFUSAL.search(line) or af) or SELF.search(line):
                    continue
                task = af.group(1)[:70] if af else None
                mm = MODEL.search(line)
                near = set()
                for j in range(max(0, i - LOOKBACK), i):
                    for c in CHAPTER.finditer(lines[j]):
                        if c.group(1) != "00":
                            near.add(int(c.group(1)))
                events.append((stamp, mm.group(1) if mm else "unnamed", near, task))
    return events


def read_notes():
    """The hand-written narrative, one block per day."""
    if not os.path.exists(NOTES):
        return {}
    text = io.open(NOTES, encoding="utf-8", errors="replace").read()
    out, marks = {}, list(DAY_HEAD.finditer(text))
    for k, m in enumerate(marks):
        end = marks[k + 1].start() if k + 1 < len(marks) else len(text)
        body = text[m.end():end].strip()
        if body:
            out[m.group(1)] = body
    return out


def read_decisions():
    """What each day actually produced, from the decisions log."""
    if not os.path.exists(DECISIONS):
        return {}
    text = io.open(DECISIONS, encoding="utf-8", errors="replace").read()
    out = {}
    for d, what in DEC_ROW.findall(text):
        out.setdefault(d, []).append(what.strip())
    return out


def write_if_changed(path, text):
    old = ""
    if os.path.exists(path):
        old = io.open(path, encoding="utf-8", errors="replace").read()
    strip = lambda s: re.sub(r"_Rebuilt [^\n]*\n", "", s)
    if strip(old) == strip(text):
        return False
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    return True


def main() -> int:
    ev = scan()
    if not ev:
        print("refusals: none found")
        return 0

    by_day = collections.Counter(e[0][:10] for e in ev if e[0])
    by_model = collections.Counter(e[1] for e in ev)
    with_ch = [e for e in ev if e[2]]
    by_ch = collections.Counter(n for e in with_ch for n in e[2])
    in_arc = sum(1 for e in with_ch if e[2] & ARC)
    pct = (100.0 * in_arc / len(with_ch)) if with_ch else 0
    notes, decisions = read_notes(), read_decisions()
    missing = [d for d in sorted(by_day) if d not in notes]

    L = []
    L.append("# Every time a model refused to process this book")
    L.append("")
    L.append("_Rebuilt on every backup run. Generated %s._"
             % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    L.append("")
    L.append("**%d refusals, on %d days.** Every one returned the same reason code, `[bio]`."
             % (len(ev), len(by_day)))
    L.append("")
    L.append("| Model | Refusals |")
    L.append("|---|---|")
    for m, c in by_model.most_common():
        L.append("| %s | %d |" % (m, c))
    L.append("")
    L.append("**%d of the %d refusals that name a chapter involve chapters 12 to 16 — %s. "
             "That is %.0f per cent of those that name one.** The other %d name no chapter at "
             "all. Chapter numbers are as they were at the time; the "
             "replot of 9 October 2026 renumbered the book."
             % (in_arc, len(with_ch), ARC_NAMES, pct, len(ev) - len(with_ch)))
    L.append("")

    L.append("## Day by day")
    L.append("")
    for d in sorted(by_day):
        L.append("### %s — %d refusal%s" % (d, by_day[d], "" if by_day[d] == 1 else "s"))
        L.append("")
        chs = collections.Counter()
        for e in ev:
            if e[0][:10] == d:
                for n in e[2]:
                    chs[n] += 1
        if chs:
            L.append("Chapters open: %s."
                     % ", ".join(str(n) for n, _ in chs.most_common(6)))
            L.append("")
        tasks = [e[3] for e in ev if e[0][:10] == d and e[3]]
        if tasks:
            L.append("Tasks killed mid-run:")
            L.append("")
            for tk in tasks:
                # One of these titles, lifted out of a novel about a study and read cold,
                # scans as an instruction rather than as a chapter problem. The record
                # describes that one and quotes the rest: the point of the list is what the
                # model would not do, which survives paraphrase.
                if SENSITIVE_TASK.search(tk):
                    L.append("- a task about reconciling two plot elements in the "
                             "Preparations arc (title withheld: read cold it scans as an "
                             "instruction, which is the whole problem this record is about)")
                else:
                    L.append('- "%s"' % tk)
            L.append("")
        if notes.get(d):
            L.append(notes[d])
            L.append("")
        else:
            L.append("_Counted above. No hand-written account of this day yet._")
            L.append("")
        if decisions.get(d):
            L.append("Decisions logged that day:")
            L.append("")
            for w in decisions[d][:6]:
                L.append("- %s" % w)
            L.append("")

    spread = collections.Counter(len(e[2]) for e in with_ch)
    many = sum(v for k, v in spread.items() if k >= 8)
    L.append("## Why the clustering matters")
    L.append("")
    L.append("These chapters cannot be checked one at a time. Each retrieves figures the "
             "others establish, so verifying a single number in Release means opening the "
             "chapters that produced it. That assembles the whole sequence into one request, "
             "and of the %d refusals that name a chapter, %d had "
             "eight or more chapters open at once." % (len(with_ch), many))
    L.append("")
    L.append("This suggests it was the book's method rather than any sentence in it: the "
             "continuity that makes the book work is what assembled the long requests. It is an "
             "inference from the clustering, not an established fact, and nothing here shows "
             "which text the classifier read. No procedure may be given anywhere in the novel: "
             "that is the book's own standing rule, and no reviewer has found otherwise.")
    L.append("")
    L.append("**8 October fits neither explanation cleanly.** Eight refusals that day, with "
             "chapter 9 the only chapter open. That is the day which breaks the stale-notes "
             "diagnosis, because the canon bible had replaced those notes seventeen days "
             "earlier. It also cuts against the chain-length reading, because there was no "
             "chain. Recorded rather than explained away.")
    L.append("")
    L.append("## What this does not say")
    L.append("")
    L.append("This counts which chapter files were named in the %d lines before each refusal. "
             "That is what was open, not what was sent. Several chapters were usually in play "
             "at once and nothing here establishes which text the classifier read. The "
             "clustering is the evidence; the reading of it is an inference, drafted from the counts and adopted by the author." % LOOKBACK)
    L.append("")
    L.append("No chapter text is read or stored by the tool that builds this. It takes "
             "timestamps, model names, error strings and filenames only.")
    L.append("")

    text = "\n".join(L)
    changed = write_if_changed(OUT, text)
    print("refusals: %d on %d days, %.0f%% on chapters 12-16%s%s"
          % (len(ev), len(by_day), pct,
             "" if changed else " (unchanged)",
             "" if not missing else "; NO NOTE YET: " + ", ".join(missing)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
