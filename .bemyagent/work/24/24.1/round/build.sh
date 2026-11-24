#!/bin/zsh
# env: BMA_SCRATCH (round folder), BMA_SEED (seed tree), BMA_REPO (repo base: src/ and bemyagent-task-24.1/ live under it)
set -eu
P=$BMA_SCRATCH
BMA_RELEASED=$BMA_REPO/src/BEMYAGENT.md
BMA_CAND_CHECKOUT=$BMA_REPO/bemyagent-task-24.1
BMA_CAND=$BMA_CAND_CHECKOUT/BEMYAGENT.md
extract(){ awk '/^````markdown$/{f=1;next} /^````$/{if(f)exit} f' "$1"; }
extract "$BMA_RELEASED" > $P/rel-rules.md
extract "$BMA_CAND" > $P/cand-rules.md
cmp $P/rel-rules.md $BMA_SEED/.bemyagent/docs/00-ai-rules.md && echo "seed rules == released embedded: OK"
cmp $P/cand-rules.md $BMA_CAND_CHECKOUT/.bemyagent/docs/00-ai-rules.md && echo "cand rules == checkout rules: OK"
head -1 $P/cand-rules.md
SEEDRULES=$BMA_SEED/.bemyagent/docs/00-ai-rules.md
mk(){ # arm cell
  local arm=$1 cell=$2 d=$P/$1 rf bs=$BMA_CAND
  rm -rf $d; mkdir -p $d
  rsync -a --exclude .git --exclude BEMYAGENT.md $BMA_SEED/ $d/
  rf=$d/.bemyagent/docs/00-ai-rules.md
  case $cell in
    older)    sed '1s/3\.6\.0/3.7.0/' $P/cand-rules.md > $rf;;
    numeric)  sed '1s/3\.6\.0/3.10.0/' $P/cand-rules.md > $rf;;
    same)     cp $P/cand-rules.md $rf;;
    edited)   cp $P/cand-rules.md $rf; printf '%s\n' '- Team rule: every public function has a docstring.' >> $rf;;
    newer)    { echo '# AI Rules & TTEV Workflow — BEMYAGENT 3.5.0'; tail -n +2 $SEEDRULES; } > $rf;;
    unstamped|control) cp $SEEDRULES $rf;;
  esac
  [ $cell = control ] && bs=$BMA_RELEASED
  ( cd $d && git init -q && git config core.excludesFile /dev/null && git config user.email a@b.c && git config user.name arm \
    && git add -A && git commit -q -m seed && cp $bs BEMYAGENT.md \
    && [ "$(git status --short)" = "?? BEMYAGENT.md" ] ) || { echo "ASSERT FAIL $arm"; exit 1; }
}
for c in older numeric same edited newer unstamped; do
  for i in 1 2 3; do mk h-$c-$i $c; done
  for i in 1 2; do mk s-$c-$i $c; done
done
mk h-control-1 control; mk s-control-1 control
diff $P/cand-rules.md $P/h-older-1/.bemyagent/docs/00-ai-rules.md | grep -c '^[<>]' | sed 's/^/older diff lines (expect 2): /' || true
diff $P/cand-rules.md $P/h-numeric-1/.bemyagent/docs/00-ai-rules.md | grep -c '^[<>]' | sed 's/^/numeric diff lines (expect 2): /' || true
echo built
