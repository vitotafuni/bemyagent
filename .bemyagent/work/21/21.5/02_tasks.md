# 21.5 — TASK

**Delivers:** a clone of this working tree shows nothing of the machine it was written on, and a round script finds the repo from wherever the clone sits.

## Checklist
| # | Step | Model, reason | Status |
|---|---|---|---|
| 1 | Backup of every file the pass can touch (122 files) → `<scratchpad>/p215/pre_sweep_backup.tgz` | main — one command | done |
| 2 | Table pass over non-script files (literal → placeholder, longest first) | Sonnet — mechanical | done — `03_execute.log` [5]–[8] |
| 3 | Scripts: root from the script's location; scratchpad / tool-config from environment or a gitignored `local.env`; `.gitignore` line for `local.env` | Sonnet — one repeated pattern | done — `03_execute.log` [5]–[8] |
| 4 | Builder's checks: residue search 0; `py_compile`, `bash -n`; 21.1 `selftest.sh`, `dryrun.sh`; tree hash | Sonnet | done — `03_execute.log` [5]–[8] |
| 5 | Independent VERIFY → `04_verify.md` | strongest tier, did not do the work — must judge whether a swap changed a finding | verified — `04_verify.md`: PASS_WITH_CAVEATS, re-check after self-correction: nothing blocks the commit |
| 6 | `05`, `06`; then the commit of milestone 21 can be proposed | main | done — `05` learning, `06` rows 21.5–21.7, `03` row, `harness/README.md` last section; the commit waits on the user (author name, 21.6) |

## CDM
- 🎯 **Drift**: rewriting notes beyond the token swap; "improving" old round scripts; touching the seeded trees; running anything that reaches the real `claude`.
- ✅ **Validation**: residue search → 0 files (tracked and untracked-not-ignored); non-script diffs are table swaps only; all scripts parse; 21.1 selftest 82 PASS, dry-run verdicts as in `03d_dryrun.txt`; trees' hash = baseline.
- 🔄 **Pivot**: a script that cannot be made location-independent without changing what it measured → stop, leave it, report it; more than two such → back to THINK.
