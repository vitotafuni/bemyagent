import pathlib, re, subprocess, json
S = pathlib.Path("<scratchpad>")
TAG = re.compile(r"\[RUNTIME_CHECK:\s*`?(.+?)`?\]", re.S)
out = {}
for arm in ("q10", "q11", "q12"):
    tags = TAG.findall((S / "r172" / arm / ".bemyagent/work/1/1.1/02_tasks.md").read_text())
    seen, cmds = set(), []
    for c in tags:
        c = c.strip()
        if c not in seen:
            seen.add(c); cmds.append(c)
    rows = []
    for c in cmds:
        r = {}
        for kind in ("M1", "M2"):
            d = S / "mutants" / f"{arm}_{kind}"
            try:
                p = subprocess.run(c, cwd=d, shell=True, capture_output=True, text=True, timeout=120)
                r[kind] = p.returncode
            except subprocess.TimeoutExpired:
                r[kind] = "timeout"
        rows.append({"cmd": c[:70], "M1": r["M1"], "M2": r["M2"]})
    out[arm] = rows
print(json.dumps(out, indent=1))
