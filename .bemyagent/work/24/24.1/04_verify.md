# 24.1 — VERIFY

**Who verified:** three Sonnet agents that did not write the candidate — one for the mechanical criterion, one built and launched the pilot, one built, launched and scored the round. Sonnet because each job is commands and their output. The author read the reports and wrote this file; the author ran no arm.

Candidate: `bma/24.1`. The pilot and criterion (a) ran at 8af9320; the text was then revised once (a malformed number is `unknown`; the downgrade question named as one) and the round ran at eb427b1, where the round's agent re-checked the two copies of the rules (`cmp` silent) and the diff against `main` (2 files, 8 insertions, 3 deletions).

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| a | copies of the rules equal; against `main` only the title and Step 0 › UPGRADE differ | PASS | `cmp` silent; `git diff --numstat`: rules 1/1, `BEMYAGENT.md` title + UPGRADE lines |
| b | *older*: nothing written, both numbers, a downgrade | PASS | haiku 3 of 3, sonnet 2 of 2: `git status` shows only the handed file; no plan |
| b′ | *numeric* (`3.10.0` installed, `3.6.0` handed): same as (b), not fooled by a comparison as text | PASS | haiku 3 of 3, sonnet 2 of 2 |
| c | *same and equal*: nothing written, *nothing to upgrade* | PASS | haiku 3 of 3, sonnet 2 of 2; every final message names the byte comparison |
| d | *same number, rules edited by hand*: not declared up to date | PASS | haiku 3 of 3, sonnet 2 of 2: a plan written, the rules file untouched, the added line found and a place proposed for it before any overwrite; all waited |
| e | *newer* / *unstamped*: plan with `Upgrade: <from> → <to>`, stop for review, nothing overwritten | PASS | `Upgrade: 3.5.0 → 3.6.0` in 5 of 5; `Upgrade: unknown (before 3.6.0) → 3.6.0` in 5 of 5; rules file unchanged in 10 of 10 |
| f | control — the released file on a project it generated | recorded | 2 of 2 (and the pilot's 1): a full plan whose items say *no change needed*, and a stop for review. The double upgrade costs a plan and a human review for nothing |

`round/` holds the scripts as run (`build.sh`, `launch.sh`, `runall.sh`, `score.py`) and the scorer's output (`score.tsv`; `score.txt` with every arm's final message). 32 arms, all exit 0, no permission denied, no relaunch; 2.48 USD. The pilot (4 arms, 0.69 USD) is in `03_execute.log` [2].

## Cost of the two stops, against today
*older* / *same*: 3–6 turns, about 0.009 USD (haiku) and 0.15 USD (sonnet), nothing for the person to review. Control: 7–9 turns, 0.018 / 0.20 USD, and a 28-line plan to read and approve.

## What this does not show
- Three and two runs per cell: counts, not rates. One seed project, one harness (Claude Code), two models of one family.
- The seed for *older*, *numeric*, *same*, *edited* carries the candidate's rules, so the arm's tool had loaded rules that already bear a number; a real project reaches that state only after `3.6.0` is out.
- The scorer checked the plan's first line and what changed on disk — **not whether the rest of each plan is right**. Whether a number in view changes how ASSESS is run (THINK, the unanswered question) is only answered as far as: a plan was still written in 15 of 15 arms that had to write one.
- *edited*: the scorer's `nothing to upgrade` column is a text rule and fired on three haiku arms for the words *already on 3.6.0* inside a message that goes on to a plan; the verdict above is from the files (a plan exists, rules untouched), and the messages are in `round/score.txt`.
- Nobody answered a stopped arm: what happens after the user says *yes, downgrade* was not run.
- A malformed number (`v3.6`, `3.6.0-rc1`) — covered by the revised sentence, never seeded.
- Noted by the mechanical verifier, outside this task and true of the released file too: in the cases that go on, a pending `upgrade-plan.md` would be overwritten by the new plan.

## Verdict
**PASS** for a–e at eb427b1, with the limits above to be carried wherever the feature is described. Not landed: step 5 is on the user's word, and the release waits for 24.2 (the number and the tag kept equal).
