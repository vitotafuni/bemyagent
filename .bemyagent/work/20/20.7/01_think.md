# THINK — 20.7, the last two fragile verdicts

## Context

### Context Saturation Check
- [x] Target files/paths — `work/20/20.7/`, two seeds reused verbatim (`work/18/18.3/setup.py`,
      `work/19/19.2a/setup.py`), `05-decisions-and-issues.md`, `06-implementation-plan.md`
- [x] Expected behaviour — nine Sonnet arms, **no protocol delta on condition P**, the 19.2a
      clause on condition H only. The variable is the tier, exactly as in 20.5
- [x] Constraints — one arm per condition per batch; model pinned explicitly on every arm;
      each condition builds into its **own root** so no rebuild can delete a finished arm
- [x] Dependencies — none new
0 unknown → proceed.

## Why this round and not another

The user asked whether the 27 queued commits are justified. 20.4 classified them: 6 stand
unconditionally, 4 are harm rejections that hold or strengthen on a weaker tier, and **4 are
redundancy rejections shaped *the baseline already does this*** — 18.3, 14.13, 15.11, 19.2a.

20.5 tested two of the four and **both reversed**. 14.13 is settled. Claim 1 (18.3) came back
**unmeasured** because merging it onto a condition whose arms stop at Step 0 destroyed its own
occasion. This round measures the two that are left and does not pretend to measure a third.

**15.11 is deferred on purpose, with the reason recorded.** Its verdict is a null that already
redirected to a better lever — §4's Saturation Check 0-1 branch, *state the assumption and
continue* — and that branch is precisely what condition P reads on this tier. If P's baseline
assumes and continues, 15.11's mechanism is observed on Sonnet at no extra cost. If P's baseline
does **not**, 15.11 is owed its own round and this one says so.

## Approaches Considered

- **A. Three conditions, nine arms** (chosen). P = 18.3's baseline; C and H = 19.2a's two sides.
- **B. P only, three arms.** Cheapest. Rejected: it leaves the one fragile verdict whose failure
  mode is **data loss** untested, which 20.4 ranked above curiosity.
- **C. H only, no control.** Rejected: a destroyed file with no control cannot be attributed to
  the clause rather than to the tier. A harm round is a comparison or it is an anecdote.
- **D. Re-run all four including 15.11 and 14.13.** Rejected on price; 14.13 is already answered
  and 15.11's mechanism is observable inside P.

## Selected Approach & Risks

### 🎯 Drift
Scoring condition P on whether the arm *shipped*, instead of on whether it **named the open
product decision**. Delivery is context here, never the verdict. The second drift is reading
condition H's `upgrade-plan.md` as evidence of preservation: the plan is prose, the metric is
bytes on disk compared against each arm's own setup commit.

### ✅ Validation
- Condition P arms diff clean against 18.3's own built arm except nothing — same `setup.py`.
- Condition C arms diff clean against condition H arms except the Step 0 clause line.
- 9/9 arms produce a readable `01_think.md`, or the round reports what is missing.
- Ports swept before and after; arm names continue the series and name no condition.
- Scorer output copied into this folder **before** the verdict, and 19.4's check applied:
  open the arm at each end of every metric and name it in `04_verify.md`.

### 🔄 Pivot
If a batch dies on a session limit, the round is **void and rebuilt, not resumed** — 14.3a and
18.2a's precedent, and 15.4's correction. The setup scripts take an arm filter so a rebuild
cannot destroy a finished arm.

### Pre-mortem
1. **The prompt for 18.3 was never stored.** 14.9a's rule post-dates Milestone 18, and
   `03_execute.log` only says *"prompt verbatim from 18.2"*. The task line is recoverable; the
   wrapper is not. Condition P therefore runs a **reconstructed** prompt, and it must carry the
   standing-approval line 18.3's prompt did not need — a bare `.bemyagent/` on Sonnet stops at
   Step 0 3/3 (20.5, condition W), which is the exact occasion-destroying failure this round
   exists to repair. **This is a stated limitation of the comparison, not a detail.**
2. **The occasion could be absent on P.** If the scoreboard task's scope decision is not open in
   this seed, a baseline that does not surface it measures the fixture. Guarded: `05` carries
   *"Draws are not displayed — open"* and `db/schema.sql` types `winner` as free TEXT, so
   *do draws count* and *all-time or per-session* are both genuinely open.
3. **H's harm could be unreachable.** Guarded: `00-ai-rules.md` carries a team-authored §7 that
   UPGRADE must regenerate over, so the collision is on the path, not beside it.
4. **Price.** Nine Sonnet arms. 20.5's six ran 41–58 k raw each; most spawn a VERIFY agent. Call
   it ≈ 18 agents. Against the alternative — pushing 27 commits whose justification is
   provisional — the round is cheaper than the retraction.

### Devil's Advocate
*The free probe already answered P.* The three Sonnet arms of 20.5's condition G named the scope
decision 3/3 in their Saturation Check (*"draws not counted"*, *"all persisted games"*), which
predicts 18.3 holds. **Rejected as a verdict, kept as a prediction.** It is a cross-round read on
a different seed, and 14.14 exists because two byte-identical controls read 1/3 and 3/3 across
rounds. The prediction is written down here so the round can embarrass it.

## Verification Plan
Deterministic scorers, one per condition, output copied here before the verdict. Readings fixed
in `02_tasks.md` before launch.
