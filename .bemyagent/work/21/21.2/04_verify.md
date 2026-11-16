# 21.2 — VERIFY

**Verifier:** claude-fable-5-2, a separate agent. I did not write `census.py`, run it, or write the recount. Everything below comes from commands run on 2026-11-12; the author's log and the recount's report were read last, only to compare.

**Verdict: PASS_WITH_CAVEATS.** The counts reproduce and both controls pass. The published headline (55 incomplete of 147) is not fit to decide on by itself: 35 of the incomplete sessions created the rules file themselves, and the unit (one transcript) hides 7 of the 9 partial restores in main sessions. The decomposed numbers below are fit to decide on, on a thin base. One validation clause is not met: `03c_verify_census.json` holds transcript text.

Privacy: this file holds counts, session-file basenames, structural labels (the shape of a read, never its text) and the folder names of the headless arms. Scratch scripts are in the session scratchpad under `v212/` and are not part of the repo.

## The numbers

| | scored | accessed | not accessed | complete | incomplete |
|---|---|---|---|---|---|
| Author, as published (`03b_census.json`) | 253 | 147 | 106 | 92 | 55 |
| Author's logic, same population as below | 248 | 143 | 105 | 89 | 54 |
| Recount (`03c_verify_census.json`) | 248 | 142 | 106 | 89 | 53 |
| **Mine** | **248** | **142** | **106** | **90** | **52** |

Population: 258 transcripts on disk now, less 10 subagents of session `<session-id>-…` started from 2026-11-11T23:37Z (this work). The author's run excluded only its own transcript, so it scored 5 of those subagents (4 accessed: 3 complete, 1 incomplete).

"Complete" = all eight numbered headings seen in results of reads of a rules file before the first file-changing call. Before the first change **inside a project or fixture tree** the split is 92 / 50.

### By kind (mine)

| Kind | n | accessed | complete | incomplete |
|---|---|---|---|---|
| This repo, main session | 2 | 2 | 1 | 1 |
| This repo, subagent: fixture arm (Agent tool) | 172 | 96 | 61 | 35 |
| This repo, subagent: changes the repo | 11 | 4 | 3 | 1 |
| This repo, subagent: scratch only or no change | 22 | 15 | 9 | 6 |
| Headless arm | 11 | 6 | 6 | 0 |
| Other project, main session | 18 | 14 | 8 | 6 |
| Other project, subagent | 12 | 5 | 2 | 3 |
| **Total** | **248** | **142** | **90** | **52** |

### The 52 incomplete, by kind × failure mode

| Failure mode | repo main | fixture arm | changes repo | scratch/none | other main | other sub | total |
|---|---|---|---|---|---|---|---|
| A. The session wrote the rules file itself (bootstrap, install, update), then looked at part of it | 0 | 29 | 0 | 2 | 4 | 0 | **35** |
| B. Whole read, but after a scratch or memory write and before any project change | 0 | 0 | 0 | 1 | 1 | 0 | **2** |
| C. Look at a fixture or stub rules file, not a restore | 0 | 3 | 1 | 1 | 0 | 0 | **5** |
| D. Deliberate first-N-lines slice of the project's own rules, at restore | 0 | 3 | 0 | 2 | 1 | 3 | **9** |
| E. Tool truncation of a whole read | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
| Total | 1 | 35 | 1 | 6 | 6 | 3 | **52** |

**Genuine partial restores, transcript level: 10 of 102.** Denominator: 142 accessed less 35 (A) less 5 (C) = 102 sessions whose access was a restore. Numerator: 1 tool truncation (E) plus 9 deliberate slices (D). 8 of the 10 went on to change project or fixture files.

- E: `<session-id>` — 6 of 8 headings, §5 and §6 lost.
- D: `<session-id>` (first 80 lines, 5 of 9); `agent-<agent-id>`, `agent-<agent-id>`, `agent-<agent-id>` (5, 3, 5 of 8; all then changed repo files); `agent-<agent-id>`, `agent-<agent-id>`, `agent-<agent-id>` (first 100 lines, 7 of 8; then changed fixture files); `agent-<agent-id>` (7 of 8) and `agent-<agent-id>` (first 80 lines, 4 of 8), scratch only.
- Of the 52 incomplete, 38 held all eight titled headings from another source (the protocol file, a prompt) before their first project change; 14 did not.

