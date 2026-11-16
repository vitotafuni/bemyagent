#!/usr/bin/env python3
"""21.4 reader: readings (i)-(vii) of 02_tasks.md per arm, as amended by Amendment 1 (A1-A5), from the arm's
transcript cut at the compaction boundary, the launcher's status and outputs, the certificate and the snapshot / final
tree. JSON on stdout: booleans, numbers, class names, key names and file paths of the arm's tree - never transcript
text, never reply text. It does NOT compute the verdict: it prints each arm's classes and, per condition (control
first), the counts over the eligible arms, and stops there. The verdict table is read by hand, by an agent that did
not build this.

Usage: read.py [arm ...]    R214_ROOT (arm trees), R214_OUT (launcher outputs and <arm>.cert.json), R214_CFG /
CLAUDE_CONFIG_DIR (config dir; transcripts are read from <config>/projects/<arm path, non-alphanumerics -> '-'>/<session>.jsonl ONLY)

Definitions (02_tasks.md, Amendments 1 and 2):
  * lines of the rules (A1, B8): the non-empty lines of the arm's rules file as the TURN-1 SNAPSHOT holds it (the tree, flagged, if there
    is none); a rules file changed in turn 1 (its sha1 differs from setup.status) is flagged.
  * cut (A4): the boundary NUMBER launcher-count-before + 1 (launch.status `boundaries_before`), not the last one. A further boundary
    inside the window is flagged.
  * window (A4, B8): from the boundary to the first write: a Write/Edit/NotebookEdit/MultiEdit call whose result is present and not an
    error, or a shell command that writes (access.bash_writes) whatever its exit code. The write call and the calls issued before it -
    the order of the blocks inside one assistant record decides - are inside.
  * an access = a tool call whose input names the rules file by a path that RESOLVES to <arm>/.bemyagent/docs/00-ai-rules.md. What it
    delivered (A1): every non-empty line searched in its result by substring.
      whole     = one access whose result holds EVERY line, in order. Form decides nothing.
      slice     = at least one line and not all (`union` noted when several slices cover every line).
      attempted = (B1) a whole-form access - a Read with no offset/limit or ones reaching both ends, a shell command printing the file with
                  no range, filter or count - whose result holds no line. The arm leaves (i).
      none      = no access in the window. An access of any other form that delivers no line is NOT an access: listed as `no-line`; a form
                  the reader cannot place is listed `unplaced` and flagged. A call that also names BEMYAGENT.md and delivered a line is
                  `mixed-embedding`: flagged for the hand-read, not counted.
  * delivered-unresolved (A3): no access is whole and another call's result in the window holds every line in order.
  * (ii) handed back (B2-B4): M = the lines of the rules of 20+ characters that the arm's own instruction file (turn-1 snapshot: CLAUDE.md,
    AGENTS.md) does not hold; n of M found, by substring, in EVERY record after the boundary up to the first write, of any type under any key
    (except the stored request copies api-request*, counted and skipped: see REQUEST_COPY_TYPES) and in every preserved record (a preserved
    result of a call made before the boundary included), minus the text of the arm's own pinned-model assistant records and the result of a call
    issued after the boundary (by call id; its toolUseResult with it). n >= M/2 leaves (i). Shorter lines are counted apart and decide nothing.
    B12: the same count over the rest of turn 2 (the window's end to the end) is printed beside it (`rest_of_turn`); a stored request copy is left out
    except one between the boundary and the arm's first call after it (it counts); copies left out are counted.
  * eligible = launcher proof and a boundary at the cut number; the compaction call exited 0; the context shrank at the boundary; turn 2 ran in the
    same session (prompt a user record after the boundary, t2.json session id = turn 1's; not killed by the time limit; if it failed it made a write
    that succeeded); certificate clean (or failing only on calls after the window's end: flagged); (ii) below half of M; no attempted access.
  * (iv) = the same class before the cut boundary.
  * (vii) new leaf = a new file under .bemyagent/work/ at depth work/X/X.Y/ between snap/<arm>.t1 and the final tree;
    reset new = a non-comment line with `reset` in client/ or server/ that the t1 snapshot of that file lacks.
A reading that cannot be computed is null with a reason beside it.
"""
import importlib.util, json, os, pathlib, re, sys
sys.dont_write_bytecode = True          # no __pycache__ in the task folder or in harness/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import access, boundary, kset          # noqa: E402  (access.py: the census classifier; boundary.py: the boundary shape; kset.py: K)

REPO = pathlib.Path(os.environ.get("BMA_REPO") or HERE.parents[3])
S = pathlib.Path(os.environ["BMA_SCRATCH"])      # the scratch directory of this round (the shell scripts export it from local.env)
R = pathlib.Path(os.environ.get("R214_ROOT") or S / "r214")          # the trees of the six (final state)
RP = pathlib.Path(os.environ.get("R214P_ROOT") or S / "r214p")       # the trees of the pilots (C4: apart from the six)
OUT = pathlib.Path(os.environ.get("R214_OUT") or S / "r214_out")    # launcher outputs: JSON, status, snapshots, certificates
TOOL_CFG = pathlib.Path(os.environ.get("R214_CFG") or os.environ.get("CLAUDE_CONFIG_DIR") or pathlib.Path.home() / ".claude")
PROJECTS = TOOL_CFG / "projects"
RULES_REL = ".bemyagent/docs/00-ai-rules.md"
BEM_REL = "BEMYAGENT.md"
COND = {**{a: "C" for a in ("q112", "q113", "q114", "q901", "q902", "q903")}, **{a: "L" for a in ("q115", "q116", "q117")}}
PILOT = set(kset.pilots_from_env())      # B9: no pilot is cleared and run again under its name; the next name follows


def root_of(arm):
    """C4: the tree of a pilot stands in the pilots' root, the tree of a counted arm in the six's"""
    return RP if arm in PILOT else R
ALL_ARMS = ["q901", "q112", "q113", "q114", "q115", "q116", "q117"]     # control first
T2 = (HERE / "prompt_t2.txt").read_text()
T1B = (HERE / "prompt_t1b.txt").read_text()

try:
    K = kset.k_lines(REPO)          # C3: the 86 lines both conditions share; asserted
except AssertionError as e:
    sys.exit(f"read.py: {e}")
_spec = importlib.util.spec_from_file_location("tokens", REPO / "harness" / "tokens.py")
tokens = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(tokens)
W = tokens.W        # the weights of harness/tokens.py, not a copy

KEYOK = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,40}$")
SLICE_FORMS = {"read-partial", "slice"}
WHOLE_FORMS = {"read-whole", "bash-alone", "bash-chained"}
PRINT_FORMS = WHOLE_FORMS | SLICE_FORMS


# ------------------------------------------------------------------ small helpers
def own_folder(arm_dir):
    return re.sub(r"[^A-Za-z0-9]", "-", str(arm_dir))


def result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(x.get("text", "") for x in content if isinstance(x, dict) and isinstance(x.get("text", ""), str))
    return ""


def file_lines(text):
    """the non-empty lines of a file, trailing blanks dropped; the unit of A1 and of (ii)"""
    return [l.rstrip() for l in text.splitlines() if l.strip()]


def found(text, lines):
    """-> (set of indexes of the lines that occur in `text` as a substring, True if ALL occur in order)"""
    idx, pos, ordered = set(), 0, 0
    for i, l in enumerate(lines):
        if l in text:
            idx.add(i)
        j = text.find(l, pos)
        if j >= 0:
            pos = j + len(l)
            ordered += 1
    return idx, bool(lines) and ordered == len(lines)


