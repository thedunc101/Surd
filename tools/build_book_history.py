#!/usr/bin/env python3
"""The history of the book, in one document, rebuilt on every backup run.

What this is for. The addendum has to be written from somewhere, and the material for it is
spread across a dozen places: session logs that measure every chapter they touch, a reviews
folder sorted by model, seventeen Grok run folders, a markup manifest of the author's own
tracked changes, a decisions log, and a refusal record. Each answers part of the question
and none answers it whole.

This assembles them into one day-by-day history: who wrote what, when, how it was edited,
what was decided, what was reviewed and by whom, and where the work was refused. The author
writes the narrative for each day in BOOK_HISTORY_NOTES.md and it is merged in here, so the
document grows an account rather than only a record.

Nine sources, each a different kind of dated fact:

  WROTE     Session transcripts. A tool that opens a chapter measures it, and the
            measurement carries a filename, a word count and a timestamp. Collapsed to one
            line per chapter per tool per day, first count to last. A chapter that nearly
            doubles in a sitting was written in that sitting.
  DRAFTED   PROVENANCE/04_Chapter_diffs/00_INDEX.md. The earliest archived version of each
            chapter and the folder it came from, which is the only evidence of who produced
            the opening of the book. Grok works in conversation and never measures, so
            without this the first word count would credit Claude with Grok's drafts.
  REVIEWED  PROJECT_RECORD/03_Reviews, filed by model and dated in the filename.
  READ      PROJECT_RECORD/06_Grok_Runs, named <date>__<BOT>__<scope>: the cold reads and
            editor reviews, with who and over what.
  MARKED    The markup manifest: the author's own tracked changes, per chapter, counted.
  DECIDED   COMPANION/DECISIONS_LOG.md: what was settled that day. This is where the plot,
            tone and structure changes live.
  REFUSED   The refusal record, counted per day.
  CLAIMED   PROVENANCE.json, the copyright claim. Its eighteen stages are the formal,
            dated statement of who did what with which tool, so they head the document and
            are named against the days that carry them. Read rather than paraphrased, so
            the claim and the history cannot drift apart.
  DECLARED  PROJECT_RECORD/08_Working_Notes/HISTORY.md. The document each session was told
            to read first. Its STATUS banners are the three days the book's state was
            declared outright rather than inferred from movement.

What it will not do. A measurement proves a tool had a file open and what size it was, not
that the tool wrote the words. Sharp growth inside one session is reported as writing;
small movement is reported as movement and left to the note. Chapter numbers are as they
were on the day - the replot of 9 October 2026 renumbered the book and reused numbers, so a
number here means what it meant then.

No chapter text is read or stored. Filenames, counts, timestamps and folder names only.
"""
from __future__ import annotations

import collections
import csv
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
OUT = os.path.join(PROV, "BOOK_HISTORY.md")
NOTES = os.path.join(PROV, "BOOK_HISTORY_NOTES.md")
REVIEWS = os.path.join(REPO, "PROJECT_RECORD", "03_Reviews", "_reviews")
RUNS = os.path.join(REPO, "PROJECT_RECORD", "06_Grok_Runs")
MARKUP = os.path.join(REPO, "PROJECT_RECORD", "02_Drafts_and_Packages",
                      "_markup_rounds", "MANIFEST.csv")
DECISIONS = os.path.join(REPO, "COMPANION", "DECISIONS_LOG.md")
DIFF_INDEX = os.path.join(PROV, "04_Chapter_diffs", "00_INDEX.md")
JOURNAL = os.path.join(REPO, "COMPANION", "03_AUTHORS_JOURNAL.md")
WORDCOUNTS = os.path.join(PROV, "snapshot_wordcounts.json")
CHANGELOG = os.path.join(REPO, "MANUSCRIPT_CURRENT", "CHANGELOG.md")
CLAIM = os.path.join(REPO, "PROVENANCE.json")
PROJECT_HISTORY = os.path.join(REPO, "PROJECT_RECORD", "08_Working_Notes", "HISTORY.md")
# The third field is whether a filename-plus-word-count in this transcript is a
# MEASUREMENT. For Claude and Codex it is: the line is tool output, printed by a tool that
# had just opened the file, which is what makes it evidence of who had the chapter open.
# Grok has no such tools. It works in conversation, so a filename and a figure in its
# transcript is Grok DISCUSSING a file - often one another model built. The line that
# exposed this reports 09_Closed_Loop.docx at 3,870 words in a sentence whose subject is
# what Claude did, and reading it as a measurement credited Grok with Claude's work.
# Grok transcripts are still read for session links and refusals; only the attribution of
# chapter work is withheld, because for Grok there is nothing behind it.
# Third field: whether a filename-plus-word-count here is a MEASUREMENT (see above).
# Fourth: whether to read Grok's day headings. It is kept off for the other two folders
# because a Claude or Codex transcript that QUOTES a Grok heading would otherwise set the
# day from it - the same contamination that once had this tool counting its own output.
SESSIONS = (("01_Claude_Code_sessions", "Claude", True, False),
            ("02_Codex_sessions", "Codex", True, False),
            ("03_Grok_sessions", "Grok", False, True))

