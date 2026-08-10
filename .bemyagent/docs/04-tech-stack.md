# Tech Stack

| Technology | Version | Role | Why chosen |
|---|---|---|---|
| Markdown | Latest | Language | Universal format easily parsed by LLMs and humans. Low token count. |
| Git | Latest | VCS | For tracking changes to the workspace. |
| AI Assistants | Any | Execution | BEMYAGENT is agnostic (works with Gemini, Claude, Cursor, Copilot, etc.) |
| Node.js | >= 20 | Harness fixture runtime | Only for `harness/`; the protocol itself has no runtime |
| Express | ^4.19 | Harness fixture API layer | Gives the fixture a real API seam to slice through |
| better-sqlite3 | ^13 | Harness fixture persistence | Native module — see compatibility note below |
| Python | 3 (stdlib) | `harness/tokens.py` | No third-party packages, runs anywhere |

## Known compatibility issues and workarounds
- **Token Limits:** Large codebases can still overwhelm context. Workaround: strict enforcement of the Lazy Loading rule inside `BEMYAGENT.md`.
- **`better-sqlite3` native build:** versions `^11` and earlier fail to compile against Node 26 (node-gyp / V8 headers), which broke `npm install` in the harness fixture. Pinned to `^13`, which ships prebuilt binaries. A broken fixture is worse than no fixture: agents spend their run debugging it instead of exercising the rule under test.
- **Model Stubbornness:** Some LLMs auto-continue instead of pausing. Workaround: `CRITICAL RULE` keywords and CAPS instructions inside `BEMYAGENT.md` to force pausing.
