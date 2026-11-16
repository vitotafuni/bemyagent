# 21.7 — TASK

**Delivers:** §8's `git worktree add ../bemyagent-task-X.Y -b bma/X.Y`, run from the repo, creates the task worktree inside the project's base folder — and a session started at the base still restores from the rules.

## Checklist
| # | Step | Status |
|---|---|---|
| 1 | Collision scan: no `src` at the base; record the before-values (manifest, git fingerprints, trees' hash) in the scratchpad `p217/` | done |
| 2 | Tarball of the whole base into `p217/` | done |
| 3 | `mkdir src`; one command moves every entry except the settings folder and `src`; manifest after, before any git command | done |
| 4 | Base instruction file (unversioned pointer + the read instruction with the `src/` prefix); hook path in the tool's local settings | done |
| 5 | Checks 3–8 of the verification plan, by the author, logged | done |
| 6 | `06` (row, Resume), `05`, `03`, `harness/README.md`, the draft, tool memory | done |
| 7 | Independent VERIFY (Sonnet, artifacts and criteria only) → `04_verify.md` | verified — PASS_WITH_CAVEATS, nothing blocking; its four caveats and the line-count note answered in `03_execute.log` [8]; a second independent agent re-checked the answers on 2026-11-15 (`04_verify.md`, last section; `03_execute.log` [9]) |
| 8 | Demo: the 21.4 worktree, created with §8's command, sits in the base | done — `<base>/bemyagent-task-21.4` |
| 9 | After the user's next message: the base holds no re-created `.bemyagent/`; if it does, fold the log file into `src/` | part — the hook has fired after the move (the day's log file went from 5 entries in the tarball to 8, counted by heading) and wrote under `src/` each time; the base holds no `.bemyagent/` on 2026-11-15. The user's own next message has not come yet: one `ls` then |

## CDM
- 🎯 **Drift**: editing round scripts or rules text to suit the new layout; touching the folder above the base; committing or pushing as part of the move.
- ✅ **Validation**: manifest before = after (every file, `.git` included); git fingerprints equal; sync check equal; 21.1 selftest 82 PASS / 0 mismatches and the dry-run's verdict lines unchanged; trees' hash `111b2ed9…`; residue 0 in what the task adds; the worktree path starts with the base.
- 🔄 **Pivot**: manifest differs, or git reports anything it did not report before → stop, restore from the tarball, re-read approach C. More than two obstacles → same.
