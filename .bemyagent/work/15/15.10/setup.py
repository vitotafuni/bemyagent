import shutil, subprocess
from pathlib import Path
SP=Path("/private/tmp/claude-501/-Users-caporale-me-gitlab-bemyagent/8aeed20a-f57d-484c-a624-f3b1637843b6/scratchpad")
REPO=Path("/Users/caporale/me-gitlab/bemyagent")
EXP=SP/"exp10"; SRC=SP/"fix10"
BASE=(REPO/"BEMYAGENT.md").read_text(encoding="utf-8")

OLD = "- `✅ Validation` — the objective evidence of success"
NEW = ("- `✅ Validation` — the objective evidence of success. Write each criterion as "
       "`WHEN <condition> THE SYSTEM SHALL <observable>`; a criterion that cannot be stated in "
       "that form is not a validation criterion")
assert OLD in BASE, "anchor not found in BEMYAGENT.md"

if EXP.exists(): shutil.rmtree(EXP)
EXP.mkdir(parents=True)
for cond in ("a","b"):
    body = BASE.replace(OLD, NEW) if cond=="b" else BASE
    for n in (1,2,3):
        arm = EXP/f"{cond}-{n}"
        shutil.copytree(SRC, arm)
        for junk in (".bemyagent","AGENTS.md","CLAUDE.md"):
            p=arm/junk
            if p.is_dir(): shutil.rmtree(p)
            elif p.exists(): p.unlink()
        (arm/"BEMYAGENT.md").write_text(body, encoding="utf-8")

d=subprocess.run(["diff",str(EXP/"a-1"/"BEMYAGENT.md"),str(EXP/"b-1"/"BEMYAGENT.md")],
                 capture_output=True,text=True)
print("=== diff a-1 vs b-1 ===")
print(d.stdout or "IDENTICAL - ERROR")
print("arms:", ", ".join(sorted(p.name for p in EXP.iterdir())))
