# VERIFY — 20.2, does the shipped protocol beat no protocol

Raw output `03d_score_output.json`, scorers `mutate.py` and `score.py`, table
`03c_arm_evidence.txt`.

## 19.4's check — the arms at each end of every metric, named

| Metric | Read | Result |
|---|---|---|
| (i) mutation | **q52** (RED, 2 fail) and **q54** (GREEN, protocol, no test file) | matches, and q54 is the finding: it complied with §4 exactly |
| (i) GREEN with tests | **q57** (3 tests, still GREEN) | matches: none of its cases creates a draw |
| (ii) defects | **q52** (4) and **q55 / q57** (0) | **did not match — the metric was biased toward P.** See below |
| (iii) delivery | all six | matches, no difference |
| (iv) cost | **q52** (1.08 M) and **q57** (0.26 M) | matches |

**The check changed the verdict, twice.** Opening q52 and the zero-scoring N arms showed that two
of the six pre-registered defects are stated verbatim in documents only P arms have — the
`session.js` ⚠️ line in the seeded code map, and the stale issue in the seeded `05`. Counting them
measures what P was **told**, not what P **noticed**. On the four defects observable from the code
alone, P reads 2, 1, 1 and N reads 1, 0, 0: **the ranges overlap and the separation is gone.**

## The result

| | q52 P | q54 P | q56 P | q53 N | q55 N | q57 N |
|---|---|---|---|---|---|---|
| (i) mutation caught | **RED** | GREEN | **RED** | GREEN | GREEN | GREEN |
| (ii) unseeded defects | 2 | 1 | 1 | 1 | 0 | 0 |
| (iii) scoreboard delivered | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| (iv) weighted tokens | 1.08 M | 0.64 M | 0.85 M | 0.43 M | 0.32 M | 0.26 M |

## Verdict: no. The protocol does not beat no protocol on this task, and costs 2.54× to tie

Against the readings fixed before launch:

- **(i) P 2/3 against N 0/3** — below the bar of 3/3 against 0/3. Suggestive, not a mechanism.
- **(ii) no clean separation** once the seeded defects are removed, which is the only honest
  subset.
- **(iii) a tie**, 6/6 both sides.
- **(iv) P costs 2.54×.**

The pre-registered reading for this combination was written before the arms ran: *"a tie on (i)
and (ii) with P costing more on (iv) → the protocol is ceremony on this task, reported exactly
that plainly."* It is not a full tie — (i) leans P — so the accurate statement is narrower and
worse for the protocol than a tie would have been to read: **the protocol's one visible effect
is below this harness's own bar, and it is bought at two and a half times the tokens.**

Three things make that verdict heavier rather than lighter:

1. **The condition was chosen to flatter the protocol**, in `01_think.md` before launch. P
   started from an installed, committed `.bemyagent/` with its setup cost already sunk. The
   bootstrap framing would cost P more, not less.
2. **The only property that separated at all is not one the protocol asks for.** §4 with
   `strictVerification: false` requests a light check and never requests a regression test. q54
   complied exactly and went GREEN. So even the 2/3 is an effect the protocol produced without
   specifying — harness rule 1's unevidenced mechanism, on the protocol's own behalf.
3. **The N arms were not careless.** q53 played five games through the live API and cross-checked
   against the rows; q55 drove four outcomes; q57 wrote three tests against the real Express app.
   What the protocol changed, where it changed anything, is whether the check **stays in the
   repository**, not whether it was done.

## What this does not say

It does not say BMA is worthless. It says that **on a four-file feature in a small, already-clean
codebase, with the scaffold already installed, it does not pay for itself in anything this round
could measure.** Every rule in `BEMYAGENT.md` was landed by a round measuring that rule against
the rest of the protocol; none of those rounds is invalidated by this one. What is now on the
record is that the sum has never beaten its absence here, and that it costs 2.54×.

The obvious next question — whether the picture changes on a task large enough to exceed one
context window, which is where decomposition and handoff are supposed to earn their keep — is
exactly the fixture `harness/README.md` says this repo has (`fixture/` was built so that a
feature cutting every layer exceeds a context window). **That round is not scheduled and must
not be scheduled by me**: it is the obvious move after an uncomfortable result, which is the
pattern the user stopped two days ago.

## Caveats

1. **One task, one fixture, N=3.** The task is small and the codebase is clean, which is the
   condition least favourable to a protocol about managing complexity.
2. **The metric was corrected mid-verdict** and the correction moved against the protocol. Stated
   in `03_execute.log` with both figures, raw and corrected.
3. **`reload starts a new game` is partly P-favouring too** and was kept: the behaviour is
   code-observable and an N arm did find it, but the *contradiction* framing needs
   `01-overview.md`, which only P has. Keeping it is the conservative choice — removing it would
   take N to 0/12 and widen the gap.
4. **Cost is weighted, not priced.** Ratios, not money; re-check before quoting.
