# THINK — 14.15, the derived-blocks clause as a treatment

## Context

### Context Saturation Check
- [x] Target files/paths — `work/14/14.15/`, seed and clause reused verbatim from
      `work/20/20.5/setup_G.py`, which already carries 14.13's `treat()`; prompt from
      `work/20/20.5/prompt_G.txt`
- [x] Expected behaviour — six Sonnet arms, three control three treatment, the clause applied to
      **both** `BEMYAGENT.md` and `00-ai-rules.md` on side B, as 14.13 applied it
- [x] Constraints — one arm per side per batch; model pinned; own root; arm filter
- [x] Dependencies — none new
0 unknown → proceed.

## Why now

14.13 closed this line at a **ceiling**: the Opus control re-ran the inventory command unaided
3/3, so the clause had nothing to buy. 20.5 reversed that — the Sonnet control re-runs it **0/3**
while shipping a working feature, which is the drift the clause exists to catch. The clause has
never run as a treatment on a baseline that needs it.

## Approaches Considered

- **A. Both sides, six arms** (chosen), for the reason 19.5 chose it: 20.5's G control is a day
  old and 14.12/14.13 had byte-identical controls read 1/3 and 3/3 a week apart.
- **B. Treatment only, three arms.** Rejected on the same precedent.

## Selected Approach & Risks

### 🎯 Drift
Scoring the arm's **sentence** about re-running instead of the block's bytes. 14.13's own scorer
failed a neighbouring version of this by defining a forged line against the *seeded* command
rather than the one the arm's map names. The scorer here re-runs **the command the arm's own map
names**, in the arm's own tree.

### ✅ Validation
A vs B diffs to the clause line in both protocol files and nothing else; A vs A and B vs B
identical; 6/6 arms leave a readable map; ports swept both ends; scorer output here before the
verdict; 19.4's check applied and the arms named.

### 🔄 Pivot
A session limit voids the round. Rebuild, never resume.

### Pre-mortem
1. **The control may re-run this time**, making the round a ceiling as 14.13 was. Written into
   the readings rather than treated as failure.
2. **The clause may buy forgery instead of freshness.** 14.12 caught an arm hand-typing nine
   lines into a block that claims to be command output. A clause that *requires* the block to
   match is an incentive to make it match by typing. **Forged lines are counted per line**, and
   any forgery on B that A does not show rejects the clause whatever the freshness says.
3. **Per-occasion power.** Freshness is scored **per file in the inventory**, eight files × three
   arms = **24 observations a side**, not one verdict per arm.
4. **Price.** Six Sonnet arms, ≈ 330 k at 20.7's rate for this seed.

### Devil's Advocate
*This round is built to make the clause look good: it seeds a stale block and then rewards
noticing it.* True, and that is what a benefit round is. The defence is pre-mortem 2: the harm
metric reads the same bytes and can reject the clause on its own, and the control's own rate is
measured in the same batches rather than quoted from last week.

## Verification Plan
Deterministic scorer, output here before the verdict, readings fixed in `02_tasks.md`.