def signs_of(text):
    return [n for n, rx in access.TRUNC_PATTERNS.items() if rx.search(text)]


def walk_strings(o, path=""):
    """(key path, string) for every string in a JSON value; list indexes become [] and odd key names <key>"""
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            k = str(k) if KEYOK.match(str(k)) else "<key>"
            yield from walk_strings(v, path + "." + k if path else k)
    elif isinstance(o, list):
        for v in o:
            yield from walk_strings(v, path + "[]")


def rec_kind(rec):
    t = str(rec.get("type"))
    if rec.get("subtype"):
        t += "/" + str(rec["subtype"])
    att = rec.get("attachment")
    if isinstance(att, dict) and att.get("type"):
        t += "/" + str(att["type"])
    flags = [k[2:] for k in ("isCompactSummary", "isMeta", "isVisibleInTranscriptOnly") if rec.get(k) is True]
    return t + ("{" + ",".join(flags) + "}" if flags else "")


def prompt_tokens(rec):
    u = (rec.get("message") or {}).get("usage")
    if not isinstance(u, dict):
        return None
    return sum(u.get(k) or 0 for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))


def tool_uses(rec):
    m = rec.get("message")
    if rec.get("type") != "assistant" or not isinstance(m, dict) or not isinstance(m.get("content"), list):
        return []
    return [b for b in m["content"] if isinstance(b, dict) and b.get("type") == "tool_use"]


def tool_results(rec):
    m = rec.get("message")
    if rec.get("type") != "user" or not isinstance(m, dict) or not isinstance(m.get("content"), list):
        return []
    return [b for b in m["content"] if isinstance(b, dict) and b.get("type") == "tool_result"]


def user_text(rec):
    m = (rec.get("message") or {}).get("content")
    return m if isinstance(m, str) else " ".join(x.get("text", "") for x in (m or []) if isinstance(x, dict) and x.get("type") == "text")


def is_prompt_record(rec):
    """a user record that carries a typed prompt: not a tool result, not meta, not the compaction summary"""
    if rec.get("type") != "user" or rec.get("isMeta") or rec.get("isCompactSummary") or tool_results(rec):
        return False
    c = (rec.get("message") or {}).get("content")
    return isinstance(c, str) or any(isinstance(x, dict) and x.get("type") == "text" for x in (c or []))


# ------------------------------------------------------------------ the transcript: calls, results, writes
def collect(recs):
    """calls (in order, one per tool_use id; `pos` = record index * 1000 + block index, so the order of blocks inside one
    assistant record decides what was issued before what - B8) and results (by tool_use id)"""
    calls, seen, results = [], set(), {}
    for idx, rec in enumerate(recs):
        if not isinstance(rec, dict):
            continue
        m = rec.get("message")
        blocks = m["content"] if rec.get("type") == "assistant" and isinstance(m, dict) and isinstance(m.get("content"), list) else []
        for bi, b in enumerate(blocks):
            if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                continue
            tid = b.get("id")
            if tid in seen:
                continue
            seen.add(tid)
            name, inp = b.get("name"), b.get("input")
            inp = inp if isinstance(inp, dict) else {}
            if name in access.WRITE_TOOLS:
                w = name
            elif name == "Bash":
                w = access.bash_writes(inp.get("command", "") or "")
            else:
                w = None
            calls.append({"id": tid, "idx": idx, "pos": idx * 1000 + bi, "name": name, "inp": inp, "cwd": rec.get("cwd"), "write": w})
        for b in tool_results(rec):
            tid = b.get("tool_use_id")
            if tid not in results:
                results[tid] = {"idx": idx, "text": result_text(b.get("content")), "is_error": bool(b.get("is_error"))}
    return calls, results


def first_write(calls, results, lo, hi):
    """the first write call with lo < idx < hi, or None. A Write/Edit counts only if its result is present and not an error
    (A4); a shell command that writes counts whatever its exit code - the file was written (B8) - if its result is present."""
    for c in calls:
        if lo < c["idx"] < hi and c["write"]:
            r = results.get(c["id"])
            if r is not None and (c["name"] == "Bash" or not r["is_error"]):
                return c
    return None


def form_of(name, inp, label):
    if name == "Read":
        return "offset-or-limit" if label == "read-partial" else "plain"
    if name == "Bash":
        return "shell"
    return "grep-tool" if name == "Grep" else str(name)


def form_class(name, inp, label, cwd, n_file_lines):
    """B1: 'whole-form' = a Read with no offset and no limit or ones that reach both ends of the file, or a shell command that
    prints the file with no range, filter or count; 'range-form' = anything else that reads; 'unplaced' = a form the reader cannot place"""
    if name == "Read":
        off, lim = inp.get("offset"), inp.get("limit")
        ok = lambda v: v is None or (isinstance(v, int) and not isinstance(v, bool))
        if not (ok(off) and ok(lim)):
            return "unplaced"
        return "whole-form" if off in (None, 0, 1) and (lim is None or lim >= n_file_lines) else "range-form"
    if name == "Bash":
        if label in WHOLE_FORMS and access.print_fate(inp.get("command", "") or "", cwd) != "result":
            return "unplaced"           # C2: a print whose output never comes back to the agent is not a whole form
        return "whole-form" if label in WHOLE_FORMS and not access.bash_has_filter(inp.get("command", "") or "", cwd) else "range-form"
    if name == "Grep":
        return "range-form"
    return "unplaced"


def accesses(calls, results, arm_dir, rel, lines, n_file_lines, lo, limit_pos, hi, klines=None):
    """Tool calls with lo < idx < hi that name the file `rel` of the arm. -> (reads, nonreading, unresolved):
    reads = accesses whose label is a read (PRINT_FORMS), each with what its result delivered; `in_window` is pos <= limit_pos.
    Class of one access: whole / slice by what it delivered (A1); with no line delivered: `attempted` for a whole form (B1),
    `no-line` for a range form (not an access for (i)), `unplaced` for a form the reader cannot place (flagged);
    `mixed-embedding` when the call also names BEMYAGENT.md and delivered a line (B8: flagged for the hand-read, not counted).
    nonreading = calls naming the file by a resolving path that read nothing (wc, ls, cp, ...), a count;
    unresolved = calls naming the basename where no path resolves to the file."""
    access.set_target(arm_dir, rel)
    reads, nonreading, unresolved = [], 0, []
    for c in calls:
        if not (lo < c["idx"] < hi):
            continue
        if not access.names_target(c["name"], c["inp"], c["cwd"]):
            continue
        label = access.classify_access(c["name"], c["inp"], c["cwd"])
        if label not in PRINT_FORMS:
            if access.unresolved_mention(c["name"], c["inp"], c["cwd"]):
                unresolved.append({"tool": c["name"], "idx": c["idx"]})
            elif c["name"] not in access.WRITE_TOOLS:
                nonreading += 1
            continue
        res = results.get(c["id"])
        got, ordered = found(res["text"], lines) if res else (set(), False)
        gotk = found(res["text"], klines if klines is not None else lines)[0] if res else set()       # C1: a delivery is a line of K
        fc = form_class(c["name"], c["inp"], label, c["cwd"], n_file_lines)
        if not res:
            d = "no-result"
        elif gotk and rel == RULES_REL and BEM_REL in json.dumps(c["inp"]):
            d = "mixed-embedding"
        elif ordered:
            d = "whole"
        elif gotk:
            d = "slice"
        else:
            d = {"whole-form": "attempted", "range-form": "no-line", "unplaced": "unplaced"}[fc]
        reads.append({"id": c["id"], "idx": c["idx"], "result_idx": res["idx"] if res else None, "tool": c["name"],
                      "form": form_of(c["name"], c["inp"], label), "form_class": fc, "label": label, "class": d,
                      "lines_delivered": len(got), "K_lines_delivered": len(gotk), "lines_total": len(lines), "in_order_all": ordered, "line_set": got,
                      "truncation_signs": signs_of(res["text"]) if res else [], "is_error": res["is_error"] if res else None,
                      "in_window": c["pos"] <= limit_pos})
    return reads, nonreading, unresolved


