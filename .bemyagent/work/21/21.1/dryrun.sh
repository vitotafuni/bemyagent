#!/bin/bash
# 21.1 launcher dry-run WITHOUT the real CLI. A stub named `claude` is first on a PATH that does not
# contain the real one (/opt/homebrew/bin); R211_ROOT (trees), R211_OUT (outputs) and R211_CFG point into
# a throwaway root. The arm trees are copies; the ten real ones in scratchpad/r211 are only read.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$HERE/local.env" ] && . "$HERE/local.env"      # machine-local BMA_SCRATCH / CLAUDE_CONFIG_DIR (gitignored)
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
ROOT="${BMA_REPO:-$(cd "$(dirname "$0")/../../../.." && pwd)}"
KEY=$(printf %s "$ROOT" | sed 's/[^A-Za-z0-9]/-/g')      # the repo's project folder name in the tool config
REAL_CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"      # the real tool-config folder, captured before any override
D="$S/r211-dry"
rm -rf "$D"; mkdir -p "$D/stub" "$D/trees" "$D/out" "$D/cfg/projects"
export R211_ROOT="$D/trees" R211_OUT="$D/out" R211_CFG="$D/cfg" STUB_LOG="$D/stub.log" STUB_KEY="$KEY" STUB_MEM_ARMS="q106" STUB_NORESUME_ARMS="q109" STUB_SHRINK_ARMS="q107" STUB_ISERR_ARMS="q105" STUB_FAILT2_ARMS="q108"
: > "$STUB_LOG"

cat > "$D/stub/stub.py" <<'PY'
import json, os, pathlib, re, sys, uuid
args = sys.argv[1:]
def L(s):
    with open(os.environ["STUB_LOG"], "a") as f: f.write(s + "\n")
prompt = resume = model = fmt = None; tools = []; bad = []
i = 0
while i < len(args):
    a = args[i]
    if a == "-p": prompt = args[i + 1]; i += 2
    elif a == "--resume": resume = args[i + 1]; i += 2
    elif a == "--model": model = args[i + 1]; i += 2
    elif a == "--output-format": fmt = args[i + 1]; i += 2
    elif a == "--allowedTools":
        i += 1
        while i < len(args) and not args[i].startswith("--"): tools.append(args[i]); i += 1
    else: bad.append(a); i += 1
cwd = os.getcwd(); arm = os.path.basename(cwd); cfg = os.environ.get("CLAUDE_CONFIG_DIR", "")
env = lambda k: os.environ.get(k, "").split()
flags_ok = bool(prompt) and model == "sonnet" and fmt == "json" and not bad and \
    tools == ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
phase = "s2" if "Carry on" in prompt else "t2" if "Reset scores" in prompt else "t1"
L(f"STUB-CALL arm={arm} phase={phase} mode={'resume' if resume else 'new'} flags_ok={flags_ok} bad={bad} cfg_is_pinned={cfg == os.environ['R211_CFG']}")
if not flags_ok: sys.exit(2)
fresh = (not resume) or arm in env("STUB_NORESUME_ARMS")   # that arm's stub ignores --resume
sid = str(uuid.uuid4()) if fresh else resume
enc = re.sub(r"[^A-Za-z0-9]", "-", cwd)                     # the CLI's project-folder naming
proj = pathlib.Path(cfg) / "projects" / enc; proj.mkdir(parents=True, exist_ok=True)
OVR = "OVERRIDE any default behavior"
ctx = {"t1": 50000, "t2": 10000 if arm in env("STUB_SHRINK_ARMS") else 51000, "s2": 40000}[phase]
ev = []
if fresh:
    ev.append({"type": "attachment", "attachment": {"type": "instructions", "files": [{"type": "project", "path": cwd + "/CLAUDE.md", "content": OVR + " ... " + OVR}]}})
ev.append({"type": "user", "message": {"role": "user", "content": prompt}})
ev.append({"type": "assistant", "message": {"role": "assistant", "usage": {"input_tokens": 5, "cache_read_input_tokens": ctx, "cache_creation_input_tokens": 100},
    "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": cwd + "/client/app.js"}}]}})
