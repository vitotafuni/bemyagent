# THINK — 14.14, correct the reading rule the harness scores by

No arms. This task spends none, and that is the point: what it fixes was found by 14.13 for free,
by noticing that two rounds had run the same condition and reported opposite results.

## Context

### Context Saturation Check
- [x] Target files/paths — `harness/README.md`, Scoring section and the instrument-rule list.
- [x] Expected behavior — a reader scoring a round can tell a null from a ceiling from an
      under-powered draw, and does not file all three as "null".
- [x] Constraints — `harness/README.md` is not part of the distributable; no `BEMYAGENT.md` delta,
      so no tag.
- [x] Dependencies — none.

0 unknown. Proceed.

## What is wrong

> *"At N=3 a real mechanism shows as clean separation (0/3 vs 3/3); anything narrower is noise and
> should be treated as a null."*

The sentence is sound for what it was written against: a mechanism either fires or it does not,
and the control sits at zero because the rule under test does not exist there. Most rounds in this
repo are that shape.

It is wrong wherever the control has a real, middling rate. There, three arms do not measure the
condition, they draw from it, and the sentence converts an undrawable conclusion into a verdict.
That matters because in this repo a null is an instruction: the rule is deleted.

**This is now measured, not argued.** 14.12 and 14.13 ran the same control condition, verified
byte-identical across protocol, rules file, seeded map, prompt and model pin, and read 1/3 and
3/3. One of those two rounds was going to be wrong whatever the candidate did.

## Approaches Considered

**A. Raise N.** Rejected as the primary fix. It is the right answer for a specific round that
needs resolving and the wrong answer as a standing rule: most candidates here separate cleanly at
N=3 and paying four times the budget by default would buy nothing. It belongs in the text as the
remedy for one case, not as the new default.

**B. Name the three outcomes the rule currently collapses.** Selected. The repo already behaves
this way and only the README does not: 14.11 was refused as *uninterpretable* rather than null,
and 14.13 is recorded as a ceiling. The fix is to make the document say what the practice does.

**C. Measure the control's rate before every round.** Rejected. It doubles the cost of every
round to protect against a case that is visible for free, by asking whether the control plausibly
sits at zero before designing the arms.

## Selected Approach & Risks

Three writes to `harness/README.md`:

1. **Rewrite the Scoring rule** to distinguish a **null** (control at zero, treatment at zero,
   the rule had no effect), a **ceiling** (control already at the top, nothing left to buy), and
   an **under-powered draw** (control in the middle, N=3 cannot resolve it). Say that the first
   deletes the rule, the second deletes it and says something true about the baseline, and the
   third resolves nothing and must not be written up as either.
2. **A new instrument rule on shared scratch**, the port-collision rule extended past ports.
3. **A new instrument rule on metric definition**: score an artifact against what it claims, not
   against the condition the setup seeded. 14.13's near-miss is the case.

### Pre-mortem

1. **The rewrite reads as a licence to rescue a failed candidate** by calling its round
   under-powered. Mitigated by binding the label to a fact decided before the data: the control's
   rate. A treatment that loses against a control at zero is a null and stays one.
2. **The README grows and stops being read.** Mitigated by replacing the existing sentence rather
   than appending beside it, and keeping each new rule to its own short paragraph in the list
   that already exists.

## Verification Plan

`diff` the file before and after and confirm the delta is the three intended places and nothing
else. Confirm `BEMYAGENT.md` is untouched, so no tag is due. Re-read the Scoring section whole and
check it no longer contains the collapsed claim.
