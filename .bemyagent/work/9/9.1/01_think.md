## Context
Add a model-agnostic Protocol Anchoring Gate to prevent Recency Bias and Protocol Drift. The gate must be procedural (not declarative), work across all LLMs and context sizes, and create a forced-output checkpoint before any write to `.bemyagent/`.

### Context Saturation Check
- [x] **Target files/paths** — `00-ai-rules.md` (§3), `BEMYAGENT.md` (embedded rules), `05-decisions.md`, `06-implementation-plan.md`
- [x] **Expected behavior** — Agent must output `PROTOCOL_CHECK:` before any file creation/modification in `.bemyagent/`
- [x] **Constraints** — Minimal token cost (~80 tokens/session). Must not break existing workflow.
- [x] **Dependencies** — None. Pure protocol addition.

## Approaches Considered
1. **Narrow fix**: Anchor to `06-implementation-plan.md` only. Pro: simple. Con: doesn't cover drift toward other wrong files.
2. **Generic Write Gate**: Procedural checkpoint before ANY write to `.bemyagent/`. Pro: model-agnostic, covers all drift. Con: slight overhead per write.
3. **Periodic re-read**: Re-read `00-ai-rules.md` every N turns. Pro: refreshes all rules. Con: LLMs can't count turns reliably.

## Selected Approach & Risks
Approach 2 — Generic Write Gate. The gate makes the Routing Table **bidirectional** (not just "read before task" but also "check before write"). Forced output (`PROTOCOL_CHECK:`) creates a token dependency that is structurally hard to skip.

Risk: Overhead on micro-tasks (e.g., writing `03_execute.log`). Mitigation: The gate applies to file *creation* and *structural modifications*, not to appending to existing TTEV files during normal workflow execution.

## Verification Plan
- The new rule exists in both `00-ai-rules.md` and `BEMYAGENT.md` (in sync)
- Decision documented in `05-decisions.md`
- Milestone 9 added to `06-implementation-plan.md`
- The rule is generic (not tied to any specific file) and procedural (forced output)
