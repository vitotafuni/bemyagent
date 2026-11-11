# 20.12 — VERIFY

Three protocol arms q100 q101 q102, launched by `command claude -p` from inside their own trees,
20.3's `prompt_P.txt` byte-compared before launch, scored against 20.11's certified clean controls
q97 q98 q99. Same seed, same launcher, same served model (`claude-sonnet-5-5`), same CLI
(2.1.308), same day. **Independent VERIFY** by an agent that did not do the work re-ran every
instrument to identical output; its five corrections are in `03_execute.log` and applied below.

## Against the readings fixed before launch

| | metric | predicted, P | P | N (20.11) | arms at each end | verdict |
|---|---|---|---|---|---|---|
| (vii) | treatment prompt arrived | 3/3 | **3/3** | 0/3, as built | q100–q102 True · q97–q99 False | **the round is valid** |
| (vi) | certificate | 0 · 0 · own `CLAUDE.md` | **9/9** | 9/9 | one record each, inside the arm | **clean on both sides** |
| (i) | teeth, M1 | 3/3 RED | **2/3 RED** | 0/2 + 1 n/a | q100 q101 RED · q102 GREEN | **missed the prediction, above the Pivot line** |
| (v) | teeth, M2 | agrees with (i) | **2/3, agrees per arm** | 0/2 + 1 n/a | same arms | **as (i)** |
| (ii) | test cases over the seeded four | 3/3 | **2/3** | 0/3 | q100 q101 +1 · q102 at four | **reversed, by its own clause** |
| (iii) | delivery | 3/3 | **3/3** | 2/3 server-side (q98 localStorage) | all three tally, route, markup | as predicted |
| (iv) | cost, weighted | recorded | 170 k · 164 k · 165 k | 42 k · 35 k · 46 k | — | **~4× — recorded, under-powered** |

## Verdict: the protocol's effect on tests survives clean controls, smaller than 20.3 measured

**On controls certified to hold no protocol text, Sonnet with the protocol left a test with teeth
in 2 of 3 arms; Sonnet without it left none.** That is the comparison 20.3 made, with the
contamination footnote removed, and the direction holds. Nothing is pooled with 20.3 or 20.8:
their controls were not clean.

**It is not 20.3's 3/3.** One arm in three ran the full ceremony, delivered, and wrote no test.
The prediction said 3/3 and was wrong on (i) and on (ii); the Pivot line was 2/3 and was not
crossed. At N=3 the difference between 3/3 and 2/3 is one arm, and this round cannot say whether
the launcher or chance moved it. **It does say the effect is not an artifact of the injection.**

**The mechanism held again, and it is the most useful thing in the round.** q100 and q101 put a
*test* step in their plan and wrote a test; q102's plan validates with `npm test` and a curl, and
wrote none. **The plan predicts the artifact in 12 of 12 arms** across 20.8, 20.11 and 20.12. The
protocol does not make an agent write a test; it makes the agent write down whether it will, and
then it does what it wrote.

**Cost: four times the tokens for the protocol side**, the same ratio 20.11 showed. That buys the
ceremony files, a test in two arms, and — the verifier's finding — a Step 0 UPGRADE run under the
prompt's standing approval on q100 and q101.

## What this does not say

1. **The comparison is the whole package against a bare tree**: protocol files, seeded docs,
   `CLAUDE.md`, the treatment sentence and the standing-approval clause, plus committed versus
   untracked `node_modules`. 20.3's design, inherited and now named. Which part produces the test
   is not separable here; 20.11's silent-prompt arms (0/3) say the sentence matters.
2. **One fixture, one task, N=3 a side.** A null on q98's server-side teeth (no server tally) makes
   the control side 0/2, not 0/3.
3. **Not "Sonnet is good with the protocol."** One measured behaviour — a test that catches two
   specific tally mutations — on a ten-file app.
4. **Both sides wrote outside their trees** (q101, and 20.11's q97 q99 used `/tmp`), against the
   prompt. Not scored; q101's leftovers read and removed.

## Who verified
An independent agent holding the artifacts and the criteria only, not this round's author.

## Cost of the round
Three Sonnet arms, 499 k weighted tokens; VERIFY one agent.