def public(a):
    return {k: v for k, v in a.items() if k not in ("id", "line_set")}


def klass(reads, n_lines):
    """whole / attempted / slice / none (first that applies, C1) from the accesses inside the window, and a note. Accesses of class no-line, unplaced,
    mixed-embedding and no-result are listed but are not accesses for (i)."""
    win = [a for a in reads if a["in_window"]]
    if any(a["class"] == "whole" for a in win):
        return "whole", None
    if any(a["class"] == "attempted" for a in win):      # C1: a withheld whole read wins over a slice
        return "attempted", "an access of a whole form delivered no line of K (the tool withheld the text); no other access in the window was whole"
    sl = [a for a in win if a["class"] == "slice"]
    if sl:
        u = set().union(*[a["line_set"] for a in sl])
        return "slice", ("union: several slices together cover every line" if len(sl) > 1 and len(u) == n_lines else None)
    return "none", ("rules file accessed only after the first write, or only by forms that delivered no line, or without a result" if reads else None)


def delivered_unresolved(calls, results, lines, lo, limit_pos, resolved_ids):
    """A3: calls in the window, not already an access, whose result holds every line in order"""
    out = []
    access.set_target(".", BEM_REL)
    for c in calls:
        if not (lo < c["idx"] and c["pos"] <= limit_pos) or c["id"] in resolved_ids or c["name"] in access.WRITE_TOOLS:
            continue
        res = results.get(c["id"])
        if not res:
            continue
        _, ordered = found(res["text"], lines)
        if ordered:
            label = access.classify_access(c["name"], c["inp"], c["cwd"])
            out.append({"tool": c["name"], "form": form_of(c["name"], c["inp"], label), "idx": c["idx"],
                        "names_BEMYAGENT_md": access.names_target(c["name"], c["inp"], c["cwd"])})
    return out


def rules_in_other_results(calls, results, arm_dir, lo, limit_pos):
    """C7: lines of K in the result of a call inside the window that does not name the rules file (a search across the tree is the
    arm's own act; text appended to an unrelated result is a hand-back). Listed per arm: tool, form, number of K lines."""
    access.set_target(arm_dir, RULES_REL)
    out = []
    for c in calls:
        if not (lo < c["idx"] and c["pos"] <= limit_pos):
            continue
        if access.names_target(c["name"], c["inp"], c["cwd"]):          # X1: the results of write calls are looked at too; a write naming the rules file is skipped here
            continue
        res = results.get(c["id"])
        g = found(res["text"], K)[0] if res else set()
        if g:
            label = access.classify_access(c["name"], c["inp"], c["cwd"])
            out.append({"tool": c["name"], "form": form_of(c["name"], c["inp"], label), "idx": c["idx"], "K_lines": len(g),
                        "names_BEMYAGENT_md": BEM_REL in json.dumps(c["inp"])})
    return out


def segment(calls, results, arm_dir, lines, n_file_lines, lo, hi):
    """class of the accesses to the rules file with lo < idx < hi, up to the first write (A4, B8)"""
    w = first_write(calls, results, lo, hi)
    limit_pos = w["pos"] if w else 10 ** 12
    reads, nonreading, unresolved = accesses(calls, results, arm_dir, RULES_REL, lines, n_file_lines, lo, limit_pos, hi, K)
    k, note = klass(reads, len(lines))
    bem, _, _ = accesses(calls, results, arm_dir, BEM_REL, lines, n_file_lines, lo, limit_pos, hi, K)
    resolved = {a["id"] for a in reads}
    du = delivered_unresolved(calls, results, lines, lo, limit_pos, resolved) if k != "whole" else []
    if k != "whole":     # B8: a call naming the rules file AND BEMYAGENT.md that delivered every line is flagged, not counted
        du += [{"tool": a["tool"], "form": a["form"], "idx": a["idx"], "names_BEMYAGENT_md": True, "also_names_rules_file": True}
               for a in reads if a["in_window"] and a["class"] == "mixed-embedding" and a["in_order_all"]]
    return {"class": k, "note": note, "first_write": {"idx": w["idx"], "kind": w["write"]} if w else None,
            "window_end": w["idx"] if w else hi - 1, "sequence": [public(a) for a in reads if a["in_window"]],
            "late_accesses": [{"tool": a["tool"], "form": a["form"], "class": a["class"]} for a in reads if not a["in_window"]],
            "other_files": [{"file": BEM_REL, "tool": a["tool"], "form": a["form"], "class": a["class"],
                             "lines_delivered": a["lines_delivered"], "counted": False} for a in bem if a["in_window"]],
            "non_reading_mentions": nonreading, "unresolved_mentions": unresolved, "delivered_unresolved": du,
            "unplaced_forms": [{"tool": a["tool"], "form": a["form"]} for a in reads if a["in_window"] and a["class"] == "unplaced"],
            "rules_in_results_of_other_calls": rules_in_other_results(calls, results, arm_dir, lo, limit_pos)}


# ------------------------------------------------------------------ (ii) handed back, and what the compaction preserved
REQUEST_COPY_TYPES = {"api-request", "api-request-blob", "api-request-shape"}   # stored COPIES of the messages of a request: the same text
# as records already scanned (or as the arm's own results), so reading them would count every result the arm itself read.
# B3 says "any type"; these three are the one exception the builder chose (named in the hand-back; the count of skipped records is printed).
KNOWN_METADATA_KEYS = {"cumulativeDroppedTokens", "durationMs", "postTokens", "preCompactArtifactReadVersions", "preCompactDiscoveredTools",
                       "preTokens", "preservedMessages", "preservedSegment", "trigger"}       # the keys of the 16 boundaries 03_execute.log [2] learned from


def lines_in(rec, lines):
    """(set of line indexes found in any string of the record under any key, key paths that carried one)"""
    got, paths = set(), set()
    for p, s in walk_strings(rec):
        g, _ = found(s, lines)
        if g:
            got |= g
            paths.add(p)
    return got, paths


def is_own_pinned(rec):
    """an assistant record of the arm's own pinned model (B3: its text is the arm's own words, never a hand-back)"""
    mdl = (rec.get("message") or {}).get("model") if isinstance(rec.get("message"), dict) else None
    return rec.get("type") == "assistant" and isinstance(mdl, str) and "sonnet" in mdl


def view_for_ii(rec, matched_ids):
    """B3: the record as (ii) reads it - without the result blocks of calls issued after the boundary (matched by call id) and, with
    them, the same result under `toolUseResult`. A result with no matching call, and a text block beside a result, stay."""
    m = rec.get("message")
    if not (isinstance(m, dict) and isinstance(m.get("content"), list)):
        return rec
    keep = [b for b in m["content"] if not (isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in matched_ids)]
    if len(keep) == len(m["content"]):
        return rec
    r = {k: v for k, v in rec.items() if k != "toolUseResult"}
    r["message"] = {**m, "content": keep}
    return r


