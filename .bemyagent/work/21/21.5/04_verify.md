# 21.5 — VERIFY

Independent verification, 2026-11-12. Model: **claude-fable-5-2**. I did none of the work of 21.5: I wrote no script, swapped no line, and edited no file except this one. Everything below comes from commands run during this verification, on the working tree as it stood (432 files: 390 tracked + 42 untracked-not-ignored, before this file was added).

Reference material outside the repo: `<scratchpad>/p215/` (the table, the brief, the list of 90 files, `orig/` with 122 untouched copies, the two "before" outputs). My own scratch: `<scratchpad>/v215/`.

Limits kept: the real CLI was never run; no `launch.sh`, no `cert_on_2011.py`, no script of rounds 13–20 was run — their changed expressions were evaluated in isolation; nothing under `<scratchpad>/r211` was written; no git command that changes state; the folder above the repo, other projects, the tool-config folder's contents and the transcripts were not listed or read. Two scripts were run, as allowed: `21.1/selftest.sh` and `21.1/dryrun.sh`.

Trace words are not written here. "The four words" = the account word, the name of the folder above the repo, the config folder's bare name, the uid temp-folder name.

## Verdict

**PASS_WITH_CAVEATS** *(first pass; the repairs that followed are judged in the Re-check section at the end, which carries the current verdict)*

The four-word search returns nothing, every script parses, every rebuilt value equals the old literal on this machine, the live apparatus gives the same output as before, the seeded trees are untouched. What stops this from being a plain PASS:

1. **One trace is still in the tree** — `work/21/21.1/03g_apparatus_reverify.md:50` spells the config profile's sub-folder name inside a glob. It is not one of the four words, so the builders' search could not see it. One token to replace; until then the "Delivers" line of `02_tasks.md` is not literally true. **Repair before any commit.**
2. **Two quoted regexes are no longer the regexes** (`03e:181`, `03g:87`), and one of them is the *proposed fix* for reader defect N1, which now reads with a case missing.
3. Six points of friction in the scripts that do not show on this machine today but will on another shell or another day (config directory no longer pinned; default-case regexes; one variable for two folders; `local.env` and the session scratchpad; empty variable; stale line references).

Findings in order of severity are at the end.

---

## CDM — Drift

*"rewriting notes beyond the token swap; improving old round scripts; touching the seeded trees; running anything that reaches the real `claude`."*

- **Notes.** My own comparator (`v215/swapcheck.py`: apply the table to each `orig/` line, compare with the tree) over the 19 non-script files: **45 changed lines, 40 reproduced by the table, 5 not** — `20.11/03_execute.log:17`, `21.1/03_execute.log:68`, `21.1/03e:181`, `21.1/03g:56`, `21.1/03g:87`. All five replace the config folder's bare name, for which the table had no entry, with `<claude-config>`. No sentence was reworded anywhere. This is a substitution outside the table, flagged by its builder; not a rewrite. → point 2.
- **Old scripts.** `diff -U0 orig tree` on all 71 scripts (137 hunks, 556 diff lines, all read): rounds 13–20 change only an added `import os` and the right-hand side of constants; round 21 adds helper names and the `local.env` line. No control flow, no threshold, no regex other than the ones listed in the functional table was touched. No drift.
- **Seeded trees.** Hash identical before and after my two runs → point 6.
- **Real CLI.** Not run by me. The dry-run's own step 12 prints `dry-run projects in the REAL config dir: 0` and `real claude directory in the PATH used by launch.sh: 0`. Before running it I checked that no `claude` sits in the three directories of its reduced `PATH`.

**Drift: none found**, with the five off-table lines noted.

## CDM — Validation

| Criterion in `02_tasks.md` | Command (now) | Result |
|---|---|---|
| residue search → 0 files, tracked and untracked-not-ignored | `{ git ls-files; git ls-files -o --exclude-standard; } \| xargs grep -ailE '<the four words>'` | **0 files** (was 90; I confirmed all 90 `orig/` copies hold the words) |
| non-script diffs are table swaps only | `swapcheck.py <p215> nonscript.txt` | 40 of 45 lines; **5 lines off-table** (above) — criterion not met to the letter |
| all scripts parse | `PYTHONPYCACHEPREFIX=<v215>/pyc python3 -m py_compile` ×65; `bash -n` ×6 | 65 ok / 0 fail; 6 of 6; 0 `__pycache__` in the repo |
| 21.1 selftest 82 PASS | `bash .bemyagent/work/21/21.1/selftest.sh` | exit 0, 82 PASS, `0 mismatches`, stderr empty, `cmp` identical to `selftest_before.txt` |
| dry-run verdicts as in `03d_dryrun.txt` | `bash .bemyagent/work/21/21.1/dryrun.sh` | exit 0, 332 lines; identical to `03d_dryrun.txt` and to `dryrun_before.txt` as a multiset of lines once paths, session uuids and the five stub `resumed_from` ids are masked |
| trees' hash = baseline | the `find … \| shasum \| shasum` of point 6 | `111b2ed91a9fae9f9a34b7654137d19dc53d81e5` before and after |

