# Think: Evolution Modules (Context Probing, Session Restore, Capability Handshake)

## Context
- The user proposed integrating three functional modules inspired by DEVPROTOCOL into BEMYAGENT: Context Probing, Capability Handshake, and Adaptive Session Restore.
- The goal is to evolve BEMYAGENT from a "task executor" to a "conscious collaborator" without sacrificing its zero-friction philosophy.

### Context Saturation Check
- [x] **Target files/paths** — Known: `_template_think.md`, `00-ai-rules.md` (sandbox + master), `BEMYAGENT.md`
- [x] **Expected behavior** — Clear: integrate modules inside existing TTE phases, not as new gates
- [x] **Constraints** — Defined: no emoji (human-editable), no separate session summary file (token cost), no bureaucratic gates
- [x] **Dependencies** — Mapped: no external dependencies, pure protocol documentation changes

## Approaches Considered

### A. Separate Layers (DEVPROTOCOL style)
- **Pro:** Clean separation of concerns
- **Con:** Creates 3 new interruption points (Context Probing → Capability Handshake → THINK → TASK → EXECUTE). Kills BEMYAGENT's zero-friction identity.

### B. Merge Into Existing TTE Phases (chosen)
- **Pro:** No new gates. Context Probing becomes part of THINK, Capability Handshake merges into TASK, Session Restore is an algorithm upgrade to §2.
- **Con:** Slightly more complex individual phases.

### C. Optional Plugin System
- **Pro:** Maximum flexibility (user enables what they want)
- **Con:** Premature engineering for a documentation protocol.

## Selected Approach & Risks
- **Chosen:** Approach B — Merge into existing TTE phases.
- **Key insight:** The difference between BEMYAGENT and DEVPROTOCOL is not *what* checks you do, but *where* you put them. DEVPROTOCOL puts controls *between* user and agent (barriers). BEMYAGENT puts them *inside* the agent's thinking process (cognition).
- **Risk:** Template may become too verbose → mitigated by keeping checklist minimal (4 items).

## Decisions Made During Execution
1. **Session Summary file rejected** — User correctly argued that `work/` + `06-implementation-plan.md` already contain enough state to reconstruct context. Solution: smarter restore algorithm, not a new file.
2. **ALWAYS_ASSUME override rejected** — User argued humans are lazy and won't read docs. Solution: Quick Reference Card printed at end of bootstrap, when user is most receptive.
3. **Emoji markers rejected** — User requested `[x]`/`[ ]` checkboxes instead of ✅/❓ for human editability and keyboard accessibility.

## Verification Plan
- [x] `_template_think.md` has Context Saturation Check as checklist
- [x] `00-ai-rules.md` §2 has 2-step restore algorithm
- [x] `00-ai-rules.md` §4 references the checklist rule
- [x] `BEMYAGENT.md` master template synced with all changes
- [x] `BEMYAGENT.md` Step 4 includes Quick Reference Card
- [ ] Test on a real task in sandbox (next session)
