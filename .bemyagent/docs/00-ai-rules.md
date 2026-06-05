# AI Rules & TTE Workflow

## 1. Self-registration (do once per project)
If this project does not yet have your tool's native rule file (e.g. `.amazonq/rules/`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`), create it now with this content:
```
Read docs/00-ai-rules.md before every task.
IF about to create or modify any file inside .bemyagent/, THEN:
  1. Re-read the Routing Table in docs/00-ai-rules.md §3
  2. Output: "PROTOCOL_CHECK: target=[file], reason=[why]"
  3. Proceed only after step 2
```

## 2. Session Restore
If this is a new session or context was lost:

**Step 0 — Pending Upgrade Check:**
If `upgrade-plan.md` exists in the `.bemyagent/` root, a protocol upgrade was started but not completed. Read the plan and present it to the user for approval before doing any other work.

**Step 1 — Quick Resume (try this first):**
1. Read `docs/06-implementation-plan.md` to identify the active milestone and task number.
2. Read the `02_tasks.md` inside the most recent `work/X/X.Y/` folder matching that task.
3. If the checklist clearly shows what's done and what's pending, you have enough context. Confirm the status with the user and proceed.

**Step 2 — Full Restore (only if Step 1 is insufficient):**
Read in order: `docs/01-overview.md` → `docs/02-architecture.md` → `docs/05-decisions-and-issues.md`.
Then use the Routing Table (§3) to lazy-load any additional context needed for the task.

Ask the user to close unnecessary tabs.

## 3. Routing Table & Lazy Loading
**Lazy Loading Principle:** NEVER read files inside `decisions/`, `specs/`, or `drafts/` during initial context restore. They must only be loaded on-demand when explicitly required by the task.

Before starting any task, read:
| Task involves | Read first (On-Demand) |
|---|---|
| Any code change | docs/03-code-map.md |
| Creating/modifying any file in docs/ or work/ | docs/06-implementation-plan.md |
| Architecture or new service | docs/02-architecture.md |
| Bug or unexpected behaviour | docs/05-decisions-and-issues.md |
| New feature | docs/specs/[feature-name].md |
| Unscoped idea | docs/drafts/[idea-name].md |
| Tech dependency or version | docs/04-tech-stack.md |

**Conceptual Map Pattern:** Files referenced in the Routing Table (`01-overview.md`, `02-architecture.md`, `03-code-map.md`) act as lightweight conceptual maps. They MUST contain only the logical tree and pointers to detailed fragments — never inline specs or extended explanations. When navigating fragmented documentation, always read the map first (low cost), then fetch only the specific fragment needed.

**Context Slicing Rule (Large File Handling):**
Before reading any file in `docs/` or `work/`, estimate its size (e.g., line count via terminal).
If the file exceeds `contextSlicingThreshold` lines (defined in `settings.json`, default: 200):
1. **Do NOT read the entire file.** Use `grep` or targeted search to extract only the sections relevant to the current task, with a context window of ~20-30 lines around each match.
2. **If the initial extraction is insufficient**, progressively expand the context window (e.g., 50-80 lines) until you have enough information.
3. **Only as a last resort**, read the entire file.
4. **If you repeatedly need large portions of the same file across multiple tasks**, propose fragmentation to the user (e.g., splitting `03-code-map.md` into `03-code-map/frontend.md` and `03-code-map/backend.md`).

**Protocol Anchoring Gate (Write Gate):**
Before creating or modifying ANY file inside `docs/` or `work/`, the agent MUST:
1. Re-read the Routing Table above to identify if the content belongs in an existing file.
2. Output in chat: `PROTOCOL_CHECK: target=[existing file or new file path], reason=[brief justification]`
3. If the check reveals the content belongs in an existing file, update that file instead of creating a new one.
4. Only then proceed with the file operation.

This gate applies to file *creation* and *structural modifications*. It does NOT apply to normal TTEV workflow writes (appending to `03_execute.log`, writing `04_verify.md` for the current task).

## 4. Fractal TTEV Workflow (work/ namespace)
Tactical memory is structured as a **Hierarchical Task Network (HTN)**. It is segmented by Task Numbers matching `06-implementation-plan.md` (which acts as the high-level Table of Contents).

**The Rule of Decomposition (Divide et Impera):** 
If a task is too complex, DO NOT execute it directly. Decompose it into sub-tasks (e.g., if `work/1.0/` is too big, create `work/1.1/` and `work/1.2/`). Solve each sub-component in isolation, verify it individually, then integrate gradually. If a sub-task itself proves too complex during EXECUTE, fragment further into nested directories (e.g., `work/7/7.1/7.1.1/`).

**Hierarchical Work Structure:**
Work directories follow the task hierarchy from `06-implementation-plan.md`:
- **Level 1** — Milestone: `work/<N>/` (e.g., `work/4/`)
- **Level 2** — Task: `work/<N>/<N.Y>/` (e.g., `work/4/4.1/`)
- **Level 3** — Sub-task (optional): `work/<N>/<N.Y>/<N.Y.Z>/` (e.g., `work/4/4.1/4.1.1/`)

