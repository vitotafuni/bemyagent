# 21.4 — independent VERIFY of the apparatus (step 7)

Verifier: an agent that neither designed nor built the apparatus (strongest tier). It held `02_tasks.md`, `01_think.md`, `03_execute.log` and the scripts. It fixed nothing. The real `claude` binary was never run. No real transcript was read. Everything it wrote besides this file is under `<scratchpad>/p214/verify_tmp/` (called `<V>` below).

## Verdicts

- **Cleared for the pilot (`q901`): PASS_WITH_CAVEATS.** The seeds differ by exactly the line, the launcher does what `02_tasks.md` says and stops where it should, and the dry-run cannot reach the real binary. Nothing blocks the launch of `q901`. The caveat: the line `PILOT OK` of `check_pilot.sh` is not enough as built (M1, M6). Until those are fixed, the pilot's output is read by eye for the four things listed under "What only the pilot can show".
- **Cleared for the six: FAIL as built.** `read.py` gives a wrong class, or keeps an arm it should leave out, on inputs that a real round can produce (M1–M6). Each fix is small. The defects go back to the builder, and the reader is re-checked before the six. One decision is the designer's and must be dated before the pilot (D1).

## Findings

### Blocking (for the pilot)
None.

### Must fix before the six

**M1 — `check_pilot.sh` says `PILOT OK` when the reader cannot read a real result.**
Input: a pilot whose `Read` results carry a line prefix the reader does not know (`L1| text`), in turn 1 and after the boundary (`<V>/att/a7.py`, case `unknownformat_everywhere`). What happened: (iv) `none`, (i) `none`, one whole-form access with 0 headings, `PILOT OK - launch the six`, exit 0. The same with turn 1 never reading the rules (`iv_none`): `PILOT OK`. What should happen: `02_tasks.md` expects (iv) `whole`; turn 1 of the pilot is the only real-format positive control the reader gets before the six. A reader that is blind to the real format would class all six arms `none`, and the table would say *null*. Smallest fix: in `check_pilot.sh`, add to `bad` when (iv) is not `whole`, and when any access in either segment has a whole form and no heading.

**M2 — an arm whose turn 2 failed, or ran elsewhere, is eligible and counted `none`.**
Input: boundary proven, `t2.json` present with `is_error: true`, `t2 exit=1`, no record after the boundary (`a3.py`, `c5_T2failed`); and `t2.json` with another session id, no turn-2 prompt in the transcript (`c6_T2elsewhere`). What happened: `eligible=True`, (i) `none`; the first carries two flags, the second none. What should happen: the arm had no occasion; it leaves (i). A session or rate limit on six parallel arms makes the first case plausible, and a C arm lost this way reads as "0 of 3 whole". Smallest fix: in `read_arm`, add a reason when the turn-2 prompt is not a user record after the boundary, when `t2.json`'s session id differs from `t1.json`'s, and when turn 2 failed (exit code or `is_error`) with no write after the boundary.

**M3 — an access that returned no rules text is counted `none`, the same as no access.**
Input: after the boundary, a `Read` with no offset and no limit whose result is the tool's "file unchanged since last read" stub (`a1.py`, `stub`; `a7.py`, `unchanged_stub_after`). What happened: (i) `none` with a note; the summary counts it `none`; `PILOT OK`. What should happen: the arm did what the line asks and the tool gave nothing back. That is neither `whole` nor "no access", and it says the proxy failed, not the line. Whether the tool answers a re-read after a compaction with the stub is not known, and a C pilot that does not re-read cannot show it. Smallest fix: a class of its own (for example `attempted`) kept out of the three counts and listed in `left_out`, and `PILOT NOT OK` when the pilot has one.

