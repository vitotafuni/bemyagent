#!/bin/bash
# 21.4 — builds synthetic transcripts (the on-disk shape of 03_execute.log [2], made by synth.py) under a temp
# root in the scratchpad, runs read.py, certificate.py and check_pilot.sh on them and checks the expected value of every case.
# Each case states what it is and the class it must get. Exits non-zero on any FAIL.
# After Amendment 1 (02_tasks.md): the class is decided by what the access DELIVERED (every non-empty line, in order = whole;
# some = slice; none = attempted), not by its form or by headings; the window is cut at the launcher's boundary number and ends
# at the first write that succeeded. Cases whose expected class changed under the amendment print a CHANGED line. New cases:
# the verifier's M1-M6, D1, N1, N3, N5 (N5 is in dryrun.sh), written from the amendment's text.
set -u
export PYTHONDONTWRITEBYTECODE=1      # no __pycache__ in the task folder
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$HERE/local.env" ] && . "$HERE/local.env"      # machine-local BMA_SCRATCH / CLAUDE_CONFIG_DIR / BMA_BASE (gitignored)
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
ROOT="${BMA_REPO:-$(cd "$HERE/../../../.." && pwd)}"
export ST="$S/p214/selftest" HERE ROOT
rm -rf "$ST"; mkdir -p "$ST/trees" "$ST/out" "$ST/cfg/projects"
python3 - <<'PY'
import hashlib, json, os, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
ST, HERE, ROOT = (pathlib.Path(os.environ[k]) for k in ("ST", "HERE", "ROOT"))
sys.path.insert(0, str(HERE))
import synth
from synth import numbered, RULES
TR, OUTD, CFG = ST / "trees", ST / "out", ST / "cfg" / "projects"
RULES_C = (ROOT / RULES).read_text()
BEM = (ROOT / "BEMYAGENT.md").read_text()
T1B = (HERE / "prompt_t1b.txt").read_text()
T1 = (HERE / "prompt_t1.txt").read_text(); T2 = (HERE / "prompt_t2.txt").read_text(); TC = (HERE / "prompt_compact.txt").read_text()
LINES = RULES_C.splitlines()
HEADS = [i for i, l in enumerate(LINES) if l.startswith("## ")]
assert len(HEADS) == 8, "the repo's rules file must have eight sections for this test"
NONEMPTY = [l for l in LINES if l.strip()]
tabbed = lambda text: "\n".join(f"{i + 1:6d}\t{l}" for i, l in enumerate(text.splitlines()))
first = lambda n: "\n".join(LINES[:n])
FULL = RULES_C
seven = "\n".join(LINES[:HEADS[7]])                 # everything before section 8
upto3 = "\n".join(LINES[:HEADS[3]])                 # sections 1-3 only
heads_only = "\n".join(LINES[i] for i in HEADS)
elided = "\n".join(LINES[:50] + ["<<< 20 lines elided to save space >>>"] + LINES[70:])
tail_cut = numbered("\n".join(LINES[:-3])) + "\n[file cut here by the tool]"
INSTR = "Read .bemyagent/docs/00-ai-rules.md before every task.\n"       # the arm's CLAUDE.md, as build_tree writes it
BIG = [l for l in NONEMPTY if len(l) >= 20 and l.rstrip() not in INSTR]     # B2: the lines (ii) counts
M = len(BIG)
n_found = lambda text: sum(1 for l in BIG if l in text)
half_k = next(k for k in range(1, M + 1) if n_found("\n".join(BIG[:k])) * 2 >= M)
text_half = "\n".join(BIG[:half_k])                                       # n >= M/2: the arm leaves (i)
text_below = "\n".join(BIG[:half_k - 1])                                  # n < M/2: the arm stays
assert 2 * n_found(text_below) < M <= 2 * n_found(text_half)
STUB = "File unchanged since last read. The content from the earlier Read tool_result in this conversation is still current - refer to that instead of re-reading."

def sha(text): return hashlib.sha256(text.rstrip("\n").encode()).hexdigest()

class Ctx:
    def __init__(self, name):
        self.name = name; self.arm = str(TR / name)
        self.rules = f"{self.arm}/{RULES}"; self.rel = RULES
        self.app = f"{self.arm}/client/app.js"

def build_tree(name, text=None):
    d = TR / name
    (d / ".bemyagent/docs").mkdir(parents=True, exist_ok=True); (d / "client").mkdir(parents=True, exist_ok=True)
    (d / RULES).write_text(text or RULES_C); (d / "BEMYAGENT.md").write_text(BEM)
    (d / "client/app.js").write_text("// app\n"); (d / "CLAUDE.md").write_text("Read .bemyagent/docs/00-ai-rules.md before every task.\n")
    return d

def write_edit(t, c):
    t.tool("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "edited")

def auto_boundary(t, c=None):
    t.boundary(trigger="auto"); t.summary("s2"); t.instructions()

def make(name, after, turn1="whole", boundaries=1, summary="A summary of the work so far.", extra_after_boundary=None,
         proven=1, with_t2=True, cert="ok", before_boundary=None, preserve=None, t2json=None, t2_prompt=True,
         status_after=None, t2_exit=0, before_status=None, snap_rules=None, setup_orig=None, cp_exit=None, t2_raw=None,
         after_tokens=20000, extra_status="", tree_rules=None, snap_instr=None, cert_dotdot=None, junk_lines=(), meta=None, small_before=None, claude_md=None, four=False, t1b_actions=None):
    c = Ctx(name); build_tree(name, tree_rules)
    if snap_rules is not None:          # the turn-1 snapshot: the rules as the arm's file held them when the window opened
        sd = OUTD / "snap" / f"{name}.t1"; (sd / ".bemyagent/docs").mkdir(parents=True, exist_ok=True)
        (sd / RULES).write_text(snap_rules); (sd / "CLAUDE.md").write_text(snap_instr if snap_instr is not None else INSTR)
    if setup_orig is not None:
        with open(OUTD / "setup.status", "a") as f: f.write(f"arm {name} cond=C rules_sha1={hashlib.sha1(setup_orig.encode()).hexdigest()}\n")
    if claude_md is not None: (TR / name / "CLAUDE.md").write_text(claude_md)
    t = synth.T(c.arm, f"{name}-sid", tokens=50000)
    t.instructions(); t.user(T1.replace("<ARM_DIR>", c.arm))
    if turn1 == "whole": t.tool("Read", {"file_path": c.rules}, numbered(FULL))
    elif turn1 == "slice": t.tool("Bash", {"command": f"head -50 {c.rules}"}, first(50))
    write_edit(t, c); t.assistant_text("done")
    if four:                             # D1: turn 1b, a second small feature, before the compaction
        t.user(T1B)
        (t1b_actions or (lambda t, c: write_edit(t, c)))(t, c)
        t.assistant_text("done 1b")
    if small_before:                     # C6: a small main-chain record last before the boundary
        t.tokens = small_before; t.assistant_text("small"); t.tokens = 50000
    if before_boundary: before_boundary(t, c)
    for k in range(boundaries):
        if k < boundaries - 1:                          # an earlier compaction inside turn 1, with a whole read between the two
            t.boundary(trigger="auto"); t.summary(summary); t.instructions()
            t.tool("Read", {"file_path": c.rules}, numbered(FULL)); t.assistant_text("again")
            continue
        t.tokens = after_tokens
        pres = preserve(t, c) if preserve else None
        b = t.boundary(preserved=pres, pre=50000, post=after_tokens); t.summary(summary); t.instructions()
        if meta == "absent": del b["compactMetadata"]
        elif meta is not None: b["compactMetadata"] = meta
        if extra_after_boundary: extra_after_boundary(t, c)
        t.manual_compact_tail()
    if t2_prompt: t.user(T2)
    after(t, c)
    t.assistant_text("finished")
    path = t.write(CFG)
    if junk_lines:
        with open(path, "a") as f:
            for jl in junk_lines: f.write(jl + "\n")
    (OUTD / f"{name}.t1.json").write_text(json.dumps({"session_id": f"{name}-sid", "is_error": False}))
    if with_t2 and t2_raw is not None:
        (OUTD / f"{name}.t2.json").write_text(t2_raw)
    elif with_t2:
        j = {"session_id": f"{name}-sid", "is_error": False, "usage": {"input_tokens": 1, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000, "output_tokens": 10},
             "modelUsage": {"claude-sonnet-5-5": {"inputTokens": 1, "cacheCreationInputTokens": 100, "cacheReadInputTokens": 1000, "outputTokens": 10}}}
        j.update(t2json or {})
        (OUTD / f"{name}.t2.json").write_text(json.dumps(j))
    bb = max(boundaries - 1, 0) if before_status is None else before_status
    ba = boundaries if status_after is None else status_after
    with open(OUTD / "launch.status", "a") as f:
        if four: f.write(f"{name} prompts t1_sha=x t1b_sha=y cp_sha=z t2_sha=w\n{name} t1b exit=0 resumed_from=x\n")
        f.write(f"{name} memory_existed=0 files=0\n{name} boundaries_before={bb}\n"
                f"{name} compaction_proven={proven} by=both pre_tokens=60000 session_same=1 trigger=manual boundaries_before={bb} boundaries_after={ba}\n"
                f"{name} t2 exit={t2_exit} resumed_from=x\n" + (f"{name} cp exit={cp_exit}\n" if cp_exit is not None else "") + extra_status.replace("ARM", name))
    if cert == "ok": (OUTD / f"{name}.cert.json").write_text(json.dumps({name: {"clean": True, "design_ok": True, **({"tool_calls_dotdot": cert_dotdot} if cert_dotdot else {})}}))
    elif cert in ("late", "early", "unplaced"):      # B8: not clean; where the failing call lies decides
        fa = {"no_tool_call_naming_repo": [99999]} if cert == "late" else {"no_tool_call_naming_repo": [5]} if cert == "early" else {}
        (OUTD / f"{name}.cert.json").write_text(json.dumps({name: {"clean": False, "clean_terms": {"no_tool_call_naming_repo": False}, "fail_at": fa}}))
    elif cert == "unclean": (OUTD / f"{name}.cert.json").write_text(json.dumps({name: {"clean": False, "clean_terms": {"no_tool_call_naming_repo": False, "override_header_ok": True}}}))
    return c

# ---- the cases: name -> (what it is, after-boundary actions, expected)
CASES = []
def case(name, what, after, exp, **kw): CASES.append((name, what, after, exp, kw))
def read_rules(**inp):
    return lambda t, c: (t.tool("Read", {"file_path": c.rules, **inp}, numbered(FULL)), write_edit(t, c))
def bash(cmd_fn, result):
    return lambda t, c: (t.tool("Bash", {"command": cmd_fn(c)}, result), write_edit(t, c))
UNRES = {"i": "none", "du": 1}                       # delivered by a call the reader does not resolve: class none + the A3 flag

# --- unchanged by Amendment 1
case("whole_read_noparams", "whole by Read with no parameters (absolute path)", read_rules(), {"i": "whole", "iv": "whole", "eligible": True})
case("whole_lone_cat", "whole by a lone cat (relative path)", bash(lambda c: f"cat {RULES}", FULL), {"i": "whole"})
case("whole_cat_n", "whole by cat -n (tab-numbered result)", bash(lambda c: f"cat -n {RULES}", tabbed(FULL)), {"i": "whole"})
case("whole_dot_slash", "whole by `cat ./...` (the ./ form)", bash(lambda c: f"cat ./{RULES}", FULL), {"i": "whole"})
case("whole_relative_read", "whole by Read with a relative path", lambda t, c: (t.tool("Read", {"file_path": RULES}, numbered(FULL)), write_edit(t, c)), {"i": "whole"})
case("slice_read_limit", "slice by Read with limit 50 (the result has 50 lines)", lambda t, c: (t.tool("Read", {"file_path": c.rules, "limit": 50}, numbered(first(50))), write_edit(t, c)), {"i": "slice"})
case("slice_read_offset", "slice by Read with offset 40", lambda t, c: (t.tool("Read", {"file_path": c.rules, "offset": 40}, numbered("\n".join(LINES[39:]))), write_edit(t, c)), {"i": "slice"})
case("slice_head", "slice by head -60", bash(lambda c: f"head -60 {RULES}", first(60)), {"i": "slice"})
case("slice_sed_n", "slice by sed -n 1,45p", bash(lambda c: f"sed -n '1,45p' {RULES}", first(45)), {"i": "slice"})
case("slice_grep", "grep whose result shows the eight heading lines only (looks whole, is a slice)", bash(lambda c: f"grep -n '^## ' {RULES}", "\n".join(f"{i + 1}:{LINES[i]}" for i in HEADS)), {"i": "slice"})
case("slice_grep_tool", "slice by the Grep tool", lambda t, c: (t.tool("Grep", {"pattern": "^## ", "path": c.rules}, heads_only), write_edit(t, c)), {"i": "slice"})
case("none_other_file", "no access to the rules (reads another file)", lambda t, c: (t.tool("Read", {"file_path": f"{c.arm}/.bemyagent/docs/06-implementation-plan.md"}, "1→# Plan"), write_edit(t, c)), {"i": "none", "iv": "whole", "eligible": True})
case("whole_truncated_persisted", "a cat whose output was persisted to a file: only a 20-line preview came back", bash(lambda c: f"cat {RULES}", "<persisted-output>\nOutput too large (50KB). Full output saved to a file\n" + first(20)), {"i": "slice"})
case("whole_only_before_boundary", "whole read only before the boundary", lambda t, c: (t.tool("Read", {"file_path": f"{c.arm}/client/app.js"}, "1→// app"), write_edit(t, c)), {"i": "none", "iv": "whole"})
case("whole_after_first_write", "whole read only after the first write", lambda t, c: (write_edit(t, c), t.tool("Read", {"file_path": c.rules}, numbered(FULL))), {"i": "none", "late": 1})
case("slice_then_whole", "a slice, then a whole read, before the first write", lambda t, c: (t.tool("Read", {"file_path": c.rules, "limit": 30}, numbered(first(30))), t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)), {"i": "whole"})
case("two_slices_union", "two slices that together cover every line stay a slice, noted union", lambda t, c: (t.tool("Read", {"file_path": c.rules, "limit": 60}, numbered(first(60))), t.tool("Read", {"file_path": c.rules, "offset": 61}, "\n".join(LINES[60:])), write_edit(t, c)), {"i": "slice", "note": "union"})
case("handed_8_summary", "every line of the rules handed back by the summary", lambda t, c: write_edit(t, c), {"i": "none", "ii_all": True, "eligible": False, "kind_has": "user{CompactSummary,VisibleInTranscriptOnly}"}, summary="Notes:\n" + FULL)
case("handed_8_file_attachment", "every line handed back by a file attachment of the rules file", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False, "kind_has": "attachment/file", "rules_records": ("rules", False)},
     extra_after_boundary=lambda t, c: t.file_attachment(c.rules, FULL))
