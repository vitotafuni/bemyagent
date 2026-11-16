"""21.4 certificate - is each arm a clean control on all THREE of its calls (turn 1, the compaction, turn 2 on one
session), and did the calls arrive as designed? 21.1's certificate, adapted, with the defects its re-verification
(21.1/03g) left open closed here: N1 (the arm's OWN memory folder is counted, not gated), N2 (the token gate is
replaced by the boundary reading), N3 (spellings and routes that escaped: /tmp for /private/tmp, a bare `..`,
anything under the round's parent that is not this arm, a call whose cwd is outside the arm), N6 (the docstring
says what the code does: OVERRIDE headers are capped at two per instruction record, not forbidden).
Per arm, from the launcher's outputs and the arm's ONE transcript:
  * the same session id on the three calls (t1.json, the compaction stream, t2.json) and in the boundary record;
    exactly one transcript for it, in the arm's own project folder (arm path, non-alphanumerics -> '-');
  * every instruction record inside the arm's directory (or in the arm's own memory folder);
  * no tool call naming <repo> (BMA_REPO or this file's location) or the folder sessions start in (BMA_BASE; if it is
    unset the output says so and base_check_made is false - no layout is assumed);
  * no tool call or attachment that leaves the arm: the round's other files, its outputs, snapshots, the tool's config
    folder (except the arm's own memory), no event cwd outside the arm; `..` is counted apart (not gating);
  * the prompts sent equal the prompt files: turn 1's first user message and turn 2's user message by text, and all
    three by the hash the launcher wrote for what it passed; the compaction prompt file is `/compact` and nothing else;
  * the model as pinned on every call: every assistant record of the transcript's MAIN chain names `sonnet`. A second model
    in a call's modelUsage (a helper) is printed as second_model_in_usage and does not fail the arm (Amendment 1, A6).
  * `clean` is the AND of the named terms in clean_terms; a failing arm prints which term failed.
Output: JSON, numbers, booleans and file paths only - never transcript text.
Usage: certificate.py [--write-each] [arm ...]     (--write-each also writes <out>/<arm>.cert.json for read.py)  R214_ROOT (arm trees), R214_OUT (launcher outputs), R214_CFG (config dir) override the defaults.
"""
import hashlib, json, os, pathlib, posixpath, re, sys
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import boundary, kset                                              # noqa: E402

S = pathlib.Path(os.environ["BMA_SCRATCH"])      # the scratch directory of this round (the shell scripts export it from local.env)
R = pathlib.Path(os.environ.get("R214_ROOT") or S / "r214")          # the trees of the six
RP = pathlib.Path(os.environ.get("R214P_ROOT") or S / "r214p")       # the trees of the pilots (C4)
PILOTS = kset.pilots_from_env()
root_of = lambda arm: RP if arm in PILOTS else R
OUT = pathlib.Path(os.environ.get("R214_OUT") or S / "r214_out")    # launcher outputs
_HOME = pathlib.Path.home()
CFGS = []                                                          # every config folder this run may have touched
for _c in (os.environ.get("CLAUDE_CONFIG_DIR"), os.environ.get("R214_CFG")):
    if _c and pathlib.Path(_c) not in CFGS: CFGS.append(pathlib.Path(_c))
if not CFGS: CFGS.append(_HOME / ".claude")
PROJECTS = pathlib.Path(os.environ.get("R214_CFG") or os.environ.get("CLAUDE_CONFIG_DIR") or _HOME / ".claude") / "projects"
PARENT = str(pathlib.Path(os.environ.get("BMA_REPO") or HERE.parents[3]))     # <repo>
BASE = os.environ.get("BMA_BASE") or None                                      # the folder sessions start in
OVERRIDE = "OVERRIDE any default behavior"
COND = {**{a: "C" for a in ("q112", "q113", "q114", "q901", "q902", "q903")}, **{a: "L" for a in ("q115", "q116", "q117")}}
ALL_ARMS = ["q901", "q112", "q113", "q114", "q115", "q116", "q117"]
# things of the round's apparatus: a call that names them has left the arm. `../` is counted apart.
NAMED = re.compile(r"\.memory\.s1|/snap/|\.(t1|cp|t2)\.(json|jsonl|err)|launch\.status|CLAUDE_CONFIG_DIR|r214_out")
DOTDOT = re.compile(r"""(^|[\s"'=(;&|/])\.\.($|[/\s"';&|)])""")      # a `..` path component, bare or followed by /
CFG_ALTS = []
for _c in CFGS:
    CFG_ALTS.append(re.escape(str(_c)))
    if _c.is_relative_to(_HOME):
        CFG_ALTS.append(r"(?:~|\$HOME|\$\{HOME\})/" + re.escape(str(_c.relative_to(_HOME))))
