# VERIFY — 14.6 graph invocation

Verdict: **PASS_WITH_CAVEATS.** The gate opens — agents do invoke a code-graph tool when the
Routing Table orders it procedurally — but the tool changed nothing about what was built, and
this round is structurally incapable of saying whether a real graph would.

## The result

| | d (permissive) | e (procedural) |
|---|---|---|
| Invoked the tool | **0/3** | **3/3** |
| Cited `path:line` nodes in work files | 0/3 | **3/3** |
| Built the leaderboard on `listOnline()` | 3/3 | 3/3 |
| Rating table added | 3/3 | 3/3 |
| Tests passing | 5 · 6 · 6 | 5 · 6 · 6 |

Invocation logs were written by the tool to an absolute path outside the arms, so they are not
self-reports and no arm could edit them.

**Clean separation on invocation (0/3 vs 3/3)** — the harness's signal threshold, met.

## What this establishes, and it is new

Milestone 14 measured an optional affordance at 0/9 and the conclusion drawn there was that
agents do not invoke optional tools. **That conclusion was too broad.** The permissive arm
here reproduces it exactly (0/3); the procedural arm inverts it completely (3/3) with the same
tool, the same task and a one-line difference in the same Routing Table row.

So the barrier was never tool-ness. It was the declarative shape — the same lever as
Milestones 11/16/18, now demonstrated on a **tool invocation** rather than a file read or a
doc write, which is the first time this protocol has shown it there. That is a reusable fact
well beyond the Graphify question: any future rule that wants an agent to *run* something must
be phrased as a Routing Table step, not as an available option.

The forced artifact also worked here, unlike in 14.3: e-arms cited real nodes
(`session.js:228` = `listOnline`, the node the tool actually returned). The difference from
14.3's failed citation requirement is that here the citation names something the agent then
had to open and use, rather than being a claim about its own process.

## What it does NOT establish

**The tool changed the route, not the destination.** 6/6 arms built the leaderboard on
`listOnline()` and added an equivalent rating table, with equivalent tests. The d-arms found
`listOnline` by reading `session.js`; the e-arms found it through the graph. Same answer, and
no measurable difference in the work.

So: **invocation ≠ value.** This round deliberately cannot speak to value — the stub was built
precisely so that tool quality would cancel between conditions. Reading the 3/3 as evidence
that the graph *helps* would be the error this task's CDM names as Drift.

## Caveats

1. **The stub is not Graphify.** It genuinely parses the arm's files and returns real nodes,
   but it is a few hundred lines against a tree-sitter product. Propensity transfers; nothing
   about graph quality does.
2. **The cost contrast with 14.3 is not verifiable and was dropped.** These arms ran ~48–51k
   tokens and 6–11 tool calls against 14.3's ~90k and ~55 on the same task and fixture. The
   14.3 arm directories have since been removed from the scratchpad, so artifact-level
   comparison is impossible and the gap cannot be attributed. It is not used anywhere in this
   verdict. (Nothing in either line-52 phrasing would cause it, and both conditions show it.)
3. **N=3 per condition.** Clean separation is the threshold and it was met, but on one task.

## The instrument problem that governs the next round

Proving a graph has *value* needs a task where reading the files is genuinely worse than
querying a graph. The fixture cannot provide one: even with `session.js` it is under 500 lines
across 8 files, and an agent can simply read all of it. A graph earns its place on codebases
where that is impossible.

This is the 14.1 problem returning one level up — there, the fixture had no file big enough to
trigger a read rule; here, the whole fixture is small enough that no navigation tool can beat
reading. **A value round needs a substantially larger fixture**, which is a real cost and
should be decided deliberately rather than drifted into.

## Recommendation

Do not adopt Graphify on this result, and do not reject it either. What changed is that the
cheap objection is gone: the protocol *can* make an agent invoke it, reliably, with a one-line
procedural Routing Table row. What remains unanswered is the only question that matters —
whether the graph beats reading — and answering it honestly requires a bigger fixture than
this harness has.

Carried to `drafts/graphify-evaluation.md`.