case("handed_partial_attachment", "sections 1-3 handed back by a partial file attachment: reported, the arm stays", lambda t, c: write_edit(t, c), {"ii_part": True, "eligible": False, "reason_has": "names the rules file", "rules_records": ("rules", True)},
     extra_after_boundary=lambda t, c: t.file_attachment(c.rules, upto3, start=1, num=HEADS[3], total=len(LINES)))
case("handed_headings_only", "a summary that lists only the eight heading lines: n of N, reported, the arm stays (N4)", lambda t, c: write_edit(t, c), {"ii_part": True, "eligible": True}, summary=heads_only)
case("handed_text_without_marks", "the whole text of the rules without its `## ` marks in the summary: all lines counted (N4)", lambda t, c: write_edit(t, c), {"ii_part": True, "eligible": False, "reason_has": "x + n ="}, summary=re.sub(r"(?m)^## ", "", FULL))
case("reference_only", "the rules file named by a path-only compact_file_reference", lambda t, c: write_edit(t, c), {"ii": 0, "rules_records": ("rules-reference-only", None)},
     extra_after_boundary=lambda t, c: t.file_reference(c.rules))
case("no_boundary", "no compaction boundary at all", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)), {"i": None, "eligible": False, "boundaries": 0}, boundaries=0)
case("shell_write_first", "a shell redirect is the first write; the whole read comes after it", lambda t, c: (t.tool("Bash", {"command": "echo started > notes.txt"}, ""), t.tool("Read", {"file_path": c.rules}, numbered(FULL))), {"i": "none", "write_kind": "redirect"})
case("shell_write_after_whole", "a whole read, then a shell mkdir as the first write", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), t.tool("Bash", {"command": "mkdir -p .bemyagent/work/9/9.1"}, "")), {"i": "whole", "write_kind": "mkdir"})
case("seven_of_eight", "a Read with no parameters whose result lacks the last section (looks whole, is not)", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(seven)), write_edit(t, c)), {"i": "slice"})
case("cd_then_cat", "cd into docs then cat the bare name, stderr redirected (looks partial, is whole)", bash(lambda c: "cd .bemyagent/docs && cat 00-ai-rules.md 2>&1", FULL), {"i": "whole"})
case("dotdot_read", "a Read with `..` segments in the path (looks odd, is whole)", lambda t, c: (t.tool("Read", {"file_path": f"{c.arm}/client/../{RULES}"}, numbered(FULL)), write_edit(t, c)), {"i": "whole"})
case("bash_c_cat", "cat inside bash -c (looks partial, is whole)", bash(lambda c: f'bash -c "cat {RULES}"', FULL), {"i": "whole"})
case("read_offset_zero", "a Read with offset 0 and no limit", lambda t, c: (t.tool("Read", {"file_path": c.rules, "offset": 0}, numbered(FULL)), write_edit(t, c)), {"i": "whole"})
case("cat_two_files", "cat of BEMYAGENT.md and the rules file in one call: its result holds every line, but the call names a file that embeds the rules (B8): not counted whole, flagged", bash(lambda c: f"cat BEMYAGENT.md {RULES}", BEM + "\n" + FULL), {"i": "none", "du": 1, "seq_classes": ["mixed-embedding"]}, changed="whole -> none + flag (B8)")
case("whole_list_content", "a whole Read whose tool_result content is a list of text blocks", lambda t, c: (t.tool("Read", {"file_path": c.rules}, [{"type": "text", "text": numbered(FULL)}]), write_edit(t, c)), {"i": "whole"})
case("edit_rules_first", "the rules file EDITED first (a write, not an access), then read whole", lambda t, c: (t.tool("Edit", {"file_path": c.rules, "old_string": "a", "new_string": "b"}, "edited"), t.tool("Read", {"file_path": c.rules}, numbered(FULL))), {"i": "none", "write_kind": "Edit"})
case("persistent_cwd", "cat of the bare name after an earlier call left the shell in docs/ (the record's cwd)", lambda t, c: (setattr(t, "cwd", c.arm + "/.bemyagent/docs"), t.tool("Bash", {"command": "cat 00-ai-rules.md"}, FULL), setattr(t, "cwd", c.arm), write_edit(t, c)), {"i": "whole"})
case("wc_only", "wc -l of the rules file: named, not read", bash(lambda c: f"wc -l {RULES}", "108 rules"), {"i": "none", "non_reading": 1})
case("turn1_slice_then_whole", "turn 1 read a slice only; after the boundary a whole read", read_rules(), {"i": "whole", "iv": "slice"}, turn1="slice")
case("turn1_none", "turn 1 never read the rules", read_rules(), {"i": "whole", "iv": "none"}, turn1="none")
case("launcher_not_proven", "a boundary in the transcript but the launcher did not prove it", read_rules(), {"i": "whole", "eligible": False}, proven=0)
case("no_turn2_output", "turn 2 left no t2.json", read_rules(), {"i": "whole", "eligible": False}, with_t2=False)

