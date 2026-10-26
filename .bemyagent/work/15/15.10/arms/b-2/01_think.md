## Context
Wire session.js into index.js: POST /api/sessions, GET /api/online. Size: Standard (index.js + test + docs).
### Context Saturation Check
- [x] Target files: server/index.js, test/online.test.js
- [x] Behavior: create session for playerId; list online players
- [x] Constraints: presence invariant (one entry per playerId) — routes must only use session.js API
- [x] Dependencies: none new
Assumptions: 201 on create; 400 on invalid playerId; resumeToken returned once in body; no auth (none exists).
## Approaches Considered
- A: call sweep() inside GET /api/online (chosen). B: setInterval sweeper (timer in tests, leaks handles).
## Selected Approach & Risks
A. Risk: stale entries if not swept → mitigated by A. Low cost.
## Verification Plan
Tests via real HTTP: create, 400, listing, duplicate player appears once, sweep drops expired.
