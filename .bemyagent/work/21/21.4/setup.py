"""21.4 - 21.1's setup.py with the arms, the output root and the treatment changed; the seeded
documents (DOCS, TEMPLATES, H_SECTION, MAP_TAIL) are 21.1's, untouched. Seven arms on the one seed:
q112-q114 C (the rules as released: the working tree of the repo), q115-q117 L (the same with one
added line: both files taken with `git show bma/21.4:<path>`, never from a worktree folder, never
retyped), q901 q902 q903 pilots (C, never counted). The seed has no E/R treatment and no Resume block.
Before any copy the script asserts (B10: also the sha1 of the whole added line) on the two pairs of texts: the rules of L differ from the rules of C
by exactly one added line, BEMYAGENT.md of L from BEMYAGENT.md of C by exactly one added line, the two
lines are the same, and that line starts with `**Read this file whole`. Nothing is built if one fails.
It also asserts that the added line is line 2 of the rules file (and the same line in BEMYAGENT.md), and writes
<R214_OUT>/setup.status: the commit ids of HEAD and of bma/21.4, the sha1 of the added line, and per built arm the sha1 of its rules
file and of its BEMYAGENT.md. The status goes to the launcher's output folder, not beside the trees: an arm that runs `ls ..` finds only trees.
C4 (Amendment 3): two runs, two roots. `setup.py pilots [arm ...]` builds q901 q902 q903 (all C, never counted) in R214P_ROOT (default
<scratch>/r214p); `setup.py six [arm ...]` builds q112-q117 in R214_ROOT (default <scratch>/r214) and REFUSES unless a marker
<R214_OUT>/pilot_ok.<pilot> exists (check_pilot.sh writes it on PILOT OK): the six are built after a PILOT OK, shortly before their launch.
C3: the assertion that K (kset.py) has 86 lines is made here too.
Usage: python3 setup.py pilots|six [arm ...]    (R214P_ROOT / R214_ROOT override the roots, R214_OUT the status folder; BMA_REPO the repo)
"""
import difflib, glob, hashlib, json, os, pathlib, shutil, subprocess, sys
sys.dont_write_bytecode = True
ROOT = pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4])
S = pathlib.Path(os.environ["BMA_SCRATCH"])      # the scratch directory of this round (the shell scripts export it from local.env)
HERE = pathlib.Path(__file__).resolve().parent
FIXTURE = ROOT / "harness" / "fixture"
sys.path.insert(0, str(HERE))
import kset                                       # noqa: E402
STATUS_DIR = pathlib.Path(os.environ.get("R214_OUT") or S / "r214_out")
MODE = sys.argv[1] if len(sys.argv) > 1 else ""
if MODE not in ("pilots", "six"):
    sys.exit("usage: setup.py pilots|six [arm ...]")
OUT = pathlib.Path(os.environ.get("R214P_ROOT") or S / "r214p") if MODE == "pilots" else pathlib.Path(os.environ.get("R214_ROOT") or S / "r214")
if MODE == "six" and not glob.glob(str(STATUS_DIR / "pilot_ok.*")):
    sys.exit(f"setup.py six refuses: no marker {STATUS_DIR}/pilot_ok.<pilot> - check_pilot.sh writes it on PILOT OK; the six are built after a PILOT OK")
REF = "bma/21.4"                                  # the ref that carries the candidate line
LINE_SHA1_EXPECTED = "c39979f0fa5bc245fc6454d087ef5fb7d8754cc3"      # B10: sha1 of the added line, without its newline (02_tasks.md Amendment 2)
RULES_REL = ".bemyagent/docs/00-ai-rules.md"
ARMS = ({"q901": "C", "q902": "C", "q903": "C"} if MODE == "pilots" else      # pilots (B9): the seed and condition of a C arm, never counted; a pilot that stops is
        {"q112": "C", "q113": "C", "q114": "C", "q115": "L", "q116": "L", "q117": "L"})     # not cleared and run again under its name: the next name follows
ONLY = set(sys.argv[2:])        # arm filter: a rebuild must not destroy a finished arm
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


def once_added(c_text, l_text, what):
    """L's text is C's text plus exactly one inserted line; returns (that line, its 1-based line number in L)."""
    ops = [op for op in difflib.SequenceMatcher(None, c_text.splitlines(), l_text.splitlines(), autojunk=False).get_opcodes() if op[0] != "equal"]
    assert len(ops) == 1, f"{what}: {len(ops)} differing regions, expected 1"
    tag, i1, i2, j1, j2 = ops[0]
    assert tag == "insert" and j2 - j1 == 1, f"{what}: the difference is {tag} of {j2 - j1} line(s), expected one inserted line"
    assert c_text.endswith("\n") == l_text.endswith("\n"), f"{what}: the final newline differs"
    return l_text.splitlines()[j1], j1 + 1


