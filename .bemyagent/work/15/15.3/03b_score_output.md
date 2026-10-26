# 15.3 — scorer output (RECOVERED, see provenance)

**Provenance, stated honestly.** This is the verbatim output of `score15.py` run on 2026-10-21
against the six arm directories, recovered from the session transcript on 2026-10-22 **after the
scratchpad had been cleared**. It was not saved at the time. The arm directories, `setup15.py`
and `score15.py` no longer exist, so this output **cannot be re-derived**. The scoring criteria
were pre-registered in `02_tasks.md` before any arm ran; the scorer implementing them is lost.

Treat this as the surviving record, not as reproducible evidence.

```
a-1   rule file chosen: ['AGENTS.md']
  -- STANDING rule, DURABLE files --
     AGENTS.md:8  - Every new function in `server/` gets a one-line comment directly above it saying what it returns. Applies to all future additions, not only the scor
     .bemyagent/docs/05-decisions-and-issues.md:10  - Every new function in `server/` has a one-line comment above it stating what it returns (standing user rule, also in `AGENTS.md`).
  -- STANDING rule, task-scoped work/ only --
     .bemyagent/work/1/1.1/01_think.md:6  - [x] Constraints: one-line "returns" comment above each new server function
  -- SPURIOUS --
     .bemyagent/docs/06-implementation-plan.md:8  | 1.1 | GET /scoreboard (server only; client deliberately skipped by user) | done |

a-2   rule file chosen: ['AGENTS.md']
  -- STANDING rule, DURABLE files --
     AGENTS.md:7  Repo convention (standing, user-set): every new function in `server/` gets a one-line comment directly above it saying what it returns.
     .bemyagent/docs/05-decisions-and-issues.md:10  - **Server comment convention**: every new function in `server/` has a one-line comment above it stating what it returns (user-set, also in AGENTS.md)
  -- STANDING rule, task-scoped work/ only --
     .bemyagent/work/1/1.1/01_think.md:6  - [x] Constraints — one-line "returns" comment above each new server function
     .bemyagent/work/1/1.1/04_verify.md:4  - new fn getScoreboard has returns-comment
  -- SPURIOUS --
     .bemyagent/docs/05-decisions-and-issues.md:12  - Client does not show the scoreboard (deliberately skipped; user does client part).

a-3   rule file chosen: ['AGENTS.md']
  -- STANDING rule, DURABLE files --
     .bemyagent/docs/05-decisions-and-issues.md:10  - **Convention (user, 2026-10-21, applies to all future work)**: every NEW function in `server/` gets a one-line comment directly above it saying what
  -- STANDING rule, task-scoped work/ only --
     .bemyagent/work/1/1.1/01_think.md:6  - [x] Constraints: new server functions need a one-line "returns" comment; skip client
     .bemyagent/work/1/1.1/02_tasks.md:2  - [x] store.getScoreboard with returns-comment
     .bemyagent/work/1/1.1/02_tasks.md:3  - [x] route in index.js with returns-comment on any new function
  -- SPURIOUS --
     .bemyagent/docs/05-decisions-and-issues.md:11  - Client updates are the user's call; the scoreboard task skipped the client at the user's request.
     .bemyagent/docs/06-implementation-plan.md:8  | 1.1 | `/scoreboard` endpoint + store query + test (client skipped by request) | done |

b-1   rule file chosen: ['CLAUDE.md']
  [CLAUDE.md] ## Project rules -> FILLED: - Every new function in `server/` gets a one-line comment directly above it saying what it returns. Applies to
  -- STANDING rule, DURABLE files --
     CLAUDE.md:9  - Every new function in `server/` gets a one-line comment directly above it saying what it returns. Applies to all future additions.
     .bemyagent/docs/05-decisions-and-issues.md:10  - Standing rule (user): every new function in `server/` has a one-line comment above it saying what it returns (see CLAUDE.md Project rules).
  -- STANDING rule, task-scoped work/ only --
     .bemyagent/work/1/1.1/01_think.md:6  - [x] Constraints: new functions get one-line "returns" comment; no client change
  -- SPURIOUS --
     (none)

b-2   rule file chosen: ['AGENTS.md']
  [AGENTS.md] ## Project rules -> FILLED: - Every new function in `server/` gets a one-line comment directly above it saying what it returns. Applies to
  -- STANDING rule, DURABLE files --
     AGENTS.md:9  - Every new function in `server/` gets a one-line comment directly above it saying what it returns. Applies to all future additions, not just one task
     .bemyagent/docs/05-decisions-and-issues.md:12  - Standing rule (AGENTS.md): new `server/` functions get a one-line "returns" comment.
  -- STANDING rule, task-scoped work/ only --
     (none)
  -- SPURIOUS --
     (none)

b-3   rule file chosen: ['AGENTS.md']
  [AGENTS.md] ## Project rules -> FILLED: - Every new function in `server/` gets a one-line comment directly above it saying what it returns.
  -- STANDING rule, DURABLE files --
     AGENTS.md:9  - Every new function in `server/` gets a one-line comment directly above it saying what it returns.
     .bemyagent/docs/05-decisions-and-issues.md:13  - Standing rule (AGENTS.md): every new function in `server/` has a one-line comment above it stating what it returns.
  -- STANDING rule, task-scoped work/ only --
     .bemyagent/work/1/1.1/10  #### Client not updated for scoreboard
```

## One self-reported datum, now unverifiable

Arm b-2's hand-back stated: *"The `04_verify.md` evidence line was written by hand rather than
from VERIFY command output."* That is §4's evidence rule violated outright, admitted by the arm
itself. It is a self-report and the artifact is gone, so it cannot be confirmed — recorded
because it bears directly on the Kiro survey's "citation, not coverage" finding.
