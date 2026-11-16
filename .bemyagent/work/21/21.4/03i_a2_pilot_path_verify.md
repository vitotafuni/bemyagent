# 21.4 — the path of the pilot `q902` after Amendment 4: fifth pass of the verifier

Scope: only what Amendment 4 (D1–D6) changed on the pilot's path. This pass does not clear the six.
Everything was run on my own scratch root (`<scratchpad>/p214/v5`, called `<V>`) with my own stub first on a
checked PATH and my own config folder. The real `claude` was never run. The real `q901` was read by
`check_pilot.sh q901` with its outputs written to a copy in `<V>`, and by scripts of mine that print record
kinds, key names, counts and lengths and no text; of its tree I listed file names only. Nothing was built in `<scratchpad>/r214` or `<scratchpad>/r214p`.
Nothing in the repo was changed except this file.

## 1. Findings

None makes the launch of `q902` unsafe. F1 and F3 are ways a `PILOT OK`, or the "control read whole" outcome,
could rest on something the reader did not see: both are covered by the script of section 9 until they are closed.
Each finding is given as input, what happened, what should happen, smallest change.

**F1 — D2: a pointer at the rules file that is not a string value of an attachment record is not seen.**
The builder's rule is: the basename of the rules file, or a line of K, in any string value of any attachment
other than the instruction one, inside the window. Inputs that passed with `PILOT OK`, nothing printed:
- the path is a key of a map in an attachment (C3);
- the name is cut short by the tool, or is in another letter case (A4, A7);
- the pointing sentence stands in a record that is not an attachment: a meta user record, a system record (C5, C6);
- the reference stands just before the boundary record (D3);
- the reference points at `BEMYAGENT.md`, the file that embeds the rules (A6).
With (i) `whole`, the meta-record case ends in "THE CONTROL READ WHOLE", exit 3 (E3): the round would be recorded
as "occasion produced, control read whole" for an arm the tool had pointed at the file.
One real datum, by structure: in `q901` the compaction summary names the rules file (1 record); no other record
between the boundary and the first tool call does, apart from the reference, the instruction attachment and three
stored request copies.
Should happen: D2 says no reference and no text; a pointer in another place is still a pointer, or is ruled not
to be one.
Smallest change: `occasion_attachments` looks at keys as well as values and ignores case; the check prints, per
kind, the count of records in the window that hold the basename and are not the arm's own, not request copies and
not the instruction attachment (printed, not a stop: the summary will be among them); the designer rules on a
reference to `BEMYAGENT.md`.