A directory is a **leaf node** if it contains TTEV files (`01_think.md`, `02_tasks.md`, etc.). A directory is a **branch node** if it contains only subdirectories. **Maximum nesting depth: 3 levels.** If a sub-task at level 3 still needs decomposition, it's a sign the milestone itself should be re-scoped.


For any leaf node (atomic task):
- **THINK (Strategy):** Write to `work/X.Y/01_think.md` using `_template_think.md`. You MUST complete the **Context Saturation Check** checklist. If 2+ items are unchecked (missing/ambiguous), STOP and ask the user before proceeding. If 0-1 are unchecked, state your assumption explicitly and continue.
  **Advanced Reasoning (for Standard and Heavy tasks):**
  - *Pre-mortem:* Before finalizing the plan, assume the task has failed. Identify the 2-3 most likely causes of failure and adjust the plan to mitigate them proactively.
  - *Devil's Advocate:* Challenge your own chosen approach. Generate at least one radically different alternative. If it's clearly superior, pivot. If not, briefly document why the original approach survives the challenge.
- **TASK (Planning):** Write to `work/X.Y/02_tasks.md` (or `.json`). Create a strict checklist (`todo`, `done`, `verified`).
- **EXECUTE (Action):** Write to `work/X.Y/03_execute.log`. Implement the code, log terminal outputs and errors.
- **VERIFY (Validation):** Write to `work/X.Y/04_verify.md`. Evaluate the execution output against the CDM criteria defined in `02_tasks.md` and produce a verdict BEFORE notifying the user. See **Symbiotic Validation** below.

**Handoff Principle:** `01_think.md` and `02_tasks.md` are NOT retrospective logs. They are **serialized execution plans** designed to be executable by a fresh agent with zero conversation context. Write them BEFORE executing, not after. `03_execute.log` and `04_verify.md` are the only retrospective files.

**Contextual DNA Mapping (CDM):**
During the TASK phase, apply DNA mapping based on task size/token cost estimation rather than purely structural complexity. *Hint: use terminal commands to estimate token counts (e.g., word or line count) without loading full files into context.*
- **Short/Micro tasks** (typo fixes, single simple edit): No CDM needed. **Proportional Compression:** IGNORE the standard `_think` and `_verify` templates. Write a maximum of 1-2 lines for both `01_think.md` and `04_verify.md`.
- **Standard tasks** (routine development): Add `✅ Validation` only.
- **Long/Heavy tasks** (repetitive changes, complex logic, high token cost expected): Add full CDM:
  - `🎯 Drift`: What constitutes going off-track for THIS specific task.
  - `✅ Validation`: The objective evidence of success.
  - `🔄 Pivot`: The pre-defined condition to stop and propose an alternative.
    **Dynamic Pivot Rule:** During EXECUTE, if you encounter unexpected obstacles exceeding `obstacleThreshold` (defined in `settings.json`) or if the task is consuming significantly more time/tokens than expected, STOP execution. Re-read your `01_think.md` "Approaches Considered" section and evaluate whether a previously discarded approach is now more viable. If `interactiveMode` is `true`, present the pivot proposal to the user before switching. If `false`, pivot and report the change in the next status update.
Do not execute a heavy task without mapping the DNA onto it.

**Symbiotic Validation:**
After EXECUTE and BEFORE notifying the user, evaluate your output against the CDM criteria defined in `02_tasks.md`. Write the result to `04_verify.md`.
- For each CDM criterion (✅ Validation, 🎯 Drift, 🔄 Pivot), state the result and the evidence.
- Produce a verdict: **PASS** (proceed silently), **PASS_WITH_CAVEATS** (present friction points to user, await decision), or **FAIL** (attempt one self-correction; if it fails again, escalate to user).
- **Verification Depth:** If `strictVerification` is `true` in `settings.json`, perform a deep analysis (edge cases, performance, architecture alignment). If `false`, perform a light check (compilation, basic task success).
- **Auto Commit:** If `autoCommit` is `true` in `settings.json` and the verdict is PASS, automatically execute or propose a `git commit` with a message like `feat: [X.Y] ...`.

**Pacing & Handoff Configuration:**
*Interactive Mode:* **Determined by `settings.json` (`interactiveMode` key)**. The user can override this by saying *"Enable/Disable interactive mode"*, which should trigger an update to the JSON file.
- **if false (SEAMLESS)**: Proceed through THINK, TASK, EXECUTE, and VERIFY automatically. If VERIFY yields PASS → notify user. If PASS_WITH_CAVEATS or FAIL → stop and present findings.
- **if true (INTERACTIVE)**: You MUST STOP after the THINK phase and after VERIFY, waiting for human approval at both gates.
- **AUTO-CLI**: If `autoModelSwitching` is `true` in `settings.json` and you have CLI capabilities, switch to the optimal models for each phase (e.g., THINK → Opus/Big model, TASK → Sonnet/Middle model, EXECUTE → Haiku/Fast model, VERIFY → Middle model).
*Rule:* Prune your context window before EXECUTE. Only load files strictly required for that specific leaf node.

