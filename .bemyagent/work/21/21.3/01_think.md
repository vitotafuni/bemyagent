# 21.3 — THINK

## Context
Spec: `docs/specs/rejected-register.md`. The register has to exist on this repo before its rule is worth measuring anywhere: this record holds the most rejections and has already walked one of them twice.

### Context Saturation Check
- [x] **Target files/paths** — new `docs/decisions/rejected.md`; sources `docs/05-decisions-and-issues.md`, `docs/06-implementation-plan.md` (dropped rows, Backlog), `docs/drafts/*.md`.
- [x] **Expected behaviour** — one table line per idea that was **evaluated** and turned down: *Idea* (as someone would propose it again, ≤ 12 words) · *Verdict* (date, kind: `measured-null` / `harm` / `redundancy` / `design`) · *Rests on* · *Reopens when* · *Evidence* (`file:line`).
- [x] **Constraints** — every cell traceable to a source line; where the source gives no reopening condition the cell says `not stated`; nothing is inferred into it. No line for an idea dismissed at the door.
- [x] **Dependencies** — none.

## Approaches Considered
- **A. One file, read whole** (chosen): catches a paraphrased re-proposal, which a grep cannot.
- **B. One ADR per rejection in `decisions/`** (what the folder was made for). Forty files nobody lists; the index is still missing.
- **C. A `Rejected` section inside `05`.** `05` is 175 KB and partly on the restore path; the section would be found by grep or not at all.

## Selected Approach & Risks
A. The sweep is mechanical and long (two files with 1–3 KB lines) → a Sonnet subagent. VERIFY is not mechanical: §4 puts it on the strongest tier, run by an agent that did not do the work. *(Corrected 2026-11-12: first written as "a second Sonnet"; the user caught it.)*
- Estimated token cost: medium.

**Pre-mortem**
1. *The register invents a tidy reopening condition the source never gave.* → `not stated` is a legal cell, and VERIFY samples exactly that column.
2. *It becomes a second `05`.* → hard cap: one line per idea, no prose, ≤ 60 lines; the evidence column points, it does not quote at length.
3. *Rejections later reversed are listed as standing.* → a `Status` word per line: `stands` / `reopened → where` / `reversed → where`.

**Devil's Advocate** — let the next re-proposal find its verdict by grep, as the 2026-11-11 review did find Decision 18. It found the verdict and missed that its premise was dead; the column that would have shown it is the one this file adds.

## Verification Plan
An independent agent draws ten lines, opens each cited source line and confirms idea, premise and reopening condition; any cell not supported is a defect of the register.
