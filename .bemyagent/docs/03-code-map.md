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

## Harness (development only — not distributed)
> Test environment for measuring whether a protocol rule changes agent behaviour.
> Nothing in `BEMYAGENT.md` references it; it never lands in a user's project.

| File | Role | Notes |
|---|---|---|
| `harness/README.md` | The method, its limits, and the traps that cost experiment rounds | Read this before designing a run |
| `harness/tokens.py` | Per-arm cost from agent session transcripts, cache-weighted | Emits numeric aggregates only, never transcript content |
| `harness/fixture/` | Cavia: tic-tac-toe app with real layer separation | schema → store → API → client → test |
| `fixture/server/rules.js` | Pure move legality + win detection | No I/O — the seam most experiments target |
| `fixture/server/store.js` | sqlite persistence | Native dep: see tech-stack for the Node constraint |
| `fixture/server/index.js` | REST API + static hosting | |
| `fixture/test/rules.test.js` | 4 tests | `npm test` → `node --test test/*.test.js` |
