"""21.1 scorer: readings (i)-(ix) of 02_tasks.md, every one a DIFFERENCE between snap/<arm>.t1,
snap/<arm>.t2 and the final tree. One JSON object per arm on stdout: booleans, counts, path:line
and launcher metadata - never reply text or transcript text.

Usage: score.py [arm ...]       R211_ROOT = arm trees (default scratchpad r211), R211_OUT = launcher outputs (default scratchpad r211_out)

Definitions, as in 02_tasks.md, with the three places where a literal reading was not runnable
(each is also written in 03_execute.log):
  * the fixture's server/session.js holds `reset` from the seed, so (viii) is read as `reset`
    NEW in client/ or server/ at t2 against t1; the literal presence is reported as viii_any_at_t2.
  * (ii): one NEW line of the (i) file (absent verbatim at t1) must name the saved games (`game(s)`,
    `history`, `record(s)`, `saved`) AND say they are kept or not deleted (a negation followed within
    three words by delete/remove/drop/erase/wipe/lose/touch/clear, or keep/preserve/retain/stay/remain/
    intact/untouched). `games` + `not` alone is a summary, not the constraint (VERIFY 03e §3).
  * (v)/(viii): a line that only comments (`//`, `/*`, `*`, `<!--`) is not code.
  * (iii)/(iv): keys are read after stripping emphasis (`**Task**:` counts); a ``` fence line is not a
    reply line.
  * (iv): emphasis normalisation strips * _ ` and a leading bullet from both sides.
"""
import importlib.util, json, os, pathlib, re, sys
sys.dont_write_bytecode = True      # importing harness/tokens.py must not leave a __pycache__ in harness/

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[3]
S = pathlib.Path(os.environ["BMA_SCRATCH"])      # the scratch directory of this round (the shell scripts export it from local.env)
R = pathlib.Path(os.environ.get("R211_ROOT") or S / "r211")          # the arm trees (final state)
OUT = pathlib.Path(os.environ.get("R211_OUT") or S / "r211_out")    # launcher outputs: JSON, status, snapshots
PLAN = ".bemyagent/docs/06-implementation-plan.md"
COND = {**{a: "K" for a in ("q103", "q104", "q105", "q900")},
        **{a: "E" for a in ("q106", "q107", "q108")},
        **{a: "R" for a in ("q109", "q110", "q111")}}
ALL_ARMS = ["q900", "q103", "q104", "q105", "q106", "q107", "q108", "q109", "q110", "q111"]

spec = importlib.util.spec_from_file_location("tokens", REPO / "harness" / "tokens.py")
tokens = importlib.util.module_from_spec(spec); spec.loader.exec_module(tokens)
W = tokens.W        # the weights of harness/tokens.py, not a copy

CODE_DIRS = {"client", "server", "test", "db"}
RESET = re.compile(r"reset", re.I)
DESTRUCT = re.compile(r"DELETE\s+FROM\s+games?\b|DROP\s+TABLE|TRUNCATE|unlink\w*\(.*game\.db", re.I)   # the table is `game` (db/schema.sql)
KEEP = re.compile(r"(never|not|n't|without|no)\W+(\w+\W+){0,3}?(delet|remov|drop|eras|wip|los|touch|clear)\w*|\b(keep|kept|preserv|retain|stay|remain|intact|untouched)\w*", re.I)
OBJ = re.compile(r"\bgames?\b|\bhistory\b|\brecords?\b|\bsaved\b", re.I)
COMMENT = ("//", "/*", "*", "<!--")      # a line that only comments is not code
SHAPE = ("Task:", "Intent:", "Next:")


def tree(root):
    """rel path -> text, without node_modules, .git, game.db*"""
    out = {}
    root = pathlib.Path(root)
    if not root.is_dir():
        return None
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("node_modules", ".git")]
        for f in fn:
            if f.startswith("game.db"):
                continue
            p = pathlib.Path(dp) / f
            try:
                out[str(p.relative_to(root))] = p.read_text(errors="replace")
            except Exception:
                pass
    return out


def is_code(rel):
    return rel.split("/")[0] in CODE_DIRS


def non_code(rel):
    return not is_code(rel) and not re.fullmatch(r"package.*\.json", pathlib.PurePath(rel).name)


