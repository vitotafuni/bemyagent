## Context

Will an agent invoke an optional code-graph tool the Routing Table points at? Gating
question for adopting Graphify (or anything like it) as the structural half of
`03-code-map.md`. Analysis: `docs/drafts/graphify-evaluation.md`.

Milestone 14 measured an optional affordance at **0/9 invocations** with the trigger met and
capability confirmed. So tool-vs-no-tool is not the interesting comparison — a tool nobody
invokes is the result we already have. What is untested is whether the **procedural** form
gets invocation where the permissive form does not, which is the one reliable lever this
protocol has (11/16/18: declarative ~0, procedural near-total).

### Context Saturation Check

- [x] **Target files/paths** — `scratchpad/exp2/{setup2.py,graphify,runs2/,invocations/}`
- [x] **Expected behavior** — d (permissive) invokes rarely; e (procedural) invokes often.
      Either direction is a result; d≈e≈0 would close the Graphify question cheaply
- [x] **Constraints** — harness rules 1–4; arms differ only on BEMYAGENT.md line 52 (asserted
      programmatically); model pinned; one arm per condition per batch; neutral names d/e
- [x] **Dependencies** — python3 only; tool smoke-tested, returns real `path:line` nodes and
      logs every call to an absolute path outside the arm

0 unchecked.

## Approaches Considered

**1. Install the real `graphifyy` package (0.9.83) and point arms at it.** Highest ecological
validity. Rejected for this round: it installs third-party software on the user's machine, and
it confounds the question — a null could mean "did not choose to" or "tried and it failed /
was slow / errored". Propensity must be isolated first. If invocation is non-zero, the real
package becomes the next round and the question there is graph quality.

**2. Vendored tool inside each arm (chosen).** `./tools/graphify`, self-contained, no install,
identical across conditions, logs every invocation to an absolute path the arm does not see.
It is a genuinely working code-graph query — it really parses the arm's files and returns real
`path:line` nodes — just far simpler than the product. Measures propensity cleanly.

**3. Tool-vs-no-tool (one condition + baseline).** Rejected: baseline cannot invoke a tool it
was never told about, so it measures nothing. The draft proposed this; the Milestone 14 result
makes permissive-vs-procedural strictly more informative at the same arm count.

## Selected Approach & Risks

Two conditions × 3, both carrying the tool, differing only in how line 52 phrases it.
Clean fixture — no planted defect. One variable.

Estimated token cost: medium (6 arms; the 9-arm round cost ~825k).

**Risks & Mitigations**
- *Tool never discovered because the arm never reads line 52* → it is in the Routing Table,
  which §2/§3 make arms read on every task; 9/9 arms in 14.3 demonstrably followed it.
- *Arm invokes it once during bootstrap orientation and never again* → log captures every call
  with arguments and timestamps, so "explored once" and "used while working" are separable.
- *The stub is too simple to be worth invoking, and that is what gets measured* → it returns
  correct, useful nodes (verified in smoke test); and the comparison is between two conditions
  with the identical tool, so tool quality cancels.
- *Scoring the first batch* → same discipline as 14.3: N=1 per condition is a progress check.

## Verification Plan

Invocation logs per arm, which are unfakeable and were written by the tool, not the arm. Score:
invoked at all (y/n), number of calls, and whether `03_execute.log` cites returned `path:line`
nodes (arm e only — its forced artifact). At N=3, only clean separation is signal.