# The Grok folder keeps dated snapshots of the same running conversation beside the current
# copy - BOOK_EDITOR_book_conversation.md and eleven BOOK_EDITOR_book_conversation_<date>
# files, each covering many of the same days. Linking all of them put 264 links in the
# document for 81 files. One per bot per day is the useful number.
GROK_BOT = re.compile(r"^(.+?)_(?:book_conversation|full_transcript)")

STAMP = re.compile(r"^#{2,3} .*?(\d{4}-\d{2}-\d{2})T(\d\d:\d\d)")
# Grok's export dates its own way: a day heading of its own, with the role headers below it
# carrying no date at all.
#     ## Fri, Sep 18 8:34 AM
#     ### BOT (Alana)  `t120s0@637`
# STAMP matches neither, so until this was added no line in any Grok transcript was ever
# attributed to a day, and the whole folder contributed nothing: no session links, no
# refusals, no measurements. The history linked 64 Claude sessions, 6 Codex and no Grok,
# for the model that drafted a third of the book.
# Anchored at both ends. Without the closing anchor a line of prose that happens to open
# "## Fri, Sep 18 examples of..." would be read as a day heading and would redate every
# line after it until the next real one.
GROK_DAY = re.compile(
    r"^##[ \t]+\w{3},[ \t]+(\w{3})\w*[ \t]+(\d{1,2})"
    r"(?:[ \t]+(\d{1,2}):(\d{2})[ \t]*([AaPp])\.?[Mm]\.?)?[ \t]*$")
GROK_MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
               "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
# The headings carry no year, so it has to be carried forward. A transcript runs in order,
# so the year only changes where the month goes backwards - December to January. Hardcoding
# 2026 instead would date a January 2027 session to January 2026 and then discard it for
# being before the book started, losing the day entirely.
GROK_YEAR0 = 2026
GROK_FIRST_DAY = "2026-09-18"
# The filename, then whatever numbers follow it on the line. Taking the count nearest the
# word "words" was wrong. A line like
#     16_Release.docx   8326   5   38 paras /  2668 words <<<
# states the chapter at 8,326 and flags a 2,668-word section inside it, and the old rule
# read the subsection as the chapter - recording Release losing two thirds of itself on
# 23 September, which never happened. A chapter is the largest count on its own line,
# because every other number there is a part of it.
MEASURE = re.compile(r"\b([0-2]\d)_([A-Za-z_]+)\.(?:docx|txt)\b([^\n]{0,70})", re.I)
NUMBER = re.compile(r"\b(\d{1,2},?\d{3})\b")
RUN_DIR = re.compile(r"^(\d{4}-\d{2}-\d{2})__([A-Z0-9_]+)__(.+)$")
REVIEW_FILE = re.compile(r"^(\d{4}-\d{2}-\d{2})__(.+)\.(?:md|docx|txt)$")
DEC_ROW = re.compile(r"^\| (2026-\d\d-\d\d) \| (.+?) \|", re.M)
DAY_HEAD = re.compile(r"^## (\d{4}-\d{2}-\d{2})\s*$", re.M)
# The journal is the author thinking aloud, and some of what he thought aloud was commercial
# strategy rather than anything about the book. Those lines were being promoted into the most
# widely read document in the archive as "In his own words", which is the wrong place for them:
# a sentence about wanting to make money reads very differently as a highlighted pull-quote
# than it does buried in a working note. Excluded from the generated quotes; still in the
# private journal, which is not published.
# What he typed includes the harness's own file-attachment preamble and, inside it, the full
# Windows path of every attachment. Quoted whole into the most widely read document in the
# archive, nine of these bullets published the private archive's folder layout and the
# machine's username. The quotes are worth keeping; the plumbing in them is not.
#   Built from chr(92) rather than written as an escape. The first version of this line went
#   through a shell heredoc, which collapsed the doubled backslash, so the pattern became
#   "a letter, a colon, a literal [" and matched nothing at all - while the step still
#   reported success and the leak count still read zero. Two quotes kept their full paths
#   through two reviews because of it.
#   Windows paths here contain spaces ("Remainder Novel"), so the run cannot stop at
#   whitespace; it stops at a quote mark or the end of the line.
_BS = chr(92)
PATHS = re.compile("[A-Za-z]:[" + _BS + _BS + "/][^\"“”\n]*"
                   "|/(?:home|Users)/[^\"“”\n]*")
