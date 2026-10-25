# SURD: An Unresolved Root — the working record

A novel whose prose was written entirely by AI language models, and the evidence record of
how that happened.

The book is 25 chapters and 58,283 words, counted across the chapter documents on 25 October
2026 (57,775 counting labelled prose only). More than 8,000 prompts across three models —
Claude, Grok and Codex — produced it. The author set the premise, the rules the narrator lives
under and the brief for every chapter, approved or refused everything that came back, and wrote
none of the sentences.

This repository is the record, not the book.

---

## What the author did, and did not do

He chose the premise and typed it, unedited, into a chat window: a first-person account kept by an
artificial intelligence, looking back over thirty-one years. He chose the tone from options the
model offered, then re-anchored it when it drifted. He set the briefs for every chapter, and directed the canon and the rules the narrator
lives by rather than writing them: both were drafted by the models and frozen on his say-so. He commissioned the audits, read the findings, and
approved or refused each one. He marked up the chapters by hand, in tracked changes, and argued with the reviewers when he
disagreed. The manifest counts over 120 rounds; 25 of them are preserved as files, covering
nine chapters, and the rest are in the private snapshots.

He deliberately wrote no prose. The narrator is a machine, and he wanted the narration to be one.
His own account of the method: *I guide and approve.*

**One definition, because the record would otherwise read two ways.** Where this archive says "the
author's own" text, or that a passage of his was left untouched, it means *the version he approved*,
not text he wrote. His only direct intervention in the prose is occasional: a single word swapped
for a better one, a term changed because it was wrong for the world — ward to precinct, and the
like. Those words reach the page the same way everything else does, through a brief to a model. He
wrote no sentences, and he claims no expression on the basis of the substituted words. The formal
version is in [`PROVENANCE.json`](PROVENANCE.json) under `method.summary`.

The one part of the finished book he writes himself is the addendum, on how and why it was made.

## The three models, and what each one did

**Grok** drafted. Chapters 1 to 11 were produced in a single morning on 18 September 2026, then
redrafted repeatedly against a locked style package. It later ran as a staff of separate agents — an
Editor, a Cover Designer, a series of Cold Readers — each briefed and each given the book to
read fresh.

**Claude** cut what Grok had written and wrote what came after it, then built the archive, the
tooling and every document in this repository.

**Codex** judged. It delivered the first whole-book assessment and the only complete read of the
replotted book, and it was used throughout as an adversary: asked to prove the work wrong rather
than to praise it.

All three reviewed. A single cold read of chapters 1 to 12 was also taken from Gemini on 14
October, on a free account and in one pass; it is in the logs with everything else, and is
not counted among the three. [`BOOK_HISTORY.md`](BOOK_HISTORY.md) has it day by day.

## The parts that are not flattering

They are in here because without them the rest is not worth believing.

**197 refusals.** On 21 September 2026 the work stopped roughly every few minutes for eighteen
hours: a safeguard classifier refused to process the manuscript, 172 times in one day. It kept
happening for another month. Ninety per cent of the refusals that name a chapter involve the same
five-chapter block. [`MODEL_REFUSALS.md`](MODEL_REFUSALS.md) counts every one and sets out what the
clustering appears to mean — and what it does not establish.

**The book was cut by more than a third.** It reached a complete draft of 95,012 words on 30 September.
A replot on 9 October cut it to 25 chapters, planned at about 75,000 words; the rewrite
landed at 60,682 on 10 October, and revision brought it to 58,283 by 25 October. Most chapter titles changed and
the numbering was reused, so every chapter number in the history has to be read as of its own date.

**Reviewer findings were adopted on their merits rather than by whose they were**, and the
record shows which, including the arguments the author lost. It also shows the models correcting themselves: an
attribution withdrawn, a comparison admitted to be false, a proposal withdrawn when it did not
survive checking.

**Mistakes in the record are marked in the record.** Four figures in the day accounts were wrong
before the archived files were counted properly, one of them backwards. The corrections are left
visible rather than quietly fixed.

**It was a biological-risk filter.** Every one of the 197 refusals carried the reason code
`[bio]`, and they cluster on five chapters: the arc from preparing the event to its aftermath. So
the honest version of this is not *the novel an AI would not write* but *a biosafety classifier blocked
work on this book 197 times, and here is the record of it.*

The answer is in the book's own method. **No procedure may be given anywhere in the novel** — that is a standing rule, written into the canon on the day the refusals started, and the
narrator's own stated method is that technique appears only as constraints and consequences. The book's standing rule is that nothing in it can be followed, and no reviewer has found
otherwise. The refusals also fired on a day when the only chapter open was
chapter 9, and again on chapter 23 five weeks later, so the pattern suggests they tracked how much of the
book was in one request rather than any single passage. Of the 197, 120 name no chapter at all;
the five-chapter clustering is 69 of the 77 that do.

**And most of the reviews in this archive were done by AI.** 230 of them. That is not a hidden
fact to be discovered in the logs — it is why the author's own side of the record, 8,837 author turns and 824,327 words of direction against a 58,283-word book (measured on the published logs, 25 October 2026), is the part that carries the weight.
Models reviewing models proves very little on its own.

## How to check any of it

