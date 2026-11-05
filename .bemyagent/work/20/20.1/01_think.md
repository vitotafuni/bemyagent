# THINK — 20.1, what a round costs and where its question comes from

## Context

### Context Saturation Check
- [x] Target files/paths — `harness/README.md`, `05-decisions-and-issues.md`, `06-implementation-plan.md`.
- [x] Expected behavior — a reader can price a round before running it, and knows why the arms
      run on the tier they do.
- [x] Constraints — **zero agents**: the user has paused rounds and will say when they resume.
      No `BEMYAGENT.md` delta, so no tag.
- [x] Dependencies — none. The figures come from this session's transcripts.

0 unknown. Proceed.

## Why this is a milestone of its own rather than a line somewhere

Two things surfaced in conversation today that exist nowhere in the repository, and the round
that closed an hour earlier measured exactly this failure: **a record that lives only in the
conversation is invisible to everyone who was not in it.** Writing them down is the rule I just
spent six arms failing to improve.

**1. Nobody has ever priced a round.** `harness/README.md` mentions `tokens.py` for per-arm cost
and warns never to use it for quality. It does not say what a round costs, so every round has
been authorised without a number. Today four rounds and a voided batch ran against a session
limit that was hit at 18:30, which was arithmetic rather than bad luck.

**2. The arm model tier was inherited, not argued.** The harness rule says *pin the model*; it
never says which. Opus was used because the coordinator runs Opus and the record started there.

## The measurement

From this session's agent transcripts, 119 of them:

| | total | per agent |
|---|---|---|
| cache read | 289.4 M | 2.43 M |
| cache write | 16.7 M | 140 k |
| output | 5.6 M | 47 k |
| uncached input | 10 k | 86 |

Weighted at cache-read 0.1×, cache-write 1.25×, output 5×: **≈ 78 M equivalent, ≈ 653 k per
agent.** Cache read is 93% of the raw total, which is the structural driver: an arm re-reads a
large context at every step.

**An arm is not an agent.** Most arms spawn a second agent for the independent VERIFY that §4
asks for, so **a six-arm round is about twelve agents, ≈ 7.8 M equivalent.**

## On the tier, and the argument that got weaker this week

The case for Opus was comparability with the record. That case is now weak on this repo's own
evidence: 14.12 against 14.13 read the same condition at 1/3 and 3/3, and the Write Gate's
coverage read 60% and 89% a day apart. **Cross-round comparison is already untrustworthy**, so
little is lost by changing tier, and the design protects itself anyway because control and
treatment sit in the same batch.

Against that, a real gap: **BMA ships to everyone and has only ever been measured on the most
expensive tier.** A clause that lands on one tier and not another is a finding about the
protocol, not an inconvenience.

Not decided here as a change — rounds are paused. Recorded as the standing choice, its reason,
and the conditions under which it should change.

## Approaches Considered

**A. Leave it in the conversation.** Rejected, and the rejection is this week's own result.

**B. One sentence in `05`.** Rejected as insufficient for the cost half: a number a reader needs
*before* authorising a round belongs beside the instructions for running one.

**C. `harness/README.md` for cost and tier, `05` for the cadence decision.** Selected. The
Routing Table's own split: the apparatus is documented where it is used, the decision where
decisions live.

### Pre-mortem

1. **The figures rot.** Token accounting and model pricing change. Mitigated by recording the
   measurement, its date and its method rather than a verdict, so a reader can re-run it.
2. **"A round costs 7.8 M" reads as a licence to spend it.** Mitigated by stating in the same
   breath what today bought: four rounds, zero lines changed in the distributable.

## Verification Plan

`diff` both files and confirm the delta is the intended places. Confirm `BEMYAGENT.md` untouched.
Confirm the cost figures in the text match the script's output.
