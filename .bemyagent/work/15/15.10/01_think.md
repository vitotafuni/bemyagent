# THINK — 15.10 EARS-formatted Validation criteria, and the coverage question

## Two questions, one round

**Primary (the EARS hypothesis).** Kiro constrains acceptance criteria to
`WHEN <condition> THE SYSTEM SHALL <observable>`. This project previously dismissed RFC-2119-style
proposals because Decision 16 measured *wording strength* as not moving compliance. **That
argument does not apply here**: EARS is a schema constraint on artifact content, not a stronger
adjective — you cannot state *"the code is clean"* in that form at all. It makes an unverifiable
criterion syntactically impossible, which puts it on the forced-artifact side of our own measured
line.

**Secondary, and free (the coverage question).** The Kiro survey's sharpest finding: **§4's
evidence rule is a citation rule, not a coverage rule.** It demands evidence from a command run
during VERIFY, but never that the command *touch the change*. `npm test` over a suite that does
not exercise the modified path yields a PASS with a valid citation and zero information. Scoring
this round for coverage as well as citation costs nothing extra and produces the first data on
it.

## Context Saturation Check

| Item | Known? |
|---|---|
| What EARS is, and Kiro's exact short form | yes — `WHEN <condition> THE SYSTEM SHALL <observable>`, verified on kiro.dev |
| Where the condition difference goes | yes — the `✅ Validation` bullet of the CDM in §4 |
| Whether the harness can run it | yes — same fixture, same shape as 15.3 |
| Whether arms will have an occasion to fire | yes — any Standard/Heavy task writes `02_tasks.md` with Validation criteria |
| What "the command touched the change" means mechanically | **assumption stated**: the cited command either names the changed file/test, or is a test run whose suite includes a test added or modified in this task |

0–1 unknown → state the assumption and continue.

## Approaches considered

1. **Compare against Kiro directly.** Rejected, and the reason is recorded for the plan: a
   BMA-vs-Kiro run varies protocol, harness, model, system prompt and IDE context simultaneously.
   There is no isolated mechanism, so any result would be uninterpretable — the same class as the
   consent rules already parked as unmeasurable. What *is* testable is Kiro's schema extracted and
   run as a condition inside our own harness, which is this round.
2. **Score only the EARS hypothesis.** Rejected as waste: the arms produce `04_verify.md` either
   way, and coverage is readable from the same artifact.
3. **Chosen: 2 conditions × 3, scored for EARS-form uptake, citation, and coverage.**

## Pre-mortem

1. **The agent writes a beautiful `WHEN…SHALL` criterion and then verifies it by recollection
   anyway.** This is the obvious failure and it is the `Layers:` shape — the form is produced, the
   behaviour is not. *Mitigation*: the form is scored separately from the behaviour, and a round
   where b adopts EARS 3/3 while coverage stays flat is a **null with a named mechanism**, not a
   positive.
2. **Both conditions already cover their change**, because the fixture task naturally produces a
   new test. Then coverage separates nothing and the secondary question is unanswered rather than
   answered negatively. *Mitigation*: accept it. A ceiling effect is reportable, and the task is
   not being bent to manufacture a gap.
3. **The scratchpad is cleared before the round is written up** — this just happened to 15.3 and
   cost that round its evidence. *Mitigation*: the new `harness/README.md` rule applies — the
   scorer and its raw output are copied into this folder **before** the verdict is written.

## Devil's advocate

The stronger round is 15.11, the approval gate: it costs the user wall-clock on *every task*,
nobody has measured it, and we hold both the flag and the harness. Not pivoting, because 15.11
needs two-phase arms (stop after THINK, resume on a constant approval token) and therefore new
orchestration, whereas this round runs on the 15.3 shape unchanged. Build the cheap one first and
keep 15.11 queued — but it remains the more valuable question and should not be quietly dropped.

## Assumption carried forward

One model, one harness — the same external-validity limit the 2026-10-20 survey named. Replication
on a second model family is queued as its own task rather than confounded into this one.
