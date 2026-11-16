#!/bin/bash
# 21.4 — 21.1's launcher (one arm = `command claude -p` runs from inside its own tree, so no parent-project
# instruction is injected; outputs outside the trees' parent; refuses to run an arm twice) with the three
# calls this round needs, on ONE session:
#   turn 1      -p <prompt_t1>                              --output-format json         -> <arm>.t1.json   snap/<arm>.t1/
#   compaction  -p "/compact" --resume <session of turn 1>  --output-format stream-json --verbose -> <arm>.cp.jsonl
#   turn 2      -p <prompt_t2>  --resume <same session>     --output-format json         -> <arm>.t2.json   snap/<arm>.t2/
# What is new against 21.1, and why:
#   * `/compact` under `-p --resume` has never run in this repo (the pilot, q901, is its first test). The launcher
#     therefore PROVES the compaction before it spends turn 2: (a) the stream output holds a record
#     type=system subtype=compact_boundary, and/or (b) the on-disk transcript holds one more boundary record
#     than before the call. No proof -> `turn2=skipped`, the arm ends. The shape of a boundary is in boundary.py.
#   * The session id must survive the compaction. If the stream reports another id, turn 2 would resume the
#     pre-compaction history: the arm stops with that said (the Pivot of 02_tasks.md: --resume does not carry the session).
#   * The arm's tool-memory folder is RECORDED after turn 1 (exists, number of files) and NOT moved: unlike
#     21.1 there is no session 2, and a main session has that memory too.
#   * The hash of each prompt exactly as passed is written to launch.status; certificate.py checks it against the files.
# Kept from 21.1 (each was a failure before it was a finding):
#   * `command claude` — the user's shell defines a `claude` function that hands a headless run a fresh
#     `mktemp -d` config dir, which has no auth and no transcript path.
#   * CLAUDE_CONFIG_DIR pinned by `local.env` (env R214_CFG overrides it, for the dry-run only).
#   * --allowedTools on every call — in `-p` mode an unpermitted call is denied, not queued.
#   * `--model sonnet` on every call (a resumed call does not inherit it).
#   * OUTPUTS LIVE OUTSIDE THE ARM TREES' PARENT ($OUT, not under $R); the transcript is read only from the arm's
#     own project folder (arm path, every non-alphanumeric a dash); a turn that exits non-zero or reports
#     is_error stops the arm; arm names are validated; an arm is never run twice.
#   * A7 (Amendment 1): a repeated arm name is run once; a per-arm lock (`mkdir <out>/locks/<arm>`) is taken before the arm starts, so a second
#     launch cannot start it either; each call has a time limit (below).
#   * C4 (Amendment 3): a pilot's tree stands in R214P_ROOT, a counted arm's in R214_ROOT; a counted arm is refused unless check_pilot.sh has
#     written a marker <out>/pilot_ok.<pilot> on a PILOT OK.
# Usage: launch.sh <arm> [<arm> ...]     (arms run in parallel; each arm's calls in sequence; R214_TIMEOUT seconds per call)
set -u
export PYTHONDONTWRITEBYTECODE=1      # no __pycache__ in the task folder
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$HERE/local.env" ] && . "$HERE/local.env"      # machine-local BMA_SCRATCH / CLAUDE_CONFIG_DIR (gitignored)
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
R="${R214_ROOT:-$S/r214}"          # the trees of the six (untouched by this script except by the arms themselves)
RP="${R214P_ROOT:-$S/r214p}"       # the trees of the pilots (C4): a pilot's tree is found in this root, a counted arm's in $R
PILOTS="${R214_PILOTS:-q901 q902 q903}"
is_pilot() { case " $PILOTS " in *" $1 "*) return 0;; esac; return 1; }
root_of() { if is_pilot "$1"; then echo "$RP"; else echo "$R"; fi; }
OUT="${R214_OUT:-$S/r214_out}"      # every launcher output
export CLAUDE_CONFIG_DIR="${R214_CFG:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}}"
STATUS="$OUT/launch.status"
case "$OUT/" in "$R/"*|"$RP/"*) echo "R214_OUT must not lie inside the arm trees ($R, $RP)"; exit 2;; esac
mkdir -p "$OUT/snap"

snap() {   # snap <tree> <dest>: the tree without node_modules, .git, game.db*
  rm -rf "$2"; mkdir -p "$2"
  (cd "$1" && tar -cf - --exclude=node_modules --exclude=.git --exclude='game.db*' .) | (cd "$2" && tar -xf -)
}

err_of() { python3 -c 'import json,sys; print(1 if json.load(open(sys.argv[1])).get("is_error") else 0)' "$1" 2>/dev/null; }
sid_of() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("session_id",""))' "$1" 2>/dev/null; }
sha() { if command -v shasum > /dev/null; then shasum -a 256; else sha256sum; fi | cut -d' ' -f1; }

