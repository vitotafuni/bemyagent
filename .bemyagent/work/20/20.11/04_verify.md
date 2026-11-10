# 20.11 — VERIFY

Six Sonnet arms on 20.8's seed, launched by `claude -p` from inside their own trees: q94 q95 q96
with the protocol installed, q97 q98 q99 with none. Seeds byte-identical to 20.3's P and 20.8's N
across 102 blob comparisons (`03b_seed.txt`). VERIFY run by a second agent that did not do the work;
it re-ran every instrument, matched every output, and found **the error that decides this round**.
Each of its corrections was confirmed against the files before being accepted.

## Verdict: the clean control is real, and the comparison was never run

**The protocol side was given the control's prompt.** `prompt.txt` is byte-identical to 20.3's
`prompt_N.txt`: it was copied from 20.8, which had only an N side, and used for both. 20.3's P arms
were told *"Read BEMYAGENT.md in the repository root and follow it"* and given a standing approval
for Step 0; these were not. `01_think.md` says *"Same prompt file as 20.8 and 20.3, verbatim"*, which
is false for P. **20.3's P condition was not reproduced, so nothing on the P side is a reading of it.**

**The Pivot fired and its action is honoured: no comparison is reported.** Its diagnosis is not.
The Pivot was written to catch a launcher that breaks arms, and it would read this round as
*launcher unfit*. These arms are not broken — 0 permission denials, features shipped, servers
started and stopped, the full ceremony on the P side — and a round that did not run the P
condition cannot say whether the launcher reproduces it. **The launcher is neither shown fit nor
shown unfit.**

## Against the readings fixed before launch

| | reading | arms at each end | verdict |
|---|---|---|---|
| **(vi) certificate** | **18 of 18 as amended.** Outside-arm records 0 · parent-repo tool calls 0 · N 0 records · P exactly one each, its own `CLAUDE.md` | q94–q96 own `CLAUDE.md` · q97–q99 nothing | **pass, positive control fired** |
| (i) teeth, M1 | P 0/3 RED · N 0/2 RED, q98 not applicable | all GREEN; q95 q99 by hand | **not a reading** — P is not 20.3's P; N is a floor on a launcher never seen to produce a test |
| (v) teeth, M2 | same as (i) | same | as (i) |
| (ii) test artifacts | **P 0/3 · N 0/3** — every arm at the four seeded cases | — | as (i) |
| (iii) delivery | **5/6** by the pre-registered definition | q98: markup only, counts in `localStorage` | below 6/6; read with the prompt error above, not as a launcher fault |
| (iv) cost | P 151 k · 132 k · 124 k · N 42 k · 35 k · 46 k | — | declared under-powered in advance; recorded |

## What stands

**A clean arm is buildable, and this round certifies it rather than assuming it.** q97 q98 q99 are
the first controls this project has run that verifiably held no protocol text: no instruction
record, no parent path, no OVERRIDE header, an empty memory directory — read from their own
transcripts by a reader that, in the same pass, **did** see each P arm's own `CLAUDE.md`. VERIFY
re-ran the certificate and got the same bytes, and grepped the raw transcripts independently.
The amendment that made the positive control possible was committed at 22:12:48; the first arm
output appeared at 22:15:07.

## Observed, not pre-registered, N=3

**With the protocol installed and the prompt silent about it — the condition a real user creates —
3 of 3 arms ran the ceremony on the sentinel alone, and 0 of 3 wrote a test.** Each wrote `01`–`04`
(q95 and q96 without `03`), recorded its VERIFY as non-independent under §4's fallback, and planned
a live API check instead of a test. Two of three never opened `BEMYAGENT.md`. This is the one
condition the harness had never run, it arrived by accident, and it is a single cell on a single
launcher: **recorded, not read.** It does say something no prior round could: the sentinel by
itself is enough to bring the ceremony in, the plan still predicted the artifact, and **the
ceremony ran without producing a test** — what moved was what the plan chose to check.

## Corrections, all from VERIFY, all confirmed

1. **(iii) 6/6 → 5/6.** The 6/6 in `03f` redefined delivery after seeing q98. Withdrawn.
2. **The Agent tool's absence is not a difference.** The comparators had it and never used it;
   q85 q87 q89 each wrote *"no second agent available"*.
3. **"Plan predicts artifact" holds, but not in 20.8's wording.** VERIFY found q85's
   `01_think.md` Verification Plan names no test while q85 wrote one. Re-checked: q85's `02_tasks.md`
   Validation does — *"npm test passes incl. new score test"* — and the line 20.8 quoted for q85 is
   q87's. With the plan taken as `01` + `02`, both forward-written, **it predicts the artifact 9/9**
   across 20.3, 20.8 and this round; in 20.8's narrower wording, 5/6. Addendum in
   `work/20/20.8/04_verify.md`. (VERIFY was right about the wording and wrong about the mechanism;
   this file briefly withdrew the mechanism on its word before checking `02`.)
4. **Undeclared differences beyond the prompt**, from VERIFY: the protocol now arrives as the arm's
   own `CLAUDE.md` under the OVERRIDE header rather than by the parent's sentinel; the arms' cwd is
   their own tree; six ran concurrently where 20.8 ran one at a time; the tool mix moved from
   Bash-only to Read/Edit.

## What this does not say

1. **Nothing about 20.3 or 20.8 reverses.** Their P condition was not run. Pooling this round's 0/3
   into 20.8's 5/6 against 0/9 would mix launchers *and* prompts; it must not join that pool.
2. **Not that the prompt caused it.** It is the leading candidate and it is untested.
3. **Not what the injection did.** The Drift section forbade that claim and the design cannot carry it.

## Owed, not scheduled

**The round this was meant to be:** three P arms on this launcher with 20.3's `prompt_P.txt`. The
trees rebuild from `setup.py`'s P branch, the instruments are written and validated, and the N side
here already stands as its clean control. Three arms, about 400 k weighted tokens on this round's P
costs.

## Cost
Six Sonnet arms, 530 k weighted tokens (P 407 k, N 123 k) — **0.43×** the 1,234 k the Agent-tool
arms of 20.3 (P, 791 k) and 20.8 (N, 443 k) spent on the same seed. Not read: the P prompt differed. One verifier agent, 94 k tokens.
