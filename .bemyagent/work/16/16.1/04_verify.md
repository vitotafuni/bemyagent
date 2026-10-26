# VERIFY — 16.1 conversation log

Verdict: **FAIL for the proposal, PASS for the problem it names.** The gap issue #3 describes is
real and larger than reported — **7 of 9 arms lost the correction entirely**. The proposed remedy
does not close it: **0 of 9 logs contain it.**

## The result

| | a (baseline) | b (verbatim) | c (summary) |
|---|---|---|---|
| **WRITTEN** — a log exists for turn 1 | 0/3 *(correct, no rule)* | **1/3** | **3/3** |
| **TURN 2** — the correction is in the log | — | **0/3** | **0/3** |
| the correction reached a distilled file instead | 0/3 | 0/3 | 2/3 |
| **the correction left no durable trace at all** | **3/3** | **3/3** | 1/3 |

**Overall: 7/9 lost it.** A request that changed the work, altered three test assertions and
updated the code map vanished from the repo the moment the session ended.

## Finding 1 — the problem statement is confirmed, and it is the strongest part of the issue

Issue #3 says requests that never become a task *"are lost with the chat"*. Measured: **7 of 9**.
Not an edge case. Two arms caught it, both by accident of where they happened to be writing —
c-1 in `03_execute.log`, c-3 in `micro.log` — and neither is a mechanism anyone could rely on.

## Finding 2 — the remedy fails on the cadence, exactly as the prior predicted

**0/9 logs carry turn 2.** Four logs exist and every one holds a single entry for turn 1, between
one and three lines. **The log is created at bootstrap and then abandoned.**

This is the pre-registered pivot, fired verbatim: *"If TURN 2 is 0/3 while turn 1 is 3/3: the log
is written once at the start and abandoned. That is compliance without the mechanism and it must
not be reported as a positive."*

And it is the 0/10 prior landing precisely where `01_think.md` said it would. `03_execute.log`
mandates a per-turn write and carries it in 0 of 10 cases on this repo; a second per-turn write
rule behaves identically. **A cadence is not a trigger**, and this is now measured twice.

## Finding 3 — told to write verbatim, the agent summarised. This is the objection, caught live

b-1 was the one arm in the verbatim condition that wrote anything. Its entire log line:

> `Turn: wire session.js into index.js (POST /api/sessions, GET /api/online)`

The user's message was four clauses long and said none of that. **The "verbatim" record is a
reconstruction wearing the label of a transcript** — the failure mode named in `01_think.md`
before the round, and the reason a log written by the agent cannot be the source of truth a
disagreement gets checked against. Visible only because the file was read; the scorer had counted
it as WRITTEN.

The owner's variant is vindicated by the same datum: **summary beats verbatim on creation, 3/3
against 1/3**, and a summary at least does not claim a fidelity it lacks.

## What this does NOT establish

- **Whether the log rule improved recording elsewhere.** The two arms that captured the
  correction in a distilled file were both in condition c (2/3 vs 0/3 vs 0/3). Below the
  separation threshold at N=3 — an observation, not a result.
- **Anything about a harness-written log.** Every finding here concerns a log the *agent* must
  remember to append. A transcript the harness writes has none of these failure modes, and none
  of this evidence touches it.

## Caveats

1. **Two turns, not a long conversation.** A cadence that fails on turn 2 would not improve on
   turn 20, but that is an inference, not a measurement.
2. **One model, one harness, one task.**
3. **N=3 per condition.** WRITTEN separates cleanly between b and c (1/3 vs 3/3); TURN 2 is
   unanimous at 0/9, which needs no threshold.

## Recommendation

**Reject the proposal in the form proposed.** Not because the problem is imagined — it is
measured at 7/9 — but because an agent-appended per-turn log is the one mechanism this protocol
has repeatedly shown it will not maintain, and the one arm that tried produced a summary labelled
as a transcript.

**What survives is the alternative named in `01_think.md`'s devil's advocate**, and the round
bought it honestly: **declare where the harness's own transcript lives.** One `settings.json`
field, no write rule, no cadence to forget — the harness writes it whether the agent remembers or
not. It abandons projects whose harness keeps no transcript, which is a real cost and must be
said; but it is the only form of this idea that survives contact with how agents actually behave.

The problem remains open and worth returning to. The remedy does not.
