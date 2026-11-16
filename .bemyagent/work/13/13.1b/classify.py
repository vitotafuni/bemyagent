"""13.1b — every unit of 00-ai-rules.md, three-way, judged by verifiability x cost x cost-of-failure.

Classes: P procedural (tied to a forced action or an inspectable artifact), D declarative (a
disposition with no artifact), N non-rule (reference data, config semantics, definitions, rationale).
Cost is an estimate, chars/4, applied identically to every unit; only the ratios are read.
Evidence is what the record holds, found by grep over docs/, work/ and the commit log - "none"
means none was found, not that the rule is inert.
Verdicts: KEEP; TRIM (non-rule text removable on inspection, 13.3's precedent); KEEP-untested
(declarative, never measured either way, low cost of failure - each was a cut candidate and each
failed its own overlap or cost check, recorded per unit in the evidence column).
"""
import os
import pathlib, sys
RULES = (pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4]) / ".bemyagent" / "docs" / "00-ai-rules.md").read_text().splitlines()
U = [  # id, section, name, lines, class, V, F, evidence, verdict
 (1,"1","Self-Registration",(3,15),"P","high","high","sentinel obeyed by 58/118 arms (20.10); CLAUDE.md precedence landed in 15.1 (#3)","KEEP"),
 (2,"2.0","Pending upgrade",(18,18),"P","high","high","19.5 UPGRADE rounds","KEEP"),
 (3,"2.0","UNPOPULATED search",(19,19),"P","high","high","Decision 17","KEEP"),
 (4,"2.1","Quick Resume",(20,20),"P","med","med","none in isolation","KEEP"),
 (5,"2.2","Full Restore",(21,21),"P","med","med","none in isolation","KEEP"),
 (6,"3","Lazy-load prohibition",(24,24),"D","med","low","none","KEEP"),
 (7,"3","Precedence rules>plan>memory",(25,25),"D","low","high","landed 15.5 (#7c); occasion never measured","KEEP"),
 (8,"3","Routing Table",(26,35),"N","n/a","high","consumed by the Write Gate (Decision 13)","KEEP"),
 (9,"3","Conceptual maps",(37,37),"D","high","med","decisions: map shape entries","KEEP"),
 (10,"3","Context Slicing",(39,39),"D","med","low","13.2 INCONCLUSIVE; 14.3 gave it an occasion nobody scored; semantics of the live key contextSlicingThreshold, which a cut would leave meaningless","KEEP-untested"),
 (11,"3","Conversation log",(41,41),"N","high","low","rationale inline on purpose (05 L229), and it is the only way the reason travels: BEMYAGENT.md ships to projects without this repo's 05","KEEP"),
 (12,"3","Write Gate",(43,47),"P","high","med","Decision 13; 19.3: 6/6 arms emit PROTOCOL_CHECK, 55% of governed files named","KEEP"),
 (13,"4","HTN structure",(50,51),"N","high","med","every round's work/ tree","KEEP"),
 (14,"4","Decomposition",(52,52),"D","low","med","none; overlaps Delivers re-cut (L64) and depth cap (L51)","KEEP-untested"),
 (15,"4","Ceremony sizing + CDM",(54,60),"P","high","high","13.4; every round since","KEEP"),
 (16,"4","THINK (with the TTEV-files header)",(62,63),"P","high","high","20.8: Verification Plan predicts the artifact 6/6","KEEP"),
 (17,"4","TASK",(64,64),"P","high","high","Delivers line, every round","KEEP"),
 (18,"4","EXECUTE (incl. redact secrets)",(65,65),"P","high","high","the 13.1b canonical case: 13 tokens, unverifiable, keep","KEEP"),
 (181,"4","VERIFY pointer",(66,66),"N","n/a","low","points at Symbiotic Validation","KEEP"),
 (19,"4","Handoff Principle",(67,67),"D","high","med","20.9 null, fixture-limited; enforced by Git (L80)","KEEP"),
 (20,"4","Symbiotic Validation",(69,72),"P","high","high","13.5; 15.5 (#6)","KEEP"),
 (21,"4","Who verifies",(73,73),"P","high","high","15.8; 5/6 arms ran an independent VERIFY, unscored; 20.10's verifier moved 49->58","KEEP"),
 (22,"4","Autonomous rigor",(74,74),"D","low","high","Decision 15, never measured in isolation","KEEP"),
 (23,"4","strictVerification depth",(75,75),"N","n/a","low","config semantics","KEEP"),
 (24,"4","Pacing",(77,77),"N","high","high","config semantics + STOP","KEEP"),
 (25,"4","Model switching",(78,78),"N","low","low","config semantics; no round exercised it","KEEP"),
 (26,"4","Git",(80,80),"P","high","med","every round's commit order","KEEP"),
 (27,"5","Read before modify",(83,83),"D","high","high","harness-enforced in most CLIs","KEEP"),
 (28,"5","Label inferences",(84,84),"D","med","med","none that isolates it: 20.9's 3/3 split was about where the documents came from","KEEP"),
 (29,"5","User premises",(85,85),"D","med","high","decisions: 3/3 spot-checked a fabricated premise","KEEP"),
 (30,"5","New dependency",(86,86),"P","high","med","none in isolation","KEEP"),
 (31,"5","Critical Review Protocol",(87,87),"P","med","med","decisions: guarantee-3 entry","KEEP"),
 (32,"6","Surgical scope",(90,90),"D","high","med","13.2: one accidental occasion","KEEP"),
 (33,"6","Brevity",(91,91),"D","med","low","13.2 INCONCLUSIVE; overlap with harness defaults seen on Claude Code only","KEEP-untested"),
 (34,"6","Language",(92,92),"N","n/a","low","config semantics","KEEP"),
 (35,"6","Glossary use",(93,93),"D","med","low","its declarative sibling (P3) measured 0/8","KEEP-untested"),
 (36,"6","Unpopulated 01 guard",(94,94),"P","high","high","Decision 17","KEEP"),
 (37,"6","Discussion capture",(95,95),"P","high","med","drafts/ writes","KEEP"),
 (38,"6","CRITICAL same-response",(96,96),"P","high","high","Milestone 11: 7-8/8 against 0/8 declarative","KEEP"),
 (39,"6","specs/ milestone done",(97,97),"P","high","med","none in isolation","KEEP"),
 (40,"7","Migration",(100,101),"P","high","high","UPGRADE rounds","KEEP"),
 (41,"8","Multi-Agent Parallelism",(104,107),"P","high","med","none: no round ever ran parallel worktrees; 13.3 already relocated the human-choice part (dispatch); steps 2-3 guard shared docs","KEEP-untested"),
]
VER = {9: "P", 10: "N", 11: "P", 13: "P", 19: "P", 24: "P", 27: "P", 32: "P"}  # VERIFY's reading, 04_verify.md

