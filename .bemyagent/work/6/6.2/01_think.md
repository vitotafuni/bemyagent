## Context
We are implementing Task 6.2 from Milestone 6.0.
Goal: Sync the changes made in Task 6.1 (Dynamic Pivot rule, token cost estimation, settings.json) into the master template `BEMYAGENT.md` and the template file `_template_think.md` so that future bootstrap processes generate the correct rules and settings out-of-the-box.

### Context Saturation Check
> Before proceeding, fill this checklist. If 2+ items are unchecked, STOP and ask the user.
> If 0-1 are unchecked, state your assumption explicitly and proceed.

- [x] **Target files/paths** — Known: `BEMYAGENT.md`, `sandbox/.bemyagent/work/_template_think.md`.
- [x] **Expected behavior** — Clear: `BEMYAGENT.md` must contain the updated `00-ai-rules.md` (section 4), the `_template_think.md` with the new note in Approaches, and the instruction to generate `.bemyagent/settings.json`. The sandbox `_template_think.md` must also be updated.
- [x] **Constraints** — Defined: Keep existing formatting. Ensure the `settings.json` is generated with the default content during step 3.
- [x] **Dependencies** — Mapped: None.

## Approaches Considered
- **Approach 1**: Add `settings.json` generation inside the Step 3 template section of `BEMYAGENT.md`.
- **Approach 2**: Modify `_template_think.md` in both sandbox and `BEMYAGENT.md` with a quote block under `## Approaches Considered`.

## Selected Approach & Risks
We will use Approach 1 and 2. 
- Edit `sandbox/.bemyagent/work/_template_think.md` using replace_file_content.
- Edit `BEMYAGENT.md` using multi_replace_file_content to:
  1. Update Section 4 of `00-ai-rules.md` within the template.
  2. Add the `.bemyagent/settings.json` generation block in Step 3.
  3. Update `_template_think.md` inside Step 3.

Risk: Syntax errors in the markdown code blocks inside `BEMYAGENT.md`.
Mitigation: Carefully replace the exact lines and check the final output.

## Verification Plan
We will verify that:
1. `BEMYAGENT.md` contains `settings.json` in Step 3.
2. `BEMYAGENT.md` contains the new CDM rule.
3. `_template_think.md` (both sandbox and master) has the new Approaches text.
