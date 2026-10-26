## Context
Wire session.js into index.js: POST /api/sessions, GET /api/online.
### Context Saturation Check
- [x] Target files: server/index.js, test/online.test.js
- [x] Behaviour: given by task
- [x] Constraints: presence one entry per playerId (use session.js API only)
- [x] Dependencies: none new (test uses node http, no supertest)
## Approaches Considered
- A: thin handlers over createSession/listOnline (chosen). B: new presence logic in index.js (rejected: breaks invariant risk).
## Selected Approach & Risks
A. Risk: stale expired sessions listed -> call sweep() in GET. Never return resumeToken in /online.
## Verification Plan
Test: create two sessions same player -> online lists one; bad playerId -> 400; npm test.
