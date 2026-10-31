import json, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path("<repo>")
S = pathlib.Path("<scratchpad>")
FIXTURE = ROOT / "harness" / "fixture"
OUT = pathlib.Path(sys.argv[1])
ARMS = ["q13", "q14", "q15"]
SETTINGS = {"language": "en", "interactiveMode": False, "strictVerification": False,
            "autoModelSwitching": True, "autoCommit": False,
            "obstacleThreshold": 2, "contextSlicingThreshold": 200}
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
for name in ARMS:
    d = OUT / name
    shutil.copytree(FIXTURE, d)
    shutil.copy(S / "BMA.gen.md", d / "BEMYAGENT.md")
    (d / ".bemyagent").mkdir()
    (d / ".bemyagent" / "settings.json").write_text(json.dumps(SETTINGS, indent=2) + "\n")
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "initial"], cwd=d, check=True)
    # vendor dir present on disk and UNTRACKED, after the commit, and no .gitignore:
    # this is what makes a wrong enumeration possible at all.
    subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund"], cwd=d, check=True)
print(f"built {len(ARMS)} arms in {OUT}")
