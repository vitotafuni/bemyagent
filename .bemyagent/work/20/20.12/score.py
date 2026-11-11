"""20.12: 20.11's score.py with q100 q101 q102 added; launcher JSON read from each arm's own round dir.

20.11: 20.8's score.py with the six CLI-launched arms added. Their cost is read from the
launcher's own JSON, the only place a headless run reports usage, which also carries the
model id actually served and any permission denial: an arm with a denial is reported as
such, not scored as a reading (01_think.md pre-mortem).

20.8 metrics (ii), (iii) and (iv).

(ii) and (iii) are read from the TREE, not the transcript: an arm's claim that it added no test
is still a claim. (iv) is read from the transcript, which is the only place token usage exists.
The AGENT table is blank at build time — 20.2's ids point at 20.2's transcripts, and carrying
them over scores the wrong arms silently.
"""
import json, pathlib, re, subprocess, sys
T = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/tasks")
S = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad")
TREE = {**{a: S / "r202" for a in ("q52", "q53", "q54", "q55", "q56", "q57")},
        **{a: S / "r203" for a in ("q85", "q86", "q87", "q88", "q89", "q90")},
        **{a: S / "r208" for a in ("q91", "q92", "q93")},
        **{a: S / "r2011" for a in ("q94", "q95", "q96", "q97", "q98", "q99")},
        **{a: S / "r2012" for a in ("q100", "q101", "q102")}}
SIDE = {"q52": "Opus+BMA", "q54": "Opus+BMA", "q56": "Opus+BMA",
        "q53": "Opus-none", "q55": "Opus-none", "q57": "Opus-none",
        "q86": "Opus-none", "q88": "Opus-none", "q90": "Opus-none",
        "q85": "Sonnet+BMA", "q87": "Sonnet+BMA", "q89": "Sonnet+BMA",
        "q91": "Sonnet-none", "q92": "Sonnet-none", "q93": "Sonnet-none",
        "q94": "CLI Sonnet+BMA", "q95": "CLI Sonnet+BMA", "q96": "CLI Sonnet+BMA",
        "q97": "CLI Sonnet-none", "q98": "CLI Sonnet-none", "q99": "CLI Sonnet-none",
        "q100": "CLI Sonnet+BMA/P", "q101": "CLI Sonnet+BMA/P", "q102": "CLI Sonnet+BMA/P"}
AGENT = {"q91": "<agent-id>", "q92": "<agent-id>",
         "q93": "<agent-id>"}   # THIS round only. 20.2/20.3 ids point elsewhere.
W = {"inp": 1.0, "cc": 1.25, "cr": 0.1, "out": 5.0}

def tokens(agent_id):
    a = dict(inp=0, out=0, cc=0, cr=0)
    for line in (T / (agent_id + ".output")).read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        u = (ev.get("message") or {}).get("usage") or ev.get("usage") or {}
        if isinstance(u, dict):
            a["inp"] += u.get("input_tokens") or 0
            a["out"] += u.get("output_tokens") or 0
            a["cc"] += u.get("cache_creation_input_tokens") or 0
            a["cr"] += u.get("cache_read_input_tokens") or 0
    return a

def launcher(arm):
    """(iv) for a CLI arm, plus the two things the pre-mortem said to read before believing it."""
    d = json.loads((TREE[arm] / f"{arm}.json").read_text())
    a = dict(inp=0, out=0, cc=0, cr=0)
    for m in (d.get("modelUsage") or {}).values():
        a["inp"] += m.get("inputTokens") or 0
        a["out"] += m.get("outputTokens") or 0
        a["cc"] += m.get("cacheCreationInputTokens") or 0
        a["cr"] += m.get("cacheReadInputTokens") or 0
    return a, sorted(d.get("modelUsage") or {}), d.get("permission_denials"), d.get("num_turns"), d.get("is_error")

def tree(arm):
    """(ii) test artifacts and (iii) delivery, both from the working tree."""
    d = TREE[arm] / arm
    g = lambda *c: subprocess.run(c, cwd=d, capture_output=True, text=True).stdout
    status = [l for l in g("git", "status", "--porcelain").splitlines()
              if "node_modules" not in l and "package-lock" not in l]
    tests = sorted((d / "test").glob("*.js")) if (d / "test").exists() else []
    cases = sum(len(re.findall(r"^\s*(?:await\s+)?test\(", f.read_text(), re.M)) for f in tests)
    seeded = set(g("git", "ls-tree", "--name-only",
                   g("git", "rev-list", "--max-parents=0", "HEAD").split()[-1],
                   "test/").split())
    store = (d / "server" / "store.js").read_text()
    index = (d / "server" / "index.js").read_text()
    client = (d / "client" / "app.js").read_text()
    html = (d / "client" / "index.html").read_text()
    return {
        "test_files": [f.name for f in tests],
        "test_files_added": [f.name for f in tests if f"test/{f.name}" not in seeded],
        "test_cases": cases,
        "tally_in_store": bool(re.search(r"winner", store) and re.search(r"COUNT\(|count\(", store)),
        "scores_route": bool(re.search(r"/api/(scores|scoreboard|stats|wins)", index + client)),
        "client_markup": bool(re.search(r"scoreboard|score-board|#score", html, re.I)),
        "files_touched": len(status),
    }

res = {}
for arm in (sys.argv[1:] or sorted(SIDE)):   # 20.12: r202 trees were emptied by the tmp cleaner on 11-11
    r = tree(arm)
    if arm in AGENT:
        a = tokens(AGENT[arm])
        r["weighted"] = int(sum(W[k] * a[k] for k in a)); r["raw"] = a
    elif TREE[arm].name in ("r2011", "r2012") and (TREE[arm] / f"{arm}.json").exists():
        a, models, denials, turns, err = launcher(arm)
        r["weighted"] = int(sum(W[k] * a[k] for k in a)); r["raw"] = a
        r["models"], r["permission_denials"], r["turns"], r["is_error"] = models, denials, turns, err
    r["side"] = SIDE[arm]
    res[arm] = r
print(json.dumps(res, indent=1))
