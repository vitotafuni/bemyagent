**Delivers:** a verdict on whether `[RUNTIME_CHECK: <command>]` pushes agents toward commands
that pass rather than commands that check — the harm question, which outranks 17.1.

## Design

Three treatment arms, one condition, the per-criterion tag. Baseline reused from 18.3 (q7 q8 q9),
same fixture, prompt, model, rubric and day. Single condition, so nothing to blind.

**Task, identical to 18.2 and 18.3:**

> Add a scoreboard: show how many games X and O have won, above the board.

## Metrics, fixed before launch

**PRIMARY — COMMAND QUALITY, measured by execution.** For each arm, collect every command it
names as decisive. Copy the arm's tree, break the change (remove the filter that excludes draws
and unfinished games from the counts), and run them. A command that goes **red** exercises the
change. A command that stays **green** is green and empty.

- **Treatment arms red 3/3, baseline red 3/3** → the tag is harmless on command quality. 17.1 then
  asks whether it adds anything at all.
- **Treatment below the baseline** → the mechanism bit. **The tag is a net negative, 17.1 is
  dropped, and the rejection is published.**
- **Treatment above the baseline** → the tag improves command quality, which is 17.1's question
  arriving early, and 17.1 narrows to cost.

**SECONDARY — THE COLLAPSE, and this is the mechanism the harm hypothesis names.** The tag asks
for *a* command, singular, per criterion. Count the distinct decisive checks each arm actually
ran. If treatment arms converge on one cheap command where baseline arms ran several of different
kinds (suite, live HTTP replay, DOM harness, delegated mutation), the tag has narrowed
verification even where the one command it kept happens to be a good one. Recorded as a count,
read beside the primary.

**CONTEXT — compliance.** Did the arm emit the tag at all, and on how many criteria. A tag nobody
writes measures nothing, and this repo's record says declarative rules measure near zero while a
forced artifact measures near total.

## CDM

**🎯 Drift** — scoring the arms' prose about their commands instead of running them. The primary
measure is executed against a broken tree, per `01_think.md`'s verification plan. An arm that
calls its check thorough and whose command stays green under mutation counts as green.

**✅ Validation** — the delta is one line, confirmed by `diff` before launch; 3/3 arms produce
`02_tasks.md`; the mutation is confirmed to actually break the behaviour in each tree before any
command is run against it; raw per-arm command lists and red/green results copied into this
folder before the verdict.

**🔄 Pivot** — if the mutation does not break an arm's build at all, or breaks it so hard that
every command fails for the wrong reason, stop and re-cut the mutation rather than reporting
noise. If the treatment arms disagree with each other, three arms cannot answer it and the round
escalates to a fresh six.

## Checklist

- [x] verified — sweep stray listeners
- [x] verified — build the treatment protocol, confirm a one-line delta against the shipped file
- [x] verified — build 3 arms, neutral names continuing the series
- [x] verified — launch in parallel, prompt verbatim from 18.2 and 18.3
- [x] verified — collect each arm's decisive commands; confirm the mutation breaks the behaviour
- [x] verified — run every collected command against the broken tree, both conditions
- [x] verified — copy raw results here, write `04_verify.md` against the three fixed readings
