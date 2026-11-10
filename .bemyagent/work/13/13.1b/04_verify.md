# 13.1b — VERIFY

Run by a second agent that did not do the work, holding the rules file, the table, `classify.py` and
the criterion, and asked to argue against the conclusion (§4). Every correction it made was
spot-checked against the record before being accepted; all held. Full table: `03b_classification.md`.

## Verdict: **AGREE WITH CORRECTIONS — and the Pivot fired**

**Nothing is cut on inspection.** The conclusion survived; the reasoning under it did not, quite.

`01_think.md` fixed the Pivot before VERIFY ran: *more than two disputed classes → the categories
are not well-defined enough to cut by, and the verdict becomes "no cut possible on inspection"
regardless of the table.* **VERIFY disputed 8 of 42 units (602 tok).** The Pivot is honoured as
written. That is the round's real finding:

| reading | P | D | N |
|---|---|---|---|
| this audit | 21 units · 2138 tok · **62%** | 13 · 736 · **21%** | 8 · 565 · **16%** |
| independent VERIFY | 28 · 2658 · **77%** | 8 · 439 · **13%** | 6 · 342 · **10%** |
| 13.1 (2026-08) | 32 units | 36 units, *"42% of rule content"* | — |

**The three-way split is reader-dependent by about fifteen points**, and 13.1's 42% lies outside
both readings — its own caveat said it was inflated, and two independent readers now agree it was.
What survives every reading: **the declarative share is between an eighth and a fifth of the
file, and no reading puts it near the 42% that started Milestone 13.**

## The eight disputed classes

| unit | ours → VERIFY's | VERIFY's reason, which holds |
|---|---|---|
| 13 HTN structure | N → P | max depth and leaf/branch are inspectable in the `work/` tree |
| 24 Pacing | N → P | *"MUST STOP for human approval"* is a forced action |
| 11 Conversation log | N → P | holds three rules — never by you, never read on restore, cite as `<file> HH:MM` |
| 10 Context Slicing | D → N | our own pre-mortem said settings semantics are N, and our evidence column called it that |
| 9 Conceptual maps · 19 Handoff · 27 Read-before-modify · 32 Surgical scope | D → P | each is marked verifiable=high, and D means *no artifact*; each has one |

The last row is the class definition failing, not the reader: a rule whose compliance shows in an
artifact the agent produces anyway (a diff, a file's contents) is procedural by one reading of
*"tied to an inspectable artifact"* and declarative by another.

## Evidence corrections, all verified against the record

- **Unit 1** — CLAUDE.md precedence landed in **15.1** (#3), not 19.x.
- **Unit 12** — 100% / 55% are **19.3's** measurement, not Decision 13's; 19.3 calls Decision 13's
  estimate unmeasurable.
- **Unit 21** — *"verifiers found real defects 5/6"* was overstated: `05` L319 says 5 of 6 arms
  **ran** an independent VERIFY, *"Not scored and not a result"*.
- **Unit 28** — 20.9's 3/3 split does not isolate the rule: it separated where the documents came
  from. Replaced with *none that isolates it*.
- **Unit 35** — cost column 32, evidence said 25.

## Verdicts re-argued

- **Conversation log.** Our rejection appealed to an earlier decision, which is not an overlap or
  cost check. VERIFY supplied the reason that does hold: `BEMYAGENT.md` ships to projects without
  this repo's `05`, so inline is **the only way the reason travels.** Restated in the table.
- **Context Slicing.** *"A cut is a migration"* was overstated — Decision 12's convergence upgrade
  removes keys anyway. What holds: cutting the line leaves the live key `contextSlicingThreshold`
  (`settings.json`, `BEMYAGENT.md` L151 and L288, glossary L29) with no meaning. Also: 14.3 gave the
  rule an occasion (`session.js` 309 lines against 200) that nobody scored.
- **Multi-Agent Parallelism, missed.** The cut rule covered only N and D, so no procedural unit was
  ever tested for a trim. Evaluated now: **KEEP-untested.** The human-choice part (dispatch) is
  what 13.3 already relocated; steps 2–3 are agent rules that keep parallel agents from colliding on
  shared docs. Never exercised in twenty milestones.
- **One more, against this audit, that VERIFY did not raise:** *"25 tokens is below the cost of a
  release"* was the stated reason to keep Glossary use. **It does not hold while 3.4.0 is due
  anyway** — a cut would ride that release for free. Withdrawn. What keeps the unit is the Pivot.

## What this does not say

1. **The five KEEP-untested units are not shown to work.** Context Slicing, Decomposition, Brevity,
   Glossary use, Multi-Agent Parallelism — 353 tokens, 10% of the file, never measured in either
   direction. 13.2b would have measured them and is dropped for want of a fixture.
2. **`01_think.md` and `02_tasks.md` were written after the classification**, against the Handoff
   Principle. The Pivot condition was written before VERIFY ran, so it binds VERIFY; nothing else in
   this task is a prediction.

## Cost
One verifier agent, 80 k tokens, 19 tool calls. The audit itself: zero agents.
