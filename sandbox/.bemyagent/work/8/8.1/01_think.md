## Context
We are implementing Task 8.1 from Milestone 8.0 (Draft 04: Updating BEMYAGENT in Existing Projects).
Goal: Introduce a standard protocol behavior for updating a project that already has `.bemyagent`. Prevent file loss by banning manual file enumeration in favor of atomic operations (`cp -r`, `mv`), and prevent filename collisions by enforcing a collision check and safe resolution before copying new protocol files.

### Context Saturation Check
> Before proceeding, fill this checklist. If 2+ items are unchecked, STOP and ask the user.
> If 0-1 are unchecked, state your assumption explicitly and proceed.

- [x] **Target files/paths** — Known: `00-ai-rules.md` and `BEMYAGENT.md`.
- [x] **Expected behavior** — Clear: Add a new section 8 to rules. Add a check in Step 0 of the bootstrap template to handle existing installations safely.
- [x] **Constraints** — Defined: Don't break formatting.
- [x] **Dependencies** — Mapped: None.

## Approaches Considered
- **Approach 1**: Create a separate `MIGRATION.md` file.
  - Pros: Clean separation.
  - Cons: Requires modifying the core bootstrap list and increases file count.
- **Approach 2**: Add a new section "8. Protocol Updates & Migration Rules" to `00-ai-rules.md` and a warning in Step 0 of `BEMYAGENT.md`.
  - Pros: Centralized rules. The agent reads `00-ai-rules.md` constantly.

## Selected Approach & Risks
Approach 2. We will add Section 8 to `00-ai-rules.md` defining atomic operations, collision checks, and safe resolutions. We will also update Step 0 in `BEMYAGENT.md` to trigger these rules if a `.bemyagent` folder is detected during bootstrap.
Since this touches architectural concepts, we will use a full CDM to be safe, even if token count is borderline Standard.

## Verification Plan
Verify the new rules are visible in both files.
