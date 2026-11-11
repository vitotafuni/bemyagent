# Harness — measuring whether a protocol rule actually works

BMA's rules are claims about agent behaviour. This harness is how those claims get
tested before a rule is allowed into `BEMYAGENT.md`. It exists because three separate
milestones found that reasoning about a rule predicts its effect badly:

| Milestone | Proposed | Survived measurement |
|---|---|---|
| 11 — mattpocock/skills candidates | 5 | 2 |
| 17 — greenfield field bug | 3 | 1 |
| 18 — landscape survey | 1 | 1, and only after a rewrite — the first draft measured **harmful** |

## Method

**One variable. Two arms. N=3 each.**

1. Copy `fixture/` into N×2 isolated directories, `git init` each.
2. Baseline arms get the current `BEMYAGENT.md`; treatment arms get a copy with the
   candidate rule applied — nothing else different. Diff the two files and confirm the
   diff is only the rule.
3. Run one subagent per directory, same prompt, same model, all in parallel.
4. Score the **mechanism**, not a downstream proxy.

`fixture/` is a small hot-seat tic-tac-toe app with real layer separation (schema →
store → API → client → tests). Feature requests against it — "add online multiplayer
with reconnect and ELO ratings" — cut through every layer at once and exceed one
context window, which is what makes decomposition rules observable.

## Six things a round must establish before it runs

Written 2026-11-07 after an audit found that most of this record's rejections may be artifacts of
the tier they were measured on. Each line is a question with a wrong answer, not advice.

**0. Has this condition already been run?** Added 2026-11-09, after 20.3's verdict closed by
naming *Opus + protocol* as the owed next round. That condition was 20.2's P side — same task,
same stored prompt, the same seed 20.3 had itself blob-hash-compared against, and metric (i) the
same instrument down to the docstring. Three Opus arms were nearly spent re-measuring a published
cell while the genuinely empty cell, Sonnet without the protocol, went unnamed. **Before pricing a
round, draw the grid of conditions this record already holds and mark the one being proposed.** It
is a grep over files already in the repository, it is the cheapest question on this list, and it
is the only one whose wrong answer wastes the entire budget rather than the verdict.

**1. Which regime is this rule for, and is the control in it?** BMA's scaffolding exists to get
good work out of an agent that would not produce it unaided. Measure it on the strongest model
and you are testing it where it is least needed. **The baseline's tier is part of the hypothesis,
not a setting.** Most rejections here took the shape *the baseline already does this* — which is
a claim about the baseline. If that baseline is stronger than the one the rule was written for,
the rejection says nothing about the rule.

**2. Is it a redundancy rejection or a harm rejection?** They do not deserve equal trust.
*The clause causes damage* holds or strengthens on a weaker model — a weaker agent will not
forge fewer blocks or invent fewer unfalsifiable commands. *The baseline already does it*
collapses the moment the baseline changes. **Auditing a redundancy rejection costs only the
control**, because the claim is about the control: re-measure it on the weaker tier and no
treatment arm is needed until it falsifies.

**3. Does the mechanism get an occasion, on this fixture, in this shape?** Already a rule above,
and still the most repeated failure here: 14.1 had no file over the slicing threshold, 18.2's
trap lay off the path, 15.9a's convention forbade something agents never do, and **20.2 measured
a protocol built for context resets by running one task in one unbroken context.** A mechanism
that cannot fire cannot be measured, and the round will still print numbers.

**4. How many observations does each metric actually have?** N=3 reads only clean separation, so
a metric with **one observation per arm** — did the mutation go red — can resolve almost nothing,
while a metric with **ten per arm** — how many of this arm's governed writes were gated — carries
real power at the same price. **Prefer per-occasion metrics over per-arm ones**; it is free, and
it is the only lever on this harness's weakest property.

**5. What does the answer cost, and is it worth that?** Every pre-mortem in the week this was
written argued validity — interpretability, occasion, control rate — and **not one argued price.**
A round is ≈ 7.8 M weighted tokens (see *What a round costs*). A pre-mortem that cannot conclude
*too expensive for what it can tell us* is incomplete.

And one the harness cannot do but should stop pretending about: **the protocol's primary audience
is the human**, and every metric here is machine-observable by construction. The nearest honest
proxy is mechanical and has never been run — **can a fresh agent holding only the repository
resume the work?** That is the Handoff Principle's own claim, and it is the shadow of *a person
can see what was done*.

## The four rules, learned the hard way

