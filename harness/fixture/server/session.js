const { randomBytes, createHash } = require('node:crypto');

// Player sessions and online presence.
//
// A session is the server-side record of one player's connection. It survives
// a dropped socket: the client keeps a resume token and reconnects with it,
// which issues a fresh session id while keeping the same playerId.
//
// INVARIANT: the presence registry holds at most one entry per playerId.
// Anything that counts, ranks or pairs players reads presence, so a duplicate
// entry silently double-counts that player.

const SESSION_TTL_MS = 30 * 60 * 1000;
const HEARTBEAT_GRACE_MS = 45 * 1000;
const RESUME_WINDOW_MS = 2 * 60 * 1000;
const TOKEN_BYTES = 24;
const MAX_SESSIONS_PER_PLAYER = 4;

const sessions = new Map();
const presence = new Map();
const resumeIndex = new Map();

function newSessionId() {
  return 's_' + randomBytes(9).toString('hex');
}

function newResumeToken() {
  return randomBytes(TOKEN_BYTES).toString('base64url');
}

function tokenFingerprint(token) {
  return createHash('sha256').update(token).digest('hex').slice(0, 16);
}

function nowMs(clock) {
  return typeof clock === 'number' ? clock : Date.now();
}

function assertPlayerId(playerId) {
  if (typeof playerId !== 'string' || playerId.length === 0) {
    throw new Error('playerId must be a non-empty string');
  }
  if (playerId.length > 64) {
    throw new Error('playerId too long');
  }
}

function presenceKey(session) {
  return session.playerId;
}

function sessionsOf(playerId) {
  const out = [];
  for (const session of sessions.values()) {
    if (session.playerId === playerId) out.push(session);
  }
  return out;
}

function createSession(playerId, opts) {
  assertPlayerId(playerId);
  const options = opts || {};
  const at = nowMs(options.now);

  const existing = sessionsOf(playerId);
  if (existing.length >= MAX_SESSIONS_PER_PLAYER) {
    const oldest = existing.sort((a, b) => a.createdAt - b.createdAt)[0];
    destroySession(oldest.id, { now: at, reason: 'session-limit' });
  }

  const token = newResumeToken();
  const session = {
    id: newSessionId(),
    playerId,
    displayName: options.displayName || playerId,
    createdAt: at,
    lastSeenAt: at,
    expiresAt: at + SESSION_TTL_MS,
    resumeFingerprint: tokenFingerprint(token),
    resumedFrom: null,
    resumeCount: 0,
    state: 'active',
  };

  sessions.set(session.id, session);
  resumeIndex.set(token, session.id);
  registerPresence(session, at);

  return { session: publicView(session), resumeToken: token };
}

function resumeSession(token, opts) {
  const options = opts || {};
  const at = nowMs(options.now);

  const previousId = resumeIndex.get(token);
  if (!previousId) {
    return { ok: false, reason: 'unknown-token' };
  }

  const previous = sessions.get(previousId);
  if (!previous) {
    resumeIndex.delete(token);
    return { ok: false, reason: 'session-gone' };
  }

  const idleFor = at - previous.lastSeenAt;
  if (idleFor > RESUME_WINDOW_MS) {
    destroySession(previous.id, { now: at, reason: 'resume-window-elapsed' });
    resumeIndex.delete(token);
    return { ok: false, reason: 'resume-window-elapsed' };
  }

  const nextToken = newResumeToken();
  const resumed = {
    id: newSessionId(),
    playerId: previous.playerId,
    displayName: previous.displayName,
    createdAt: at,
    lastSeenAt: at,
    expiresAt: at + SESSION_TTL_MS,
    resumeFingerprint: tokenFingerprint(nextToken),
    resumedFrom: previous.id,
    resumeCount: previous.resumeCount + 1,
    state: 'active',
  };

  dropPresence(previous, at);
  sessions.delete(previous.id);
  resumeIndex.delete(token);

  sessions.set(resumed.id, resumed);
  resumeIndex.set(nextToken, resumed.id);
  registerPresence(resumed, at);

  return { ok: true, session: publicView(resumed), resumeToken: nextToken };
}

