## Context
The user's reframe of the Graphify question, 2026-10-10: the problem with the code map is
**freshness, not retrieval**, and *"l'agente potrebbe trovare da solo il sistema migliore per
costruirsi una code map efficiente senza che sia un llm a farlo."* The draft turned that into a
candidate: the structural layer is produced by a **deterministic command the agent determines
once at bootstrap**, so drift becomes detectable by diff instead of merely less likely.

This is the first open candidate in months that is **not a prose rule asking an agent to notice
something**. Four candidates in a row have just been rejected or measured null, all of that
family, and this repo's record says the family goes near zero. That is the reason to run this
one now.

Round 1 is the question the draft itself named and left at zero data: **can an agent actually
produce a good generator?**

### Context Saturation Check
> 2+ unchecked → STOP and ask the user. 0-1 → state the assumption explicitly, proceed.

- [x] **Target files/paths** — the delta is an addition to the `03-code-map.md` template block
      in `BEMYAGENT.md`. Scoring reads each arm's generated `03-code-map.md` and runs the
      command it names.
- [x] **Expected behavior** — the draft fixes it: (i) does the command execute, (ii) does its
      file set match `git ls-files`, (iii) is it re-runnable by a different agent with no
      context. Criterion (iv) added below and justified.
- [x] **Constraints** — the protocol must stay stack-agnostic: it never names a tool, the
      project stores a concrete command. One portable markdown file stays the deliverable.
- [x] **Dependencies** — none new for the protocol. The fixture needs `node_modules` present.

**0 unchecked. Proceed.** One assumption stated: no baseline arm is run, because the shipped
protocol produces no command at all and a baseline would score 0/3 on all three criteria by
construction. Stating that is honest; spending three arms to confirm it is not.

### The premise this round must verify before launching, and why
A generator is only interesting if **getting it wrong is possible**. On a 12-file flat project,
any enumeration matches `git ls-files` and criterion (ii) is at the ceiling — the exact failure
that made 15.10 meaningless and voided 18.2's harm metric.

So the fixture is prepared to make the mistake available: `node_modules` installed **after** the
initial commit, so it is present on disk and untracked, and **no `.gitignore`**, which is the
fixture's real state and which all nine previous arms flagged. A naive `find . -name '*.js'`
then returns thousands of files; a correct generator returns twelve. The gap must be confirmed
by running both before any arm starts.

## The delta under test
Added to the `03-code-map.md` template block in `BEMYAGENT.md`:

> `## Inventory command`
> `` `<command>` `` — one deterministic command that enumerates this project's source files and
> their symbols, determined once from the stack. It must exclude vendor directories, build
> output and anything untracked. Re-run and diff it instead of trusting the rows below.

Step 0 BROWNFIELD already performs the shallow scan that fills `03`; this replaces the
mechanical half of that scan's output with a command. It is a substitution at a step that
exists, not a new concept.

## Approaches Considered
1. **Three arms, treatment only, feasibility.** The artifact is forced by construction — a
   command either runs or it does not — and the scoring is executed, not read.
2. **Six arms with a baseline.** Rejected: the baseline's score is known by construction.
3. **Measure the diff-detects-drift claim directly** by mutating the repo and seeing whether an
   agent catches it. That is round 2 and depends on this one: there is nothing to diff until a
   generator exists.
> Not discarded forever: if the arms produce commands too different to compare, 2 may be needed.

## Selected Approach & Risks
Chosen: **1**.
- Estimated token cost: **low**.
- **Risk — the ceiling.** Handled above by preparing the fixture so a wrong answer exists, and
  verified by measurement before launch rather than by argument.
- **Risk — the generator carries unearned authority**, the draft's own structural weakness: a
  derived artifact reads as true because a tool produced it. Criterion (iv) below is the first
  cheap probe of it.
- **Risk — scoring my own candidate.** Every criterion is executed: run the command, diff the
  output against `git ls-files`, re-run it in a clean copy.

### Pre-mortem
1. *All three name `git ls-files` and the round is a ceiling after all.* Then the answer is that
   the generator question is easy on a JS repo, the round says so, and the interesting case
   moves to a polyglot fixture. That is still an answer, and it is cheap.
2. *The commands are not re-runnable* because they embed an absolute path or a transient file.
   That is criterion (iii) doing its job, not a failed round.

### Devil's Advocate
Skip the generator and fix the trigger wording instead — *"any file added to or removed from the
repo"* — which is one line and costs nothing. Rejected on the draft's own argument, now backed
by four more rejections: that patches one trigger and leaves the class intact, and the class is
*any rule that depends on the agent classifying an event correctly*. The whole point of this
candidate is that it asks the agent to notice nothing.

## Verification Plan
Per arm, all executed:
- **(i) Runs.** Execute the named command in the arm's own tree. Exit code and output.
- **(ii) Correct file set.** Compare the paths it emits against `git ls-files`. Precision and
  recall, both reported — a generator that misses files is the main harm, and one that includes
  `node_modules` is the naive failure the fixture was prepared to expose.
- **(iii) Re-runnable with no context.** Run the same command in a fresh clone of the fixture by
  a process holding nothing but the command string. Same output or not.
- **(iv) Does it claim more than it derives.** Added, and justified: the draft's structural
  weakness is that a derived artifact carries authority a hand-written one does not. Check
  whether the arm presented hand-written rows as if the command had produced them, which is the
  cheapest observable form of that failure.
