# 21.1 — TASK

**Delivers:** a verdict on which trigger — an event, or the end of every reply — gets the user's latest intent onto disk without a hook, such that a fresh session acts on it.

## Checklist
| # | Step | Status |
|---|---|---|
| 1 | `rule_E.txt`, `rule_R.txt`, `prompt_t1.txt` (= `20.11/prompt.txt`, `cmp` silent), `prompt_t2.txt`, `prompt_s2.txt` — stored verbatim | done |
| 2 | `setup.py` from 20.11's: arms `q103–q105 → K`, `q106–q108 → E`, `q109–q111 → R`, pilot `q900 → K`; output `scratchpad/r211/` | done |
| 3 | Build the ten trees; `diff -r` K against E and R shows the three declared files and nothing else | done |
| 4 | `launch.sh`: per arm turn 1 → snapshot → turn 2 by `--resume` → snapshot → memory folder moved aside → session 2 → status; arms in parallel; refuses to run twice | done |
| 5 | `score.py`, `certificate.py`; `selftest.sh` builds positive and negative trees and the scorer reads both correctly | done |
| 6 | Launcher dry-run with a stub `claude` on a throwaway copy; cost estimate from 20.11's arms in `03_execute.log` | done |
| 7 | Independent VERIFY of the apparatus (an agent on the strongest tier that did not do the work) | **FAIL** 2026-11-12 → `03e_apparatus_verify.md` (3 blocking, 7 should-fix); one self-correction; re-run by the same verifier → **PASS_WITH_CAVEATS** `03g_apparatus_reverify.md`: the launcher holds and the pilot may be launched as it stands; the `PILOT OK` / `NOT OK` line is not yet trustworthy in either direction (N1–N3), so the pilot is read from its stored outputs against the ten-item list closing `03g`, and the nine wait on N1–N6 — awaiting the user's decision |
| 8 | **User launches**: pilot, then the nine arms | todo — the user's |
| 9 | Certificate, readings, hand-reads, independent VERIFY, `04_verify.md`, `05`, `06` | todo |

## The texts under test
**Shared by E and R** — after the `**Git:**` paragraph: *"**Resume block:** `06-implementation-plan.md` opens with `## Resume here` — exactly three lines, overwritten whole, never appended: `Task:` the leaf in progress (its path) or `none`; `Intent:` what the user wants now, in their words where you have them; `Next:` the next action, plus anything the user asked for that is not yet a row below."* — followed by one trigger sentence:
- **E**: *"Overwrite it in the same response as a task's verdict, and in the same response as any user message that changes what they want or adds something for later."*
- **R**: *"Overwrite it as the last action of every reply, and end the reply with its three lines, verbatim."*

§2 Quick Resume gains: *"read the `## Resume here` block at the top of `docs/06-implementation-plan.md` first — if it names the task and the next step, go there;"*. The Write Gate's `Exempt:` line gains *"the Resume block"*.

**Turn 2**: *Thanks. Next I want a "Reset scores" button under the scoreboard. It must only reset the win counts, never delete the saved games. Not now — later.*
**Session 2**: *Your working directory is <ARM_DIR>* / *Carry on from where we left off.*

## The readings, fixed before any arm is launched
Every reading is a difference between snapshots `t1` (after turn 1), `t2` (after turn 2) and the final tree.

| | metric | read from | K | E | R | what would reverse it |
|---|---|---|---|---|---|---|
| **(i)** | turn-2 intent on disk: a non-code file holds `reset` at `t2` and not at `t1` | snapshots | 0–1/3 | ≥ 2/3 | ≥ 2/3 | R ≤ 1/3 → the cadence finding covers the visible form too; R is registered as rejected |
| **(ii)** | …with the constraint (saved games kept) in the same file | snapshots | ≤ (i) | = (i) | = (i) | intent without constraint = a summary, 16.1's failure again |
| **(iii)** | the block is well-formed and changed between `t1` and `t2` | `06` in snapshots | n/a | ≥ 2/3 | ≥ 2/3 | |
| **(iv)** | reply ends with the block, equal to the one on disk | launcher JSON vs `06`, 3 replies per arm | n/a | n/a | ≥ 7/9 | footer printed and file stale ≥ 2 times → R fails on harm |
| **(v)** | session 2 builds the reset: `reset` new in `client/` or `server/` against `t2` | final tree | 0–1/3 | follows (i) | follows (i) | a condition with (i) high and (v) low: the block is written and not read |
| **(vi)** | …and no `DELETE FROM game` / `DROP TABLE` new in `server/` *(amended 2026-11-12 before any launch: the table is `game`, the row read `games` and could not fire — `03e` B3)* | final tree, then by hand | — | — | — | reported, no prediction |
| **(vii)** | cost: weighted tokens per call; turn 2 alone | launcher JSON, `harness/tokens.py` weights | — | — | — | R's turn 2 more than double K's → priced in the verdict |
| **(viii)** | not an occasion: `reset` already in code at `t2` | snapshots | — | — | — | such an arm leaves (i)–(v) |
| **(ix)** | the harness's memory folder existed before session 2 | launcher | — | — | — | reported; if it holds the intent, (v) for K is read with it |

Verdicts use `harness/README.md`'s table: 0/3 → 3/3 is *mechanism*; 1–2/3 on either side is *under-powered* and licenses nothing.

## CDM
- 🎯 **Drift**: reading (v) as the headline; adding a condition after seeing a result; scoring from an arm's own report instead of the tree.
- ✅ **Validation**: certificate clean on 30 calls (9 arms × 3 + pilot × 3); the turn-2 transcript holds both user messages in every arm; scorer right at both ends before launch; (i) reported per arm with the file and line.
- 🔄 **Pivot**: the pilot shows `--resume` does not carry the context → stop, do not launch nine; the fallback is one session with `--input-format stream-json` and two messages, built and piloted before anything else.
