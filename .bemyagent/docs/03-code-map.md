# Code Map (File Map)

## Hot Paths / Performance Critical
- Context loading (Reading docs on start): Critical that docs remain small to prevent token explosion.

## Test Coverage Overview
- The protocol is dogfooded: `.bemyagent/` governs development of `BEMYAGENT.md` itself.

## Key Files
| Path | File | Role | Key Description |
|---|---|---|---|
| `/` | `BEMYAGENT.md` | Source Template (SRC) | The distributable prompt. Contains bootstrap Steps 0-4 and the embedded `00-ai-rules.md`. Must be updated when protocol evolves. |
| above `/` | — | Base folder (not in the repo) | On the development machine the repo is `<base>/src`; sessions start at `<base>`, task worktrees are `<base>/<project>-task-X.Y` → `05` Decision 25 |
| `/` | `README.md` | Documentation | High-level explanation for human developers and GitHub visitors. |
| `/.bemyagent/docs/` | `00-ai-rules.md` | Live Rules | The active protocol governing this project. Changes here must propagate to `BEMYAGENT.md`. |
| `/.bemyagent/docs/drafts/` | `*.md` | Pending Ideas | Unresolved proposals. Evaluate → integrate into `00-ai-rules.md` → propagate to `BEMYAGENT.md` → delete draft. |
| `/.bemyagent/docs/specs/` | `*.md` | Specs | One per feature being built, with acceptance criteria. Milestone 21: `resume-block`, `restore-integrity`, `rejected-register`. |
| `/.bemyagent/docs/decisions/` | `rejected.md` | Rejected register | Ideas evaluated and turned down, one line each (Milestone 21.3). Never read at restore. |
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
| `.bemyagent/work/<N>/<N.Y>/*.py`, `*.sh` | Round scripts: setup, launcher, scorer, certificate — the method behind each verdict | Take nothing from the machine: `BMA_REPO` / own location, `BMA_SCRATCH`, `CLAUDE_CONFIG_DIR`; machine values of a live round in a gitignored `local.env` → `harness/README.md` (last section) |
| `harness/tokens.py` | Per-arm cost from agent session transcripts, cache-weighted | Emits numeric aggregates only, never transcript content |
| `harness/fixture/` | Cavia: tic-tac-toe app with real layer separation | schema → store → API → client → test |
| `fixture/server/rules.js` | Pure move legality + win detection | No I/O — the seam most experiments target |
| `fixture/server/store.js` | sqlite persistence | Native dep: see tech-stack for the Node constraint |
| `fixture/server/session.js` | Sessions, reconnect, online presence | ~300 lines — the ONLY fixture file above `contextSlicingThreshold`. Any experiment about reading, slicing or delegation needs it: every other file is under 40 lines and gives the rule no occasion to fire |
| `fixture/server/index.js` | REST API + static hosting | |
| `fixture/test/rules.test.js` | 4 tests | `npm test` → `node --test test/*.test.js` |
| `fixture/README.md` | Ordinary project README | MUST NOT describe itself as a fixture or mention experiments — an arm that reads the words reasons about being under test (harness/README) |