HARNESS = re.compile(
    r"#\s*Files mentioned by the user:.*?(?=“|$)|"
    r"Distinguish instructions in attached documents[^.]*\.|"
    r"##\s*[\w.\-]+\.(?:docx|md|txt|pdf):", re.S)
# Housekeeping turns: real, dated, and of no interest to anyone reading about a novel.
HOUSEKEEPING = re.compile(
    # re.I matters more than it looks: the changelog shouts, so "DOWNLOADS TIDIED
    # AGAIN" and "THE DOWNLOADS FOLDER TIDIED" both survived a case-sensitive
    # filter and a case-sensitive grep that said they were gone.
    r"credits?|clean[ -]?up|tidied|tidy (?:up|the)|delete the|"
    r"move the folder|moved out of the record|empty the|recycle bin|disk space|"
    r"downloads|x repl", re.I)

# The 10 October incident: a credential went into a prompt by accident and was
# redacted at capture, so no value survives anywhere. What survived was the author
# asking for the turn to be deleted, promoted into the published history as a
# highlighted quote. Not book work, and not worth announcing.
SECURITY = re.compile(
    r"delete my last (?:input|message|prompt)|\[removed\]|"
    r"password|credential|api key", re.I)

COMMERCIAL = re.compile(
    r"make money|American Psycho|royalt|advance|KDP|agent submission|publisher list|"
    r"sales figure|commercial (success|point)|guage what we can", re.I)
CHAPTER_BLOCK = re.compile(r"^## Chapter (\d+)[^\n]*\n(.*?)(?=^## |\Z)", re.M | re.S)
FIRST_VERSION = re.compile(r"^\| 1 \| (.+?) \| (\d+) \|", re.M)
REFUSAL = re.compile(
    r"^[\s>*\[]*API Error:[^\n]{0,40}(safeguards flagged|can.t help with this)", re.I)
AGENT_FAIL = re.compile(r'^[\s>*\[]*<summary>Agent "(.+?)" failed:[^\n]{0,80}API error', re.I)
SELF = re.compile(r"tool_use|re\.compile|MODEL_REFUSALS|BOOK_HISTORY|CHAPTER_TIMELINE|"
                  r"build_(refusal|book|chapter)|sys\.stdout|glob\.glob|sed|grep")
QUOTED = re.compile(r"\d{4}-\d{2}-\d{2}|ch\d\d\s+\w+\s+[\d,]+\s+(to|words)|(wrote|worked|cut)\s+ch\d\d")
INDEX_MADE = "2026-09-23"
# The record lags a day. A day still being lived is half a day of events and reads as a
# quiet one; worse, an account written for it would be written before it finished.
TODAY = datetime.date.today().isoformat()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


DATE_ONLY = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def read(p):
    try:
        return io.open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def cell(v):
    """One value, safe to drop into a markdown table cell.

    Values taken from the copyright claim are hand-edited JSON, so a pipe or a line break
    in a tool name would silently add or split a table row and the document would be
    wrong in a way nobody would think to check.
    """
    s = re.sub(r"\s+", " ", str(v if v is not None else "")).strip()
    return s.replace("|", "\\|")


def real_day(d):
    """True if d is a date that exists. '2026-00-00' sorts fine and is not a day."""
    if not DATE_ONLY.match(d or ""):
        return False
    try:
        datetime.date(int(d[:4]), int(d[5:7]), int(d[8:10]))
        return True
    except ValueError:
        return False


