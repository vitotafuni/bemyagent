#!/bin/bash
# 21.4 — stdin -> stdout with this machine's values replaced by placeholders, for every output saved into the repo:
#   <scratchpad> <repo> <base> <claude-config> <home>   (the raw path and the tool's dashed project-folder form of each).
# The values come from the environment (local.env), never from this file. Longest value first.
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$HERE/local.env" ] && . "$HERE/local.env"
export M_REPO="${BMA_REPO:-$(cd "$HERE/../../../.." && pwd)}"
export M_BASE="${BMA_BASE:-$(dirname "$M_REPO")}" M_SCRATCH="${BMA_SCRATCH:-}" M_CFG="${CLAUDE_CONFIG_DIR:-}" M_HOME="$HOME"
python3 -c '
import os, re, sys
pairs = [("M_SCRATCH", "<scratchpad>"), ("M_REPO", "<repo>"), ("M_BASE", "<base>"), ("M_CFG", "<claude-config>"), ("M_HOME", "<home>")]
subs = []
for k, ph in pairs:
    v = os.environ.get(k, "").rstrip("/")
    if not v: continue
    forms = {v, re.sub(r"[^A-Za-z0-9]", "-", v)}
    if v.startswith("/private/tmp/"): forms.add(v[len("/private"):])
    subs += [(f, ph) for f in forms]
subs.sort(key=lambda x: -len(x[0]))
for line in sys.stdin:
    for f, ph in subs: line = line.replace(f, ph)
    sys.stdout.write(line)
'