def tok(a, b): return round(len("\n".join(RULES[a-1:b])) / 4)
covered = set()
for u in U: covered |= set(range(u[3][0], u[3][1] + 1))
uncovered = [i for i, l in enumerate(RULES, 1) if l.strip() and not l.startswith("#") and i not in covered
             and l.strip() not in ("```",) and not l.startswith("|---")]
print("| # | § | unit | lines | class | VERIFY's class | verifiable | cost (tok) | cost of failure | evidence | verdict |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
agg = {}
for i, s, n, (a, b), c, v, f, e, d in U:
    t = tok(a, b); agg.setdefault(c, [0, 0]); agg[c][0] += 1; agg[c][1] += t
    vc = VER.get(i, c)
    print(f"| {i} | {s} | {n} | {a}-{b} | {c} | {'**' + vc + '**' if vc != c else vc} | {v} | {t} | {f} | {e} | **{d}** |")
total = sum(x[1] for x in agg.values())
print()
for c in "PDN": print(f"{c}: {agg[c][0]} units, {agg[c][1]} tok, {100*agg[c][1]/total:.0f}%")
print(f"total classified: {total} tok over {len(U)} units")
va = {}
for u in U:
    c = VER.get(u[0], u[4]); va.setdefault(c, [0, 0]); va[c][0] += 1; va[c][1] += tok(*u[3])
print("under VERIFY's classes: " + " · ".join(f"{c} {va[c][0]} units {va[c][1]} tok {100*va[c][1]/total:.0f}%" for c in "PDN"))
print(f"disputed: {len(VER)} of {len(U)} units, {sum(tok(*u[3]) for u in U if u[0] in VER)} tok")
q = [u for u in U if u[8] == "KEEP-untested"]; t_ = [u for u in U if u[8] == "TRIM"]
print(f"KEEP-untested: {len(q)} units, {sum(tok(*u[3]) for u in q)} tok — " + ", ".join(u[2] for u in q))
print(f"TRIM : {len(t_)} units, {sum(tok(*u[3]) for u in t_)} tok — " + ", ".join(u[2] for u in t_))
print("non-blank, non-heading lines NOT covered by any unit:", uncovered)
