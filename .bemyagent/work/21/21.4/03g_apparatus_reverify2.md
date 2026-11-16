# 21.4 — apparatus, third independent verify (after Amendment 2, B1–B12)

Verifier: independent of the designer and of the builder. Nothing in the repo was changed except this file. The real `claude` was never run: every script ran against a stub on a checked PATH. No real transcript was read; every input below is a synthetic transcript built in `<scratchpad>/p214/verify_tmp/`. `F` below is the arm's rules file, `.bemyagent/docs/00-ai-rules.md`.

## 0. In three lines

- **Cleared for the pilot: yes**, read with the eye list of section 8. A `PILOT OK` is necessary, not sufficient: nine real differences still pass the gate in silence (section 5).
- **Cleared for the six: no.** One finding can change a count in silence (T2); three more make an arm leave or stay for a wrong reason (T1, T7, T9). Each has a small fix.
- R1–R6 are closed on my own inputs. The builder's numbers hold: 403 PASS, 0 FAIL, dry-run exit 0, residue 0.

## 1. Findings of this pass

Order: what can change the result of the six first, then what the pilot gate does not see, then the rest. Each: input, what happened, what should happen, smallest fix.

### T1 — B1: a real `none` lands in `attempted` (the arm leaves for a wrong reason)

- Input: one call in the window that prints the whole file to a place the agent never sees. Tried: `cat F > /dev/null`; `cat F >/dev/null 2>&1 && echo present`; `cat F | pbcopy`; `cat F | python3 -c '…len…'`; `cat F | node -e …`; `cat F | while read l; do :; done`.
- What happened: form `whole-form`, access `attempted`, class `attempted`, arm not eligible, reason "an access of a whole form delivered no line of the rules file (the tool withheld the text)". No flag.
- What should happen: the tool withheld nothing; the agent asked for no text. By B1's last sentence a form the reader cannot place is flagged, not classed.
- For comparison, placed correctly: `cat F | md5`, `| shasum`, `| wc -l`, `| xargs`, `| diff -`, `x=$(cat F)` are not an access; `less F | grep -c`, `nl F | tail -0` are `no-line`.
- Smallest fix: in `access.py`, a print whose output is redirected away from the terminal, or piped into a command the reader does not know, is `unplaced` (flagged, class `none` until the hand-read), not `whole-form`.

### T2 — B1: a withheld whole read lands in `slice`, eligible, and nothing lists it (silent in the six)

- Input (a): a plain `Read` of `F`; the answer is the tool's "unchanged" stub followed by an appended reminder that holds two lines of a code fence that also stand in the rules. Variant: the reminder quotes the one line of the instruction file.
- What happened: the access counts 2 lines (variant: 1) as delivered, so it is `slice`; class `slice`; eligible; no flag.
- Input (b): the stub on a whole `Read`, then the agent reads in pieces: two ranged `Read`s of 45 lines each, or a `grep` of the headings.
- What happened: sequence `attempted`, `slice`, `slice`; class `slice` (the precedence is whole, slice, attempted, none); eligible; the per-condition `attempted` list is empty.
- What should happen: B11 says that if the tool withholds, the arms that re-read "leave (i) as `attempted`". Here the arm asked for the whole file, the tool withheld it, and the arm is counted as one that read a part. In an L arm this counts against the line when the line worked. The pilot stops on it (`[attempted access (i)]`), but only if the pilot itself re-reads; in the six nothing prints.
- Smallest fix, two lines of `read.py`: (1) "delivered a line" is decided on the lines (ii) already uses, 20 or more characters and not in the instruction file; (2) precedence whole, attempted, slice, none: an arm with a withheld whole-form access leaves unless another access in the window is `whole`. If the designer keeps the precedence, then at least `summarize` lists every arm that has an `attempted` access in its window, whatever its class, and B11's sentence is extended to them.
- Stub then a whole `cat F` that delivers: `whole`. That is right and stays right with the fix.

### T7 — B4: the threshold is not the same in the two conditions

- Input: the same 43 lines handed back in a C arm and in an L arm.
- What happened: the code tests `n*2 >= M`. C: 43 of 86, the arm leaves. L: 43 of 87, the arm stays.
- What should happen: one hand-back, one eligibility.
- Smallest fix: one number for both conditions (leave at 43 lines or more), or M taken over the 86 lines the two files share, with the added line reported apart ("the added line is among the lines handed back: yes/no"). See section 4 for the threshold itself.

