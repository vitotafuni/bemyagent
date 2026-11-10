# 20.12 — THINK

## Context

20.11 certified the first clean controls this project has run: q97 q98 q99, launched by
`command claude -p` from inside their own trees, carry no instruction record, no parent path and
no OVERRIDE header. It compared nothing, because its protocol side was sent the control's prompt
(`20.11/prompt.txt` is byte-identical to `20.3/prompt_N.txt`). The comparison 20.11 was built
for is still owed: **the protocol condition as 20.3 ran it, on the launcher that produced clean
controls, against those controls.**

This round runs only the missing side. Three P arms, 20.3's `prompt_P.txt` verbatim, the
20.11 launcher unchanged except its output directory and prompt file. The N side is not rerun:
it already exists on the same seed, the same launcher and the same model id, certified, and was
scored the same day.

### Context Saturation Check
- [x] **Target files/paths** — `work/20/20.12/`; trees in `scratchpad/r2012/q100 q101 q102`;
      seed from 20.11's `setup.py` with `ARMS` narrowed to three P arms; instruments are 20.11's,
      with the new arms added and nothing else.
- [x] **Expected behavior** — P arms run the ceremony, deliver the scoreboard, and leave a test
      that turns RED under M1 and M2. That is 20.3's published reading for this condition.
- [x] **Constraints** — Sonnet, served model id read from the launcher's own `modelUsage`. The
      prompt is copied from `20.3/prompt_P.txt` and `cmp`'d against it before launch — the check
      20.11 never ran.
- [x] **Dependencies** — same CLI, `command claude`, `CLAUDE_CONFIG_DIR` pinned; the launch needs
      the user's permission prompt (20.11's precedent, granted 2026-11-10: *"se devi fare altri
      test prima di dichiarare che tutto è completo procedi"*).

## Approaches Considered

1. **Rerun both sides, six arms.** Simultaneity is the only thing it buys, and nothing on this
   launcher varies by hour that the record can name; the served model id is read per arm. It
   costs another ~123 k for a control already certified. Rejected.
2. **Three P arms against the existing clean controls.** Chosen. One variable relative to 20.11's
   P arms (the prompt), one relative to 20.3's P arms (the launcher).
3. **Agent-tool P arms instead.** That is 20.3 itself; it already exists. Rejected.

## Selected Approach & Risks

### Pre-mortem
1. **The wrong prompt again.** Mitigated by a byte-compare against `20.3/prompt_P.txt` as a
   checklist step before launch, and by reading the first user message out of each transcript
   after it.
2. **The launcher, not the protocol, floors the P side** — `-p` mode, no Agent tool. If P reads
   below 2/3 on (i), the round cannot tell launcher from protocol, and says so: the Agent-tool
   arms of 20.3 ran the same prompt and the same seed, so the only difference is the launcher.
3. **A regex scorer misses the query**, as it did on three of 20.11's arms. Mitigated by 20.11's
   procedure: hand-derived mutation, restored in `finally`, `git status` before and after.

### Devil's Advocate
*The comparison is already settled by 20.10: the contamination was inert, the controls wrote 0
TTEV files.* True of the control's ceremony, not of its tests: 20.10 measured TTEV files and
`PROTOCOL_CHECK`s, never whether a contaminated control writes fewer or more tests. A clean
reproduction of 5/6 against 0/9 is the only thing that removes the footnote from 20.3 and 20.8.
Kept.

## Verification Plan
The readings in `02_tasks.md`, each read from a command, both ends named; independent VERIFY by
an agent holding the artifacts and the criteria only.