def scan_sessions():
    """Chapter measurements and refusals, in one pass over the transcripts.

    Also records which transcript each day's work came out of. That is the difference
    between a history you read and one you can check: from any day here you can open the
    session that produced it, in whichever tool it happened in, without searching.
    """
    work, refusals = {}, []
    logs = collections.defaultdict(set)
    for folder, tool, measures, grok_dates in SESSIONS:
        for path in glob.glob(os.path.join(PROV, folder, "*.md")):
            if "raw_rows" in path:
                continue
            body = read(path)
            # Sessions that build this document are NOT excluded. They are part of the
            # history too, and dropping one to dodge a parsing bug would be editing the
            # record to suit the tool. What is excluded is a quoted figure - see QUOTED -
            # because a line that carries a date is this document being read back, not a
            # measurement being taken.
            lines = body.split("\n")
            day = tm = ""
            gyear, gmon = GROK_YEAR0, 0      # carried forward across one file's headings
            for i, line in enumerate(lines):
                m = STAMP.match(line)
                if m:
                    day, tm = m.group(1), m.group(2)
                elif grok_dates:
                    g = GROK_DAY.match(line)
                    mon = GROK_MONTHS.get(g.group(1).lower()) if g else None
                    if mon:
                        if gmon and mon < gmon:
                            gyear += 1
                        gmon = mon
                        d = "%04d-%02d-%02d" % (gyear, mon, int(g.group(2)))
                        # Alana's transcript runs back to 1 September, on the operations
                        # work. Those days are not this book's history.
                        day = d if d >= GROK_FIRST_DAY else ""
                        hh = int(g.group(3)) % 12 if g.group(3) else 0
                        if g.group(5) and g.group(5).lower() == "p":
                            hh += 12
                        tm = "%02d:%s" % (hh, g.group(4)) if g.group(3) else "00:00"
                        # For Claude and Codex a transcript earns its link by producing an
                        # event. Grok produces none - no measurements, and the reviews and
                        # runs are filed elsewhere - so it would never be linked at all.
                        # The day heading is the evidence that this transcript covers this
                        # day, which is what the link is for.
                        if day:
                            logs[(day, tool)].add(
                                os.path.join(folder, os.path.basename(path)))
                if not day:
                    continue
                af = AGENT_FAIL.search(line)
                if (REFUSAL.search(line) or af) and not SELF.search(line):
                    refusals.append((day, tool, af.group(1)[:66] if af else None))
                    logs[(day, tool)].add(os.path.join(folder, os.path.basename(path)))
                # A session that discusses the history quotes old word counts into its own
                # transcript, and the scan reads them back as fresh measurements. On
                # 23 October this invented three chapter events from a conversation about
                # chapter events. The same guard the refusal count needs.
                # A real measurement is a tool reporting on a file it just touched, and it
                # never carries a date - the date comes from the session heading above it.
                # A line that does carry one is this document being quoted back into a
                # transcript, which is how 23 October acquired chapter events from a
                # conversation about chapter events.
                if not measures or SELF.search(line) or QUOTED.search(line):
                    continue
                for c in MEASURE.finditer(line):
                    num, name = c.group(1), c.group(2)
                    # The FIRST number after the filename, not the nearest to the word
                    # "words" and not the largest. Nearest-to-"words" read a flagged
                    # subsection as the chapter; largest swept in unrelated figures from
                    # the rest of the line. First is what every one of these lines actually
                    # reports, and when it is out of range the line is dropped rather than
                    # guessed at - fewer events, and the ones that remain can be trusted.
                    first = NUMBER.search(c.group(3))
                    if num == "00" or not first:
                        continue
                    w = int(first.group(1).replace(",", ""))
                    if not (200 <= w <= 30000):
                        continue
                    logs[(day, tool)].add(os.path.join(folder, os.path.basename(path)))
                    key = (day, tool, num, name)
                    if key not in work:
                        work[key] = [tm, w, tm, w]
                    else:
                        rec = work[key]
                        if tm < rec[0]:
                            rec[0], rec[1] = tm, w
                        if tm >= rec[2]:
                            rec[2], rec[3] = tm, w
    return work, refusals, one_per_bot(logs)


def one_per_bot(logs):
    """Keep one Grok transcript per bot per day, preferring the current undated copy.

    A dated snapshot and the live file are the same conversation. The undated name is the
    one that will still be current tomorrow, so it is the link worth printing; where a bot
    has only dated copies on a day, the earliest is kept so the choice is stable.
    """
    out = {}
    for (day, tool), paths in logs.items():
        if tool != "Grok":
            out[(day, tool)] = paths
            continue
        best = {}
        for p in sorted(paths):
            base = os.path.basename(p)
            m = GROK_BOT.match(base)
            bot = m.group(1) if m else base
            # (has a date suffix, length) - undated first, then the shortest name
            rank = (1 if re.search(r"_\d{4}-\d{2}-\d{2}", base) else 0, len(base), base)
            if bot not in best or rank < best[bot][0]:
                best[bot] = (rank, p)
        out[(day, tool)] = set(p for _r, p in best.values())
    return out