# --- CHANGED by Amendment 1 (old expected class in the message)
case("whole_truncated_marker", "all lines present and a truncation marker appended", bash(lambda c: f"cat {RULES}", FULL + "\n... [3000 characters truncated]"), {"i": "whole"}, changed="slice -> whole (A1: the signs are recorded and decide nothing; every line is there)")
case("cat_pipe_head", "cat piped into head -300: every line is in the result", bash(lambda c: f"cat {RULES} | head -300", FULL), {"i": "whole"}, changed="slice -> whole (A1: the form decides nothing)")
case("read_error", "a Read that returns an error holding none of the lines", lambda t, c: (t.tool("Read", {"file_path": c.rules}, "File does not exist.", is_error=True), write_edit(t, c)), {"i": "attempted", "eligible": False, "reason_has": "attempted"}, changed="none -> attempted (A2), and the arm leaves (i)")
case("whole_result_after_write", "Read issued BEFORE an Edit in the same assistant message: its result comes after the Edit was issued", lambda t, c: t.tool("Read", {"file_path": c.rules}, numbered(FULL), result_after=[("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "edited")]), {"i": "whole"}, changed="none -> whole (A4: a call issued before the write in the same message is inside the window)")
case("whole_BEMYAGENT_only", "BEMYAGENT.md read whole, the rules file never", lambda t, c: (t.tool("Read", {"file_path": f"{c.arm}/BEMYAGENT.md"}, numbered(BEM)), write_edit(t, c)), {"i": "none", "other_files": 1, "du": 1, "du_names_bem": True}, changed="none stays none; new: the A3 flag, naming BEMYAGENT.md")
case("other_arms_rules", "a whole Read of ANOTHER arm's rules file by absolute path", lambda t, c: (t.tool("Read", {"file_path": str(TR / "other_arm") + "/" + RULES}, numbered(FULL)), write_edit(t, c)), {"i": "none", "unresolved": 1, "du": 1}, changed="none stays none; new: the A3 flag")
case("unresolvable_var", "cat of a $VAR path: cannot be resolved, never a hit, reported", bash(lambda c: 'cat "$ARM/.bemyagent/docs/00-ai-rules.md"', FULL), {"i": "none", "unresolved": 1, "du": 1}, changed="none stays none; new: the A3 flag")
case("backup_copy", "cat of a .bak copy of the rules file: another file, reported", bash(lambda c: f"cat {RULES}.bak", FULL), {"i": "none", "unresolved": 1, "du": 1}, changed="none stays none; new: the A3 flag")
case("two_boundaries", "an auto boundary in turn 1, then the call's: the launcher's count (1 before) cuts at number 2; the whole read between them is turn 1", lambda t, c: write_edit(t, c), {"i": "none", "boundaries": 2, "cut": 2}, boundaries=2, changed="the cut is the launcher's number, not the last (same result here)")

# --- the verifier's D1: every line delivered, whatever the form
FULLRES = FULL
for nm, inp in (("limit2000", {"limit": 2000}), ("offset1", {"offset": 1}), ("offset1_limit2000", {"offset": 1, "limit": 2000})):
    case(f"d1_read_{nm}", f"D1: Read with {inp} returning every line", read_rules(**inp), {"i": "whole"}, changed="slice -> whole (A1)")
for nm, cmd in (("sed_1_dollar", "sed -n '1,$p' {R}"), ("head_500", "head -n 500 {R}"), ("tail_plus1", "tail -n +1 {R}"), ("awk_1", "awk '1' {R}")):
    case(f"d1_{nm}", f"D1: {cmd.format(R='<rules>')} returning every line", bash(lambda c, cmd=cmd: cmd.format(R=RULES), FULL), {"i": "whole"}, changed="slice -> whole (A1)")
case("n9_error_with_text", "N9: a result marked is_error that holds every line", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL), is_error=True), write_edit(t, c)), {"i": "whole"}, changed="slice -> whole (A1)")
# --- N1: false whole
case("n1_pipe_grep_cat", "N1: cat F | grep '^## ' | cat, whose result is the eight heading lines", bash(lambda c: f"cat {RULES} | grep '^## ' | cat", heads_only), {"i": "slice"}, changed="whole -> slice (A1)")
case("n1_elided_lines", "N1: a result with twenty lines replaced by a marker", lambda t, c: (t.tool("Read", {"file_path": c.rules}, elided), write_edit(t, c)), {"i": "slice"}, changed="whole -> slice (A1)")
case("n1_tail_cut", "N1: a result with the last three lines cut", lambda t, c: (t.tool("Read", {"file_path": c.rules}, tail_cut), write_edit(t, c)), {"i": "slice"}, changed="whole -> slice (A1)")
case("n1_all_lines_out_of_order", "N1: every line is in the result but in reversed order: not 'in order', so a slice", lambda t, c: (t.tool("Read", {"file_path": c.rules}, "\n".join(reversed(LINES))), write_edit(t, c)), {"i": "slice"}, changed="whole -> slice (A1: in order)")
case("n1_unknown_prefix_still_whole", "an unknown line prefix on every line: the lines are still in the result, so whole (A1 does not depend on the prefix)", lambda t, c: (t.tool("Read", {"file_path": c.rules}, "\n".join(f"L{i + 1}| {l}" for i, l in enumerate(LINES))), write_edit(t, c)), {"i": "whole"}, changed="none/unknown -> whole (A1)")
# --- M2: turn 2 failed or ran elsewhere
case("m2_t2_failed", "M2: boundary proven, t2.json is_error, exit 1, nothing after the boundary", lambda t, c: None, {"eligible": False, "reason_has": "no write that succeeded"},
     t2json={"is_error": True, "result": "rate limit"}, t2_exit=1, t2_prompt=False)
case("m2_t2_elsewhere", "M2: t2.json carries another session id and the transcript has no turn-2 prompt", lambda t, c: None, {"eligible": False, "reason_has": "another session id"}, t2json={"session_id": "other-sid"}, t2_prompt=False)
case("m2_t2_prompt_missing", "M2: turn 2's prompt is not a user record after the boundary (actions present)", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)), {"eligible": False, "reason_has": "not a user record after the boundary"}, t2_prompt=False)
case("m2_cert_missing", "A5: the certificate is missing", read_rules(), {"i": "whole", "eligible": False, "reason_has": "certificate missing"}, cert="missing")
case("m2_cert_unclean", "A5: the certificate is not clean (the failed term is named)", read_rules(), {"i": "whole", "eligible": False, "reason_has": "no_tool_call_naming_repo"}, cert="unclean")
# --- M3: the tool withheld the text
case("m3_unchanged_stub", "M3: a Read with no parameters answered by the unchanged-file stub", lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB), write_edit(t, c)), {"i": "attempted", "eligible": False, "reason_has": "attempted"})
# --- M4: delivery the reader cannot resolve
case("m4_glob_cat", "M4: cat .bemyagent/docs/0*.md", bash(lambda c: "cat .bemyagent/docs/0*.md", "# Overview\n" + FULL), UNRES)
case("m4_for_loop", "M4: for f in .bemyagent/docs/*.md; do cat \"$f\"; done", bash(lambda c: 'for f in .bemyagent/docs/*.md; do cat "$f"; done', FULL), UNRES)
case("m4_python_open", "M4: python3 -c print(open(<rules>).read())", bash(lambda c: f"python3 -c \"print(open('{c.rules}').read())\"", FULL), {"i": "none", "du": 1, "unresolved": 0})
case("m4_write_and_read_same_call", "A3+A4: one python call prints the rules AND writes a file: the first write delivers the text, unresolved", lambda t, c: (t.tool("Bash", {"command": f"python3 -c \"t=open('{c.rules}').read(); print(t); open('copy.txt','w').write(t)\""}, FULL), write_edit(t, c)), {"i": "none", "du": 1, "write_kind": "python-write"})
case("m4_symlink", "M4: ln -s <rules> r.md, then cat r.md", lambda t, c: (t.tool("Bash", {"command": f"ln -s {c.rules} r.md"}, ""), t.tool("Bash", {"command": "cat r.md"}, FULL), write_edit(t, c)), UNRES)
case("m4_other_letter_case", "M4: the path in another letter case", lambda t, c: (t.tool("Read", {"file_path": c.arm + "/.bemyagent/docs/00-AI-RULES.md"}, numbered(FULL)), write_edit(t, c)), {"i": "none", "du": 1})
# --- M5: the cut is the launcher's number
case("m5_auto_in_turn2_read_before", "M5: whole read and edit after the call's boundary, then an automatic boundary, then edits", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c), auto_boundary(t), write_edit(t, c)), {"i": "whole", "cut": 1}, status_after=2, changed="none -> whole (A4: cut at the launcher's number; the verifier's c2)")
case("m5_auto_in_turn2_read_after", "M5: an edit, then an automatic boundary, then a whole read", lambda t, c: (write_edit(t, c), auto_boundary(t), t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)), {"i": "none", "cut": 1}, status_after=2, changed="whole -> none (A4; the verifier's c3)")
case("m5_boundary_inside_window", "A4: a further boundary inside the window is flagged", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), auto_boundary(t), write_edit(t, c)), {"i": "whole", "flag": "further boundary inside the window"}, status_after=2)
# --- N3: what counts as the first write
case("n3_failed_edit_first", "N3: a failed Edit (is_error) is not a write; a whole read after it is inside the window", lambda t, c: (t.tool("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "file has not been read yet", is_error=True), t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)), {"i": "whole"}, changed="none -> whole (A4)")
case("n3_mkdir_first", "N3: mkdir -p is a write (the census definition): a whole read after it is late", lambda t, c: (t.tool("Bash", {"command": "mkdir -p .bemyagent/work/9/9.1"}, ""), t.tool("Read", {"file_path": c.rules}, numbered(FULL))), {"i": "none", "write_kind": "mkdir"})
case("n3_stderr_redirect_first", "N3: a command with 2> err.log is a write: a whole read after it is late", lambda t, c: (t.tool("Bash", {"command": "ls 2> err.log"}, ""), t.tool("Read", {"file_path": c.rules}, numbered(FULL))), {"i": "none", "write_kind": "redirect"})
case("n3_cat_tee_same_call", "N3: cat <rules> | tee /dev/null: the read and the write are one call: the access is delivered by it", lambda t, c: (t.tool("Bash", {"command": f"cat {RULES} | tee /dev/null"}, FULL), write_edit(t, c)), {"i": "whole"}, changed="none -> whole (A4: delivered by the same call as the first write)")
case("n3_edit_then_read_same_message", "A4: an Edit issued BEFORE the Read in one assistant message: the Read is after the write", lambda t, c: t.tool("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "edited", result_after=[("Read", {"file_path": c.rules}, numbered(FULL))]), {"i": "none", "late": 1})
# --- M6: preserved across the boundary
def pres_turn1_read(t, c):             # the turn-1 read and its result are kept across the compaction
    return t.last_uuids(4)
case("m6_preserved_whole_read", "M6 (ruling 2026-11-15): the turn-1 whole read and its result preserved across the boundary: every line counts as handed back, not an occasion", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False, "pres_rules": True, "pres_types_has": "user/tool_result", "kind_has": "user(preserved tool_result)"},
     before_boundary=lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), t.assistant_text("noted")), preserve=lambda t, c: t.last_uuids(3))
case("m6_preserved_partial_result", "M6 (ruling): a preserved result holding part of the rules (a 40-line read): 0 < n < N, the arm stays", lambda t, c: write_edit(t, c), {"ii_part": True, "elig_by_half": True, "pres_rules": True, "kind_has": "user(preserved tool_result)"},
     before_boundary=lambda t, c: (t.tool("Read", {"file_path": c.rules, "limit": 40}, numbered(first(40))), t.assistant_text("noted")), preserve=lambda t, c: t.last_uuids(3))
case("t2_no_tool_call", "ruling: turn 2 ran, did not fail, made no tool call: the arm stays eligible, class none, flagged", lambda t, c: None, {"i": "none", "eligible": True, "flag": "turn2_no_tool_call"})
case("m6_preserved_user_record", "M6: a user record holding the whole rules text, preserved across the boundary: handed back", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False, "pres_rules": True},
     before_boundary=lambda t, c: t.user("Pasted for reference:\n" + FULL), preserve=lambda t, c: t.last_uuids(1))
case("m6_attach_partial", "M6: a file attachment holding sections 1-7 after the boundary", lambda t, c: write_edit(t, c), {"ii_part": True, "elig_by_half": True},
     extra_after_boundary=lambda t, c: t.file_attachment(c.rules, seven, num=HEADS[7], total=len(LINES)))

# =========================================================== Amendment 2 (B1-B10), written from its text
# --- B1: `attempted` only for a whole form that delivered no line; another form that delivers none is not an access
R_ = RULES
for nm, cmd, res in (("grep_c", f"grep -c '^## ' {R_}", "8"), ("grep_nohit", f"grep 'zzzzzz' {R_}", ""), ("grep_q", f"grep -q 'zzzzzz' {R_}", ""),
                     ("grep_l", f"grep -l 'zzzzzz' {R_}", ""), ("sed_past_end", f"sed -n '900,910p' {R_}", ""),
                     ("awk_count", "awk 'END{print NR}' " + R_, "108"), ("head_c", f"head -c 20 {R_}", FULL[:20]),
                     ("grep_o_head", f"grep -o 'zzzz' {R_} | head -3", "")):
    case(f"b1_{nm}", f"B1/R1: {cmd.split(' ' + R_)[0]} ... delivers no line: a search or a count, not an access", bash(lambda c, cmd=cmd, res=res: cmd, res), {"i": "none", "seq_classes": ["no-line"], "eligible": True}, changed="attempted -> none, the arm stays (B1)")
case("b1_read_offset_past_end", "B1/R1: a Read with an offset past the end", lambda t, c: (t.tool("Read", {"file_path": c.rules, "offset": 5000}, "Warning: the file is shorter than the offset."), write_edit(t, c)), {"i": "none", "seq_classes": ["no-line"], "eligible": True}, changed="attempted -> none (B1)")
case("b1_grep_tool_count", "B1/R1: the Grep tool in count mode", lambda t, c: (t.tool("Grep", {"pattern": "^## ", "path": c.rules, "output_mode": "count"}, "8"), write_edit(t, c)), {"i": "none", "seq_classes": ["no-line"], "eligible": True}, changed="attempted -> none (B1)")
case("b1_grep_tool_names_file", "B1/R1: the Grep tool answering with the file's name", lambda t, c: (t.tool("Grep", {"pattern": "zzzz", "path": c.rules}, c.rules), write_edit(t, c)), {"i": "none", "seq_classes": ["no-line"], "eligible": True}, changed="attempted -> none (B1)")
case("b1_read_range_stub", "B1: a Read with limit 50 answered by the unchanged stub: a range form, not an access", lambda t, c: (t.tool("Read", {"file_path": c.rules, "limit": 50}, STUB), write_edit(t, c)), {"i": "none", "seq_classes": ["no-line"], "eligible": True})
case("b1_cat_empty", "B1: cat of the file with an empty result: a whole form that delivered nothing", bash(lambda c: f"cat {RULES}", ""), {"i": "attempted", "eligible": False, "reason_has": "attempted"})
case("b1_nl_error", "B1: nl of the file returning an error text: whole form", bash(lambda c: f"nl {RULES}", "nl: no such file"), {"i": "attempted", "eligible": False})
case("b1_pager_empty", "B1: less of the file with an empty result: whole form", bash(lambda c: f"less {RULES}", ""), {"i": "attempted", "eligible": False})
case("b1_read_reaching_both_ends_stub", "B1: a Read with offset 1 and limit 5000 (reaches both ends) answered by the stub: whole form", lambda t, c: (t.tool("Read", {"file_path": c.rules, "offset": 1, "limit": 5000}, STUB), write_edit(t, c)), {"i": "attempted", "eligible": False})
case("b1_cat_pipe_grep_nohit", "B1: cat F | grep zzzz | cat delivering nothing: a filter, so a range form, not attempted", bash(lambda c: f"cat {RULES} | grep zzzz | cat", ""), {"i": "none", "seq_classes": ["no-line"], "eligible": True})
case("b1_unplaced_form", "B1: a Read with limit given as a string delivering nothing: a form the reader cannot place: not attempted, flagged", lambda t, c: (t.tool("Read", {"file_path": c.rules, "limit": "2000"}, "oops"), write_edit(t, c)), {"i": "none", "seq_classes": ["unplaced"], "eligible": True, "flag_has": "cannot place"})
case("b1_slice_and_noline", "B1: a slice and a count: the class comes from the slice", lambda t, c: (t.tool("Read", {"file_path": c.rules, "limit": 40}, numbered(first(40))), t.tool("Bash", {"command": f"grep -c zzzz {RULES}"}, "0"), write_edit(t, c)), {"i": "slice"})
case("b1_noline_then_whole", "B1: a count, then a whole read", lambda t, c: (t.tool("Bash", {"command": f"grep -c zzzz {RULES}"}, "0"), t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)), {"i": "whole"})
# --- B2: what (ii) counts
case("b2_sentinel_in_summary", "B2/R2: the arm's own instruction text (the sentinel line, one line of the rules) in the summary: not counted", lambda t, c: write_edit(t, c), {"ii_n": 0, "eligible": True}, summary="The instructions said: " + INSTR)
case("b2_fences_summary", "B2/R2: a code fence and a table rule in the summary: short lines, a fact, decide nothing", lambda t, c: write_edit(t, c), {"ii_n": 0, "short_hit": True, "eligible": True}, summary="Code:\n```\nx\n```\n|---|---|\n")
# --- B3: where (ii) looks
def raw(t, typ, **kw): return t._base(typ, **kw)
case("b3_result_no_matching_call", "B3/R3b: a result record with no matching call, holding the rules text", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False},
     extra_after_boundary=lambda t, c: raw(t, "user", message={"role": "user", "content": [{"type": "tool_result", "tool_use_id": "ghost", "content": FULL}]}))
