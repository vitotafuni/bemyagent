# 21.4 — re-verification of the apparatus after Amendment 1 (step 7, second pass)

2026-11-15. Same verifier as `03e_apparatus_verify.md`: I designed nothing and built nothing here. The specification I read against is `02_tasks.md` with Amendment 1 (A1–A8). The real `claude` was never run: every launcher run used a stub first on a three-folder `PATH`, checked before each run. No real transcript was read; every input is synthetic and lives in `<scratchpad>/p214/verify_tmp/` (`att/` the first pass's inputs, `att2/` their re-run and the new ones, `lk/` the launcher cases, `run2/` my runs of the two scripts). Nothing in `<repo>` was changed except this file.

## Verdicts

- **Cleared for the pilot: PASS_WITH_CAVEATS.** Nothing blocks launching `q901`. Two caveats. (1) A healthy real pilot will probably print `PILOT NOT OK` for a reason that is not a defect of the round (R2: one code fence in the compaction summary is enough). (2) `PILOT OK` is not yet sufficient by itself: six real differences pass in silence or as a printed fact only (R3). Until R2 and R3 are in, the list at the end of this file is read by eye. `check_pilot.sh` only reads, so it can be run again on the same pilot after a fix; the pilot does not have to be repeated.
- **Cleared for the six: FAIL as built.** Five findings change who is counted or let a broken occasion through (R1–R5), and one ruling is incomplete (R6). None needs a redesign; each has a small fix or a dated sentence in `02_tasks.md`.

## Findings

### Blocking (for the pilot)

None.

### Must fix before the six

**R1 — `attempted` is wider than the amendment means, and it removes arms.**
Input: after the boundary and before the first write, one of `grep -c`, a `grep` with no hit, `grep -q`, `grep -l`, `sed -n '200,210p'`, `awk 'END{print NR}'`, `head -c 20`, `grep -o … | head`, a `Read` with an offset past the end, the `Grep` tool in count mode or in its default mode (it answers with the file's name).
What happened: the access is classed `attempted`, the arm is not eligible and leaves (i). In the pilot the stop reads "the tool withheld the text", which is not what happened. `wc -l` on the same file is `none` and the arm stays.
What should happen: A2 says "holds none of its lines" and gives two examples, the tool's "unchanged" answer and an error. The code took the sentence, not the examples. An arm that searches the rules instead of reading them is a real `none` (or `slice`): it had the occasion and did not read. Dropping it loses arms, and not evenly if the added line changes how often an arm searches.
Smallest fix: `attempted` only when the result is an error, or is the tool's "unchanged" answer, or the access was of a whole form (no range, no filter) and delivered no line. An access of a slice form that delivers no line is not an access for (i); it is listed with its form. If the designer wants the wide reading, A2 should say so before the six.

**R2 — the (ii) gate counts short lines and the sentinel line: a healthy pilot stops, and in the six every arm would be listed as handed back partly.**
Input: a pilot whose compaction summary holds a code fence; one with a table rule; one where a record after the boundary carries the text of the arm's own `CLAUDE.md` (that text is one line of the rules file, word for word); one where a turn-1 read of the seed's `README.md` (it has fences) is kept across the boundary.
What happened: `2 of 90 lines (0 of them 20+ characters)`, `1 of 90`, `1 of 90 (1 of them 20+)`, `2 of 90` with "preserved across the boundary" — each `PILOT NOT OK`, "the designer's ruling is needed". The count of 20+ character lines is already printed beside n; it does not gate.
What should happen: three of the 90 lines are a fence (twice) and a table rule; they match anywhere. A summary of a coding turn very likely holds a fence. The stop is loud and safe, but it costs a dated amendment for nothing, and in the six `handed_back_partly` would name every arm, which hides a real partial hand-back.
Smallest fix: gate and list on the lines of 20 characters or more, leaving out the sentinel line when the record that carries it is the arm's own instruction record; print the short-line hits as a fact. Whether the real instruction record carries the file's text is not established (the synthetic one in `synth.py` carries only the header, so the builder's cases cannot show it).

**R3 — what the pilot check passes in silence.** Each of these printed `PILOT OK`.
(a) Preserved records named but absent. Input: `preservedMessages` lists six ids that are not in the file; a `preservedSegment` whose head and tail are not in the file; a preserved field that is a string, not an object. Printed: "uuids listed 6, records found 0" (the six is three ids counted in both lists), or "fields present True" with nothing found. Should stop: the reader was told something was kept and could not look at it. Fix: stop when a preserved field is present and non-empty and no record is found.
(b) Rules text after the boundary in a shape the reader skips. Input: the turn-1 read's result written again after the boundary under a new id; the text in a record of a type other than `user`, `attachment`, `system`; the text as a text block of a record that also carries a tool result; the text under a `toolUseResult` key only; the text in an assistant record of a synthetic model. Printed: `0 of 90`. Should count. Fix: scan every record after the boundary except the arm's own assistant output and the result blocks of calls issued after the boundary. This is the case that matters most: with the rules back in context under a skipped shape, six arms would read nothing in both conditions and the round would be read as "the line does nothing".
(c) Compaction that did not shrink the context. Input: prompt tokens equal before and after the boundary. Printed: "(shrank: False)". Should stop, or stay on the eye list.
(d) Preserved field absent or empty: printed "fields present … False". This is right when nothing was kept, and silent when the real tool names the field otherwise. Eye list.

**R4 — a turn 2 that failed after its first tool call is counted `none`** (residue of M2).
Input: turn 2 runs `ls`, then the call fails (`is_error`, or exit code not 0); the same with one `Edit` before the failure.
What happened: eligible, class `none`, flags only.
What should happen: A5(b) excludes only "failed before any tool call", and the code follows it. With a read-only call and no write, the window never closed: the arm did not reach the point where it would have read or not read. Counting it `none` pulls toward 0 in whichever condition fails more.
Smallest fix: an arm whose turn 2 failed and made no successful write leaves (i) with that reason. An arm that failed after a successful write is rightly kept.

**R5 — the compaction call killed by the time limit does not end its arm.**
Input: my stub hangs in the compaction call after writing the boundary; limit 4 seconds.
What happened: status `cp exit=142`, "cp killed by the time limit", proof found, turn 2 ran, the reader gave eligible, `whole`, with the flag "cp exit code 142".
What should happen: A7 — "a call that hits it ends its arm like a failed call". The launcher never tests the compaction call's exit code; only the proof decides. A call killed part way may have written the boundary and not the rest. `check_pilot.sh` does stop on this exit code; the six have no such check.
Smallest fix: in `launch.sh`, an exit code other than 0 from the compaction call skips turn 2; or the reader leaves the arm out when the status carries one.

**R6 — the ruling on partial hand-back needs a number before the six** (for the designer).
The ruling: a partial hand-back stops the pilot and, in the six, is reported and does not exclude. It is sound against bias (the hand-back is the tool's, the same in both conditions) and, with R2 as built, necessary: otherwise every arm is out. It is not sound for the reading of a null. Inputs: summaries carrying 82 and 85 of 90 lines → both eligible. An arm with 80 of the 87 long lines back in context had no occasion; three such arms at `none` would read as "the line does nothing". What to write, dated before the six: the count is on lines of 20+ characters; n of N is printed beside each arm's class in the verdict; and either a threshold above which the arm is not an occasion, or the sentence that a null with partial hand-back is reported as "not tested", not as "no effect".

### Notes

- **R7 — the window against A4, three small differences.** (a) A shell write whose command returned an error (`npm test > out.txt 2>&1` failing; a here-doc followed by a failing test) is not a first write, so a later whole read is `whole`. A4 exempts a failed `Write` or `Edit` only; the file was written. (b) A `Write` with no result record is not a write. (c) One assistant record holding an `Edit` and then a `Read`: the `Read` is inside the window, though A4 says "issued before it". Whether the real tool ever puts two calls in one record is not established. Fix: (a) a shell write counts whatever its exit code; (c) compare block order inside the record.
- **R8 — `head -3 <rules file>; cat BEMYAGENT.md` is `whole`.** The call names the rules file, the result holds every line through the other file. A3's rule says a delivery through `BEMYAGENT.md` is `none`. `wc -l <rules file> && cat BEMYAGENT.md` is `none` with the flag, which is right. Fix: a call that also names a file embedding the rules is flagged for the hand-read instead of counted.
- **R9 — the reader takes the rules' lines from the final tree.** An arm that added a line to its rules file after reading it → (i) `slice` and (iv) `slice`, with a flag only when a turn-1 snapshot exists. Fix: take the lines from the turn-1 snapshot when there is one.
- **R10 — the certificate join looks at the whole transcript.** A call naming another arm's tree, or a non-existing absolute path beside the trees, made after the counted read → not clean → arm out. Relative `git worktree add ../project-task-1.1`, `ls ..`, `cd .. && pwd` stay clean; `../q115/…` does not. So an arm can leave for what it did after the window. The reason depends on the condition only through arms that act on more of the rules (the worktree rule). Fix: print whether the first failing call lies after the window's end; the designer rules once.
- **R11 — turn 2 killed by the limit after it acted.** `t2.json` is empty, the reader says "turn 2 did not run" and leaves the arm out even with a whole read in the transcript. Conservative; the reason is wrong. Fix: name it "turn 2 killed by the time limit".
- **R12 — `R214_TIMEOUT=abc` or `=0`.** Printed "time limit per call: abcs" / "0s"; no limit applied. Fix: refuse a value that is not a positive integer.
- **R13 — after a crash.** A second launch says "`<out>/q901.t1.json` exists - refusing to run twice"; with that file removed, "locked by another launch (`<out>/locks/q901`) - refusing to run twice". Refusing is the right default. No file says what to clear to run a pilot again after a trivial failure (tree, the three outputs, the lock, the status lines, the arm's project folder in the tool's configuration). Fix: four lines in `02_tasks.md`, or name the lock's path as the thing to remove in the message.
- **R14 — a whole delivery in JSON-escaped form** (`jq -Rs .`, `json.dumps`) is `none` with no flag. Unlikely.
- **R15 — stops of the pilot that may be the real tool's normal behaviour**, all loud and named: the summary record written by a second model on the main chain (`model_pinned_on_main_chain`); the turn-2 prompt recorded wrapped in other text (`design_ok`); a resume that changes the session id; an override header counted 5 against 4 when the summary quotes it; an attachment naming a path outside the arm; a permission denial. Each needs a ruling if it fires, not a re-run.
- **R16 — N6's residue.** `setup.py` now asserts line 2, the same line in both files, one inserted line, and writes both commit ids and the line's sha1 to `setup.status`. It still asserts only the line's first words, not the whole line of `02_tasks.md`.

## My earlier findings, re-run on my own inputs

| Finding | State | What my input gave now |
|---|---|---|
| M1 | closed | (iv) not `whole` → `PILOT NOT OK`; an unknown line prefix no longer matters (substring) |
| M2 | closed for my two inputs; residue R4 | failed before any call → out, named; turn 2 in another session → out, two reasons; failed after one read-only call → still counted `none` |
| M3 | closed | the "unchanged" answer → `attempted`, arm out; pilot stops. New side effect R1 |
| M4 | closed as the amendment says | glob, loop, script → `none` + `delivered-unresolved`, listed for the hand-read; in the pilot a WARNING, not a stop |
| M5 | closed | read before a turn-2 boundary → counted; cut at the launcher's number; a further boundary flagged; a count too high → out, named |
| M6 | closed for the pilot; closed differently for the six | any n > 0 or anything kept → stop; in the six a partial hand-back is listed and does not exclude (R6). Silent cases left: R3 |
| D1 | closed | `limit: 2000`, `offset: 1`, `sed -n '1,$p'`, `head -n 500`, `tail -n +1`, `awk '1'` → `whole`, form recorded |
| N1 | closed | grep of headings piped through `cat`, an elided middle, a cut tail → `slice` |
| N2 | unchanged by design | moved to the hand-read (A8) |
| N3 | closed, with R7 | failed `Edit`/`Write` not a write; `mkdir -p … && cat`, `tee /dev/null` → `whole`; order of read and write in one turn right |
| N4 | partly closed | text without marks or in bold → 82 of 90, reported; other record types and a text block in a result record → still 0 (R3b) |
| N5 | closed | repeated name run once; lock refuses; two launches at once → one refusal; time limit applied (but R5, R12) |
| N6 | closed but for R16 | line number, both files, commit ids recorded |
| N7 | closed | every stop names its check and term; second model printed only |
| N8 | closed | certificate not clean → arm out with the failed terms (but R10) |
| N9–N11 | not re-examined | notes; `harness/README.md` still has the ceiling row as `3/3`, `3/3` where `02_tasks.md` has `3/3`, `any` |

Both directions of the verdict still read right on synthetic rounds: C 0/3 with L 3/3, the reverse, a mixed round, exclusions named, labels not used. The rules' lines are taken per arm: 90 non-empty lines in C, 91 in L; an L arm given the C text is `slice`.

## Amendment 1 against the code

| Point | Does the code do it | Where the text is open, what the code chose |
|---|---|---|
| A1 | yes | "holds" = each non-empty line, right-trimmed, found as a substring, in order (greedy). Leading whitespace must match. Lines twice or with a prefix still `whole`; sorted or reversed order `slice` with 90 of 90; each line cut at a width `slice`. The lines come from the final tree (R9) |
| A2 | yes, to the letter | any counted access that delivers no line, searches included (R1). A stub followed by a slice → `slice` |
| A3 | yes | flag when another call's result in the window holds every line in order; class stays `none` until the hand-read. One leak: R8. JSON-escaped text not seen (R14) |
| A4 | yes, with R7 | the failed-write exemption is applied to shell writes too; a write with no result is not a write; "same message" = same record, whatever the order of blocks |
| A5 | yes | (b) an empty `t2.json` reads as "did not run"; "failed before any tool call" taken literally (R4). (ii) skips every record that carries a tool result unless it is preserved, so a result written again after the boundary is skipped (R3b). N of N → out; 0 < n < N listed |
| A6 | yes | all gates present and named. `delivered-unresolved` is a WARNING, not a stop. Second model printed. Short lines gate (R2) |
| A7 | partly | repeated name and lock: yes. Limit: yes for turn 1 and turn 2; the compaction call's exit code is not tested (R5); an invalid limit is no limit (R12) |
| A8 | not code | a step of the hand-read; nothing in the reader lists the shell commands before a counted `whole`. Printing them per arm would make the step short |

## The new parts, attacked

- **Line-in-order test.** A false `whole` needs every one of 87 long lines in order; I found one route, R8. `grep -n ''`, the file twice, CRLF, trailing blanks, a number glued to each line, a result in two blocks split inside a line, a block list with an image → `whole`. `sort`, `tac`, halves swapped → `slice`. `cut -c1-80` (40 lines), `fold` (48), fences removed (88), only the three short lines (3), leading blanks stripped (84), colour codes (48), HTML-escaped (78), squeezed blanks (84) → `slice`. `rev` → `none`. `diff /dev/null <file>` → `none` with the flag. A real whole delivery classed `slice` needs the tool to change the text inside lines (tabs: the file has none; a width cut: the longest line is 621).
- **`attempted`.** A real `slice` cannot land there (one line is enough). A real `none` lands there (R1). An error result that still holds the text is `slice` or `whole`.
- **Boundary number.** Launcher and reader count with the same `boundary.py`, so an off-by-one from a turn-1 boundary is not reachable; a wrong number in the status would cut at the wrong boundary in silence.
- **Launcher.** The binary is looked up once with `command -v` and run through `perl … exec`: same lookup as before, same environment, stdin still the null device (the stub logs it), the alarm survives the exec, exit code 142.

## The pilot check as the only gate

| A real pilot differs in | Outcome |
|---|---|
| read results in a format the reader cannot match (cut lines, escaped text, a reference to a saved file) | `PILOT NOT OK`, (iv) not `whole` |
| turn 1 read the rules through a glob or a script | `PILOT NOT OK`, (iv) `none`; WARNING if delivered whole |
| no boundary, or a boundary only in the stream | `PILOT NOT OK` |
| turn 1 compacted by itself | handled; cut number 2 printed |
| compaction did not shrink the context | printed "(shrank: False)" — **silent as a gate** (R3c) |
| session id changes on resume, or two transcripts | `PILOT NOT OK` (may be the tool's normal behaviour, R15) |
| turn-2 prompt recorded wrapped | `PILOT NOT OK` (R15); as a block list: handled |
| preserved records present and found | counted; `PILOT NOT OK` if they hold a line |
| preserved records named, not in the file, or the field in another shape | printed numbers — **silent** (R3a) |
| preserved field under another name | printed "fields present False" — **silent** (R3d) |
| summary holds a fence or a table rule | `PILOT NOT OK`, false stop (R2) |
| instruction record after the boundary carries the sentinel text | `PILOT NOT OK`, false stop (R2) |
| rules re-attached as an attachment record | counted; `PILOT NOT OK` |
| rules re-attached as a new result record, another record type, a text block beside a result | `0 of 90` — **silent** (R3b) |
| reference-only attachment about the rules file | printed under "records about the rules file itself" |
| summary written by a second model on the main chain | `PILOT NOT OK` (R15) |
| second model in usage only | printed, not a stop (as ruled) |
| attachment naming a foreign path, or of a foreign type | first: `PILOT NOT OK`; second: printed `foreign_attachment_types` |
| turn 2 answers "unchanged" on a re-read | `PILOT NOT OK` (`attempted`) |
| turn 2 only searches the rules | `PILOT NOT OK` with the wrong reason (R1) |
| turn 2 makes no tool call, or is denied a permission | `PILOT NOT OK` |
| turn 2 never re-reads (likely in C) | `PILOT OK`; what a re-read returns stays unknown until the six |

## The two scripts and the disclosure search

- `./selftest.sh`, own scratch root: exit 0, 400 lines, byte-equal to `03c_selftest.txt`, 247 PASS lines, "0 mismatches", nothing on stderr.
- `./dryrun.sh`, own scratch root: exit 0, 309 lines against 309. The 40 differing lines are the order of the stub's call lines from arms run in parallel and one "elapsed" line; sorted, only the elapsed line differs. The stub guard lines are there. The count of project folders in the tool's configuration was the same before and after. No `__pycache__` in the task folder.
- Disclosure search over the task folder, `local.env` left out (it is git-ignored and is the probe: 3 hits there): user name, host names, home prefix, temp prefixes, base folder name, configuration folder name, mail domain, session-id prefixes, package-manager prefix, uuid shapes, hex runs of 16 or more. Hits: five lines in `certificate.py`, `mask.sh`, `selftest.sh`, `03c_selftest.txt` naming the operating system's temp link in general terms, no user or session part; three hex values in `03d_dryrun.txt`, two commit ids of the public repo and the sha1 of the added line. No machine value.

## The designer's two decisions

- **The probe arm, dropped.** Not a mistake, with one thing to write down. The reason given holds: a probe that read one file would be re-attached that file, so it would not show what the pilot's arm gets. What the probe would have shown is now caught by `attempted` and a pilot stop. The gap: a C pilot that never re-reads cannot show it, so the first sight of the tool's answer to a re-read may be in the six. If the tool withholds, the arms that re-read leave (i), and those are mostly L arms if the line works: the round ends under-powered, not wrong. Name that outcome in `02_tasks.md` before the six ("fewer than two eligible arms in a condition = not tested").
- **The alarm does not kill children.** Acceptable. For turn 1 and turn 2 the arm is out anyway and the cost is processes left running. The gap is not the children; it is R5, where the killed call is the compaction and the arm goes on.

## Not established

- What the real tool records after a compaction under `-p`: whether the instruction record carries the file's text, in what shape a recently read file comes back, the real shape and name of the preserved fields in this version. I worked on the builder's structure-only account.
- Whether a real assistant record ever holds two tool calls (R7c).
- What a re-read of an already read file returns after a compaction.
- Whether the summary record names a second model on the main chain (R15).
- What children the real binary leaves when killed by the alarm.
- That the trees for the six build: I did not build in `<scratchpad>/r214`.
- N9–N11 of the first pass were not re-run.

## What a human reads by eye in the pilot's output

Read these even when the last line is `PILOT OK`. With R2 and R3 fixed, only 1, 5 and 6 remain.

1. `(iv) turn-1 restore: whole`, and in the access list the form and `90/90` — one plain read, not a shell detour.
2. `(shrank: True)` on the token line, with two numbers that are far apart.
3. `preserved across the boundary`: "fields present" both False and "uuids listed 0", or else "records found" equal to the number listed (halve it if both lists are present). Any other pair is a stop.
4. `0 of 90 non-empty lines` and "carried by: no record". If it says n > 0 with "(0 of them 20+ characters)", it is R2, not a hand-back: note it and go on to the ruling.
5. `records about the rules file itself`: "none", or a line that says what the tool attached; and `foreign_attachment_types` empty in the "after boundary" line. Anything named here is the tool handing something back that the count may not see.
6. `(i) after the boundary` and the access list of turn 2: if the pilot re-read, the class and the lines delivered say what the tool answers to a re-read; if `attempted`, look at the form before believing "withheld" (R1). No `WARNING`.
7. `second model in usage` — write the value down; it is not a stop.
