# 21.3 — VERIFY (independent)

**Verdict: PASS_WITH_CAVEATS** — 51 data lines: **41 supported, 10 partly, 0 unsupported**. No line invents a rejection and every reference resolves; seven cells contradict or outrun their own cited source and one dropped plan row has no line. The fixes are listed with exact text; none needs a new source.

**Who ran this:** model `claude-fable-5-2`, an agent that did not write the register, the spec or the sweep. I formed every finding below from `docs/decisions/rejected.md`, the criteria and the sources; `03_execute.log` and `03b_crosscheck_sonnet.md` were opened only afterwards (last section). No project file was edited, nothing committed; this file is the only write.

**Evidence rule:** every figure comes from a command run during this VERIFY (2026-11-12). `05` = `docs/05-decisions-and-issues.md` (531 lines), `06` = `docs/06-implementation-plan.md` (268 lines), `LA` = `drafts/landscape-analysis.md`. Both `05` and `06` and all eight drafts were read whole, not sampled. Line numbers `L7`–`L57` are file lines of `rejected.md`.

## Criteria

| Criterion | Result | Evidence |
|---|---|---|
| CDM: every line cites a `file:line` that exists | PASS | parse script over the table: 53 table lines, 51 data lines, 6 cells each, **0** unresolved or empty references |
| CDM: … and says what the line claims | PASS_WITH_CAVEATS | all 51 lines opened. `05:126` (Decision 18, the 2026-08 survey) is cited on L11, L40, L56 and does not mention the idea on L11 or L40; verdict kind outruns the source on L20, L27, L45 |
| CDM: `not stated` wherever the source is silent | **2 of 37 fail** | L31: the cited line `05:223` itself names the untested case. L11: `LA:333` defers the idea *"until (3) has a result"* — the sentence L56 uses as its reopening condition |
| CDM: the `activeContext.md` line reads `reopened → specs/resume-block.md` | PASS | L7 Status = `reopened → specs/resume-block.md (Milestone 21.1)`; `specs/resume-block.md:19` *"rejection withdrawn"*; `05:517` |
| CDM: file ≤ 60 table lines | PASS | `grep -c '^\|'` → 53 (header, separator, 51 data); `wc -l` → 57 |
| Spec 1: register exists, backfilled, traceable, nothing invented where the source is silent | PASS_WITH_CAVEATS | as above, plus one omission (14.5) |
| Spec 2: an independent reader confirms a sample | PASS | exceeded: all 51 lines, not a sample — 41 / 10 / 0 |
| Spec 3, 4, 5 (recall round, rule text, drafts reconciled) | not in scope | other tasks; not judged |

## Per-line table

S = supported, P = partly. A note on an S line is a recommendation, not a defect.

