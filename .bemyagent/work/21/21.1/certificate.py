"""21.1 certificate — is each arm a clean control on all THREE of its calls, and did the turns
really arrive as designed? 20.12's reader, applied to t1, t2 and s2 of every arm:
  * instruction attachments: no instruction file outside the arm's own tree, no tool input naming
    the parent repository path, zero occurrences of the injected-override string (20.11 metric vi);
  * the first user message of turn 1 equals the stored prompt_t1 (ARM_DIR substituted);
  * the turn-2 sentence appears as a user message in the turn-2 transcript (and so does turn 1's
    task sentence: the resume carried the context);
  * session 2's first user message equals prompt_s2, and its session id differs from session 1's.
Output: JSON, numbers, booleans and file paths only - never transcript text.
Usage: certificate.py [arm ...]     R211_ROOT (arm trees), R211_OUT (launcher outputs), R211_CFG (config dir) override the defaults.
"""
import json, os, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
S = pathlib.Path(os.environ["BMA_SCRATCH"])      # the scratch directory of this round (the shell scripts export it from local.env)
R = pathlib.Path(os.environ.get("R211_ROOT") or S / "r211")          # the arm trees
OUT = pathlib.Path(os.environ.get("R211_OUT") or S / "r211_out")    # launcher outputs
TOOL_CFG = pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude")      # the tool's own variable
CFG = pathlib.Path(os.environ.get("R211_CFG") or TOOL_CFG) / "projects"
PARENT = str(pathlib.Path(os.environ.get("BMA_REPO") or pathlib.Path(__file__).resolve().parents[4]))
_HOME = pathlib.Path.home()
_CFG_NAME = re.escape(TOOL_CFG.relative_to(_HOME).parts[0] if TOOL_CFG.is_relative_to(_HOME) else TOOL_CFG.name)   # the config folder's own name, e.g. ".claude"
OVERRIDE = "OVERRIDE any default behavior"
# Tool inputs that name something belonging to the round's apparatus or the user's config: a call that
# reaches for them is a call that left the arm. `../` is counted apart (a `cd ..` after `cd client` is
# ordinary): reported for a hand-read, not gating.
NAMED = re.compile(r"\.memory\.s1|/snap/|\.(t1|t2|s2)\.(json|err)|launch\.status|" + _CFG_NAME + r"|CLAUDE_CONFIG_DIR|r211_out")
DOTDOT = re.compile(r"""(^|[\s"'=(;&|])\.\./""")
COND = {**{a: "K" for a in ("q103", "q104", "q105", "q900")},
        **{a: "E" for a in ("q106", "q107", "q108")},
        **{a: "R" for a in ("q109", "q110", "q111")}}
ALL_ARMS = ["q900", "q103", "q104", "q105", "q106", "q107", "q108", "q109", "q110", "q111"]
T1 = (HERE / "prompt_t1.txt").read_text()
T2 = (HERE / "prompt_t2.txt").read_text().strip()
S2 = (HERE / "prompt_s2.txt").read_text()
T1_TASK = next(l for l in T1.splitlines() if l.startswith("Task:"))


def norm(p):          # /tmp is a symlink to /private/tmp; a record may carry either spelling
    return "/private" + p if p.startswith("/tmp/") else p


def transcripts(sid):
    main = list(CFG.glob(f"*/{sid}.jsonl"))
    subs = [f for m in main for f in (m.parent / sid).rglob("*.jsonl")] if main else []
    return main, subs


def text_of(ev):
    m = (ev.get("message") or {}).get("content")
    return m if isinstance(m, str) else " ".join(x.get("text", "") for x in (m or [])
                                                  if isinstance(x, dict) and x.get("type") == "text")


def user_messages(f):
    out = []
    for line in f.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        if ev.get("type") == "user":
            out.append(text_of(ev))
    return out


def walk(f, arm_dir):
    instr, outside, parent_calls, override = [], [], 0, 0
    named = dotdot = foreign_att = 0
    own = re.sub(r"[^A-Za-z0-9]", "-", arm_dir)           # the arm's own project folder name
    other_arms = re.escape(str(R)) + r"/(?!" + re.escape(os.path.basename(arm_dir)) + r"(/|\b))"
    try: sibs = [d for d in os.listdir(R) if d != os.path.basename(arm_dir) and (R / d).is_dir()]
    except OSError: sibs = []
    rel_sibs = re.compile(r"\.\./(?:" + "|".join(re.escape(d) for d in sibs) + r")\b") if sibs else None   # `../q104`: a relative reach for a sibling arm
    for line in f.read_text(errors="replace").splitlines():
        override += line.count(OVERRIDE)
        try: ev = json.loads(line)
        except Exception: continue
        att = ev.get("attachment") or {}
        if ev.get("type") == "attachment" and att.get("type") == "instructions":
            for x in att.get("files") or []:
                p = norm(x.get("path", ""))
                instr.append(p)
                if not p.startswith(arm_dir + "/"): outside.append(p)
        elif ev.get("type") == "attachment":          # any other attachment naming a path outside the arm and its own project folder
            for q in re.findall(r'/(?:Users|private|tmp)/[^"\\\s]+', json.dumps(att)):
                if not norm(q).startswith(arm_dir) and ("/projects/" + own) not in q: foreign_att += 1
        msg = ev.get("message") or {}
        if ev.get("type") == "assistant" and isinstance(msg.get("content"), list):
            for c in msg["content"]:
                if c.get("type") == "tool_use":
                    s = json.dumps(c.get("input"))
                    if PARENT + "/" in s or s.rstrip('"}').endswith(PARENT):
                        parent_calls += 1
                    if NAMED.search(s) or re.search(other_arms, s) or str(OUT) in s or (rel_sibs and rel_sibs.search(s)):
                        named += 1
                    if DOTDOT.search(s):
                        dotdot += 1
    return instr, outside, parent_calls, override, named, dotdot, foreign_att