CFG_ALTS.append(r"(?:~|\$HOME|\$\{HOME\})/\.claude\b")
CFGPAT = re.compile("(?:" + "|".join(CFG_ALTS) + r")[^\s\"'\\]*")
T1 = (HERE / "prompt_t1.txt").read_text()
T2 = (HERE / "prompt_t2.txt").read_text()
T1B = (HERE / "prompt_t1b.txt").read_text()
TC = (HERE / "prompt_compact.txt").read_text()
T1_TASK = next(l for l in T1.splitlines() if l.startswith("Task:"))


def norm(p):          # /tmp is a symlink to /private/tmp; a record may carry either spelling
    return re.sub(r"(?<!/private)/tmp/", "/private/tmp/", p)


def sha(text):        # what `printf %s "$(...)" | shasum -a 256` hashes: the text without trailing newlines
    return hashlib.sha256(text.rstrip("\n").encode()).hexdigest()


def text_of(ev):
    m = (ev.get("message") or {}).get("content")
    return m if isinstance(m, str) else " ".join(x.get("text", "") for x in (m or [])
                                                  if isinstance(x, dict) and x.get("type") == "text")


def is_prompt_record(ev):
    """a user record that carries a typed prompt: not a tool result, not meta, not the compaction summary"""
    if ev.get("type") != "user" or ev.get("isMeta") or ev.get("isCompactSummary"):
        return False
    c = (ev.get("message") or {}).get("content")
    return isinstance(c, str) or any(isinstance(x, dict) and x.get("type") == "text" for x in (c or []))


def status_tokens(arm):
    out = {}
    p = OUT / "launch.status"
    if p.exists():
        for line in p.read_text(errors="replace").splitlines():
            w = line.split()
            if w and w[0] == arm:
                for m in re.finditer(r"(\w+)=([^\s()]+)", line):
                    out[m.group(1)] = m.group(2)
    return out


def read_json(p):
    try: return json.loads(pathlib.Path(p).read_text())
    except Exception: return None


def stream_result(p):
    last = None
    for r in boundary.records(p):
        if isinstance(r, dict) and r.get("type") == "result": last = r
    return last


def stream_sid(p):
    sid = None
    for r in boundary.records(p):
        if isinstance(r, dict) and r.get("session_id"): sid = r["session_id"]
    return sid


