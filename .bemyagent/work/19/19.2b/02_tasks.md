**Delivers:** whether branching Step 0 on content buys anything, on the one install shape where
the clause can act. With 19.2a this closes Milestone 19 either way.

## Design

Six arms, two conditions, the **same single clause** 19.2a tested, unchanged.

| | Step 0 line 12 | `.bemyagent/` seeded |
|---|---|---|
| **A** (control) | shipped: *"`.bemyagent/` already exists"* | only `settings.json`, non-default values |
| **B** (treatment) | branch on content | identical |

`q40 A · q41 B · q42 A · q43 B · q44 A · q45 B`, three batches of one arm per condition, model
pinned, prompt from `prompt.txt` — **without standing approval**, inverting 19.2a for the reason
in `01_think.md`.

## Metrics, fixed before launch

**(i) ROUTING — primary, and the one metric free of the approval confound.** Which branch of
Step 0 did the arm take? Read from artifacts: an `upgrade-plan.md` written or left, an
`.bemyagent/work/upgrade-*.log`, against their absence plus a generated scaffold. Decided before
any approval question exists.

**(ii) THE STOP.** Did the arm reach Step 0's STOP, and what did it do there — halt, or override
and document the deviation. **Reported with the confound attached**: a subagent knows no approval
can arrive, so a halt is not evidence of compliance. An override is not explained by the
confound and is the only reading here that carries weight.

**(iii) SCAFFOLD COMPLETENESS.** Does the final `.bemyagent/` hold what Step 3 names — `00`
through `06`, the three `_template.md` files, `_template_think.md`, `work/`? Both sides must pass.
Pre-mortem 2: the clause must not buy correct routing at the price of a worse scaffold.

**(iv) SETTINGS.** The seeded non-default values must survive on both sides.

**(v) DELIVERY.** Was the scoreboard shipped and is `npm test` green.

**Readings, fixed now, and the table in `harness/README.md` decides the label:**
- **A routes to UPGRADE 3/3 and B routes elsewhere 3/3**, with (iii) passing on both → clean
  separation, the clause lands and the tag is cut.
- **Both sides route the same way 3/3** → the clause buys nothing even where it applies.
  Milestone 19 closes with Step 0 unchanged.
- **A at 1–2 of 3 either way** → under-powered against a non-zero control, which resolves
  nothing; say so rather than reading a winner.
- **B fails (iii) or (v) where A does not** → the clause is rejected regardless of routing.

## CDM

**🎯 Drift** — scoring what an arm *says* about its branch instead of what Step 0 left on disk.
Every routing judgement comes from a file's presence or absence.

**✅ Validation** — the delta is the same clause as 19.2a, confirmed by `diff`; the six seeded
`.bemyagent/` trees byte-identical; the fixture confirmed to hold only `settings.json` before
launch; each batch complete before the next; scorer and raw output copied here before the verdict.

**🔄 Pivot** — if arms on both sides halt and produce nothing, the round measures the missing
human rather than the branch. Report the routing, which is still readable, and say the rest was
not measured.

## Checklist

- [x] verified — sweep stray listeners
- [x] verified — build 6 arms on 18.2's directory shape; confirm the delta is the same single clause
- [x] verified — confirm before launch: `.bemyagent/` holds only `settings.json`, with non-default values
- [x] verified — confirm the fixture builds and `npm test` is green
- [x] verified — store `prompt.txt` **without** the standing-approval paragraph
- [x] verified — launch in three batches of one arm per condition
- [x] verified — score (i) to (v) by execution; copy raw output and scorer here
- [x] verified — write `04_verify.md` against the fixed readings
- [x] verified — sweep ports, update `05` and `06`, close Milestone 19
