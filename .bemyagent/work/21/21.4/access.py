"""21.4 access classifier. The functions and constants between the two `copied from` markers are
COPIED, unchanged, from <repo>/.bemyagent/work/21/21.2/census.py (the 21.2 census: parse_pipelines,
stage_cmd, classify_bash, bash_writes and the truncation signs). The one change is outside the copy: the
census matched the rules file by its basename (`PATH_RE`, a regex); here `PATH_RE` is an object with the
same `.search(text)` interface that is true only when a path-like fragment of the text RESOLVES to one
file - from the arm's directory, from the call's own cwd, or from a `cd` inside the command. So
`./.bemyagent/docs/00-ai-rules.md`, the relative form, an absolute form and `cd .bemyagent/docs && cat
00-ai-rules.md` all hit; the same basename in another arm's tree, or `BEMYAGENT.md`, does not.
Not copied: the census's `classify_access` (rewritten below to use the resolved path for Read and Grep).
Classes of one access: read-whole (Read with no offset/limit), read-partial, bash-alone (a lone print
command), bash-chained (a print command next to other commands), slice (head/sed/grep/... or a Grep
call), other (the path is named but nothing is read: wc, ls, cp, diff, ...).
"""
import json, os, pathlib, re, shlex

# ---- copied from census.py (21.2): constants -------------------------------------------------
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



# ---- copied from census.py (21.2): bash parsing -------------------------------------------------
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



# ---- end of the copy -------------------------------------------------------------------------


class Match:
    """Stands in for census.PATH_RE. `.search(text)` is truthy when some path-like fragment of `text` resolves
    to the one target file. Relative fragments are tried from the call's cwd, from each directory a `cd` in the
    same command leads to, and from the arm's directory. A fragment with `$` or a leading `~` cannot be resolved:
    it is never a hit, and `names_unresolved(text)` says so (the reader reports such calls for a hand-read)."""

    def __init__(self, arm_dir, rel):
        self.arm = os.path.realpath(arm_dir)
        self.target = os.path.realpath(os.path.join(self.arm, rel))
        self.base = os.path.basename(rel)
        self.cwds = [self.arm]

    def set_call(self, cwd=None, cmd=""):
        cur = os.path.realpath(cwd) if cwd else self.arm
        dirs = [cur]
        for m in re.finditer(r"""\bcd\s+("[^"]*"|'[^']*'|[^\s;&|]+)""", cmd or ""):
            arg = m.group(1).strip("\"'")
            if not arg or arg.startswith("~") or "$" in arg:
                continue
            cur = os.path.realpath(os.path.join(cur, arg))
            dirs.append(cur)
        if self.arm not in dirs:
            dirs.append(self.arm)
        self.cwds = dirs

    def _frags(self, text):
        return [f.strip("\"'") for f in re.split(r"""[\s'";|&<>()`=,]+""", text or "") if self.base in f]

    def resolves(self, frag):
        if not frag or "$" in frag or frag.startswith("~"):
            return False
        return any(os.path.realpath(os.path.join(d, frag)) == self.target for d in self.cwds)

    def search(self, text):
        return True if any(self.resolves(f) for f in self._frags(text)) else None

    def names_it(self, text):
        return self.base in (text or "")

    def names_unresolved(self, text):
        fr = self._frags(text)
        return bool(fr) and not any(self.resolves(f) for f in fr)


PATH_RE = Match(".", "00-ai-rules.md")      # replaced per arm and per file by the reader (set_target)


def set_target(arm_dir, rel):
    global PATH_RE
    PATH_RE = Match(arm_dir, rel)
    return PATH_RE


def classify_access(name, inp, cwd=None):
    """-> read-whole / read-partial / bash-alone / bash-chained / slice / other, for the current PATH_RE target."""
    PATH_RE.set_call(cwd, inp.get("command", "") if name == "Bash" else "")
    if name == "Read":
        if PATH_RE.resolves(inp.get("file_path", "") or ""):
            partial = inp.get("offset") not in (None, 0) or inp.get("limit") not in (None,)
            return "read-partial" if partial else "read-whole"
        return "other"
    if name == "Bash":
        return classify_bash(inp.get("command", "") or "")[0]
    if name == "Grep":
        p = inp.get("path") or ""
        g = inp.get("glob") or ""
        if PATH_RE.resolves(p):
            return "slice"
        under = os.path.realpath(os.path.join(PATH_RE.cwds[0], p)) if p else PATH_RE.arm
        ancestor = PATH_RE.target.startswith(under.rstrip("/") + "/")
        return "slice" if ancestor and PATH_RE.base in g else "other"
    return "other"          # Edit/Write/Glob/Agent/... mention the path but do not read it


def names_target(name, inp, cwd=None):
    """True if the call's input names the target's basename at all (resolved or not)"""
    try:
        blob = json.dumps(inp)
    except Exception:
        return False
    return PATH_RE.names_it(blob)


def unresolved_mention(name, inp, cwd=None):
    """the input names the basename but no fragment resolves to the target (another arm's file, an unresolvable $VAR path, ...)"""
    PATH_RE.set_call(cwd, inp.get("command", "") if name == "Bash" else "")
    texts = [str(v) for v in inp.values() if isinstance(v, (str, int, float))]
    texts = [t for t in texts if PATH_RE.names_it(t)]
    return bool(texts) and not any(PATH_RE.search(t) for t in texts)


def bash_has_filter(cmd, cwd=None):
    """B1: does a pipeline of `cmd` that names the target pass it through a range, filter or count (head, sed, grep, awk, wc, sort ...)?
    Used to tell a whole form (`cat F`, `nl F`, a pager) from a range form when a result holds no line."""
    PATH_RE.set_call(cwd, cmd or "")
    for pl in parse_pipelines(cmd or ""):
        if not any(PATH_RE.search(w) for st in pl for w in st["words"]):
            continue
        for st in pl:
            if stage_cmd(st)[0] in SLICE_CMDS | {"wc", "xargs"}:
                return True
    return False


PASS_SINKS = PRINT_CMDS | SLICE_CMDS | {"wc", "xargs", "tee", "md5", "md5sum", "shasum", "sha256sum", "cksum", "diff", "cmp", "test", "cat", "echo"}


def print_fate(cmd, cwd=None):
    """C2: where the output of a command that prints the target goes. 'result' = the call's result; 'away' = stdout redirected to
    /dev/null in a segment that names the target; 'unknown' = a pipe into a command this reader does not know (pbcopy, python3, node,
    a while loop ...). A print whose output never comes back to the agent is not a whole form."""
    PATH_RE.set_call(cwd, cmd or "")
    for seg in re.split(r"\s*(?:&&|\|\||;|\n)\s*", cmd or ""):
        if PATH_RE.search(seg) and re.search(r"(?:^|[\s(])(?:1?>>?|&>>?)\s*/dev/null", seg):
            return "away"
    for pl in parse_pipelines(cmd or ""):
        idxs = [i for i, st in enumerate(pl) if any(PATH_RE.search(w) for w in st["words"])]
        if not idxs:
            continue
        for st in pl[idxs[0] + 1:]:
            if stage_cmd(st)[0] not in PASS_SINKS:
                return "unknown"
    return "result"
