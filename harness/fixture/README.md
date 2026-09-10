# tictactoe

Hot-seat tic-tac-toe. Two players share one device; the board lives server-side.

## Layout

```
db/schema.sql       game persistence schema
server/rules.js     move legality + win detection (pure)
server/store.js     sqlite persistence
server/session.js   player sessions, reconnect, online presence
server/index.js     REST API + static hosting
client/             vanilla UI
test/               unit tests
```

## Running

```
npm install && npm test   # 4 passing
npm start                 # http://localhost:3000
```

Requires Node >= 20 (`better-sqlite3` is a native module).