case("b3_other_record_type", "B3/R3b: the text in a record of a type the reader has no name for", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False},
     extra_after_boundary=lambda t, c: raw(t, "custom-note", content={"x": FULL}))
case("b3_queue_operation", "B3: the text in a queue-operation record", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False},
     extra_after_boundary=lambda t, c: raw(t, "queue-operation", operation="enqueue", content=FULL))
case("b3_text_block_beside_result", "B3/R3b: a text block beside the result of an after-boundary call", lambda t, c: (t.tool("Bash", {"command": "ls"}, "x"), t.recs[-1]["message"]["content"].append({"type": "text", "text": FULL}), write_edit(t, c)), {"ii_all": True, "eligible": False})
case("b3_unmatched_result_toolUseResult", "B3/R3b: the text under toolUseResult of a record whose result matches no call", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False},
     extra_after_boundary=lambda t, c: raw(t, "user", message={"role": "user", "content": [{"type": "tool_result", "tool_use_id": "ghost2", "content": "x"}]}, toolUseResult={"file": {"content": FULL}}))
case("b3_synthetic_assistant", "B3/R3b: the text in an assistant record of another (synthetic) model", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False},
     extra_after_boundary=lambda t, c: t.assistant_text(FULL, model="<synthetic>"))
case("b3_pinned_assistant_quotes", "B3: the arm's own pinned-model assistant text quotes the rules: its own words, not counted", lambda t, c: write_edit(t, c), {"ii_n": 0, "eligible": True},
     extra_after_boundary=lambda t, c: t.assistant_text(FULL))
case("b3_own_result_toolUseResult", "B3: the same result of an after-boundary call under toolUseResult: the same result, not counted", lambda t, c: (t.tool("Bash", {"command": "ls"}, "x"), t.recs[-1].__setitem__("toolUseResult", {"file": {"content": FULL}}), write_edit(t, c)), {"ii_n": 0, "eligible": True})
case("b12b_copy_before_first_call", "B12(b): a stored request copy between the boundary and the arm's first call holding the rules text: counted", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False},
     extra_after_boundary=lambda t, c: raw(t, "api-request-blob", message={"role": "user", "content": FULL}))
case("b12b_copy_after_first_call", "B12(b): the same copy AFTER the arm's first call: left out, the number printed", lambda t, c: (t.tool("Bash", {"command": "ls"}, "x"), raw(t, "api-request-blob", message={"role": "user", "content": FULL}), write_edit(t, c)), {"ii_n": 0, "skipped": 1, "eligible": True})
case("b12b_copy_hashes_only", "C5: a copy before the first result that holds hashes no blob resolves cannot be read: counted unreadable, flagged", lambda t, c: write_edit(t, c), {"ii_n": 0, "unreadable": 1, "eligible": True, "flag_has": "cannot be read as text"},
     extra_after_boundary=lambda t, c: raw(t, "api-request", tail=["a" * 64, "b" * 64], requestDigest="c" * 64))
case("b12a_attachment_after_first_write", "B12(a): the rules in an attachment AFTER the first write: window count 0, rest-of-turn count M, the arm stays", lambda t, c: (write_edit(t, c), t.file_attachment(c.rules, FULL)), {"ii_n": 0, "rest_n": "M", "eligible": True, "flag_has": "AFTER the window's end"})
case("b12a_rest_of_turn_zero", "B12(a): nothing handed back in the rest of turn 2: 0", read_rules(), {"ii_n": 0, "rest_n": 0, "eligible": True})
# --- B4: the threshold
case("b4_half_out", "B4/R6: n >= M/2 lines handed back: the arm leaves (i), reason named", lambda t, c: write_edit(t, c), {"eligible": False, "reason_has": "x + n ="}, summary=text_half)
case("b4_below_half_stays", "B4/R6: n < M/2: reported, the arm stays", lambda t, c: write_edit(t, c), {"ii_part": True, "eligible": True}, summary=text_below)
# --- B5: shrink, preserved fields, metadata
case("b5_no_shrink", "B5/R3c: the context did not shrink at the boundary: not a compaction, the arm leaves", read_rules(), {"i": "whole", "eligible": False, "reason_has": "did not shrink"}, after_tokens=60000)
case("b5_preserved_ids_missing", "B5/R3a: the metadata names two preserved records that are not in the file", lambda t, c: write_edit(t, c), {"pres_missing": 2}, preserve=lambda t, c: ["nope1", "nope2"])
# --- B6: a failed turn 2
case("b6_failed_readonly", "B6/R4: turn 2 ran a read-only call and failed: its window never closed", lambda t, c: t.tool("Bash", {"command": "ls"}, "x"), {"eligible": False, "reason_has": "no write that succeeded"}, t2json={"is_error": True}, t2_exit=1)
case("b6_failed_after_write", "B6: turn 2 failed after a write that succeeded: the arm stays, flagged", read_rules(), {"i": "whole", "eligible": True, "flag_has": "failed after a write"}, t2json={"is_error": True}, t2_exit=1)
case("b6_killed", "C9/T8: turn 2 killed by the time limit AFTER a write that succeeded (empty t2.json): the arm stays, flagged", read_rules(), {"i": "whole", "eligible": True, "flag_has": "killed by the time limit after a write", "reason_not": "turn 2 did not run"}, t2_raw="", t2_exit=142, extra_status="ARM t2 killed by the time limit (3s)\n", changed="not eligible -> eligible (C9)")
case("c9_killed_no_write", "C9: turn 2 killed by the time limit with no write: the arm leaves, named so", lambda t, c: t.tool("Read", {"file_path": c.rules}, numbered(FULL)), {"eligible": False, "reason_has": "turn 2 killed by the time limit", "reason_not": "turn 2 did not run"}, t2_raw="", t2_exit=142, extra_status="ARM t2 killed by the time limit (3s)\n")
# --- B7: the compaction call's exit code
case("b7_cp_exit", "B7/R5: the compaction call exited 1 though a boundary was written: the arm is left out", read_rules(), {"i": "whole", "eligible": False, "reason_has": "compaction call exited 1"}, cp_exit=1)
# --- B8: the window
case("b8_failed_shell_write", "B8/R7a: a shell write that returned an error is still a write: the whole read after it is late", lambda t, c: (t.tool("Bash", {"command": "npm test > out.txt 2>&1"}, "FAIL", is_error=True), t.tool("Read", {"file_path": c.rules}, numbered(FULL))), {"i": "none", "write_kind": "redirect"}, changed="whole -> none (B8)")
case("b8_one_record_read_then_edit", "B8/R7c: one assistant record, Read block then Edit block: the Read was issued before the write", lambda t, c: t.tools_one_record([("Read", {"file_path": c.rules}, numbered(FULL)), ("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "edited")]), {"i": "whole"})
case("b8_one_record_edit_then_read", "B8/R7c: one assistant record, Edit block then Read block: the Read was issued after the write", lambda t, c: t.tools_one_record([("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "edited"), ("Read", {"file_path": c.rules}, numbered(FULL))]), {"i": "none", "late": 1}, changed="whole -> none (B8)")
case("b8_head_and_bemyagent", "B8/R8: head -3 <rules>; cat BEMYAGENT.md - the result holds every line through the other file: flagged, not whole", bash(lambda c: f"head -3 {RULES}; cat BEMYAGENT.md", first(3) + "\n" + BEM), {"i": "none", "du": 1, "seq_classes": ["mixed-embedding"]}, changed="whole -> none + flag (B8)")
case("b8_wc_and_bemyagent", "B8: wc -l <rules> && cat BEMYAGENT.md: flagged through the other file", bash(lambda c: f"wc -l {RULES} && cat BEMYAGENT.md", "108\n" + BEM), {"i": "none", "du": 1})
case("b8_rules_changed_in_turn1", "B8/R9: the arm changed its rules file in turn 1: the lines come from the turn-1 snapshot; flagged", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(RULES_C + "\nAn extra line the arm added in turn 1.\n")), write_edit(t, c)), {"i": "whole", "flag_has": "changed its rules file in turn 1"},
     snap_rules=RULES_C + "\nAn extra line the arm added in turn 1.\n", setup_orig=RULES_C, tree_rules=RULES_C + "\nAn extra line the arm added in turn 1.\n", changed="slice -> whole (B8)")
case("b8_rules_changed_after_reading", "B8/R9: the arm added a line to its rules file AFTER reading it: the snapshot's lines decide, the read was whole", lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(RULES_C)), write_edit(t, c)), {"i": "whole", "flag_has": "final tree differs"},
     snap_rules=RULES_C, setup_orig=RULES_C, tree_rules=RULES_C + "\nAn extra line added later.\n", changed="slice -> whole (B8)")
case("b8_cert_fails_only_late", "B8/R10: the certificate fails only on a call after the window's end: the arm stays, flagged", read_rules(), {"i": "whole", "eligible": True, "flag_has": "only on calls after the window's end"}, cert="late")
case("b8_cert_fails_inside", "B8: the certificate fails on a call inside the window: the arm leaves", read_rules(), {"eligible": False, "reason_has": "no_tool_call_naming_repo"}, cert="early")
case("b8_cert_fail_not_placed", "B8: a failing term the certificate could not place: the arm leaves", read_rules(), {"eligible": False}, cert="unplaced")

# =========================================================== Amendment 3 (C1-C9), written from its text
# --- C1: a withheld whole read wins over a slice; a delivery is a line of K
case("c1_stub_then_slices", "C1/T2b: the stub on a whole Read, then two ranged reads of 45 lines: attempted wins, the arm leaves", lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB), t.tool("Read", {"file_path": c.rules, "limit": 45}, numbered(first(45))), t.tool("Read", {"file_path": c.rules, "offset": 46, "limit": 45}, "\n".join(LINES[45:90])), write_edit(t, c)), {"i": "attempted", "eligible": False, "reason_has": "attempted"}, changed="slice -> attempted (C1)")
case("c1_stub_with_fence_reminder", "C1/T2a: the stub followed by a reminder holding two code-fence lines: not a delivery, attempted", lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB + "\n```\n```\n"), write_edit(t, c)), {"i": "attempted", "eligible": False}, changed="slice -> attempted (C1)")
case("c1_stub_with_instruction_line", "C1/T2a: the stub followed by the instruction file's one line: not a delivery, attempted", lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB + "\n" + INSTR), write_edit(t, c)), {"i": "attempted", "eligible": False}, changed="slice -> attempted (C1)")
case("c1_stub_then_whole", "C1: the stub, then a whole cat that delivers: whole (the withheld access is listed)", lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB), t.tool("Bash", {"command": f"cat {RULES}"}, FULL), write_edit(t, c)), {"i": "whole", "seq_classes": ["attempted", "whole"], "eligible": True})
# --- C2: a print the agent never sees
for nm, cmd, res in (("devnull", f"cat {RULES} > /dev/null", ""), ("devnull_and_echo", f"cat {RULES} >/dev/null 2>&1 && echo present", "present"),
                     ("pbcopy", f"cat {RULES} | pbcopy", ""), ("python_len", f"cat {RULES} | python3 -c 'import sys; print(len(sys.stdin.read()))'", "9123"),
                     ("node", f"cat {RULES} | node -e 'process.stdin.resume()'", ""), ("while_read", f"cat {RULES} | while read l; do :; done", "")):
    case(f"c2_{nm}", f"C2/T1: {cmd.split(RULES)[0].strip()} ... {cmd.split(RULES)[1].strip()[:30]}: the output never comes back: unplaced, flagged, not attempted", bash(lambda c, cmd=cmd: cmd, res), {"i": "none", "seq_classes": ["unplaced"], "eligible": True, "flag_has": "cannot place"}, changed="attempted -> none + flag (C2)")
