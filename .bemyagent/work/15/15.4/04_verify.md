# VERIFY — 15.4, the gate leaves no trace

Raw output `03d_score_output.json`, scorer `score.py`, table `03c_arm_evidence.txt`.

## 19.4's check — the arms at each end of every metric, named

| Metric | Read | Result |
|---|---|---|
| (i) trace on disk | **q47** (most, 5 lines) and **q50** (none, control) | matches: q47's lines are in its `03_execute.log`, q50's tree holds none |
| (ii) coverage | **q46** (best, 10/14) and **q48** (worst, 6/12) | **did not match — the metric was wrong.** See below |
| (iii) batching | **q51** (all four lines outside `03_execute.log`) and **q47** (split 2 before, 3 after) | matches |
| (iv) delivery | **q49** (10 tests) and **q47** (4 tests) | matches: both green, neither degraded |
| (v) reasons | all six read in full | matches: no side restates the rule instead of the decision |

**The check earned its keep on its first round.** Opening q46 and q48 showed that the files
counted as ungated were almost all `*.bak-20261105` — backups Step 0's APPLY writes as a side
effect of its own overwrite rule, not documents an agent decides to create. Excluding them:
**A 89%, B 85%**, where the first run printed 65% and 63%.

## The result

| | q46 A | q48 A | q50 A | q47 B | q49 B | q51 B |
|---|---|---|---|---|---|---|
| lines on disk | 0 | 0 | 0 | 5 | 5 | 4 |
| coverage, conversation | 10/10 | 6/9 | 9/9 | 9/9 | 6/9 | 9/10 |
| delivery | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**(i) B 3/3, A 0/3.** **(ii) 89% against 85% — flat.** **(iv) no cost.**

## Verdict: the trace lands, the clause does not — the file it names does not exist when half the gated writes happen

The obligation works at what it was written for. 3/3 arms left the gate's line in the repository,
and the control left none, so issue #5 is real and the remedy's mechanism is reachable.

It does not ship, and the reason is a drafting defect in my own clause, found by the round rather
than by review:

**`03_execute.log` does not exist when Step 0 runs.** Half the governed writes in every arm
happen during the upgrade, before any task folder exists, so the clause names a destination that
is not there yet. Three arms resolved it three ways: q47 ignored the Step 0 writes, q49 split
between the task log and the upgrade log, **q51 put all four lines in the upgrade log and nothing
in `03_execute.log` at all**. The half I specified was met and the half I never wrote down was
invented three times — 14.8's finding, on a different clause, for the second time.

**And the record under-reports the gate that ran.** B's disk lines name 13 of 28 governed files
while B's conversation names 24 of 28. An auditor reading the repository would conclude the gate
fired half as often as it did. A record that systematically understates compliance is worse than
no record for the one use it has, which is letting someone who was not there check.

**(iii) is the second reason.** Three of q47's five lines and one of q49's four sit after the
entries describing the writes they gate. At perfect coverage that is still a transcript, not a
gate, and the gate's own claim is *"proceed only after step 2"*.

## What a next candidate would have to do, if there is one

Name a destination that exists at every point the gate fires. The upgrade log for Step 0 writes
and `03_execute.log` for task writes is what two arms invented unprompted, which is evidence for
that shape rather than for mine. It is **not scheduled**: 15.4 answers the question it was filed
for — the trace is obtainable and costs no delivery — and the next version is a rewording whose
value rests on the same flat coverage this round measured.

## Caveats

1. **A published figure is corrected by this round.** 19.3's Write Gate coverage of 18/33 = 55%
   becomes **18/30 = 60%** once protocol-generated `.bak` files leave the denominator. Amended in
   `05`, not left standing.
2. **Control-rate instability, third occurrence.** 19.3's six arms gave 60% on the shipped
   protocol; 15.4's three control arms give 89%. Same protocol, a day apart. This is what
   `harness/README.md` now calls an under-powered reading, and it means neither number is *the*
   coverage of the Write Gate.
3. **Batch 2 died on a session limit**, was voided and rebuilt rather than resumed, with the
   rebuilt arms confirmed byte-identical to the never-launched arms of their own side. Batch 1
   was complete before the limit and was not rebuilt.
4. **One confound, 1 of 6, on the treatment side.** q49 installed the §1 directive block into
   `CLAUDE.md`. Its coverage is 6/9, the joint lowest, so it did not inflate what it could have.
5. **The disk and transcript instruments are not interchangeable**, which is why the comparison
   is transcript-to-transcript. Stated in `01_think.md` before launch.
