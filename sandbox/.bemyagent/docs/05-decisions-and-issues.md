# Decisions & Issues

## Decisions index
| # | Decision | Summary | File |
|---|---|---|---|
| 1 | Add Step 0 (Discovery) | Make the prompt adaptive to empty vs existing repos. | - |
| 2 | Fractal TTE Workflow | Use HTN for task breakdown to manage context sizes. | - |
| 3 | Model Handoff Pauses | Force AI to pause between Think/Task/Execute to switch models. | - |
| 4 | Sandbox Dogfooding | Use `sandbox/` as the actual development docs for the repo. | - |
| 5 | Native Language Localization | Generate templates in the user's interaction language. | - |
| 6 | Directory Encapsulation | Move `docs/` and `work/` inside a hidden `.bemyagent/` folder. | - |
| 7 | Strict Hierarchical Task Nesting | Organize `.bemyagent/work/` tasks under their parent Milestone directories. | - |
| 8 | Semver Versioning Strategy | Use semver adapted for protocol lifecycle: MAJOR=breaking, MINOR=features, PATCH=fixes. | - |
| 9 | Contextual DNA Mapping (CDM) | Embed Drift/Validation/Pivot metadata in tasks during TTE explosion. | - |
| 10 | Symbiotic Validation (VERIFY step) | Add a fourth TTEV phase: post-execution self-validation against CDM criteria before notifying user. | - |
| 11 | Documentation Language Rule | Language set at bootstrap, overridable anytime. Chat language and doc language are independent. | - |

### Inline decisions
#### 1. Add Step 0 (Discovery)
- **Problem**: In an existing project, generating blank `docs/` files leaves the user with the burden of filling them.
- **Decision**: Added a "Discovery" step where the AI scans the codebase (or asks the user) and auto-fills the docs.
- **Trade-off**: Slightly longer initialization time, but huge time saver overall.

#### 2. Fractal TTE Workflow
- **Problem**: A flat `work/1.0/` directory structure fails when tasks are too large for a single AI prompt.
- **Decision**: Implement Hierarchical Task Networks (HTN). The AI can decompose `work/1.0/` into `work/1.1/` and `work/1.2/`.
- **Trade-off**: More folders created, but cleaner context windows per leaf-node.

#### 3. Model Handoff Pauses
- **Problem**: Using an expensive "Reasoning" model for simple execution tasks wastes tokens and money.
- **Decision**: Imposed mandatory pauses between Think, Task, and Execute phases.
- **Trade-off**: Less "one-shot autonomous" behavior, but much better economic efficiency.

#### 5. Native Language Localization
- **Problem**: Generating English scaffolds forces non-English users to translate them or mix languages.
- **Decision**: Instruct the AI to dynamically translate the generated markdown templates into the user's conversation language during the bootstrap.
- **Trade-off**: Slightly less predictable output depending on the AI's translation, but much better user experience.

#### 6. Directory Encapsulation
- **Problem**: Generating `docs/` and `work/` in the project root can conflict with existing folders or clutter the repo.
- **Decision**: Encapsulate all protocol files within a `.bemyagent/` directory.
- **Trade-off**: An extra folder level, but much cleaner integration into existing projects.

#### 7. Strict Hierarchical Task Nesting
- **Problem**: A flat `work/` directory where all tasks (`1.1/`, `4.1/`, `5.1/`) are at the root level becomes cluttered and unmanageable.
- **Decision**: Enforce a strict hierarchy where tasks are nested inside their Milestone folders (e.g., `work/1/1.1/`).
- **Trade-off**: Deeper folder structure, but much easier for humans to audit and navigate.

#### 8. Semver Versioning Strategy
- **Problem**: The project needs a clear tagging strategy. As a protocol (not a library), standard semver triggers are ambiguous — there are no API contracts to break.
- **Decision**: Adopt semver with protocol-specific semantics:
  - **MAJOR** (X.0.0): Breaking changes that require manual migration of existing `.bemyagent/` setups (e.g., renaming core files, restructuring `docs/` incompatibly).
  - **MINOR** (1.X.0): New features, rules, or structural improvements that are additive and backward-compatible. An agent re-reading the updated `00-ai-rules.md` can adapt without manual intervention.
  - **PATCH** (1.1.X): Bug fixes to protocol rules (ambiguous wording causing agent misbehavior, incorrect path references, typos in instructions).
- **Trade-off**: Semver is designed for APIs, not documentation protocols. The "breaking change" boundary is subjective — we define it as "does a project bootstrapped with vN require manual work to use vN+1?". If yes → MAJOR. If the agent can self-adapt by re-reading the updated rules → MINOR.

#### 9. Contextual DNA Mapping (CDM)
- **Problem**: Tasks in `02_tasks.md` are flat checklists — the agent knows WHAT to do but not HOW to detect failure, WHEN to stop, or WHAT counts as done. The user must mentally reconstruct these criteria during validation.
- **Decision**: During the TASK phase (TTE explosion), embed Drift/Validation/Pivot metadata in each task, scaled by complexity. Simple tasks get no CDM, medium tasks get Validation only, complex tasks get full CDM (Drift + Validation + Pivot).
- **Trade-off**: Slightly denser planning output, but eliminates implicit assumptions and makes human validation faster (criteria are visible, not mental). Complexity threshold to be refined during dogfooding.

#### 10. Symbiotic Validation (VERIFY step)
- **Problem**: CDM defines validation criteria in `02_tasks.md`, but nobody explicitly verifies them after execution. The agent says "done" without self-evaluating. There is an entry gate (Context Saturation Check) but no exit gate.
- **Decision**: Add a fourth step to the workflow — VERIFY (`04_verify.md`). After EXECUTE, the agent evaluates its output against CDM criteria and produces a verdict (PASS / PASS_WITH_CAVEATS / FAIL) before notifying the user. The flow becomes TTEV.
- **Trade-off**: One extra file per validated task, but the cost is marginal (~800 tokens) compared to the risk of having to rollback an entire milestone for an undetected error. Calibration (when to skip, how deep to go) is left to the human-agent pair, not prescribed by the protocol.

#### 11. Documentation Language Rule
- **Problem**: The previous rule ("use the user's preferred language") was ambiguous — it conflated chat interaction language with documentation language. In a public repo with international audience, the user may interact in Italian but need English documentation.
- **Decision**: Documentation language is set at bootstrap time (matching the bootstrap interaction language). It can be overridden at any time with "Set documentation language to [language]". Chat and documentation languages are independent.
- **Trade-off**: Slightly more complex rule, but eliminates the ambiguity that caused Italian text in an English-convention repo.

## Known issues
### AI forgets to pause
- **Symptom**: The AI ignores the "Handoff" rule and proceeds straight to execution.
- **Root cause**: Instruction tuning in some models prioritizes fulfilling the user's ultimate goal in one go.
- **Status**: Mitigated
- **Workaround**: Explicitly state "STOP" and "Wait for the user" in the prompt.
