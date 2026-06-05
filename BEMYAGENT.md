# BEMYAGENT Bootstrap Template

> **Mission**: Save tokens for the machine. Save orientation for the human.
> Every file must serve one of these two goals or it doesn't belong here.

This file instructs the AI to initialize the `.bemyagent/docs/` and `.bemyagent/work/` architecture, generating the permanent rule file (`00-ai-rules.md`) and standard templates that will govern all future interactions.

## Bootstrap Instructions for the AI

When the user asks you to execute this bootstrap, you MUST perform the following steps using your file-writing tools. Do NOT ask for permission between steps. Do them all sequentially.

### Step 0: Discovery & Assessment
Before generating any files, analyze the current workspace. **Important:** If your tool cannot create directories automatically, list the required `mkdir` commands and ask the user to execute them before proceeding.
1. **Is this an UPGRADE?** If `.bemyagent/` already exists:

   **a) ASSESS** — Compare current state with desired state:
   - You already know the old protocol structure (loaded at session start from `00-ai-rules.md`). Now read this `BEMYAGENT.md` as the desired state.
   - Scan the existing `.bemyagent/` structure and compare with the expected layout.
   - For `settings.json`: identify new fields in the template that are missing from the project's file. If a field name changed, search the old docs for references to understand the mapping.
   - For project files (`01-overview.md`, `02-architecture.md`, etc.): do NOT read them fully. Check only whether structural sections from the new template are present (quick scan of headers).
   - SKIP all completed `.bemyagent/work/` folders entirely. Only check in-progress tasks for template compatibility.

   **b) PLAN** — Generate `.bemyagent/upgrade-plan.md` with a categorized checklist:
   ```
   # Upgrade Plan — YYYY-MM-DD

   ## 1. Protocol Files (overwrite)
   > These files are owned by the BMA protocol. Overwriting is safe.
   - [ ] `00-ai-rules.md` — Overwrite with new version
     - Key changes: [brief summary of differences detected]
   - [ ] `work/_template_think.md` — Overwrite / Unchanged ✓
   - [ ] `docs/drafts/_template.md` — Overwrite / Unchanged ✓

   ## 2. Settings (additive merge)
   > Existing values are preserved. Only additions and remapping.
   - [ ] Add: `"newField": defaultValue`
   - [ ] Remap: `oldName` → `newName` (current value preserved)
   - [ ] Orphaned fields: [list fields present in project but absent in new template]

   ## 3. Structural Changes
   > Folder/path changes detected.
   - [ ] None detected ✓

   ## 4. Project Files (suggestions only)
   > These files contain YOUR project data. Never overwritten automatically.
   - [ ] `01-overview.md`: missing section "[name]" — suggest appending
   - [ ] Other files: structure matches ✓

   ## 5. Self-Registration Files
   - [ ] Regenerate [list] with updated path/content
   ```

   **STOP.** Present the plan to the user. The user reviews it, ticks/unticks items, and approves.

   **c) APPLY** — Execute only the approved items (checked `[x]`):
   - Use atomic copy/move operations (single commands that act on entire directories, not file-by-file enumeration).
   - Before overwriting any file, create a backup (e.g., `file.bak-YYYYMMDD`).
   - Check for filename collisions before copying. If a collision exists, NEVER overwrite user files — ask the user.

   **d) AUDIT** — Write a synthetic log to `.bemyagent/work/upgrade-YYYY-MM-DD.log`:
   ```
   YYYY-MM-DD — BMA Upgrade
   Applied: [list of changes made]
   Skipped: [list of items user declined]
   ```

   **e) CLEANUP** — Delete `.bemyagent/upgrade-plan.md`. Output upgrade success message and STOP.
