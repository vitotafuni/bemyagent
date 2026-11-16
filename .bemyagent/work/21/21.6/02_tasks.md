# 21.6 — TASK

**Delivers:** the unpushed history of `main` can be pushed: no commit of it describes the machine it was written on, and nothing already published has changed.

## Checklist
| # | Step | Status |
|---|---|---|
| 1 | `04-tech-stack.md` gets `git-filter-repo`; `brew install git-filter-repo` (the user's grant, 2026-11-16) | done — 2.47.0 |
| 2 | Backup: `git bundle create <base>/bemyagent-before-21.6.bundle --all`, `git bundle verify`; the four refs and the tree of `main` written in `03_execute.log` | done — verified "is okay", 25 refs |
| 3 | Inventory of the strings in `origin/main..main`, `..bma/21.4`, `..3.4.0` (blobs and messages), by word and by shape → the table `literal → placeholder`, longest first, in `<base>/21.6-table.txt` (outside the repo). By a Sonnet agent; counts only in the log | done — 13 lines (`03_execute.log` [3]) |
| 4 | Trial: `git clone --no-local <repo> <base>/src-21.6-trial` with `origin/main` kept as a ref; `git filter-repo --replace-text <table> --replace-message <table> --refs origin/main..main origin/main..bma/21.4 3.4.0 --force` (the exact form is the builder's to settle on the trial, never on `src`) | done — on the trial clone (`03_execute.log` [4]; its tip hash corrected in [6]) |
| 5 | Independent VERIFY of the trial clone (the list of `01_think.md`) → `04_verify.md` | verified — PASS_WITH_CAVEATS, cleared to apply (`04_verify.md`) |
| 6 | On PASS only: `src` fetches the three refs from the trial clone and moves them; `git status` clean in `src` (but for this task's own files) and, after `reset --hard`, in the worktree | done — `main` `0ef8e31`, `bma/21.4` `77b0f00`, tag object `5c8a130` (`03_execute.log` [7]) |
| 7 | The verifier repeats its search on `src`; then reflogs expired, unreachable objects pruned; the trial clone removed | verified — "the unpushed part may be pushed" (`04_verify.md`, *After apply*); reflogs expired, pruned, 0 unreachable, the old objects gone; trial clone removed |
| 8 | `05` (the issue closed for the unpushed part), `06`; the summary of what would be pushed goes to the user — the push is theirs | part — `05`, `06` written for both passes; the summary is with the user; the push is theirs |
| 9 | **Second pass — session references** (the user, 2026-11-16: the three lines of prose stay, the author identity stays, the session ids go). Inventory of real session ids, their short forms and agent ids in `origin/main..main`, `..bma/21.4`, `..3.4.0`; table outside the repo; trial clone; `git filter-repo` as in step 4. The last tree changes this time: check 4 becomes "every differing line differs only by an id turned into a placeholder" | done — third clone: 254 table lines (16 full session ids, 12 short forms, 190 agent ids, 36 cut agent ids); the second clone failed the check on 31 cut agent ids and was thrown away |
| 10 | Independent VERIFY of the second trial (the same verifier, its patterns plus the id shapes) → `04_verify.md`, a new section | verified — second clone FAIL (31 cut agent ids left), third clone **PASS**, cleared to apply (`04_verify.md`, *Second pass*) |
| 11 | Apply as step 6, then `reset --hard` in `src` (clean before) and in the worktree; verifier's search on `src`; expire and prune; bundles and tables stay outside the repo | verified — applied (`main` `344cb22`, `bma/21.4` `0801b06`, tag object `bbd2156`), both trees reset and clean; the verifier on `src`: "may be pushed"; reflogs expired, pruned, 0 unreachable, old objects gone; clone removed |

## CDM
- 🎯 **Drift**: touching a published commit or tag; running the tool on `src` before the trial is cleared; writing a string of the table into a file of the repo; pruning before the verifier's PASS.
- ✅ **Validation**: the verifier's own search finds nothing in the three ranges; `origin/main` is `ccc23dd` and an ancestor of `main`; `main^{tree}` is the tree it was; 42 commits with the same subjects, authors and dates; `3.4.0` annotated; the 19 published tags resolve as before.
- 🔄 **Pivot**: the table cannot be made complete or breaks the tree after two tries → stop; approach C (one clean commit) goes to the user as a question.
