const test = require('node:test');
const assert = require('node:assert');
const { applyMove, winnerOf } = require('../server/rules');

test('a completed row wins', () => {
  assert.equal(winnerOf('XXX------'), 'X');
});

test('a full board with no line is a draw', () => {
  assert.equal(winnerOf('XXOOOXXOX'), 'draw');
});

test('a move flips the turn', () => {
  const next = applyMove('---------', 'X', 4);
  assert.equal(next.board, '----X----');
  assert.equal(next.turn, 'O');
});

test('an occupied cell is rejected', () => {
  assert.throws(() => applyMove('----X----', 'O', 4), /occupied/);
});
