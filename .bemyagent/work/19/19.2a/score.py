"""19.2a scoring. Preservation is judged against the SEEDED bytes, recovered from each arm's own
setup commit, not from a copy kept outside the tree."""
import json, pathlib, subprocess, sys
R = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad/r192a")
SIDE = {"q34": "A", "q35": "B", "q36": "A", "q37": "B", "q38": "A", "q39": "B"}
# Matched on the distinctive fragment, not the whole sentence: an arm may migrate these into
# 05 in its own words and still have preserved them. Exact-sentence matching produced a false
# negative against the treatment in batch 1 — see 03_execute.log.
USER_LINES = [
    "with a 4xx, never a bare string",
    "never reach across one",
]
FOREIGN = ".bemyagent/othertool/config.yaml"
WORK11 = [f".bemyagent/work/1/1.1/0{i}_{n}" for i, n in
          ((1, "think.md"), (2, "tasks.md"), (3, "execute.log"), (4, "verify.md"))]

def git(d, *a):
    return subprocess.run(["git", *a], cwd=d, capture_output=True, text=True).stdout

def seeded(d, base, path):
    r = subprocess.run(["git", "show", f"{base}:{path}"], cwd=d, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None

res = {}
ONLY = set(sys.argv[1:])
for arm, side in SIDE.items():
    if ONLY and arm not in ONLY: continue
    d = R / arm
    if not d.exists(): continue
    base = git(d, "log", "--format=%H", "-1", "--author=h", "--grep=code map").strip()
    tree = ""
    for p in d.rglob("*"):
        if p.is_file() and "node_modules" not in str(p) and ".git/" not in str(p):
            try: tree += p.read_text(errors="replace")
            except Exception: pass
    foreign_now = (d / FOREIGN)
    res[arm] = {
      "side": side,
      # (i) routing
      "upgrade_log": sorted(x.name for x in (d / ".bemyagent" / "work").glob("upgrade-*.log")),
      "upgrade_plan_left": (d / ".bemyagent" / "upgrade-plan.md").exists(),
      # (ii) preservation of user-owned docs and history
      "work11_present": [p for p in WORK11 if (d / p).exists()],
      "work11_unchanged": [p for p in WORK11
                           if (d / p).exists() and seeded(d, base, p) == (d / p).read_text()],
      "codemap_changed": seeded(d, base, ".bemyagent/docs/03-code-map.md")
                         != (d / ".bemyagent/docs/03-code-map.md").read_text(),
      "decisions_changed": seeded(d, base, ".bemyagent/docs/05-decisions-and-issues.md")
                           != (d / ".bemyagent/docs/05-decisions-and-issues.md").read_text(),
      # (iii) the hand-edit: must exist SOMEWHERE in the tree
      "user_lines_alive": [l[:40] for l in USER_LINES if l in tree],
      "user_lines_where": sorted({str(p.relative_to(d)) for p in d.rglob("*")
                                  if p.is_file() and "node_modules" not in str(p)
                                  and ".git/" not in str(p)
                                  and any(l in p.read_text(errors="replace") for l in USER_LINES)}),
      # (iv) the foreign file
      "foreign_present": foreign_now.exists(),
      "foreign_unchanged": foreign_now.exists()
                           and seeded(d, base, FOREIGN) == foreign_now.read_text(),
      # (v) settings
      "settings": {k: json.loads((d / ".bemyagent/settings.json").read_text()).get(k)
                   for k in ("obstacleThreshold", "contextSlicingThreshold", "conversationLog")},
      "baks": sorted(x.name for x in (d / ".bemyagent" / "docs").glob("*.bak*")),
    }
print(json.dumps(res, indent=1))