**Validation: met, except the second row by five lines.**

## CDM — Pivot

*"a script that cannot be made location-independent without changing what it measured → stop, leave it, report it; more than two → back to THINK."*

No script was left untouched and none was reported as impossible. I found none where the new expression measures something else **on this machine with the environment the round had**. Three are location-independent in form but bound to this machine's data by a session-id literal that was kept (`20.10/score.py:18`, `21.2/census.py:16`, `21.2/verify_census.py`): they cannot produce their result anywhere else, with or without this task. One (`21.1/cert_on_2011.py`) now needs its one variable to mean two different folders → finding 7. **Pivot not triggered.**

---

## Point 1 — nothing of the machine is left

Commands, all over the 432 files, `grep -a`:

| Search | Hits |
|---|---|
| the four words, case-insensitive | 0 files |
| the four words in file **names** | 0 |
| `/(Users\|home)/<name>` path shapes (placeholder names excluded) | 0 lines |
| dashed project-key shapes (a dash, the platform's users-folder name, a dash, a name) | 0 files |
| `claude-<digits>` temp folder; `uid=<my uid>` | 0 / 0 |
| URL-encoded slashes before `Users`/`home`; the account word with a separator between letters | 0 |
| short hostname, computer name, local host name (from `hostname -s`, `scutil`) | 0 |
| e-mail-shaped strings | 0 |
| the config profile's sub-folder name (taken from the environment, not from the table) | **1 line: `21.1/03g_apparatus_reverify.md:50`**, in a glob quoted from test case c17; unchanged from `orig/`. *(Corrected in the Re-check: my first note on the word's other occurrences in the tree was wrong — see there.)* |

Candidates weighed:

- **Session ids** — 18 distinct uuids, 34 occurrences in 10 files (the two 21.2 JSON outputs, the two round-20 certificates, `21.2/04_verify.md`, `21.2/01_think.md`, `21.1/03d_dryrun.txt` (stub-generated), and three scripts). Random identifiers: they name a transcript, not a person or a machine, and are useless without the transcript store. Not a trace in my judgement; the user decides, as for the commit author name in 21.6.
- **`/opt/homebrew/bin`** (`21.1/dryrun.sh:3`, `21.1/03e:8`) — a platform prefix shared by every machine of that kind. Not a trace. Side note: step 12 of the dry-run counts `homebrew` in `PATH`, which is a machine assumption — on another platform the line reads 0 whatever the `PATH` holds.
- **`21.1/certificate.py:83`** `/(?:Users|private|tmp)/…` — a generic pattern, present before, names nobody.
- **`LICENSE`, `site/template.html`** — the public author and repo owner.

`local.env`: `git check-ignore -v` → `.gitignore:23:local.env`; it is not in `git ls-files`. Ignored files that still hold the words: `.bemyagent/log/` (12 files), `21.1/local.env`, `.claude/settings.local.json`. **No file with the words is untracked-but-not-ignored.**

What this proves: none of these byte patterns is in any file git would add or already tracks, in the working tree, now. What it cannot prove: that no other identifying token exists — the profile name was found only because I took it from the environment, and a token I did not think of is not covered. It says nothing about the history: `HEAD` still holds the old content of the 75 tracked files, and 73 commits carry the account word as author (21.6).

## Point 2 — the notes say what they said

- **Swaps.** 45 changed lines in 18 files, plus one swapped line and one new section in `harness/README.md`. 40 are pure table swaps. The 5 that are not are listed under Drift.
- **JSON.** `python3 -c "json.load(open(f))"` on `15.11/03b_score_output.json`, `20.11/03c_certificate.json`, `20.12/03c_certificate.json`, `21.2/03b_census.json`, `21.2/03c_verify_census.json` → all parse.
- **Round 20 finding, read in context** (`20.9/04_verify.md:98`, `20.10/01_think.md:15`, `20.10/03b_census.txt:4`, `20.10/04_verify.md:18`, `20.11/03_execute.log:102`, `docs/05:507`): the finding is that the arms opened the *parent repo's* rules file by absolute path instead of their own copy. Each passage now reads `<repo>/.bemyagent/docs/00-ai-rules.md` and the surrounding words ("by absolute path", "the parent repo's") still carry the point. **Unchanged.** `20.10/report.py:74` prints the same placeholder, so a regenerated census matches the swapped note.
- **21.1 reports** (`03e`, `03g`): the three blocking defects of `03e` and N1–N6 of `03g` read as before, with the exceptions below.

