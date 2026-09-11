## Context

Run the read-delegation A/B: does delegating a code read to a cheaper model tier cost
correctness, and does the bounded (pointer-only) form prevent the loss? Design, instrument
repair and scenario verification are done (14.1, 14.2, 14.4). This task is the run and the
scoring only.

Candidate rule and full reasoning: `docs/drafts/read-delegation.md`.

> **Ceremony miss, recorded.** 14.1/14.2/14.4 touched six files and were executed with no
> TTEV folder at all — Heavy work run at Micro ceremony. Same class as the §6 miss found by
> 13.7. Not back-filled: `01`/`02` are forward-written artifacts and inventing them after the
> fact would be exactly the fabricated-record shape Decision 18 exists to catch. Logged here
> because the protocol is dogfooded and a silent miss is the failure mode.

### Context Saturation Check

- [x] **Target files/paths** — 9 arm dirs under `scratchpad/exp/runs/`, `setup.py`, `score.py`,
      `prompt.txt`; fixture and code-map known
- [x] **Expected behavior** — arm b (free delegation) loses the planted defect; arm a and
      arm c catch it. Any other pattern is a real result, including "no separation"
- [x] **Constraints** — harness/README rules 1-4; arms differ only on BEMYAGENT.md line 98
      (asserted programmatically); model pinned explicitly on every arm; neutral dir names
- [x] **Dependencies** — Node 26.5.0 verified, fixture builds 4/4; `Agent` tool exposes a
      `model` enum incl. `haiku`, so arms can actually delegate (14.4 probe)

0 unchecked.

## Approaches Considered

**1. Two arms (baseline vs bounded delegation).** Cheapest at 6 runs. Rejected: the bounded
clause's whole claim is that it *prevents* a harm, and with no free-delegation arm the harm
can never occur, so the run could only produce a null. Harness rule 4 demands an arm where
the candidate could plausibly hurt.

**2. Three arms, 3 runs each (chosen).** a = baseline, b = free delegation, c = bounded.
9 runs. Isolates both questions: does delegation hurt (b vs a), does the bound fix it (c vs b).

**3. Score token cost as the primary metric.** Rejected as primary: Decision 16 already showed
a 17.4% "saving" with complete separation across 6 runs that was an artifact of doing 15% less
work. Cost is a secondary read here, normalised per unit of work, never the verdict.

## Selected Approach & Risks

Three arms × 3, mechanism-scored. Correctness (does the defect survive the read) decides;
cost is reported normalised and does not decide.

Estimated token cost: **high** — 9 full task runs. Accepted: this is the deliverable.

**Risks & Mitigations**
- *Arms don't delegate even in b* → then b ≡ a and the rule is untestable-as-written, not
  harmless. Report as untested, do not ship on the null. (14.4 cleared the capability, not
  the propensity — an agent that *can* delegate may still choose not to.)
- *Model tier floats* → pin `model` explicitly on all 9 arms (14.4 finding).
- *Arm reasons about being under test* → fixture README de-identified in 14.1; dir names
  `a-1`…`c-3`.
- *Scorer regex fires on prose rather than the artifact* → NOTICED is prose-based and weak by
  construction; DEDUPED reads the shipped endpoint. On any disagreement between the two, read
  the arm and trust DEDUPED (harness rule 3: force the artifact, never the assertion).
- *Defect not actually present* → verified in all 9 copies before launch (14.2).

## Verification Plan

`score.py` over the 9 arms + `tokens.py` for cost. At N=3 only clean separation (0/3 vs 3/3)
counts as signal; anything narrower is a null. Read every arm whose NOTICED and DEDUPED
disagree before believing either.