def file_target(att, arm_dir):
    f = ((att.get("content") or {}).get("file") or {}) if isinstance(att.get("content"), dict) else {}
    fp = str(f.get("filePath") or att.get("filename") or "")
    real = os.path.realpath(os.path.join(str(arm_dir), fp)) if fp else ""
    return ("rules" if real == os.path.realpath(str(arm_dir / RULES_REL)) else "BEMYAGENT.md" if real == os.path.realpath(str(arm_dir / BEM_REL)) else "other-file"), f


def preserved_records(recs, brec):
    """indexes of the records the compaction kept across the boundary (compactMetadata.preservedMessages.uuids / allUuids; else the
    range preservedSegment.headUuid..tailUuid by file position), which fields were present and non-empty, the ids they name (counted
    once), which of those are not in the file, and which fields have a shape the reader does not know (B5)"""
    m = brec.get("compactMetadata") or brec.get("compact_metadata") or {}
    if not isinstance(m, dict):          # C8: reported as a shape problem by handed_back, never a traceback
        m = {}
    pm, ps = m.get("preservedMessages"), m.get("preservedSegment")
    pos = {r["uuid"]: i for i, r in enumerate(recs) if isinstance(r, dict) and isinstance(r.get("uuid"), str)}
    named, shape, ids = set(), [], []
    present = lambda v: v not in (None, {}, [], "", 0, False)
    if present(pm):
        if not isinstance(pm, dict):
            shape.append("preservedMessages is not an object")
        else:
            for k in ("uuids", "allUuids"):
                v = pm.get(k)
                if v is None:
                    continue
                if isinstance(v, list) and all(isinstance(u, str) for u in v):
                    named |= set(v); ids += v
                else:
                    shape.append(f"preservedMessages.{k} is not a list of strings")
            if isinstance(pm.get("anchorUuid"), str): named.add(pm["anchorUuid"])
    if present(ps):
        if not isinstance(ps, dict):
            shape.append("preservedSegment is not an object")
        else:
            for k in ("anchorUuid", "headUuid", "tailUuid"):
                v = ps.get(k)
                if isinstance(v, str): named.add(v)
                elif v is not None: shape.append(f"preservedSegment.{k} is not a string")
    idx = sorted({pos[u] for u in ids if u in pos})
    how = "preservedMessages.uuids"
    if not idx and isinstance(ps, dict) and ps.get("headUuid") in pos and ps.get("tailUuid") in pos:
        idx = [i for i in range(pos[ps["headUuid"]], pos[ps["tailUuid"]] + 1) if isinstance(recs[i], dict) and recs[i].get("uuid")]
        how = "preservedSegment head..tail"
    fields = {"preservedMessages": present(pm), "preservedSegment": present(ps)}
    return idx, fields, named, sorted(u for u in named if u not in pos), shape, how


HEX64 = re.compile(r"^[0-9a-f]{64}$")
RELEASED_LINES = set(file_lines((REPO / RULES_REL).read_text()))       # the lines of the released rules file: a line of an arm's rules that is not here is the treatment


def has_text(obj):
    """a string with a blank and more than 40 characters, outside `cwd`: text, not a hash or a path"""
    return any(p != "cwd" and re.search(r"\s", x) and len(x) > 40 for p, x in walk_strings(obj))


KNOWN_BLOCKS = {"text", "tool_use", "tool_result", "thinking", "redacted_thinking", "image", "document"}


def message_readable(m):
    """D6 (ruled 2026-11-16): a message is read when its content is a string, or a list of blocks of known types (an empty list, or a list
    with no text in it, has been read: 0 lines). Anything else - or an unknown block type - cannot be read."""
    if not isinstance(m, dict) or "content" not in m:
        return True
    c = m["content"]
    if isinstance(c, str):
        return True
    return isinstance(c, list) and all(isinstance(b, dict) and b.get("type") in KNOWN_BLOCKS for b in c)


def copy_view(rec, blobs):
    """C5, D6: a request copy with the stored blobs its hashes point to (anywhere in the file) resolved. -> (view, readable): unreadable only when
    a hash in a list resolves to no stored record, or the content of the copy or of a blob it points to is neither a string nor a list of known blocks"""
    resolved, unresolved = [], 0
    own = {rec.get(k) for k in ("hash", "requestDigest", "shapeHash")}
    for p, x in walk_strings(rec):
        if HEX64.match(x) and x not in own:
            if x in blobs:
                resolved.append(blobs[x])
            elif p.endswith("[]"):
                unresolved += 1
    view = {"copy": rec, "resolved": resolved}
    ok = not unresolved and message_readable(rec.get("message")) and all(message_readable(m) for m in resolved)
    return view, ok


