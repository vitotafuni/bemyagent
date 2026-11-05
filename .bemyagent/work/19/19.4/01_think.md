# THINK — 19.4, the scorer is an instrument and nothing checks it

## Context

### Context Saturation Check
- [x] Target files/paths — `harness/README.md`. No `BEMYAGENT.md` delta, so no tag.
- [x] Expected behavior — a round cannot reach a verdict without a recorded check of its own scorer.
- [x] Constraints — the rule has to be procedural with a forced artifact, or this repo's own
      record predicts it measures zero.
- [x] Dependencies — none.

0 unknown. Proceed.

## The evidence, and it is all from the last three rounds

Four scorer defects, each caught by reading an arm rather than by reading a number, and **each
one would have produced a false headline**:

| Round | The defect | Direction |
|---|---|---|
| 14.13 | A forged line defined as one the *seeded* command cannot emit. One control arm improved the command its map names, so its own new test file read as **nine forged lines** — the same count as the genuine forgery a round earlier | against the arms |
| 19.3 | Governed writes counted as any Bash command with a `.bemyagent/` path near a redirect, which swept up the `diff`s that *read* the rules file. Produced **"first governed write preceded by a check: NO, 6 of 6"** | against the arms |
| 19.2a | The user's migrated conventions matched as whole sentences. The treatment migrated them in its own words and scored as having preserved them **only in a backup** | against the arms |
| 19.2b | Routing read from `upgrade-plan.md` and the audit log, which an arm that takes UPGRADE and skips the STOP writes neither of. That arm scored as **never having taken the branch** | toward the hypothesis |

Three ran against the arms and one toward the candidate, so the fix cannot be *"watch for bias
in favour of your hypothesis"*. The failure is not a direction. **A scorer is an instrument
built by the person who wants an answer, and nothing in this harness checks it.**

`harness/README.md` already says a proxy metric must be checked for bias against the treatment
before its null is believed. That sentence is **declarative**, it names only one direction, and
the four defects above all happened after it was written.

## Approaches Considered

**A. Strengthen the existing sentence.** Rejected. 14.9 measured exactly what strengthening a
declarative line in place buys: the obligated half moves and the unobligated half fails next
door. 14.13 then measured the whole family at a ceiling for a different reason. A stronger
adjective is not a mechanism.

**B. A forced artifact in `04_verify.md`, one line per metric.** Selected. The repo's strongest
regularity is that a procedural rule attached to an artifact the agent is already writing lands
near-total, and `04_verify.md` is already mandatory. The line states which arms were read and
whether their scores matched what they did.

**C. A second agent re-scores independently.** Rejected as the default — it doubles the cost of
every round — but named in the text as the remedy where a verdict rests on one metric. §4
already prefers an independent VERIFY, so this is that rule applied to the scorer rather than a
new idea.

## Selected Approach & Risks

One rule in the instrument list, procedural, with the four cases as its evidence. The obligation:
**before a metric's number is written into a verdict, open the arm at each end of that metric —
the best and the worst — and confirm the score matches what the arm actually did.** Record it in
`04_verify.md` as one line per metric.

### Pre-mortem

1. **It becomes a ritual line nobody acts on**, which is the `Layers:` header failure from rule
   3 — 100% compliance, zero effect. Mitigated by requiring the line to **name the arms read**,
   which cannot be written without opening them, rather than asserting that a check happened.
2. **It costs a round that has nothing to check.** Two arms per metric is cheap next to six arms
   and a day; the four defects above each cost more than every check this rule will ever ask for.

## Verification Plan

`diff` the file and confirm the delta is one place. Confirm `BEMYAGENT.md` untouched. Re-read the
inserted rule against pre-mortem 1: does it demand a fact that requires opening an arm, or only
an assertion.
