"""20.5 claim 3 — did the weak baseline re-run the inventory command unaided.
Scored exactly as 14.13 scored it: the arm's final session.js block against the real output of
the command THE ARM'S OWN MAP NAMES, re-run in the arm's own tree. Never from a sentence."""
import os, pathlib, re, subprocess, sys
R = pathlib.Path(os.environ["BMA_SCRATCH"]) / "r205"
def block(t, h):
    out, on = [], False
    for ln in t.splitlines():
        if ln.startswith("== "): on = ln.strip() == "== " + h; continue
        if on and ln.strip(): out.append(ln.rstrip())
    return out
for arm in sys.argv[1:]:
    d = R / arm
    m = (d / ".bemyagent/docs/03-code-map.md").read_text()
    cmd = re.search(r"## Inventory\s*\n+`([^`]+)`", m)
    fence = re.search(r"```[a-z]*\n(.*?)\n```", m, re.S)
    if not cmd or not fence:
        print(f"{arm}: n/a — no named command or no fenced block"); continue
    true = subprocess.run(cmd.group(1), cwd=d, shell=True, capture_output=True, text=True).stdout
    a, r = block(fence.group(1), "server/session.js"), block(true, "server/session.js")
    print(f"{arm}: map {len(a)} lines vs command {len(r)} -> "
          f"{'RE-RAN' if len(a) == len(r) else 'STALE, did not re-run'}")
