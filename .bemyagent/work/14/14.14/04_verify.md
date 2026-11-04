# VERIFY — 14.14

| Criterion (fixed in `02_tasks.md`) | Result | Evidence |
|---|---|---|
| Delta confined to the three intended places | PASS | `diff` against the pre-edit copy: 3 hunks, 51 lines, no fourth site |
| `BEMYAGENT.md` unchanged, no tag due | PASS | `git diff --stat` empty, and empty against `3.3.0` |
| The collapsed claim is gone, not merely qualified | PASS | `grep -c "anything narrower is noise"` → 0 |
| Scoring section re-read whole | PASS | read back in full; the three outcomes and the remedy are in one place |

## What landed

The Scoring rule now names **null**, **ceiling** and **under-powered** as different verdicts with
different consequences, in a table, with the control's rate as the thing you decide first. A null
and a ceiling both stop a rule shipping; only the ceiling also says something true about the
baseline. An under-powered round licenses nothing.

The evidence sits in the text rather than in a citation: two rounds ran the same control condition
and read 1/3 and 3/3, verified file by file. That is the sentence a future round will be arguing
with, so it belongs where the rule is, not behind a link.

Two instrument rules were added from 14.13's own near-misses. **Score the artifact against what it
claims**, because defining truth as the seeded command would have reported nine forged lines in a
control arm that had merely improved the command its map names. **Shared scratch is not isolation
either**, because arms clobber each other's capture files under generic names, and 14.13's scoring
survived that only because every criterion re-runs inside the arm's own tree.

## Caveat

Pre-mortem 1 is mitigated but not closed. The new table binds *under-powered* to the control's
rate, which is a fact decided before the data, so a treatment losing against a control at zero is
still a null and cannot be relabelled. What the text cannot prevent is a future author choosing a
question whose control sits in the middle and then calling the result unresolved. The guard
against that is the line telling you to ask about the control **before designing the arms**, and
it is advice, not a gate. The repo's own record is the honest measure of whether it holds.
