# 21.4 — the pilot's path after Amendment 3: fourth pass of the verifier

Scope: only the pilot's path (`q901`) after Amendment 3 (C1–C9). This pass does not clear the six.
Everything below was run on my own scratch root (`<scratchpad>/p214/verify_tmp`, called `<V>`), with my stub
first on a checked PATH and my own config folder. The real `claude` was never run. No real transcript and no
real output file was read. Nothing was built in `<scratchpad>/r214` or `<scratchpad>/r214p`, nothing was touched
in `<scratchpad>/r211`. Nothing in the repo was changed except this file.

## 1. Findings

None of them makes the launch of `q901` unsafe. G1–G3 and X1 matter for the six; P1 and the minor ones are
defects of form. Each is given as input, what happened, what should happen, smallest change.

**G1 — the marker of an earlier pilot survives a later pilot that stops.**
Input: `pilot_ok.q901` present; `q902` built, launched (the stub does not compact), `check_pilot.sh q902`.
Happened: `PILOT NOT OK` (12 reasons), exit 1, and `pilot_ok.q901` stays. After that `launch.sh q113` ran
(3 stub calls) and `setup.py six q114` built. The marker also says nothing about which version of the reader
wrote it.
Should happen: the gate reflects the latest check of any pilot.
Smallest change: `check_pilot.sh` removes every `pilot_ok.*` in the outputs folder at its start, before the two
scripts run (today it removes only its own pilot's marker, and only after them).

**G2 — any file named `pilot_ok.*` opens both gates.**
Input: an empty file `pilot_ok.x` in a fresh outputs folder, then `launch.sh q115`.
Happened: the counted arm ran (3 stub calls). Neither `launch.sh` nor `setup.py six` reads the content or the
name after the dot.
Should happen: the gate opens only on a marker written by the check.
Smallest change: both gates require the content `PILOT OK <name>` with `<name>` one of the pilot names.

**G3 — `R214_PILOTS` set by hand, together with `R214P_ROOT`, turns a counted arm into a pilot.**
Input and what happened, by runs:
- `R214_PILOTS=q112 check_pilot.sh q112`, nothing else set: `PILOT NOT OK` (the tree is looked for in the pilots'
  root). Alone the variable opens nothing.
- `R214_PILOTS=q114 launch.sh q114` without a marker: "no tree at ... (skipped)". Alone it opens nothing.
- the same two with `R214P_ROOT` pointing at the root of the six: `check_pilot.sh q112` gives `PILOT OK` and
  writes `pilot_ok.q112` for a counted arm; `launch.sh q114` launches a counted arm with no marker (3 stub calls).
- `R214_PILOTS=q902 read.py`: `q901` is listed with role `arm`, condition C, among the C arms. It is not
  eligible only because its tree is not found in the root of the six.
- `setup.py` does not honour the variable. `setup.py pilots q112` prints "built 0 arms" and does not say that
  the name is not a pilot's.
Should happen: a test-only override cannot move a counted name across the gate, and its use is visible.
Smallest change: the override is refused when it names one of `q112`–`q117` or leaves out one of `q901`–`q903`
unless a second, test-only variable is set; every script that honours it prints one line saying so. Before the
real launch the environment line in section 7 must print nothing.

**X1 — the rules handed back in the result of a write call are not seen (C7).**
Input: the 86 lines of K appended to the result of (a) the first write call itself, (b) a failed `Edit` inside
the window, before the first write that succeeds. Neither call names the rules file.
Happened: `PILOT OK`, n = 0, rest of turn 0, nothing printed.
Should happen: C7 says the lines of K in the result of a call inside the window that does not name the rules
file stop the pilot.
Cause: `rules_in_other_results` in `read.py` skips every call whose name is in `access.WRITE_TOOLS`.
Smallest change: drop that exclusion; a write that names the rules file is already skipped by the test on the
target's name.

**P1 — a transcript line that is valid JSON but not an object ends in two tracebacks.**
Input: one line holding a JSON string (also tried: a JSON list) in the pilot's transcript.
Happened: `certificate.py` stops with a traceback at `is_prompt_record` (line 78, `.get` on a string), then the
verdict part of `check_pilot.sh` stops with a second traceback on the empty certificate file. Exit 1, the marker
is removed, no verdict line.
Should happen: it stops with the named check (`[unparsed lines]`), as C8 asks, with no traceback.
Smallest change: `certificate.py` drops records that are not objects where it loads the transcript, as `read.py`
does, and counts them with the unparsed lines.

**Minor.**
- m1. `launch.sh` exits 0 and prints "all arms finished" when it refuses a counted arm. Smallest change: exit 1
  when any arm was refused.
- m2. `setup.py` reads `BMA_SCRATCH` from the environment and does not source `local.env`. Run bare it ends in
  `KeyError: 'BMA_SCRATCH'` with a traceback; nothing is built. The build line in section 7 avoids it. Smallest
  change: one clear message, or source `local.env` as the shell scripts do.
- m3. A check interrupted between its two scripts leaves the old marker (read in the code, not run). The change
  of G1 removes it.
- m4. T4, rules as JSON inside one string of a request copy: counted 35 of 86, with no "unreadable" flag. It stops
  the pilot (n > 0). For the six 35 is under the threshold of 43: an undercount to settle in the pass on the six.
- m5. T9, the parent reached through `cat "$(dirname "$PWD")/..."`: no stop and `tool_calls_dotdot` stays 0.
  With the pilots in their own root this route reaches only pilot trees.
- m6. A pilot whose transcript holds no usage numbers at all passes: the line prints `None / None` with no
  `(shrank ...)` suffix, and the boundary's own numbers decide alone. This is what C6 says; it is on the eye list.

## 2. Point 1 — the pilot's tree and the three calls

`python3 setup.py pilots q901` on my root builds `<V>/p4/r214p/q901`.

| Check | Result |
|---|---|
| rules file | byte-equal to the repo's, 107 lines |
| instruction file | `CLAUDE.md`, one line, the seeded sentence; no `AGENTS.md` |
| K, threshold | 86, 43 |
| git state of the tree | 2 commits, clean |
| against my C seed from before the amendment | `diff -r` silent |
| where `launch.sh` looks | the pilots' root for the three pilot names, the root of the six for the counted names |
| the three calls | cwd is the pilot's tree in all three |
| flags | `-p <prompt> [--resume <session>] --model sonnet --output-format json or stream-json [--verbose] --allowedTools Read Write Edit Bash Glob Grep` |
| prompts | equal to the three prompt files; hashes of the compaction and turn-2 prompts identical to the earlier passes |
| stdin | the null device |
| outputs, lock, status, snapshots | in the outputs folder (`<V>/p4/r214_out`), where `check_pilot.sh` and `read.py` look |
| transcript | in the config's project folder named after the pilot's path |
| `check_pilot.sh q901` | `PILOT OK`, exit 0, marker `pilot_ok.q901` holding `PILOT OK q901`, `q901.cert.json` and `q901.read.json` written beside it |

## 3. Point 2 — the gates between the pilot and the six

| Input | Result |
|---|---|
| `check_pilot.sh q112` | refused, "it is not a pilot", exit 2, nothing written |
| `check_pilot.sh q904` | refused, exit 2 |
| `launch.sh q112`, no marker | refused, 0 stub calls, but exit 0 (m1) |
| `setup.py six q112`, no marker | refused, exit 1 |
| `launch.sh`, no argument | runs nothing |
| marker present: `setup.py six q112 q113 q115` | builds in the root of the six, the L assertions printed |
| marker present: `launch.sh q112` | 3 stub calls from the arm's tree |
| same pilot checked again, one unparsable line added | stop `[unparsed lines] 1`, exit 1, marker removed; `launch.sh q113` and `setup.py six q114` refused |
| same pilot, healthy again | `PILOT OK`, marker rewritten |
| same pilot, its project folder emptied | `PILOT NOT OK` (8 reasons), marker removed |
| same pilot, `t1.json` not valid | `PILOT NOT OK`, marker removed |
| marker for `q901`, then `q902` checked and stopping | marker stays, the six open: G1 |
| any file `pilot_ok.x` | the six open: G2 |
| `R214_PILOTS` by hand | alone opens nothing; with `R214P_ROOT` it does: G3 |

## 4. Point 3 — T1–T12 through `check_pilot.sh q901` only

Baseline (slice, whole read, no access): `PILOT OK`, marker written.

| Input | Result | Where it shows |
|---|---|---|
| T1 six shell forms that read the file and print nothing | silent, `PILOT OK` | class `none`, access listed as unplaced 0/90, WARNING "a form the reader cannot place" |
| T2a stub answer to a Read, alone or with a reminder | stop | `[attempted access (i)]` |
| T2b stub answer, then ranged Reads or a heading search | stop | `[attempted access (i)]` |
| T3 request copy holding the rules, before the first call or before its result | stop, n = 86 | "carried by: api-request-blob ... (86)" |
| T4 copy compressed | stop | `[request copies] 1 ... cannot be read as text` |
| T4 copy split into short pieces | stop | n = 10 and unreadable 1 |
| T4 copy as JSON inside one string | stop, n = 35 | undercount, m4 |
| T4 hash list, one hash not resolved | stop | n = 86 and unreadable 1 |
| T4 hash list, all resolved | stop | n = 86 |
| T5 instruction file holds the rules | stop | `[instruction file] it holds 86 line(s) of K` |
| T5 instruction file holds 60 lines | stop | x = 47 |
| T5 60 lines handed back | stop | n = 47 |
| T6 record with zero usage first, side-chain record first, or no shrink | stop | `[token numbers] ... they disagree` |
| T6 small record last before the boundary | stop | `[token numbers]` |
| T7 43 lines handed back | stop | n = 42 |
| T7 one line handed back | stop | n = 1 |
| T8 turn 2 killed after a write | stop | `[exit codes] t2 exit code is 142`, flag C9 |
| T9 ten routes through `..` | silent, `PILOT OK` | `tool_calls_dotdot: 1` in the "after boundary" line |
| T9 `dirname` of the working folder | silent, count 0 | not seen, m5 |
| T9 absolute path of a sibling tree | stop | `[certificate clean] no_tool_call_naming_apparatus` |
| T10 a listing whose result carries 60 lines | stop | `[rules in another call's result]`, 47 |
| T10 a listing whose result carries all lines | stop | 86, plus WARNING delivered-unresolved |
| T10 the rules in a write call's result | silent, `PILOT OK` | nothing printed: X1 |
| T11 a line that does not parse | stop | `[unparsed lines] 1` |
| T11 a line that is JSON but not an object | stops by traceback | P1 |
| T11 blank lines, trailing newlines | silent, `PILOT OK` | not counted, correct |
| T12 unknown metadata key | stop | `[boundary metadata] keys the reader does not know` |
| T12 metadata not an object | stop | named message, no traceback |
| T12 metadata absent | stop | named message |
| T12 no usage anywhere | silent, `PILOT OK` | `None / None` printed: m6 |

Silent and wrong: one input, X1. Silent and printed for the eye: T1, T9 (`..`), T12 without usage. Silent and
not printed: the `dirname` route.

## 5. False stops to expect on a healthy real pilot

All run on synthetic transcripts. Whether the real tool writes any of these records is not established here.

| Input | Result |
|---|---|
| shape-only request copy between the boundary and the first tool result | stop `[request copies]`: the builder's statement is confirmed |
| the same copy before the boundary, or after the first tool result | no stop ("request copies left out: 1") |
| hash-list copy in the span whose blobs are not in the file | stop |
| hash-list copy whose blobs are in the file and hold no rules; readable copy with no rules | no stop |
| the compaction's own request copy written after the boundary, holding the turn-1 read | stop, n = 86, with the Pivot sentence "the rules come back without the arm acting" |
| assistant records grow while the boundary's numbers shrink | stop `[token numbers] ... disagree` |
| boundary without its post number, records shrink | no stop |
| boundary without its post number, records grow | stop `[context shrink]` |
| a search across the tree whose result holds one rules line | stop `[rules in another call's result]` |
| a files-only search, a listing of the docs folder | no stop |
| a Read or `cat` of `BEMYAGENT.md` inside the window | stop (86), WARNING delivered-unresolved |
| a Read of the rules file answered "unchanged" by the tool | stop `[attempted access (i)]` |
| an attachment naming a path under the home or the system temp folder, outside the tree | stop `no_attachment_naming_foreign_path` |
| an instructions record listing a user-level file | stop `no_instruction_file_outside_arm` |
| an assistant record of another model on the main chain | stop `model_pinned_on_main_chain` |
| a metadata key the reader does not know | stop |
| session changed by `--resume`, compaction not proven | the designed stops |
| other record types after the boundary, a skill listing without paths | no stop |

Two of these need care when they happen. The row of the compaction's own copy prints a Pivot conclusion that would be wrong if taken at face value: when n > 0, read the "carried by"
line before any ruling. The token rows are plausible on a short turn 1 if the boundary's post number counts only
what the compaction produced while the records also count the fixed prompt and the tools; what the real numbers
mean is not established.

The real roots, by names and counts only: no `R214_*` or `STUB_*` variable in my environment; `r214p`, `r214`
and `r214_out` absent under `<scratchpad>`; `r211` present, untouched; no project folder for the pilot's path in
`<claude-config>`. In `<claude-config>`, by existence and key names only: no user-level instruction file, no
rules folder, no managed instruction file, no hooks, no local settings file, no instruction or settings file in
the scratch folder or the six levels above it. So the two instruction-file stops and the hook stop are not
expected.

## 6. Point 4 — the scripts and the disclosure search

- `./selftest.sh` on my root: exit 0, 526 PASS lines, 0 FAIL, "0 mismatches". The masked output is byte-equal to
  `03c_selftest.txt`.
- `./dryrun.sh` on my root: exit 0, 386 lines. Against `03d_dryrun.txt` 20 sorted lines differ: the turn-1 hash
  lines of eight arms and the `resumed_from=` lines of two pilots, as expected for a new run. Guard line: stub
  yes, other `claude` none. 23 stub calls. Project folders in the real config: 23 before, 23 after.
- Disclosure search over the 23 task files other than `local.env` (user name, home, system temp spellings, the
  session folder, the host names, an id shape): no machine value. The 6 lines that match are the generic system
  temp spellings in `certificate.py` (3), `mask.sh` (1), `selftest.sh` (1) and `03c_selftest.txt` (1), each a
  rule about the spelling, not a path of this machine. The probe: the same pattern hits `local.env` 3 times, and
  `local.env` is ignored by git. No `__pycache__` and no hidden file in the task folder.

Not established by this pass, because nothing real was run or read: what request copies the real tool writes
and where; the real text of the "unchanged" answer; what the boundary's token numbers count; the real metadata
keys; whether `--resume` keeps the session.

## 7. Verdict and the eye list

**Cleared for the pilot: yes.** The tree is the designed one, the three calls are the same as before, outputs,
lock, status and marker are where the reader looks, the real roots are clean, and every T1–T12 input that should
stop the pilot stops it or is printed, except X1. A `PILOT OK` for `q901` is to be read with the list below; it
does not clear the six. G1, G2, G3 and X1 are to be closed, or ruled on, before the six; G1 before any second
pilot is checked.

Before the launch, two lines:

```
env | grep -E '^(R214_|STUB_)'            # must print nothing
( . ./local.env && python3 setup.py pilots q901 )
```

Printed by `check_pilot.sh q901`, to be read line by line:
1. the `launch.status` lines and the three exit codes;
2. the session, and that turn 2 resumed it;
3. the compaction line: the boundary's pre and post numbers and `agree`;
4. the token pair of the assistant records; `None / None` must be read as "no numbers", not as a pass;
5. n, x, x + n, the added line, short lines, request copies left out and unreadable, rest of turn;
6. "carried by", whenever n > 0, before any Pivot ruling;
7. the records about the rules file, the preserved fields, the unknown metadata keys;
8. the classes (iv) and (i) and the access list with the lines delivered;
9. every WARNING (unplaced form, delivered-unresolved) and every flag;
10. cost, memory, the certificate's terms, a second model;
11. `tool_calls_dotdot`, before and after the boundary;
12. the verdict line and the marker.

Not printed; one line each. The first reads the reader's own output:

```
python3 -c "import json,sys;r=json.load(open(sys.argv[1]))['arms']['q901'];print('unparsed lines:',r['transcript']['unparsed_lines'],' K lines in the snapshot rules file:',r['ii']['K_lines_in_snapshot_rules'],' K lines in results of other calls:',r['i']['rules_in_results_of_other_calls'],' shrank by records / by boundary:',r['iii']['shrank_by_records'],r['iii']['shrank_by_boundary'])" <scratchpad>/r214_out/q901.read.json
```

On my stub pilot it prints: unparsed lines 0, K lines in the snapshot 86, results of other calls `[]`, shrank
`True True`.

The second prints the structure of the span from the boundary to the first tool result: record types, metadata
key names, presence of usage, counts. It prints no text of any record. It is for whoever is allowed to inspect
the real transcript's structure, and it answers the open questions of section 5 (a request copy in the span, the
metadata keys, the usage numbers):

