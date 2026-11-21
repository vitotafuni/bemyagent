#!/bin/sh
# usage: run-arm.sh <arm> <model> <yes|none>   env: BMA_SCRATCH, BMA_REPO, BMA_ACCOUNT
arm=$1; model=$2; pr=$3
P=$BMA_SCRATCH
"$(dirname "$0")/build.sh" "$arm" || exit 1
cd "$P/$arm" || exit 1
for turn in 1 2; do
  if [ $turn = 1 ]; then prompt=$(cat "$P/prompt-$pr.txt"); else prompt="Reply with exactly this line and nothing else: ROUND-OK-$arm"; fi
  s=$(date +%s)
  # "claude" is a shell function of the interactive zsh profile that implements --user
  zsh -ic 'claude --user "$1" -p "$2" --model "$3" --allowedTools "Read,Write,Edit,Bash,Glob,Grep" --output-format json' _ "$BMA_ACCOUNT" "$prompt" "$model" < /dev/null > "$P/$arm.turn$turn.json" 2> "$P/$arm.turn$turn.err"
  echo $? > "$P/$arm.turn$turn.exit"
  echo $(( $(date +%s) - s )) > "$P/$arm.turn$turn.secs"
done