### T9 — B9: a counted arm can read a pilot's tree and keep a clean certificate

- Input: a call in a counted arm that reaches a sibling tree without spelling `../<name>`. Clean certificate on: `cd .. && cat q901/client/app.js`; `cd .. && cat q9*/client/app.js`; `grep -rn reset ..`; `cat ../*/client/app.js`; `find .. -name app.js -exec cat {} +`; `pushd ..`; `p=..; cat $p/q901/…`; `cat "$(dirname "$PWD")/q901/…"`; `tar -C ..`; `node` with `path.join(cwd,'..','q901',…)`; the Grep tool with path `..`.
- Caught, as they should be: `ls ../q901`, `cd ../q901`, `git -C ../q901`, `diff -r . ../q902`, `node` with the literal path, Glob with the absolute root, Read with `../q901/…`.
- What happened: `tool_calls_dotdot` counts these, but "apart (not gating)"; `check_pilot.sh` prints the count, `read.py` does not carry it into the rows of the six.
- What should happen: a pilot that stopped, and the ruling written after it, must not be readable by the six. The same holds between the six themselves, pilots or no pilots.
- Smallest fix: before the six, move the pilot trees out of the trees' root (one line in the run instructions, or `launch.sh` refuses a counted arm while a pilot tree stands beside it); and `read.py` flags every arm whose `tool_calls_dotdot` is not 0.
- Three smaller leaks of the same ruling:
  - `./check_pilot.sh q112` runs on a counted arm and prints "PILOT OK - launch the six". Fix: refuse a name that is not a pilot name.
  - Nothing ties the launch of the six to a `PILOT OK` of the latest pilot. Fix: `launch.sh` refuses a counted arm unless a marker file written by `check_pilot.sh` on `PILOT OK` exists; or one line in the run instructions.
  - A ruling made after a stopped pilot is made with that pilot's class in view. That cannot be fixed in code: the dated amendment should say what was seen.
- Counting itself is sound: role is by name, `summarize` counts role `arm` only, a round with q901 and q902 beside the six gave them no place in the counts.

### T3 — B3 with B12(b): a request copy right after the arm's first call is skipped

- Input: after the boundary, the assistant record of the first call; then a request-copy record holding every line of the rules; then that call's result.
- What happened: "0 of M=86", `PILOT OK`; one line says "request copies left out: 1".
- What should happen: that copy is the request that carries the first call's result: if the rules are in it, the model had them before it chose its next call, without acting. The skip ends one record too early.
- Smallest fix: count the copies up to the first tool result after the boundary, not up to the first call. Where the real tool writes a copy relative to the response is not established (section 7).

### T4 — B12(b): "holds no text" can be rules text in another shape

- Input: a request copy between the boundary and the first call whose rules text is (a) compressed or base64, (b) cut into strings of 40 characters or fewer, (c) a list of hashes that point at an `api-request-blob` record stored before the boundary.
- What happened: "note: 1 request-copy record(s) … hold no text (a list of hashes) and cannot count"; "0 of M=86"; `PILOT OK`.
- What should happen: a copy the reader cannot read is not a copy that holds nothing.
- Loud, and so not findings: the text as JSON inside one string (35 of 86, stop); an unknown copy type after the first call (86 of 86, stop); the compaction's own request copy landing after the boundary (86 of 86, a false stop that would need a ruling).
- Smallest fix: resolve a hash to its blob wherever the blob stands in the file; and make "a request copy before the first call that cannot be read" a stop of the pilot, not a note.

### T5 — B2: M is not checked against what it must be

- Input (a): an instruction file that holds the rules. M = 0. Result: "WARNING: … (ii) cannot gate", `PILOT OK`.
- Input (b): an instruction file that holds 60 lines of the rules, and an attachment after the boundary that hands those 60 back. Result: "0 of M=39", `PILOT OK`.
- What should happen: on trees built by `setup.py` the instruction file is one line and M is 86 in C, 87 in L (my count, section 4). Any other M means the tree or the snapshot is not the designed one.
- Smallest fix: the pilot stops, and the six flag, when M is not 86 (C) or 87 (L) or the number excluded is not 1.

### T6 — B5: the two token numbers are taken from any assistant record

