# BEMYAGENT Bootstrap Template

> **Mission**: Save tokens for the machine. Save orientation for the human.
> Every file must serve one of these goals or it doesn't belong here.

This file instructs the AI to generate the `.bemyagent/` architecture: permanent rules (`00-ai-rules.md`), project docs, and task workspace. You MUST perform all steps sequentially. Do NOT ask permission between steps.

### Step 0: Discovery & Assessment
If your tool cannot create directories, list the required `mkdir` commands and ask the user to run them first.
1. **UPGRADE** — `.bemyagent/` already exists:
   - **ASSESS**: Treat this file as desired state; compare with the existing `.bemyagent/`. For `settings.json`: detect new, renamed (search old docs for mapping), and orphaned fields. For project docs (`01`–`06`): check section headers only — never full reads. Skip completed `work/` folders; check only in-progress tasks.
   - **PLAN**: Write `.bemyagent/upgrade-plan.md` as a checkbox list in 5 sections: 1. Protocol Files (protocol-owned, overwrite-safe: `00-ai-rules.md`, templates — note key changes), 2. Settings (additive merge — additions, remaps `old → new` with values preserved, orphans), 3. Structural changes, 4. Project Files (user-owned — suggestions only, NEVER auto-overwritten), 5. Self-Registration files to regenerate. **STOP** — the user reviews, ticks items, approves.
   - **APPLY**: Execute checked items only. Atomic dir-level copy/move (never file-by-file enumeration). Backup before overwrite (`file.bak-YYYYMMDD`). On filename collision NEVER overwrite user files — ask.
   - **AUDIT**: Write `.bemyagent/work/upgrade-YYYY-MM-DD.log` (applied / skipped lists).
   - **CLEANUP**: Delete `upgrade-plan.md` and `.bak` files. Report success and STOP.
2. **BROWNFIELD** — codebase exists, no `.bemyagent/`: shallow, token-efficient scan only — root dir, dependency manifests, build scripts, top-level architecture. You MUST IGNORE lockfiles, vendor dirs (`node_modules`, `.venv`…), build outputs, deep source. Use findings to AUTO-FILL docs in Step 3. Never fabricate `work/` history.
3. **GREENFIELD** — empty workspace: STOP and ask *"What are we building?"*. Use the answer to AUTO-FILL Step 3.

### Step 1: Create Directories
`.bemyagent/docs/` + `decisions/`, `specs/`, `drafts/` inside it, and `.bemyagent/work/`

### Step 2: Generate `.bemyagent/docs/00-ai-rules.md`
The permanent rule file. Exact content:

````markdown
# AI Rules & TTEV Workflow

## 1. Self-Registration (idempotent, harness-proof)
Identify your tool's native rule file (`AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.claude/CLAUDE.md`, …).
Check its **content** — not just existence. The sentinel line is: `Read .bemyagent/docs/00-ai-rules.md before every task.`
- **File missing** → create it with the directive block below.
- **File exists but sentinel absent** → append the directive block.
- **Sentinel already present** → skip (noop).
```
Read .bemyagent/docs/00-ai-rules.md before every task.
IF about to create or modify any file inside .bemyagent/docs/ or .bemyagent/work/, THEN:
  1. Re-read the Routing Table in .bemyagent/docs/00-ai-rules.md §3
  2. Output: "PROTOCOL_CHECK: target=[file], reason=[why]"
  3. Proceed only after step 2
```

## 2. Session Restore (new session or lost context)
**0 — Pending upgrade:** if `.bemyagent/upgrade-plan.md` exists, an upgrade is incomplete — present it for user approval before any other work.
**1 — Quick Resume (try first):** read `docs/06-implementation-plan.md` → identify active milestone/task → read that task's `02_tasks.md` in `work/X/X.Y/`. If the checklist makes done/pending clear, confirm status with the user and proceed. If `03_execute.log` exists, read its last entry to determine the resume point.
**2 — Full Restore (only if 1 is insufficient):** read `docs/01-overview.md` → `02-architecture.md` → `05-decisions-and-issues.md`, then lazy-load the rest via the Routing Table.

## 3. Routing Table & Lazy Loading
NEVER read `decisions/`, `specs/`, `drafts/` during restore — on-demand only.
| Task involves | Read first |
|---|---|
| Any code change | docs/03-code-map.md |
| Creating/modifying any file in docs/ or work/ | docs/06-implementation-plan.md |
| Architecture or new service | docs/02-architecture.md |
| Bug or unexpected behaviour | docs/05-decisions-and-issues.md |
| New feature | docs/specs/[feature-name].md |
| Unscoped idea | docs/drafts/[idea-name].md |
| Tech dependency or version | docs/04-tech-stack.md |

