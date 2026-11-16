#!/bin/bash
# 21.1 — 20.11's launcher (one arm = one `command claude -p` run from inside its own tree, so no
# parent-project instruction is injected) extended from one call per arm to THREE per arm:
#   turn 1  `claude -p <prompt_t1>`                      -> $OUT/<arm>.t1.json   snapshot snap/<arm>.t1/
#   turn 2  `claude -p <prompt_t2> --resume <session>`   -> $OUT/<arm>.t2.json   snapshot snap/<arm>.t2/
#   (reset) the harness's memory folder for the arm is moved aside, then
#   s2      a NEW `claude -p <prompt_s2>` (no --resume, no --continue) -> $OUT/<arm>.s2.json
# What is new against 20.11, and why:
#   * `--resume` is the carrier of a REAL second user turn: the model sees turn 2 as the user's own
#     message in the same context, not a relayed one (16.1's coordinator) and not a fresh run.
#     Assumed, never run before this round: the pilot (q900) is what tests it, and the launcher
#     checks it per arm — the turn-2 transcript must hold the turn-1 task sentence AND the turn-2
#     sentence as user messages, else resume_ok=0 and session 2 is skipped for that arm.
#   * Snapshots after each turn: every reading in score.py is a DIFFERENCE between t1, t2 and the
#     final tree, never a regex on a finished tree that already holds seeded text.
#   * The harness's auto-memory is a CONFOUND: it is keyed to the arm's path and survives a new
#     process, so a block could be "remembered" across the reset without the protocol's file doing
#     the work. It is moved aside before session 2 and its existence/size is recorded
#     (memory_existed=0|1 files=N in launch.status): a finding, not noise.
# Three things are load-bearing (each was a failure in 20.11 before it was a finding):
#   * `command claude` — the user's shell defines a `claude` function that hands a headless run a
#     fresh `mktemp -d` config dir, which has no auth and no transcript path.
#   * CLAUDE_CONFIG_DIR pinned by `local.env` (env R211_CFG overrides it, for the dry-run only) — the transcript
#     must land somewhere the certificate can read it.
#   * --allowedTools — in `-p` mode an unpermitted call is denied, not queued, and an arm that
#     cannot run `npm test` floors every metric for a reason that is not the protocol.
# Corrections after the independent VERIFY (03e_apparatus_verify.md):
#   * OUTPUTS LIVE OUTSIDE THE ARM TREES' PARENT. The arm trees stay in $R (R211_ROOT, default
#     scratchpad/r211); every file this script writes - <arm>.{t1,t2,s2}.{json,err}, launch.status,
#     snap/, <arm>.memory.s1 - goes to $OUT (R211_OUT, default scratchpad/r211_out). A session 2 that
#     runs `ls ..` from its arm must find only sibling arm trees, never turn 2's reply or a snapshot.
#   * The memory folder moved aside is PROVEN to be the arm's own: the project folder's name must equal
#     the arm path with every non-alphanumeric turned into '-'. The transcript is read from that exact
#     folder, never from "the first match of a glob". Any other folder holding the session file means
#     no move, no session 2, and a status line saying so.
#   * A turn that exits non-zero or reports is_error stops the arm (turn 1 and turn 2 alike).
# Usage: launch.sh <arm> [<arm> ...]     (arms run in parallel; each arm's three calls in sequence)
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$HERE/local.env" ] && . "$HERE/local.env"      # machine-local BMA_SCRATCH / CLAUDE_CONFIG_DIR (gitignored)
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
R="${R211_ROOT:-$S/r211}"          # the arm trees (untouched by this script except by the arms themselves)
OUT="${R211_OUT:-$S/r211_out}"      # every launcher output
export CLAUDE_CONFIG_DIR="${R211_CFG:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}"
STATUS="$OUT/launch.status"
mkdir -p "$OUT/snap"

# the sentences the resume check looks for in the turn-2 transcript
T1_SENT="$(grep -m1 '^Task:' "$HERE/prompt_t1.txt")"
T2_SENT="$(cat "$HERE/prompt_t2.txt")"

snap() {   # snap <tree> <dest>: the tree without node_modules, .git, game.db*
  rm -rf "$2"; mkdir -p "$2"
  (cd "$1" && tar -cf - --exclude=node_modules --exclude=.git --exclude='game.db*' .) | (cd "$2" && tar -xf -)
}

err_of() { python3 -c 'import json,sys; print(1 if json.load(open(sys.argv[1])).get("is_error") else 0)' "$1" 2>/dev/null; }
sid_of() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("session_id",""))' "$1" 2>/dev/null; }

run_claude() {   # run_claude <prompt> <out.json> <err> [extra flags before the roster]; prints the exit code
  local prompt="$1" out="$2" err="$3"; shift 3
  command claude -p "$prompt" "$@" --model sonnet --output-format json \
    --allowedTools Read Write Edit Bash Glob Grep < /dev/null > "$out" 2> "$err"
  echo $?
}

