"""19.2b — 18.2's directory shape: `.bemyagent/` holding ONLY settings.json."""
import os, json, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4])
FIXTURE = ROOT / "harness" / "fixture"
OUT = pathlib.Path(sys.argv[1])
ARMS = {"q58": "A", "q60": "A", "q62": "A"}
SETTINGS = {"language": "en", "interactiveMode": False, "strictVerification": False,
            "autoModelSwitching": True, "autoCommit": False, "conversationLog": "",
            "obstacleThreshold": 5, "contextSlicingThreshold": 150}

ANCHOR = "1. **UPGRADE** — `.bemyagent/` already exists:"
REPL = ("1. **UPGRADE** — `.bemyagent/` holds something this step could overwrite or must not "
        "touch: any `docs/` or `work/` file, or any file this protocol does not name. **Branch on "
        "content, not on the directory existing.** Where it holds none of those — empty, or only "
        "`settings.json`, whose merge is additive and destroys nothing — there is nothing to "
        "review: go to BROWNFIELD or GREENFIELD, generate what is missing, and report in one line "
        "what was already there:")

def treat(text):
    n = text.count(ANCHOR)
    assert n == 1, f"anchor appears {n} times"
    return text.replace(ANCHOR, REPL)

if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir(parents=True)
proto = (ROOT / "BEMYAGENT.md").read_text()

for name, side in ARMS.items():
    d = OUT / name
    shutil.copytree(FIXTURE, d)
    (d / "BEMYAGENT.md").write_text(treat(proto) if side == "B" else proto)
    bm = d / ".bemyagent"
    bm.mkdir()
    (bm / "settings.json").write_text(json.dumps(SETTINGS, indent=2) + "\n")
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "code map"], cwd=d, check=True)
    subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund"], cwd=d, check=True)
print(f"built {len(ARMS)} arms in {OUT}")
