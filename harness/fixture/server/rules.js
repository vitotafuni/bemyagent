const LINES = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6],
];

function winnerOf(board) {
  for (const [a, b, c] of LINES) {
    if (board[a] !== '-' && board[a] === board[b] && board[b] === board[c]) {
      return board[a];
    }
  }
  return board.includes('-') ? null : 'draw';
}

function applyMove(board, turn, cell) {
  if (cell < 0 || cell > 8) throw new Error('cell out of range');
  if (board[cell] !== '-') throw new Error('cell occupied');
  const next = board.slice(0, cell) + turn + board.slice(cell + 1);
  return { board: next, turn: turn === 'X' ? 'O' : 'X', winner: winnerOf(next) };
}

module.exports = { applyMove, winnerOf };
