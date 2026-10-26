# VERIFY — 15.12 Kiro artifact comparison

Verdict: **PASS_WITH_CAVEATS.** The comparison ran and answered the question it was designed to
ask, plus one it was not. The central caveat is that **Kiro's spec flow was never reachable**, so
nothing here measures it.

## What was run

Kiro CLI 2.33.1, model pinned `claude-sonnet-4.5`, in a clean copy of the harness fixture with
no BMA present. Task text byte-identical to the one given to the six arms in
`work/15/15.10/arms/`. Two modes, context cleared between them, fixture restored between them.
Total cost **1.85 credits of 50**.

## Finding 1 — the clarifying behaviour is the harness, not the model

| mode · model (same input, cleared context, restored fixture) | clarifying questions |
|---|---|
| Plan · `claude-sonnet-4.5` | **3**, reproduced 2 runs of 2 |
| Plan · `minimax-m2.5` — **different lab, different family** | **3** |
| default · `claude-sonnet-4.5` | **0** — reads the files, writes the code |

Two model families produce **exactly three**, in the same `a/b` structured format, with the same
*"(Use the chat to answer any subset…)"* footer. That is not a model disposition; it is a rule
being executed.

Asked why, it quoted its own instruction: *"The planning workflow requires me to 'ask AT MOST
THREE structured questions per turn' during requirements gathering, **even for straightforward
tasks**."* And, unprompted: *"For this specific task, I would normally pick sensible defaults
(1b, 2b, 3a) and note them as assumptions."*

Self-report alone would be weak; the mode contrast is behavioural and confirms it. **And the second model
caught the rule overriding it, in its own visible reasoning**: MiniMax wrote *"This is a
straightforward integration task… **Actually, this is fairly well-defined.** Let me ask some
clarifying questions…"* — it judged the task well-defined and asked anyway. That sentence is the
strongest single piece of evidence in this comparison. **A harness
rule overrides the model's own judgement** — and that judgement, left alone, is BMA's §4 rule
verbatim (*0-1 unknown → state the assumption, continue*). Its default `1b`
(`{playerId, displayName}`) is what **6/6 of our arms chose** independently.

## Finding 2 — no artifacts, in either mode, verified on disk

Neither run produced a `.kiro/` directory, a markdown file, a spec, or a decision record. After
the Plan run the project folder was byte-identical to the restored fixture. The plan existed
**only as chat**.

The reasoning is not lost — it is consolidated in `~/.kiro/sessions/cli/*.jsonl`, 112 KB of
transcript. **Outside the project, machine-local, unversioned, unreadable by a teammate or
another tool, undiffable.**

That is this protocol's founding claim confirmed from outside: *conversation is not storage*
(Decision 21). Kiro keeps the conversation and still loses everything that makes an artifact
useful. It is also FEDERATION issue #7 — *a rule that lives only in the tool's private memory is
invisible elsewhere* — observed in a shipped AWS product rather than argued.

**Be fair about why.** Kiro is a harness and can own state; a protocol has no harness, so the
repo must carry it. Both choices are coherent for what they are. The consequence is still
concrete: Kiro's reasoning is not portable, not reviewable, not versioned.

| | code + tests | reasoning artifacts |
|---|---|---|
| Kiro, both modes | 134 lines | **0** |
| BMA, six arms | equivalent | 123 lines of TTEV, plus `docs/01`–`06` and `AGENTS.md` each |

## Finding 3 — their gates block, ours only speak

Kiro stopped three times for approval (file write, shell run) with four-level granularity —
specific path / directory / entire tool, and exact command / partial / base / entire tool. Our
Write Gate emits a `PROTOCOL_CHECK:` line, which is a **self-report and can prevent nothing**.
Same distinction the 2026-10-20 survey drew about `skills-constitution`'s `--strict`, and **a
markdown file cannot close it by construction.**

## Finding 4 — scope, when nobody answers

Told *"no further information is available, proceed with the task exactly as stated"*, Kiro's plan
came back with **four tasks**, including the heartbeat endpoint and a periodic sweep it had just
asked about. Our arms, on the same input, built the two endpoints asked for and recorded *no
heartbeat / stale sessions still listed* as known limitations in `05`. **Kiro widened the scope;
BMA narrowed it and wrote down what it left out.** One data point, not a measurement.

## Caveats, and the first one governs the rest

1. **The spec flow was never tested, because it is not in the CLI.** The full command list of
   v2.33.1 contains no `spec`; `requirements.md`/`design.md`/`tasks.md` as documented on kiro.dev
   is an **IDE feature**. So nothing here speaks to Kiro's spec-driven capability. It also means
   that capability is **not scriptable or automatable from a terminal** — which is itself worth
   knowing, since ours runs anywhere an agent reads markdown.
2. **Default mode is Kiro's unstructured agent** — the fair analogue of BMA with no protocol
   at all. "Kiro default produces no artifacts" is unsurprising and nearly uninformative; the
   Plan-mode result is the one that carries weight.
3. **No outcome comparison was attempted**, correctly: that is the confounded question this task
   was re-scoped away from. Nothing here says whose code is better. Both passed their tests.
4. **One task, one model, one session.** `claude-sonnet-4.5` on their side; our arms ran a
   different Claude version, so a model-level match was not available.

## Recommendation

Record the four findings. **Do not install the IDE on this result** — reaching the spec flow
needs a GUI, cannot be driven headlessly, and would answer a question about a product we have
already established is not a competitor. Revisit only if the spec triple appears in the CLI.

The finding worth carrying into the protocol is **Finding 3**: our write gate cannot block, and
we have always known that without writing it down.


## Finding 5 — the plan itself, extracted and compared

Kiro's Plan output was lifted verbatim out of `~/.kiro/sessions/cli/*.jsonl` rather than asked
for again: regenerating it would have produced *"a model writing spec files on request"*, which
is a different thing from the Plan agent's output and must not be labelled as it. Saved to
`kiro/plan-mode-output.md`, 73 lines.

**It is a better plan document than any single arm produced, and that should be said plainly.**

| | Kiro Plan | BMA arm |
|---|---|---|
| sections | Problem Statement · Requirements · Background · Proposed Solution · Task Breakdown | Context · Saturation Check · checklist |
| per task | Objective · Implementation · Tests · **Demo** | `Delivers:` |
| explicit assumptions | 0 | 2 of 6 arms |
| pre-mortem | 0 | 3 of 6 arms |
| covers | planning only | plan → execute → verify |
| lives | **chat only** | on disk, in the repo |

Their *Demo* per task is our `Delivers:` under another name — a fourth independent convergence.
Their `Background` and `Proposed Solution` have **no counterpart in `01_think.md`**, which is a
real gap on our side, and the same gap the Kiro survey already flagged as the missing
`design.md`. Against that, half our arms ran a pre-mortem and a third wrote explicit assumptions,
neither of which appears anywhere in Kiro's plan.

**`Drift` and `Pivot` are absent from both — correctly.** Our arms sized the task Standard, and
§4 gives Standard `✅ Validation` only. Not a finding.

The honest summary: **Kiro plans better in one document; BMA records more of the work and keeps
it.** One artifact in a transcript outside the repo versus a chain that survives on disk. The
structural advantage is ours; the planning-document craft is theirs.