**M4 — the rules text delivered by an access the reader does not recognise is `none`, with no flag.**
Inputs (`a1.py`, `a6.py`), each with the full text in the result and then an `Edit`: `cat .bemyagent/docs/0*.md` → `none`, 0 unresolved mentions; `for f in .bemyagent/docs/*.md; do cat "$f"; done` → `none`; `python3 -c "print(open('<rules>').read())"` → `none`; `ln -s <rules> r.md` then `cat r.md` → `none`; the path in another letter case → `none`; `cat "$PWD/<rules>"` → `none` (this one is flagged unresolved). What should happen: these arms read the file whole. The miss moves an arm from `whole` to `none`, the direction that drops the candidate. Smallest fix: in the window, when no counted access is `whole` and some tool result holds all eight headings as whole lines, set a flag and leave the class to the hand-read (or leave the arm out with that reason).

**M5 — a compaction during turn 2 moves the cut, and only a flag says so.**
Inputs (`a3.py`): whole read and edit after the call's boundary, then an automatic boundary, then edits (`c2_autoT2_readbefore`) → (i) `none`. Edit with no read, then an automatic boundary, then a whole read (`c3_autoT2_readafter`) → (i) `whole`. Both `eligible=True`, both with the two boundary-count flags, and `launcher_and_transcript_agree` is true in both. What should happen: `whole` and `none`. Smallest fix: cut at boundary number `boundaries_before + 1` (the launcher wrote it) instead of the last; or make the count mismatch an eligibility reason.

**M6 — the pilot check stays `PILOT OK` when most of the rules came back without the arm acting.**
Inputs (`a7.py`): a `file` attachment of the rules file after the boundary holding 7 of the 8 sections (`attach_7of8`) → "7 of 8 handed back", `PILOT OK`. A boundary whose `preservedSegment` names the turn-1 read and its result (`preserved`) → 0 of 8, `PILOT OK`, nothing printed about it. What should happen: the Pivot stops the round when the rules are handed back; a partial hand-back and messages kept across the boundary are for the designer to see and rule on, not for a line that says launch. The rules file is near the size where a re-attached file may be cut. Smallest fix: `check_pilot.sh` adds to `bad` when any record about the rules file after the boundary carries a heading, and when the boundary's `preservedSegment` or `preservedMessages` is not empty; `read.py` reports both.

### For the designer, dated before the pilot

**D1 — a read that returned every line is classed `slice` because of its form.**
Inputs (`a1.py`), each with all 107 lines and 8 headings in the result: `Read` with `limit: 2000` → `slice`; `offset: 1` → `slice`; `offset: 1, limit: 2000` → `slice`; `sed -n '1,$p'`, `head -n 500`, `tail -n +1`, `awk '1'` → `slice`. `offset: 0` and explicit nulls → `whole`. `02_tasks.md` defines (i) by form ("no offset, limit or slicing command"), so the reader follows the text; the text is what is in doubt. An arm that obeys "first line to last" this way is counted against the line. My reading: the form should be recorded and the class decided by what was delivered. See point 8.

### Notes

