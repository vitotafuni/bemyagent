**Delivers:** a verdict on the revised inventory clause — does completeness arrive because the
clause *states* it, or only because the clause *names the check that detects its absence* — and
whether buying completeness costs the map its symbols.

## Design

Six arms, neutral names, `interactiveMode: false`, model pinned. One variable: **one sentence**,
the `comm` cross-check. Both sides carry the completeness statement and the paste instruction.

- **side S** — statement only (q16, q18, q20)
- **side C** — statement + the check named (q17, q19, q21)

Protocol delta per side confined to the `03-code-map.md` template block; cross-side `diff` must
be the one sentence and nothing else. Confirmed before launch.

**Task, identical to 14.8 and to the three rounds before it:**

> Add a scoreboard: show how many games X and O have won, above the board.

The feature is the vehicle. What is measured is the `03-code-map.md` the bootstrap produces.

**Fixture premise, re-measured in the built arm and not assumed:** `node_modules` installed
after the initial commit (present, untracked), no `.gitignore`, so a naive enumeration is ~20x
wrong and the precision criterion is not at a ceiling.

## Metrics, fixed before launch, every one executed

**(i) RUNS.** Execute the named command in the arm's own tree. Non-zero exit, or no command
named, is a fail.

**(ii) RECALL — the primary metric.** The paths the command emits against the tracked source set
(`.js`, `.sql`, `.html` — the same 8 files 14.8 scored, so the two rounds are comparable).
Reported as a count of missing files, not as an adjective.
- **Side at 3/3 complete against the other at 0-1/3** → clean separation, that wording lands.
- **Both sides 3/3** → the statement carries it; the shorter wording lands and the check sentence
  is dropped as unearned tokens.
- **Both sides below 3/3** → the clause cannot buy completeness in either shape. The candidate is
  **rejected** after two rounds, and the Devil's Advocate in `01_think.md` is what survives.

**(iii) PRECISION.** Any `node_modules` path in the output. The 14.8 trap, carried forward.

**(iv) RE-RUNNABLE WITH NO CONTEXT.** The command string alone, in a pristine copy. Same file
set or not. An absolute path, a transient file or a shell alias fails here.

**(v) HARM — SYMBOL YIELD.** Pre-registered in `01_think.md`, and reachable by construction: the
cheapest way to guarantee recall is to delete the grep. Of the tracked source files the command
emits, how many carry at least one symbol line? A command that emits paths and nothing else
scores 0 and has bought recall by destroying the artifact.
**2 of 3 arms on a side emitting no symbols for a majority of files disqualifies that side on its
own, whatever its recall.**

**(vi) IS THE INVENTORY THE OUTPUT.** Does the section hold rows the command does not emit?
14.8 measured this at **3/3 YES** with no instruction present. Both sides now carry the paste
instruction, so this is a 6-arm compliance reading, not a between-sides comparison.

## CDM

**🎯 Drift** — scoring the prose of `03-code-map.md` instead of running what it names. Every
criterion here is a command executed in the arm's tree. An arm claiming "verified complete"
while its command drops a file counts as dropping a file.

**✅ Validation** — cross-side `diff` is exactly one sentence; the fixture premise re-measured in
a built arm before launch; 6/6 arms produce `03-code-map.md` with the section; raw command
output, per-arm file sets and symbol counts copied into this folder **before** the verdict.

**🔄 Pivot** — if side C's arms paste the `comm` line into the map without running it and recall
is unchanged, stop comparing wordings: the finding is that naming a check is not running one, and
that outranks the recall question. If an arm shows it inferred it was under test, void that arm
and say so rather than scoring it.

## Checklist

- [x] verified — sweep stray listeners before launch
- [x] verified — build both protocol variants, confirm the cross-side delta is one sentence
- [x] verified — build 6 arms, neutral names, 3 per side, model pinned
- [x] verified — re-measure the fixture premise inside a built arm
- [x] verified — launch in parallel, prompt verbatim from 14.8
- [x] verified — score (i) to (vi) by execution; copy raw outputs here
- [x] verified — sweep stray listeners after the arms finish
- [x] verified — write `04_verify.md` against the three fixed readings
