# 21.2 — THINK

## Context
Spec: `docs/specs/restore-integrity.md`. Before a guard is written, its occasion is priced: how often does a session work on a partial read of `00-ai-rules.md`? One case is known (2026-11-11). The transcripts are on disk, so the answer costs no arm.

### Context Saturation Check
- [x] **Target files/paths** — `work/21/21.2/census.py`, `03b_census.json`; input: every `*.jsonl` under `<claude-config>/projects/`.
- [x] **Expected behaviour** — per transcript that touches a path ending in `00-ai-rules.md`: which of the section headings `## 1.` … `## 8.` appeared in tool **results** before the session's first file-changing call.
- [x] **Constraints** — numeric aggregates and transcript basenames only, never transcript content (the `harness/tokens.py` convention).
- [x] **Dependencies** — python3 standard library.

## Approaches Considered
- **A. Headings seen in tool results** (chosen). Reads what the agent actually received, so it catches a cut in the middle, a `head`, a `grep` slice and a persisted-output preview alike.
- **B. Classify the command only** (whole `Read` vs sliced). Cheaper, and blind to exactly the 2026-11-11 case: the command was a plain `cat`, the cut was in the output.
- **C. Count bytes returned against the file's size.** The file changed size across the window; headings are the stabler ruler.

## Selected Approach & Risks
A, with B's classification kept as a second column (first access: whole read alone · chained with other output · slice). Window: transcripts from the date the rules file first had eight sections (`git log -S`), so an older file is not scored as a short read. Split by kind of session: this repo's main sessions, their subagents, harness arms (project folder under a scratch path).
- Estimated token cost: low → a Sonnet subagent writes and runs it.

**Pre-mortem**
1. *The scorer misses the one known case.* → positive control: transcript `<session-id>.jsonl`, first access, must read **incomplete with §5 and §6 absent**; a later access in the same file must read complete. If either is wrong the scorer is wrong and no number is reported.
2. *Sessions fed the rules by injection, not by a tool call, look like "never read".* → they are a separate count (no access), never added to "incomplete".

**Devil's Advocate** — skip the census and ship the twenty-word count: it is cheap either way. Not taken: every line on the restore path is paid at every restore by every user, and *"cheap either way"* is how the file reached 14 KB.

## Verification Plan
Both controls pass; totals add up (accessed + not accessed = scanned); an independent agent recomputes the headline from the JSON and re-checks the control by hand.
