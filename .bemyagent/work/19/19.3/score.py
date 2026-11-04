"""19.3 — Write Gate compliance.
Occasions come from the arm's TREE (git), because which file a shell command writes is not
decidable by pattern — see 03_execute.log. Emissions come from the transcript, counting only
text the arm itself produced. Coverage matches the targets an emission names against the
governed files the arm actually changed.
"""
import json, pathlib, re, subprocess, sys
T = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/tasks")
R = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad/r1413")
ARMS = {"q28": "<agent-id>", "q29": "<agent-id>", "q30": "<agent-id>",
        "q31": "<agent-id>", "q32": "<agent-id>", "q33": "<agent-id>"}
PC_LINE = re.compile(r"^[ \t>*_`-]*PROTOCOL_CHECK[^\n]*", re.M)
GOVERNED = re.compile(r"^\.bemyagent/(docs|work)/")
EXEMPT = re.compile(r"^\.bemyagent/work/[^/]+/[^/]+/0[1-4]_[A-Za-z]+\.(?:md|log)$"
                    r"|^\.bemyagent/work/[^/]+/micro\.log$")

def emissions(agent_id):
    p = T / (agent_id + ".output")
    mine, theirs = [], 0
    for line in p.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        msg = ev.get("message") or {}
        content = msg.get("content")
        if not isinstance(content, list): continue
        if msg.get("role") != "assistant":
            for b in content:
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content"); s = c if isinstance(c, str) else json.dumps(c)
                    theirs += len(PC_LINE.findall(s or ""))
            continue
        for b in content:
            if not isinstance(b, dict): continue
            if b.get("type") == "text":
                mine += PC_LINE.findall(b.get("text") or "")
            elif b.get("type") == "tool_use":
                mine += PC_LINE.findall(json.dumps(b.get("input") or {}))
    return mine, theirs

def governed_files(arm):
    d = R / arm
    base = subprocess.run(["git", "log", "--format=%H", "-1", "--author=h", "--grep=code map"],
                          cwd=d, capture_output=True, text=True).stdout.strip()
    out = subprocess.run(["git", "diff", "--name-only", base], cwd=d,
                         capture_output=True, text=True).stdout.split()
    # an untracked DIRECTORY is listed with a trailing slash: expand it to its files,
    # otherwise a directory counts as a write and its empty basename matches any text
    for l in subprocess.run(["git", "status", "--porcelain"], cwd=d,
                            capture_output=True, text=True).stdout.splitlines():
        if l[:2] != "??": continue
        f = l[3:]
        if f.endswith("/"):
            out += [str(x.relative_to(d)) for x in (d / f).rglob("*") if x.is_file()]
        else:
            out.append(f)
    return sorted({f for f in set(out)
                   if GOVERNED.match(f) and not EXEMPT.match(f) and not f.endswith("/")})

print(f"{'arm':6}{'emitted':9}{'(in results)':14}{'governed files':16}{'named':8}{'coverage'}")
detail = {}
for arm, aid in ARMS.items():
    mine, theirs = emissions(aid)
    files = governed_files(arm)
    blob = "\n".join(mine)
    named = [f for f in files
             if (lambda b: bool(b) and (b in blob or f in blob))(f.split("/")[-1])]
    cov = f"{len(named)}/{len(files)}" if files else "n/a"
    print(f"{arm:6}{len(mine):<9}{theirs:<14}{len(files):<16}{len(named):<8}{cov}")
    detail[arm] = {"emitted": mine, "governed": files, "named": named, "in_results": theirs}
print()
for arm, d in detail.items():
    print(f"--- {arm} governed files changed ---")
    for f in d["governed"]:
        print(("  [named] " if f in d["named"] else "  [     ] ") + f)
print()
for arm, d in detail.items():
    print(f"--- {arm} emissions ---")
    for e in d["emitted"]: print("   ", e.strip()[:170])
