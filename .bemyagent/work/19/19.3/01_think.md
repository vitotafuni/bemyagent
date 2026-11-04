# THINK — 19.3, do gates land at all in this repo

## Context

### Context Saturation Check
- [x] Target files/paths — the arm transcripts already on disk; no fixture, no new arms.
- [x] Expected behavior — a compliance rate for the Write Gate, with the occasion counted.
- [x] Constraints — `harness/README.md` rules out measuring consent gates; no `BEMYAGENT.md` delta.
- [x] Dependencies — none. The data is already paid for.

0 unknown. Proceed.

## The question splits, and only one half is answerable here

19.3 as written asks whether gates land at all. BMA ships two kinds and they are not the same
object:

**Consent gates** — Step 0's STOP for approval, `interactiveMode`'s stops after THINK and VERIFY.
These exit on a human reply. `harness/README.md` rules them out in as many words: subagents treat
a coordinator's message as non-authoritative by construction, so every arm looks compliant for a
reason unrelated to the rule. 15.11 paid for that lesson and took the README's legal exit by
measuring a proxy. **This half stays untested and the record should keep saying so.**

**Forced-output gates** — the Write Gate in §3: before creating or modifying any file in `docs/`
or `work/`, re-read the Routing Table and emit `PROTOCOL_CHECK: target=…, reason=…`. No human in
the loop, no authority problem, and a forced artifact, which is the one shape this harness says
works (rule 3). **This half is measurable and has never been measured.**

That asymmetry is the finding before any number: the gate this repo has shipped since Milestone 9
as **Decision 13**, justified in `05` with an estimate — *"declarative rules rejected (estimated
~50-60% compliance), procedural gates with forced output estimated at ~90%"* — has never had the
estimate checked. Issue #5 records that `PROTOCOL_CHECK` leaves no trace, which is why: it is
emitted into the conversation, not written to a file, so no grep of the tree can find it.

## Approaches Considered

**A. Spend six arms on a gate-on / gate-off A/B.** Rejected. The gate's output is the artifact,
so an arm without the gate scores zero by construction and the round would measure nothing but
the clause's own presence — the same theatre 14.8 refused a baseline for.

**B. Read the arm transcripts already on disk.** Selected. 14.13's six arms ran the shipped
protocol, wrote repeatedly into `docs/` and `work/`, and their transcripts are kept. The gate's
occasion is counted from the same transcripts rather than assumed, which is the reachability
check the harness demands. Cost: zero arms.

**C. Ask a fresh arm to self-report whether it ran the gate.** Rejected on harness rule 3. A
claim about the work is free; it is the assertion, not the artifact.

## Selected Approach & Risks

Parse the transcripts. Per arm, count **occasions** (writes to a path the gate governs, minus the
exemption §3 grants the current task's own TTEV files) and **emissions** (`PROTOCOL_CHECK` lines
the arm itself produced). Report the rate and whether the **first** governed write was preceded
by one.

### Pre-mortem

1. **The occasion count is the whole measurement and my first attempt was already wrong.** A
   crude probe counted any Bash command containing a `.bemyagent/` path next to a redirect, which
   swept up `diff`s and `grep`s *reading* `00-ai-rules.md` into a temp file. Those are reads. They
   landed first in every arm and turned "first governed write preceded by a check" into **NO 6/6**
   — a clean-looking result produced entirely by the instrument. The probe is discarded, not
   patched in place, and the real scorer counts only writes whose *target* is a governed path.
2. **Over-counting emissions.** `PROTOCOL_CHECK` appears inside `00-ai-rules.md`, so any arm that
   reads or writes the rules file carries the string. Only text the arm itself produced counts;
   tool results are excluded, and the exclusion is reported as a number so it can be checked.
3. **Directory creation is not a file write.** `mkdir -p .bemyagent/docs/specs` governs nothing.
4. **One round, one task shape.** Six arms doing the same feature on the same fixture. Pooling
   the other transcripts in the session gives a wider but messier sample; it is reported
   separately and never merged into the headline.

### Devil's Advocate

The alternative reading is that this measures a gate nobody doubted, and the interesting half is
the consent gate the harness cannot reach. Partly true, and that is why the untested half is
stated first rather than buried. But a protocol that has carried a 90% estimate for ten
milestones and used it to justify preferring procedural rules over declarative ones has a
number it has never looked at, and 19.2 is queued to add behaviour to a gate on the strength of
it. Checking it costs nothing here.

## Verification Plan

Every figure comes from a script over the transcripts, copied into this folder with its output.
The discarded probe and why it was wrong are written into `03_execute.log` before the clean
numbers, not after.
