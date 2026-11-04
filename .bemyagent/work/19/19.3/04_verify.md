# VERIFY — 19.3, do gates land at all in this repo

Zero arms spent. Every figure comes from `score.py` over transcripts and trees already paid for.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| The discarded probes and their false result are logged before the clean numbers | PASS | `03_execute.log`, two instruments discarded |
| Scorer and raw output copied here | PASS | `score.py`, `03c_gate_evidence.txt` |
| Occasion count spot-checked against one arm's real diff | PASS | q32, five files, exact match |
| Emissions separated from the string being read | PASS | `in tool results` column, **0** for all six |

## The question splits, and the record has to keep saying so

**The consent half is still untested and this round does not change that.** Step 0's STOP and
`interactiveMode`'s stops exit on a human reply, and `harness/README.md` rules those out: a
subagent treats a coordinator's message as non-authoritative by construction, so every arm looks
compliant for a reason unrelated to the rule. 15.11 already paid for that. Anyone citing this
round for *gates work* is citing the wrong half.

**The forced-output half is measurable, and this is the first time it has been measured.**

## The result

| | emissions | governed files changed | named in an emission |
|---|---|---|---|
| q28 | 6 | 4 | 4 |
| q29 | 3 | 5 | 2 |
| q30 | 7 | 3 | 3 |
| q31 | 3 | 12 | 3 |
| q32 | 2 | 5 | 2 |
| q33 | 4 | 4 | 4 |
| **total** | **25** | **33** | **18 — 55%** |

**6 of 6 arms ran the gate, and ran it properly.** Not boilerplate: the emissions carry real
reasons that cite the rule doing the work — *"Routing Table sends a new feature to specs/ and no
spec file exists yet"*, *"rules §6 requires the code map updated in the same response as the code
change"*, *"existing file is the index, so updated not created"*. That last one is step 3 of the
gate, the part that asks whether an existing file fits, visibly firing.

**55% of governed writes were named.** The gate fires on what the agent plans to write and misses
what it touches on the way: `01-overview.md` edited in passing for a glossary line, and the nine
template and `.bak` files Step 0's UPGRADE path rewrote in q31, which is most of the gap on its
own. Arms that stayed on the planned path scored 4/4, 3/3 and 4/4.

## Verdict: the gate lands, and Decision 13's estimate was never checkable as worded

`05` justifies Decision 13 with *"declarative rules rejected (estimated ~50-60% compliance),
procedural gates with forced output estimated at ~90%"*. Ten milestones of preferring procedural
rules over declarative ones rest partly on that number, and this is the first look at it.

It does not resolve to one figure, because the sentence never said what it counted:

- **Does the agent run the gate at all: 6/6, 100%.** Comfortably above the estimate.
- **Is every governed write gated: 18/33, 55%.** At the bottom of the range the same sentence
  assigns to *declarative* rules.

Both are true of the same six arms. The estimate was not wrong, it was unmeasurable, and the
lesson belongs with the clause-writing findings from 14.8 and 14.9: **a compliance claim has to
name its denominator or it cannot be checked, and an unchecked number still steers ten
milestones of decisions.**

What this licenses for 19.2: a forced-output gate is a real mechanism here and may be designed
on. It will fire where the agent is already heading and not where it wanders, so a gate meant to
catch an incidental write is not this shape.

## Caveats

1. **Six arms, one task, one fixture.** The wider transcript pool in this session was not used:
   mapping transcripts of earlier rounds to their trees is not recoverable here, and emissions
   without a denominator are the exact uncheckable number this round is about.
2. **Occasions under-count repeat edits.** One file edited four times counts once. The rate is
   per governed *file*, stated, not per write.
3. **Naming is matched by filename appearing in an emission.** An arm could name a file and write
   a different one; nothing here detects that. Reads of the six emission lists give no sign of it.
4. **The retired reading is retired, not answered.** Whether the gate fires *before* the write
   is undecidable from this data, because the arms edit through inline Python heredocs and no
   pattern can say which file a shell command writes.
5. **The exemption is taken at face value.** §3 exempts the task's own `01`–`04`; three arms
   emitted a check for those anyway and said they were exempt. Counted as neither occasion nor
   miss.