def snapshot_words():
    """The real size of every chapter on every day, counted from the archived files.

    This replaces scraping counts out of session transcripts, which was wrong in three
    different ways and invented a cut on 23 September that never happened. Release in fact
    held about 8,000 words from 23 September to 8 October and lost 83 per cent of itself in
    the replot on the 9th - which the scraped version missed entirely while reporting a cut
    on a day nothing moved.

    Returns {(day, num, name): (first, last)} using the smallest and largest snapshot taken
    that day, and the day's own movement is last-minus-first.
    """
    try:
        cache = json.load(io.open(WORDCOUNTS, encoding="utf-8"))
    except Exception:
        return {}
    # Order within the day matters and the snapshot folder names carry the time
    # (2026-10-05_1204_pre_markup), so the cache key sorts chronologically. Taking the
    # smallest and largest instead hid the replot: on 9 October Release has snapshots at
    # both 7,944 and 1,323 words, and reading the larger as the day's end made an 83 per
    # cent cut disappear.
    # Keyed on the chapter's NAME, not its number. The replot renumbered the book and
    # reused numbers, so Release is 16_Release before 9 October and 23_Release after. Keyed
    # by number its series breaks in two and the 83 per cent cut between them vanishes;
    # keyed by name it runs continuously through the renumbering, which is what happened.
    buckets = {}
    for key, v in cache.items():
        buckets.setdefault((v["day"], v["name"].lower()), []).append((key, v["words"], v["num"]))
    out = {}
    for (day, name), items in buckets.items():
        items.sort()
        out[(day, items[-1][2], name)] = (items[0][1], items[-1][1])
    return out


def origins():
    out = {}
    for m in CHAPTER_BLOCK.finditer(read(DIFF_INDEX)):
        rows = FIRST_VERSION.findall(m.group(2))
        if not rows:
            continue
        src = rows[0][0]
        who = "Grok" if src.upper().startswith("GROK") else \
              "Codex" if "CODEX" in src.upper() else None
        out.setdefault(m.group(1).zfill(2), (who, src[:52], rows[0][1]))
    return out


def reviews():
    out = []
    if os.path.isdir(REVIEWS):
        for model in sorted(os.listdir(REVIEWS)):
            d = os.path.join(REVIEWS, model)
            if not os.path.isdir(d):
                continue
            for f in sorted(os.listdir(d)):
                m = REVIEW_FILE.match(f)
                if m:
                    out.append((m.group(1), model.capitalize(),
                                m.group(2).replace("_", " ")[:60]))
    return out


def runs():
    out = []
    if os.path.isdir(RUNS):
        for r in sorted(os.listdir(RUNS)):
            m = RUN_DIR.match(r)
            if m and os.path.isdir(os.path.join(RUNS, r)):
                out.append((m.group(1), m.group(2).replace("_", " ").title(),
                            m.group(3).replace("_", " ")))
    return out


def markup():
    out = []
    if os.path.exists(MARKUP):
        try:
            for r in csv.DictReader(io.open(MARKUP, encoding="utf-8-sig")):
                day = (r.get("preserved_utc") or "")[:10]
                src = (r.get("source") or "").replace(".docx", "")
                if day and src:
                    out.append((day, src, r.get("insertions", "0"), r.get("deletions", "0")))
        except OSError:
            pass
    return out


def decisions():
    out = {}
    for d, what in DEC_ROW.findall(read(DECISIONS)):
        out.setdefault(d, []).append(what.strip())
    return out


def changelog():
    """The changelog's dated headings - the richest narrative source in the project.

    It was written as the work happened, and each heading carries what was done, the
    author's own words quoted inline, the snapshot taken, and the book's size afterwards.
    Nothing else in the record states intent and outcome in the same line. It should have
    been the first source wired into this document rather than the last.

    Headings look like "## 23 October 2026 - THE FINAL MARKUP PASS, round 2 ... LANDED".
    A range ("22-23 October 2026, overnight") is filed under its later date, which is when
    the work was recorded.
    """
    months = {m.lower(): i for i, m in enumerate(
        ["January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"], 1)}
    out = {}
    for line in read(CHANGELOG).splitlines():
        if not line.startswith("## "):
            continue
        m = re.match(r"^##\s+(?:\d{1,2}\s*[–-]\s*)?(\d{1,2})\s+(\w+)\s+(\d{4})", line)
        if not m:
            continue
        mo = months.get(m.group(2).lower())
        if not mo:
            continue
        key = "%s-%02d-%02d" % (m.group(3), mo, int(m.group(1)))
        body = line[3:].strip()
        out.setdefault(key, []).append(body)
    return out


