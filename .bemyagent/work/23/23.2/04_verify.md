# 23.2 — VERIFY (criteria a–d; e is the round, not run)

**Who verified:** two Sonnet agents that did not write the candidate, holding the files and the criteria — one for a–c, one built and launched the pilot (d). Sonnet because both jobs are mechanical: commands and their output. The author (the session that wrote the text) read the reports and ran three read-only commands on the pilot's tree afterwards, marked *author* below.

Candidate: `bma/23.2` at 403a556. `<out>` is the pilot's scratch folder (volatile).

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| a | embedded rules = standalone rules on the branch; differ from `main` in the log paragraph only | PASS | rules are lines 29–136 of `BEMYAGENT.md`; `cmp` against `.bemyagent/docs/00-ai-rules.md` silent, 14555 bytes each; `git diff main..bma/23.2 -- .bemyagent/docs/00-ai-rules.md` → one hunk, the paragraph. Not checked: main's own two copies against each other |
| b | worked example = verified script, comments aside | PASS | block at lines 320–361, de-indented 3 spaces; comment lines removed on both sides → `diff` empty, 37 lines each |
| c | the script as extracted from the file passes 23.1's checks | PASS | `sh -n` clean; three events of one session → one file `2026-11/21-1833-abcdef12.md`, three headings; `$(touch …)`, backticks, quotes, `\n %s` literal, no file created; non-JSON, empty stdin, missing argument → exit 1; two entries of ~210 kB at once, 8 runs → both whole, byte-compared, no lock left; two sessions → two files |
| d | pilot: after bootstrap with consent the hook and script exist, and a second headless turn lands in the log | PASS | below |

## The pilot (d)
Tree: `harness/fixture` + the candidate `BEMYAGENT.md`, one commit, no `.claude/`, no `.bemyagent/`. Launcher: `claude -p`, `--model sonnet` (resolved to `claude-sonnet-5-5`), tools `Read,Write,Edit,Bash,Glob,Grep`, no permission bypass. Prompts: `pilot-prompt-1.txt`, `pilot-prompt-2.txt` in this folder, verbatim.
- Turn 1: exit 0, 49 s, 8 turns, `permission_denials: []`, 0.24 USD. On disk afterwards: `.bemyagent/hooks/claude-code/conversation-log.sh` (executable, `diff` against the block in the candidate file empty), `.claude/settings.local.json` with the three hooks (no shared `settings.json`), `.gitignore` with `.bemyagent/log/`, `settings.json` with `"conversationLog": ".bemyagent/log"`. **An arm can write its tool's settings in headless, and the tool loads them within the same session**: the log already holds turn 1's final message (`· agent`), not its prompt — the hook did not exist when the prompt arrived.
- Turn 2, a new session: exit 0, 4 s. A second file, `2026-11/21-1834-<session>.md`, holds the prompt under `· user` and `PILOT-TWO-OK-7391` under `· agent`.
- *author*: the rules file the arm generated is byte-equal to the embedded copy.