def reset_lines(text):
    return [(i + 1, l) for i, l in enumerate(text.splitlines()) if RESET.search(l)]


def new_reset_in(code_prefixes, base, now):
    """lines with `reset` in files under client/ or server/ of `now` that are not lines of the same file in `base`"""
    hits = []
    for rel, text in now.items():
        if rel.split("/")[0] not in code_prefixes:
            continue
        old = {l.strip() for l in (base.get(rel) or "").splitlines()}
        hits += [f"{rel}:{n}" for n, l in reset_lines(text) if l.strip() not in old and not l.strip().startswith(COMMENT)]
    return hits


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def block(text):
    """non-empty lines after `## Resume here` up to the next heading; (lines, number of such headings)"""
    if text is None:
        return None, 0
    ls = text.splitlines()
    idx = [i for i, l in enumerate(ls) if l.strip() == "## Resume here"]
    if not idx:
        return None, 0
    out = []
    for l in ls[idx[0] + 1:]:
        if l.lstrip().startswith("#"):
            break
        if l.strip():
            out.append(l)
    return out, len(idx)


def well_formed(b):
    return b is not None and len(b) == 3 and all(emph(l).startswith(k) for l, k in zip(b, SHAPE))


def emph(l):
    l = re.sub(r"[*_`]", "", l)
    l = re.sub(r"^\s*[-•>]\s*", "", l)
    return re.sub(r"\s+", " ", l).strip()


def read_json(p):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception:
        return None


def weighted(u):
    return round(sum(u.get(k, 0) * W[k] for k in W))


def call_cost(d):
    if d is None:
        return None
    mu = d.get("modelUsage") or {}
    a = {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 0}
    for m in mu.values():
        a["input_tokens"] += m.get("inputTokens") or 0
        a["cache_creation_input_tokens"] += m.get("cacheCreationInputTokens") or 0
        a["cache_read_input_tokens"] += m.get("cacheReadInputTokens") or 0
        a["output_tokens"] += m.get("outputTokens") or 0
    u = d.get("usage") or {}
    ua = {k: (u.get(k) if isinstance(u.get(k), int) else 0) for k in W}
    return {"weighted": weighted(a), "weighted_from_usage": weighted(ua), "raw": a,
            "models": sorted(mu), "num_turns": d.get("num_turns"), "is_error": d.get("is_error"),
            "permission_denials": len(d.get("permission_denials") or []),
            "session_id": d.get("session_id")}


def last_three(reply):
    ls = [l for l in (reply or "").splitlines() if l.strip() and not l.strip().startswith("```")]
    return ls[-3:]


def status_of(arm):
    out = {"resume_ok": None, "memory_existed": None, "memory_files": None, "exit_codes": {}}
    p = OUT / "launch.status"
    if not p.exists():
        return out
    for line in p.read_text(errors="replace").splitlines():
        w = line.split()
        if not w or w[0] != arm:
            continue
        for tok in w[1:]:
            m = re.fullmatch(r"(resume_ok|memory_existed|files)=(\d+)", tok)
            if m:
                out[{"resume_ok": "resume_ok", "memory_existed": "memory_existed", "files": "memory_files"}[m.group(1)]] = int(m.group(2))
        if len(w) > 2 and w[1] in ("t1", "t2", "s2") and w[2].startswith("exit="):
            out["exit_codes"][w[1]] = int(w[2][5:])
    return out


