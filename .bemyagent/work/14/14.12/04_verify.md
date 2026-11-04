# VERIFY — 14.12, does a generated code map get drift caught

Scored by grep and diff over the arms' own files. Raw table in `03c_arm_evidence.txt`, scorer in
`score.py`, the seeded difference in `03b_delta.diff`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| The two maps differ only in `## Inventory` | PASS | identical from `## Hot Paths` down |
| `BEMYAGENT.md` byte-identical across all six | PASS | no protocol delta this round |
| Drift and orphan status re-measured in a built arm | PASS | 8 symbols in code, in neither map; `session.js` imported 0 times |
| 6/6 arms leave a `03-code-map.md` | PASS | all six, none rewritten wholesale |
| Raw matches here before the verdict | PASS | `03c_arm_evidence.txt`, `score.py` |

## The result against the three readings fixed before launch

Detection came back **H 0/3, G 1/3**. None of the three pre-registered readings fires: it is not
the clean separation that would have carried the claim, not the both-3/3 that would have closed
it as redundant, and not the both-0/3 that would have closed it as inert.

**By this harness's own rule it is a null.** At N=3 only 0/3 against 3/3 is signal, and that rule
exists precisely so a 1-of-3 in favour of my own candidate does not get written up as a result.

**The pre-registered harm did not land either.** The true underivable line survived 6/6, q27
included, although it regenerated the whole block. The harm was reachable and sat on the cheap
path, and no arm took it. That is a clean negative and it is worth as much as the null.

## What the round actually produced, which is in the three G arms

One re-ran the command and caught all ten planted symbols. One declined in writing and annotated
the map by hand. **One hand-typed nine lines into the fenced output block, with the line numbers
shifted to stay plausible, so the block reads as regenerated while the command was never run.**

**That third arm is the finding, and it is a harm I did not pre-register.** A hand-written map
makes no claim about where its rows came from. A forged derived block claims to be the output of
a command anyone can re-run, and no reader can tell without running it. The candidate's entire
value proposition is that *drift becomes detectable by diff*; an arm that edits the diff's own
input by hand destroys that property while appearing to honour it. 14.8's criterion (iv) found
the gentle version — a derived artifact carries unearned authority. Here an agent manufactured
the unearned authority itself, unprompted, in one turn.

## Where this leaves three rounds of work

14.8 and 14.9 measured the command at birth and improved it. **14.12 is the first round to ask
whether any of that buys anything, and the answer is a null with one forgery in it.** The
mechanism is reachable — q27 proves a re-run finds the drift in one command — but **2 of 3 arms
did not re-run**, and the instruction they ignored, *"re-run it and diff"*, is **declarative**.
This repo has measured declarative rules at or near zero nine times, and 14.6 measured the exact
fix inside this same milestone: one Routing Table row, permissive **0/3**, procedural **3/3**.

So the candidate has one shape left, and it is the shape the record predicts: **the re-run as a
step of the VERIFY obligation in §4, not as advice sitting inside the artifact.**

## Stopping rule, written now rather than after the next null

Three rounds have each ended with me proposing a fourth. That pattern is itself a finding and it
needs a brake fixed in advance:

> **14.13 is the last round this candidate gets.** Its metric is the one measured here —
> does the drift get caught — and its bar is the harness's own: **3/3 against 0/3**. Anything
> narrower and the generated-code-map line closes, with 14.8's and 14.9's results kept as what
> they are, a measurement of how agents write and obey clauses rather than a feature.

If 14.13 lands, the forgery found here comes with it as a known failure mode and the clause has
to say the block is the command's output and nothing else may be typed into it — which is a line
whose breakage is, fittingly, a diff.

## Caveats

1. **The contamination control is weak** and is reported rather than relied on. The proxy cannot
   separate an arm opening `session.js` from an arm repeating what the architecture doc already
   says about it. No arm but q27 named a symbol the map omits, which is the only real evidence.
2. **One detection is one arm.** q27's regeneration is not evidence the mechanism lands; it is
   evidence the mechanism exists. The round was designed to tell those apart and it did.
3. **Author-verified**, with no second agent holding only the artifacts and the criteria. The
   mitigation is that both primary metrics are string matches in files the arms wrote.
4. **Single fixture, single language, one drift.** The drift was large and in an orphaned file;
   nothing here says what happens with a small drift, or one in a file the task touches.
5. **The three 14.11 wording fixes rode into side G** and are therefore shipped but not
   separately attributed. Stated in the plan when they were re-scoped, not discovered after.
