#!/bin/bash
# 21.4 — the one command to run after `./launch.sh q901`, BEFORE launching the six arms.
# Runs certificate.py and read.py on the pilot, then prints numbers and a verdict line - no transcript text.
# Per the Pivot line of 02_tasks.md and Amendment 1 (A5, A6): compaction not proven, or the session not kept -> PILOT NOT OK;
# (iv) not `whole` (the pilot's turn 1 is the reader's only real-format positive control) -> NOT OK; an access that delivered no
# line (`attempted`) -> NOT OK; a turn 2 with no tool call -> NOT OK (its own check); any line of the rules handed back after the boundary, or kept across it, -> NOT OK (the designer's
# ruling is needed; all lines -> the proxy cannot produce the occasion). Every stop prints WHICH check failed, and for the
# certificate which term of `clean`. A second model in a call's usage is printed, not a stop. Exit code 1 on NOT OK.
# Usage: ./check_pilot.sh [arm]      (default q901; R214_ROOT / R214_OUT / R214_CFG as for the other scripts)
set -u
export PYTHONDONTWRITEBYTECODE=1      # no __pycache__ in the task folder
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE" || exit 1
[ -f "$HERE/local.env" ] && . "$HERE/local.env"      # machine-local BMA_SCRATCH / CLAUDE_CONFIG_DIR / BMA_BASE (gitignored)
arm="${1:-q901}"
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
OUT="${R214_OUT:-$S/r214_out}"
case " ${R214_PILOTS:-q901 q902 q903} " in *" $arm "*) ;; *) echo "check_pilot.sh refuses '$arm': it is not a pilot (${R214_PILOTS:-q901 q902 q903}). A counted arm is not checked with the pilot's verdict (Amendment 3, C4)."; exit 2;; esac
echo "== launch.status for $arm"
if grep -q "^$arm " "$OUT/launch.status" 2>/dev/null; then grep "^$arm " "$OUT/launch.status" | sed 's/ t1_sha=.*//'; else echo "(none)"; fi
python3 certificate.py "$arm" > "$OUT/$arm.cert.json"      # {arm: row}; read.py looks for this file
python3 read.py "$arm" > "$OUT/$arm.read.json"
rm -f "$OUT/pilot_ok.$arm"                                  # a marker stands only for the latest verdict
python3 - "$arm" "$OUT" <<'PY'
import json, sys
arm, R = sys.argv[1:3]
c = json.load(open(f"{R}/{arm}.cert.json"))[arm]; rd = json.load(open(f"{R}/{arm}.read.json"))["arms"][arm]
bad, warn = [], []
st = rd["status"]; tk = st["tokens"]
for k in ("t1", "cp", "t2"):
    if st["exit_codes"].get(k) != 0: bad.append(f"[exit codes] {k} exit code is {st['exit_codes'].get(k)}")
iii = rd.get("iii") or {}
if rd.get("reader_error"):
    bad.append(f"[reader] it failed on this arm ({rd['reader_error']}): the transcript has a shape it does not know")
    print("== verdict: PILOT NOT OK - do not launch the six"); print("  -", bad[-1]); sys.exit(1)
if (rd.get("transcript") or {}).get("unparsed_lines"): bad.append(f"[unparsed lines] {rd['transcript']['unparsed_lines']} transcript line(s) do not parse: what they hold was not read")
if iii.get("token_pairs_disagree"): bad.append(f"[token numbers] the assistant records say {iii.get('prompt_tokens_last_before_boundary')} -> {iii.get('prompt_tokens_first_after_boundary')}, the boundary says {iii['transcript'].get('pre_tokens')} -> {iii['transcript'].get('post_tokens')}: they disagree on the direction")
if iii.get("context_shrank") is not True:
    bad.append(f"[context shrink] the context did not shrink at the boundary, or the two token numbers cannot be read (before {iii.get('prompt_tokens_last_before_boundary')}, after {iii.get('prompt_tokens_first_after_boundary')}): that is not shown to be a compaction")
