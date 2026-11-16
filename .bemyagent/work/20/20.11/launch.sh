#!/bin/bash
# 20.11 — the round's one novel instrument: an arm launched by the CLI from inside its own
# directory instead of by the Agent tool, so that no parent-project instruction is injected.
#
# Three things in here are load-bearing and each was a failure in testing:
#   * `command claude` — the user's shell defines a `claude` function that hands a headless run a
#     fresh `mktemp -d` config dir, which has no auth and no transcript path.
#   * CLAUDE_CONFIG_DIR pinned — the transcript must land somewhere the certificate can read it.
#   * --allowedTools — in `-p` mode an unpermitted call is denied, not queued, and an arm that
#     cannot run `npm test` floors every metric for a reason that is not the protocol.
set -u
S="${BMA_SCRATCH:?set BMA_SCRATCH to the scratch directory of this round}"
R="$S/r2011"
PROMPT_FILE="$(dirname "$0")/prompt.txt"
export CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

for a in "$@"; do
  d="$R/$a"
  p=$(sed "s|<ARM_DIR>|$d|" "$PROMPT_FILE")
  (
    cd "$d" || exit 1
    command claude -p "$p" --model sonnet --output-format json \
      --allowedTools Read Write Edit Bash Glob Grep > "$R/$a.json" 2> "$R/$a.err"
    echo "$a exit=$?" >> "$R/launch.status"
  ) &
done
wait
echo "all arms finished"
cat "$R/launch.status"
