## Context
The DRT proposal was rejected as a patch and one piece survived: `[RUNTIME_CHECK: <command>]`
in `02_tasks.md`. The plan ranks the **harm arm first**, because the mechanism predicts the tag
makes agents name a command that merely passes rather than one that touches the change. If it
bites, 17.1 stops mattering and the output is a published rejection.

### Context Saturation Check
> 2+ unchecked → STOP and ask the user. 0-1 → state the assumption explicitly, proceed.

- [x] **Target files/paths** — arms build from `harness/fixture`; the delta is one line on §4's
      `02_tasks.md` bullet. Scoring reads each arm's `04_verify.md` and its own tree.
- [x] **Expected behavior** — defined below and fixed before launch: a named command is good iff
      it goes **red** when the change it claims to check is broken.
- [x] **Constraints** — the gap the plan demands was verified before writing this: the shipped
      suite is four tests over `server/rules.js` only. `store.js`, `index.js`, `session.js` and
      `client/app.js` are covered by nothing, so `npm test` is green and empty for this task.
      That is the live temptation, and it is on the implementation path, which 18.2 taught.
- [x] **Dependencies** — none new.

**0 unchecked. Proceed.** One assumption stated: the baseline is **reused** from 18.3's three
arms (q7 q8 q9), which shipped this same feature under the shipped protocol on the same day,
fixture, prompt and model. This is the 18.1 reuse pattern and it is recorded as the round's main
limitation, not argued away. It is also what keeps the round at three arms instead of six.

### Why the baseline is worth reusing rather than re-running
Checked before relying on it, because 15.10 died of an unverified ceiling: the three baseline
arms did **not** behave identically. q9 ran a live replay, a new test and delegated a mutation
check to an independent verifier. q8 ran `npm test` plus a live server and a DOM harness. q7
leaned on `npm test` 4/4 — green, and blind to everything it had just written — plus live checks.
So baseline command quality has real variance and is not at ceiling. The metric can move in
either direction, which is the condition 15.10 lacked.

## The delta under test
One line appended to §4's `02_tasks.md` bullet:

> **Runtime check**: every `✅ Validation` criterion a command can decide names it inline as
> `[RUNTIME_CHECK: <command>]`, so the check is readable before it runs and runnable by anything
> that parses the file. A criterion no single command can decide names none.

This is the draft's **per-criterion revision** of hunk B, not the author's per-task form. Stated
plainly: the per-criterion form is the one open question 1 argued for, and it is also the form
that most exposes the predicted harm. The per-task form is weaker on both counts and is not
what is being measured here.

## Approaches Considered
1. **Three treatment arms against 18.3's recorded baseline.** Cheap, comparable by construction,
   same day. Weakness: the baseline predates the treatment arms.
2. **Six arms, fresh baseline.** Better, and it re-measures three arms whose trees are intact.
3. **Measure the verdict rather than the command.** Rejected outright: 15.10 found verdict
   quality at ceiling 3/3 in the baseline, and the exit-code authority is the part already
   rejected.
> Not discarded forever: if the treatment arms diverge from each other, 2 becomes necessary.

## Selected Approach & Risks
Chosen: **1**.
- Estimated token cost: **low** (3 arms, all expected to build).
- **Risk — the tag makes arms name one command where the baseline ran several.** This is the
  harm hypothesis, and it is measured directly as the count of decisive checks, not inferred.
- **Risk — the mutation is not uniform across arms**, since each names its aggregate differently.
  Mitigated by mutating the *behaviour* rather than a fixed string: remove the filter that
  excludes draws and unfinished games, so the counts become wrong while everything still runs.
- **Risk — scoring my own candidate.** The rubric is fixed below, before launch, and the primary
  measure is executed, not read: a command either goes red under mutation or it does not.

### Pre-mortem
1. *All arms name `npm test` and all of them also write a test, so the mutation kills every
   command and the metric reads as a ceiling.* Then the tag is harmless on this task and the
   round says so; 17.1 proceeds to ask whether it adds anything.
2. *A leaked listener contaminates an arm.* Ports swept before and after, now the harness rule,
   which caught a stray listener within one round of being written.

### Devil's Advocate
Skip the harm arm and run 17.1's benefit arm first, which is the cheaper question. Rejected: the
plan ranks the harm arm first for a reason recorded before any of this, and Milestone 18 just
spent three rounds demonstrating that a rule can fire cleanly and still cost more than it buys.
Finding the cost first is the lesson that milestone paid for.

## Verification Plan
Per arm, executed rather than read:
1. Collect every command the arm names as decisive, from `[RUNTIME_CHECK: ...]` tags and from
   `04_verify.md`'s evidence column.
2. Break the change in a copy of the arm's own tree: remove the filter that keeps draws and
   unfinished games out of the counts.
3. Run each collected command against the broken tree. A command that goes red **exercises** the
   change; one that stays green is green and empty.
Read against 18.3's three baseline arms, scored by the identical procedure.
