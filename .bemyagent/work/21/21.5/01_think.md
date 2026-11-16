# 21.5 — THINK

## Context
Found 2026-11-12 while weighing a repo move: round scripts and notes carry the development machine's account name, folder layout, tool-config folder and temp paths. The repo is public. The user: remove every trace, and nobody can run the harness as it is. This leaf is the **working tree**; the history is 21.6, the `src/` layout 21.7.

Inventory (case-insensitive search, 2026-11-12): 75 tracked files and 15 untracked ones hold at least one of the four residue words; 71 are scripts, the rest are logs, verdicts and notes citing it. Published so far (last push 2026-10-29): 4 files. The words and the literal → placeholder table are kept **outside the repo** (`<scratchpad>/p215/patterns.txt`) — written here they would be the thing this task removes.

### Context Saturation Check
- [x] **Target files/paths** — every tracked or untracked-not-ignored file matching the residue search; ignored files (drafts, `log/`) are not published and are out of scope.
- [x] **Expected behaviour** — prose, logs, verdicts, JSON: the literal becomes its placeholder (`<repo>`, `<scratchpad>`, `<project-key>`, `<claude-config>`, `~`), nothing else on the line changes. Scripts: the repo root comes from the script's own location; machine-specific values (scratchpad, tool-config folder) come from the environment or from a gitignored `local.env` beside the script, with a clear error when absent.
- [x] **Constraints** — the ten seeded trees of 21.1 are not touched; the real `claude` is never run; `launch.sh` is never run; no number, verdict or finding changes; 21.1's apparatus was verified on 2026-11-12 and any edit to it goes back to the verifier.
- [ ] **Dependencies** — *assumption*: the name on the commits themselves is history, not working tree, and belongs to 21.6.

## Approaches Considered
- **A. One scripted pass with a fixed table, longest literal first, then hand edits of the script constants** (chosen): the same literal gets the same placeholder in 90 files; the diff of a note is a token swap and can be checked as such.
- **B. Delete the old round scripts.** They are the method behind published verdicts; a verdict whose script is gone cannot be re-read.
- **C. Fix only what will run again (21.1).** Leaves 80 files of the trace the user asked to remove.

## Selected Approach & Risks
A. Mechanical and wide → a Sonnet subagent (reason: token swaps by table and one repeated edit pattern in scripts; no judgement on findings). VERIFY: an agent that did not do the work, strongest tier per §4 — it must judge whether a swap changed what a finding says (several findings are *about* which file an arm read), which the builder's own grep cannot show.
- Estimated token cost: medium.

**Pre-mortem**
1. *A placeholder changes a finding* (20.9/20.10 turn on arms reading the parent repo's rules file). → placeholders keep the distinction: `<repo>` is the parent repo, an arm's tree is never `<repo>`; VERIFY reads those passages.
2. *A script edit breaks 21.1's verified apparatus.* → `selftest.sh` and `dryrun.sh` (stubs only) before and after, same counts; tree hash unchanged; the apparatus goes back to its verifier with N1–N6.
3. *Residue survives in a form the search does not spell* (URL-encoded, split across lines, the dash form). → the dash form is in the table; VERIFY searches with its own patterns, not the builder's.

**Devil's Advocate** — leave the working tree and rewrite everything in one history pass (21.6) with a replace-text table. One tool, one pass. Not chosen: a blind text replace turns `ROOT = "<repo>"` into a script that cannot run; the scripts need an edit a history filter cannot make. The table is reused by 21.6.

## Verification Plan
Independent agent: its own residue search over tracked + untracked-not-ignored → 0 files; every changed line of a non-script file differs from the backup only by table swaps; every `.py` compiles, every `.sh` passes `bash -n`; 21.1 selftest 82 PASS and dry-run verdicts unchanged; the ten trees' hash equals the baseline.
