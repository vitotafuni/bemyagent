# 15.9a — feasibility probe, not a round

**This is a probe, not a TTEV leaf, and it is filed as one.** `harness/README.md` requires
checking that a rule has an occasion to fire *before* arms are designed; 14.1 and 18.2 both paid
for skipping it. Writing a forward `01`/`02` for work already done would be theatre, so there is
none. Zero arms spent: every figure comes from trees four earlier rounds already paid for.

## The question

15.9 asks about a standing rule that does **not** announce itself. 19.2a's fixture carried two
team conventions appended by hand inside `00-ai-rules.md`, which 6/6 arms migrated into
`05-decisions-and-issues.md` and several arms then claimed had shaped their code:

> every HTTP handler in `server/index.js` returns `{ error }` with a 4xx, never a bare string
> tests live beside the layer they exercise and never reach across one

Three later rounds ran the same fixture family and the same task **without** those conventions:
14.13, 19.2b and 15.4. That is a free comparison, 6 arms against 18.

## Convention 1 has no occasion at all

The feature's only new route is `GET /api/scores`, which takes no input. Several arms wrote this
down themselves — *"no error path, dispositioned as unreachable"*. A rule about 4xx shapes cannot
fire where a 4xx cannot occur.

## Convention 2's stated behaviour is already near-universal

A test that reaches across a layer — booting the app, fetching over HTTP — appears in **2 of the
18 arms that were never told not to**. With the convention, 0 of 6.

**0/6 against 2/18 is not separation, it is an absent occasion.** The convention forbids
something these agents almost never do on this fixture. Running six arms to confirm that is the
14.1 mistake, where the fixture had no file above the slicing threshold and no delegation rule
could have fired.

## What does correlate, recorded as an observation and not as a result

| | layer-named (`store.test.js`) | feature-named (`scores.test.js`, `scoreboard.test.js`) |
|---|---|---|
| **19.2a, convention present** | **6 of 6** | 0 |
| 14.13, 19.2b, 15.4 — no convention | 3 | 10 |

Among arms that added a test file at all, every arm holding the convention named it after the
module it exercises, and 3 of 13 did so without it.

**Not believed, and the reasons are the ones this repo keeps relearning.** It was not
pre-registered. It compares across rounds rather than within one, and 14.12 against 14.13 showed
the same condition reading 1/3 and 3/3 a day apart. A filename is a visible correlate of a
convention, not the behaviour the convention describes — which is harness rule 1, measure the
mechanism and not a downstream proxy. It is written down so it is not re-discovered as news.

## What this decides

**15.9 does not get a round on this fixture**, for this pair of conventions. A round needs a
convention whose violation is the *cheap* path, so that following it costs something. These two
cost nothing to follow here, which is why the control already follows them.

That is the constraint 15.9 now carries, and it is the same shape as the one 19.2a handed 19.2b
and 19.3 handed 19.2: each round this week has narrowed the next by saying what cannot be
measured, which is cheaper than six arms saying it.
