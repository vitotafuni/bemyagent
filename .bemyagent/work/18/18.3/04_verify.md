# VERIFY — 18.3, the baseline arm

Scored from the arm trees. Raw figures and the nine-arm attribution table in
`03b_arm_evidence.txt`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| Built arm diffs clean against an 18.2 arm except the clause line | PASS | `diff -r` → line 91 only |
| 3/3 arms produce `01_think.md` | PASS | 34 / 59 / 40 lines |
| Ports swept before and after | PASS | no fixture listener in 3xxx before launch; none left after |
| Raw counts in this folder before the verdict | PASS | `03b_arm_evidence.txt`, `setup.py` |

## The reading

`02_tasks.md` fixed three readings before launch. The baseline came back **0 blocking items in
3/3 arms, 3/3 shipped**, which is the first: *the clause causes the stops.* It does. The baseline
is at the floor on this task, as it was on 15.11's.

That settles attribution and immediately raises the question the reading named: **is the rate
worth the lines.** Re-scoring all nine arms together on the checkbox count answers it, and
changes one of 18.2's numbers.

## Correction to 18.2

18.2 recorded ownership 2/3 and reversibility 1/3 and compared them as two effects. The shipped
rule is *2+ unchecked → STOP; 0-1 → state the assumption and continue*, so a stop is attributable
to the clause only where the arm stopped with **0 or 1** unchecked. q5 stopped with **two**, and
its own text names the shipped rule first. **Under the shipped protocol q5 stops anyway.**

| condition | attributable stops | shipped |
|---|---|---|
| baseline | 0/3 | 3/3 |
| ownership | 2/3 | 1/3 |
| reversibility | **0/3** | 2/3 |

**The reversibility wording is a null.** It caused nothing. That is the wording three independent
routes pointed at — the arms' own rewriting in 18.1, guarantee 4, and the approval-gate
literature — and measured flat. Deleted as a candidate.

## Verdict on the ownership wording: it works, and it still does not land

It causes stops the baseline never makes, 2/3, and it never enumerates. The reason to reject it
is not an absence of evidence this time.

**The baseline does not hide the decision.** 3/3 baseline arms named the scope question
explicitly in `01_think.md`, carried it as a stated assumption, and raised it unprompted in the
hand-back under their own heading. q8 went further and named the reversal: *"if that is what was
wanted, the fix is a filter on the same query."* The clause was added to surface a product
decision. **The shipped 0-1 rule already surfaces it.**

So what the clause buys is **ordering, not visibility**: the question arrives before the code
instead of beside it. What it costs is the delivery, 3/3 down to 1/3. And the decision it stops
for is reversible by one `WHERE` clause in one query — stated independently by arms on all three
conditions.

**A rule that converts two of three working deliveries into a question the other arms were
already asking, about a choice that costs one line to reverse, fails guarantee 1.** The default
must buy the best outcome at the lowest cognitive price; this one raises the price and the
outcome was already there.

**Both wordings rejected. Nothing lands from Milestone 18.** 18.1's clean 3/3 stands as what it
was called at the time: a mechanism demonstration, not a licence.

## What survives, and it is not a rule

The question Milestone 18 was built on came from 15.11's null — the approval gate could not
surface a decision because the Saturation Check had already told the agent to assume it. Three
rounds later the answer is that **the Check's 0-1 branch is not the problem**. Arms that take it
state the assumption, record it, and raise it. The protocol's existing machinery was doing the
job the whole time, and two rounds of candidates measured either harmful to delivery or flat.

The open question left is narrow and honest: this task's decision was cheap to undo. **Nothing
here tests a decision that is genuinely expensive to undo**, because no arm needed one. That is
not a reason to keep the clause; it is the one condition under which a future candidate could
earn its lines, and it needs a fixture where the cheapest correct implementation forces a schema
or interface choice. Recorded in the plan, not scheduled.

## Caveats

1. **The baseline ran after the treatment arms**, not beside them. Same fixture, prompt, model,
   rubric and day. Stated rather than argued away; a nine-arm single batch is strictly better.
2. **`node_modules` absent** from the fixture, the residue of 15.11. All three baseline arms ran
   `npm install` themselves and all three flagged the missing `.gitignore`.
3. **Single-condition batch**, so there was nothing to blind, as in 18.1.
