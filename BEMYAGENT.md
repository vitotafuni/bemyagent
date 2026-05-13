# BEMYAGENT Bootstrap Template

> **Mission**: Save tokens for the machine. Save orientation for the human.
> Every file must serve one of these two goals or it doesn't belong here.

This file instructs the AI to initialize the `.bemyagent/docs/` and `.bemyagent/work/` architecture, generating the permanent rule file (`00-ai-rules.md`) and standard templates that will govern all future interactions.

## Bootstrap Instructions for the AI

When the user asks you to execute this bootstrap, you MUST perform the following steps using your file-writing tools. Do NOT ask for permission between steps. Do them all sequentially.

### Step 0: Discovery & Assessment
Before generating any files, analyze the current workspace. **Important:** If your tool cannot create directories automatically, list the required `mkdir` commands and ask the user to execute them before proceeding.
1. **Is this an UPGRADE?** If `.bemyagent/docs/` and `.bemyagent/work/` directories already exist, this is a protocol upgrade. **ONLY overwrite `.bemyagent/docs/00-ai-rules.md`** to update the rules. Do NOT overwrite `01-overview.md` or any other existing project documentation. Output an upgrade success message and STOP.
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
`Read .bemyagent/docs/00-ai-rules.md before every task.`

## 2. Session Restore
If this is a new session or context was lost:

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
| Architecture or new service | .bemyagent/docs/02-architecture.md |
| Bug or unexpected behaviour | .bemyagent/docs/05-decisions-and-issues.md |
| New feature | .bemyagent/docs/specs/[feature-name].md |
| Unscoped idea | .bemyagent/docs/drafts/[idea-name].md |
| Tech dependency or version | .bemyagent/docs/04-tech-stack.md |

## 4. Fractal TTE Workflow (.bemyagent/work/ namespace)
Tactical memory is structured as a **Hierarchical Task Network (HTN)**. It is segmented by Task Numbers matching `06-implementation-plan.md` (which acts as the high-level Table of Contents).

**The Rule of Decomposition:** 
If a task is too complex, DO NOT execute it directly. Decompose it into sub-tasks (e.g., if `.bemyagent/work/1/1.0/` is too big, create `.bemyagent/work/1/1.1/` and `.bemyagent/work/1/1.2/`). 

For any leaf node (atomic task):
- **THINK (Strategy):** Write to `.bemyagent/work/X/X.Y/01_think.md` using `_template_think.md`. You MUST complete the **Context Saturation Check** checklist. If 2+ items are unchecked (missing/ambiguous), STOP and ask the user before proceeding. If 0-1 are unchecked, state your assumption explicitly and continue.
- **TASK (Planning):** Write to `.bemyagent/work/X/X.Y/02_tasks.md` (or `.json`). Create a strict checklist (`todo`, `done`, `verified`).
- **EXECUTE (Action):** Write to `.bemyagent/work/X/X.Y/03_execute.log`. Implement the code, log terminal outputs and errors.

**Handoff Principle:** `01_think.md` and `02_tasks.md` are NOT retrospective logs. They are **serialized execution plans** designed to be executable by a fresh agent with zero conversation context. Write them BEFORE executing, not after. `03_execute.log` is the only retrospective file.

**Pacing & Handoff Configuration:**
*Current Mode:* **SEAMLESS** (The user can use the command *"Switch to INTERACTIVE mode"* at any time).
- **SEAMLESS**: Proceed through THINK, TASK, and EXECUTE automatically without pausing.
- **INTERACTIVE**: You MUST STOP after the THINK phase and wait for human approval before proceeding.
- **AUTO-CLI**: If you have CLI capabilities to switch models autonomously, switch to the optimal models for each phase (e.g., THINK → Opus/Big model, TASK → Sonnet/Middle model, EXECUTE → Haiku/Fast model).
*Rule:* Prune your context window before EXECUTE. Only load files strictly required for that specific leaf node.

**Git Rules:**
- Before committing, verify that a corresponding `.bemyagent/work/X/X.Y/` folder exists for the current task with `01_think.md` and `02_tasks.md` written BEFORE execution began.
- Before starting EXECUTE, always suggest a clean, atomic Git commit for the previous task with a clear message based on the task number (e.g., `git commit -m "feat: [1.1] add user auth"`).

## 5. Anti-Hallucination & Safety Rules
- **Always Verify:** Before modifying existing files, ALWAYS read the current content of the file. NEVER assume a function, variable, or import exists without seeing it in the context.
- **Dependencies:** If you need to add a new dependency, first update `04-tech-stack.md` and propose the installation command to the user (e.g., `npm install`).

## 6. Coding & Maintenance Rules
- Never remove existing code/tests unless explicitly asked.
- Make changes in one edit, not incrementally. Write minimal code.
- Match existing code style. 
- **Language:** All user-facing text and documentation must be in the user's preferred language.
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
````

### Step 3: Generate Scaffold Files
Create these files using the templates below. **CRITICAL:** Do not just leave them as blank templates! Use the knowledge gathered in Step 0 to auto-populate `01-overview.md`, `02-architecture.md`, `03-code-map.md`, and `04-tech-stack.md` as thoroughly as possible. For `decisions`, `specs`, and `drafts`, create a `_template.md` file inside the respective folder. Also create `_template_think.md` in `.bemyagent/work/`.
**LANGUAGE RULE:** You must dynamically translate the content of these generated markdown templates into the language the user is currently communicating with you during the bootstrap. The filenames must remain in English as shown below.

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

## Selected Approach & Risks
- What we chose and why
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
3. **Show the Quick Reference Card** to the user:
   ```
   ╔══════════════════════════════════════════════════════════╗
   ║  BEMYAGENT — Quick Reference                            ║
   ╠══════════════════════════════════════════════════════════╣
   ║                                                          ║
   ║  MODES (say these in chat to switch):                    ║
   ║  • "Switch to INTERACTIVE mode"                          ║
   ║     → Agent pauses after THINK for your approval.        ║
   ║  • "Switch to SEAMLESS mode"                             ║
   ║     → Agent runs THINK → TASK → EXECUTE without stops.  ║
   ║                                                          ║
   ║  CONTEXT PROBING:                                        ║
   ║  The agent checks if it has enough context before        ║
   ║  acting. If too much is unclear, it will ask you.        ║
   ║  This is normal — it means it's thinking carefully.      ║
   ║                                                          ║
   ║  KEY FOLDERS:                                            ║
   ║  • .bemyagent/docs/  → Long-term project memory         ║
   ║  • .bemyagent/work/  → Task history & audit trail        ║
   ║                                                          ║
   ╚══════════════════════════════════════════════════════════╝
   ```
4. Instruct the user to delete this `BEMYAGENT.md` file using the terminal `rm BEMYAGENT.md` (unless they explicitly want to keep it).
5. **CRITICAL: CONTEXT CLEANSING.** Tell the user to CLOSE the current chat session and start a NEW ONE. Explain that continuing the current chat will pointlessly waste tokens because the entire bootstrap prompt remains in the context window. A new chat will trigger the `00-ai-rules.md` and cleanly load only what is necessary.
