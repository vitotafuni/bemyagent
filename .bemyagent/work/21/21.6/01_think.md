# 21.6 — THINK

## Context
The unpushed part of `main` holds, in the blobs of its commits, strings that describe the machine the repo is written on (`05`, the issue of 2026-11-12). The working tree was cleaned by hand and committed (`0825c49`, 2026-11-16): the last tree is clean, the commits before it are not. Nothing may be pushed until they are. The user's decisions: the published history is not touched (2026-11-14, `drafts/history-rewrite.md`, option 3); the tool is `git filter-repo`, installed by the agent (2026-11-16).

State measured 2026-11-16, before anything: `origin/main` `ccc23dd`; `main` `0825c49`, 42 commits ahead, linear, no merge; annotated tag `3.4.0` on `0df8e6d`, inside the range; `bma/21.4` `46f4621`, one commit on `main~1`, checked out in the worktree `<base>/bemyagent-task-21.4`.

### Context Saturation Check
- [x] **Target** — the refs `main`, `bma/21.4`, `3.4.0`, over the range `origin/main..`; nothing published.
- [x] **Expected behaviour** — no commit of the range holds a residue word in a blob or in its message; `origin/main` and everything before it keep their hashes; the tree of `main` is the same tree as before (it is already clean, so the table changes nothing in it); authors, dates, messages and the number of commits are kept.
- [x] **Constraints** — the replacement table holds the strings themselves, so it lives outside the repo; no push by the agent; a backup first; the check by an agent that did not do the rewrite.
- [ ] **Dependencies** — one unknown: the full list of strings in the range. The table of 2026-11-12 was lost with the session's temporary folder. **Assumption: it can be rebuilt from the range itself** — the inventory is step 3 and the verifier searches by shape (home prefixes, temporary prefixes, key-like folder names), not only by the list.

## Approaches Considered
- **A — `git filter-repo --replace-text --replace-message --refs`, on a trial clone, then move the refs of `src` to the result.** The trial clone is checked whole before `src` changes; in `src` only three refs move, and since the tree of `main` is the same the working tree and the index stay valid.
- **B — the same, run in place in `src`.** One step fewer, but the first run is the real one, and `src` has a second worktree.
- **C — squash the 42 commits into one clean commit.** No tool at all and nothing to get wrong in a table; loses 42 commit messages and leaves `3.4.0` without a commit of its own. Not what the user chose; named because it is the fallback if the table cannot be made right.
- **D — `git filter-branch`.** Turned down by the user with the comparison in view.

## Selected Approach & Risks
**A.**

**Pre-mortem**
1. *The table misses a string.* → the inventory is built from the range by words and by shapes; the verifier does its own search by shape on every blob of the rewritten range, with its list proven on a positive control; a miss sends the table back, the trial clone is thrown away and made again.
2. *A replacement breaks a file* (a short word replaced inside another word; a script that needs the real path). → longest strings first, no bare short word without its context; the tree of `main` must come out identical, and for the commits before it the scripts are records, not things to run.
3. *The published part changes.* → `--refs origin/main..` limits; checked: `origin/main` is the same hash and an ancestor of the new `main`, and the 19 published tags resolve as before.
4. *The old commits stay reachable in `src`* (reflog, the old tag object) and go out with a push. A push sends only what the pushed refs reach; still → after the refs move, reflogs are expired and unreachable objects pruned, once the verifier has cleared the result. The bundle in the base is then the only copy of the old history.
5. *The worktree of `bma/21.4` is left pointing at a tree that no longer matches its branch.* → it is clean now; after its ref moves, `git -C <worktree> reset --hard`, then `git status` clean in both.

**Devil's advocate** — C: one commit, no table, nothing to verify but one tree. Cheaper and safer. Not taken because the user asked for the history to be kept and chose the tool; kept as the fallback of risk 1.

## Verification Plan
An agent that built neither the table nor the trial clone (strongest tier: a miss is published for good) checks, on the trial clone and again on `src` after the refs move: no residue by its own list and by shape in any blob or message of `origin/main..main`, `..bma/21.4`, `..3.4.0`; `origin/main` unchanged and an ancestor; 42 commits, same authors, dates and subjects in order; `main^{tree}` equal to `47dc9bd…`; the tag annotated, same tagger and message; the 19 published tags unchanged.
