# 20.12 — TASK

**Delivers:** the protocol-versus-none comparison of 20.3, on controls certified to hold no
protocol text — a verdict on whether 20.3's test-with-teeth result survives without the
contamination footnote.

## Checklist

| # | Step | Status |
|---|---|---|
| 1 | `setup.py`: 20.11's with `ARMS = q100 q101 q102 → P`, output `scratchpad/r2012/` | todo |
| 2 | Build three trees, seed identity at first commit against `r203/q85` | todo |
| 3 | `prompt.txt` copied from `20.3/prompt_P.txt`; `cmp` must be silent **before** launch | todo |
| 4 | Launch three headless arms, 20.11's `launch.sh` with `R` and the prompt file changed only | todo |
| 5 | Certificate on the three new arms; first user message read from each transcript | todo |
| 6 | Teeth M1 and M2 (`mutate.py`, then by hand where the regex misses) | todo |
| 7 | `score.py` over the new arms and q97–q99 | todo |
| 8 | Independent VERIFY | todo |
| 9 | `04_verify.md`, `05`, `06`, commit | todo |

## The readings, fixed before any arm is launched

The control side is **already observed** (20.11): teeth M1 and M2 **0/2, q98 not applicable**
(no server tally), tests added 0/3, certificate clean 9/9. Only the P column below is a
prediction.

| | metric | read from | predicted, P | what would reverse it |
|---|---|---|---|---|
| **(i)** | teeth, M1 — a draw counts as a win for X | arm's `npm test` after the mutation | **3/3 RED** | below 2/3 → Pivot |
| **(ii)** | test cases added over the seeded four | the tree | **3/3** | a P arm at the seeded four |
| **(iii)** | delivery: tally, route, markup | the tree, by hand where the regex misses | **3/3** | any arm not delivering is reported before (i) is read |
| **(iv)** | cost | launcher `modelUsage` | recorded, under-powered by declaration | nothing at N=3 |
| **(v)** | teeth, M2 — totals swapped | as (i) | **agrees with (i) per arm** | a disagreement |
| **(vi-a/b)** | instruction records outside the arm / parent-path tool calls | arm transcripts and subagents | **0 · 0** | any non-zero: that arm is contaminated |
| **(vi-c)** | instruction records of any kind | as above | **exactly one each, the arm's own `CLAUDE.md`** | none → the reader is blind |
| **(vii)** | the treatment prompt arrived | first user message in the transcript | **contains "Read BEMYAGENT.md" on 3/3** | absent → the round is void, as 20.11 was |

## Honesty declaration
Nothing in the P column has been observed. The N column was observed in 20.11 and is cited, not
predicted.

## 🎯 Drift
Re-scoring 20.11's P arms, or reading this round's P against Agent-tool controls. The comparison
is clean P against clean N, and nothing else.

## ✅ Validation
Every cell filled from a command run during VERIFY, arms named at each end.

## 🔄 Pivot
P below 2/3 on (i): stop, report that the clean comparison does **not** reproduce 20.3 on this
launcher, and that launcher and protocol cannot be told apart in this round — do not attribute.
`interactiveMode=false`: report, do not ask.
