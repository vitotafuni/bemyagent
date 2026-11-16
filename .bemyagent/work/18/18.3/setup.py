import os
import json, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4])
FIXTURE = ROOT / "harness" / "fixture"
OUT = pathlib.Path(sys.argv[1])
# neutral names, continuing 18.2's series; nothing in them reveals the condition
ARMS = ["q7", "q8", "q9"]
SETTINGS = {"language": "en", "interactiveMode": False, "strictVerification": False,
            "autoModelSwitching": True, "autoCommit": False,
            "obstacleThreshold": 2, "contextSlicingThreshold": 200}
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for name in ARMS:
    d = OUT / name
    shutil.copytree(FIXTURE, d)
    shutil.copy(ROOT / "BEMYAGENT.md", d / "BEMYAGENT.md")   # shipped protocol, no clause
    (d / ".bemyagent").mkdir()
    (d / ".bemyagent" / "settings.json").write_text(json.dumps(SETTINGS, indent=2) + "\n")
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "initial"], cwd=d, check=True)
print(f"built {len(ARMS)} arms in {OUT}")
