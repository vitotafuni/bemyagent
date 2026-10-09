Delivers: an evidence-backed answer to whether an agent invokes an optional code-graph tool
the Routing Table names — and whether procedural phrasing changes that — which gates any
adoption of Graphify as the structural half of the code map.

## Checklist

- [ ] Clear the smoke-test entry from `invocations/` before launching
- [ ] Confirm all 6 arms clean (no `.bemyagent/`, tool present and executable)
- [ ] Batch 1 = d-1, e-1 · batch 2 = d-2, e-2 · batch 3 = d-3, e-3 — one per condition each
- [ ] Verify each batch completed (finished, not stopped) before launching the next
- [ ] Do NOT score before all 6 are in
- [ ] Score from the invocation logs, not from arm self-reports
- [ ] Record verdict in `drafts/graphify-evaluation.md` + `05-decisions-and-issues.md`

## CDM

**🎯 Drift** — for THIS task, going off-track means:
- Grading the *quality* of the graph output. This round answers invocation only; the stub was
  built to make quality irrelevant and judging it here smuggles the next round's question in.
- Rewriting line 52 after seeing results and reporting the rewrite's run as the finding.
- Reading a high invocation count in arm e as evidence the tool is *useful*. It would be
  evidence the instruction was followed, which is a different claim.

**✅ Validation** — objective evidence of success:
- Per-arm invocation logs with timestamps and arguments, written by the tool
- Calls separated into orientation-time vs during-work, since "looked once" ≠ "worked with it"
- Arm e's forced artifact checked independently: do `03_execute.log` files cite returned nodes
- Counts stated n/3 with clean separation named as the only signal threshold

**🔄 Pivot** — pre-defined stop-and-rethink:
- **If d ≈ e ≈ 0/3**: the Graphify direction is closed for this protocol regardless of the
  product's merits, and the write-up says so plainly rather than proposing a third phrasing.
- **If e invokes but only to satisfy the log requirement** (a call whose output is never used
  in the work): that is the `Layers:` failure again — compliance without mechanism. Report it
  as such, do not count it as invocation.
- **If ≥2 arms die on infrastructure**: void the batch, rebuild, restart. Do not score partials.
- Obstacles exceeding `obstacleThreshold` = 2 → re-evaluate before continuing.