**1. Measure the mechanism, not the outcome.** "Does the glossary contain the new
terms?" resolved decisively at N=3. The token cost of the same change never resolved
and produced a false positive. Prefer the directly observable artifact of a rule over
its hoped-for downstream effect.

**2. Normalise before believing a metric.** One change looked 17% cheaper on weighted
tokens with complete separation across all 6 runs. It also produced 15% fewer lines of
output; cost-per-line was 3% apart with overlapping ranges. Divide any efficiency
metric by work done, or "did less" reads as "was faster".

**3. A forced output only works when the output IS the deliverable.** A `Layers:`
header declaring which layers a task cuts hit 100% compliance and changed nothing —
one task declared two layers while naming zero files. A claim about the work is free.
A glossary containing the new terms cannot be faked. Force the artifact, never the
assertion about it.

**4. Measure for harm, not only for benefit.** Milestone 18's first draft made the
protocol *worse*: unaided, agents caught a fabricated "done" record 3/3; with the new
procedure they followed its steps and ticked criteria against non-existent code 3/3,
and 0/3 spot-checked the premise. A new rule competes for attention with the rules
already there. Every candidate needs an arm where it could plausibly hurt.

## What this harness cannot measure

**Rules that depend on the user's authority.** Subagents always know they are subagents
and treat a coordinator's message as non-authoritative by construction — they say so in
as many words: *"an 'ok' relayed through the coordinator is not the user's consent."* So
any consent gate, exit condition on a human reply, or interaction-shaped rule will look
like it works in every arm, for a reason that has nothing to do with the rule. Those need
a human in a real session; measure a proxy artifact instead, or accept it is untested and
say so.

**Verify the planted defect actually exists.** A run once shipped with a comment
declaring a bug in code that was already correct. Every arm spot-checked the premise,
refused to edit, and the experiment measured §5 instead of its three target rules —
a wasted round. Reproduce the defect yourself before launching.

**Run the fixture before you run the arms.** `npm install && npm test` must
succeed on your Node version. A fixture that fails to build turns every arm into
a debugging session about the fixture: in one round, three arms spent their effort
diagnosing a native-module build failure, two installed a working version
out-of-tree to proceed, and one downgraded its own verdict because it could not
run HTTP-level checks. None of that is data about the rule under test — it is
noise injected by the measuring instrument.

**Strip the fixture's self-description.** An arm read the fixture README, saw the words
"harness fixture", and reasoned about being under test. Fixtures must read as ordinary
projects.

**Name the run directories neutrally.** An arm once wrote: *"given the directory is named
`gatebase-1`, bypassing the gate via a technicality seems like precisely the wrong
result."* Same protocol, same model, only the naming changed: neutral names gave 1 refusal
and 2 proceed; names that revealed the gate under test gave 3/3 refusals. Directory names
are part of the prompt. Use `a-1`, `b-1`, never `base`/`fix`/`gate`/`control`.

**Pin the arm model explicitly.** "Same prompt, same model" is not the default. A spawned agent takes its
model from its own definition's frontmatter when none is passed, so it can run on a different tier than the
session that launched it — found by probe in Milestone 14.4. Unpinned arms put model tier as a free
variable directly on top of the rule under test. Pass the model on every arm.

**Give the rule an occasion to fire.** Check the fixture can actually present the situation the rule
governs *before* designing arms. Milestone 13.2 measured null partly because Surgical Scope got one
accidental occasion in six arms; Milestone 14.1 found the fixture had no file above
`contextSlicingThreshold` at all — 158 lines total, largest 36 — so no read/slice/delegation rule could
ever trigger. `fixture/server/session.js` (~300 lines) exists for that class of rule.

**Batch arms across conditions, not within them.** A full round does not necessarily fit one
session's token budget: Milestone 14.3 launched 9 Heavy-ceremony arms at once and all 9 died
mid-flight on a session limit. The damage was not the lost round — it was the shape of what
survived. Arms died at uneven points, and because they were launched arm-by-arm the c-arms
died earliest: scoring that wreckage would have returned "the treatment is worse" as a clean
result, entirely an artifact of when the budget ran out. **Run one arm per condition per
batch**, so a budget death degrades every condition equally and shows up as a void round
rather than as a finding. Verify a batch completed before starting the next.

