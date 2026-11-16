#!/usr/bin/env python3
"""21.2 census: of the sessions that read 00-ai-rules.md through a tool call, how many had
all numbered sections (## 1. .. ## 8.) in tool results before their first file-changing call?

Stdlib only. Streams every *.jsonl under ROOT. Emits numeric aggregates and transcript basenames only;
it never prints or stores transcript text (tool results are scanned in memory for headings/markers).

Usage:  python3 census.py [--root DIR] [--out FILE] [--control]
"""
import json, os, pathlib, re, sys, shlex, subprocess, collections, argparse

ROOT = str(pathlib.Path(os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude") / "projects")      # the tool's own CLAUDE_CONFIG_DIR
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REPO_FOLDER = re.sub(r"[^A-Za-z0-9]", "-", os.environ.get("BMA_REPO") or REPO)      # the tool's folder name for the repo path
POS_CONTROL = "<session-id>.jsonl"
NEED = set(range(1, 9))

PATH_RE = re.compile(r"00-ai-rules\.md(?![\w.\-])")
HEAD_RE = re.compile(r"^[ \t]*(?:\d+[ \t]*[→\t:][ \t]*)?##[ \t]+(\d+)\.", re.M)
HEAD_TITLE_RE = re.compile(r"^[ \t]*(?:\d+[ \t]*[→\t:][ \t]*)?##[ \t]+(\d+)\.[ \t]*(.*)$", re.M)
# truncation signs (first one found in the positive control; the rest are other signs Claude Code is known to emit)
TRUNC_PATTERNS = {
    "mid_marker": re.compile(r"\.\.\. \[\d+ (?:characters?|chars|lines?|bytes) truncated\]"),
    "persisted_output": re.compile(r"<persisted-output>"),
    "output_too_large": re.compile(r"Output too large"),
    "full_output_saved": re.compile(r"Full output saved to"),
    "read_token_limit": re.compile(r"exceeds maximum allowed tokens"),
    "bracket_truncated": re.compile(r"\[(?:output |content )?truncated[^\]]*\]", re.I),
    "lines_truncated": re.compile(r"\(\s*\d+ (?:more )?lines? truncated\)|\(truncated\)", re.I),
}
WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
PRINT_CMDS = {"cat", "bat", "nl", "less", "more", "tac", "pr"}
SLICE_CMDS = {"head", "tail", "cut", "grep", "egrep", "fgrep", "rg", "ag", "awk", "gawk", "sed", "sort",
              "uniq", "tr", "column", "fold", "expand", "perl"}
PASS_CMDS = {"cd", "time", "sudo", "command", "env", "exec", "nohup", "do", "then", "else", "if", "while"}
OPS = {"&&", "||", ";", "|", "&", ";;", "|&"}
WRITE_CMDS = {"tee", "mkdir", "rm", "mv", "cp"}


# ---------------------------------------------------------------- bash parsing
def strip_heredocs(cmd):
    out, term = [], None
    for ln in cmd.split("\n"):
        if term is not None:
            if ln.strip() == term:
                term = None
            continue
        out.append(ln)
        m = re.search(r"<<-?\s*['\"]?(\w+)['\"]?", ln)
        if m:
            term = m.group(1)
    return "\n".join(out)


def join_continuations(cmd):
    return re.sub(r"\\\n", " ", cmd)


def tokenize_line(ln):
    try:
        lex = shlex.shlex(ln, posix=True, punctuation_chars=True)
        lex.whitespace_split = False
        lex.commenters = ""
        return list(lex)
    except ValueError:
        return ln.split()


def parse_pipelines(cmd):
    """-> list of pipelines; a pipeline is a list of stages; a stage = dict(words, redir_out, redir_targets)."""
    cmd = join_continuations(strip_heredocs(cmd))
    pipelines = []
    for ln in cmd.split("\n"):
        ln = ln.strip()
        if not ln:
            continue
        toks = tokenize_line(ln)
        stages, cur, redir, pipeline, i = [], [], False, [], 0
        targets = []

        def end_stage():
            nonlocal cur, redir, targets
            if cur or redir:
                pipeline.append({"words": cur, "redir_out": redir, "targets": targets})
            cur, redir, targets = [], False, []

        def end_pipeline():
            nonlocal pipeline
            end_stage()
            if pipeline:
                pipelines.append(pipeline)
            pipeline = []

        while i < len(toks):
            t = toks[i]
            if t in ("|", "|&"):
                end_stage()
            elif t in OPS:
                end_pipeline()
            elif re.fullmatch(r"[0-9]*>{1,2}|&>{1,2}|>\|", t) or re.fullmatch(r"[<>&|;()]+", t) and ">" in t:
                # output redirection; drop the target token
                if t.endswith("&") and t != "&>":      # fd dup like 2>&1 : '>&' then '1'
                    i += 1
                else:
                    tgt = toks[i + 1] if i + 1 < len(toks) else ""
                    if tgt != "/dev/null":
                        redir = True
                        targets.append(tgt)
                    i += 1
            elif t in ("<", "<<", "<<<", "<<-"):
                i += 1
            elif re.fullmatch(r"[0-9]", t) and i + 1 < len(toks) and re.fullmatch(r">{1,2}|>&|&>", toks[i + 1]):
                pass     # file-descriptor number in front of a redirection
            elif t in ("(", ")", "{", "}"):
                pass
            else:
                cur.append(t)
            i += 1
        end_pipeline()
    return pipelines


def stage_cmd(stage):
    ws = list(stage["words"])
    while ws:
        w = ws[0]
        if w in PASS_CMDS or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", w):
            ws = ws[1:]
            if w == "cd" and ws:
                ws = ws[1:]      # drop cd's argument
            continue
        break
    return (os.path.basename(ws[0]) if ws else ""), ws


def classify_bash(cmd, depth=0):
    """-> (kind, first_words_of_path_stage) ; kind in bash-alone/bash-chained/slice/other"""
    pls = parse_pipelines(cmd)
    path_kinds = []        # kinds of pipelines that touch the path
    other_output = 0       # pipelines that are not cd/echo-less no-ops and don't touch the path
    nfiles_in_print = 0
    for pl in pls:
        touches = any(PATH_RE.search(w) for st in pl for w in st["words"])
        redir_to_path = any(PATH_RE.search(t) for st in pl for t in st["targets"])
        # bash -c "..." : recurse on the inner string
        handled_inner = False
        for st in pl:
            c, ws = stage_cmd(st)
            if c in ("bash", "sh", "zsh", "eval") and depth < 2:
                for a in ws[1:]:
                    if PATH_RE.search(a) and (" " in a or ";" in a or "&" in a or "|" in a):
                        k, _ = classify_bash(a, depth + 1)
                        path_kinds.append(("inner", k))
                        handled_inner = True
        if handled_inner:
            continue
        if not touches:
            cs = [stage_cmd(st)[0] for st in pl]
            if all(c == "" for c in cs):
                continue                 # pure `cd`
            other_output += 1
            continue
        # which stage names the path, and what is the last stage?
        cs = [stage_cmd(st) for st in pl]
        pstages = [i for i, st in enumerate(pl) if any(PATH_RE.search(w) for w in st["words"])]
        first = pstages[0]
        c0, ws0 = cs[first]
        last_c = cs[-1][0]
        if redir_to_path or pl[-1]["redir_out"] and last_c in PRINT_CMDS | SLICE_CMDS | {""}:
            path_kinds.append(("pl", "other"))          # path is a write target / output goes to a file
            continue
        if c0 in PRINT_CMDS or (c0 == "git" and len(ws0) > 1 and ws0[1] == "show"):
            k = "print"
            nfile = sum(1 for w in ws0[1:] if not w.startswith("-") and not re.fullmatch(r"\d+", w) and w not in ("--", "show"))
            nfiles_in_print = max(nfiles_in_print, nfile)
            if len(pl) > 1:
                if last_c in SLICE_CMDS:
                    k = "slice"
                elif last_c in ("wc", "md5", "md5sum", "shasum", "sha256sum", "cksum", "xargs", "test", "diff", "cmp"):
                    k = "other"
                elif last_c in PRINT_CMDS or last_c == "tee":
                    k = "print"
                else:
                    k = "unknown_pipe"
            path_kinds.append(("pl", k))
        elif c0 in SLICE_CMDS:
            if c0 == "sed" and any(w.startswith("-i") or w == "--in-place" for w in ws0[1:]):
                path_kinds.append(("pl", "other"))
            else:
                k = "slice"
                if len(pl) > 1 and last_c in ("wc",):
                    k = "other"
                path_kinds.append(("pl", k))
        elif c0 == "" and first > 0:       # path only appears in a later stage, first stage is something else
            path_kinds.append(("pl", "slice" if last_c in SLICE_CMDS else "other"))
        else:
            path_kinds.append(("pl", "other"))       # wc, ls, stat, git, cp, mv, rm, python, echo, test ...
    kinds = [k for _, k in path_kinds]
    if "inner" in [t for t, _ in path_kinds]:
        # use the recursive classification of the inner string, merged with the outer context
        inner = [k for t, k in path_kinds if t == "inner"]
        for k in inner:
            if k in ("bash-alone", "bash-chained"):
                return ("bash-chained" if (other_output or nfiles_in_print > 1 or len(path_kinds) > 1) else k), None
        kinds = [k for t, k in path_kinds if t == "pl"] + [("slice" if k == "slice" else "other") for k in inner]
    if any(stage_cmd(st)[0] in ("diff", "cmp", "comm") for pl in pls for st in pl if any(PATH_RE.search(w) for w in st["words"])
           or any(stage_cmd(s2)[0] in ("diff", "cmp", "comm") for s2 in pl) and any(PATH_RE.search(w) for s3 in pl for w in s3["words"])):
        return "other", None
    prints = [k for k in kinds if k in ("print", "unknown_pipe")]
    if prints:
        if len(kinds) == 1 and prints[0] == "print" and other_output == 0 and nfiles_in_print <= 1:
            return "bash-alone", None
        return "bash-chained", None
    if "slice" in kinds:
        return "slice", None
    return "other", None


def bash_writes(cmd):
    """Heuristic: does this Bash command plainly write a file?"""
    why = None
    for pl in parse_pipelines(cmd):
        for st in pl:
            if st["redir_out"]:
                return "redirect"
            c, ws = stage_cmd(st)
            if c in WRITE_CMDS:
                return c
            if c == "sed" and any(w.startswith("-i") or w == "--in-place" for w in ws[1:]):
                return "sed-i"
            if c == "git" and len(ws) > 1 and ws[1] == "commit":
                return "git-commit"
    if re.search(r"open\([^)]*,\s*['\"][wa]b?\+?['\"]|\.write_text\(|\.write_bytes\(|\bjson\.dump\(", cmd):
        return "python-write"
    return None


# ---------------------------------------------------------------- results
def result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(x.get("text", "") for x in content if isinstance(x, dict))
    return ""


def load_known_titles():
    """(N, normalised title prefix) pairs from the rules file's own git history (for the 'titled' sensitivity)."""
    known = collections.defaultdict(set)
    try:
        revs = subprocess.run(["git", "-C", REPO, "log", "--format=%h", "--", ".bemyagent/docs/00-ai-rules.md"],
                              capture_output=True, text=True, timeout=60).stdout.split()
        for r in revs:
            txt = subprocess.run(["git", "-C", REPO, "show", r + ":.bemyagent/docs/00-ai-rules.md"],
                                 capture_output=True, text=True, timeout=60).stdout
            for m in re.finditer(r"^##\s+(\d+)\.\s*(.*)$", txt, re.M):
                known[int(m.group(1))].add(m.group(2).strip()[:10].lower())
    except Exception:
        pass
    return known


KNOWN_TITLES = load_known_titles()
NOTFOUND_RE = re.compile(r"No such file or directory|File does not exist|ENOENT")
NOTFOUND_FLAG = []


def scan_result(text):
    nums = {int(m.group(1)) for m in HEAD_RE.finditer(text)}
    titled = set()
    for m in HEAD_TITLE_RE.finditer(text):
        n = int(m.group(1))
        if m.group(2).strip()[:10].lower() in KNOWN_TITLES.get(n, ()):
            titled.add(n)
    signs = [name for name, rx in TRUNC_PATTERNS.items() if rx.search(text)]
    if NOTFOUND_RE.search(text) and not nums:
        NOTFOUND_FLAG.append(1)
    return nums, titled, signs


# ---------------------------------------------------------------- per-transcript scoring
def session_kind(rel):
    parts = rel.split(os.sep)
    folder = parts[0]
    if "-private-tmp-" in folder or "scratchpad" in folder:
        return "arm"
    if folder == REPO_FOLDER:
        return "repo-main" if len(parts) == 2 else "repo-subagent"
    return "other"


def group_key(rel):
    folder = rel.split(os.sep)[0]
    return re.sub(r"-q\d+$", "", folder).replace("-<session-id>", "")


def classify_access(name, inp):
    if name == "Read":
        fp = inp.get("file_path", "")
        if PATH_RE.search(fp or ""):
            partial = inp.get("offset") not in (None, 0) or inp.get("limit") not in (None,)
            return "read-partial" if partial else "read-whole"
        return "other"
    if name == "Bash":
        return classify_bash(inp.get("command", ""))[0]
    if name == "Grep":
        return "slice"
    return "other"          # Edit/Write/Glob/Agent/... mention the path but do not read it


def scan_transcript(path):
    rec = {"first_ts": None, "accesses": [], "first_write_idx": None, "first_write_type": None, "no_result": 0,
           "first_write_idx_ns": None, "first_bash_other_words": []}
    seen, pending = set(), {}
    done_results = set()
    for idx, line in enumerate(open(path, "r", errors="replace")):
        if '"type":"api-request' in line[:60] or '"type":"file-history' in line[:60]:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        if rec["first_ts"] is None and isinstance(o.get("timestamp"), str):
            rec["first_ts"] = o["timestamp"]
        m = o.get("message")
        if not isinstance(m, dict) or not isinstance(m.get("content"), list):
            continue
        for b in m["content"]:
            if not isinstance(b, dict):
                continue
            t = b.get("type")
            if t == "tool_use":
                tid = b.get("id")
                if tid in seen:
                    continue
                seen.add(tid)
                name, inp = b.get("name"), b.get("input") or {}
                if not isinstance(inp, dict):
                    inp = {}
                wt = None
                if name in WRITE_TOOLS:
                    wt = name
                elif name == "Bash":
                    wt = bash_writes(inp.get("command", "") or "")
                if wt:
                    if rec["first_write_idx"] is None:
                        rec["first_write_idx"], rec["first_write_type"] = idx, wt
                    if rec["first_write_idx_ns"] is None:
                        txt = (inp.get("file_path") or inp.get("notebook_path") or "") if name in WRITE_TOOLS else (inp.get("command") or "")
                        scratch = (re.search(r"^\s*(?:cd\s+|[A-Za-z_]+=)\S*(?:/private/tmp|/tmp|scratchpad)", txt) if name == "Bash" else re.search(r"^(?:/private/tmp|/tmp)/|scratchpad", txt))
                        if not scratch:
                            rec["first_write_idx_ns"] = idx
                try:
                    blob = json.dumps(inp)
                except Exception:
                    blob = ""
                if PATH_RE.search(blob):
                    kind = classify_access(name, inp)
                    if name == "Bash" and kind == "other":
                        _, w0 = (lambda pl: stage_cmd(next((st for p in pl for st in p if any(PATH_RE.search(w) for w in st["words"])), {"words": []})))(parse_pipelines(inp.get("command", "") or ""))
                        rec["first_bash_other_words"].append((w0[0] if w0 else "?")[:20])
                    a = {"tool": name, "kind": kind, "use_idx": idx, "res_idx": None, "sections": set(),
                         "titled": set(), "signs": [], "is_error": None, "notfound": False}
                    rec["accesses"].append(a)
                    pending[tid] = a
            elif t == "tool_result":
                tid = b.get("tool_use_id")
                if tid in pending and tid not in done_results:
                    done_results.add(tid)
                    a = pending[tid]
                    a["res_idx"] = idx
                    a["is_error"] = b.get("is_error")
                    del NOTFOUND_FLAG[:]
                    a["sections"], a["titled"], a["signs"] = scan_result(result_text(b.get("content")))
                    a["notfound"] = bool(NOTFOUND_FLAG)
    rec["no_result"] = sum(1 for a in rec["accesses"] if a["res_idx"] is None)
    return rec


def score(rec, ruler=NEED):
    reads = [a for a in rec["accesses"] if a["kind"] != "other"]
    fw = rec["first_write_idx"]
    out = {"accessed": bool(reads)}
    if not reads:
        return out
    first = reads[0]
    out["first_access_kind"] = first["kind"]
    out["first_access_sections"] = sorted(first["sections"])
    strict = [a for a in reads if a["res_idx"] is not None and (fw is None or a["res_idx"] < fw)]
    lenient = [a for a in reads if (fw is None or a["use_idx"] < fw)]
    u = set().union(*[a["sections"] for a in strict]) if strict else set()
    ul = set().union(*[a["sections"] for a in lenient]) if lenient else set()
    ut = set().union(*[a["titled"] for a in strict]) if strict else set()
    uw = set().union(*[a["sections"] for a in strict if a["kind"] in ("read-whole", "bash-alone", "bash-chained")]) if strict else set()
    out["sections_before_first_write"] = sorted(u)
    out["complete"] = ruler <= u
    out["complete_lenient"] = ruler <= ul
    out["complete_titled"] = ruler <= ut
    out["complete_whole_print_only"] = ruler <= uw
    fns = rec["first_write_idx_ns"]
    strict_ns = [a for a in reads if a["res_idx"] is not None and (fns is None or a["res_idx"] < fns)]
    uns = set().union(*[a["sections"] for a in strict_ns]) if strict_ns else set()
    out["complete_ignoring_scratch_writes"] = ruler <= uns
    out["complete_ever"] = ruler <= set().union(*[a["sections"] for a in reads])
    out["n_reads_before_first_write"] = len(strict)
    out["all_pre_write_reads_notfound"] = bool(strict) and all(a["notfound"] for a in strict)
    out["missing"] = sorted(ruler - u)
    out["trunc_any_read"] = any(a["signs"] for a in reads)
    out["first_access_trunc"] = bool(first["signs"])
    out["any_slice_before_first_write"] = any(a["kind"] in ("slice", "read-partial") for a in strict)
    out["has_write"] = fw is not None
    out["n_reads"] = len(reads)
    return out


def inc_label(rec, sc):
    """for an incomplete session: truncation sign on a reading access that preceded the first write, vs slice only."""
    fw = rec["first_write_idx"]
    pre = [a for a in rec["accesses"] if a["kind"] != "other" and (fw is None or a["use_idx"] < fw)]
    sign = any(a["signs"] for a in pre if a["kind"] in ("read-whole", "bash-alone", "bash-chained"))
    deliberate = any(a["kind"] in ("slice", "read-partial") for a in pre)
    if sign and deliberate:
        return "both"
    if sign:
        return "truncation-sign"
    if deliberate:
        return "slice-only"
    return "neither"


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--out", default=os.path.join(HERE, "03b_census.json"))
    ap.add_argument("--window-start", default="2026-05-26")
    ap.add_argument("--control", action="store_true", help="print only the positive-control access sequence")
    ap.add_argument("--debug-other", action="store_true")
    ap.add_argument("--exclude", action="append", default=[], help="basename of a transcript to leave out (e.g. the census agent's own)")
    args = ap.parse_args()

    files = []
    for dp, dn, fn in os.walk(args.root):
        for f in fn:
            if f.endswith(".jsonl"):
                files.append(os.path.join(dp, f))
    files.sort()
    excluded = [f for f in files if os.path.basename(f) in args.exclude]
    files = [f for f in files if os.path.basename(f) not in args.exclude]
    recs = {}
    for p in files:
        if args.control and os.path.basename(p) != POS_CONTROL:
            continue
        recs[p] = scan_transcript(p)

    if args.control:
        for p, r in recs.items():
            print("control transcript:", os.path.basename(p), "first_ts:", r["first_ts"], "first_write_idx:",
                  r["first_write_idx"], r["first_write_type"])
            print_sequence(r)
            print(score(r))
        return

    scanned = len(files)
    kinds = ["repo-main", "repo-subagent", "arm", "other"]
    inwin = {k: [] for k in kinds}
    outside, no_ts = 0, 0
    for p, r in recs.items():
        rel = os.path.relpath(p, args.root)
        ts = r["first_ts"]
        if ts is None:
            no_ts += 1
            continue
        if ts[:10] < args.window_start:
            outside += 1
            continue
        inwin[session_kind(rel)].append((rel, r))

    # groups: determine a per-group ruler from untruncated whole prints (diagnostic for rounds with a cut file)
    gsec = collections.defaultdict(lambda: {"sessions": set(), "ruler": set(), "wholes": 0, "any": set()})
    for k in kinds:
        for rel, r in inwin[k]:
            g = gsec[(k, group_key(rel))]
            g["sessions"].add(rel)
            for a in r["accesses"]:
                if a["kind"] != "other":
                    g["any"] |= a["sections"]
                if a["kind"] in ("read-whole", "bash-alone") and not a["signs"] and a["sections"]:
                    g["ruler"] |= a["sections"]
                    g["wholes"] += 1
    short_groups = {key for key, g in gsec.items() if g["wholes"] >= 2 and not (NEED <= g["ruler"])}

    result = {"scanned": scanned, "window_start": args.window_start, "outside_window": outside,
              "no_timestamp": no_ts, "excluded_basenames": [os.path.basename(f) for f in excluded], "in_window": sum(len(v) for v in inwin.values()),
              "by_kind": {}, "short_ruler_groups": [], "incomplete_sessions": [], "per_group": {}}
    result["required_sections"] = sorted(NEED)
    tot_acc = tot_not = 0
    for k in kinds:
        rows = inwin[k]
        acc, notacc = [], 0
        by = {"in_window": len(rows), "accessed": 0, "not_accessed": 0, "complete": 0, "incomplete": 0,
              "complete_lenient": 0, "complete_titled": 0, "complete_whole_print_only": 0,
              "first_access_kind": collections.Counter(), "trunc_any_read": 0, "first_access_trunc": 0,
              "missing_sections_in_incomplete": collections.Counter(),
              "incomplete_cause": collections.Counter(), "other_access_only": 0,
              "accessed_but_no_result": 0, "short_ruler": {"accessed": 0, "complete_vs_group_ruler": 0, "incomplete_vs_group_ruler": 0},
              "complete_by_first_access_kind": collections.Counter(), "incomplete_by_first_access_kind": collections.Counter(),
              "had_write": 0, "complete_ignoring_scratch_writes": 0,
              "incomplete_no_read_before_first_write": 0, "incomplete_partial_read_before_first_write": 0,
              "partial_cause": collections.Counter(), "partial_missing_sections": collections.Counter(),
              "partial_by_first_access_kind": collections.Counter(), "partial_with_truncation_sign": 0,
              "partial_deliberate_slice_only": 0, "partial_all_reads_file_not_found": 0, "incomplete_but_complete_ever_in_session": 0,
              "incomplete_never_complete_in_session": 0, "complete_ignoring_scratch_writes_total": 0}
        other_words = collections.Counter()
        for rel, r in rows:
            gk = (k, group_key(rel))
            ruler = NEED
            is_short = gk in short_groups
            if is_short:
                ruler = gsec[gk]["ruler"]
            sc = score(r, ruler)
            for w in r["first_bash_other_words"]:
                other_words[w] += 1
            if not sc["accessed"]:
                by["not_accessed"] += 1
                if r["accesses"]:
                    by["other_access_only"] += 1
                continue
            by["accessed"] += 1
            if r["no_result"]:
                by["accessed_but_no_result"] += 1
            if is_short:
                by["short_ruler"]["accessed"] += 1
                by["short_ruler"]["complete_vs_group_ruler" if sc["complete"] else "incomplete_vs_group_ruler"] += 1
                continue                       # counted separately, not in the main complete/incomplete tallies
            by["first_access_kind"][sc["first_access_kind"]] += 1
            by["trunc_any_read"] += int(sc["trunc_any_read"])
            by["first_access_trunc"] += int(sc["first_access_trunc"])
            by["had_write"] += int(sc["has_write"])
            by["complete_ignoring_scratch_writes"] += int(sc["complete_ignoring_scratch_writes"])
            by["complete_lenient"] += int(sc["complete_lenient"])
            by["complete_titled"] += int(sc["complete_titled"])
            by["complete_whole_print_only"] += int(sc["complete_whole_print_only"])
            if sc["complete"]:
                by["complete"] += 1
                by["complete_by_first_access_kind"][sc["first_access_kind"]] += 1
            else:
                by["incomplete"] += 1
                by["incomplete_by_first_access_kind"][sc["first_access_kind"]] += 1
                for n in sc["missing"]:
                    by["missing_sections_in_incomplete"][str(n)] += 1
                cause = inc_label(r, sc)
                by["incomplete_cause"][cause] += 1
                by["incomplete_but_complete_ever_in_session" if sc["complete_ever"] else "incomplete_never_complete_in_session"] += 1
                if sc["n_reads_before_first_write"] == 0:
                    by["incomplete_no_read_before_first_write"] += 1
                else:
                    by["incomplete_partial_read_before_first_write"] += 1
                    by["partial_cause"][cause] += 1
                    by["partial_by_first_access_kind"][sc["first_access_kind"]] += 1
                    by["partial_with_truncation_sign"] += int(cause in ("truncation-sign", "both"))
                    by["partial_deliberate_slice_only"] += int(cause == "slice-only")
                    by["partial_all_reads_file_not_found"] += int(sc["all_pre_write_reads_notfound"])
                    for n in sc["missing"]:
                        by["partial_missing_sections"][str(n)] += 1
                result["incomplete_sessions"].append({"basename": os.path.basename(rel), "kind": k,
                                                      "first_access_kind": sc["first_access_kind"],
                                                      "missing": sc["missing"], "cause": cause,
                                                      "had_write": sc["has_write"],
                                                      "reads_before_first_write": sc["n_reads_before_first_write"]})
        for key in ("first_access_kind", "missing_sections_in_incomplete", "incomplete_cause",
                    "complete_by_first_access_kind", "incomplete_by_first_access_kind", "partial_cause",
                    "partial_missing_sections", "partial_by_first_access_kind"):
            by[key] = dict(sorted(by[key].items()))
        by["bash_other_access_first_words"] = dict(other_words.most_common(25))
        # arithmetic checks per kind
        main_acc = by["accessed"] - by["short_ruler"]["accessed"]
        by["check_accessed_plus_not_eq_inwindow"] = by["accessed"] + by["not_accessed"] == by["in_window"]
        by["check_complete_plus_incomplete_eq_accessed_excl_short"] = by["complete"] + by["incomplete"] == main_acc
        result["by_kind"][k] = by
        tot_acc += by["accessed"]
        tot_not += by["not_accessed"]
    result["totals"] = {"accessed": tot_acc, "not_accessed": tot_not,
                        "check_accessed_plus_not_eq_in_window": tot_acc + tot_not == result["in_window"],
                        "check_in_window_plus_outside_plus_nots_eq_scanned": result["in_window"] + outside + no_ts == scanned}
    for (k, g), v in sorted(gsec.items()):
        result["per_group"][f"{k}|{g}"] = {"sessions": len(v["sessions"]), "untruncated_whole_reads": v["wholes"],
                                           "ruler_sections": sorted(v["ruler"]), "sections_seen_any_read": sorted(v["any"]),
                                           "short_ruler": (k, g) in short_groups}
        if (k, g) in short_groups:
            result["short_ruler_groups"].append(g)

    if args.debug_other:
        c = collections.Counter()
        for k in kinds:
            for rel, r in inwin[k]:
                for a in r["accesses"]:
                    if a["kind"] == "other":
                        c[a["tool"]] += 1
        print("other-kind accesses by tool:", dict(c))

    with open(args.out, "w") as fh:
        json.dump(result, fh, indent=1)

    # controls -------------------------------------------------------------
    pos_path = None
    for p in recs:
        if os.path.basename(p) == POS_CONTROL:
            pos_path = p
    print("== POSITIVE CONTROL ==")
    ok_pos = False
    if pos_path:
        r = recs[pos_path]
        print("first_write_idx:", r["first_write_idx"], r["first_write_type"])
        print_sequence(r)
        sc = score(r)
        print(sc)
        fa = [a for a in r["accesses"] if a["kind"] != "other"][0]
        ok_pos = (fa["kind"] == "bash-chained" and {5, 6} <= (NEED - fa["sections"]))
        print("first access bash-chained & first-access sections missing 5 and 6:", ok_pos)
    print("== NEGATIVE CONTROL ==")
    cands = []
    for rel, r in inwin["repo-main"]:
        sc = score(r)
        if sc["accessed"] and sc["first_access_kind"] == "read-whole" and sc["complete"] \
                and set(sc["first_access_sections"]) >= NEED:
            cands.append((len(r["accesses"]), rel, r))
    cands.sort(key=lambda x: (x[0], x[1]))
    ok_neg = False
    if cands:
        _, rel, r = cands[0]
        print("negative control transcript:", os.path.basename(rel), "kind repo-main; candidates:", len(cands))
        print("(reading accesses only; %d accesses total, %d of kind other omitted)" % (len(r["accesses"]), sum(1 for a in r["accesses"] if a["kind"] == "other")))
        print_sequence(r, only_reads=True)
        sc = score(r)
        print({k: sc[k] for k in ("first_access_kind", "first_access_sections", "sections_before_first_write", "complete")})
        ok_neg = sc["complete"] and sc["first_access_kind"] == "read-whole" and set(sc["sections_before_first_write"]) >= NEED
    print("CONTROLS_PASS:", ok_pos and ok_neg)
    print("wrote", args.out)


def print_sequence(r, only_reads=False):
    fw = r["first_write_idx"]
    for i, a in enumerate(r["accesses"]):
        if only_reads and a["kind"] == "other":
            continue
        rel = ("no-result" if a["res_idx"] is None else
               ("before-first-write" if (fw is None or a["res_idx"] < fw) else "after-first-write"))
        print((i, a["tool"], a["kind"], sorted(a["sections"]), "trunc:" + (",".join(a["signs"]) or "none"),
               rel, "use@%s res@%s" % (a["use_idx"], a["res_idx"]), "err=%s" % a["is_error"]))


if __name__ == "__main__":
    main()