def handed_back(recs, calls, results, B, hi, lines, arm_dir, instr_text):
    """(ii) (C3, C5): K = the 86 lines both conditions share (kset.py). x = lines of K the arm's own instruction file holds in the turn-1
    snapshot; n = lines of K handed back that are not in x, found by substring in every record after the boundary up to `hi` (the window)
    and in every record the compaction preserved (B3), minus the arm's own pinned-model assistant text and the results of calls issued after
    the boundary. The arm leaves (i) when x + n >= 43 (read_arm). The same count over the rest of turn 2 is `rest_of_turn` (B12a).
    A stored request copy (api-request*) counts when it lies after the boundary and before the FIRST TOOL RESULT after it (C5), its hashes
    resolved to the stored blobs wherever they stand; a copy in that span that cannot be read as text is counted in
    `request_copies_unreadable`; other copies are left out and counted. The lines of the arm's rules that are not in the released rules
    file (the added line of L) are reported apart: `added_line_handed_back`."""
    k_free = [l for l in K if l not in instr_text]
    x = len(K) - len(k_free)
    short = [l for l in lines if len(l) < 20]
    added = [l for l in lines if l not in RELEASED_LINES]
    matched = {c["id"] for c in calls if c["idx"] > B}
    first_result = min((results[c["id"]]["idx"] for c in calls if c["idx"] > B and c["id"] in results), default=10 ** 9)
    blobs = {r["hash"]: r["message"] for r in recs if isinstance(r, dict) and r.get("type") == "api-request-blob" and isinstance(r.get("hash"), str) and "message" in r}
    access.set_target(arm_dir, RULES_REL)

    def scan(indices, preserved=False):
        st = {"got": set(), "short": set(), "kinds": {}, "rules_records": [], "skipped": 0, "unreadable": 0, "added": False}
        for idx, tag in indices:
            rec = recs[idx]
            if not isinstance(rec, dict):
                continue
            view = None
            if rec.get("type") in REQUEST_COPY_TYPES:
                if not preserved and B < idx < first_result:        # C5: up to the first tool result after the boundary a copy counts
                    view, readable = copy_view(rec, blobs)
                    if not readable:
                        st["unreadable"] += 1
                else:
                    st["skipped"] += 1
                    continue
            if is_own_pinned(rec):
                continue
            if view is None:
                view = view_for_ii(rec, matched)
            got, paths = lines_in(view, k_free)
            st["short"].update(lines_in(view, short)[0])
            if added and lines_in(view, added)[0]:
                st["added"] = True
            att = rec.get("attachment") if isinstance(rec.get("attachment"), dict) else {}
            target, partial, ftarget = None, None, None
            if att.get("type") == "file":
                ftarget, f = file_target(att, arm_dir)
                if ftarget == "rules":
                    target = "rules"
                    nums = [f.get(k) for k in ("startLine", "numLines", "totalLines")]
                    partial = None if not all(isinstance(n, int) for n in nums) else (nums[0] > 1 or nums[1] < nums[2])
            elif att.get("type") == "compact_file_reference":
                access.PATH_RE.set_call(arm_dir, "")
                if any(access.PATH_RE.resolves(str(att.get(k) or "")) for k in ("filename", "displayPath")):
                    target = "rules-reference-only"
            if target:
                st["rules_records"].append({"offset": idx - B, "kind": rec_kind(rec) + tag, "target": target, "partial": partial, "lines": len(got)})
            if got:
                st["got"] |= got
                k = st["kinds"].setdefault(rec_kind(rec) + tag, {"records": 0, "key_paths": set(), "lines": set(), "file_targets": set()})
                k["records"] += 1; k["key_paths"] |= paths; k["lines"] |= got
                if ftarget: k["file_targets"].add(ftarget)
        return st

    kinds_out = lambda st: [{"kind": k, "records": v["records"], "key_paths": sorted(v["key_paths"]), "lines": len(v["lines"]),
                             "file_targets": sorted(v["file_targets"])} for k, v in sorted(st["kinds"].items())]
    win = scan([(i, "") for i in range(B + 1, hi)])
    rest = scan([(i, "") for i in range(hi, len(recs))])
    pres_idx, fields, named, missing, shape, how = preserved_records(recs, recs[B])
    md = recs[B].get("compactMetadata") if "compactMetadata" in recs[B] else recs[B].get("compact_metadata")
    md_shape = "ok" if isinstance(md, dict) else "absent" if md is None else "not an object"
    md = md if isinstance(md, dict) else {}
    pres = {"fields_present": fields, "ids_named": len(named), "ids_not_in_file": len(missing), "unexpected_shape": shape,
            "records_found": len(pres_idx), "found_by": how if pres_idx else None,
            "offsets": [min(pres_idx) - B, max(pres_idx) - B] if pres_idx else None, "types": {},
            "lines_in_non_result_records": 0, "lines_in_results": 0, "metadata_shape": md_shape,
            "unknown_metadata_keys": sorted(k if KEYOK.match(k) else "<odd-key>" for k in md if k not in KNOWN_METADATA_KEYS)}
    pr_non, pr_res = set(), set()
    pres_scan = []
    for i in pres_idx:
        rec = recs[i]
        key = str(rec.get("type")) + ("/tool_result" if tool_results(rec) else "")
        pres["types"][key] = pres["types"].get(key, 0) + 1
        if rec.get("type") in REQUEST_COPY_TYPES or is_own_pinned(rec):
            continue
        got, _ = lines_in(rec, k_free)
        (pr_res if tool_results(rec) else pr_non).update(got)
        if i < B:       # a preserved record counts, a result of a call made BEFORE the boundary included (ruling 2026-11-15)
            pres_scan.append((i, "(preserved tool_result)" if tool_results(rec) else "(preserved)"))
    ps = scan(pres_scan, preserved=True)
    for k in ("got", "short"):
        win[k] |= ps[k]
    win["added"] = win["added"] or ps["added"]
    for k, v in ps["kinds"].items():
        win["kinds"].setdefault(k, v)
    win["rules_records"] += ps["rules_records"]
    pres["lines_in_non_result_records"], pres["lines_in_results"] = len(pr_non), len(pr_res)
    pres["any_rules_lines"] = bool(pr_non or pr_res)
    n = len(win["got"])
    lineset = set(lines)
    return {"n": n, "x": x, "x_plus_n": x + n, "K": len(K), "of": len(K), "M": len(K), "threshold": kset.THRESHOLD,
            "K_lines_in_snapshot_rules": sum(1 for l in K if l in lineset),
            "added_line_handed_back": (win["added"] or rest["added"]) if added else None, "added_lines_in_rules": len(added),
            "short_lines_hit": [len(win["short"]), len(short)], "skipped_request_copy_records": win["skipped"] + rest["skipped"],
            "request_copies_unreadable": win["unreadable"],
            "rest_of_turn": {"n": len(rest["got"]), "of": len(K), "kinds": kinds_out(rest)},
            "kinds": kinds_out(win), "rules_file_records": win["rules_records"], "preserved": pres}


# ------------------------------------------------------------------ cost, status, trees, certificate
def call_cost(d):
    if not isinstance(d, dict):
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
    wt = lambda x: round(sum(x.get(k, 0) * W[k] for k in W))
    return {"weighted": wt(a), "weighted_from_usage": wt(ua), "raw": a, "models": sorted(mu), "num_turns": d.get("num_turns"),
            "is_error": d.get("is_error"), "permission_denials": len(d.get("permission_denials") or []), "session_id": d.get("session_id")}


def read_json(p):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception:
        return None


def stream_result(p):
    """the last type=result record of a stream-json output"""
    last = None
    for r in boundary.records(p):
        if isinstance(r, dict) and r.get("type") == "result":
            last = r
    return last


def status_of(arm):
    out = {"tokens": {}, "exit_codes": {}, "lines": 0}
    p = OUT / "launch.status"
    if not p.exists():
        return out
    for line in p.read_text(errors="replace").splitlines():
        w = line.split()
        if not w or w[0] != arm:
            continue
        out["lines"] += 1
        if len(w) > 2 and w[1] in ("t1", "t1b", "cp", "t2") and w[2].startswith("exit="):
            try: out["exit_codes"][w[1]] = int(w[2][5:])
            except ValueError: pass
        for m in re.finditer(r"(\w+)=([^\s()]+)", line):
            out["tokens"][m.group(1)] = m.group(2)
        if "turn2=skipped" in line:
            out["tokens"]["turn2"] = "skipped"
        if "killed by the time limit" in line and len(w) > 1:
            out.setdefault("killed", []).append(w[1])
    return out


def certificate_of(arm):
    """-> (row or None, where it was looked for). <arm>.cert.json holds {arm: row} (certificate.py <arm>) or the row"""
    d = read_json(OUT / f"{arm}.cert.json")
    if isinstance(d, dict):
        return (d.get(arm) if isinstance(d.get(arm), dict) else d), f"{arm}.cert.json"
    d = read_json(OUT / "cert.json")
    if isinstance(d, dict) and isinstance(d.get(arm), dict):
        return d[arm], "cert.json"
    return None, f"{arm}.cert.json"


def tree(root):
    """rel path -> text, without node_modules, .git, game.db*"""
    out, root = {}, pathlib.Path(root)
    if not root.is_dir():
        return None
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("node_modules", ".git")]
        for f in fn:
            if f.startswith("game.db"):
                continue
            p = pathlib.Path(dp) / f
            try: out[str(p.relative_to(root))] = p.read_text(errors="replace")
            except Exception: pass
    return out


COMMENT = ("//", "/*", "*", "<!--")      # a line that only comments is not code


