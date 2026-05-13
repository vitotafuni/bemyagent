# Task: Evolution Modules Integration

## Checklist

- [x] **Task 1: Strategic Analysis**
  - Evaluate Context Probing, Capability Handshake, Adaptive Session Restore against existing TTE architecture.
  - Produce evaluation artifact with phased implementation plan.
- [x] **Task 2: Context Probing → THINK template**
  - Add Context Saturation Check to `_template_think.md`.
  - Initially used emoji (✅/❓), then replaced with `[x]`/`[ ]` checkboxes per user feedback.
- [x] **Task 3: Adaptive Session Restore → §2 of rules**
  - Rejected `_session_summary.md` approach (token cost not justified).
  - Implemented 2-step restore algorithm (Quick Resume → Full Restore) in `00-ai-rules.md` §2.
- [x] **Task 4: Sync master template**
  - Update `BEMYAGENT.md` embedded `00-ai-rules.md` with same §2 and §4 changes.
  - Update `BEMYAGENT.md` `_template_think.md` section with checklist version.
- [x] **Task 5: Quick Reference Card**
  - Added post-bootstrap cheat sheet in `BEMYAGENT.md` Step 4 showing modes and Context Probing behavior.
  - Replaces the rejected `ALWAYS_ASSUME` flag approach.
- [x] **Task 6: Update sandbox work/ (dogfooding)**
  - Create `work/4/4.3/` with 01_think, 02_tasks, 03_execute.
  - Update `06-implementation-plan.md`.
