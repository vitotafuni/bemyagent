#!/bin/zsh
# env: BMA_SCRATCH, BMA_ACCOUNT. usage: launch.sh <arm>; model from arm prefix h-/s-
P=$BMA_SCRATCH; arm=$1
case $arm in h-*) MODEL=haiku;; s-*) MODEL=sonnet;; esac
PROMPT='Read BEMYAGENT.md in this folder and follow it.'
cd $P/$arm || exit 99
s=$(date +%s)
export BMA_ACCOUNT MODEL PROMPT
zsh -ic 'claude --user "$1" -p "$2" --model "$3" --allowedTools "Read,Write,Edit,Bash,Glob,Grep" --output-format json' _ "$BMA_ACCOUNT" "$PROMPT" "$MODEL" < /dev/null > $P/$arm.json 2> $P/$arm.err
echo $? > $P/$arm.exit
echo $(( $(date +%s) - s )) > $P/$arm.secs
