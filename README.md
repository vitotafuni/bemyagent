# BEMYAGENT.md

> **Mission**: Save tokens for the machine. Save orientation for the human.

📖 **Website**: [bemyagent.md](https://bemyagent.md)

BEMYAGENT.md is a lightweight, self-bootstrapping protocol that bridges the gap between humans and AI agents. Instead of forcing alignment through code reviews or rigid procedures, it creates a shared workspace where the machine thinks in structured files and the human validates at the right level of abstraction.

## The Problem

When working with AI agents on complex projects, three things break down:

1. **Context bloat** — The agent reads thousands of irrelevant lines, inflating costs and slowing down.
2. **Silent drift** — The agent executes a task but drifts from the original intent. Nobody catches it until it's too late.
3. **Validation fatigue** — The human must review every line of output because there's no structured checkpoint between "done" and "delivered".

## The Solution: TTEV Workflow

BEMYAGENT.md provides a single markdown file (`BEMYAGENT.md`) that acts as a bootstrap prompt. When fed to an AI assistant, it generates a structured `.bemyagent/` workspace:

- **`.bemyagent/docs/`** — Permanent project memory (architecture, code map, tech stack, decisions).
- **`.bemyagent/work/`** — Tactical, volatile memory organized as a Hierarchical Task Network (HTN).

### Core Concepts

| Concept | What it does |
|---|---|
| **TTEV Workflow** | Think → Task → Execute → Verify. A four-phase cycle where the agent strategizes, plans atomic steps, executes, and self-validates before notifying the human. |
| **Lazy Loading** | The agent never reads specs, drafts, or decisions during context restoration unless the current task explicitly requires them. Saves tokens by default. |
| **Fractal Decomposition (HTN)** | If a task is too large, the agent decomposes it into sub-tasks (e.g., `work/1/1.1/`, `work/1/1.2/`). Each leaf node gets its own TTEV cycle. |
| **Context Saturation Check** | Before executing, the agent verifies it has enough context (target files, expected behavior, constraints, dependencies). If too much is unclear, it asks instead of guessing. |
| **Contextual DNA Mapping (CDM)** | During planning, the agent embeds validation criteria directly into each task — scaled by complexity, in three tiers: Micro tasks get none, Standard tasks get Validation criteria, and Heavy tasks get the full set — Drift sensors, Validation criteria and Pivot triggers. |
| **Symbiotic Validation** | After execution, the agent evaluates its own output against the CDM criteria and produces a verdict (PASS / PASS\_WITH\_CAVEATS / FAIL) before presenting results. The human validates the *sense*, the agent has already validated the *form*. |
| **Self-Registration** | The agent configures the project's native rule files (`.cursorrules`, `AGENTS.md`, etc.) to read `00-ai-rules.md` before every task. |

### Pacing Modes

The human controls how much autonomy the agent has:

- **SEAMLESS** — The agent runs TTEV automatically. It only stops if verification finds issues.
- **INTERACTIVE** — The agent pauses after THINK (plan approval) and after VERIFY (result approval). Two human gates.

Independently of pacing, `autoModelSwitching` lets the agent use a stronger model for THINK and VERIFY and cheaper tiers for mechanical EXECUTE steps. It composes with either mode rather than being a third one.

## Usage

1. Drop `BEMYAGENT.md` into the root of your project.
2. Ask your AI assistant to read the file and execute its instructions.
3. The AI generates the `.bemyagent/` directory structure and templates.
4. Delete `BEMYAGENT.md` and start a fresh chat session (the bootstrap context is no longer needed).

That's it. From this point on, the agent reads `.bemyagent/docs/00-ai-rules.md` before every task and knows how to operate.

## Human-invoked routines

These live here rather than in `00-ai-rules.md` so they cost nothing at session restore —
they are for you to run, not for the agent to carry in context every turn.

### Monthly audit

Every procedural rule in the protocol forces an artifact to *exist*; none checks that it is
*true*. This prompt is the reconciliation pass. Paste it into a session roughly monthly:

> "Compare `03-code-map.md` vs the real file structure; report drift. Check `01-overview.md`
> env vars vs actual config. Verify `.gitignore` coverage. Check test coverage vs recent
> changes. List recent decisions missing from `05-decisions-and-issues.md`. Flag placeholder
> sections and language inconsistencies in docs/."

### Version-control conventions

`.bemyagent/` is tracked in git by default. Teams preferring a clean VCS history may
`.gitignore` `work/` — the audit trail is kept locally and lost in VCS.

### Multi-agent dispatch

In the worktree workflow (`00-ai-rules.md` §8) the human dispatches one session per worktree,
merges via PR, and resolves conflicts. There is no automated orchestrator by design.

## How It Works (The Files)

```
.bemyagent/
├── docs/                          # Permanent project memory
│   ├── 00-ai-rules.md             # The protocol itself (agent reads this first)
│   ├── 01-overview.md             # What the project does, quick start
│   ├── 02-architecture.md         # System diagram, component roles
│   ├── 03-code-map.md             # Routes, key functions, data schemas
│   ├── 04-tech-stack.md           # Technologies, versions, external services
│   ├── 05-decisions-and-issues.md # Decision log and known issues
│   ├── 06-implementation-plan.md  # Milestones and task index
│   ├── decisions/                 # Complex ADRs (loaded on-demand)
│   ├── specs/                     # Feature specifications (loaded on-demand)
│   └── drafts/                    # Unscoped ideas (loaded on-demand)
└── work/                          # Tactical memory (volatile)
    └── {milestone}/{task}/        # One folder per atomic task
        ├── 01_think.md            # Strategy & context check
        ├── 02_tasks.md            # Checklist with CDM criteria
        ├── 03_execute.log         # What happened (retrospective)
        └── 04_verify.md           # Self-validation report
```

## `harness/` — measuring whether a rule actually works

**Not part of the protocol.** `BEMYAGENT.md` is still the only thing you copy into
your project; `harness/` is never referenced by it and never lands in your repo.
It is the test environment used to develop the protocol — and it is generic
enough to reuse.

The problem it solves: a rule written for an AI agent is a *claim* about
behaviour, and reasoning about that claim predicts the outcome badly. Across
three milestones here, most proposed rules did not survive measurement — several
turned out inert, and one made the agent measurably worse before it was reworked.

**The method** — one variable, two arms, N=3 each:

1. Copy `fixture/` into 6 isolated directories.
2. Three get your current rules; three get the same rules plus the candidate.
   Diff the two and confirm the only difference is the rule.
3. Run one agent per directory, same prompt, same model, in parallel.
4. Score the **artifact** the rule should produce — not a downstream proxy like
   token count, which is noisy enough to produce false positives.

**What's inside:**

- `fixture/` — a small tic-tac-toe app (Express + sqlite + vanilla client, ~120
  lines) with real layer separation: schema → store → API → client → tests. It is
  deliberately layered so a feature request cuts through everything at once, which
  is what makes decomposition and scoping rules observable. Swap in your own
  codebase if you prefer.
- `tokens.py` — per-arm cost from agent session transcripts, cache-weighted
  (raw token sums mislead: cache reads are ~10× cheaper than fresh input).
- `README.md` — the method, plus what the harness **cannot** measure and the
  traps that cost real experiment rounds: consent-shaped rules are unmeasurable
  because subagents never treat a coordinator as the user; directory names leak
  the hypothesis to the agents; a fixture that advertises itself as a test
  changes behaviour; a planted defect that doesn't actually exist turns every
  arm into a different experiment.

Useful for anyone tuning agent instructions — prompts, skills, rule files — who
wants evidence instead of intuition.

## Contributing & Dogfooding

This repository uses the BEMYAGENT.md protocol to develop itself. The `.bemyagent/` directory contains the live workspace where the protocol is planned, documented, and evolved — using its own rules.

Explore `.bemyagent/work/` to see real TTEV cycles, CDM annotations, and verification reports in action.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
