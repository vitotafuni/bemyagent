# THINK — 15.4, the gate leaves no trace

## Context

### Context Saturation Check
- [x] Target files/paths — `BEMYAGENT.md` §3 Write Gate, step 2. One sentence.
- [x] Expected behavior — the gate's line survives in the repository, and coverage does not drop.
- [x] Constraints — one variable; N=3 per side; the harm is a write per governed file, so it
      needs its own metrics; **19.4's scorer check applies to this round**.
- [x] Dependencies — 14.13's setup as the base.

0 unknown. Proceed.

## Why this round is worth running now rather than when it was filed

Issue #5 said `PROTOCOL_CHECK` leaves no trace. It sat as a principle. Two rounds this week put
numbers under it from opposite directions:

- **19.3**: the gate fires 6/6 but names only **18 of 33** governed files — 55%. Measured from
  transcripts, because the tree holds nothing.
- **19.2b**: a control arm overrode Step 0's gate and left **no record on disk at all**. On disk
  it is indistinguishable from an arm that never took the branch, and Milestone 19 closed saying
  that this, not the branch condition, is what outlives it.

Both findings are the same shape: **a gate whose output goes to the conversation is invisible to
everyone who was not in the conversation**, which includes the next session, the user reading a
diff, and this harness. 19.3's 55% could only be measured because I had the transcripts; a user
has none.

## The candidate

One sentence added to step 2:

> 2. Output: `PROTOCOL_CHECK: target=[path], reason=[why]` — **and append that same line to the
>    current task's `03_execute.log` (`work/<N>/micro.log` for a Micro task). The conversation is
>    not a record.**

It is procedural, and it attaches to an artifact the protocol already forces. That is the
strongest regularity in this repo's measurement record, and the one 14.6 demonstrated inside a
single milestone: permissive 0/3, procedural 3/3.

## The harm is the reason this needs its own arms

A write per governed file is not free, and three failure modes are reachable:

1. **Delivery.** Milestone 18's clause cost two deliveries of three. A rule competing for
   attention with the rules already there is harness rule 4.
2. **Batching, which is compliance without the mechanism.** An arm can do all its work and then
   append six gate lines at the end. The file then holds a record that looks like a gate and was
   written as a transcript. The gate's claim is *"proceed only after step 2"*; a line written
   afterwards proves the opposite of what it asserts.
3. **Ritual lines.** Lines naming files the arm never wrote, or reasons that restate the rule
   rather than the decision. 19.3 found the opposite in the shipped gate — reasons that cite the
   Routing Table doing real work — so a drop in reason quality is a cost the obligation could
   buy.

## Approaches Considered

**A. A dedicated `work/protocol-check.log`.** Rejected. A new file is a new thing to keep in
sync, and the repo's own learning says multiple hand-synced copies drift. `03_execute.log`
already exists, is already mandatory, and is already the place where *command → result → next
intended action* lives.

**B. Append to `03_execute.log`.** Selected.

**C. Have the harness capture it.** Rejected for the same reason the conversation-log contract
shipped as opt-out: the protocol specifies what must be true, not how a tool produces it, and a
trace only a particular harness can write is no trace at all for everyone else.

### Pre-mortem

1. **Coverage is measured from disk on one side and from transcripts on the other**, which are
   not the same instrument. Both sides get **both** measurements, and the transcript figure is
   what the two conditions are compared on. Stated now, not in VERIFY.
2. **The exemption confuses the count.** §3 exempts the task's own `01`–`04` files, so an arm
   writing its own TTEV owes nothing — and the treatment asks it to write the gate line *into*
   one of those exempt files. That is not a contradiction but it reads like one, and an arm may
   resolve it either way. Scored, not assumed.
3. **Batching is the likely compliant failure**, and it is invisible to a count. Detected by
   reading where the lines sit in `03_execute.log` relative to the entries around them.

### Devil's Advocate

Do nothing: 55% is not terrible, the gate fires 6/6, and the repo has a bias toward adding rules
after a round makes a gap visible. Genuinely the thing to beat. What decides it is 19.2b: the
problem is not that coverage is 55%, it is that **nobody outside the conversation can tell
whether it was 55% or 0%**. A protocol whose compliance can only be audited by the agent that
was already there is not auditable.

## Verification Plan

Coverage from both instruments on both sides. Batching read from the position of the lines in
the log. Delivery from `npm test` and the client. **19.4's rule applies**: for every metric, the
arms at each end get opened and named in `04_verify.md` before the number enters the verdict.
