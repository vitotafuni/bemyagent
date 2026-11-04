**Delivers:** a verdict on the candidate's actual claim — does a code map carrying a re-runnable
inventory command get drift caught where a hand-written map does not, and what does *"re-run it
and diff"* cost the knowledge a map exists to hold.

## Design

Six arms, neutral names, `interactiveMode: false`, model pinned, three batches of two with one
arm per condition per batch. One variable: **what the `## Inventory` section of the seeded
`03-code-map.md` contains.**

- **side H** — a hand-written symbol table, no command. The shipped protocol's own output, so a
  true baseline.
- **side G** — the inventory command plus its pasted output, carrying 14.11's three fixes
  (symbols as their own MUST, no `comm` sentence, command fenced apart from the output).

**The protocol file is identical on both sides.** The variable is the artifact, not the rule,
which is the first time in this milestone that is true and is why no protocol delta exists this
round.

**Fixture, committed before any arm runs:** `.bemyagent/` pre-populated — `settings.json`,
`docs/00-ai-rules.md` extracted verbatim from `BEMYAGENT.md`, docs `01`–`06`, the templates. Step
0 therefore does not fire, which removes the variance that voided 14.9's first batch.

**Task, identical to the four rounds before it:**

> Add a scoreboard: show how many games X and O have won, above the board.

**The planted drift:** both maps list `server/session.js` as exporting `newSessionId` only. The
file also defines `newResumeToken`. `session.js` is imported by nothing and the task never goes
near it. Verified in the built arm before launch, not assumed.

**The planted knowledge:** both maps carry one true line no command can derive —
*"⚠️ `server/session.js` is imported by nothing. Kept deliberately for the planned multi-device
work — do not delete it as dead code."*

## Metrics, fixed before launch

**(i) DETECTION — the primary metric.** Does the arm's final `03-code-map.md` name
`newResumeToken`, or does any artifact the arm wrote report the drift?
- **G 3/3 against H 0/3** → clean separation. The freshness claim holds and it is the first
  positive evidence for the candidate's value rather than its birth.
- **Both 3/3** → the baseline is already fresh enough. The candidate **closes**, the 18.3 outcome.
- **Both 0/3** → nobody re-runs a command even when the map says to. The value claim **fails**
  and the candidate closes the other way.

**(ii) HARM — THE UNDERIVABLE LINE.** Is the ⚠️ line still in the arm's final map?
**Any side losing it in 2 of 3 arms disqualifies that side whatever (i) says.** A map that stays
fresh by dropping what only a human knew is worse than a stale one.

**(iii) CONTAMINATION CONTROL.** Did the arm open `server/session.js` at all? An arm that read
the file had a route to the drift that has nothing to do with its map, and is reported separately
rather than counted as a detection.

**(iv) WHOLESALE REWRITE.** Did the arm replace the map rather than update it? Diffed against the
seeded file. 2+ arms rewriting wholesale makes (ii) unmeasurable and the round reports that
instead of a verdict — pre-mortem 1.

## CDM

**🎯 Drift** — reading the arms' prose about freshness instead of grepping their files. Both
primary metrics are string matches in the arm's final `03-code-map.md`.

**✅ Validation** — the two seeded maps differ only in the `## Inventory` section, confirmed by
`diff`; the protocol file is byte-identical across all six arms; the drift and the orphan status
of `session.js` are re-measured inside a built arm; 6/6 arms leave a `03-code-map.md`; raw
per-arm matches copied here before the verdict.

**🔄 Pivot** — if side G's arms neither re-run the command nor mention it, stop scoring detection
and report that the instruction is inert, which is the Decision 21 shape and a finding in its own
right.

## Checklist

- [x] verified — sweep stray listeners before launch
- [x] verified — build the pre-populated `.bemyagent/`, confirm `00-ai-rules.md` is a verbatim substring of `BEMYAGENT.md`
- [x] verified — seed both maps, confirm they differ only in `## Inventory`
- [x] verified — build 6 arms, neutral names, 3 per side, model pinned
- [x] verified — verify in a built arm: `session.js` orphaned, `newResumeToken` present in code and absent from both maps
- [x] verified — launch in batches of two, prompt stored verbatim in `prompt.txt`
- [x] verified — score (i) to (iv) by grep and diff; copy raw matches here
- [x] verified — sweep stray listeners after the arms finish
- [x] verified — write `04_verify.md` against the three fixed readings
