# 21.6 — VERIFY of the trial clone (step 5)

Verifier: an agent that built neither the table nor the trial clone. It held the artefacts and the criteria of `01_think.md` / `02_tasks.md`; the builder's table was opened only after the search was finished. Every number below comes from a command run during this check. Nothing was changed in the repo or in the trial clone; temporary files went to `<scratchpad>/v216/`.

## Verdict

**PASS_WITH_CAVEATS — cleared to apply to the repo**, under the conditions of F4, and with F1 put to the owner first (it is a ruling, not a defect of the rewrite).

The rewrite does what the plan asks: no trace by shape or by word in any blob, message or file name of the three ranges; nothing published moved; the range is the same history but for 131 lines in 82 blobs, every one of them a path turned into a placeholder; the tree of `main` is `47dc9bd17ff8ebf1583e209bd4f7484864b23198`.

## Findings

**F1 — prose that lets a reader derive the account word (owner's ruling).**
Input: the tip commit of `main` (1 commit of the range; 0 in the published history). What happened: 3 lines in 2 files (`docs/06-implementation-plan.md:265`, `work/21/21.5/04_verify.md:82` and `:177`) say which public commit field carries the account word. No table rule can see this: no path, no literal. What should happen: the owner decides whether that sentence may stand. Weight: low — the published tip already holds the home prefix itself in 2 files (measured, count only), so the sentence tells nothing that is not already public. Smallest fix if not wanted: reword the 3 lines in a new commit on top (the tip tree then changes, and criterion 4 is re-measured on the commit before it), or accept as is. The exact wording was handed to the caller outside the repo.

**F2 — two shell scripts of the history no longer parse.**
Input: `work/20/20.11/launch.sh` and `work/20/20.12/launch.sh` in 7 and 3 commits of the range (not in the tip, where both parse). What happened: an unquoted assignment whose value became an angle-bracket placeholder; `bash -n` fails on the first such line of each (2 lines per file). What should happen: per `01_think.md` pre-mortem 2 the scripts of older commits are records, not things to run — so this is accepted by the plan, but it is damage and is named. Smallest fix: none needed; if wanted, a table line that writes the placeholder quoted for these two assignments.

**F3 — the log names a tip that is not in the trial clone.**
Input: `03_execute.log` entry [4]. What happened: it gives a new tip hash for `main` that does not exist as an object in the trial clone; the clone's `main` is `0ef8e31`, `bma/21.4` is `77b0f00`, the new tag object is `5c8a130` on commit `cb6c4bc`. What should happen: the log states the hashes of the clone that was verified. Smallest fix: correct the entry; apply only if the trial still shows these four hashes.

**F4 — the trial clone still reaches the old history; the apply step must be exact.**
Input: the trial clone's refs. What happened: `refs/remotes/origin/HEAD`, `origin/main`, `origin/bma/21.4` each reach all 42 old commits; the old tag object is present (unreachable, 1 object); reflogs exist for 5 refs; no `refs/original`, no replace refs, no notes, no stash. What should happen: the repo takes exactly three refs by explicit refspec (`refs/heads/main`, `refs/heads/bma/21.4`, `refs/tags/3.4.0`) and nothing else. Three things to hold: (a) the tag must be moved with force — a plain fetch does not replace an existing tag, and the old tag object, if left, would carry 38 old commits out with any push of tags; (b) both branches are checked out (repo and worktree), so the move is `update-ref` after fetching to a temporary ref, not a fetch onto the branch; (c) after the move, `git for-each-ref --contains` for an old commit must list no ref before anything is pushed. Measured for (a)–(c): the three clean refs reach 1511 objects, 0 of the 82 old blobs that held a trace, and 1 commit in common with the old range — the first commit after the published tip, which the rewrite left identical because nothing in it needed replacing (legitimate).

**F5 — table: sufficient for this range, not a general tool.** See check 7.

## Evidence per check

### 1. Own search
Scope: `git rev-list --objects main bma/21.4 3.4.0 --not published` → 484 blobs, 43 commits, 1 tag object, 300 trees; every blob dumped and read as bytes (binary-safe; `file --mime-encoding`: 410 utf-8, 74 us-ascii, 0 binary); the 43 commit objects and the tag object raw, headers included; every path of every tree of the 43 commits (554 distinct, 0 non-ASCII). Same dump on the repo's range (496 blobs) as the positive control of the procedure.

30 patterns, case-insensitive, each proven on a control string that holds it (30 of 30 match; 0 match a neutral line). Hits = matches, trial / repo:

| Pattern (shape) | Trial | Repo (control) | Surviving class → trace? |
|---|---|---|---|
| home prefix, any unix OS, followed by a name | 0 | 55 | — |
| platform users-folder word + any separator + name | 1 | 143 | prose "users-f…older" in a description of shapes — no |
| Windows home | 0 | 0 | — |
| JSON-escaped slashes before a path root | 0 | 0 | — |
| `~` or `$HOME` + dot-folder | 107 | 107 | 3 distinct, all generic tool folders — no |
| tool-config dot-folder with any suffix | 64 | 73 | 1 distinct, the generic one — no |
| project-key shape (dash, root word, dash) | 5 | 84 | `-private-tmp-` inside code that tests for that shape and an elided example — no |
| `/private/tmp`, `/private/var` | 23 | 101 | bare prefixes in code and prose that normalise spellings — no |
| `/tmp/<name>` | 5 | 82 | `/tmp/...` elided, 2 file names of a probe — no |
| `/var/folders/<id>` | 0 | 0 | — |
| uid-bearing folder name | 0 | 77 | — |
| the uid as a number | 0 | 77 | — |
| host-like names | 25 | 25 | `Path.home`, `settings.local`, the word "hostname" in prose — no |
| mail addresses | 87 | 87 | all 87 in author/committer/tagger lines, 1 distinct = the commit identity — no |
| account word, substring, any case | 174 | 307 | 174 = 87 header lines × 2 (name + mail); 0 in message bodies, 0 in blobs, 0 in paths — no |
| account word, lower case only | 87 | 220 | the 87 mail occurrences of the identity — no |
| account word with a separator between letters | 174 | 307 | same 174 |
| account word reversed | 0 | 0 | — |
| profile folder, other profile names, owner's name outside the identity | 87 | 105 | the 87 are inside the identity mail — no |
| folder layout above the repo | 0 | 127 | — |
| names of the owner's other projects (16 names taken from the machine) | 36 | 36 | 36 × the word "revision" (substring of one name); 0 as a whole word — no |
| base64 of home prefix / account word / key prefix, 3 alignments | 0 | 0 | proven on control only |
| URL-encoded path roots | 0 | 0 | proven on control only |
| bare uuid | 68 | 124 | 18 distinct session ids — not a trace by the designer's ruling |
| uuid touching a path separator or extension | 47 | 91 | see below |
| the word "scratchpad" | 444 | 473 | generic word; 0 with a real path before it |
| IPv4, MAC address, OS version / architecture | 0 | 0 | — |
| user-environment words | 111 | 111 | `whoami` (a protocol word), `first_user=` — no |
| runs of base64 ≥ 80 chars, hex > 40 | 0 | 0 | nothing encoded to decode |
| placeholder glued to a word character | 0 | — | no replacement fired inside a word |

Uuid inside a path (reported as asked): 35 lines in older commits where one session id stands between placeholders (`<tmp>/<project-key>/…<id>/scratchpad|tasks`, 33; `<claude-config>/projects/<project-key>/<id>/subagents`, 2). Every other part of those paths is a placeholder, so the id stands with no identifying neighbour. 0 such lines in the tip tree, where 34 lines in 10 files hold bare ids or `<id>.jsonl` basenames.

Not in the owner's definition, named for completeness: a time-zone name (3) and two zone abbreviations (2); the worktree folder name `bemyagent-task-21.4` (13) — the shape the published rules §8 prescribe.

### 2. Nothing published changed
`published` = the repo's `origin/main` = `ccc23dd0f1bc7ba428137ef5cd0e10f92ba2aeff`; `merge-base --is-ancestor published main` and `… bma/21.4` → 0. `git tag --merged` gives the same 19 names in both; 19 of 19 resolve to the same tag object and the same commit. `git rev-list` of the published tip: 72 commits, the same checksum of the list in both.

### 3. Same history
`rev-list --count published..main` = 42, 0 merges. `git log --reverse --date=raw` with subject, body, author and committer name, mail and date, NUL-separated, over the 42: byte-identical between repo and trial (44244 bytes, `cmp`). Raw commit objects minus `tree`/`parent` lines over the 43 (the branch included): same checksum; headers are only tree, parent, author, committer (no signature, no extra header). `bma/21.4^` = `main~1` in the trial; its metadata checksum equals the repo's; its diff against `main~1` names the same 2 files in both. `3.4.0`: type `tag` in both; the two tag objects differ in 1 line, the `object` line; the target is commit 38 of 42 in both. 0 commit or tag messages changed.

### 4. Trees
`main^{tree}` in the trial = `47dc9bd17ff8ebf1583e209bd4f7484864b23198`.
43 commit pairs by position, `ls-tree -r` of each: path sets equal in 43; 0 mode or type changes; differing files per commit rise from 0 (first commit) to 71 (`main~1` and the branch), 0 at the tip; 41 commits have at least one. Distinct blob pairs that differ: 82 (71 paths: 56 `.py`, 14 `.md`, 4 `.txt`, 3 `.json`, 3 `.log`, 2 `.sh`), each old blob mapping to exactly one new blob; 0 binary; line counts and final newline equal in all 82.
Differing lines: 131. For each, the trial line was split at its placeholders and matched against the repo line: 131 of 131 match with every captured piece made only of path characters; 0 lines differ in anything else. The pieces replaced reduce to 5 path strings (repo path, scratchpad path, temp root with project key, project key alone, tool-config profile folder in full and in bare form), 169 placeholder occurrences in all.

### 5. Damage
JSON: 3 of 3 changed `.json` parse (as before). Python: 56 of 56 changed `.py` compile (in memory, no cache folder written; 0 `__pycache__` created in either tree). Shell: 0 of 2 changed `.sh` pass `bash -n` (both passed before) — F2. Replacement inside an unrelated word: 0.

### 6. Leftovers in the trial clone
26 refs. Reaching old commits: the 3 `refs/remotes/origin/*`. Old tag object: present, unreachable. `refs/original`: none. Replace refs: 0. Reflogs: 5 files. `ORIG_HEAD` = the new tip. The remote `origin` is still configured. See F4.

### 7. The table (read after the search)
13 literal rules, longest first; the order is right (no shorter rule can pre-empt a longer one).
- Too narrow as a general tool, sufficient here: every rule is a case-sensitive literal built on full paths. There is no rule for the account word alone, the layout folder alone, the uid-bearing folder name alone, or the profile folder without its profile. My shape search shows none of those stands alone in this range (0 hits each), so nothing was missed — but a new commit added before the apply step needs the search again, not just the table.
- Two rules never fired in this range (the ones giving `<base>` and `<home>`); harmless.
- Too wide at one edge: the rule giving `<repo>` has no right boundary and would also fire on a sibling folder whose name starts with the repo folder's name (the worktree, the trial clone, the bundle). It did not happen (0 placeholders glued to a following character), noted for a re-run.
- One scratchpad rule is tied to a single session id; a scratchpad of another session would fall to the shorter rule and still come out clean.
- The table cannot see F1, by construction.

## Not established
- The uncommitted state of the repo (16 entries in `git status`), the worktree of `bma/21.4`, and the bundle were not searched: only committed objects of the three ranges.
- The state of the repo after the apply step (step 7 repeats the search there).
- Encodings other than base64, URL-encoding and escaped slashes (none was indicated: no binary blob, no long encoded run).
- A token nobody thought of. The word lists (other projects, profiles) were taken from the machine's folders as they are today; a project or profile that no longer exists there is not covered.
- Whether the Python scripts of older commits still run: they compile; their paths are now placeholders, which the plan accepts.
- Whether the time-zone name and the session ids are acceptable to publish: outside the definition given, left to the owner.

---

# After apply (step 7)

Same verifier, same 30 patterns (control re-run: 30 of 30), on the repo after the three refs were moved. Read-only; nothing expired, nothing pruned.

## Verdict

**The unpushed part may be pushed** — `main` and tag `3.4.0`, as they stand now (`0ef8e31`, tag object `5c8a130`). What a push would send holds no trace by the owner's definition. Open as before: F1 (owner's ruling, low weight). Two things to hold: push the two refs by name (not `--all`, not `--mirror`), and A2 below if the worktree branch is ever pushed.

