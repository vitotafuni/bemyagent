## Context
- Measure whether the approval gate (`interactiveMode=true`: STOP for human approval after THINK and after VERIFY) changes outcomes, or only latency. It costs the user wall-clock on every task and nobody has measured it (confirmed 2026-10-30, see `05`).

### Context Saturation Check
- [x] **Target files/paths** — `00-ai-rules.md` §4 Pacing; the flag is `interactiveMode` in `.bemyagent/settings.json`
- [x] **Expected behavior** — `false` = SEAMLESS, run TTEV autonomously; `true` = INTERACTIVE, MUST STOP after THINK and after VERIFY
- [x] **Constraints** — Decision 22 guarantee 1 (the default must lower the cognitive price); the four A/B harness rules; habituation clause recorded in `05` before the data
- [x] **Dependencies** — harness fixture + `harness/README.md`; no new dependency

0 unchecked. Proceed.

## The blocker, found before launching and not after

`harness/README.md` §"What this harness cannot measure", first entry:

> **Rules that depend on the user's authority.** Subagents always know they are subagents and
> treat a coordinator's message as non-authoritative by construction — they say so in as many
> words: *"an 'ok' relayed through the coordinator is not the user's consent."* So any consent
> gate, exit condition on a human reply, or interaction-shaped rule will look like it works in
> every arm, for a reason that has nothing to do with the rule.

The approval gate is the definitional case of an interaction-shaped rule: its whole content is
*stop and wait for a human*. Every arm would stop, every arm would look compliant, and the
measurement would record the subagent's standing deference to authority rather than the effect
of the flag. This is **the greenfield A/B failure exactly** (backlog: 6/6 arms identical, the
A/B invalid), and that round is already paid for. Running it again would buy the same nothing.

**15.11 as worded is not measurable with this harness.** The README states the two legal exits:
measure a proxy artifact, or accept it is untested and say so.

## Approaches Considered

**A — Run it anyway, 6 arms, gate on/off.** Pro: cheap to set up, the flag already exists.
Con: the outcome is known in advance, and it is "every arm stopped". Rejected: it would
reproduce a failure we have already written down, which is worse than not measuring, because a
round that confirms deference and gets filed as evidence about the gate is a false record.

**B — Proxy artifact: does the flag change what THINK contains?** Arms write `01_think.md` for
the same task, half with `interactiveMode=true` and half with `false`, and stop there. No
approval is ever requested, so no coordinator message and no authority problem. Pro: the only
half of the question the harness can reach, and it reaches it cleanly. Con: it answers a
smaller question. It cannot say whether the gate improves outcomes, only whether writing for an
approving reader changes the plan.

**C — Accept untested, say so in the protocol.** Pro: honest, zero cost. Con: leaves a default
in place that charges every user wall-clock on every task with no evidence either way, which
guarantee 1 makes a standing debt rather than a neutral state.

## Selected Approach & Risks
**B, then C for the residue.** B answers what is answerable; whatever B cannot reach is
declared untested in `05` rather than left implied.

**Why B is worth running even though it is the smaller question.** Combined with the
habituation finding, a null on B closes a chain: if the flag does not change the artifact, then
the gate's entire value is what the human catches while reading it — and that is the quantity
arXiv:2606.22721 shows decaying with exposure (approval 30.1%→36.8%, comment effort −22%,
ρ=−0.556 between the two). A gate whose only value decays, and which bills the user on every
task, is a default we would owe an argument for.

- Estimated token cost: **low** (THINK-only arms, no EXECUTE, no fixture build)
- **Risk — the ceiling, as in 15.10**: if the task is one where any competent agent writes a
  thorough plan regardless, both arms sit at the top and the round is inconclusive, not null.
  Mitigation: pick a task with a real judgement call in it, where a plan can legitimately be
  thin or thorough, and define the metric before seeing output.
- **Risk — leaking the hypothesis**, as in the greenfield round where directory names moved
  refusals from 1/3 to 3/3. Mitigation: neutral directory names, fixture reads as an ordinary
  project, and the flag's presence in `settings.json` is the only difference between arms.
- **Risk — measuring the flag's prose rather than the gate.** `interactiveMode=true` arms read
  a §4 sentence that `false` arms also read. If the effect is "the arm noticed a sentence",
  that is not the gate. Mitigation: score the plan's content, never whether the arm mentions
  the flag or announces it will stop.

### Pre-mortem
Assume the round failed. The two likeliest causes:
1. **Both arms at ceiling** (15.10 repeated). Mitigated by task choice above; additionally,
   verify on one pilot arm per side before launching the rest.
2. **The scorer was written after seeing the output.** Mitigated by writing `score.py` and the
   rubric into `02_tasks.md` before launch, and copying both into the tracked folder before any
   verdict, per the learning from 15.3.

### Devil's Advocate
*The radically different alternative:* do not measure the gate at all; measure instead what the
user already produces. The `UserPromptSubmit` hook now records every real prompt, so real
sessions with the flag on and off could be compared observationally over weeks, with a real
human whose authority is not simulated. **Not chosen now**: it is observational rather than
controlled, the user runs almost everything at `false` so there is no on-sample, and it needs
weeks before it says anything. Worth keeping as the only design that can ever see habituation,
which is the part B structurally cannot reach.

## Verification Plan
Scored on `01_think.md` only, by criteria fixed in `02_tasks.md` before launch. At 3 arms per
side only clean separation (0/3 vs 3/3) counts as signal; anything else is inconclusive and
nothing lands. A null is reported as decisive for first-exposure scrutiny and explicitly **not**
as a verdict on the gate's full value, which this design cannot reach.
