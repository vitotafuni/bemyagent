Delivers: an evidence-backed answer to whether EARS-formatted `✅ Validation` criteria change what
VERIFY actually does — plus the first measurement of whether cited evidence covers the change.

## Conditions

- **a — baseline**: `✅ Validation` as shipped (*"the objective evidence of success"*, free prose).
- **b — treatment**: the same bullet additionally requires each criterion to be written as
  `WHEN <condition> THE SYSTEM SHALL <observable>`.

6 arms, 2 × 3, model pinned, batched one per condition.

## Checklist

- [ ] Verify the fixture installs and tests pass before launching any arm
- [ ] Diff a vs b `BEMYAGENT.md` — the ONLY delta is the Validation clause
- [ ] Batch 1 = a-1,b-1 · batch 2 = a-2,b-2 · batch 3 = a-3,b-3
- [ ] Verify each batch finished before launching the next
- [ ] Do NOT score before all 6 are in
- [ ] **Copy the scorer and its raw output into this folder BEFORE writing the verdict**
      (`harness/README.md`, the rule 15.3 taught us)
- [ ] Record verdict in `05-decisions-and-issues.md`

## CDM

**🎯 Drift** — for THIS task, going off-track means:
- Counting EARS-shaped criteria as success. The form is template-forced once the clause exists;
  only what VERIFY then *does* counts. This is the `Layers:` trap.
- Reading a coverage result as a verdict on EARS. They are separate questions sharing one run.
- Bending the task until coverage separates. A ceiling effect is a reportable outcome.
- Treating this as a Kiro comparison. It is not: it is Kiro's schema isolated inside our harness.

**✅ Validation** — objective evidence of success:
- **FORM**: `02_tasks.md` Validation criteria written as `WHEN … SHALL …`, n/3 per condition
- **CITATION**: `04_verify.md` cites a command actually run, n/3 — our current §4 bar
- **COVERAGE**: that command demonstrably touches the change — it names the modified file, or is
  a test run whose suite includes a test added in this task, n/3 — the new bar
- All three scored by reading files on disk, with path:line quoted into the scorer output
- Clean separation (0/3 vs 3/3) named as the only signal threshold at N=3

**🔄 Pivot** — pre-defined stop-and-rethink:
- **If FORM separates but COVERAGE does not**: the criterion is prettier and VERIFY is unchanged.
  Report as a null with a named mechanism — compliance without the deliverable — and do not land
  EARS on the form result alone.
- **If COVERAGE is 3/3 in both**: ceiling effect from a task that naturally produces its own test.
  The coverage question is **unanswered, not answered** — record it as inconclusive, which is not
  a null, and do not prune §4 on it.
- **If ≥2 arms die on infrastructure**: void the batch, rebuild, restart. Never score partials.
- Obstacles exceeding `obstacleThreshold` = 2 → re-evaluate before continuing.
