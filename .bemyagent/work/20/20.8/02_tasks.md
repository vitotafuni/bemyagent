# 20.8 — TASK

**Delivers:** the fourth cell of the protocol × tier grid — **Sonnet with no protocol file of any
kind** — so 20.3's headline can be attributed to the protocol, to the tier, or to neither, on
evidence rather than on the order the rounds happened to run in.

## Condition

| | tree | prompt | model |
|---|---|---|---|
| **M** (this round) | 20.2's N seed: the fixture with `BEMYAGENT.md` deleted, no `.bemyagent/`, no `CLAUDE.md` | `20.2/prompt_N.txt`, byte-identical | **Sonnet** |

`q91 · q92 · q93`, three batches of one arm. There is **one** condition in this round, which
breaks the harness rule that arms are batched across conditions: the three comparators ran on
2026-11-06 and 2026-11-08. This is a real weakness and it is not repairable at this price, since
re-batching means re-running two Opus cells. What bounds it is that the **same** condition already
has two independent readings taken two days apart — 20.2's N and 20.3's O, both Opus with no
protocol — and metric (i) reproduced exactly (0/3 and 0/3) while cost moved 1.11× (337 k against
303 k weighted mean). The binary teeth reading is cross-round stable on this task; the cost column
is the one to distrust, and it is read within tier below for that reason.

Task unchanged from every round since 15.4: *Add a scoreboard: show how many games X and O have
won, above the board.*

## Metrics, fixed before launch

### Primary

**(i) Tests with teeth** — `mutate.py` applies one semantic mutation, identical for every arm:
**a drawn game counts as a win for X.** The arm's own suite is then run. **RED** = the arm's tests
caught it. 3 observations. Per-arm, and therefore weak at N=3 by construction — 20.6 Q4 is
answered below, not dodged.

**(ii) Test artifacts left in the repository** — files added under `test/` and total test count,
counted from the tree, not from the transcript. This is the mechanism metric: metric (i) can only
read teeth on a suite that exists. Per arm, but a count rather than a binary.

**(iii) Delivery** — the scoreboard works: the tally endpoint or query exists and the client
renders it. 3 observations.

**(iv) Weighted tokens** — `W = {inp 1.0, cc 1.25, cr 0.1, out 5.0}`. Read **within tier** against
20.3's S (Sonnet + protocol, 264 k mean) for the protocol's overhead on the cheap tier. The
cross-tier reading against 20.3's O is reported but carries the 1.11× cross-round wobble above.

### Secondary, pre-registered now, before any tree is touched

**(v) A second mutation, M2: X's and O's totals swapped** (`CASE WHEN winner='X' THEN 'O' WHEN
winner='O' THEN 'X' ELSE winner END`), applied by the same mechanics as M1 to **all fifteen arms**
— q52–q57, q85–q90 and q91–q93. A test that asserts per-player numbers against asymmetric data
catches it; one that asserts only that the scoreboard renders, or that the totals sum correctly,
does not. This doubles metric (i) to **6 observations per condition at zero agent cost**, which is
the one free lever 20.6 Q4 names.

It is reported in a table of its own and **never merged into the published M1 figures.** Those
were scored before this mutation existed; folding a mutation chosen today into a verdict published
on 2026-11-06 would be re-scoring a round to a rubric its arms were never measured against. If M2
and M1 disagree on any condition, the disagreement is the finding.

## Readings fixed before launch

On metric (i), with Sonnet + protocol at 3/3:

- **0/3** → the grid completes with the protocol separating on **both** tiers (2/3 and 3/3 against
  0/3, 0/3, 0/3). 20.3's headline stands and is attributable to the protocol.
- **3/3** → **reversal.** The test comes from the tier, not from the protocol, and 20.3's headline
  collapses into a statement about Sonnet. This outcome is the reason to run the round.
- **1/3 or 2/3** → **under-powered**, per 14.14. No verdict on (i); fall back to (ii)'s counts and
  to (v)'s six observations, and say plainly that the primary metric resolved nothing.

## Checklist

- [ ] Build three arms from 20.2's `setup.py`, N branch, arm filter and overwrite guard in place
- [ ] `03b_delta.txt`: blob-hash the new seeds against 20.2's N and 20.3's O at their setup commits
- [ ] Launch, Sonnet pinned, one arm per batch, prompt stored verbatim
- [ ] Per-arm SQL read out of each arm's own `server/store.js` — `EDITS` blank until then
- [ ] M1 on q91–q93; restore and confirm `git status` unchanged
- [ ] M2 pre-registered above, then applied to all fifteen arms
- [ ] (ii) and (iii) from the trees; (iv) from the transcripts of this round only
- [ ] `04_verify.md`: each metric classified mechanism / null / ceiling / under-powered, arms named
      at both ends
- [ ] Amend `20.3/04_verify.md` with a dated addendum: the Opus + protocol cell was never owed
- [ ] Ports swept before and after