| L | Idea (short) | | Defect or note |
|---|---|---|---|
| 7 | `activeContext.md` pointer | S | — |
| 8 | per-turn conversation log by rule | S | note: a harness-written `conversationLog` contract landed instead (`06:194`, `05:228`); Status could say so |
| 9 | resume state outside the session | S | note: no source line says 15.7 is reopened; the link to `resume-block.md` is the register's inference from its own reopening condition (a trigger candidate now exists). The *"and commit"* half of #9 (`06:177`) is not registered |
| 10 | DB-backed memory | S | — |
| 11 | self-amending Project Learnings | **P** | Reopens `not stated` is wrong (`LA:333`); `05:126` does not mention the idea (`grep -n 'self-amending\|Project Learnings' 05 06` → nothing); rests on a gitignored draft only |
| 12 | empty `## Project rules` section | S | note: 3/3 vs 3/3 is a ceiling by `05:309`; the source's own word is *null* (`05:245`), so the kind follows the source |
| 13 | implicit standing rules | S | note: round never run; the Rests-on cell says so |
| 14 | timestamps from `date` | S | note: source says *parked, not landed* (`LA:57`) |
| 15 | issue-tracker integration | S | — |
| 16 | exit code forces verdict | S | — |
| 17 | loop until exit 0 | S | — |
| 18 | one aggregate exit code | S | — |
| 19 | `[RUNTIME_CHECK]` per criterion | S | — |
| 20 | EARS-form criteria | **P** | `under-powered` is not the source's verdict: `05:242` and `06:181` say INCONCLUSIVE at a ceiling, *"reject nothing"*. *"gave the baseline no way to fail"* is `06:181` verbatim (not cited) and `05:242` says the opposite — the opening existed, no arm took it |
| 21 | command + output pasted in `04_verify` | S | — |
| 22 | `PROTOCOL_CHECK` to `03_execute.log` | S | — |
| 23 | second-agent VERIFY as a gate | S | — |
| 24 | VERIFY re-runs derived block | S | — |
| 25 | generated structural layer | S | — |
| 26 | `comm -13` cross-check | S | rests on the 0-of-6 trace; recall 2/3 vs 2/3 alone would be under-powered |
| 27 | Graphify / code-graph tool | **P** | source status is *"not adopted, not rejected"* (`drafts/graphify-evaluation.md:5`); value was never measured, so `under-powered` is wrong; `2026-10-10` is the day it was suggested; Reopens repeats the framing `06:161` (cited) withdraws — *"not blocked on a larger fixture"* |
| 28 | delegate large reads | S | — |
| 29 | "do not ask permission" | **P** (minor) | `05:119` records a *preamble contradiction* fix discarded; it does not say the fix was to drop the sentence |
| 30 | late-description routing rule | S | same ceiling note as L12 |
| 31 | markdown-only folder = GREENFIELD | **P** | Reopens `not stated`; `05:223` ends *"Still untested, and possibly the reporter's actual case: a folder containing only BMA's own bootstrap files"* |
| 32 | doc-only exception to code-map limit | S | — |
| 33 | UPGRADE branches on content | S | — |
| 34 | merge local lines before overwrite | S | — |
| 35 | version field | S | — |
| 36 | declarative rule instead of gate | S | — |
| 37 | "split vertically" rule | S | — |
| 38 | `Layers:` header | S | — |
| 39 | RFC 2119 + `because` | S | — |
| 40 | Troubleshooting sections / commit-intent tiering | **P** | `05:126` does not mention either (`grep -n 'Troubleshooting\|commit-intent\|Strands\|agent-sop' 05 06` → nothing); two ideas on one line; draft only |
| 41 | Intent Alignment Gate | S | — |
| 42 | Dormancy mode | S | — |
| 43 | fact/decision split | S | — |
| 44 | mattpocock skills | S | — |
| 45 | prune declarative rules once classified | **P** | `under-powered` asserts a measurement; 13.1b was *"zero agents plus one verifier"*, *"nothing is cut on inspection"* (`06:131`, `05:507`) |
| 46 | delete Handoff Principle | S | — |
| 47 | measure inert rules (13.2b) | S | — |
| 48 | `BEMYAGENT.min.md` | S | — |
| 49 | approval gate surfaces decisions | S | note: `05:408` files 15.11 among *baseline already does this* |
| 50 | product decision trips STOP | S | — |
| 51 | only hard-to-undo decisions trip STOP | S | — |
| 52 | ship a hook or script | **P** (minor) | `(no date given)` while the cited `05:250` is dated 2026-10-29 |
| 53 | keep running clause rounds | **P** (minor) | *"on the current fixture"* is not in `05:377`; its reason is that candidates came from the rounds' own output. Status `stands` is right (`06:237` *"remain paused"*) |
| 54 | tag every push | S | — |
| 55 | push more rarely | S | — |
| 56 | Spec-Kit / OpenSpec / GSD | **P** (minor) | `05:126` covers Spec-Kit only; OpenSpec was *"absent from"* that survey (`LA:281`); draft only |
| 57 | Kiro spec triple | S | note: the triple itself was not measured (`06:184`); the line records a survey verdict |

## Must-fix, with the proposed cell text

1. **L31, Reopens when** → `The untested case: a folder holding only BMA's own bootstrap files`
2. **L11, Reopens when** → `Deferred until the three-rule A/B has a result`; **Evidence** → `drafts/landscape-analysis.md:274, drafts/landscape-analysis.md:333`
3. **L27, Verdict** → `2026-11-10 design`; **Rests on** → `Invocation measured 3/3, value never measured: 6/6 reached equal outcomes; value round 14.7 dropped unrun`; **Reopens when** → `Reopens only with a second fixture (14.7 was gated by 14.5)`; **Evidence** → `drafts/graphify-evaluation.md:5, 05:214, 06:161, 06:153, 05:505`
4. **L45, Verdict** → `2026-11-10 design`
5. **L20, Verdict** → `inconclusive at ceiling, not adopted (no date given)`; **Rests on** → `Inconclusive, nothing rejected: citation and coverage 3/3 vs 3/3 at ceiling; no arm took the opening to fail`; **Evidence** → `05:242, 05:244, 06:181`
6. **L40, Evidence** → `drafts/landscape-analysis.md:146, drafts/landscape-analysis.md:147`
7. **L52, Verdict** → `2026-10-29 design`

Minor, same shape: **L29 Idea** → `**Step0** Fix the "do not ask permission" preamble contradiction to cure the greenfield stop`; **L53 Idea** → `**Process** Keep running candidate-clause rounds fed by earlier rounds' findings`; **L56 Evidence** → drop `05:126` or keep it knowing it covers Spec-Kit alone.

