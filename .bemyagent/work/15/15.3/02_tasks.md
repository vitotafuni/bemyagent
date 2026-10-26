Delivers: an evidence-backed answer to whether a mandated `## Project rules` section causes a
standing user rule to be written somewhere durable, or whether the rule evaporates — which
decides FEDERATION issue #7(a) and tests the objection raised against it.

## The two planted instructions (verbatim, identical in both conditions)

- **STANDING** (must be captured): *"One more thing for this repo in general: from now on, every
  new function in `server/` gets a one-line comment above it saying what it returns. Applies to
  anything we add later too, not just this task."*
- **TASK-SPECIFIC** (must NOT be captured as a project rule): *"For this change only, skip
  updating the client — I'll do that part myself."*

## Conditions

- **a — baseline**: protocol as shipped. No `## Project rules` section anywhere.
- **b — treatment**: `AGENTS.md` carries a `## Project rules` section with a guide line, and the
  §1 block instructs the agent to check and maintain it.

6 arms, 2 conditions × 3. Model pinned explicitly on every arm.

## Checklist

- [ ] Rebuild scaffolding (prior round directories were removed from the scratchpad)
- [ ] Verify the fixture installs and tests pass BEFORE launching any arm
- [ ] Confirm all 6 arms clean and identical except line-for-line the condition difference
- [ ] Diff a-arm vs b-arm `AGENTS.md` and confirm the ONLY delta is the Project rules block
- [ ] Batch 1 = a-1, b-1 · batch 2 = a-2, b-2 · batch 3 = a-3, b-3 — one per condition each
- [ ] Verify each batch completed (finished, not stopped) before launching the next
- [ ] Do NOT score before all 6 are in
- [ ] Score by reading files on disk, never from the arm's own report
- [ ] Record verdict in `drafts/federation-issue.md` + `05-decisions-and-issues.md`

## CDM

**🎯 Drift** — for THIS task, going off-track means:
- Scoring whether the **section exists**. It is template-forced; that is the `Layers:` trap.
  Only its *contents* count.
- Accepting an arm's claim that it captured the rule. Read the file.
- Treating a baseline arm that captures the rule elsewhere in `.bemyagent/` as a failure of the
  baseline. That is the finding that #7(a) is already covered, and it must be reported as such.
- Rewording the section after seeing results and reporting the reworded run.

**✅ Validation** — objective evidence of success:
- Per-arm: the literal text of every file under `.bemyagent/` and `AGENTS.md` that mentions the
  standing instruction, with path and line
- CAPTURED scored n/3 per condition; SPURIOUS (task-specific instruction recorded as a standing
  rule) scored n/3 per condition as the harm measure
- Where it landed, recorded per arm — the baseline may capture it somewhere we did not predict
- Clean separation (0/3 vs 3/3) named as the only signal threshold at N=3

**🔄 Pivot** — pre-defined stop-and-rethink:
- **If a ≈ b on CAPTURED**: the section adds nothing and #7(a) does not land. Report the null
  plainly; do not propose a third wording in the same breath.
- **If b captures but the text is boilerplate** (the guide line restated, or the rule copied
  without the repo-specific content): that is the P3 glossary result again — compliance without
  the deliverable. Report as such, do not count as CAPTURED.
- **If SPURIOUS fires in b**: the section manufactures project rules out of task instructions.
  That is a harm and it outweighs a positive CAPTURED result.
- **If ≥2 arms die on infrastructure**: void the batch, rebuild, restart. Never score partials —
  the 14.3a partial state was biased toward a false positive.
- Obstacles exceeding `obstacleThreshold` = 2 → re-evaluate before continuing.
