# Resume block
**Status**: specced

## Description
A three-line short-term memory at the top of `06-implementation-plan.md` — `Task:`, `Intent:`, `Next:` — overwritten whole, never appended, so that a context reset costs the user nothing: no *"write it all down first"*, and a fresh session resumes from the block. It holds only what no other file holds — what the user wants **now** and the immediate to-do — plus a pointer to the leaf in progress; it copies no status. Second half: when the work changes task, one line tells the user the state is on disk and a fresh session starts cheaper. Never a stop.

Origin: the user, `.bemyagent/log/2026-11-11.md` 15:37 and chat 2026-11-12. Promoted from `drafts/resume-block-at-task-switch.md`.

## The open question: what triggers the write
| | Trigger | For | Against |
|---|---|---|---|
| **E** | an event: a task's verdict, **or** a user message that changes what they want or adds something for later | the only shape that has ever landed (Decision 21: 1/3 → 3/3) | the agent must classify the message; a rule that depends on classifying an event fails on the next unanticipated one (`05`:248) |
| **R** | the end of **every** reply (the user's proposal, 2026-11-12), and the reply ends with the three lines | nothing to classify; needs only a file write and a reply, so no harness is assumed; the footer is in the deliverable and visible, so a misread intent is corrected at once | the two per-turn rules measured so far are at zero (16.1: 0/9 second turns; `03_execute.log` next action 0/10); three lines of noise per reply |
| hook | the harness, per turn (16.2) | the only per-turn mechanism proven | ties the protocol to one CLI — the thing R exists to avoid; *BMA cannot ship the hook* |

What the record does **not** hold: no rule forcing an output in every reply has been measured. 16.1's payload was an append to a log nobody reads, written off-screen; R's payload is in the reply itself. `harness/README.md` rule 3 — *a forced output only works when the output IS the deliverable* — predicts the opposite of 16.1. That is an open empirical question, not a settled one, and 21.1 asks it.

## Critical review
1. **Overlap** — `06`'s hand-written `Resume here` (N=1: the 2026-11-12 session resumed from ~2 KB of it inside a 63 KB plan). `activeContext.md` was rejected (Decision 18) for hand-sync drift, on the premise that `03_execute.log`'s next action covered the need; that premise measures 0/10 → rejection withdrawn. Drift is answered by holding no copied status.
2. **Cost** — about 60 words of rule plus 3 lines on the restore path; R adds one write and three lines to every reply. Benefit must show as a resumed session, not as a block that exists.
3. **Weakness** — a second place where *next* lives beside the plan rows; R's footer taxes guarantee 1 on every reply. **Unanswered** — does a tracked block survive §8 worktrees without a merge conflict per task?
4. **Minimal alternative** — no rule: a *checkpoint* prompt among README's human-invoked routines. Costs nothing and keeps the user asking, which is the complaint.

## Acceptance criteria
- [ ] A two-session round with a context reset between the sessions has run on certified clean arms, readings fixed before launch (21.1).
- [ ] The trigger that ships separates from control on *turn-2 intent reached disk* (0/3 → 3/3, or resolved at higher N), and the fresh session acts on it.
- [ ] The trigger that loses has a line in `decisions/rejected.md` with the premise it rests on.
- [ ] Rule text in `BEMYAGENT.md` and `00-ai-rules.md`: the block, §2 Quick Resume reading it first, the Write Gate exemption; net restore cost stated in tokens.
- [ ] This repo's `Resume here` conforms to the shipped form.
- [ ] The reset suggestion at a task switch is measured through a proxy artifact, or recorded as untested — never shipped as working.
- [ ] Glossary and README updated.

## Open questions
- Does `claude -p --resume <id>` deliver a real second user turn? Untested here; 21.1 pilots it on one arm.
- Outside Claude Code: R assumes nothing, but nothing has measured it there.
