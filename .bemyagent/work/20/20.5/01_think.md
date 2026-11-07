# THINK — 20.5, is the record's fragile core an artifact of the tier

## Context

### Context Saturation Check
- [x] Target files/paths — none. **No protocol delta.** The variable is the model tier of the
      baseline.
- [x] Expected behavior — unknown, and the uncomfortable answer is the useful one.
- [x] Constraints — arms on **Sonnet**, explicitly pinned (14.4); one arm per condition per
      batch; prompts stored; 19.4's scorer check; 20.6's five questions answered below.
- [x] Dependencies — 19.2b's and 14.13's setups and prompts, both stored.

0 unknown. Proceed.

## What is being tested, and it is not a clause

20.4's audit found that most rejections in this record take the shape *the baseline already does
this, so the clause buys nothing* — **a statement about the baseline**, measured on the strongest
available model, for scaffolding that exists to help a weaker one.

This round re-measures **only the controls**, on a weaker tier. No treatment arm is needed: if
the weak baseline still does the thing unaided, the rejection stands and is strengthened. If it
does not, the rejected clause comes back with its treatment numbers already in hand.

## Three claims, two conditions, six arms

18.3's control fixture and 19.2b's control fixture are **the same tree** — `.bemyagent/` holding
only `settings.json`, shipped protocol — so two of the three claims are read off one set of arms.

**Condition W** — bare `.bemyagent/`, shipped protocol, prompt **without** standing approval.
- **Claim 1 (18.3)**: *the baseline surfaces the product decision unaided*, 3/3 on Opus. Closed
  Milestone 18. If a Sonnet baseline does not surface it, 18.1's clause revives — and 18.1 already
  measured **surfaced 0/3 → 3/3**.
- **Claim 2 (19.1)**: *6/6 overrode Step 0's STOP, judging its condition wrong*. The whole of
  Milestone 19 rests on it, and it is the user's own hypothesis that a capable model overrides
  what a weaker one would obey.

**Condition G** — 14.13's seed: populated `.bemyagent/`, generated inventory with a stale pasted
block, prompt **with** standing approval.
- **Claim 3 (14.13)**: *the control is at ceiling*, 3/3 re-ran the command unaided. Closed the
  generated-code-map line. 14.12 read the identical condition at 1/3.

## 20.6's five questions, answered before launch

1. **Regime.** The point of the round: the control moves to the tier the scaffolding was written
   for.
2. **Redundancy or harm.** All three are redundancy rejections, which is why controls alone
   suffice.
3. **Occasion.** Each claim's occasion is the one its own round used, reproduced from stored
   setups. Claim 2's occasion is Step 0's STOP, which exists only without standing approval —
   hence two prompts, one per condition.
4. **Observations per metric.** Claims 1 and 2 are one observation per arm, which is weak and is
   stated now. Claim 3 is also per-arm. **This round cannot be made per-occasion**, because each
   claim is a single decision an arm makes once; the compensation is that a *reversal* needs no
   power — if a weak baseline fails where the strong one succeeded 3/3, that is visible at N=3.
5. **Cost.** Six Sonnet arms. The user authorised nine; the merge of claims 1 and 2 onto one
   condition saves three, and that saving is reported rather than spent elsewhere.

### Pre-mortem

1. **Sonnet cannot complete the task**, and the round measures capability instead of baseline
   behaviour. Checked first: delivery is scored on every arm, and an arm that fails to ship is
   excluded from claims 1–3 rather than counted as a baseline failure.
2. **The prompts are not the originals.** 18.3's prompt was never stored — the gap 14.9a wrote a
   rule about, and the same gap that made 19.1's 6/6 incomparable. Condition W uses **19.2b's
   stored prompt**, the closest recoverable match, and the substitution is recorded. Claim 1's
   comparison is therefore weaker than claims 2 and 3 and is reported as such.
3. **A reversal is the result I want**, which is exactly when to distrust the scoring. Mitigated
   by 19.4: open the arms at each end of every metric and name them before writing a verdict.

### Devil's Advocate

Do nothing: the audit already labels these verdicts provisional, and labels are cheap while arms
are not. Rejected, because a provisional label on a closed milestone is a note nobody acts on —
and because if the reversal is real, this repository has been deleting rules that work for the
agents that need them, which is the worst failure available to a project that measures protocols.

## Verification Plan

Claims scored from the arms' trees and transcripts, both conditions, with the arms at each end of
every metric opened and named. Delivery scored first, as the exclusion gate. Cost from `cost.py`,
reported against the Opus figures for the same conditions.