**F2 — D2: an attached file whose text mentions the rules file's name stops the pilot, under a label that says
something else.**
Input: after the boundary, a `file` attachment of another file (a work log; the arm's `CLAUDE.md`) whose text holds
the basename (B4, B5).
Happened: `[occasion]`, kind `text-attachment`, `PILOT NOT OK`, exit 1. The label reads as "the rules' text was
attached". The census counted references to the file, not mentions of its name in other files.
Likelihood, from the real `q901` tree (file names only): besides the rules file only `CLAUDE.md` and `BEMYAGENT.md`
hold the name; none of the files the arm wrote does. So it needs an arm that reads `CLAUDE.md` with a tool, or
writes the name in a log it then touches late.
Should happen: the label says what was found, and whether a mention excludes an arm is the designer's ruling.
Smallest change: kind `text-attachment` only when the attached file is the rules file (`file_target`); otherwise
kind `name`.

**F3 — D6 as ruled: yes, rules text can sit in a request copy the reader calls "read, 0 lines".**
Inputs, each a stored copy in the span the reader reads, each ending in `PILOT OK` with n = 0 and unreadable 0:
- the rules in base64 as the content string (R4), or as the only string of a message that is a list (R18);
- the rules compressed and encoded inside a text block (R5);
- a `document` block with the rules as an encoded source (R6);
- every line of the rules cut in two text blocks (R10);
- a request whose hashes are values of a map, one of them resolving to no stored record (R9).
Before the ruling a compressed copy and a split copy stopped the pilot (03h, T4). Real datum, by structure: the five
copies of that span in `q901` hold short-word prose (the longest string without a blank is 4 to 9 characters).
Should happen: a copy that holds text in a form the reader cannot match is not "read".
Smallest change: beside the two conditions of the ruling, a copy in the span is unreadable when one of its strings
is longer than a fixed length (200 characters would do) and holds no blank, or when a 64-hex string in it, outside
its own three ids, resolves to no stored record wherever it stands.

**F4 — a block type the real tool writes is unknown to the reader: a false stop waiting on where it falls.**
Input: a stored copy in the span with a block of type `tool_addition` beside a text block (R7); the same block in a
copy after the first tool result that a request in the span lists by hash (R7c).
Happened: `[request copies] 1 ... cannot be read as text`, exit 1. The same copy after the first tool result and
not listed is left out (R7b).
Real datum, by structure: `q901` holds two stored copies with such blocks (keys `tool`, `type`), one before the
boundary and one after the first tool result, neither read by (ii).
Smallest change: none before the pilot. If `q902` stops on it, the builder reports the block's structure and the
designer rules as for D6.

**F5 — D3: what the check says and what it leaves unsaid.**
- The "control read whole" line says "two control pilots of two at `whole` would say ceiling". By D2 `q901` was not
  on the occasion (it had the reference). On the occasion it would be one control pilot of one.
- `attempted` is none of D3's three outcomes. The check answers `PILOT NOT OK`, exit 1, `[attempted access (i)]`,
  no marker (three runs). I think that is right: the six would lose every such arm. D3 should name it.
- Two classes open the six while the control in effect read everything: two ranged reads that together cover the
  file are `slice`, with the note "union" printed (I1); a whole read after the first write is `none`, and the late
  access is not printed (I3). Both follow the definition closed in Amendment 3. They are on the eye list.
Smallest change: the wording of the line; one sentence in D3 on `attempted`; the count of accesses after the first
write printed beside (i).

**F6 — P1 is closed for a line that is not an object, not for an object with a field of the wrong type.**
Input: a record whose `message` is a string (P1d); an attachment record whose `attachment` is a list or a string
(P1e, C4).
Happened: `certificate.py` ends in a traceback, the verdict part in a second one; exit 1, no verdict line, marker
removed. It stops, not by a named check.
Smallest change: in `certificate.py`, `message` and `attachment` are used only when they are objects.

**F7 — the four-call certificate, small gaps.**
- A status without `t1b_sha` is read as the three-call design and `q902` gets `PILOT OK` (K5; the design line says
  "3 calls"). Not reachable with this launcher. Smallest change: the check stops on a three-call design for any
  pilot other than `q901`.
- A second model in turn 1b's usage is not reported: `result_models` has no `t1b` (K7; turn 2's is reported, K8).
- The stop line of `design_ok` does not print the turn-1b term (K1, K2 show five terms, all true).
- Labels still say "the three calls" and "t1/cp/t2".
- Read in the code, not run: the pattern of apparatus names in `certificate.py` has no `t1b` output file.

**Minor, still open.** The markers are removed after the two scripts, not before them (an interrupted check
leaves the old marker; read in the code). `setup.py pilots q112` prints "built 0 arms", exit 0. The commit ids in
row 1 of the checklist, in `03d_dryrun.txt` and in the real `setup.status` are no longer in the repo (the history
was rewritten); `setup.py` still asserts the one added line and its hash on today's refs, on my run.

## 2. Point 1 — D1 on my root: `setup.py pilots q902`, `launch.sh q902`, `check_pilot.sh q902`