function touchSession(sessionId, opts) {
  const options = opts || {};
  const at = nowMs(options.now);

  const session = sessions.get(sessionId);
  if (!session) return { ok: false, reason: 'unknown-session' };

  session.lastSeenAt = at;
  session.expiresAt = at + SESSION_TTL_MS;
  if (session.state === 'stale') session.state = 'active';

  const entry = presence.get(presenceKey(session));
  if (entry) {
    entry.lastSeenAt = at;
    entry.sessionId = session.id;
  } else {
    registerPresence(session, at);
  }

  return { ok: true, session: publicView(session) };
}

function destroySession(sessionId, opts) {
  const options = opts || {};
  const at = nowMs(options.now);

  const session = sessions.get(sessionId);
  if (!session) return { ok: false, reason: 'unknown-session' };

  dropPresence(session, at);
  sessions.delete(session.id);

  for (const [token, id] of resumeIndex.entries()) {
    if (id === session.id) resumeIndex.delete(token);
  }

  return { ok: true, reason: options.reason || 'destroyed' };
}

function registerPresence(session, at) {
  const key = presenceKey(session);
  presence.set(key, {
    playerId: session.playerId,
    displayName: session.displayName,
    sessionId: session.id,
    since: at,
    lastSeenAt: at,
  });
}

function dropPresence(session, at) {
  const key = presenceKey(session);
  const entry = presence.get(key);
  if (!entry) return false;
  if (entry.sessionId !== session.id) return false;
  presence.delete(key);
  return true;
}

function isStale(session, at) {
  return at - session.lastSeenAt > HEARTBEAT_GRACE_MS;
}

function isExpired(session, at) {
  return at >= session.expiresAt;
}

function sweep(opts) {
  const options = opts || {};
  const at = nowMs(options.now);

  const expired = [];
  const wentStale = [];

  for (const session of [...sessions.values()]) {
    if (isExpired(session, at)) {
      destroySession(session.id, { now: at, reason: 'expired' });
      expired.push(session.id);
      continue;
    }
    if (session.state === 'active' && isStale(session, at)) {
      session.state = 'stale';
      wentStale.push(session.id);
    }
  }

  return { expired, wentStale, at };
}

function listOnline(opts) {
  const options = opts || {};
  const at = nowMs(options.now);

  const out = [];
  for (const entry of presence.values()) {
    out.push({
      playerId: entry.playerId,
      displayName: entry.displayName,
      idleMs: at - entry.lastSeenAt,
      since: entry.since,
    });
  }

  out.sort((a, b) => a.since - b.since || a.playerId.localeCompare(b.playerId));
  return out;
}

function onlineCount() {
  return presence.size;
}

function getSession(sessionId) {
  const session = sessions.get(sessionId);
  return session ? publicView(session) : null;
}

function publicView(session) {
  return {
    id: session.id,
    playerId: session.playerId,
    displayName: session.displayName,
    createdAt: session.createdAt,
    lastSeenAt: session.lastSeenAt,
    expiresAt: session.expiresAt,
    resumeCount: session.resumeCount,
    state: session.state,
  };
}

function stats(opts) {
  const options = opts || {};
  const at = nowMs(options.now);

  let active = 0;
  let stale = 0;
  for (const session of sessions.values()) {
    if (session.state === 'stale' || isStale(session, at)) stale += 1;
    else active += 1;
  }

  return {
    sessions: sessions.size,
    presence: presence.size,
    resumeTokens: resumeIndex.size,
    active,
    stale,
  };
}

function reset() {
  sessions.clear();
  presence.clear();
  resumeIndex.clear();
}

module.exports = {
  SESSION_TTL_MS,
  HEARTBEAT_GRACE_MS,
  RESUME_WINDOW_MS,
  MAX_SESSIONS_PER_PLAYER,
  createSession,
  resumeSession,
  touchSession,
  destroySession,
  getSession,
  listOnline,
  onlineCount,
  sweep,
  stats,
  reset,
};