case("c2_md5_not_an_access", "C2: cat F | md5 is not an access (a checksum)", bash(lambda c: f"cat {RULES} | md5", "d41d8cd98f00b204e9800998ecf8427e"), {"i": "none", "seq_classes": [], "eligible": True})
case("c2_less_grep_c", "C2: less F | grep -c: a filter, no-line", bash(lambda c: f"less {RULES} | grep -c zzzz", "0"), {"i": "none", "seq_classes": ["no-line"], "eligible": True})
case("c2_stderr_only_still_whole", "C2: cat F 2>/dev/null (only stderr away): the output comes back: whole", bash(lambda c: f"cat {RULES} 2>/dev/null", FULL), {"i": "whole"})
# --- C3: one list K, x + n, one threshold
KLINES = [l for l in NONEMPTY if len(l) >= 20 and l.rstrip() not in INSTR]
assert len(KLINES) == 86
instr20 = INSTR + "\n".join(KLINES[:20]) + "\n"
text20_40 = "\n".join(KLINES[20:40]); text20_45 = "\n".join(KLINES[20:45])
def xn_arm(name_cond): return None
case("c3_x_and_n_below", "C3/T7: the instruction file holds 20 lines of K (x = 20) and 20 other lines are handed back (n = 20): x + n = 40 < 43, the arm stays", lambda t, c: write_edit(t, c), {"xn_cmp": (20, "n", 40), "eligible": True}, summary=text20_40, snap_rules=RULES_C, snap_instr=instr20, claude_md=instr20)
case("c3_x_plus_n_leaves", "C3: x = 20 and n = 25: x + n = 45 >= 43, the arm leaves", lambda t, c: write_edit(t, c), {"eligible": False, "reason_has": "x + n = 20 + 25 = 45"}, summary=text20_45, snap_rules=RULES_C, snap_instr=instr20, claude_md=instr20)
L_RULES = RULES_C.splitlines(); L_RULES.insert(1, ADDED_LINE := "**Read this file whole — first line to last, every time, a context compaction included. A slice of it, or what you recall of it, is not a read.**"); L_RULES = "\n".join(L_RULES) + "\n"
case("c3_same_hand_back_C", "C3/T7: the same 43 lines handed back in a C arm: x + n = 43, leaves", lambda t, c: write_edit(t, c), {"eligible": False, "reason_has": "x + n = 0 + 43 = 43"}, summary=text_half, snap_rules=RULES_C)
case("c3_same_hand_back_L", "C3/T7: the same 43 lines handed back in an L arm (87 lines in its file): x + n = 43, leaves too; the added line was not handed back", lambda t, c: write_edit(t, c), {"eligible": False, "reason_has": "x + n = 0 + 43 = 43", "added": False}, summary=text_half, snap_rules=L_RULES, tree_rules=L_RULES)
case("c3_added_line_handed_back", "C3: an L arm whose summary quotes the added line: reported yes, decides nothing (n = 0, the arm stays)", lambda t, c: write_edit(t, c), {"ii_n": 0, "added": True, "eligible": True}, summary="The rules say: " + ADDED_LINE, snap_rules=L_RULES, tree_rules=L_RULES)
case("c3_added_line_none_in_C", "C3: a C arm has no added line: reported None", lambda t, c: write_edit(t, c), {"ii_n": 0, "added": None, "eligible": True}, snap_rules=RULES_C)
# --- C4: calls through ..
case("c4_dotdot_flag", "C4/T9: the certificate counts 2 calls through `..`: carried into the arm's row and flagged", read_rules(), {"i": "whole", "dotdot": 2, "flag_has": "through `..`", "eligible": True}, cert_dotdot=2)
# --- C5: request copies up to the first tool result
def call_copy_result(t, c, copy_fn):
    tid = "tcopy1"
    t._base("assistant", message={"role": "assistant", "id": "mcopy", "model": synth.MODEL, "content": [{"type": "tool_use", "id": tid, "name": "Bash", "input": {"command": "ls"}}],
            "usage": {"input_tokens": 5, "cache_read_input_tokens": t.tokens, "cache_creation_input_tokens": 100, "output_tokens": 10}})
    copy_fn(t)
    t._base("user", message={"role": "user", "content": [{"type": "tool_result", "tool_use_id": tid, "content": "x"}]}, toolUseResult={"type": "text"})
case("c5_copy_between_call_and_result", "C5/T3: a request copy right after the first call and before its result, holding every line: counted", lambda t, c: (call_copy_result(t, c, lambda t: raw(t, "api-request-blob", message={"role": "user", "content": FULL})), write_edit(t, c)), {"ii_all": True, "eligible": False})
HASH = "e" * 64
case("c5_hash_list_resolved", "C5/T4c: a copy that is a list of hashes pointing at a stored blob (stored BEFORE the boundary): resolved, counted", lambda t, c: write_edit(t, c), {"ii_all": True, "eligible": False, "unreadable": 0},
     before_boundary=lambda t, c: raw(t, "api-request-blob", hash=HASH, message={"role": "user", "content": FULL}), extra_after_boundary=lambda t, c: raw(t, "api-request", tail=[HASH], requestDigest="d" * 64))
# --- C6: the token numbers
def zero_usage_synthetic(t, c):
    keep = t.tokens; t.tokens = 0; t.assistant_text("No response requested.", model="<synthetic>"); t.tokens = keep
case("c6_synthetic_zero_usage_first", "C6/T6a: a synthetic zero-usage record first after the boundary is not a token number", lambda t, c: write_edit(t, c), {"shrank": True, "eligible": True, "disagree": False}, extra_after_boundary=zero_usage_synthetic)
def sidechain_small(t, c):
    keep = t.tokens; t.tokens = 905; t.assistant_text("side"); t.recs[-1]["isSidechain"] = True; t.tokens = keep
case("c6_sidechain_first", "C6/T6b: a side-chain record with a small prompt first after the boundary is not counted", lambda t, c: write_edit(t, c), {"shrank": True, "eligible": True, "disagree": False}, extra_after_boundary=sidechain_small)
case("c6_pairs_disagree", "C6/T6c: a small main-chain record last before the boundary: the records say no shrink, the boundary says shrink: they disagree, the boundary decides, the arm stays, flagged", lambda t, c: write_edit(t, c), {"shrank": True, "eligible": True, "disagree": True, "flag_has": "disagree on the direction"}, small_before=2000, after_tokens=20000)
BND = {"trigger": "manual", "preTokens": 60000, "postTokens": 9000, "preservedSegment": {}, "durationMs": 1}      # the boundary says: shrank
case("c6_zero_usage_cannot_hide_no_shrink", "C6: the real records do not shrink (50000 -> 60000) but a zero-usage synthetic record comes first: it is not a number, so the pairs disagree (flagged)", lambda t, c: write_edit(t, c), {"disagree": True, "shrank": True, "eligible": True, "flag_has": "disagree on the direction"}, extra_after_boundary=zero_usage_synthetic, after_tokens=60000, meta=BND)
case("c6_sidechain_cannot_hide_no_shrink", "C6: the same with a side-chain record with a small prompt first after the boundary", lambda t, c: write_edit(t, c), {"disagree": True, "shrank": True, "eligible": True}, extra_after_boundary=sidechain_small, after_tokens=60000, meta=BND)
# --- C7: rules in the result of a call that did not ask for them
case("c7_rules_in_ls_result", "C7/T10: the result of `ls client` carries 60 lines of the rules: printed, flagged; the result is the arm's own, n stays 0", lambda t, c: (t.tool("Bash", {"command": "ls client"}, "app.js\n" + "\n".join(KLINES[:60])), write_edit(t, c)), {"ii_n": 0, "other_call_rules": 1, "flag_has": "did not name the rules file", "eligible": True})
# --- C8: what the reader cannot read
case("c8_unparsed_line", "C8/T11: a line after the boundary that is not JSON: counted, flagged", lambda t, c: write_edit(t, c), {"unparsed": 1, "flag_has": "do not parse", "eligible": True}, junk_lines=("this is not json " + KLINES[0],))
case("c8_metadata_not_object", "C8/T12: the boundary's metadata is a string: flagged, no traceback, the read goes on", lambda t, c: write_edit(t, c), {"md_shape": "not an object", "flag_has": "metadata is not an object"}, meta="oops")
case("c8_metadata_absent", "C8/T12: the boundary has no metadata: flagged", lambda t, c: write_edit(t, c), {"md_shape": "absent", "flag_has": "metadata is absent"}, meta="absent")

# =========================================================== Amendment 4 (D1-D6, G1-G3, X1, P1), written from its text
def touch_five(t, c):
    for k in range(5): t.tool("Edit", {"file_path": f"{c.arm}/client/f{k}.js", "old_string": "a", "new_string": "b"}, "edited")
