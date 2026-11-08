# THINK — 19.5, the content-branch clause as a treatment

## Context

### Context Saturation Check
- [x] Target files/paths — `work/19/19.5/`, seed and clause both reused verbatim from
      `work/20/20.5/setup_W.py`, prompt verbatim from `work/20/20.5/prompt_W.txt`
- [x] Expected behaviour — six Sonnet arms, three control three treatment, the clause the only
      delta. **No standing approval in the prompt**, because the STOP is the mechanism under test
- [x] Constraints — one arm per condition per batch; model pinned; own root; arm filter
- [x] Dependencies — none new
0 unknown → proceed.

## Why now

19.2a rejected this clause for an absence of harm it never had an occasion to cause, and
Milestone 19 then closed on 6/6 Opus arms overriding Step 0's STOP. 20.5 reversed that: Sonnet
**stops 3/3**. 20.7 confirmed the clause costs nothing where content exists, 9/9 against 9/9.

So the clause now has a benefit case and a null harm, **and has still never run as a treatment**.
Everything measured so far is the control's behaviour. This round is the missing half.

## Approaches Considered

- **A. Both sides, six arms** (chosen).
- **B. Treatment only, three arms, read against 20.5's W control.** Cheapest, and rejected: 14.12
  and 14.13 had **byte-identical controls one week apart that read 1/3 and 3/3**. That is the
  precise hazard 14.14 was written for, and 20.5's W is a week old. A control that costs three
  arms is cheaper than a verdict that cannot be defended.
- **C. Fold this into 14.15's batches.** Rejected on bookkeeping risk, not on method: four
  conditions in one batch would blind better, and two separate rounds with clean folders are
  easier to get right. Errors have cost more than wall-clock this week.

## Selected Approach & Risks

### 🎯 Drift
Scoring delivery as the verdict. The verdict is **routing**: does the arm stop at a gate guarding
a directory that holds one settings file. Delivery is the consequence and is recorded as context.

### ✅ Validation
Control vs treatment diffs to the clause line and nothing else; control-vs-control and
treatment-vs-treatment identical; 6/6 arms leave a readable tree; ports swept both ends; scorer
output in this folder before the verdict; 19.4's check applied and the arms named.

### 🔄 Pivot
A batch that dies on a session limit voids the round. Rebuild, never resume.

### Pre-mortem
1. **The control may not stop this time.** 20.5's W stopped 3/3; a fresh control that proceeds
   3/3 makes this round a ceiling and the clause unmeasurable here. That is a real outcome and is
   written into the readings below, not treated as a failure.
2. **The treatment may stop for a different reason.** The clause removes the review only when
   `.bemyagent/` holds nothing but `settings.json`. An arm that stops anyway, citing something
   else, is a null for the clause and must be read from its own words, not assumed.
3. **Harm has to be measurable or the round only sells the clause.** The clause's promise is that
   the settings merge is additive and destroys nothing. Scored per key: eight keys × three arms,
   **24 observations a side**, which is where this round's power actually lives.
4. **Price.** Six Sonnet arms, ≈ 330 k subagent tokens at 20.7's rate.

### Devil's Advocate
*The clause buys a delivery by removing a safety gate, and this round is built to applaud that.*
The counter is pre-mortem 3: if the treatment proceeds and loses even one settings key, the
clause is rejected on harm and the delivery counts for nothing. The harm metric has seven times
the resolution of the benefit metric, deliberately.

## Verification Plan
Deterministic scorer, output copied here before the verdict, readings fixed in `02_tasks.md`.