## Findings

**A1 — old objects are still in the repo, held by reflogs.** Expected at this point; none is reachable from a ref and none would be pushed. Commands and target state under check 4.

**A2 — four published blobs with traces stay in every commit below the tip.** Input: the full trees (not only the new objects) of `main` and `bma/21.4`. What happened: 4 files (`work/15/15.10/` and `work/16/16.1/`, `setup.py` and `score.py` in each) carry the home prefix, the layout, the uid-bearing folder and a project key (6 account-word hits in all). They are byte-identical to blobs already in the published history, which the owner decided not to touch; the tip of `main` has them cleaned; `bma/21.4` (and its worktree folder, 390 files, clean against its commit) still has them. What should happen: nothing for this push — it sends no new copy of them. Named so that nobody reads "0 hits in the range" as "0 hits in the tree of every commit".

**A3 — published tag objects carry a second tagger identity.** 15 annotated tag objects other than `3.4.0` are reachable from refs and not from the published commit: all 15 are published tags, identical to the bundle. 8 carry the commit identity, 7 another name and mail. Already public and unchanged; not in the push set. Outside this task; named because check 1 asked for every ref.

## Evidence

### 1. Every ref, not the published tip
23 refs (3 branches/remote, 20 tags); no stash, no notes, no replace refs; `refs/original` and a temporary ref folder exist as empty directories (0 files, 0 packed entries). `rev-list --objects --all --not origin/main`: 843 objects — 484 blobs, 43 commits, 300 trees, 16 tag objects; 554 tree paths. The blobs, commits, trees and the `3.4.0` tag object are the set verified in the trial clone; the scan gives the same counts as there for all 30 patterns except in tag objects (A3): mail 102 = 87 + 15 taggers; account word 190 = 174 + 8 taggers × 2; 0 in any tag message body, 0 in blobs, 0 in paths. Home prefix 0, project key 5 (generic, as before), uid-bearing name 0, layout 0, encoded forms 0.

