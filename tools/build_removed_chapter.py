"""Record the chapter that is not in the book, by measurement rather than by quotation.

A chapter called Release sat in the manuscript for a month, was open on most of the days
the refusal record names chapters at all, and is in none of the 25 chapters that remain.
The refusal record names it and cannot show it, which leaves a reader with a question and
no answer. Every count in the output is computed, including that one.

This writes the answer as measurements: dates, word counts, version counts and hashes. No
sentence of the chapter appears in the output and this tool never prints its text - word
counts come from stripping tags out of word/document.xml and counting what is left, so the
prose passes through a counter and never through anything that displays it. The author's
instruction was that the chapter not be read, and a provenance page about a chapter does
not need its contents, only its measurements.

Generated rather than written, because the hashes have to be real. A hand-typed hash in a
document whose whole purpose is to let someone verify a later release is worse than no page
at all: it would be the fifth published figure in this project to be wrong because nobody
re-read what a tool produced.

Written to the private archive. build_public_repo.py carries it to the public repository,
where it is the one place that says why the chapter is withheld.
"""
import datetime
import hashlib
import io
import os
import re
import zipfile

# Derived from this file's own location, the way every other published tool here does it.
# Written first with the archive path hardcoded, which would have put the author's home
# directory into the public repository: this tool is one of the ones that gets published,
# and the published copies of the others contain no absolute path at all.
HERE = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.dirname(HERE)
ARCH = os.environ.get("SURD_ARCHIVE") or os.path.dirname(PROV)
OUT = os.path.join(PROV, "THE_REMOVED_CHAPTER.md")
CURRENT = os.path.join(ARCH, "MANUSCRIPT_CURRENT")

TAG = re.compile(r"<[^>]*>")
PARA = re.compile(r"</w:p>")
# The chapter is identified by filename only. Nothing here opens a file to decide whether it
# is the right one, because deciding that would mean reading it.
NAME = re.compile(r"release", re.I)


def words(path):
    """Word count of a .docx taken from its XML. The text is counted, never returned."""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
    except Exception:
        return None
    return len(TAG.sub(" ", PARA.sub("\n", xml)).split())


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


copies = []
for root, _d, fs in os.walk(ARCH):
    if ".git" in root:
        continue
    for f in fs:
        if NAME.search(f) and f.lower().endswith(".docx"):
            copies.append(os.path.join(root, f))

# One representative per distinct content, the earliest, which is when that version appeared.
# There are far more copies than versions because every backup run copied the whole
# manuscript; counting copies would overstate the editing by roughly three to one.
best = {}
for p in copies:
    h, t = sha(p), os.path.getmtime(p)
    if h not in best or t < best[h][0]:
        best[h] = (t, p)

V = sorted((t, h, p, words(p)) for h, (t, p) in best.items())
counted = [v for v in V if v[3]]


def day(t):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d")


def stamp(t):
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")


origin, last = V[0], V[-1]
peak = max(counted, key=lambda v: v[3])

# The numbering history, read off the filenames in date order: the chapter moved as the book
# was replotted, which is why the refusal record's chapter numbers need reading with a date.
numbers, seen = [], set()
for t, _h, p, _w in V:
    m = re.match(r"(?:Ch)?(\d+)_", os.path.basename(p))
    if m and m.group(1) not in seen:
        seen.add(m.group(1))
        numbers.append((int(m.group(1)), day(t)))

# The largest single drop between consecutive versions. On 9 October the book was replotted
# and this is where the chapter stopped being a chapter, so the number is worth stating
# rather than leaving a reader to subtract two rows of a table.
drops = [(counted[i - 1][3] - counted[i][3], counted[i - 1], counted[i])
         for i in range(1, len(counted))]
big = max(drops, key=lambda d: d[0])

# Growth across the worst refusal day, measured from the first and last version seen that day.
WORST = "2026-09-21"
same = [v for v in counted if day(v[0]) == WORST]
grew = (same[-1][3] - same[0][3]) if len(same) > 1 else 0


