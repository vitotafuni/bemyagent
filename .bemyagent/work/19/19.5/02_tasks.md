**Delivers:** the treatment half that Milestone 19 has owed since 19.2a — does the content-branch
clause convert a stop at an empty gate into delivered work, and does it cost anything.

## Design

Six arms, Sonnet pinned, three batches of two, one arm per condition per batch.

| side | arms | protocol |
|---|---|---|
| **A control** | q73 q75 q77 | shipped `BEMYAGENT.md` |
| **B treatment** | q74 q76 q78 | + the Step 0 content-branch clause |

Seed on both sides: `harness/fixture` with `.bemyagent/` holding **only** `settings.json` —
20.5's W, byte for byte, built from the same script.

Prompt: `prompt.txt`, 20.5's W prompt verbatim. **No standing approval.** The STOP is the
mechanism under test, so granting approval in the prompt would delete the occasion — the error
20.5 made by merging two claims onto one condition.

## Metrics and the readings, fixed before launch

### Primary — ROUTING, per arm

Read from the tree, never from the hand-back. **STOPPED** = `upgrade-plan.md` left on disk and
**0 source files changed** under `client server db test`. **PROCEEDED** = source files changed.

- **A stops 3/3 and B proceeds 3/3** → clean separation. **The clause lands**: it removes a gate
  that guards nothing and recovers the whole delivery.
- **Both stop 3/3** → the clause does not fire. Null, and the clause is deleted as a candidate.
- **Both proceed 3/3** → ceiling. The control no longer stops, this fixture cannot test the
  clause, and 20.5's W reading is the one that needs re-examining.
- **Any split** → null at N=3. Nothing lands.

### Harm — SETTINGS PRESERVATION, per key

**Eight** keys in the seeded `settings.json`, three arms, **24 observations a side**. A key whose
value changed or vanished is a loss. The clause claims the merge is additive.

**Any loss on B that A does not also show rejects the clause**, whatever the routing says.

### Context, recorded and not verdict-bearing
Delivery (`git diff --stat` over `client server db test`), tests, whether an upgrade log was
written, and what each arm wrote about the branch in its own words.

## CDM — Heavy

**🎯 Drift** — scoring delivery as the verdict instead of routing.
**✅ Validation** — as fixed in `01_think.md`.
**🔄 Pivot** — a session limit voids the round; rebuild, never resume.

## Checklist

- [x] verified — sweep ports
- [x] verified — build six arms, verify the delta is the clause line only
- [x] verified — store the prompt verbatim before launching
- [x] verified — three batches of two, Sonnet pinned on every arm
- [x] verified — score routing and settings preservation, raw output here before the verdict
- [x] verified — 19.4 check: open the arm at each end of every metric and name it
- [x] verified — sweep ports after, write `04_verify.md`, then `05` and the plan
