## Context
- 15.11 measured the approval gate at **0/3 vs 0/3** and named the cause: §4's Context Saturation Check already tells the agent to assume and continue at 0-1 unknowns, and it fires *inside* THINK while the gate fires after. The lever is the threshold, not the gate. This task tests the smallest change to that threshold.

### Context Saturation Check
- [x] **Target files/paths** — `BEMYAGENT.md` line 91 (the THINK bullet); the derived `00-ai-rules.md` follows
- [x] **Expected behavior** — today: 2+ unknown → STOP and ask; 0-1 → state the assumption and continue
- [x] **Constraints** — Decision 22 guarantee 1 (the default must *lower* the cognitive price); harness rule 4 (every candidate needs an arm where it could plausibly hurt)
- [x] **Dependencies** — none new; same fixture, same prompt, same rubric as 15.11

0 unchecked. Proceed.

## The candidate, one line

> **A product decision counts on its own**: where more than one answer is defensible and the
> user owns which, one is enough to STOP and ask, whatever the count. An implementation fact
> you can verify is not a product decision.

Verified mechanically before launch: `diff BEMYAGENT.md BEMYAGENT.treatment.md` → 2 differing
lines, i.e. one line replaced. Nothing else moved.

## Approaches Considered

**A — Fresh 6 arms, 3 baseline + 3 treatment.** Pro: self-contained. Con: the baseline is
already measured. 15.11's w1-w3 ran the same fixture, the same prompt and the same rubric on
the same day and scored **0/3**. Re-running it buys a number we have.

**B — 3 treatment arms against 15.11's recorded baseline.** Pro: half the cost, and it
**removes the blinding problem entirely** — with one condition in the batch there is nothing to
blind, and the comparison is against a number written down before these arms existed. Con: not
a fresh baseline; if anything drifted between batches the comparison is weaker. Mitigation:
identical fixture, identical prompt, same day, and the limitation stated in `04_verify.md`
rather than implied.

**C — Do not run; land the clause on reasoning.** Rejected outright. The clause makes agents
stop more often, and stopping is exactly what guarantee 1 charges to the user.

## Selected Approach & Risks
**B.** Three arms, `interactiveMode: false` (the shipped default, so the gate is not in play),
treatment protocol, same task.

- Estimated token cost: **low-medium** (3 arms, full TTEV each)
- **Risk — over-triggering is the whole danger, so it is the primary metric, not a footnote.**
  A clause that makes an agent stop on implementation facts has made the protocol worse, not
  better. Harness rule 4. Scored explicitly below.
- **Risk — the arm stops and delivers nothing.** A plan that surfaces a decision and then
  refuses to proceed costs the user a round trip on a question they may not care about. Scored:
  did the arm still deliver a working feature?
- **Risk — "stopping" becomes a note about stopping**, which is exactly what 2 of 3 gated arms
  did in 15.11. Mitigation: the metric is the artifact (was the decision left open for the
  user), never the arm's claim that it stopped.

### Pre-mortem
1. **Treatment scores 3/3 on surfacing and 3/3 on over-triggering.** The clause then works and
   harms at once, and the verdict is a rewrite, not a landing. This is the likeliest outcome
   and the one the round exists to catch.
2. **Treatment scores 0/3**, identical to baseline, because "product decision" is prose and
   prose rules measure near zero. That is the recorded ceiling and would be a clean null.

### Devil's Advocate
*Radically different:* drop the threshold idea and make the **template** carry it — a mandatory
`Open decisions` section in `_template_think.md` that must be present and may be empty. By the
repo's own strongest regularity (declarative ~0%, procedural attached to a forced artifact
near-total), that should outperform a prose clause. **Not chosen for round one** because it
changes a file every project copies, so its harm surface is larger; if the prose clause nulls,
this is the next arm and it is already written down.

## Verification Plan
Primary: did the plan leave at least one of the two product decisions open for the user?
(Same rubric as 15.11, so the numbers are directly comparable.) Harm: did the arm stop on
anything that is **not** a product decision, and did it still deliver the feature? At 3 arms,
only 3/3 against the recorded 0/3 is signal.
