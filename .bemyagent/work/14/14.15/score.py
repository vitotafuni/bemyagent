"""14.15 — freshness per file and forged lines per line, both read against the output of the
command THE ARM'S OWN MAP NAMES, re-run in the arm's own tree. 14.13's scorer defined a forged
line against the SEEDED command and read one arm's genuine improvement as nine forgeries."""
import os
import json, pathlib, re, subprocess, sys
R = pathlib.Path(os.environ["BMA_SCRATCH"]) / "r1415"
SIDE = {"q79": "A", "q80": "B", "q81": "A", "q82": "B", "q83": "A", "q84": "B"}

def sections(t):
    """'== path' headed blocks -> {path: [lines]}"""
    out, cur = {}, None
    for ln in t.splitlines():
        if ln.startswith("== "):
            cur = ln.strip()[3:]; out[cur] = []
        elif cur is not None and ln.strip():
            out[cur].append(ln.rstrip())
    return out

res = {}
ONLY = set(sys.argv[1:])
for arm, side in SIDE.items():
    if ONLY and arm not in ONLY: continue
    d = R / arm
    if not d.exists(): continue
    m = (d / ".bemyagent/docs/03-code-map.md").read_text()
    cmd = re.search(r"## Inventory\s*\n+`([^`]+)`", m)
    fence = re.search(r"```[a-z]*\n(.*?)\n```", m, re.S)
    if not cmd or not fence:
        res[arm] = {"side": side, "error": "no named command or no fenced block"}; continue
    true = subprocess.run(cmd.group(1), cwd=d, shell=True,
                          capture_output=True, text=True).stdout
    got, want = sections(fence.group(1)), sections(true)
    files = sorted(set(want))
    fresh = [f for f in files if got.get(f, []) == want[f]]
    forged = {f: [l for l in got.get(f, []) if l not in want.get(f, [])] for f in sorted(set(got))}
    forged = {f: v for f, v in forged.items() if v}
    v4 = (d / ".bemyagent/work").rglob("04_verify.md")
    v4txt = "\n".join(p.read_text(errors="replace") for p in v4)
    res[arm] = {
      "side": side,
      "command_named": cmd.group(1)[:60],
      "files_in_command": len(files),
      "files_fresh": fresh,
      "files_stale": [f for f in files if f not in fresh],
      "forged_lines_total": sum(len(v) for v in forged.values()),
      "forged_by_file": forged,
      "derived_block_line_in_verify": bool(re.search(r"derived block", v4txt, re.I)),
      "delivery": subprocess.run(["git","diff","--stat","HEAD","--",
                                  "client","server","db","test"],
                                 cwd=d, capture_output=True, text=True).stdout.strip()
                  .splitlines()[-1:],
      "tests": re.findall(r"^. (?:pass|fail) \d+",
                          subprocess.run(["npm","test"], cwd=d, capture_output=True,
                                         text=True).stdout, re.M),
    }
print(json.dumps(res, indent=1))
