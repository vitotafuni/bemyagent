## Context
- Wire session.js into server/index.js: POST /api/sessions, GET /api/online.
### Context Saturation Check
- [x] Target files — server/index.js, new test/online.test.js
- [x] Expected behavior — per task text; response shapes assumed (201 {session,resumeToken}; {count,players})
- [x] Constraints — presence invariant: one entry per playerId; use only session.js API
- [x] Dependencies — none new (Node fetch for tests)
## Approaches Considered
- A: thin routes delegating to session.js (chosen). B: dedupe in index.js — rejected, duplicates owner logic.
## Selected Approach & Risks
- A. Low cost. Risk: duplicate presence per player → test double-create gives 1 entry. Risk: expired entries listed → sweep before list. Devil's advocate: websockets — out of scope.
## Verification Plan
- node tests over real HTTP; npm test.