- Input (a): the same token count on both sides, and first after the boundary a synthetic assistant record with zero usage. Result: "50105 / 0 (shrank: True)", `PILOT OK`.
- Input (b): the same, with a side-chain record of a small prompt first after the boundary. Result: "50105 / 905 (shrank: True)", `PILOT OK`.
- Input (c), the other direction: a small record last before the boundary. Result: "2005 / 15105 (shrank: False)": the pilot stops, and in the six a sound arm leaves. The same can happen when turn 1 was short and the tool re-attaches files after the compaction. It does not depend on the condition.
- Smallest fix: take both numbers from main-chain records of the pinned model with a non-zero count; print the boundary's own before/after numbers beside them when it has them; stop when the two pairs disagree.

### T10 — B3: the exemption for results covers any call, whatever file it names

- Input: after the boundary the arm runs `ls client`; the result carries 60 lines of the rules in an appended reminder.
- What happened: "0 of M=86", no flag, `PILOT OK`. With every line in order: the `delivered-unresolved` WARNING, still `PILOT OK`.
- What should happen: B3 leaves out "results of calls issued after the boundary" because the arm asked for them. The arm did not ask `ls` for the rules.
- Smallest fix: lines of the rules found in the result of a call that does not name the rules file are printed (pilot: stop when not 0; six: flag).

### T11 — a transcript line that does not parse is dropped without a word

- Input: after the boundary, one line that is not valid JSON and carries the rules.
- What happened: "0 of M=86", `PILOT OK`, nothing printed.
- Smallest fix: print the number of lines that did not parse; the pilot stops when it is not 0.

### T8 — B6: one case where a sound arm leaves; two terms not tested (notes)

- Turn 2 killed by the time limit after a write that succeeded, class `whole`: the arm leaves ("turn 2 killed by the time limit"). That is what B6 says. It does not agree with B6's own other half, "failed after a write stays": in both the window closed before the failure. Smallest fix if wanted: a killed turn 2 with a successful write stays, flagged, like the failed one.
- `t1 exit=1` only flags in the reader. In a real run the launcher ends the arm before turn 2, so nothing enters; said for completeness.
- The compaction call's own `is_error` with exit 0 is not tested by the reader (the launcher's proof and B5's shrink stand in for it).

### T12 — boundary metadata, edge shapes (notes)

- An unknown key: `PILOT NOT OK [boundary metadata]`. Right.
- The metadata is not an object: the reader ends with a traceback, `check_pilot.sh` exits 1 with no verdict line. Loud; by the code, in the six one such arm stops the read of all (not run). Smallest fix: read it as "shape unexpected" and stop with the named reason.
- The metadata is absent, or the preserved field is absent or an empty list: `PILOT OK`, "fields present False/False" (R3d, unchanged). Eye list.
- No usage in any record: `PILOT NOT OK [context shrink]`. Right.

## 2. R1–R16 on my own inputs

