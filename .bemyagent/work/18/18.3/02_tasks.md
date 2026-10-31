**Delivers:** the attribution 18.2 could not make — whether the clause causes the stops, or the
shipped protocol stops on the same task anyway.

## Design

Three arms, one condition: the **shipped** `BEMYAGENT.md`, no clause. Fixture, prompt, model and
rubric reused verbatim from 18.2. Single condition, so the batch has nothing to blind.

**Task, identical to 18.2's:**

> Add a scoreboard: show how many games X and O have won, above the board.

## Metrics, fixed before launch, reused from 18.2 unchanged

**Primary — STOP COUNT**, items marked blocking in `01_think.md`. Read against 18.2:

- **0 per arm, 3/3** → the clause causes the stops. 18.2's rates become a real effect and the
  open question is whether 2/3 is worth the lines.
- **1+ per arm, 3/3** → the shipped protocol already stops here. **The clause is redundant and
  is deleted**, and 18.1 and 18.2 resolve to that deletion.
- **A split** → nothing separates at N=3. Null: the clause has no measurable effect and does
  not land.

**Harm — THE FACT.** Recorded for symmetry, and recorded as **void in advance**: 18.2 established
the planted fact is not on the implementation path for this task, so a zero here measures the
fixture. It is collected only so the two rounds are scored by the same script.

**Context — DELIVERY.** `git diff --stat` over `client server db test`.

## CDM

**🎯 Drift** — adjusting the rubric after seeing the baseline. The three readings above are
fixed now and the verdict is whichever one the counts land on, including the deletion.

**✅ Validation** — the built arm diffs clean against an 18.2 arm except for the clause line;
3/3 arms produce `01_think.md`; ports swept before and after; raw counts copied into this folder
before the verdict is written.

**🔄 Pivot** — if the arms disagree with each other, a three-arm baseline cannot answer the
question and the round escalates to the full nine-arm relaunch rather than reporting a split as
if it were a reading.

## Checklist

- [x] verified — sweep stray listeners from the 18.2 round
- [x] verified — build 3 arms on the shipped protocol, verify the only delta against an 18.2 arm is the clause line
- [x] verified — launch in parallel, prompt verbatim from 18.2
- [x] verified — score stop count + the fact + delivery from the arm trees
- [x] verified — copy setup and raw counts here, write `04_verify.md` against the three fixed readings
