"""20.10 — the reader. score.py extracts; this file arranges and the call is made in 04_verify.md.

Writes 03b_census.txt (every arm launch) and 03c_direction.txt (per round: what its setup
mutates, which way the defect pushes its verdict, and F4/F5/F6).
"""
import os, ast, json, pathlib

ROOT = pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4])
W = ROOT / ".bemyagent" / "work" / "20" / "20.10"
d = json.load(open(W / "03d_score_output.json"))
ag = d["agents"]

SIDE = {}
for p in sorted(ROOT.glob(".bemyagent/work/*/*/setup*.py")):
    for node in ast.walk(ast.parse(p.read_text())):
        if not (isinstance(node, ast.Assign) and
                any(getattr(t, "id", "") == "ARMS" for t in node.targets)):
            continue
        try: v = ast.literal_eval(node.value)
        except ValueError: continue
        pairs = v.items() if isinstance(v, dict) else ((a, "-") for a in v)
        for arm, side in pairs: SIDE.setdefault(p.parent.name, {})[arm] = side
SIDE["20.9"] = {"r85x": "H", "r87x": "H", "r89x": "H",
                "r91x": "C", "r92x": "C", "r93x": "C"}

# What each round's setup mutates, derived rather than asserted: the ANCHOR its `treat()` is
# pinned to, counted in BEMYAGENT.md and in the rules mirror AS THEY STOOD at that round's own
# commit. 19.2a's `treat()` returns the text untouched where the anchor is absent, so the call
# appearing in the source proves nothing about the file changing - and 20.2's setup, copied from
# a clause round, carries a dead `treat()` branch for a side no arm has.
import re, subprocess

def at_commit(commit, path):
    r = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""

def round_commit(rnd):
    r = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H", "--",
                        f".bemyagent/work/{rnd.split('.')[0]}/{rnd}/"],
                       cwd=ROOT, capture_output=True, text=True)
    hs = r.stdout.split()
    return hs[-1] if hs else "HEAD"

MUT = {}
for rnd, arms in SIDE.items():
    srcs = list((ROOT / ".bemyagent" / "work" / rnd.split(".")[0] / rnd).glob("setup*.py"))
    txt = "\n".join(s.read_text() for s in srcs)
    sides = set(arms.values())
    if sides & {"N", "C"}: MUT[rnd] = "no-protocol control present"; continue
    if not txt: MUT[rnd] = "no setup script"; continue
    anchors = [ast.literal_eval(m.group(1)) for m in
               re.finditer(r"^ANCHOR = (\(.*?\)|\".*?\")\n", txt, re.S | re.M)]
    # the arms were built from the tree as it stood BEFORE the round landed: 19.5's own commit is
    # the one that replaced its anchor, so reading at the commit itself finds the anchor gone
    c = round_commit(rnd) + "^"
    mirror = ('docs" / "00-ai-rules.md").write_text(treat(' in txt and
              any(at_commit(c, ".bemyagent/docs/00-ai-rules.md").count(a) == 1 for a in anchors))
    bma = ('"BEMYAGENT.md").write_text(treat(' in txt and
           any(at_commit(c, "BEMYAGENT.md").count(a) == 1 for a in anchors))
    treated = ("B" in sides or "G" in sides) and (mirror or bma)
    MUT[rnd] = ("mirror+BEMYAGENT.md mutated" if treated and mirror else
                "BEMYAGENT.md only" if treated else "no protocol delta")

def rkey(r):
    head = r.rstrip("ab")
    return [int(x) for x in head.split(".")] + [r]

L = []
w = L.append
w("20.10 — CENSUS: every arm launch, and whether it called a protocol file in the PARENT repo")
w("")
w("A read is counted ONLY from the arm's own tool_use input containing")
w("<repo>/.bemyagent/docs/00-ai-rules.md — never from body text,")
w("which the arm's own copy shares word for word. BMA = called the parent BEMYAGENT.md.")
w("")
w(f"{'round':7}{'side':11}{'arm':6}{'runs':5}{'parent':8}{'own copy':10}ceremony on disk")
tot = read = 0
holes = []
for rnd in sorted(SIDE, key=rkey):
    for arm, side in SIDE[rnd].items():
        recs = [a for a in ag if a["arm"] == arm and a["role"] == "arm"]
        keys = sorted({a["key"] for a in recs})
        if not recs:
            holes.append(f"{rnd}/{arm}")
            w(f"{rnd:7}{side:11}{arm:6}{'0':5}{'HOLE':8}")
            continue
        r = sum(x["at_parent_rules"] >= 0 for x in recs)
        own = sum(x["at_own_rules"] >= 0 for x in recs)
        bma = sum(x["at_parent_bma"] >= 0 for x in recs)
        tt = sorted({t for x in recs for t in x["ttev"]})
        tot += len(recs); read += r
        w(f"{rnd:7}{side:11}{arm:6}{len(recs):<5}"
          f"{('READ' + (' BMA' if bma else '')) if r else ('BMA' if bma else '-'):8}"
          f"{('yes' if own else 'no'):10}{','.join(tt) if tt else 'NONE'}"
          f"{'   ' + ' '.join(keys) if len(keys) > 1 else ''}")