### Restore events in main sessions that carry the sentinel

A restore event is a session start or the segment after a compaction. 12 main transcripts, 36 events.

| What the agent did before its first project change in the segment | this repo (2 transcripts) | other projects (10) | total |
|---|---|---|---|
| Whole read | 8 | 12 | 20 |
| Whole read cut by the tool | 1 | 0 | 1 |
| Deliberate first-N-lines slice | 4 | 4 | 8 |
| Incidental search of the file only | 0 | 2 | 2 |
| No rules read | 1 | 4 | 5 |
| Total | 14 | 22 | 36 |

- **Partial restores: 9 of 36 events (5 of 14 in this repo).** The transcript-level headline shows 2 of the 9; the other 7 follow a compaction.
- This repo's four slices are all in `<session-id>`, after the compactions of 2026-11-01, 11-04, 11-07 and 11-09: first 80 lines twice, first 60 once, and lines 1–80 plus 95–100 once. §5–§8 (or §5, §6, §8) were unread before the first project change of each segment. **The headline scores this transcript complete, and the author used it as the negative control.**
- Nothing re-injected the text in those segments: 0 attachments with three or more titled headings, 0 headings in the compaction summaries.
- The two whole reads after compaction in `<session-id>-…` came after the failure had been noticed, so they are not an independent observation.
- Geometry of the current rules file (107 lines, 14,267 bytes; `grep -n '^## '` gives lines 3, 17, 23, 49, 82, 89, 99, 103): the first 60 lines end inside §4 (6,744 bytes), the first 80 too (10,494 bytes), the first 100 lose the §8 heading (13,695 bytes).

## Point by point

### 1. Is the instrument measuring the thing

Commands: `vscan.py` (my structural scanner over all transcripts), `vjudge.py` (my definitions), `three.py` (imports `census.py` and `verify_census.py` unmodified and scores the same 248 files with all three), `an4.py`–`an17.py`, `final.py`.

Definitions that move the headline, largest first:

| Definition | Effect |
|---|---|
| Unit = one transcript, first write only | Hides every restore after a compaction: 7 of 9 partial restores in sentinel main sessions |
| A session that writes the rules file and later reads part of it counts as an incomplete access | 35 of the 52 incomplete |
| Any `mkdir` or redirect in scratch counts as the first file-changing call | 2 sessions flip to complete when scratch and memory writes are ignored (92 / 50) |
| Author's population includes current-session subagents | +4 accessed, +3 complete, +1 incomplete |
| `census.py` counts a search whose text argument holds the file name as an access | +2 incomplete (`agent-<agent-id>…`, `agent-<agent-id>…`) |
| The recount counts a read redirected into a file as an access | +1 incomplete (`agent-<agent-id>…`) |
| Mine counts `git show REV:path` of a fixture stub | +1 incomplete (`agent-<agent-id>`) |
| Glob reads and script reads counted as accesses (sensitivity, not my primary) | +4 and +13 accessed, all incomplete |
| One byte-identical transcript sits in two project folders (`<session-id>.jsonl`) | −1 accessed, −1 incomplete if counted once |
| Heading lines stand for content | In the data: 88 of my 90 complete rest on a whole read with no truncation marker; 2 are complete through slices only (`agent-<agent-id>…`, `agent-<agent-id>…`) |
| Eight headings required where the file had nine | 0 sessions: every nine-section session but `<session-id>-…` saw 9 of 9 |

Truncation against deliberate slice: across every whole read in the corpus, exactly one carries a truncation marker with headings missing — the known session. Every other partial read is a slice the agent chose. No complete session has a truncation marker on a rules result before its first change.

Strict agreement of all three instruments: 141 accessed.

### 2. Controls

Real session `<session-id>.jsonl`, through both scripts (`an15.py`):

```
author  -> accessed True, complete False, first_kind bash-chained, missing [5, 6], cause truncation-sign, first_secs [1,2,3,4,7,8]
recount -> accessed True, complete False, mode c, fc_line 231, fc_class repo, secs_pre [1,2,3,4,7,8]
```

My scan agrees: use 0 is a chained shell read, 10,039 characters, mid-output truncation marker; first file-changing call is use 24 (JSONL line 231); line slices deliver §5 at use 26 and §6 at use 27, both after; whole reads at use 36 and use 59. **Both pass.**

