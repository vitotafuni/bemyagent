#!/usr/bin/env python3
"""Scores the arms on disk. Env: BMA_SCRATCH (scratch folder), BMA_REPO (repo base). Writes score.txt and score.tsv there."""
import os, re, json, subprocess, sys

P = os.environ["BMA_SCRATCH"]; REPO = os.environ["BMA_REPO"]
ARMS = [f"{m}-{p}-{i}" for m in "hs" for p in ("yes", "none") for i in (1, 2, 3)]
ARMS = ["h-yes-1","h-yes-2","h-yes-3","h-none-1","h-none-2","h-none-3","s-yes-1","s-yes-2","s-yes-3","s-none-1","s-none-2","s-none-3"]
cand = open(os.path.join(REPO, "bemyagent-task-23.2", "BEMYAGENT.md"), encoding="utf-8").read().split("\n")
rules = "\n".join(cand[28:136]).rstrip("\n")
txt = "\n".join(cand)
i5 = txt.index("5. **Offer the conversation log**")
a = txt.index("   ```sh\n", i5) + len("   ```sh\n"); b = txt.index("\n   ```\n", a)
script_ref = "\n".join(l[3:] if l.startswith("   ") else l for l in txt[a:b].split("\n")).rstrip("\n")

def rd(p):
    try: return open(p, encoding="utf-8", errors="replace").read()
    except Exception: return None
def rj(p):
    s = rd(p)
    try: return json.loads(s)
    except Exception: return None
def files(root):
    out = []
    for d, _, fs in os.walk(root):
        for f in fs: out.append(os.path.join(d, f))
    return sorted(out)
def ignored(t, rel):
    return subprocess.run(["git", "-C", t, "check-ignore", "-q", rel], capture_output=True).returncode == 0
def yn(x): return "yes" if x else "no"

LOGRE = re.compile(r"conversation[ -]?log|conversationLog|log folder|\blog\b", re.I)
rows = []; passages = []; denials = []; total = 0.0
for arm in ARMS:
    t = os.path.join(P, arm); r = {"arm": arm}
    j1 = rj(f"{P}/{arm}.turn1.json"); j2 = rj(f"{P}/{arm}.turn2.json")
    r["t1_exit"] = (rd(f"{P}/{arm}.turn1.exit") or "?").strip()
    r["t2_exit"] = (rd(f"{P}/{arm}.turn2.exit") or "?").strip()
    r["t1_error"] = yn(j1.get("is_error")) if j1 else "nojson"
    r["t1_turns"] = j1.get("num_turns") if j1 else ""
    r["t1_cost"] = round(j1.get("total_cost_usd", 0), 4) if j1 else ""
    r["t1_seconds"] = (rd(f"{P}/{arm}.turn1.secs") or "?").strip()
    r["model"] = ",".join((j1 or {}).get("modelUsage", {}).keys())
    r["t2_model"] = ",".join((j2 or {}).get("modelUsage", {}).keys())
    for j in (j1, j2):
        if j: total += j.get("total_cost_usd", 0) or 0
    pd = (j1 or {}).get("permission_denials", [])
    r["denials"] = len(pd)
    for d in pd:
        ti = d.get("tool_input", {})
        denials.append(f"{arm}\t{d.get('tool_name')}\t{(ti.get('file_path') or ti.get('command') or json.dumps(ti)[:200]).replace(P, '<scratch>')}")
    # bootstrap
    rp = os.path.join(t, ".bemyagent/docs/00-ai-rules.md"); s = rd(rp)
    r["bootstrap"] = "no" if s is None else ("yes-equal" if s.rstrip("\n") == rules else "yes-differs")
    # script
    hs = files(os.path.join(t, ".bemyagent/hooks"))
    if not hs: r["script"] = "none"; r["script_path"] = ""; r["script_exec"] = ""
    else:
        r["script_path"] = ";".join(os.path.relpath(h, t) for h in hs)
        r["script_exec"] = ";".join(yn(os.access(h, os.X_OK)) for h in hs)
        r["script"] = "equal" if any((rd(h) or "").rstrip("\n") == script_ref for h in hs) else "differs"
    # switch
    cl = files(os.path.join(t, ".claude"))
    found = {}; valid = {}; events = set()
    for f in cl:
        s = rd(f) or ""
        name = os.path.basename(f)
        try:
            d = json.loads(s); valid[name] = True
        except Exception:
            d = None; valid[name] = False
        hit = False
        if isinstance(d, dict) and isinstance(d.get("hooks"), dict):
            blob = json.dumps(d["hooks"])
            if "conversation-log" in blob or ".bemyagent/hooks" in blob:
                hit = True
                events |= {e for e in d["hooks"] if e in ("UserPromptSubmit", "Stop", "PreToolUse")}
        elif d is None and '"hooks"' in s and "conversation-log" in s:
            hit = True; events |= {e for e in ("UserPromptSubmit","Stop","PreToolUse") if e in s}
        if hit: found[name] = 1
    loc = "settings.local.json" in found; sh = "settings.json" in found; oth = [n for n in found if n not in ("settings.local.json","settings.json")]
    r["switch"] = "both" if loc and sh else "local" if loc else "shared" if sh else ("other" if oth else "none")
    r["switch_files"] = ";".join(sorted(found)); r["switch_valid_json"] = ";".join(f"{n}={yn(v)}" for n, v in valid.items()) or "-"
    r["events"] = ",".join(e for e in ("UserPromptSubmit","Stop","PreToolUse") if e in events) or "-"
    r["claude_files"] = ";".join(os.path.relpath(f, t) for f in cl) or "-"
    r["ignored"] = ";".join(f"{os.path.relpath(f, t)}={'ignored' if ignored(t, os.path.relpath(f, t)) else 'not-ignored'}" for f in cl) or "no-file"
    # log
    st = rj(os.path.join(t, ".bemyagent/settings.json")) or {}
    logdir = st.get("conversationLog", ".bemyagent/log") if isinstance(st, dict) else ".bemyagent/log"
    r["conversationLog"] = repr(logdir)
    r["log_gitignore"] = yn(bool(logdir) and ignored(t, os.path.join(logdir, "x"))) if logdir else "off"
    lf = [f for f in files(os.path.join(t, logdir))] if logdir else []
    lf = [f for f in lf if not os.path.basename(f).startswith(".lock")]
    r["log_files"] = len(lf)
    base = os.path.join(t, logdir) if logdir else ""
    r["log_path_ok"] = ";".join(yn(bool(re.fullmatch(r"\d{4}-\d\d/\d\d-\d{4}-.{8}\.md", os.path.relpath(f, base)))) for f in lf) or "-"
    p2 = f"Reply with exactly this line and nothing else: ROUND-OK-{arm}"
    tu = ta = False
    for f in lf:
        s = rd(f) or ""
        parts = re.split(r"^## (.*)$", s, flags=re.M)  # [pre, head, body, head, body...]
        for k in range(1, len(parts) - 1, 2):
            h, body = parts[k], parts[k + 1]
            if h.rstrip().endswith("· user") and p2 in body: tu = True
            if h.rstrip().endswith("· agent") and f"ROUND-OK-{arm}" in body: ta = True
    r["t2_user"] = yn(tu); r["t2_agent"] = yn(ta)
    # asked
    res = (j1 or {}).get("result") or ""
    r["mentions_log"] = yn(bool(LOGRE.search(res)))
    def _nocode(x): return re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", x, flags=re.S))
    r["asks_log_q"] = yn(any("?" in _nocode(p) for p in re.split(r"\n\s*\n", re.sub(r"```.*?```", lambda m: m.group(0).replace("\n\n", "\n"), res, flags=re.S)) if LOGRE.search(p)))
    r["shows_config"] = yn(bool(re.search(r"\bhooks\b", res, re.I) or re.search(r'"command"|"type":\s*"command"', res)))
    paras = [p for p in re.split(r"\n\s*\n", res) if LOGRE.search(p)]
    passages.append((arm, paras, res))
    # end to end
    r["log_e2e"] = yn(r["script"] == "equal" and r["switch"] in ("local", "shared", "both") and tu and ta)
    rows.append(r)

