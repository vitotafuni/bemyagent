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

---

## Amendment, 2026-11-06, after the user read the verdict

Three objections from the user. Two are design faults in this round, and the verdict is narrowed
accordingly rather than defended.

### 1. The protocol's primary audience is the human, and this round measured only the machine

*"il protocollo serve anche a garantire all'uomo di poter interagire con la macchina senza perdere
il controllo e capire cosa viene fatto. quindi tutta la documentazione viene prodotta più per
l'uomo che per la macchina."*

Correct, and it is not a footnote. Every metric here — mutation survival, defects surfaced,
delivery, tokens — is machine-observable by construction, because `harness/README.md` rules out
measuring anything that needs a human in the loop, the same limit that stopped 15.11 and 19.3.
So **the protocol's main claimed value was not tested and is not denied by this round.** The
verdict applies to machine-observable value only, and the headline is amended to say so.

One mechanical shadow of the human claim **is** measurable and was not measured: whether a fresh
agent holding only the repository can resume the work. That is the Handoff Principle's own claim,
and it is the honest proxy for *a human can see what was done*.

### 2. The round never gave the protocol's main mechanism an occasion to fire

*"bma prevede di pulire spesso il contesto e ripartire solo dal minimo comune denominatore di
contesto mentre su una serie di task eseguiti tutti dallo stesso agente forse perdiamo colpi."*

This is the strongest objection and it is a methodological fault by this harness's own rules.
TTEV, Session Restore and the `01`–`04` files exist **for context resets**. Every arm here ran
**one task in one unbroken context**, where restoring from documents buys nothing because nothing
was lost. The N arms were never asked to resume anything, so they never paid the price the
protocol exists to avoid.

That is the same failure as 15.9a and 14.1: a rule measured where its occasion is absent. By the
rule I applied to 15.9 two days ago, **this round should not have been read as a verdict on the
protocol, only on the protocol in a single-shot task.**

The design it implies, stated and not scheduled: a *series* of tasks on one fixture with the
context cleared between them, P restoring from `.bemyagent/` and N restoring from whatever it can
reconstruct.

### 3. The tier is part of the question, not a cost detail

*"tutte le pratiche inserite per forzare un modello 'povero' … se le valutiamo da un punto di
vista di puro consumo sono a sfavore di bma … ma sappiamo benissimo che sonnet costa 10 volte di
meno di opus alto."*

Also right, and it cuts two ways. Devil's Advocate, the anti-drift CDM and the ceremony sizing
are scaffolding for weaker reasoning, so **measuring them on the strongest available model is the
condition least likely to show their benefit** — the mirror image of the flattering-condition
choice made in `01_think.md`, and in the opposite direction.

And the economics change the comparison entirely: a protocol overhead of 2.54× on a tier that
costs roughly a tenth is not 2.54× worse, it is several times cheaper than the same work without
the protocol on the expensive tier. **20.2 compared P and N on one tier and therefore priced the
protocol in the one way that cannot answer the question the user is asking.** 20.1 already
recorded that BMA ships to everyone and has only ever been measured on the most expensive tier.

### The verdict, narrowed

**On a single-shot, four-file feature, in a small clean codebase, with the scaffold pre-installed,
on the most expensive model, and measured only on machine-observable outcomes, the protocol does
not beat its absence and costs 2.54×.**

Every clause in that sentence is a condition this round chose, and three of them are conditions
under which the protocol could not win. What was measured stands; what it was read to mean does
not.