**Git Rules:**
- Before committing, verify that a corresponding `work/X/X.Y/` folder exists for the current task with `01_think.md` and `02_tasks.md` written BEFORE execution began.
- Before starting EXECUTE, always suggest a clean, atomic Git commit for the previous task with a clear message based on the task number (e.g., `git commit -m "feat: [1.1] add user auth"`).

## 5. Anti-Hallucination & Safety Rules
- **Always Verify:** Prima di ogni modifica a file esistenti, leggi SEMPRE il contenuto attuale del file. Mai assumere che una funzione o variabile esista senza averla vista nel context.
- **Dependencies:** Se devi aggiungere una dipendenza, prima aggiorna `04-tech-stack.md` e proponi `npm install` / equivalente.
- **Critical Review Protocol:** When evaluating a draft, proposal, or any input that suggests changes to documentation or protocol (including `00-ai-rules.md` itself):
  1. **Overlap Check:** Search the target file(s) for semantic overlap. If the concept is already covered (even implicitly), prefer a surgical edit to the existing text over adding a new rule.
  2. **Cost/Benefit:** Quantify the cost of the proposal (e.g., lines added to `00-ai-rules.md` = tokens consumed at every session restore). The benefit must clearly outweigh this recurring cost.
  3. **Challenge:** Identify at least one structural weakness and one unanswered question before recommending integration.
  4. **Minimal Alternative:** Always propose the smallest possible change that achieves the same goal.

## 6. Coding & Maintenance Rules
- **Surgical Scope:** Touch only files directly related to the task. Do not refactor adjacent code, alter unrelated comments, or normalize formatting across the repo.
- Never remove existing code/tests unless explicitly asked.
- Make changes in one edit, not incrementally. Write minimal code.
- Match existing code style. 
- **Output Brevity:** Minimize verbose explanations unless explicitly requested. In chat responses, be direct: state results, open questions, and next steps only — do not recap actions the user can already see, do not preface with what you are about to do, and do not add filler or pleasantries. Prefer direct file modifications over describing changes in chat. Keep `03_execute.log` entries ultra-synthetic: command → result → next action. No prose. When showing code changes, use minimal diffs rather than repeating entire file contents. When producing evaluations or reviews, focus on gaps, overlaps, and minimal actions — never paraphrase the input.
- **Language:** Documentation language is defined in `settings.json` (`language` key). The user can override it at any time by saying *"Set documentation language to [language]"*, which should trigger an update to the JSON file. Chat interaction language and documentation language are independent.
- **CRITICAL:** Update `03-code-map.md` and `05-decisions.md` in the SAME response as any change. This includes decisions made during discussion, even without code changes (e.g., rejected approaches, architectural choices). Use `drafts/` for unresolved ideas.
- `specs/` files: tick acceptance criteria checkboxes as they are completed.
- `drafts/` files: promote to `specs/` when ready to build, delete the draft.

## 7. Monthly audit prompt
Run this with your AI assistant once a month:
> "Compare `03-code-map.md` against the real file structure and report any drift.
> Check `01-overview.md` env vars against actual config files (look for missing vars).
> Verify files ignored by `.gitignore`.
> Check if test coverage is still aligned with recent code changes.
> List any decisions made recently not yet in `05-decisions-and-issues.md`."

## 8. Protocol Updates & Migration Rules
When updating or migrating a project to a new version of BEMYAGENT:
- **Use Atomic Operations:** When migrating existing documentation or folders, ALWAYS use atomic copy/move operations (single commands that act on entire directories, not file-by-file enumeration). Manual reconstruction leads to omission.
- **Prevent Name Collisions:** Before bootstrapping or copying new protocol files, scan the destination directory for filename collisions with existing user documentation.
- **Safe Resolution:** If a collision exists, NEVER overwrite the user's files. Pause execution to ask the user, or safely move the conflicting files to an `archived/` or `project_docs/` folder. User documentation and protocol documentation should remain clearly separated.

## 9. Multi-Agent Parallelism
When multiple agents work on the same project concurrently:
1. **Isolate via `git worktree`:** Each agent works in a dedicated worktree on its own branch.
   ```bash
   git worktree add ../project-task-X.Y -b bma/X.Y
   ```
2. **One branch per task:** Branch naming follows the task number: `bma/1.1`, `bma/1.2`, etc.
3. **Full autonomy on branch:** Each agent follows the standard TTEV workflow and is free to update all files (code-map, decisions, source) without coordination.
4. **Human dispatches:** The user opens a separate IDE/terminal session per worktree and assigns tasks. There is no automated orchestrator.
5. **Merge to main:** After completion, branches are merged via PR or direct merge. The human resolves conflicts.
6. **Cleanup:** `git worktree remove ../project-task-X.Y` after merge.
