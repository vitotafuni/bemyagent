# THINK — 16.1 Conversation log: does it get written, and does it capture anything new?

## The question

Issue #3 proposes an optional, harness-agnostic raw conversation log in the repo: user messages,
the agent's reply, and a `→` line naming what the turn produced. Appended as the conversation
happens, cited by THINK and decisions, never read at restore.

**The value is real and we proved half of it ourselves.** Milestone 15.12 found Kiro keeping its
transcript in `~/.kiro/sessions/*.jsonl` — outside the project, harness-owned, deletable,
unreadable by another tool — and we recorded that as external confirmation of *"conversation is
not storage"*. A log **in the repo** is that criticism turned into a design.

**Two objections, and the second shaped this round.**

1. *"Appended as the conversation happens"* is a behaviour-during rule, our worst-measured
   category. `03_execute.log` mandates exactly that cadence and is present in **0 of 10** cases
   on this repo's own history (Decision 21). The prior is bad and specific.
2. An agent writing the user's words *verbatim* is **reporting, not transcribing**. If it drifts,
   the "source to check" is corrupt and looks authoritative — worse than having none. The
   proposal's escape is a converter from the harness transcript, which is harness-specific: the
   very dependency it sets out to avoid. **You can have fidelity or agnosticism in one
   mechanism, not both.**

The owner's variant dissolves the second: **make the agent summarise rather than transcribe.** A
summary does not claim a fidelity it lacks. So verbatim and summary become two conditions rather
than one proposal and one objection.

## Context Saturation Check

| Item | Known? |
|---|---|
| What is proposed | yes — issue #3, and `drafts/prompt-logs.md` is the same document |
| The competing prior | yes — 0/10 on the one existing per-turn rule |
| The duplication risk | yes, and the issue names it itself: tools that copy prompts verbatim *"duplicate what THINK files already hold"* |
| Whether the harness can run it | **no — and this is the hard part.** Arms receive one prompt and run to completion; there is no conversation to log |
| What "captures something new" means | **assumption stated**: a request that changes the work but produces no task — a correction, a retraction — is the thing the issue says is lost today |

1 unknown resolved below, 1 assumption stated → continue.

## The instrument problem, and the fix

A single-prompt arm has no conversation, so a conversation log would have nothing to capture and
the round would measure nothing. **Arms must be two-turn**: send the task, take the hand-back,
then send a second message that is a *correction*, and let the arm continue. The second turn is
deliberately the case the issue names — a request that alters the work and would normally leave
no trace of itself anywhere.

This is the same two-phase shape 15.11 needs, built here first.

## Approaches considered

1. **Single prompt containing several sequential instructions.** Rejected: it simulates a
   conversation inside one turn, which is exactly the thing whose absence is under test.
2. **Only verbatim vs baseline.** Rejected after the owner's point: it would test the weaker of
   the two forms and leave the better one unmeasured.
3. **Chosen: 3 conditions × 3, two turns each** — baseline, verbatim log, summary log.

## Pre-mortem

1. **Nothing is logged in either treatment**, and the round reduces to confirming the 0/10 prior.
   *That is a result*, and a cheap one: it would mean the log only exists where the harness
   produces it, and the proposal shrinks to *"declare where your harness transcript lives"* —
   smaller, still useful, far cheaper.
2. **The log is written but duplicates the TTEV files**, adding bytes and no information. The
   issue names this failure itself, so it is scored, not discovered.
3. **The second turn never reaches the arm** — orchestration failure rather than a finding.
   Mitigation: verify each arm actually received and acted on turn 2 before scoring it.

## Devil's advocate

Do nothing and tell the reporter to point the protocol at the harness transcript they already
have. It is one settings field, no new write rule, and it sidesteps objection 1 entirely. Not
pivoting, because it abandons every project whose harness keeps no transcript or an unreadable
one — but if this round comes back 0/3 on both treatments, **that is the proposal that survives**,
and the round will have bought it honestly.

## Assumption carried forward

One model, one harness, one task shape. Same external-validity limit named on 2026-10-20.
