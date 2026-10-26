# Kiro Plan agent — the plan it produced, extracted verbatim

**Provenance.** Extracted on 2026-10-23 from `~/.kiro/sessions/cli/a1cab57c-….jsonl`, the
session transcript Kiro keeps **outside the project**. Kiro wrote **no file** for this: the
project folder was byte-identical to the restored fixture afterwards. Nothing was regenerated
and nothing was asked of the model to produce this text — it is the single
`AssistantMessage` that carried the plan, lifted out of the transcript.

Model `claude-sonnet-4.5`, Plan mode, context cleared, fixture restored, task text identical to
the one given to the six arms in `work/15/15.10/arms/`. The three clarifying questions it asked
first were answered only with *"No further information is available. Proceed with the task
exactly as stated."*

Compare with any arm's `01_think.md` + `02_tasks.md` in `work/15/15.10/arms/`.

---

Now let me create the implementation plan.

---

## **Implementation Plan - HTTP Presence Endpoints**

### **Problem Statement:**
The `server/session.js` module implements sessions and online presence tracking but is not exposed via HTTP. We need to wire it into `server/index.js` by adding two endpoints: `POST /api/sessions` to create player sessions and `GET /api/online` to list currently online players.

### **Requirements:**
- Add `POST /api/sessions` endpoint that accepts a playerId (and optional displayName) and returns a session with resumeToken
- Add `GET /api/online` endpoint that returns the list of currently online players
- Wire the session module into the Express application
- Ensure expired sessions are cleaned up automatically
- Add comprehensive tests for the new endpoints

### **Background:**
The session.js module provides:
- `createSession(playerId, opts)` - creates a new session and registers presence
- `listOnline(opts)` - returns array of online players with playerId, displayName, idleMs, since
- `sweep(opts)` - removes expired sessions and marks stale ones
- Session TTL is 30 minutes, with 45-second heartbeat grace period
- The project uses Node's built-in test runner and supertest for HTTP testing (already in devDependencies)

### **Proposed Solution:**
Integrate the session module into the Express server with minimal endpoints to expose the core functionality. Add automatic session cleanup via periodic sweep. Follow the existing API patterns (POST for creation, GET for retrieval) and test structure (node:test + assertions).

### **Task Breakdown:**

**Task 1:** Add GET /api/online endpoint with tests
- **Objective:** Expose the listOnline() function via HTTP to show currently online players
- **Implementation:**
  - Import the session module functions into server/index.js
  - Add GET /api/online route that calls listOnline() and returns JSON
  - Create test/session-api.test.js using supertest to test the endpoint
  - Test should verify: empty list when no sessions, correct format when sessions exist
- **Tests:** Verify endpoint returns 200 with empty array initially, and correct player list after creating sessions
- **Demo:** curl GET /api/online returns `[]` initially; after manual session creation via code, returns list of online players

**Task 2:** Add POST /api/sessions endpoint with tests
- **Objective:** Create player sessions via HTTP and return session + resumeToken
- **Implementation:**
  - Add POST /api/sessions route in server/index.js
  - Accept JSON body with required playerId and optional displayName
  - Call createSession(playerId, { displayName }) and return the result
  - Add validation: return 400 if playerId is missing or invalid
  - Add tests for successful creation, missing playerId, and invalid playerId
- **Tests:** Verify 201 response with session object and resumeToken; 400 for invalid input; session appears in GET /api/online
- **Demo:** POST /api/sessions with `{"playerId":"alice"}` returns session object with resumeToken; GET /api/online shows alice is online

**Task 3:** Add automatic session cleanup with sweep interval
- **Objective:** Ensure expired and stale sessions are automatically cleaned up
- **Implementation:**
  - Add periodic sweep() call using setInterval in server/index.js
  - Set interval to run every 30 seconds (frequent enough to catch expiry)
  - Store the interval reference and clear it on server shutdown if needed
  - Add test that verifies expired sessions are cleaned up (using time manipulation if needed)
- **Tests:** Create session with short TTL, wait, verify it's removed from online list
- **Demo:** Create a session, wait for TTL to expire, verify GET /api/online no longer shows the player

**Task 4:** Add session heartbeat endpoint with tests
- **Objective:** Allow clients to keep sessions alive and update lastSeenAt timestamp
- **Implementation:**
  - Add POST /api/sessions/:id/heartbeat route
  - Call touchSession(sessionId) and return updated session on success
  - Return 404 if session doesn't exist
  - Add tests for successful heartbeat and unknown session
- **Tests:** Verify heartbeat updates lastSeenAt, extends expiresAt, and prevents expiry
- **Demo:** Create session, call heartbeat endpoint, verify lastSeenAt is updated and session doesn't expire prematurely

---

Does this plan look good, or would you like me to adjust anything?
