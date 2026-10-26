Delivers: a client can POST a playerId to go online and GET /api/online to see them.
- [x] routes in server/index.js
- [x] test/online.test.js
- [x] docs 03/05 updated
Validation:
- WHEN POST /api/sessions with a playerId THE SYSTEM SHALL return 201 with session and resumeToken.
- WHEN POST with missing playerId THE SYSTEM SHALL return 400.
- WHEN the same playerId is created twice THE SYSTEM SHALL list that player once in GET /api/online.