```
. ./local.env; f=$(ls -t "$CLAUDE_CONFIG_DIR"/projects/*r214p-q901/*.jsonl | head -1); python3 -c "
import json,sys,collections
R=[]
for l in open(sys.argv[1]):
    try: r=json.loads(l)
    except ValueError: r=None
    R.append(r if isinstance(r,dict) else {'type':'NOT-AN-OBJECT'})
def k(r):
    a=r.get('attachment'); m=r.get('message'); c=m.get('content') if isinstance(m,dict) else None
    return str(r.get('type'))+('/'+str(a.get('type')) if isinstance(a,dict) else '')+('['+','.join(sorted({str(x.get('type')) for x in c if isinstance(x,dict)}))+']' if isinstance(c,list) else '')+(' usage' if isinstance(m,dict) and isinstance(m.get('usage'),dict) else '')
B=[i for i,r in enumerate(R) if r.get('subtype')=='compact_boundary']
b=B[-1] if B else 0
e=next((i for i in range(b+1,len(R)) if 'tool_result' in k(R[i])),len(R)-1)
md=R[b].get('compactMetadata')
print('records',len(R),'boundaries',B,'first tool result after the last',e)
print('metadata keys',sorted(md) if isinstance(md,dict) else type(md).__name__)
[print(i,k(R[i])) for i in range(b,e+1)]
print('all kinds',dict(collections.Counter(k(r) for r in R)))
" "$f"
```

On my stub pilot it prints 19 records, the boundary at 7, the first tool result at 15, five metadata keys and
the nine records of the span with their kinds.

Standing: after any change to the reader, `check_pilot.sh q901` is run again before its marker is trusted. The
12 items of section 8 of `03g_apparatus_reverify2.md` still stand, item by item, before the six.
