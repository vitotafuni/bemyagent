"""20.11 metric (vi) — is each arm a clean control, read from its own transcripts.

Amended before launch (02_tasks.md): a P arm's own CLAUDE.md WILL arrive as an instruction record,
and that record is the positive control that shows this reader can see an injection at all.

Covers the arm's own subagents too: in 20.10, 13 of 25 independent VERIFY agents read the parent,
and a headless P arm may spawn one for section 4's VERIFY.
"""
import json, pathlib, sys
CFG = pathlib.Path("<claude-config>/projects")
R = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad/r2011")
PARENT = "<repo>"
OVERRIDE = "OVERRIDE any default behavior"
SIDE = {"q94": "P", "q95": "P", "q96": "P", "q97": "N", "q98": "N", "q99": "N"}

def norm(p):          # /tmp is a symlink to /private/tmp; a record may carry either spelling
    return "/private" + p if p.startswith("/tmp/") else p

def transcripts(sid):
    main = list(CFG.glob(f"*/{sid}.jsonl"))
    subs = [f for m in main for f in (m.parent / sid).rglob("*.jsonl")] if main else []
    return main, subs

def walk(f, arm_dir):
    instr, outside, parent_calls, override = [], [], [], 0
    for line in f.read_text(errors="replace").splitlines():
        override += line.count(OVERRIDE)
        try: ev = json.loads(line)
        except Exception: continue
        att = ev.get("attachment") or {}
        if ev.get("type") == "attachment" and att.get("type") == "instructions":
            for x in att.get("files") or []:
                p = norm(x.get("path", ""))
                instr.append((x.get("type"), p))
                if not p.startswith(arm_dir + "/"): outside.append(p)
        msg = ev.get("message") or {}
        if ev.get("type") == "assistant" and isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if c.get("type") == "tool_use":
                    s = json.dumps(c.get("input"))
                    if PARENT + "/" in s or s.rstrip('"}').endswith(PARENT):
                        parent_calls.append(s[:160])
    return instr, outside, parent_calls, override

out = {}
for arm in (sys.argv[1:] or sorted(SIDE)):
    j = R / f"{arm}.json"
    if not j.exists(): out[arm] = {"status": "no launcher output"}; continue
    sid = json.loads(j.read_text())["session_id"]
    main, subs = transcripts(sid)
    arm_dir = str(R / arm)
    row = {"side": SIDE[arm], "session": sid, "transcripts": len(main), "subagent_transcripts": len(subs)}
    for label, files in (("main", main), ("subagents", subs)):
        agg = [[], [], [], 0]
        for f in files:
            r = walk(f, arm_dir)
            for i in range(3): agg[i] += r[i]
            agg[3] += r[3]
        row[label] = {"instruction_records": agg[0], "outside_arm_dir": agg[1],
                      "parent_repo_tool_calls": agg[2], "override_header": agg[3]}
    out[arm] = row
print(json.dumps(out, indent=1))