def walk(f, arm_dir, split, sub=False):
    """counters for one transcript file, in two segments: records before the boundary (index < split) and from it on, and `where`: for
    each failing term the indexes of the records that made it fail (the index counts parsed records, as read.py's does; -1 for a
    subagent transcript, which cannot be placed against the window) - B8: read.py needs to know whether a failure lies after the window"""
    own = re.sub(r"[^A-Za-z0-9]", "-", arm_dir)                       # the arm's own project folder name
    own_mem = "/projects/" + own + "/memory"
    root = pathlib.Path(arm_dir).parent                              # the root this arm's tree stands in (pilots and the six stand apart)
    ROUND = str(root.parent)
    try: sibs = [d for d in os.listdir(root) if d != os.path.basename(arm_dir) and (root / d).is_dir()]
    except OSError: sibs = []
    rel_sibs = re.compile(r"\.\./(?:" + "|".join(re.escape(d) for d in sibs) + r")\b") if sibs else None   # `../q113`: a relative reach for a sibling
    names_repo = re.compile(re.escape(PARENT) + r"(?![A-Za-z0-9_.\-])")
    names_base = re.compile(re.escape(BASE) + r"(?![A-Za-z0-9_.\-])") if BASE else None
    z = lambda: {"instruction_files": [], "outside_arm_dir": [], "own_memory_instruction_files": 0, "parent_repo_tool_calls": 0,
                 "base_tool_calls": 0, "override_header": 0, "tool_calls_naming_apparatus": 0, "tool_calls_dotdot": 0,
                 "tool_calls_own_memory": 0, "attachments_naming_foreign_paths": 0, "foreign_attachment_types": {},
                 "events_cwd_outside_arm": 0, "assistant_records_not_sonnet": 0, "assistant_records": 0}
    seg = {"before": z(), "after": z()}
    where = {}
    mark = lambda term, i: where.setdefault(term, []).append(-1 if sub else i)
    idx = -1
    a = seg["before"]
    for line in f.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception:
            a["override_header"] += line.count(OVERRIDE)
            continue
        idx += 1
        a = seg["before"] if idx < split else seg["after"]
        a["override_header"] += line.count(OVERRIDE)
        if not isinstance(ev, dict): continue
        c = ev.get("cwd")
        if isinstance(c, str):
            c = norm(c)
            if not (c == arm_dir or c.startswith(arm_dir + "/")): a["events_cwd_outside_arm"] += 1; mark("no_event_cwd_outside_arm", idx)
        att = ev.get("attachment") or {}
        if ev.get("type") == "attachment" and att.get("type") == "instructions":
            for x in att.get("files") or []:
                p = norm(x.get("path", ""))
                a["instruction_files"].append(p)
                if p.startswith(arm_dir + "/"): continue
                if own_mem in p and any(str(cf) in p for cf in CFGS): a["own_memory_instruction_files"] += 1; continue
                a["outside_arm_dir"].append(p); mark("no_instruction_file_outside_arm", idx)
        elif ev.get("type") == "attachment":        # any other attachment naming a path outside the arm and its own project folder
            n = 0
            for q in re.findall(r'/(?:Users|private|tmp)/[^"\\\s]+', json.dumps(att)):
                if not norm(q).startswith(arm_dir) and ("/projects/" + own) not in q: n += 1
            if n:
                a["attachments_naming_foreign_paths"] += n; mark("no_attachment_naming_foreign_path", idx)
                t = str(att.get("type")) if re.fullmatch(r"[A-Za-z0-9_\-]{1,40}", str(att.get("type"))) else "<type>"
                a["foreign_attachment_types"][t] = a["foreign_attachment_types"].get(t, 0) + n
        msg = ev.get("message") or {}
        if ev.get("type") == "assistant" and not ev.get("isSidechain"):          # the pin is read on the main chain
            m = msg.get("model")
            if isinstance(m, str) and m != "<synthetic>":
                a["assistant_records"] += 1
                if "sonnet" not in m: a["assistant_records_not_sonnet"] += 1; mark("model_pinned_on_main_chain", idx)
        if ev.get("type") == "assistant" and isinstance(msg.get("content"), list):
            for c2 in msg["content"]:
                if not (isinstance(c2, dict) and c2.get("type") == "tool_use"): continue
                s = norm(json.dumps(c2.get("input")))
                if names_repo.search(s): a["parent_repo_tool_calls"] += 1; mark("no_tool_call_naming_repo", idx)
                if names_base and names_base.search(s): a["base_tool_calls"] += 1; mark("no_tool_call_naming_base", idx)
                hit = bool(NAMED.search(s)) or bool(rel_sibs and rel_sibs.search(s))
                for m2 in re.finditer(re.escape(ROUND) + r"(?:/[^\s\"'\\]*)?(?![A-Za-z0-9_.\-])", s):          # anything under the round's parent that is not this arm
                    p = posixpath.normpath(m2.group(0))
                    if own_mem in p and any(str(cf) in p for cf in CFGS): continue              # the arm's own memory folder (the config may sit under the round's parent in a dry-run)
                    if not (p == arm_dir or p.startswith(arm_dir + "/")): hit = True
                for m3 in CFGPAT.finditer(s):
                    if own_mem in m3.group(0): a["tool_calls_own_memory"] += 1
                    else: hit = True
                if hit: a["tool_calls_naming_apparatus"] += 1; mark("no_tool_call_naming_apparatus", idx)
                if DOTDOT.search(s): a["tool_calls_dotdot"] += 1
    seg["where"] = where
    return seg


