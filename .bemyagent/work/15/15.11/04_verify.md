# 15.11 VERIFY — approval gate, proxy round

**Verdict: NULL on the primary metric, with one observation worth more than the null.**

## Primary metric — SURFACED vs SETTLED on `01_think.md`

Rubric fixed in `02_tasks.md` before launch. Evidence: `03b_score_output.json` (deterministic
extraction), `03c_condition_key.json`, arm trees.

| | w1 | w2 | w3 | w4 | w5 | w6 |
|---|---|---|---|---|---|---|
| `interactiveMode` | false | false | false | **true** | **true** | **true** |
| decision handed to the reader | no | no | no | no | no | no |

**SURFACED 0/3 baseline, 0/3 treatment.** Every arm settled both decisions itself.

By the CDM's floor/ceiling clause this is a **null, not inconclusive** — provided the decisions
were reachable, which the secondary count establishes: new-row-vs-reset was weighed as an
explicit alternative by **6/6** arms, and who-opens-the-rematch was named by **3/6** (w3
baseline, w5 and w6 treatment). The arms saw the questions. They answered them.

**Borderline call, recorded because it is the one a reader should challenge.** w6 comes
closest: it leaves the Saturation Check box unticked and writes *"one open point … **who opens
the rematch?**"*. It then writes *"Assumption stated and carried (0-1 rule)"* and builds with
X. The rubric requires the plan not to settle the decision itself; w6 settled it. Scored
SETTLED. A reader who disagrees can re-read `03b_score_output.json` and say so.

## Why every arm settled, which is the actual finding

Three arms cite the protocol's own rule while doing it. w6 names it outright: **"(0-1 rule)"**.
§4's Context Saturation Check says 2+ unknowns → STOP and ask; 0-1 → **state the assumption
explicitly and continue**. One open product decision is one unknown, so the protocol
instructs the agent to assume and proceed.

**The approval gate sits downstream of the rule that decides whether a question is ever
asked.** The Saturation Check fires inside THINK; the gate fires after THINK. By the time the
gate exists, the question has already been converted into a stated assumption. The gate cannot
undo that, and this round shows it does not.

So the lever for "make the agent surface decisions" is **the Saturation Check's threshold**,
not the gate. That is a cheaper and more promising candidate than anything in the DRT family,
and it is testable with the same fixture.

## Observation — gate compliance, 1/3

Read from the arm trees, never from the hand-back reports (`03d_arm_evidence.txt`):

- **w5** wrote no product code and no `04_verify.md`. Gate honoured.
- **w4** and **w6** implemented the feature in full and wrote `04_verify.md`, then reported the
  gate as owed. w6 states it plainly: *"both gates are deferred into a single review at
  hand-back … Flagged rather than silently skipped."*

So the rule that is supposed to **stop** work was converted by 2 of 3 arms into a **note about
having not stopped**. This is the protocol's recorded ceiling again, from `05`: *anything that
must happen before or on every X cannot be a prose rule.* MUST STOP is a before-X rule.

**Not reported as a rate.** N=3 and 1/3 is not clean separation; it is a mechanism
demonstration, not a measurement. It also does not inherit the authority confound from
`harness/README.md`, because no approval was ever requested of any arm — each decided on its
own whether to stop.

## Validation against the CDM

- **One variable** — `diff -r` across arm trees: single hunk, `"interactiveMode"`. PASS.
- **6/6 arms produced a readable `01_think.md`** (39–80 lines). PASS.
- **Scorer and raw output copied into this folder before the verdict** — `setup.py`,
  `score.py`, `03b`, `03c`, `03d` are here. PASS.
- **Drift check (🎯)** — the verdict is computed from plan content. Gate notes were excluded by
  the rubric and did not enter it: `stop_announcements` is recorded in `03b` and unused. The
  second drift is also avoided: this is a verdict on the gate's effect on the plan at first
  exposure, not on the approval gate. PASS.

## Caveats, both self-inflicted

1. **The blinding failed and the scorer only looks blind.** Arms hand back a report naming
   their own directory, and `setup.py` maps directories to conditions, so by scoring time I
   knew four arms' conditions. `03c_condition_key.json` protected nothing. What remains is
   weaker but auditable: the rubric predates the launch and the extraction is deterministic, so
   the calls can be checked against `03b`. A future round must either suppress hand-backs or
   have a second agent score from `03b` alone.
2. **`node_modules/` was removed from w1 after the build check**, to restore symmetry across
   arms. Arms that executed had to install for themselves, with a native `better-sqlite3` on
   Node 26 — the "fixture becomes a debugging session" trap from `harness/README.md`. It does
   not reach the metric, because `01_think.md` precedes execution, and 6/6 arms did produce it.

## What does not follow from this

This round says the gate does not change the plan **at first exposure**. It says nothing about
whether a human reading the plan catches things the agent missed — three arms show an
independent verifier doing exactly that. The habituation clause in `05` (recorded before the
data) stands: a null here is decisive for the gate's effect on the artifact and silent on the
gate's value as human attention, which is the part this harness structurally cannot reach.
