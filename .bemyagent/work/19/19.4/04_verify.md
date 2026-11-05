# VERIFY — 19.4

| Criterion (fixed in `02_tasks.md`) | Result | Evidence |
|---|---|---|
| One insertion, no other edit | PASS | `diff` against the pre-edit copy: one hunk |
| `BEMYAGENT.md` untouched, no tag due | PASS | `git diff --stat` empty, and empty against `3.3.0` |
| The rule demands a fact, not an assertion | PASS | it requires the arms to be **named**, at each end of the metric |

## What landed

Before a metric's number goes into a verdict, the arm at each end of that metric gets opened and
the score confirmed against what the arm did, recorded in `04_verify.md` as one line per metric
naming those arms. The four defects from 14.13, 19.3, 19.2a and 19.2b are in the text as a
table, with what each would have reported, because the rule has to carry its own evidence or it
reads as caution.

The text also says plainly what the failure is **not**: three of the four ran against the arms
and one toward the candidate, so this is not a rule about watching for bias in your own favour.
A scorer is an instrument built by the person who wants an answer, and nothing here checked it.

## Caveats

1. **This rule has not been measured**, and that is uncomfortable in this repo. It is in
   `harness/README.md`, not in `BEMYAGENT.md`, so it binds the measuring apparatus rather than
   shipping to users — a lower bar than a protocol clause and stated as such. The first round to
   run under it is the test, and 15.4 is next.
2. **Naming arms can be faked.** An agent could write two arm names without opening them. That
   is a lie rather than a gap, and no rule in this file prevents a lie; what the rule removes is
   the case where nobody looked and nobody noticed.
3. **It cannot catch a defect that scores both ends the same way.** A metric wrong in the middle
   of its range survives this check. The independent re-score named in the rule is the remedy
   where a verdict rests on one metric, and it is deliberately not the default, because doubling
   the cost of every round to catch a case none of the four defects took is the wrong trade.
