# AI Rules & TTE Workflow

## 1. Self-registration (do once per project)
If this project does not yet have your tool's native rule file (e.g. `.amazonq/rules/`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`), create it now with this content:
`Read docs/00-ai-rules.md before every task.`

## 2. Session Restore
If this is a new session or context was lost, read in order:
`docs/01-overview.md` → `docs/02-architecture.md` → `docs/05-decisions-and-issues.md` → `docs/06-implementation-plan.md`.
Then confirm the current milestone and the active `work/X.Y/` task folder before proceeding. Ask the user to close unnecessary tabs.

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

## 4. Fractal TTE Workflow (work/ namespace)
Tactical memory is structured as a **Hierarchical Task Network (HTN)**. It is segmented by Task Numbers matching `06-implementation-plan.md` (which acts as the high-level Table of Contents).

**The Rule of Decomposition:** 
If a task is too complex, DO NOT execute it directly. Decompose it into sub-tasks (e.g., if `work/1.0/` is too big, create `work/1.1/` and `work/1.2/`). 

For any leaf node (atomic task):
- **THINK (Strategy):** Write to `work/X.Y/01_think.md`. Define the approach and verification criteria. If the task is too large, break it down here and create sub-folders.
- **TASK (Planning):** Write to `work/X.Y/02_tasks.md` (or `.json`). Create a strict checklist (`todo`, `done`, `verified`).
- **EXECUTE (Action):** Write to `work/X.Y/03_execute.log`. Implement the code, log terminal outputs and errors.

**Pacing & Handoff Configuration:**
*Current Mode:* **SEAMLESS** (The user can instruct you to change this at any time).
- **SEAMLESS**: Proceed through THINK, TASK, and EXECUTE automatically without pausing.
- **INTERACTIVE**: You MUST STOP after the THINK phase and wait for human approval (or a manual model switch in the UI) before proceeding.
- **AUTO-CLI**: If you have CLI capabilities to switch models autonomously, switch to the pre-agreed models for each phase without pausing.
*Rule:* Prune your context window before EXECUTE. Only load files strictly required for that specific leaf node.

## 5. Coding & Maintenance Rules
- Never remove existing code/tests unless explicitly asked.
- Make changes in one edit, not incrementally. Write minimal code.
- Match existing code style. 
- **Language:** All user-facing text and documentation must be in the user's preferred language.
- **CRITICAL:** Update `03-code-map.md` and `05-decisions.md` in the SAME response as any change.
- `specs/` files: tick acceptance criteria checkboxes as they are completed.
- `drafts/` files: promote to `specs/` when ready to build, delete the draft.

## 6. Monthly audit prompt
Run this with your AI assistant once a month:
> "Compare `03-code-map.md` against the real file structure and report any drift.
> Check `01-overview.md` env vars against actual config files.
> List any decisions made recently not yet in `05-decisions-and-issues.md`."
