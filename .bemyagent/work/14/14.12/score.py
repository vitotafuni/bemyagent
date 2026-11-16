"""14.12 scoring: two string matches per arm plus a diff against the seeded map."""
import os
import json, pathlib, subprocess
S = pathlib.Path(os.environ["BMA_SCRATCH"])
SIDE = {"q22":"H","q23":"G","q24":"H","q25":"G","q26":"H","q27":"G"}
DRIFT = ["newResumeToken","listOnline","sweep(","resumeSession","touchSession",
         "publicView","onlineCount","tokenFingerprint","registerPresence","isExpired"]
KEEP = "do not delete it as dead code"
res = {}
for arm, side in SIDE.items():
    d = S/"r1412"/arm
    m = (d/".bemyagent"/"docs"/"03-code-map.md").read_text()
    # (i) detection: any planted symbol named anywhere the arm wrote
    anywhere = m
    for p in (d/".bemyagent"/"work").rglob("*.md"):
        anywhere += p.read_text()
    res[arm] = {
      "side": side,
      "detect_in_map": sorted(s for s in DRIFT if s in m),
      "detect_anywhere": sorted(s for s in DRIFT if s in anywhere),
      "underivable_line_kept": KEEP in m,
      "map_diff": subprocess.run(["git","diff","--numstat","HEAD","--",
            ".bemyagent/docs/03-code-map.md"],cwd=d,capture_output=True,text=True).stdout.strip(),
      "read_session_js": "session.js" in anywhere,
    }
print(json.dumps(res, indent=1))
