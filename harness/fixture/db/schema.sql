-- Local hot-seat tic-tac-toe. Single-device play, no accounts.
CREATE TABLE IF NOT EXISTS game (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  board       TEXT    NOT NULL DEFAULT '---------',  -- 9 chars, 'X' 'O' or '-'
  turn        TEXT    NOT NULL DEFAULT 'X',
  winner      TEXT,                                   -- 'X' | 'O' | 'draw' | NULL
  created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
