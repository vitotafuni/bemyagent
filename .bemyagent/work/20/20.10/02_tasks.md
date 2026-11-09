# TASK — 20.10

**Delivers:** the record states, per round, how much of the shipped protocol each arm actually
had in context — measured from the arms' own tool calls rather than assumed from the directory
the harness built.

## What was already seen before this file was written

This round is forensics on data that was already on disk, and the exploration came first. The
declaration matters more here than the pre-registration, so it is made in full:

- **Already seen:** the per-round count of arms whose tool calls name the parent rules file
  (`14.13` 6/6, `15.4` 6/6, `19.2a` 5/6, `19.2b` 6/6, `20.2` 6/6, `20.3` 3/6, `20.8` 1/3,
  `20.9` 3/6, `14.15` 0/6, `19.5` 0/6, `20.5` 0/6, `20.7` 0/9); that the twelve no-protocol
  controls produced no TTEV artifact; and that one arm, `q39`, reached the parent `BEMYAGENT.md`.
- **Not yet looked at, pre-registered here:** F4, F5 and F6 below.

14.15's precedent is the reason this paragraph exists: a metric invented after the data is worth
less than one fixed before it, and the only honest repair is to say which is which.

## Fact table, fixed before the scorer runs

| # | Fact | Status |
|---|---|---|
| F1 | Every arm launch in every round is attributed to a round, or printed as a hole | retro |
| F2 | A parent read is counted only from a `tool_use` input containing the parent absolute path | retro |
| F3 | None of the twelve no-protocol controls wrote `01_think.md`, `02_tasks.md`, `03_execute.log`, `04_verify.md` or emitted `PROTOCOL_CHECK` | retro |
| F4 | **Order**: in the rounds that mutate the rules mirror, the parent read lands before the arm's own copy is read | **pre-registered, unseen** |
| F5 | **VERIFY agents**: the independent §4 verifiers of 14.13, 15.4 and 20.2 also reached the parent repository | **pre-registered, unseen** |
| F6 | **Record leak**: no agent read the parent's `05-decisions-and-issues.md` or `06-implementation-plan.md` — this project's own results | **pre-registered, unseen** |

F4, F5 and F6 are predictions. F6 is the one worth being wrong about: an arm that read this
project's decisions file read the conclusions of the rounds it was itself an observation in.

## Checklist

- [ ] `score.py` — one pass over all 201 transcripts, attribution from the directory prefix
- [ ] `03b_census.txt` — per round, per arm, the raw census
- [ ] `03c_direction.txt` — per round, what its setup mutates and which way the defect pushes
- [ ] `03d_score_output.json` — raw scorer output, copied before the verdict
- [ ] F4, F5, F6 measured and recorded whichever way they come out
- [ ] `04_verify.md` — every criterion with evidence from a command run during VERIFY
- [ ] Independent VERIFY by an agent that did not do the work (§4: the author checking their own
      work is the weakest available check)
- [ ] The two committed sentences this round contradicts, struck in place with the correction
      dated beside them — `work/20/20.9/04_verify.md` and `harness/README.md`
- [ ] `harness/README.md` — the doctrine item, and the section rewritten on measurement
- [ ] `05-decisions-and-issues.md`, `06-implementation-plan.md`

## CDM criteria

See `01_think.md`. In short: attribution complete with holes printed; the read counted from a
tool call; the direction of effect per round stated before its count; the controls checked for
ceremony; every corrected claim quoted as committed before it is struck.