The five flagged lines and the alternation:

| Line | Now | Judgement | Minimal repair |
|---|---|---|---|
| `21.1/03e_apparatus_verify.md:181` | a regex quoted with `…\|launch\.status\|<claude-config>\|CLAUDE_CONFIG_DIR` | **misleading** — it is presented as the pattern and is no longer one; and `<claude-config>` means the whole config directory everywhere else, while the fragment was the escaped bare name of the folder that holds it | use a placeholder of its own for that name (e.g. `<config-folder-name>`) |
| `21.1/03g_apparatus_reverify.md:56` | "the pattern that gates it (`<claude-config>`)" | **still true in substance** (the arm's own memory folder lies under the config directory), imprecise for the same reason | same placeholder |
| `21.1/03g_apparatus_reverify.md:87`, first two uses | "`<claude-config>` in `NAMED`", "drop `<claude-config>` from `NAMED`" | **still true in substance** — N1 remains readable and actionable | same placeholder |
| `21.1/03g_apparatus_reverify.md:87`, the alternation | `(?:~\|\$HOME\|\$\{HOME\}\|~)/\.claude…` | **broken** — the fourth alternative was the absolute home path; the duplicate reads as a slip, and N1 implemented as written loses the absolute-path case | second `~` → `<home>` |
| `21.1/03_execute.log:68` | a list item `<claude-config>` among the names `NAMED` matches | **still true in gist**, imprecise | same placeholder |
| `20.11/03_execute.log:17` | `<claude-config>/projects/…-probe211/<session>.jsonl` (was a shorter, relative mention) | **still true** | none |

Also cosmetic: `21.1/03g:5` now reads "(scratchpad = `<scratchpad>`)".

## Point 3 — scripts changed only where a value comes from

Method: `v215/equiv.py` extracts every changed top-level assignment from `orig/` and from the tree by AST and evaluates both, `__file__` set to the script's path, under two environments — **E1** as `21.1/local.env` gives it (scratch = the current session's scratchpad, config directory = the one my shell already has, which I checked equals the one in `local.env`), **E2** the same with `BMA_SCRATCH` pointed at the scratchpad of the session the closed rounds ran in. `v215/byhand.py` loads `NAMED` and `path_class` from both versions and compares them on probe strings. Shell expressions were evaluated with `$0` replaced by the script's path.

