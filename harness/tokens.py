#!/usr/bin/env python3
"""Aggregate token usage per arm from Claude Code session transcripts.

Prints ONLY numeric totals — never transcript content, which would be far too
large to read directly.

Usage:
    python3 tokens.py ~/.claude/projects/<project>/*.jsonl

Cost weights approximate published Claude pricing ratios, normalised so that
1.0 == one fresh input token. Raw token sums mislead here: cache reads are
~10x cheaper than fresh input and output is ~5x dearer, so an arm that reads a
lot of cached context looks expensive by raw count and is not.
"""
import json
import sys
from pathlib import Path

W = {
    "input_tokens": 1.0,
    "cache_creation_input_tokens": 1.25,
    "cache_read_input_tokens": 0.1,
    "output_tokens": 5.0,
}


def totals(path):
    acc = {k: 0 for k in W}
    msgs = 0
    for line in path.open(errors="ignore"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        u = (d.get("message") or {}).get("usage")
        if not u:
            continue
        msgs += 1
        for k in W:
            v = u.get(k)
            if isinstance(v, int):
                acc[k] += v
    acc["msgs"] = msgs
    acc["weighted"] = round(sum(acc[k] * W[k] for k in W))
    return acc


def main(paths):
    hdr = f"{'run':<14}{'msgs':>6}{'fresh_in':>10}{'cache_wr':>10}{'cache_rd':>11}{'out':>9}{'weighted':>11}"
    print(hdr)
    print("-" * len(hdr))
    for p in paths:
        p = Path(p)
        if not p.exists():
            continue
        t = totals(p)
        print(
            f"{p.stem[:12]:<14}{t['msgs']:>6}{t['input_tokens']:>10}"
            f"{t['cache_creation_input_tokens']:>10}{t['cache_read_input_tokens']:>11}"
            f"{t['output_tokens']:>9}{t['weighted']:>11}"
        )


if __name__ == "__main__":
    main(sys.argv[1:])