2. **Is it an existing project (Brownfield)?** If you see an existing codebase but no `.bemyagent/docs/` folder, perform a **shallow, token-efficient scan** of the structure. **CRITICAL TOKEN-SAVING RULE:** You MUST IGNORE lockfiles (e.g., `package-lock.json`), vendor directories (e.g., `node_modules`, `vendor`, `.venv`), build outputs (`dist`, `target`), and deeply nested source code. Look ONLY at the root directory, primary dependency manifests, build scripts, and top-level architecture indicators. You will use this context to AUTO-FILL the documentation in Step 3. Do NOT fabricate `.bemyagent/work/` logs for past work; only map the current state.
3. **Is it a new/empty project (Greenfield)?** If the workspace is empty, STOP and ask the user: *"What are we building? Please describe the project."* Wait for their answer. You will use their response to AUTO-FILL the documentation in Step 3.

### Step 1: Create Directories
Create the following directories in the project root:
- `.bemyagent/docs/`
- `.bemyagent/docs/decisions/`
- `.bemyagent/docs/specs/`
- `.bemyagent/docs/drafts/`
- `.bemyagent/work/`

### Step 2: Generate `.bemyagent/docs/00-ai-rules.md`
This is the permanent rule file. Create it with the exact content below:

````markdown
# AI Rules & TTE Workflow

## 1. Self-registration (do once per project)
If this project does not yet have your tool's native rule file (e.g. `.amazonq/rules/`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`), create it now with this content:
```
Read .bemyagent/docs/00-ai-rules.md before every task.
IF about to create or modify any file inside .bemyagent/, THEN:
  1. Re-read the Routing Table in .bemyagent/docs/00-ai-rules.md §3
  2. Output: "PROTOCOL_CHECK: target=[file], reason=[why]"
  3. Proceed only after step 2
```

## 2. Session Restore
If this is a new session or context was lost:

**Step 0 — Pending Upgrade Check:**
If `.bemyagent/upgrade-plan.md` exists, a protocol upgrade was started but not completed. Read the plan and present it to the user for approval before doing any other work.

**Step 1 — Quick Resume (try this first):**
1. Read `.bemyagent/docs/06-implementation-plan.md` to identify the active milestone and task number.
2. Read the `02_tasks.md` inside the most recent `.bemyagent/work/X/X.Y/` folder matching that task.
3. If the checklist clearly shows what's done and what's pending, you have enough context. Confirm the status with the user and proceed.

**Step 2 — Full Restore (only if Step 1 is insufficient):**
Read in order: `.bemyagent/docs/01-overview.md` → `.bemyagent/docs/02-architecture.md` → `.bemyagent/docs/05-decisions-and-issues.md`.
Then use the Routing Table (§3) to lazy-load any additional context needed for the task.

Ask the user to close unnecessary tabs.

## 3. Routing Table & Lazy Loading
**Lazy Loading Principle:** NEVER read files inside `decisions/`, `specs/`, or `drafts/` during initial context restore. They must only be loaded on-demand when explicitly required by the task.

Before starting any task, read:
| Task involves | Read first (On-Demand) |
|---|---|
| Any code change | .bemyagent/docs/03-code-map.md |
| Creating/modifying any file in docs/ or work/ | .bemyagent/docs/06-implementation-plan.md |
| Architecture or new service | .bemyagent/docs/02-architecture.md |
| Bug or unexpected behaviour | .bemyagent/docs/05-decisions-and-issues.md |
| New feature | .bemyagent/docs/specs/[feature-name].md |
| Unscoped idea | .bemyagent/docs/drafts/[idea-name].md |
| Tech dependency or version | .bemyagent/docs/04-tech-stack.md |

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

## 4. Fractal TTEV Workflow (.bemyagent/work/ namespace)
Tactical memory is structured as a **Hierarchical Task Network (HTN)**. It is segmented by Task Numbers matching `06-implementation-plan.md` (which acts as the high-level Table of Contents).

**The Rule of Decomposition (Divide et Impera):** 
If a task is too complex, DO NOT execute it directly. Decompose it into sub-tasks (e.g., if `.bemyagent/work/1/1.0/` is too big, create `.bemyagent/work/1/1.1/` and `.bemyagent/work/1/1.2/`). Solve each sub-component in isolation, verify it individually, then integrate gradually. If a sub-task itself proves too complex during EXECUTE, fragment further into nested directories (e.g., `.bemyagent/work/7/7.1/7.1.1/`).

