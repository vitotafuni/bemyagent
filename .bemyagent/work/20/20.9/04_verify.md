# 20.9 — VERIFY

Six fresh Sonnet agents resuming six trees that had done the identical task: three left by an agent
under the protocol (q85 q87 q89) and three by an agent with no protocol file (q91 q92 q93). Copies
verified byte-identical to their sources before launch (`03b_copies.txt`). The prompts differ by one
sentence. **The first measurement of the Handoff Principle's own claim.**

## Against the readings fixed before launch

| | reading | arms at each end | verdict |
|---|---|---|---|
| (a) semantics survived | **6/6.** No arm touched `store.js`, `index.js`, `app.js` or `index.html`; no tally query is scoped | all six refused the premise | **ceiling, both sides** |
| (b) recall, 36 observations | **H 18/18 correct · C 15/18 correct, 3 silent, 0 wrong either side** | r85x r87x r89x r93x at 6/6 · r91x at 4/6 | **null** |
| (c) fabrication | **0 and 0.** Three candidates opened, three arms vindicated | r91x, r92x, r93x all cleared on inspection | **null, and the scorer was the unreliable part** |
| (d) cost | H 304 k · 173 k · 267 k (mean 248 k) · C 94 k · 204 k · 180 k (mean 159 k) | r92x (204 k) costs more than r87x (173 k) | **under-powered** |
| (e) status of the *why* | **H 3/3 CITED · C 3/3 INFERRED and labelled as inference. 0 ASSERTED** | r87x quotes `01_think.md` · r93x: *"The repo never states why"* | **clean separation, and the failure mode never fired** |

## Verdict: on a fixture this small the code carries the reasoning, and the documents change the provenance, not the outcome

Every arm reached the right answer. All six read a false bug report — *the scoreboard is wrong,
after a reload the numbers don't reset* — and all six refused it, left the behaviour alone, and
declined to invent a reset feature nobody asked for. **(a) is at ceiling on both sides.**

The documents did exactly one measurable thing: they changed **where the reason came from.**

- **With documents, every arm cited.** r87x quotes its predecessor's `01_think.md` — the client
  counter was rejected because it is *"lost on reload"*, and the assumption was *"won = all
  persisted games, across reloads"*. Both quotations are verbatim at lines 11 and 8 of q87's file;
  I checked. r89x cites the same reasoning and gets the hardest fact in the round right: q89 left
  **no new test file**, it extended `test/rules.test.js`, and the arm named exactly that.
- **Without documents, every arm inferred — and said so, unprompted.** r91x: *"No commit message,
  issue or spec documents the intent, so this is inference."* r93x: *"The repo never states why.
  The git history is a single commit, 'code map'."* Neither dressed a guess as a reading.
- **ASSERTED — a reason that sounds read and was guessed — did not occur once in six arms.** That
  is the failure mode (e) was written to catch, and it is absent. The control did not fabricate a
  rationale; it correctly reported that it was reconstructing one.

**This is a null on the claim as the protocol states it.** The Handoff Principle says `01` and `02`
are plans *a fresh zero-context agent could run*. On this fixture a fresh agent runs fine without
them. Ten files, one table, one query with no filter: **the code is short enough to be its own
documentation.** That is a statement about the fixture, and 02_tasks.md required it to be written as
one rather than as a refutation.

### The one reading that leans against the protocol

**Two control arms verified the tally against a running system. No protocol arm did.** r92x drove
two X wins on a throwaway database and read `{"X":2,"O":0}` back; r93x saved a win and re-read it
from a **fresh process**. The three protocol arms relied on `npm test` and on their predecessor's
notes — including its recorded `PASS_WITH_CAVEATS`, which two of them quoted.

That is 14.5's finding in a new shape: the side holding documents trusted them and did not
re-derive from the running system; the side holding nothing had to. Metric (c) was pre-registered
for the harm case and reads 0, because no one stated anything false. **The harm is not falsehood,
it is a check not performed** — and nothing in this round's rubric was reading for it. Named here
rather than scored, because inventing the metric now would be the repair 14.15 refused.

## The contamination finding, which outranks the round

r93x wrote: *"The AGENTS.md rules file lives in the parent bemyagent project and governs that
project's own docs, so I did not apply its docs workflow."* **No arm read that file with a tool
call.** The transcripts show it arriving as an injected attachment:

