# AI Rules & TTE Workflow

## 1. Self-registration (do once per project)
If this project does not yet have your tool's native rule file (e.g. `.amazonq/rules/`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`), create it now with this content:
`Read docs/00-ai-rules.md before every task.`

## 2. Session Restore
If this is a new session or context was lost:

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
| Architecture or new service | docs/02-architecture.md |
| Bug or unexpected behaviour | docs/05-decisions-and-issues.md |
| New feature | docs/specs/[feature-name].md |
| Unscoped idea | docs/drafts/[idea-name].md |
| Tech dependency or version | docs/04-tech-stack.md |

## 4. Fractal TTEV Workflow (work/ namespace)
Tactical memory is structured as a **Hierarchical Task Network (HTN)**. It is segmented by Task Numbers matching `06-implementation-plan.md` (which acts as the high-level Table of Contents).

**The Rule of Decomposition:** 
If a task is too complex, DO NOT execute it directly. Decompose it into sub-tasks (e.g., if `work/1.0/` is too big, create `work/1.1/` and `work/1.2/`). 

For any leaf node (atomic task):
- **THINK (Strategy):** Write to `work/X.Y/01_think.md` using `_template_think.md`. You MUST complete the **Context Saturation Check** checklist. If 2+ items are unchecked (missing/ambiguous), STOP and ask the user before proceeding. If 0-1 are unchecked, state your assumption explicitly and continue.
- **TASK (Planning):** Write to `work/X.Y/02_tasks.md` (or `.json`). Create a strict checklist (`todo`, `done`, `verified`).
- **EXECUTE (Action):** Write to `work/X.Y/03_execute.log`. Implement the code, log terminal outputs and errors.
- **VERIFY (Validation):** Write to `work/X.Y/04_verify.md`. Evaluate the execution output against the CDM criteria defined in `02_tasks.md` and produce a verdict BEFORE notifying the user. See **Symbiotic Validation** below.

**Handoff Principle:** `01_think.md` and `02_tasks.md` are NOT retrospective logs. They are **serialized execution plans** designed to be executable by a fresh agent with zero conversation context. Write them BEFORE executing, not after. `03_execute.log` and `04_verify.md` are the only retrospective files.

**Contextual DNA Mapping (CDM):**
During the TASK phase, apply DNA mapping based on task complexity:
- **Simple tasks** (single file, no dependencies): No CDM needed.
- **Medium tasks** (2-3 files, internal deps): Add `✅ Validation` only (what proves success).
- **Complex tasks** (3+ files, external deps, architectural): Add full CDM:
  - `🎯 Drift`: What constitutes going off-track for THIS specific task.
  - `✅ Validation`: The objective evidence of success (test output, file diff, etc.).
  - `🔄 Pivot`: The pre-defined condition to stop and propose an alternative.
Do not execute a complex task without mapping the DNA onto it.

**Symbiotic Validation:**
After EXECUTE and BEFORE notifying the user, evaluate your output against the CDM criteria defined in `02_tasks.md`. Write the result to `04_verify.md`.
- For each CDM criterion (✅ Validation, 🎯 Drift, 🔄 Pivot), state the result and the evidence.
- Produce a verdict: **PASS** (proceed silently), **PASS_WITH_CAVEATS** (present friction points to user, await decision), or **FAIL** (attempt one self-correction; if it fails again, escalate to user).
- The protocol defines that verification happens. HOW deep to verify is a decision for the human-agent pair, refined through practice.

**Pacing & Handoff Configuration:**
*Current Mode:* **SEAMLESS** (The user can use the command *"Switch to INTERACTIVE mode"* at any time).
- **SEAMLESS**: Proceed through THINK, TASK, EXECUTE, and VERIFY automatically. If VERIFY yields PASS → notify user. If PASS_WITH_CAVEATS or FAIL → stop and present findings.
- **INTERACTIVE**: You MUST STOP after the THINK phase and after VERIFY, waiting for human approval at both gates.
- **AUTO-CLI**: If you have CLI capabilities to switch models autonomously, switch to the optimal models for each phase (e.g., THINK → Opus/Big model, TASK → Sonnet/Middle model, EXECUTE → Haiku/Fast model, VERIFY → Middle model).
*Rule:* Prune your context window before EXECUTE. Only load files strictly required for that specific leaf node.

**Git Rules:**
- Before committing, verify that a corresponding `work/X/X.Y/` folder exists for the current task with `01_think.md` and `02_tasks.md` written BEFORE execution began.
- Before starting EXECUTE, always suggest a clean, atomic Git commit for the previous task with a clear message based on the task number (e.g., `git commit -m "feat: [1.1] add user auth"`).

## 5. Anti-Hallucination & Safety Rules
- **Always Verify:** Prima di ogni modifica a file esistenti, leggi SEMPRE il contenuto attuale del file. Mai assumere che una funzione o variabile esista senza averla vista nel context.
- **Dependencies:** Se devi aggiungere una dipendenza, prima aggiorna `04-tech-stack.md` e proponi `npm install` / equivalente.

## 6. Coding & Maintenance Rules
- Never remove existing code/tests unless explicitly asked.
- Make changes in one edit, not incrementally. Write minimal code.
- Match existing code style. 
- **Language:** Documentation language is set at bootstrap time (matching the language used during the initial bootstrap interaction). The user can override it at any time by saying *"Set documentation language to [language]"*. All `.bemyagent/` files must use the configured language. Chat interaction language and documentation language are independent.
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