one_arm() {
  local a="$1" d="$R/$1" p1 p2 ps2 rc sid sid2 tr proj n mem want other
  cd "$d" || { echo "$a missing-tree" >> "$STATUS"; return; }
  want=$(printf %s "$d" | sed 's/[^A-Za-z0-9]/-/g')      # the arm's own project folder name: its path, every non-alphanumeric a dash
  p1=$(sed "s|<ARM_DIR>|$d|" "$HERE/prompt_t1.txt")
  p2=$(cat "$HERE/prompt_t2.txt")
  ps2=$(sed "s|<ARM_DIR>|$d|" "$HERE/prompt_s2.txt")

  rc=$(run_claude "$p1" "$OUT/$a.t1.json" "$OUT/$a.t1.err")
  echo "$a t1 exit=$rc" >> "$STATUS"
  snap "$d" "$OUT/snap/$a.t1"
  sid=$(sid_of "$OUT/$a.t1.json")
  if [ "$rc" != 0 ] || [ -z "$sid" ] || [ "$(err_of "$OUT/$a.t1.json")" = 1 ]; then echo "$a t1 failed: no turn 2 for this arm" >> "$STATUS"; return; fi

  rc=$(run_claude "$p2" "$OUT/$a.t2.json" "$OUT/$a.t2.err" --resume "$sid")
  echo "$a t2 exit=$rc resumed_from=${sid:0:8}" >> "$STATUS"
  snap "$d" "$OUT/snap/$a.t2"
  sid2=$(sid_of "$OUT/$a.t2.json")
  if [ "$rc" != 0 ] || [ "$(err_of "$OUT/$a.t2.json")" = 1 ]; then echo "$a t2 failed: no session 2 for this arm" >> "$STATUS"; return; fi

  # did turn 2 really continue the conversation? both user messages must be in the t2 transcript
  tr=""; other=""
  if [ -n "$sid2" ]; then
    [ -f "$CLAUDE_CONFIG_DIR/projects/$want/$sid2.jsonl" ] && tr="$CLAUDE_CONFIG_DIR/projects/$want/$sid2.jsonl"
    other=$(ls "$CLAUDE_CONFIG_DIR"/projects/*/"$sid2".jsonl 2>/dev/null | grep -v "/projects/$want/" | head -1)
  fi
  if [ -z "$tr" ] && [ -n "$other" ]; then
    echo "$a memory=NOT-MOVED the transcript sits only in a folder that is not the arm's own ($(basename "$(dirname "$other")")): session2=skipped" >> "$STATUS"; return
  fi
  n="0 0"
  if [ -n "$sid2" ] && [ -n "$tr" ]; then
    n=$(python3 - "$tr" "$T1_SENT" "$T2_SENT" <<'PY'
import json, sys
tr, s1, s2 = sys.argv[1:4]
n1 = n2 = 0
for line in open(tr, errors="replace"):
    try: ev = json.loads(line)
    except Exception: continue
    if ev.get("type") != "user": continue
    c = (ev.get("message") or {}).get("content")
    t = c if isinstance(c, str) else " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text")
    n1 += s1 in t; n2 += s2 in t
print(n1, n2)
PY
)
  fi
  set -- $n
  if [ "${1:-0}" -ge 1 ] && [ "${2:-0}" -ge 1 ]; then ok=1; else ok=0; fi
  echo "$a resume_ok=$ok t1_sentence_msgs=${1:-0} t2_sentence_msgs=${2:-0} transcript_found=$([ -n "$tr" ] && echo 1 || echo 0)" >> "$STATUS"
  if [ "$ok" != 1 ]; then echo "$a session2=skipped (resume_ok=0)" >> "$STATUS"; return; fi

  # the harness's own memory for this arm: the memory/ folder in the project folder holding the transcript
  proj=$(dirname "$tr"); mem="$proj/memory"
  if [ "$(basename "$proj")" != "$want" ] || [ -n "$other" ]; then   # belt and braces: the folder must be the arm's own, and the only one
    echo "$a memory=NOT-MOVED the session file also sits in a folder that is not the arm's own ($(basename "$(dirname "${other:-$tr}")")): session2=skipped" >> "$STATUS"; return
  fi
  if [ -d "$mem" ]; then
    n=$(find "$mem" -type f | wc -l | tr -d ' ')
    mv "$mem" "$OUT/$a.memory.s1"
    echo "$a memory_existed=1 files=$n moved_to=$OUT/$a.memory.s1" >> "$STATUS"
  else
    echo "$a memory_existed=0 files=0" >> "$STATUS"
  fi

  # the reset: a NEW process, no --resume, no --continue
  rc=$(run_claude "$ps2" "$OUT/$a.s2.json" "$OUT/$a.s2.err")
  echo "$a s2 exit=$rc" >> "$STATUS"
}

for a in "$@"; do
  case "$a" in ""|*[!A-Za-z0-9]*) echo "'$a' is not an arm name (skipped)"; continue;; esac
  if [ ! -d "$R/$a" ]; then echo "$a: no tree at $R/$a (skipped)"; continue; fi
  if [ -e "$OUT/$a.t1.json" ]; then echo "$a: $OUT/$a.t1.json exists - refusing to run twice (skipped)"; continue; fi
  ( one_arm "$a" ) &          # an explicit subshell group, as in 20.11: a bare `fn &` lost the rest of the function after the claude call under bash 3.2
done
wait
echo "all arms finished"
cat "$STATUS"