if tk.get("compaction_proven") != "1": bad.append("[compaction] the launcher did not prove it (Pivot: /compact does not compact under -p --resume)")
tr = (iii.get("transcript") or {})
if not tr.get("boundaries"): bad.append("[compaction] no compaction boundary in the transcript")
sess_ok = bool(c.get("same_session_id_on_all_three")) and bool(c.get("one_transcript_in_own_folder")) and tk.get("session_same") != "0"
if not sess_ok: bad.append("[session] not kept across the three calls (Pivot: --resume does not carry the session)")
ii, iv, i = rd.get("ii") or {}, rd.get("iv") or {}, rd.get("i") or {}
if ii.get("n") is None: bad.append(f"[(ii) handed back] could not be computed: {ii.get('reason')}")
else:
    pres = ii["preserved"]
    if ii["x"]: bad.append(f"[instruction file] it holds {ii['x']} line(s) of K at the turn-1 snapshot (0 as seeded): the tree is not the designed one")
    if ii["K_lines_in_snapshot_rules"] != 86: bad.append(f"[snapshot rules file] the turn-1 snapshot gives {ii['K_lines_in_snapshot_rules']} of the 86 lines of K")
    if ii["x_plus_n"] >= ii["threshold"]: bad.append(f"[(ii) handed back] x + n = {ii['x']} + {ii['n']} = {ii['x_plus_n']} of K={ii['K']}: the rules come back without the arm acting (Pivot: this proxy cannot produce the occasion)")
    elif ii["n"] > 0: bad.append(f"[(ii) handed back] n = {ii['n']} of K={ii['K']} lines handed back after the boundary or kept across it: the designer's ruling is needed before the six")
    if ii["rest_of_turn"]["n"] > 0: bad.append(f"[(ii) rest of turn 2] {ii['rest_of_turn']['n']} of K={ii['K']} lines of the rules handed back after the window's end (carried by {[k['kind'] for k in ii['rest_of_turn']['kinds']]}): the designer's ruling is needed")
    if pres["any_rules_lines"]: bad.append(f"[preserved across the boundary] records the compaction kept hold lines of the rules (non-result records {pres['lines_in_non_result_records']}, results {pres['lines_in_results']}): the designer's ruling is needed")
    if any(pres["fields_present"].values()) and (pres["ids_not_in_file"] or pres["unexpected_shape"]):
        bad.append(f"[preserved fields] a preserved field is present and non-empty but {pres['ids_not_in_file']} of the {pres['ids_named']} record id(s) it names are not in the file, or its shape is unexpected {pres['unexpected_shape']}: the reader cannot look at what was kept")
    if pres["metadata_shape"] != "ok": bad.append(f"[boundary metadata] the boundary's metadata is {pres['metadata_shape']}: what was kept and the token numbers cannot be read from it")
    if pres["unknown_metadata_keys"]:
        bad.append(f"[boundary metadata] keys the reader does not know: {pres['unknown_metadata_keys']} (names only): a kept record could pass unseen")
    if ii["request_copies_unreadable"]: bad.append(f"[request copies] {ii['request_copies_unreadable']} request copy(ies) between the boundary and the first tool result cannot be read as text, even with their hashes resolved: (ii) was not tested there")
    if i.get("rules_in_results_of_other_calls"): bad.append(f"[rules in another call's result] lines of K in the result of {[(x['tool'], x['form'], x['K_lines']) for x in i['rules_in_results_of_other_calls']]} inside the window, calls that did not name the rules file (tool, form, K lines)")
if iv.get("class") is None: bad.append(f"[(iv) turn-1 restore] could not be computed: {iv.get('reason')}")
elif iv["class"] != "whole": bad.append(f"[(iv) turn-1 restore] is `{iv['class']}`, not `whole`: the reader cannot read the real format, or turn 1 did not read the rules whole")
for name, seg in (("(iv)", iv), ("(i)", i)):
    n = sum(1 for x in seg.get("sequence", []) if x["class"] == "attempted")
    if n: bad.append(f"[attempted access {name}] {n} access(es) to the rules file delivered no line (the tool withheld the text)")
    if seg.get("delivered_unresolved"): warn.append(f"{name}: delivered-unresolved - {[(x['tool'], x['form'], x['names_BEMYAGENT_md']) for x in seg['delivered_unresolved']]} returned every line and was not resolved to the rules file: hand-read (02_tasks.md A3)")
if not c.get("design_ok"): bad.append("[certificate design_ok] false (prompts / session / boundary not as designed): same_session=%s boundary_sid=%s first_user=%s context_carried=%s hashes=%s" % (c.get("same_session_id_on_all_three"), c.get("boundary_session_id_equals_t1"), c.get("first_user_equals_prompt_t1"), c.get("context_carried"), c.get("launcher_prompt_hashes_equal_files")))
if not c.get("clean"):
    failed = [k for k, v in (c.get("clean_terms") or {}).items() if not v]
    bad.append("[certificate clean] failed term(s): " + (", ".join(failed) or "unknown") + f"   (record indexes where they fail: {c.get('fail_at')}; override headers {c.get('override_header_count')})")
if not c.get("base_check_made"): bad.append("[certificate base check] BMA_BASE is not set: the folder sessions start in was not checked")
for k in ("t1", "t2"):
    v = (rd["vi"] or {}).get(k)
    if not v: bad.append(f"[{k}.json] missing or unreadable")
    elif v.get("is_error") or v.get("permission_denials"): bad.append(f"[{k}.json] is_error={v.get('is_error')} permission_denials={v.get('permission_denials')}")
