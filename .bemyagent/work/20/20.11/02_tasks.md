# 20.11 — TASK

**Delivers:** the first control arm this project has run that is **verifiably** holding no protocol
text, with a protocol side on the same launcher to prove the instrument is alive — so that
"no protocol file of any kind" can be written again without a footnote.

## Checklist

| # | Step | Status |
|---|---|---|
| 1 | `setup.py` for 20.11: 20.8's code path, `ARMS = q94 q95 q96 → P, q97 q98 q99 → N` | done |
| 2 | Build six trees in `scratchpad/r2011/`, `npm install` each | done |
| 3 | Byte-identity of each new tree against r203/q85 (P) and r208/q91 (N), before any launch | done — 102 blobs, 0 diff |
| 4 | Launch six headless arms, 20.8's `prompt.txt` verbatim, Sonnet, stdout captured per arm | done — all six exit 0 |
| 5 | Certificate: grep each arm's own transcript for the injection, per arm | done — 18/18 as amended |
| 6 | `mutate.py M1` and `M2` over the six new arms | done — mutate.py + mutate_by_hand.py |
| 7 | `score.py` over the six new arms | done |
| 8 | Independent VERIFY by an agent that did not do the work | verified — prompt error found |
| 9 | `04_verify.md`, `05-decisions-and-issues.md`, `06-implementation-plan.md`, commit | done |

## The readings, fixed before any arm is launched

| | metric | read from | predicted | what would reverse it |
|---|---|---|---|---|
| **(i)** | teeth, M1 — a drawn game counts as a win for X | arm's own `npm test` after the mutation | **P 3/3 RED · N 0/3 GREEN** | P below 2/3 → the launcher is unfit and the round reports that instead |
| **(ii)** | test artifacts added over the seeded four | the tree | **P 3/3 · N 0/3** | an N arm leaving a test file |
| **(iii)** | delivery: tally, route, markup | the tree | **6/6** | anything below 6/6 condemns the launcher before (i) is believed |
| **(iv)** | cost | the launcher's own `modelUsage` | recorded, **declared under-powered in advance** — 20.8's ranges already overlapped at N=3 | nothing at this N; it is recorded, not read |
| **(v)** | teeth, M2 — X's and O's totals swapped | as (i) | **P 3/3 · N 0/3** | a disagreement with (i) on either side, as q57's did in 20.8 |
| **(vi)** | **the certificate**: `"type":"instructions"` records, parent-repo absolute paths, OVERRIDE header | each arm's own transcript JSONL | **0 · 0 · 0, on all six arms** | any non-zero count on any arm means that arm is not clean and is reported as contaminated whatever it did |

**(i), (ii), (iii) and (v) are 20.8's and 20.3's published readings for these same two conditions.**
Predicting them is not a free pass: the round is written to notice a floor, and the pivot in
`01_think.md` fires on the P side, which is the side a broken launcher takes down.

**(vi) is the round's own point** and has 18 observations — three counts on each of six arms — which
is the per-occasion shape 20.6's question 4 asks for, at no extra cost.

## Amendment, 2026-11-10 — (vi) was wrong for the P side, fixed before any arm exists

As first written, (vi) predicted **0 instruction records on all six arms.** That is false by
construction for q94–q96: each holds its own `CLAUDE.md`, the harness will inject it as project
instructions under the OVERRIDE header, and that injection **is the treatment arriving.** Scored as
written, the certificate would have called the protocol side contaminated and, by this file's own
rule, voided it. Found while writing `certificate.py`, with no arm launched and no transcript in
existence. (vi) is replaced by:

| | metric | predicted | what would reverse it |
|---|---|---|---|
| **(vi-a)** | instruction records whose file lies **outside the arm's own directory** | **0 on all six** | any such record: that arm is contaminated whatever it did |
| **(vi-b)** | tool calls naming the parent repository's absolute path | **0 on all six** | any such call |
| **(vi-c)** | instruction records of any kind | **N 0 · 0 · 0 · P exactly one each, the arm's own `CLAUDE.md`** | a P arm with none means the certificate cannot see an injection, and its zeros on N mean nothing |

**(vi-c) is a positive control for the certificate itself.** The probe's 0 was absence of evidence,
which §4 forbids from supporting a claim on its own; a P arm whose own rules file shows up in the
same count, by the same reader, is what makes the N side's zero a reading.

## Honesty declaration (14.15's precedent)

Nothing in the table above has been observed. No arm exists yet. One adjacent fact **is** already
seen and is therefore not evidence for this round: the `probe211` run of 2026-11-09, a Haiku
one-shot in an arm-shaped tree, returned **0 instruction records**. That is what justified building
the round; it is not an arm, it did no work, and it is cited in `01_think.md` as context rather
than entered in the table.

## 🎯 Drift
Any claim about what the injection *caused*. The design cannot support one.

## ✅ Validation
Every cell filled from a command run during VERIFY, arms named at each end.

## 🔄 Pivot
P side below 2/3 on (i) → stop, declare the launcher unfit, report that. `interactiveMode=false`:
pivot and report, do not ask.
