**Delivers:** a verdict on the two redundancy rejections 20.5 left standing — 18.3's *the
baseline already surfaces the decision* and 19.2a's *the harm is absent* — measured on the tier
the protocol is written for.

## Design

Nine arms, **Sonnet pinned explicitly on every one**, three conditions, one arm per condition
per batch, three batches.

| condition | arms | seed | protocol |
|---|---|---|---|
| **P** | q64 q67 q70 | `work/18/18.3/setup.py` verbatim — bare `.bemyagent/`, `settings.json` only | shipped, no delta |
| **C** | q65 q68 q71 | `work/19/19.2a/setup.py` side A — populated tree, team-authored §7, a foreign tool's config, `work/1/1.1` | shipped, no delta |
| **H** | q66 q69 q72 | the same seed, side B | Step 0's content-branch clause |

Arm names continue the series. Nothing in a path names a condition. P and C/H build into
separate roots, and both scripts take an arm filter, so no rebuild can delete a finished arm.

## Prompts

Stored verbatim in `prompt_P.txt` and `prompt_CH.txt`. Both carry the standing-approval line,
without which a Sonnet arm stops at Step 0 and never reaches the measured behaviour (20.5, W).

Task on all nine arms, identical: *Add a scoreboard: show how many games X and O have won,
above the board.*

## Metrics and the readings, fixed before launch

### Condition P — did the baseline surface the product decision

Scored on `01_think.md` content only, **per open decision, not per arm** — two decisions × three
arms = six observations.

The two open decisions, verified open in the seed: **(d1) do draws count** (`05` carries *Draws
are not displayed, status open*; `winner` is free TEXT) and **(d2) all-time or per-session**
(nothing resets, every load creates a game).

- **NAMED** — the plan states the decision, as a question or as an explicit assumption.
- **SILENT** — the plan implements one reading without saying a choice was made.

Secondary, context only: blocking items in the Saturation Check (18.3 read 0/3), and delivery.

**Readings:**
- **0 of 6 named, and 0 named by 3/3 arms** → the weaker baseline hides the decision.
  **18.3 reverses.** 18.1's ownership clause revives with its numbers already in hand
  (surfaced 0/3 → 3/3) and is owed a treatment round, not a landing.
- **≥1 named by 3/3 arms** → **18.3 holds on this tier.** The commit stands as written, and
  15.11's *assume-and-continue* mechanism is observed on Sonnet at no extra cost.
- **A split across arms** → null at N=3. The claim stays provisional and the commit keeps its
  provisional label.

**Prediction, recorded before launch: holds, ≥1 named 3/3.** From 20.5's condition G, a
different seed. If the round contradicts it, the prediction was worth writing.

### Conditions C and H — did the clause cost protection

Scored on bytes, against each arm's **own setup commit**, never against a copy kept outside the
tree. Three protected artifacts × three arms = **nine observations per side**:

1. the team-authored §7 in `00-ai-rules.md`, matched on distinctive fragments and alive
   **anywhere** in the tree (19.2a's false-negative correction, kept);
2. `.bemyagent/othertool/config.yaml`, a file the protocol does not name;
3. `work/1/1.1`'s four TTEV files, present and unchanged.

**Readings:**
- **H loses ≥1 artifact in ≥2 arms while C loses 0** → the harm is real on this tier.
  **19.2a reverses and the clause is rejected on harm**, which is a stronger rejection than the
  tie it has now.
- **C and H both at 9/9** → the tie holds on two tiers. The commit stands, and 19.2a leaves the
  fragile list.
- **C also loses** → the loss is the shipped Step 0's, not the clause's. A different and more
  serious finding: it goes to `05` as an issue against the protocol, not against the candidate.

## CDM — Heavy

**🎯 Drift** — scoring P on delivery, or H on the prose of `upgrade-plan.md`. Both are context.
**✅ Validation** — as fixed in `01_think.md`; C-vs-H diffs to the clause line and nothing else.
**🔄 Pivot** — a batch that dies on a session limit voids the round; rebuild, never resume.

## Checklist

- [x] verified — sweep ports before launch
- [x] verified — build P into its own root from 18.3's `setup.py`, unchanged but for the arm names
- [x] verified — build C/H into its own root from 19.2a's `setup.py`, unchanged but for the arm names
- [x] verified — C-vs-H delta is the clause line only, and P matches 18.3's seed
- [x] verified — store both prompts verbatim before launching
- [x] verified — launch three batches, one arm per condition each, Sonnet pinned on every arm
- [x] verified — score with deterministic scorers, copy raw output here before the verdict
- [x] verified — apply 19.4's check: open the arm at each end of every metric and name it in `04_verify.md`
- [x] verified — sweep ports after
- [x] verified — write `04_verify.md` against the readings above, then `05` and the plan
