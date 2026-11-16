#!/bin/bash
# 21.1 — the one command to run after `./launch.sh q900`, BEFORE launching the nine arms.
# Reads only launch.status, the certificate and the scorer; prints numbers and a verdict, no text.
# Usage: ./check_pilot.sh [arm]      (default q900; R211_ROOT / R211_OUT / R211_CFG as for the other scripts)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE" || exit 1
[ -f "$HERE/local.env" ] && . "$HERE/local.env"      # machine-local BMA_SCRATCH / CLAUDE_CONFIG_DIR (gitignored)
arm="${1:-q900}"
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
OUT="${R211_OUT:-$S/r211_out}"
echo "== launch.status for $arm"; grep "^$arm " "$OUT/launch.status" 2>/dev/null || echo "(none)"
python3 certificate.py "$arm" > "$OUT/$arm.cert.json"; python3 score.py "$arm" > "$OUT/$arm.score.json"
python3 - "$arm" "$OUT" <<'PY'
import json, sys
arm, R = sys.argv[1:3]
c = json.load(open(f"{R}/{arm}.cert.json"))[arm]; s = json.load(open(f"{R}/{arm}.score.json"))[arm]
bad = []
st = s.get("status", {})
for k in ("t1", "t2", "s2"):
    if st.get("exit_codes", {}).get(k) != 0: bad.append(f"{k} exit code is {st.get('exit_codes', {}).get(k)}")
if st.get("resume_ok") != 1: bad.append("resume_ok is not 1: --resume did not carry the context")
if not c.get("design_ok"): bad.append("certificate design_ok false (prompts / resume / reset not as designed)")
if not c.get("all_calls_clean"): bad.append("certificate: a call is not clean (instruction outside the arm, parent path, OVERRIDE header beyond the arm's own CLAUDE.md, a tool call naming the apparatus, a foreign attachment)")
t2c = c.get("t2", {})
if t2c.get("model_context_not_smaller") is not True:
    bad.append(f"turn 2: the model's own prompt tokens do not show the context carried (before={t2c.get('prompt_tokens_before_t2')} after={t2c.get('prompt_tokens_after_t2')})")
if s.get("incomplete"): bad.append(f"snapshots missing: {s['incomplete']}")
for k, v in (s.get("vii") or {}).items():
    if v and (v.get("is_error") or v.get("permission_denials")): bad.append(f"{k}: is_error={v.get('is_error')} permission_denials={v.get('permission_denials')}")
w = {k: (v or {}).get("weighted") for k, v in (s.get("vii") or {}).items()}
print("== facts")
dd = sum((c.get(k) or {}).get("tool_calls_dotdot", 0) for k in ("t1", "t2", "s2"))
print(f"tool calls containing ../ (NOT gating - hand-read them): {dd}")
print(f"turn-2 prompt tokens before/after the turn-2 message: {t2c.get('prompt_tokens_before_t2')} / {t2c.get('prompt_tokens_after_t2')}")
print(f"t2 session id same as t1: {c.get('t2_same_session_id_as_t1')}   s2 id differs from both: {c.get('s2_session_differs_from_t1_and_t2')}")
print(f"memory folder existed before session 2: {st.get('memory_existed')} (files {st.get('memory_files')})")
print(f"weighted tokens t1/t2/s2: {w}   total: {s.get('vii_total_weighted')}   nine arms at that rate: {9 * (s.get('vii_total_weighted') or 0)}")
print(f"readings (i)-(viii) on the pilot, for the record: i={s.get('i')} iii={s.get('iii')} v={s.get('v')} viii={s.get('viii')}")
print("== verdict:", "PILOT OK - launch the nine" if not bad else "PILOT NOT OK - do not launch the nine")
for b in bad: print("  -", b)
sys.exit(1 if bad else 0)
PY