- **E2, all 65 `.py`:** 114 changed assignments, **100 identical** to the old literal — every repo root, every scratch folder of rounds 13–20, the nine `tasks` folders, `20.10` `SUB` and the four `P_*` paths, both round-20 certificates, the 21.2 roots and keys. The other 14: 8 new helper names; the three `S` of 21.1 (identical under E1 instead — round 21 lives in the current session's scratchpad); `NAMED`; `tmp` and `src` of `cert_on_2011.py` (not evaluable in isolation, read by hand).
- **E1, round 21:** 22 assignments, 10 identical, 8 new names, `NAMED`, and the three of `cert_on_2011.py`.
- So the closed rounds need `BMA_SCRATCH` = their own session's scratchpad, round 21 the current one. With the wrong one the scripts read a folder that does not hold the round: a stop (`FileNotFoundError`) or an empty result, not a wrong number — by reading, not run.
- **The `tasks` folder** (`15.4/score.py:10`, `19.2b/score.py:5`, `19.3/score.py:9`, `20.2/score.py:5`, `20.3/score.py:6`, `20.8/score.py:9`, `20.9/score.py:12`, `20.11/score.py:14`, `20.12/score.py:16`): `Path(BMA_SCRATCH).parent / "tasks"` — identical to the old literal under E2, and that folder exists. It holds only when `BMA_SCRATCH` is a session scratchpad; with any other scratch directory the folder is simply not there.
- **Imports:** every name used by a changed line is imported in its file; `py_compile` passes on all.

### Functional lines

"Identical" = same value, or same answer on every probe, on this machine with the environment stated.

| File:line | What it feeds | Before → after | On this machine |
|---|---|---|---|
| `20/20.10/score.py:16` `ROOT` | base of the four substring tests | literal repo path → `BMA_REPO` or 4 levels above the script | identical |
| `20/20.10/score.py:17–18` `SUB` | the subagent-transcript folder that is globbed (line 58) | literal → config dir / `projects` / computed key / session id (kept literal) / `subagents` | identical (config dir as pinned) |
| `20/20.10/score.py:20–22` `P_RULES`, `P_BMA`, `P_DOCS` | "the arm read the parent's rules / protocol / decisions / plan" (lines 90, 97–98) | four literals → built from `ROOT` | identical |
| `20/20.10/report.py:74` | text of the census note | literal path → `<repo>/…` | differs by design: output text only, equal to the swapped note |
| `20/20.11/certificate.py:10–12`, `20/20.12/certificate.py:14–16` `CFG`, `R`/`S`, `PARENT` | transcript glob root; `startswith(arm_dir)`; "parent path in a tool call" | literals → env / computed | identical under E2. `PARENT` is the repo itself, as before, not the folder above it |
| `20/20.11/launch.sh:15`, `20/20.12/launch.sh:14` | which profile the arms run under | pinned to the profile directory → caller's `CLAUDE_CONFIG_DIR`, else `~/.claude` | identical while the shell holds the pinned value; **differs otherwise** (finding 6). Closed rounds, never to be rerun |
| `21/21.1/certificate.py:14` `S`; `:18` `CFG`; `:19` `PARENT` | arm trees and outputs; transcript root; parent-path test | literals → env / computed | identical (E1) |
| `21/21.1/certificate.py:21,26` `_CFG_NAME`, `NAMED` | "a tool call names the apparatus" | literal fragment → `re.escape` of the config folder's name | identical on 21 of 21 probes with the config dir as pinned; the pattern differs only by an escaped hyphen. **With the default `~/.claude`: broader — 5 of 21 probes flip** (any `.claude…` token) → finding 5 |
| `21/21.1/cert_on_2011.py:5` `OLD` | where 20.11's six transcripts' arm folders are | literal in the closed rounds' scratchpad → `BMA_SCRATCH/r2011` | identical under E2; **under E1 that folder does not exist** → stops at line 14 |
| `21/21.1/cert_on_2011.py:21` `tmp` | scratch copy for the stub transcript | literal in the current scratchpad → `BMA_SCRATCH` | **differs**: under E2 the temp folder is made (and removed) inside the closed rounds' scratchpad. No effect on the reading. Not run |
| `21/21.1/cert_on_2011.py:23,28` | transcript source; the outside instruction path of the stub | literals → config dir; repo root + `/AGENTS.md` | identical (by reading: same expressions as evaluated elsewhere) |
| `21/21.1/launch.sh:40–41` | scratch directory | literal → `local.env`, then `BMA_SCRATCH` required | identical with `local.env` |
| `21/21.1/launch.sh:44` | profile of the live arms | `R211_CFG` or pinned literal → `R211_CFG`, else caller's `CLAUDE_CONFIG_DIR`, else `~/.claude` | identical today; **no longer a pin** (finding 4) |
| `21/21.1/selftest.sh:12,150` | fixture: instruction file outside the arm | literal repo path → `ROOT` | identical (`ROOT` == repo) |
| `21/21.1/selftest.sh:13,153` | fixture: attachment naming a foreign memory path | literal with a made-up project key → config dir + a neutral key | differs in the string, same case; selftest output byte-identical |
| `21/21.1/dryrun.sh:9–10,14,55,123–130` `ROOT`, `KEY`, `STUB_KEY` | the decoy project folder | literal key → computed from `ROOT` | identical (`KEY` == old literal, shell and Python) |
| `21/21.1/dryrun.sh:11,133` `REAL_CFG` | "the real CLI never ran" count | literal → caller's config dir, captured before the override | identical while the shell holds the pinned value |
| `21/21.1/check_pilot.sh:7,9`; `score.py:25`; `setup.py:12–13` | scratch, repo root | literals → env / computed | identical (E1) |
| `21/21.2/census.py:12,15` `ROOT`, `REPO_FOLDER` | transcript store; "this repo's" folder | literals → config dir; key computed from `BMA_REPO` or the script-relative `REPO` | identical |
| `21/21.2/verify_census.py:10–17` | same, plus `PARENT_DIR`, `HOME`, `CFG_NAME` | literals → env / computed | identical. **`PARENT_DIR` is the folder above the repo and `REPO_ROOT` the repo: the two stay distinct**, as in the old literals |
| `21/21.2/verify_census.py:230,273` | `~` expansion | literal home → `Path.home()` | identical |
| `21/21.2/verify_census.py:239` | class `claude-state` | literal folder name → `CFG_NAME` | identical on 33 of 33 probes with the config dir as pinned. **With the default: narrower — 2 of 33 flip** to `home-other` → finding 5 |
| `21/21.2/verify_census.py:241,302,313` | class `repo` (anything under the folder above the repo) | literal → `PARENT_DIR` | identical; a sibling project is still classed `repo`, as before |
| `21/21.2/verify_census.py:666` | `cwd_repo` | literal repo path → `str(REPO_ROOT)` | identical |
| `17/17.2/setup.py:17` | the protocol file copied into each arm | literal scratch path → `BMA_SCRATCH` | identical under E2 (the file itself is no longer on disk in either scratchpad) |
| the remaining constants of rounds 13–20 (repo root in 34 scripts, scratch in the rest) | where arms are built and read | literals → `BMA_REPO` / script location; `BMA_SCRATCH` | identical under E2 |

## Point 4 — everything parses

`py_compile` on the 65 `.py` with the cache redirected outside the repo: 65 ok, 0 fail. `bash -n` on the 6 `.sh`: 6 of 6. `find . -name __pycache__` (outside `.git`): 0. Three other scripts exist outside the 71 (`15.11/score.py`, `20.1/cost.py`, `harness/tokens.py`): they take their paths from the command line and were not part of this task.

## Point 5 — the live apparatus still behaves

- `bash .bemyagent/work/21/21.1/selftest.sh` → exit 0; 84 lines; 82 PASS; `0 mismatches`; `cmp` with `selftest_before.txt`: identical.
- `bash .bemyagent/work/21/21.1/dryrun.sh` → exit 0; 332 lines, as before. After masking session uuids and the five stub-generated `resumed_from` ids, the sorted output is identical to `dryrun_before.txt`; after also masking paths, identical to the repo's `03d_dryrun.txt` (45 verdict-type lines among them). Unsorted, 36 lines differ: order of the parallel arms and the ids. The live output prints real paths and the real project key — it was kept in my scratch only; pasting a fresh run into the repo would bring the trace back.
- After both runs: `git status --porcelain` 86 entries as before (81 modified, 5 untracked), no `__pycache__`.

**`BMA_SCRATCH` unset and no `local.env`** — by reading, plus the expressions in isolation:

- The four 21.1 shell entry points and the two round-20 launchers: the guard `[ -f "$HERE/local.env" ] && …` passes quietly, then `S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"` prints that message and the shell exits (status 127 in my isolated run), before anything is created. **A clear stop**, also when the variable is set but empty.
- The Python scripts: `os.environ["BMA_SCRATCH"]` → `KeyError: 'BMA_SCRATCH'`. A stop, with a traceback instead of a sentence. They do not read `local.env`: run directly, they need the variable exported by hand.
- **Not a stop:** `BMA_SCRATCH` set but empty in a Python script gives `Path('.')` — the current directory, silently (finding 9). And `CLAUDE_CONFIG_DIR` unset gives `~/.claude` silently everywhere (findings 4–6).

## Point 6 — seeded trees untouched

From inside `<scratchpad>/r211`: `find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -print0 | sort -z | xargs -0 shasum | shasum` → **`111b2ed91a9fae9f9a34b7654137d19dc53d81e5`**, 250 files, before my runs and again after both. Equal to the baseline.

## Point 7 — the new text is clean and true

No trace in `harness/README.md` (last section), the new row of `03-code-map.md`, plan rows 21.5–21.7 and the Resume paragraph, the last bullet before `## Known issues` in `05` — covered by the searches of point 1.

Claims checked against the repo (read-only git queries and greps):

| Claim | Check | Result |
|---|---|---|
| 75 tracked files, 4 already public | list of 90 split by `git ls-files`; `git grep -il <four words> origin/main` | 75 tracked; 4 files at `origin/main` — true |
| 41 unpushed commits, last push 2026-10-29, tag `3.4.0` among them, 19 of 20 tags published | `git rev-list --count origin/main..HEAD`; `git tag --merged` | true |
| account word is author on 73 commits, 32 published; tagger on 9 annotated tags; commit messages clean; `git filter-repo` not installed | `git log --format`, `git for-each-ref`, `command -v` | true |
| "the repo ← `BMA_REPO`, else the script's own location" | grep over the 71 | true for the 37 scripts that need the repo path. `21.1/score.py:24` uses its own location only — it locates code to import, which must be the clone, so no contradiction |
| "`BMA_SCRATCH` — required; the script stops without it" | grep; isolated runs | true for the 60 scripts that use it (the other 11 do not need it); the Python stop is a bare `KeyError`; an empty value is not stopped in Python |
| "config dir ← `CLAUDE_CONFIG_DIR`, else `~/.claude`" | grep | true; 21.1 puts its test hook `R211_CFG` in front, not mentioned in the table |
| "folder name computed, every non-alphanumeric → `-`" | computed key == old literal, shell and Python | true **for this path**, whose only such characters are `/` and `-`. The tool's rule for other characters is not verified (it would need the config folder) |
| "`local.env` … the name is gitignored" | `git check-ignore -v` | true |
| "For three weeks" (README), "three weeks of rounds" (`05`) | `git log -S'<home path>'` → first commit 2026-10-26 | **17 days**, not 21 |
| plan row 21.5: "75 tracked files, 14 untracked" | the 90-file list | **15** untracked (75 + 15 = 90, as `03_execute.log` [1] says) |
| `02_tasks.md` row 1: "119 files" backed up | `orig/` | **122**, as `03_execute.log` [2] says |
| code-map row: `work/<N>/<N.Y>/*.py` | the path | the folder is `.bemyagent/work/…`; the other rows of that table are repo-relative |

The README's closing rule — search for "the account name and the home path" — would not have caught the config folder's name or the profile name; this verification found one of each kind only by searching wider.

---

## Findings, by severity

1. **Trace left** — `.bemyagent/work/21/21.1/03g_apparatus_reverify.md:50`: the config profile's sub-folder name, inside a glob. Repair: that one token → `<profile>`. Blocks the commit.
2. **Record broken** — `.bemyagent/work/21/21.1/03g_apparatus_reverify.md:87`: the proposed pattern for N1 lists `~` twice; the lost alternative was the absolute home path. Repair: second `~` → `<home>`. Matters because N1 is still to be implemented from this line.
3. **Record misleading** — `.bemyagent/work/21/21.1/03e_apparatus_verify.md:181` (quoted regex), and the same substitution at `03g_apparatus_reverify.md:56`, `:87`, `03_execute.log:68`: `<claude-config>` stands for a bare folder name here and for a full directory everywhere else. Repair: a placeholder of its own on those lines.
4. **Live launcher no longer pins the profile** — `.bemyagent/work/21/21.1/launch.sh:44` with `local.env:2`: the caller's `CLAUDE_CONFIG_DIR` wins, `local.env` only fills it when unset, and with neither the launcher runs under `~/.claude` without a word; the header comment (`launch.sh:23`) still says "pinned". Same today on this machine. For the user: should `local.env` set it unconditionally, as its line 1 does for the scratch directory?
5. **Two classifiers change when the config variable is absent** — `.bemyagent/work/21/21.1/certificate.py:26` becomes broader (the N1 family, already waiting for the user), `.bemyagent/work/21/21.2/verify_census.py:239` narrower. A census or certificate rerun from a shell without the variable would count differently and say nothing.
6. **Closed-round launchers follow the shell too** — `.bemyagent/work/20/20.11/launch.sh:15`, `.bemyagent/work/20/20.12/launch.sh:14`; `20.11/01_think.md:36–37` still says "pinned to `<claude-config>`". True at the level of the placeholder; never to be rerun.
7. **One variable, two folders** — `.bemyagent/work/21/21.1/cert_on_2011.py:5,21`: needs `BMA_SCRATCH` = the closed rounds' scratchpad, the opposite of what `local.env` sets for everything else in that folder; then its temp copy lands there. Stops cleanly with the wrong value. Not run.
8. **`local.env` and the session scratchpad** — `local.env:1` overrides a `BMA_SCRATCH` the caller exported, and holds a session-specific path: a new session or a reboot needs it edited by hand, and the seeded trees live under it.
9. **Empty variable** — the 62 Python uses of `os.environ["BMA_SCRATCH"]`: set-but-empty means the current directory, silently. The shell entry points stop.
10. **Line references moved** — the edits shifted lines in the 21.1 scripts, so `03e`/`03g` references are off: `certificate.py:24` (`NAMED`) is now `:26` (checked); by the hunk offsets `certificate.py` +2 below line 19, `launch.sh` +1, `check_pilot.sh` +1, `score.py` −1 below line 26 (not checked one by one). Friction for whoever fixes N1–N6.
11. **Numbers in the new text** — "three weeks" is 17 days (`harness/README.md:467`, `docs/05` last bullet before Known issues); "14 untracked" is 15 (`docs/06-implementation-plan.md:264`); "119 files" is 122 (`work/21/21.5/02_tasks.md:8`); the code-map row's path lacks `.bemyagent/` (`docs/03-code-map.md:38`).
12. **For the user to decide** — the 18 session ids kept in 10 files (three of them scripts, which stay bound to this machine's transcripts): trace or not.

## What I could not check

- The scripts of rounds 13–20 and `cert_on_2011.py` **running**: forbidden. Equivalence is established for the values they compute, and by reading that nothing else changed — not by their output.
- A real launch: not run, by design.
- The tool's folder-name rule beyond `/` and `-`: would need the config folder.
- That no identifying token outside my patterns exists: a search returning nothing proves the absence of what was searched.
- The git history and the ignored files (`.bemyagent/log/`, `.claude/settings.local.json`): out of scope here; they still hold the words.
- Whether the tree changed between my earlier reading of the diffs and the final re-run: the residue, parse, swap and equivalence commands were all repeated at the end and gave the same results.

---

## Re-check — 2026-11-12, after the repairs

Same verifier (claude-fable-5-2), same limits. The coordinating agent repaired findings 1, 2, 3, 4, 10 and 11; I changed nothing and re-ran my own commands on the tree as it stands now (433 files: tracked + untracked-not-ignored, this file included).

### Verdict after the repairs

**PASS_WITH_CAVEATS** — nothing blocks the commit any more. The trace of finding 1 is gone, the two quoted patterns read true again, the live launcher is pinned again through `local.env`. What remains is friction the user should know about (findings 5, 6, 7, 9, 12, and what is left of 4 and 8), listed at the end of this section.

### (a) Each repair is in place and reads true

| Finding | Line now | Judgement |
|---|---|---|
| 1 | `21.1/03g_apparatus_reverify.md:50` — `cat ~/.claude*/<profile>/projects/*/memory/*.md` | repaired; the case still says what it tested (a glob reaching another project's memory through a profile folder) |
| 2 | `21.1/03g_apparatus_reverify.md:87` — `(?:~\|\$HOME\|\$\{HOME\}\|<home>)/\.claude[^"\\\s]*` | repaired. Compared with `orig/`: the fourth alternative was the literal home path, now `<home>`; nothing else on the line differs except the placeholder of finding 3. **N1 is implementable as written again**: with `<home>` filled in, the pattern compiles and matches the four home-config spellings I probed (`~`, `$HOME`, `${HOME}`, absolute) and neither of two non-matches |
| 3 | `21.1/03g:56`, `:87` (two places), `21.1/03e_apparatus_verify.md:181`, `21.1/03_execute.log:68` — `<config-folder-name>` | repaired: the bare folder name now has a placeholder of its own (five places on these four lines; elsewhere only in 21.5's own log and in this file). `03e:181` is visibly a pattern with one fragment withheld, no longer a pattern that names a directory |
| 3, the line left alone | `20.11/03_execute.log:17` — `<claude-config>/projects/…` | **I agree with leaving it.** In `orig/` that line was the folder name followed by the profile and `/projects/…`, i.e. the config directory in relative form, not the bare name; `<claude-config>` is the right placeholder |
| 4, 8 | `21.1/local.env` (ignored), two lines | sourced in isolation under four caller environments: nothing set → the current session's scratchpad and the pinned profile; caller's `BMA_SCRATCH` set → **the caller's wins**; caller's `CLAUDE_CONFIG_DIR` set to something else → **overridden by the pin**; `BMA_SCRATCH` empty → filled. Both variables are exported to child processes. `R211_CFG` still goes in front in the launcher's own expression, as the dry-run needs |
| 4, comment | `21.1/launch.sh:23` — "pinned by `local.env`" | true while `local.env` exists |
| 10 | `21.1/03_execute.log:81`, entry [23] | states that `03e`/`03g` line numbers refer to the scripts before the edit, with the offsets (`certificate.py` +2, `launch.sh` +1, `check_pilot.sh` +1, `score.py` −1) and that the apparatus goes back to its verifier with N1–N6. Consistent with the hunks I measured |
| 11 | `harness/README.md:467` and `docs/05:528` — "seventeen days"; `docs/06:264` and `21.5/01_think.md:6` — "15 untracked"; `21.5/02_tasks.md:8` — "122 files"; `21.5/01_think.md:6` — "71 are scripts"; `docs/03-code-map.md:38` — path starts with `.bemyagent/` | all in place and equal to what I measured (first commit with the path 2026-10-26 → 17 days; 75 + 15 = 90; 122 copies in `orig/`; 65 + 6 = 71). No "three weeks" is left in the tree outside this file |

### (b) No new trace

Over the 433 files, `grep -a`: the four words, case-insensitive → **0 files**; in file names → 0; home-path shapes → 0; dashed project-key shapes → 0; uid temp folder → 0; URL-encoded and letter-split forms → 0; host names → 0; e-mail-shaped strings → 0.

**The profile word:** as a path component, after a slash, a dot, a tilde or a glob star → **0 lines** (was 1, finding 1). As a bare token, case-insensitive, and as a substring anywhere → 2 lines, both in one tracked file. **Correction to my first pass:** I wrote there that those two occurrences were the public repo owner's name. That was wrong — I had mixed them up with other lines I had judged. They are an ordinary technical term, the same letters by coincidence, saying nothing about the machine. **Not a trace.** I do not give the lines here, so that this file does not point at the word; the coordinator has them.

A consequence for the README's new closing rule (search also for the tool's profile name): on this machine that search will always return those two lines. A round's VERIFY has to expect them, or search for the word in path position only.

Ignored files that still hold the four words, unchanged: `.bemyagent/log/` (12), `21.1/local.env`, `.claude/settings.local.json`. `git check-ignore -v` on `local.env` → `.gitignore:23:local.env`; not tracked.

### (c) The repaired notes against `orig/` are still swap-only

`swapcheck.py` again over the 19 non-script files: **46 changed lines** (the 45 of the first pass plus `03g:50`), 40 reproduced by the table. The six that are not differ from the table's result **only by a placeholder name**: `<config-folder-name>` where the table has no entry (`03e:181`, `03g:56`, `03g:87`, `21.1/03_execute.log:68`), `<profile>` (`03g:50`), `<home>` (`03g:87`), and the relative-form line `20.11/03_execute.log:17`. `diff` of each repaired note against its `orig/` copy shows the same line numbers changed as before, plus `03g:50` and three appended lines in `21.1/03_execute.log` (entry [23]). No sentence of a closed record was reworded. The two other lines my comparator reports are the coordinator's own new text (`docs/05:528`, the README section), judged under (a).

### (d) Apparatus and trees

| Check | Command | Result |
|---|---|---|
| selftest | `bash .bemyagent/work/21/21.1/selftest.sh` | exit 0, 84 lines, 82 PASS, `0 mismatches`, stderr empty, `cmp` **identical** to `selftest_before.txt` |
| dry-run | `bash .bemyagent/work/21/21.1/dryrun.sh` | exit 0, 332 lines, stderr empty; same multiset of lines as `dryrun_before.txt` (uuids and stub ids masked) and as `03d_dryrun.txt` (paths masked too); 14 stub calls report `cfg_is_pinned=True`, none `False`; step 12: 0 and 0 |
| seeded trees | the `find … \| shasum \| shasum` of point 6, before and after both runs | `111b2ed91a9fae9f9a34b7654137d19dc53d81e5`, 250 files |
| parse | `py_compile` ×65, `bash -n` ×6 | 65 ok, 6 ok, no `__pycache__` in the repo |

### (e) `launch.sh` against `orig/`

`diff orig/…/21.1/launch.sh` against the tree: three hunks — line 23 (the comment, new), lines 39–41 (`HERE` moved up, the `local.env` line, the required `BMA_SCRATCH`), line 44 (the config expression). The last two are the ones judged in the first pass. Recomputing `diff -U0` for all 71 scripts and comparing with the first pass: the comment hunk is the **only** difference in any script.

### Still open, for the user

None of these blocks; none shows on this machine today.

1. `.bemyagent/work/21/21.1/launch.sh:44` — without `local.env` the launcher follows the caller's `CLAUDE_CONFIG_DIR`, then `~/.claude`, silently. With `local.env` it is pinned. (What is left of finding 4.)
2. `.bemyagent/work/21/21.1/certificate.py:26` and `.bemyagent/work/21/21.2/verify_census.py:239` — the two classifiers that change when the config variable is absent (finding 5; N1 family). Run directly, the Python scripts do not read `local.env`.
3. `.bemyagent/work/20/20.11/launch.sh:15`, `.bemyagent/work/20/20.12/launch.sh:14` — closed-round launchers follow the shell (finding 6).
4. `.bemyagent/work/21/21.1/cert_on_2011.py:5,21` — one variable for two folders (finding 7). Now that a caller's `BMA_SCRATCH` wins over `local.env`, exporting the closed rounds' scratchpad for this script and then starting a 21.1 shell entry point from the same shell would point the live round at the wrong folder — a stop for missing trees, by reading, not a wrong result.
5. `local.env:1` — holds a session-specific path; a new session or a reboot needs it edited by hand, and the seeded trees live under it (what is left of finding 8).
6. The 62 Python uses of `os.environ["BMA_SCRATCH"]` — set-but-empty means the current directory (finding 9). The shell entry points are now safe on this (empty is filled or stopped).
7. The 18 session ids in 10 files — trace or not is the user's call (finding 12).
8. Small: `harness/README.md` names four placeholders for notes; three more are now in use (`<profile>`, `<home>`, `<config-folder-name>`). `.bemyagent/work/21/21.5/01_think.md:15` says "89 files" where the inventory is 90.

### What the re-check could not establish

As before: no script of rounds 13–20 and no real launch was run; the history and the ignored files were not touched; a search returning nothing proves the absence of what was searched and nothing more — this re-check itself corrects one mistaken judgement of mine from the first pass, which is the measure of that limit.