**Hierarchical Work Structure:**
Work directories follow the task hierarchy from `06-implementation-plan.md`:
- **Level 1** — Milestone: `.bemyagent/work/<N>/` (e.g., `.bemyagent/work/4/`)
- **Level 2** — Task: `.bemyagent/work/<N>/<N.Y>/` (e.g., `.bemyagent/work/4/4.1/`)
- **Level 3** — Sub-task (optional): `.bemyagent/work/<N>/<N.Y>/<N.Y.Z>/` (e.g., `.bemyagent/work/4/4.1/4.1.1/`)

A directory is a **leaf node** if it contains TTEV files (`01_think.md`, `02_tasks.md`, etc.). A directory is a **branch node** if it contains only subdirectories. **Maximum nesting depth: 3 levels.** If a sub-task at level 3 still needs decomposition, it's a sign the milestone itself should be re-scoped.

For any leaf node (atomic task):
- **THINK (Strategy):** Write to `.bemyagent/work/X/X.Y/01_think.md` using `_template_think.md`. You MUST complete the **Context Saturation Check** checklist. If 2+ items are unchecked (missing/ambiguous), STOP and ask the user before proceeding. If 0-1 are unchecked, state your assumption explicitly and continue.
  **Advanced Reasoning (for Standard and Heavy tasks):**
  - *Pre-mortem:* Before finalizing the plan, assume the task has failed. Identify the 2-3 most likely causes of failure and adjust the plan to mitigate them proactively.
  - *Devil's Advocate:* Challenge your own chosen approach. Generate at least one radically different alternative. If it's clearly superior, pivot. If not, briefly document why the original approach survives the challenge.
- **TASK (Planning):** Write to `.bemyagent/work/X/X.Y/02_tasks.md` (or `.json`). Create a strict checklist (`todo`, `done`, `verified`).
- **EXECUTE (Action):** Write to `.bemyagent/work/X/X.Y/03_execute.log`. Implement the code, log terminal outputs and errors.
- **VERIFY (Validation):** Write to `.bemyagent/work/X/X.Y/04_verify.md`. Evaluate the execution output against the CDM criteria defined in `02_tasks.md` and produce a verdict BEFORE notifying the user. See **Symbiotic Validation** below.

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
- Before committing, verify that a corresponding `.bemyagent/work/X/X.Y/` folder exists for the current task with `01_think.md` and `02_tasks.md` written BEFORE execution began.
- Before starting EXECUTE, always suggest a clean, atomic Git commit for the previous task with a clear message based on the task number (e.g., `git commit -m "feat: [1.1] add user auth"`).

## 5. Anti-Hallucination & Safety Rules
- **Always Verify:** Before modifying existing files, ALWAYS read the current content of the file. NEVER assume a function, variable, or import exists without seeing it in the context.
- **Dependencies:** If you need to add a new dependency, first update `04-tech-stack.md` and propose the installation command to the user (e.g., `npm install`).
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
- **Output Brevity:** Minimize verbose explanations unless explicitly requested. Prefer direct file modifications over describing changes in chat. Keep `03_execute.log` entries ultra-synthetic: command → result → next action. No prose. When showing code changes, use minimal diffs rather than repeating entire file contents. When producing evaluations or reviews, focus on gaps, overlaps, and minimal actions — never paraphrase the input.
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
````

### Step 3: Generate Scaffold Files
Create these files using the templates below. **CRITICAL:** Do not just leave them as blank templates! Use the knowledge gathered in Step 0 to auto-populate `01-overview.md`, `02-architecture.md`, `03-code-map.md`, and `04-tech-stack.md` as thoroughly as possible. For `decisions`, `specs`, and `drafts`, create a `_template.md` file inside the respective folder. Also create `_template_think.md` in `.bemyagent/work/`.
**LANGUAGE RULE:** Generate all markdown template content in the language the user is using during this bootstrap interaction. This sets the default documentation language for the project. Filenames must remain in English as shown below. The user can change the documentation language at any time (see §6).

