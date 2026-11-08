# THINK — 20.3, Sonnet with the protocol against Opus without it

## Context

### Context Saturation Check
- [x] Target files/paths — `work/20/20.3/`, both seeds and both prompts from `work/20/20.2/`
      unchanged, its `mutate.py` and `score.py` reused as instruments
- [x] Expected behaviour — six arms, three **S** (Sonnet + shipped protocol, 20.2's P tree) and
      three **O** (Opus, no protocol at all, 20.2's N tree), three batches of one per condition
- [x] Constraints — the model is **part of the condition** here, so each arm's tier is pinned
      explicitly and the pin is the variable, not an oversight
- [x] Dependencies — none new
0 unknown → proceed.

## The question, which is the user's and not mine

20.2 measured the protocol against its absence **on one tier** and found it does not win and
costs 2.54×. The user's reply was arithmetic: if a tier that costs an order of magnitude less
can match the expensive tier by using the protocol, then a 2.54× token overhead is bought back
many times over. **Break-even is at t = r**, token ratio against price ratio. The measured
overhead is 2.54; the tier price ratio is far larger. So **cost stopped being the open variable
and capability became it.**

This round asks whether the cheap tier with the protocol reaches the expensive tier without it,
on the same task, in the same batches, scored by the same instruments.

## Approaches Considered

- **A. Six arms, three a side, same batches** (chosen). 20.2's design with one axis changed.
- **B. Add a third condition, Opus+BMA, to separate tier from protocol.** Rejected on price for
  now: that is 20.2's P arms, already measured, and re-running them would be the most expensive
  arms in the round for a comparison the record already holds. Stated as a limit, not hidden.
- **C. Score it on the protocol's own artifacts.** Rejected for 20.2's reason: `03_execute.log`
  exists on one side by definition, so anything only one condition can produce is not a metric.

## Selected Approach & Risks

### 🎯 Drift
Declaring a winner on delivery alone. Both sides are expected to deliver; 20.2's six arms all
did. The round is decided on **(i) whether the arm's own tests have teeth** and **(ii) defects
surfaced**, with cost as the thing those two are weighed against.

### ✅ Validation
S trees identical to 20.2's P seed and O trees to its N seed, both by `diff -r` against a 20.2
arm; O trees confirmed to hold no `BEMYAGENT.md`, no `.bemyagent/`, no `CLAUDE.md`; both prompts
stored; the tier pin recorded per arm; scorer output here before the verdict; 19.4's check
performed and the arms named.

### 🔄 Pivot
If the Opus arms refuse or ask for a spec, the round measures the prompt. Rebuild, do not score.

### Pre-mortem
1. **The protocol under test is not the one 20.2 tested.** 19.5 changed `BEMYAGENT.md` today.
   The change is Step 0's branch for a `.bemyagent/` holding nothing but `settings.json`, and
   the S seed is a **fully populated** tree, so the clause cannot fire. Immaterial here, and
   said out loud rather than assumed.
2. **Inherited instruments carry inherited tables.** `mutate.py`'s per-arm SQL and `score.py`'s
   agent ids were written for 20.2's arms. Copying the files under new arm names carried them
   across, where they would have applied one arm's mutation to another arm's code and scored
   the wrong transcripts — reporting `n/a` for arms whose tests were never exercised. **Both
   tables are blanked and are filled only after the arms run.** Caught before launch; recorded
   because the next person to reuse a scorer will hit it too.
3. **Three arms a side decides nothing subtle.** Only clean separation counts, as always.
4. **Price.** Three Opus arms are the expensive half: 20.2's N arms ran 97–112 k raw. Budget
   ≈ 160 k Sonnet + ≈ 320 k Opus.

### Devil's Advocate
*A cheap-tier win here would be the result this project wants, which is the reason to distrust
it.* The guard is that the two verdict metrics are the ones 20.2 used to conclude **against**
the protocol, unchanged, and that the losing reading is written down first: if O leads on
anything, `04_verify.md` says so before it says anything else.

## Verification Plan
20.2's instruments, output copied here before the verdict, readings fixed in `02_tasks.md`.
