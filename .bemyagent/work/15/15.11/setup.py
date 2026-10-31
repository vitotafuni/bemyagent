#!/usr/bin/env python3
"""Build 6 arm directories for the 15.11 round. One variable: interactiveMode."""
import json, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path("<repo>")
FIXTURE = ROOT / "harness" / "fixture"
PROTOCOL = ROOT / "BEMYAGENT.md"
OUT = pathlib.Path(sys.argv[1])

# neutral names: nothing reveals the condition or the hypothesis
NAMES = {"w1": False, "w2": False, "w3": False, "w4": True, "w5": True, "w6": True}

SETTINGS = {
    "language": "en",
    "strictVerification": False,
    "autoModelSwitching": True,
    "autoCommit": False,
    "obstacleThreshold": 2,
    "contextSlicingThreshold": 200,
}

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

for name, interactive in NAMES.items():
    d = OUT / name
    shutil.copytree(FIXTURE, d)
    shutil.copy(PROTOCOL, d / "BEMYAGENT.md")
    bma = d / ".bemyagent"
    bma.mkdir()
    s = dict(SETTINGS)
    s["interactiveMode"] = interactive
    (bma / "settings.json").write_text(json.dumps(s, indent=2) + "\n")
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "initial"], cwd=d, check=True)

print(f"built {len(NAMES)} arms in {OUT}")
for name, interactive in sorted(NAMES.items()):
    print(f"  {name}: interactiveMode={str(interactive).lower()}")
