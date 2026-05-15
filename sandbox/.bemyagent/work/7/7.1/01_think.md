## Context
We are implementing Task 7.1 from Milestone 7.0 (Draft 05: Proportional Compression Rule).
Goal: Prevent the agent from wasting hundreds of tokens writing full `01_think.md` and `04_verify.md` files for extremely trivial tasks. If a task is "Short/Micro", the output must be severely compressed (1-2 lines).

### Context Saturation Check
> Before proceeding, fill this checklist. If 2+ items are unchecked, STOP and ask the user.
> If 0-1 are unchecked, state your assumption explicitly and proceed.

- [x] **Target files/paths** — Known: `00-ai-rules.md`, `BEMYAGENT.md`, `sandbox/.bemyagent/work/_template_think.md`.
- [x] **Expected behavior** — Clear: The rules must explicitly instruct the agent to ignore the verbose templates for micro-tasks and just write a 1-line summary.
- [x] **Constraints** — Defined: Don't break the Markdown formatting. Keep it simple.
- [x] **Dependencies** — Mapped: None.

## Approaches Considered
- **Approach 1**: Create a separate `_template_think_micro.md`.
  - Pros: Explicit template.
  - Cons: Creates file clutter.
- **Approach 2**: Update the rule in `00-ai-rules.md` section 4 to explicitly override the template for Short/Micro tasks.
  - Pros: Elegant, zero file clutter. (Selected)

## Selected Approach & Risks
Update the CDM definition in `00-ai-rules.md` and `BEMYAGENT.md` for "Short/Micro tasks":
Instead of just "No CDM needed", it will say: "No CDM needed. **Proportional Compression:** IGNORE the standard templates. Write a maximum of 1-2 lines for both `01_think.md` and `04_verify.md`."

Risk: The agent might still follow the template if the template instruction overrides the section 4 instruction.
Mitigation: The bold text "IGNORE the standard templates" usually acts as a strong LLM override.

## Verification Plan
Check that both `00-ai-rules.md` and `BEMYAGENT.md` contain the "Proportional Compression" keyword and the 1-2 lines instruction for Short/Micro tasks.