| Question | Document |
|---|---|
| What happened on a given day, who did it, and why it mattered | [`BOOK_HISTORY.md`](BOOK_HISTORY.md) |
| Every time a model refused to process the book | [`MODEL_REFUSALS.md`](MODEL_REFUSALS.md) |
| The formal authorship claim, stage by stage | [`PROVENANCE.json`](PROVENANCE.json) |
| What is claimed, and what is not | the section below |
| How the figures above were produced | [`tools/`](tools/) |
| The conversations themselves, all 131 transcripts (128 distinct sessions) | [`logs/`](logs/) |
| What the unpublished raw files are, fixed by hash | [`RAW_SESSIONS.md`](RAW_SESSIONS.md) |

The documents in `tools/` are the method. They read filenames, counts, timestamps and error
strings, never prose, and they rebuild the derived documents on every backup run, so the figures stay close to the archive.
Anyone who wants to know where a number came from can read the code that produced it.

## What is not here, and why

**The novel.** Publishing it here would give the book away, permanently and in one command.

**The chapter diffs.** The 83 word-level HTML diffs render every chapter in full across every
version — about 298,000 words, 5.2 times the length of the novel. The index that summarised them
was a month out of date and stopped at chapter 19, so it was pulled rather than published stale.

**The ending.** Chapter 25 is 957 words and the logs happen to cover all of it. Its prose is removed
wherever it appears, and each removal carries its word count and the first 16 hex digits of a SHA-256 of what was
taken, so anyone given the private archive can confirm that only that was removed.

**Nothing else of the book.** That is a decision rather than an oversight, so here is
the number, measured on 25 October 2026 against the 25 chapters as they now stand:

> **1,261 of the book's 1,531 distinctive sentences appear somewhere in [`logs/`](logs/).**
> That is 82% of them, and they carry 24,857 words, so about 43% of the book's 58,283 words
> can be found in the transcripts somewhere. The sentences that recur are the short, quoted,
> argued-over ones, which is why the share of sentences is well above the share of words.
> They are also scattered. Book text appears in 3,398 separate places across 6.66 million
> words of transcript, and 3,210 of those places are a single isolated paragraph with no book
> text on either side of it. The longest unbroken run anywhere is six paragraphs. Anyone
> reassembling the novel from this would be left with an unordered bag of paragraphs and 57%
> of the book missing. Removing it would have cost the most interesting thing in the archive
> to defend against very little.

**What is held back is the archive itself**, not its contents: 316 MB of dated chapter snapshots, the
file-level pre-edit history, and the git history whose commit chain the Bitcoin proofs anchor. It is shown
in full on request — to an agent, a publisher's lawyer, a registration examiner, a journalist, or
anyone else who asks and has a reason.

**Which version of the archive this is.** This repository was built from the private archive at
commit `10bc6d019512d0660485cf5e10c40ff5dd4d640f`, committed on 25 October 2026. That commit is anchored by
[`timestamps/HEAD_2026-10-25_public-release.txt.ots`](timestamps/HEAD_2026-10-25_public-release.txt.ots), so the state
it was derived from is dated independently of anything said here. The archive has not stopped:
the book goes to beta readers next and their responses will produce revisions, so the private
repository will move ahead of this one. When it does, this copy still corresponds to that
commit, and the figures in it were measured against the chapters as they stood that day.

## Proving when the work happened

This repository's own commits begin the day it was created, so its history proves nothing about
dates. [`timestamps/`](timestamps/) is how you check anyway, and you do not have to take anyone's
word for it.

Each `HEAD_<date>.txt` records the private archive's state on that date: the HEAD commit hash, when
it was committed, and how many commits the archive held. Beside it, each `.ots` file is an
[OpenTimestamps](https://opentimestamps.org) proof anchoring that file's SHA-256 to the **Bitcoin
blockchain**. Twenty-three of them, from 30 September 2026 onward.

A git commit hash is the root of a Merkle tree over the entire repository — every file, every
directory, every parent commit. Change one byte anywhere in the history and the hash changes. So a
proof over a single 40-character hash establishes that **the whole archive behind it existed at that
moment**, without publishing any of its contents.

To verify, install the OpenTimestamps client and run:

```
ots verify timestamps/HEAD_2026-09-30.txt.ots
```

It will report the Bitcoin block that attests the file, and the date that block was mined. The claim it supports is narrow: *this exact file existed no later than that date.* What the
hash inside it covers can only be confirmed by someone holding the archive, which is the point
of showing the archive on request. Anyone can
run it, forever, without the author's cooperation and without access to the archive.

---

## What is claimed, and what is not

The prose of the novel was generated by language models under direction. The author wrote none of
the sentences, and says so everywhere rather than being caught at it.

What is claimed is the work as a whole: the premise, the structure, the rules the narrator lives
under, the selection of what stayed and what went, the editorial direction — 8,837 author turns
and 824,327 words of it, against a 58,283-word book — and the addendum, written by the author
himself.

Whether copyright subsists in machine-generated prose is unsettled in both the UK and the US.
Nothing here asserts that it does. All rights that do exist are reserved, and no permission is
granted to reproduce the novel or to train models on it.

This position does not depend on that question being resolved. It depends on the record, which is
dated, anchored to the Bitcoin blockchain, and open to anyone who asks.

---

*The novel is all rights reserved. The tooling is MIT. See [`LICENSE`](LICENSE).*
