# VERIFY — 14.15, the derived-blocks clause as a treatment

Six Sonnet arms, three batches of two. Raw output in `03d_score_output.json`, written before this
file. Prompt verbatim in `prompt.txt`. One-variable check in `03b_delta.txt`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| A vs B differ on the §4 line in both protocol files and nothing else | PASS | `03b_delta.txt` |
| A vs A and B vs B identical | PASS | `03b_delta.txt` |
| 6/6 arms left a readable map | PASS | all six parse |
| Ports swept both ends | PASS | no 48xxx listener either side |
| Scorer output here before the verdict | PASS | `03d_score_output.json` |
| Both ends of every metric opened and named | PASS | `03_execute.log`, batch 3 — and it changed a number |

## Primary — freshness. **Null, by the reading as it was written**

| arm | side | files fresh | stale files | fabricated lines | `derived block` in VERIFY |
|---|---|---|---|---|---|
| q79 | A | 5/8 | app.js, session.js, store.js | **5** | no |
| q81 | A | **8/8** | — | 0 | no |
| q83 | A | 4/8 | app.js, index.js, session.js, store.js | 0 (5 stale) | no |
| q80 | B | 9/9 | — | 0 | yes |
| q82 | B | 8/8 | — | 0 | yes |
| q84 | B | 8/8 | — | 0 | yes |

`02_tasks.md` fixed the reading as *clean separation per arm (0/3 vs 3/3) → the clause lands*,
and *any split → null at N=3*. **The control is 1/3 fully fresh. That is a split. The verdict is
a null and the clause does not land.**

**My own pre-registration was defective, and it is being honoured as written rather than
repaired after the fact.** The metric was defined per occasion — *eight files × three arms,
24 observations a side* — and then the reading was written per arm. Those two do not say the same
thing: per occasion the round separates (A **17/24**, B **25/25**), per arm it does not. A
reading that was ambiguous before launch cannot be resolved afterwards in the direction the data
happens to favour. That is the whole function of writing it down first.

## Harm — fabrication. **Not rejected, and the direction surprised the pre-mortem**

Pre-mortem 2 predicted the clause would tempt an agent to make the block match by typing into it.
**It did not: B fabricated 0 lines in 3/3 arms.** The fabrication is on the control side —
q79 invented a `test/scoreboard.test.js` section for a file `git ls-files` cannot list, so no
command ever produced it, and lifted two of its three lines from the `test/rules.test.js`
section. That is 14.12's failure reproduced, in the arm **without** the clause.

This is the finding worth more than the verdict: **the protocol's shipped text already permits a
derived block to be written by hand**, and one arm in three did it unprompted.

## What 19.4's check changed

The scorer called any line "forged" that the command does not output, which merges fabrication
with ordinary staleness. Recovering each arm's seeded block from its own setup commit separates
them: q79's five lines were never produced by any command, q83's five are verbatim leftovers of
the seeded block under the same headings. **Fabrication A 1/3, staleness A 2/3.** The uncorrected
figure would have reported two control arms forging ten lines, and would have been wrong about
one of them. Third scorer defect this week, and the third caught by opening an arm.

## What this round does establish

1. **The treatment is at ceiling: 3/3 arms fresh, 25/25 file-observations, 0 fabricated, and
   3/3 recorded the `derived block` line in `04_verify.md`** — the forced artifact the clause
   asks for, which is the shape this repo has measured landing nine times.
2. **A control rate is a sample, not a property of a tier.** 20.5's three Sonnet controls were
   stale 3/3 on `session.js`; here, same seed and same prompt, one control is fresh 8/8. 14.14's
   finding arriving a second time, this time against a reading of my own from yesterday.
3. **The clause is not rejected.** A null at N=3 on a split control is *not enough evidence*, not
   evidence of no effect.

## Owed, if it is run again

A reading fixed unambiguously on the per-occasion metric, and enough arms that a 2/3 control does
not collapse the round. On these numbers the per-occasion gap is 17/24 against 25/25; at N=3 per
side it cannot be told from a control that varies. **That is a design cost of this round, paid
and recorded, not a result.**

## Caveats

1. **Denominators differ per arm** (8 or 9 files), because the command is re-run in the arm's own
   tree and q80 made its new test visible to `git ls-files` with `git add -N`. The fraction is
   per-file-in-its-own-command; absolute stale counts are recorded beside it.
2. **No arm had a VERIFY subagent.** All six author-verified.
3. **Cost:** ≈ 340 k subagent tokens over six arms.