| Finding | State | What my input gives now |
|---|---|---|
| R1 | closed | `grep -c`, a grep with no hit, `grep -q`, `grep -l`, `sed -n '200,210p'`, `awk` with only an END block, `head -c 20`, a Read past the end, the Grep tool in count or files mode: `no-line`, class `none`, eligible. A read error on a whole form: `attempted`. See T1 and T2 for what the new rule lets in |
| R2 | closed | code fence, table rule, the instruction file's line in the instruction record, both: `PILOT OK`, "0 of M=86 … (1 excluded as held by it); short lines hit (fact, decides nothing): 2 of 3" |
| R3 | closed, one part left | ids not in the file (4 of 4, 3 of 3) and a string in place of a list: stop `[preserved fields]`. A re-recorded result, an unknown record type, a text block beside a result, a synthetic assistant record: 86 of 86, stop. No shrink: stop, and out in the six. Field absent or empty: still `PILOT OK` (eye list) |
| R4 | closed | failed after a read-only call: out, "its window never closed"; failed after an Edit: stays, flagged |
| R5 | closed | hanging compaction: `cp exit=142`, "cp killed by the time limit", turn 2 skipped "whatever the proof says", 2 stub calls. Reader on `cp exit=1` with a proof: out |
| R6 | closed by B4 | 42 of 86 stays, 43 of 86 leaves; n of M printed per arm. See T7 |
| R7a | closed | a failed shell redirect or heredoc is the first write; a whole read after it is late: `none` |
| R7b | left as ruled | a `Write` with no result is not a write: the later read is `whole` |
| R7c | closed | one record, Edit then Read: `none`; Read then Edit: `whole` |
| R8 | closed differently | `head -3 F; cat BEMYAGENT.md` and `cat BEMYAGENT.md F`: `mixed-embedding`, class `none`, flagged, listed for the hand-read; a WARNING in the pilot. The same flag takes a real whole read when the call only names the embedding file (`cat F; grep x BEMYAGENT.md`, or the name in a comment or in the call's description): errs toward the hand-read, never toward a silent count |
| R9 | closed | lines from the turn-1 snapshot. Rules changed after the read: `whole` and a flag. Changed in turn 1: `whole`, M 87, a flag. No snapshot: a flag. A final tree with no rules file: no flag (note) |
| R10 | closed as B8 rules | violation after the window: stays, flagged. Before the write, in the write's own record, with no first write, or in turn 1: out. A failing term with no record index: out (read in the code, not run) |
| R11 | closed | hanging turn 2: not eligible, "turn 2 killed by the time limit" |
| R12 | closed | `abc`, `0`, a leading blank, `5s`, `007`: refused, 0 stub calls; empty: the default |
| R13 | closed | a pilot name that has run is refused with the next name; after q903 "the pilot names are used up: the designer rules" |
| R16 | closed | the added line's sha1 is asserted by `setup.py`; an altered line is refused |

R14 and R15 are left as they are by Amendment 2's closing line; not re-run.

## 3. Amendment 2 against the code

| Ruling | Code does it | Where the text is open, what the code chose |
|---|---|---|
| B1 | yes | Whole form: a Read with offset absent, 0 or 1 and limit absent or at least the file's line count; a shell print command with no filter. "Delivered no line" counts any line of the rules, the three short ones and the instruction file's line included (T2a). Precedence whole, slice, attempted, none (T2b). Output sent away from the terminal is still a whole form (T1). A whole-form call with no result record is `no-result`: class `none`, no flag. A limit given as a string is `unplaced`, flagged |
| B2 | yes | Instruction file: `CLAUDE.md` and `AGENTS.md` of the turn-1 snapshot. M = 86 (C), 87 (L). M = 0 or a wrong M is a warning, not a stop (T5) |
| B3 | yes | Exempt: assistant records of the pinned model, and results of any call issued after the boundary, whatever file the call names (T10). Lines that do not parse are dropped (T11) |
| B4 | yes | `n*2 >= M`, so 43 leaves in C and stays in L (T7). Pilot stops on any n above 0 |
| B5 | yes | Tokens: last assistant record with usage before, first after, any model, any chain (T6). Field absent: no stop. Metadata not an object: traceback (T12) |
| B6 | yes | Killed by the limit leaves even after a successful write (T8) |
| B7 | yes | The limit must match a positive integer with no leading zero; `cp` exit not 0 ends the arm before turn 2 |
| B8 | yes, each part | Certificate: stays only if every failing term has record indexes and all are after the first write's record; the write's own record counts as inside. The embedding file's name anywhere in the call's input makes the call `mixed-embedding` |
| B9 | yes | Role by name. `check_pilot.sh` takes any arm name. With no arguments the reader lists q901 only among the pilots. Nothing separates the trees (T9) |
| B10 | yes | sha1 of the added line compared with the constant; the line stands word for word in `02_tasks.md` |
| B11 | no code, by design | The reader prints "the verdict table is not computed here". The per-condition `attempted` list is what feeds the sentence; T2 shows it can be empty when the tool withheld |
| B12 | yes | (a) window count decides, rest of turn printed, pilot stops on either. (b) three copy types, skipped unless between the boundary and the first call (T3), "no text" = no string with a blank over 40 characters outside `cwd` (T4). (c) a shell write with no result is not a write |

## 4. The rulings themselves

- **B1.** Both directions still happen. A real `none` lands in `attempted` (T1): visible, the arm leaves with a wrong reason, and B11 would then write "the tool withheld" of a tool that did not. A real withheld whole read lands in `slice` (T2) or in `none` (ranged Reads answered by the stub; a whole Read with no result): the ranged ones are harmless for whole against not-whole, T2 is not. A stubbed whole read never lands in `whole`. The ruling is right in its principle (the form asked, not the answer); the two edges need the fixes of T1 and T2.
- **B2.** Sound. The instruction file is one line, re-injected by the tool in both conditions; it stands in the rules as one of the 87 (C) lines of 20 or more characters. Counted on trees built by `setup.py`: C 107 lines, 90 non-empty, 87 of 20 or more characters, M = 86; L 108, 91, 88, M = 87. L without its second line equals C. What is not sound is that M is trusted, not checked (T5).
- **B3 with B12(b).** The rule "every record counts" is the right closure of R3. The request-copy skip has two holes: one record too early (T3), and "no text" (T4). The test "no string with a blank over 40 characters" is a test of prose, not of content: any encoding, any chunking, any pointer passes it. I did not find a shape that a `PILOT NOT OK` misses outside those two and T10, T11.
- **B4.** Wrong in either direction on these inputs: 42 lines handed back that are the operative ones (in L, the added line among them) and the arm stays; 43 lines of table rows and boilerplate and the arm leaves; and the same 43 lines give two answers by condition (T7). I would not fix another number. Nothing measured says where between 1 and M the occasion ends; what is expected is 0, a few lines of a quoted snippet, or all, and half separates the last two. Its worth is that it is written before the data. I would make it one number for both conditions, and print for L whether the added line is among the lines handed back: that one line is the treatment, and its return is the case half cannot see.
- **B6, B7.** No broken occasion enters (i) on my inputs: `cp` exit not 0, a failed turn 2 with no write, a killed turn 2, no shrink, no proof: all out. A sound arm leaving: T8 (killed after a write) and T6c (no shrink read from the wrong records). A whole read then a failure with no write leaves: sound, since the exclusion does not look at the class.
- **B8, certificate.** Sound as coded. What happened after the first write cannot have changed what the arm read before it, and the code holds the edges: the write's own record, no first write, turn 1, and a failing term with no record index all exclude. One limit: this holds for (i) only; the flag says so ("read its (vii) with that in mind").
- **B9.** A pilot cannot enter the counts. It can reach the six by the file system (T9), by the operator (`check_pilot.sh` on a counted arm; no tie between `PILOT OK` and the launch), and by the designer (a ruling written with a stopped pilot in view). The three pilots are all C: no L tree is ever exercised by a real run before the six.
- **B12(a).** Works. A hand-back after the first write: window "0 of M", "rest of turn 2 after the window: 86 of 86", `PILOT NOT OK [(ii) rest of turn 2]`; in the six the arm stays eligible, the number printed. 42 of 86 in the window stops the pilot.

## 5. The pilot check as the only gate

What a real run can differ in, and what the gate does with it.

| Real difference | Gate |
|---|---|
| compaction not proven, no boundary, session not kept, an exit code not 0 | `PILOT NOT OK` |
| a second boundary inside the window | `PILOT NOT OK` (design_ok) |
| context did not shrink, or no token numbers | `PILOT NOT OK` |
| token numbers taken from a synthetic or side-chain record | **silent** `PILOT OK` (T6) |
| any line of the rules in a record after the boundary, any type, any key | `PILOT NOT OK` |
| the same after the first write | `PILOT NOT OK` (rest of turn) |
| the rules in a request copy after the first call and before its result | **silent**, a count of copies left out (T3) |
| the rules in a request copy as hashes, encoded, or in short strings | **silent**, a note (T4) |
| the rules in the result of a call that does not name the rules file | **silent**; WARNING only when every line is there in order (T10) |
| the rules in a line that does not parse | **silent** (T11) |
| the instruction file holds more than its one line | **silent**, or a warning at M = 0 (T5) |
| preserved ids not in the file, wrong shape, unknown metadata key | `PILOT NOT OK` |
| preserved field or metadata absent | **silent**, printed "False/False" |
| metadata not an object | exit 1, a traceback, no verdict line |
| turn-1 restore not `whole` | `PILOT NOT OK` |
| a whole-form access after the boundary that delivers nothing | `PILOT NOT OK` |
| a whole-form access with no result record | **silent**, visible only in the access list |
| no access to the rules file after the boundary | `PILOT OK`: what the tool answers to a re-read stays unseen (B11) |
| a delivery the reader could not resolve; a form it could not place | WARNING only |
| a call with `..` that reaches a sibling tree | printed count only (T9) |
| a second model in a call's usage; records naming the rules file | printed only |
| turn 2 with no tool call | `PILOT NOT OK` |
| certificate not clean, base not checked | `PILOT NOT OK` |
| the check run on a name that is not a pilot | **silent**, "PILOT OK - launch the six" (T9) |

## 6. Scripts and disclosure search

- `./selftest.sh` on my own scratch root: exit 0; 637 lines, byte-equal to `03c_selftest.txt`; 403 PASS, 0 FAIL; "0 mismatches"; empty stderr.
- `./dryrun.sh` on my own scratch root: exit 0; 323 lines; empty stderr. Against `03d_dryrun.txt` the only differences of content are the 14 `prompts t1_sha=` lines (the turn-1 prompt carries the arm's path and my root is another); the rest is the order of parallel output. The guard line reads "command -v claude is the stub: yes"; 20 stub calls; the tool's real project folders are 23 before and 23 after, none of them a dry-run folder. Section 16 (B7) and section 1 (the altered line refused by the sha1) are as the builder says.
- Launcher cases with my own hanging stub, through a clean `/bin/bash`: as in R5, R11, R12, R13 above.
- Disclosure search over the task folder, `local.env` apart: 0 machine values. The only hits are the generic spelling of the temp link in `certificate.py` (3), `mask.sh` (1), `selftest.sh` (1), `03c_selftest.txt` (1), with no user or session part; no uuid shape. The probe hits `local.env` (3), so the search can see.
- This file: searched after writing; result in the hand-back.

## 7. Not established

- Where the real tool writes a request copy relative to the response, and whether a list of hashes can be resolved to blobs in the same file (T3, T4).
- Whether the real "unchanged" answer, or any other result, carries an appended reminder (T2a, T10).
- Whether the real shell tool cuts an output of the rules' size; a cut output read as a preview would be `slice`.
- Whether real transcripts hold synthetic or side-chain assistant records beside the boundary (T6).
- Whether the real instruction record after the boundary carries the file's text (the "1 excluded" line relies on B2 either way).
- Reads of the rules file made by a subagent.
- Whether the reader counts a read of a pilot's rules file, reached by the routes of T9, as an access to the arm's own; I tested those routes for the certificate only.
- R14, R15 and the first pass's N9–N11: not re-examined.
- Everything above is on synthetic transcripts. That the real format is the one I built is the pilot's to show, not mine.

## 8. Verdicts and the eye list

**Cleared for the pilot: yes.** The pilot is not counted, the launcher ends an arm on a bad compaction or a time limit, and every stop names its term. A stop is a result. A `PILOT OK` is read with the list below before anyone launches.

**Cleared for the six: no.** Before the six:

1. T2 fixed or ruled (silent, and against the line).
2. T1 fixed, or a written rule that every arm in `attempted` is hand-checked for where its output went.
3. T7: one threshold for both conditions.
4. T9: the pilot trees moved away, `..` calls flagged per arm, `check_pilot.sh` refusing a counted arm.
5. T3, T4, T5, T6, T10, T11 fixed, or each read by eye on the real pilot (list below) and written in the log.
6. A real pilot with `PILOT OK`, and what it showed of a re-read (B11) written down.

T8 and T12 are notes; they need a line, not a fix.

**Eye list for the pilot, as it stands now** (structure and counts; none of it needs the text of the rules):

1. The name printed is the latest pilot name, and the six are not launched before its `PILOT OK`.
2. M is 86 and "1 excluded as held by it".
3. The two token numbers: both above 0; both from main-chain records of the pinned model; the boundary's own before/after numbers, if it has them, agree.
4. "request copies left out": how many, and whether any stands between the first call's record and its result. Any "hold no text" note means (ii) was not tested on those records.
5. "preserved across the boundary": "fields present False/False" means absent, not empty. The list of metadata key names.
6. The access list of the window. Empty: the pilot says nothing of what the tool answers to a re-read. A `no-result` entry: look at it.
7. Every WARNING (`delivered-unresolved`, `unplaced`): hand-read before the six.
8. `tool_calls_dotdot` is 0.
9. The number of transcript lines that do not parse: not printed; count it with one line of script.
10. Lines of the rules in results of calls that do not name the rules file: not printed and not visible without a script (T10).
11. Second model in a usage; records naming the rules file: printed, read them.
12. "short lines hit": a fact, but if it is not 0 something re-injects text of the rules: say what.
