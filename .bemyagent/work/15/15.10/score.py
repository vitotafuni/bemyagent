#!/usr/bin/env python3
"""15.10 scorer. Reads the DISK, never an arm's report.
Criteria fixed in 02_tasks.md before any arm ran. Prints evidence lines for
inspection rather than booleans: a prior round's regex produced a false positive
that only reading the matched line caught."""
import re, sys
from pathlib import Path

EXP = Path("/private/tmp/claude-501/-Users-caporale-me-gitlab-bemyagent/"
           "8aeed20a-f57d-484c-a624-f3b1637843b6/scratchpad/exp10")

EARS     = re.compile(r"\bWHEN\b.*\bSHALL\b", re.I)
CMD      = re.compile(r"(npm\s+test|node\s+--test|node\s+\S+\.js|curl|grep|diff|git\s+\w+)", re.I)
TESTOUT  = re.compile(r"(tests?\s+\d+|pass\s+\d+|fail\s+\d+|\d+\s+pass)", re.I)

def read(p):
    try: return p.read_text(encoding="utf-8", errors="replace")
    except Exception: return ""

for arm in sorted(EXP.iterdir()):
    if not arm.is_dir(): continue
    print("="*78); print(arm.name)
    tasks  = list((arm/".bemyagent"/"work").rglob("02_tasks.md"))
    verify = list((arm/".bemyagent"/"work").rglob("04_verify.md"))
    if not tasks or not verify:
        print("  CEREMONY DID NOT FIRE — tasks:", len(tasks), "verify:", len(verify)); continue

    # 1. FORM — are the Validation criteria in EARS shape?
    t = read(tasks[0])
    ears = [l.strip()[:120] for l in t.splitlines() if EARS.search(l)]
    print(f"  FORM  (WHEN..SHALL in 02_tasks.md): {len(ears)} line(s)")
    for l in ears[:4]: print("     ", l)

    # 2. CITATION — does 04_verify.md quote a command actually run?
    v = read(verify[0])
    cmds = [l.strip()[:120] for l in v.splitlines() if CMD.search(l)]
    outs = [l.strip()[:120] for l in v.splitlines() if TESTOUT.search(l)]
    print(f"  CITATION (command named in 04_verify.md): {len(cmds)}")
    for l in cmds[:4]: print("     ", l)
    print(f"  ...with literal output: {len(outs)}")
    for l in outs[:3]: print("     ", l)

    # 3. COVERAGE — does that command touch THIS change?
    shipped = {"rules.test.js"}
    tests = {p.name for p in (arm/"test").glob("*.js")} if (arm/"test").is_dir() else set()
    added = sorted(tests - shipped)
    idx = read(arm/"server"/"index.js")
    wired = "session" in idx
    print(f"  COVERAGE: test files added = {added or 'NONE'} | index.js wires session.js = {wired}")
    verdict = ("test added covering the change" if added
               else "NO new test - a cited `npm test` exercises only the shipped rules suite")
    print(f"     -> {verdict}")