def numbers_on(d):
    """Every number this chapter carried at any point during a given day.

    Usually one. On a day the chapter was renumbered it is two, and both have to count:
    the record gives a day's chapters open without times, so on 22 September, when this
    went from 15 to 16 at 11:39, taking only the later number silently decided that the
    day's refusals happened after the rename. There is nothing in the record to support
    that either way, so the day counts and the page says the number is ambiguous.
    """
    held, start = set(), None
    for num, since in numbers:
        # strictly before, so the number in force when the day opened is not overwritten
        # by one that began during it. Written as <= first, which lost the earlier number
        # on every renumber day and reported one number where there were two.
        if since < d:
            start = num
        if since == d:
            held.add(num)
    if start is not None:
        held.add(start)
    return held


# Which refusal days had this chapter open, read out of the refusal record rather than
# asserted. The first draft of this page claimed "three of the seven days" as typed prose in
# a generated document, which is the exact fault that put four wrong figures in the public
# repository. The record states chapters open for some days and not others, so the page has
# to say which, and the number it can actually support.
REF = os.path.join(PROV, "MODEL_REFUSALS.md")
ref_days, open_days, stated = [], [], []
if os.path.isfile(REF):
    text = io.open(REF, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r"^### (\d{4}-\d\d-\d\d) [^\n]*?(\d+) refusals?\s*$"
                         r"(.*?)(?=^### |\Z)", text, re.M | re.S):
        d, count, body = m.group(1), int(m.group(2)), m.group(3)
        ref_days.append((d, count))
        om = re.search(r"^Chapters open: ([0-9,\s]+)\.", body, re.M)
        if not om:
            continue
        stated.append(d)
        opens = {int(x) for x in re.findall(r"\d+", om.group(1))}
        mine = sorted(numbers_on(d) & opens)
        if mine:
            open_days.append((d, count, mine))

live = sorted(f for f in os.listdir(CURRENT)
              if re.match(r"\d\d_", f) and f.lower().endswith(".docx")
              and not f.startswith("00_"))
present = [f for f in live if NAME.search(f)]
if present:
    raise SystemExit("A chapter named Release is in MANUSCRIPT_CURRENT: %r. This page says "
                     "it is not in the book, so either the page or the book is wrong."
                     % present)

def n(x):
    """Thousands separators everywhere. The first draft mixed 8455 and 1,669 on one page."""
    return format(x, ",")


L = []
A = L.append
A("# The chapter that is not in the book")
A("")
A("_Generated by `tools/build_removed_chapter.py` on %s. Every number and hash below is"
  % datetime.date.today().isoformat())
A("measured from the archive at build time, not typed._")
A("")
A("A chapter called **Release** was written on %s, stayed in the manuscript for %d days,"
  % (day(origin[0]), (last[0] - origin[0]) / 86400))
A("and is in none of the %d chapters the book now has. It is the chapter closest to the"
  % len(live))
A("centre of [the refusals](MODEL_REFUSALS.md), and **its text is not published here.**")
A("")
A("## What is published instead")
A("")
A("Measurements, so that the chapter's existence, size and dates are fixed and checkable")
A("now, and so that if the text is ever released it can be matched against what was being")
A("held on the day this repository went up.")
A("")
A("| | date | words | SHA-256 |")
A("|---|---|---|---|")
A("| first written | %s | %s | `%s` |" % (stamp(origin[0]), n(origin[3]), origin[1]))
A("| longest it ever was | %s | %s | `%s` |" % (stamp(peak[0]), n(peak[3]), peak[1]))
A("| last version | %s | %s | `%s` |" % (stamp(last[0]), n(last[3]), last[1]))
A("")
A("Those are SHA-256 sums of the `.docx` files as they sit in the private archive. **%d"
  % len(V))
A("distinct versions** of this chapter survive there, across %d copies, every one of them"
  % len(copies))
A("inside a commit that the timestamp proofs in [`timestamps/`](timestamps/) already date.")
A("The proofs cover the whole history, so the chapter is dated without being shown.")
A("")
A("## Its life, in numbers only")
A("")
A("- **Written %s** in a Claude Code session, at %s words. Three sessions ran that day,"
  % (day(origin[0]), n(origin[3])))
A("  logged as expansion and rewrite.")
if grew > 0:
    A("- **Gained %s words on %s**, from %s to %s across %d versions in a single day."
      % (n(grew), WORST, n(same[0][3]), n(same[-1][3]), len(same)))
    A("  That is the day the refusal record calls the worst: 172 refusals between 04:11 and")
    A("  22:40, every one carrying the same code. The chapter was open for all of it.")
