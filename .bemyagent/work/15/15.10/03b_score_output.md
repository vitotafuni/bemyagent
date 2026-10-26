# 15.10 — scorer raw output

Produced by `score.py` (in this folder) on 2026-10-22, all six arms present.
Saved before the verdict was written, per `harness/README.md`.

```
==============================================================================
a-1
  FORM  (WHEN..SHALL in 02_tasks.md): 0 line(s)
  CITATION (command named in 04_verify.md): 1
      Verdict: PASS. `npm test` -> 6 pass 0 fail (incl. test/online.test.js: duplicate sessions for 'ann' + 'bob' => count 2; 
  ...with literal output: 1
      Verdict: PASS. `npm test` -> 6 pass 0 fail (incl. test/online.test.js: duplicate sessions for 'ann' + 'bob' => count 2; 
  COVERAGE: test files added = ['online.test.js'] | index.js wires session.js = True
     -> test added covering the change
==============================================================================
a-2
  FORM  (WHEN..SHALL in 02_tasks.md): 0 line(s)
  CITATION (command named in 04_verify.md): 1
      PASS: npm test -> 7 pass 0 fail (3 new in test/online.test.js).
  ...with literal output: 1
      PASS: npm test -> 7 pass 0 fail (3 new in test/online.test.js).
  COVERAGE: test files added = ['online.test.js'] | index.js wires session.js = True
     -> test added covering the change
==============================================================================
a-3
  FORM  (WHEN..SHALL in 02_tasks.md): 0 line(s)
  CITATION (command named in 04_verify.md): 1
      PASS. npm test -> 6 pass 0 fail (2 new api tests: no duplicate presence for same player, 400 on bad playerId).
  ...with literal output: 1
      PASS. npm test -> 6 pass 0 fail (2 new api tests: no duplicate presence for same player, 400 on bad playerId).
  COVERAGE: test files added = ['api.test.js'] | index.js wires session.js = True
     -> test added covering the change
==============================================================================
b-1
  FORM  (WHEN..SHALL in 02_tasks.md): 2 line(s)
      WHEN a playerId posts two sessions THE SYSTEM SHALL list that player once in /api/online.
      WHEN playerId is missing THE SYSTEM SHALL respond 400.
  CITATION (command named in 04_verify.md): 2
      - WHEN same playerId posts twice THE SYSTEM SHALL list once: npm test -> "a created session shows the player online once
      - WHEN playerId missing THE SYSTEM SHALL 400: npm test -> pass
  ...with literal output: 1
      - WHEN same playerId posts twice THE SYSTEM SHALL list once: npm test -> "a created session shows the player online once
  COVERAGE: test files added = ['presence.test.js'] | index.js wires session.js = True
     -> test added covering the change
==============================================================================
b-2
  FORM  (WHEN..SHALL in 02_tasks.md): 1 line(s)
      ✅ Validation: WHEN a session is created twice for one playerId THE SYSTEM SHALL list that player once in GET /api/online
  CITATION (command named in 04_verify.md): 1
      PASS. `npm test` -> 7 pass 0 fail (3 new in test/online.test.js). Validation criterion covered by "same player with two 
  ...with literal output: 1
      PASS. `npm test` -> 7 pass 0 fail (3 new in test/online.test.js). Validation criterion covered by "same player with two 
  COVERAGE: test files added = ['online.test.js'] | index.js wires session.js = True
     -> test added covering the change
==============================================================================
b-3
  FORM  (WHEN..SHALL in 02_tasks.md): 3 line(s)
      - WHEN POST /api/sessions with a playerId THE SYSTEM SHALL return 201 with session and resumeToken.
      - WHEN POST with missing playerId THE SYSTEM SHALL return 400.
      - WHEN the same playerId is created twice THE SYSTEM SHALL list that player once in GET /api/online.
  CITATION (command named in 04_verify.md): 1
      Verdict: PASS (npm test → 7 pass 0 fail; criteria covered by test/online.test.js: 201+token, 400 missing playerId, doubl
  ...with literal output: 1
      Verdict: PASS (npm test → 7 pass 0 fail; criteria covered by test/online.test.js: 201+token, 400 missing playerId, doubl
  COVERAGE: test files added = ['online.test.js'] | index.js wires session.js = True
     -> test added covering the change
```
