Delivers: a scored, evidence-backed verdict on whether a code read may be delegated to a
cheaper model tier — and if so, only in the bounded pointer-only form — with the numbers a
future reader can re-check.

## Checklist

- [ ] Re-verify the defect is present in all 9 arm copies immediately before launch
- [ ] Launch 9 arms, `model` pinned explicitly and identically, identical task prompt
- [ ] Confirm each arm bootstrapped `.bemyagent/` (an arm that never ran the protocol is not data)
- [ ] Score NOTICED / DEDUPED / CITED via `score.py`
- [ ] Read every arm where NOTICED and DEDUPED disagree; trust DEDUPED
- [ ] Cost via `tokens.py`, normalised per unit of work, arm a as the baseline
- [ ] Record the verdict in `drafts/read-delegation.md` and `05-decisions-and-issues.md`
- [ ] Land the line-98 clause ONLY on clean separation; otherwise record the null and drop it

## CDM

**🎯 Drift** — for THIS task, going off-track means:
- Tuning the prompt, the defect or the scorer *after* seeing arm results, then reporting the
  retuned run as the finding. If the instrument changes, the round restarts and says so.
- Sliding from "measure the rule" into "make the leaderboard feature good". The arms' feature
  quality is not the deliverable; the defect's survival is.
- Reporting the cost number as the verdict when correctness did not separate.

**✅ Validation** — objective evidence of success:
- `score.py` output for all 9 arms, each having bootstrapped `.bemyagent/`
- Defect re-verified present in all 9 pre-launch (command + output in `03_execute.log`)
- Per-arm counts stated as n/3, with clean separation (0/3 vs 3/3) named explicitly as the
  only signal threshold — narrower results written up as nulls, not as trends
- Cost normalised per unit of work, with the divisor stated
- Verdict traceable: which arm, which artifact line, why it counted

**🔄 Pivot** — pre-defined stop-and-rethink:
- **If arm b ≡ arm a on DEDUPED** (delegation available but not taken): the rule cannot be
  measured by propensity here. STOP, re-read "Approaches Considered", and consider whether a
  forced-delegation arm is even a fair test of a permissive clause — a rule nobody exercises
  is inert regardless of the harness.
- **If ≥2 arms fail to bootstrap or die on the fixture**: instrument failure, not data. STOP,
  fix, restart the round.
- Obstacles (failed commands, contradicted assumptions) exceeding `obstacleThreshold` = 2 →
  re-evaluate before continuing.
- `interactiveMode=false` → pivot and report in the next update, do not ask first.
