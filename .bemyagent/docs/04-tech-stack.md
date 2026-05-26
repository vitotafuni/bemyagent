# Tech Stack

| Technology | Version | Role | Why chosen |
|---|---|---|---|
| Markdown | Latest | Language | Universal format easily parsed by LLMs and humans. Low token count. |
| Git | Latest | VCS | For tracking changes to the workspace. |
| AI Assistants | Any | Execution | BEMYAGENT is agnostic (works with Gemini, Claude, Cursor, Copilot, etc.) |

## Known compatibility issues and workarounds
- **Token Limits:** Large codebases can still overwhelm context. Workaround: strict enforcement of the Lazy Loading rule inside `BEMYAGENT.md`.
- **Model Stubbornness:** Some LLMs auto-continue instead of pausing. Workaround: `CRITICAL RULE` keywords and CAPS instructions inside `BEMYAGENT.md` to force pausing.
