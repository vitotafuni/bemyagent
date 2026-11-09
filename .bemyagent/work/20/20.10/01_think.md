# THINK — 20.10, what every arm could reach outside its own tree

**Heavy.** Four or more files, and the round changes the reading of six earlier ones.

## Context

20.9 found that the parent repository's `AGENTS.md` — *"Read `.bemyagent/docs/00-ai-rules.md`
before every task."* — and the session's `MEMORY.md` are injected into every arm as overriding
project instructions, and recorded it as *"it never opened that file"*. That sentence was written
from one arm's output. It was never measured.

The question this round asks is the one 20.9 should have asked next: **the instruction names a
path — did any arm follow it?** The path resolves two ways. Relative, against the arm's own
working directory, where in a control arm nothing exists. Absolute, against
`<repo>/`, where the real file sits — 107 lines, 14 KB, the shipped
protocol in full, a verbatim substring of `BEMYAGENT.md`.

### Context Saturation Check
- [x] Target files/paths — 201 subagent transcripts under this session's `subagents/`, one JSONL
      per agent, complete back to 14.8 on 2026-10-22.
- [x] Expected behavior — none. This is a census, not a hypothesis with a bar.
- [x] Constraints — no arms are launched. The entire round is reading what is already on disk.
- [x] Dependencies — the arm→round attribution comes from each round's own `setup*.py` `ARMS`
      dict and from the scratchpad directory prefix the launch prompt names (`r1413/q28`), never
      from a bare arm name: `q4` is a substring of `q46`.

## Approaches Considered

1. **Grep the transcripts for the parent path and count files.** Cheapest, and wrong twice: it
   cannot tell a tool call from the arm's own prose repeating a path, and it cannot tell the
   arm's own `00-ai-rules.md` from the parent's, because both bodies open with the same heading.
2. **Count only a `tool_use` input containing the parent absolute path.** What an arm *did*,
   not what it mentioned. Chosen.
3. **Re-run the arms with the injection removed.** The clean measurement, and it is the round
   this project still owes. It cannot be done from here: the injection is keyed to the session's
   project directory, not the arm's, so every arm launched from this session receives it however
   far outside the repository its tree lives.

## Selected Approach & Risks

One scorer over all 201 transcripts. For each agent: the launch prompt, the arm directory it
names, every `tool_use` input, and whether the `instructions` attachment was delivered. An arm
counts as having reached the parent repository only when one of its own tool calls contains the
parent absolute path.

### Pre-mortem
1. **The census says 45% and the conclusion is drawn from the number.** The number is not the
   finding; the direction of effect per round is. A control arm reading the protocol understates
   a benefit and inflates a harm; a clause arm reading the *unmutated* mirror defeats its own
   manipulation; an arm whose round mutates only `BEMYAGENT.md` is untouched by a mirror read.
   Each round must be read on its own mutation, and the write-up states the direction before the
   count.
2. **The needle cannot distinguish the arm's own copy from the parent's.** Guarded by matching
   the absolute path, which only the parent has, and never the body text, which both have.
3. **Arms go missing and the census looks clean because they were never counted.** Every round's
   arm list comes from its `setup*.py`; any arm with no transcript is printed as a hole, not
   dropped.

### Devil's Advocate
**The opposite reading: this is not contamination, it is the protocol's own Step 1 working.**
The sentinel line exists to be found and followed; an agent that reads it and obeys is behaving
exactly as designed, and what the census measures is compliance, not pollution. That reading is
right about the arm and wrong about the harness: the file it obeys its way into is not the one
the experiment installed. Both can be true, and the second is the one that decides whether a
verdict means what it says. Noted, not pivoted to.

## Verification Plan

- Attribute every arm launch in every round, with holes printed.
- Count a parent read only from a `tool_use` input.
- For the twelve no-protocol controls, check whether any TTEV artifact followed the read — a
  protocol in context that produces no ceremony is inert; one that produces ceremony is a
  treatment arm mislabelled.
- Name, per round, what its mutation touches, and from that the direction the contamination
  pushes its verdict.
- Three measurements not yet looked at, declared here before they are run: the **order** of the
  parent read against the arm's own protocol read; whether the independent **VERIFY agents** also
  reached the parent repository; and whether any agent read the parent's `docs/` beyond the
  protocol — `05-decisions-and-issues.md`, `06-implementation-plan.md`, this project's whole
  record of its own results.

## 🎯 Drift

Drift is declaring a past verdict void when the contamination could only have pushed it toward
the verdict already reached. A control arm handed the protocol and still producing nothing is
evidence *for* the treatment effect, not against it. The round that goes wrong here is the one
that converts an isolation defect into a retraction it does not support.

Second drift: scoring the arms' obedience as a protocol benefit. An arm reading a file this
harness did not install is a fact about the harness.

## ✅ Validation

1. Every arm in every round attributed or printed as a hole.
2. The read counted from a tool call, never from prose, never from body text.
3. Per round: what its setup mutates, and the direction of effect stated before the count.
4. The twelve no-protocol controls checked for TTEV artifacts.
5. Every claim this round corrects quoted as committed, then struck in place.

## 🔄 Pivot

If arms cannot be attributed to rounds without hand-transcription, stop and rebuild the
attribution from the `ARMS` dicts rather than typing a table. `obstacleThreshold` is 2.
