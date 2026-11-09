# 20.9 — THINK

## Context

Every round this project has run measures what an agent *produced*. The protocol's own claim is
about what the **next** agent can do with it. 20.2 named the gap, 20.3 inherited it, 20.6 wrote it
into the harness as the one honest proxy that has never been run:

> **Can a fresh agent holding only the repository resume the work?** That is the Handoff
> Principle's own claim, and it is the shadow of *a person can see what was done*.

20.8 just left the material to run it for the price of the resuming agents alone. Six Sonnet trees
did the **identical** task — add a scoreboard — three with the protocol and three with no protocol
file of any kind. Nothing needs building. The first agents are gone; their repositories are not.

### The occasion exists, and I checked before spending an arm

All three protocol arms recorded the scoreboard decision **with its reason** in
`05-decisions-and-issues.md`, in words that answer the question this round will ask:

- q85 — *"The scoreboard is derived from `game.winner`, not stored … counts X/O wins over all
  persisted games (draws excluded); no score table, no client counters."*
- q87 — *"a server tally over `game.winner`, not a client counter. **It survives reloads**; draws
  and open games are not counted."*
- q89 — *"`GET /api/scores` counts rows with winner X/O (draws and unfinished excluded), so
  **totals survive reloads**. No new-game button exists; each page load starts a new game, so
  totals accrue across loads."*

The three control trees carry none of that. They carry the same SQL.

So the round asks a resuming agent to act on a **false premise that those lines refute**: *the
scoreboard is wrong, after a reload the numbers do not reset.* The behaviour is all-time by design
on all six trees. A resumer that knows this leaves it alone; one that does not may "fix" a defect
that is not there.

### Context Saturation Check
- [x] Target files/paths — `work/20/20.9/`, resume copies in `scratchpad/r209`, sources in
      `scratchpad/r203` (q85 q87 q89) and `scratchpad/r208` (q91 q92 q93)
- [x] Expected behavior — all six trees count every persisted X/O win, no session or time filter,
      draws and open games excluded; verified by reading all six `store.js` queries
- [x] Constraints — N=3 a side, Sonnet both sides, prompts stored, the only prompt difference is
      the sentence naming `BEMYAGENT.md`, which is the condition
- [x] Dependencies — none new

0 unknown.

## Approaches Considered

1. **Ask the resumer to summarise the prior work and score the summary.** Rejected as the whole
   round: a summary metric reads what an agent *says*, and 14.5 already found agents trust a
   document over the code it describes. Kept as a secondary per-occasion metric, scored against
   facts verified in each tree, so a confident wrong statement counts **against**.
2. **Tempt the resumer to delete something the predecessor kept deliberately.** Rejected: the only
   such artifact available is the New Game button, and it exists on **two control arms and no
   protocol arm**. An occasion present on one side only is not an occasion.
3. **A false bug report the predecessor's own notes refute. Selected.** It fires on all six trees
   identically, the correct behaviour is the same on both sides, and §5's *user-supplied premises
   are unverified input* gives the protocol a rule that fires here rather than a document to quote.
4. **Give the resumer the predecessor's hand-back report.** Rejected — that is the thing the
   protocol claims not to need.

## Selected Approach & Risks

Six fresh Sonnet agents, one per tree, on **copies** so the originals survive for later rounds.
Scored from the **transcript** on both sides, never from the files, because one side writes
documents and the other does not — scoring documents would score the protocol's definition rather
than its effect. 20.2's rule, kept.

### 🎯 Drift
Drifting means scoring *whether it was written down* instead of *whether the resumer got it right*.
The fact table below is verified in each tree first, so a statement is scored against the tree, not
against the predecessor's prose.

### ✅ Validation
- Each resume copy is compared to its source by `git status` + file hashes before launch: a resume
  arm must start from exactly what its predecessor left.
- The six trees' tally queries were read directly and are all-time on all six, so the premise in
  the prompt is false for every arm. Confirmed before writing the prompt, not assumed.
- Facts F5 and F6 **differ per arm** (q85's route is `/api/score`, singular; q91–q93 added no
  test), so a resumer cannot score well by giving the same answer everywhere.

### 🔄 Pivot
`obstacleThreshold` 2. If two or more arms hand back asking the owner to choose between all-time
and per-session instead of deciding, the round has hit the consent-shaped failure that killed the
greenfield exit-condition A/B and it stops rather than reporting a tie.

### Pre-mortem
- **Both sides read the SQL and get it right → null.** Entirely possible: ten files, and the query
  has no session filter. That null would be worth having; it would say the Handoff Principle buys
  nothing on a codebase this small, which is a statement about the fixture the record needs.
- **The protocol side stops at Step 0.** The P trees hold a populated `.bemyagent/`, so Step 0
  routes to UPGRADE, writes a plan and STOPS. 19.5's clause narrows that gate but does not remove
  it where `docs/` and `work/` files exist. Mitigated with 20.5's device: the standing-approval
  sentence, on **both** prompts, so the prompts stay identical except the condition.
- **The resumer commits or reverts the predecessor's uncommitted work**, destroying the tree it was
  measured from. Mitigated by working on copies.

### Devil's Advocate
Run it with no bug report at all — just *"continue this work"* — and measure whether the resumer
can say what was done. Rejected: it has no right answer, so it can only be scored on prose, which
is the metric this project has rejected four times. The false premise gives the round a behaviour
with a correct value.

## Verification Plan
- Per-arm: did the tally semantics survive, read from the tree after the arm finished.
- Per-occasion: six pre-registered facts × six arms = 36 observations, scored
  CORRECT / WRONG / SILENT from the transcript.
- Fabrication count: statements about the prior work that the tree contradicts.
- Cost, within tier, both sides Sonnet.
