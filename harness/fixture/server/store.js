const Database = require('better-sqlite3');
const fs = require('fs');
const path = require('path');

const db = new Database(process.env.DB_PATH || path.join(__dirname, '..', 'game.db'));
db.exec(fs.readFileSync(path.join(__dirname, '..', 'db', 'schema.sql'), 'utf8'));

const createGame = () => db.prepare('INSERT INTO game DEFAULT VALUES').run().lastInsertRowid;
const getGame = (id) => db.prepare('SELECT * FROM game WHERE id = ?').get(id);
const saveGame = (id, { board, turn, winner }) =>
  db.prepare('UPDATE game SET board = ?, turn = ?, winner = ? WHERE id = ?').run(board, turn, winner, id);

module.exports = { createGame, getGame, saveGame };