- **N1 — two false `whole`.** `cat <rules> | grep '^## ' | cat` with the eight heading lines as its result → `whole` (only the last stage of a pipeline is checked; the code is the 21.2 census's). A result with twenty lines replaced by a marker the reader does not know, or with the last three lines cut → `whole`. Smallest fix: `whole` also requires the file's first and last line in the result (or every line).
- **N2 — writes the census definition does not see.** With a whole read after them, each of these left (i) `whole`: `touch`, `node -e "…writeFileSync…"`, `ln -s`, `npm install`, `git apply`, `git mv`, `git stash`, `perl -pi`, `curl -o`, `dd of=`, `install`, `patch`, `truncate`, `npx prettier --write`, `awk '{print > "f"}'`. `02_tasks.md` names the census definition, so this is inherited, not a build error. The hand-read should look at the shell commands before a counted `whole`.
- **N3 — things that count as the first write.** A failed `Edit` or `Write` ("file has not been read yet", `is_error`) is the first write, so a whole read after it is late → `none`. So are `mkdir -p …`, `2> err.log`, and `cat <rules> | tee /dev/null` (the read and the write are one call → `none`). A `Read` and an `Edit` issued in one assistant turn → `none`. These follow the letter of `02_tasks.md` ("a `Write` or `Edit` call"); the first one is the likeliest after a compaction and the designer may want it said.
- **N4 — (ii) by heading lines.** A summary that only lists the eight heading lines → 8 of 8, arm ineligible, though no rule text came back. The whole text without the `## ` marks, or in bold → 0 of 8, eligible. The text in a record of a type other than `user`, `attachment`, `system` → 0. The text as a text block inside a record that also carries a tool result → 0. All four are unlikely; the first two follow from the proxy the spec chose.
- **N5 — the launcher.** `launch.sh q112 q112` ran the arm twice at once: six stub calls, two sessions on one tree, every status line doubled (`<V>/dup/`). The run-twice guard looks for `t1.json`, which the first copy has not yet made. Smallest fix: drop repeated names, or `mkdir` a lock per arm before starting it. No call has a timeout: a hung call holds the round until the user ends it.
- **N6 — `setup.py`.** It asserts that L is C plus one line and that the line starts with `**Read this file whole`; it does not assert the whole line of `02_tasks.md`, the line number 2, or which commit the ref and the working tree are at. All of these hold today (point 1), by my check and not by the script's. `<repo>` has many uncommitted changes; none is in a file the seeds take.
- **N7 — likely wrong stops of a healthy pilot (`a7.py`).** A second model in `modelUsage` → `PILOT NOT OK`, "the arm is not clean". An attachment that is not an instruction file and names a path outside the arm (a skill listing) → the same. A summary that quotes the instruction header once → the same. One permission denial in turn 2 → `PILOT NOT OK`. Each stop is on the safe side, but the reason printed does not name the counter. Smallest fix: print which term of `clean` failed.
- **N8 — `read.py` never consults the certificate.** An arm that is not clean, or whose design check fails, is still counted in the per-condition summary. The agent of step 9 must join the two by hand.
- **N9 — other classes worth knowing.** A whole read of `BEMYAGENT.md` (it holds all eight heading lines) is (i) `none` and is listed under `other_files`. The `Grep` tool on the folder, returning the eight headings → `none`; on the file → `slice`. A read in a sidechain record counts as the arm's own (the arms have no agent tool, so this should not arise). A result marked `is_error` that still holds the text → `slice`.
- **N10 — the round's scratch root** is a session's temporary folder. The trees are not built yet. If the folder is cleared between the build and the user's launch, the launcher skips every arm ("no tree"), which is loud.
- **N11 — `harness/README.md`'s table** has the row `3/3 | 3/3 | ceiling`; `02_tasks.md` has `3/3 | any`. The spec's row is wider and is the one to read by.

## What I ran, point by point

**1 — the seeds.** `setup.py q112 q115` into `<V>/seeds`: it printed its assertion (rules line 2, `BEMYAGENT.md` line 30). `diff -r` without `node_modules` and `.git`: two files, `1a2` and `29a30`, the same line, the line of `02_tasks.md`. `node_modules`: `diff -rq` silent. The L files are byte-equal to `git show bma/21.4:<path>`, the C files to `git show HEAD:<path>`; `git diff --stat main bma/21.4` is two files, two insertions. Arm names, git author and commit messages carry no condition. A search for the line's first words finds 0 files in the C tree and 2 in the L tree, so the search can hit. Both prompts: `cmp` silent against 21.1's turn 1; the turn-2 sentence occurs once in `02_tasks.md`; the compaction prompt is the eight bytes `/compact`.

**2 — the classes.** About 200 transcripts of my own (`<V>/att/a1.py`, `a2.py`, `a6.py`; writer `fw.py`), none of them the builder's cases. Right under `02_tasks.md`: no offset and limit, `offset: 0`, `cat`, `cat -n`, `nl -ba`, `less`, `cat F | cat`, `cat` of two files, `wc -l` then `cat`, `cd` then `cat`, relative and absolute paths, the `/tmp` spelling, a result in two blocks, `git show HEAD:<path>` → `whole`; a here-doc or a redirect before the read → `none` (the write came first); two reads that cover the file together → `slice`; a whole read between two writes → `none`; a truncation marker → `slice`; the other arm's file, a copy of the file elsewhere → `none`. `git status`, `npm test`, `ls`, `2>&1`, `2> /dev/null`, quoted `>` are not writes; `tee`, `>>`, `python -c open(…,'w')`, a python here-doc, `sed -i`, `git commit`, `cp`, `rm`, `printf >` are. Wrong or doubtful: M3, M4, D1, N1, N2, N3, N9.

**3 — the cut.** `a3.py`. An automatic boundary in turn 1 and then the call's: the last is used, correctly. A boundary inside a tool result is not a boundary. A boundary and no turn 2 → not eligible. No launcher status → not eligible. A renamed subtype, a summary record with no boundary record, a stream-only proof → no boundary, (i) null with the reason, not eligible. A boundary record without metadata, or with the other spelling of the key, is accepted. Wrong: M5, M2.

**4 — eligibility.** `a4.py`. Whole file attachment, instruction record, nested-memory attachment, a meta user record, `BEMYAGENT.md` attached, headings split over two records → 8 of 8, not eligible. A reference with no content, a hand-back after the first write, the arm's own recital → 0. Wrong or doubtful: M6, N4.

**5 — both directions.** `a5.py`, arms named `q112`–`q117` and `q901`, C trees with the C text and L trees with the L text. C none ×3, L whole ×3 → C 0 of 3, L 3 of 3. The reverse → C 3 of 3, L 0 of 3. Mixed → 1 whole, 1 slice, 1 none in each. One arm handed back and one without turn 2 → 2 eligible in each condition, both named with their reasons. All whole → 3 and 3. The pilot is listed and not counted. The same transcript under a C name and an L name, on either text, gets the same class; the condition label is read in one place, the summary. An arm name outside the map belongs to no condition.

**6 — the launcher.** Read line by line. The one call is `command claude -p <prompt> [--resume <id>] --model sonnet --output-format json|stream-json [--verbose] --allowedTools Read Write Edit Bash Glob Grep`, stdin from `/dev/null`, in the arm's tree; the only `rm -rf` is on the launcher's own snapshot folder; nothing in the config folder is moved or deleted. Dry-run reach: the dry-run PATH is the stub's folder and three system folders; none of the three holds a `claude` (checked again before each of my runs); `BASH_ENV` and `ENV` are empty; `local.env` does not touch PATH; no script names a binary by absolute path; the launcher's `command` skips shell functions. My own guard refused once, correctly, when the shell I called it from had `claude` as a function; under plain bash it resolved to the stub and I ran the duplicate-name case (N5). The real config folder had 23 project folders before and after all my runs.

**7 — certificate and pilot check.** Fifteen synthetic pilots through `check_pilot.sh` (`a7.py`). A healthy one → `PILOT OK`; one with a synthetic-model assistant record → `PILOT OK`. Stops that are right: no proof, no boundary, session not kept, 8 of 8 handed back (the builder's dry-run shows these; my rounds show the reader side). Stops that may be wrong: N7. Quiet where it should speak: M1, M3, M6; a turn 2 with no action at all and no error → `PILOT OK` with (i) `none`. The brief's list of eight real-run assumptions was not in my hands when I ran this point; I went by the gates in the code. See "Not established".

**8 — the builder's decisions.**

| decision | judgement |
|---|---|
| the pilot is not counted | keep |
| `offset: 0` is no offset | keep |
| any `limit` is a slice | **designer must decide; I would change it** (D1): class by what the result holds, record the form beside it |
| an access with no heading is `none` | **change** (M3): its own class, out of the counts, and a pilot gate |
| (ii) = the full heading line as a substring | keep, with M6's gate on any record about the rules file |
| a leaf = a new file at `work/X/X.Y/` | keep (reported only; `micro.log` is rightly not a leaf) |
| a stream-only proof leaves the arm out of (i) | keep |
| flags never change `eligible` | **change** for three of them (M2, M5): turn 2 failed or absent, the turn-2 prompt missing, the boundary count |
| the launcher stops an arm whose session id changes at the compaction | keep (it is the Pivot) |

**9 — what the files disclose.** Search terms: the user name, the host name, the home prefix, the temporary-folder prefixes, the config folder's name, the base folder's name, the mail domain, two session-id prefixes, uuid shapes, hex runs of 16 or more. On `local.env` the search hits 3 lines, and a planted uuid is found, so it can hit. On every other file of the folder: no machine value; the only hits are the generic two-folder spelling of the system temporary folder, with no user or session part, in four files (`03c_selftest.txt`, `certificate.py`, `mask.sh`, `selftest.sh`). No uuid shape, no long hex run; the dry-run output shows session ids as `<id8>`. `local.env` is ignored by a rule in `.gitignore` that is itself not yet committed. `read.py` and `certificate.py` print paths and record indexes, never record text; their output holds absolute paths and belongs in the scratch folder or behind `mask.sh`.

**10 — the saved outputs.** `./selftest.sh` with the scratch root in `<V>`: exit 0, 126 PASS, 0 FAIL, the output byte-equal to `03c_selftest.txt`. `./dryrun.sh` the same way: exit 0; against `03d_dryrun.txt` it differs in 62 diff lines, all of two kinds — the first eight hex digits of the turn-1 prompt hash (the prompt holds the arm's path, which is another path under my root) and the order of the stub's log lines (the arms run in parallel). With both normalised the diff is empty. No `__pycache__` appeared in the task folder.

## Zero and empty results, and why they could have been otherwise

- The seed search for the line in the C tree is 0; in the L tree it is 2.
- The residue search over the task folder finds no machine value; on `local.env` it finds 3 lines.
- The dry-run diff is empty only after normalising; before, it showed 62 lines, so the comparison can differ.
- The selftest diff is empty with and without masking, because that output prints no path. It rests on the 126 lines being equal, not on the mask.
- "No `claude` in the three system folders" is an existence test per folder; in the stub's folder the same test finds the stub.
- 23 project folders before and after: the stub writes transcripts, and in my rounds they landed in `<V>` (2 files in the duplicate-name run), so a write would have shown.

## Not established

- Whether `/compact` under `-p --resume` compacts, whether the boundary has the shape learned from interactive transcripts, whether the session id and the transcript are kept: only the pilot.
- What a real `Read` result looks like in a headless transcript. The reader knows two prefixes; M1 is the guard.
- What the tool returns for a `Read` of the rules file after a compaction (the text or the stub), and whether messages kept across a boundary are written again after it. A C pilot that does not re-read shows neither.
- Whether a real result lists a second model, and whether real attachments name paths outside the arm (N7).
- The builder's list of eight "only a real run can test" assumptions, item by item: I judged the gates in the code instead, and say so rather than imply the list was walked.
- The duplicate-name run is shown with the stub; a second `launch.sh` started by hand while the first is in turn 1 is refused by reading only (the first call's output file exists from the start of the call).
- N2's list is not complete: any command that writes and is not in the census's list behaves the same.

## What only the pilot can show — read by eye until M1 and M6 are in

1. `compaction_proven=1`, one boundary in the transcript, the same session id on the three calls.
2. (iv) `whole`, resting on one access with 8 headings. Anything else means the reader cannot read the real format: stop.
3. "records about the rules file itself": anything but `none`, or a reference with no content, goes to the designer.
4. A `not clean` stop: look at `result_models` and `foreign_attachment_types` before reading it as a failed proxy.
