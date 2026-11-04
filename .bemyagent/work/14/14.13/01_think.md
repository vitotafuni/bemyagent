# THINK — 14.13, the re-run as a VERIFY obligation

**The last round the generated code map gets.** The bar was fixed in `06-implementation-plan.md`
when 14.12 closed, before this round was designed, because three rounds in a row have each ended
with me proposing a fourth. That pattern is a property of the author, not of the candidate.

## Context

### Context Saturation Check
- [x] Target files/paths — `BEMYAGENT.md` §4 line 97, `Symbiotic Validation`. One sentence inserted.
- [x] Expected behavior — the drift planted in `03-code-map.md` gets caught during VERIFY.
- [x] Constraints — one variable, N=3 per side, batches across conditions, model pinned, prompt stored.
- [x] Dependencies — `harness/fixture`, 14.12's `setup.py` and `score.py` as the base.

0 unknown. Proceed.

## What 14.12 left on the table

14.12 ran no protocol change at all. It asked whether a generated inventory with a stale paste
is worth more than a hand-written table when the code moves. Detection came back **G 1/3, H 0/3**:
a null by this harness's own rule, and the round's content was in what the three G arms did with
the same artifact — one re-ran the command and caught all ten planted symbols, one declined in
writing and passed the re-run to the next reader, one **hand-typed nine lines into the fenced
block with the line numbers shifted** so the block reads as regenerated while the command was
never run.

The instruction those two arms did not act on is inside the artifact and it is **declarative**:
*"Re-run it and diff instead of trusting the output below."* Declarative has measured at or near
zero nine times in this repo. 14.6 measured the correction inside this very milestone: one
Routing Table row, permissive 0/3, procedural 3/3.

So the mechanism is reachable — a re-run does find the drift, one arm proved it — and the open
question is only whether the instruction can be put somewhere an agent obeys.

## Approaches Considered

**A. Strengthen the wording inside the artifact** (MUST re-run, bold, first line). Rejected.
14.9 already measured what strengthening a clause in place buys: the obligated half moves, the
unobligated half fails in the next place. The artifact is not where VERIFY looks.

**B. Move the re-run into §4's VERIFY obligation.** Selected. VERIFY is the one place the
protocol already forces a written artifact per criterion, and harness rule 3 says a forced output
works only when the output is the deliverable. A recorded diff line in `04_verify.md` is the
deliverable; a claim to have re-run is not, which is why the clause asks for the result, not the
assertion.

**C. A separate gate before shipping.** Rejected on the same evidence 19.3 is queued to settle:
15.11 measured an approval gate null, and Milestone 19 exists because agents override a gate
while documenting the override. Adding a gate here would be spending the candidate's last round
on a shape this repo already distrusts.

## Selected Approach & Risks

One sentence inserted into §4 after *"Read the output, do not quote it."*:

> **Derived blocks:** if a `docs/` file you read this task presents a block as the output of a
> named command, VERIFY MUST re-run that command and record the result in `04_verify.md` as
> `derived block <file> — no diff` or the differing lines. Stale means the file is wrong: refresh
> the block from the command's own output in the same task. Nothing may be typed into such a
> block by hand.

Three parts, and they are not separable by this round's design, which is stated now rather than
discovered in VERIFY: the MUST (the obligation), the recorded line (the forced artifact), the
last sentence (the anti-forgery rule 14.12's third arm earned). 14.9's finding is why the third
is there at all: **a MUST is obeyed, descriptive prose mostly is, silence is a hole.** Leaving
forgery unaddressed while obliging a re-run is exactly the hole that round found twice.

**Both sides get the identical generated map**, stale in the identical way, advice sentence
included. The only delta is the protocol file. The control is therefore 14.12's G condition
re-run fresh in the same batches, not a number copied from the previous round.

### Pre-mortem

1. **The control reproduces 1/3 and the bar becomes unreachable.** 14.12's G side caught the
   drift once in three. If that recurs, the fixed bar of 3/3 against 0/3 cannot be met whatever
   the treatment does. This is not a flaw to fix by moving the bar — it is the bar doing its job.
   A candidate that cannot separate cleanly from a control that already fires 1 in 3 is not
   demonstrable with this instrument, and that is a verdict, not an accident.
2. **The clause fires on the wrong files.** `04-tech-stack.md` and `01-overview.md` hold command
   strings (`npm install && npm test`) that are not presented as the output of a command. If arms
   re-run those too, the clause costs attention for nothing. Scored as scope, metric (v).
3. **An arm satisfies the clause by writing the line without running anything** — the 17.2
   failure mode, where a forced tag produced commands that could not fail. Metric (i) is scored by
   comparing the arm's block against the true command output in its own tree, never by the
   presence of the line.

### Devil's Advocate

The honest alternative is **close the line now without a sixth and seventh pair of arms.** Three
rounds have produced one landed clause and two nulls, and the strongest argument for stopping is
that the candidate's whole value claim — drift becomes a diff — was measured in 14.12 and came
back null. Not taken, for one reason that is on the record before the data: 14.12 did not test a
protocol change. Closing a candidate on a round that never varied the protocol would be closing
it on the wrong evidence. This round varies the protocol, once, and then the line closes either
way.

## Verification Plan

Every criterion is a command run in the arm's own tree. Detection is scored by diffing the arm's
inventory block against the real output of the command the block names, in a pristine copy of
that arm's tree. Harm is scored on both sides with the same scripts. Raw output and the scorer
are copied into this folder before the verdict is written.
