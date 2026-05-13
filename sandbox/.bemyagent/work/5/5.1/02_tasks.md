# Task: Integrate the VERIFY step into the BEMYAGENT protocol

## Checklist

- [x] **Task 1: Update `00-ai-rules.md` §4 — Add the VERIFY rule**
  - Add the VERIFY block after CDM in §4 of the sandbox file.
  - The flow becomes: THINK → TASK → EXECUTE → VERIFY.
  - `04_verify.md` is the VERIFY report: evaluates output against CDM criteria.
  - Do not prescribe calibration — the protocol says THAT verify exists, not HOW to calibrate it.
  - ✅ **Validation**: §4 contains the VERIFY rule. The flow is described as TTEV.
  - 🎯 **Drift**: If the VERIFY rule exceeds 10 lines, we are over-engineering. Compact it.

- [x] **Task 2: Sync `BEMYAGENT.md` with the sandbox**
  - Copy the updated §4 into the master template embedded in `BEMYAGENT.md`.
  - ✅ **Validation**: Diff between sandbox `00-ai-rules.md` §4 and `BEMYAGENT.md` embedded §4 → zero delta on VERIFY content.

- [x] **Task 3: Register Decision #10 in `05-decisions-and-issues.md`**
  - Add to the index table and as an inline decision.
  - ✅ **Validation**: The decision is consistent with the actual discussion (not fabricated).

- [x] **Task 4: Update `06-implementation-plan.md`**
  - Open Milestone 5.0 with task 5.1.
  - ✅ **Validation**: The plan reflects the actual state.

- [x] **Task 5: Create `04_verify.md` for THIS task (meta-test)**
  - First VERIFY in the protocol's history.
  - Evaluate the CDM criteria defined above.
  - Produce verdict: PASS / PASS_WITH_CAVEATS / FAIL.
  - 🎯 **Drift**: If the verify becomes longer than the tasks themselves, we are doing it wrong.
  - 🔄 **Pivot**: If the meta-test reveals the verify format doesn't work, propose revision before committing.

- [x] **Task 6: Stage and commit**
  - Stage all modified files.
  - ✅ **Validation**: `git status` clean after commit.
  - 🎯 **Drift**: Only files in `sandbox/` and `BEMYAGENT.md` should appear in the diff.