# A7 (Amendment 1): every call has a time limit (R214_TIMEOUT seconds, default 3600). `perl -e 'alarm shift; exec @ARGV'` sets an
# alarm and execs the binary, so the alarm survives the exec and kills that process; the shell then sees exit code 142 and the
# arm ends like a failed call. The binary is resolved ONCE, here, by `command -v` - the same lookup `command claude` made - and
# perl execs that absolute path, so the dry-run stub is what runs there and the user's shell function is still bypassed.
# Children the real binary may have spawned are not killed by the alarm.
LIMIT="${R214_TIMEOUT:-3600}"
case "$LIMIT" in [1-9]*) case "$LIMIT" in *[!0-9]*) echo "R214_TIMEOUT='$LIMIT' is not a positive integer - refusing to start"; exit 2;; esac;;
  *) echo "R214_TIMEOUT='$LIMIT' is not a positive integer - refusing to start"; exit 2;; esac      # B7
CLAUDE_BIN="$(command -v claude)"
[ -n "$CLAUDE_BIN" ] || { echo "no claude on the PATH"; exit 2; }
command -v perl > /dev/null || { echo "perl is needed for the time limit"; exit 2; }
echo "claude resolves to: $CLAUDE_BIN   time limit per call: ${LIMIT}s"

claude_call() {   # claude_call <out> <err> <prompt> <resume id or ""> <json|stream-json>; prints the exit code
  local out="$1" err="$2" prompt="$3" resume="$4" fmt="$5" args
  args=(-p "$prompt")
  [ -n "$resume" ] && args+=(--resume "$resume")
  args+=(--model sonnet --output-format "$fmt")
  [ "$fmt" = stream-json ] && args+=(--verbose)
  # accepted (ruling 2026-11-15): the alarm ends the exec'd process only; children the real binary may have spawned are not killed
  perl -e 'alarm shift; exec @ARGV' "$LIMIT" "$CLAUDE_BIN" "${args[@]}" --allowedTools Read Write Edit Bash Glob Grep < /dev/null > "$out" 2> "$err"
  echo $?
}
timeout_note() { [ "$3" = 142 ] && echo "$1 $2 killed by the time limit (${LIMIT}s)" >> "$STATUS"; return 0; }

