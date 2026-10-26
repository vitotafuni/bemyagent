## Context
Wire session.js into server/index.js: POST /api/sessions, GET /api/online.
Saturation: all known (files: index.js + new test + docs); 0 unknown.
## Approaches Considered
- A: routes call createSession/listOnline (chosen). B: write presence directly (rejected: breaks one-entry-per-playerId invariant ownership).
## Pre-mortem
Duplicate online entries on repeated POST (mitigated: createSession keys presence by playerId; tested). Stale sessions listed (mitigated: sweep before list).
## Devil's Advocate
Timer-based sweep: more moving parts, rejected.
## Verification Plan
Test: two POSTs same playerId -> one online entry; bad playerId -> 400.