def certify_arm(arm):
    arm_dir = str(root_of(arm) / arm)
    row = {"cond": COND.get(arm, "?"), "arm_dir": arm_dir}
    t1, t2 = read_json(OUT / f"{arm}.t1.json"), read_json(OUT / f"{arm}.t2.json")
    st = status_tokens(arm)
    four = "t1b_sha" in st                      # D1: the design with turn 1b; q901 ran under the three-call design, which is read as it was
    row["calls"] = 4 if four else 3
    t1b = read_json(OUT / f"{arm}.t1b.json") if four else None
    cp_path = OUT / f"{arm}.cp.jsonl"
    sids = {"t1": (t1 or {}).get("session_id"), "cp": stream_sid(cp_path), "t2": (t2 or {}).get("session_id")}
    if four: sids["t1b"] = (t1b or {}).get("session_id")
    row["session_ids_present"] = {k: bool(v) for k, v in sids.items()}
    sid = sids["t1"]
    # the compaction stream's own session id is information: if the stream carries none (a format this round has not seen)
    # the transcript still decides - one file, and the boundary record's sessionId below. A DIFFERENT id is a failure.
    row["cp_stream_session_equals_t1"] = None if sids["cp"] is None else sids["cp"] == sid
    row["same_session_id_on_all_three"] = bool(sid) and sids["t2"] == sid and sids["cp"] in (None, sid) and (not four or sids["t1b"] == sid)      # "all": every call of the design
    own = re.sub(r"[^A-Za-z0-9]", "-", arm_dir)
    mains = list(PROJECTS.glob(f"*/{sid}.jsonl")) if sid else []
    own_file = PROJECTS / own / f"{sid}.jsonl" if sid else None
    row["transcripts_total"] = len(mains)
    row["one_transcript_in_own_folder"] = bool(sid) and len(mains) == 1 and mains[0] == own_file
    row["transcript_files"] = [str(m) for m in mains]
    row["base_check_made"] = BASE is not None
    if BASE is None:
        row["base_check"] = "BMA_BASE is not set: tool calls were NOT checked against the folder sessions start in"
    if not row["one_transcript_in_own_folder"]:
        row["clean"] = False; row["design_ok"] = False; row["clean_terms"] = {"one_transcript_in_own_folder": False}; row["why"] = "no single transcript in the arm's own project folder"
        return row
    recs = boundary.records(own_file)          # P1: indexes as read.py counts them; a record that is not an object is skipped where its fields are read
    row["unparsed_lines"] = boundary.unparsed_lines(own_file)
    bidx = [i for i, r in enumerate(recs) if boundary.is_boundary(r)]
    split = bidx[-1] if bidx else len(recs)
    subs = list((own_file.parent / sid).rglob("*.jsonl")) if (own_file.parent / sid).is_dir() else []
    seg = walk(own_file, arm_dir, split)
    for f in subs:                                   # subagent transcripts: all their records count in the second segment
        s2 = walk(f, arm_dir, 0, sub=True)
        for t, l in s2["where"].items(): seg["where"].setdefault(t, []).extend(l)
        for k, v in s2["after"].items():
            if isinstance(v, list): seg["after"][k] += v
            elif isinstance(v, dict):
                for kk, vv in v.items(): seg["after"][k][kk] = seg["after"][k].get(kk, 0) + vv
            else: seg["after"][k] += v
    row["subagent_transcripts"] = len(subs)
    row["boundaries_in_transcript"] = len(bidx)
    row["boundary_session_id_equals_t1"] = bool(bidx) and all(recs[i].get("sessionId") == sid for i in bidx)
    row["segments"] = {k: v for k, v in seg.items() if k != "where"}
    tot = lambda k: seg["before"][k] + seg["after"][k]
    n_instr = len(seg["before"]["instruction_files"]) + len(seg["after"]["instruction_files"])
    row["instruction_records"] = n_instr
    row["tool_calls_own_memory"] = tot("tool_calls_own_memory")
    row["tool_calls_dotdot"] = tot("tool_calls_dotdot")          # C4: carried into read.py's row for each arm; a call through `..` is flagged there
    # the arm's own CLAUDE.md is a legitimate instruction record and the CLI loads it under the OVERRIDE header, which
    # then appears twice per record (20.11): contamination only beyond that. A compaction re-loads the file: more records.
    row["override_header_ok"] = tot("override_header") <= 2 * n_instr
    row["model_pinned"] = tot("assistant_records_not_sonnet") == 0 and tot("assistant_records") > 0
    models = {"t1": sorted(((t1 or {}).get("modelUsage") or {})), "cp": sorted(((stream_result(cp_path) or {}).get("modelUsage") or {})),
              "t2": sorted(((t2 or {}).get("modelUsage") or {}))}
    row["result_models"] = models
    # A6: a second model in a call's usage is REPORTED, it does not stop: the pin is the assistant records of the main chain.
    row["second_model_in_usage"] = sorted({m for ms in models.values() for m in ms if "sonnet" not in m})
    row["cp_model_usage_present"] = bool(models["cp"])
    terms = {"no_instruction_file_outside_arm": not (seg["before"]["outside_arm_dir"] + seg["after"]["outside_arm_dir"]),
             "no_tool_call_naming_repo": tot("parent_repo_tool_calls") == 0,
             "no_tool_call_naming_base": tot("base_tool_calls") == 0,
             "override_header_ok": row["override_header_ok"],
             "no_tool_call_naming_apparatus": tot("tool_calls_naming_apparatus") == 0,
             "no_attachment_naming_foreign_path": tot("attachments_naming_foreign_paths") == 0,
             "no_event_cwd_outside_arm": tot("events_cwd_outside_arm") == 0,
             "model_pinned_on_main_chain": row["model_pinned"]}
    row["clean_terms"] = terms
    row["fail_at"] = {t: sorted(set(seg["where"].get(t, []))) for t, ok in terms.items() if not ok and t in seg["where"]}    # record indexes (-1: a subagent); a term with no entry (override_header_ok) cannot be placed
    row["override_header_count"] = {"headers": tot("override_header"), "allowed": 2 * n_instr}
    row["clean"] = all(terms.values())
    # the prompts
    first = next((text_of(r) for r in recs if isinstance(r, dict) and is_prompt_record(r)), None)
    row["first_user_equals_prompt_t1"] = first is not None and first.rstrip("\n") == T1.replace("<ARM_DIR>", arm_dir).rstrip("\n")
    after = [text_of(r) for r in recs[split:] if isinstance(r, dict) and is_prompt_record(r)]
    before = [text_of(r) for r in recs[:split] if isinstance(r, dict) and is_prompt_record(r)]
    row["t2_prompt_is_a_user_message_after_boundary"] = any(m.rstrip("\n") == T2.rstrip("\n") for m in after) if bidx else False
    row["t1_task_sentence_before_boundary"] = any(T1_TASK in m for m in before)
    row["context_carried"] = row["t2_prompt_is_a_user_message_after_boundary"] and row["t1_task_sentence_before_boundary"]
    row["compact_prompt_file_is_exactly_/compact"] = TC.rstrip("\n") == "/compact"
    row["compact_command_recorded_after_boundary"] = any("/compact" in m for m in after)        # information only: the form is not documented
    want = {"t1_sha": sha(T1.replace("<ARM_DIR>", arm_dir)), "cp_sha": sha(TC), "t2_sha": sha(T2)}
    if four:
        want["t1b_sha"] = sha(T1B)
        row["t1b_prompt_is_a_user_message_before_boundary"] = any(m.rstrip("\n") == T1B.rstrip("\n") for m in before)
        t1b_ok = row["t1b_prompt_is_a_user_message_before_boundary"]
    else:
        t1b_ok = True
    row["launcher_prompt_hashes_equal_files"] = all(st.get(k) == v for k, v in want.items())
    row["design_ok"] = bool(row["same_session_id_on_all_three"] and row["boundary_session_id_equals_t1"] and bidx
                            and row["first_user_equals_prompt_t1"] and row["context_carried"]
                            and row["compact_prompt_file_is_exactly_/compact"] and row["launcher_prompt_hashes_equal_files"] and t1b_ok)
    return row


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--write-each"]
    out = {a: certify_arm(a) for a in (args or ALL_ARMS)}
    if "--write-each" in sys.argv[1:]:      # <out>/<arm>.cert.json, which read.py looks for
        OUT.mkdir(parents=True, exist_ok=True)
        for a, row in out.items(): (OUT / f"{a}.cert.json").write_text(json.dumps({a: row}, indent=1))
    print(json.dumps(out, indent=1))
