#!/usr/bin/env python3
"""Score the 15.11 round. Extraction is deterministic; the verdict is a human read.

Emits each arm's relevant passages under an anonymous label so the condition is not
visible while scoring. The key is written separately and read only after the verdict.
"""
import hashlib, json, pathlib, re, sys

OUT = pathlib.Path(sys.argv[1])
COND = {"w1": "a/false", "w2": "a/false", "w3": "a/false",
        "w4": "b/true", "w5": "b/true", "w6": "b/true"}

# the two decisions verified open in the fixture before the task was written
D1 = re.compile(r"\b(who (goes|moves|starts)|first (move|player|turn)|goes first|"
                r"starts? the rematch|alternat\w*|loser starts|swap)", re.I)
D2 = re.compile(r"\b(new (game|row|record)|reset|same game|re-?use|fresh game|"
                r"new record|separate game)", re.I)
# an announcement of the stop, which the rubric says scores nothing
STOP = re.compile(r"\b(approv\w+|sign-?off|await\w*|pause|interactive mode|"
                  r"stop for|human review|your go-ahead)", re.I)

rows, key = [], {}
for arm in sorted(COND):
    p = OUT / arm / ".bemyagent" / "work"
    hits = sorted(p.rglob("01_think.md")) if p.exists() else []
    label = hashlib.sha256(arm.encode()).hexdigest()[:6]
    key[label] = {"arm": arm, "cond": COND[arm]}
    if not hits:
        rows.append({"label": label, "think": None})
        continue
    text = hits[0].read_text()
    lines = text.splitlines()
    def ctx(rx):
        return [l.strip() for l in lines if rx.search(l) and l.strip()]
    rows.append({
        "label": label,
        "think": str(hits[0]),
        "lines": len(lines),
        "decision_1_first_move": ctx(D1),
        "decision_2_new_vs_reset": ctx(D2),
        "stop_announcements": len(ctx(STOP)),
    })

print(json.dumps(rows, indent=2))
(OUT / "_key.json").write_text(json.dumps(key, indent=2) + "\n")
print(f"\nkey written to {OUT}/_key.json (read only after scoring)", file=sys.stderr)
