## Context
We are implementing Task 6.1 from Milestone 6.0.
Goal: Introduce a `settings.json` file inside `.bemyagent/` to hold configurable protocol flags, and update `00-ai-rules.md` section 4 with the "Dynamic Pivot Rule" logic based on token cost estimation rather than just structural complexity.
We also need to incorporate the rule that the AI agent should use terminal commands (like `wc`) to estimate token cost without loading files into context.

### Context Saturation Check
> Before proceeding, fill this checklist. If 2+ items are unchecked, STOP and ask the user.
> If 0-1 are unchecked, state your assumption explicitly and proceed.

- [x] **Target files/paths** — Known: `.bemyagent/settings.json`, `.bemyagent/docs/00-ai-rules.md`, `work/6/6.1/` directories.
- [x] **Expected behavior** — Clear: `settings.json` is created with default pivot settings. `00-ai-rules.md` §4 is updated to use task length/token size for CDM mapping instead of complexity, and the Dynamic Pivot Rule is added, referencing the `settings.json`.
- [x] **Constraints** — Defined: Do not micromanage. Keep rule additions lightweight. Use terminal commands for word count.
- [x] **Dependencies** — Mapped: None.

## Approaches Considered
- **Approach 1**: Add the settings directly to `00-ai-rules.md` as markdown metadata.
  - Pros: Single file to parse.
  - Cons: Hard to parse programmatically, less standard for settings.
- **Approach 2**: Create `.bemyagent/settings.json`.
  - Pros: Extensible, standard format, easy to read by scripts or other agentic tools.
  - Cons: One more file. (Selected)

## Selected Approach & Risks
We will create `settings.json` in the `.bemyagent/` directory with the default settings proposed in the draft 01 analysis.
Then we will update `00-ai-rules.md` section 4 (CDM):
1. Change complexity-based mapping to size/token-based mapping.
2. Add the terminal command tip (`wc -w` or similar) for token estimation.
3. Add the "Dynamic Pivot Rule".

Risk: The user might forget to create this file in existing projects.
Mitigation: Task 6.2 will ensure the master template is updated to create this file during bootstrap.

## Verification Plan
We will verify that:
1. `.bemyagent/settings.json` exists and contains valid JSON.
2. `.bemyagent/docs/00-ai-rules.md` contains the Dynamic Pivot Rule and the reference to `settings.json`.