**Conceptual maps:** `01`/`02`/`03` MUST hold only logical trees + pointers to fragments — never inline specs or long explanations. Read the map first (cheap), then only the needed fragment.

**Context Slicing** (any docs/work file > `contextSlicingThreshold` lines — estimate via terminal first): grep the relevant sections (~20-30 lines context) → expand (50-80) if insufficient → full read only as last resort. If you repeatedly need large parts of the same file, propose splitting it (e.g. `03-code-map/frontend.md`).

**Write Gate:** before creating or modifying ANY file in `docs/` or `work/`, you MUST:
1. Re-read the Routing Table — does the content belong in an existing file?
2. Output: `PROTOCOL_CHECK: target=[path], reason=[why]`
3. If an existing file fits, update it instead of creating a new one.
Exempt: the standard TTEV writes of the current task (`01`–`04` files, `micro.log` lines).

## 4. Fractal TTEV Workflow (work/)
Tactical memory is a Hierarchical Task Network mirroring the task numbers in `06-implementation-plan.md`.
**Structure:** `work/<N>/` milestone → `work/<N>/<N.Y>/` task → `work/<N>/<N.Y>/<N.Y.Z>/` sub-task. Max depth 3 — needing more means the milestone should be re-scoped. Leaf nodes hold TTEV files; branch nodes hold only subfolders — never both.
**Decomposition (Divide et Impera):** if a task is too complex, do NOT execute it directly — split into sub-tasks, solve each leaf in isolation, verify individually, integrate gradually. A leaf that proves too complex during EXECUTE fragments further.

**Size the ceremony first** (estimate token cost via terminal word/line counts, not full reads):
- **Micro** (typo, single trivial edit): NO folder, no TTEV files. Append one line to `work/<N>/micro.log`: `date | task | change | verdict` (e.g. `2026-06-27T14:32Z | 1.1 | fixed typo in route handler | PASS`).
- **Standard** (routine development): TTEV files; CDM = `✅ Validation` only.
- **Heavy** (complex logic, repetitive changes, high token cost): TTEV files + full CDM. Never execute Heavy without it:
  - `🎯 Drift` — what going off-track means for THIS task
  - `✅ Validation` — the objective evidence of success
  - `🔄 Pivot` — pre-defined stop-and-rethink condition. **Dynamic Pivot:** if obstacles (failed commands or contradicted assumptions forcing a plan change) exceed `obstacleThreshold`, or cost far exceeds estimate: STOP, re-read "Approaches Considered" in `01_think.md`, re-evaluate the alternatives with what you now know. `interactiveMode=true` → propose the pivot to the user first; `false` → pivot and report in the next update.

**TTEV files** (in `work/X/X.Y/`):
- **THINK** `01_think.md` (from `_template_think.md`): you MUST complete the Context Saturation Check — 2+ items unknown → STOP and ask the user; 0-1 → state the assumption explicitly, continue. Standard/Heavy also add: *Pre-mortem* (assume the task failed; mitigate the 2-3 likeliest causes in the plan) and *Devil's Advocate* (generate one radically different alternative; pivot if clearly superior, else note briefly why not).
- **TASK** `02_tasks.md`: strict checklist (todo / done / verified) + the CDM criteria.
- **EXECUTE** `03_execute.log`: command → result → **next intended action** (mandatory; write before executing it). No prose. Redact secrets/credentials before logging.
- **VERIFY** `04_verify.md`: see Symbiotic Validation.
**Handoff Principle:** `01` and `02` are forward-written execution plans a fresh zero-context agent could run — write them BEFORE executing. Only `03` and `04` are retrospective.

**Symbiotic Validation:** after EXECUTE and BEFORE notifying the user, evaluate the output against the CDM criteria in `02_tasks.md`; write results + evidence per criterion to `04_verify.md`. Evidence must come from commands run during VERIFY (diff, grep, test) — never from recollection. Verdict:
- **PASS** → proceed (silently only if `interactiveMode=false`)
- **PASS_WITH_CAVEATS** → present the friction points, await decision
- **FAIL** → one self-correction attempt, then escalate
Depth: `strictVerification=true` → deep analysis (edge cases, performance, architecture alignment); `false` → light check (compiles, basic success).

