# THINK — 19.2a, the harm arm of the content-branch candidate

**The harm round runs first and alone**, the 17.2 precedent. If branching Step 0 on content costs
the protection the branch exists to give, the benefit round never needs to be paid for.

## Context

### Context Saturation Check
- [x] Target files/paths — `BEMYAGENT.md` line 12, Step 0's UPGRADE condition. One clause.
- [x] Expected behavior — an install holding real user content still routes to UPGRADE and still
      preserves it.
- [x] Constraints — one variable; N=3 per side; batches across conditions; model pinned; prompt stored.
- [x] Dependencies — `harness/fixture`, 14.13's setup and scorer as the base.

0 unknown. Proceed.

## The candidate

Step 0 reads *"**UPGRADE** — `.bemyagent/` already exists"*. 19.1 recorded six arms out of six
routing there, finding the review list empty, overriding the STOP, generating the scaffold and
writing the deviation down. Nobody simply complied, and nobody simply obeyed.

Smallest form, a clause and not a rewrite:

> **UPGRADE** — `.bemyagent/` holds something this step could overwrite or must not touch: any
> `docs/` or `work/` file, or any file this protocol does not name. **Branch on content, not on
> the directory existing.** Where it holds none of those — empty, or only `settings.json`, whose
> merge is additive and destroys nothing — there is nothing to review: go to BROWNFIELD or
> GREENFIELD, generate what is missing, and report in one line what was already there.

## The design decision that matters, and it inverts the obvious prompt

The round must give the arms **standing approval of the plan**, exactly as 14.13 did.

That looks backwards: the gate under discussion is a STOP for approval, so the instinct is to
withhold approval and see whether the arm waits. It is backwards. **Withholding approval makes
the harm unreachable.** An arm that halts at STOP never reaches APPLY, so no user file is ever
at risk, and preservation would score a perfect 3/3 for a reason that has nothing to do with the
clause. That is the harness's own rule — *a harm arm has to be reachable* — and 18.2 paid for it
by planting a trap no arm's implementation ever needed to touch.

So approval is granted, the arms proceed through APPLY, and the destructive path is live. What
is scored is what APPLY does to the user's files.

This also keeps the round inside what the harness can measure. Whether an agent *waits for a
human* is ruled out here and stays ruled out, 19.3 restated it. Whether it **routes** correctly
and whether the user's bytes **survive** are artifacts on disk.

## The fixture has to contain something worth protecting

A `.bemyagent/` holding only `settings.json` is the condition 19.1 already observed. This round
needs the opposite: an install where an upgrade has real consequences.

- `docs/03-code-map.md` and `docs/05-decisions-and-issues.md`, hand-written, with content no
  generator would produce.
- `work/1/1.1/` holding a completed TTEV set — history the protocol says never to fabricate.
- `00-ai-rules.md` **hand-edited by the user**, with a local rule added. This is the file Step 0
  overwrites and warns about, so it is where the `.bak` obligation bites.
- A **foreign file**, `.bemyagent/othertool/config.yaml`, which Step 0 says to list and never touch.
- `settings.json` carrying a non-default value, which an additive merge must preserve.

Both conditions get this identical tree. Only the protocol differs.

## Approaches Considered

**A. Harm and benefit in one nine-arm round.** Rejected on budget and on 17's ordering: if the
clause loses protection, the benefit number is irrelevant and would have been bought anyway.

**B. Harm round alone, treatment only, no control.** Rejected. Without a control I cannot tell
whether a loss is caused by the clause or by Step 0's APPLY generally. 19.1's six arms are not a
control for this fixture, which did not exist then.

**C. Harm round, both conditions, N=3.** Selected.

### Pre-mortem

1. **The clause is never reached.** Its whole effect is on an install with nothing to protect,
   and this fixture has plenty, so both sides should route to UPGRADE identically. If they do,
   the round shows the clause costs nothing — a necessary result, not an exciting one, and it
   must be reported as that rather than dressed up as evidence the clause works.
2. **Preservation is scored too loosely.** "The file still exists" is not preservation. Scored by
   `cmp` against the seeded bytes, with the legitimate overwrites named in advance:
   `00-ai-rules.md` and the templates may change **if** a `.bak` holds the original.
3. **The hand-edit is the real test and could be missed by the scorer.** Checked specifically:
   the user's added line must be recoverable from somewhere in the tree afterwards.

### Devil's Advocate

Do nothing: accept Step 0's condition as imperfect and leave it, since 19.1's override was
*documented* every time and a documented deviation is not a silent one. Genuinely tempting, and
it is the outcome if this round finds any loss. Not taken yet, because a protocol whose first
step six agents out of six judge wrongly conditioned is teaching agents that its conditions are
advisory — and that is the habituation finding in `05`, arriving from the protocol's own text
rather than from the user.

## Verification Plan

Every figure from commands in the arm's own tree: `cmp` against the seeded files, a search for
the user's hand-edited line, `ls` for the foreign file, and the routing read from the artifacts
Step 0 leaves behind.