### 2. Refs and the old history
`for-each-ref --contains` → 0 refs for the old tip, 0 for the old `main~1`, 0 for the old tag's commit, 0 for the old branch commit, and 0 summed over all 42 old commits that received a new hash. `origin/main` = `ccc23dd`. `main` `0ef8e31`, `bma/21.4` `77b0f00`, `3.4.0` tag object `5c8a130` → commit `cb6c4bc`; `main^{tree}` = `47dc9bd17ff8ebf1583e209bd4f7484864b23198`. Bundle `list-heads`: 25 entries; 19 of 19 published tags resolve in the repo to the object the bundle records; the bundle holds the old values of the three moved refs.

### 3. What a push would send
`rev-list --objects origin/main..main` = 821 objects, plus the tag object = 822: 482 blobs, 42 commits, 297 trees, 1 tag. Scan of exactly that set: home prefix 0; project-key shape 5 (generic); `/private/tmp`-style bare prefixes 23; uid-bearing name 0; uid 0; layout 0; other projects 0 as a word; base64 / URL-encoded 0; mail 85, 1 distinct, all in the 42 × 2 + 1 identity lines; account word 170, all in those same lines; bare session ids 68 (18 distinct), 47 touching a separator; tree paths 0 hits. The branch `bma/21.4` adds 1 commit and 21 objects if pushed, with the same result.

