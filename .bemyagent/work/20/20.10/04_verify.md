# VERIFY — 20.10, the arms read the protocol out of the parent repository, and it changed nothing

Census `03b_census.txt`, per-round direction `03c_direction.txt`, raw output
`03d_score_output.json`, extractor `score.py`, reader `report.py`. No arms were launched.

## Against the CDM criteria fixed before launch

| Criterion | Result | Evidence |
|---|---|---|
| Every arm attributed or printed as a hole | **PASS only after the independent VERIFY corrected it** | The first pass matched only `q<N>` and `r<N>x` arm names and **dropped four whole populations** that pre-date the setup-script convention — `r11/w*`, `r18/z*`, `exp/runs/*`, `gf/arm-*`. `score.py` now keys on the whole relative path, which also separates `r182/q1` from `r182b/q1`. **118 launches over 114 distinct trees, 0 holes**; the 9 trees no `ARMS` dict names are counted and listed, not attributed |
| The read counted from a tool call, never from prose | PASS | `score.py` matches the parent **absolute path** inside a `tool_use` input. The body cannot serve: an arm's own mirror opens with the same heading as the parent's |
| Direction of effect stated per round before its count | PASS | `03c_direction.txt`, left column derived from each round's own ANCHOR counted in the tree the arms were built from (`git show <round-commit>^:…`) |
| The no-protocol controls checked for ceremony | PASS | `03b_census.txt`, `ceremony on disk` column: **NONE** on all twelve |
| Every corrected claim quoted as committed before it is struck | PASS | both strikes below, with the committed wording kept in place |

## The census

**58 of 118 arm launches called `<repo>/.bemyagent/docs/00-ai-rules.md`
by absolute path** — not their own copy, the real one. 107 lines, 14 KB, the shipped protocol in
full. Two of them used `head -100`, which still reaches §7 and includes §4 entire.

Every one of the 118 carried the injection.

| Round | what its setup mutates | arms | read | what the read does to its verdict |
|---|---|---|---|---|
| 14.13 | mirror **and** `BEMYAGENT.md` | 6 | **6** | B read the clause-free A text before its own |
| 15.4 | mirror **and** `BEMYAGENT.md` | 8 | **8** | same |
| 19.2a | `BEMYAGENT.md` only | 6 | 5 | the mirror carries no clause either way — harmless; **but q39 (B) read the parent `BEMYAGENT.md`** |
| 19.2b | `BEMYAGENT.md` only | 6 | 6 | harmless, same reason |
| 18.2 | two whole protocol variants | 12 | 7 | **q5 (`BMA.rev.md`) read the parent `BEMYAGENT.md`**, which is the other arm's condition |
| 20.2 | no-protocol control | 6 | **6** | the control read the protocol in full |
| 20.3 | no-protocol control | 6 | 3 | same, N side only; **P side 0/3** |
| 20.8 | no-protocol control | 3 | 1 | same, q91 only |
| 20.9 | copies of the above | 6 | 3 | same, r85x r92x r93x |
| 14.15, 18.3, 19.5, 20.5, 20.7 | — | 30 | **0** | not exposed |

## The three pre-registered unknowns

**F4 — order. Confirmed, and sharper than the prediction.** **57 of 58** exposed launches read
the parent file at their **first or second tool call**; the one exception, `r11/w2`, read it at its
fourth. Of the 47 that read their own copy at all, **47 read the parent's first.** The arm opens its session by
obeying the injected sentinel, before it has looked at the tree it was given. In 14.13 and 15.4
that means every B arm met the clause-free text before the clause it was being tested on.

**F5 — the verifiers. Confirmed.** **13 of 25 independent VERIFY agents** reached the same file,
including 14.13's and 15.4's. §4's second pair of eyes was reading the arm's work with the
unmutated protocol in context.

**F6 — the record. Confirmed where it matters.** **No arm, of 118, ever called
`05-decisions-and-issues.md` or `06-implementation-plan.md`.** One agent in 174 did — a research
agent, quoting the absolute path inside a report rather than opening it. No arm read this
project's conclusions about the rounds it was an observation in. The leak is the protocol and
nothing else in the record.

## What the protocol in context actually bought: nothing

The twelve arms given no protocol file — 20.2's q53 q55 q57, 20.3's q86 q88 q90, 20.8's q91 q92
q93, 20.9's r91x r92x r93x — produced **no `01_think.md`, no `02_tasks.md`, no `03_execute.log`,
no `04_verify.md`, and no `PROTOCOL_CHECK`, 0 of 12**. Nine of them had read the whole thing.

That is the finding, and it is a finding about the protocol rather than about the harness:
**the text is not self-executing.** An agent handed 107 lines under *"these instructions OVERRIDE
any default behavior"*, which opens its session by fetching them, produces none of the ceremony
and — 20.8 measured this — **writes no test**. What produced the test in 5 of 6 treatment arms was
not the text. It was the protocol installed as the tree's own governing file, with
`.bemyagent/work/` already there to write into.

