## Context
- 14.8 measured the first round of the structural generator: **runs 3/3, precision 3/3, re-runnable 3/3, recall 0/3**. The cause was shared and none of the three arms noticed it: `git ls-files <globs> | xargs grep <pattern>` lets the **grep decide membership**, so a file holding no matching symbol leaves the inventory. Two arms globbed `client/index.html` explicitly and lost it anyway.
- The clause required the command to *exclude* vendor, build output and untracked files. **3/3 obeyed exactly.** It never required the command to *emit every tracked source file*. The specified half was met; the unwritten half failed everywhere. A drafting error in the candidate, not a failure of the arms.
- This round fixes the drafting error and asks the only question that follows from this repo's record.

### Context Saturation Check
- [x] **Target files/paths** — `BEMYAGENT.md` line 175, the `03-code-map.md` template block, same insertion point as 14.8
- [x] **Expected behavior** — the command's file set equals the tracked source set, and the inventory is its output
- [x] **Constraints** — harness rule 4 (harm arm); harness rule: a harm arm has to be reachable; only clean separation at N=3
- [x] **Dependencies** — none new; same fixture, same task, same model as 14.8

0 unchecked. Proceed.

## The question this round exists to answer

Not *"can the clause be fixed"* — the fix is obvious and writing it is free. The question is
which **shape** of the fix works, and this repo has measured that shape nine times:

> Milestones 11, 13, 14.3, 14.6 and 16 all found the same thing. A **declarative** rule measures
> at or near zero. A **procedural** rule, one naming an artifact or a command, measures near
> total. 14.6 is the cleanest: one Routing Table row, two phrasings, permissive **0/3** against
> procedural **3/3**.

So: does *stating* the completeness requirement buy completeness, or does the clause have to
**name the check that detects its absence**?

## The two wordings

Both carry the completeness statement and both carry the paste instruction. The **only**
cross-side difference is one sentence, confirmed by `diff` before launch.

**Side S (statement)**
```
## Inventory
`<command>` — one deterministic command that enumerates this project's source files and their
symbols, determined once from the stack. It MUST emit every tracked source file, including one
that holds no symbol it recognises, and MUST exclude vendor directories, build output and
anything untracked. What follows this line is that command's output pasted; anything you know
that it cannot derive goes in a later section, marked hand-written. Re-run it and diff instead
of trusting the paste.
```

**Side C (statement + the check named)** — the same, plus, after *"anything untracked."*:
```
Check it before pasting: `comm -13` its sorted paths against the sorted source paths from
`git ls-files`, and nothing may remain.
```

That sentence is the cross-check the draft named as the bound on this exact harm, and which
went unwritten in 14.8 and therefore unused.

## The harm, pre-registered, and why it is reachable

Forcing completeness has an obvious cheap exit: **drop the grep.** `git ls-files '*.js' '*.sql'
'*.html'` has perfect recall, perfect precision, is re-runnable from the string alone, and names
**zero symbols**. It satisfies every completeness criterion and destroys the artifact.

This is the mirror image of 14.8's failure. There, extraction ate enumeration. Here, enumeration
could eat extraction — and the stronger the clause pushes on recall, the cheaper that exit gets.

**Reachability is not assumed.** The cheapest correct implementation under the new clause *is*
the bare enumeration; the clause's own first sentence is the only thing arguing against it, and
14.8 established that arms supply exactly what a clause says and nothing it omits. The trap is
live by construction, which is what harness rule 4 requires and what 18.2b failed to have.

## Approaches Considered
**A — 3 arms, the fixed clause only.** Answers "is it fixed" and nothing else. Cheapest, and it
cannot distinguish the fix working from the clause being verbose.
**B — 6 arms, statement against statement+check.** One variable. Answers which half does the
work, which is the question the repo's record poses and the only one whose answer changes the
shipped line. **Chosen: B.**

## Selected Approach & Risks
- Estimated token cost: **medium-high** (6 arms, each bootstraps and builds)
- **Risk — both sides reach 3/3 recall.** Then the statement is enough, the check sentence buys
  nothing, and the shorter wording lands. This is a real and welcome outcome, not a null: it is
  the first time a declarative half would have carried a candidate in this repo.
- **Risk — both sides collapse to a bare file list.** Then the clause trades the harm it was
  written to fix for a worse one and the candidate is rejected after two rounds.
- **Risk — scoring my own candidate.** Same unfixable constraint as every round here: both sides
  run in one batch and hand-back reports name their directory. Mitigation is the rubric below,
  fixed before launch and computed by **executing** each command, never by reading its prose.

### Pre-mortem
1. *The `comm` sentence is copied verbatim into the map instead of run.* Then side C's recall is
   indistinguishable from side S's and the finding is that naming a check is not running it.
   Detected directly: the check leaves no artifact, so score recall by execution either way.
2. *Both sides produce the same command.* 14.8 already hit a single-language ceiling, all three
   arms choosing `git ls-files`. If it recurs, say so plainly: the answer is that this is easy on
   a one-stack repo and 14.10 is where it gets hard.
3. *An arm satisfies recall by emitting paths with no symbols.* This is the pre-registered harm,
   not a surprise; it is scored as such and disqualifies its side.

### Devil's Advocate
Drop the clause and ship the **check alone**, with no inventory command at all: *"before trusting
`03-code-map.md`, diff its file list against `git ls-files`."* That is the freshness guarantee
the whole 14.7/14.8 line is actually after, and it costs one line instead of five. Not tested
this round because it changes the deliverable rather than the wording, and because 14.8 measured
criterion (iv) at 3/3 — a map whose rows are hand-written will fail that diff forever, so the
check alone reports permanent drift and gets ignored. Recorded for 14.10 if both sides fail.

## Verification Plan
Every criterion executed in the arm's own tree, then re-run in a pristine copy. Scored from the
commands, never from the hand-back text. Signal is a clean separation in recall between sides;
absent that, the verdict is about the absolute recall and the sides are reported as equivalent.
