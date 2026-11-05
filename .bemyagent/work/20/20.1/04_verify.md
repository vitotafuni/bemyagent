# VERIFY — 20.1

| Criterion (fixed in `02_tasks.md`) | Result | Evidence |
|---|---|---|
| Delta confined to the intended places in `harness/README.md` | PASS | `diff` against the pre-edit copy: one hunk |
| `BEMYAGENT.md` unchanged | PASS | `git diff --stat` empty; no tag due |
| The figures in the text match the script | PASS | `cost.py` and `cost_output.txt` in this folder; 653,510 per agent, 77,767,714 weighted |
| Script and output copied here before the verdict | PASS | both present |

## What landed

**A round now has a price.** ≈ 653 k weighted tokens per agent over 119 transcripts, cache read
93% of the raw total, and the distinction that makes the number useful: **an arm is not an
agent.** Most arms spawn a second for §4's independent VERIFY, so six arms is about twelve
agents and ≈ 7.8 M. The README states the other half beside it — that the day those figures come
from changed zero lines of the distributable — because a cost without an outcome reads as a
budget.

**The arm tier is a recorded choice** with its reason, the evidence that weakened it, and three
conditions for changing it. Two things are marked as not changing: the explicit pin, and the
verifier agent arms spawn, which is where they have repeatedly found real defects in their own
work.

**The pause is in `05` with its arithmetic**: `BEMYAGENT.md` untouched since 2026-10-27, 24
commits since, external inputs exhausted, and every recent candidate traceable to one of my own
earlier rounds.

## Caveats

1. **The figures rot.** Token accounting and pricing change, and the weights are ratios rather
   than prices. Recorded with the method, the date and the script so a reader re-runs rather than
   trusts.
2. **One session, one project.** 119 transcripts from one day of one repository. It is an order
   of magnitude, not a constant.
3. **The tier is recorded, not changed.** Nothing in this task runs an arm, so the claim that a
   cheaper tier would cost less *in practice* is untested — a cheaper arm may need more turns.
   The README says to read that off `cost.py` after the first round that uses one.
4. **This task is the thing it describes.** It writes down what was only in a conversation,
   which is the failure 15.4 had just finished measuring from six arms. Worth noting that the
   fix here was free and the measurement was not.