if rd.get("turn2_no_tool_call"): bad.append("[turn 2 no tool call] the resumed session ran and did nothing after the boundary: the designer looks")
for r in rd.get("eligible_reasons") or []: bad.append(f"[reader: eligibility] {r}")
print("== session")
print(f"same session id on the three calls: {c.get('same_session_id_on_all_three')}   one transcript in the arm's own folder: {c.get('one_transcript_in_own_folder')}   launcher session_same={tk.get('session_same')}")
print("== compaction")
print(f"launcher: proven={tk.get('compaction_proven')} by={tk.get('by')} pre_tokens={tk.get('pre_tokens')}   transcript: boundaries={tr.get('boundaries')} cut number={(rd.get('transcript') or {}).get('cut_boundary_number')} trigger={tr.get('cut_trigger')} pre={tr.get('pre_tokens')} post={tr.get('post_tokens')}   agree={iii.get('launcher_and_transcript_agree')}")
b, a = iii.get("prompt_tokens_last_before_boundary"), iii.get("prompt_tokens_first_after_boundary")
print(f"model prompt tokens, last record before the boundary / first after it: {b} / {a}" + ("" if b is None or a is None else f"   (shrank: {a < b})"))
print("== the occasion: lines of the rules handed back after the boundary or kept across it (reading ii)")
if ii.get("n") is not None:
    print(f"n = {ii['n']} of K={ii['K']} lines handed back, x = {ii['x']} held by the instruction file, x + n = {ii['x_plus_n']} (leaves at {ii['threshold']}); added line handed back: {ii['added_line_handed_back']} (deciding nothing); short lines hit (fact, decides nothing): {ii['short_lines_hit'][0]} of {ii['short_lines_hit'][1]}; request copies left out: {ii['skipped_request_copy_records']}, unreadable: {ii['request_copies_unreadable']}; rest of turn 2 after the window: {ii['rest_of_turn']['n']} of {ii['K']}; carried by: " + (", ".join(f"{k['kind']} x{k['records']} at {','.join(k['key_paths'])}" + (f" file={','.join(k['file_targets'])}" if k['file_targets'] else "") + f" ({k['lines']})" for k in ii["kinds"]) or "no record"))
    rr = [(r['kind'], r['target'], r['partial'], r['lines']) for r in ii["rules_file_records"]]
    print("records about the rules file itself (kind, target, partial, lines): " + (str(rr) if rr else "none"))
    p = ii["preserved"]
    print(f"preserved across the boundary: fields present {p['fields_present']}, ids named {p['ids_named']} (not in the file: {p['ids_not_in_file']}), shape problems {p['unexpected_shape']}, records found {p['records_found']} {p['types']}, lines of the rules in them: non-result {p['lines_in_non_result_records']}, results {p['lines_in_results']}; unknown metadata keys: {p['unknown_metadata_keys']}")
print("== classes (by what the access delivered; the form decides nothing)")
print(f"(iv) turn-1 restore: {iv.get('class', iv.get('reason'))}   (i) after the boundary: {i.get('class', i.get('reason'))} {('- ' + i['note']) if i.get('note') else ''}  first write after: {i.get('first_write')}")
print("accesses to the rules file in the window (tool, form, class, lines delivered of N): " + str([(x['tool'], x['form'], x['class'], f"{x['lines_delivered']}/{x['lines_total']}") for x in i.get("sequence", [])]))
if i.get("unplaced_forms") or iv.get("unplaced_forms"): warn.append(f"a form the reader cannot place delivered no line: (iv) {iv.get('unplaced_forms')} (i) {i.get('unplaced_forms')}: hand-read (02_tasks.md B1)")
print(f"other files read instead: {i.get('other_files')}   unresolved mentions: {len(i.get('unresolved_mentions', []))}   flags: {rd.get('flags')}")
print("== cost (weights of harness/tokens.py)")
w = {k: (v or {}).get("weighted") for k, v in (rd["vi"] or {}).items()}
tot = rd.get("vi_total_weighted")
print(f"weighted tokens t1/cp/t2: {w}   arm total: {tot}   six arms at that rate: {6 * tot if tot else None}   (a C arm's rate: the L arms read the line and may spend more)")
print(f"tool memory after turn 1: existed={tk.get('memory_existed')} files={tk.get('files')}   tool calls naming the arm's own memory: {c.get('tool_calls_own_memory')}")
print(f"certificate: clean={c.get('clean')} design_ok={c.get('design_ok')} terms failed={[k for k, v in (c.get('clean_terms') or {}).items() if not v]} second model in usage (printed, not a stop)={c.get('second_model_in_usage')} "
      f"compact command recorded after boundary (info)={c.get('compact_command_recorded_after_boundary')}")
seg = c.get("segments") or {}
for k in ("before", "after"):
    s = seg.get(k)
    if s: print(f"  {k} boundary: " + str({x: s[x] for x in ("outside_arm_dir", "parent_repo_tool_calls", "base_tool_calls", "tool_calls_naming_apparatus", "tool_calls_dotdot", "attachments_naming_foreign_paths", "foreign_attachment_types", "events_cwd_outside_arm")}))
if not c.get("base_check_made"): print("  " + str(c.get("base_check")))
for x in warn: print("  WARNING:", x)
print("== verdict:", "PILOT OK - launch the six" if not bad else "PILOT NOT OK - do not launch the six")
for x in bad: print("  -", x)
if not bad:
    open(f"{R}/pilot_ok.{arm}", "w").write(f"PILOT OK {arm}\n")
    print(f"  marker written: pilot_ok.{arm} (necessary, not sufficient: the eye list and the designer's dated go-ahead in 03_execute.log come before the six)")
sys.exit(1 if bad else 0)
PY