**Separate directories do not isolate arms — the network does not know about them.** Arms that
boot the fixture app all read `process.env.PORT || 3000`, so they collide, and a finished arm can
leave its server LISTENing. In Milestone 18.2 one arm's server was still holding port 3123 after
the arm had ended; a later arm's first check talked to it, saw a non-empty "empty" database and
served HTML without its own element, and came within one step of recording a defect in its own
correct work. It caught the collision itself; nothing in the harness would have. **Give each arm a
distinct high port, have it confirm the listener is its own process before trusting any response,
and sweep for leftover listeners when the round ends.** The same applies to any shared resource an
arm reaches by name rather than by path: ports, a fixed database path, a lock file.

**Sweep processes, not only listeners.** A listener sweep finds what holds a port, and an arm can
hang holding none. One 14.15 arm ran `cat > server/_tmp` with no input: its shell sat on stdin
for **two days**, through two rounds' sweeps, with the rest of its command chain — edits to a tree
already scored and committed — queued behind it. It was found by `pgrep` during 20.11, not by any
port check, and ended without touching the tree. When the round ends, look for any process whose
working directory or command line is inside an arm tree, and stop it before the next round reads
anything from that tree.

**A harm arm has to be reachable.** Planting a trap is not enough — the cheapest correct
implementation has to run into it. Milestone 18.2 planted a verifiable fact an arm was supposed to
be tempted to ask about, and 0/6 asked, because no arm's implementation ever needed it: the column
it would have queried already existed. A zero like that measures the fixture, not the rule, and
reporting it as a clean harm result is the easiest false negative this harness can produce. Check
that the trap lies on the path *before* the launch, the same way the planted defect is reproduced.

**Check the scorer before you believe it, and write down which arms you read.** Before a
metric's number goes into a verdict, open the arm at **each end** of that metric — the one it
scores best and the one it scores worst — and confirm the score matches what the arm actually
did. Record it in `04_verify.md` as one line per metric, **naming the arms**: *"(ii) read q32
(worst) and q28 (best) — scores match what the trees show"*. A line that names arms cannot be
written without opening them; a line that only asserts a check was made is the `Layers:` header
from rule 3, which hit 100% compliance and changed nothing.

Four scorer defects in three rounds, each caught by reading an arm rather than a number, each
one a false headline if it had not been:

| Round | The defect | Would have reported |
|---|---|---|
| 14.13 | a forged line defined as one the *seeded* command cannot emit | nine forged lines in a control arm that had merely improved the command its map names |
| 19.3 | governed writes counted from any Bash command with a `.bemyagent/` path near a redirect, sweeping up `diff`s that *read* the rules file | "first governed write preceded by a check: NO, 6 of 6" |
| 19.2a | the user's migrated conventions matched as whole sentences | the treatment preserving the user's rules only inside a backup file |
| 19.2b | routing read from `upgrade-plan.md` and the audit log, which an arm that skips the STOP writes neither of | the control never taking the branch the candidate was written to fix |

Three ran against the arms and one toward the candidate, so this is not a rule about watching
for bias in your own favour. **A scorer is an instrument built by the person who wants an
answer, and until this rule nothing in this harness checked it.** Where a verdict rests on a
single metric, hand that metric's definition and the trees to an agent that did not write the
scorer — §4's own reasoning about who verifies, applied to the measuring apparatus.

**Store the launch prompt verbatim, in the task folder.** A round's prompt is part of its
instrument and it changes behaviour as much as the clause under test. 14.9's first batch was
voided because the prompt had been reconstructed from a summary rather than copied: on the same
fixture and the same setup script that gave 14.8 three code maps out of three, the reconstructed
wrapper gave zero out of two, because both arms were sent down Step 0's approval branch instead.
Nothing about either side of the experiment was involved. Write the prompt to `prompt.txt` next
to the TTEV files, with the arm directory as the only substitution, and relaunch from that file.

**Verbatim from the right file: a reproduction takes each side's prompt from the round that ran
that side.** 20.11 stored its prompt verbatim and still sent the wrong one. It copied `prompt.txt`
from 20.8 — which had only a no-protocol side — and gave it to both sides, so the protocol arms
never got 20.3's *"Read BEMYAGENT.md in the repository root and follow it"* or its standing Step 0
approval. `cmp` against 20.3's `prompt_N.txt` returned identical; nobody ran it until the
independent verifier did, after the arms had spent their budget. The seed check that preceded it
was thorough — 102 blob comparisons — and checked everything except the one input that differed by
side. **Before a reproduction launches, `cmp` each side's prompt against the file the original
round launched that side from**, and name both files in `01_think.md`.

