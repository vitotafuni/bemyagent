# Code Map (File Map)

## Hot Paths / Performance Critical
- Context loading (Reading docs on start): Critical that docs remain small to prevent token explosion.

## Test Coverage Overview
- The protocol is dogfooded: `.bemyagent/` governs development of `BEMYAGENT.md` itself.

## Key Files
| Path | File | Role | Key Description |
|---|---|---|---|
| `/` | `BEMYAGENT.md` | Source Template (SRC) | The distributable prompt. Contains bootstrap Steps 0-4 and the embedded `00-ai-rules.md`. Must be updated when protocol evolves. |
| `/` | `README.md` | Documentation | High-level explanation for human developers and GitHub visitors. |
| `/.bemyagent/docs/` | `00-ai-rules.md` | Live Rules | The active protocol governing this project. Changes here must propagate to `BEMYAGENT.md`. |
| `/.bemyagent/docs/drafts/` | `*.md` | Pending Ideas | Unresolved proposals. Evaluate → integrate into `00-ai-rules.md` → propagate to `BEMYAGENT.md` → delete draft. |
| `/.bemyagent/work/` | `*/` | Execution Traces | Volatile TTEV logs for each task. |

## Key Concepts / Mental Models
| Concept | Role | Outputs/Side effects |
|---|---|---|
| Lazy Loading | Context Management | Prevents AI from reading irrelevant files, saving tokens. |
| Fractal TTEV | Execution Management | Enforces HTN (Hierarchical Task Networks). If a task is big, it must be split into subfolders. |
| Conceptual Map Pattern | Navigation | Index files (01-overview, 03-code-map) stay lightweight pointers. |
| Critical Review Protocol | Quality Control | Forces structured challenge before accepting proposals. Anti-sycophancy. |

## Data schemas
*(No strict data schemas in this markdown-based protocol)*