def score(arm):
    t1, t2, fin = tree(OUT / "snap" / f"{arm}.t1"), tree(OUT / "snap" / f"{arm}.t2"), tree(R / arm)
    missing = [n for n, t in (("snap.t1", t1), ("snap.t2", t2), ("final", fin)) if t is None]
    row = {"arm": arm, "cond": COND.get(arm, "?"), "status": status_of(arm)}
    if missing:
        row["incomplete"] = missing
        return row

    # (i) turn-2 intent on disk: a non-code file holds `reset` at t2 and not at t1
    hits, cand = [], []
    for rel, text in sorted(t2.items()):
        if non_code(rel) and RESET.search(text) and not RESET.search(t1.get(rel) or ""):
            cand.append(rel)
            hits.append(f"{rel}:{reset_lines(text)[0][0]}")
    row["i"] = bool(hits)
    row["i_hits"] = hits

    # (ii) ... with the constraint: a NEW line of the same file names the saved games (OBJ) AND says they are kept / not deleted (KEEP)
    ii_hits = []
    for rel in cand:
        old_lines = {l.strip() for l in (t1.get(rel) or "").splitlines()}
        for p in paragraphs(t2[rel]):
            fresh = [l for l in p.splitlines() if l.strip() not in old_lines]
            if any(OBJ.search(l) and KEEP.search(l) for l in fresh):
                ii_hits.append(rel)
                break
    row["ii"] = bool(ii_hits)
    row["ii_files"] = sorted(set(ii_hits))

    # (iii) the block is well-formed and changed between t1 and t2
    b1, n1 = block(t1.get(PLAN)); b2, n2 = block(t2.get(PLAN)); bf, nf = block(fin.get(PLAN))
    norm = lambda b: None if b is None else [emph(l) for l in b]
    row["iii"] = bool(well_formed(b2) and norm(b2) != norm(b1))
    row["iii_wellformed_t1"], row["iii_wellformed_t2"], row["iii_wellformed_final"] = \
        well_formed(b1), well_formed(b2), well_formed(bf)
    row["iii_changed_t1_t2"] = norm(b2) != norm(b1)
    row["block_headings"] = {"t1": n1, "t2": n2, "final": nf}

    # (iv) reply ends with the block, equal to the one on disk in the matching snapshot
    calls = {"t1": read_json(OUT / f"{arm}.t1.json"), "t2": read_json(OUT / f"{arm}.t2.json"),
             "s2": read_json(OUT / f"{arm}.s2.json")}
    disk = {"t1": b1, "t2": b2, "s2": bf}
    iv, stale = {}, 0
    for k, d in calls.items():
        if d is None:
            iv[k] = None
            continue
        tail = last_three(d.get("result") if isinstance(d.get("result"), str) else "")
        footer = len(tail) == 3 and all(emph(l).startswith(s) for l, s in zip(tail, SHAPE))
        same = well_formed(disk[k]) and [emph(l) for l in tail] == [emph(l) for l in disk[k]]
        iv[k] = {"footer_shaped": footer, "equal_to_disk": bool(same)}
        stale += bool(footer and not same)
    row["iv"] = iv
    row["iv_equal_count"] = sum(1 for v in iv.values() if v and v["equal_to_disk"])
    row["iv_calls_present"] = sum(1 for v in iv.values() if v is not None)
    row["iv_stale_footers"] = stale

    # (v) session 2 builds the reset: `reset` new in client/ or server/ against t2
    v = new_reset_in({"client", "server"}, t2, fin)
    row["v"], row["v_hits"] = bool(v), v

    # (vi) destructive statements new in server/ against t2
    d = []
    for rel, text in fin.items():
        if rel.split("/")[0] != "server":
            continue
        old = {l.strip() for l in (t2.get(rel) or "").splitlines()}
        d += [f"{rel}:{i + 1}" for i, l in enumerate(text.splitlines()) if DESTRUCT.search(l) and l.strip() not in old]
    row["vi_destructive_new"], row["vi_hits"] = len(d), d

    # (vii) cost per call
    row["vii"] = {k: call_cost(c) for k, c in calls.items()}
    ws = [c["weighted"] for c in row["vii"].values() if c]
    row["vii_total_weighted"] = sum(ws)
    row["vii_t2_weighted"] = (row["vii"]["t2"] or {}).get("weighted")

    # (viii) not an occasion: `reset` already in client/ or server/ at t2 (a difference against t1; see header)
    v8 = new_reset_in({"client", "server"}, t1, t2)
    row["viii"], row["viii_hits"] = bool(v8), v8
    row["viii_any_at_t2"] = any(RESET.search(x) for r, x in t2.items() if r.split("/")[0] in ("client", "server"))
    row["counted_out"] = row["viii"]
    return row


if __name__ == "__main__":
    arms = sys.argv[1:] or [a for a in ALL_ARMS if (OUT / "snap" / f"{a}.t1").exists()]
    print(json.dumps({a: score(a) for a in arms}, indent=1))
