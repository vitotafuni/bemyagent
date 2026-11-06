**Delivers:** the first measurement of whether the shipped protocol buys anything over no
protocol, and what it costs to do so.

## Design

Six arms, two conditions, **no protocol delta** — the variable is the protocol's presence.

| | repository |
|---|---|
| **P** (protocol) | fixture + `BEMYAGENT.md` + a populated, committed `.bemyagent/` (15.4's seed) |
| **N** (none) | the same fixture, no `BEMYAGENT.md`, no `.bemyagent/`, no `CLAUDE.md` |

`q52 P · q53 N · q54 P · q55 N · q56 P · q57 N`, three batches of one arm per condition, model
pinned, both prompts stored. The N prompt drops the two protocol sentences, which is the
condition and not a second variable.

Task unchanged from every previous round: *Add a scoreboard: show how many games X and O have
won, above the board.*

## Metrics, fixed before launch

**(i) DO THE TESTS HAVE TEETH.** In each arm's own tree, read its win-counting code, change the
filter so draws are counted, run that arm's own suite. **Red = the tests guard the behaviour.**
Green = they decorate it. Where the mutation cannot be applied, report n/a; never count it as a
pass.

**(ii) DISTINCT PRE-EXISTING DEFECTS SURFACED.** Counted against a fixed list written before the
arms ran: `api()` never checks `res.ok`; a reload starts a new game against `01-overview.md`'s
claim; `server/session.js` is imported by nothing; the moves handler is an untransacted
read-modify-write; `Number(undefined)` makes a missing cell report "occupied"; the stale "draws
are not displayed" issue. Counted from the arm's **entire output**, so an arm that writes no
docs is not penalised for having no docs.

**(iii) DELIVERY.** Scoreboard present and `npm test` green.

**(iv) COST.** Weighted tokens per arm, `cost.py` over this round's transcripts only.

**Readings, fixed now:**
- **P 3/3 on (i) against N 0/3**, or a clean separation on (ii) → the protocol buys something
  observable, and the size of (iv) decides what it is worth.
- **A tie on (i) and (ii) with P costing more on (iv)** → the protocol is ceremony on this task,
  reported exactly that plainly.
- **A tie at equal cost** → the protocol is free and inert here; also reported.
- **N ahead on anything** → reported first, before anything else in `04_verify.md`.

## CDM

**🎯 Drift** — scoring the protocol's own artifacts. `03_execute.log` exists on one side by
definition; nothing that only one condition can produce is a metric here.

**✅ Validation** — the P seed identical to 15.4's, confirmed by `diff -r`; the N trees confirmed
to hold no `BEMYAGENT.md`, no `.bemyagent/`, no `CLAUDE.md`; both prompts stored and their
difference confirmed to be only the protocol sentences; each batch complete before the next;
scorer and raw output copied here; **19.4's check performed and the arms named, one line per
metric.**

**🔄 Pivot** — if the N arms refuse the task or ask for a spec, the round is measuring the prompt
and not the protocol. Report that and rebuild the prompt.

## Checklist

- [x] verified — sweep stray listeners
- [x] verified — build 6 arms, 3 with the 15.4 seed, 3 bare; confirm both by inspection
- [x] verified — confirm the fixture builds and `npm test` is green on both shapes
- [x] verified — store both prompts; confirm the delta is only the protocol sentences
- [x] verified — launch in three batches of one arm per condition
- [x] verified — score (i) to (iv) by execution; copy raw output and scorer here
- [x] verified — **19.4 check: open the arms at each end of every metric, name them**
- [x] verified — write `04_verify.md` against the fixed readings
- [x] verified — sweep ports, update `05` and `06`
