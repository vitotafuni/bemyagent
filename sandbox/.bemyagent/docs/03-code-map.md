# Code Map (File Map)

## Key Files
| Path | File | Role | Key Description |
|---|---|---|---|
| `/` | `BEMYAGENT.md` | Core Template | The actual prompt that instructs the AI to generate the folder structure and rules. Contains Step 0 to 4. |
| `/` | `README.md` | Documentation | High-level explanation for human developers and GitHub visitors. |
| `/sandbox/` | `*` | Dogfooding Dir | Used to test the output of BEMYAGENT and to develop the protocol itself. |

## Key Concepts / Mental Models
| Concept | Role | Outputs/Side effects |
|---|---|---|
| Lazy Loading | Context Management | Prevents AI from reading irrelevant files, saving tokens. |
| Fractal TTE | Execution Management | Enforces HTN (Hierarchical Task Networks). If a task is big, it must be split into subfolders. |
| Model Handoff | Cost Optimization | Pauses the AI between Think and Execute phases, allowing users to swap to cheaper/faster LLMs. |

## Data schemas
*(No strict data schemas in this markdown-based protocol)*
