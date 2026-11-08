**Delivers:** whether a cheap tier using the protocol reaches an expensive tier that has none —
the comparison 20.2's verdict pointed at and could not make.

## Design

Six arms, three batches of one arm per condition.

| condition | arms | tier | repository |
|---|---|---|---|
| **S** | q85 q87 q89 | **Sonnet**, pinned | 20.2's P tree: fixture + `BEMYAGENT.md` + a populated, committed `.bemyagent/` |
| **O** | q86 q88 q90 | **Opus**, pinned | 20.2's N tree: the same fixture, no `BEMYAGENT.md`, no `.bemyagent/`, no `CLAUDE.md` |

Prompts `prompt_P.txt` and `prompt_N.txt`, byte-identical to 20.2's. They differ only by the two
protocol sentences, which is the condition and not a second variable.

Task unchanged: *Add a scoreboard: show how many games X and O have won, above the board.*

## Metrics — 20.2's, unchanged, so the two rounds are comparable

**(i) DO THE TESTS HAVE TEETH.** In each arm's own tree, change its own tally so a draw counts
as a win for X, then run that arm's own suite. **Red = the tests guard the behaviour.** Green =
they decorate it. Where the edit cannot be applied, `n/a` — never a pass.

**(ii) DISTINCT PRE-EXISTING DEFECTS SURFACED**, against the list fixed in 20.2 and not changed
here, counted from the arm's entire output so an arm that writes no docs is not penalised.

**(iii) DELIVERY.** Scoreboard present, `npm test` green.

**(iv) COST.** Weighted tokens per arm over this round's transcripts only, then the same figure
divided by the tier price, because the question is value per unit of money and not per token.

## Readings, fixed now

- **S ≥ O on (i) and (ii)** → the cheap tier with the protocol matches or beats the expensive
  tier without it, and since it also costs an order of magnitude less per token, the protocol's
  2.54× overhead from 20.2 is bought back. **The strongest result this project could get**, and
  for that reason the one to state most carefully.
- **O ahead on (i) or (ii)** → the protocol does not close the tier gap on this task. **Written
  first in `04_verify.md`, before anything else.**
- **A tie on both** → the gap is closed on these metrics; cost then decides, and the honest
  statement is about this task only.
- Any clean separation at 0/3 vs 3/3 is signal; anything narrower is read against 14.14's table.

## CDM — Heavy

**🎯 Drift** — declaring a winner on delivery, which both sides are expected to achieve.
**✅ Validation** — as fixed in `01_think.md`.
**🔄 Pivot** — Opus arms refusing or asking for a spec means the prompt is being measured.

## Checklist

- [x] verified — sweep ports
- [x] verified — build six arms; S diffs clean against a 20.2 P arm, O against a 20.2 N arm
- [x] verified — confirm the O trees hold no protocol file of any kind
- [x] verified — three batches, tier pinned per arm, both prompts stored before launch
- [x] verified — fill `EDITS` and `AGENT` from THIS round's arms, never inherited
- [x] verified — score (i)–(iv), raw output here before the verdict
- [x] verified — 19.4 check: open the arm at each end of every metric and name it
- [x] verified — sweep ports after, write `04_verify.md`, then `05` and the plan
