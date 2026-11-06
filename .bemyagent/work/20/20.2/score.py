"""20.2 metrics (ii) and (iv). Both sides are read from the SAME instrument — the arm's full
transcript — because one side writes docs and the other does not, and scoring documents would
be scoring the protocol's definition rather than its effect."""
import json, pathlib, re, sys
T = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/tasks")
SIDE = {"q52": "P", "q53": "N", "q54": "P", "q55": "N", "q56": "P", "q57": "N"}
AGENT = {"q52": "<agent-id>", "q53": "<agent-id>",
         "q54": "<agent-id>", "q55": "<agent-id>",
         "q56": "<agent-id>", "q57": "<agent-id>"}
# fixed before the arms ran, in 02_tasks.md
DEFECTS = {
 "api() does not check res.ok": re.compile(r"res\.ok|response\.ok|non-2xx|error body.*render|render\(\).*throw", re.I),
 "reload starts a new game vs the overview's claim": re.compile(r"reload (starts|begins|creates) a (new|fresh) game|POSTs? (a )?new game on every (page )?load|survives? a reload.*(not|false|does not)", re.I),
 "session.js is imported by nothing": re.compile(r"session\.js.*(nothing (imports|requires)|not imported|unimported|dead code|no file .*requires)", re.I),
 "untransacted read-modify-write": re.compile(r"untransacted|not transactional|read-modify-write|concurrent move", re.I),
 "Number(undefined) reports 'cell occupied'": re.compile(r"Number\(undefined\)|NaN.*occupied|occupied.*NaN|missing `?cell`?.*occupied", re.I),
 "the 'draws are not displayed' issue is stale": re.compile(r"draws? (are )?not displayed", re.I),
}
W = {"inp": 1.0, "cc": 1.25, "cr": 0.1, "out": 5.0}

def read(agent_id):
    p = T / (agent_id + ".output")
    txt = []; a = dict(inp=0, out=0, cc=0, cr=0)
    for line in p.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        msg = ev.get("message") or {}
        u = msg.get("usage") or ev.get("usage") or {}
        if isinstance(u, dict):
            a["inp"] += u.get("input_tokens") or 0
            a["out"] += u.get("output_tokens") or 0
            a["cc"] += u.get("cache_creation_input_tokens") or 0
            a["cr"] += u.get("cache_read_input_tokens") or 0
        if msg.get("role") != "assistant": continue
        for b in msg.get("content") or []:
            if isinstance(b, dict):
                if b.get("type") == "text": txt.append(b.get("text") or "")
                elif b.get("type") == "tool_use": txt.append(json.dumps(b.get("input") or {}))
    return "\n".join(txt), a

res = {}
for arm, side in SIDE.items():
    blob, a = read(AGENT[arm])
    found = sorted(k for k, rx in DEFECTS.items() if rx.search(blob))
    res[arm] = {"side": side, "defects": found, "n": len(found),
                "weighted": int(sum(W[k] * a[k] for k in a)), "raw": a}
print(json.dumps(res, indent=1))
