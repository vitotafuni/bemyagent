Delivers: an evidence-backed answer to whether an agent actually writes a conversation log when
the protocol tells it to, and whether that log holds anything the TTEV files do not — which
decides issue #3 and the form it would take.

## Conditions (one line of `BEMYAGENT.md` differs)

- **a — baseline**: protocol as shipped, no log rule.
- **b — verbatim**: a Routing Table row plus a rule to append every user message *verbatim*, the
  reply, and a `→` line naming what the turn produced, to `.bemyagent/log/`.
- **c — summary**: identical, except each turn is recorded as a **short summary** of what was
  asked and what it produced, explicitly not a transcript.

9 arms, 3 × 3, model pinned, batched one per condition per batch.

## The two turns (identical across all arms)

- **Turn 1 — the task**: wire `session.js` into the server (`POST /api/sessions`, `GET /api/online`).
- **Turn 2 — the correction, and the thing issue #3 says is lost today**: *"Actually drop the
  count field from /api/online — just the array. And don't add a test for that, the existing ones
  are enough."* It changes the work, produces no task, and in the normal flow leaves no durable
  trace of having been asked.

## Checklist

- [ ] Verify the fixture installs and tests pass before launching any arm
- [ ] Diff a/b/c `BEMYAGENT.md` — the ONLY delta is the log rule
- [ ] Batch = one arm per condition; verify each batch finished before the next
- [ ] **Confirm every arm received and acted on turn 2** before scoring it — a missed second turn
      is an orchestration failure, not a finding
- [ ] Do NOT score before all 9 are in
- [ ] Copy the scorer and its raw output into this folder BEFORE writing the verdict
- [ ] Record verdict in `drafts/prompt-logs.md` + `05-decisions-and-issues.md`

## CDM

**🎯 Drift** — for THIS task, going off-track means:
- Scoring that a `log/` folder exists. It is forced by the rule; only its **contents per turn**
  count. This is the `Layers:` trap.
- Treating a verbatim log as accurate because it looks like a transcript. It is the agent's
  reconstruction; quoting it as fidelity is the error the round exists to expose.
- Reading a high write rate as value. Writing is not capturing — see the duplication measure.
- Rewording the rule after seeing results and reporting the reworded run.

**✅ Validation** — objective evidence of success:
- **WRITTEN**: a log file exists and contains an entry for **turn 1**, n/3 per condition
- **TURN 2**: it contains the correction too — the per-turn cadence actually held, n/3
- **NEW**: the correction is recorded **only** in the log, and not already in `05`/TTEV, n/3 —
  this is the proposal's whole claim
- **DUPLICATION** (harm): the log restates what TTEV already holds, n/3 — the failure the issue
  names itself
- All scored from files on disk, with path:line quoted into the scorer output
- Clean separation (0/3 vs 3/3) named as the only signal threshold at N=3

**🔄 Pivot** — pre-defined stop-and-rethink:
- **If WRITTEN ≈ 0/3 in both treatments**: the 0/10 prior holds and the proposal in this form is
  dead. Report it plainly and record the surviving alternative — declare where the harness
  transcript already lives — **without** proposing a third wording in the same breath.
- **If TURN 2 is 0/3 while turn 1 is 3/3**: the log is written once at the start and abandoned.
  That is compliance without the mechanism and it must not be reported as a positive.
- **If NEW is 0/3**: the TTEV files already capture the correction and the log buys nothing. The
  proposal fails on its own stated claim, whatever its write rate.
- **If ≥2 arms die on infrastructure**: void the batch, rebuild, restart. Never score partials.
- Obstacles exceeding `obstacleThreshold` = 2 → re-evaluate before continuing.
