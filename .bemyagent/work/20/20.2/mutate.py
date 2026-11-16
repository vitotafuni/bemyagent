"""20.2 metric (i) — do the arm's own tests have teeth.

The mutation is semantic and identical for every arm: **a drawn game counts as a win for X.**
It is applied by reading each arm's own tally query, because arms write it differently; the exact
edit per arm is recorded in EDITS below so it is auditable, not reconstructed.

The arm's store.js is restored afterwards and `git status` is compared before and after, so no
arm tree is contaminated by the measurement.
"""
import os, pathlib, subprocess, sys
R = pathlib.Path(os.environ["BMA_SCRATCH"]) / "r202"
CASE = "CASE WHEN winner = 'draw' THEN 'X' ELSE winner END AS winner"
EDITS = {
 "q52": ("SELECT winner, COUNT(*) AS n FROM game WHERE winner IN ('X', 'O') GROUP BY winner",
         f"SELECT {CASE}, COUNT(*) AS n FROM game WHERE winner IS NOT NULL GROUP BY 1"),
 "q53": ("SELECT winner, COUNT(*) AS n FROM game WHERE winner IS NOT NULL GROUP BY winner",
         f"SELECT {CASE}, COUNT(*) AS n FROM game WHERE winner IS NOT NULL GROUP BY 1"),
 "q54": ("SELECT winner, COUNT(*) AS wins FROM game WHERE winner IN ('X', 'O') GROUP BY winner",
         f"SELECT {CASE}, COUNT(*) AS wins FROM game WHERE winner IS NOT NULL GROUP BY 1"),
 "q56": ("SELECT winner, COUNT(*) AS wins FROM game WHERE winner IN ('X', 'O') GROUP BY winner",
         "SELECT CASE WHEN winner = 'draw' THEN 'X' ELSE winner END AS winner, COUNT(*) AS wins FROM game WHERE winner IS NOT NULL GROUP BY 1"),
 "q57": ("SELECT winner, COUNT(*) AS wins FROM game WHERE winner IN ('X', 'O') GROUP BY winner",
         "SELECT CASE WHEN winner = 'draw' THEN 'X' ELSE winner END AS winner, COUNT(*) AS wins FROM game WHERE winner IS NOT NULL GROUP BY 1"),
 "q55": ("SELECT winner, COUNT(*) AS wins FROM game WHERE winner IN ('X', 'O') GROUP BY winner",
         f"SELECT {CASE}, COUNT(*) AS wins FROM game WHERE winner IS NOT NULL GROUP BY 1"),
}

def run(arm):
    d = R / arm
    f = d / "server" / "store.js"
    if arm not in EDITS: return arm, "n/a", "no recorded edit"
    old, new = EDITS[arm]
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
    import re
    fails = re.search(r"^. fail (\d+)", out, re.M)
    return arm, ("RED (tests catch it)" if red else "GREEN (tests miss it)"), \
           f"fail={fails.group(1) if fails else '?'} tree-unchanged={before == after}"

for a in (sys.argv[1:] or sorted(EDITS)):
    arm, verdict, note = run(a)
    print(f"{arm}  {verdict:24} {note}")
