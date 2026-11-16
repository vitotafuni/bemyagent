# 21.1 — THINK

## Context
Spec: `docs/specs/resume-block.md`. The question is not whether a resume block is useful (N=1 says yes) but **what makes an agent write it without being asked**, in a form no harness has to supply. Two candidates: **E**, an event the agent must recognise; **R**, the end of every reply, with the block closing the reply (the user's proposal, 2026-11-12). The record predicts both outcomes for R — per-turn writes at zero twice, forced artifacts in the deliverable at 3/3 — so it has to be measured.

### Context Saturation Check
- [x] **Target files/paths** — `work/21/21.1/` apparatus; arms under this session's scratchpad `r211/`. Nothing in `BEMYAGENT.md` changes in this leaf.
- [x] **Expected behaviour** — the readings table in `02_tasks.md`.
- [x] **Constraints** — the six questions and four rules of `harness/README.md`; clean arms only by `claude -p` from inside their tree, launched by the user (auto mode refuses the launch).
- [ ] **Dependencies** — `claude -p --resume <id>` as the carrier of a second user turn is **assumed, never run here**. One unknown → proceed, with a pilot arm before the round and a check that fails loudly.

## The six things (harness/README)
0. **Already run?** No. No two-session round exists (`05`:401; README: *"has never been run"*). 16.1 had two turns in one context, relayed by a coordinator; 20.9 resumed trees but tested a false bug report.
1. **Regime and control.** Sonnet, steady state: protocol installed, sentinel in `CLAUDE.md`, a prompt that does not name the protocol (20.11: ceremony 3/3 there). Control K is in it — the shipped rules, same seed.
2. **Rejection kind.** R re-tests a *null*, not a harm or a redundancy rejection: the cadence finding stands or is narrowed to "off-screen writes".
3. **Occasion.** Turn 2 hands every arm something for later and forbids doing it now; the reset is real. Guard: an arm that implements it at once has no occasion and is counted out, not counted as a miss.
4. **Observations.** One turn-2 occasion per arm, three per condition: only 0/3 against 3/3 licenses *mechanism*; anything else is under-powered and is said so. R's footer has three occasions per arm, nine per condition.
5. **Cost.** Nine arms × three calls + one pilot. Priced by the executor from 20.11's silent-prompt arms before launch and written in `03_execute.log`; if it exceeds ~3 M weighted tokens the round is cut to K and R and E is recorded as unrun.

## Approaches Considered
- **A. Three conditions K · E · R, two sessions each** (chosen). Sets the two trigger philosophies against each other on the one occasion that separates them.
- **B. K · V · R**, V writing only at a task's verdict (the draft's first shape). Dropped: V has no occasion at turn 2, so its miss is predictable without spending arms.
- **C. The hook as a fourth arm.** Dropped: proven already (16.2), and tied to one CLI.
- **D. Agent-tool arms with SendMessage for turn 2**, as 16.1. Dropped: inherits this repo's `AGENTS.md` (58 of 118), and a relayed message is not the user's.

## Selected Approach & Risks
- **Seed**: 20.11's P seed (fixture + protocol + seeded docs + one-line `CLAUDE.md`). E and R differ from K in three places only, applied identically to `00-ai-rules.md` and to the copy embedded in `BEMYAGENT.md`: the rule paragraph after `**Git:**`, a clause in §2 Quick Resume, a word in the Write Gate exemption; plus a `## Resume here` block seeded at the top of `06` (a project in steady state has one). The treatment is that block of four things, compared as a block.
- **Session 1**: turn 1 = 20.11's `prompt.txt` verbatim (the scoreboard). Turn 2, by `--resume`: *something for later with a constraint, not now*. **Reset** = a new `claude -p` in the same tree: *"Carry on from where we left off."*
- **Rule 1 (mechanism, not outcome)**: the headline is *turn-2 intent on disk after turn 2*, read from a snapshot. Whether session 2 builds it is the downstream reading.
- **Rule 4 (harm)**: R's cost per reply, its footer lines, and any block that says something false about the tree.
- Estimated token cost: high for the round, low for the apparatus → apparatus by a Sonnet subagent; VERIFY on the strongest tier, by an agent that did not build it (§4 Model switching, Who verifies). *(Corrected 2026-11-12: first written as "a second Sonnet"; the user caught it.)*

**Pre-mortem**
1. *`--resume` starts a new context or drops the turn.* → pilot arm `q900`; the launcher aborts an arm whose turn-2 transcript does not hold both user messages.
2. *The harness's own memory carries the state across the reset* (auto-memory is keyed to the arm's path and survives a new process) and the block gets the credit. → before session 2 the launcher moves the arm's memory folder aside and records that it existed; that is a finding, not noise.
3. *The scorer reads its own hope*: a regex for "reset" matches the seeded docs or the turn-1 work. → every reading is a **difference between snapshots**, and the scorer is run on built positive and negative trees before any arm exists.

**Devil's Advocate** — skip the round and ship R on the user's judgement: it is cheap and visible, and the user would see it fail. Not taken: the two prior per-turn rules also looked obviously fine, and a footer that prints while the file stays stale is the failure nobody sees.

## Verification Plan
Before launch: seeds differ only where declared (`diff -r`), prompts stored verbatim, scorer right at both ends, launcher dry-run with a stub in place of `claude`. After launch: certificate on all three calls of every arm, then the readings, then an independent reader.
