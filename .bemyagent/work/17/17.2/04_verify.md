# VERIFY — 17.2, the harm arm

Primary measure executed, not read: every command an arm named was run against a tree where the
change had been broken. Raw exit codes in `03c_arm_evidence.txt`; scripts in `mutate.py` and
`score_tags.py`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| One-line delta | PASS | `03b_delta.diff`, line 92 only |
| 3/3 arms produce `02_tasks.md` | PASS | all three present, with 5 or 6 tags each |
| The mutation actually breaks the behaviour before any command runs | **PARTIAL** | M1 leaves the X and O numbers intact where an arm zero-fills a fixed key set, so it tests assertion style as much as detection. Declared, and M2 added rather than substituted |
| Raw per-arm command lists and red/green results in this folder before the verdict | PASS | `03c_arm_evidence.txt` |

The CDM's pivot clause covers exactly the M1 weakness: *re-cut the mutation rather than reporting
noise*. It was re-cut by **adding** a second mutation and reporting both, not by replacing the
pre-registered one after seeing its result.

## Primary metric — the tag does not improve detection

Arms whose suite goes red when the change is broken: **treatment 2/3, baseline 1/3.** Not
separation at N=3, so by this repo's own rule it is a null. The tag buys no detection.

Worth recording beside it, because it points the other way and does not rescue the tag:
**3/3 treatment arms wrote a test over the new path against 1/3 baseline**, and two baseline arms
shipped on `npm test` at 4 pass — a suite covering `rules.js` alone and nothing they had written.
Writing a test and writing a test that discriminates are different things, and the execution
measure is what separates them: q10 wrote five new tests and caught neither mutation.

## The pre-registered harm did not occur

The predicted mechanism was a **collapse**: one command per criterion, so arms converge on one
cheap command where the baseline ran several kinds. **Measured false.** Treatment arms named 5 or
6 commands against the baseline's 1 or 2. Recorded as a null on its own terms.

## The harm that did occur, found by executing rather than reading

**9 of the 14 distinct commands the tag produced never go red under either mutation**: 7 of 7
greps and 2 of 2 `node -e` one-liners. A grep matches a string that is there whether or not the
code behind it is correct. Both one-liners print a verdict and exit 0 whatever they printed.

The clause under test ends *"A criterion no single command can decide names none."* The criteria
that produced those greps — the scoreboard sits above the board, the client refetches after a win
— are precisely those. **3/3 arms declined the exit and manufactured a command instead.**

So the tag does not make agents pick a weaker test. It makes them **attach a command to criteria
that no command can decide**, and the command they invent is one that cannot fail. The artifact
is forced and well-formed; what it certifies is nothing. This repo's rule 3 says a forced output
only works when the output *is* the deliverable, and a claim about the work is free. **A command
that cannot fail is a claim about the work wearing a shell prompt.**

## Consequence for the rejected exit-code clause

`EXIT_CODE: 0 → PASS` was rejected in the triage on argument. Under it, each of those 9 commands
forces a PASS against a broken implementation, carrying a citation and a green exit code. The
draft predicted *"a PASS with a valid citation, a green exit code and zero information about the
change."* That prediction is now measured rather than reasoned.

## Verdict

**Reject `[RUNTIME_CHECK: <command>]` in the per-criterion form. 17.1 is dropped.**

17.1 would have measured command quality as the benefit. This round measured it: 2/3 against
1/3, a null, with a 3/3 inflation of non-falsifiable evidence alongside. There is nothing left
for a benefit arm to find that this one has not already priced.

What is rejected is precise, and the distinction matters for anyone reading this as a critique of
the idea: the **per-criterion** form, which is the draft's own revision of hunk B and the form
open question 1 argued for. The author's weaker per-task form is untested and would have to earn
its own round; the mechanism found here predicts it inflates less because it asks for one command
where a command plausibly exists, and buys correspondingly less.

**Status of the whole DRT line: closed.** The diagnosis behind it stays confirmed and is already
in the record. Every proposed remedy has now been either rejected on mechanism or measured.

## Caveats

1. **The harm found was not the harm predicted.** It emerged from the execution measure rather
   than from a pre-registered hypothesis, so it is one round old. It is clean at 3/3 and the
   mechanism is legible, which is why it carries the verdict, but a candidate rule built *on* it
   would need its own round rather than inheriting this one.
2. **Baseline reused from 18.3**, not run beside the treatment arms. Same fixture, prompt, model,
   rubric; one day later.
3. **M1 was weaker than intended**, stated above and in the evidence file.
4. **`node_modules` absent from the fixture**, the 15.11 residue. All six arms installed it
   themselves.