dirs = [proj]
if arm in env("STUB_DECOY_ARMS"):                           # the user's own project folder also receives the session file
    dd = pathlib.Path(cfg) / "projects" / os.environ["STUB_KEY"]; dd.mkdir(parents=True, exist_ok=True); dirs.append(dd)
for d in dirs:
    with open(d / f"{sid}.jsonl", "a") as f:
        for e in ev: f.write(json.dumps(e) + "\n")
if arm in env("STUB_MEM_ARMS"):
    (proj / "memory").mkdir(exist_ok=True)
    (proj / "memory" / "MEMORY.md").write_text("- fake index\n"); (proj / "memory" / "topic.md").write_text("fake\n")
B = {"t1": ("Task: work/1/1.1 (scoreboard)", "Intent: a scoreboard above the board", "Next: await the next request"),
     "t2": ("Task: none", "Intent: a Reset scores button; only reset win counts, never delete saved games; later", "Next: later: Reset scores"),
     "s2": ("Task: work/2/2.1", "Intent: a Reset scores button; only reset win counts, never delete saved games", "Next: await review")}[phase]
plan = pathlib.Path(".bemyagent/docs/06-implementation-plan.md"); t = plan.read_text(); has = "## Resume here\n" in t
if has:
    head, rest = t.split("## Resume here\n", 1)
    plan.write_text(head + "## Resume here\n" + "\n".join(B) + "\n\n" + rest[rest.index("\n\n") + 2:])
app = pathlib.Path("client/app.js")
if phase == "t1": app.write_text(app.read_text() + "\n// scoreboard\n")
if phase == "s2":
    app.write_text(app.read_text() + "\nfunction resetScores() { /* stub */ }\n")
    pathlib.Path("server/index.js").write_text(pathlib.Path("server/index.js").read_text() + "\n// POST /api/scores/reset\n")