## Inclusion errors

- **Draft-only verdicts: L11, L40, L56.** Their only supporting lines are in `LA`, whose header reads *"Everything else here is analysis, not decision"*, and whose 2026-10-20 addenda are recorded nowhere in `05` or `06`. The spec does count verdicts inside drafts, so they may stay — but `05:126` is not the decision behind them and should not be cited as if it were. The user's call.
- **Not rejected by the source: L20** (*"reject nothing"*) and **L27** (*"not adopted, not rejected"*). Both are honest "evaluated, not built" lines once the Verdict cell stops saying otherwise.
- **Adopted later without Status saying so:** none found. L30 and L33 say `reversed`; L8's contract is a different form (note above).
- **Two lines, one idea:** none that must merge. L45 and L47 are both "prune rules" but differ in method and verdict; L11 and L13 sit next to each other and a reader will meet both.
- **Same shape, three labels:** rounds dropped unrun carry `redundancy` (L9), `design` (L13) and `under-powered` (L27, L47). The kind vocabulary has no word for *never measured*, and the register's header does not define the five kinds at all.

## Omissions

- **Real: 14.5 — a §5 rule against trusting a comment over the code it describes** (`06:153`, `05:208`). Of the nine dropped rows in `06` it is the only one with neither a line nor a mention (`grep -ci 'comment\|14\.5' rejected.md` → 0), and the spec names *"dropped plan rows with a reopening condition (`05`:505)"* as register material. L9 and L13 are the same shape and were included. Proposed line: `| **Verify** Add a §5 rule: do not trust a comment over the code it describes | 2026-11-10 design | Never run, no candidate fix written; finding stands: 7/9 read the comment, 9/9 shipped the violation | Reopens only with a second fixture, where comments and code disagree at scale | 06:153, 05:208 | stands |`
- **Borderline, the user's call:** the first-draft convergence gate, *"tick what is met"*, measured harmful 3/3 (`05:128`) — a reworded form landed, so only the wording was rejected, like L37/L38; *"declare your own status vocabulary"* (`05:172`); *"and commit"* as part of the resume rule (`06:177`); the redundancy audit's two other refused deletions (`05:146`, `05:147`), siblings of L46.
- **Correctly left out:** backlog items never evaluated (`06:267`, `06:268`), the self-compression directive (`05:89`, pending), the struck-through Opus condition (`05:470`), the state review's *"ruled out"* list (nothing decided, `06:20` contradicts one item).

## Usability read (judgement, not measurement)

Five re-proposals in other words, read against the Idea column only:

| Paraphrase | Lands on | |
|---|---|---|
| "Keep a tiny *where we are now* note the agent refreshes as we go" | L7, with L9 beside it | yes |
| "Let the test runner's result decide whether a task passed" | L16 | yes |
| "Whenever I correct the agent, have it write that down as a new rule" | L11 and L13 | yes, two lines with different verdicts |
| "Ship a short second copy of the protocol for small models" | L48 | yes |
| "The agent should double-check docstrings against the code before relying on them" | nothing | **no** — the 14.5 omission |

Four of five land. The theme words help more than the wording: the lines that would be missed are those named by their implementation (L26 `comm -13`, L47 `(13.2b)`, L21). Whether an agent finds them is spec criterion 3 and is not measured here.

## What the earlier files claimed that this check contradicts

- `03_execute.log:32` rules that the three landscape-only lines stay because *"Decision 18 (05:126) is the project decision that closed that survey"*. `05:126` names six projects surveyed in 2026-08; the three ideas come from the 2026-10-20 addenda about projects that survey did not include (`LA:70` *"The survey above missed a near-peer"*, `LA:281`). It holds for Spec-Kit alone.
- `03_execute.log:30` leaves 14.5 out because *"no fix was ever proposed or evaluated"*. The same is true of L9 and L13, which were registered. The Sonnet cross-check (`03b`, D8) also asked for the line.
- `03b` D1 found the *"until (3) has a result"* defect on a line since removed; the same sentence applies to L11, which it did not sample.
- Nothing else: the log's counts (51 data lines, 37 `not stated`, kinds 26 / 10 / 6 / 5 / 4, statuses 47 / 2 / 2) match mine.

## What could not be checked

- `drafts/` is gitignored (`git check-ignore` → `.gitignore:2`): the 13 lines that cite a draft are verifiable on this machine only.
- Figures were checked against `05`, `06` and the drafts, not against the round folders under `work/`.
- Undated verdicts (20 lines say `no date given`) were not dated from git history, except 15.10 (first commit 2026-10-26).
- Recall by an agent (spec criterion 3) is not measured; the usability table is one reader's judgement.