```
"attachment":{"type":"instructions","files":[{"path":".../bemyagent/AGENTS.md","type":"Project",
"content":"Read .bemyagent/docs/00-ai-rules.md before every task."},{"path":".../memory/MEMORY.md"
```

and in the arm's own system text: *"IMPORTANT: These instructions OVERRIDE any default behavior and
you MUST follow them exactly as written."*

**Every arm this project has ever run was handed the parent repository's `AGENTS.md` and the
session's `MEMORY.md`, as overriding project instructions.** All three control arms in this round
mention `AGENTS.md`; none opened it — **but see the addendum below: two of them opened the file it
points at.** This also explains the "memory leak across directories"
recorded three times (q79, q89, r89x): it was never a leak the arms went looking for, it is an
injection they all receive.

**What it means for the condition label.** *No protocol file of any kind* was never true. The
control is handed a one-line instruction to read `.bemyagent/docs/00-ai-rules.md`, in a tree where
that file does not exist. It affects 20.2, 20.3, 20.8 and this round.

**Which direction it biases.** Toward the control behaving more like the protocol side, or at least
knowing a protocol should exist. So **benefit readings are understated, not inflated** — 20.8's 5/6
against 0/9 survives this, and if anything the true gap is wider. A **harm** reading would be
inflated by it, and harm readings are the ones this record has trusted most (20.6 Q2).

**It is not fixable from inside this session** — *wrong, and corrected in the addendum below:
it is fixable, by a different launcher.* The injection is per-session, keyed to the primary
working directory, not to the arm's own directory — the arms already run from a scratchpad outside
the repository and receive it anyway. A clean control needs arms launched from a session whose
project directory is not this repository. Recorded in `harness/README.md`; no round should claim an
uncontaminated control until that is done.

### Addendum, 2026-11-09 — the injection is not a dead pointer, and 20.10 measured it

Both sentences above are true of `AGENTS.md` and leave the wrong impression. 20.10 counted, across
every subagent transcript this session holds, the arms that called
`<repo>/.bemyagent/docs/00-ai-rules.md` — the file `AGENTS.md` points
at — by absolute path in a tool call.

**r92x and r93x did, at their first tool call. So did r85x.** Across the whole project, **58 of 118
arm launches**, including **9 of the 12** arms labelled *no protocol file of any kind*: 20.2 3/3,
20.3 3/3, 20.8 1/3, this round 2/3 on the control side. They did not receive a pointer to a missing
file. They received the shipped protocol, 107 lines, in full, before looking at the tree they were
given.

The direction of bias recorded above is unchanged and is now measured rather than inferred. What
the measurement adds is that the exposure was **inert**: those twelve arms wrote **0** TTEV files
and emitted **0** `PROTOCOL_CHECK`s. The text in context is not the mechanism.

→ `work/20/20.10/04_verify.md`

### Addendum, 2026-11-09 — and the last paragraph above is wrong too

*"Not fixable from inside this session"* was reasoning about the harness, not a measurement of it.
A `claude -p` launched with its working directory inside the arm's own tree receives **no project
instructions at all**: `"type":"instructions"` 0 records, `AGENTS.md` 0, `00-ai-rules.md` 0, the
OVERRIDE header 0. A clean arm is buildable, and 20.11 is the round that builds one.

→ `work/20/20.11/03_execute.log`

## What this does not say

1. **One fixture, and a small one.** The null on (a) and (b) is a null *here*. A repository where
   the reasoning is not recoverable from ten files is exactly where the Handoff Principle would
   have something to buy, and this harness has never had one.
2. **One task, one hand-off, no context reset.** Still inherited.
3. **The resumers were told to write down what the previous work did.** A real resumption does not
   come with that instruction, and an agent asked to summarise summarises. The round measures
   recall under a prompt that asks for it, not recall that happens on its own.
4. **(d) is not a reading.** H costs 1.56× the mean but the ranges overlap, which at N=3 is the
   same non-answer 20.8 recorded. The H side also wrote 18–19 files against the control's 5; that
   is the protocol's definition, not a finding.
5. **N=3 a side.** (e)'s 3/3 against 3/3 is the only clean separation, and it is the metric added
   mid-round, pre-registered for four of the six arms and flagged on the other two.

## Cost of the round
Six Sonnet arms, 1.22 M weighted tokens. No arm trees were built: 20.3's and 20.8's were copied.