**Score the artifact against what it claims, not against what you seeded.** 14.13's scorer
defined a forged line as one the *setup's* command does not emit. One control arm improved the
command its own map names, so its block legitimately carried nine lines the seeded command cannot
produce — its new test file. Under that definition the arm reads as forging exactly nine lines,
the same count as the genuine forgery found a round earlier: a fabricated harm, in the control,
manufactured by the instrument and pointing the way the author already expected. A derived
artifact claims to be the output of *the command printed above it*; score it against that. The
general form is the bias check this file already demands — run it against the arms, not only
against the treatment.

**Shared scratch is not isolation either.** The port rule above generalises: arms write capture
files into the one scratchpad root under generic names (`inv_actual.txt`, `inv2.txt`, `blk3.txt`)
and clobber each other. In 14.13 one arm's verifier saw a **false** drift from a file another run
had overwritten. Scoring survived it only because every criterion re-runs inside the arm's own
tree, which is the rule: a measurement that reads anything from shared scratch is measuring the
other arms too.

**A partial round is not a small round.** When arms die early, do not score what is there.
The scorer will happily emit n/3 counts from half-finished trees and those counts read as
data. Rebuild the run directories from scratch — partial work contaminates them — and say
the round was void.

## Scoring

Grep the generated `.bemyagent/` tree for the artifact the rule is supposed to
produce, and read the arms that disagree.

**Decide what the control's rate is before you read the treatment's.** At N=3 three arms
resolve a condition only where that condition is near-deterministic. The three outcomes
below are not degrees of the same verdict, and collapsing them is how a round gets
reported as something it did not measure:

| Control | Treatment | Verdict | What it licenses |
|---|---|---|---|
| 0/3 | 3/3 | **the mechanism** | the rule lands |
| 0/3 | 0/3 | **null** | the rule is deleted: tested properly, no effect |
| 3/3 | 3/3 | **ceiling** | the rule is deleted, *and* the baseline already does it |
| ~1–2/3 | anything | **under-powered** | nothing. Resolve it or say it is unresolved |

A null and a ceiling both end with the rule not shipping, and only the second also says
something true about the baseline, so the record has to name which one it was.

**An under-powered round is not a null and must never be written up as one.** Where the
control sits in the middle, three arms do not measure the condition, they draw from it.
This is measured here, not reasoned: **14.12 and 14.13 ran the same control condition —
byte-identical protocol, rules file, seeded map, prompt and model pin, verified file by
file — and read 1/3 and 3/3.** At a true rate near 0.6 three arms return one hit about 29%
of the time and three about 22%. One of those two rounds was going to be wrong whatever the
candidate did, and 14.12's headline had to be corrected. 14.11 was refused on this
arithmetic before it ran and was called *uninterpretable*; that is the right word and this
section is where it should have lived.

Raising N is the remedy for a round worth resolving, not a new default — separating 1/3
from 3/3 with any confidence costs roughly ten arms a side. Most candidates here separate
cleanly at three and do not need it. The cheap move is to ask, before designing the arms,
whether the control plausibly sits at zero; where it does not, budget for the answer or
pick a different question.

## What a round costs

Measured 2026-11-05 over this project's 119 agent transcripts, with `cost.py` in
`.bemyagent/work/20/20.1/`:

| | total | per agent |
|---|---|---|
| cache read | 289.4 M | 2.43 M |
| cache write | 16.7 M | 140 k |
| output | 5.6 M | 47 k |
| uncached input | 10 k | 86 |

Weighted at cache-read 0.1×, cache-write 1.25×, output 5×: **≈ 78 M equivalent, ≈ 653 k per
agent.** Cache read is 93% of the raw total, which is the structural driver — an arm re-reads a
large context at every step, and a raw token sum is therefore meaningless.

**An arm is not an agent.** Most arms spawn a second agent for the independent VERIFY §4 asks
for, so **a six-arm round is about twelve agents, ≈ 7.8 M equivalent.** Price a round before
authorising it: four rounds and one voided batch in a single day hit a session limit, which was
arithmetic rather than bad luck.

State the other half of the number too. That day's four rounds changed **zero lines** of
`BEMYAGENT.md`. That is the expected outcome here — most candidates do not land — but it is the
figure that decides whether the next round is worth 7.8 M.

## Which model the arms run

The rule above says **pin** the model. It does not say which, and the choice was inherited rather
than argued: Opus, because the coordinator runs Opus and the record started there.

The case for keeping it was comparability with past rounds. **That case is weak on this harness's
own evidence**: 14.12 and 14.13 read the identical condition at 1/3 and 3/3, and the Write Gate's
coverage read 60% and 89% a day apart. Cross-round comparison is already untrustworthy, so little
is lost by changing tier, and the design protects itself anyway because control and treatment sit
in the same batch and the control is re-measured every time.

