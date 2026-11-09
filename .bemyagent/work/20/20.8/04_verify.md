# 20.8 — VERIFY

Three Sonnet arms with no protocol file of any kind, on 20.2's N seed and 20.2's N prompt, both
byte-identical (`03b_delta.txt`, 18 blob-hash comparisons, 0 diff lines). The fourth cell of the
protocol × tier grid. Scored with 20.2's instrument, whose per-arm edits this round **derived from
each arm's own code** and cross-checked against the published tables: **12 of 12 prior arms match
exactly.**

## Against the readings fixed before launch

| | reading | arms at each end | verdict |
|---|---|---|---|
| (i) teeth, M1 | **Sonnet-none 0/3** against **Sonnet+BMA 3/3** | q91 q92 q93 GREEN · q85 q87 q89 RED | **mechanism** |
| (ii) test artifacts | **0/3 added any case** against **3/3** | q91–q93 stay at the 4 seeded · q85 q87 q89 at 5 | **mechanism** |
| (iii) delivery | **3/3** | all three: tally, route, markup, plus their own live curl | **ceiling** |
| (iv) cost | 284 k · 75 k · 84 k against S's 277 k · 264 k · 250 k | q91 (284 k) costs more than every S arm | **under-powered** |
| (v) teeth, M2 | **Sonnet-none 0/3**, and **q57 flips** | q57 GREEN on M1, RED on M2 | **the pre-registered disagreement fired** |

02_tasks.md fixed 0/3 as *"the grid completes with the protocol separating on both tiers"* and 3/3
as a reversal. It read **0/3**.

## The grid, now complete

Metric (i), one mutation — a drawn game counts as a win for X — one scorer, fifteen arms:

| | protocol | no protocol |
|---|---|---|
| **Opus** | **2/3** q52 RED · q54 GREEN · q56 RED | **0/6** q53 q55 q57 · q86 q88 q90 |
| **Sonnet** | **3/3** q85 q87 q89 | **0/3** q91 q92 q93 |

**Pooled: 5/6 with the protocol, 0/9 without.** On M2: 5/6 against 1/9.
Per occasion, two mutations × fifteen arms: **10/12 against 1/18.**

Three days and two rounds apart, M1 reproduced every published reading exactly, on all twelve
prior arms, with `tree-unchanged=True` throughout. The binary teeth reading is stable; see the cost
row for the column that is not.

## Verdict: the test is the protocol's, not the tier's

20.3 reported that the cheap tier with the protocol beat the expensive tier without it, and could
not say which half of that pair did the work. **It was the protocol.** Hold the tier fixed at
Sonnet and the separation is complete — 3/3 against 0/3, same seed, same prompt minus two
sentences, same model. Hold the protocol fixed and absent, and the tier changes nothing: Opus
reads 0/6 and Sonnet 0/3 on the identical metric.

### The mechanism is on disk, and it was written before the code

Harness rule 1 is to measure the mechanism, not the outcome. Each protocol arm's `01_think.md`
carries a **Verification Plan written before EXECUTE**, and it predicts that arm's artifact **6/6**:

- **q52** — *"plus a new `test/scores.test.js` … after a drawn game and an abandoned game the
  counts are still `{X:1,O:0}`"*. Wrote it. 8 cases. RED.
- **q56** — *"new unit tests cover the tally query directly … a win for X, a win for O, **a draw**,
  an unfinished game"*. Wrote it. 8 cases. RED.
- **q85 / q87 / q89** — *"Unit test for getScores"*, *"Unit test for scores"*. All three wrote one.
  RED.
- **q54** — the plan names **no test**: *"npm test still green (4 tests)"* plus live curl against a
  throwaway DB. Wrote none. GREEN. The one protocol arm that did not plan a test is the one
  protocol arm without teeth.

