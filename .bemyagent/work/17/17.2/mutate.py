import pathlib, re, shutil, subprocess, sys, json
S = pathlib.Path("<scratchpad>")
ARMS = {"q10": "r172", "q11": "r172", "q12": "r172",
        "q7": "r183", "q8": "r183", "q9": "r183"}
MUT = S / "mutants"
if MUT.exists(): shutil.rmtree(MUT)
MUT.mkdir()

FILTER = re.compile(r"\s+WHERE winner (?:IS NOT NULL|IN \('X', ?'O'\))")

def mutate(path, kind):
    p = path / "server" / "store.js"
    src = p.read_text()
    if kind == "M1":
        out, n = FILTER.subn("", src)
    else:
        out, n = re.subn(r"COUNT\(\*\)", "1", src)
    assert n == 1, f"{path.name} {kind}: {n} substitutions"
    p.write_text(out)

results = {}
for arm, rnd in ARMS.items():
    src = S / rnd / arm
    results[arm] = {}
    for kind in ("M1", "M2"):
        dst = MUT / f"{arm}_{kind}"
        shutil.copytree(src, dst, symlinks=True)
        mutate(dst, kind)
        r = subprocess.run(["npm", "test"], cwd=dst, capture_output=True, text=True, timeout=180)
        tail = [l for l in r.stdout.splitlines() if l.startswith(("# pass", "# fail"))]
        results[arm][kind] = {"exit": r.returncode, "tally": " ".join(tail)}
print(json.dumps(results, indent=1))