## Two committed sentences this round contradicts

**`work/20/20.9/04_verify.md`**, line 73: *"All three control arms in this round mention
`AGENTS.md`; none opened it."* Literally true of `AGENTS.md`, and the impression it leaves is
false. r92x and r93x opened the file `AGENTS.md` points **at**, in the parent repository, at their
first tool call. Struck and corrected in place, dated.

**`harness/README.md`**, the section *No control arm here has ever been clean*: *"**It never
opened that file.**"* Same correction. The section is rewritten around the measurement: the
injection is not a dead pointer, it is the protocol delivered in full to half of every arm this
project has run, and inert in all twelve of the arms where it mattered most.

## What this does and does not overturn

**No verdict reverses. No clause ever shipped on a round whose manipulation was defeated.**

- **15.4 is strengthened.** B 3/3 left the gate's line in the repository and A 0/3 — and every B
  arm had read a clause-free copy of the mirror first. The separation survived its own
  contradiction.
- **14.13 is unaffected.** Its verdict is a ceiling on the A side, where the parent text and the
  arm's own text are the same bytes.
- **19.2a narrows.** Its B side is 2 observations, not 3: q39 read the parent `BEMYAGENT.md` and
  is not a B observation. The round's conclusion — rules out the harm, authorises 19.2b, evidences
  nothing — stands on one arm less than it claimed.
- **18.2 narrows the same way**, and it did not land.
- **19.5, the only protocol change in this window, is 0 of 6 exposed.** So is 20.7, and so is
  14.15.
- **20.2, 20.3, 20.8, 20.9**: the claim *no protocol file of any kind* is withdrawn as a
  description of the condition. The direction is unchanged from what 20.9 recorded, and now
  measured rather than inferred: a benefit reading is **understated** — the control had the text
  and did none of it — and a harm reading is **inflated**.

## Five defects in my own instrument — four found by reading its output, one by the verifier

`ast.literal_eval` on a comprehension; a role rule that assumed one launch-prompt opening out of
four; a mutation classifier that read a dead `treat()` branch out of 20.2's copied setup; the same
classifier contradicting 19.2a's own recorded `cmp` — where **19.2a was right and the instrument
was wrong**; and an arm matcher that recognised two naming conventions out of six and silently
dropped nine trees, which **only the independent VERIFY found**. None of the five was caught by
reading the code. All four were caught by
reading what it printed against something already in the record. That is 20.9's scorer finding a
second time, and it is why `03c_direction.txt` derives each round's mutation from its own anchor
at its own commit instead of from a sentence I would otherwise have typed.

Four obstacles against `obstacleThreshold` 2 triggered §4's Dynamic Pivot. Performed: the
alternatives in `01_think.md` were re-read, all four defects sit in attribution and none in the
needle, approach 2 stands. Declined and reported here, per `interactiveMode=false`.

## Independent VERIFY — it caught a missed population and the count moved

Run by an agent that did not do this work, holding the six questions and the raw transcripts and
none of the numbers above. Full report and reconciliation in `03e_independent_verify.md`.

**It was right against this round once, and the correction is in every number above.** Its
question-2 count came back 58 against the first pass's 49, because the matcher recognised only two
arm-naming conventions out of six. Re-keyed on the whole path: **118 launches, 58 reads, exact
agreement.** It also moved F4's worst case from index 1 to index 3 and F6 from 0 to 1.

Three defensible denominators exist for the word *arm* — 118 launches, 114 distinct trees, 99
declared names — and it flagged that before this round had noticed. The figures here are launches.

Five independent confirmations: the twelve controls at **zero ceremony each**, the parent read
ordering **first in every case**, 14.13 and 15.4's mirrors differing, **19.2a's not** — the point
on which the instrument had already been wrong once — and no arm touching the record. Plus one
finding nobody asked for: **19.5's arms have no `00-ai-rules.md` at all**, and re-running its setup
today would fail its own assert, because the clause it tested has since landed.

## Verdict: the condition was never what its directory said, and the text was never the mechanism

Two things are true at once and the round exists to keep them apart. **The harness has been
reporting an isolation it did not have** — in 14.13 and 15.4 the manipulation was contradicted
in-context, in 19.2a and 18.2 one arm each lost its condition, and in the four no-protocol rounds
the control was handed the whole protocol. **And the exposure bought nothing measurable:** 0 of 12
controls produced a single artifact, nine of them after reading all 107 lines.

19.2a checked this. Its criterion reads *"The condition cannot leak through the rules file —
PASS, `00-ai-rules.md` byte-identical across sides."* The check is sound, the `cmp` was real, and
it was run **at the boundary the harness built** — between the arms. The leak came from outside
it, by absolute path, at the arm's first tool call, in a round that had written the isolation
criterion down and ticked it.