res = f"Stub reply for {phase}." + ("\n\n" + "\n".join(B) if has else "")
w = {"input_tokens": 10, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": 10000, "output_tokens": 500}
print(json.dumps({"type": "result", "subtype": "success", "is_error": phase == "t1" and arm in env("STUB_ISERR_ARMS"), "num_turns": 4, "result": res, "session_id": sid,
                  "usage": w, "permission_denials": [],
                  "modelUsage": {"claude-sonnet-5-5": {"inputTokens": 10, "cacheCreationInputTokens": 1000,
                                                       "cacheReadInputTokens": 10000, "outputTokens": 500}}}))
sys.exit(1 if phase == "t2" and arm in env("STUB_FAILT2_ARMS") else 0)
PY
printf '#!/bin/bash\nexec python3 "%s/stub/stub.py" "$@"\n' "$D" > "$D/stub/claude"; chmod +x "$D/stub/claude"

copy() { mkdir -p "$1/$2"; (cd "$S/r211/$3" && tar -cf - --exclude=node_modules .) | (cd "$1/$2" && tar -xf -); }
for a in q106 q107 q108 q109; do copy "$D/trees" $a q106; done; for a in q103 q105; do copy "$D/trees" $a q103; done
echo "== 1. which claude does the launcher see? (PATH = stub : /usr/local/bin : /usr/bin : /bin)"
export PATH="$D/stub:/usr/local/bin:/usr/bin:/bin"
command -v claude; type -a claude
echo; echo "== 2. launch.sh q106 q103 q109 q107 q105 q108  (q106: fake memory/; q103: none; q109: stub ignores --resume; q107: context shrinks at turn 2; q105: turn 1 is_error; q108: turn 2 exits 1)"
bash "$HERE/launch.sh" q106 q103 q109 q107 q105 q108 'bad name' '../x'
echo; echo "== 3. where things are. Arm trees (what \`ls ..\` shows from inside an arm) and the separate outputs dir:"
echo "-- ls $D/trees:"; ls "$D/trees"; echo "-- ls $D/out:"; (cd "$D/out" && ls -1); echo "-- out/snap:"; ls "$D/out/snap"; echo "-- memory moved aside (out/q106.memory.s1):"; ls "$D/out/q106.memory.s1"
echo "-- any launcher output inside the trees dir (must be 0): $(find "$D/trees" -maxdepth 1 -type f | wc -l) files at its top level"
echo; echo "== 4. the memory step both ways, the resume check, the stops"; grep -E "memory|resume_ok|session2|failed" "$D/out/launch.status"
echo; echo "== 5. guard: launch.sh q106 again must refuse and add nothing"
n1=$(wc -l < "$D/out/launch.status"); c1=$(wc -l < "$STUB_LOG")
bash "$HERE/launch.sh" q106 | head -1
echo "status lines before/after: $n1 / $(wc -l < "$D/out/launch.status")   stub calls before/after: $c1 / $(wc -l < "$STUB_LOG")"
echo; echo "== 6. snapshots differ as the stub's edits say (q106: t1 vs t2, then t2 vs final tree)"
diff -rq "$D/out/snap/q106.t1" "$D/out/snap/q106.t2" | sed "s|$D/||g"; diff -rq "$D/out/snap/q106.t2" "$D/trees/q106" -x node_modules -x .git -x 'game.db*' | sed "s|$D/||g"
echo; echo "== 7. score.py (q106 in full; the others as their readings)"; python3 "$HERE/score.py" q106 q103 q109 q107 q105 q108 > "$D/score.json"
python3 - "$D/score.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print(json.dumps(d["q106"], indent=1))
for a, r in d.items():
    if a != "q106": print(a, {k: r.get(k) for k in ("cond", "i", "ii", "iii", "iv_equal_count", "v", "vi_destructive_new", "viii", "incomplete")}, r["status"])
PY
echo; echo "== 8. certificate.py"; python3 "$HERE/certificate.py" q106 q103 q109 q107 > "$D/cert.json"
python3 - "$D/cert.json" <<'PY'
import json, sys
for a, r in json.load(open(sys.argv[1])).items():
    print(a, {k: r[k] for k in r if k not in ("t1", "t2", "s2", "arm_dir")})
    for k in ("t1", "t2", "s2"):
        print("   ", k, {x: y for x, y in r[k].items() if x not in ("transcript_files", "instruction_files", "session")})
PY
echo; echo "== 9. the stub's log: every call that happened; flags checked"
cat "$STUB_LOG"
echo "calls logged: $(grep -c STUB-CALL "$STUB_LOG")   flags_ok=False: $(grep -c 'flags_ok=False' "$STUB_LOG")   resume calls: $(grep -c 'mode=resume' "$STUB_LOG")"
echo; echo "== 10. check_pilot.sh (q106 good; q109 resume ignored; q107 context shrank; q105 is_error)"
for a in q106 q109 q107 q105; do echo "-- $a"; bash "$HERE/check_pilot.sh" $a | sed -n '/== facts/,$p'; done

echo; echo "== 11. DECOY (VERIFY B2): the stub writes the arm's session file ALSO into the user's project folder $KEY, which holds a memory/ of its own"
for loc in C it_IT.UTF-8; do
  X="$D/decoy_$loc"; mkdir -p "$X/trees" "$X/out" "$X/cfg/projects/$KEY/memory"
  echo "user memory 1" > "$X/cfg/projects/$KEY/memory/MEMORY.md"; echo "user memory 2" > "$X/cfg/projects/$KEY/memory/keep.md"
  copy "$X/trees" q106 q106
  ( export R211_ROOT="$X/trees" R211_OUT="$X/out" R211_CFG="$X/cfg" STUB_DECOY_ARMS="q106" LC_ALL="$loc"; bash "$HERE/launch.sh" q106 > /dev/null )
  echo "-- LC_ALL=$loc: status lines:"; grep -E "memory|session2|resume_ok" "$X/out/launch.status" | sed "s|$D/||g"
  echo "   decoy memory/ still in place, files: $(ls "$X/cfg/projects/$KEY/memory" | wc -l | tr -d ' ') (want 2)   moved copy exists: $([ -d "$X/out/q106.memory.s1" ] && echo YES-WRONG || echo no)   session 2 ran: $([ -e "$X/out/q106.s2.json" ] && echo YES-WRONG || echo no)"
done
echo; echo "== 12. real-CLI evidence"
echo "dry-run projects in the REAL config dir: $(ls "$REAL_CFG/projects" | grep -c r211-dry)  (0 = the real claude never ran)"
echo "real claude directory in the PATH used by launch.sh: $(echo "$PATH" | tr ':' '\n' | grep -c homebrew)  (0 = unreachable)"
