# THINK: Integrate the VERIFY step into the BEMYAGENT protocol

## Context
The user identified a gap in the TTEV flow: there is an entry gate (Context Saturation Check) but no exit gate after execution. The agent says "done" without self-evaluating against the CDM criteria defined in `02_tasks.md`.

The proposal is to add a fourth step: **VERIFY** (`04_verify.md`), which acts as a post-execution validation report, proportional to task complexity.

### Context Saturation Check
- [x] **Target files/paths** — Known: `00-ai-rules.md` §4 (TTE rules), `BEMYAGENT.md` (master template), `_template_think.md` (unchanged), `05-decisions-and-issues.md`, `06-implementation-plan.md`
- [x] **Expected behavior** — Clear: the flow becomes TTEV. After EXECUTE, the agent evaluates output against CDM criteria and produces a verdict BEFORE notifying the user.
- [x] **Constraints** — Defined: must not bloat the initial prompt excessively. Validation criteria stay in `02_tasks.md` (where CDM defines them). The `04_verify.md` is only the "report card" — it does not duplicate criteria.
- [x] **Dependencies** — CDM already integrated (Decision #9, task 4.5). No external dependencies.

## Approaches Considered

### A: VERIFY as a mandatory fourth step with a dedicated file
- **Pro**: Traceable, impossible to skip, clean separation (task = plan, execute = actions, verify = judgment)
- **Pro**: Hooks naturally into CDM — criteria are already there, verify evaluates them
- **Con**: One extra file per task (but only when CDM requires it)

### B: VERIFY as an additional section inside `03_execute.log`
- **Pro**: Fewer files, everything in one place
- **Con**: Mixes the retrospective log (what happened) with judgment (did it go well?). Breaks separation of responsibility.

### C: VERIFY as an optional layer external to the TTE flow
- **Pro**: No impact on the existing flow
- **Con**: If it's optional and outside the flow, it will be ignored. Not traceable. Discarded after discussion with the user.

## Selected Approach & Risks
**Approach A**: VERIFY as a fourth step with a `04_verify.md` file.

**Guiding principle**: The protocol defines the structure (a VERIFY moment exists), it does not prescribe the calibration (how deep to go). The human-agent pair calibrates through practice.

**Risks & Mitigations**:
- *Risk*: The agent produces ceremonial, useless verification reports → *Mitigation*: The human corrects, the agent adapts. This is the symbiotic loop.
- *Risk*: §4 becomes too long → *Mitigation*: The VERIFY rule is compact (5-8 lines), not a manual.

## Verification Plan
- The VERIFY rule is present in §4 of `00-ai-rules.md`
- `BEMYAGENT.md` is synced
- Decision #10 is registered
- Milestone 5.0 is opened in `06-implementation-plan.md`
- **Meta-test**: This very task (5.1) produces the first `04_verify.md` in the protocol's history