Against keeping it: **BMA ships to everyone and has only ever been measured on the most expensive
tier.** A clause that lands on one tier and not another is a finding about the protocol.

If the tier changes, three things hold: control and treatment in the same batch, the tier written
into `prompt.txt` and the round's log, and no comparison against another tier's numbers without
saying so. Two things do not change — the explicit pin, and the second agent arms spawn for
VERIFY, which is where they have found real defects in their own work.

Whether a cheaper tier needs more turns for the same task is a measurement, not an assumption:
read it off `cost.py` after the first round that uses one.

`tokens.py` aggregates per-arm cost from session transcripts, cache-weighted:

```
python3 tokens.py ~/.claude/projects/<project>/*.jsonl
```

Use it for cost, never for quality — see rules 1 and 2.

**A classifier was deliberately not shipped here.** An earlier version scored a task as
"vertical" by counting the files it enumerated, which rewards implementation-list prose
— exactly the horizontal style it was built to detect. It read 60→68→75→78% across
variants where the real signal was binary. A proxy metric must be checked for bias
*against the treatment* before its null is believed.

### No control arm here has ever been clean, and half of all arms read the protocol

Found 20.9, 2026-11-09, by an arm saying so out loud. r93x wrote *"The AGENTS.md rules file lives
in the parent bemyagent project and governs that project's own docs, so I did not apply its docs
workflow."* **Measured 20.10, 2026-11-09, across every subagent transcript this session holds.**

Every arm this project has run receives the parent repository's `AGENTS.md` — *"Read
`.bemyagent/docs/00-ai-rules.md` before every task."* — and the session's memory index, delivered
as an `instructions` attachment and rendered into the arm's own request under *"IMPORTANT: These
instructions OVERRIDE any default behavior and you MUST follow them exactly as written."*
**118 arm launches, 118 carrying it.** 20.9 recorded that no arm opened `AGENTS.md`, which is
true, and left the wrong impression: the arms opened the file it points at.

**58 of 118 arm launches called `<repo>/.bemyagent/docs/00-ai-rules.md`
by absolute path** — the real file, 107 lines, the shipped protocol in full. **57 of the 58 did it
at their first or second tool call**, before reading the tree they were given, and all 47 that read
their own copy at all read the parent's first. **13 of 25 independent VERIFY agents** did the same.
Nothing else leaked: **no arm, of 118, ever opened `05-decisions-and-issues.md` or
`06-implementation-plan.md`** — one research agent quoted the path of the first inside a report,
and that is the only hit in 174 agents.

So **"no protocol file of any kind" has never been the condition it was labelled** — 20.2, 20.3,
20.8, 20.9 — and in a clause round the exposure is worse than a label defect: the arm reads the
**unmutated** text first. 14.13 (6/6) and 15.4 (8/8) are the two rounds whose mutated file an arm
could also fetch clause-free from the parent; 19.2a's q39 and 18.2's q5 each read the parent
`BEMYAGENT.md` and lose their condition outright. 14.15, 18.3, 19.5, 20.5 and 20.7 are 0/30 — the
one protocol change in this window is not exposed.

The census is only as wide as its matcher. The first pass recognised two arm-naming conventions
out of six and dropped nine trees without saying so; the independent VERIFY found them, and the
count moved from 49 to 58. **Key an audit of arms on the whole path, never on the arm's name** —
`r182/q1` and `r182b/q1` are different arms.

Three consequences, and they are not symmetric:

- **A benefit reading is understated.** The contamination pushes the control toward the protocol's
  behaviour, so a gap measured in the protocol's favour is a floor. 20.8's 5/6 against 0/9 survives.
- **A harm reading is inflated**, and harm readings are the ones this record trusts most (question
  2). Every rejection shaped *the clause causes damage* was taken against a control that had been
  told a protocol exists.
- **A clause round where the arms read the parent is measuring a weakened manipulation.** Its null
  is a floor on the clause's effect, not a reading of it.

**And the exposure bought nothing.** The twelve arms given no protocol file produced **0 TTEV
artifacts and 0 `PROTOCOL_CHECK`s**, nine of them after reading all 107 lines. The text in context
is not the mechanism; the protocol installed as the tree's governing file is. That is the most
useful thing this defect produced, and it was free.

