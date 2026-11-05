"""What a round costs. Run over the agent transcripts of a session.

    python3 cost.py <tasks-dir>

Cache read dominates the raw total and is the cheapest token there is, so a raw sum is
meaningless. The weights below are ratios, not prices: re-check them before quoting money.
"""
import json, pathlib, sys
W = {"inp": 1.0, "cc": 1.25, "cr": 0.1, "out": 5.0}
T = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
agg = dict(inp=0, out=0, cc=0, cr=0); n = 0
for p in sorted(T.glob("*.output")):
    a = dict(inp=0, out=0, cc=0, cr=0)
    for line in p.read_text(errors="replace").splitlines():
        try: ev = json.loads(line)
        except Exception: continue
        u = ((ev.get("message") or {}).get("usage")) or ev.get("usage") or {}
        if not isinstance(u, dict): continue
        a["inp"] += u.get("input_tokens") or 0
        a["out"] += u.get("output_tokens") or 0
        a["cc"] += u.get("cache_creation_input_tokens") or 0
        a["cr"] += u.get("cache_read_input_tokens") or 0
    if any(a.values()):
        n += 1
        for k in agg: agg[k] += a[k]
if not n: sys.exit("no agent transcripts found")
w = sum(W[k] * agg[k] for k in agg)
print(f"agents: {n}")
for k, lab in (("inp", "uncached input"), ("cc", "cache write"),
               ("cr", "cache read"), ("out", "output")):
    print(f"  {lab:16} {agg[k]:>14,}   per agent {agg[k]//n:>10,}")
print(f"\nweighted equivalent: {int(w):,}   per agent {int(w)//n:,}")
print("NOTE: an arm is not an agent. Most arms spawn a second agent for the independent")
print("VERIFY in §4, so a six-arm round is about twelve agents.")