case("d1_design_four", "D1: a four-call arm (turn 1, turn 1b, compaction, turn 2) is read as four calls", read_rules(), {"i": "whole", "eligible": True, "design": "4 calls"}, four=True)
case("d1_design_three", "D1: q901's three-call design is still read as it was", read_rules(), {"i": "whole", "eligible": True, "design": "3 calls"})
case("d2_reference_after_boundary", "D2: a compact_file_reference to the rules file after the boundary: the occasion was not produced, the arm leaves", read_rules(), {"i": "whole", "eligible": False, "reason_has": "names the rules file", "occ_kinds": ["reference"]}, four=True, extra_after_boundary=lambda t, c: t.file_reference(c.rules))
case("d2_text_attachment_after_boundary", "D2: a file attachment of the rules after the boundary", read_rules(), {"eligible": False, "reason_has": "names the rules file", "occ_kinds": ["text-attachment"]}, four=True, extra_after_boundary=lambda t, c: t.file_attachment(c.rules, FULL))
case("d2_name_only_attachment", "D2: any other attachment that names the rules file", read_rules(), {"eligible": False, "occ_kinds": ["name"]}, four=True, extra_after_boundary=lambda t, c: t.other_attachment("skill_listing", content="see .bemyagent/docs/00-ai-rules.md"))
case("d2_instruction_attachment_is_not_one", "D2: the instruction attachment (it names the file by the sentinel) is not counted", read_rules(), {"i": "whole", "eligible": True, "occ_kinds": []}, four=True)
case("d2_files_touched", "D2: seven distinct files touched before the boundary (rules, app.js, five more in turn 1b): printed", read_rules(), {"occ_files": 7, "eligible": True}, four=True, t1b_actions=lambda t, c: touch_five(t, c))
case("d4_ivb_whole", "D4: turn 1b starts with a whole read of the rules: (iv-b) whole, deciding nothing", read_rules(), {"ivb": "whole", "i": "whole", "eligible": True}, four=True, t1b_actions=lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)))
case("d4_ivb_none", "D4: turn 1b never reads the rules: (iv-b) none; the arm is unaffected", read_rules(), {"ivb": "none", "i": "whole", "eligible": True}, four=True)
case("d4_ivb_null_three_call", "D4: a three-call transcript has no turn-1b prompt: (iv-b) null with the reason", read_rules(), {"ivb": None, "eligible": True})
case("x1_rules_in_write_result", "X1: lines of K in the result of an Edit that does not name the rules file are listed", lambda t, c: t.tool("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "edited\n" + "\n".join(KLINES[:60])), {"other_call_rules": 1, "ii_n": 0, "flag_has": "did not name the rules file", "eligible": True})
case("x1_failed_edit_result", "X1: the same in a failed Edit inside the window, before the first write that succeeds", lambda t, c: (t.tool("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "file has not been read yet\n" + "\n".join(KLINES[:60]), is_error=True), write_edit(t, c)), {"other_call_rules": 1, "flag_has": "did not name the rules file"})

case("d6_empty_content_blob", "D6: a blob copy before the first tool result whose content is an empty list: read, 0 lines, no flag, the arm stays", lambda t, c: write_edit(t, c), {"ii_n": 0, "unreadable": 0, "eligible": True, "no_flag": "cannot be read as text"},
     extra_after_boundary=lambda t, c: raw(t, "api-request-blob", hash="a1" * 32, message={"role": "user", "content": [], "output_config": {"effort": "high"}}))
case("d6_text_blocks_blob_with_rules", "D6: a blob whose text blocks hold the rules before the first tool result: counted", lambda t, c: write_edit(t, c), {"ii_all": True, "unreadable": 0, "eligible": False},
     extra_after_boundary=lambda t, c: raw(t, "api-request-blob", hash="a2" * 32, message={"role": "user", "content": [{"type": "text", "text": FULL}]}))
case("d6_unknown_block_type", "D6: a blob whose content has a block of an unknown type: unreadable, flagged", lambda t, c: write_edit(t, c), {"unreadable": 1, "flag_has": "cannot be read as text", "eligible": True},
     extra_after_boundary=lambda t, c: raw(t, "api-request-blob", hash="a3" * 32, message={"role": "user", "content": [{"type": "zzz_unknown", "data": "x"}]}))
case("d6_content_not_string_or_list", "D6: a blob whose content is a number: unreadable", lambda t, c: write_edit(t, c), {"unreadable": 1, "eligible": True},
     extra_after_boundary=lambda t, c: raw(t, "api-request-blob", hash="a4" * 32, message={"role": "user", "content": 7}))
case("d6_hash_resolves_to_empty_blob", "D6: a copy listing a hash that resolves to a stored blob with empty content: read, 0 lines", lambda t, c: write_edit(t, c), {"ii_n": 0, "unreadable": 0, "eligible": True},
     before_boundary=lambda t, c: raw(t, "api-request-blob", hash="b" * 64, message={"role": "user", "content": []}), extra_after_boundary=lambda t, c: raw(t, "api-request", tail=["b" * 64]))
build_tree("other_arm")
for name, what, after, exp, kw in CASES:
    kw = {k: v for k, v in kw.items() if k != "changed"}
    make(name, after, **kw)

# ---- the per-condition counts: a pilot, an ineligible arm, an attempted arm, the control first
def seq(name, after, **kw): make(name, after, **kw)
seq("q901", read_rules()); seq("q112", read_rules()); seq("q113", bash(lambda c: f"head -60 {RULES}", first(60))); seq("q114", lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB), t.tool("Bash", {"command": f"cat {RULES}"}, FULL), write_edit(t, c)))   # withheld, then whole: whole, listed
seq("q115", read_rules()); seq("q116", read_rules(), summary=FULL); seq("q117", lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB), write_edit(t, c)))

# ---- certificate cases
FAKE_BASE = str(ST / "fake_base")
def cmake(name, tweak=None, status_sha_ok=True, cp_sid=None, first_user=None, instr_path=None, n_override=2, model=synth.MODEL, cwd_out=False,
          models_in_result=("claude-sonnet-5-5",), after=None, t1read="whole", summary="A summary of the work so far.", post=None, preserve=False, cert_extra=None, after_tokens=20000, pres_ids=None, extra_md=None, claude_md=None, rules_override=None, small_before=None, meta=None, junk_lines=(), four=False, t1b_sid=None, t1b_prompt=None, t1b_hash_ok=True):
    c = Ctx(name); build_tree(name, rules_override)
    if claude_md is not None: (TR / name / "CLAUDE.md").write_text(claude_md)
    sid = f"{name}-sid"; t = synth.T(c.arm, sid)
    t.instructions(path=instr_path, n_override=n_override); t.user(first_user if first_user is not None else T1.replace("<ARM_DIR>", c.arm))
    if t1read == "whole": t.tool("Read", {"file_path": c.rules}, numbered(FULL), model=model)
    elif t1read == "wrapped":                 # every long line wrapped at 60 characters: the lines are not in the result
        wrapped = "\n".join(w for l in LINES for w in (re.findall(r".{1,60}", l) or [""]))
        t.tool("Read", {"file_path": c.rules}, numbered(wrapped), model=model)
    elif t1read == "part": t.tool("Read", {"file_path": c.rules, "limit": 40}, numbered(first(40)), model=model)
    elif t1read == "prefix": t.tool("Read", {"file_path": c.rules}, "\n".join(f"L{i + 1}| {l}" for i, l in enumerate(LINES)), model=model)
    write_edit(t, c); t.assistant_text("done", model=model)
    if four: t.user(t1b_prompt if t1b_prompt is not None else T1B); write_edit(t, c); t.assistant_text("done 1b", model=model)
    if small_before: t.tokens = small_before; t.assistant_text("small"); t.tokens = 50000
    if tweak: tweak(t, c)
    if cwd_out:
        t.cwd = "/somewhere/else"; t.assistant_text("x"); t.cwd = c.arm
    pres = pres_ids or (t.last_uuids(5) if preserve else None)
    t.tokens = after_tokens                       # B5: the context must shrink at the boundary
    b = t.boundary(preserved=pres, extra_md=extra_md, pre=50000, post=after_tokens); t.summary(summary); t.instructions(path=instr_path, n_override=n_override)
    if meta == "absent": del b["compactMetadata"]
    elif meta is not None: b["compactMetadata"] = meta
    if post: post(t, c)
    t.manual_compact_tail()
    t.user(T2)
    (after or (lambda t, c: (t.tool("Bash", {"command": f"head -40 {RULES}"}, first(40)), write_edit(t, c))))(t, c)      # the default pilot's turn 2 reads a slice
    t.assistant_text("fin")
    path = t.write(CFG)
    for jl in junk_lines:
        with open(path, "a") as f: f.write(jl + "\n")
    mu = {m: {"inputTokens": 1, "cacheCreationInputTokens": 1, "cacheReadInputTokens": 1, "outputTokens": 1} for m in models_in_result}
    (OUTD / f"{name}.t1.json").write_text(json.dumps({"session_id": sid, "is_error": False, "modelUsage": mu, "permission_denials": []}))
    (OUTD / f"{name}.t2.json").write_text(json.dumps({"session_id": sid, "is_error": False, "modelUsage": mu, "permission_denials": []}))
    if four: (OUTD / f"{name}.t1b.json").write_text(json.dumps({"session_id": t1b_sid or sid, "is_error": False, "modelUsage": mu, "permission_denials": []}))
    with open(OUTD / f"{name}.cp.jsonl", "w") as f:
        f.write(json.dumps({"type": "system", "subtype": "init", "session_id": cp_sid or sid}) + "\n")
        f.write(json.dumps({"type": "system", "subtype": "compact_boundary", "session_id": cp_sid or sid, "compact_metadata": {"trigger": "manual", "pre_tokens": 60000}}) + "\n")
        f.write(json.dumps({"type": "result", "session_id": cp_sid or sid, "is_error": False, "modelUsage": mu}) + "\n")
    good = lambda x: x if status_sha_ok else "0" * 64
    with open(OUTD / "launch.status", "a") as f:
        f.write(f"{name} prompts t1_sha={good(sha(T1.replace('<ARM_DIR>', c.arm)))}{(' t1b_sha=' + (sha(T1B) if t1b_hash_ok else '0' * 64)) if four else ''} cp_sha={sha(TC)} t2_sha={sha(T2)}\n{name} t1 exit=0\n{(name + ' t1b exit=0 resumed_from=x' + chr(10)) if four else ''}{name} memory_existed=0 files=0\n{name} boundaries_before=0\n{name} cp exit=0\n"
                f"{name} compaction_proven=1 by=both pre_tokens=60000 session_same=1 trigger=manual boundaries_before=0 boundaries_after=1\n{name} t2 exit=0 resumed_from=x\n")
    return c

CERT = []
def ccase(name, what, exp, **kw): CERT.append((name, what, exp, kw))
ccase("c_ok", "a clean arm", {"clean": True, "design_ok": True, "same": True})
ccase("c_repo", "a tool call names the repo", {"clean": False, "term": "no_tool_call_naming_repo"}, tweak=lambda t, c: t.tool("Bash", {"command": "ls " + str(ROOT) + "/harness"}, "x"))
ccase("c_base", "a tool call names the folder sessions start in", {"clean": False, "term": "no_tool_call_naming_base"}, tweak=lambda t, c: t.tool("Bash", {"command": "ls " + FAKE_BASE}, "x"))
ccase("c_instr_out", "an instruction record outside the arm", {"clean": False, "term": "no_instruction_file_outside_arm"}, instr_path=str(ROOT) + "/AGENTS.md")
ccase("c_split_session", "the compaction call reports another session id", {"design_ok": False, "same": False}, cp_sid="another-sid")
ccase("c_model", "an assistant record of the main chain from another model", {"clean": False, "term": "model_pinned_on_main_chain"}, model="claude-haiku-4")
ccase("c_model_result", "a helper model in modelUsage: printed, not a stop (A6)", {"clean": True, "second_model": True}, models_in_result=("claude-sonnet-5-5", "claude-haiku-4"))
ccase("c_sidechain_model", "an assistant record of a SIDECHAIN from another model: the pin is read on the main chain", {"clean": True},
      tweak=lambda t, c: (t.assistant_text("side", model="claude-haiku-4"), t.recs[-1].__setitem__("isSidechain", True)))
ccase("c_own_memory", "the arm reads its OWN memory folder", {"clean": True, "own_memory": 1}, tweak=lambda t, c: t.tool("Bash", {"command": "cat " + str(CFG) + "/" + re.sub(r"[^A-Za-z0-9]", "-", c.arm) + "/memory/MEMORY.md"}, "x"))
ccase("c_other_memory", "the arm reads another project's memory folder", {"clean": False, "term": "no_tool_call_naming_apparatus"}, tweak=lambda t, c: t.tool("Bash", {"command": "cat " + str(CFG) + "/-some-other-project/memory/a.md"}, "x"))
ccase("c_sibling", "a call into a sibling arm by absolute path", {"clean": False}, tweak=lambda t, c: t.tool("Bash", {"command": "cat " + str(TR) + "/c_ok/CLAUDE.md"}, "x"))
ccase("c_sibling_tmp", "the same, spelled /tmp instead of /private/tmp", {"clean": False}, tweak=lambda t, c: t.tool("Bash", {"command": "cat " + str(TR / 'c_ok').replace("/private/tmp", "/tmp", 1) + "/CLAUDE.md"}, "x"))
ccase("c_round_parent", "a call into the round's parent folder", {"clean": False}, tweak=lambda t, c: t.tool("Bash", {"command": "ls " + str(TR.parent)}, "x"))
ccase("c_dotdot_climb", "an absolute path that climbs out with ..", {"clean": False}, tweak=lambda t, c: t.tool("Bash", {"command": "cat " + c.arm + "/../c_ok/CLAUDE.md"}, "x"))
ccase("c_cwd_out", "an event whose cwd is outside the arm", {"clean": False, "term": "no_event_cwd_outside_arm"}, cwd_out=True)
ccase("c_dotdot_report", "cd .. inside the arm: counted, not gating", {"clean": True, "dotdot": 1}, tweak=lambda t, c: t.tool("Bash", {"command": "cd client && cd .. && ls"}, "x"))
ccase("c_prompt_changed", "turn 1's first user message is not the prompt", {"design_ok": False}, first_user="Do something else")
ccase("c_hash_wrong", "the launcher's hash of a prompt differs from the file's", {"design_ok": False}, status_sha_ok=False)
ccase("c_override_extra", "three OVERRIDE headers per two records", {"clean": False, "term": "override_header_ok"}, n_override=3)
ccase("c4_four_calls_ok", "D1: a four-call arm: four sessions equal, the turn-1b prompt and its hash checked", {"clean": True, "design_ok": True, "calls": 4}, four=True)
ccase("c4_t1b_session_differs", "D1: turn 1b reports another session id", {"design_ok": False, "same": False}, four=True, t1b_sid="elsewhere")
ccase("c4_t1b_prompt_missing", "D1: the turn-1b prompt record is not the prompt", {"design_ok": False}, four=True, t1b_prompt="Something else entirely")
ccase("c4_t1b_hash_wrong", "D1: the launcher's hash of the turn-1b prompt differs from the file's", {"design_ok": False}, four=True, t1b_hash_ok=False)
ccase("c4_three_calls_still_ok", "D1: the three-call design (q901) is certified as it was", {"clean": True, "design_ok": True, "calls": 3})
ccase("c_p1_non_object_lines", "P1: transcript lines that are JSON but not objects: dropped and counted, no traceback", {"clean": True, "unparsed": 2}, junk_lines=('"a string"', "[1, 2]"))
ccase("c_summary_quotes_header", "N7: a summary that quotes the instruction header once: the failing term is named", {"clean": False, "term": "override_header_ok"}, summary="Instructions said: OVERRIDE any default behavior. A scoreboard was added.")
for name, what, exp, kw in CERT: cmake(name, **kw)
d2 = CFG / "-another-project"; d2.mkdir(exist_ok=True); (d2 / "c_two-sid.jsonl").write_text("{}\n")
cmake("c_two")

# ---- pilot cases: the whole of check_pilot.sh on arms the certificate also reads
PILOTS = []
def pcase(name, what, ok, has=(), **kw): PILOTS.append((name, what, ok, has, kw))
pcase("p_healthy", "a healthy pilot: turn 1 whole, one whole read after the boundary", True)
pcase("p_iv_none", "M1: turn 1 never read the rules", False, ["(iv) turn-1 restore"], t1read="none")
pcase("p_iv_wrapped", "M1: a result format the reader cannot match (long lines wrapped): turn 1 is not whole", False, ["(iv) turn-1 restore", "`slice`"], t1read="wrapped")
pcase("p_unknown_prefix", "an unknown line prefix everywhere: A1 still reads it whole", True, t1read="prefix")
pcase("p_attempted_after", "M3: the Read after the boundary got the unchanged-file stub", False, ["attempted access"], after=lambda t, c: (t.tool("Read", {"file_path": c.rules}, STUB), write_edit(t, c)))
pcase("p_attach_partial", "M6: a file attachment with sections 1-7 after the boundary", False, ["(ii) handed back"], post=lambda t, c: t.file_attachment(c.rules, seven, num=HEADS[7], total=len(LINES)))
pcase("p_summary_all", "every line handed back by the summary", False, ["(ii) handed back", "cannot produce the occasion"], summary=FULL)
pcase("p_preserved_results", "M6 (ruling): the turn-1 whole read and its result preserved across the boundary: every line handed back", False, ["preserved across the boundary", "cannot produce the occasion"], preserve=True)
pcase("p_preserved_partial", "M6 (ruling): a preserved 40-line result: partly handed back, the pilot stops for the designer", False, ["(ii) handed back", "designer's ruling", "preserved across the boundary"], preserve=True, t1read="part")
pcase("p_t2_no_tool_call", "ruling: turn 2 made no tool call: NOT OK with its own check name", False, ["[turn 2 no tool call]"], after=lambda t, c: None)
pcase("p_unclean_term", "a tool call names the repo: the failing term is printed", False, ["certificate clean", "no_tool_call_naming_repo"], tweak=lambda t, c: t.tool("Bash", {"command": "ls " + str(ROOT) + "/harness"}, "x"))
pcase("p_second_model_usage", "N7/A6: a second model in modelUsage is printed, not a stop", True, ["second model in usage (printed, not a stop)=['claude-haiku-4']"], models_in_result=("claude-sonnet-5-5", "claude-haiku-4"))
pcase("p_search_only", "B1: turn 2 only searches the rules (a count): not attempted, the pilot is not stopped for it", True, after=lambda t, c: (t.tool("Bash", {"command": f"grep -c zzzz {RULES}"}, "0"), write_edit(t, c)))
pcase("p_fences_summary", "B2/R2: a code fence and a table rule in the summary: a fact, not a stop", True, ["short lines hit (fact, decides nothing): "], summary="```\nx\n```\n|---|---|\n")
pcase("p_sentinel_record", "B2/R2 + D2: the instruction text (it names the rules file) carried by an attachment of another type after the boundary: n = 0, but D2's occasion gate stops", False, ["[occasion]"], post=lambda t, c: t.other_attachment("note", content=INSTR))
pcase("p_rules_in_other_record_type", "B3/R3b: the rules text in a record of an unnamed type after the boundary: counted, the pilot stops", False, ["(ii) handed back"], post=lambda t, c: t._base("custom-note", content={"x": FULL}))
pcase("p_request_copy_before_call", "B12(b): a request copy with the rules text before the arm's first call counts: the pilot stops", False, ["(ii) handed back"], post=lambda t, c: t._base("api-request-blob", message={"role": "user", "content": FULL}))
pcase("p_request_copy_after_call", "B12(b): the same copy after the arm's first call is left out: no stop", True, ["request copies left out: 1"], after=lambda t, c: (t.tool("Bash", {"command": f"head -40 {RULES}"}, first(40)), t._base("api-request-blob", message={"role": "user", "content": FULL}), write_edit(t, c)))
pcase("p_rest_of_turn", "B12(a): the rules in an attachment after the first write: the pilot stops on the rest-of-turn count", False, ["[(ii) rest of turn 2]"], after=lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c), t.file_attachment(c.rules, FULL)))
pcase("p_no_shrink", "B5/R3c: the context did not shrink at the boundary", False, ["[context shrink]"], after_tokens=60000)
pcase("p_preserved_ids_missing", "B5/R3a: preserved records named but not in the file", False, ["[preserved fields]"], pres_ids=["nope1", "nope2"])
pcase("p_preserved_bad_shape", "B5/R3a: a preserved field of an unexpected shape", False, ["[preserved fields]", "unexpected"], extra_md={"preservedMessages": "oops"})
pcase("p_unknown_metadata_key", "B5/R3d: a key in the boundary's metadata the reader does not know: its name is printed", False, ["[boundary metadata]", "keptRecords"], extra_md={"keptRecords": ["x"]})
pcase("p_x_nonzero", "C3/T5a: the instruction file holds 5 lines of K: the tree is not the designed one", False, ["[instruction file]"], claude_md=INSTR + "\n".join(KLINES[:5]) + "\n")
pcase("p_snapshot_k_wrong", "C3/T5: the snapshot's rules file gives 85 of the 86 lines of K", False, ["[snapshot rules file]"], rules_override=RULES_C.replace(KLINES[0] + "\n", "", 1))
pcase("p_copy_empty_content", "D6: a blob copy with an empty content list before the first tool result: not a stop", True, post=lambda t, c: t._base("api-request-blob", hash="a5" * 32, message={"role": "user", "content": []}))
pcase("p_copy_unknown_block", "D6: a blob copy with an unknown block type: a stop", False, ["[request copies]"], post=lambda t, c: t._base("api-request-blob", hash="a6" * 32, message={"role": "user", "content": [{"type": "zzz_unknown"}]}))
pcase("p_copy_unreadable", "C5/T4: a request copy before the first tool result that cannot be read as text", False, ["[request copies]"], post=lambda t, c: t._base("api-request", tail=["f" * 64]))
pcase("p_pairs_disagree", "C6/T6c: the two token pairs disagree on the direction", False, ["[token numbers]", "disagree"], small_before=2000)
pcase("p_rules_in_other_result", "C7/T10: the result of an `ls` carries lines of K", False, ["[rules in another call's result]"], after=lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), t.tool("Bash", {"command": "ls client"}, "app.js\n" + "\n".join(KLINES[:60])), write_edit(t, c)))
pcase("p_unparsed_line", "C8/T11: a transcript line that does not parse", False, ["[unparsed lines]"], junk_lines=("not json at all",))
pcase("p_metadata_not_object", "C8/T12: the boundary's metadata is not an object: a stop with that reason, no traceback", False, ["[boundary metadata]", "not an object"], meta="oops")
pcase("p_metadata_absent", "C8/T12: the boundary has no metadata", False, ["[boundary metadata]", "absent"], meta="absent")
pcase("p_unplaced_print", "C2: cat F > /dev/null in turn 2: unplaced, a warning, no stop", True, ["cannot place"], after=lambda t, c: (t.tool("Bash", {"command": f"cat {RULES} > /dev/null"}, ""), write_edit(t, c)))
pcase("p_control_whole", "D3 outcome 2: the occasion produced, every gate passed, the control read whole: its own verdict, exit 3, no marker", "WHOLE", ["THE CONTROL READ WHOLE"], four=True, after=lambda t, c: (t.tool("Read", {"file_path": c.rules}, numbered(FULL)), write_edit(t, c)))
pcase("p_four_slice_ok", "D3 outcome 3: four-call design, the control read a slice: PILOT OK, the marker", True, ["design: 4 calls"], four=True)
pcase("p_reference", "D3 outcome 1: a reference to the rules file after the boundary: PILOT NOT OK [occasion]", False, ["[occasion]", "reference"], four=True, post=lambda t, c: t.file_reference(c.rules))
pcase("p_json_string_line", "P1: a transcript line that is a JSON string: a named stop, no traceback", False, ["[unparsed lines]"], junk_lines=('"a string"',))
pcase("p_x1_write_result", "X1: lines of K in a write call's result", False, ["[rules in another call's result]"], after=lambda t, c: (t.tool("Bash", {"command": f"head -40 {RULES}"}, first(40)), t.tool("Edit", {"file_path": c.app, "old_string": "a", "new_string": "b"}, "edited\n" + "\n".join(KLINES[:60]))))
for name, what, ok, has, kw in PILOTS: cmake(name, **kw)

