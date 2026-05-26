# Think: Localization and Directory Encapsulation in .bemyagent

## Objective
The user requested two fundamental changes to the BEMYAGENT protocol:
1. **Dynamic Localization:** Generated files (templates in `docs/` and rules) must be written in the language the user is interacting with the AI during the bootstrap phase.
2. **Encapsulation (`.bemyagent/` Directory):** Move the `docs/` and `work/` directories inside a hidden `.bemyagent/` directory at the project root. This prevents conflicts with existing user directories (like `docs/` or `work/`) and keeps the project root clean.

## Implementation Strategy
This represents an architectural change to the protocol, so we categorize it under Milestone 4.0.

### 1. Update `BEMYAGENT.md` (The Core Protocol)
- **Localization**: Add an instruction in `BEMYAGENT.md` (Step 0 or Step 3) that explicitly orders the AI to translate the scaffold files (including `00-ai-rules.md` and templates) into the user's current conversation language. The `BEMYAGENT.md` file itself will remain in English as requested.
- **Paths**: Find and replace all occurrences of `docs/` with `.bemyagent/docs/` and `work/` with `.bemyagent/work/`. 

### 2. Update `README.md`
- Modify explanations to reflect the new `.bemyagent/` structure.

### 3. Sandbox Migration (Dogfooding)
- Since we are testing the protocol internally (`sandbox/`), we must migrate `sandbox/docs/` and `sandbox/work/` to `sandbox/.bemyagent/docs/` and `sandbox/.bemyagent/work/`.
- Update files in `sandbox/.bemyagent/docs/`:
  - `01-overview.md` (to reflect the new path).
  - `02-architecture.md` (to update the directory tree).
  - `05-decisions-and-issues.md` (Add two inline decisions: Localization and Encapsulation).
  - `06-implementation-plan.md` (Add Milestone 4.0).

## Verification Criteria
- [x] `BEMYAGENT.md` clearly instructs the AI regarding language.
- [x] `BEMYAGENT.md` refers to `.bemyagent/docs` and `.bemyagent/work`.
- [x] Directories in `sandbox/` are moved consistently.
- [x] Internal sandbox documentation reflects these decisions and updated paths.
