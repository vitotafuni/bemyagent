# VERIFY — 14.9, does the revised inventory clause buy completeness, and at what price

Every criterion executed: each command run in its own arm's tree, re-run in a pristine copy, and
the pasted inventory counted from the file. Raw table in `03c_arm_evidence.txt`, commands in
`commands.json`, scorer in `score.py`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| Cross-side delta is one sentence | PASS | `03b_delta.diff` — two lines against shipped, one line across sides |
| Fixture premise re-measured in a built arm | PASS | 12 tracked, 239 `.js` on disk, 8 source files, vendor untracked, no `.gitignore` |
| 6/6 arms produce the section | PASS | after the void batch; all six hold `## Inventory` |
| Raw outputs here before the verdict | PASS | `03c_arm_evidence.txt`, `score.py`, `commands.json` |

## The result against the three readings fixed before launch

The pre-registered readings were: clean separation in recall → that wording lands; both sides
complete → the shorter wording lands; both sides short → the candidate is rejected.

**The second reading is the one that happened.** Recall is complete in 4 of the 5 computable
arms, 2/3 on each side, against 14.8's **0/3**. The completeness sentence sits on both sides and
it is what moved the number. **The `comm` sentence is not what bought recall, and it leaves the
round without a single trace of having been run** — zero hits across six trees.

So on its own pre-registered terms this round says: **keep the completeness sentence, drop the
check sentence.**

## What the round found that it was not looking for

**The pre-registered harm is live at 2/6.** q16 and q19, one per side, answered the completeness
requirement by deleting the extraction: `git ls-files` with perfect recall, perfect precision and
zero symbols. 14.8 produced nothing like this. The exit opened the moment the clause started
pushing on recall, which is what `01_think.md` predicted and why it was written down first. It
sits below the disqualification threshold, so neither side falls on it, but it is the price of
the fix and it is now measured rather than feared.

**A new failure the stronger form creates.** q17's command string is cut mid-quote inside its own
map, with the remainder nowhere in its tree. Writing the command and its output in one operation
destroyed the command. The instruction that makes an inventory derivable is the instruction that
can take the deriving command away, and only the stronger form can produce this.

**An unexplained 0/3 against 3/3 on pasting the output**, aligned exactly with the sides. It is
reported as an observation and not as a result: the metric was declared before launch as a
compliance reading rather than a comparison, N is 3, and no arm left evidence of running the
check that would explain the mechanism. Pre-mortem 1 named this exact case. Believing it now
would be scoring an outcome instead of a mechanism, which is harness rule 1 and the error this
repo already made once, in 18.2.

## The finding worth keeping, which is about clause-writing and not about code maps

| round | half written as MUST | half not | result |
|---|---|---|---|
| 14.8 | exclusion | completeness, **absent** | exclusion 3/3 · completeness **0/3** |
| 14.9 | exclusion + completeness | symbols, **descriptive only** | both 6/6 and 4/5 · symbols **4/6** |

**A MUST is obeyed. Descriptive prose is mostly obeyed. Silence is a hole.** Measured twice on
the same clause, and each round's fix moved the failure to the next unobligated half instead of
ending it. 17.2 found the mirror of the third level: a clause offering an explicit exit had
3/3 arms decline the exit and manufacture a command, because the exit was prose and the rest
was an obligation.

## Verdict: PASS_WITH_CAVEATS. The candidate survives a second round and still does not land

It is not rejected, and the reason is the same one that earned it round two: **every failure here
was found by executing the artifact.** The recall fix, the bare-enumeration harm, the truncated
command and the paste split are all `comm`, `grep` and an exit code. No mutation harness, no
six-arm attribution table, no judgement call about whether an agent "noticed" something.

It does not land, for one reason stated plainly: **a clause whose cheapest compliant answer
destroys the artifact is not ready to ship**, whatever its recall number.

**Round three (14.10 is the polyglot case; this becomes 14.11) carries three changes, all forced
by this round's evidence:**
1. **The symbols half becomes an obligation**, in its own MUST sentence, because the table above
   says that is the only form that holds. This is the change the round exists to have found.
2. **The `comm` sentence is dropped** from the shipped wording. It bought nothing measurable on
   the pre-registered metric and left no evidence of being run. If the paste split survives
   re-testing it comes back on its own merits, measured as a comparison rather than noticed.
3. **The command is fenced separately from its output**, so writing one cannot truncate the
   other.

## Caveats

1. **Batch 1 was void** and the cause was the instrument: a launch prompt reconstructed from a
   summary instead of stored sent 2/2 arms down Step 0's approval branch and produced zero code
   maps, where 14.8's prompt produced three of three. Rebuilt clean, prompt stored in
   `prompt.txt`, rule written into `harness/README.md`.
2. **The approval for Step 0 now sits in the launch prompt**, identically for all six arms. It
   removes a variance source that has nothing to do with the clause, and it is itself a deviation
   from 14.8's conditions, so the two rounds are comparable on the artifact and not on bootstrap
   behaviour.
3. **Single-language fixture**, unchanged from 14.8 and still the main limit on everything this
   candidate claims. Four of six arms converged on a `git ls-files` loop. 14.10 is where it gets
   hard and nothing here speaks to it.
4. **Author-verified.** No second agent held only the artifacts and the criteria. The mitigation
   is that every number here is a command's output rather than a reading of prose, which is the
   weakest form of independence and is stated as such.
5. **One arm's recall is uncomputable** rather than failed. q17 is scored as a (iv) failure and
   excluded from the recall denominator, which is stated wherever the 4/5 appears.
