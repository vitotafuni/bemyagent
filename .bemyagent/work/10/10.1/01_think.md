# 10.1 — Single Slim BEMYAGENT.md

## Context
Replace the 457-line `BEMYAGENT.md` with one maximally slim version (mission: save tokens). `BEMYAGENT.min.md` was a comparison experiment only — it proved compression works (~45% smaller) but is not shippable: orphaned settings keys (`strictVerification`, `autoModelSwitching` defined nowhere), lost Handoff Principle, lost CDM criteria definitions, lost specs/drafts lifecycle, inherited known bugs. One file must remain.

### Context Saturation Check
- [x] **Target files/paths** — `BEMYAGENT.md` (rewrite), `BEMYAGENT.min.md` (delete), plan + decisions updates
- [x] **Expected behavior** — same protocol semantics, fewest tokens; uncontroversial bug fixes from 2026-06-10 evaluation folded in (B-series); strategic items (C1 version field) excluded pending user decision
- [x] **Constraints** — zero semantic loss (every settings key must have a defining rule; every referenced file/path must exist in templates); human-facing scaffold templates stay readable per mission
- [x] **Dependencies** — none

## Approaches Considered
1. **Adopt min.md as-is, patch gaps** — Pro: done. Con: gaps are large; bugs inherited; easier to drift than to rebuild.
2. **Rewrite from full version with min's compression style + eval fixes** — Pro: zero-loss guarantee via checklist against full version; fixes land in one pass. Con: bigger diff to review.
3. **Keep both files, generate min via CI** — rejected by user: one file only.

*Pre-mortem*: likely failures = (a) a settings key or path silently dropped → mitigate with mechanical VERIFY (grep every key/path); (b) compression introduces ambiguity an agent misreads → mitigate by keeping exact output formats, thresholds, paths verbatim.
*Devil's Advocate*: ship full version, only delete min? Rejected — recurring bootstrap+restore token cost is the protocol's #1 measured complaint (see drafts/token-optimization-strategies.md).

## Selected Approach & Risks
Approach 2. Estimated token cost: medium. Risk: review burden of a full rewrite — mitigated by listing every incorporated eval item explicitly.

## Verification Plan (mechanical, not recollection)
- `wc -l` old vs new (target ≤ ~60% of original)
- grep: every `settings.json` key referenced in embedded rules
- grep: zero hits for `05-decisions.md` (broken ref), `TTE Workflow` (stale name)
- embedded rules block extracts cleanly (```` fences balanced)
- `06-implementation-plan` template contains a Task table
- `BEMYAGENT.min.md` removed
