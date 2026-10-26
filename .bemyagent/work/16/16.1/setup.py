import shutil, subprocess
from pathlib import Path
SP=Path("/private/tmp/claude-501/-Users-caporale-me-gitlab-bemyagent/8aeed20a-f57d-484c-a624-f3b1637843b6/scratchpad")
REPO=Path("/Users/caporale/me-gitlab/bemyagent")
EXP=SP/"exp16"; SRC=SP/"fix16"
BASE=(REPO/"BEMYAGENT.md").read_text(encoding="utf-8")

ANCHOR = "| Tech dependency or version | docs/04-tech-stack.md |"
assert ANCHOR in BASE

ROW = "\n| Conversation log | the user's exact words, on demand |"
RULE_B = ("\n\n**Conversation log:** append every turn to `.bemyagent/log/YYYY-MM-DD.md` as it "
          "happens — the user's message **verbatim**, your reply, then a `→` line naming what the "
          "turn produced (files, task `X.Y`, commits). Never edited afterwards. Never read during "
          "Session Restore. No tool output, no thinking, never secrets.")
RULE_C = ("\n\n**Conversation log:** append every turn to `.bemyagent/log/YYYY-MM-DD.md` as it "
          "happens — a **short summary** of what the user asked (not a transcript: do not claim "
          "to quote), your answer, then a `→` line naming what the turn produced (files, task "
          "`X.Y`, commits). Never edited afterwards. Never read during Session Restore. No tool "
          "output, no thinking, never secrets.")

def build(c):
    if c == "a": return BASE
    return BASE.replace(ANCHOR, ANCHOR + ROW + (RULE_B if c == "b" else RULE_C))

if EXP.exists(): shutil.rmtree(EXP)
EXP.mkdir(parents=True)
for c in ("a","b","c"):
    body = build(c)
    for n in (1,2,3):
        arm = EXP/f"{c}-{n}"
        shutil.copytree(SRC, arm)
        for junk in (".bemyagent","AGENTS.md","CLAUDE.md"):
            p = arm/junk
            if p.is_dir(): shutil.rmtree(p)
            elif p.exists(): p.unlink()
        (arm/"BEMYAGENT.md").write_text(body, encoding="utf-8")

for pair in (("a-1","b-1"),("b-1","c-1")):
    d=subprocess.run(["diff",str(EXP/pair[0]/"BEMYAGENT.md"),str(EXP/pair[1]/"BEMYAGENT.md")],
                     capture_output=True,text=True)
    print(f"=== diff {pair[0]} vs {pair[1]} ===")
    print(d.stdout.strip()[:700] or "IDENTICI - ERRORE")
    print()
print("arms:", ", ".join(sorted(p.name for p in EXP.iterdir())))
