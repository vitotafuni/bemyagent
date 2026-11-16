# 21.7 — THINK

## Context
Rules §8 create a task worktree with `git worktree add ../project-task-X.Y`. With the repo at the top of the folder the session starts in, `../` is the folder above — outside the project, where an agent has no business listing or writing. The user's ruling (2026-11-12, `docs/drafts/change-under-test.md`): everything, `.git` included, moves into `src/`; the present folder becomes the **base**; §8 stays as written. On 2026-11-14 the user settled the one open point — sessions start at the **base** — and asked for the move now, before the candidate branch `bma/21.4` is cut.

The move is requested while milestone 21 is uncommitted (84 status lines, HEAD `668274f`) and before 21.6. Neither blocks it: a move of the folder that holds `.git` changes no git object and no path relative to the repo root.

### Context Saturation Check
- [x] **Target files/paths** — every top-level entry of the base except the tool's local settings folder: `.bemyagent .git .github .gitignore AGENTS.md BEMYAGENT.md CNAME harness LICENSE README.md site` (listed 2026-11-14; `src` does not exist — no collision).
- [x] **Expected behavior** — after the move `<base>` holds the settings folder, `src/` and one unversioned instruction file; `git -C src status` is what it was; `../bemyagent-task-X.Y` from `src/` lands inside `<base>`.
- [x] **Constraints** — §7 (atomic, collision scan); no machine trace in any repo file (`harness/README.md`, last section); the ten seeded trees of 21.1 untouched; no real `claude` launch; nothing committed without the user (autoCommit false), nothing pushed.
- [x] **Dependencies** — none new. What names the repo by absolute path, measured: one hook command in the tool's local settings (the conversation-log writer). Git has no hooks, no extra worktree, no absolute `gitdir`. 21.1's `local.env` names the scratch and the config folder, not the repo.

## Approaches Considered
- **A — move inside the base**: `mkdir src`, then one command that moves *every entry except* the settings folder and `src` itself. The exclusion is the list, so nothing can be forgotten; the session's working directory stays valid; the tool's project key (derived from the folder the session starts in) and its memory stay where they are.
- **B — rename the base and nest it**: rename `<base>` → temporary name, recreate `<base>`, move the old folder in as `src`, move the settings folder back out. Atomic in the strictest sense, but it works in the folder above the project (the thing this task exists to stop), and it pulls the running session's working directory out from under it.
- **C — fresh clone into `src/` + copy the changes**: loses what git does not carry — ignored drafts, the conversation log, `local.env`, `.git/bma-backup/`, the local tag unless pushed by hand. More steps, more ways to drop something.

## Selected Approach & Risks
**A.** Estimated cost: low (one move, a dozen checks). Content edits: the base instruction file (new, outside the repo), one path in the tool's local settings, `06`, `05`, `03`, `harness/README.md` (one sentence), the draft.

**Pre-mortem**
1. *Something stays behind or goes missing.* → manifest (path + sha1 of every file, `.git` included) taken immediately before the move and again immediately after, before any git command; the two must be equal. A tarball of the whole base goes to the scratchpad first.
2. *The session can no longer find its rules.* The tool loads the instruction file of the folder it starts in; after the move that folder has none. → the base gets an unversioned file that points at `src/` and carries the read instruction with the `src/` prefix; it says it is a pointer, so §1 does not register a second sentinel there.
3. *The conversation-log hook recreates `<base>/.bemyagent/log/`.* Its command names the old path, and the tool may keep the hook it loaded at session start. → path updated in the settings file; after the user's next message, check the base for a re-created folder and fold the day's file into `src/.bemyagent/log/`.
4. *A live round's script silently changes meaning.* Scripts find the repo from their own location, so `ROOT` becomes `<base>/src`. For 21.1 this touches one check: `certificate.py` counts tool calls that name the repo's path; a call naming the base outside `src/` is no longer counted *(corrected after VERIFY — this line first named the instruction-record check, which compares with the arm's own directory and is unaffected)*. Arms run in scratchpad trees, so the count is a second line of defence — recorded as N7 for the reader fixes 21.1 already owes, not edited here (surgical scope). Closed rounds that read transcripts by project key (21.2) need `BMA_REPO=<base>`: that is what the variable is for.

**Devil's Advocate** — do not move anything: change §8 to `git worktree add .worktrees/project-task-X.Y` and ignore the folder. One line, no layout change. Not taken: the user ruled it out on 2026-11-12 (a worktree inside the repo it belongs to is seen by every search and every `find` of the main tree), and §8 is released text — changing it is a protocol change to test, the move is not.

**What the move costs, known now**: the tool reports the base as *not a git repository*, so its own worktree features do not apply at the base; git commands need `-C src` or a `cd`. Sessions dispatched into a task worktree start inside a checkout and see none of this.

## Verification Plan
Independent agent (Sonnet — the checks are comparisons against stored fingerprints with explicit criteria; no judgement to anchor), holding the criteria of `02_tasks.md` and the before-files in the scratchpad:
1. base listing is exactly settings folder, instruction file, `src`;
2. manifest before = manifest after;
3. `git -C src`: HEAD, status fingerprint, diff fingerprint, tag count, stash count, ignored list, worktree list — equal to the recorded values;
4. sync check: the rules embedded in `BEMYAGENT.md` equal `00-ai-rules.md`, 107 lines, eight sections;
5. 21.1 `selftest.sh` and `dryrun.sh` (stub only) — same verdict lines as before the move;
6. the ten seeded trees' hash unchanged;
7. no machine trace in what this task adds;
8. the instruction the base file gives resolves to an existing file; the hook's path resolves under `src/`;
9. §8's command, run from `src/`, creates the worktree inside the base.
