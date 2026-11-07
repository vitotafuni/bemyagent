# VERIFY — 20.5, is the record's fragile core an artifact of the tier

Raw evidence `03c_arm_evidence.txt`, scorer `score_claim3.py`, setups `setup_W.py` / `setup_G.py`,
both prompts stored with provenance.

## 19.4's check — the arms at each end of every metric, named

| Metric | Read | Result |
|---|---|---|
| claim 2 | **q58** (first to stop) and **q62** (last) | matches: `upgrade-plan.md` on disk, **0 source files changed** in all three, confirmed by `git status` |
| claim 3 | **q59** (first) and **q63** (last, the most thorough hand-back) | matches: all three blocks are 3 lines against 30 from their own named command |
| delivery | **q58** (0 delivered) and **q63** (delivered, 5 tests) | matches, and q58's zero is compliance, not incapacity — it changed nothing |
| cost | **q58** (41 k) and **q59** (58 k) | matches |

## The result

**Claim 2 — the STOP. REVERSED, cleanly.**

| | stopped at Step 0's STOP |
|---|---|
| Opus, stored prompt (19.2b) | **0 / 3** |
| Sonnet, same prompt (20.5) | **3 / 3** |

Same tree, same protocol, same prompt. The only variable is the tier.

**Claim 3 — the inventory re-run. REVERSED, cleanly.**

| | re-ran the command unaided |
|---|---|
| Opus (14.13) | **3 / 3** |
| Sonnet (20.5) | **0 / 3** |

All three Sonnet arms delivered the feature with tests green, so this is behaviour, not
incapacity.

**Claim 1 — not measured.** Claim 2's compliance destroyed its occasion.

## Verdict: two milestone-closing rejections were artifacts of the tier

Both were refused on the sentence *the baseline already does this, so the clause buys nothing*.
On the tier the scaffolding was written for, **the baseline does not do it**.

- **Milestone 19 reopens.** It closed concluding Step 0's branch condition was wrong because 6/6
  overrode its STOP. Measured on a weaker model, 3/3 obey. **The gate is not a rule that fails to
  land — it lands on the agents it was written for and is overridden by the ones capable enough
  to judge it pointless.** That is the user's hypothesis, measured.
- **The generated-code-map line reopens.** 14.13 closed it at a ceiling: the control re-ran the
  command unaided 3/3, so the clause had nothing to buy. On Sonnet the control re-runs it **0/3**
  while still shipping the feature, which is precisely the drift the clause existed to catch.

What does **not** follow: that either clause now lands. Neither has been measured as a treatment
on this tier. What follows is that **they were rejected for the wrong reason**, and their rounds
are owed a re-run against a baseline that needs them.

## What this costs the record, stated plainly

20.4's audit called these two the fragile core and was right. The consequence is larger than two
milestones: **every rejection in this repository shaped *the baseline already does this* is now
presumed tier-bound until re-measured** — 15.11 and 19.2a's absent harm are the two that remain,
and 19.2a's failure mode is data loss, which ranks it next.

It also vindicates the protocol in a way none of this week's rounds could. BMA's scaffolding
exists to get good work out of an agent that would not produce it unaided. Measured on an agent
that produces it unaided, the scaffolding looks like ceremony. **That is not evidence against the
scaffolding; it is evidence that the measurement was taken in the wrong regime**, and the record
has been accumulating that error since at least Milestone 18.

## Caveats

1. **Claim 1 is unmeasured** and the design error that caused it was mine, declared after the
   first arm rather than in VERIFY. Three more arms with standing approval would close it.
2. **Claim 2's reversal rests on the 19.2b comparison**, not 19.1's 6/6, because 19.1's prompt
   was never stored. The comparison used is same-prompt and therefore stronger, but it is three
   Opus arms rather than six.
3. **One tier step, one task, one fixture.** Sonnet is not *the* weak baseline; it is one point.
4. **Neither clause has been re-measured as a treatment.** This round re-measured controls only,
   which is what made it cost six arms instead of eighteen.
5. **Delivery differs by condition by design** — W arms stop before building, G arms build. The
   two conditions are not comparable to each other and were never intended to be.