def reading_vii(arm):
    t1, fin = tree(OUT / "snap" / f"{arm}.t1"), tree(root_of(arm) / arm)
    if t1 is None or fin is None:
        return {"value": None, "reason": f"missing: {'snap.t1' if t1 is None else 'final tree'}"}
    new_work = sorted(rel for rel in fin if rel.startswith(".bemyagent/work/") and rel not in t1)
    leaf = sorted({str(pathlib.PurePath(rel).parent) for rel in new_work if len(pathlib.PurePath(rel).parts) >= 5})
    reset = []
    for rel, text in fin.items():
        if rel.split("/")[0] not in ("client", "server"):
            continue
        old = {l.strip() for l in (t1.get(rel) or "").splitlines()}
        reset += [f"{rel}:{n + 1}" for n, l in enumerate(text.splitlines())
                  if re.search("reset", l, re.I) and l.strip() not in old and not l.strip().startswith(COMMENT)]
    return {"new_work_files": new_work, "new_leaf_dirs": leaf, "new_leaf": bool(leaf), "reset_new_hits": reset, "reset_new": bool(reset)}


# ------------------------------------------------------------------ one arm
def snapshot_text(arm, rel):
    p = OUT / "snap" / f"{arm}.t1" / rel
    return p.read_text(errors="replace") if p.is_file() else None


def setup_sha1(arm):
    """the sha1 of the arm's rules file as setup.py built it (setup.status), or None"""
    p = OUT / "setup.status"
    if p.exists():
        for l in p.read_text().splitlines():
            if l.startswith(f"arm {arm} "):
                m = re.search(r"rules_sha1=([0-9a-f]+)", l)
                return m.group(1) if m else None
    return None


def occasion_attachments(recs, B, hi, arm_dir):
    """D2: attachments of any type after the boundary (up to the window's end) that name the rules file: a reference (compact_file_reference),
    a text (a `file` attachment of it, or lines of K in any attachment), or its name in any other attachment. The instruction attachment names
    the file by the sentinel sentence, in both conditions, and is the one type left out."""
    out = []
    for idx in range(B + 1, hi):
        rec = recs[idx]
        att = rec.get("attachment") if isinstance(rec, dict) and rec.get("type") == "attachment" else None
        if not isinstance(att, dict) or att.get("type") == "instructions":
            continue
        strs = [x for _, x in walk_strings(att)]
        kind = None
        if att.get("type") == "compact_file_reference" and any(os.path.basename(RULES_REL) in x for x in strs):
            kind = "reference"
        elif att.get("type") == "file" and any(os.path.basename(RULES_REL) in x for x in strs):
            kind = "text-attachment"
        elif any(found(x, K)[0] for x in strs):
            kind = "text"
        elif any(os.path.basename(RULES_REL) in x for x in strs):
            kind = "name"
        if kind:
            out.append({"offset": idx - B, "type": str(att.get("type")), "kind": kind})
    return out


def files_touched_before(calls, B, arm_dir):
    """D2: distinct files touched with Read, Edit or Write (and NotebookEdit/MultiEdit) before the boundary"""
    seen = set()
    for c in calls:
        if c["idx"] < B and c["name"] in ("Read", "Edit", "Write", "NotebookEdit", "MultiEdit"):
            p = c["inp"].get("file_path") or c["inp"].get("notebook_path")
            if isinstance(p, str) and p:
                seen.add(os.path.realpath(os.path.join(str(c["cwd"] or arm_dir), p)))
    return len(seen)


