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

# Second pass — session references

Same verifier as the first pass; it built neither the tables nor the clones, and opened the table only after its own search. Read-only on the repo and on the clones. Ids are never quoted here: counts and file names only. Two clones were checked: the second trial clone failed (part B, kept as measured), the third, corrected, passed (part A).

## A. Third trial clone — verdict

**PASS — cleared to apply to the repo.** No real session reference is left in any new object of the three ranges; the two findings of part B that asked for a change (S1, S2) are answered; S3 is information for the owner, not a defect of the rewrite. Hashes verified in the clone: `main` `344cb2264954824998ed1fed7122876c98aface0`, `bma/21.4` `0801b06c83e6f973722a4c0e6eecee5c839ca863`, tag object `bbd2156d5dc6d313ab059efda20357e1caf48136` on commit `0a11ec550726a09c91e288b2936a9be16eb6067c`, `main^{tree}` `a00eee76d9612158870d9be70429256ca724f14a`.

### What changed against part B
- **S1 answered.** `work/20/20.10/03b_census.txt`: 31 lines differ, each by one cut agent id turned into `<agent-id>`; cut agent ids that prefix one on disk: 0 (were 31).
- **S2 answered.** The two dry-run files are the same objects as in the repo, in the tip and in every commit (0 lines of them among the differing lines). Their stub values stay as they were: 3 uuid-shaped strings (2 distinct) in `work/21/21.1/03d_dryrun.txt` and 16 `resumed_from=` short forms in the two files — synthetic, drawn by the stub's `uuid4`, none on disk.
- **S3 stands** as written in part B: 12 `.py` files of the tip (27 paths over the range) lose id constants; all compile; none re-runs as it stands.

### Evidence (same commands as part B, run again on the third clone)
1. **Session references.** Lists rebuilt from the names on disk: 73 session ids, 339 agent ids. Control: 16 of 16 patterns hit. Set: 508 blobs (0 binary), 45 commit objects, the tag object, 561 tree paths. Hits in the clone: any uuid shape 3 (the stub ones, 1 file); uuid on disk 0; other separators, 32 hex, upper case 0; real id as a hex stream 0; two groups 0; 8-hex prefix of a real id 0; first 8 hex of a real id anywhere 0; full agent id 0; cut agent id prefixing one on disk **0**; `agent-` + hex 0; tree paths 0; messages 0. Placeholders: 88 `<session-id>`, 392 `<agent-id>`.
   Letter + 7 hex tokens that are not agent ids: 6 occurrences of 4 distinct tokens in the new objects (5 in `work/21/21.4/03d_dryrun.txt`: stub `resumed_from=` values and one cut sha of a prompt; 1 cut tree hash in `work/21/21.1/03e_apparatus_verify.md`) — the same 6 as in the repo, untouched. Over the full trees, published blobs included, they are 7 occurrences of 5 distinct tokens: the seventh is in a published blob. That settles the two counts: 6 is the new objects, 7 is the full trees.
   Inherited blobs: over the full trees of the 45 commits (633 distinct blobs) the only real id is the same one, once in each of the 4 published blobs (`setup.py`, `score.py` of `work/15/15.10/` and `work/16/16.1/`), each an object of the published history, absent from the tip of `main`, present in `bma/21.4`.