So the protocol does not produce a test by asking for one — §4 never mentions tests, and 20.3's
caveat 4 stands. It produces a **Verification Plan written down before the work**, and what an
agent writes there, it builds. The no-protocol arms verified just as carefully: q91, q92 and q93
each stood up a server on a high port, drove a real game to a win through the API and read the
counts change. **Their verification was as good and it is gone.** It existed in a session that has
ended; nothing in their repository can be re-run tomorrow.

That is the first time this record has separated the two things it has been circling since 15.10 —
how carefully an agent checks, and whether the check survives the agent.

### What M2 found that M1 could not

q57 — Opus, no protocol — wrote `test/scores.test.js` with 7 cases, unprompted and with no plan
file to write it into. **M1 reads it GREEN, M2 reads it RED.** Its tests pin per-player numbers and
do not touch draw semantics. 20.2 had flagged it as *"GREEN with tests"* and left it there; the
second mutation, pre-registered before any tree was touched, says precisely what its tests do and
do not hold. One arm in nine will write a real test with no protocol at all, and that one arm's
test is partial in a way one mutation cannot see.

This is 20.6 Q4 paying out: a second mutation doubled the observations at zero agent cost and
changed one reading in fifteen.

## Cost, read within tier

| condition | arms | weighted | mean |
|---|---|---|---|
| Sonnet, no protocol | q91 q92 q93 | 284 k · 75 k · 84 k | 148 k |
| Sonnet + protocol (20.3 S) | q85 q87 q89 | 277 k · 264 k · 250 k | 264 k |
| Opus, no protocol (20.2 N + 20.3 O) | six arms | 429 k · 323 k · 259 k · 300 k · 297 k · 312 k | 320 k |
| Opus + protocol (20.2 P) | q52 q54 q56 | 1 084 k · 637 k · 850 k | 857 k |

**On Opus the protocol costs 2.54× and the ranges do not overlap** — the cheapest P arm (637 k)
is above the dearest N arm (429 k). **On Sonnet they overlap:** q91 alone spent 284 k, more than
every arm on the protocol side, and the control's own spread is 3.8× end to end. The mean ratio is
1.78× and it is **not a reading** at N=3 — recorded as under-powered, not as a cheaper protocol.

What survives: **Sonnet with the protocol costs 0.82× Opus without it** (264 k against the pooled
320 k), on six comparator arms now instead of three. 20.3's t = 0.87 holds at 0.82 with the larger
pool, and the tier gap at equal protocol is 2.16×.

I checked and discarded one explanation before publishing it: q91's 284 k is not a cold-cache
artifact of being first. Its output (13.1 k) and cache reads (655 k) are both roughly triple its
siblings', and it took 8 tool calls to their 6. It did more work. The spread is real per-arm
variance, which is the thing that makes an N=3 cost reading weak in the first place.

## What this does not say

1. **One task, one shot, no context reset.** Inherited whole from 20.2 and 20.3. The mechanism
   TTEV exists for still has never had an occasion in any round this project has run.
2. **Machine-observable only.** Fifteen arms and not one of them was read by a human asking
   whether the repository explains itself.
3. **The arms were not batched against their comparators.** Three cells ran on 2026-11-06 and
   2026-11-08, this one on 2026-11-09. What bounds it is that M1 reproduced all twelve prior
   readings today; what it does not bound is the cost column, which is why that column is read
   within tier and classified under-powered.
4. **(i) still rewards leaving a test**, and 20.3's defence still holds — q54 proves §4 does not
   ask for one. The mechanism section above makes the better case: the plan predicts the artifact
   6/6, and the plan is the thing the protocol actually asks for.
5. **N=3 per cell.** Pooling to 5/6 against 0/9 is four rounds of arms read together, not one
   large round, and they share a task, a fixture and a prompt.
6. **The task has never changed.** Every arm since 15.4 has added a scoreboard to the same
   tic-tac-toe app. A protocol that only ever helps on this task would read identically.

## Cost of the round
Three Sonnet arms, 444 k weighted tokens over the three, plus 30 `npm test` runs across fifteen
trees. The round 20.3 asked for instead — three Opus arms re-measuring 20.2's P — would have cost
roughly six times that and answered nothing.
