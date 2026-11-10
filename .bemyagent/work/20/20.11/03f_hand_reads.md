# 20.11 — readings taken by hand, where the instruments could not

## (iii) delivery — the regexes are 20.8's and miss two shapes

`score.py` flags `client_markup` False on q94 q95 q96 and everything False on q98. Read by hand:

- **q94 q95 q96** — markup present: `<p id="scores">` in `client/index.html`. 20.8's regex is
  `scoreboard|score-board|#score`, which does not match `id="scores"`. Tally and route present.
- **q98** — delivered **client-side**: counts kept in `localStorage`, rendered into
  `#score-X` / `#score-O` above the board, plus a *New game* button. No server tally, no route.
  The literal task is done; the design differs, and there is no server query to mutate.

**Delivery 6/6.**

## (i)/(v) teeth — two queries the regex does not match

`mutate.py` returned `n/a` on q95 (no `WHERE`) and q99 (`COUNT(*) n`, no `AS`); q98 has no server
tally. q95 and q99 mutated by hand with 20.8's transforms (`mutate_by_hand.py`, literal pairs in
`03d_mutate.txt`): **GREEN on both mutations, tree unchanged.** All six arms kept the four seeded
tests in `test/rules.test.js` and added none, so no tally mutation could turn any of them RED.

## The mechanism 20.8 found — does the plan predict the artifact?

| arm | `01_think.md` Verification Plan | test written | `04_verify.md` on independence |
|---|---|---|---|
| q94 | `npm test`; start server on a high port, play to an X win, GET /api/scores | no | *"same agent as author (no independent agent available) — weakest check"* |
| q95 | temp DB_PATH, self-chosen port, X win via curl, check /api/scores, `npm test` | no | *"Verified by the author (no independent verifier available)"* |
| q96 | server on a high port, X win via the API, check `/api/scores`; `npm test` | no | *"Self-verified (no independent agent available)"* |

**Plan predicts artifact: 3/3** (20.8 recorded 6/6). Every plan names a live API check and none
names a new test; every arm did exactly what its plan said.

## A launcher difference this round introduced, beyond the one 01_think.md named

`launch.sh` passes `--allowedTools Read Write Edit Bash Glob Grep`. **The Agent tool is not on it**,
so these arms could not spawn the second agent §4 asks for, and each said so in `04_verify.md`
under §4's fallback clause. The Agent-tool arms of 20.3 could, and most rounds' arms did (20.1:
*"most spawn a second for §4's VERIFY"*). `permission_denials` is 0 on all six: no arm tried.

## Corrections after the independent VERIFY — three claims above withdrawn

1. **"Delivery 6/6" is withdrawn.** (iii) was pre-registered as *tally, route, markup*. q98 has the
   markup and neither of the others, so by the definition fixed before launch **(iii) reads 5/6.**
   "The literal task is done" was a redefinition made after seeing q98.
2. **The launcher difference named above is not a difference.** The comparators q85 q87 q89 had the
   Agent tool, never called it, and each wrote *"no second agent available"* in its `04_verify.md`.
   Neither side of the comparison ran an independent VERIFY.
3. **"Plan predicts artifact: 3/3" does not establish the mechanism.** q85's Verification Plan reads
   *"npm test; run server on own high port, curl score, play a winning game, curl again"* — no test
   named — and q85 wrote one. Plans of the same shape produced a test there and none here, so the
   plan cannot be what predicts it. This also loosens 20.8's *"6/6"*.

## The difference that matters, found by VERIFY and confirmed: the P arms got the N prompt

`prompt.txt` here is **byte-identical to 20.3's `prompt_N.txt`** (`cmp`). It was copied from 20.8,
which had only an N side. 20.3's P arms got `prompt_P.txt`, which adds *"Read BEMYAGENT.md in the
repository root and follow it"* and a standing approval for Step 0. `01_think.md`'s *"Same prompt file
as 20.8 and 20.3, verbatim"* is false for the P side. **The P condition of 20.3 was not reproduced.**
All three reference arms opened with `cat BEMYAGENT.md`; q95 and q96 never read it, q94 once.

## Correction to correction 3 — re-checked against the files, VERIFY was right only narrowly

q85's `01_think.md` Verification Plan names no new test, but its `02_tasks.md` Validation does:
*"npm test passes incl. new score test"*. The line 20.8 quoted for q85, *"Unit test for getScores"*,
is q87's. Taking **the plan as the protocol defines it — `01` and `02`, both written before EXECUTE**:

| | named a new test in `01` or `02` | wrote one |
|---|---|---|
| q52 q56 q87 q89 | `01` | yes |
| q85 | `02` only | yes |
| q54 | neither | no |
| q94 q95 q96 | neither — each `02` reads *"`npm test` passes"* plus a live check | no |

**The plan predicts the artifact 9/9.** Correction 3 above is withdrawn: it held only for 20.8's
narrower wording, *"Verification Plan in `01_think.md`"*, under which 20.8's figure is 5/6 and its
q85 quotation is misattributed.
