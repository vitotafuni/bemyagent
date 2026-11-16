"""20.11 — M1 and M2 for the two arms whose tally query mutate.py's regex does not match.

q95 counts with no WHERE; q99 writes `COUNT(*) n` with no AS. The transforms are 20.8's, applied by
hand to each arm's own query and printed literally, with the same discipline as mutate.py: store.js
restored in a finally block and `git status --porcelain` compared before and after. q98 has no
server tally at all — its count lives in localStorage — so there is nothing on the server to mutate.
"""
import os, pathlib, re, subprocess
R = pathlib.Path(os.environ["BMA_SCRATCH"]) / "r2011"
DRAW = "CASE WHEN winner = 'draw' THEN 'X' ELSE winner END AS winner"
SWAP = "CASE WHEN winner = 'X' THEN 'O' WHEN winner = 'O' THEN 'X' ELSE winner END AS winner"
Q = {"q95": "SELECT winner, COUNT(*) AS n FROM game GROUP BY winner",
     "q99": "SELECT winner, COUNT(*) n FROM game WHERE winner IN ('X','O') GROUP BY winner"}
EDIT = {
 ("q95", "M1"): f"SELECT {DRAW}, COUNT(*) AS n FROM game GROUP BY 1",
 ("q95", "M2"): f"SELECT {SWAP}, COUNT(*) AS n FROM game GROUP BY 1",
 ("q99", "M1"): f"SELECT {DRAW}, COUNT(*) n FROM game WHERE winner IS NOT NULL GROUP BY 1",
 ("q99", "M2"): f"SELECT {SWAP}, COUNT(*) n FROM game WHERE winner IN ('X','O') GROUP BY 1",
}
for (arm, m), new in EDIT.items():
    d = R / arm; f = d / "server" / "store.js"; src = f.read_text(); old = Q[arm]
    assert src.count(old) == 1, (arm, "query not found verbatim")
    before = subprocess.run(["git", "status", "--porcelain"], cwd=d, capture_output=True, text=True).stdout
    f.write_text(src.replace(old, new, 1))
    try:
        p = subprocess.run(["npm", "test"], cwd=d, capture_output=True, text=True, timeout=300)
        out = p.stdout + p.stderr; red = p.returncode != 0
    finally:
        f.write_text(src)
    after = subprocess.run(["git", "status", "--porcelain"], cwd=d, capture_output=True, text=True).stdout
    fails = re.search(r"^. fail (\d+)", out, re.M)
    print(f"{arm} {m}  {'RED (tests catch it)' if red else 'GREEN (tests miss it)':24} "
          f"fail={fails.group(1) if fails else '?'} tree-unchanged={before == after}")
    print(f"     old: {old}\n     new: {new}")
