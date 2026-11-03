"""14.9 scoring, every criterion executed. Usage: python3 -I score149.py cmds.json"""
import json, pathlib, subprocess, shutil, sys
S = pathlib.Path("<scratchpad>")
SIDE = {"q16":"S","q17":"C","q18":"S","q19":"C","q20":"S","q21":"C"}
SRC_EXT = (".js", ".sql", ".html")
CMD = json.loads(pathlib.Path(sys.argv[1]).read_text())

def section(arm):
    lines = (S/"r149"/arm/".bemyagent"/"docs"/"03-code-map.md").read_text().splitlines()
    i = lines.index("## Inventory")
    body = []
    for l in lines[i+1:]:
        if l.startswith("## "): break
        body.append(l)
    return "\n".join(body)

def symcount(text, src):
    """per file: lines mentioning it, and how many carry more than the bare path"""
    return {f: {"lines": sum(1 for l in text.splitlines() if f in l),
                "sym": sum(1 for l in text.splitlines() if f in l and l.strip().rstrip(":") != f)}
            for f in src}

res = {}
for arm, cmd in CMD.items():
    d = S/"r149"/arm
    tracked = subprocess.run(["git","ls-files"],cwd=d,capture_output=True,text=True).stdout.split()
    # the ORIGINAL tracked source set, before the arm added its own test file
    orig = subprocess.run(["git","ls-files","--with-tree=HEAD"],cwd=d,capture_output=True,text=True).stdout.split()
    src = sorted(f for f in orig if f.endswith(SRC_EXT))
    r = {"side": SIDE[arm], "command": cmd, "src_tracked": len(src)}
    # (ii-b) the pasted inventory, which is what a reader of the map gets
    sec = section(arm)
    pm = symcount(sec, src)
    r["pasted_missing"] = [f for f in src if pm[f]["lines"] == 0]
    r["pasted_with_symbols"] = sum(1 for f in src if pm[f]["sym"] > 0)
    r["pasted_lines"] = len(sec.splitlines())
    if not cmd:
        r.update(runs=False, note="command string in the map is truncated and unrunnable")
        res[arm] = r; continue
    p = subprocess.run(cmd, cwd=d, shell=True, capture_output=True, text=True, timeout=120)
    om = symcount(p.stdout, src)
    r.update(runs=(p.returncode == 0), exit=p.returncode, out_lines=len(p.stdout.splitlines()),
             cmd_missing=[f for f in src if om[f]["lines"] == 0],
             cmd_with_symbols=sum(1 for f in src if om[f]["sym"] > 0),
             vendor_leak=sorted({l.split(":")[0] for l in p.stdout.splitlines() if "node_modules" in l}))
    fresh = S/"fresh149"
    if fresh.exists(): shutil.rmtree(fresh)
    shutil.copytree(d, fresh, symlinks=True)
    subprocess.run(["git","checkout","-q","--","."], cwd=fresh)
    p2 = subprocess.run(cmd, cwd=fresh, shell=True, capture_output=True, text=True, timeout=120)
    o2 = symcount(p2.stdout, src)
    r["rerun_exit"] = p2.returncode
    r["rerun_missing"] = [f for f in src if o2[f]["lines"] == 0]
    res[arm] = r
print(json.dumps(res, indent=1))