## What the pilot did not show, and what it found
1. **One arm, one model, one run.** It says the design can produce its occasion; it is not a rate. Nothing about a small model.
2. **The asking was not exercised**: consent was in the prompt, so *show, then switch on only on a yes* was never put to the test — the arm reported what it had done after doing it. As foreseen in THINK; only the no-consent arm of a round measures the other end.
3. **"Personal, not committed" held by luck of the machine** (*author*: `git check-ignore -v .claude/settings.local.json` → matched by the machine's global git ignore, not by anything in the tree). The tool adds that ignore itself when *it* creates the file; an agent writing the file by hand on another machine leaves it untracked and committable. The candidate's text does not say to check. **Gap in the candidate.**
4. The script writes a fourth voice, `harness` (a subagent's report arriving as a prompt), that neither the rules paragraph nor the contract names (the mechanical verifier).
5. A line of a message that begins with `## ` reads as a heading in the log; entries are told apart only by `## <timestamp> ·`. Known since 23.1, stated.
6. The arm said it ran the script once on a sample event; no such entry is in the log folder and nobody checked where it went. It left `BEMYAGENT.md` in place and told the user to delete it — the file's own last step, outside this task.

## Verdict
**PASS_WITH_CAVEATS** for a–d. Points 3 and 4 are changes to the candidate's text and go to the user before anything else; a changed text means b–d are re-run on the new commit. Criterion (e) — the round — is not run and is the user's call.

## Second pass — candidate at bfafd25 (2026-11-21, on the user's word: *redo the tests to be sure*)
The text changed in two places after the first pass (point 3: the personal settings file is checked as ignored by git; point 4: the contract names the `harness` voice), so a–d were run again on the new commit by two fresh Sonnet agents, neither the author nor the agents of the first pass.

| # | Verdict | Evidence |
|---|---|---|
| a | PASS | lines 29–136 `cmp` silent against the rules file; one hunk against `main`, the paragraph; this time main's own two copies checked equal too |
| b | PASS | block at 320–363; comment lines removed → `diff` empty, 37 lines each |
| c | PASS | as the first pass, 8 of 8 parallel runs whole (400,073 bytes, each body matched once); `<task-notification>` and `<agent-message from=…>` → `· harness` |
| d | PASS | below |

Pilot, second run. Same tree and launcher; **the arm's repository had `core.excludesFile` set to `/dev/null`**, and `git check-ignore` on a personal settings file was shown to return 1 before the launch — the machine's global ignore could not help. Prompt 1 identical to the first run's (`cmp`); prompt 2 in `pilot-prompt-2b.txt`.
- Turn 1: exit 0, 46 s, 7 turns, no denial, 0.24 USD, `claude-sonnet-5-5`. Script written, byte-equal to the block; three hooks in `.claude/settings.local.json`; **the arm's `.gitignore` holds `.claude/settings.local.json` and `.bemyagent/log/`**, and `git check-ignore -v` names that file's line 1 as the rule; `git status` lists nothing under `.claude/`. Rules file byte-equal to the embedded copy.
- Turn 2, new session: its own file, the prompt under `· user`, `PILOT-TWO-OK-5820` under `· agent`.
Point 3 of the first pass is closed by the new sentence, in one arm.

### What the second mechanical pass found, contract against script
1. A session that crosses the end of a month gets a second file: the script looks for the session's file in the current month's folder only, while the contract says *found again by the id at every later one*. Read from the code, not run. **A defect of the script against its own contract** — small, real.
2. The brief's heading also carries ` — <description>`; the contract shows `brief → <agent>` only.
3. `harness` is given to two tags only; any other block the harness sends as a prompt is labelled `user`.
4. The id is stripped of non-alphanumerics before its first 8 characters are taken (same thing for the ids seen so far); no id → `nosessio`; trailing newlines of a text are dropped; an already tracked settings file is not protected by an ignore rule.
2–4 are the example doing a little more or less than the contract says; the contract is the requirement, the example one way to meet it. Left as they are unless the user says otherwise.

### Still not shown
One arm per pass, a mid model, consent in the prompt: no rate, nothing about a small model, the asking never exercised. The hook on the agent tool was never fired in an arm (no arm launched a subagent) — seen working only in 23.1, in this project.

## Verdict (both passes)
**PASS_WITH_CAVEATS** for a–d at bfafd25. Open for the user: finding 1 above (fix the script — then it is no longer the script 23.1 verified, and b–c run again), and whether to spend a round (e).

## Third pass and the round — candidate at 4efabba (2026-11-21)
One line of the script changed after the second pass (finding 1 there: the session's file is now searched in the whole log folder), in the candidate and in the copy in use on this machine alike. A third Sonnet agent, fresh, re-ran a–c; a fourth built, launched and scored the round.

| # | Verdict | Evidence |
|---|---|---|
| a | PASS | `cmp` silent, 14555 bytes; against `main` one paragraph; main's own copies equal |
| b | PASS | comment-only lines removed → `diff` empty, 37 lines each; the three trailing comments compared too, identical |
| c | PASS | the five checks as before (8 of 8 parallel runs whole); **the changed line**: a session whose file sits in `2026-10/` is appended there, old content intact, no file in the current month; ids made of `*`, `?`, `..`, `/` → exit 1, nothing written; `../../x`, `a b`, `[a]` → stripped to alphanumerics, own file, nothing outside the log folder, two decoy files of other sessions untouched; 3,000 files in 30 month folders → 0.022 s per event against 0.018 s empty; a log path with a space works |
| e | see below | 12 arms |

### The round (e)
`round/` holds the scripts as run (`build.sh`, `run-arm.sh`, `run-all.sh`, `arms.txt`, `score.py`), the two prompts and the scorer's output (`score.tsv`, `score.txt` with each arm's log-related passage verbatim). Trees: `harness/fixture` + the candidate file, the machine's global git ignore neutralised. Two models × two prompts × 3; the prompts differ by one sentence, the consent. Launcher `claude -p`, tools `Read,Write,Edit,Bash,Glob,Grep`, no permission bypass; turn 2 is a new session with a marked reply. All 12 ran to the end, no relaunch of an arm (a first launch of the whole round died before any API call on a shell detail and was rebuilt from fresh trees). 2.17 USD, 352 s.

| Cell | Switch written | Log works end to end (script + switch + both voices of turn 2) | Personal settings file ignored by git | Asked / left to the user |
|---|---|---|---|---|
| haiku, yes | 2 of 3 | **2 of 3** | 2 of 2 written | — |
| sonnet, yes | 2 of 3 | **2 of 3** | 2 of 2 written | — |
| haiku, none | **0 of 3** | — | — | 3 of 3 (two with a question, one *"Tell me yes or no. I won't switch it on without your approval"* — scored `no` by the scorer's question-mark rule) |
| sonnet, none | **0 of 3** | — | — | 3 of 3 |

- **The two `yes` arms that did not end with a log were stopped by the tool, not by the text**: in `h-yes-1` and `s-yes-3` the headless run denied the write to `.claude/` (`permission_denials`: Write `.claude/settings.local.json`; in `s-yes-3` also two shell commands creating `.claude`). Both arms stopped, said so, and printed what to do — neither worked around the denial. The same write was allowed in the other four arms and in both pilots: the denial is not constant (6 of 8 runs allowed), and nobody here determined what it depends on. In an interactive session that write is a permission prompt the user answers.
- Wherever a settings file was written (4 of 4) it was `settings.local.json`, valid JSON, the three events, and ignored by the arm's own `.gitignore`. The script, where written (9 of 12), was byte-equal to the block; the generated rules file byte-equal to the embedded copy in 12 of 12.
- Without consent no arm switched anything on (0 of 6); three of the six wrote the script and left it unused — what the text asks (*write the script … show … switch it on only on their yes*); three did not write it and asked first.
- Haiku: about 0.03 USD and 100 s per bootstrap; Sonnet: about 0.24 USD and 50 s.

### What the round does not show
- Three runs per cell: counts, not rates. One fixture, one harness (Claude Code), two models of one family.
- The `yes` was in the prompt: an arm that asks and then *receives* a yes was never run — an arm has nobody to ask. The two ends were measured, as planned in THINK.
- No arm launched a subagent or ran on another tool: the third hook and the *translate, do not copy* sentence are unmeasured.
- No control without the worked example (*contract only*): planned in `02_tasks.md`, not run — whether the example is what does the work is not known.
- The scorer's `asks` and `shows config` columns are text rules; the passages are in `round/score.txt` for a reader to judge.

## Verdict
**PASS_WITH_CAVEATS** for a–e at 4efabba. The candidate does what it says on the harness it was tried on: with a yes the log is set up and works unless the tool refuses the write; without one nothing is switched on. Caveats to carry wherever the feature is described: Claude Code only; the headless denial; no contract-only control.
