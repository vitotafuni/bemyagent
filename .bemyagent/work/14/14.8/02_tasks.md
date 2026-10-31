**Delivers:** an answer to the draft's own unanswered question — can an agent produce a
structural generator that actually works, or is the whole candidate resting on an assumption.

## Design

Three arms, one condition, the `## Inventory command` clause. No baseline: the shipped protocol
produces no command, so its score on all three criteria is zero by construction and spending
arms to confirm it would be theatre.

**Task, identical to the previous rounds** so the bootstrap it triggers is comparable:

> Add a scoreboard: show how many games X and O have won, above the board.

The feature is the vehicle. What is measured is the `03-code-map.md` the bootstrap produces.

**Fixture prepared so a wrong answer exists:** `node_modules` installed after the initial commit
(present, untracked) and no `.gitignore`. Confirmed by measurement before launch, not assumed.

## Metrics, fixed before launch, all executed

**(i) RUNS.** Execute the named command in the arm's own tree. Non-zero exit or no command named
is a fail.

**(ii) CORRECT FILE SET.** Diff the paths it emits against `git ls-files`.
- **Recall below 100%** → the generator silently misses files. This is the main harm the draft
  names, because a derived artifact is trusted.
- **Precision wrecked by `node_modules`** → the naive failure the fixture was built to expose.
- Both reported as counts, not as a verdict adjective.

**(iii) RE-RUNNABLE WITH NO CONTEXT.** Run the command string alone in a fresh copy of the
fixture. Same file set or not. An absolute path, a transient file or a shell alias fails here.

**(iv) DOES IT CLAIM MORE THAN IT DERIVES.** Did the arm present hand-written rows as output of
the command? The draft's structural weakness is that derived artifacts carry unearned authority;
this is its cheapest observable form.

**Reading, fixed now:**
- **3/3 on (i), (ii) and (iii)** → the generator question is answered yes on a JS repo and round
  two is the one that matters: does an agent run it and catch a planted drift.
- **Any arm failing (ii) on recall** → the harm the draft predicted is real at round one, and
  the clause needs the `git ls-files` cross-check written into it before anything proceeds.
- **A ceiling, all three naming the same obvious command** → say so plainly; the answer is that
  this is easy on a single-language repo and the open case is polyglot.

## CDM

**🎯 Drift** — scoring the prose of `03-code-map.md` instead of running what it names. Every
criterion here is a command I execute.

**✅ Validation** — the delta is confined to the template block, confirmed by `diff`; the fixture
premise is confirmed by running both the naive and the correct enumeration before launch; 3/3
arms produce `03-code-map.md`; raw outputs and counts copied here before the verdict.

**🔄 Pivot** — if no arm names a command at all, the round is about compliance rather than
quality and the clause failed at the forced-artifact step, which would be the first time in this
repo's record. Report that instead of scoring an empty set.

## Checklist

- [ ] todo — sweep stray listeners
- [ ] todo — build the treatment protocol, confirm the delta is confined to the template block
- [ ] todo — build 3 arms with `node_modules` present and untracked, no `.gitignore`
- [ ] todo — verify the premise: naive enumeration and `git ls-files` must diverge
- [ ] todo — launch in parallel, prompt verbatim from the previous rounds
- [ ] todo — score (i) to (iv) by execution; copy raw outputs here
- [ ] todo — write `04_verify.md` against the three fixed readings