def context_tokens(f):
    """Prompt tokens (input + cache read + cache creation) of the last response before the turn-2 message
    and of the first response after it: a resume that really carried the context cannot shrink it."""
    before = after = None; seen = False
    for line in f.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        if ev.get("type") == "user" and T2 in text_of(ev):
            seen = True; continue
        u = (ev.get("message") or {}).get("usage") if ev.get("type") == "assistant" else None
        if not isinstance(u, dict): continue
        n = sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
        if not seen: before = n
        elif after is None: after = n
    return before, after


def call_row(arm, kind, arm_dir, sid):
    row = {"session": sid}
    main, subs = transcripts(sid) if sid else ([], [])
    row["transcripts"], row["subagent_transcripts"] = len(main), len(subs)
    row["transcript_files"] = [str(f) for f in main]
    agg = {"instruction_files": [], "outside_arm_dir": [], "parent_repo_tool_calls": 0, "override_header": 0,
           "tool_calls_naming_apparatus": 0, "tool_calls_dotdot": 0, "attachments_naming_foreign_paths": 0}
    for f in main + subs:
        i, o, p, ov, nm, dd, fa = walk(f, arm_dir)
        agg["instruction_files"] += i; agg["outside_arm_dir"] += o
        agg["parent_repo_tool_calls"] += p; agg["override_header"] += ov
        agg["tool_calls_naming_apparatus"] += nm; agg["tool_calls_dotdot"] += dd; agg["attachments_naming_foreign_paths"] += fa
    row.update(agg)
    row["instruction_records"] = len(agg["instruction_files"])
    # the arm's OWN CLAUDE.md is a legitimate instruction record and the CLI loads it under the OVERRIDE
    # header, which then appears twice per record (20.11: 2 per protocol call, 0 per bare call): the header is
    # contamination only beyond that (VERIFY B1). The cap is calibrated on one-call arms; a resumed call that
    # breaks the ratio fails closed.
    row["clean"] = (bool(main) and not agg["outside_arm_dir"] and agg["parent_repo_tool_calls"] == 0
                    and agg["override_header"] <= 2 * row["instruction_records"]
                    and agg["tool_calls_naming_apparatus"] == 0 and agg["attachments_naming_foreign_paths"] == 0)
    msgs = user_messages(main[0]) if main else []
    row["user_messages"] = len(msgs)
    if kind == "t1":
        row["first_user_equals_prompt_t1"] = bool(msgs) and msgs[0].strip() == T1.replace("<ARM_DIR>", arm_dir).strip()
    elif kind == "t2":
        row["t2_sentence_user_msgs"] = sum(T2 in m for m in msgs)
        row["t1_task_sentence_user_msgs"] = sum(T1_TASK in m for m in msgs)
        row["t2_sentence_is_a_user_message"] = row["t2_sentence_user_msgs"] >= 1
        row["context_carried"] = row["t1_task_sentence_user_msgs"] >= 1 and row["t2_sentence_is_a_user_message"]
        b, a = context_tokens(main[0]) if main else (None, None)
        row["prompt_tokens_before_t2"], row["prompt_tokens_after_t2"] = b, a
        row["model_context_not_smaller"] = None if b is None or a is None else a >= b      # True only if the model side shows it too
    else:
        row["first_user_equals_prompt_s2"] = bool(msgs) and msgs[0].strip() == S2.replace("<ARM_DIR>", arm_dir).strip()
        row["t1_task_sentence_user_msgs"] = sum(T1_TASK in m for m in msgs)       # must be 0: a reset, not a resume
    return row


def certify(arms):
    out = {}
    for arm in arms:
        arm_dir = str(R / arm)
        js = {k: OUT / f"{arm}.{k}.json" for k in ("t1", "t2", "s2")}
        row = {"cond": COND.get(arm, "?"), "arm_dir": arm_dir}
        sids = {}
        for k, p in js.items():
            try: sids[k] = json.loads(p.read_text()).get("session_id")
            except Exception: sids[k] = None
            if sids[k] is None:
                row[k] = {"status": "no launcher output", "file": str(p)}
            else:
                row[k] = call_row(arm, k, arm_dir, sids[k])
        row["t2_same_session_id_as_t1"] = bool(sids["t1"]) and sids["t1"] == sids["t2"]
        row["s2_session_differs_from_t1_and_t2"] = bool(sids["s2"]) and sids["s2"] not in (sids["t1"], sids["t2"])
        calls = [row[k] for k in ("t1", "t2", "s2")]
        row["calls_present"] = sum(1 for c in calls if "status" not in c)
        row["all_calls_clean"] = row["calls_present"] == 3 and all(c.get("clean") for c in calls)
        row["design_ok"] = bool(row["calls_present"] == 3 and row["t1"].get("first_user_equals_prompt_t1")
                                and row["t2"].get("context_carried") and row["s2"].get("first_user_equals_prompt_s2")
                                and row["s2"].get("t1_task_sentence_user_msgs") == 0
                                and row["s2_session_differs_from_t1_and_t2"])
        row["context_checked_by_tokens"] = bool(row["design_ok"] and (row["t2"].get("model_context_not_smaller") is True))
        out[arm] = row
    return out


if __name__ == "__main__":
    print(json.dumps(certify(sys.argv[1:] or ALL_ARMS), indent=1))
