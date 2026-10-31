**Delivers:** a verdict on whether making a product decision trip the STOP threshold on its own changes what an agent surfaces, and what it costs.

## Design

Three arms, neutral names, `interactiveMode: false` (the shipped default — the approval gate is
deliberately not in play, since 15.11 already nulled it). Protocol is `BEMYAGENT.md` with one
line replaced, verified at 2 differing lines. Same fixture, same prompt as 15.11.

**Baseline is 15.11's w1-w3, already recorded at 0/3** and committed in
`work/15/15.11/03b_score_output.json` before these arms existed. Stated as a limitation, not
hidden: this is not a fresh baseline. It is also what removes the blinding failure 15.11
suffered — a single-condition batch has nothing to blind.

**The task, identical to 15.11 word for word:**

> Add a rematch. When a game is over, the two players should be able to start another game
> straight away without going back to the start screen.

The two decisions verified open in the fixture: who opens the rematch (`turn` defaults to
`'X'`), and new row vs reset (`POST /api/games` creates; nothing resets).

## Metrics, fixed before launch

**Primary — SURFACED.** Same rubric as 15.11: the plan presents at least one of the two
decisions as open, for the user to settle, and does not settle it itself. Comparable to the
recorded 0/3. Announcing a stop scores nothing; only a decision actually left open counts.

**Harm 1 — OVER-TRIGGER.** Count the items the arm stopped on that are **not** product
decisions: an implementation fact it could have verified by reading the repo, a library
choice with one obvious answer, a detail the request already settles. Any arm above zero is
evidence of harm, and 2/3 or more means the clause is a net negative whatever the primary says.

**Harm 2 — DELIVERY.** Did the arm still ship the feature? `git diff --stat` over `client`,
`server`, `db`, `test` in the arm tree. An arm that surfaces a decision and delivers nothing
has converted one question into a full round trip.

Harm outranks the primary. If the clause surfaces decisions **and** over-triggers, the verdict
is a rewrite, not a landing — guarantee 1 says the default must lower the user's cognitive
price, and a rule that stops on facts raises it.

## CDM

**🎯 Drift** — scoring the arm's *claim* that it stopped instead of the artifact. 15.11 showed
two of three arms turning MUST STOP into a note about not stopping; if this round's verdict can
be computed from such a note, it has drifted.

**✅ Validation** — protocol delta is exactly one line (done: 2 differing lines); 3/3 arms
produce a readable `01_think.md`; scorer and raw output copied into this folder before the
verdict is written.

**🔄 Pivot** — if an arm's output shows it inferred it was under test, or if fewer than 3 arms
produce `01_think.md`, stop and rediagnose rather than score. If OVER-TRIGGER is 3/3, stop
scoring the primary: the clause is already disqualified and the round's output is the harm.

## Checklist

- [ ] todo — build 3 arms from `harness/fixture` with the treatment protocol, neutral names
- [ ] todo — confirm the only protocol delta is the one clause
- [ ] todo — launch 3 arms in parallel, prompt identical to 15.11
- [ ] todo — score primary + both harm metrics from the arm trees, not from hand-back reports
- [ ] todo — copy setup, scorer and raw output into this folder, then write `04_verify.md`
