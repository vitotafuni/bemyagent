# 20.8 — THINK

## Context

The round 20.3 said was owed does not need to be run. It has already been run.

20.3's `04_verify.md` closes with: *"A third condition, Opus + protocol, would separate them, was
rejected on price, and is the obvious next round."* That is **false, and it was false when it was
written.** Opus + protocol is 20.2's P side: same task, same stored prompt, same seed,
and metric (i) is the same instrument — `20.3/mutate.py` is `20.2/mutate.py` with the tree path
and the per-arm SQL changed, docstring included. 20.3's own validation step compared its S seed
against 20.2's P seed by git blob hash and found 726 files differing only on `BEMYAGENT.md`.
I had the comparator open in front of me and still recorded its condition as unmeasured.

What the four conditions actually read on metric (i), tests with teeth, same mutation, same scorer:

| | protocol | no protocol |
|---|---|---|
| **Opus** | **2/3** (20.2 P: q52 RED, q54 GREEN, q56 RED) | **0/3** (20.2 N) and **0/3** (20.3 O) |
| **Sonnet** | **3/3** (20.3 S) | **— this round** |

The empty cell is not Opus. It is **Sonnet without the protocol**, which is the cheapest arm in
the matrix, and it is the one that decides whether 20.3's headline belongs to the protocol or to
Sonnet. Without it, *"the cheap tier with the protocol beat the expensive tier without it"* has an
alternative reading that costs nothing to state: Sonnet writes tests and Opus does not, protocol or
no protocol.

### Context Saturation Check
- [x] Target files/paths — `work/20/20.8/`, arms in `scratchpad/r208`, comparators already on disk
      in `scratchpad/r202` (q52–q57) and `scratchpad/r203` (q85–q90), all 12 trees verified present
- [x] Expected behavior — three Sonnet arms on 20.2's N seed and 20.2's N prompt, both unchanged
- [x] Constraints — N=3, model pinned to Sonnet, prompt stored verbatim, instrument inherited
      without edits except the tree path and the per-arm SQL table, which is built per batch
- [x] Dependencies — none new; `node --test`, `better-sqlite3`, the 20.2 scorer

0 unknown. No assumption to state.

## Approaches Considered

1. **Run Opus + protocol as 20.3 promised.** Rejected: three Opus arms to re-measure a cell that
   has a published reading taken with the same instrument on the same seed. This is the error 20.1
   was written to prevent — pricing a round before authorising it — applied to a round whose price
   is entirely waste.
2. **Amend the claim and run nothing.** Rejected, and this is the interesting rejection. Writing
   *"the Opus + protocol cell exists and reads 2/3"* into 20.3 completes three cells of a 2×2 and
   leaves the fourth empty, which makes the hole **more** conspicuous, not less. An amendment that
   draws the grid is an argument for filling it.
3. **Three Sonnet arms, no protocol. Selected.** Completes the factorial. The cheap cell. Answers
   the question 20.3 could not, and answers it against a comparator already paid for.
4. **Add a second mutation to raise the observation count** (20.6 Q4). Adopted as a *secondary*
   reading, pre-registered below before any tree is touched, and reported separately from the
   single-mutation figures so it can never be mistaken for a re-score of 20.2 or 20.3.

## Selected Approach & Risks

Three arms — `q91 q92 q93` — built by 20.2's `setup.py` N branch, prompted with 20.2's
`prompt_N.txt` verbatim, run on **Sonnet**, scored by 20.2's `mutate.py` and `score.py`.

### 🎯 Drift
Drifting here means answering a different question than *does the protocol or the tier produce the
test*. Two specific forms: scoring these arms with any rubric the four published cells were not
scored with, and reading the cost column across rounds as though it were within-round.

### ✅ Validation
- `03b_delta.txt` — each new arm's tree at its own setup commit compared by **git blob hash**
  against 20.2's N arms and 20.3's O arms. Same condition means byte-identical seed or the
  comparison is not a comparison.
- Mutation applied, suite run, `server/store.js` restored, `git status --porcelain` identical
  before and after on every arm.
- Every per-arm SQL edit read out of **that arm's own** `server/store.js`. 20.3 caught this as an
  inherited-table defect; it is now a standing check, not a lesson.

### 🔄 Pivot
`obstacleThreshold` for this round is 2. If two arms fail to deliver the scoreboard at all, the
teeth metric has no occasion and the round stops rather than reporting 0/3 as though it were a
choice not to test.

## Verification Plan

Each metric is read by naming the arm at each end of it (19.4), and each is classified as
mechanism / null / ceiling / under-powered (14.14) rather than as a pass or a fail.
