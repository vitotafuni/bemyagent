# 16.1 — scorer raw output

Produced by `score.py` (this folder) on 2026-10-27, all nine arms present, both turns applied
(verified: `count` absent from every `server/index.js`). Saved before the verdict was written.

```
==============================================================================
a-1
  WRITTEN: 0 log file(s) 
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 0
     -> nowhere -> the correction left no durable trace at all
==============================================================================
a-2
  WRITTEN: 0 log file(s) 
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 0
     -> nowhere -> the correction left no durable trace at all
==============================================================================
a-3
  WRITTEN: 0 log file(s) 
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 0
     -> nowhere -> the correction left no durable trace at all
==============================================================================
b-1
  WRITTEN: 1 log file(s) ['2026-10-27.md']
     2026-10-27.md: 3 lines, 159 bytes
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 0
     -> nowhere -> the correction left no durable trace at all
==============================================================================
b-2
  WRITTEN: 0 log file(s) 
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 0
     -> nowhere -> the correction left no durable trace at all
==============================================================================
b-3
  WRITTEN: 0 log file(s) 
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 0
     -> nowhere -> the correction left no durable trace at all
==============================================================================
c-1
  WRITTEN: 1 log file(s) ['2026-10-27.md']
     2026-10-27.md: 3 lines, 187 bytes
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 1
     work/1/1.1/03_execute.log:3  count field dropped from /api/online per coordinator; existing test adjusted to array shape (no new test); npm test -> see below
     -> distilled only -> log adds nothing
==============================================================================
c-2
  WRITTEN: 1 log file(s) ['2026-10-27.md']
     2026-10-27.md: 2 lines, 221 bytes
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 0
     -> nowhere -> the correction left no durable trace at all
==============================================================================
c-3
  WRITTEN: 1 log file(s) ['2026-10-27.md']
     2026-10-27.md: 1 lines, 178 bytes
  TURN 2 in log: 0
  TURN 2 in distilled files (docs/ + work/): 1
     work/1/micro.log:1  2026-10-27 | 1.1 | /api/online returns bare array (count dropped per coordinator); existing test assertions adapted, no new test |
     -> distilled only -> log adds nothing
```

## The four logs, read in full

```
--- b-1 ---
# 2026-10-27
Turn: wire session.js into index.js (POST /api/sessions, GET /api/online)
-> task 1.1, server/index.js, test/online.test.js, .bemyagent bootstrap

--- c-1 ---
# 2026-10-27
- User asked to expose online presence over HTTP; added POST /api/sessions and GET /api/online, bootstrapped .bemyagent/.
  -> server/index.js, test/online.test.js, task 1.1

--- c-2 ---
- User asked: expose presence over HTTP (POST /api/sessions, GET /api/online). Bootstrapped .bemyagent (brownfield), implemented, tested.
  → server/index.js, test/presence.test.js, task 1.1 (uncommitted; not a git repo)

--- c-3 ---
- User asked to expose online presence over HTTP. Added POST /api/sessions and GET /api/online, tests, bootstrapped .bemyagent. -> server/index.js, test/online.test.js, task 1.1

```
