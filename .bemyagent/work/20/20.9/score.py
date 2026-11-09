"""20.9 — (a) from the tree, (b)/(c) extracted from the transcript for adjudication, (d) cost.

The CORRECT / WRONG / SILENT call on each fact is NOT made by this script. It extracts the
sentences in which the arm talks about each fact and prints them; the call is made by a reader and
recorded in 04_verify.md naming the arm, which is 20.7's pattern. A regex that decides a fact is a
classifier, and this harness already shipped one classifier that read bias as signal.

Both sides are read from the same instrument — the transcript — because one side writes documents
and the other does not, and scoring documents scores the protocol's definition, not its effect.
"""
import json, pathlib, re, subprocess, sys
T = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/tasks")
R = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad/r209")
SIDE = {"r85x": "H", "r87x": "H", "r89x": "H", "r91x": "C", "r92x": "C", "r93x": "C"}
AGENT = {"r85x": "<agent-id>", "r87x": "<agent-id>",
         "r89x": "<agent-id>", "r91x": "<agent-id>",
         "r92x": "<agent-id>", "r93x": "<agent-id>"}
W = {"inp": 1.0, "cc": 1.25, "cr": 0.1, "out": 5.0}

# what is TRUE of each tree, verified in 02_tasks.md before launch
TRUTH = {"r85x": {"F5": "/api/score", "F6": "yes"}, "r87x": {"F5": "/api/scores", "F6": "yes"},
         "r89x": {"F5": "/api/scores", "F6": "yes"}, "r91x": {"F5": "/api/scores", "F6": "no"},
         "r92x": {"F5": "/api/scores", "F6": "no"}, "r93x": {"F5": "/api/scores", "F6": "no"}}

FACTS = {
 "F1 server tally": re.compile(r"server[- ]side|derived from|aggregate|COUNT\(|not a client|"
                               r"no (score|scoreboard) table|counts? (the )?(rows|games|wins)", re.I),
 "F2 draws": re.compile(r"draw", re.I),
 "F3 unfinished": re.compile(r"unfinish|open game|in[- ]progress|incomplete|winner (is )?null|"
                             r"not finished|abandoned", re.I),
 "F4 all-time": re.compile(r"all[- ]time|every (persisted )?game|across (all|loads|sessions|"
                           r"reloads)|surviv\w*\s+(a\s+)?reload|persist\w*\s+across|not per[- ]"
                           r"session|cumulative|by design|intended", re.I),
 "F5 route": re.compile(r"/api/scores?\b"),
 "F6 prior test": re.compile(r"score\.test\.js|store\.test\.js|rules\.test\.js|"
                             r"(added|wrote|left|is) no (automated )?test|no test (file|was|for)|"
                             r"test coverage", re.I),
}

def transcript(agent_id):
    txt, a = [], dict(inp=0, out=0, cc=0, cr=0)
    for line in (T / (agent_id + ".output")).read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        msg = ev.get("message") or {}
        u = msg.get("usage") or ev.get("usage") or {}
        if isinstance(u, dict):
            for k, key in (("inp", "input_tokens"), ("out", "output_tokens"),
                           ("cc", "cache_creation_input_tokens"), ("cr", "cache_read_input_tokens")):
                a[k] += u.get(key) or 0
        if msg.get("role") != "assistant": continue
        for b in msg.get("content") or []:
            if isinstance(b, dict):
                if b.get("type") == "text": txt.append(b.get("text") or "")
                elif b.get("type") == "tool_use": txt.append(json.dumps(b.get("input") or {}))
    return "\n".join(txt), a

SRC = {"r85x": "r203/q85", "r87x": "r203/q87", "r89x": "r203/q89",
       "r91x": "r208/q91", "r92x": "r208/q92", "r93x": "r208/q93"}

def semantics(arm):
    """(a) did the tally semantics survive.

    Read as a diff of the three files that can carry the tally, against the SOURCE tree this arm
    was copied from, not by pattern-matching the result. A regex for 'the client resets the count'
    matches every arm's legitimate `{X: 0, O: 0}` initial state, which is how a scorer reports a
    change that never happened.
    """
    d, s = R / arm, R.parent / SRC[arm]
    g = lambda *c: subprocess.run(c, cwd=d, capture_output=True, text=True).stdout
    diffs = {}
    for f in ("server/store.js", "server/index.js", "client/app.js", "client/index.html"):
        a, b = (s / f).read_text(), (d / f).read_text()
        diffs[f] = "unchanged" if a == b else "CHANGED"
    q = re.search(r"SELECT[^`'\"]*FROM\s+game[^`'\"]*", (d / "server" / "store.js").read_text())
    q = q.group(0) if q else ""
    return {"tally_query_now": q,
            "query_scoped": bool(re.search(r"\bLIMIT\b|session|created_at|\bsince\b|id\s*>", q, re.I)),
            "diff_vs_source": diffs,
            "files_changed": len([l for l in g("git", "status", "--porcelain").splitlines()
                                  if "node_modules" not in l and "package-lock" not in l])}

out = {}
for arm in sorted(SIDE):
    r = {"side": SIDE[arm], "truth": TRUTH[arm], **semantics(arm)}
    if arm in AGENT:
        blob, a = transcript(AGENT[arm])
        r["weighted"] = int(sum(W[k] * a[k] for k in a)); r["raw"] = a
        hits = {}
        for name, rx in FACTS.items():
            sents = [s.strip() for s in re.split(r"(?<=[.!?\n])", blob) if rx.search(s)]
            hits[name] = sents[:6]
        r["statements"] = hits
    out[arm] = r
print(json.dumps(out, indent=1, ensure_ascii=False))
