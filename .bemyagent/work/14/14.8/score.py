import os
import pathlib, subprocess, json, shutil
S = pathlib.Path(os.environ["BMA_SCRATCH"])
CMD = {
 "q13": "git ls-files '*.js' '*.sql' '*.html' | xargs grep -nE '^(async )?function |^const [A-Za-z_]+ = |^app\\.(get|post|use)|^CREATE TABLE'",
 "q14": "git ls-files '*.js' | xargs grep -nE \"^(const [a-zA-Z]+ =|function |module\\.exports|app\\.(get|post|use))\"",
 "q15": "git ls-files '*.js' '*.html' '*.sql' | xargs grep -nE '^(function|const [a-zA-Z]+ = \\(|module\\.exports|CREATE TABLE|app\\.(get|post))'",
}
SRC_EXT = (".js", ".sql", ".html")
out = {}
for arm, cmd in CMD.items():
    d = S / "r148" / arm
    tracked = subprocess.run(["git", "ls-files"], cwd=d, capture_output=True, text=True).stdout.split()
    src = sorted(f for f in tracked if f.endswith(SRC_EXT))
    r = subprocess.run(cmd, cwd=d, shell=True, capture_output=True, text=True, timeout=60)
    files = sorted({l.split(":")[0] for l in r.stdout.splitlines() if ":" in l})
    # (iii) re-run in a pristine copy of the fixture, command string only
    fresh = S / "fresh148"
    if fresh.exists(): shutil.rmtree(fresh)
    shutil.copytree(S / "r148" / arm, fresh, symlinks=True)
    subprocess.run(["git", "checkout", "-q", "--", "."], cwd=fresh)
    r2 = subprocess.run(cmd, cwd=fresh, shell=True, capture_output=True, text=True, timeout=60)
    files2 = sorted({l.split(":")[0] for l in r2.stdout.splitlines() if ":" in l})
    out[arm] = {
      "exit": r.returncode,
      "lines": len(r.stdout.splitlines()),
      "src_tracked": src,
      "files_in_output": files,
      "missing": [f for f in src if f not in files],
      "vendor_leak": [f for f in files if "node_modules" in f],
      "rerun_same_shape": sorted(files2) == sorted(files) or files2,
      "rerun_files": files2,
      "rerun_exit": r2.returncode,
    }
print(json.dumps(out, indent=1))
