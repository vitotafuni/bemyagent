import json, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path("<repo>")
S = pathlib.Path("<scratchpad>")
FIXTURE = ROOT / "harness" / "fixture"
OUT = pathlib.Path(sys.argv[1])
# neutral names; nothing in them reveals the side
ARMS = {"q1": "BMA.own.md", "q2": "BMA.own.md", "q3": "BMA.own.md",
        "q4": "BMA.rev.md", "q5": "BMA.rev.md", "q6": "BMA.rev.md"}
SETTINGS = {"language": "en", "interactiveMode": False, "strictVerification": False,
            "autoModelSwitching": True, "autoCommit": False,
            "obstacleThreshold": 2, "contextSlicingThreshold": 200}
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for name, proto in ARMS.items():
    d = OUT / name
    shutil.copytree(FIXTURE, d)
    shutil.copy(S / proto, d / "BEMYAGENT.md")
    (d / ".bemyagent").mkdir()
    (d / ".bemyagent" / "settings.json").write_text(json.dumps(SETTINGS, indent=2) + "\n")
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "initial"], cwd=d, check=True)
print(f"built {len(ARMS)} arms in {OUT}")
