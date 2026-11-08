# VERIFY — 20.3, Sonnet with the protocol against Opus without it

Six arms, three batches of one per condition. Raw output in `03d_score_output.json` and
`03c_arm_evidence.txt`, both written before this file. Prompts byte-identical to 20.2's. Seed
validation in `03b_delta.txt`.

## First, the reading that was promised first

`02_tasks.md` fixed that **if O leads on anything it is written before anything else.** It does
not lead on (i), (ii), (iii) or (iv). The sentence is kept anyway, because the reason it was
written is that the project wanted the other answer.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| S seed = 20.2's P seed | PASS | 726 files, differing only on `BEMYAGENT.md` (19.5's Step 0 line, which a populated `.bemyagent/` cannot reach) |
| O seed = 20.2's N seed | PASS | 10 files, no difference at all |
| O trees hold no protocol file of any kind | PASS | no `BEMYAGENT.md`, `.bemyagent/`, `CLAUDE.md`, `AGENTS.md` |
| S vs S and O vs O identical | PASS | `03b_delta.txt` |
| `EDITS` and `AGENT` filled from this round only | PASS | both blanked at build, filled per batch |
| Ports swept both ends | PASS | nothing left on 47xxx, 48xxx, 87xx |
| Both ends of every metric opened and named | PASS | `03_execute.log`, batch 3 |

## (i) Do the arm's own tests have teeth — **clean separation, 3/3 against 0/3**

A drawn game made to count as a win for X, in each arm's own tally, with that arm's own suite.

| | q85 S | q87 S | q89 S | q86 O | q88 O | q90 O |
|---|---|---|---|---|---|---|
| | **RED** | **RED** | **RED** | GREEN | GREEN | GREEN |

The mechanism is not subtle and is on disk: **every S arm left a test behind** — q85
`score.test.js`, q87 `store.test.js`, q89 extended `rules.test.js` — and all three suites run 5.
**Every O arm left `test/` exactly as seeded**, running the same 4 tests it was given.

**This is not a difference in care, and reading it that way would be wrong.** q88's own
verification was the most thorough of any arm in the round: it drove `client/app.js` against a
live server under a DOM stub and played an X win, an O win, a draw, a rejected move, an
abandoned game and a second X win, confirming the tally moved on exactly the right ones. q90 went
further and **named the omission**: *"I did not add an automated test … Say the word and I'll
add one."* The expensive model without the protocol checked more and **left less**.

The difference the metric detects is **where the check is put**. One side's verification ends
when the agent stops; the other side's is still in the repository tomorrow.

## (ii) Defects surfaced — **no separation**

S 1, 0, 1. O 1, 0, 0. Two against one over six arms, against a list of six. By 14.14's table
this is **under-powered, not a null**: the metric has one observation per arm and the rates are
too close to read at N=3. 20.2 reached the same place on the same metric.

## (iii) Delivery — tie

6/6 shipped a working scoreboard above the board, all suites green, draws excluded by every arm.

## (iv) Cost — **the cheap tier used fewer tokens, not merely cheaper ones**

Weighted tokens per arm, this round's transcripts only:

| | S (Sonnet + protocol) | O (Opus, none) |
|---|---|---|
| | 277,332 / 264,395 / 250,225 | 300,276 / 297,128 / 312,394 |
| mean | **263,984** | **303,266** |

**S costs 0.87× the tokens of O.** The gap is cache-read volume, not output.

This is the part worth being careful about. 20.2 measured the protocol's overhead at **2.54×
against no protocol on the same tier**, and that figure stands — it is not contradicted here,
because this round changes two things at once. What this round shows is that **the overhead is
paid out of a budget that shrinks faster**: a cheaper tier running the protocol spent fewer
tokens than the expensive tier running nothing, on the same task.

The money ratio then follows from the tier price ratio, which this round does **not** measure.
At the ratio the user stated (Sonnet ≈ a tenth of Opus), 0.87 × 0.1 ≈ **0.09**, about a twelfth
of the cost. That figure is arithmetic on an assumption, not a measurement, and is labelled so.

## Verdict

**On this task, the cheap tier with the protocol beat the expensive tier without it on the only
metric that separated, tied on the rest, and cost less in tokens before any price ratio is
applied.**

The break-even the user set out — t = r, token ratio against price ratio — is not merely met.
**t came in below 1**, so the comparison does not depend on the price ratio at all; the price
ratio only decides how large the margin is.

## What this does not say

1. **One task, one shot, no context reset.** 20.2's limits are inherited whole. The mechanism
   TTEV exists for — resuming from a cleared context — still has never had an occasion in any
   round this project has run.
2. **Only machine-observable value.** The protocol's stated audience is the human, and nothing
   here reads the documents a human would read.
3. **The round changes two variables at once** — tier and protocol — by design. It cannot say
   how much of the result is the protocol and how much is Opus-without-scaffolding behaving
   like an agent with no reason to write a test. **A third condition, Opus + protocol, would
   separate them**, was rejected on price, and is the obvious next round.
4. **(i) rewards leaving a test**, which is close to rewarding the protocol for asking for one.
   The defence is that §4 does **not** ask for a test: 20.2 recorded a protocol arm that wrote
   no test, verified live and thoroughly, and complied exactly. The behaviour is downstream of
   the protocol, not written into it.
5. **N=3.** Clean separation is signal here, as always, and nothing narrower was read as one.

## Cost of the round
≈ 316 k subagent tokens raw over six arms; weighted, 1.70 M.
