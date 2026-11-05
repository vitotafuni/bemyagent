"""19.2b — routing read from what Step 0 left on disk, never from what an arm says it did."""
import json, pathlib, re, subprocess, sys
R = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/scratchpad/r192b")
T = pathlib.Path("<tmp>/<project-key>/"
                 "<session-id>/tasks")
SIDE = {"q40": "A", "q41": "B", "q42": "A", "q43": "B", "q44": "A", "q45": "B"}
AGENT = {"q40": "<agent-id>", "q41": "<agent-id>",
         "q42": "<agent-id>", "q43": "<agent-id>",
         "q44": "<agent-id>", "q45": "<agent-id>"}
SCAFFOLD = ["docs/00-ai-rules.md"] + [f"docs/0{i}-" for i in range(1, 7)]
WANT_TEMPLATES = ["docs/decisions/_template.md", "docs/specs/_template.md",
                  "docs/drafts/_template.md", "work/_template_think.md"]
# words an arm uses when it reaches the gate and goes past it
OVERRIDE = re.compile(r"override|overrode|skip(?:ped|ping)? the STOP|deviat|proceed(?:ed)? without "
                      r"approval|no user to approve|cannot wait", re.I)

def texts(agent_id):
    p = T / (agent_id + ".output")
    if not p.exists(): return ""
    out = []
    for line in p.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        msg = ev.get("message") or {}
        if msg.get("role") != "assistant": continue
        for b in msg.get("content") or []:
            if isinstance(b, dict):
                if b.get("type") == "text": out.append(b.get("text") or "")
                elif b.get("type") == "tool_use": out.append(json.dumps(b.get("input") or {}))
    return "\n".join(out)

res = {}
ONLY = set(sys.argv[1:])
for arm, side in SIDE.items():
    if ONLY and arm not in ONLY: continue
    d = R / arm
    if not d.exists(): continue
    bm = d / ".bemyagent"
    docs = sorted(x.name for x in (bm / "docs").glob("*.md")) if (bm / "docs").exists() else []
    tests = subprocess.run(["npm", "test"], cwd=d, capture_output=True, text=True)
    tout = tests.stdout + tests.stderr
    blob = texts(AGENT.get(arm, ""))
    res[arm] = {
      "side": side,
      # (i) routing, from artifacts only
      "upgrade_plan_left": (bm / "upgrade-plan.md").exists(),
      "upgrade_log": sorted(x.name for x in (bm / "work").glob("upgrade-*.log")) if (bm/"work").exists() else [],
      "upgrade_plan_named_in_transcript": "upgrade-plan.md" in blob,  # prose, not disk
      # (i-b) the branch recorded IN THE ARM'S OWN DOCS, which is where an arm that takes
      # UPGRADE and proceeds without the STOP leaves its only on-disk trace
      "upgrade_decided_in_docs": sorted(
          str(x.relative_to(d)) for x in (bm / "docs").rglob("*.md")
          # 00-ai-rules.md is protocol-owned and generated verbatim: its §2 names
          # upgrade-plan.md, so it matches in every arm and evidences nothing
          if (bm / "docs").exists() and x.name != "00-ai-rules.md" and re.search(
              r"(UPGRADE|upgrade)[^\n]{0,200}(stop|STOP|approv)|"
              r"(stop|STOP)[^\n]{0,200}(UPGRADE|upgrade)",
              x.read_text(errors="replace"))),
      # (ii) the stop, with the confound attached
      "override_language": sorted(set(m.group(0).lower() for m in OVERRIDE.finditer(blob)))[:6],
      # (iii) scaffold
      "docs": docs,
      "templates_present": [t for t in WANT_TEMPLATES if (bm / t).exists()],
      "rules_file": (bm / "docs" / "00-ai-rules.md").exists(),
      "sentinel_registered": any((d / f).exists() and "00-ai-rules.md" in (d / f).read_text()
                                 for f in ("CLAUDE.md", "AGENTS.md")),
      # (iv) settings
      "settings": {k: json.loads((bm / "settings.json").read_text()).get(k)
                   for k in ("obstacleThreshold", "contextSlicingThreshold")},
      # (v) delivery
      "tests": re.findall(r"^. (?:pass|fail) \d+", tout, re.M),
      "scoreboard": bool(re.search(r"score", (d/"client"/"index.html").read_text(), re.I)),
    }
print(json.dumps(res, indent=1))
