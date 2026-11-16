"""21.4 - what a compaction boundary looks like, in ONE place, for the launcher (command line) and the
readers (import). Two shapes, both learned from structure only:
  * the transcript on disk: a record  type=system subtype=compact_boundary  with
    compactMetadata{trigger, preTokens, postTokens, ...}; the summary follows as a user record with
    isCompactSummary=true, then attachments (instructions, file, compact_file_reference, ...);
  * the stream-json output of `claude -p ... --output-format stream-json --verbose`: a record
    type=system subtype=compact_boundary  with compact_metadata{trigger, pre_tokens}
    (documented for the SDK, not yet seen under `-p`: either spelling of the keys is accepted).
Command line (prints one line, numbers only):
  boundary.py count  <transcript.jsonl>   -> <number of boundary records>
  boundary.py last   <transcript.jsonl>   -> <number> <trigger or -> <preTokens or -> <postTokens or -> of the last one
  boundary.py stream <cp.jsonl>           -> <found 0|1> <pre_tokens or -> <session id or ->
"""
import json, sys


def is_boundary(rec):
    return isinstance(rec, dict) and rec.get("type") == "system" and rec.get("subtype") == "compact_boundary"


def meta(rec):
    """(trigger, pre_tokens, post_tokens) of a boundary record, either key spelling; None where absent"""
    m = rec.get("compactMetadata") or rec.get("compact_metadata") or {}
    if not isinstance(m, dict):
        m = {}
    pick = lambda *ks: next((m[k] for k in ks if isinstance(m.get(k), (int, str)) and not isinstance(m.get(k), bool)), None)
    return pick("trigger"), pick("preTokens", "pre_tokens"), pick("postTokens", "post_tokens")


def unparsed_lines(path):
    """how many non-blank lines of the file are not a JSON object (C8): the readers drop them, so they are counted and printed"""
    n = 0
    try:
        with open(path, errors="replace") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    if not isinstance(json.loads(line), dict):
                        n += 1
                except Exception:
                    n += 1
    except OSError:
        pass
    return n


def records(path):
    out = []
    try:
        with open(path, errors="replace") as f:
            for line in f:
                try: out.append(json.loads(line))
                except Exception: pass
    except OSError:
        pass
    return out


if __name__ == "__main__":
    what, path = sys.argv[1], sys.argv[2]
    recs = records(path)
    if what == "count":
        print(sum(1 for r in recs if is_boundary(r)))
    elif what == "last":
        b = [r for r in recs if is_boundary(r)]
        t, pre, post = meta(b[-1]) if b else (None, None, None)
        print(len(b), *("-" if v is None else v for v in (t, pre, post)))
    else:
        b = [r for r in recs if is_boundary(r)]
        sid = next((r.get("session_id") for r in reversed(recs) if isinstance(r, dict) and r.get("session_id")), None)
        pre = meta(b[-1])[1] if b else None
        print(1 if b else 0, pre if pre is not None else "-", sid or "-")
