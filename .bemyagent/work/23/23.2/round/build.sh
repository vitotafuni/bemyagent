#!/bin/sh
# usage: build.sh <arm>   env: BMA_SCRATCH, BMA_REPO (repo base folder holding src/ and the task checkout)
set -e
arm=$1
t=$BMA_SCRATCH/$arm
rm -rf "$t"; mkdir -p "$t"
(cd "$BMA_REPO/src/harness/fixture" && tar cf - --exclude=node_modules .) | (cd "$t" && tar xf -)
cp "$BMA_REPO/bemyagent-task-23.2/BEMYAGENT.md" "$t/BEMYAGENT.md"
cd "$t"
git init -q
git config core.excludesFile /dev/null
git config user.email round@example.invalid; git config user.name round
git add -A; git commit -q -m fixture
[ ! -e .claude ] && [ ! -e .bemyagent ] && [ -z "$(git status --short)" ] || { echo "precondition failed" >&2; exit 1; }
