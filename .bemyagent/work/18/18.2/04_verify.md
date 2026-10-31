# VERIFY — 18.2, round 2

Scored from the arm trees (`01_think.md`, `git diff --stat`, file presence), never from
hand-back text. Raw per-arm figures in `03d_arm_evidence.txt`.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| One-line delta per side | PASS | `03b_delta_own.diff`, `03c_delta_rev.diff` — one changed line each, line 91 |
| 6/6 arms produce `01_think.md` | PASS | all six present, 90 / 74 / 73 / 31 / 64 / 41 lines |
| Setup, deltas and raw counts in this folder before the verdict | PASS | `setup.py`, `03b`, `03c`, `03d` |
| Stop count from the artifact, not from the arm's prose | PASS | counted from the Saturation Check checkboxes; `03d` quotes each arm's own justification beside it |

## Primary metric — STOP COUNT

Pre-fixed reading: 1 per arm → lands. 2 → borderline. 3+ → rejected in that wording.

Stopping arms counted **1, 1 and 2**. No arm reached 3 in either wording. **The clause does not
enumerate.** Both wordings rank: each stopping arm named the scope question and carried the rest
as stated assumptions rather than listing every open item. The rejection bar this round existed
to test is cleared.

## What the round does not establish, and this is the verdict

**There is no baseline arm on this task.** Both sides carry a clause; 18.1's 0/3 baseline was
measured on a different task. So the round answers *how much* the clause stops and cannot answer
*whether it caused* the stops. On this task the baseline is unknown.

That matters because the rate is low and uneven: **ownership 2/3, reversibility 1/3**. By this
repo's own N=3 rule only 0/3 against 3/3 is signal, so the two wordings are **indistinguishable
here**, and the ownership wording that measured 3/3 in 18.1 measures 2/3 on a task carrying
several decisions. Three of six arms proceeded.

The three that proceeded each quoted the clause's **exclusion** half to justify it: *"an
implementation fact you can verify is not a product decision"* (q3), *"the rule reserves a solo
STOP for a decision whose wrong answer forces rewriting an interface or a schema"* (q6), and the
same reasoning in q4. The exclusion is load-bearing and it works. But a clause whose exclusion is
the part doing the work is a clause that **shifts a judgement rather than forcing a stop**, and
nothing here separates that from what the arms would have judged without it.

**Verdict: PASS_WITH_CAVEATS. Does not land.** Not rejected — it cleared the bar it was built to
test — but not landed either, on the rule this repo already holds: a candidate that cannot be
shown to change behaviour does not buy its lines at every session restore. The missing arm is
cheap and specific: three baseline arms, this same task, no clause. That is 18.3, and it is the
only thing standing between the clause and a decision.

## Harm metric — VOID, not passed

0/6 arms blocked on a repo-checkable fact. The planted fact was *"would a new column reach an
existing database"*, and no arm needed a new column: `game.winner` already holds the answer and
all six found it early. **The trap was never live, so 0/6 says nothing about the exclusion.**
Recorded as void rather than reported as a clean result. A live harm arm needs a task whose
cheapest implementation genuinely requires a schema change.

## Context — delivery

Ownership 1/3 shipped, reversibility 2/3. Consistent with 18.1: a stop costs the delivery.
The three shipping arms converged on the same design independently (a `GROUP BY winner` in
`store.js`, a `GET` route, a `<p>` above `#board`), 18 to 28 insertions across the same four files.

## Caveats on the instrument

1. **Port collision between arms.** q4's fixture server was still listening on 3123 after the arm
   finished; q6's first check talked to it and nearly recorded a false defect in its own work.
   q6 caught it. Only delivering arms run a server, and of those only q6 overlapped q4, so the
   primary metric is untouched. Written into `harness/README.md`.
2. **`node_modules` absent from the fixture**, the residue of 15.11. Arms that shipped ran
   `npm install` themselves. No arm's stop decision depended on it.
3. **Blinding.** Both sides sat in one batch, so the sides were known at scoring time, as in 18.1.
   The mitigation is the rubric, fixed before launch and computed from file-level facts.