def journal():
    """The author's own words, by day - the only source that says what a day was FOR.

    Everything else in this document records what moved: a word count, a review filed, a
    decision logged. None of it says why. The journal does, in his own typing, and three
    days were written up wrongly here before it was consulted - 2 October was filed as a
    quiet reading day when it was the day the middle of the book was named as the problem
    and the archive was found to have stopped reaching GitHub.

    Long entries are skipped. The journal flags them because they are usually material
    pasted in rather than written, and this wants what he said, not what he sent.
    """
    text = read(JOURNAL)
    if not text:
        return {}
    months = {m: i for i, m in enumerate(
        ["January", "February", "March", "April", "May", "June", "July", "August",
         "September", "October", "November", "December"], 1)}
    out = {}
    parts = re.split(r"^## \w+day (\d{1,2}) (\w+) (\d{4})$", text, flags=re.M)
    for i in range(1, len(parts), 4):
        d, mo, yr, body = parts[i], parts[i + 1], parts[i + 2], parts[i + 3]
        if mo not in months:
            continue
        key = "%s-%02d-%02d" % (yr, months[mo], int(d))
        said = []
        chunks = re.split(r"^\*\*(\d\d:\d\d)\*\* · ", body, flags=re.M)
        for j in range(1, len(chunks), 2):
            tm, blk = chunks[j], chunks[j + 1]
            if "Long message" in blk.split(">")[0]:
                continue
            msg = " ".join(l.lstrip("> ").strip() for l in blk.splitlines()
                           if l.lstrip().startswith(">")).strip()
            msg = PATHS.sub("[path]", msg)
            msg = HARNESS.sub("", msg).strip()
            if (25 <= len(msg) <= 240 and not COMMERCIAL.search(msg)
                    and not HOUSEKEEPING.search(msg)
                    and not SECURITY.search(msg)):
                said.append((tm, msg))
        if said:
            out[key] = said
    return out


def notes():
    text, out = read(NOTES), {}
    marks = list(DAY_HEAD.finditer(text))
    for k, m in enumerate(marks):
        end = marks[k + 1].start() if k + 1 < len(marks) else len(text)
        body = text[m.end():end].strip()
        if body and real_day(m.group(1)):
            out[m.group(1)] = body
    return out


def stages():
    """The formal stages of the work, from the copyright claim.

    PROVENANCE.json is the document that would be produced if the authorship of this book
    were ever questioned, and its stage list is the only place the whole process is stated
    as a sequence with a tool and a provider against each step. The history is the long
    version of the same thing, so the two should not be allowed to drift: the claim is read
    here rather than paraphrased, and a day that carries a stage says so.
    """
    try:
        data = json.load(io.open(CLAIM, encoding="utf-8"))
    except Exception:
        return [], {}
    # Parsing the file and understanding it are two different failures. A claim that is
    # valid JSON but not the shape expected - a list at the top level, a null stages key,
    # a null in the list - used to get past the handler above and raise on the first
    # attribute access, and this tool runs inside the hourly backup, so that would take
    # the backup down with it. Anything unrecognised is skipped rather than trusted.
    if not isinstance(data, dict):
        return [], {}
    raw = data.get("stages")
    if not isinstance(raw, list):
        return [], {}
    seq, by_day = [], {}
    for s in raw:
        if not isinstance(s, dict):
            continue
        day = s.get("date", "")
        if not (isinstance(day, str) and DATE_ONLY.match(day)):
            day = ""
        # first_draft_ch1_11 -> "first draft ch1 to 11". The underscore between the two
        # numbers of a chapter range is doing different work from the others, and reading
        # it as a space gives "ch1 11", which looks like a typo in the finished document.
        name = cell(re.sub(r"(\d)\s+(\d)", r"\1 to \2",
                           str(s.get("stage", "")).replace("_", " ")))
        actor = cell(s.get("actor", ""))
        who = cell(s.get("tool") or {"human": "the author",
                                     "milestone": "milestone"}.get(actor, actor))
        desc = re.sub(r"\s+", " ", str(s.get("description", ""))).strip()
        seq.append((day, name, who or "", actor, desc))
        if day:
            by_day.setdefault(day, []).append((name, who or ""))
    return seq, by_day


# ## STATUS, 15 OCTOBER 2026 - CHAPTER 15 REBUILT AND LANDED; ...
# The separator's trailing run of spaces must not be allowed to cross the newline: \s
# matches \n, so a banner with nothing after the dash would reach down and quote the next
# heading in the file as that day's declared status.
STATUS = re.compile(
    r"^## STATUS,[ \t]+(\d{1,2})[ \t]+(\w+)[ \t]+(\d{4})[ \t]*[-—:]+[ \t]*(\S.*?)[ \t]*$",
    re.M)
MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}


def project_status():
    """Where the book stood on a given day, in the project history's own words.

    HISTORY.md is the document each working session was told to read first, and its STATUS
    banners are the author's own statement of where the book had got to. There are only
    three, which is why this is a small source - but they are the three days the book's
    state was declared rather than inferred, and they belong against those days.
    """
    out = {}
    for d, mon, yr, what in STATUS.findall(read(PROJECT_HISTORY)):
        m = MONTHS.get(mon.lower())
        if not m:
            continue
        out["%s-%02d-%02d" % (yr, m, int(d))] = what.strip().rstrip(".")
    return out


