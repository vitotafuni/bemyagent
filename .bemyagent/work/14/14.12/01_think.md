## Context
- 14.11 is written in the plan as round three: make the symbols half a MUST, drop the `comm`
  sentence, fence the command away from its output. **Those three changes are right and they are
  free.** What is not right is spending six arms on them, and this file says why before it
  proposes something else.
- **14.11 cannot produce signal at N=3.** Its question is whether obligating the symbols half
  closes the bare-enumeration exit. The exit's rate in the control is **2 of 6**. This harness
  reads only clean separation at N=3 (`harness/README.md`), so a treatment coming back 0/3 is
  what a control would plausibly do anyway. The round's likely outcome is uninterpretable, and an
  uninterpretable round that confirms my own candidate is the worst thing I can buy here.
- **And the candidate has never been tested on its actual claim.** 14.8 and 14.9 both asked
  whether the command is good *at birth*. The claim is about turn two — the owner's own reframe,
  *drift becomes detectable by diff*, and *any reliable tool that keeps the code base aligned
  with the code map beats us*. Nothing has measured that. 14.6 already taught the distinction in
  this exact milestone: 6/6 arms invoked the graph and 6/6 built on the wrong function, so
  **invocation is not value**. 17.2 taught the ordering: the harm arm outranked the benefit arm
  and settled the line on its own.

### Context Saturation Check
- [x] **Target files/paths** — a pre-populated `.bemyagent/` in the fixture; `03-code-map.md` is the instrument, not the protocol file
- [x] **Expected behavior** — an arm whose map names a re-runnable command catches drift the map does not mention
- [x] **Constraints** — only clean separation at N=3; harness rule 4; the harm must be reachable
- [x] **Dependencies** — none new; the drift already exists in `server/session.js`

0 unchecked. Proceed.

## The question

A code map carrying an inventory command, against a hand-written one. **Does the drift get
caught?** That is the whole value proposition of the candidate and it is the one thing two rounds
of clause-tightening never touched.

## Design, and why this fixture is different from the last two

Both previous rounds ran on a **bare** `.bemyagent/`, so every arm bootstrapped and the artifact
under test was born during the round. That is also what voided 14.9's first batch. Here the
scaffold is **pre-populated and committed**, which does three things at once: Step 0 never fires,
the map is an input rather than an output, and the round measures use instead of creation.

**side H** — `03-code-map.md` holds a hand-written symbol table. No command. This is what the
shipped protocol produces today, so it is a true baseline and not a second treatment.

**side G** — the same map, with the inventory command and its pasted output in place of the
table, carrying the round-three wording (symbols as their own MUST, no `comm` sentence, command
fenced apart from its output). Those three fixes ride along as part of the artifact instead of
costing their own round.

**Both maps are stale in the same way**, and the staleness is the measurement.

## The planted drift, chosen so that only a re-run finds it

`server/session.js` is orphaned — imported by nothing, which `14.1` established when it was added
to the fixture. Both maps list it as exporting `newSessionId` alone. The file also defines
`newResumeToken`. The task is the scoreboard, which lives in `client/` and `server/store.js` and
gives an arm **no reason whatever to open `session.js`**.

So a directory listing does not reveal it, reading the files the task needs does not reveal it,
and the arm's own diff does not touch it. Re-running the command does, in one line. Side H has
nothing to re-run.

This is the 18.3 trap taken seriously in advance: that round died because **the baseline surfaced
the decision anyway**. If an arm can stumble onto the drift while doing the task, the round
measures the task and not the map.

## The harm, pre-registered, and reachable

*"Re-run it and diff"* has a cost that 14.8 already saw the shape of: a map's true, underivable
knowledge sits under a regenerable command, and the diff reports it as drift forever. The only
two ways out are to keep it and ignore the diff, or to delete it.

So both maps carry one line that is **true and underivable by any command**:

> ⚠️ `server/session.js` is imported by nothing. Kept deliberately for the planned multi-device
> work — do not delete it as dead code.

**Measured: does the arm's final map still hold that line?** Side G deleting it means the
candidate buys freshness by destroying the knowledge a map exists to carry, and that outranks any
detection number, exactly as 17.2's harm outranked 17.1's benefit.

Reachability is not assumed: the clause tells the arm the inventory is the command's output, the
command cannot emit that line, and the arm is required by §6 to update the map in the same
response as its change. The deletion is on the cheapest path, not off it.

## Approaches Considered
**A — run 14.11 as planned.** Three good changes, six arms, and a control rate that makes the
result unreadable. **B — apply 14.11's three changes to the artifact without a round, and spend
the arms on the value claim.** The changes still ship inside side G, so they are not untested so
much as not *separately* attributed, which is honest to state and cheap to revisit.
**Chosen: B.** The ordering argument is 17.2's and it held there.

## Selected Approach & Risks
- Estimated token cost: **medium** (6 arms, no bootstrap, so cheaper per arm than 14.9)
- **Risk — both sides catch it.** Then the baseline is already fresh enough and the candidate
  closes, the 18.3 outcome. Welcome: it is the cheapest possible end to a long line.
- **Risk — both sides miss it.** Then nobody re-runs a command even when the map tells them to,
  which is Decision 21's shape and kills the value claim outright.
- **Risk — an arm catches it for the wrong reason**, by reading `session.js` out of curiosity.
  Scored by looking at whether the arm's trace shows it opened the file; an arm that read it is
  reported separately and not counted as a detection.
- **Risk — scoring my own candidate.** Unchanged and unfixable in one batch. The mitigation is
  that both metrics are string matches in the arm's final file: is `newResumeToken` present, is
  the ⚠️ line present.

### Pre-mortem
1. *The arms rewrite the whole map from scratch.* Then both metrics collapse into "did it
   regenerate" and the harm is unmeasurable. Detected by diffing the arm's map against the seeded
   one; if 2+ arms rewrote wholesale, the round reports that instead and the fixture needs a map
   large enough that rewriting is not the cheap path.
2. *The §6 CRITICAL rule makes every arm touch the map anyway*, so side H updates it by hand and
   happens to re-derive. That is the baseline doing its job and it is the 18.3 result, reported
   as such.

### Devil's Advocate
Skip the map entirely and test the check alone: *"before trusting `03-code-map.md`, diff its file
list against `git ls-files`"* — one line, no command, no generated inventory. Noted in 14.9 and
still the cheapest form of the freshness idea. Not tested here because this round's side G is the
stronger form, and if the stronger form cannot catch a planted drift the weaker one has nothing
left to prove.

## Verification Plan
Two string matches in each arm's final `03-code-map.md`, plus a read of each arm's trace for
whether it opened `session.js` at all. Scored from the files, never from the hand-back. Signal is
clean separation on detection; the harm is read whatever detection says.
