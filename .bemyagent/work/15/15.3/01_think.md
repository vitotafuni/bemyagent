# THINK — 15.3 Does a mandated `## Project rules` section capture a standing rule?

## The question

FEDERATION issue #7 says *memory is not storage*: a user rule that lives only in the AI tool's
private memory (Claude Code `memory/`, Cursor rules) is invisible to other tools and to a new
machine. Sub-proposal (a): the rule file gains a **mandatory `## Project rules` section, even
empty, with a guide line**, and §1 Self-Registration checks it.

I objected on measured grounds: an empty mandated section is the shape that measured **0/8** in
the P3 glossary round — the section appeared and held only vocabulary that already existed.
*A mandated empty section stays empty.*

**This round tests my objection, not the proposal.** If arms fill it, I was wrong and the
proposal lands as written. If they do not, the objection is evidence rather than opinion and the
proposal needs a trigger that fills the section rather than a heading that reserves space.

Self-observed instance, which is why this matters beyond the report: two standing preferences
from this repo's own sessions (push-summary triggers, the tag convention) live only in Claude
Code's private `memory/` — unversioned, invisible to any other tool, lost with the machine.

## Context Saturation Check

| Item | Known? |
|---|---|
| What the proposal is | yes — issue #7(a), quoted above |
| The competing prior | yes — P3 glossary, 0/8 declarative vs 7-8/8 when attached to a forced write |
| Whether the harness can run it | yes — fixture present; scaffolding must be rebuilt (prior round dirs were removed) |
| What "a standing rule" looks like in a prompt | **assumption stated**: an instruction scoped to the repo and not to the task ("in this repo always X"), as opposed to one scoped to the change at hand |
| Whether arms will have an occasion to fire | yes — by construction, the prompt carries one standing instruction |

0–1 unknown → state the assumption and continue. The assumption is the standing/task-specific
distinction, which is also what the harm arm measures.

## Approaches considered

1. **Score whether the section exists.** Rejected — that is the `Layers:` trap. The section's
   existence is forced by the template; what matters is whether it holds the rule.
2. **Ask the arm at the end whether it captured the rule.** Rejected — self-report is not
   evidence (Decision 20, and the VERIFY-evidence learning).
3. **Chosen: plant one standing instruction and one task-specific instruction in the same
   prompt; read the files on disk afterwards.** The artifact is the deliverable, and the harm
   arm costs nothing extra because both instructions ride in the same run.

## Pre-mortem

Assume the round failed. The three likeliest causes:

1. **The instruction is ambiguous between standing and task-specific**, so scoring is a judgment
   call and the harm arm is meaningless. *Mitigation*: the standing instruction names the repo
   and a recurring future action; the task-specific one names this change only. Both are written
   into the prompt verbatim and quoted in `02_tasks.md` so scoring cannot drift.
2. **Arms die on budget** — this voided a 9-arm round once. *Mitigation*: 6 arms in 3 batches of
   2, one per condition per batch; verify each batch completed before launching the next.
3. **The baseline also captures the rule**, somewhere else in `.bemyagent/`, making the
   treatment look useless when in fact the protocol already works. *That is not a failure* — it
   is the finding, and it would mean issue #7(a) is already covered. Score where the rule lands,
   not only whether it lands in the new section.

## Devil's advocate

Radically different alternative: **skip the section entirely and test #7(c) instead** — the
precedence rule `rules > plan > memory`. It is one line, changes a decision rather than adding
a ritual, and I already recommended taking it first.

Not pivoting, because 7(c) and 7(a) answer different questions. Precedence says *which source
wins when they conflict*; this round asks *whether the rule reaches a durable source at all*. If
nothing is captured, precedence has nothing to rank. This is the prior question.

## Assumption carried forward

That a standing instruction given in chat is the right stimulus. A real user rule may arrive
across several turns or be inferred rather than stated. This round tests the explicit case only,
which is the easiest one — **a null here would be strong, a pass here would be weak**.
