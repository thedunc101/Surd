# Blockchain timestamps

*Set up 30 September 2026.*

## What these files are

Each `HEAD_<date>.txt` records the repository's state on a date: the HEAD commit hash, when
it was committed, and how many commits the repository held. Each `.ots` file beside it is an
OpenTimestamps proof that anchors that file's SHA-256 to the **Bitcoin blockchain**.

A proof is about 800 bytes and says one thing, verifiable by anyone, forever: *this exact
content existed no later than the date this block was mined.*

## Why a git commit hash is enough

A commit hash is the root of a Merkle tree over the entire repository — every file, every
directory, every parent commit. Change a single byte anywhere in the history and the hash
changes. So timestamping one 40-character hash proves that **the whole archive behind it
existed at that moment**, without publishing anything.

## Why this exists at all

The strongest thing in this archive is not the files. It is that a third party holds a dated
record of when each push arrived, which the author cannot backdate.

That record lives in one company's account. The OneDrive bundle protects the *data* if that
account is lost — every file survives — but it proves nothing about *when*, because it is the
author's own file in the author's own folder, with commit dates set by his own machine.

**A blockchain timestamp is the part that survives losing everything.** No account, no
company, no hosting. If GitHub vanished, OneDrive vanished, and every credential were lost,
these proofs would still establish that the work existed by these dates. That is the piece
of the copyright claim that cannot be reconstructed after the fact.

## Privacy

Only a SHA-256 digest leaves the machine. The calendar servers never see a filename or any
content, and a hash reveals nothing about what it was computed from. Nothing in this archive
becomes public by being timestamped.

## Pending versus complete

A fresh proof is a **pending commitment**: the calendar servers have accepted the hash and
promised to include it in a Bitcoin transaction. It becomes **complete** when that block is
mined, a few hours later, and the proof is upgraded to carry the block header path.

Both are real. A pending proof is backed by four independent calendars
(`opentimestamps.org` ×2, `eternitywall.com`, `catallaxy.com`); a complete one needs no
trust in them at all.

## How it runs

The scheduled task **Remainder blockchain timestamp**, daily at 09:45, runs
`PROVENANCE\tools\ots_stamp.py --auto`, which:

1. upgrades every pending proof whose Bitcoin block has since confirmed, then
2. stamps the current HEAD, unless the day is already stamped.

It is set to start when available, so a day the laptop is off is collected on the next run.
Nothing is lost by missing a day: the calendars hold the commitment regardless.

## Commands

```
python PROVENANCE\tools\ots_stamp.py            stamp the current HEAD now
python PROVENANCE\tools\ots_stamp.py --upgrade  complete confirmed proofs
python PROVENANCE\tools\ots_stamp.py --verify   check every proof on disk
```

To verify without this repository, anyone can install the OpenTimestamps client and run
`ots verify HEAD_<date>.txt.ots` with the matching `.txt` file beside it.

## A note on the workaround in the tool

The `opentimestamps-client` package cannot import on this machine: it pulls in
`python-bitcoinlib`, which loads OpenSSL 1.0-era symbols that OpenSSL 3 no longer provides.
Those symbols are only used for Bitcoin key operations, which stamping never performs —
stamping talks to calendar servers over HTTP. The unused loader is therefore stubbed before
the import, and restored immediately after. If anything ever does reach for it, it fails
loudly rather than producing a bad proof. This is documented because a workaround nobody
recorded is a workaround nobody can audit.
