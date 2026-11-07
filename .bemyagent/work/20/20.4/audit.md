# 20.4 — tier-sensitivity audit of the record since 2026-10-27

Zero agents. Every verdict reached since `BEMYAGENT.md` last changed, classified by whether a
different model tier could overturn it. Requested by the user, 2026-11-07.

## The systematic bias, stated first because it organises everything else

BMA's scaffolding — Devil's Advocate, the anti-drift CDM, ceremony sizing, the Saturation
Check — exists to get good work out of an agent that would not produce it unaided.

**Every round in this window measured that scaffolding on the strongest available model**, which
is the regime where it is least needed. And the shape most of the rejections took is:

> *the baseline already does this, so the clause buys nothing.*

That sentence is a statement about the baseline, not about the clause. **Measured on a weaker
baseline it could reverse**, and if it reverses, the rejected clause was rejected for doing
exactly its job.

## The classification

**A — tier-independent.** Instrument and logic; no agent behaviour in the conclusion. Safe.

| | verdict |
|---|---|
| 14.14 | null / ceiling / under-powered are different verdicts |
| 19.4 | a scorer is an instrument and must be checked at each end of a metric |
| 20.1 | what a round costs; the tier was inherited, not argued |
| 14.9a | store the launch prompt verbatim |
| 18.2a, 14.3a | a partial round is void, not small |
| 15.4 (half) | the clause names `03_execute.log`, which **does not exist** when Step 0 runs. Pure logic |

**B — rejections on harm.** The clause was refused because it *causes* something bad. A weaker
model would plausibly cause the same or more, so these hold or strengthen. Robust.

| | verdict |
|---|---|
| 17.2 | `RUNTIME_CHECK` inflates non-falsifiable evidence 3/3 |
| 14.9 | 2/6 arms bought recall by deleting the grep — perfect recall, zero symbols |
| 14.12 | one arm hand-typed nine lines into a block that claims to be command output |
| 15.4 (half) | the on-disk record names 13 of 28 governed files against 24 in conversation: it under-reports the gate for its only reader |

**C — rejections on redundancy. The fragile core, and these closed milestones.**

| | verdict | what a weaker baseline could do |
|---|---|---|
| **18.3** | *the baseline already surfaces the decision* 3/3 → **Milestone 18 closed, nothing landed** | not surface it, which would revive 18.1's clause — already measured at **surfaced 0/3 → 3/3** |
| **14.13** | *the control is at ceiling*, 3/3 re-ran the command unaided → **the generated-code-map line closed** | not re-run it, which is 14.12's original 1/3 reading |
| **15.11** | approval gate null, because §4 already says assume-and-continue | not assume competently, making the gate load-bearing |
| **19.2a** | harm absent: 6/6 preserved the user's content through an overwrite | **destroy it** — this one is fragile in the dangerous direction |

**D — behaviour rates, fragile in magnitude.** The direction may survive; the number will not.

| | verdict |
|---|---|
| 19.1 / 19.2b | 6/6 overrode Step 0's STOP, judging its condition wrong — **the user named this one**: a capable model overrides what it judges pointless; a weaker one may simply comply |
| 19.3 / 15.4 | Write Gate emitted 6/6, coverage 60% and 89% a day apart |
| 14.8 / 14.9 | a MUST is obeyed, descriptive prose mostly is, silence is a hole |
| 15.9a | a layer-crossing test appears in 2 of 18 arms — the occasion is absent **on this tier** |
| 20.2 | already narrowed on 2026-11-06 for this and two other reasons |

## Are the commits necessary

Nothing is deleted. Publishing rejections on the same terms as acceptances is this repo's own
rule, and a verdict that later turns out to be tier-bound is still evidence of what that tier
does. What changes is the **label**: every verdict in C and D is provisional, and the record now
says so.

The honest count: of 24 commits, **6 record instrument work that stands unconditionally**, 4
record harm findings that hold or strengthen on a weaker tier, and **the rest rest on a baseline
that may be too capable to need the protocol under test.**

## The re-test plan, cheapest first, none of it launched

**The key economy: to audit a redundancy rejection you only need to re-measure the baseline.**
The claim *"the baseline already does it"* is about the control, so a cheap-tier control alone
falsifies or confirms it. No treatment arm is needed until it falsifies.

| | what | arms | why first |
|---|---|---|---|
| **P1** | 18.3's and 14.13's **controls only**, cheap tier: does a weaker baseline surface the product decision, and does it re-run the inventory command unaided? | 3 + 3, cheap | Two closed milestones hang on these two sentences. If either baseline fails, a measured candidate comes back from the dead with its treatment numbers already in hand (18.1: surfaced 0/3 → 3/3) |
| **P2** | 19.1's override rate on a cheap tier: `.bemyagent/` holding only `settings.json`, does a weaker agent comply with Step 0's STOP instead of overriding it? | 3, cheap | The user's hypothesis, and the whole of Milestone 19 rests on 6/6 |
| **P3** | **20.3** — Sonnet+BMA against Opus-without-BMA, same batches | 3 cheap + 3 expensive | Break-even is at t = r; the measured overhead is 2.54× against a tier ratio an order of magnitude larger |
| **P4** | 19.2a's harm on a cheap tier: does a weaker agent destroy the user's content during an upgrade? | 3, cheap | The only fragile verdict whose failure mode is **data loss**, so it ranks above curiosity |

P1 and P2 together are nine cheap arms and answer the question that matters most: **has this
repository been rejecting rules that a weaker agent needs?**

## Two notes on method, from this audit

**The protocol's own cost rule measures zero.** `autoModelSwitching: true` was set in every
seeded `settings.json` this week. Across 30 subagents the arms spawned: **0 with a cheaper model,
29 with no model specified at all, and 0 arms that even name the setting.** The unpinned 29 are
also the exact failure 14.4 documented and `harness/README.md` forbids — applied by the arms to
their own verifiers, where it went unnoticed for four rounds.

**The pre-mortems were pointed at correctness and never at price.** Every `01_think.md` this week
carries a Pre-mortem and a Devil's Advocate. Re-read, they all argue about validity — is the
round interpretable, is the occasion present, is the control at zero — and **not one asks whether
the answer is worth what it costs.** A pre-mortem that cannot say *too expensive for what it can
tell us* is incomplete, and that is the gap that let this week happen.
