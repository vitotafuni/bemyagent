## Context
Wire session.js into index.js: POST /api/sessions, GET /api/online.
### Context Saturation Check
- [x] Target files: server/index.js, new test/online.test.js
- [x] Behavior: create session for playerId; list presence
- [x] Constraints: presence invariant lives in session.js; don't duplicate it
- [x] Dependencies: none new (node:test + http)
Assumption (0 unknown): 201 + {session, resumeToken}; 400 on invalid playerId.
## Approaches Considered
1. Delegate to createSession/listOnline (chosen). 2. Build online list from sessions (rejected: double-counts).
Devil's advocate: websocket presence — out of scope.
## Selected Approach & Risks
Delegate. Pre-mortem: bad body (missing req.body) -> guard; leaking resumeToken in /online -> listOnline doesn't expose it. Cost low.
## Verification Plan
node --test with a real listen on ephemeral port; duplicate createSession yields one online entry.