### 4. What still holds old objects locally
- Reflogs naming old commits: `logs/HEAD` (43 of 60 lines), `logs/refs/heads/main` (43 of 60), `logs/refs/heads/bma/21.4` (3 of 3), the worktree's `logs/HEAD` (3 of 4). `logs/refs/remotes/origin/main`: 0.
- `fsck --unreachable --no-reflogs`: 357 objects (56 commits, 84 blobs, 207 trees, 10 tag objects). With reflogs counted as roots: 11 (10 tag objects, 1 blob) — so the reflogs are what keeps the rest.
- `ORIG_HEAD` of the repo names an object that does not exist; `FETCH_HEAD` and the worktree's `ORIG_HEAD` name new objects only. `FETCH_HEAD` holds a local path (a file of `.git`, never pushed).
- Outside the repo: the bundle (the intended backup, holds the old history) and the trial clone.

Commands, not run:
```
git -C <repo> reflog expire --expire=now --expire-unreachable=now --all
git -C <repo> gc --prune=now
```
(`--all` covers the worktree's reflog; `gc` is needed, not `prune` alone, because old objects sit in packs.) True afterwards:
- `git -C <repo> fsck --unreachable --no-reflogs` prints nothing;
- `git -C <repo> cat-file -e <old>` fails for the old tip, the old branch commit and the old tag object;
- `git -C <repo> cat-file --batch-all-objects --batch-check | wc -l` equals `git -C <repo> rev-list --objects --all | sort -u | wc -l` plus what index and worktree index hold alone;
- the four refs of check 2, `git status` in the repo (16 entries) and in the worktree (0) are as before;
- the pattern search over `--batch-all-objects` finds only the A2 blobs.
After that the bundle is the only copy of the old history: keep it outside the repo, remove the trial clone.

### 5. Uncommitted state and the worktree folder
Repo: 16 `status` entries = 14 modified, 2 untracked entries holding 5 files; 19 files scanned (text, 0 binary): home prefix 0, project key 1 (generic), uid 0, account word 0, layout 0, profiles 0, mail 0, session ids 0, encoded 0; survivors are the generic classes of the table in check 1 above (bare temp prefixes 8, generic tool folder 7, the word "scratchpad" 26). 31 ignored files exist and were not scanned (they are not committed).
Worktree folder: 390 files, all tracked, `status` empty, HEAD `77b0f00`: hits only in the 4 files of A2 (each equal to its committed, published blob); elsewhere home prefix 0, account word 0.

## Not established (after apply)
- The remote itself: what it holds was not fetched or compared; `origin/main` is the local record of it.
- The 31 ignored files, the bundle's content, the tool's own folders outside the repo.
- The state after expire and prune (the commands were not run).
- F1 and F3 of the first part are unchanged by the apply step.