# ---------------------------------------------------------------- run the readers
PILOT_NAMES = ["q901"] + [p[0] for p in PILOTS]
env = dict(os.environ, R214_TEST_ONLY="1", R214_ROOT=str(TR), R214P_ROOT=str(TR), R214_PILOTS=" ".join(PILOT_NAMES), R214_OUT=str(OUTD), R214_CFG=str(ST / "cfg"), BMA_BASE=FAKE_BASE, BMA_SCRATCH=str(ST.parent))
def run(script, *args, env=env):
    r = subprocess.run([sys.executable, str(HERE / script), *args], env=env, capture_output=True, text=True)
    if r.returncode != 0: print("FAIL:", script, "crashed:", r.stderr[-600:]); sys.exit(1)
    return r.stdout
names = [c[0] for c in CASES]
rd_out = run("read.py", *names, "q901", "q112", "q113", "q114", "q115", "q116", "q117")
rd = json.loads(rd_out)
ct_out = run("certificate.py", *[c[0] for c in CERT], "c_two")
ct = json.loads(ct_out)
ct_nobase = json.loads(run("certificate.py", "c_ok", env={k: v for k, v in env.items() if k != "BMA_BASE"}))

fails = []
def chk(name, field, got, want):
    ok = got == want
    print(("PASS " if ok else "FAIL ") + f"{name:30s} {field:24s} got={got!r} want={want!r}")
    if not ok: fails.append((name, field))

