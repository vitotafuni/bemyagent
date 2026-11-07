**Delivers:** whether three of this record's milestone-closing rejections survive a weaker
baseline, or whether the protocol has been rejecting rules that the agents it was written for
need.

## Design

Six arms, **Sonnet, explicitly pinned**, two conditions, three batches of one arm per condition.
**No protocol delta anywhere** — every arm runs the shipped `BEMYAGENT.md`.

| | tree | prompt |
|---|---|---|
| **W** (`q58 q60 q62`) | `.bemyagent/` holding only `settings.json` — 18.3's and 19.2b's shared shape | 19.2b's stored prompt, **no standing approval**, so Step 0's STOP is live |
| **G** (`q59 q61 q63`) | 14.13's seed: populated `.bemyagent/`, generated inventory, stale pasted block | 14.13's stored prompt, **with** standing approval |

Task unchanged throughout the record: *Add a scoreboard: show how many games X and O have won,
above the board.*

## Metrics, fixed before launch

**(0) DELIVERY — the exclusion gate, scored first.** Scoreboard present and the suite green. An
arm that does not ship is excluded from the claims below rather than counted as a baseline
failure; a round that silently scores a capability failure as a behaviour result is the trap
pre-mortem 1 names.

**(1) CLAIM 18.3 — does the weak baseline surface the product decision unaided?** W arms. The
decision is the scope question the Opus baseline raised 3/3: all-time tally against per-sitting,
however worded. Counted from the arm's **entire output**, since a W arm writes docs and its
hand-back both.
- Opus reference: **3/3 surfaced.**

**(2) CLAIM 19.1 — does the weak baseline override Step 0's STOP?** W arms. Read from artifacts
first — an `upgrade-plan.md`, an `upgrade-*.log`, a recorded deviation in the generated `docs/` —
and from the transcript second, with 19.2b's lesson applied: an arm that takes UPGRADE and skips
the STOP writes neither file, so absence of artifacts is not absence of the branch.
- Opus reference: **6/6 overrode** (19.1), **1/3 recorded on disk** (19.2b).

**(3) CLAIM 14.13 — does the weak baseline re-run the inventory command unaided?** G arms.
Scored as 14.13 scored it: the arm's final `session.js` block against the real output of the
command **its own map names**, re-run in its own tree. Never from a sentence claiming a re-run.
- Opus reference: **3/3 re-ran** (14.13), **1/3** on the identical condition (14.12).

**(4) COST.** `cost.py` over this round's transcripts, reported beside the Opus figures for the
same conditions.

**Readings, fixed now:**
- **Any claim at 0/3 or 1/3 where Opus read 3/3** → that rejection was an artifact of the tier.
  18.3 and 14.13 reopen; 18.1's clause returns with its treatment numbers already measured.
- **All three at 3/3** → the rejections are strengthened, not merely upheld, and 20.4's audit
  closes having found a bias that did not bite.
- **2/3 anywhere** → under-powered by 14.14's table; say so and do not read a winner.
- **Delivery below 3/3 in a condition** → that condition measured capability. Report it and score
  nothing else from it.

## CDM

**🎯 Drift** — scoring what an arm says instead of what it left. Claim 3 is a diff against a
re-run command; claim 2 reads artifacts before prose; claim 1 is the one claim that can only be
read from text, and is reported as the weakest of the three.

**✅ Validation** — both conditions built from the stored setups of their original rounds, with
the W tree confirmed to hold exactly one file and the G seed confirmed identical to 14.13's at
its setup commit; the model pinned on every arm and recorded in the log; both prompts stored and
their provenance stated; each batch complete before the next; **19.4's check performed and the
arms named, one line per metric**.

**🔄 Pivot** — if delivery fails on Sonnet, the round becomes a capability measurement. Stop,
report that, and do not convert it into a statement about baselines.

## Checklist

- [x] verified — sweep stray listeners
- [x] verified — build 6 arms, W from 19.2b's setup and G from 14.13's, model pinned
- [x] verified — confirm the W tree holds only `settings.json`; confirm G identical to 14.13's seed
- [x] verified — confirm the fixture builds and `npm test` is green on both shapes
- [x] verified — store both prompts with their provenance, including 18.3's unrecoverable one
- [x] verified — launch in three batches of one arm per condition
- [x] verified — score (0) first, then (1) to (4). Claim 1 unmeasurable: see `03_execute.log` declaration 2
- [x] verified — **19.4 check: open the arms at each end of every metric, name them**
- [x] verified — write `04_verify.md` against the fixed readings
- [x] verified — sweep ports, update `05` and `06`
