# Decisions & Issues

## Decisions index
| # | Decision | Summary | File |
|---|---|---|---|
| 1 | Add Step 0 (Discovery) | Make the prompt adaptive to empty vs existing repos. | - |
| 2 | Fractal TTE Workflow | Use HTN for task breakdown to manage context sizes. | - |
| 3 | Model Handoff Pauses | Force AI to pause between Think/Task/Execute to switch models. | - |
| 4 | Sandbox Dogfooding | Use `sandbox/` as the actual development docs for the repo. | - |

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

## Known issues
### AI forgets to pause
- **Symptom**: The AI ignores the "Handoff" rule and proceeds straight to execution.
- **Root cause**: Instruction tuning in some models prioritizes fulfilling the user's ultimate goal in one go.
- **Status**: Mitigated
- **Workaround**: Explicitly state "STOP" and "Wait for the user" in the prompt.