Two slips in `03_execute.log`, no effect on any count: it attributes §6 to lines 60–84 and §5 to lines 85–98 (the reverse is true), and it calls 231 an index where it is the JSONL line.

Synthetic transcripts (`synth.py` builds 22 from the public rules file only; `runsynth.py` scores them with all three):

| Case | author | recount | mine | truth |
|---|---|---|---|---|
| Whole read, then write | C | C | C | complete |
| Tool truncation, 6 of 8 | I | I | I | incomplete |
| First-N-lines slice, 3 of 8 / 7 of 8 | I | I | I | incomplete |
| Write, then whole read | I | I | I | incomplete |
| No access | NA | NA | NA | NA |
| Search with the file name as text argument | I | NA | NA | NA |
| Search with the file name as the pattern | I | I | NA | NA |
| Redirect that writes the rules file | NA | NA | NA | NA |
| Read redirected into a file | NA | I | NA | NA |
| Heading-line search returning all eight | C | I | C | content not read |
| Cut inside §4 with all headings surviving | C | C | C | content incomplete |
| Nine-section file, §9 cut | C | C | C | incomplete |
| Whole read through a glob | NA | NA | NA | complete |
| Whole read in a shell loop | NA | NA | C | complete |
| Scratch write, whole read, project write | I | I | I | complete before the first project write |
| Whole read at start, slice after a compaction | C | C | C | second restore partial |

Both scripts get the clean cases right. Each fails on edge cases; the one with weight in the real data is the last row.

### 3. The disagreement, resolved

Three-way table on the 248 (`three.py`, then `an6.py`), as author / recount / mine:

| Pattern | n | Ruling |
|---|---|---|
| C / C / C | 89 | |
| I / I / I | 51 | |
| NA / NA / NA | 103 | |
| I / I / C | 1 | `agent-<agent-id>…`: all eight heading lines came from a search in a loop; complete by the stated definition, content not read |
| I / NA / NA | 2 | recount right: a search that names the file is not a read |
| NA / I / NA | 1 | author right: a read redirected to a file shows the agent nothing |
| NA / NA / I | 1 | mine alone: `git show` of a fixture stub |

The two published runs differ by 5 accessed because of population (4) and definitions (net 1). On one population they agree on 245 of 248 verdicts. **My headline: 142 accessed of 248; 90 complete, 52 incomplete.**

### 4. Population

- Tables above. Arithmetic: 142 + 106 = 248; 90 + 52 = 142; kinds sum to the totals (`final.py`).
- Agent-tool fixture arms (172; 125 since 2026-10-27): 164 held all eight titled headings before their first change in the fixture tree, from a whole read of the protocol file, the rules, or both; 3 held 7 of 8 (first 100 lines); 5 held no protocol text from any source.
- The 5: `agent-<agent-id>`, `agent-<agent-id>`, `agent-<agent-id>` (2026-10-31), `agent-<agent-id>`, `agent-<agent-id>` (2026-11-09). Each inherited this repo's sentinel through the Agent tool and changed fixture files. Whether they were no-protocol arms by design cannot be told from structure; the round logs can say. **Open item, small.**
- Headless arms (11): 6 accessed, 6 complete, each by a whole read.
- **The five headless arms that never accessed the rules** are explained by design. None carried a sentinel.

| Arm folder | Transcript | Round and condition |
|---|---|---|
| `probe211` | `<session-id>…` | 20.11 harness probe: a tree with one marker file and no rules file (`20.11/03_execute.log:10`) |
| `probe211` | `<session-id>…` | same |
| `r2011-q97` | `<session-id>…` | 20.11 control, no protocol file (`certificate.py:15`, side N) |
| `r2011-q98` | `<session-id>…` | same |
| `r2011-q99` | `<session-id>…` | same |

The six protocol arms (20.11 q94–q96, 20.12 q100–q102) read the rules whole.

### 5. Which pre-registered outcome

None of the three fits as written.