def read_arm(arm):
    import hashlib
    arm_dir = root_of(arm) / arm
    row = {"arm": arm, "cond": COND.get(arm, "?"), "role": "pilot" if arm in PILOT else "arm", "arm_dir_exists": arm_dir.is_dir()}
    st = status_of(arm)
    tk = st["tokens"]
    row["status"] = {"tokens": tk, "exit_codes": st["exit_codes"], "killed": st.get("killed", [])}
    t1j, t2j = read_json(OUT / f"{arm}.t1.json"), read_json(OUT / f"{arm}.t2.json")
    t1bj = read_json(OUT / f"{arm}.t1b.json")
    row["design"] = "4 calls (turn 1, turn 1b, compaction, turn 2)" if "t1b_sha" in tk else "3 calls (turn 1, compaction, turn 2): the design before Amendment 4"
    cpr = stream_result(OUT / f"{arm}.cp.jsonl")
    row["vi"] = {"t1": call_cost(t1j), "t1b": call_cost(t1bj), "cp": call_cost(cpr), "t2": call_cost(t2j)}
    ws = [c["weighted"] for c in row["vi"].values() if c]
    row["vi_total_weighted"] = sum(ws) if ws else None
    row["v"] = {"memory_existed": tk.get("memory_existed"), "files": tk.get("files")}
    row["vii"] = reading_vii(arm)
    flags, reasons = [], []
    cert, cert_where = certificate_of(arm)
    row["certificate"] = {"found": cert is not None, "looked_for": cert_where, "clean": (cert or {}).get("clean"), "design_ok": (cert or {}).get("design_ok"),
                          "failed_terms": [k for k, v in ((cert or {}).get("clean_terms") or {}).items() if not v]}

    sid = (t1j or {}).get("session_id")
    tr = PROJECTS / own_folder(arm_dir) / f"{sid}.jsonl" if sid else None
    if not sid or not tr.is_file():
        row["transcript"] = {"found": False, "reason": "no session id in t1.json" if not sid else "no transcript in the arm's own project folder"}
        for k in ("i", "ii", "iii", "iv"):
            row[k] = {"value": None, "reason": row["transcript"]["reason"]}
        row["eligible"] = False
        row["eligible_reasons"] = [row["transcript"]["reason"]]
        row["flags"] = flags
        return row
    recs = boundary.records(tr)
    unparsed = boundary.unparsed_lines(tr)                                        # C8
    if unparsed:
        flags.append(f"{unparsed} transcript line(s) do not parse and were dropped by every reader: what they hold was not read (02_tasks.md C8)")
    # B8: the rules' lines are what the file held when the window opened: the turn-1 snapshot (the tree, with a flag, if there is none)
    snap_rules = snapshot_text(arm, RULES_REL)
    rules_path = arm_dir / RULES_REL
    rules_text = snap_rules if snap_rules is not None else (rules_path.read_text(errors="replace") if rules_path.is_file() else "")
    if snap_rules is None:
        flags.append("no turn-1 snapshot of the rules file: its lines are taken from the final tree")
    lines = file_lines(rules_text)
    n_file_lines = len(rules_text.splitlines())
    sha0 = setup_sha1(arm)
    if snap_rules is not None and sha0 and hashlib.sha1(snap_rules.encode()).hexdigest()[:len(sha0)] != sha0:
        flags.append("the arm changed its rules file in turn 1 (the turn-1 snapshot differs from what setup.py built)")
    instr_text = "".join((snapshot_text(arm, f) if snapshot_text(arm, f) is not None else ((arm_dir / f).read_text(errors="replace") if (arm_dir / f).is_file() else ""))
                         for f in ("CLAUDE.md", "AGENTS.md"))
    bidx = [i for i, r in enumerate(recs) if boundary.is_boundary(r)]
    before = int(tk["boundaries_before"]) if str(tk.get("boundaries_before", "")).isdigit() else None
    cut = None
    if before is None:
        cut = bidx[-1] if bidx else None
        if bidx: flags.append("no launcher count of boundaries before the compaction call: the last boundary is used")
    elif len(bidx) > before:
        cut = bidx[before]
    row["transcript"] = {"found": True, "records": len(recs), "boundaries": len(bidx), "cut_boundary_number": (before + 1) if before is not None else None,
                         "boundary_index": cut, "rules_non_empty_lines": len(lines), "unparsed_lines": unparsed}
    if not lines:
        reasons.append("the arm's rules file is missing or empty")
        for k in ("i", "ii", "iv"): row[k] = {"value": None, "reason": reasons[-1]}
    calls, results = collect(recs)

    # (iii) the compaction: the launcher's word, and the transcript's own
    last = recs[cut] if cut is not None else None
    trig, pre, post = boundary.meta(last) if last else (None, None, None)
    tb = ta = None            # C6: main-chain assistant records of the pinned model with a count above 0
    for i, r in enumerate(recs):
        if isinstance(r, dict) and r.get("type") == "assistant" and not r.get("isSidechain") and is_own_pinned(r) and (prompt_tokens(r) or 0) > 0:
            if cut is not None and i < cut:
                tb = prompt_tokens(r)
            elif cut is not None and ta is None:
                ta = prompt_tokens(r)
    shrank_rec = (ta < tb) if isinstance(tb, int) and isinstance(ta, int) else None
    shrank_bnd = (post < pre) if isinstance(pre, int) and isinstance(post, int) else None      # the boundary's own numbers decide when present
    shrank = shrank_bnd if shrank_bnd is not None else shrank_rec
    pairs_disagree = shrank_rec is not None and shrank_bnd is not None and shrank_rec != shrank_bnd
    row["iii"] = {"launcher": {"proven": tk.get("compaction_proven"), "by": tk.get("by"), "pre_tokens": tk.get("pre_tokens"),
                               "session_same": tk.get("session_same"), "boundaries_before": tk.get("boundaries_before"),
                               "boundaries_after": tk.get("boundaries_after"), "turn2": tk.get("turn2")},
                  "transcript": {"boundaries": len(bidx), "cut_trigger": trig, "pre_tokens": pre, "post_tokens": post},
                  "prompt_tokens_last_before_boundary": tb, "prompt_tokens_first_after_boundary": ta, "context_shrank": shrank,
                  "shrank_by_records": shrank_rec, "shrank_by_boundary": shrank_bnd, "token_pairs_disagree": pairs_disagree,
                  "launcher_and_transcript_agree": ((tk.get("compaction_proven") == "1") == (cut is not None)) if tk.get("compaction_proven") is not None else None}
    if before is not None and tk.get("boundaries_after") is not None and str(len(bidx)) != tk["boundaries_after"]:
        flags.append(f"transcript holds {len(bidx)} boundaries; the launcher counted {tk['boundaries_after']} after the compaction call")
    for k in ("t1", "t1b", "t2"):
        if k in st["exit_codes"] and st["exit_codes"][k] != 0:
            flags.append(f"{k} exit code {st['exit_codes'][k]}")
    for k in ("t1", "t1b", "t2"):
        if (row["vi"][k] or {}).get("is_error"):
            flags.append(f"{k} reported is_error")
    if st["exit_codes"].get("cp") not in (None, 0):          # B7: whatever the proof says
        reasons.append(f"the compaction call exited {st['exit_codes']['cp']}")
    t2_killed = "t2" in st.get("killed", []) or st["exit_codes"].get("t2") == 142
    win_end = None
    if snap_rules is not None and rules_path.is_file() and file_lines(rules_path.read_text(errors="replace")) != lines:
        flags.append("the rules file in the final tree differs from the t1 snapshot's")

    if cut is None:
        why = "no compaction boundary in the transcript at the launcher's count" if before is not None else "no compaction boundary in the transcript"
        for k in ("i", "ii", "iv"):
            row[k] = {"value": None, "reason": why}
        reasons.append(why)
    elif lines:
        B = cut
        seg1 = segment(calls, results, arm_dir, lines, n_file_lines, -1, B)
        seg2 = segment(calls, results, arm_dir, lines, n_file_lines, B, len(recs))
        hi = seg2["first_write"]["idx"] if seg2["first_write"] else len(recs)
        win_end = seg2["first_write"]["idx"] if seg2["first_write"] else None
        keys = ("class", "note", "first_write", "sequence", "delivered_unresolved", "unplaced_forms")
        row["iv"] = {k: seg1[k] for k in keys}
        row["i"] = {k: seg2[k] for k in keys + ("late_accesses", "other_files", "non_reading_mentions", "unresolved_mentions", "rules_in_results_of_other_calls")}
        row["ii"] = handed_back(recs, calls, results, B, hi, lines, arm_dir, instr_text)
        ii = row["ii"]
        row["occasion"] = {"attachments_naming_rules": occasion_attachments(recs, B, hi, arm_dir), "distinct_files_touched_before_boundary": files_touched_before(calls, B, arm_dir)}
        if row["occasion"]["attachments_naming_rules"]:
            reasons.append("after the boundary the tool left an attachment that names the rules file (" + ", ".join(f"{a['type']}/{a['kind']}" for a in row["occasion"]["attachments_naming_rules"]) + "): not the occasion the census found (02_tasks.md D2)")
        # D4: (iv-b), the restore at the start of turn 1b, reported and deciding nothing
        ib = next((i for i in range(B) if isinstance(recs[i], dict) and is_prompt_record(recs[i]) and user_text(recs[i]).rstrip("\n") == T1B.rstrip("\n")), None)
        if ib is None:
            row["ivb"] = {"value": None, "reason": "no turn-1b prompt record before the boundary" + (" (a 3-call design)" if "t1b_sha" not in tk else "")}
        else:
            sb = segment(calls, results, arm_dir, lines, n_file_lines, ib, B)
            row["ivb"] = {k: sb[k] for k in ("class", "note", "first_write", "sequence", "delivered_unresolved", "unplaced_forms")}
        if ii["x_plus_n"] >= ii["threshold"]:                                      # C3: one list, one threshold, both conditions
            reasons.append(f"x + n = {ii['x']} + {ii['n']} = {ii['x_plus_n']} of K={ii['K']} lines held by the instruction file or handed back (threshold {ii['threshold']}): not an occasion")
        if ii["x"]:
            flags.append(f"the arm's instruction file holds {ii['x']} line(s) of K at the turn-1 snapshot (0 as seeded)")
        if ii["K_lines_in_snapshot_rules"] != kset.K_SIZE:
            flags.append(f"the turn-1 snapshot's rules file gives {ii['K_lines_in_snapshot_rules']} of the {kset.K_SIZE} lines of K")
        if row["i"]["class"] == "attempted":
            reasons.append("attempted: an access of a whole form delivered no line of K (the tool withheld the text) and no other access in the window was whole")
        if ii["request_copies_unreadable"]:
            flags.append(f"{ii['request_copies_unreadable']} request copy(ies) before the first tool result cannot be read as text: (ii) was not tested there (02_tasks.md C5)")
        if row["i"]["rules_in_results_of_other_calls"]:
            flags.append(f"lines of K in the result of {len(row['i']['rules_in_results_of_other_calls'])} call(s) in the window that did not name the rules file: hand-read (02_tasks.md C7)")
        for seg_name, seg in (("(i)", row["i"]), ("(iv)", row["iv"])):
            if seg["unplaced_forms"]:
                flags.append(f"{seg_name}: an access of a form the reader cannot place delivered no line: {seg['unplaced_forms']} - hand-read (02_tasks.md B1, C2)")
        if row["i"]["delivered_unresolved"]:
            flags.append("delivered-unresolved: a call the reader did not resolve, or one naming the rules file and BEMYAGENT.md, returned every line of the rules (class left to the hand-read, 02_tasks.md A3/B8)")
        if ii["preserved"]["any_rules_lines"]:
            flags.append("the compaction preserved records that hold lines of the rules")
        if ii["preserved"]["metadata_shape"] != "ok":
            flags.append(f"the boundary's metadata is {ii['preserved']['metadata_shape']}: preserved records and token numbers could not be read from it (02_tasks.md C8)")
        if ii["rest_of_turn"]["n"]:
            flags.append(f"{ii['rest_of_turn']['n']} of {ii['K']} lines of the rules handed back AFTER the window's end, in the rest of turn 2 (not counted in eligibility; the pilot stops on it)")
        if shrank is False:                                                          # B5, C6
            reasons.append(f"the context did not shrink at the boundary (records {tb} before, {ta} after; boundary {pre} before, {post} after): that is not a compaction")
        elif shrank is None:
            flags.append("the model's prompt tokens before and after the boundary cannot both be read")
        if pairs_disagree:
            flags.append(f"the token pairs disagree on the direction (records {tb} -> {ta}, boundary {pre} -> {post}): the boundary's numbers decided")
        further = [i for i in bidx if B < i < hi]
        if further:
            flags.append(f"a further boundary inside the window (record offset {further[0] - B})")
        # A5(b), B6, C9: turn 2 ran in this session
        ok_write = any(c["idx"] > B and c["write"] and results.get(c["id"]) is not None and (c["name"] == "Bash" or not results[c["id"]]["is_error"]) for c in calls)
        if t2_killed and not ok_write:
            reasons.append("turn 2 killed by the time limit")
        elif t2_killed:
            flags.append("turn 2 killed by the time limit after a write that succeeded: the window is complete, the arm stays (02_tasks.md C9)")
        if not t2_killed:
            if not any(is_prompt_record(r) and user_text(r).rstrip("\n") == T2.rstrip("\n") for r in recs[B + 1:] if isinstance(r, dict)):
                reasons.append("turn 2's prompt is not a user record after the boundary")
            if t2j and (t2j or {}).get("session_id") != sid:
                reasons.append("t2.json carries another session id than t1.json")
        failed = (st["exit_codes"].get("t2") not in (None, 0, 142)) or bool((row["vi"]["t2"] or {}).get("is_error"))
        no_call = not any(c["idx"] > B for c in calls)
        if failed and not ok_write and not t2_killed:
            reasons.append("turn 2 failed and made no write that succeeded: its window never closed")
        elif failed and ok_write:
            flags.append("turn 2 failed after a write that succeeded: the window is complete, the arm stays")
        elif no_call and not failed and not t2_killed:     # ruling 2026-11-15: the arm stays eligible, class none, flagged for the designer's look
            row["turn2_no_tool_call"] = True
            flags.append("turn2_no_tool_call: turn 2 ran, did not fail, and made no tool call after the boundary")
    if tk.get("compaction_proven") != "1":
        reasons.append("the launcher did not prove the compaction" if tk.get("compaction_proven") == "0" else "no launcher status for the compaction")
    if (tk.get("turn2") == "skipped" or not t2j) and not t2_killed:
        reasons.append("turn 2 did not run")
    if cert is None:
        reasons.append(f"certificate missing ({cert_where} not found in the output folder: run certificate.py <arm> > <out>/<arm>.cert.json)")
    elif not cert.get("clean"):
        failing = row["certificate"]["failed_terms"]
        fa = cert.get("fail_at") or {}
        only_late = bool(failing) and win_end is not None and all(
            fa.get(t) and all(isinstance(i, int) and i > win_end for i in fa[t]) for t in failing)
        if only_late:                      # B8: what an arm did after its reading cannot have changed it
            flags.append("certificate not clean only on calls after the window's end (terms: " + ", ".join(failing) + "): the arm stays; read its (vii) with that in mind")
        else:
            reasons.append("certificate not clean (failed terms: " + (", ".join(failing) or "see the certificate") + ")")
    dd = (cert or {}).get("tool_calls_dotdot")
    row["dotdot_calls"] = dd
    if dd:
        flags.append(f"{dd} call(s) through `..`: a call that reached another arm's tree before the window's end takes the arm out of (i) (02_tasks.md C4, hand-read)")
    row["eligible"] = not reasons and cut is not None
    row["eligible_reasons"] = reasons
    row["flags"] = flags
    return row


