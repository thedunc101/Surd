# The session logs

Every conversation in which this book was written, across three models and five weeks. 131 transcripts (128 distinct sessions), about 6.6 million words.

> **Spoiler warning.** These logs discuss the book's ending throughout and in detail. If you intend
> to read the novel, read it first.

## What is in here

| Folder | Files | What it is |
|---|---|---|
| `01_Claude_Code_sessions/` | 77 | Claude. Cut the opening chapters, wrote the middle of the book, built the archive and the tooling. |
| `02_Codex_sessions/` | 46 | Codex. The judge — whole-book assessments, acquisition reads, and the adversary asked to prove the work wrong. |
| `03_Grok_sessions/` | 15 | Grok. Drafted chapters 1 to 11 in a morning, then ran as a staff: an Editor, a Cover Designer, a series of Cold Readers. |

The Grok folder holds one file per bot. The private archive also keeps dated snapshots of each
running conversation, which are copies of the same material rather than separate work.

Two Claude sessions ran for weeks and were too large to render in a browser, so they are split on
day boundaries into seven parts. The original filename is kept as an index of its parts, so every
link into it still resolves.

## What has been removed, and what has not

**Removed: the prose of the final chapter**, wherever it appears. Each removal is marked in place:

```
> `[final-chapter text removed — 84 words, sha256:3f9c1a2b7d4e5f60]`
```

*(An example. Real markers carry the real counts and hashes.)*

The word count and hash mean anyone given the private archive can confirm that exactly that was
taken out and nothing else. Chapter 25 is 957 words, and the logs happened to cover all of it.
Spoiling the ending is the one exposure here with a real cost.

**Also removed: 69 sentences, at the author's request.** One line of commercial positioning, which
sat in a review rubric that was pasted into session after session. Each removal is marked the same
way, with its word count and a hash prefix:

```
`[removed at the author's request — 14 words, sha256:a1b2c3d4e5f60789]`
```

*(That is an example, not a real marker.)*

Nothing else has been taken out. The hashes in all markers are the first 16 hex digits of a
SHA-256, not the full digest.

**One disclosure, deliberately undated.** A credential was pasted into a session by mistake at
some point in the project. It was not repeated or used, and it was blanked from the saved
transcripts before any of this was published. The day is not named, because naming it would
tell a reader which transcripts to search.

**Not removed: everything else, including a good deal of the book.** About 43 per cent of the
novel's words appear somewhere in these files: 1,261 of its 1,531 distinctive sentences,
carrying 24,857 words, measured on 25 October 2026 against the 25 chapters as they now stand. That is a decision, not an accident:

Of the 1,723 distinctive sentences in the finished chapters, 1,307 appear at least once across these
transcripts. They are scattered — 95 per cent of occurrences are a single isolated paragraph, and
the longest unbroken run anywhere in 6.6 million words is six paragraphs. It is what *fix paragraph
36* and *read paragraph 12 again* look like on the page. Reassembling a novel out of that is unlikely to be worth anyone's effort, and what they would get
is an unordered bag of paragraphs with more than half missing. Stripping it would have cost the most
interesting thing in this archive to defend against a threat worth very little.

## How to read them

The transcripts are long and nobody should read them end to end.
[`../BOOK_HISTORY.md`](../BOOK_HISTORY.md) is the way in: it goes day by day, says who did what, and
links the session each day came out of. Start from a day that interests you and follow the link.

Some days worth that treatment:

- **18 September 2026** — the first day. The premise typed into a chat window, and chapters 1 to 11
  drafted by Grok in a single morning.
- **21 September 2026** — the day the work stopped. 172 safeguard refusals in eighteen hours.
- **9 October 2026** — the replot. 26 chapters to 25, and the book cut from 95,012 words to a planned 75,000; the rewrite landed at 60,682 the next day, and revision took it to 58,283.
- **17 October 2026** — the Editor reads the whole book and delivers a verdict, and withdraws a
  claim it had made about its own experience.

## What these are not

They are a working record, not a performance. They contain the author losing arguments, models
contradicting each other and themselves, wrong figures later corrected, and long stretches of
mechanical work. One credential was pasted in by mistake and has been blanked.

The models' side is also, inevitably, models talking about their own output. Most of the reviews in
this project were done by AI. That is stated here rather than left for someone to discover: it is
why the author's own side — 8,837 author turns and 824,327 words of direction, against a 58,283-word
book — is the part that carries the weight.
