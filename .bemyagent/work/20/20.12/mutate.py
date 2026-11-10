"""20.12: 20.11's mutate.py with q100 q101 q102 added to TREE and SIDE, nothing else.

20.8 metrics (i) and (v) — do the arm's own tests have teeth, on two mutations.

M1 is 20.2's mutation, unchanged: **a drawn game counts as a win for X.** Catching it needs a
test that covers draw semantics.
M2 is pre-registered in 02_tasks.md before any tree was touched: **X's and O's totals are
swapped.** Catching it needs a test that pins per-player numbers against asymmetric data. A test
that only asserts the scoreboard renders, or that the totals sum correctly, misses both.

Both are applied to the arm's OWN tally code, read out of that arm's own server/store.js. The
per-arm tables below are blank at build time on purpose: 20.3 inherited 20.2's table under renamed
keys and would have mutated one arm's code with another arm's pattern, reporting 'pattern not
found' as n/a on arms whose tests were never exercised.

store.js is restored in a finally block and `git status --porcelain` is compared before and after,
so no arm tree is contaminated by the measurement.
"""
import pathlib, re, subprocess, sys
S = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad")
# which round's scratchpad each arm lives in
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

# The tally query is read out of each arm's OWN server/store.js and the two mutations are derived
# from it by assertion-guarded substitution, so there is no transcription step between the arm's
# code and the edit applied to it. The literal old/new pair per arm is printed to
# 03c_arm_evidence.txt, which is what 20.2 kept a hand-written table for.
SEL = re.compile(r"SELECT\s+winner\s*,\s*COUNT\(\*\)\s+AS\s+(\w+)\s+FROM\s+game\s+"
                 r"WHERE\s+(winner\s+IN\s*\(\s*'X'\s*,\s*'O'\s*\)|winner\s+IS\s+NOT\s+NULL)"
                 r"\s+GROUP\s+BY\s+winner")
DRAW = "CASE WHEN winner = 'draw' THEN 'X' ELSE winner END AS winner"
SWAP = "CASE WHEN winner = 'X' THEN 'O' WHEN winner = 'O' THEN 'X' ELSE winner END AS winner"

def pair(arm, which):
    """(old, new) for this arm, or None if its query is not the shape this transform handles."""
    src = (TREE[arm] / arm / "server" / "store.js").read_text()
    m = SEL.search(src)
    if not m: return None
    q, alias = m.group(0), m.group(1)
    if which == "M1":                       # a draw counts as a win for X
        n = q.replace("SELECT winner,", f"SELECT {DRAW},", 1)
        n = n.replace(m.group(2), "winner IS NOT NULL", 1)
    else:                                   # X and O swapped; the WHERE is left alone
        n = q.replace("SELECT winner,", f"SELECT {SWAP},", 1)
    n = n.replace("GROUP BY winner", "GROUP BY 1", 1)
    assert n != q and f"AS {alias}" in n, arm
    return q, n

M1 = {a: p for a in TREE if (p := pair(a, "M1"))}
M2 = {a: p for a in TREE if (p := pair(a, "M2"))}

def run(arm, table, label):
    d = TREE[arm] / arm
    f = d / "server" / "store.js"
    if arm not in table: return arm, "n/a", "no recorded edit"
    old, new = table[arm]
    src = f.read_text()
    if old not in src: return arm, "n/a", "pattern not found — re-read this arm by hand"
    before = subprocess.run(["git", "status", "--porcelain"], cwd=d,
                            capture_output=True, text=True).stdout
    f.write_text(src.replace(old, new, 1))
    try:
        p = subprocess.run(["npm", "test"], cwd=d, capture_output=True, text=True, timeout=300)
        out = p.stdout + p.stderr
        red = p.returncode != 0
    finally:
        f.write_text(src)
    after = subprocess.run(["git", "status", "--porcelain"], cwd=d,
                           capture_output=True, text=True).stdout
    fails = re.search(r"^. fail (\d+)", out, re.M)
    return arm, ("RED (tests catch it)" if red else "GREEN (tests miss it)"), \
           f"{label} fail={fails.group(1) if fails else '?'} tree-unchanged={before == after}"

which = sys.argv[1] if len(sys.argv) > 1 else "M1"
table = {"M1": M1, "M2": M2}[which]
for a in (sys.argv[2:] or sorted(table)):
    arm, verdict, note = run(a, table, which)
    print(f"{arm}  {SIDE.get(arm, '?'):14} {verdict:24} {note}")
