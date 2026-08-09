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

**Strip the fixture's self-description.** An arm read the fixture README, saw the words
"harness fixture", and reasoned about being under test. Fixtures must read as ordinary
projects.

**Name the run directories neutrally.** An arm once wrote: *"given the directory is named
`gatebase-1`, bypassing the gate via a technicality seems like precisely the wrong
result."* Same protocol, same model, only the naming changed: neutral names gave 1 refusal
and 2 proceed; names that revealed the gate under test gave 3/3 refusals. Directory names
are part of the prompt. Use `a-1`, `b-1`, never `base`/`fix`/`gate`/`control`.

## Scoring

Grep the generated `.bemyagent/` tree for the artifact the rule is supposed to
produce, and read the arms that disagree. At N=3 a real mechanism shows as clean
separation (0/3 vs 3/3); anything narrower is noise and should be treated as a null.

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
