const express = require('express');
const path = require('path');
const { applyMove } = require('./rules');
const { createGame, getGame, saveGame } = require('./store');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'client')));

app.post('/api/games', (req, res) => {
  const id = createGame();
  res.status(201).json(getGame(id));
});

app.get('/api/games/:id', (req, res) => {
  const game = getGame(req.params.id);
  if (!game) return res.status(404).json({ error: 'no such game' });
  res.json(game);
});

app.post('/api/games/:id/moves', (req, res) => {
  const game = getGame(req.params.id);
  if (!game) return res.status(404).json({ error: 'no such game' });
  if (game.winner) return res.status(409).json({ error: 'game over' });
  try {
    const next = applyMove(game.board, game.turn, Number(req.body.cell));
    saveGame(game.id, next);
    res.json(getGame(game.id));
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

const port = process.env.PORT || 3000;
if (require.main === module) app.listen(port, () => console.log(`listening on ${port}`));
module.exports = app;