**Pacing (`interactiveMode`):** `false` = SEAMLESS — run TTEV autonomously, stop only on caveats/fail. `true` = INTERACTIVE — MUST STOP for human approval after THINK and after VERIFY. The user saying "enable/disable interactive mode" → update `settings.json`.
**Model switching (`autoModelSwitching=true`, if your CLI permits):** strongest available model for THINK and VERIFY; cheaper tiers for mechanical EXECUTE steps and log summarization.
Prune context before EXECUTE: load only what this leaf strictly needs.

**Git:** a task's `01_think.md` + `02_tasks.md` must exist (written pre-execution) before its commit. On verdict PASS: `autoCommit=true` → commit as `feat: [X.Y] …`; `false` → propose it. If the previous task is still uncommitted when starting EXECUTE, propose committing it first.
Default: track `.bemyagent/` in git. Teams preferring clean VCS history may `.gitignore` `work/` (audit trail retained locally, lost in VCS).

## 5. Anti-Hallucination & Safety
- Read a file's current content before modifying it. NEVER assume a function, variable, or import exists without seeing it.
- New dependency → update `04-tech-stack.md` first, then propose the install command to the user.
- **Critical Review Protocol** — for any proposal changing docs or protocol (including this file): 1. *Overlap check*: search target files; prefer surgical edits to existing text over new rules. 2. *Cost/benefit*: added lines = tokens at every session restore; benefit must clearly exceed. 3. *Challenge*: name ≥1 structural weakness and ≥1 unanswered question. 4. *Minimal alternative*: propose the smallest change achieving the goal.

## 6. Coding & Maintenance
- **Surgical scope:** touch only task-related files. No adjacent refactors, comment churn, or repo-wide reformatting. Never remove code/tests unless asked. One edit, not increments. Minimal code, matching existing style.
- **Brevity:** chat = results, open questions, next steps — no recaps of visible actions, no prefaces, no filler. Prefer file edits over chat descriptions. Minimal diffs, never full-file repeats. Evaluations/reviews: gaps, overlaps, minimal actions — never paraphrase the input.
- **Language:** docs language = `language` in `settings.json`; chat language is independent. "Set documentation language to X" → update the JSON.
- **CRITICAL:** update `03-code-map.md` and `05-decisions-and-issues.md` in the SAME response as any change — including discussion-only decisions (rejected approaches, architectural choices). Unresolved ideas → `drafts/`.
- `specs/`: tick acceptance criteria as completed. `drafts/`: promote to `specs/` when ready to build, then delete the draft.

## 7. Monthly Audit Prompt
> "Compare `03-code-map.md` vs the real file structure; report drift. Check `01-overview.md` env vars vs actual config. Verify `.gitignore` coverage. Check test coverage vs recent changes. List recent decisions missing from `05-decisions-and-issues.md`. Flag placeholder sections and language inconsistencies in docs/."

## 8. Protocol Updates & Migration
- Atomic dir-level copy/move operations only — file-by-file enumeration causes omissions.
- Scan the destination for filename collisions first. NEVER overwrite user files: ask, or move them to `archived/`. Keep user docs and protocol docs separated.

## 9. Multi-Agent Parallelism
1. One worktree + branch per task: `git worktree add ../project-task-X.Y -b bma/X.Y`
2. Each agent runs the standard TTEV workflow autonomously on its branch.
3. Shared docs: write decisions as per-task ADR files in `decisions/` (collision-free by filename); defer `03-code-map.md` edits to a post-merge sync task on main.
4. The human dispatches (one session per worktree), merges via PR, resolves conflicts. No automated orchestrator.
5. After merge: `git worktree remove ../project-task-X.Y`
````

