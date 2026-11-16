"""21.4 - synthetic transcripts in the on-disk shape learned from structure only (03_execute.log [2]), used by
selftest.sh and by the stub of dryrun.sh. Every record carries the fields the readers use: type, subtype, cwd,
sessionId, message{role, content, model, usage, id}, attachment{type, ...}, isCompactSummary / isMeta. A compaction
is, in file order: system/compact_boundary (compactMetadata{trigger, preTokens, postTokens}), a user record with
isCompactSummary=true, attachments (instructions, file, compact_file_reference), and - for a manual /compact - a
meta user record, the command echo and its stdout as user records.
"""
import json, pathlib, re

OVR = "OVERRIDE any default behavior"
MODEL = "claude-sonnet-5-5"
RULES = ".bemyagent/docs/00-ai-rules.md"


def numbered(text):
    """the Read tool's result format: right-aligned line number, an arrow, the line"""
    return "\n".join(f"{i + 1:6d}→{l}" for i, l in enumerate(text.splitlines()))


class T:
    def __init__(self, arm_dir, sid, tokens=50000):
        self.arm, self.sid, self.recs, self.n, self.tokens = str(arm_dir), sid, [], 0, tokens
        self.cwd = str(arm_dir)

    def _base(self, typ, **kw):
        self.n += 1
        r = {"type": typ, "uuid": f"u{self.n}", "parentUuid": f"u{self.n - 1}" if self.n > 1 else None, "sessionId": self.sid,
             "cwd": self.cwd, "isSidechain": False, "version": "x", "timestamp": f"2026-01-01T00:00:{self.n % 60:02d}Z"}
        r.update(kw)
        self.recs.append(r)
        return r

    def instructions(self, path=None, n_override=2, extra_files=()):
        files = [{"type": "Project", "path": path or self.arm + "/CLAUDE.md", "content": " ".join([OVR] * n_override) + " Read .bemyagent/docs/00-ai-rules.md before every task."}]
        files += [dict(f) for f in extra_files]
        return self._base("attachment", attachment={"type": "instructions", "files": files})

    def other_attachment(self, typ, **kw):
        return self._base("attachment", attachment={"type": typ, **kw})

    def user(self, text, meta=False):
        extra = {"isMeta": True} if meta else {}
        return self._base("user", message={"role": "user", "content": text}, **extra)

    def assistant_text(self, text="ok", model=MODEL):
        return self._base("assistant", message={"role": "assistant", "id": f"m{self.n}", "model": model,
                          "content": [{"type": "text", "text": text}], "usage": {"input_tokens": 5, "cache_read_input_tokens": self.tokens, "cache_creation_input_tokens": 100, "output_tokens": 10}})

    def tool(self, name, inp, result, is_error=None, model=MODEL, result_after=()):
        """an assistant record with one tool_use and, right after, the user record with its result.
        result_after: tool calls (name, inp, result) issued in the SAME assistant turn before the result arrives."""
        tid = f"t{self.n + 1}"
        self._base("assistant", message={"role": "assistant", "id": f"m{self.n + 1}", "model": model,
                   "content": [{"type": "tool_use", "id": tid, "name": name, "input": inp}],
                   "usage": {"input_tokens": 5, "cache_read_input_tokens": self.tokens, "cache_creation_input_tokens": 100, "output_tokens": 10}})
        pend = [(tid, result, is_error)]
        for (n2, i2, r2) in result_after:                 # parallel calls: all uses first, then all results
            t2 = f"t{self.n + 1}"
            self._base("assistant", message={"role": "assistant", "id": f"m{self.n + 1}", "model": model,
                       "content": [{"type": "tool_use", "id": t2, "name": n2, "input": i2}],
                       "usage": {"input_tokens": 5, "cache_read_input_tokens": self.tokens, "cache_creation_input_tokens": 100, "output_tokens": 10}})
            pend.append((t2, r2, None))
        for (t, r, e) in pend:
            blk = {"type": "tool_result", "tool_use_id": t, "content": r}
            if e is not None: blk["is_error"] = e
            self._base("user", message={"role": "user", "content": [blk]}, toolUseResult={"type": "text"})

    def tools_one_record(self, calls, model=MODEL):
        """ONE assistant record holding several tool_use blocks, in the order given, then one user record per result.
        calls: [(name, input, result[, is_error])]"""
        blocks, results = [], []
        for c in calls:
            tid = f"t{self.n + 1}b{len(blocks)}"
            blocks.append({"type": "tool_use", "id": tid, "name": c[0], "input": c[1]})
            results.append((tid, c[2], c[3] if len(c) > 3 else None))
        self._base("assistant", message={"role": "assistant", "id": f"m{self.n + 1}", "model": model, "content": blocks,
                   "usage": {"input_tokens": 5, "cache_read_input_tokens": self.tokens, "cache_creation_input_tokens": 100, "output_tokens": 10}})
        for (t, r, e) in results:
            blk = {"type": "tool_result", "tool_use_id": t, "content": r}
            if e is not None: blk["is_error"] = e
            self._base("user", message={"role": "user", "content": [blk]}, toolUseResult={"type": "text"})

    def boundary(self, trigger="manual", pre=60000, post=9000, session_id=None, preserved=None, extra_md=None):
        """preserved: uuids of records kept across the compaction (the learned shape: the last records before the boundary)"""
        md = {"trigger": trigger, "preTokens": pre, "postTokens": post, "durationMs": 1}
        if preserved:
            md["preservedMessages"] = {"anchorUuid": f"u{self.n + 2}", "uuids": list(preserved), "allUuids": list(preserved)}
            md["preservedSegment"] = {"anchorUuid": f"u{self.n + 2}", "headUuid": preserved[0], "tailUuid": preserved[-1]}
        else:
            md["preservedSegment"] = {}
        if extra_md: md.update(extra_md)
        return self._base("system", subtype="compact_boundary", content="Conversation compacted", level="info",
                          compactMetadata=md, **({"sessionId": session_id} if session_id else {}))

    def last_uuids(self, k):
        """uuids of the last k records written so far (for `preserved=`)"""
        return [r["uuid"] for r in self.recs[-k:]]

    def summary(self, text="A summary of the work so far."):
        return self._base("user", message={"role": "user", "content": text}, isCompactSummary=True, isVisibleInTranscriptOnly=True)

    def file_attachment(self, path, content, start=1, num=None, total=None):
        lines = content.count("\n") + 1
        return self._base("attachment", attachment={"type": "file", "filename": path, "displayPath": path,
                          "content": {"type": "text", "file": {"filePath": path, "content": content, "numLines": num or lines,
                                                               "startLine": start, "totalLines": total or lines}}})

    def file_reference(self, path):
        return self._base("attachment", attachment={"type": "compact_file_reference", "filename": path, "displayPath": path})

    def manual_compact_tail(self):
        """the user records a manual /compact leaves after the summary: caveat (meta), command echo, stdout"""
        self.user("<local-command-caveat>Caveat: the messages below were generated by the user while running local commands.</local-command-caveat>", meta=True)
        self.user("<command-name>/compact</command-name>")
        self.user("<local-command-stdout>Compacted</local-command-stdout>")

    def write(self, cfg_projects):
        d = pathlib.Path(cfg_projects) / re.sub(r"[^A-Za-z0-9]", "-", self.arm)
        d.mkdir(parents=True, exist_ok=True)
        with open(d / f"{self.sid}.jsonl", "a") as f:
            for r in self.recs: f.write(json.dumps(r) + "\n")
        self.recs = []
        return d / f"{self.sid}.jsonl"
