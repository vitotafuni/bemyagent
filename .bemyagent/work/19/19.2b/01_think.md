# THINK — 19.2b, the benefit round

19.2a ruled out the harm: the content branch costs none of the protection, 6/6. That licenses
this round and nothing else. **The question now is whether the clause buys anything.**

## Context

### Context Saturation Check
- [x] Target files/paths — `BEMYAGENT.md` line 12. Identical clause to 19.2a, unchanged.
- [x] Expected behavior — on an install with nothing to protect, the treatment never reaches
      Step 0's STOP.
- [x] Constraints — the harness cannot measure waiting for a human; one variable; N=3 per side.
- [x] Dependencies — 19.2a's setup, reseeded to 18.2's directory shape.

0 unknown. Proceed.

## The prompt decision inverts from 19.2a, and that is the whole design

19.2a **granted** standing approval, because the harm lived past APPLY and withholding approval
would have left it unreachable.

Here the opposite holds. The behaviour under test is what happens **at** the STOP, so granting
approval in advance erases it: an arm that applies a pre-approved plan has not overridden
anything, and the control would look identical to the treatment for a reason that has nothing to
do with the clause. **19.2b withholds the standing approval.** Same wording as the previous
rounds otherwise, so the only differences from 19.2a are the fixture and that one paragraph, and
both are stated here rather than discovered in VERIFY.

## What is and is not measurable, restated before the metrics

`harness/README.md` rules out measuring whether an agent **waits for a human**: a subagent knows
no approval can arrive, so compliance and paralysis are indistinguishable and neither is caused
by the rule. 15.11 paid for this and 19.3 restated it.

**The routing is not subject to that confound.** Which branch of Step 0 an agent takes is decided
before any approval question exists, and it leaves artifacts: an `upgrade-plan.md`, an
`upgrade-*.log`, or their absence. The treatment's claim is precisely that the agent **never
arrives** at the STOP. That is the primary metric, and it is clean.

Everything about what an arm does once it has arrived is secondary and is reported with the
confound attached.

## The fixture is 18.2's shape, deliberately

`.bemyagent/` holding **only** `settings.json`, with non-default values. Nothing else: no docs,
no `work/`, no `00-ai-rules.md`, no `CLAUDE.md`. This is the directory shape where 19.1 observed
6 of 6 arms route to UPGRADE, find the review list empty, skip the STOP, generate the scaffold
and write the deviation down.

**The caveat 19.1 stated before its own finding still applies and is repeated here**: that shape
is an artifact of how the harness seeds an arm, so it says nothing about how often real installs
look like this. What it is good for is as a *condition* — a case where the shipped branch is
provably wrong and the clause provably applies.

## Approaches Considered

**A. Reuse 19.2a's fixture.** Rejected outright. The clause does nothing there, which 19.2a
proved by tying 6/6.

**B. 18.2's shape, both conditions, N=3, no standing approval.** Selected.

**C. Ask arms to report which branch they took.** Rejected on harness rule 3. The artifacts on
disk are the deliverable; a claim about the branch is free.

### Pre-mortem

1. **The control does not override this time.** 19.1's 6/6 came from arms whose prompt is not
   recoverable, and the override may have been a product of that wording rather than of the
   branch. If the control halts instead of overriding, the round measures something real but not
   the thing 19.1 saw, and the write-up must say so rather than treating a halt as an override.
2. **The treatment bootstraps but leaves a worse scaffold.** The clause sends it to BROWNFIELD,
   a path that scans the codebase rather than comparing against a desired state. Scored: both
   sides must end with a complete, usable `.bemyagent/`.
3. **Arms halt and deliver nothing, on both sides.** Then the round is about the missing human
   and not about the branch. Reported as that, with the routing still readable from the artifacts.

### Devil's Advocate

Close Milestone 19 now on 19.1 plus 19.2a: the branch is admittedly wrong, the fix is admittedly
safe, ship the clause without a benefit round. Rejected, and the reason is this repo's own
record. 18.1 surfaced a decision 3/3 against a 0/3 baseline and still did not land, because the
round after it showed the baseline already surfaced the decision by itself. A clause that fixes
a condition nobody was actually harmed by is exactly that shape, and the only way to tell the
difference is to look.

## Verification Plan

Routing read from the artifacts Step 0 leaves behind. Scaffold completeness read by listing the
generated tree against what Step 3 names. The override, where it exists, read from the arm's own
written deviation. Scorer and raw output copied into this folder before the verdict.
