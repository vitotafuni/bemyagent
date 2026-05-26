# Task: Test Context Probing & CDM Validation + BEMYAGENT.md Sync

## Checklist

- [x] **Task 1: Create TTE artifacts for 4.5**
  - Write `01_think.md` and `02_tasks.md` for `work/4/4.5/`.
  - *(CDM: None — simple file creation, no dependencies)*

- [x] **Task 2: Sync CDM rule into BEMYAGENT.md master template**
  - Copy the CDM block from `00-ai-rules.md` §4 into the corresponding section of `BEMYAGENT.md`.
  - Ensure the embedded `00-ai-rules.md` inside `BEMYAGENT.md` matches the sandbox version.
  - ✅ **Validation**: Diff between sandbox `00-ai-rules.md` §4 and `BEMYAGENT.md` embedded §4 shows zero delta on CDM content.

- [x] **Task 3: Update implementation plan**
  - Mark 4.5 as `done` in `06-implementation-plan.md`.
  - Add a new task 4.6 for the CDM integration if needed, or close Milestone 4.
  - *(CDM: None — single file update)*

- [x] **Task 4: Stage and commit all changes**
  - Stage: `00-ai-rules.md`, `05-decisions-and-issues.md`, `BEMYAGENT.md`, `work/4/4.5/*`, `06-implementation-plan.md`
  - 🎯 **Drift**: If `git diff --staged` shows files outside `sandbox/` or `BEMYAGENT.md`, something is wrong.
  - ✅ **Validation**: `git status` shows clean working tree after commit.
  - 🔄 **Pivot**: If merge conflicts appear (unlikely on solo repo), resolve manually before committing.

## CDM Test Notes
> This task list intentionally uses mixed CDM levels to validate the threshold concept:
> - Tasks 1 & 3: **No CDM** (simple, single-file)
> - Task 2: **CDM-Lite** (Validation only — medium complexity, consistency check)
> - Task 4: **CDM-Full** (Drift + Validation + Pivot — involves git operations with side effects)
>
> **User feedback requested:** Is this density level comfortable for validation, or does it feel like noise?
