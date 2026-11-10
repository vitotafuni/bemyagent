# 13.1b — THINK

> **Written after the classification was executed, not before.** The Handoff Principle requires
> `01` and `02` to be forward-written; for this task they were not. `classify.py` and its first
> output exist from before this file. Declared here and in `02_tasks.md` rather than backdated.

## Context

13.1 (2026-08) counted 32 procedural against 36 declarative units, *"42% of rule content"*, and its
own caveat said the 42% was inflated by reference data, config semantics and human-process text,
which are not inert rules and needed a third category before anything was pruned. Its artifacts
were never committed — two delegated audits whose numbers alone reached the record. The file has
also changed a great deal since: Decision 17, the Write Gate's coverage finding, 15.5, 15.8, 19.5.
So 13.1b starts over on the current text.

The object is `.bemyagent/docs/00-ai-rules.md`, the text every agent loads at every task. It is
embedded verbatim in `BEMYAGENT.md` (90 of 90 non-empty lines), so any cut is a protocol change and a
tag.

### Context Saturation Check
- [x] **Target files/paths** — the rules file; output in `work/13/13.1b/`.
- [x] **Expected behavior** — every line belongs to exactly one unit; every unit gets a class, a
      verifiability, a cost, a cost of failure, the evidence the record holds, and a verdict.
- [x] **Constraints** — the plan's own criterion: *verifiability × cost × cost-of-failure, not
      verifiability alone*, with "redact secrets" as the fixed point that must come out KEEP.
- [x] **Dependencies** — none; zero agents for the work, one for VERIFY.

## Approaches Considered

1. **Re-derive 13.1's counts and add the third category.** Rejected: its unit boundaries are lost
   with its artifacts, and the text under them has changed.
2. **Unit table over current line ranges, evidence by grep, verdict by the plan's criterion.**
   Chosen. Line ranges make coverage checkable mechanically: a line no unit claims is printed.
3. **Measure the declarative remainder with arms.** That is 13.2b, and it needs the fixture item
   2 of the roadmap names; out of scope for a desk task and for a phase that is closing.

## Selected Approach & Risks

The cut rule is the record's, not mine: **13.3 cut restatements and non-rules on inspection, and
13.2 pruned nothing on an inconclusive measurement.** Non-rule text can go without arms, because
removing it cannot change behaviour. A declarative rule cannot, because the evidence that would
justify cutting it is the same evidence that would have justified adding it.

### Pre-mortem
- **The classifier finds what it is looking for.** Mitigation: every proposed cut is put back
  through its own overlap check (Critical Review Protocol step 1) before it is reported.
- **Evidence by grep reads absence as inertness.** Mitigation: "none" in the evidence column means
  *none found*, stated as such in the script's docstring.
- **A cut orphans a setting.** Mitigation: every unit that is the semantics of a `settings.json`
  key is classed N and checked against the settings file.

### Devil's Advocate
Every unmeasured rule fails the Critical Review Protocol's own bar — *benefit must clearly exceed*
the tokens at every restore — so by the protocol's standard they should all go. Not adopted: that
bar is written for **proposals**, and applied retroactively it would delete the high-cost-of-failure
dispositions (Autonomous rigor, Precedence) the plan's criterion exists to protect. It does
correctly identify the four low-cost-of-failure declarative units, which is why they are named.

## Verification Plan
A second agent, holding only the rules file, the table and the criterion, checks coverage, the
class of every unit, every evidence claim it can grep, and argues against any verdict it disputes.

## 🎯 Drift
Proposing new rules. 13.1b classifies and judges deletions; it adds nothing.

## ✅ Validation
Coverage: zero unclaimed lines, printed by the script. Every verdict traceable to a column.

## 🔄 Pivot
If VERIFY disputes more than two class assignments, the categories are not well-defined enough to
cut by, and the verdict becomes "no cut possible on inspection" regardless of the table.