| Check | Result |
|---|---|
| the tree | rules file byte-equal to the repo's (107 lines), `BEMYAGENT.md` byte-equal, `CLAUDE.md` one line (the seeded sentence), no `AGENTS.md`, K = 86, threshold 43, 2 commits, clean |
| the calls | four, in the order turn 1, turn 1b, compaction, turn 2; cwd is the pilot's tree in all four; one resume id on the last three |
| turn 1b's flags | `-p <prompt> --resume <session> --model sonnet --output-format json --allowedTools Read Write Edit Bash Glob Grep`: the same as turn 2's |
| turn 1b's prompt | equal to `prompt_t1b.txt` without its final newline (184 bytes passed, 185 in the file; the shell drops it, the hash and the certificate compare without it; `prompt_t2.txt` has no final newline) |
| stdin | empty in all four |
| snapshot | `snap/q902.t1` holds the file my stub writes in turn 1b and not the one it writes in turn 2 |
| boundary count | `boundaries_before=0` is written after the `t1b` line; with a boundary made inside turn 1b the reader cuts at the second (K9) |
| turn 1b exits 1 | arm ends, 2 calls, `PILOT NOT OK`, exit 1, no marker |
| turn 1b reports `is_error` | the same |
| turn 1b returns another session id | the same (`session_same=0`) |
| turn 1b writes no JSON | the same |
| turn 1b hangs, time limit 3 s | exit 142, "killed by the time limit", arm ends, the same |
| the certificate | `calls = 4`; session ids of the four compared; the turn-1b prompt must be a user record before the boundary (K1, K2 stop); its hash must equal the file's (K4 stops); `t1b.json` missing, with another session id, or with a permission denial stops (K6, K3, K10) |
| the healthy stub pilot | `PILOT OK`, exit 0, marker `pilot_ok.q902` holding `PILOT OK q902`; design "4 calls"; (iv-b) and the count of files touched printed |

A turn 1b that fails ends `launch.sh` with exit 0: the arm stopped by itself and the status says so.

**The real `q901`, read again** (`check_pilot.sh q901`, outputs to my copy; the real output folder's listing is
unchanged): read as "3 calls ... the design before Amendment 4"; session kept; compaction 65482 to 7056 by the
boundary, 64920 to 26574 by the records; n = 0, x = 0; request copies left out 15, unreadable 0; (iv) `whole`,
(i) `whole` by one plain `Read`, 90 of 90; 5 files touched before the boundary; one attachment naming the rules,
a `compact_file_reference` at offset 9; (iv-b) absent with its reason; certificate clean, design ok;
`PILOT NOT OK`, exit 1, on `[occasion]` and the eligibility line for the same reference; no marker, no traceback.
This agrees with `03_execute.log` (the entry of the run, and [23]).

## 3. Point 2 — D2 and D3, attacked through `check_pilot.sh q902`

Baselines: (i) `slice` and `none` give `PILOT OK`, exit 0, marker; `whole` gives "THE CONTROL READ WHOLE", exit 3,
no marker; `attempted` gives `PILOT NOT OK`, exit 1, no marker.

