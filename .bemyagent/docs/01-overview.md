# Overview: BEMYAGENT

BEMYAGENT is a lightweight, markdown-based bootstrapping protocol designed to initialize AI-assisted software projects. It provides a standardized directory structure and a rigid workflow (Fractal TTEV & Lazy Loading) to prevent AI context bloat, reduce token consumption, and maintain deep historical logs of executions without confusing the AI.

## ⚠️ Self-Referential Project

This repository IS the source code of the BEMYAGENT protocol. The protocol governs its own development (dogfooding).

**Key distinction:**
- **`/BEMYAGENT.md`** — The **source template** (SRC). This is the distributable artifact: the prompt users drop into their repos. It MUST be updated whenever `00-ai-rules.md` or the bootstrap workflow evolves. Treat it as production code, not documentation.
- **`/.bemyagent/`** — The **live instance** of BMA governing this project. Same protocol, applied to itself.

**Rule:** Never delete `BEMYAGENT.md`. When integrating a draft or changing a rule in `00-ai-rules.md`, always propagate the change to the corresponding section in `BEMYAGENT.md`.

## Domain Glossary
> Shared vocabulary. Use these terms verbatim in docs, tasks, and chat — never re-explain them.

| Term | Meaning |
|---|---|
| **TTEV** | The four-phase task cycle: Think → Task → Execute → Verify (`01`–`04` files in a work leaf). |
| **HTN** | Hierarchical Task Network — the `work/<N>/<N.Y>/` tree mirroring `06-implementation-plan.md`. |
| **Leaf / branch** | A leaf holds TTEV files; a branch holds only subfolders. Never both. |
| **CDM** | Contextual DNA Mapping — the Drift / Validation / Pivot criteria embedded in `02_tasks.md`. |
| **Ceremony** | The weight of a task: Micro (one `micro.log` line), Standard (TTEV + Validation), Heavy (TTEV + full CDM). |
| **Write Gate** | The `PROTOCOL_CHECK:` output required before creating or modifying any file in `docs/` or `work/`. |
| **Symbiotic Validation** | The VERIFY phase: self-evaluation against CDM criteria yielding PASS / PASS_WITH_CAVEATS / FAIL. |
| **Context Saturation Check** | The THINK entry gate — 2+ unknowns means stop and ask. |
| **Lazy Loading** | Never read `decisions/`, `specs/`, `drafts/` during restore; load on demand via the Routing Table. |
| **Context Slicing** | Grep-then-expand instead of full-reading any file over `contextSlicingThreshold` lines. |
| **Vertical slice** | A leaf cutting a complete path through every layer it touches, verifiable alone. Opposite: horizontal, layer-at-a-time. |
| **Dynamic Pivot** | Stop-and-rethink once obstacles exceed `obstacleThreshold`. |
| **Pacing** | `interactiveMode`: SEAMLESS (autonomous) vs INTERACTIVE (human gates after THINK and VERIFY). |
| **Self-Registration** | Writing the sentinel line into the tool's native rule file (`AGENTS.md`, `CLAUDE.md`, …). |
| **SRC vs live instance** | `/BEMYAGENT.md` is the distributable template; `/.bemyagent/` is this repo's own instance. |

## Success Metrics (Measurable KPIs)
- Token consumption per task (reduction)
- Context window drift and hallucinations (reduction)
- Human orientation time when returning to a project (reduction)

## Repository Structure
- `/BEMYAGENT.md` — Source template (SRC). The distributable bootstrap prompt.
- `/README.md` — Human-facing project description.
- `/.bemyagent/docs/` — Permanent knowledge (architecture, rules, decisions).
- `/.bemyagent/work/` — Volatile memory (execution traces, task logs).
- `/harness/` — Test environment for measuring rules. NOT part of the distributed protocol; never referenced by `BEMYAGENT.md`.
- `/site/` — Generated site for bemyagent.md (built by CI).

## Quick Start Commands
- Drop `BEMYAGENT.md` in your repo and ask the AI: "Read BEMYAGENT.md and execute the bootstrap".

## Environment Variables
*(None for this documentation project)*

## Ports
*(None for this documentation project)*