one_arm() {
  local a="$1" d="$(root_of "$1")/$1" p1 pc p2 rc sid sid2 want proj tr other mem n before after iserr
  local s_found s_pre s_sid t_n t_trig t_pre t_post by pre same cprc
  cd "$d" || { echo "$a missing-tree" >> "$STATUS"; return; }
  want=$(printf %s "$d" | sed 's/[^A-Za-z0-9]/-/g')      # the arm's own project folder name: its path, every non-alphanumeric a dash
  proj="$CLAUDE_CONFIG_DIR/projects/$want"
  p1=$(sed "s|<ARM_DIR>|$d|" "$HERE/prompt_t1.txt")
  pc=$(cat "$HERE/prompt_compact.txt")
  p2=$(cat "$HERE/prompt_t2.txt")
  echo "$a prompts t1_sha=$(printf %s "$p1" | sha) cp_sha=$(printf %s "$pc" | sha) t2_sha=$(printf %s "$p2" | sha)" >> "$STATUS"

  # ---- turn 1
  rc=$(claude_call "$OUT/$a.t1.json" "$OUT/$a.t1.err" "$p1" "" json)
  echo "$a t1 exit=$rc" >> "$STATUS"; timeout_note "$a" t1 "$rc"
  snap "$d" "$OUT/snap/$a.t1"
  sid=$(sid_of "$OUT/$a.t1.json"); iserr=$(err_of "$OUT/$a.t1.json")
  if [ "$rc" != 0 ] || [ -z "$sid" ] || [ "$iserr" != 0 ]; then
    echo "$a t1 failed (exit=$rc is_error=${iserr:-?} session=$([ -n "$sid" ] && echo yes || echo no)): arm stopped, no compaction, no turn 2" >> "$STATUS"; return
  fi

  # ---- the transcript: the arm's own project folder, and only there
  tr="$proj/$sid.jsonl"
  other=$(ls "$CLAUDE_CONFIG_DIR"/projects/*/"$sid".jsonl 2>/dev/null | grep -vF "$proj/" | head -1)
  if [ ! -f "$tr" ] || [ -n "$other" ]; then
    echo "$a transcript_found=$([ -f "$tr" ] && echo 1 || echo 0) in_other_folder=$([ -n "$other" ] && echo 1 || echo 0): arm stopped, no compaction, no turn 2" >> "$STATUS"; return
  fi

  # ---- the arm's tool memory: recorded, never moved
  mem="$proj/memory"
  if [ -d "$mem" ]; then n=$(find "$mem" -type f | wc -l | tr -d ' '); echo "$a memory_existed=1 files=$n" >> "$STATUS"
  else echo "$a memory_existed=0 files=0" >> "$STATUS"; fi
  before=$(python3 "$HERE/boundary.py" count "$tr")
  echo "$a boundaries_before=$before" >> "$STATUS"

  # ---- the compaction call
  rc=$(claude_call "$OUT/$a.cp.jsonl" "$OUT/$a.cp.err" "$pc" "$sid" stream-json)
  echo "$a cp exit=$rc" >> "$STATUS"; timeout_note "$a" cp "$rc"; cprc="$rc"
  set -- $(python3 "$HERE/boundary.py" stream "$OUT/$a.cp.jsonl")
  s_found="${1:-0}"; s_pre="${2:--}"; s_sid="${3:--}"
  set -- $(python3 "$HERE/boundary.py" last "$tr")
  after="${1:-0}"; t_trig="${2:--}"; t_pre="${3:--}"; t_post="${4:--}"
  by="-"
  if [ "$s_found" = 1 ] && [ "$after" -gt "$before" ]; then by=both
  elif [ "$s_found" = 1 ]; then by=stream
  elif [ "$after" -gt "$before" ]; then by=transcript; fi
  pre="$s_pre"; [ "$pre" = "-" ] && pre="$t_pre"
  if [ "$s_sid" = "-" ]; then same="?"; elif [ "$s_sid" = "$sid" ]; then same=1; else same=0; fi
  if [ "$by" = "-" ]; then
    echo "$a compaction_proven=0 by=- pre_tokens=- session_same=$same boundaries_before=$before boundaries_after=$after" >> "$STATUS"
    echo "$a turn2=skipped (compaction not proven)" >> "$STATUS"; return
  fi
  echo "$a compaction_proven=1 by=$by pre_tokens=$pre session_same=$same trigger=$t_trig boundaries_before=$before boundaries_after=$after" >> "$STATUS"
  if [ "$cprc" != 0 ]; then echo "$a turn2=skipped (the compaction call exited $cprc: whatever the proof says, the arm ends - B7)" >> "$STATUS"; return; fi
  if [ "$same" = 0 ]; then echo "$a turn2=skipped (the session id changed at the compaction: turn 2 would not resume the compacted history)" >> "$STATUS"; return; fi

  # ---- turn 2, on the same session
  rc=$(claude_call "$OUT/$a.t2.json" "$OUT/$a.t2.err" "$p2" "$sid" json)
  echo "$a t2 exit=$rc resumed_from=${sid:0:8}" >> "$STATUS"; timeout_note "$a" t2 "$rc"
  snap "$d" "$OUT/snap/$a.t2"
  sid2=$(sid_of "$OUT/$a.t2.json"); iserr=$(err_of "$OUT/$a.t2.json")
  if [ "$rc" != 0 ] || [ "$iserr" != 0 ]; then echo "$a t2 failed (exit=$rc is_error=${iserr:-?})" >> "$STATUS"; return; fi
  echo "$a done t2_session_same=$([ "$sid2" = "$sid" ] && echo 1 || echo 0) boundaries_final=$(python3 "$HERE/boundary.py" count "$tr")" >> "$STATUS"
}

pilot_hint() { case "$1" in q901) echo " - a pilot that has run is not cleared and run again under its name: use the next pilot name, q902";; q902) echo " - use the next pilot name, q903";; q903) echo " - the pilot names are used up: the designer rules";; esac; }   # B9
SEEN=" "
mkdir -p "$OUT/locks"
for a in "$@"; do
  case "$a" in ""|*[!A-Za-z0-9]*) echo "'$a' is not an arm name (skipped)"; continue;; esac
  case "$SEEN" in *" $a "*) echo "$a: named twice - run once (the repeat is skipped)"; continue;; esac
  SEEN="$SEEN$a "
  if ! is_pilot "$a" && ! ls "$OUT"/pilot_ok.* > /dev/null 2>&1; then echo "$a: refused - a counted arm is launched only after a PILOT OK: no marker $OUT/pilot_ok.<pilot> (check_pilot.sh writes it)"; continue; fi    # C4
  if [ ! -d "$(root_of "$a")/$a" ]; then echo "$a: no tree at $(root_of "$a")/$a (skipped)"; continue; fi
  if [ -e "$OUT/$a.t1.json" ]; then echo "$a: $OUT/$a.t1.json exists - refusing to run twice (skipped)$(pilot_hint "$a")"; continue; fi
  if ! mkdir "$OUT/locks/$a" 2> /dev/null; then echo "$a: locked by another launch ($OUT/locks/$a) - refusing to run twice (skipped)$(pilot_hint "$a")"; continue; fi   # mkdir is atomic: two launches cannot both start an arm
  ( one_arm "$a" ) &          # an explicit subshell group, as in 20.11: a bare `fn &` lost the rest of the function after the claude call under bash 3.2
done
wait
echo "all arms finished"
cat "$STATUS"