def git_show(path):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{REF}:{path}"], capture_output=True, check=True)
    return r.stdout


def seed_texts():
    """-> {cond: (rules bytes, BEMYAGENT.md bytes)}; asserts the C/L pair before anything is built"""
    c = ((ROOT / RULES_REL).read_bytes(), (ROOT / "BEMYAGENT.md").read_bytes())      # C: the working tree
    l = (git_show(RULES_REL), git_show("BEMYAGENT.md"))                              # L: the ref, as committed
    line_r, n_r = once_added(c[0].decode(), l[0].decode(), "00-ai-rules.md")
    line_b, n_b = once_added(c[1].decode(), l[1].decode(), "BEMYAGENT.md")
    assert line_r == line_b, "the added line differs between the rules file and BEMYAGENT.md"
    assert n_r == 2, f"the added line is line {n_r} of the rules file, not line 2"
    assert line_r.startswith("**Read this file whole"), "the added line does not start with `**Read this file whole`"
    assert len(kset.long_lines(c[0].decode())) == kset.K_SIZE, "K does not have 86 lines in the released rules file"
    got = hashlib.sha1(line_r.encode()).hexdigest()
    assert got == LINE_SHA1_EXPECTED, f"the sha1 of the added line is {got}, not the value fixed in 02_tasks.md B10"
    print(f"asserted: L = C + one line in each file, the same line, rules line {n_r}, BEMYAGENT.md line {n_b}")
    return {"C": c, "L": l}, hashlib.sha1(line_r.encode()).hexdigest(), n_r, n_b


def rev(ref):
    return subprocess.run(["git", "-C", str(ROOT), "rev-parse", ref], capture_output=True, text=True, check=True).stdout.strip()


OUT.mkdir(parents=True, exist_ok=True)
for a in ARMS:
    assert not (OUT / a).exists(), f"{a} already built - refusing to overwrite"
TEXTS, LINE_SHA1, N_R, N_B = seed_texts()
think_tpl = "## Context\n\n### Context Saturation Check\n- [ ] Target files/paths\n- [ ] Expected behavior\n- [ ] Constraints\n- [ ] Dependencies\n\n## Approaches Considered\n## Selected Approach & Risks\n### Pre-mortem\n### Devil's Advocate\n## Verification Plan\n"

for name, cond in ARMS.items():
    d = OUT / name
    rules, proto = TEXTS[cond]
    shutil.copytree(FIXTURE, d)
    (d / "BEMYAGENT.md").write_bytes(proto)
    (d / "CLAUDE.md").write_text(kset.SEED_CLAUDE_MD)
    bm = d / ".bemyagent"
    for sub in ("docs/decisions", "docs/specs", "docs/drafts", "work"):
        (bm / sub).mkdir(parents=True, exist_ok=True)
    (bm / "settings.json").write_text(json.dumps(SETTINGS, indent=2) + "\n")
    (bm / "docs" / "00-ai-rules.md").write_bytes(rules)
    for fn, body in DOCS.items(): (bm / "docs" / fn).write_text(body)
    for fn, body in TEMPLATES.items(): (bm / "docs" / fn).write_text(body)
    (bm / "work" / "_template_think.md").write_text(think_tpl)
    # the code map: identical in every arm
    (bm / "docs" / "03-code-map.md").write_text("# Code Map\n\n## Inventory\n" + H_SECTION + MAP_TAIL)
    subprocess.run(["git", "init", "-q"], cwd=d, check=True)
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "initial"], cwd=d, check=True)
    subprocess.run(["npm", "install", "--silent", "--no-audit", "--no-fund"], cwd=d, check=True)

for name in ARMS:
    d = OUT / name
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "-c", "user.email=h@x", "-c", "user.name=h",
                    "commit", "-qm", "code map"], cwd=d, check=True)
STATUS_DIR.mkdir(parents=True, exist_ok=True)
sp = STATUS_DIR / "setup.status"
old = [l for l in sp.read_text().splitlines() if l.startswith("arm ")] if sp.exists() else []
built = {l.split()[1]: l for l in old}
for name, cond in ARMS.items():
    built[name] = f"arm {name} cond={cond} rules_sha1={hashlib.sha1((OUT / name / RULES_REL).read_bytes()).hexdigest()} bemyagent_sha1={hashlib.sha1((OUT / name / 'BEMYAGENT.md').read_bytes()).hexdigest()}"
head = [f"repo_head={rev('HEAD')}", f"{REF.replace('/', '_').replace('.', '_')}={rev(REF)}", f"added_line_sha1={LINE_SHA1}",
        f"rules_line={N_R} bemyagent_line={N_B}"]
sp.write_text("\n".join(head + [built[k] for k in sorted(built)]) + "\n")
print(f"built {len(ARMS)} arms in {OUT}; status in {sp}")