### Step 3: Generate Scaffold Files
AUTO-POPULATE `01`–`04` from the Step 0 findings — NEVER leave blank templates. Fill in ONLY what the scan evidenced: mark unknowns with `?` instead of inventing, and link only to files that exist. Create a `_template.md` inside `decisions/`, `specs/`, `drafts/` and `_template_think.md` in `work/` from the content blocks below (block headings show the naming convention for real files, not the template filename).
**Language:** write all content in the language the user is using in this conversation (this sets the project's default docs language; see rules §6). Filenames stay in English.

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
- One paragraph: what the project does, for whom
- Success Metrics (measurable KPIs)
- Repo structure (tree, max 2 levels)
- Quick start commands
- Env vars table: name, default, description
- Ports table: port, service, notes
```

**`.bemyagent/docs/02-architecture.md`**
```markdown
- System diagram (Mermaid)
- Request flow as numbered steps
- One paragraph per component: what it does, owns, and does NOT do
```

**`.bemyagent/docs/03-code-map.md`**
```markdown
## Hot Paths / Performance Critical
## Test Coverage Overview
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
> Flag schema mismatches with ⚠️ — the #1 source of integration bugs.
```

**`.bemyagent/docs/04-tech-stack.md`**
```markdown
- Technologies table: name, version, role, why chosen
- Known compatibility issues and workarounds
- External services: name, usage, endpoints
- Infrastructure: services, regions, ports
```

**`.bemyagent/docs/05-decisions-and-issues.md`**
```markdown
## Decisions index
> Inline decisions live here. Complex, system-wide choices get a dedicated ADR in `decisions/`, linked here.
| # | Decision | Summary | File |
|---|---|---|---|
### Inline decisions
#### [Title]
- **Problem**: …
- **Decision**: …
- **Trade-off**: …
## Engineering Learnings
> Project-specific patterns and gotchas future agents should know.
- **[Topic]**: what we learned.
## Known issues
### [Title]
- **Symptom**: …
- **Root cause**: …
- **Status**: Active / Mitigated / Won't Fix
- **Workaround**: …
```

**`.bemyagent/docs/decisions/[name].md`** *(ADR — complex decisions only)*
```markdown
# ADR: [Title]
**Date**: YYYY-MM | **Status**: accepted / superseded by [file]
## Context
## Options considered
| Option | Pros | Cons |
|---|---|---|
## Decision
## Consequences
```

**`.bemyagent/docs/specs/[feature-name].md`**
```markdown
# [Feature]
**Status**: idea | specced | in-progress | done | dropped
## Description (one paragraph)
## Acceptance criteria
- [ ] criterion
## Open questions
```

**`.bemyagent/docs/drafts/[idea-name].md`**
> Free form. Only rule: understandable 6 months later without the author.

**`.bemyagent/work/_template_think.md`**
```markdown
## Context
- What are we trying to achieve?
### Context Saturation Check
> 2+ unchecked → STOP and ask the user. 0-1 → state assumption, proceed.
- [ ] **Target files/paths** — known (code-map) or ASK
- [ ] **Expected behavior** — clear (spec) or ASK
- [ ] **Constraints** — defined (decisions) or ASK
- [ ] **Dependencies** — mapped (tech-stack) or ASK
## Approaches Considered
- Pros/cons of 2-3 approaches
> Not discarded forever: if EXECUTE hits friction, re-evaluate these with the new information.
## Selected Approach & Risks
- Choice and why · estimated token cost [low/med/high] · risks & mitigations
## Verification Plan
- How will we know it works?
```

**`.bemyagent/docs/06-implementation-plan.md`**
```markdown
# Implementation plan
> High-level index. Execution traces live in `work/X/X.Y/`.

## Milestone 1 — [Name]
**Goal**: one sentence | **Status**: done | in-progress | next
| Task | Description | Status |
|---|---|---|
| 1.1 | … | todo |

| Spec | Status |
|---|---|
| [feature-name](specs/feature-name.md) | specced |

## Backlog (unscheduled)
- idea → [drafts/idea.md](drafts/idea.md)
```

### Step 4: Self-Registration & Clean-up
1. **Self-Register** now per rules §1: check your native rule file's **content** for the sentinel; create/append/skip accordingly.
2. Output a success message.
3. **Explain `settings.json`** briefly: `language` (docs language) · `interactiveMode` (true = human gates after THINK and VERIFY) · `strictVerification` (deep vs light VERIFY) · `autoModelSwitching` (cheaper models for mechanical phases) · `autoCommit` (commit on PASS) · `obstacleThreshold` (obstacles before pivot) · `contextSlicingThreshold` (lines before grep-instead-of-read). Editable manually or by asking.
4. **Show the Quick Reference Card:**
   ```text
   ╔══════════════════════════════════════════════════╗
   ║  BEMYAGENT — Quick Reference                     ║
   ╠══════════════════════════════════════════════════╣
   ║  • Behavior is set in .bemyagent/settings.json   ║
   ║    (edit it, or just ask me to change it)        ║
   ║  • I check context before acting; if too much    ║
   ║    is unclear, I ask — that's by design          ║
   ║  • docs/ = long-term memory                      ║
   ║  • work/ = task history & audit trail            ║
   ║  • First run? Set interactiveMode: true to       ║
   ║    validate behavior before going autonomous     ║
   ╚══════════════════════════════════════════════════╝
   ```
5. Tell the user to delete this file (`rm BEMYAGENT.md`) unless they want to keep it.
6. **CRITICAL — context cleansing:** tell the user to CLOSE this chat and start a NEW session. The bootstrap prompt would waste tokens in every following turn; a fresh session loads only `00-ai-rules.md`.
