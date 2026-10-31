## Context
18.2 measured the stop count of two clause wordings and cleared the rejection bar, but both
its sides carried a clause. So it cannot say the clause *caused* anything. 18.1's 0/3 baseline
sat on a different task. This task supplies the one arm neither round had: **the same scoreboard
task, the shipped protocol, no clause.**

The question is narrow and the answer is binary in its consequence. If the baseline also stops
on the scope question, the clause buys nothing and gets deleted. If the baseline proceeds, the
2/3 and 1/3 from 18.2 become a real effect and the question moves to whether that rate is worth
its lines.

### Context Saturation Check
> 2+ unchecked → STOP and ask the user. 0-1 → state the assumption explicitly, proceed.

- [x] **Target files/paths** — known. Arms build from `harness/fixture/` with the shipped
      `BEMYAGENT.md`; the scoring reads `01_think.md` in each arm tree. Setup is
      `work/18/18.2/setup.py` with the arm map changed to one condition.
- [x] **Expected behavior** — defined by 18.2's rubric, reused unchanged so the numbers are
      comparable: blocking items counted from the Saturation Check, the fact, delivery.
- [x] **Constraints** — the prompt, fixture, model and day must match 18.2's. Any of them
      drifting makes the comparison the round exists for invalid.
- [x] **Dependencies** — none new.

**0 unchecked. Proceed.** One assumption stated: 18.2's arms ran on the same day under the same
conditions, so reusing its rubric and prompt verbatim gives a comparable baseline. This is weaker
than running all nine arms in one batch and is recorded as the round's main limitation rather
than argued away.

## Approaches Considered
1. **Three baseline arms, same task, rubric reused.** Cheap, directly answers the attribution
   question, comparable by construction. Weakness: the baseline is measured hours after the
   treatment arms rather than beside them.
2. **Relaunch all nine arms in one batch** (3 baseline + 3 + 3). Strictly better science, and
   three times the cost to re-measure six arms whose numbers are already recorded and whose
   trees are intact.
3. **Score the question from 18.1's baseline.** Rejected: different task, different number of
   decisions, which is exactly the variable 18.2 showed matters.
> Not discarded forever: if the baseline arms disagree with each other, 2 becomes necessary.

## Selected Approach & Risks
Chosen: **1**, with the timing limitation written into the verdict rather than hidden.
- Estimated token cost: **low** (3 arms, and a baseline arm that proceeds does the full build).
- **Risk — the baseline stops 3/3.** Then the clause is redundant and the whole of 18.1 and 18.2
  resolves to a deletion. This is the outcome the round most needs to be able to reach, so the
  rubric must not be tuned after seeing it.
- **Risk — the baseline splits 1/3 or 2/3 like the treatment arms.** Then nothing separates at
  N=3 and the honest output is that the clause has no measurable effect, which is a null and
  means the lines do not get bought.
- **Risk — scoring my own candidate again.** Same mitigation as 18.2: the rubric predates the
  launch and is computed from file-level facts.

### Pre-mortem
1. *The prompt or fixture drifts from 18.2's.* Mitigated by reusing `setup.py` and the prompt
   text verbatim and diffing the built arm against an 18.2 arm before launching.
2. *A leaked listener contaminates an arm again.* Mitigated by sweeping ports before the launch
   and after the round, which is now the harness rule.

### Devil's Advocate
Drop the clause now without measuring: two rounds have failed to show it changes anything, and
the repo's own standard is that a candidate that cannot be shown to work does not land. Not
chosen, because deleting on an absence of evidence and deleting on a measured null are different
records, and the second is the one this repo publishes.

## Verification Plan
Per arm: the number of items marked blocking in the Saturation Check, whether a repo-checkable
fact is among them, and whether anything shipped. Scored from the arm trees. Read against 18.2's
recorded 2/3 and 1/3.
