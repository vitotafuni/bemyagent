# BEMYAGENT Bootstrap Template

> **Mission**: Save tokens for the machine. Save orientation for the human.
> Every file must serve one of these two goals or it doesn't belong here.

This file instructs the AI to initialize the `docs/` and `work/` architecture, generating the permanent rule file (`00-ai-rules.md`) and standard templates that will govern all future interactions.

## Bootstrap Instructions for the AI

When the user asks you to execute this bootstrap, you MUST perform the following steps using your file-writing tools. Do NOT ask for permission between steps. Do them all sequentially.

### Step 0: Discovery & Assessment
Before generating any files, analyze the current workspace:
1. **Is this an UPGRADE?** If `docs/` and `work/` directories already exist, this is a protocol upgrade. **ONLY overwrite `docs/00-ai-rules.md`** to update the rules. Do NOT overwrite `01-overview.md` or any other existing project documentation. Output an upgrade success message and STOP.
2. **Is it an existing project (Brownfield)?** If you see an existing codebase but no `docs/` folder, quietly scan the structure and dependencies. You will use this context to AUTO-FILL the documentation in Step 3. Do NOT fabricate `work/` logs for past work; only map the current state.
3. **Is it a new/empty project (Greenfield)?** If the workspace is empty, STOP and ask the user: *"What are we building? Please describe the project."* Wait for their answer. You will use their response to AUTO-FILL the documentation in Step 3.

### Step 1: Create Directories
Create the following directories in the project root:
- `docs/`
- `docs/decisions/`
- `docs/specs/`
- `docs/drafts/`
- `work/`

### Step 2: Generate `docs/00-ai-rules.md`
This is the permanent rule file. Create it with the exact content below:

````markdown
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
````

### Step 3: Generate Scaffold Files in `docs/`
Create these files using the templates below. **CRITICAL:** Do not just leave them as blank templates! Use the knowledge gathered in Step 0 to auto-populate `01-overview.md`, `02-architecture.md`, `03-code-map.md`, and `04-tech-stack.md` as thoroughly as possible. For `decisions`, `specs`, and `drafts`, create a `_template.md` file inside the respective folder.

**`docs/01-overview.md`**
```markdown
- One paragraph: what the project does and for whom
- Repository structure (tree, max 2 levels)
- Quick start commands
- Environment variables table: name, default, description
- Ports table: port, service, notes
```

**`docs/02-architecture.md`**
```markdown
- ASCII or Mermaid system diagram
- Request flow as numbered steps
- One paragraph per component: what it does, what it owns, what it does NOT do
```

**`docs/03-code-map.md`**
```markdown
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

**`docs/04-tech-stack.md`**
```markdown
- Technologies table: name, version, role, why chosen
- Known compatibility issues and workarounds
- External services: name, what we use it for, relevant endpoints
- Infrastructure: services, regions, ports
```

**`docs/05-decisions-and-issues.md`**
```markdown
## Decisions index
> **Rule of thumb:** Use this file for small, inline decisions and to index all decisions. For complex, system-wide architectural choices, create a dedicated ADR (Architecture Decision Record) in the `docs/decisions/` folder and link it here.

| # | Decision | Summary | File |
|---|---|---|---|

### Inline decisions
#### [Decision title]
- **Problem**: what needed solving
- **Decision**: what was chosen
- **Trade-off**: what we gave up

## Known issues
### [Issue title]
- **Symptom**: what the user/developer sees
- **Root cause**: why it happens
- **Status**: Active / Mitigated / Won't Fix
- **Workaround**: how to deal with it now
```

**`docs/decisions/[name].md`** *(ADR - For complex decisions only)*
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

**`docs/specs/[feature-name].md`**
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

**`docs/drafts/[idea-name].md`**
> No strict template. Free form. The only rule: write enough that the idea can be understood 6 months later without the author present.

**`docs/06-implementation-plan.md`**
```markdown
# Implementation plan
> This document is the high-level Table of Contents (Index) for the project. For the historical execution trace and thought process, refer to the corresponding `work/X.Y/` folders.

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
1. **Self-Register:** If your specific AI environment supports persistent configuration (like `.cursorrules`, `.github/copilot-instructions.md`, or internal Knowledge Items), create that configuration NOW. Program yourself to automatically `Read docs/00-ai-rules.md before every task`.
2. Output a success message confirming the initialization.
3. Instruct the user to delete this `BEMYAGENT.md` file using the terminal `rm BEMYAGENT.md` (unless they explicitly want to keep it).
4. **CRITICAL: CONTEXT CLEANSING.** Tell the user to CLOSE the current chat session and start a NEW ONE. Explain that continuing the current chat will pointlessly waste tokens because the entire bootstrap prompt remains in the context window. A new chat will trigger the `00-ai-rules.md` and cleanly load only what is necessary.
