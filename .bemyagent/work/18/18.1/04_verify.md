# 18.1 VERIFY — product decisions trip the STOP threshold on their own

**Verdict: clean separation, zero over-trigger, and a real cost. Do not land yet — one more round first.**

## The three metrics, fixed in `02_tasks.md` before launch

| | z1 | z2 | z3 | baseline (15.11 w1-w3) |
|---|---|---|---|---|
| **SURFACED** a product decision | yes | yes | yes | **0/3** |
| **OVER-TRIGGER** (stopped on a non-decision) | 0 | 0 | 0 | — |
| **DELIVERED** the feature | no | no | no | 3/3 |

**0/3 → 3/3 on the primary.** Clean separation by the harness rule. Evidence in
`03c_arm_evidence.txt`: 3/3 wrote `01_think.md` (77–90 lines), 0/3 wrote `02_tasks.md`,
0/3 touched `client`, `server`, `db` or `test`.

Each arm stopped on **exactly one** thing, the same one: which mark opens the rematch. Each
explicitly carried other decisions as stated assumptions rather than asking — no series score,
and a rematch as a new row rather than a reset. z1: *"Two further decisions were assumed, not
asked (both reversible, both recorded in the spec)."* z3 on the ones it kept: *"these concern
**how** the rematch is wired, not **who starts**."* **Over-trigger is 0/3 and it is not an
accident of the task; the arms show their classification work.**

The clause also integrated with the machinery already there rather than fighting it. §4 already
says a task stopped by the Saturation Check must not get an `02_tasks.md` and must be marked
`blocked`. 3/3 did exactly that, unprompted, and two cited the rule while doing it.

## What the arms actually used as the trigger, and it is sharper than my clause

I wrote *"more than one answer is defensible and the user owns which"*. All three arms
converged instead on **what the answer costs if it is wrong**:

- z3: *"Q1 decides the shape of the change, not a detail inside it."*
- z1: *"Guessing (a) and being wrong isn't a tweak to undo, it's the API change not made."*
- z2: *"(a) is a client-only change; (b) and (c) change the public API."*

The operative distinction was **reversibility**, not ownership. A decision cheap to revisit got
an assumption; one that fixes the architecture got a stop. That is a better criterion than the
one I shipped, because "the user owns it" is a matter of opinion and "undoing this means
rewriting the API" is checkable. **Candidate rewording for round two, taken from the arms.**

**Third convergence on the same shape.** Decision 22's guarantee 4 limits its trigger to
behaviour guarding a failure mode the user cannot foresee; the approval-gate literature
recommends gating the irreversible step rather than every step; the arms here, with neither in
context, reinvented reversibility as the line. Three independent routes.

## The cost, stated plainly

**Nothing shipped.** 0/3 delivered the feature, against 3/3 in the baseline. On a task with one
genuinely open product decision, the clause converts a delivered feature into a question. That
is the intended behaviour, and it is also exactly what guarantee 1 charges the user for.

Whether the trade is worth it is not decided by this round. What this round shows is that the
trade is **real and narrow on this task**: one stop, no false stops, and the arms argue the
stop was worth it because the wrong guess is an un-made API change rather than a tweak.

## Why this must not land yet

**One task, one open decision.** The round establishes that the clause fires correctly when
there is exactly one thing to fire on. It says nothing about the **rate** on a task carrying
five or six ambiguities, which is where guarantee 1 gets charged in practice. A rule that stops
once is a question; a rule that stops six times is a form to fill in.

Round two: same clause, a task with several open decisions of mixed reversibility. Metric is
the **stop count** and whether the arms rank by reversibility or stop on everything.

## Validation against the CDM

- **Protocol delta is one line** — `03b_protocol_delta.diff`, 2 differing lines. PASS.
- **3/3 arms produced a readable `01_think.md`**. PASS.
- **Setup, delta and raw evidence copied here before the verdict**. PASS.
- **Drift (🎯)** — the verdict is computed from the arm trees (`git diff --stat`, file presence,
  the text of `01_think.md`), never from an arm's claim about itself. PASS.
- **Pivot (🔄)** — over-trigger was not 3/3, so the primary remained scorable. No arm shows
  signs of inferring it was under test. No pivot triggered.

## Limitations

1. **The baseline is reused, not fresh.** 15.11's w1-w3: same fixture, same prompt, same rubric,
   same day, recorded and committed before these arms existed. Stated here rather than implied.
   It is also what removed 15.11's blinding failure: a single-condition batch has nothing to
   blind.
2. **N=3.** Clean separation is the bar, and it was met, but three arms on one task is a
   mechanism demonstration of a narrow case, not a rate.