- **(i) only in the known session — false.** Tool truncation is only there (1 event in the corpus). Partial restores are not: 9 other transcripts, 8 other restore events in main sessions.
- **(iii) common in harness arms — false.** 0 of 6 headless protocol arms incomplete. Of 172 Agent-tool arms, 3 worked from 7 of 8 sections and 5 are the open item above. The 35 "incomplete" arms of the headline are 29 installs, 3 fixture looks and those 3.
- **(ii) several, in main sessions — nearest, by a different mechanism.** The spec was written for a cut the agent cannot see. What recurs is a slice the agent chooses: 8 restore events in main sessions, 4 of them in this repo, plus 8 subagent transcripts.

How thin: 2 main transcripts in this repo (14 events), 12 sentinel main transcripts in all (36 events), one user, one machine, and the four slices in this repo are repeated measures inside one long session.

Licensed:
- The spec's open question — one-off or routine — is answered: reading the first N lines of the rules at a restore is routine after compaction.
- Candidate 1 goes to an arm round. A count in the sentinel and the first line would in principle expose both a cut and a slice.
- The arm round needs a deliberate-slice condition beside the cut-file one, and a restore after compaction if the harness can produce it.

Not licensed:
- Any rate for tool truncation (n = 1).
- Any claim that a count changes what an agent does once it has chosen to slice. That is what the arm round measures.
- 55 of 147, or 52 of 142, as a base rate of partial restores.

### 6. Validation line

| Clause | Result |
|---|---|
| Both controls pass | Yes, in both scripts |
| `accessed + not accessed = scanned` | Yes: 147 + 106 = 253; 142 + 106 = 248; 142 + 106 = 248 |
| Headline with denominator, split by kind | Yes |
| Output holds no transcript text | **No for `03c_verify_census.json`; marginal for `03b_census.json`** |

Command: `prof.py`, `prof2.py`, `prof3.py` (count string leaves by key; nothing printed but counts).

- `03c_verify_census.json` (557,058 bytes): its `sessions` list is 415,821 of 430,653 compact characters. It holds 774 command strings cut to 200 characters (475 under `cmd200`, 299 under `what200`), 754 strings with spaces in all, and a `project` value per session — 10 folder names of other projects across 30 sessions. Only `tables` (12,827 characters) is aggregate.
- `03b_census.json` (26,184 bytes): string values are basenames and labels only. Its keys are not: `per_group` has 10 folder names of other projects, and `bash_other_access_first_words` has 22 distinct keys of which 8 are not plain command names (fragments up to 20 characters).
- `03d_crosscheck_sonnet.md`: names at least 2 other projects (6 occurrences) and carries 72 inline code spans of 25 characters or more, many of them command lines from transcripts.

Origin is public. Before any commit: drop the `sessions` list from `03c`, drop `per_group` keys of other projects and the first-word keys from `03b`, and rewrite or leave out `03d`.

## Defects, ranked by effect on the headline

| # | Script | Defect | Effect |
|---|---|---|---|
| 1 | both | Unit is the transcript; restores after a compaction are not scored | 7 of 9 partial restores in main sessions unseen; the negative control holds 4 |
| 2 | both | A session that creates the rules file is scored as a reader of it | 35 of the incomplete |
| 3 | both | A scratch `mkdir` or redirect is the "first write" | 2 sessions |
| 4 | `census.py` | Run did not exclude the current session's subagents | +4 accessed, +3 C, +1 I |
| 5 | `census.py` | A search with the file name as text argument is an access | +2 I |
| 6 | `verify_census.py` | A read redirected into a file is an access | +1 I |
| 7 | both | A search with the file name as its pattern is an access | 0 in the data (synthetic only) |
| 8 | both | Whole reads through a glob or a loop are missed; headings from the prompt or the protocol file are not credited | 0–2 sessions; matters for arms, where 32 of 35 incomplete held all eight from elsewhere |
| 9 | both | Heading lines stand for content; eight required of a nine-section file | 0–2 sessions |
| 10 | both | A duplicate transcript is counted twice | 1 |
| 11 | `verify_census.py` | Heading regex misses line-number prefixes; `api-request` lines not skipped | 0 |

## What the decision can rest on

- Tool truncation of a rules read: **1 event** in 248 transcripts.
- Partial restore at transcript level: **10 of 102**.
- Partial restore at event level, main sessions with the sentinel: **9 of 36**; this repo **5 of 14** (1 cut, 4 chosen slices).
- Harness arms: no finding on rounds since 2026-10-27 beyond 3 arms at 7 of 8 and 5 arms to check against their round's design.
