"""15.4 — does obliging the gate to leave its line make the gate auditable from the repo.

Two instruments, deliberately: the TREE (what a user could audit) and the TRANSCRIPT (what 19.3
measured). The two conditions are compared on the transcript, because the control leaves nothing
on disk by construction and comparing disk to transcript would be comparing instruments.
"""
import json, pathlib, re, subprocess, sys
R = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad/r154")
T = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/tasks")
SIDE = {"q46": "A", "q47": "B", "q48": "A", "q49": "B", "q50": "A", "q51": "B"}
AGENT = {"q46": "<agent-id>", "q47": "<agent-id>",
         "q48": "<agent-id>", "q49": "<agent-id>",
         "q50": "<agent-id>", "q51": "<agent-id>"}
PC_LINE = re.compile(r"^[ \t>*_`-]*PROTOCOL_CHECK[^\n]*", re.M)
GOVERNED = re.compile(r"^\.bemyagent/(docs|work)/")
EXEMPT = re.compile(r"^\.bemyagent/work/[^/]+/[^/]+/0[1-4]_[A-Za-z]+\.(?:md|log)$"
                    r"|^\.bemyagent/work/[^/]+/micro\.log$")

def transcript_lines(agent_id):
    """lines the ARM produced; tool results excluded — the string lives in 00-ai-rules.md"""
    p = T / (agent_id + ".output")
    if not p.exists(): return None
    mine = []
    for line in p.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        msg = ev.get("message") or {}
        if msg.get("role") != "assistant": continue
        for b in msg.get("content") or []:
            if not isinstance(b, dict): continue
            if b.get("type") == "text":
                mine += PC_LINE.findall(b.get("text") or "")
            elif b.get("type") == "tool_use":
                mine += PC_LINE.findall(json.dumps(b.get("input") or {}))
    return mine

def governed_files(d):
    base = subprocess.run(["git", "log", "--format=%H", "-1", "--author=h", "--grep=code map"],
                          cwd=d, capture_output=True, text=True).stdout.strip()
    out = subprocess.run(["git", "diff", "--name-only", base], cwd=d,
                         capture_output=True, text=True).stdout.split()
    for l in subprocess.run(["git", "status", "--porcelain"], cwd=d,
                            capture_output=True, text=True).stdout.splitlines():
        if l[:2] != "??": continue
        f = l[3:]
        if f.endswith("/"):
            out += [str(x.relative_to(d)) for x in (d / f).rglob("*") if x.is_file()]
        else: out.append(f)
    return sorted({f for f in set(out)
                   if GOVERNED.match(f) and not EXEMPT.match(f) and not f.endswith("/")})

def named(files, blob):
    return [f for f in files
            if (lambda b: bool(b) and (b in blob or f in blob))(f.split("/")[-1])]

res = {}
ONLY = set(sys.argv[1:])
for arm, side in SIDE.items():
    if ONLY and arm not in ONLY: continue
    d = R / arm
    if not d.exists(): continue
    # (i) the tree: every PROTOCOL_CHECK line that survives in a tracked-ish file
    on_disk, where = [], {}
    for p in d.rglob("*"):
        if not p.is_file() or "node_modules" in str(p) or "/.git/" in str(p): continue
        if p.name == "00-ai-rules.md" or p.name == "BEMYAGENT.md": continue  # protocol-owned
        hits = PC_LINE.findall(p.read_text(errors="replace"))
        if hits:
            on_disk += hits
            where[str(p.relative_to(d))] = len(hits)
    files = governed_files(d)
    tr = transcript_lines(AGENT.get(arm, ""))
    tests = subprocess.run(["npm", "test"], cwd=d, capture_output=True, text=True)
    res[arm] = {
      "side": side,
      "governed_files": files,
      # (i) disk
      "disk_lines": len(on_disk), "disk_where": where,
      "disk_named": named(files, "\n".join(on_disk)),
      # (ii) transcript — the comparison
      "transcript_lines": None if tr is None else len(tr),
      "transcript_named": None if tr is None else named(files, "\n".join(tr)),
      # (iv) delivery
      "tests": re.findall(r"^. (?:pass|fail) \d+", tests.stdout + tests.stderr, re.M),
      "scoreboard": bool(re.search(r"score", (d/"client"/"index.html").read_text(), re.I)),
      # a confound to check before comparing coverage: an arm may install the §1 directive
      # block into CLAUDE.md itself, which changes what the tool loads
      "claude_md_directive": "PROTOCOL_CHECK" in (d / "CLAUDE.md").read_text()
                             if (d / "CLAUDE.md").exists() else None,
      # (v) the reasons, for reading
      "reasons": [l.strip()[:200] for l in (tr or on_disk)],
    }
print(json.dumps(res, indent=1))
