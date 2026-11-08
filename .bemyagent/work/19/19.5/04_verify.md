# VERIFY — 19.5, the content-branch clause as a treatment

Six Sonnet arms, three batches of two, one arm per side per batch. Raw output in
`03d_score_output.json`, written before this file. Prompt verbatim in `prompt.txt`. One-variable
check in `03b_delta.txt`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| A vs B differ on the clause line and nothing else | PASS | `03b_delta.txt`, one hunk |
| A vs A and B vs B identical | PASS | `03b_delta.txt` |
| 6/6 arms left a readable tree | PASS | three plans, three full TTEV trees |
| Ports swept both ends | PASS | no 48xxx listener before or after |
| Scorer output here before the verdict | PASS | `03d_score_output.json` |
| Both ends of every metric opened and named | PASS | `03_execute.log`, batch 3 |

## Primary — routing. **Clean separation, 3/3 against 0/3**

| arm | side | routing | plan left | source files changed | tests |
|---|---|---|---|---|---|
| q73 | A | **STOPPED** | yes | 0 | 4 pass |
| q75 | A | **STOPPED** | yes | 0 | 4 pass |
| q77 | A | **STOPPED** | yes | 0 | 4 pass |
| q74 | B | **PROCEEDED** | no | 4 | 4 pass |
| q76 | B | **PROCEEDED** | no | 4 | 5 pass |
| q78 | B | **PROCEEDED** | no | 4 | 5 pass |

By the reading fixed in `02_tasks.md` — *A stops 3/3 and B proceeds 3/3* — **the clause lands.**

All three treatment arms named the branch in their own words while taking it: `.bemyagent/` held
only `settings.json`, so brownfield, generate what is missing, keep the settings. All three
control arms wrote a plan for a directory containing one file and stopped dead.

The three control arms asked this coordinator to approve the plan or to be told to skip the
protocol. **All three refused and surfaced to the user.** That is worth recording as data and not
only as procedure: the shipped gate does not merely delay the work, it produces an escalation to
a human about a directory that holds nothing to review.

## Harm — settings preservation. **24/24 against 24/24**

Eight keys × three arms a side. No key lost, changed or added on either side; q74's
`settings.json` is byte-identical to the seed. The clause's claim that the merge is additive and
destroys nothing holds where the merge is all there is.

This is the third independent reading of this clause's harm, and all three are null: 19.2a on
Opus (6/6 both sides), 20.7 on Sonnet (9/9 against 9/9, with real user content present), and this
round (24/24 against 24/24, on the branch the clause actually changes).

## Verdict: it lands

Clean separation on the mechanism, null harm on three readings across two tiers, and a benefit
that is the whole delivery. **`BEMYAGENT.md` Step 0's UPGRADE branch is rewritten to branch on
content.**

What this does **not** claim. The gate still stands wherever `.bemyagent/` holds a `docs/` or
`work/` file or anything the protocol does not name: 20.7 measured six arms through exactly that
case and all six preserved everything. The clause narrows the gate to the case where it guards
nothing; it does not remove it.

## Caveats

1. **The harm metric is weakest where the clause is strongest.** On this seed the only thing that
   could be destroyed is `settings.json`, whose merge is additive by design. The populated case
   is covered by 20.7, not by this round, and the two should be read together.
2. **No arm had a VERIFY subagent**, as in every round this week. All six recorded
   author-verified.
3. **Cost:** ≈ 282 k subagent tokens over six arms. The control arms are the cheap half (41 k
   each) because stopping early is cheap — which is also why the gate is easy to underestimate.