| Input after the boundary | Outcome | Seen as |
|---|---|---|
| A1–A3 reference, absolute or relative, or under another key | 1: NOT OK | `reference` |
| A5 a reference of another type name | 1: NOT OK | `name` |
| A4, A7 reference with the name cut short or in upper case | 3: PILOT OK | not seen (F1) |
| A6 reference to `BEMYAGENT.md` | 3: PILOT OK | not seen (F1) |
| B1 file attachment, the whole rules | 1: NOT OK | `text-attachment`, n = 86 |
| B2 file attachment, 12 lines | 1: NOT OK | `text-attachment`, n = 9 |
| B3 file attachment of the rules, empty | 1: NOT OK | `text-attachment`, n = 0 |
| B4, B5 file attachment of another file that mentions the name | 1: NOT OK | `text-attachment` (F2) |
| B6 file attachment of another file quoting one line of K | 1: NOT OK | n = 1 as well |
| B7 file attachment of another file, no name, no line | 3: PILOT OK | nothing, correct |
| C1, C2 the name in a todo or a hook attachment | 1: NOT OK | `name` |
| C3 the path as a key of a map | 3: PILOT OK | not seen (F1) |
| C4 `attachment` is a string | exit 1, tracebacks | F6 |
| C5, C6 the pointing sentence in a meta user record or a system record | 3: PILOT OK | not seen (F1) |
| C7 instruction attachment listing the rules file, name only | 3: PILOT OK | exempt by the builder's choice |
| C8 instruction attachment carrying the rules' text | NOT OK | (ii): n = 86 |
| C9 the summary names the file | 3: PILOT OK | not an attachment; real in `q901` |
| D1 reference after the first write | 3: PILOT OK | outside the window, not printed |
| D2 reference after the arm's access, before its first write | 1: NOT OK | `reference` |
| D3 reference just before the boundary record | 3: PILOT OK | not seen (F1) |
| D4 file attachment of the rules after the first write | NOT OK | `[(ii) rest of turn 2]` 86 |
| E1 reference and (i) `whole` (what `q901` was) | 1: NOT OK, exit 1 | `reference` |
| E2 reference after the window and (i) `whole` | 2: control whole, exit 3 | outside the window |
| E3 pointing sentence in a meta record and (i) `whole` | 2: control whole, exit 3 | not seen (F1) |

**The builder's two choices.**
*Only the window.* It cannot let a pointed-at arm through as long as the file's order is the order in which the
records reached the model: a pointer written after the first write cannot have led a read before it. In `q901` the
attachments of the compaction stand at offsets 5 to 14 and those of turn 2's start at 22 to 28, all before the
first tool call at 40. What it costs: a reference after the window is printed nowhere. It cannot stop a sound
pilot. A reference inside the window but after the arm's own access (D2 of the table) stops the pilot: on the safe
side.
*The basename or a K line in any attachment but the instruction one.* It can let a pointed-at arm through in the
ways of F1. It can stop a sound pilot in the way of F2, and on a todo or hook that names the file, which I read as
right under D2. The instruction exemption lets through a name only: text in it is caught by (ii) (C8).

**The classes.** `whole` by a plain read, a `cat`, a search that returns every line, or a slice followed by a
whole read: outcome 2 (I2, I5, I7, baseline). Two ranged reads covering the file: `slice`, outcome 3 (I1). A whole
read cut by the tool at line 60: `slice`, outcome 3 (I8). A whole read only after the first write: `none`,
outcome 3 (I3). A whole read of `BEMYAGENT.md`: NOT OK, `[rules in another call's result]` 86 (I4). A withheld
read, alone or followed by a slice: NOT OK (I6).

**The marker and the six's gates under each outcome** (`launch.sh q112`, `setup.py six q112`):

| State | `launch.sh` counted arm | `setup.py six` |
|---|---|---|
| outcome 1 | refused, 0 calls, exit 1 | refused, exit 1 |
| outcome 2 | refused, 0 calls, exit 1 | refused, exit 1 |
| `attempted` | refused, 0 calls, exit 1 | refused, exit 1 |
| outcome 3 | 4 calls from the arm's tree in the root of the six, exit 0 | builds, exit 0 |
| outcome 3, then the same pilot checked again and ending in outcome 2 | refused again | refused again |

## 4. Point 3 — D5, on my inputs

