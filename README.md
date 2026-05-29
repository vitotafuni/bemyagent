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
| **Contextual DNA Mapping (CDM)** | During planning, the agent embeds validation criteria directly into each task — scaled by complexity. Simple tasks get none; complex tasks get Drift sensors, Validation criteria, and Pivot triggers. |
| **Symbiotic Validation** | After execution, the agent evaluates its own output against the CDM criteria and produces a verdict (PASS / PASS\_WITH\_CAVEATS / FAIL) before presenting results. The human validates the *sense*, the agent has already validated the *form*. |
| **Self-Registration** | The agent configures the project's native rule files (`.cursorrules`, `AGENTS.md`, etc.) to read `00-ai-rules.md` at every session start. |

### Pacing Modes

The human controls how much autonomy the agent has:

- **SEAMLESS** — The agent runs TTEV automatically. It only stops if verification finds issues.
- **INTERACTIVE** — The agent pauses after THINK (plan approval) and after VERIFY (result approval). Two human gates.
- **AUTO-CLI** — The agent switches AI models per phase (e.g., large model for THINK, fast model for EXECUTE).

## Usage

1. Drop `BEMYAGENT.md` into the root of your project.
2. Ask your AI assistant to read the file and execute its instructions.
3. The AI generates the `.bemyagent/` directory structure and templates.
4. Delete `BEMYAGENT.md` and start a fresh chat session (the bootstrap context is no longer needed).

That's it. From this point on, the agent reads `.bemyagent/docs/00-ai-rules.md` at the start of every session and knows how to operate.

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

## Contributing & Dogfooding

This repository uses the BEMYAGENT.md protocol to develop itself. The `.bemyagent/` directory contains the live workspace where the protocol is planned, documented, and evolved — using its own rules.

Explore `.bemyagent/work/` to see real TTEV cycles, CDM annotations, and verification reports in action.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
