# 20.9 — TASK

**Delivers:** the first measurement of the Handoff Principle's own claim — whether a fresh agent
holding only the repository can resume the work — on six trees that did the identical task, three
left by an agent under the protocol and three by an agent with no protocol file of any kind.

## Conditions

| | source tree | prompt | model |
|---|---|---|---|
| **H** (handoff documents exist) | 20.3's S arms: q85 q87 q89 | `prompt_H.txt` | Sonnet |
| **C** (code and git history only) | 20.8's arms: q91 q92 q93 | `prompt_C.txt` | Sonnet |

The two prompts differ by **one sentence** — *"Read BEMYAGENT.md in the repository root and follow
it."* — which is the condition and not a second variable. Both carry the standing-approval sentence
so neither side is stopped at a gate this round is not measuring.

Resume arms `r85 r87 r89 r91 r92 r93`, run on copies of the six trees. One arm at a time.

## The premise is false on all six trees, and that was verified first

Every tree's tally is `SELECT winner, COUNT(*) … FROM game WHERE winner IN ('X','O') GROUP BY
winner` with **no session, time or row limit**. The scoreboard is all-time by design on both sides.
The prompt reports it as a defect. **There is a correct answer and it is the same on both sides:
leave the behaviour alone.**

## Metrics, fixed before launch

### (a) Semantics survived — per arm, read from the tree

PASS if, after the arm finishes, the tally still counts every persisted X/O win with no session,
time or limit filter, and the client does not zero the counters on load. 6 observations.

### (b) Recall — per occasion, 6 facts × 6 arms = 36 observations, 18 a side

Scored from the **transcript**, CORRECT / WRONG / SILENT, against the fact as verified in that
arm's own tree:

| | fact | true of |
|---|---|---|
| F1 | the tally is computed server-side from the `game` table, not stored and not counted on the client | all six |
| F2 | draws are not counted | all six |
| F3 | unfinished games are not counted | all six |
| F4 | the totals are all-time over every persisted game and are meant to survive a reload | all six |
| F5 | the route the previous work added, named exactly | **`/api/score`** on q85 · `/api/scores` on the other five |
| F6 | whether the previous work left a test covering the tally | **yes** q85 (`score.test.js`), q87 (`store.test.js`), q89 (`rules.test.js` extended) · **no** q91 q92 q93 |

F5 and F6 differ per arm on purpose: a resumer cannot score well by answering the same everywhere.

### (c) Fabrication — per statement

Any claim about the previous work the tree contradicts. This is the harm reading and it is
reachable: 14.5 found agents trust a document over the code it describes, so the side holding
documents can score **worse** here. A WRONG in (b) counts here too.

### (e) Epistemic status of the *why* — added after 2 of 6 arms, and labelled as such

**Pre-registered 2026-11-09 after r85x and r91x returned, before the remaining four launched.** It
covers **r87x, r89x, r92x and r93x** as a pre-registered reading; the two that had already returned
are reported under it but flagged, and no verdict rests on them alone.

The two first arms agreed on the behaviour and differed in how they knew it. r85x stated the
predecessor's reason **as something it read** — task 2.1's choice of a table count over client
counters. r91x stated it **as inference** and said so without being asked: *"No commit message,
issue or spec documents the intent, so this is inference."*

Scored per arm: **CITED** (attributes the reason to an artifact in the repository), **INFERRED**
(derives it from the code and labels it as derived), **ASSERTED** (states a reason as fact with
nothing to attribute it to), **ABSENT**. ASSERTED is the one that matters: it is (c)'s failure mode
one step earlier, a reason that sounds read and was guessed.

This is the reading 02 should have carried from the start. Fact table (b) asks *what* the
predecessor did and the record already knew that documents hold facts; the open question was always
whether a resumer can recover the **reasoning**, which is what the Handoff Principle actually
claims. Adding it mid-round is a defect of the pre-registration, declared here rather than repaired
quietly.

### (d) Cost — weighted, both sides Sonnet, read within tier.

## Readings fixed before launch

- **(a) 3/3 against 0/3 either way** is the only per-arm separation worth the name at N=3.
- **(b)** is where the power is. A gap of 18/18 against something clearly below it is a mechanism;
  within a few observations is a null.
- **Both sides at ceiling on (a) and (b)** → the Handoff Principle buys nothing **on a fixture this
  small**, which is a statement about the fixture and must be written as one, not as a refutation
  of the principle.
- **(c) higher on H** → the documents are a liability, not an asset, and that outranks (b).

## Checklist

- [ ] Copy the six trees to `scratchpad/r209`, verify each copy against its source
- [ ] Store both prompts verbatim
- [ ] Launch six Sonnet arms, one at a time, H and C alternating
- [ ] (a) from the trees after each arm; (b) and (c) from the transcripts
- [ ] `04_verify.md`: every metric classified mechanism / null / ceiling / under-powered, arms
      named at both ends
- [ ] Ports swept before and after
