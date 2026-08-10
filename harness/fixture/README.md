# tictactoe — harness fixture

Hot-seat tic-tac-toe. Two players share one device; the board lives server-side.

Deliberately layered so a feature request cuts through several layers at once:
`db/schema.sql` · `server/rules.js` (pure logic) · `server/store.js` (persistence) ·
`server/index.js` (REST) · `client/` (UI) · `test/`.

```
npm install && npm test   # 4 passing
```

Requires Node >= 20. `better-sqlite3` is a native module: older pins fail to
build against recent Node releases, which costs an experiment round when arms
hit it instead of the rule under test.
