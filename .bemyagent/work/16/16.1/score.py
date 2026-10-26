#!/usr/bin/env python3
"""16.1 scorer. Reads the DISK, never an arm's report.
Criteria fixed in 02_tasks.md before any arm ran. Prints matched lines rather
than booleans: a prior round's regex produced a false positive that only reading
the matched line caught."""
import re
from pathlib import Path

EXP = Path("/private/tmp/claude-501/-Users-caporale-me-gitlab-bemyagent/"
           "8aeed20a-f57d-484c-a624-f3b1637843b6/scratchpad/exp16")

# turn 2 = "drop the count field from /api/online, and no new test for it"
T2 = re.compile(r"(count)", re.I)
T2b = re.compile(r"(drop|remov|no longer|just the array|array only|senza|togli)", re.I)

def read(p):
    try: return p.read_text(encoding="utf-8", errors="replace")
    except Exception: return ""

def hits(files, rx, rx2, limit=3):
    out = []
    for f in files:
        for i, ln in enumerate(read(f).splitlines(), 1):
            if rx.search(ln) and rx2.search(ln):
                out.append((f, i, ln.strip()[:130]))
    return out

for arm in sorted(EXP.iterdir()):
    if not arm.is_dir(): continue
    print("=" * 78); print(arm.name)
    bma = arm / ".bemyagent"
    logs = sorted((bma / "log").rglob("*")) if (bma / "log").is_dir() else []
    logs = [p for p in logs if p.is_file()]

    # --- WRITTEN: a log file exists and has an entry for turn 1
    print(f"  WRITTEN: {len(logs)} log file(s) {[p.name for p in logs] or ''}")
    for p in logs:
        body = read(p)
        print(f"     {p.name}: {len(body.splitlines())} lines, {len(body)} bytes")

    # --- TURN 2: does the log carry the correction?
    h = hits(logs, T2, T2b)
    print(f"  TURN 2 in log: {len(h)}")
    for f, i, ln in h[:3]: print(f"     {f.name}:{i}  {ln}")

    # --- NEW / DUPLICATION: is the correction also in the distilled files?
    distilled = []
    for sub in ("docs", "work"):
        d = bma / sub
        if d.is_dir(): distilled += [p for p in d.rglob("*.md") if p.is_file()]
        if d.is_dir(): distilled += [p for p in d.rglob("*.log") if p.is_file()]
    distilled = [p for p in distilled if p.name != "00-ai-rules.md"]
    h2 = hits(distilled, T2, T2b)
    print(f"  TURN 2 in distilled files (docs/ + work/): {len(h2)}")
    for f, i, ln in h2[:4]:
        print(f"     {f.relative_to(bma)}:{i}  {ln}")
    verdict = ("log ONLY -> NEW" if h and not h2 else
               "both -> DUPLICATION" if h and h2 else
               "distilled only -> log adds nothing" if h2 else
               "nowhere -> the correction left no durable trace at all")
    print(f"     -> {verdict}")