2. **The 30 first-pass patterns.** Control 30 of 30. Same counts as the repo's range for 28; uuid 68 → 3 (the stub ones), uuid at a path separator 47 → 0. Home prefix, uid, layout, encoded forms 0; mail 91 and account word 182 in the 45 × 2 + 1 identity lines only.
3. **Published part.** `published` = `ccc23dd`, ancestor of `main`; 72 commits, same checksum of the list; 19 of 19 published tags resolve to the same object.
4. **Same history.** 44 commits, 0 merges; subject, body, names, mails, dates byte-identical (`cmp`, 44769 bytes); raw commit objects minus `tree`/`parent` lines: same checksum over the 45; the first 12 commits keep their hashes, 33 are new; `bma/21.4` on commit 41 of 44 in both, same metadata; `3.4.0` annotated, tag objects differ in the `object` line only, target commit 38 of 44 in both.
5. **Trees.** 45 commit pairs: path sets equal, 0 mode changes; 51 blob pairs differ (38 paths), one new blob per old one, line counts equal; 418 differing lines, every one explained by ids put back: full uuid 65, two groups 11, 8 hex 10, agent id of 17 characters 355, of 16: 5, of 10: 1, of 8: 31 — 478 ids, all on disk. Last tree: 23 files, 357 lines.
   Hex tokens of 7+ characters (decimal runs included; message bodies included): 926 before (350 distinct), 383 after (90 distinct); 543 removed, 0 added, 0 unexplained — they are exactly the hex groups of the 478 ids. (The builder's 349 → 91 comes from a slightly different way of cutting tokens; the statement that matters is the same in both: nothing added, nothing removed but ids.) None of the 478 prefixes any of the 1564 git objects of the repo; no commit hash, tree hash or checksum quoted in a file changed; 0 placeholders next to a hex character.
   Damage: 5 of 5 changed `.json` parse; 38 of 38 changed `.py` blobs compile; no `.sh` changed.
6. **Leftovers in the clone.** 23 refs, none reaches an old commit; no remote, no replace refs; 34 old commit and tag objects present, held by 4 reflog files; a stale `packed-refs` line for the old tag, overridden by the loose ref. A fetch by refspec carries none of it.

### Apply (the guards are the repo's values before the apply)
```
git -C <repo> status --porcelain                      # empty; same in <worktree>
git -C <repo> fetch --no-tags <trial> +refs/heads/main:refs/tmp216/main +refs/heads/bma/21.4:refs/tmp216/bma +refs/tags/3.4.0:refs/tmp216/tag
git -C <repo> rev-parse refs/tmp216/main refs/tmp216/bma refs/tmp216/tag
#   344cb2264954824998ed1fed7122876c98aface0
#   0801b06c83e6f973722a4c0e6eecee5c839ca863
#   bbd2156d5dc6d313ab059efda20357e1caf48136
git -C <repo> update-ref refs/heads/main     344cb2264954824998ed1fed7122876c98aface0 71e3bcf68d546ee7d62fe219de15964a733f108a
git -C <repo> update-ref refs/heads/bma/21.4 0801b06c83e6f973722a4c0e6eecee5c839ca863 77b0f009509cb8d7372ccaa2e3d61490cf9d6501
git -C <repo> update-ref refs/tags/3.4.0     bbd2156d5dc6d313ab059efda20357e1caf48136 5c8a130accda0c9ca563a9f6ddd97f9c5ca36f63
git -C <repo> update-ref -d refs/tmp216/main; git -C <repo> update-ref -d refs/tmp216/bma; git -C <repo> update-ref -d refs/tmp216/tag
git -C <repo> reset --hard
git -C <worktree> reset --hard
```
True afterwards: `status --porcelain` empty in both; `main^{tree}` = `a00eee76d9612158870d9be70429256ca724f14a`; `3.4.0^{commit}` = `0a11ec550726a09c91e288b2936a9be16eb6067c`; `for-each-ref --contains 71e3bcf` lists nothing; `origin/main` = `ccc23dd`. Then, after the verifier's search on the repo:
```
git -C <repo> reflog expire --expire=now --expire-unreachable=now --all
git -C <repo> gc --prune=now
```
True afterwards: `fsck --unreachable --no-reflogs` prints nothing; `cat-file -e` fails for the three old values. The bundles and the tables outside the repo still hold the ids.

### Not established (third clone)
- That the list of real ids is complete: it is the names on disk today; a session whose transcript was deleted is caught only by shape, and by shape nothing is left but the stub values.
- That the stub values and the 6 non-agent tokens are what their context says: I read the scripts that produce them, not the runs.
- The state of the repo after the apply (to be searched again there); the bundles, the two archives beside the repo and the tables were not searched.

---

## B. Second trial clone — FAIL (as measured; that clone no longer exists)

### Verdict

**FAIL — not cleared to apply.** One class of real session reference survives the rewrite: 31 cut agent ids in one file, present in 12 commits of the range, the tip included. Everything else checked holds. One table fix and a new trial clone are enough (S1); the rest of this section can then be re-measured on the new clone.

### Findings

**S1 — 31 cut agent ids are still there (blocking).**
Input: `work/20/20.10/03b_census.txt`, the list under "unclassified agents … : 31". What happened: each of the 31 rows carries the first 8 characters of an agent id (the letter and 7 hex digits); all 31 are prefixes of agent transcripts that exist on disk; none was replaced — the file is byte-identical in the repo and in the clone. The table has rules for full agent ids and for 5 longer cut forms, none for the 8-character form. What should happen: 31 `<agent-id>`. Smallest fix: 31 rules, one per literal prefix, each with the same word boundaries the short session rules use. Not a general "letter + 7 hex" rule: in this range that shape also matches 6 tokens that are not agent ids (4 stub ids of a dry run, 1 cut sha of a prompt, 1 cut tree hash) and would damage them.

**S2 — stub ids of two dry runs: 16 left, 3 replaced, by the same rule read two ways.**
Input: `work/21/21.1/03d_dryrun.txt` and `work/21/21.4/03d_dryrun.txt`. What happened: both files are the output of a stub that stands in for the tool and draws a fresh random id per call (`uuid4` in each `dryrun.sh`); no id in them names a session of the tool, and none is on disk. In the first file the 2 full ids (3 occurrences) and 1 short form were replaced as real, while 4 `resumed_from=` short forms of the same stub were left; in the second, 12 `resumed_from=` short forms were left. What should happen: one reading for both. They are synthetic by construction, so leaving all of them would have been right; replacing them is harmless too (see check 6). Smallest fix: none needed for a PASS; if uniformity is wanted, 16 more short rules or 3 fewer.

**S3 — more scripts lose constants than the log says.**
Input: `03_execute.log` entry [9], "three scripts hold a session id as a constant". What happened: true for session ids; but agent ids are constants too — 12 `.py` files change in the last tree (9 `score.py` with tables of agent ids, plus the three named), 27 `.py` paths across the range, 46 lines carry two or more placeholders. All 38 changed Python blobs still compile; none can be re-run as it stands, because every arm now maps to the same placeholder. What should happen: the owner was told three; the number is 12 in the tip. Smallest fix: say so.

### Evidence per check

#### 1. Session references — own search
Real ids from names on disk only (transcript and folder names under the tool-config folders of every profile and under the uid temp folder; no file was opened): 73 session ids, 339 agent ids. Set searched: 508 blobs (0 binary), 45 commit objects, the tag object, 561 tree paths — everything reachable from the three refs and not from `published`. 16 patterns, each proven on a control built from one real id (full, upper case, other separator, no separator, split across a line break, two groups with ellipsis, 8 hex after `resumed_from=`, 8 hex embedded in a word, agent id full, cut, after `agent-`, in a tree path). Hits, clone / repo (positive control):

| Pattern | Clone | Repo |
|---|---|---|
| any uuid shape, any case | 0 | 68 (18 distinct) |
| uuid on disk | 0 | 65 (16 distinct) |
| uuid with other separators / 32 hex / upper case | 0 | 0 |
| real id as a hex stream (catches line breaks and any separator) | 0 | 65 |
| first two groups, any / real | 0 / 0 | 11 / 11 |
| 8-hex token that prefixes a real id | 0 | 21 |
| first 8 hex of a real id anywhere, even inside a word | 0 | 86 |
| last group or middle groups of a real id | 0 | — |
| agent shape (letter + 7..16 hex) as a token | 37 | 398 |
| full agent id on disk | 0 | 355 (190 distinct) |
| cut agent id that prefixes one on disk | **31** | 37 |
| `agent-` + hex | 0 | 268 |
| ids of API calls (message, tool-use, request) | 0 | 0 |
| in tree paths, any of the above | 0 | 0 |
| in commit or tag messages, any of the above | 0 | 0 |

The 37 agent-shaped tokens in the clone: 31 = S1; 6 are not agent ids (4 stub `resumed_from=` values, 1 cut sha, 1 cut tree hash). Uuid-shaped strings left in the new objects: 0. Synthetic ids left: the 16 stub short forms of S2; code that calls `uuid4` (no value).
Inherited blobs: over the full trees of all 45 commits (633 distinct blobs, the published ones included) the only uuid hits are 4, one and the same real id, in `setup.py` and `score.py` of `work/15/15.10/` and `work/16/16.1/`. Each of the 4 blobs is an object of the published history (same object id there), is absent from the tip tree of `main`, present in `bma/21.4`. Confirmed as the builder says; this push sends no new copy.

#### 2. The 30 first-pass patterns
Control 30 of 30. Clone and repo give the same count for 28 patterns; the 2 uuid patterns go 68 → 0 and 47 → 0. Home prefix, uid, layout, encoded forms: 0. Mail 91, account word 182: the 45 × 2 + 1 identity lines only. Nothing came back.

#### 3. Published part
`published` = `ccc23dd`, ancestor of new `main`; the list of its 72 commits has the same checksum in both; 19 of 19 published tags resolve to the same object.

#### 4. Same history
44 commits, 0 merges; subject, body, author and committer name, mail and date byte-identical over the 44 (`cmp`, 44769 bytes); raw commit objects minus `tree`/`parent` lines: same checksum over the 45. The first 12 commits keep their hashes (nothing to replace in them); 33 commits are new. `bma/21.4` sits on commit 41 of 44 in both, same metadata. `3.4.0`: annotated in both, the two tag objects differ in the `object` line only, target is commit 38 of 44 in both. The builder's four hashes are the ones in the clone (`main` `8d6f8d6`, `bma/21.4` `dc55117`, tag object `3005a7b` on commit `0fd1ade`).

#### 5. Trees
45 commit pairs: path sets equal, 0 mode changes. 51 blob pairs differ (38 paths: 38 `.py` blobs, 5 `.json`, 4 `.log`, 3 `.md`, 1 `.txt`), one new blob per old blob, line counts equal. 391 differing lines; each matches its old line once the placeholders are put back, and every piece put back is one of: full uuid (68), 8 hex (11), two groups (11), agent id of 17 characters (355), 16 (5), 10 (1) — 451 ids. Last tree: 23 files, 330 lines (as the builder says).
Hex tokens of 7+ characters, whole range, message bodies included: 926 before (350 distinct), 407 after (117 distinct); 519 removed, 0 added; the 519 are exactly the hex groups of the 451 replaced ids (90 of 8, 68 of 12, 355 of 17, 5 of 16, 1 of 10) — 0 removed token is unexplained. None of the 451 replaced ids prefixes any of the 1564 git objects of the repo. Every commit hash, tree hash, sha1 and md5 quoted in a file is therefore unchanged. Nothing was replaced inside a longer hex string (0 placeholders next to a hex character).
Damage: 5 of 5 changed `.json` parse; 38 of 38 changed `.py` compile (in memory); no `.sh` changed. See S3 for what "compile" does not cover.

#### 6. The two stub uuids of `work/21/21.1/03d_dryrun.txt`
Each stands in that one file only (1 file each in the whole range, 0 on disk); no script reads the file (1 mention, a comment). Replacing them breaks no expectation and no cross-reference. One loss: the file used to show by eye that turn 1 and turn 2 share an id and the second session has another; the three ids now read alike, and only the boolean lines of the same file still say it.

#### 7. Leftovers in the clone, and the apply
Clone: 23 refs, none reaches an old commit; no remote, no replace refs; 34 old commit and tag objects still present, held by 4 reflog files; `packed-refs` keeps a stale line for the old tag, overridden by the loose ref. A fetch by refspec carries none of it.
The apply commands are in part A.

#### 8. The table (read after the search)
226 lines: 18 full session ids, 190 full agent ids, 13 short session rules, 5 cut agent rules. The counts match what the range holds (18 distinct uuids, 190 distinct full agent ids).
- Too narrow: no rule for the 8-character cut agent form — S1.
- Not too wide: the short rules are bounded on both sides by "no letter or digit" and the hex comparison of check 5 shows they hit nothing else. One edge to know: a short rule would also fire on the first group of an id written with three or four groups cut; no such form exists in the range.
- 3 rules (2 full, 1 short) are for stub ids — S2.

### Not established
- That the list of real ids is complete: it is the names on disk today; a session whose transcript was deleted is caught only by shape (and by shape nothing is left but S1 and S2).
- Whether the 6 agent-shaped tokens and the 16 stub values are what their context says; I read the scripts that produce them, not the runs.
- The state of the repo after the apply; the new clone that S1 requires.
- The two bundles, the two archives beside the repo and the tables were not searched.

---

## C. After the second apply

Same verifier, read-only, on the repo after the third clone's refs were moved and both trees reset. Nothing expired, nothing pruned by me.

### Verdict

**May be pushed** — `git push origin main` and `git push origin 3.4.0`, the two refs by name. What those two pushes send holds no trace by the first-pass definition and no real session reference. Standing notes, none blocking: S3 (scripts that lost id constants), F1 (three lines of prose, kept by the owner's ruling), A2 (four published blobs below the tip), C1 below.

### Findings

**C1 — 31 ignored files in the repo folder hold traces and real ids.** Input: the files `git status --ignored` lists (12 under `docs/drafts/`, 17 under `log/`, 2 `local.env`). What happened: they carry home paths, the layout, the uid folder, 148 real session ids and 216 real agent ids. None is tracked, none is in any commit of the range (0 of their paths in any tree); three `.gitignore` rules keep them out. What should happen: nothing for this push. They would go out only by `git add -f` or by a change of those rules — worth knowing before either.

**C2 — old objects of the second pass are still in the repo, held by reflogs.** Expected; see check 4.

### Evidence

1. **Every ref, and the push set.** 23 refs (3 branches/remote, 20 tags); no stash, notes, replace refs or leftover temporary refs. Controls: 30 of 30 and 16 of 16.
   - *All refs, not the published tip*: 881 objects — 508 blobs, 45 commits, 312 trees, 16 tag objects; 561 tree paths. It is the set verified in the third clone plus the 15 published tag objects (A3). The 30 patterns give the third clone's counts, the tag objects apart (mail 106 = 91 + 15 taggers; account word 198 = 182 + 8 taggers × 2). The 16 session patterns: uuid shapes 3 (the stub ones, 1 file), every real-id pattern 0, cut agent ids 0, non-agent letter + 7 hex tokens 6.
   - *What the two pushes send* (`rev-list --objects origin/main..main` = 859, plus the tag object = 860: 506 blobs, 44 commits, 309 trees, 1 tag): home prefix 0, uid 0, layout 0, encoded forms 0, project-key shape 6 (generic); mail 89 and account word 178, all in the 44 × 2 + 1 identity lines; uuid shapes 3 (stub); uuid on disk 0; hex-stream form 0; two groups 0; 8-hex prefixes 0; full agent ids 0; cut agent ids 0; `agent-` + hex 0; tree paths 0; messages 0.
2. **Refs and old history.** 75 old commits of the two passes: 0 reachable from any ref. `for-each-ref --contains` → 0 for the pre-apply tip, 0 for the pre-apply branch commit, 0 for the pre-apply tag's commit. `origin/main` = `ccc23dd`, ancestor of `main`, 72 commits, same checksum of the list as before; `main` `344cb22`, `bma/21.4` `0801b06`, `3.4.0` tag object `bbd2156` on `0a11ec5`, `main^{tree}` `a00eee7`; 44 commits ahead. The 19 published tags equal the objects the first bundle records (19 of 19).
3. **Working trees.** Repo: `status` empty, index = HEAD; each of the 467 tracked files hashed from disk equals its blob in HEAD (0 differ). Patterns over the 467: home prefix 0, uid 0, layout 0, account word 0, mail 0; uuid shapes 3 (stub); real ids 0; cut agent ids 0. Worktree folder: 390 files, all tracked, `status` empty, 0 differ from HEAD `0801b06`; hits only in the 4 inherited published blobs of A2 (home prefix 2, account word 6, the one real session id 4 times), nothing else. Ignored files: C1.
4. **What still holds old objects.** Reflogs naming old commits: `logs/HEAD` (3 of 4 lines), `logs/refs/heads/main` (3 of 3), `logs/refs/heads/bma/21.4` (1 of 1); the worktree's `logs/HEAD` 0. `ORIG_HEAD` (repo and worktree) and `FETCH_HEAD` name new objects only. `fsck --unreachable --no-reflogs`: 245 objects (33 commits, 51 blobs, 160 trees, 1 tag object); with reflogs as roots: 1 (the old tag object). The 34 old commit and tag objects of the second pass are present; the 43 of the first pass are gone. The two commands are still the right ones:
```
git -C <repo> reflog expire --expire=now --expire-unreachable=now --all
git -C <repo> gc --prune=now
```
True afterwards: `fsck --unreachable --no-reflogs` prints nothing; `cat-file -e` fails for `71e3bcf`, `77b0f00` and the old tag object `5c8a130`; the refs of check 2 and both `status` outputs are unchanged. After that the ids exist only outside the repo: the bundles, the tables, the third clone (to be removed), and the ignored files of C1.

### Not established
- The remote: `origin/main` is the local record of it; nothing was fetched.
- The state after expire and prune (not run by me).
- The bundles, archives and tables beside the repo.
- Completeness of the real-id list beyond the names on disk today.