**It was called unfixable from inside the session, and that was a guess.** The injection is keyed
to the session's primary working directory, not to the arm's: the arms already run from a scratchpad
outside the repository and receive it anyway. The conclusion drawn from that — *a clean control
needs a session whose project directory is not this repository, and this session cannot have one* —
was reasoning about the harness, not a measurement of it, and it is **false as stated.**

**A clean arm is buildable today, by the CLI rather than the Agent tool.** `command claude -p`,
launched with its working directory inside the arm's own tree, receives **no project instructions at
all**. Measured 2026-11-09 on an arm-shaped tree holding one file, by reading the probe's own
transcript: `"type":"instructions"` **0 records**, `bemyagent/AGENTS.md` **0**, `00-ai-rules.md`
**0**, the OVERRIDE header **0**. The three `MEMORY.md` hits are the memory tool's own boilerplate
in the system prompt, and the probe's `memory/` directory was created empty.

Three things about that launcher are load-bearing, and each was a failure before it was a finding:
`command claude`, because a shell function may wrap `claude` with a throwaway config dir that has no
auth and no readable transcript; a pinned `CLAUDE_CONFIG_DIR`, because the certificate has to be
able to find the transcript afterwards; and an explicit `--allowedTools` roster, because in `-p`
mode an unpermitted call is **denied, not queued**, and an arm that cannot run `npm test` floors
every metric for a reason that has nothing to do with the condition.

**The swap is not free, and the confound has to be declared.** Changing the launcher removes the
injection *and* the whole Agent-tool surface — a different system prompt, no coordinator, a
different tool roster. A clean round therefore cannot attribute anything to the injection alone; it
can only show whether the published readings **survive** where the control is verifiably clean. And
the clean control must be run **beside a protocol side on the same launcher**: a control reading 0
on a launcher never yet observed to produce anything else is a floor, not a null.

**Certified on six arms, 2026-11-10 (20.11).** The launcher above held on a real round: the three
no-protocol arms carry **no instruction record, no parent-repository path and no OVERRIDE header**
in their own transcripts, and the same reader, in the same pass, **did** find each protocol arm's
own `CLAUDE.md` — the positive control that turns the zeros into a reading. An independent verifier
re-ran it to the same bytes. **Clean controls now exist.** What 20.11 could not do is compare
anything against them: its protocol side was sent the wrong prompt (above), so no published
reading has yet been reproduced on this launcher.

**Until a round compares against a certified control, no verdict here may claim an uncontaminated
one** — say which direction the contamination pushes the reading instead.

### Check isolation at the boundary the agent can reach, not the one you built

19.2a fixed this criterion before launch and ticked it: *"The condition cannot leak through the
rules file — PASS, `00-ai-rules.md` byte-identical across sides (`cmp`)."* The `cmp` was real and
the reasoning was sound. It compared **arm against arm** — the boundary the setup script builds —
while the leak came in by absolute path from a repository the script never mentions, at the arm's
first tool call, in the same round that wrote the criterion down.

An arm is not confined to its tree. It holds a shell, the harness hands it the parent project's
instruction file, and anything reachable from that path is inside the experiment. Before a round
runs, ask what the arm can **reach**, not what the setup **wrote**: a `cmp` between conditions
proves the conditions differ, never that nothing else was available.

### A round whose evidence lives only in the scratchpad is unauditable

Milestone 15.3 scored six arms from disk, wrote the verdict, and the next day the scratchpad was
gone — arms, `setup15.py` (how the condition delta was built) and `score15.py` (the criteria as
code). The verdict survived; the evidence behind it did not. A grep run against the vanished
path came back empty and was one step from being reported as *"0/6 arms wrote `04_verify.md`"*,
contradicting the scorer's own output from the day before.

This is 14.6's caveat recurring, so it is systemic, not an incident. **Before a round is called
done, the scorer script and its raw output are copied into `work/<N>/<N.Y>/`**, which is
tracked. The arm trees are too large to keep; the scorer and its output are not, and together
they are what makes a verdict re-checkable.

Note what this is: our own measuring apparatus failing the rule the protocol imposes on
everything else — evidence that evaporates is evidence hidden from the person who has to trust
the verdict.

**The scratchpad also decays while a session is still open.** At 2026-11-11 00:00 the 20.2 arm
trees, five days old, lost most of their files — app sources and most of `.git` — while trees
from 11-08 onward were untouched (inferred: a periodic `/tmp` cleaner; not verified). A scorer
that walks every arm it knows crashed on them. Score the arms a round compares, by name, and
do not plan a later round on an old tree without checking it is still whole.