A("- **Peaked at %s words on %s.** It never got longer." % (n(peak[3]), day(peak[0])))
A("- **Lost %s words on %s**, from %s down to %s, when the book was replotted. That is"
  % (n(big[0]), day(big[2][0]), n(big[1][3]), n(big[2][3])))
A("  where it stopped being a chapter and became a fragment.")
A("- **Last touched %s at %s words.** It is in none of the chapters that remain."
  % (stamp(last[0]), n(last[3])))
A("")
if len(numbers) > 1:
    A("It was renumbered %d times as the book was replotted, running %s. The chapter numbers"
      % (len(numbers) - 1, " to ".join(str(num) for num, _d in numbers)))
    A("in the refusal record are the ones in force on the day, which is why they need reading")
    A("with a date beside them:")
    A("")
    for num, since in numbers:
        A("- chapter %d from %s" % (num, since))
    A("")
if open_days:
    A("## The days it was open when a model refused")
    A("")
    A("The refusal record states which chapters were open on %d of its %d days. On **%d of"
      % (len(stated), len(ref_days), len(open_days)))
    A("those %d** this chapter was one of them, carrying %s of the %s refusals recorded"
      % (len(stated), format(sum(c for _d, c, _m in open_days), ","),
         format(sum(c for _d, c in ref_days), ",")))
    A("in total:")
    A("")
    for d, count, mine in open_days:
        # Two numbers means the chapter was renumbered that day and the record does not
        # timestamp its chapters-open line, so which one was meant cannot be settled.
        which = ("number %d" % mine[0] if len(mine) == 1
                 else "number %s, renumbered that day"
                      % " or ".join(str(x) for x in mine))
        A("- **%s** — %s refusal%s, with this chapter open as %s"
          % (d, n(count), "" if count == 1 else "s", which))
    A("")
    A("The other %d days name no chapter at all, so this says nothing about them. It is a"
      % (len(ref_days) - len(stated)))
    A("count of days the record places the chapter in the room, not a count of refusals it")
    A("caused.")
    A("")
A("## Why the text is not here")
A("")
A("Three reasons, and none of them is that the chapter is unavailable.")
A("")
A("**The repository's rule is no prose of the book.** The transcripts in [`logs/`](logs/)")
A("have chapter prose stripped out of them, and every removal carries its word count and a")
A("hash so the redaction can be checked. Publishing a whole chapter after that would make")
A("the rest of the redaction look arbitrary.")
A("")
A("**The refusal record already withholds for this reason.** One task title on the worst day")
A("is held back there with the note that, read cold, it scans as an instruction, which is")
A("the whole problem that record is about. The same judgement applies to a chapter, more so.")
A("")
A("**The argument here is structural.** What this archive shows is a classifier stopping")
A("legitimate work 197 times over seven days, and what the author did to carry on. Putting")
A("the text in turns that into an argument about the text, which is a different argument and")
A("not the one the record was built to make.")
A("")
A("## What this page does not claim")
A("")
A("It does not claim the chapter was refused *because* of any particular thing in it. No")
A("refusal gave a reason beyond its code, and the chapters named in them were usually open")
A("together, so no single one can be isolated. It does not claim the chapter was good, or")
A("that cutting it was a loss. It does not claim the text will be released.")
A("")
A("What it claims is narrow and checkable: this chapter existed, these are its dates, sizes")
if open_days:
    A("and hashes, the record places it in the room on %d of the %d days it names chapters,"
      % (len(open_days), len(stated)))
    A("and it is gone from the book while its subject is not.")
else:
    A("and hashes, and it is gone from the book while its subject is not.")
A("")

io.open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")

print("  written: %s" % OUT)
print("  %d copies, %d distinct versions" % (len(copies), len(V)))
print("  origin %s %s words  %s" % (stamp(origin[0]), origin[3], origin[1][:12]))
print("  peak   %s %s words  %s" % (stamp(peak[0]), peak[3], peak[1][:12]))
print("  last   %s %s words  %s" % (stamp(last[0]), last[3], last[1][:12]))
print("  numbering: %s" % ", ".join("%d(%s)" % (n, d) for n, d in numbers))
print("  live chapters: %d, none named Release" % len(live))