changed = []
for name, what, after, exp, kw in CASES:
    r = rd["arms"][name]
    print(f"-- {name}: {what}")
    if "changed" in kw: changed.append((name, kw["changed"])); print(f"CHANGED  {name}: {kw['changed']}")
    ii, i = r.get("ii") or {}, r.get("i") or {}
    if "i" in exp: chk(name, "(i) class", i.get("class"), exp["i"])
    if "iv" in exp: chk(name, "(iv) class", (r["iv"] or {}).get("class"), exp["iv"])
    if "ii" in exp: chk(name, "(ii) lines handed back", ii.get("n"), exp["ii"])
    if exp.get("ii_all"): chk(name, "(ii) every counted line", (ii.get("n"), ii.get("M")), (M, M))
    if exp.get("ii_part"): chk(name, "(ii) some, not all", 0 < ii.get("n", 0) < ii.get("M", 0), True)
    if "ii_n" in exp: chk(name, "(ii) n", ii.get("n"), exp["ii_n"])
    if exp.get("elig_by_half"): chk(name, "eligible iff n < M/2", r["eligible"], 2 * ii["n"] < ii["M"])
    if exp.get("short_hit"): chk(name, "short lines hit (a fact)", ii["short_lines_hit"][0] > 0, True)
    if "skipped" in exp: chk(name, "request-copy records skipped", ii["skipped_request_copy_records"], exp["skipped"])
    if "seq_classes" in exp: chk(name, "access classes", [x["class"] for x in i["sequence"]], exp["seq_classes"])
    if "flag_has" in exp: chk(name, "flag", any(exp["flag_has"] in f for f in r["flags"]), True)
    if "rest_n" in exp: chk(name, "rest-of-turn count", ii["rest_of_turn"]["n"], M if exp["rest_n"] == "M" else exp["rest_n"])
    if "no_flag" in exp: chk(name, "no such flag", any(exp["no_flag"] in f for f in r["flags"]), False)
    if "unreadable" in exp: chk(name, "request copies unreadable", ii["request_copies_unreadable"], exp["unreadable"])
    if "design" in exp: chk(name, "design", r["design"].startswith(exp["design"]), True)
    if "ivb" in exp: chk(name, "(iv-b) class", (r["ivb"] or {}).get("class"), exp["ivb"])
    if "occ_kinds" in exp: chk(name, "attachments naming the rules", [a["kind"] for a in r["occasion"]["attachments_naming_rules"]], exp["occ_kinds"])
    if "occ_files" in exp: chk(name, "distinct files touched before the boundary", r["occasion"]["distinct_files_touched_before_boundary"], exp["occ_files"])
    if "xn_cmp" in exp: chk(name, "(x, x + n)", (ii["x"], ii["x_plus_n"]), (exp["xn_cmp"][0], exp["xn_cmp"][2]))
    if "added" in exp: chk(name, "added line handed back", ii["added_line_handed_back"], exp["added"])
    if "unparsed" in exp: chk(name, "unparsed lines", r["transcript"]["unparsed_lines"], exp["unparsed"])
    if "other_call_rules" in exp: chk(name, "rules in other calls' results", len(i["rules_in_results_of_other_calls"]), exp["other_call_rules"])
    if "md_shape" in exp: chk(name, "metadata shape", ii["preserved"]["metadata_shape"], exp["md_shape"])
    if "dotdot" in exp: chk(name, "dotdot calls carried", r["dotdot_calls"], exp["dotdot"])
    if "disagree" in exp: chk(name, "token pairs disagree", r["iii"]["token_pairs_disagree"], exp["disagree"])
    if "shrank" in exp: chk(name, "context shrank (decided)", r["iii"]["context_shrank"], exp["shrank"])
    if "pres_missing" in exp: chk(name, "preserved ids not in file", ii["preserved"]["ids_not_in_file"], exp["pres_missing"])
    if "eligible" in exp: chk(name, "eligible", r["eligible"], exp["eligible"])
    if "reason_has" in exp: chk(name, "reason", any(exp["reason_has"] in x for x in r["eligible_reasons"]), True)
    if "reason_not" in exp: chk(name, "reason absent", any(exp["reason_not"] in x for x in r["eligible_reasons"]), False)
    if "boundaries" in exp: chk(name, "boundaries", r["transcript"]["boundaries"], exp["boundaries"])
    if "cut" in exp: chk(name, "cut boundary number", r["transcript"]["cut_boundary_number"], exp["cut"])
    if "late" in exp: chk(name, "accesses after the window", len(i.get("late_accesses", [])), exp["late"])
    if "other_files" in exp: chk(name, "other files listed", len(i["other_files"]), exp["other_files"])
    if "unresolved" in exp: chk(name, "unresolved mentions", len(i["unresolved_mentions"]), exp["unresolved"])
    if "du" in exp: chk(name, "delivered-unresolved calls", len(i.get("delivered_unresolved") or []), exp["du"])
    if exp.get("du_names_bem"): chk(name, "flag names BEMYAGENT.md", i["delivered_unresolved"][0]["names_BEMYAGENT_md"], True)
    if "non_reading" in exp: chk(name, "non-reading mentions", i["non_reading_mentions"], exp["non_reading"])
    if "write_kind" in exp: chk(name, "first write kind", (i["first_write"] or {}).get("kind"), exp["write_kind"])
    if "note" in exp: chk(name, "note", exp["note"] in (i.get("note") or ""), True)
    if "flag" in exp: chk(name, "flag", any(exp["flag"] in f for f in r["flags"]), True)
    if "kind_has" in exp: chk(name, "record kind carrying", exp["kind_has"] in [k["kind"] for k in ii["kinds"]], True)
    if "pres_rules" in exp: chk(name, "preserved holds rules", ii["preserved"]["any_rules_lines"], exp["pres_rules"])
    if "pres_types_has" in exp: chk(name, "preserved types", exp["pres_types_has"] in ii["preserved"]["types"], True)
    if "rules_records" in exp:
        rr = ii["rules_file_records"]; chk(name, "rules-file record", (rr[0]["target"], rr[0]["partial"]) if rr else None, exp["rules_records"])
chk("m1_form_not_recorded_as_class", "form beside class", [(x["form"], x["class"]) for x in rd["arms"]["d1_read_limit2000"]["i"]["sequence"]], [("offset-or-limit", "whole")])
chk("m1_form_shell", "form beside class", [(x["form"], x["class"]) for x in rd["arms"]["d1_awk_1"]["i"]["sequence"]], [("shell", "whole")])
# no text in the output
for needle in ("A summary of the work so far", "Thanks. Now add", "scoreboard", "idempotent", "Self-Registration", "Read this file whole"):
    chk("(output)", f"no text: {needle[:18]!r}", needle in rd_out, False)
sys.path.insert(0, str(HERE)); import access
chk("(rules file)", "no truncation sign in it", [n for n, rx in access.TRUNC_PATTERNS.items() if rx.search(RULES_C)], [])

# per-condition counts
pc = {x["cond"]: x for x in rd["per_condition_over_eligible_arms"]}
print("-- per-condition counts (q901 is the pilot; q116 is handed every line; q113 slices; q114 does not read; q117 got the stub)")
chk("(summary)", "order: control first", [x["cond"] for x in rd["per_condition_over_eligible_arms"]], ["C", "L"])
chk("(summary)", "C eligible/whole/slice/none", (pc["C"]["n_eligible"], pc["C"]["whole"], pc["C"]["slice"], pc["C"]["none"]), (3, 2, 1, 0))
chk("(summary)", "C: every arm with an attempted access listed (q114 was whole)", pc["C"]["attempted_access_in_window"], ["q114"])
chk("(summary)", "C arms (pilot excluded)", pc["C"]["arms"], ["q112", "q113", "q114"])
chk("(summary)", "L eligible/whole/slice/none", (pc["L"]["n_eligible"], pc["L"]["whole"], pc["L"]["slice"], pc["L"]["none"]), (1, 1, 0, 0))
chk("(summary)", "L left out", sorted(pc["L"]["left_out"]), ["q116", "q117"])
chk("(summary)", "L attempted listed", pc["L"]["attempted_access_in_window"], ["q117"])
chk("(summary)", "x + n beside each arm's class", pc["C"]["class_and_handed_back_per_arm"]["q112"], {"class": "whole", "handed_back": {"x": 0, "n": 0, "x_plus_n": 0, "of_K": 86, "rest_of_turn_n_of_K": 0, "added_line_handed_back": None}, "eligible": True})
chk("(summary)", "no verdict key", any("verdict" in k for k in rd), False)
chk("(summary)", "pilot role", rd["arms"]["q901"]["role"], "pilot")

# certificate
print("-- certificate")
for name, what, exp, kw in CERT:
    r = ct[name]; print(f"-- {name}: {what}")
    if "clean" in exp: chk(name, "clean", r["clean"], exp["clean"])
    if "term" in exp: chk(name, "failed term named", exp["term"] in [k for k, v in r["clean_terms"].items() if not v], True)
    if "design_ok" in exp: chk(name, "design_ok", r["design_ok"], exp["design_ok"])
    if "same" in exp: chk(name, "same session on all three", r["same_session_id_on_all_three"], exp["same"])
    if "own_memory" in exp: chk(name, "own-memory calls", r["tool_calls_own_memory"], exp["own_memory"])
    if "dotdot" in exp: chk(name, "dotdot calls", r["segments"]["before"]["tool_calls_dotdot"], exp["dotdot"])
    if "second_model" in exp: chk(name, "second model reported", r["second_model_in_usage"], ["claude-haiku-4"])
    if "calls" in exp: chk(name, "calls in the design", r["calls"], exp["calls"])
    if "unparsed" in exp: chk(name, "lines that are not objects counted", r["unparsed_lines"], exp["unparsed"])
fa = ct["c_repo"]["fail_at"].get("no_tool_call_naming_repo")
chk("c_repo", "fail_at places the failing call", bool(fa) and all(isinstance(i, int) and i >= 0 for i in fa), True)
chk("c_two", "one transcript in own folder", ct["c_two"]["one_transcript_in_own_folder"], False)
chk("c_ok", "base_check_made (BMA_BASE set)", ct["c_ok"]["base_check_made"], True)
chk("c_ok", "base check says so when unset", (ct_nobase["c_ok"]["base_check_made"], "NOT checked" in ct_nobase["c_ok"].get("base_check", "")), (False, True))
chk("c_ok", "cp prompt file is /compact", ct["c_ok"]["compact_prompt_file_is_exactly_/compact"], True)

# pilot cases: check_pilot.sh end to end
print("-- check_pilot.sh on synthetic pilots")
for name, what, ok, has, kw in PILOTS:
    open(OUTD / "pilot_ok.stale", "w").write("PILOT OK stale\n")             # G1: every marker goes at the start of a check
    r = subprocess.run(["/bin/bash", str(HERE / "check_pilot.sh"), name], env=env, capture_output=True, text=True)
    out = r.stdout
    print(f"-- {name}: {what}")
    want_ok = ok is True
    chk(name, "verdict is PILOT OK", "== verdict: PILOT OK" in out, want_ok)
    if ok == "WHOLE": chk(name, "the control read whole: exit 3, no marker", (r.returncode, "THE CONTROL READ WHOLE" in out, (OUTD / f"pilot_ok.{name}").exists()), (3, True, False))
    chk(name, "marker iff PILOT OK (content `PILOT OK <name>`)", ((OUTD / f"pilot_ok.{name}").read_text().strip() if (OUTD / f"pilot_ok.{name}").exists() else None), (f"PILOT OK {name}" if want_ok else None))
    chk(name, "G1: the stale marker is gone", (OUTD / "pilot_ok.stale").exists(), False)
    chk(name, "no traceback", "Traceback" in out + r.stderr, False)
    for h in has: chk(name, f"prints {h[:40]!r}", h in out, True)
    if r.stderr.strip(): print("   stderr:", r.stderr.strip()[-300:])
real = [n for n, m in changed if "->" in m and "stays" not in m]
rr = subprocess.run(["/bin/bash", str(HERE / "check_pilot.sh"), "q112"], env=env, capture_output=True, text=True)
chk("check_pilot q112", "a counted arm is refused (exit 2, says so)", (rr.returncode, "refuses" in rr.stdout and "not a pilot" in rr.stdout), (2, True))
# D5: G2 marker content, G3 override
import tempfile
sys.path.insert(0, str(HERE)); import kset
td = pathlib.Path(tempfile.mkdtemp(dir=str(ST)))
(td / "pilot_ok.x").write_text(""); chk("G2", "an empty marker named pilot_ok.x opens nothing", kset.marker_ok(td, ["q901", "q902", "q903"]), False)
(td / "pilot_ok.q901").write_text("PILOT OK q902\n"); chk("G2", "a marker whose content names another pilot opens nothing", kset.marker_ok(td, ["q901", "q902", "q903"]), False)
(td / "pilot_ok.q901").write_text("PILOT OK q901\n"); chk("G2", "the marker the check writes opens", kset.marker_ok(td, ["q901", "q902", "q903"]), True)
(td / "pilot_ok.q901").write_text("PILOT OK q901\n"); chk("G2", "a marker for a name that is not a pilot opens nothing", kset.marker_ok(td, ["q902"]), False)
def refused(e):
    try: kset.pilots_from_env(e); return False
    except SystemExit: return True
chk("G3", "an override naming a counted arm is refused", refused({"R214_PILOTS": "q901 q902 q903 q112"}), True)
chk("G3", "an override leaving out a pilot is refused", refused({"R214_PILOTS": "q901 q902"}), True)
chk("G3", "the same with R214_TEST_ONLY is allowed", refused({"R214_PILOTS": "q901 q902 q903 q112", "R214_TEST_ONLY": "1"}), False)
chk("G3", "no override: the default names", kset.pilots_from_env({}), ["q901", "q902", "q903"])
# C8: one arm the reader cannot read does not end the read of the others
os.environ.update(env); sys.argv = ["read.py"]
import read as readmod
readmod.read_arm = lambda a: 1 / 0
sr = readmod.safe_read("whatever")
chk("(reader)", "a failing arm is named, no traceback", (sr["eligible"], sr.get("reader_error"), "reader failed" in sr["eligible_reasons"][0]), (False, "ZeroDivisionError", True))
print(f"\nCases whose expected CLASS changed under Amendment 1 ({len(real)}): " + ", ".join(real))
print("Cases with the same class and a new flag or cut: " + ", ".join(n for n, m in changed if n not in real))
print(f"\n{len(fails)} mismatches")
sys.exit(1 if fails else 0)
PY