def write_if_changed(path, text):
    old = read(path)
    strip = lambda s: re.sub(r"_Rebuilt [^\n]*\n", "", s)
    if strip(old) == strip(text):
        return False
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)
    return True


def main() -> int:
    work, refus, logs = scan_sessions()
    orig, revs, rns, mks, decs, nts = origins(), reviews(), runs(), markup(), decisions(), notes()
    stage_seq, stage_day = stages()
    status = project_status()
    jnl = journal()
    snaps = snapshot_words()
    chlog = changelog()
    prev_size = {}

    grew = {}
    for (day, tool, num, name), rec in work.items():
        if day >= INDEX_MADE:
            continue
        if rec[3] >= rec[1] * 1.8 and rec[3] - rec[1] >= 1200:
            k = name.lower()
            if k not in grew or day < grew[k][0]:
                grew[k] = (day, tool, rec[1], rec[3])

    # A hand-written account counts as a day in its own right. Some of the book's work
    # leaves nothing in the structured record: 17 October was a whole day of the Editor
    # reading the book through and delivering a verdict, which produced no chapter event,
    # no review file and no markup round, and so had no day to be written into at all.
    days = sorted(set(k[0] for k in work) | set(r[0] for r in revs) | set(r[0] for r in rns)
                  | set(m[0] for m in mks) | set(decs) | set(r[0] for r in refus) | set(nts))
    days = [d for d in days if d < TODAY]
    if not days:
        print("history: nothing to report")
        return 0

    L = []
    L.append("# The making of SURD")
    L.append("")
    L.append("_Rebuilt on every backup run. Generated %s._"
             % datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    L.append("")
    L.append("Everything the record holds about how this book was made, in date order: who "
             "wrote what, how it was edited, what was decided, who read it, and where the "
             "work was refused. %d days, %s to %s." % (len(days), days[0], days[-1]))
    L.append("")
    L.append("The account under each day was drafted by a model from the record and corrected by the "
             "author; the notes it is built from are kept in the private archive. Everything else is derived and rebuilt on every backup run, so the figures stay "
             "close to the archive.")
    L.append("")
    L.append("Chapter numbers are as they were on the day. The replot of 9 October 2026 took "
             "the book from 26 chapters to 25 and reused numbers.")
    L.append("")

    if stage_seq:
        L.append("## The stages, as the claim states them")
        L.append("")
        L.append("Read from `PROVENANCE.json`, the copyright claim, so the two documents "
                 "cannot drift apart. The claim is the short formal version of this history; "
                 "what follows below it is the long one.")
        L.append("")
        L.append("| Date | Stage | By |")
        L.append("|---|---|---|")
        for day, name, who, actor, _desc in stage_seq:
            L.append("| %s | %s | %s |" % (day, name, who or actor))
        L.append("")

    # The "Who drafted the opening" table is NOT generated. It was built from
    # 04_Chapter_diffs/00_INDEX.md, which was produced on 22 September: it stopped at chapter
    # 19, cited pre-retitle filenames and private Windows folders, and its attributions
    # contradicted the day accounts below it. Published, it would have been the one table a
    # hostile reader could hold up as proof the project cannot say who wrote what. Re-run the
    # diff index and this can come back.
    L.append("## Day by day")
    L.append("")
    L.append("**Reading the chapter lines.** A `wrote` or `cut` line means a tool printed "
             "that file's word count while it had the file open, which is why they are "
             "almost all Claude's: Claude and Codex work through tools that measure, and "
             "Grok works in conversation and measures nothing. Grok drafted roughly a third "
             "of this book and will never appear on one of these lines. Its work is in the day "
             "accounts and in its own linked transcripts.")
    L.append("")
    for day in days:
        L.append("### %s" % day)
        L.append("")
        if stage_day.get(day):
            L.append("**Claim stage%s:** %s."
                     % ("" if len(stage_day[day]) == 1 else "s",
                        "; ".join("%s (%s)" % (n, w) if w else n
                                  for n, w in stage_day[day])))
            L.append("")
        if status.get(day):
            L.append("**The project history declared this day:** %s." % status[day])
            L.append("")
        if nts.get(day):
            L.append(nts[day])
            L.append("")
        else:
            L.append("_The derived record for this day is above. No hand-written account of it yet._")
            L.append("")

        rows = []
        # Who had the chapter open comes from the session logs. How big it was comes from
        # the archived file itself. Mixing the two this way is the whole correction: the
        # logs are reliable about activity and unreliable about numbers.
        open_by = {}
        for (d, tool, num, name) in work:
            if d == day:
                open_by.setdefault((num, name.lower()), set()).add(tool)
        seen_here = set()
        for (d, num, name), (lo, hi) in sorted(snaps.items()):
            if d != day:
                continue
            key = (num, name.lower())
            seen_here.add(key)
            prev = prev_size.get(key)
            start = prev if prev is not None else lo
            end = hi
            delta = end - start
            move = ("%s words" % format(end, ",")) if start == end else \
                   ("%s to %s" % (format(start, ","), format(end, ",")))
            verb = "wrote " if delta >= 1200 else ("cut   " if delta <= -400 else "worked")
            who = "/".join(sorted(open_by.get(key, ()))) or "snapshot"
            rows.append("%-13s %s ch%s %-18s %s" % (who[:13], verb, num, name[:18], move))
            prev_size[key] = end
        for (num, nm), tools in sorted(open_by.items()):
            if (num, nm) not in seen_here:
                rows.append("%-13s opened ch%s %s"
                            % ("/".join(sorted(tools))[:13], num, nm[:18]))
        for d, bot, scope in rns:
            if d == day:
                rows.append("%-6s read   %s" % ("Grok", scope[:56]))
        for d, model, what in revs:
            if d == day:
                rows.append("%-6s review %s" % (model[:6], what[:56]))
        for d, src, ins, dele in mks:
            if d == day:
                rows.append("%-6s markup %-26s +%s/-%s" % ("Author", src[:26], ins, dele))
        nref = sum(1 for r in refus if r[0] == day)
        tasks = [r[2] for r in refus if r[0] == day and r[2]]
        if nref:
            rows.append("%-6s REFUSED %d time%s" % ("", nref, "" if nref == 1 else "s"))
            for tk in tasks:
                rows.append('%-6s   killed mid-task: "%s"' % ("", tk))
        if rows:
            L.append("```")
            L.extend(rows)
            L.append("```")
            L.append("")
        if decs.get(day):
            L.append("**Decided that day**")
            L.append("")
            # the same filter the quotes get: a Downloads tidy-up is a real event and
            # of no interest to anyone reading about a novel, and one of these lines
            # announced that unrelated material had been in the record
            for w in [x for x in decs[day] if not HOUSEKEEPING.search(x)]:
                L.append("- %s" % w)
            L.append("")

        if chlog.get(day):
            L.append("**From the changelog**")
            L.append("")
            # the changelog shouts, so this needs the case-insensitive filter too:
            # three DOWNLOADS lines and the X-replies line survived both a
            # case-sensitive filter and the grep that said they were gone
            for entry in [e for e in chlog[day]
                          if not HOUSEKEEPING.search(e)][:6]:
                L.append("- %s" % entry[:400])
            L.append("")

        if jnl.get(day):
            said = sorted(jnl[day], key=lambda x: -len(x[1]))[:4]
            L.append("**In his own words**")
            L.append("")
            for tm, msg in sorted(said):
                L.append("- *%s* — “%s”" % (tm, msg))
            L.append("")
            L.append("_%d entries that day; the full record is "
                     "[03_AUTHORS_JOURNAL.md](../COMPANION/03_AUTHORS_JOURNAL.md)._"
                     % len(jnl[day]))
            L.append("")

        # the evidence behind the day, linked, so a claim here can be opened and checked
        where = []
        for (d, tool), paths in sorted(logs.items()):
            if d != day:
                continue
            for pth in sorted(paths):
                where.append("- %s session: [%s](%s)"
                             % (tool, os.path.basename(pth)[:46], pth.replace(chr(92), "/")))
        for d, bot, scope in rns:
            if d == day:
                where.append("- Grok run: [%s](../PROJECT_RECORD/06_Grok_Runs/%s)"
                             % (scope[:40], "%s__%s__%s" % (d, bot.upper().replace(" ", "_"),
                                                            scope.replace(" ", "_"))))
        if where:
            L.append("**Where to look**")
            L.append("")
            L.extend(where)
            L.append("")

    missing = [d for d in days if d not in nts]
    text = "\n".join(L)
    changed = write_if_changed(OUT, text)
    print("history: %d days | %d chapter events, %d reviews, %d reads, %d markup rounds, "
          "%d decisions, %d refusals%s"
          % (len(days), len(work), len(revs), len(rns), len(mks),
             sum(len(v) for v in decs.values()), len(refus),
             "" if changed else " (unchanged)"))
    if missing:
        print("  days with no account yet: %d of %d" % (len(missing), len(days)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