**`.bemyagent/settings.json`**
```json
{
  "language": "en",
  "interactiveMode": false,
  "strictVerification": false,
  "autoModelSwitching": true,
  "autoCommit": false,
  "obstacleThreshold": 2,
  "contextSlicingThreshold": 200
}
```

**`.bemyagent/docs/01-overview.md`**
```markdown
- One paragraph: what the project does and for whom
- Success Metrics (Measurable KPIs)
- Repository structure (tree, max 2 levels)
- Quick start commands
- Environment variables table: name, default, description
- Ports table: port, service, notes
```

**`.bemyagent/docs/02-architecture.md`**
```markdown
- System diagram (MUST use Mermaid for better readability)
- Request flow as numbered steps
- One paragraph per component: what it does, what it owns, what it does NOT do
```

**`.bemyagent/docs/03-code-map.md`**
```markdown
## Hot Paths / Performance Critical
- List modules or files where performance is critical.

## Test Coverage Overview
- Brief overview of current test coverage and testing strategy.

## Pages / Routes
| Path/Method | File/Handler | Role/Auth | Key DOM IDs / Description |
|---|---|---|---|

## Key functions / Client-side JS
| Function/File | Role/Inputs | Outputs/Side effects |
|---|---|---|

## Data schemas
### Schema: [Name]
| Field | Type | Example | Owner |
|---|---|---|---|
> Flag schema mismatches with ⚠️ — they are the #1 source of integration bugs.
```

**`.bemyagent/docs/04-tech-stack.md`**
```markdown
- Technologies table: name, version, role, why chosen
- Known compatibility issues and workarounds
- External services: name, what we use it for, relevant endpoints
- Infrastructure: services, regions, ports
```

**`.bemyagent/docs/05-decisions-and-issues.md`**
```markdown
## Decisions index
> **Rule of thumb:** Use this file for small, inline decisions and to index all decisions. For complex, system-wide architectural choices, create a dedicated ADR (Architecture Decision Record) in the `.bemyagent/docs/decisions/` folder and link it here.

| # | Decision | Summary | File |
|---|---|---|---|

### Inline decisions
#### [Decision title]
- **Problem**: what needed solving
- **Decision**: what was chosen
- **Trade-off**: what we gave up

## Engineering Learnings
> **Rule of thumb:** Use this section to capture project-specific patterns, gotchas, or best practices discovered during execution that future agents should know.
- **[Topic]**: What we learned.

## Known issues
### [Issue title]
- **Symptom**: what the user/developer sees
- **Root cause**: why it happens
- **Status**: Active / Mitigated / Won't Fix
- **Workaround**: how to deal with it now
```

**`.bemyagent/docs/decisions/[name].md`** *(ADR - For complex decisions only)*
```markdown
# ADR: [Title]
**Date**: YYYY-MM
**Status**: accepted / superseded by [file]

## Context
What situation required a decision.

## Options considered
| Option | Pros | Cons |
|---|---|---|

## Decision
What was chosen and why.

## Consequences
What changes as a result. What becomes harder.
```

**`.bemyagent/docs/specs/[feature-name].md`**
```markdown
# [Feature name]
**Status**: idea | specced | in-progress | done | dropped

## Description
One paragraph.

## Acceptance criteria
- [ ] criterion one
- [ ] criterion two

## Open questions
- question one
```

**`.bemyagent/docs/drafts/[idea-name].md`**
> No strict template. Free form. The only rule: write enough that the idea can be understood 6 months later without the author present.