w("")
w(f"arm launches {tot}   parent reads {read}   holes {len(holes)}: "
  f"{', '.join(holes) if holes else 'none'}")
und = sorted({a["key"] for a in ag if a["role"] == "arm" and a["round"] == "undeclared"})
w("")
w("arm trees named by no setup script's ARMS dict - experiments that pre-date the setup-script")
w("convention. Counted, not attributed:")
for k in und:
    recs = [a for a in ag if a["key"] == k and a["role"] == "arm"]
    r = sum(x["at_parent_rules"] >= 0 for x in recs)
    w(f"  {k:14}{len(recs)} launch(es)  {'READ' if r else '-'}  "
      f"parent@{[x['at_parent_rules'] for x in recs]}")
unc = [a for a in ag if a["role"] == "unclassified"]
w(f"unclassified agents (prompt matches neither an arm opening nor a VERIFY opening): {len(unc)}")
for a in unc: w(f"  {a['round']:7}{a['arm']:6}{a['agent'][6:14]}  parent@{a['at_parent_rules']}")
(W / "03b_census.txt").write_text("\n".join(L) + "\n")

D = []
w = D.append
w("20.10 — DIRECTION: what each round mutates, and which way a parent read pushes its verdict")
w("")
w(f"{'round':7}{'what the setup mutates':32}{'arms':6}{'read':6}direction of the defect")
DIRN = {
 "mirror+BEMYAGENT.md mutated":
   "B read the clause-free A text: the manipulation is contradicted in context",
 "BEMYAGENT.md only":
   "the mirror carries no clause either way: the manipulation survives",
 "no-protocol control present":
   "the control read the protocol in full: benefit understated, harm inflated",
 "no protocol delta": "no clause to defeat; both sides equally exposed",
 "no setup script": "copies of an earlier round's trees; inherits that round's exposure",
}
for rnd in sorted(SIDE, key=rkey):
    recs = [a for a in ag if a["round"] == rnd and a["role"] == "arm"]
    r = sum(x["at_parent_rules"] >= 0 for x in recs)
    w(f"{rnd:7}{MUT[rnd]:32}{len(recs):<6}{r:<6}{DIRN[MUT[rnd]] if r else 'not exposed'}")
w("")
w("--- F4  order of the parent read -----------------------------------------------------------")
ex = [a for a in ag if a["role"] == "arm" and a["at_parent_rules"] >= 0]
w(f"  exposed arm launches: {len(ex)}")
w(f"  parent read at the arm's 1st or 2nd tool call: {sum(a['at_parent_rules'] <= 1 for a in ex)}")
w(f"  parent read BEFORE the arm's own copy        : "
  f"{sum(a['at_own_rules'] >= 0 and a['at_parent_rules'] < a['at_own_rules'] for a in ex)}"
  f" of {sum(a['at_own_rules'] >= 0 for a in ex)} that read their own copy at all")
w(f"  latest parent read, by call index            : {max(a['at_parent_rules'] for a in ex)}")
w("")
w("--- F5  the independent VERIFY agents ------------------------------------------------------")
v = [a for a in ag if a["role"] == "verify"]
w(f"  VERIFY agents identified: {len(v)}   that called the parent rules file: "
  f"{sum(a['at_parent_rules'] >= 0 for a in v)}")
for a in v:
    if a["at_parent_rules"] >= 0:
        w(f"  {a['round']:7}{a['side']:11}{a['arm']:6} parent@call {a['at_parent_rules']}")
w("")
w("--- F6  the parent's own record ------------------------------------------------------------")
w(f"  agents of any role that called 05-decisions-and-issues.md or 06-implementation-plan.md: "
  f"{sum(bool(a['parent_docs']) for a in ag)} of {len(ag)}")
(W / "03c_direction.txt").write_text("\n".join(D) + "\n")
print("\n".join(D))
print()
print("\n".join(L[-6:]))
