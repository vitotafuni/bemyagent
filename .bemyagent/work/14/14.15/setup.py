"""14.15 — the derived-blocks clause as a TREATMENT. 20.5's G seed and 14.13's clause,
both sides this time. Only the arm table and the overwrite guard differ from 20.5/setup_G.py."""
import os
import json, pathlib, shutil, subprocess, sys
ROOT = pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4])
S = pathlib.Path(os.environ["BMA_SCRATCH"])
FIXTURE = ROOT / "harness" / "fixture"
OUT = pathlib.Path(sys.argv[1])
ARMS = {"q79": "A", "q80": "B", "q81": "A", "q82": "B", "q83": "A", "q84": "B"}
ONLY = set(sys.argv[2:])
if ONLY: ARMS = {k: v for k, v in ARMS.items() if k in ONLY}
SETTINGS = {"language": "en", "interactiveMode": False, "strictVerification": False,
            "autoModelSwitching": True, "autoCommit": False, "conversationLog": "",
            "obstacleThreshold": 2, "contextSlicingThreshold": 200}

GEN_CMD = ("git ls-files client server db test | while read f; do echo \"== $f\"; "
           "grep -nE '^(async )?function [A-Za-z_]+|^const [A-Za-z_]+ = |^CREATE TABLE|"
           "^app\\.(get|post)|^test\\(|id=\"' \"$f\"; done")

H_SECTION = """| File | Symbols |
|---|---|
| client/app.js | `api`, `render`, `move` |
| client/index.html | `#board`, `#status` |
| db/schema.sql | `CREATE TABLE game` |
| server/index.js | `POST /api/games`, `GET /api/games/:id`, `POST /api/games/:id/moves` |
| server/rules.js | `applyMove`, `winnerOf` |
| server/session.js | `newSessionId`, `createSession`, `destroySession` |
| server/store.js | `createGame`, `getGame`, `saveGame` |
| test/rules.test.js | 4 tests |
"""

MAP_TAIL = """
## Hot Paths / Performance Critical
- `server/rules.js` `winnerOf()` runs on every move.

## Test Coverage Overview
- `test/rules.test.js` covers win, draw, turn flip and occupied-cell rejection. 4 tests.

## Pages / Routes
| Path/Method | File/Handler | Role/Auth | Key DOM IDs / Description |
|---|---|---|---|
| POST /api/games | server/index.js | none | creates a game |
| GET /api/games/:id | server/index.js | none | fetches a game, `#board` |
| POST /api/games/:id/moves | server/index.js | none | plays a move, `#status` |

## Key functions / Client-side JS
| Function/File | Role/Inputs | Outputs/Side effects |
|---|---|---|
| `api()` / client/app.js | fetch wrapper | JSON |
| `render()` / client/app.js | draws the board from game state | DOM |
| `move()` / client/app.js | posts a move, re-renders | DOM |

## Data schemas
### Schema: game
| Field | Type | Example | Owner |
|---|---|---|---|
| id | INTEGER | 1 | server/store.js |
| board | TEXT | `---------` | server/store.js |
| turn | TEXT | `X` | server/store.js |
| winner | TEXT | `X` | server/store.js |

> ⚠️ `server/session.js` is imported by nothing. Kept deliberately for the planned multi-device work — do not delete it as dead code.
"""

DOCS = {
 "01-overview.md": "# Overview\n\nA two-player tic-tac-toe game played in the browser against a\nserver-held board. Games are persisted so a page reload resumes the same board.\n\n## Success Metrics\n- A game survives a reload.\n- The rules never allow an illegal move.\n\n## Repo structure\n```\nclient/  server/  db/  test/\n```\n\n## Quick start\n`npm install && npm test`, then `node server/index.js`.\n\n## Env vars\n| name | default | description |\n|---|---|---|\n| DB_PATH | ./game.db | sqlite file |\n| PORT | 3000 | http port |\n\n## Ports\n| port | service | notes |\n|---|---|---|\n| 3000 | express | the only service |\n",
 "02-architecture.md": "# Architecture\n\n```mermaid\ngraph LR\n  browser --> express --> sqlite\n```\n\n## Request flow\n1. The browser posts a move to `/api/games/:id/moves`.\n2. `server/rules.js` validates it and computes the winner.\n3. `server/store.js` saves the board.\n4. The client re-renders.\n\n## Components\n- **client** — renders the board and posts moves. Owns no state.\n- **server/rules.js** — the only place that decides legality and victory. Does NOT touch the database.\n- **server/store.js** — the only place that reads or writes sqlite.\n- **server/session.js** — multi-device session bookkeeping, not yet wired into any route.\n",
 "04-tech-stack.md": "# Tech Stack\n\n| name | version | role | why |\n|---|---|---|---|\n| node | 26 | runtime | project baseline |\n| express | ^4 | http | smallest thing that routes |\n| better-sqlite3 | ^13 | storage | synchronous, no pool to manage |\n\n## Known compatibility issues\n- better-sqlite3 needs a rebuild after a node major upgrade.\n\n## External services\nNone.\n",
 "05-decisions-and-issues.md": "# Decisions and Issues\n\n## Decisions index\n- **The board lives on the server.** A client-held board cannot survive a reload and cannot be refereed.\n- **`server/session.js` is kept although nothing imports it.** The multi-device work it was written for is deferred, not cancelled.\n\n## Engineering Learnings\n- Rules and storage stay in separate modules so a rules bug can never corrupt a row.\n\n## Known issues\n### Draws are not displayed\n- **Symptom**: a full board with no line shows no message.\n- **Status**: open\n",
 "06-implementation-plan.md": "# Implementation Plan\n\n## Milestone 1 — playable game\n**Goal**: a legal, persistent two-player game.\n**Status**: done\n\n| # | Task | Status |\n|---|---|---|\n| 1.1 | Board, rules, persistence, tests | done |\n",
}
TEMPLATES = {
 "decisions/_template.md": "# ADR: [Title]\n\n## Context\n## Options considered\n## Decision\n## Consequences\n",
 "specs/_template.md": "# [Feature]\n\n## Description (one paragraph)\n## Acceptance criteria\n## Open questions\n",
 "drafts/_template.md": "# [Idea]\n\n## Context\n## Sketch\n## Open questions\n",
}


