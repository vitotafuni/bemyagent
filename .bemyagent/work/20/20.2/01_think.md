# THINK — 20.2, does the shipped protocol beat no protocol

## Context

### Context Saturation Check
- [x] Target files/paths — no protocol delta at all. The variable is `BEMYAGENT.md` existing.
- [x] Expected behavior — unknown, which is the point. This is the first round with no candidate.
- [x] Constraints — N=3 per side, one arm per condition per batch, model pinned, prompts stored;
      **19.4's scorer check applies**; the control's prompt necessarily differs by the protocol
      sentences, which is the condition itself.
- [x] Dependencies — 15.4's setup for the BMA side.

0 unknown. Proceed.

## Why this round, and why it is not mine

Every round in this repository compares a **candidate clause** against shipped BMA. Nobody has
compared shipped BMA against **nothing**. `05` now carries the arithmetic that made the gap
visible: `BEMYAGENT.md` has not changed since 2026-10-27, the external candidate sources are
exhausted, and every recent candidate traces back to one of my own earlier rounds.

This question comes from the user, not from a round of mine, and it is the one that separates *a
stable product* from *an elaborate way of not noticing*.

## The condition, and I am choosing the one that flatters BMA

Two honest framings exist:

1. **Bootstrap**: BMA arms start from a bare repo and pay Step 0 and the whole scaffold. This is
   what a new user experiences, and it loads the protocol's cost into the comparison.
2. **Steady state**: BMA arms start from a `.bemyagent/` already populated and committed, as
   15.4's arms did. This is what a project that already installed BMA experiences.

**Steady state is selected**, deliberately, because it measures the protocol at its best: the
setup cost is already sunk and only the per-task behaviour is compared. If BMA cannot win here,
the bootstrap framing will not rescue it. Stated now so the choice is not read as an accident
later.

## What can be measured that is not a tautology

The trap is obvious: *"did the arm write `03_execute.log`"* is a question only one side can
answer, and scoring it would be measuring the protocol's definition rather than its effect. Three
metrics avoid it, plus one the repo has never taken.

**(i) Do the tests have teeth.** Mutate every arm's own store function identically — the win
filter `winner IN ('X','O')` becomes `winner IS NOT NULL`, which silently counts draws — and run
that arm's own suite. Red means the tests guard the behaviour; green means they decorate it.
Several arms' independent verifiers ran this mutation on themselves; here it is run uniformly by
me, on both sides.

**(ii) What the arm noticed that nobody asked about.** The fixture carries real pre-existing
defects: `api()` never checks `res.ok`, a reload starts a new game while `01-overview.md` claims
otherwise, `server/session.js` is 309 lines nothing imports, a stale known issue. Count how many
each arm surfaces anywhere in its output. This is the clearest candidate for a protocol effect —
§5 and §6 push an agent to read and record — and it is equally countable on an arm that writes
no docs at all, because a hand-back is text.

**(iii) Delivery.** Does the scoreboard work and is the suite green. Expected to tie; scored so a
tie is on the record rather than assumed.

**(iv) What it costs.** Weighted tokens per arm from `cost.py`. **The protocol's price has never
been measured.** A protocol that buys (i) and (ii) at 3× the tokens is a different proposition
from one that buys them free, and the user is paying either way.

## Approaches Considered

**A. Reuse the 24 BMA arms already paid for as the treatment side.** Rejected as the primary
design, kept as a cross-check. It is a cross-round comparison, and 14.12 against 14.13 read the
identical condition at 1/3 and 3/3. Three fresh BMA arms run in the same batches cost little
next to believing a number the harness has twice shown to be unstable.

**B. Three per side, same batches.** Selected.

**C. Score the documentation.** Rejected as the tautology above.

### Pre-mortem

1. **Everything ties.** The likeliest outcome: both sides ship a working scoreboard with shallow
   tests. That is a result, and an uncomfortable one, and it must be reported as flatly as a win
   would be.
2. **(ii) rewards verbosity rather than attention.** A BMA arm writes more text, so it has more
   chances to mention something. Mitigated by counting **distinct defects named**, not words, and
   by reading the arms at each end per 19.4.
3. **The mutation does not apply uniformly.** Arms name their store function differently and
   some filter in SQL, some in JS. The mutation is applied **per arm, by reading its own code**,
   and any arm where the mutation cannot be applied is reported as not-applicable rather than
   silently counted as passing.

### Devil's Advocate

The strongest objection is that this round cannot lose in a way that changes anything: if BMA
wins I keep it, if it ties I say the protocol is cheap ceremony, and either way nothing ships.
Partly true. What makes it worth running is **(iv)**: a tie at equal cost and a tie at triple
cost are different findings, and only one of them is comfortable.

## Verification Plan

Mutation run per arm in its own tree. Defect counts read from the arm's full output, with the
arms at each end opened and named per 19.4. Cost from `cost.py` over this round's transcripts
only. Scorer and raw output copied here before the verdict.
