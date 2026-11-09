# Independent VERIFY — 20.10

Run by a Sonnet agent that did not perform the measurement, holding the six questions and the raw
transcripts and **none of this round's numbers**. Its own scripts, its own parser, its own scratch
directory. Reported here as received, with the reconciliation beneath.

## What it returned

| # | Question | Its answer |
|---|---|---|
| 1 | transcripts / carrying the instructions attachment | **202 / 179**; the 23 with no attachment at all are the `exp/runs/*` arms |
| 2 | arm transcripts calling the parent absolute path | **58**, listed by directory, `r154/q48` and `r154/q49` twice each |
| 3 | tool-call index, and order against the arm's own copy | index 1 in most, 0 in five, **`r11/w2` at index 3**; of the 48 that also called a non-parent path, **the parent came first in every one** |
| 4 | the twelve `N`/`C` arms, ceremony on disk | **zero for every arm**, with per-arm tool-call counts; 11 of the 12 read the parent file (by directory, 9) |
| 5 | the parent's `05-` / `06-` | **1 hit in 202**, in a research agent's report text, **no arm** |
| 6 | does the mirror differ A vs B | 14.13 **yes**, 15.4 **yes**, 19.2a **no** (`treat()` is a no-op where the anchor is absent), 19.5 **no — the file is never written at all** |

## Where it contradicted this round, and who was right

**It was right and the measurement was wrong, once.** Its question-2 count was 58 against this
round's 49. The gap is four whole arm populations — `r11/w1…w6`, `r18/z1…z3`, `exp/runs/*`,
`gf/arm-*` — dropped by a matcher that recognised only `q<N>` and `r<N>x` names. Those arms
pre-date the setup-script convention, so they are in no `ARMS` dict and the census never looked
for them. `score.py` now keys on the whole relative path, which also separates `r182/q1` from
`r182b/q1` — two different arms that shared a name. **Re-run: 118 arm launches, 58 parent reads,
agreeing with the verifier exactly.**

It also corrects F4: the latest parent read is not index 1 but **index 3, by `r11/w2`** — in the
population this round had not been counting.

And it corrects F6 from 0 to 1: one agent did call the absolute path of
`05-decisions-and-issues.md`, inside the text of a report rather than as a file operation, and it
is a research agent, not an arm. **No arm ever read this project's record.** `06-implementation-plan.md`
is 0.

**It was wrong once, and said so itself.** It places `r1413/q33`'s read at index 0 while noting
its two scripts disagree on whether that agent is an arm or a verifier. This round reads q33's arm
launch at index 1 and a separate q33 verifier at index 0, which is consistent with both of its
numbers.

**Its extra finding, which this round had not asked for:** 19.5's arms have **no
`00-ai-rules.md` at all** — its setup writes only `BEMYAGENT.md` and `settings.json`. And
re-running 19.5's setup today would fail its own assert, because the clause it was testing has
since landed in `BEMYAGENT.md` (52bb379).

**What it flagged as not derivable:** the word *arm* has three defensible denominators here — 118
launches, 114 distinct trees, or the 99 names declared in `ARMS` dicts. This round reports
launches and names the other two.
