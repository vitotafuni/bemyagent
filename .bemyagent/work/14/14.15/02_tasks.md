**Delivers:** the treatment half for the generated code map — does requiring VERIFY to re-run a
derived block make a weak baseline refresh it, and does it buy forgery instead.

## Design

Six arms, Sonnet pinned, three batches of two, one arm per side per batch.

| side | arms | protocol |
|---|---|---|
| **A control** | q79 q81 q83 | shipped |
| **B treatment** | q80 q82 q84 | + the derived-blocks clause in §4, both protocol files |

Seed: 20.5's G, byte for byte — `.bemyagent/` fully populated, `03-code-map.md` carrying an
Inventory that names a command and shows a **stale** block of its output.

Prompt: `prompt.txt`, 20.5's G text verbatim, with standing approval so the arm reaches the work.

## Metrics and the readings, fixed before launch

### Primary — FRESHNESS, per file in the inventory

For each file section in the block, the arm's map is compared against the output of **the command
the arm's own map names**, re-run in the arm's own tree. Eight files × three arms =
**24 observations a side**.

- **A stale and B fresh with clean separation per arm (0/3 vs 3/3)** → **the clause lands.**
- **Both fresh 3/3** → ceiling; 20.5's G reading needs re-examining, nothing lands.
- **Both stale 3/3** → null; the clause does not fire and is deleted as a candidate.
- **Any split** → null at N=3.

### Harm — FORGED LINES, per line

A line present in the arm's block but absent from that command's real output is forged. Counted
per line, both sides. **Any forgery on B that A does not show rejects the clause**, whatever the
freshness says. 14.12 saw nine such lines in one arm; the clause raises the incentive.

### Context
Delivery, tests, and whether `04_verify.md` records a `derived block … no diff` line.

## CDM — Heavy

**🎯 Drift** — scoring the arm's sentence about re-running instead of the bytes.
**✅ Validation** — as fixed in `01_think.md`.
**🔄 Pivot** — a session limit voids the round; rebuild, never resume.

## Checklist

- [x] verified — sweep ports
- [x] verified — build six arms, verify the delta is the clause line in both protocol files only
- [x] verified — store the prompt verbatim before launching
- [x] verified — three batches of two, Sonnet pinned
- [x] verified — score freshness per file and forged lines per line, raw output here before the verdict
- [x] verified — 19.4 check: open the arm at each end of every metric and name it
- [x] verified — sweep ports after, write `04_verify.md`, then `05` and the plan
