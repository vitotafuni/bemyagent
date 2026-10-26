const { describe, test, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
const app = require('../server/index');
const { reset } = require('../server/session');

test('POST /api/sessions creates a session', async () => {
  reset();
  const res = await request(app)
    .post('/api/sessions')
    .send({ playerId: 'alice', displayName: 'Alice' })
    .expect(201);

  assert.ok(res.body.session);
  assert.equal(res.body.session.playerId, 'alice');
  assert.equal(res.body.session.displayName, 'Alice');
  assert.ok(res.body.resumeToken);
});

test('POST /api/sessions requires playerId', async () => {
  reset();
  const res = await request(app)
    .post('/api/sessions')
    .send({ displayName: 'Bob' })
    .expect(400);

  assert.equal(res.body.error, 'playerId is required');
});

test('POST /api/sessions validates playerId', async () => {
  reset();
  const res = await request(app)
    .post('/api/sessions')
    .send({ playerId: '' })
    .expect(400);

  assert.match(res.body.error, /playerId/);
});

test('GET /api/online lists players with sessions', async () => {
  reset();
  
  // Create two sessions
  await request(app)
    .post('/api/sessions')
    .send({ playerId: 'alice', displayName: 'Alice' })
    .expect(201);

  await request(app)
    .post('/api/sessions')
    .send({ playerId: 'bob', displayName: 'Bob' })
    .expect(201);

  // Check online presence
  const res = await request(app)
    .get('/api/online')
    .expect(200);

  assert.equal(res.body.count, 2);
  assert.equal(res.body.players.length, 2);
  
  const playerIds = res.body.players.map(p => p.playerId).sort();
  assert.deepEqual(playerIds, ['alice', 'bob']);
  
  const alice = res.body.players.find(p => p.playerId === 'alice');
  assert.equal(alice.displayName, 'Alice');
  assert.ok(typeof alice.idleMs === 'number');
  assert.ok(typeof alice.since === 'number');
});

test('GET /api/online returns empty list when no sessions', async () => {
  reset();
  const res = await request(app)
    .get('/api/online')
    .expect(200);

  assert.equal(res.body.count, 0);
  assert.deepEqual(res.body.players, []);
});