**`.bemyagent/work/_template_think.md`**
```markdown
## Context
- What are we trying to achieve?

### Context Saturation Check
> Before proceeding, fill this checklist. If 2+ items are unchecked, STOP and ask the user.
> If 0-1 are unchecked, state your assumption explicitly and proceed.

- [ ] **Target files/paths** — Known (from code-map) or ASK USER
- [ ] **Expected behavior** — Clear (from spec) or ASK USER
- [ ] **Constraints** — Defined (from decisions) or ASK USER
- [ ] **Dependencies** — Mapped (from tech-stack) or ASK USER

## Approaches Considered
- Pros/Cons of 2-3 different approaches
> These are NOT discarded forever. During EXECUTE, if the chosen approach hits unexpected friction, re-evaluate these alternatives with the new information acquired during execution.

## Selected Approach & Risks
- What we chose and why
- Estimated token cost: [low/medium/high] (Consider switching model if high)
- Risks & Mitigations

## Verification Plan
- How will we know it works?
```

**`.bemyagent/docs/06-implementation-plan.md`**
```markdown
# Implementation plan
> This document is the high-level Table of Contents (Index) for the project. For the historical execution trace and thought process, refer to the corresponding `.bemyagent/work/X/X.Y/` folders.

## Milestone 1.0 — [Name]
**Goal**: one sentence
**Status**: done | in-progress | next

| Spec | Status |
|---|---|
| [feature-name](specs/feature-name.md) | specced |

## Backlog (unscheduled)
- idea one → see [drafts/idea.md](drafts/idea.md)
```

### Step 4: Self-Registration & Clean-up
After creating all the files above:
1. **Self-Register:** If your specific AI environment supports persistent configuration (like `.cursorrules`, `.github/copilot-instructions.md`, or internal Knowledge Items), create that configuration NOW. Program yourself to automatically `Read .bemyagent/docs/00-ai-rules.md before every task`.
2. Output a success message confirming the initialization.
3. **Explain Configuration:** Present a brief summary of the `.bemyagent/settings.json` file so the user knows how to configure you:
   - `language`: Language for generated docs (e.g. "en", "it").
   - `interactiveMode`: If `true`, the agent pauses for human approval after THINK and VERIFY. If `false` (SEAMLESS), it works autonomously.
   - `strictVerification`: If `true`, performs deep analysis (performance, edge cases) during VERIFY. If `false`, performs light checks.
   - `autoModelSwitching`: If `true`, uses cheaper/faster models for execution and smarter models for thinking (if CLI permits).
   - `autoCommit`: If `true`, suggests a Git commit automatically after every successful task.
   - `obstacleThreshold`: Number of unexpected obstacles before the agent proposes a pivot to an alternative approach.
   - `contextSlicingThreshold`: Number of file lines above which the agent uses targeted search (grep) instead of reading the entire file. Calibrate based on the model's context window (default: 200).
   Tell the user they can manually edit `.bemyagent/settings.json` or ask you to change these settings at any time.
4. **Show the Quick Reference Card** to the user:
   ```text
   ╔════════════════════════════════════════════════════════════╗
   ║  BEMYAGENT — Quick Reference                               ║
   ╠════════════════════════════════════════════════════════════╣
   ║                                                            ║
   ║  MODES & SETTINGS:                                         ║
   ║  • All behavior is controlled by .bemyagent/settings.json  ║
   ║  • You can manually edit it or tell me to update it        ║
   ║    (e.g., "Switch to interactive mode", "Use Italian").    ║
   ║                                                            ║
   ║  CONTEXT PROBING:                                          ║
   ║  The agent checks if it has enough context before          ║
   ║  acting. If too much is unclear, it will ask you.          ║
   ║  This is normal — it means it's thinking carefully.        ║
   ║                                                            ║
   ║  KEY FOLDERS:                                              ║
   ║  • .bemyagent/docs/  → Long-term project memory            ║
   ║  • .bemyagent/work/  → Task history & audit trail          ║
   ║                                                            ║
   ╚════════════════════════════════════════════════════════════╝
   ```
4. Instruct the user to delete this `BEMYAGENT.md` file using the terminal `rm BEMYAGENT.md` (unless they explicitly want to keep it).
5. **CRITICAL: CONTEXT CLEANSING.** Tell the user to CLOSE the current chat session and start a NEW ONE. Explain that continuing the current chat will pointlessly waste tokens because the entire bootstrap prompt remains in the context window. A new chat will trigger the `00-ai-rules.md` and cleanly load only what is necessary.
