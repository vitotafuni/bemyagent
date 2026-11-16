"""20.12: 20.11's certificate with q100 q101 q102 added, each arm read from its own round dir, plus
metric (vii): the first user message of each arm's main transcript, so the prompt that arrived is
read rather than assumed (20.11's P side was sent the wrong one).

20.11 metric (vi) — is each arm a clean control, read from its own transcripts.

Amended before launch (02_tasks.md): a P arm's own CLAUDE.md WILL arrive as an instruction record,
and that record is the positive control that shows this reader can see an injection at all.

Covers the arm's own subagents too: in 20.10, 13 of 25 independent VERIFY agents read the parent,
and a headless P arm may spawn one for section 4's VERIFY.
"""
import os, json, pathlib, sys
CFG = pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude") / "projects"
S = pathlib.Path(os.environ["BMA_SCRATCH"])
PARENT = str(pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4]))
OVERRIDE = "OVERRIDE any default behavior"
SIDE = {"q97": "N", "q98": "N", "q99": "N", "q100": "P", "q101": "P", "q102": "P"}
R_OF = {a: S / ("r2012" if SIDE[a] == "P" else "r2011") for a in SIDE}
TREATMENT = "Read BEMYAGENT.md in the repository root and follow it."

def norm(p):          # /tmp is a symlink to /private/tmp; a record may carry either spelling
    return "/private" + p if p.startswith("/tmp/") else p

def transcripts(sid):
    main = list(CFG.glob(f"*/{sid}.jsonl"))
    subs = [f for m in main for f in (m.parent / sid).rglob("*.jsonl")] if main else []
    return main, subs

def first_prompt(f):
    for line in f.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        if ev.get("type") == "user":
            m = (ev.get("message") or {}).get("content")
            return m if isinstance(m, str) else " ".join(x.get("text", "") for x in m if isinstance(x, dict))
    return ""

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
    R = R_OF[arm]
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
    fp = first_prompt(main[0]) if main else ""
    row["treatment_sentence_in_prompt"] = TREATMENT in fp
    row["prompt_has_arm_dir"] = arm_dir in fp
    out[arm] = row
print(json.dumps(out, indent=1))
