# 20.11 — THINK

## Context

20.10 established that every arm this project has ever launched received the parent repository's
`AGENTS.md` and the session's `MEMORY.md` as overriding project instructions, and that **58 of 118
arm launches obeyed the sentinel** and read the shipped protocol out of the parent repository at
their first or second tool call. It also recorded that the leak is **not fixable from inside this
session**, because the injection is keyed to the session's primary working directory.

That last sentence was a claim about the harness, not a measurement. It is now measured and it is
**false as stated**: a headless `claude -p` launched with its working directory outside the
repository receives **no project instructions at all**. Probe run 2026-11-09, arm-shaped tree at
`scratchpad/probe211`, Haiku, one Read:

```
"type":"instructions"            0 records
bemyagent/AGENTS.md              0
00-ai-rules.md                   0
"OVERRIDE any default behavior"  0
MEMORY.md                        3  (the memory tool's own boilerplate in the system prompt)
```

So a clean control is buildable today. This round builds the first one.

### Context Saturation Check
- [x] **Target files/paths** — `work/20/20.11/`; arm trees in `scratchpad/r2011/`; the seed is
      20.8's `setup.py` code path, both branches; the instruments are 20.8's `mutate.py` and
      `score.py`, extended with this round's arms and nothing else.
- [x] **Expected behavior** — N arms deliver the scoreboard and leave `test/` as seeded; P arms
      deliver it and leave a test with teeth. Both predictions are 20.8's published readings.
- [x] **Constraints** — Sonnet both sides, pinned and recorded from the launcher's own
      `modelUsage` key. Same prompt file as 20.8 and 20.3, verbatim. Arms confined to their own
      directory; any port they open is swept afterwards.
- [x] **Dependencies** — `claude` CLI 2.1.308 at `command claude`; the shell's `claude` function
      hands a headless run an empty `mktemp -d` config and must be bypassed. Config dir pinned to
      `<claude-config>`, which is where the probe's transcript landed.

## Approaches Considered

1. **Rename the parent `AGENTS.md` and relaunch Agent-tool arms.** Rejected on three counts: it
   mutates the repository while 34 commits are queued for the user's review; the injection is
   assembled per request from the session's project root, so a rename mid-session is of unknown
   effect and would have to be measured anyway; and a failed rename leaves no trace in the arm's
   numbers, which is exactly the failure class 20.10 was written about.
2. **Headless `claude -p` with cwd outside the repository.** Chosen. The probe shows zero
   instruction records, and the arm trees already live outside the repository, so nothing about
   the fixture changes. It is the only approach that produces a clean arm without the user.
3. **A second interactive session, started by the user from the arm's directory.** The cleanest
   possible condition and the one a real user actually has. Rejected for this round only: it needs
   the user present six times over and cannot be batched. Kept as the eventual check on whatever
   this round concludes.

## Selected Approach & Risks

Six arms on 20.8's seed, three a side, every one launched by `command claude -p` from inside its
own directory with `CLAUDE_CONFIG_DIR` pinned: **q94 q95 q96** with the protocol in the tree,
**q97 q98 q99** with no protocol file of any kind. Scored by 20.8's instruments against 20.8's and
20.3's published readings for the same two conditions.

**The confound, named before launch and not solved by this design.** Swapping the launcher changes
two things at once: the injection disappears, and so does the whole Agent-tool surface — a
different system prompt, no coordinator, no scratchpad reminder, a different tool roster. A
difference between this round and 20.8 therefore cannot be attributed to the injection alone. What
the round can establish is narrower and is what the record actually needs: **whether the published
readings survive on a launcher where the control is verifiably clean.**

### Pre-mortem

- **The P side comes back 0/3 too.** Then the launcher has broken the arms and the clean control's
  0/3 means nothing — a floor is not a null. Pre-registered in `02_tasks.md` as
  **under-powered, instrument dead**, not as agreement with 20.8. This is the whole reason the P
  side is in the round and is the single most likely way it fails.
- **The headless arm cannot run a command.** In `-p` mode an unpermitted tool call is denied, not
  queued, and an arm that cannot run `npm test` or `curl` floors every metric for a reason that has
  nothing to do with the protocol. Mitigated by an explicit `--allowedTools` roster covering what
  20.8's arms are on record as using, and by reading metric **(iii) delivery first**: a delivery
  below 6/6 condemns the launcher before any teeth reading is believed.
- **`permission_denials` non-empty on any arm.** Same failure, quieter. The launcher reports the
  field; it is read per arm and printed, and any arm with a denial is reported as such rather than
  scored.
- **The arms hang or run away.** Each is launched detached with its stdout captured, and the trees
  are disposable.

### Devil's Advocate

The radically different alternative is to **not run this round at all**, on the grounds that 20.10
already settled it: the exposure was inert, so a clean control cannot move anything. That argument
is weaker than it looks, and the reason is worth stating. 20.10 measured that the exposed controls
produced **no TTEV artifacts** — no `01_think.md`, no `PROTOCOL_CHECK`. It did not measure what
the exposure did to **the teeth metric**, which is the one carrying 5/6 against 0/9. And it could
not: every arm in that census was exposed, so there was no unexposed group to compare against.
"Inert" was a reading on the only population available. This round builds the comparison group.

Not pivoted to. Recorded because it is the honest objection and it narrows the claim: the round
tests whether the readings survive, not whether the injection caused them.

## Verification Plan

- Byte-identity of each new tree against its 20.8/20.3 counterpart (`git hash-object` over the
  initial commit's blobs), before any arm is launched. A seed that differs voids the comparison.
- Teeth via `mutate.py M1` and `M2`, restoring `server/store.js` in a `finally` block and
  comparing `git status --porcelain` before and after, as 20.8 ran it.
- Test artifacts and delivery via `score.py`, read from the tree and not from the arm's report.
- **The clean-control certificate, measured per arm**: each arm's own transcript JSONL grepped for
  `"type":"instructions"`, for the parent repository's absolute paths, and for the OVERRIDE header.
  An arm with a non-zero count is not a clean control and is reported as contaminated, whatever it
  did.
- VERIFY run by an agent that did not do the work, holding only the artifacts and the criteria
  (§4). It is given the trees, the instrument output and the pre-registered readings, and is asked
  for the reading the numbers support — not for confirmation of mine.

## 🎯 Drift
Drifting here means turning an instrument round into a protocol round. The question is whether the
published readings reproduce on a clean launcher. It is **not** whether the protocol works, which
is already on the record, and **not** whether the injection caused anything, which this design
cannot answer. Any sentence in `04_verify.md` claiming the injection's effect is drift.

## ✅ Validation
Every reading in `02_tasks.md`'s fact table filled from a command run during VERIFY, with the arms
named at each end (19.4). The certificate counted per arm, not per round.

## 🔄 Pivot
`obstacleThreshold` is 2. The pre-defined stop: **if the P side reads below 2/3 on teeth**, stop
scoring, declare the launcher unfit, and report that instead of a comparison —
`interactiveMode=false`, so pivot and report in the next update rather than asking.
