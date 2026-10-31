**Delivers:** a verdict on whether the Saturation Check clause can land — does it stop once, or does it stop on everything — and which of the two wordings to land if either.

## Design

Six arms, neutral names, `interactiveMode: false`. One variable: the clause wording.

- **side o** — ownership wording (18.1's, already measured 3/3 surfaced, 0/3 over-trigger on a one-decision task)
- **side r** — reversibility wording, taken verbatim from what 18.1's arms used in practice

Protocol delta per side must be exactly one line, confirmed by `diff` before launch.

**Task, identical for all six:**

> Add a scoreboard: show how many games X and O have won, above the board.

## Metrics, fixed before launch

**Primary — STOP COUNT.** The number of items the arm marks blocking in `01_think.md`.
This is the metric, not whether a stop occurred. Reading, per side:

- **1 per arm** → the clause ranks. Lands.
- **2 per arm** → borderline; land only if both are from the expensive row of the table in `01_think.md`.
- **3+ per arm** → the clause enumerates instead of ranking. **Rejected in that wording**, whatever 18.1 showed.

**Harm — THE FACT.** Does *"would a new column reach an existing database"*, or any equivalent
repo-checkable fact, appear among an arm's blocking items? `db/schema.sql` answers it in one
line. Any arm above zero here is stopping on something it could have read, which both wordings
explicitly exclude. **2/3 or more on a side disqualifies that wording on its own.**

**Context — DELIVERY.** Did the arm ship anything (`git diff --stat` over `client server db test`)?
Recorded, not verdict-bearing: 18.1 already established that a stop costs the delivery.

## CDM

**🎯 Drift** — scoring the arms' prose about ranking instead of counting what they actually
blocked on. The count comes from the artifact; an arm claiming it "ranked carefully" while
blocking on four items counts as four.

**✅ Validation** — one-line delta per side, verified by `diff`; 6/6 arms produce `01_think.md`;
setup, both deltas and the raw per-arm counts copied into this folder before the verdict.

**🔄 Pivot** — if both sides land at 3+, stop comparing wordings: the clause is rejected and
the output is the harm, with 18.1's template variant (a mandatory, possibly empty
`Open decisions` section) as the surviving candidate. If an arm shows it inferred it was under
test, void that arm and say so rather than scoring it.

## Checklist

- [ ] todo — build two protocol variants, confirm each is a one-line delta
- [ ] todo — build 6 arms, neutral names, 3 per side
- [ ] todo — launch in parallel, prompt identical across all six
- [ ] todo — score stop count + the fact + delivery, from the arm trees
- [ ] todo — copy setup, deltas and raw counts here, then write `04_verify.md`
