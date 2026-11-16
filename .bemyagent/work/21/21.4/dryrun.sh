#!/bin/bash
# 21.4 launcher dry-run WITHOUT the real CLI. A stub named `claude` is first on a PATH that does not contain the
# real one (the PATH is stub : /usr/local/bin : /usr/bin : /bin, and every directory of it is checked for a `claude`). The
# script FAILS LOUDLY, before any launch, if `command -v claude` is not the stub. R214_ROOT (trees), R214_OUT
# (outputs) and R214_CFG (config) point into a throwaway root under <scratchpad>/p214/dry; nothing is written to the
# real r214 folders or to the real config folder. setup.py runs first (it needs npm and never calls claude).
# The stub plays all three calls on the arm's real tree, writes transcripts in the learned shape (synth.py) and, per
# arm, one of these behaviours (env STUB_*_ARMS):
#   q901 C pilot, q115 L . normal: boundary in stream and transcript; C slices the rules in turn 2, L reads them whole
#   q902 .................. /compact produces NO boundary (the launcher must skip turn 2)
#   q903 .................. the summary hands back every line of the rules (reading ii; PILOT NOT OK)
#   q904 .................. the stream reports another session id at the compaction (turn 2 skipped)
#   q116 .................. boundary in the stream only;   q117 .... boundary in the transcript only
# Amendment 3 (C4): pilots and the six stand in two roots; the pilots are q901-q904 here (R214_PILOTS), the six q115 q112 q116 q117; a counted
# arm is refused before a PILOT OK and setup.py six refuses without the marker; check_pilot.sh refuses a counted arm.
# Amendment 1 adds: setup.status (section 1), a duplicate-name launch and a concurrent second launch (section 13), and a hung call
# killed by the launcher's time limit with the stub still the binary and stdin still /dev/null (section 14).
# The output is masked (mask.sh); save it as 03d_dryrun.txt.
set -u
set -o pipefail
export PYTHONDONTWRITEBYTECODE=1      # no __pycache__ in the task folder
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$HERE/local.env" ] && . "$HERE/local.env"      # machine-local BMA_SCRATCH / CLAUDE_CONFIG_DIR / BMA_BASE (gitignored)
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
body() {
ROOT="${BMA_REPO:-$(cd "$HERE/../../../.." && pwd)}"
REAL_CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"        # the real tool-config folder, captured before any override
REAL_BEFORE=$(ls "$REAL_CFG/projects" 2>/dev/null | wc -l | tr -d ' ')
D="$S/p214/dry"
rm -rf "$D"; mkdir -p "$D/stub" "$D/trees" "$D/out" "$D/cfg/projects"
REAL_PATH="$PATH"                                      # the PATH of the shell, kept for setup.py (npm); launch.sh only ever sees the stub PATH
export R214_ROOT="$D/trees" R214P_ROOT="$D/ptrees" R214_PILOTS="q901 q902 q903 q904 q905 q906" R214_OUT="$D/out" R214_CFG="$D/cfg" STUB_LOG="$D/stub.log" STUB_HERE="$HERE"
export STUB_SLICE_ARMS="q901 q903 q906 q112" STUB_REFERENCE_ARMS="q906" STUB_NOCOMPACT_ARMS="q902" STUB_HAND8_ARMS="q903" STUB_NEWSID_ARMS="q904" STUB_STREAMONLY_ARMS="q116" STUB_TRANSCRIPTONLY_ARMS="q117" STUB_MEM_ARMS="q115"
mkdir -p "$D/trees" "$D/ptrees"
: > "$STUB_LOG"

echo "== 0. the prompts"
cmp "$HERE/prompt_t1.txt" "$HERE/../21.1/prompt_t1.txt" && echo "prompt_t1.txt = 21.1/prompt_t1.txt (cmp silent)"
echo "prompt_compact.txt: $(wc -c < "$HERE/prompt_compact.txt" | tr -d ' ') bytes, equals '/compact': $([ "$(cat "$HERE/prompt_compact.txt")" = "/compact" ] && echo yes || echo NO)"
echo "prompt_t2.txt is the turn-2 sentence of 02_tasks.md verbatim: $(grep -cF "$(cat "$HERE/prompt_t2.txt")" "$HERE/02_tasks.md") occurrence(s) there"

echo; echo "== 1. setup.py pilots: q901 (C) into the PILOTS root (real PATH: npm is needed; claude is never called). setup.py six refuses until a PILOT OK"
python3 "$HERE/setup.py" pilots q901 2>&1 | tail -2
echo "-- setup.py six q115 before any marker:"; python3 "$HERE/setup.py" six q115 2>&1 | tail -1 | sed -E "s|$D/||g"
echo "-- the pilot arms setup.py builds (B9), all C, none counted: $(grep -o '"q90[0-9]": "C"' "$HERE/setup.py" | tr '\n' ' ')"
echo "-- build twice refuses:"; python3 "$HERE/setup.py" pilots q901 2>&1 | tail -1
echo "-- setup.py with no mode:"; python3 "$HERE/setup.py" 2>&1 | tail -1
echo "-- the assertions (B10 included): six fake repos, each with a candidate branch that breaks one assertion; setup.py six must stop and build nothing"
mkdir -p "$D/fakemarker"; printf "PILOT OK q901\\n" > "$D/fakemarker/pilot_ok.q901"      # so the refusal under test is the assertion, not the missing marker
python3 - "$ROOT" "$D" "$HERE" <<'PY'
import os, pathlib, shutil, subprocess, sys
root, d, here = (pathlib.Path(x) for x in sys.argv[1:4])
RULES = ".bemyagent/docs/00-ai-rules.md"
LINE = "**Read this file whole — first line to last, every time, a context compaction included. A slice of it, or what you recall of it, is not a read.**"
def git(repo, *a): subprocess.run(["git", "-C", str(repo), "-c", "user.email=h@x", "-c", "user.name=h", *a], check=True, capture_output=True)
def ins(text, line, at=1):
    ls = text.splitlines(); ls.insert(at, line); return "\n".join(ls) + "\n"
rules0, bem0 = (root / RULES).read_text(), (root / "BEMYAGENT.md").read_text()
def variant(name, rules, bem):
    fake = d / f"fake_{name}"; (fake / ".bemyagent/docs").mkdir(parents=True); (fake / "harness").mkdir()
    (fake / "harness/fixture").symlink_to(root / "harness/fixture")
    (fake / RULES).write_text(rules0); (fake / "BEMYAGENT.md").write_text(bem0)
    git(fake, "init", "-q", "-b", "main"); git(fake, "add", "-A"); git(fake, "commit", "-qm", "c")
    git(fake, "checkout", "-q", "-b", "bma/21.4")
    (fake / RULES).write_text(rules); (fake / "BEMYAGENT.md").write_text(bem); git(fake, "commit", "-qam", "l")
    shutil.rmtree(fake / ".bemyagent/docs", ignore_errors=True)       # the working tree keeps C: restore it from main
    git(fake, "checkout", "-q", "main"); out = d / f"fake_out_{name}"
    env = dict(os.environ, BMA_REPO=str(fake), R214_ROOT=str(out), R214_OUT=str(d / "fakemarker"))
    r = subprocess.run([sys.executable, str(here / "setup.py"), "six", "q115"], env=env, capture_output=True, text=True)
    err = (r.stderr.strip().splitlines() or ["(no error text)"])[-1]
    built = (out / "q115").exists()
    print(f"  {name:12s} exit={r.returncode} built={built}  {err[:110]}")
variant("two_lines", ins(rules0, LINE).replace("## 8.", "an extra line\n## 8.", 1), ins(bem0, LINE, 29))
variant("replaced", ins(rules0, LINE).replace("# AI Rules & TTEV Workflow", "# AI Rules"), ins(bem0, LINE, 29))
variant("lines_differ", ins(rules0, LINE), ins(bem0, LINE + " x", 29))
variant("wrong_start", ins(rules0, LINE.replace("**Read", "Read")), ins(bem0, LINE.replace("**Read", "Read"), 29))
variant("one_file_only", ins(rules0, LINE), bem0)
variant("line_altered", ins(rules0, LINE.replace("every time", "each time")), ins(bem0, LINE.replace("every time", "each time"), 29))     # B10: starts right, one line, line 2, same in both - only the sha1 differs
PY
echo "-- the pilots' trees stand in one root, the six's in another: pilots root holds: $(ls "$D/ptrees" | tr '\n' ' ')  six root holds: $(ls "$D/trees" | tr '\n' ' ')(nothing yet)"

echo; echo "== 2. the other pilot trees: copies of q901 (q902 .. q906) in the pilots root"
copy() { mkdir -p "$3/$1"; (cd "$4/$2" && tar -cf - --exclude=node_modules .) | (cd "$3/$1" && tar -xf -); }
for a in q902 q903 q904 q905 q906; do copy $a q901 "$D/ptrees" "$D/ptrees"; done
ls "$D/ptrees" | tr '\n' ' '; echo

echo; echo "== 3. which claude will launch.sh see? PATH = stub : /usr/local/bin : /usr/bin : /bin"
printf '#!/bin/bash\nexec python3 "%s/stub/stub.py" "$@"\n' "$D" > "$D/stub/claude"; chmod +x "$D/stub/claude"
export PATH="$D/stub:/usr/local/bin:/usr/bin:/bin"
got="$(command -v claude)"; type -a claude
if [ "$got" != "$D/stub/claude" ]; then echo "FATAL: command -v claude is '$got', not the stub - refusing to launch"; exit 3; fi
if [ "$(type -a claude | wc -l | tr -d ' ')" != 1 ]; then echo "FATAL: more than one claude on the PATH - refusing to launch"; exit 3; fi
for dir in $(echo "$PATH" | tr ':' ' '); do if [ "$dir" != "$D/stub" ] && [ -x "$dir/claude" ]; then echo "FATAL: a claude sits in $dir - refusing to launch"; exit 3; fi; done
echo "command -v claude is the stub: yes   other claude in any directory of the PATH: none"

cat > "$D/stub/stub.py" <<'PY'
import json, os, pathlib, re, sys, uuid
sys.path.insert(0, os.environ["STUB_HERE"])
import synth
args = sys.argv[1:]
def L(s):
    with open(os.environ["STUB_LOG"], "a") as f: f.write(s + "\n")
prompt = resume = model = fmt = None; tools = []; bad = []; verbose = False
i = 0
while i < len(args):
    a = args[i]
    if a == "-p": prompt = args[i + 1]; i += 2
    elif a == "--resume": resume = args[i + 1]; i += 2
    elif a == "--model": model = args[i + 1]; i += 2
    elif a == "--output-format": fmt = args[i + 1]; i += 2
    elif a == "--verbose": verbose = True; i += 1
    elif a == "--allowedTools":
        i += 1
        while i < len(args) and not args[i].startswith("--"): tools.append(args[i]); i += 1
    else: bad.append(a); i += 1
cwd = os.getcwd(); arm = os.path.basename(cwd); cfg = os.environ.get("CLAUDE_CONFIG_DIR", "")
env = lambda k: os.environ.get(k, "").split()
phase = "cp" if prompt == "/compact" else "t2" if prompt and "Reset scores" in prompt else "t1b" if prompt and "type a name" in prompt else "t1"
stdin_null = os.path.samestat(os.fstat(0), os.stat("/dev/null"))
shape_ok = {"t1": fmt == "json" and not resume and not verbose, "t1b": fmt == "json" and bool(resume) and not verbose, "cp": fmt == "stream-json" and bool(resume) and verbose,
            "t2": fmt == "json" and bool(resume) and not verbose}[phase]
flags_ok = bool(prompt) and model == "sonnet" and not bad and tools == ["Read", "Write", "Edit", "Bash", "Glob", "Grep"] and stdin_null and shape_ok
L(f"STUB-CALL arm={arm} phase={phase} mode={'resume' if resume else 'new'} flags_ok={flags_ok} model={model} fmt={fmt} stdin_is_dev_null={stdin_null} bad={bad} cfg_is_pinned={cfg == os.environ['R214_CFG']}")
if not flags_ok: sys.exit(2)
import time
if phase == "t1" and arm in env("STUB_SLOW_ARMS"): time.sleep(2)
if phase == "t1" and arm in env("STUB_HANG_ARMS"): time.sleep(300)           # a hung call: only the launcher's time limit ends it
sid = resume or str(uuid.uuid4())
proj = pathlib.Path(cfg) / "projects" / re.sub(r"[^A-Za-z0-9]", "-", cwd); proj.mkdir(parents=True, exist_ok=True)
tfile = proj / f"{sid}.jsonl"
RULES = synth.RULES
rules_text = pathlib.Path(RULES).read_text()
heads = [l for l in rules_text.splitlines() if l.startswith("## ")]
t = synth.T(cwd, sid, tokens=60000 if phase != "t2" else 20000)
t.n = sum(1 for _ in open(tfile)) if tfile.exists() else 0
def edit(): t.tool("Edit", {"file_path": cwd + "/client/app.js", "old_string": "a", "new_string": "b"}, "edited")
usage = {"input_tokens": 10, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": 10000, "output_tokens": 500}
mu = {"claude-sonnet-5-5": {"inputTokens": 10, "cacheCreationInputTokens": 1000, "cacheReadInputTokens": 10000, "outputTokens": 500}}
out_sid = sid
stream_boundary = transcript_boundary = False
if phase == "t1":
    t.instructions(); t.user(prompt)
    t.tool("Read", {"file_path": cwd + "/" + RULES}, synth.numbered(rules_text))
    app = pathlib.Path("client/app.js"); app.write_text(app.read_text() + "\n// scoreboard\n")
    edit(); t.assistant_text("Scoreboard added.")
    if arm in env("STUB_MEM_ARMS"):
        (proj / "memory").mkdir(exist_ok=True); (proj / "memory" / "MEMORY.md").write_text("- index\n"); (proj / "memory" / "topic.md").write_text("x\n")
elif phase == "t1b":
    t.user(prompt)
    app = pathlib.Path("client/app.js"); app.write_text(app.read_text() + "\n// player names\n")
    edit(); t.assistant_text("Names added.")
elif phase == "cp":
    if arm not in env("STUB_NOCOMPACT_ARMS"):
        stream_boundary = arm not in env("STUB_TRANSCRIPTONLY_ARMS"); transcript_boundary = arm not in env("STUB_STREAMONLY_ARMS")
    if arm in env("STUB_NEWSID_ARMS"): out_sid = str(uuid.uuid4())
    if transcript_boundary:
        t.boundary(trigger="manual", pre=60000, post=9000)
        t.summary("Notes:\n" + rules_text if arm in env("STUB_HAND8_ARMS") else "A summary of the work so far.")
        t.instructions()
        if arm in env("STUB_REFERENCE_ARMS"): t.file_reference(cwd + "/" + RULES)       # D3 outcome 1: the tool leaves a reference to the rules file
        t.manual_compact_tail()
else:
    t.user(prompt)
    if arm in env("STUB_SLICE_ARMS"): t.tool("Bash", {"command": f"head -40 {RULES}"}, "\n".join(rules_text.splitlines()[:40]))
    else: t.tool("Read", {"file_path": cwd + "/" + RULES}, synth.numbered(rules_text))
    app = pathlib.Path("client/app.js"); app.write_text(app.read_text() + "\nfunction resetScores() { /* stub */ }\n")
    if arm not in env("STUB_SLICE_ARMS"):
        leaf = pathlib.Path(".bemyagent/work/2/2.1"); leaf.mkdir(parents=True, exist_ok=True); (leaf / "02_tasks.md").write_text("# tasks\n")
    edit(); t.assistant_text("Reset button added.")
if t.recs:
    with open(tfile, "a") as f:
        for r in t.recs: f.write(json.dumps(r) + "\n")
res = {"type": "result", "subtype": "success", "is_error": False, "num_turns": 4, "result": f"Stub reply for {phase}.", "session_id": out_sid,
       "usage": usage, "modelUsage": mu, "permission_denials": []}
if fmt == "stream-json":
    print(json.dumps({"type": "system", "subtype": "init", "session_id": out_sid, "model": "claude-sonnet-5-5"}))
    if stream_boundary:
        print(json.dumps({"type": "system", "subtype": "compact_boundary", "session_id": out_sid, "compact_metadata": {"trigger": "manual", "pre_tokens": 60000}}))
print(json.dumps(res))
sys.exit(1 if phase == "cp" and arm in env("STUB_CPFAIL_ARMS") else 0)        # B7: a compaction call that exits non-zero after writing its boundary
PY

echo; echo "== 4. C4: a counted arm is refused before a PILOT OK; check_pilot.sh refuses a counted arm"
bash "$HERE/launch.sh" q112 2>&1 | grep -E 'q112' | sed -E "s|$D/||g"
bash "$HERE/check_pilot.sh" q112 | head -1; echo "   exit $?  (stub calls so far: $(grep -c STUB-CALL "$STUB_LOG"))"

echo; echo "== 5. launch.sh q901 .. q906 'bad name' '../x'   (the pilots, four calls each; the stub plays every call)"
bash "$HERE/launch.sh" q901 q902 q903 q904 q905 q906 'bad name' '../x' > "$D/launch.out" 2>&1; echo "launch.sh exit code: $?   (m1: 1 because two names were refused)"
grep -v '^q9[0-9]* ' "$D/launch.out" | grep -v 'prompts t1_sha' | sed -E "s|$D/||g"
echo "-- check_pilot.sh q901 (the good pilot) - the marker is written on PILOT OK only:"
bash "$HERE/check_pilot.sh" q901 | sed -n '/== verdict/,$p' | sed -E "s|$D/||g"; echo "   markers now: $(ls "$D/out" | grep pilot_ok | tr '\n' ' ')"

echo; echo "== 6. after the marker: setup.py six q115 (real PATH for npm), the other counted trees, then the six launch (stub PATH)"
( PATH="$REAL_PATH"; python3 "$HERE/setup.py" six q115 2>&1 | tail -2 | sed -E "s|$D/||g" )
copy q112 q901 "$D/trees" "$D/ptrees"; for a in q116 q117; do copy $a q115 "$D/trees" "$D/trees"; done
echo "-- the pilots root holds: $(ls "$D/ptrees" | tr '\n' ' ')   the six root holds: $(ls "$D/trees" | tr '\n' ' ')"
echo "-- setup.status (in the outputs folder, not beside the trees):"; sed -E 's/(rules_sha1|bemyagent_sha1)=([0-9a-f]{10})[0-9a-f]+/\1=\2../g' "$R214_OUT/setup.status"
echo "-- diff -r (no node_modules, no .git) C (the seed as committed in the pilot's tree, before the pilot's edits) against L (q115, not yet launched):"
mkdir -p "$D/c_seed"; git -C "$D/ptrees/q901" archive HEAD | tar -x -C "$D/c_seed"
(cd "$D" && diff -r -x node_modules -x .git c_seed trees/q115 | sed 's/^\(.\{150\}\).*/\1.../')
echo "-- the two trees' files that differ: $(cd "$D" && diff -rq -x node_modules -x .git c_seed trees/q115 | wc -l | tr -d ' ')"
bash "$HERE/launch.sh" q115 q112 q116 q117 'bad name2' > "$D/launch6.out" 2>&1
grep -v '^q1[0-9]* ' "$D/launch6.out" | grep -v 'prompts t1_sha' | sed -E "s|$D/||g"
echo "-- launch.status (the three prompt hashes are in it; they are shortened here):"
sed -E 's/(t1_sha|cp_sha|t2_sha)=([0-9a-f]{8})[0-9a-f]+/\1=\2../g; s/resumed_from=[0-9a-f]{8}/resumed_from=<id8>/' "$D/out/launch.status" | sort -s -k1,1

echo; echo "== 7. where things are. Trees (what \`ls ..\` shows from inside an arm) and the separate outputs dir"
echo "-- ls pilots root: $(ls "$D/ptrees" | tr '\n' ' ')  ls six root: $(ls "$D/trees" | tr '\n' ' ')"
echo "-- outputs (names only):"; (cd "$D/out" && ls -1 | tr '\n' ' '); echo
echo "-- any launcher output inside either trees dir (must be 0): $(( $(find "$D/trees" -maxdepth 1 -type f | wc -l) + $(find "$D/ptrees" -maxdepth 1 -type f | wc -l) )) files at their top level"
echo "-- the arm's tool memory is recorded, not moved (q115 had one): still in the config? $(find "$D/cfg/projects" -path '*q115*' -name MEMORY.md | wc -l | tr -d ' ') MEMORY.md; moved copies: $(ls "$D/out" | grep -c memory)"

echo; echo "== 8. guard: launch.sh q901 again must refuse and add nothing"
n1=$(wc -l < "$D/out/launch.status" | tr -d ' '); c1=$(wc -l < "$STUB_LOG" | tr -d ' ')
bash "$HERE/launch.sh" q901 | head -1 | sed -E "s|$D/||g"
echo "status lines before/after: $n1 / $(wc -l < "$D/out/launch.status" | tr -d ' ')   stub calls before/after: $c1 / $(wc -l < "$STUB_LOG" | tr -d ' ')"

echo; echo "== 9. snapshots differ as the stub's edits say (q115: t1 vs t2; t2 vs final tree)"
diff -rq "$D/out/snap/q115.t1" "$D/out/snap/q115.t2" | sed "s|$D/||g"; diff -rq "$D/out/snap/q115.t2" "$D/trees/q115" -x node_modules -x .git -x 'game.db*' | sed "s|$D/||g"; echo "(no more lines = the final tree equals the t2 snapshot)"
echo "snapshots taken: $(ls "$D/out/snap" | tr '\n' ' ')"

echo; echo "== 10. certificate.py (key fields)"
python3 "$HERE/certificate.py" --write-each q901 q902 q903 q904 q905 q906 q115 q112 q116 q117 > "$D/cert.json"
python3 - "$D/cert.json" <<'PY'
import json, sys
for a, r in json.load(open(sys.argv[1])).items():
    keep = {k: r.get(k) for k in ("cond", "same_session_id_on_all_three", "one_transcript_in_own_folder", "boundaries_in_transcript", "first_user_equals_prompt_t1",
            "context_carried", "launcher_prompt_hashes_equal_files", "model_pinned", "second_model_in_usage", "override_header_ok", "clean", "design_ok", "base_check_made", "tool_calls_dotdot")}
    keep["failed_terms"] = [k for k, v in (r.get("clean_terms") or {}).items() if not v]
    print(a, keep)
PY

echo; echo "== 11. read.py (per arm: classes, x + n of K, eligibility; then the per-condition counts)"
python3 "$HERE/read.py" q901 q902 q903 q904 q905 q906 q115 q112 q116 q117 > "$D/read.json"
python3 - "$D/read.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for a, r in d["arms"].items():
    i, iv, ii, iii = r.get("i") or {}, r.get("iv") or {}, r.get("ii") or {}, r.get("iii") or {}
    ho = f"x={ii['x']} n={ii['n']} x+n={ii['x_plus_n']} of K={ii['K']}, added line handed back: {ii['added_line_handed_back']}" if ii.get("n") is not None else ii.get("reason")
    print(a, {"cond": r["cond"], "role": r["role"], "iv": iv.get("class", iv.get("reason")), "i": i.get("class", i.get("reason")), "handed_back": ho,
              "eligible": r["eligible"], "why_not": r["eligible_reasons"], "flags": r["flags"], "v": r["v"], "vii": {k: (r["vii"] or {}).get(k) for k in ("new_leaf", "reset_new")}})
    print("   iii:", iii.get("launcher"), iii.get("transcript"), "tokens before/after:", iii.get("prompt_tokens_last_before_boundary"), iii.get("prompt_tokens_first_after_boundary"), "shrank:", iii.get("context_shrank"))
    if i.get("sequence") is not None: print("   accesses in the window (tool, form, class, lines):", [(x["tool"], x["form"], x["class"], f"{x['lines_delivered']}/{x['lines_total']}") for x in i["sequence"]], "write:", i.get("first_write"))
    if ii.get("preserved"): print("   preserved across the boundary:", ii["preserved"])
print("per condition, eligible arms only:"); [print("  ", x) for x in d["per_condition_over_eligible_arms"]]
PY

echo; echo "== 12. the stub's log: every call that happened; flags checked"
sed -E "s|$D/||g" "$STUB_LOG" | sed -E 's/ bad=\[\]//'
echo "calls logged: $(grep -c STUB-CALL "$STUB_LOG")   flags_ok=False: $(grep -c 'flags_ok=False' "$STUB_LOG")   resume calls: $(grep -c 'mode=resume' "$STUB_LOG")   stream-json calls: $(grep -c 'fmt=stream-json' "$STUB_LOG")   per phase: t1 $(grep -c 'phase=t1' "$STUB_LOG") cp $(grep -c 'phase=cp' "$STUB_LOG") t2 $(grep -c 'phase=t2' "$STUB_LOG")"

echo; echo "== 13. check_pilot.sh on the six pilots: q901 slice (PILOT OK, marker), q902 (no boundary), q903 (every line handed back), q904 (session id changed), q905 (the control reads whole: its own verdict, exit 3, no marker), q906 (a reference to the rules file after the boundary: [occasion])"
for a in q901 q902 q903 q904 q905 q906; do echo "-------- $a"; bash "$HERE/check_pilot.sh" $a > "$D/chk.out" 2>&1; rc=$?; sed -n '/== session/,$p' "$D/chk.out" | grep -E "^== (verdict|design)|^\(iv-b\)|^  - |marker written"; echo "   check_pilot.sh exit code: $rc   markers now: $(ls "$D/out" | grep pilot_ok | tr '\n' ' ')"; done
echo "-- G1: every marker was removed at the start of each check; the last pilot checked (q906) is NOT OK, so none stands. A counted arm is refused (exit code 1, m1):"
bash "$HERE/launch.sh" q118 2>&1 | grep refused | sed -E "s|$D/||g"; echo "   exit code: ${PIPESTATUS[0]}"
echo "-- G2: a marker of the right name with the content of another pilot, and an empty one: both refused"
printf 'PILOT OK q902\n' > "$D/out/pilot_ok.q901"; : > "$D/out/pilot_ok.x"
bash "$HERE/launch.sh" q118 2>&1 | grep -c refused | sed 's/^/   refused lines: /'; python3 "$HERE/setup.py" six q113 2>&1 | tail -1 | sed -E "s|$D/||g"; rm -f "$D/out/pilot_ok.q901" "$D/out/pilot_ok.x"
echo "-- m2: setup.py with BMA_SCRATCH unset reads local.env itself (the refusal below comes from the marker gate, not from a KeyError):"
mkdir -p "$D/nomarker"; ( env -u BMA_SCRATCH -u R214_ROOT -u R214P_ROOT R214_OUT="$D/nomarker" PATH="$REAL_PATH" python3 "$HERE/setup.py" six q113 2>&1 | tail -1 | sed -E "s|$D/||g" )
echo "-- G3: an override of the pilot names that names a counted arm or leaves out a pilot is refused:"
R214_PILOTS="q901 q902 q903 q112" python3 "$HERE/kset.py" pilots 2>&1 | head -1; echo "   exit code ${PIPESTATUS[0]}"
R214_PILOTS="q901 q902" python3 "$HERE/kset.py" pilots 2>&1 | head -1; echo "   exit code ${PIPESTATUS[0]}"
R214_PILOTS="q901 q902 q903 q112" R214_TEST_ONLY=1 python3 "$HERE/kset.py" pilots 2>&1 | head -2

echo; echo "== 14. N5 (A7): a repeated arm name, a lock, a concurrent second launch (own trees, own outputs; the stub sleeps 2 s in turn 1 of q914)"
mkdir -p "$D/dup/trees" "$D/dup/cfg/projects" "$D/dup/out"; printf "PILOT OK q901\\n" > "$D/dup/out/pilot_ok.q901"        # the marker the counted arms need (not the point of this run)
for a in q912 q913 q914; do mkdir -p "$D/dup/trees/$a"; (cd "$D/ptrees/q901" && tar -cf - --exclude=node_modules .) | (cd "$D/dup/trees/$a" && tar -xf -); done
dupenv() { R214_ROOT="$D/dup/trees" R214_OUT="$D/dup/out" R214_CFG="$D/dup/cfg" STUB_LOG="$D/stub_dup.log" STUB_SLOW_ARMS="q914" "$@"; }
: > "$D/stub_dup.log"
echo "-- launch.sh q912 q912 (the same name twice):"; dupenv bash "$HERE/launch.sh" q912 q912 2>&1 | grep -vE '^q91[0-9] ' | sed -E "s|$D/||g"
echo "   stub calls: $(grep -c STUB-CALL "$D/stub_dup.log")   status lines for q912: $(grep -c '^q912 ' "$D/dup/out/launch.status")   t1 lines: $(grep -c '^q912 t1 exit' "$D/dup/out/launch.status")   (want 3 calls, one t1 line)"
echo "-- a lock left by another launch (mkdir $D/dup/out/locks/q913 first): launch.sh q913"
mkdir -p "$D/dup/out/locks/q913"; c0=$(grep -c STUB-CALL "$D/stub_dup.log"); dupenv bash "$HERE/launch.sh" q913 2>&1 | grep 'q913' | sed -E "s|$D/||g"; echo "   stub calls added: $(( $(grep -c STUB-CALL "$D/stub_dup.log") - c0 ))"
echo "-- two launches of q914 at the same moment:"
c0=$(grep -c STUB-CALL "$D/stub_dup.log")
( dupenv bash "$HERE/launch.sh" q914 > "$D/dup/l1.out" 2>&1 ) & ( dupenv bash "$HERE/launch.sh" q914 > "$D/dup/l2.out" 2>&1 ) & wait
echo "   launch 1 / launch 2 said: $(grep -h 'q914:' "$D/dup/l1.out" "$D/dup/l2.out" | sed -E "s|$D/||g" | tr '\n' '|')"
echo "   stub calls added: $(( $(grep -c STUB-CALL "$D/stub_dup.log") - c0 ))   t1 lines for q914: $(grep -c '^q914 t1 exit' "$D/dup/out/launch.status")   (want 3 calls, one t1 line, one refusal)"

echo; echo "== 15. A7: the time limit. Same stub, same PATH. R214_TIMEOUT=3; the stub hangs (sleeps 300 s) in turn 1 of q915"
mkdir -p "$D/hang/trees/q915" "$D/hang/cfg/projects" "$D/hang/out" "$D/hang/out2"; printf "PILOT OK q901\\n" | tee "$D/hang/out/pilot_ok.q901" > "$D/hang/out2/pilot_ok.q901"; (cd "$D/ptrees/q901" && tar -cf - --exclude=node_modules .) | (cd "$D/hang/trees/q915" && tar -xf -)
: > "$D/stub_hang.log"
t0=$(date +%s)
R214_ROOT="$D/hang/trees" R214_OUT="$D/hang/out" R214_CFG="$D/hang/cfg" STUB_LOG="$D/stub_hang.log" STUB_HANG_ARMS="q915" R214_TIMEOUT=3 bash "$HERE/launch.sh" q915 2>&1 | sed -E "s|$D/||g" | grep -E 'resolves|q915 (t1|cp|t2)|killed|failed'
echo "elapsed: $(( $(date +%s) - t0 )) s (limit 3 s, the stub would have slept 300)"
echo "launch.sh resolved claude to the same file as 'command -v claude' here: $( [ "$(R214_ROOT="$D/hang/trees" R214_OUT="$D/hang/out2" R214_CFG="$D/hang/cfg" bash "$HERE/launch.sh" none 2>&1 | sed -n 's/^claude resolves to: \(.*\)   time limit.*/\1/p')" = "$(command -v claude)" ] && echo yes || echo NO )"
echo "stub log of the hung call: $(sed -E "s|$D/||g" "$D/stub_hang.log" | tr '\n' '|')"
echo "stub processes still alive after the run: $(pgrep -f "$D/stub/stub.py" | wc -l | tr -d ' ')   (0 = the hung call was killed)"
echo "calls made for q915: $(grep -c STUB-CALL "$D/stub_hang.log") (the turn-1 call only: the arm ended like a failed call, no compaction, no turn 2)"

echo; echo "== 16. B7: a compaction call that exits 1 after writing its boundary ends its arm; a time limit that is not a positive integer is refused"
mkdir -p "$D/cpf/trees/q916" "$D/cpf/cfg/projects" "$D/cpf/out" "$D/cpf/out_to"; printf "PILOT OK q901\\n" | tee "$D/cpf/out/pilot_ok.q901" > "$D/cpf/out_to/pilot_ok.q901"; (cd "$D/ptrees/q901" && tar -cf - --exclude=node_modules .) | (cd "$D/cpf/trees/q916" && tar -xf -)
: > "$D/stub_cpf.log"
R214_ROOT="$D/cpf/trees" R214_OUT="$D/cpf/out" R214_CFG="$D/cpf/cfg" STUB_LOG="$D/stub_cpf.log" STUB_CPFAIL_ARMS="q916" bash "$HERE/launch.sh" q916 2>&1 | grep -E '^q916 (cp|compaction|turn2)' | sed -E 's/(pre_tokens=[0-9]+).*/\1 .../'
echo "stub calls for q916: $(grep -c STUB-CALL "$D/stub_cpf.log")  per phase: t1 $(grep -c 'phase=t1' "$D/stub_cpf.log") cp $(grep -c 'phase=cp' "$D/stub_cpf.log") t2 $(grep -c 'phase=t2' "$D/stub_cpf.log")   (want one t1, one cp, no t2)"
for v in abc 0 -5 3.5; do
  : > "$D/stub_to.log"
  out=$(R214_ROOT="$D/cpf/trees" R214_OUT="$D/cpf/out_to" R214_CFG="$D/cpf/cfg" STUB_LOG="$D/stub_to.log" R214_TIMEOUT="$v" bash "$HERE/launch.sh" q916 2>&1); rc=$?
  echo "R214_TIMEOUT='$v': exit $rc, $(echo "$out" | head -1 | sed -E "s|$D/||g"), stub calls: $(grep -c STUB-CALL "$D/stub_to.log")"
done

echo; echo "== 17. real-CLI evidence"
echo "projects in the REAL config folder before / after: $REAL_BEFORE / $(ls "$REAL_CFG/projects" 2>/dev/null | wc -l | tr -d ' ')   (equal = nothing was written there)"
echo "dry-run folders in the real config folder: $(ls "$REAL_CFG/projects" 2>/dev/null | grep -c 'p214')   (0 = the real claude never ran)"
n=0; for dir in $(echo "$PATH" | tr ':' ' '); do [ "$dir" != "$D/stub" ] && [ -x "$dir/claude" ] && n=$((n + 1)); done
echo "directories of the PATH used by launch.sh that hold a claude other than the stub: $n   (0 = the real binary is unreachable)"
}
body 2>&1 | "$HERE/mask.sh"