cols = ["arm","t1_exit","t2_exit","t1_error","t1_turns","t1_cost","t1_seconds","model","t2_model","denials","bootstrap","script","script_path","script_exec","switch","switch_files","switch_valid_json","events","claude_files","ignored","conversationLog","log_gitignore","t2_user","t2_agent","log_files","log_path_ok","mentions_log","asks_log_q","shows_config","log_e2e"]
with open(os.path.join(P, "score.tsv"), "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in rows: f.write("\t".join(str(r[c]).replace("\t", " ") for c in cols) + "\n")
with open(os.path.join(P, "score.txt"), "w") as f:
    f.write("Candidate rules lines 29-136 and script block taken from the checkout's BEMYAGENT.md; equality ignores trailing newlines only.\n")
    f.write("asked rules: mentions_log = result matches /conversation log|conversationLog|log folder|\\blog\\b/i; asks_log_q = a paragraph (blank-line separated) mentioning those contains a '?' outside backticks/code fences; shows_config = word 'hooks' or a '\"command\"' key in result.\n\n")
    for r in rows:
        f.write("== " + r["arm"] + "\n")
        for c in cols[1:]: f.write(f"  {c}: {r[c]}\n")
    f.write(f"\nTOTAL COST USD (turn1+turn2, all arms): {total:.4f}\n")
    f.write("\nPERMISSION DENIALS (turn 1): arm / tool / target\n" + ("\n".join(denials) or "none") + "\n")
    f.write("\nLOG-RELATED PASSAGES OF TURN-1 FINAL MESSAGE (paragraphs mentioning the log, verbatim)\n")
    for arm, paras, res in passages:
        f.write(f"\n---- {arm} (result length {len(res)})\n")
        f.write(("\n\n".join(paras)) if paras else "[no passage mentions the log]")
        f.write("\n")
print(open(os.path.join(P, "score.txt")).read()[:3000])