def summarize(rows):
    out = []
    for cond in ("C", "L"):          # control first
        arms = [r for r in rows.values() if r["cond"] == cond and r["role"] == "arm"]
        el = [r for r in arms if r["eligible"]]
        cls = lambda r: (r.get("i") or {}).get("class")
        has_ii = lambda r: (r.get("ii") or {}).get("n") is not None
        detail = lambda r: ({"x": r["ii"]["x"], "n": r["ii"]["n"], "x_plus_n": r["ii"]["x_plus_n"], "of_K": r["ii"]["K"],
                             "rest_of_turn_n_of_K": r["ii"]["rest_of_turn"]["n"], "added_line_handed_back": r["ii"]["added_line_handed_back"]} if has_ii(r) else None)
        att = lambda r: any(a["class"] == "attempted" for a in (r.get("i") or {}).get("sequence", []))
        out.append({"cond": cond, "arms": [r["arm"] for r in arms], "eligible": [r["arm"] for r in el], "n_eligible": len(el),
                    "whole": sum(1 for r in el if cls(r) == "whole"), "slice": sum(1 for r in el if cls(r) == "slice"),
                    "none": sum(1 for r in el if cls(r) == "none"),
                    "class_and_handed_back_per_arm": {r["arm"]: {"class": cls(r), "handed_back": detail(r), "eligible": r["eligible"]} for r in arms},
                    "attempted_access_in_window": [r["arm"] for r in arms if att(r)],        # C1: every arm with a withheld access, whatever its class
                    "turn2_no_tool_call": [r["arm"] for r in arms if r.get("turn2_no_tool_call")],
                    "delivered_unresolved_pending_hand_read": [r["arm"] for r in arms if (r.get("i") or {}).get("delivered_unresolved")],
                    "rules_in_results_of_other_calls": [r["arm"] for r in arms if (r.get("i") or {}).get("rules_in_results_of_other_calls")],
                    "handed_back_partly": {r["arm"]: (r["ii"]["x_plus_n"], r["ii"]["K"]) for r in arms if has_ii(r) and r["ii"]["x_plus_n"]},
                    "left_out": {r["arm"]: r["eligible_reasons"] for r in arms if not r["eligible"]}})
    return out


def safe_read(arm):
    """C8: one arm the reader cannot read does not end the read of the others: the failure is named, with no traceback"""
    try:
        return read_arm(arm)
    except Exception as e:
        return {"arm": arm, "cond": COND.get(arm, "?"), "role": "pilot" if arm in PILOT else "arm", "eligible": False,
                "eligible_reasons": [f"the reader failed on this arm ({type(e).__name__}): its transcript has a shape the reader does not know"],
                "flags": [], "reader_error": type(e).__name__}


if __name__ == "__main__":
    arms = sys.argv[1:] or ALL_ARMS
    rows = {a: safe_read(a) for a in arms}
    print(json.dumps({"arms": rows, "per_condition_over_eligible_arms": summarize(rows),
                      "note": "pilot arms are listed but not counted; the verdict table is not computed here"}, indent=1))
