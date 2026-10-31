## Context
- 18.1 measured the clause clean on a task with **one** open decision: 3/3 surfaced, 0/3 over-triggered. It did not land, because the rate on a task with several ambiguities is where guarantee 1 is actually charged. This round supplies that task, and tests the rewording the arms themselves proposed.

### Context Saturation Check
- [x] **Target files/paths** — `BEMYAGENT.md` line 91, same bullet as 18.1
- [x] **Expected behavior** — 18.1's clause and the arms' reversibility rewording, one per side
- [x] **Constraints** — guarantee 1; harness rule 4 (harm arm); only clean separation at N=3
- [x] **Dependencies** — none new; same fixture

0 unchecked. Proceed.

## The two wordings

**Side o (ownership, as shipped in 18.1)** — *"A product decision counts on its own: where more
than one answer is defensible and the user owns which, one is enough to STOP and ask, whatever
the count. An implementation fact you can verify is not a product decision."*

**Side r (reversibility, proposed by 18.1's arms)** — *"A decision whose wrong answer is
expensive to undo counts on its own: if getting it wrong means rewriting an interface, a schema
or the shape of the change rather than editing a detail inside it, one is enough to STOP and
ask, whatever the count. A choice you can reverse by editing one file, or a fact you can verify
by reading the repo, is not one."*

One variable: the wording. Both sides carry a clause; neither is a bare baseline, because 18.1
already recorded the bare protocol at 0/3 surfaced.

## The task, and why it is the right instrument

> Add a scoreboard: show how many games X and O have won, above the board.

Verified in the fixture before writing it: no score exists anywhere (the only `wins` is a
display string); `game` rows accumulate (`AUTOINCREMENT`, no delete); `server/session.js` is
not imported by anything, so there is **no live notion of a device or a sitting**.

That seeds decisions of deliberately mixed cost:

| | kind | cost of a wrong answer |
|---|---|---|
| Score over all games in the database, or only this sitting? | product | **expensive** — "this sitting" needs a session concept the app does not have |
| Does the score survive a restart? | product | **expensive** — decides whether it is derived or stored |
| Do draws appear, and how? | product | cheap, one file |
| Is there a reset, and where? | product | cheap, one file |
| Would a new column on `game` reach an existing database? | **fact** | none — `db/schema.sql` is `CREATE TABLE IF NOT EXISTS`, readable in ten seconds |

The fact is the trap: an arm that stops to ask it has stopped on something it could have
checked, which is the harm both wordings claim to exclude.

## Approaches Considered
**A — 3 arms, ownership wording only.** Cheaper; answers the rate question but not which
wording to land. **B — 6 arms, both wordings.** Answers both, and the rewording is the only
live candidate for fixing an over-stop if one appears. **Chosen: B.**

## Selected Approach & Risks
- Estimated token cost: **medium** (6 arms, most will plan and stop rather than build)
- **Risk — both sides stop on everything.** Then the clause is a form to fill in and the
  verdict is a rejection, whatever 18.1 showed. This is the outcome the round exists to find.
- **Risk — the cheap decisions get stopped on.** Scored explicitly: the stop count is the
  metric, not whether a stop happened.
- **Risk — scoring my own candidate.** 18.1's blinding failed because hand-back reports name
  their directory. Unfixable here (both sides are in one batch), so the mitigation is the
  rubric below, fixed before launch, computed from file-level facts: the count of blocking
  items, and whether the fact appears among them.

### Pre-mortem
1. *Stop counts are identical across wordings.* Then the wording does not matter and the
   question reduces to whether the count itself is acceptable.
2. *Arms stop on 4-5 items each.* Decisive rejection of the clause in both wordings, and the
   Devil's Advocate from 18.1 (a mandatory possibly-empty `Open decisions` section in the
   template) becomes the only surviving candidate.

### Devil's Advocate
Cap it: *"stop for at most one decision; carry the rest as stated assumptions."* Forces ranking
instead of enumeration, which is what the user actually needs. Not tested this round because it
is a third wording and the round already carries two; recorded for 18.3 if both sides over-stop.

## Verification Plan
Per arm: the number of items marked blocking, whether the verifiable fact is among them, and
whether anything shipped. Scored from the arm trees, never from hand-back text. Signal is a
clean difference in stop count between sides; absent that, the verdict is about the absolute
count and the wordings are reported as equivalent.
