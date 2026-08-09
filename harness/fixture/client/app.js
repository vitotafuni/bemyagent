let gameId = null;

async function api(path, opts) {
  const res = await fetch(path, { headers: { 'content-type': 'application/json' }, ...opts });
  return res.json();
}

function render(game) {
  const board = document.getElementById('board');
  board.innerHTML = '';
  [...game.board].forEach((mark, cell) => {
    const b = document.createElement('button');
    b.textContent = mark === '-' ? '' : mark;
    b.disabled = mark !== '-' || !!game.winner;
    b.onclick = () => move(cell);
    board.appendChild(b);
  });
  document.getElementById('status').textContent =
    game.winner ? (game.winner === 'draw' ? 'Draw' : `${game.winner} wins`) : `${game.turn} to play`;
}

async function move(cell) {
  render(await api(`/api/games/${gameId}/moves`, { method: 'POST', body: JSON.stringify({ cell }) }));
}

(async () => {
  const game = await api('/api/games', { method: 'POST' });
  gameId = game.id;
  render(game);
})();
