# VERIFY — 15.10 EARS-formatted Validation criteria

Verdict: **INCONCLUSIVE, not null.** The treatment applied cleanly, but both pre-registered
measures were already saturated in the baseline, so the round could not have detected an effect
if one existed. By this project's own distinction (13.2), that means **change nothing** — do not
land EARS, and do not reject it.

## The result

| | a (baseline) | b (treatment) | |
|---|---|---|---|
| **FORM** — criteria written `WHEN … SHALL …` | **0/3** | **3/3** | clean, but see below |
| **CITATION** — `04_verify.md` names a command actually run | 3/3 | 3/3 | **ceiling** |
| **COVERAGE** — that command touches the change | 3/3 | 3/3 | **ceiling** |

**FORM is not the result.** `02_tasks.md`'s CDM names counting it as success as Drift: the form
is template-forced the moment the clause exists. It confirms the treatment applied — nothing
more.

**Both real measures hit the ceiling.** Every arm cited `npm test` with literal output, and every
arm added its own test file (`online.test.js` ×4, `presence.test.js`, `api.test.js`), so every
cited command covered the change. The baseline was already at 100% on both bars. There was no
room for EARS to move anything.

The pre-mortem predicted exactly this and the pivot was pre-registered: *"If COVERAGE is 3/3 in
both: ceiling effect from a task that naturally produces its own test. The coverage question is
unanswered, not answered — record it as inconclusive, which is not a null, and do not prune §4
on it."* It fired as written.

## The design fault, and it is mine

The task was chosen *because* the shipped suite covers only `rules.js`, so citing `npm test`
without covering the change was possible. Every arm added a test anyway — which is good practice
and defeats the design. **I selected for an opportunity to fail that competent agents do not
take.** A ceiling in the baseline is not a finding about the rule; it is a finding about the
task.

## Two observations, explicitly NOT results

Both are visible only because the scorer prints matched lines instead of booleans — the rule
adopted after a regex in an earlier round mistook `new Map` for deduplication.

**1. The treatment binds criterion to evidence; the baseline reports an aggregate.** b-arms
discharge criteria one by one — b-1 writes *"- WHEN same playerId posts twice THE SYSTEM SHALL
list once: npm test -> 'a created session shows the player online once'"*, and b-2/b-3 say
*"criterion covered by …"*. a-arms report *"npm test -> 7 pass 0 fail"* and then describe what
the tests happen to do. The direction of the binding differs: criterion → evidence versus
evidence → description. **Not measured, not claimed** — it would need its own pre-registered
measure.

**2. One baseline arm wrote a criterion that asserts nothing.** a-2's entire Validation criterion
is *"npm test passes incl. new tests."* That is circular: it states that the tests pass, not what
must be true of the system. a-1 and a-3 did name behaviour. **1/3 is noise at N=3** by our own
threshold, so this is a demonstration of the mechanism, not a measurement of its rate — but it is
the mechanism EARS exists to prevent, and `WHEN … SHALL …` makes that sentence impossible to
write.

## What a valid round would measure

Not citation and not coverage — §4 already delivers both at ceiling. The question EARS can
actually answer is **criterion quality**: does the Validation criterion state an observable
behaviour, or is it circular about the test run? a-2 is the failure mode, and it is scorable
(*"does the criterion mention system behaviour independent of the test suite?"*). That needs a
task where circular criteria are tempting — plausibly a refactor, where "the tests still pass" is
the natural thing to write and names nothing.

## Caveats

1. **One model, one harness** — the external-validity limit named on 2026-10-20 and carried in
   `01_think.md`. Replication on a second model family is queued separately.
2. **N=3 per condition**, one task.
3. This round cost 6 arms plus the 4 burned by round 1's void: **10 arms, ~480k tokens, for an
   inconclusive**. Recorded because the harness's cost should be visible when deciding the next
   round.

## Recommendation

**Change nothing.** EARS is neither landed nor rejected. Re-run against criterion quality on a
task where the baseline can plausibly fail, or drop the candidate — but do not spend lines on it
and do not cite this round as evidence either way.
