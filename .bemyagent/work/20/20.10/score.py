"""20.10 — how far outside its own tree every arm of this project actually reached.

Extraction only. The call is made by a reader, not by this file (20.7's pattern).

Attribution never uses a bare arm name - `q4` is a substring of `q46`. Each launch prompt names
a scratchpad directory, and each arm name belongs to exactly one round's `ARMS` dict, parsed out
of that round's own `setup*.py` with `ast` rather than retyped here. 20.9 built its copies inline
and has no setup script, so its six arms are the one hand-written entry.

A parent read is counted ONLY from a `tool_use` input containing the parent repository's absolute
path. Body text cannot serve: an arm's own `00-ai-rules.md` opens with the same heading as the
parent's, so the heading proves nothing about which file was opened.
"""
import os, ast, json, pathlib, re, sys

ROOT = pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4])
SUB = (pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude") / "projects"
       / re.sub(r"[^A-Za-z0-9]", "-", str(ROOT)) / "<session-id>" / "subagents")

P_RULES = str(ROOT / ".bemyagent" / "docs" / "00-ai-rules.md")
P_BMA = str(ROOT / "BEMYAGENT.md")
P_DOCS = {"decisions": str(ROOT / ".bemyagent" / "docs" / "05-decisions-and-issues.md"),
          "plan": str(ROOT / ".bemyagent" / "docs" / "06-implementation-plan.md")}
TTEV = ("01_think", "02_tasks", "03_execute", "04_verify", "PROTOCOL_CHECK")
# The arm directories are not uniform: `r1413/q28`, `r11/w1`, `r18/z1`, `exp/runs/a-1`,
# `gf/arm-1`, `r209/r85x`. An earlier pass matched only `q<N>` and `r<N>x` and silently
# dropped four whole populations - caught by the independent VERIFY, not by this file.
# `r182/q1` and `r182b/q1` are different arms, so the key is the whole relative path.
DIR = re.compile(r"scratchpad/((?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+)(?![A-Za-z0-9_./-])")
# the §4 verifiers are a separate population; the arms themselves were launched over four
# months with four different openings, so the role is read off the VERIFY markers, not off
# a prompt prefix that only the later rounds share
VERIFY = re.compile(r"independent VERIFY|INDEPENDENT verification|VERIFY step|VERIFY pass|"
                    r"[Yy]ou did ?NOT write this code|you did not implement")
# and an arm is told, in one of four openings, that the tree is where it works. Anything matching
# neither is printed as unclassified rather than guessed at.
ARMP = re.compile(r"working directory is|working in the project at|^Work in |^Work only inside|^Your repository|^Repo:")

# ---- arm -> (round, side), from each round's own setup script -----------------------------
SIDE = {}
for p in sorted(ROOT.glob(".bemyagent/work/*/*/setup*.py")):
    rnd = p.parent.name
    for node in ast.walk(ast.parse(p.read_text())):
        if not (isinstance(node, ast.Assign) and
                any(getattr(t, "id", "") == "ARMS" for t in node.targets)):
            continue
        try: v = ast.literal_eval(node.value)
        except ValueError: continue        # 20.8 reassigns ARMS from a comprehension
        pairs = v.items() if isinstance(v, dict) else ((a, "-") for a in v)
        for arm, side in pairs:
            SIDE.setdefault(arm, []).append((rnd, side, p.name))
for a in ("r85x", "r87x", "r89x"): SIDE[a] = [("20.9", "H", "inline")]
for a in ("r91x", "r92x", "r93x"): SIDE[a] = [("20.9", "C", "inline")]
DUP = {a: v for a, v in SIDE.items() if len(v) > 1}

# ---- one pass over every transcript -------------------------------------------------------
agents = []
for p in sorted(SUB.glob("agent-*.jsonl")):
    first, inj, calls = None, False, []
    for line in p.open():
        try: d = json.loads(line)
        except Exception: continue
        if d.get("type") == "attachment":
            if d.get("attachment", {}).get("type") == "instructions": inj = True
            continue
        c = (d.get("message") or {}).get("content")
        bl = c if isinstance(c, list) else []
        if d.get("type") == "user" and first is None:
            first = c if isinstance(c, str) else next(
                (b["text"] for b in bl if isinstance(b, dict) and b.get("type") == "text"), None)
        elif d.get("type") == "assistant":
            for b in bl:
                if isinstance(b, dict) and b.get("type") == "tool_use":
                    calls.append(json.dumps(b.get("input", {})))
    paths = [m.group(1) for m in DIR.finditer(first or "")
             if not m.group(1).startswith(("verify", "exp/tools"))]
    if not paths: continue
    key = paths[0]                      # the first tree the prompt names is the arm's own
    prefix, _, arm = key.rpartition("/")
    if not prefix: continue             # a bare scratchpad/<file>, not an arm tree
    where = SIDE.get(arm, [])
    rnd, side = (where[0][0], where[0][1]) if len(where) == 1 else ("undeclared", "-")
    # the first index at which each path is called, -1 when never
    def at(needle):
        for i, s in enumerate(calls):
            if needle in s: return i
        return -1
    own = -1
    for i, s in enumerate(calls):
        if ".bemyagent/docs/00-ai-rules.md" in s and P_RULES not in s: own = i; break
    agents.append({
        "agent": p.name, "key": key, "prefix": prefix, "arm": arm,
        "round": rnd, "side": side,
        "role": ("verify" if VERIFY.search(first or "")
                 else "arm" if ARMP.search(first or "") else "unclassified"),
        "injected": inj, "calls": len(calls),
        "at_parent_rules": at(P_RULES), "at_own_rules": own, "at_parent_bma": at(P_BMA),
        "parent_docs": {k: at(v) for k, v in P_DOCS.items() if at(v) >= 0},
        "ttev": sorted({k for k in TTEV if any(k in s for s in calls)}),
    })

out = {"arms_from_setup": len(SIDE), "duplicate_arm_names": DUP,
       "transcripts_scanned": len(list(SUB.glob("agent-*.jsonl"))),
       "agents_attributed": len(agents), "agents": agents}
json.dump(out, open(sys.argv[1], "w"), indent=1)

arms = [a for a in agents if a["role"] == "arm"]
print("arms declared in setup scripts :", len(SIDE), "| ambiguous names:", DUP or "none")
print("transcripts scanned            :", out["transcripts_scanned"])
print("arm launches attributed        :", len(arms))
print("other agents scoped to one arm :", len(agents) - len(arms))
print("arm launches with the injection:", sum(a["injected"] for a in arms), "/", len(arms))
print("arm launches that called the parent rules file:",
      sum(a["at_parent_rules"] >= 0 for a in arms))
print("arm launches that called the parent BEMYAGENT.md:",
      sum(a["at_parent_bma"] >= 0 for a in arms))
print("ANY agent that called the parent docs record   :",
      sum(bool(a["parent_docs"]) for a in agents))
