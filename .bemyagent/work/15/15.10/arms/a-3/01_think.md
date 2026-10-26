## Context
- Wire session.js into index.js: POST /api/sessions, GET /api/online.
### Context Saturation Check
- [x] Target files: server/index.js, test/api.test.js
- [x] Behavior: create session for playerId; list online players
- [x] Constraints: presence invariant (one entry per playerId) lives in session.js; don't touch it
- [x] Dependencies: none new (node:test + fetch)
## Approaches Considered
- Direct calls to session.js from routes (chosen); a router module (overkill for 2 routes).
## Selected Approach & Risks
- Standard size, low cost. Risk: expired sessions listed -> sweep before list. Risk: invalid playerId -> 400. Pre-mortem: duplicates in /online -> test creating 2 sessions for same player.
- Devil's advocate: derive online from sessions instead of presence — rejected, breaks the invariant's single source.
## Verification Plan
- npm test incl. new API tests.