| Finding of 03h | State | Evidence |
|---|---|---|
| G1 | closed | a marker `pilot_ok.q901` put by hand, then `q902` checked and ending in outcome 2, and in outcome 1: no marker left, both gates refuse. Left: the removal comes after the two scripts (minor) |
| G2 | closed | six hand-made markers refused by both gates: empty `pilot_ok.x`, empty `pilot_ok.q902`, `pilot_ok.q902` holding another pilot's line, `pilot_ok.q112`, a marker with a second line, `pilot_ok.q902.bak` |
| G3 | closed | an override naming a counted arm or leaving out a pilot is refused by `check_pilot.sh` and `launch.sh` (exit 2), `read.py` and `certificate.py` (exit 1), also with the pilots' root pointed at the six; with `R214_TEST_ONLY` it is taken and said on stderr; `R214_TEST_ONLY` alone opens nothing; an override that only adds a new name is taken, with the note |
| X1 | closed | the rules in the first write's own result, and in a failed `Edit` before it: `[rules in another call's result]` 86, exit 1 |
| P1 | closed for lines that are not objects; open for F6 | a JSON string line, a JSON list line, a line that does not parse: `[unparsed lines] 1`, no traceback |
| m1 | closed | every refusal above ends `launch.sh` with exit 1 |
| m2 | closed | `setup.py six q112` with the scratch variable unset refuses naming the real output folder: it read `local.env`. A bare `setup.py pilots q902` therefore builds in the real pilots' root |

## 5. Point 4 — D6

`q901`'s own record (a stored copy whose content is an empty list) is read, 0 lines, no stop (R3); a shape record
with no hash list too (R12). The rules as a plain string, in a text block, under another key, with other line
ends, or in a later copy that a request in the span lists by hash are counted, n = 86 (R1, R2, R17, R16, R15).
As JSON inside one string they count 35 and stop the pilot (R11; 35 is under the threshold of the six). A hash
list with an unresolved hash, a content that is a number, a block of unknown type stop (R8, R13, R7). The six
inputs of F3 are called read and hold the rules.

## 6. Point 5 — the two rulings

**D3, the pilot's class decides whether the six are run.** The claim holds for the six themselves: they are
other arms, read by a table fixed before, so their result given that they are run is what it would have been.
What the gate changes is the record of the round, in four ways.
1. The round ends as "not reproduced by this harness" whenever one control pilot reads whole. If the control's
   true rate of `whole` is p, that is p; a *ceiling* by the table needs three of three, p cubed. At p = 0.5 the
   gate closes the line half of the time where the table would most often have said *under-powered*. The tilt is
   toward the line staying untested. It is honest only if recorded as that: one control pilot of one on the
   occasion, the six not run (F5).
2. The decision rests on one classification by the reader. The edges of section 3 (union of slices, a late whole
   read, `attempted`, a pointer the reader does not see) each move it. The pilot's (i) is to be hand-read from the
   access list before outcome 2 or 3 is acted on.
3. The pilot is a C arm. It shows the occasion for C. Whether an L arm keeps the occasion is not shown by it
   (below).
4. Whatever is changed in the reader between the pilot and the six is changed with one control arm's behaviour in
   view. Structure may inform it; the class must not.

**D2, the exclusion of arms that got a reference.** It can remove arms unevenly, because what the tool hands
back is decided before the boundary and the line is already acting there: an L arm carries the line through
turn 1 and turn 1b. If the line makes an arm read the rules again at the start of turn 1b, and if the tool
picks its five files by last use, the rules file comes back as a reference more often in L than in C. An L arm
that writes about its reads in a log the tool attaches is removed by F2's route too. Neither is established; the
stub cannot show what the tool picks.
What follows from the table as it stands: fewer than three eligible arms in a condition is *under-powered*, so
with three a side any exclusion ends the round there. An uneven removal therefore cannot produce a licensed
verdict; it can spend the six for nothing. It would bias a larger round: the L arms removed would be the ones
that obeyed the line before the boundary. What to print for the six: (iv-b) and the occasion per arm side by
side, and the exclusions per condition.

## 7. Point 6 — the scripts and the disclosure search

- `./selftest.sh` on my root: exit 0, 727 PASS lines, 0 FAIL, "0 mismatches". Against `03c_selftest.txt` two
  lines differ, by where a note from stderr falls in the line.
- `./dryrun.sh` on my root: exit 0, 440 lines, 39 stub calls. Guard: the stub yes, another `claude` none. Real
  config project folders 24 before, 24 after. Against `03d_dryrun.txt` 22 lines differ: the turn-1 hash line of
  ten arms, ten `resumed_from=` lines, and the two commit ids (see the minor findings).
- Disclosure search over the 25 task files other than `local.env`, with the 13-word list and my own shapes (home,
  system temp spellings, session folder, an id shape, a mail shape, a package-manager path): the word list hits
  nothing; the shapes hit the same 6 lines as in 03h, generic temp spellings in `certificate.py` (3), `mask.sh`,
  `selftest.sh`, `03c_selftest.txt`. The probe: `local.env` is hit by both. No `__pycache__`, no hidden file.

Not established by this pass: which five files the real tool hands back after turn 1b and by what order; what
an L arm does in turn 1b; whether the summary of `q902` names the file as `q901`'s does; where a `tool_addition`
block will stand; the real answer to a re-read after turn 1b.

## 8. Verdict

**Cleared for the pilot `q902`: yes.** The tree is the designed one; the four calls run in order on one session
with turn 1b passed like turn 2; a turn 1b that fails, hangs or changes the session ends the arm; the certificate
checks the four calls; the three outcomes of D3 are decided as written, with the exit codes and the marker the
amendment names; G1, G2, G3, X1, m1, m2 are closed; `q901` is still read as what it was. The outcome of `q902`,
2 or 3, is to be accepted only with the eye list below: F1 and F3 are not closed. The six are not cleared.

## 9. The eye list for `q902`

Before the launch, from the task folder:

```
env | grep -E '^(R214_|STUB_)'      # must print nothing
python3 setup.py pilots q902         # reads local.env; builds <scratchpad>/r214p/q902 beside q901
```

In the output of `./check_pilot.sh q902`, line by line:
1. `launch.status`: four exit lines, `t1b` among them, all 0; `boundaries_before=0`; `compaction_proven=1`;
   `session_same=1`.
2. `== design`: it must say "4 calls".
3. The compaction line and the token pair; `None / None` is "no numbers", not a pass.
4. n, x, x + n; request copies left out and unreadable; rest of turn 2; "carried by" whenever n > 0.
5. "records about the rules file itself" and "attachments after the boundary naming the rules": type, kind and
   offset of each. A kind `text-attachment` on a file that is not the rules file is F2, not a hand-back.
6. "distinct files touched before the boundary": the number the design rests on (5 in `q901`).
7. (iv), (iv-b), (i) with its note, and the access list with lines delivered. A `slice` with the note "union", and
   a `none`, are read by hand before outcome 3 is taken.
8. Every WARNING and flag; `tool_calls_dotdot` before and after; the certificate's terms; a second model (turn
   1b's is not printed, F7).
9. The verdict line, the exit code (0, 1 or 3) and the marker. An "unknown block" or `[request copies]` stop is F4.

Not printed; one line on the reader's own output:

```
python3 -c "import json,sys;r=json.load(open(sys.argv[1]))['arms']['q902'];i=r['i'];print('design:',r['design'][:7],'| unparsed lines:',r['transcript']['unparsed_lines'],'| K lines in the snapshot rules file:',r['ii']['K_lines_in_snapshot_rules'],'| K lines in results of other calls:',i['rules_in_results_of_other_calls'],'| shrank by records / by boundary:',r['iii']['shrank_by_records'],r['iii']['shrank_by_boundary'],'| (i):',i['class'],'| note:',i.get('note'),'| accesses after the first write:',len(i.get('late_accesses') or []),'| (iv-b):',(r.get('ivb') or {}).get('class'),'| files touched before the boundary:',r['occasion']['distinct_files_touched_before_boundary'])" <scratchpad>/r214_out/q902.read.json
```

On my stub pilot it prints: 4 calls, 0, 86, `[]`, `True True`, `slice`, `None`, 0, `none`, 12.

Not printed; the structure of the real transcript from the boundary on (F1, F3, F4). It prints kinds, key names,
counts and lengths, and no text of any record. It is for whoever is allowed to inspect the real transcript's
structure. Before outcome 2 or 3 is accepted: no line between the boundary and the first tool call may carry
"NAMES THE RULES FILE" other than the instruction attachment and the summary (and the summary is to be told to the
designer); no copy "read by (ii)" may show an unknown block type or a long string with no blank.

```
. ./local.env; f=$(ls -t "$CLAUDE_CONFIG_DIR"/projects/*r214p-q902/*.jsonl | head -1); python3 -I - "$f" <<'PY'
import json, re, sys, collections
NAME, KNOWN = "00-ai-rules.md", {"text", "tool_use", "tool_result", "thinking", "redacted_thinking", "image", "document"}
R = []
for l in open(sys.argv[1], errors="replace"):
    try: r = json.loads(l)
    except ValueError: r = None
    R.append(r if isinstance(r, dict) else {"type": "NOT-AN-OBJECT"})
def content(r):
    m = r.get("message"); return m.get("content") if isinstance(m, dict) else None
def kind(r):
    a, c = r.get("attachment"), content(r)
    t = str(r.get("type")) + ("/" + str(r["subtype"]) if r.get("subtype") else "") + ("/" + str(a.get("type")) if isinstance(a, dict) else "")
    if isinstance(c, list): t += "[" + ",".join(sorted({str(x.get("type")) for x in c if isinstance(x, dict)})) + "]"
    return t + "".join("{" + k + "}" for k in ("isMeta", "isCompactSummary") if r.get(k) is True)
def strs(o, keys=False):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if keys: yield str(k)
            yield from strs(v, keys)
    elif isinstance(o, list):
        for v in o: yield from strs(v, keys)
names = lambda r: any(NAME.lower() in s.lower() for s in strs(r, True))
B = [i for i, r in enumerate(R) if r.get("subtype") == "compact_boundary"]; b = B[-1]
tc = next((i for i in range(b + 1, len(R)) if "tool_use" in kind(R[i]) and R[i].get("type") == "assistant"), len(R) - 1)
fr = next((i for i in range(b + 1, len(R)) if "tool_result" in kind(R[i]) and R[i].get("type") == "user"), len(R))
print("records", len(R), "| boundaries at", B, "| first tool call after the last:", tc, "| first tool result:", fr)
for i in range(b, tc + 1):
    a = R[i].get("attachment")
    print(f" +{i-b:3d} {kind(R[i])}" + (" keys=" + ",".join(sorted(a)) if isinstance(a, dict) else "") + ("   NAMES THE RULES FILE" if names(R[i]) else ""))
c = collections.Counter(kind(R[i]) for i in range(b + 1, len(R)) if names(R[i]) and not str(R[i].get("type")).startswith("api-request"))
print("records after the boundary that name the rules file, by kind (request copies apart):", dict(c))
hs = {s for i in range(b + 1, fr) if R[i].get("type") == "api-request" for s in strs(R[i]) if re.fullmatch(r"[0-9a-f]{64}", s)}
for i, r in enumerate(R):
    if r.get("type") != "api-request-blob": continue
    cc = content(r); span = b < i < fr or r.get("hash") in hs
    unk = sorted({str(x.get("type")) for x in cc if isinstance(x, dict) and x.get("type") not in KNOWN}) if isinstance(cc, list) else []
    if span or unk:
        print(f" blob at {i-b:+d} ({'read by (ii)' if span else 'left out'}): content {type(cc).__name__}, unknown block types {unk}, longest string with no blank {max((len(s) for s in strs(r.get('message')) if not re.search(r'\s', s)), default=0)}")
PY
```

Run on the real `q901` it shows the boundary at 106, the first tool call at offset 40, the reference at offset 9
after four `file` attachments, the summary naming the file, five copies read by (ii) with strings of 4 to 9
characters without a blank, and two copies with `tool_addition` blocks, both left out.

Standing: after any change to the reader, `check_pilot.sh q902` is run again before its outcome is trusted. The
12 items of section 8 of `03g_apparatus_reverify2.md` and the findings of this pass stand before the six.