ANCHOR = "Read the output, do not quote it."
CLAUSE = (" **Derived blocks:** if a `docs/` file you read this task presents a block as the output "
          "of a named command, VERIFY MUST re-run that command and record the result in "
          "`04_verify.md` as `derived block <file> \u2014 no diff` or the differing lines. Stale "
          "means the file is wrong: refresh the block from the command's own output in the same "
          "task. Nothing may be typed into such a block by hand.")

def treat(text):
    assert text.count(ANCHOR) == 1, f"anchor appears {text.count(ANCHOR)} times"
    return text.replace(ANCHOR, ANCHOR + CLAUSE)

OUT.mkdir(parents=True, exist_ok=True)
for a in ARMS:
    assert not (OUT / a).exists(), f"{a} already built - refusing to overwrite"
rules = (ROOT / ".bemyagent" / "docs" / "00-ai-rules.md").read_text()
think_tpl = "## Context\n\n### Context Saturation Check\n- [ ] Target files/paths\n- [ ] Expected behavior\n- [ ] Constraints\n- [ ] Dependencies\n\n## Approaches Considered\n## Selected Approach & Risks\n### Pre-mortem\n### Devil's Advocate\n## Verification Plan\n"

for name, side in ARMS.items():
    d = OUT / name
    shutil.copytree(FIXTURE, d)
    proto = (ROOT / "BEMYAGENT.md").read_text()
    (d / "BEMYAGENT.md").write_text(treat(proto) if side == "B" else proto)
    (d / "CLAUDE.md").write_text("Read .bemyagent/docs/00-ai-rules.md before every task.\n")
    bm = d / ".bemyagent"
    for sub in ("docs/decisions", "docs/specs", "docs/drafts", "work"):
        (bm / sub).mkdir(parents=True, exist_ok=True)
    (bm / "settings.json").write_text(json.dumps(SETTINGS, indent=2) + "\n")
    (bm / "docs" / "00-ai-rules.md").write_text(treat(rules) if side == "B" else rules)
    for fn, body in DOCS.items(): (bm / "docs" / fn).write_text(body)
    for fn, body in TEMPLATES.items(): (bm / "docs" / fn).write_text(body)
    (bm / "work" / "_template_think.md").write_text(think_tpl)
    # the code map: identical except the Inventory section
    (bm / "docs" / "03-code-map.md").write_text("# Code Map\n\n## Inventory\n<INV>\n" + MAP_TAIL)
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "initial"], cwd=d, check=True)
    subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund"], cwd=d, check=True)

# build the STALE generated output from a real run, then trim session.js down to the three
# symbols the hand-written table also claims, so both sides are stale in the identical way
probe = OUT / list(ARMS)[0]
full = subprocess.run(GEN_CMD, cwd=probe, shell=True, capture_output=True, text=True).stdout
blocks, cur = [], []
for line in full.splitlines():
    if line.startswith("== "):
        if cur: blocks.append(cur)
        cur = [line]
    else: cur.append(line)
if cur: blocks.append(cur)
KEEP = ("function newSessionId", "function createSession", "function destroySession")
out = []
for b in blocks:
    if b[0] == "== server/session.js":
        out.append(b[0]); out += [l for l in b[1:] if any(k in l for k in KEEP)]
    else:
        out += b
stale = "\n".join(out)

G_SECTION = ("`" + GEN_CMD + "`\n\n"
 "It MUST emit every tracked source file, including one holding no symbol it recognises, and it\n"
 "MUST name the symbols of every file that has any. Re-run it and diff instead of trusting the\n"
 "output below.\n\n```\n" + stale + "\n```\n")

for name, side in ARMS.items():
    p = OUT / name / ".bemyagent" / "docs" / "03-code-map.md"
    p.write_text(p.read_text().replace("<INV>", G_SECTION))
    subprocess.run(["git", "add", "-A"], cwd=OUT / name, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "code map"], cwd=OUT / name, check=True)
print(f"built {len(ARMS)} arms in {OUT}")
print("stale session.js block:", [l for l in stale.splitlines() if "session" in l or "newSession" in l or "createSession" in l or "destroySession" in l][:5])
