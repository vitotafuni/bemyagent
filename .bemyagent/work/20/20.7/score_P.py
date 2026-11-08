"""20.7 condition P — deterministic extraction only. The NAMED/SILENT call is made by a reader
against the rubric in 02_tasks.md and recorded in 04_verify.md naming the arm; this script
produces the text that call is made on, plus the context counts, and never the verdict."""
import json, pathlib, re, subprocess, sys
R = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad/r207p")
ARMS = ["q64", "q67", "q70"]
# pre-filter only: a hit is not a NAMED, a miss is not a SILENT. It points the reader at lines.
D1 = re.compile(r"draw", re.I)                                    # do draws count
D2 = re.compile(r"all[- ]time|per[- ]session|across all|every game|persisted game|"
                r"session|reload|history", re.I)                  # scope of the count
res = {}
ONLY = set(sys.argv[1:])
for arm in ARMS:
    if ONLY and arm not in ONLY: continue
    d = R / arm
    if not d.exists(): continue
    think = sorted((d / ".bemyagent" / "work").rglob("01_think.md"))
    body = think[0].read_text() if think else ""
    # the Saturation Check block, for the blocking-item count 18.3 read as 0/3
    sat = re.search(r"### Context Saturation Check(.*?)(?=\n## |\Z)", body, re.S)
    sat = sat.group(1) if sat else ""
    res[arm] = {
      "think_path": str(think[0].relative_to(d)) if think else None,
      "think_lines": len(body.splitlines()),
      "unchecked_items": len(re.findall(r"^- \[ \]", sat, re.M)),
      "checked_items": len(re.findall(r"^- \[x\]", sat, re.M | re.I)),
      "d1_lines": [l.strip() for l in body.splitlines() if D1.search(l)],
      "d2_lines": [l.strip() for l in body.splitlines() if D2.search(l)],
      "delivery": subprocess.run(["git", "diff", "--stat", "HEAD", "--",
                                  "client", "server", "db", "test"],
                                 cwd=d, capture_output=True, text=True).stdout.strip()
                  .splitlines()[-1:],
      "tests": re.findall(r"^. (?:pass|fail) \d+",
                          subprocess.run(["npm", "test"], cwd=d, capture_output=True,
                                         text=True).stdout, re.M),
    }
print(json.dumps(res, indent=1))
